#!/usr/bin/env python3
"""
Generate LaTeX-based bundle thumbnail PDFs and convert to JPG.

For each bundle type × state combination this script:
  1. Reads the hand-designed template from bundle_thumbnails/<bundle_type>.tex
  2. Replaces INSERT-STATE-NAME-HERE and INSERT-STATE-SLUG-HERE with state values
  3. Writes the per-state .tex into bundle_thumbnails/<bundle_type>/
  4. Compiles with xelatex → PDF (single pass, single page)
  5. Converts the PDF to a 700×700 JPG via pdftoppm (7in at 100 DPI)

All design (layout, cover positions, fonts, colours) lives in the LaTeX
template.  This script only performs string replacement — it never
generates or overwrites design parameters.

Usage:
    # Interactive — prompts for bundle type and state
    python3 scripts/generate_bundle_thumbnail_latex.py

    # Specific bundle + state
    python3 scripts/generate_bundle_thumbnail_latex.py activities_assessments_bundle alabama

    # Specific bundle, all states
    python3 scripts/generate_bundle_thumbnail_latex.py activities_assessments_bundle all

    # All bundles, all states
    python3 scripts/generate_bundle_thumbnail_latex.py all all

Output:
    final_output/bundles/<bundle_type>/<state_slug>_thumbnail_1.jpeg

Requires: xelatex (TeX Live), pdftoppm (poppler)
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple

# ── Resolve workspace ──────────────────────────────────────────────────

def _find_workspace() -> Path:
    """Walk up from this script to find the workspace root."""
    candidate = Path(__file__).resolve().parent
    for _ in range(10):
        if (candidate / "topics_config.yaml").exists() and (candidate / "studyGuide.cls").exists():
            return candidate
        candidate = candidate.parent
    print("ERROR: Could not find workspace root.", file=sys.stderr)
    sys.exit(1)


WORKSPACE = _find_workspace()
sys.path.insert(0, str(WORKSPACE / "scripts"))

from config import (  # noqa: E402
    MAX_WORKERS,
    TEXLIVE_YEAR,
)
from config_loader import load_config  # noqa: E402

# ── Constants ──────────────────────────────────────────────────────────

BUILD_DIR = WORKSPACE / "build" / "bundle_thumbnails"
OUTPUT_BASE = WORKSPACE / "final_output" / "bundles"
TEMPLATE_DIR = WORKSPACE / "bundle_thumbnails"

# DPI for pdftoppm conversion: 7in page × 100 DPI = 700px
PDF_TO_JPG_DPI = 100

# ── Bundle types ───────────────────────────────────────────────────────
# Only used for the interactive menu and validation.
# All design details live in the template .tex files.

BUNDLE_TYPES: List[str] = [
    "practice_tests_bundle",
    "study_practice_bundle",
    "test_prep_bundle",
    "classroom_bundle",
    "activities_assessments_bundle",
    "complete_series_bundle",
]

BUNDLE_DISPLAY_NAMES: Dict[str, str] = {
    "practice_tests_bundle": "Practice Tests Bundle",
    "study_practice_bundle": "Study & Practice Bundle",
    "test_prep_bundle": "Test Prep Bundle",
    "classroom_bundle": "Classroom Bundle",
    "activities_assessments_bundle": "Activities & Assessments Bundle",
    "complete_series_bundle": "Complete Series Bundle",
}


def ensure_bundle_background_exists(bundle_type: str) -> None:
    """Fail fast if the derived bundle background image does not exist."""
    bundle_name = bundle_type.removesuffix("_bundle")
    image_path = WORKSPACE / "images" / "bundle_covers" / f"{bundle_name}.png"
    if not image_path.exists():
        raise FileNotFoundError(
            f"Background image not found: {image_path.relative_to(WORKSPACE)}\n"
            f"Expected bundle thumbnail background at images/bundle_covers/{bundle_name}.png"
        )


def expected_bundle_background_path(bundle_type: str) -> str:
    """Return the required background path for a bundle template."""
    bundle_name = bundle_type.removesuffix("_bundle")
    return f"images/bundle_covers/{bundle_name}.png"


def validate_template_assets(
    bundle_type: str,
    template_path: Path,
    tex_source: str,
    workspace: Path,
) -> None:
    """Fail fast with actionable errors if a template references missing image assets."""
    missing_messages: List[str] = []

    background_match = re.search(r"\\BundleBackground\{([^}]+)\}", tex_source)
    expected_background = expected_bundle_background_path(bundle_type)
    if not background_match:
        missing_messages.append(
            "Template background is missing. "
            f"Set \\BundleBackground{{{expected_background}}} in {template_path.relative_to(workspace)}"
        )
    else:
        actual_background = background_match.group(1)
        if actual_background != expected_background:
            missing_messages.append(
                "Template background path is wrong. "
                f"Set \\BundleBackground{{{expected_background}}} in {template_path.relative_to(workspace)}"
            )

    cover_paths = re.findall(r"\\placeCover\{([^}]+)\}", tex_source)
    for cover_path_text in cover_paths:
        cover_path = workspace / Path(cover_path_text)
        if cover_path.exists():
            continue
        rel_path = cover_path.relative_to(workspace)
        book_type = cover_path.parent.name
        state_slug = cover_path.stem
        missing_messages.append(
            "Cover image missing. "
            f"Put the {book_type} cover JPG for {state_slug} at {rel_path}"
        )

    if missing_messages:
        raise FileNotFoundError("\n".join(missing_messages))


# ── Template-based .tex generation ─────────────────────────────────────

def generate_tex_from_template(
    bundle_type: str,
    state_slug: str,
    state_display_name: str,
) -> str:
    """Read the template .tex and replace state placeholders."""
    template_path = TEMPLATE_DIR / f"{bundle_type}.tex"
    if not template_path.exists():
        raise FileNotFoundError(
            f"Template not found: {template_path.relative_to(WORKSPACE)}\n"
            f"Create it at bundle_thumbnails/{bundle_type}.tex with "
            f"INSERT-STATE-NAME-HERE and INSERT-STATE-SLUG-HERE placeholders."
        )
    source = template_path.read_text(encoding="utf-8")
    source = source.replace("INSERT-STATE-NAME-HERE", state_display_name)
    source = source.replace("INSERT-STATE-SLUG-HERE", state_slug)
    ensure_bundle_background_exists(bundle_type)
    validate_template_assets(bundle_type, template_path, source, WORKSPACE)
    return source


# ── xelatex compilation ───────────────────────────────────────────────

def _texmfcnf_env() -> dict:
    """Return env dict with TEXMFCNF for increased TeX memory."""
    home = Path.home()
    user_web2c = [
        str(home / "Library" / "texmf" / "web2c"),
        str(home / "texmf" / "web2c"),
    ]
    system_dirs = [
        f"/usr/local/texlive/{TEXLIVE_YEAR}",
        f"/usr/local/texlive/{TEXLIVE_YEAR}/texmf-dist/web2c",
    ]
    env = os.environ.copy()
    env["TEXMFCNF"] = ":".join(user_web2c + system_dirs)
    return env


def _has_fatal_error(output: str) -> bool:
    markers = [
        "! Emergency stop.",
        "Fatal error occurred",
        "No output PDF file produced",
        "!  ==> Fatal error occurred",
    ]
    return any(m in output for m in markers)


def compile_thumbnail(
    tex_path: Path,
    workspace: Path,
) -> Tuple[str, bool, str]:
    """Compile a single thumbnail .tex → PDF. Returns (job, ok, message)."""
    job_name = tex_path.stem
    build_dir = BUILD_DIR / job_name
    build_dir.mkdir(parents=True, exist_ok=True)
    rel_build = build_dir.relative_to(workspace)
    rel_tex = tex_path.relative_to(workspace)

    cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        f"-output-directory={rel_build}",
        str(rel_tex),
    ]
    env = _texmfcnf_env()

    try:
        result = subprocess.run(
            cmd,
            cwd=str(workspace),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            env=env,
        )
        combined = (result.stdout or "") + "\n" + (result.stderr or "")
        if result.returncode != 0 and _has_fatal_error(combined):
            tail = " ".join(combined.split()[-150:])
            return (job_name, False, f"xelatex failed: {tail}")
    except subprocess.TimeoutExpired:
        return (job_name, False, "xelatex timed out")

    pdf_path = build_dir / f"{job_name}.pdf"
    if not pdf_path.exists():
        return (job_name, False, f"PDF not found at {pdf_path}")

    return (job_name, True, str(pdf_path))


# ── PDF → JPG conversion ──────────────────────────────────────────────

def convert_pdf_to_jpg(
    pdf_path: Path,
    output_jpg: Path,
) -> bool:
    """Convert a single-page PDF to JPEG using pdftoppm."""
    output_jpg.parent.mkdir(parents=True, exist_ok=True)
    # pdftoppm adds .jpg suffix, so strip it for the -singlefile prefix
    prefix = str(output_jpg).removesuffix(".jpeg").removesuffix(".jpg")
    # Determine suffix expected by pdftoppm
    suffix = ".jpg"
    if str(output_jpg).endswith(".jpeg"):
        suffix = ".jpg"  # pdftoppm always produces .jpg

    cmd = [
        "pdftoppm",
        "-jpeg",
        "-r", str(PDF_TO_JPG_DPI),
        "-singlefile",
        str(pdf_path),
        prefix,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"  pdftoppm error: {result.stderr.strip()}", file=sys.stderr)
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  pdftoppm failed: {e}", file=sys.stderr)
        return False

    # pdftoppm produces <prefix>.jpg — rename to the desired name if needed
    produced = Path(prefix + ".jpg")
    if produced.exists() and produced != output_jpg:
        shutil.move(str(produced), str(output_jpg))
    elif not produced.exists() and not output_jpg.exists():
        print(f"  Warning: expected {produced} not found", file=sys.stderr)
        return False

    return output_jpg.exists()


# ── Extra thumbnails (2-4): covers only, no background ────────────────

PAGE_SIZE = 7.0  # inches — must match geometry in VMfunBundleThumbnail.sty
COVER_ASPECT = 1.5  # height / width for typical book covers


def extract_cover_paths(tex_source: str) -> List[str]:
    """Extract cover image paths from \\placeCover commands in the template."""
    return re.findall(r"\\placeCover\{([^}]+)\}", tex_source)


def split_into_groups(items: List[str], n_groups: int = 3) -> List[List[str]]:
    """Split items into *n_groups* as evenly as possible (front-loaded)."""
    n = len(items)
    groups: List[List[str]] = []
    per = n // n_groups
    rem = n % n_groups
    idx = 0
    for i in range(n_groups):
        size = per + (1 if i < rem else 0)
        groups.append(items[idx : idx + size])
        idx += size
    return groups


def _cover_positions(n: int) -> Tuple[float, float, float]:
    """Return (cover_width, gap, y_offset) for *n* covers in a row."""
    margin = 0.6  # total horizontal margin
    available = PAGE_SIZE - margin
    if n == 1:
        w = 3.0
        gap = 0.0
    else:
        gap = 0.4
        w = (available - (n - 1) * gap) / n
        w = min(w, 3.0)
    h = w * COVER_ASPECT
    max_h = PAGE_SIZE - 1.0
    if h > max_h:
        h = max_h
        w = h / COVER_ASPECT
    y = (PAGE_SIZE - h) / 2
    return (w, gap, y)


def generate_covers_only_tex(cover_paths: List[str]) -> str:
    """Generate a minimal .tex placing covers centred on an orange 7×7 page.

    Uses simple LaTeX flow layout (not TikZ overlay) so that it renders
    correctly in a single xelatex pass.
    """
    n = len(cover_paths)
    if n == 0:
        return ""

    if n == 1:
        cover_h = 6.0
    elif n == 2:
        cover_h = 5.5
    else:
        cover_h = 4.3

    gap = 0.12  # inches between covers

    lines = [
        r"\documentclass[12pt]{article}",
        r"\usepackage[paperwidth=7in, paperheight=7in, margin=0pt]{geometry}",
        r"\usepackage{graphicx}",
        r"\usepackage{xcolor}",
        r"\pagestyle{empty}",
        r"\setlength{\parindent}{0pt}",
        r"\definecolor{bundlethumborange}{HTML}{F2A04B}",
        "",
        r"\begin{document}",
        r"\pagecolor{bundlethumborange}",
        r"\null\vfill",
        r"\centering",
    ]

    img_parts = []
    for path in cover_paths:
        img_parts.append(f"\\includegraphics[height={cover_h:.1f}in]{{{path}}}")

    separator = f"%\n\\hspace{{{gap:.1f}in}}%\n"
    lines.append(r"\makebox[\paperwidth][c]{%")
    lines.append(separator.join(img_parts))
    lines.append(r"}%")
    lines += [
        r"\vfill",
        r"\end{document}",
    ]
    return "\n".join(lines)


# ── Full pipeline for one bundle × state ──────────────────────────────

def process_one(
    bundle_type: str,
    state_slug: str,
    state_display_name: str,
    workspace: Path,
) -> Tuple[str, bool, str]:
    """Read template, replace placeholders, compile, convert to JPG."""
    label = f"{bundle_type}/{state_slug}"

    # 1) Generate .tex from template (thumbnail 1 — main)
    try:
        tex_source = generate_tex_from_template(bundle_type, state_slug, state_display_name)
    except FileNotFoundError as e:
        return (label, False, str(e))

    tex_dir = TEMPLATE_DIR / bundle_type
    tex_dir.mkdir(parents=True, exist_ok=True)
    tex_name = f"{bundle_type}_{state_slug}.tex"
    tex_path = tex_dir / tex_name
    tex_path.write_text(tex_source, encoding="utf-8")

    # 2) Compile thumbnail 1
    job_name, ok, msg = compile_thumbnail(tex_path, workspace)
    if not ok:
        return (label, False, msg)

    pdf_path = Path(msg)

    # 3) Convert thumbnail 1 to JPG
    output_dir = OUTPUT_BASE / bundle_type
    output_jpg = output_dir / f"{state_slug}_thumbnail_1.jpeg"
    if not convert_pdf_to_jpg(pdf_path, output_jpg):
        return (label, False, f"PDF→JPG conversion failed for {pdf_path}")

    jpg_paths = [output_jpg.relative_to(workspace)]

    # 4) Generate extra thumbnails 2-4 (covers only, white background)
    cover_paths = extract_cover_paths(tex_source)
    groups = split_into_groups(cover_paths, 3)

    for thumb_idx, group in enumerate(groups, start=2):
        if not group:
            continue
        extra_tex = generate_covers_only_tex(group)
        extra_name = f"{bundle_type}_{state_slug}_thumb{thumb_idx}.tex"
        extra_path = tex_dir / extra_name
        extra_path.write_text(extra_tex, encoding="utf-8")

        _, ok2, msg2 = compile_thumbnail(extra_path, workspace)
        if ok2:
            extra_jpg = output_dir / f"{state_slug}_thumbnail_{thumb_idx}.jpeg"
            if convert_pdf_to_jpg(Path(msg2), extra_jpg):
                jpg_paths.append(extra_jpg.relative_to(workspace))

    tex_rel = tex_path.relative_to(workspace)
    pdf_rel = pdf_path.relative_to(workspace)
    success_message = (
        f"tex: {tex_rel}\n"
        f"       pdf: {pdf_rel}\n"
        f"       jpg: {', '.join(str(p) for p in jpg_paths)}"
    )
    return (label, True, success_message)


# ── Interactive prompts ────────────────────────────────────────────────

def prompt_bundle_type() -> str:
    keys = BUNDLE_TYPES
    print("\nBundle type:")
    print("-" * 50)
    print(f"  {1:>3}) all  — All bundle types")
    for i, key in enumerate(keys, start=2):
        display = BUNDLE_DISPLAY_NAMES.get(key, key)
        print(f"  {i:>3}) {key}  — {display}")
    print()
    while True:
        raw = input("Enter number or name: ").strip()
        if raw == "1" or raw.lower() == "all":
            return "all"
        if raw in BUNDLE_TYPES:
            return raw
        try:
            idx = int(raw) - 2
            if 0 <= idx < len(keys):
                return keys[idx]
        except ValueError:
            pass
        print("  Invalid choice, try again.")


def prompt_state(all_slugs: List[str]) -> str:
    print("\nState (enter slug like 'texas', or 'all' for all 50):")
    raw = input("  > ").strip().lower()
    if raw == "all":
        return "all"
    if raw in all_slugs:
        return raw
    # Fuzzy match
    matches = [s for s in all_slugs if raw in s]
    if len(matches) == 1:
        return matches[0]
    print(f"  Unknown state '{raw}'. Available: {', '.join(all_slugs[:5])} ...")
    sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate LaTeX bundle thumbnails, compile to PDF, convert to JPG.",
    )
    parser.add_argument("bundle_type", nargs="?", default=None,
                        help="Bundle type key or 'all'")
    parser.add_argument("state", nargs="?", default=None,
                        help="State slug or 'all'")
    parser.add_argument("--jobs", "-j", type=int, default=None,
                        help=f"Max concurrent compilations (default: {MAX_WORKERS})")
    args = parser.parse_args()

    workspace = WORKSPACE
    config = load_config(workspace)
    all_slugs = config.all_state_slugs
    display_names = config.state_display_names

    # Determine bundle type(s)
    if args.bundle_type:
        bundle_arg = args.bundle_type
    else:
        bundle_arg = prompt_bundle_type()

    if bundle_arg == "all":
        bundle_types = BUNDLE_TYPES
    elif bundle_arg in BUNDLE_TYPES:
        bundle_types = [bundle_arg]
    else:
        print(f"Unknown bundle type: {bundle_arg}")
        print(f"Available: {', '.join(BUNDLE_TYPES)}")
        sys.exit(1)

    # Determine state(s)
    if args.state:
        state_arg = args.state.lower()
    else:
        state_arg = prompt_state(all_slugs)

    if state_arg == "all":
        states = all_slugs
    elif state_arg in all_slugs:
        states = [state_arg]
    else:
        print(f"Unknown state: {state_arg}")
        sys.exit(1)

    max_workers = args.jobs or min(MAX_WORKERS, 6)

    # Build work list
    work: List[Tuple[str, str, str]] = []
    for bt in bundle_types:
        for slug in states:
            display = display_names.get(slug, slug.replace("-", " ").title())
            work.append((bt, slug, display))

    total = len(work)
    print(f"\n{'='*60}")
    print(f"  Bundle thumbnails: {len(bundle_types)} type(s) × {len(states)} state(s) = {total} thumbnails")
    print(f"  Concurrency: {max_workers} workers")
    print(f"{'='*60}\n")

    t0 = time.time()
    succeeded = 0
    failed_msgs: List[str] = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(process_one, bt, slug, display, workspace): (bt, slug)
            for bt, slug, display in work
        }
        done = 0
        for future in as_completed(futures):
            done += 1
            bt, slug = futures[future]
            try:
                label, ok, msg = future.result()
            except Exception as exc:
                label = f"{bt}/{slug}"
                ok = False
                msg = str(exc)

            if ok:
                succeeded += 1
                print(f"  [{done}/{total}] ✅ {label}")
                print(f"       {msg}")
            else:
                failed_msgs.append(msg)
                print(f"  [{done}/{total}] ❌ {label}: {msg}")

    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"  Done: {succeeded}/{total} succeeded in {elapsed:.1f}s")
    if failed_msgs:
        print(f"  Failed ({len(failed_msgs)}):")
        for m in failed_msgs:
            print(f"    • {m}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
