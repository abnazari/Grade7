#!/usr/bin/env python3
"""
Generate and compile a bundle preview PDF.

Creates a single .tex file that samples content from each book in a bundle,
compiles it with xelatex (2 passes), and saves the PDF to:

    final_output/bundles/<bundle_type>/<state_slug>_tpt_bundle_preview.pdf

The preview includes:
  - Copyright page
  - One sample topic/content from each book type in the bundle
  - A "Get the Full Book" call-to-action page
  - A diagonal "PREVIEW" watermark on every page

Usage:
    # Interactive mode — prompts for bundle type and state
    python3 scripts/generate_bundle_preview.py

    # Positional arguments
    python3 scripts/generate_bundle_preview.py <bundle_type> <state_slug>

Examples:
    python3 scripts/generate_bundle_preview.py practice_tests_bundle texas
    python3 scripts/generate_bundle_preview.py complete_series_bundle california

Flags:
    --list-bundles    List all bundle types
    --dry-run         Generate .tex but don't compile
    --passes N        Number of xelatex passes (default: 2)
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ── Resolve workspace ──────────────────────────────────────────────────

def _find_workspace() -> Path:
    candidate = Path(__file__).resolve().parent
    for _ in range(10):
        if (candidate / "topics_config.yaml").exists() and (candidate / "studyGuide.cls").exists():
            return candidate
        candidate = candidate.parent
    print("ERROR: Could not find workspace root.", file=sys.stderr)
    sys.exit(1)


WORKSPACE = _find_workspace()
sys.path.insert(0, str(WORKSPACE / "scripts"))

from config_loader import TopicsConfig, load_config  # noqa: E402
from config import GRADE_DISPLAY, GRADE_SLUG  # noqa: E402

# ── Constants ──────────────────────────────────────────────────────────

OUTPUT_DIR = WORKSPACE / "final_output" / "bundles"
BUILD_DIR = WORKSPACE / "build"

MAX_WORKERS: int = int(os.environ.get(
    "MAX_WORKERS", str(max(1, (os.cpu_count() or 4) - 1))
))

# Bundle book types — mirrors get_bundle_facts.py / generate_bundle_thumbnails.py
BUNDLE_BOOK_TYPES: Dict[str, List[str]] = {
    "practice_tests_bundle": [
        "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests",
    ],
    "study_practice_bundle": [
        "study_guide", "workbook",
        "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests",
    ],
    "test_prep_bundle": [
        "in_30_days", "quiz",
        "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests",
    ],
    "classroom_bundle": [
        "step_by_step", "workbook", "quiz", "worksheet",
        "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests",
    ],
    "activities_assessments_bundle": [
        "puzzles", "worksheet", "quiz",
    ],
    "complete_series_bundle": [
        "study_guide", "workbook", "step_by_step", "in_30_days", "quiz",
        "puzzles", "worksheet",
        "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests",
    ],
}

BUNDLE_DISPLAY_NAMES: Dict[str, str] = {
    "practice_tests_bundle": "Practice Tests Bundle",
    "study_practice_bundle": "Study & Practice Bundle",
    "test_prep_bundle": "Test Prep Bundle",
    "classroom_bundle": "Classroom Bundle",
    "activities_assessments_bundle": "Activities & Assessments Bundle",
    "complete_series_bundle": "Complete Series Bundle",
}

# Practice test info: book_type → (num_tests, test_start, test_end)
PRACTICE_TEST_INFO: Dict[str, Tuple[int, int, int]] = {
    "3_practice_tests": (3, 1, 3),
    "5_practice_tests": (5, 4, 8),
    "7_practice_tests": (7, 9, 15),
    "10_practice_tests": (10, 16, 25),
}

# Book type → human-readable display name for chapter headings
BOOK_DISPLAY: Dict[str, str] = {
    "study_guide": "Study Guide",
    "workbook": "Workbook",
    "step_by_step": "Step-by-Step",
    "in_30_days": "Math in 30 Days",
    "quiz": "Quizzes",
    "puzzles": "Puzzles & Brain Teasers",
    "worksheet": "Worksheets",
    "3_practice_tests": "3 Practice Tests",
    "5_practice_tests": "5 Practice Tests",
    "7_practice_tests": "7 Practice Tests",
    "10_practice_tests": "10 Practice Tests",
}

# Book type → topic directory info: (base_dir, modified_dir, additional_dir)
TOPIC_DIRS: Dict[str, Tuple[str, str, str]] = {
    "study_guide": ("topics_study_guide", "topics_study_guide_modified", "topics_study_guide_additional"),
    "workbook": ("topics_workbook", "topics_workbook_modified", "topics_workbook_additional"),
    "step_by_step": ("steps_topics", "steps_topics_modified", "steps_topics_additional"),
    "quiz": ("topics_quiz", "topics_quiz_modified", "topics_quiz_additional"),
    "puzzles": ("topics_puzzles", "topics_puzzles_modified", "topics_puzzles_additional"),
    "worksheet": ("topics_worksheet", "topics_worksheet_modified", "topics_worksheet_additional"),
}


# ============================================================================
# HELPERS
# ============================================================================

def _topic_input(
    topic_id: str,
    modified_set: Set[str],
    additional_set: Set[str],
    config: TopicsConfig,
    base_dir: str,
    modified_dir: str,
    additional_dir: str,
) -> str:
    """Return the \\input{...} line for a single topic."""
    filename = config.topic_filenames[topic_id]
    if topic_id in modified_set:
        return f"\\input{{{modified_dir}/{filename}}}"
    elif topic_id in additional_set:
        return f"\\input{{{additional_dir}/{filename}}}"
    else:
        return f"\\input{{{base_dir}/{filename}}}"


def _first_topic_id(config: TopicsConfig) -> Optional[str]:
    """Return the first topic ID from Chapter 1."""
    if config.chapters and config.chapters[0].topics:
        return config.chapters[0].topics[0].id
    return None


def _first_chapter_title(config: TopicsConfig) -> str:
    """Return the title of Chapter 1."""
    if config.chapters:
        return config.chapters[0].title
    return "Chapter 1"


def _find_first_test(state_slug: str, test_start: int, test_end: int) -> Optional[int]:
    """Find the first available practice test file number."""
    practice_dir = WORKSPACE / "practice_tests" / state_slug
    for i in range(test_start, test_end + 1):
        test_file = practice_dir / f"practice_test_{i:02d}.tex"
        if test_file.exists():
            return i
    return None


def _texmfcnf_env() -> dict:
    """Build environment with extended TEXMFCNF for larger memory limits."""
    home = Path.home()
    user_web2c_dirs = [
        str(home / "Library" / "texmf" / "web2c"),
        str(home / "texmf" / "web2c"),
    ]
    # Auto-detect TeX Live year
    texlive_year = "2025"
    texlive_base = Path("/usr/local/texlive")
    if texlive_base.is_dir():
        years = sorted(
            (d.name for d in texlive_base.iterdir() if d.is_dir() and d.name.isdigit()),
            reverse=True,
        )
        if years:
            texlive_year = years[0]
    system_dirs = [
        f"/usr/local/texlive/{texlive_year}",
        f"/usr/local/texlive/{texlive_year}/texmf-dist/web2c",
    ]
    env = os.environ.copy()
    env["TEXMFCNF"] = ":".join(user_web2c_dirs + system_dirs)
    return env


# ============================================================================
# TEX GENERATION
# ============================================================================

def generate_bundle_preview_tex(
    bundle_type: str,
    state_slug: str,
    config: TopicsConfig,
) -> str:
    """Generate the .tex content for a bundle preview."""
    book_types = BUNDLE_BOOK_TYPES[bundle_type]
    bundle_name = BUNDLE_DISPLAY_NAMES[bundle_type]
    modified_set = set(config.state_modified.get(state_slug, []))
    additional_set = set(config.state_additional.get(state_slug, []))

    has_in_30_days = "in_30_days" in book_types
    has_quiz = "quiz" in book_types
    has_practice_tests = any(bt in PRACTICE_TEST_INFO for bt in book_types)
    pt_book_types = [bt for bt in book_types if bt in PRACTICE_TEST_INFO]
    topic_book_types = [bt for bt in book_types if bt in TOPIC_DIRS]

    first_tid = _first_topic_id(config)
    ch1_title = _first_chapter_title(config)

    lines: List[str] = []

    # ── Preamble ────────────────────────────────────────────────────────
    lines.append(f"% PREVIEW — {bundle_name}")
    lines.append("% Bundle preview — sample content from each book")
    lines.append(r"\documentclass[12pt, fleqn, openany]{studyGuide}")
    lines.append("")
    lines.append("% Line spacing for young readers")
    lines.append(r"\setstretch{1.4}")
    lines.append("")
    lines.append("% PREVIEW watermark on every page")
    lines.append(r"\usepackage{VM_packages/VMfunPreview}")
    lines.append("")

    if has_in_30_days:
        lines.append("% Day environments for in_30_days sample")
        lines.append(r"\usepackage{VM_packages/VMfunDays}")
        lines.append(r"\newcounter{dayNumber}")
        lines.append(r"\setcounter{dayNumber}{0}")
        lines.append("")

    if has_quiz:
        lines.append("% Enable quiz answer collection")
        lines.append(r"\enableQuizAnswers")
        lines.append("")

    if has_practice_tests:
        lines.append("% Enable practice test answer collection")
        lines.append(r"\enablePracticeTestAnswers")
        lines.append("")

    # ── Document begin ──────────────────────────────────────────────────
    lines.append(r"\begin{document}")
    lines.append("")

    # ── Initial pages ───────────────────────────────────────────────────
    lines.append(r"\pagenumbering{roman}")
    lines.append(rf"\renewcommand{{\VMBookTitle}}{{{GRADE_DISPLAY} — {bundle_name}}}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{Preview — Sample Pages from Every Book in This Bundle}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    # ── Sample from each topic-based book type ──────────────────────────
    for bt in topic_book_types:
        display = BOOK_DISPLAY[bt]
        base_dir, mod_dir, add_dir = TOPIC_DIRS[bt]

        lines.append(f"% === Sample from {display} ===")
        lines.append(f"\\chapter{{Sample: {display}}}")
        lines.append("")

        if first_tid:
            if bt == "quiz":
                # Quiz needs quizChapter counter set
                ch_num = config.chapters[0].num if config.chapters else 1
                lines.append(f"\\setcounter{{quizChapter}}{{{ch_num}}}")
            input_line = _topic_input(
                first_tid, modified_set, additional_set, config,
                base_dir, mod_dir, add_dir,
            )
            lines.append(input_line)
        else:
            lines.append("% No topics available for preview")
        lines.append("")

    # ── Sample from in_30_days ──────────────────────────────────────────
    if has_in_30_days and config.in_30_days_config:
        lines.append("% === Sample from Math in 30 Days ===")
        lines.append(r"\chapter{Sample: Math in 30 Days}")
        lines.append("")

        days_config = config.in_30_days_config
        if days_config.days:
            day_entry = days_config.days[0]  # Day 1
            modified_in_day = [t for t in day_entry.topics if t in modified_set]
            if modified_in_day:
                lines.append(f"\\input{{topics_in30days_modified/{day_entry.file}}}")
            else:
                lines.append(f"\\input{{topics_in30days/{day_entry.file}}}")
            lines.append("")

    # ── Sample from practice tests ──────────────────────────────────────
    if pt_book_types:
        # Include one sample test from the first PT book type
        first_pt = pt_book_types[0]
        num_tests, test_start, test_end = PRACTICE_TEST_INFO[first_pt]
        first_test_num = _find_first_test(state_slug, test_start, test_end)

        lines.append("% === Sample Practice Test ===")
        lines.append(r"\chapter{Sample: Practice Test}")
        lines.append("")

        if first_test_num is not None:
            lines.append(f"\\practiceTestPage{{1}}{{{30}}}")
            lines.append("")
            lines.append(f"\\input{{practice_tests/{state_slug}/practice_test_{first_test_num:02d}}}")
            lines.append("")
            lines.append(f"\\testScorePage{{1}}{{{30}}}")
            lines.append("")
        else:
            lines.append("% No practice test files found for preview")
            lines.append("")

    # ── Answer key (if quiz or PT content was included) ─────────────────
    if has_quiz or has_practice_tests:
        lines.append(r"\printAnswerKey")
        lines.append("")

    # ── CTA page ────────────────────────────────────────────────────────
    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# COMPILE
# ============================================================================

def compile_preview(
    tex_path: Path,
    passes: int = 2,
) -> Tuple[bool, str]:
    """Compile a .tex file with xelatex. Returns (success, message)."""
    job_name = tex_path.stem
    build_dir = BUILD_DIR / f"bundle_preview_{job_name}"
    build_dir.mkdir(parents=True, exist_ok=True)

    rel_tex = tex_path.relative_to(WORKSPACE)
    rel_build = build_dir.relative_to(WORKSPACE)

    cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        f"-output-directory={rel_build}",
        str(rel_tex),
    ]

    env = _texmfcnf_env()

    for pass_num in range(1, passes + 1):
        print(f"  xelatex pass {pass_num}/{passes}...")
        try:
            result = subprocess.run(
                cmd,
                cwd=str(WORKSPACE),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                env=env,
            )
            combined = (result.stdout or "") + "\n" + (result.stderr or "")

            # Check for fatal errors
            if result.returncode != 0:
                fatal_patterns = [
                    "Fatal error",
                    "Emergency stop",
                    "No pages of output",
                    "I can't find file",
                    "File not found",
                ]
                for pat in fatal_patterns:
                    if pat.lower() in combined.lower():
                        # Extract last ~20 lines for context
                        tail = "\n".join(combined.strip().splitlines()[-20:])
                        return (False, f"Fatal error on pass {pass_num}: {pat}\n{tail}")
        except FileNotFoundError:
            return (False, "xelatex not found — is TeX Live installed?")

    pdf_path = build_dir / f"{job_name}.pdf"
    if not pdf_path.exists():
        return (False, "PDF not found after compilation")

    return (True, str(pdf_path))


# ============================================================================
# INTERACTIVE PROMPTS
# ============================================================================

def prompt_bundle_type() -> str:
    """Ask the user to pick a bundle type or 'all'. Returns the key."""
    keys = list(BUNDLE_BOOK_TYPES.keys())
    print("\nBundle type:")
    print("-" * 50)
    print(f"  {1:>3}) all  — All bundle types")
    for i, key in enumerate(keys, start=2):
        display = BUNDLE_DISPLAY_NAMES.get(key, key)
        n_books = len(BUNDLE_BOOK_TYPES[key])
        print(f"  {i:>3}) {key}  — {display} ({n_books} books)")
    print()

    menu_size = 1 + len(keys)
    while True:
        try:
            raw = input("Enter number: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            raise SystemExit(1)
        if not raw.isdigit():
            print("  Please enter a number.")
            continue
        num = int(raw)
        if num == 1:
            print("  → all")
            return "all"
        if 2 <= num <= menu_size:
            selected = keys[num - 2]
            print(f"  → {selected}")
            return selected
        print(f"  Invalid choice. Enter 1–{menu_size}.")


def prompt_states(all_state_slugs: List[str]) -> Optional[List[str]]:
    """Ask the user whether to run all states or pick specific ones.

    Returns None for all states, or a list of selected slugs.
    """
    print("\nStates:")
    print("-" * 50)
    print("  1) All 50 states")
    print("  2) Specific state(s)")
    print()

    while True:
        try:
            raw = input("Enter number: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            raise SystemExit(1)
        if raw == "1":
            print("  → all states")
            return None
        if raw == "2":
            break
        print("  Please enter 1 or 2.")

    # Let the user type comma-separated slugs
    print(f"\nAvailable slugs (first 10): {', '.join(all_state_slugs[:10])}, ...")
    while True:
        try:
            raw = input("Enter state slug(s), comma-separated: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            raise SystemExit(1)
        if not raw:
            print("  Please enter at least one state slug.")
            continue
        slugs = [s.strip().lower() for s in raw.split(",")]
        unknown = [s for s in slugs if s not in all_state_slugs]
        if unknown:
            print(f"  Unknown: {', '.join(unknown)}. Try again.")
            continue
        print(f"  → {', '.join(slugs)}")
        return slugs


# ============================================================================
# MAIN
# ============================================================================

def generate_and_compile(
    bundle_type: str,
    state_slug: str,
    passes: int = 2,
    dry_run: bool = False,
) -> Tuple[bool, str]:
    """Generate preview .tex, compile, and save PDF.

    Returns (success, message).
    """
    if bundle_type not in BUNDLE_BOOK_TYPES:
        return (False, f"Unknown bundle type '{bundle_type}'")

    config = load_config(WORKSPACE)

    if state_slug not in config.all_state_slugs:
        return (False, f"Unknown state '{state_slug}'")

    bundle_name = BUNDLE_DISPLAY_NAMES[bundle_type]
    book_count = len(BUNDLE_BOOK_TYPES[bundle_type])
    job_label = f"{bundle_type}/{state_slug}"
    print(f"  > {job_label}: generating .tex ({book_count} books)...")

    # ── Generate .tex ───────────────────────────────────────────────────

    tex_content = generate_bundle_preview_tex(bundle_type, state_slug, config)

    # Write .tex to state_books/<state>/
    state_dir = WORKSPACE / "state_books" / state_slug
    state_dir.mkdir(parents=True, exist_ok=True)
    tex_filename = f"preview_bundle_{bundle_type}_{state_slug}-{GRADE_SLUG}.tex"
    tex_path = state_dir / tex_filename
    tex_path.write_text(tex_content, encoding="utf-8")

    if dry_run:
        return (True, f"{job_label}: dry-run, .tex written")

    # ── Compile ─────────────────────────────────────────────────────────
    success, result_msg = compile_preview(tex_path, passes=passes)

    if not success:
        return (False, f"{job_label}: {result_msg}")

    compiled_pdf = Path(result_msg)

    # ── Copy PDF to final output ─────────────────────────────────────────
    out_dir = OUTPUT_DIR / bundle_type
    out_dir.mkdir(parents=True, exist_ok=True)
    final_pdf_name = f"{state_slug}_tpt_bundle_preview.pdf"
    final_pdf = out_dir / final_pdf_name
    shutil.copy2(compiled_pdf, final_pdf)

    return (True, f"\u2705 {final_pdf.relative_to(WORKSPACE)}")


def main() -> None:
    if len(sys.argv) == 2:
        flag = sys.argv[1]
        if flag == "--list-bundles":
            for b, books in BUNDLE_BOOK_TYPES.items():
                print(f"  {b:40s} {len(books)} books")
            return
        if flag in ("--help", "-h"):
            print(__doc__)
            return

    # Parse arguments
    passes = 2
    dry_run = False
    positional = []

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--passes" and i + 1 < len(sys.argv):
            passes = int(sys.argv[i + 1])
            i += 2
            continue
        elif arg in ("--jobs", "-j") and i + 1 < len(sys.argv):
            # Handled later by the concurrency resolver
            i += 2
            continue
        elif arg == "--dry-run":
            dry_run = True
            i += 1
            continue
        elif arg.startswith("-"):
            print(f"Unknown flag: {arg}", file=sys.stderr)
            sys.exit(1)
        else:
            positional.append(arg)
            i += 1

    # ── Resolve bundle type(s) ──────────────────────────────────────────
    if len(positional) >= 1:
        bundle_type_arg = positional[0]
    else:
        bundle_type_arg = prompt_bundle_type()

    if bundle_type_arg == "all":
        bundle_types = list(BUNDLE_BOOK_TYPES.keys())
    else:
        if bundle_type_arg not in BUNDLE_BOOK_TYPES:
            print(f"ERROR: Unknown bundle type '{bundle_type_arg}'.", file=sys.stderr)
            print(f"Supported: {', '.join(BUNDLE_BOOK_TYPES.keys())}", file=sys.stderr)
            sys.exit(1)
        bundle_types = [bundle_type_arg]

    # ── Resolve state(s) ────────────────────────────────────────────────
    config = load_config(WORKSPACE)
    all_slugs = config.all_state_slugs

    if len(positional) >= 2:
        requested = [s.strip().lower() for s in positional[1].split(",")]
        unknown = [s for s in requested if s not in all_slugs]
        if unknown:
            print(f"ERROR: Unknown state(s): {', '.join(unknown)}", file=sys.stderr)
            sys.exit(1)
        state_slugs = requested
    elif len(positional) == 1:
        # Bundle was given positionally but state was not — prompt
        selected = prompt_states(all_slugs)
        state_slugs = selected if selected is not None else list(all_slugs)
    else:
        # Fully interactive
        selected = prompt_states(all_slugs)
        state_slugs = selected if selected is not None else list(all_slugs)

    # ── Resolve concurrency ──────────────────────────────────────────
    max_workers = MAX_WORKERS
    i_arg = 1
    while i_arg < len(sys.argv):
        a = sys.argv[i_arg]
        if a in ("--jobs", "-j") and i_arg + 1 < len(sys.argv):
            max_workers = int(sys.argv[i_arg + 1])
            break
        i_arg += 1

    # ── Build work list ─────────────────────────────────────────────────
    jobs: List[tuple] = []
    for bt in bundle_types:
        for slug in state_slugs:
            jobs.append((bt, slug))

    total = len(jobs)
    print(f"\nWill generate {total} preview(s): "
          f"{len(bundle_types)} bundle type(s) × {len(state_slugs)} state(s)")
    print(f"   Workers: {max_workers}  |  Passes: {passes}  |  Dry-run: {dry_run}")
    print()

    # ── Run concurrently ────────────────────────────────────────────────
    succeeded: List[str] = []
    failed: List[str] = []
    t0 = time.monotonic()

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(generate_and_compile, bt, slug, passes, dry_run): (bt, slug)
            for bt, slug in jobs
        }
        done_count = 0
        for future in as_completed(futures):
            done_count += 1
            bt, slug = futures[future]
            job_label = f"{bt}/{slug}"
            try:
                ok, msg = future.result()
            except Exception as exc:
                ok = False
                msg = str(exc)

            if ok:
                succeeded.append(job_label)
                print(f"  [{done_count}/{total}] OK {job_label}")
                print(f"                  {msg}")
            else:
                failed.append(msg)
                print(f"  [{done_count}/{total}] FAIL {job_label}")

    elapsed = time.monotonic() - t0
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"Succeeded: {len(succeeded)}  |  Failed: {len(failed)}  |  Time: {elapsed:.1f}s")

    if failed:
        print("\nFailed:")
        for msg in failed:
            print(f"   {msg[:200]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
