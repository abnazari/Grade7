#!/usr/bin/env python3
"""
Extract the first page of every final PDF as a 400px-wide JPEG cover image.

Output:  final_output/covers/<book_type>/<state_slug>.jpg

Run once after compiling books. The thumbnail generator uses these cached
covers instead of converting PDFs on the fly.

Usage:
    python3 scripts/extract_covers.py
    python3 scripts/extract_covers.py --jobs=8

Requires: Pillow, poppler (pdftoppm)
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image

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
FINAL_OUTPUT_DIR = WORKSPACE / "final_output"
COVERS_DIR = FINAL_OUTPUT_DIR / "covers_jpg"

COVER_WIDTH = 400          # px — enough for thumbnail composites
JPEG_QUALITY = 92
DPI = 150                  # render resolution before resizing

MAX_WORKERS: int = int(os.environ.get(
    "MAX_WORKERS", str(max(1, (os.cpu_count() or 4) - 1))
))

# Book type subdirectories under final_output/
BOOK_TYPE_DIRS = [
    "study_guide", "workbook", "step_by_step", "in_30_days",
    "quiz", "puzzles", "worksheet",
    "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests",
    "all_in_one",
]


def _pdf_first_page_to_image(pdf_path: Path) -> Optional[Image.Image]:
    """Render the first page of a PDF to a PIL Image using pdftoppm."""
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "page"
        result = subprocess.run(
            ["pdftoppm", "-jpeg", "-r", str(DPI), "-f", "1", "-l", "1",
             str(pdf_path), str(prefix)],
            capture_output=True,
        )
        if result.returncode != 0:
            return None
        jpgs = sorted(Path(tmp).glob("page-*.*"))
        if not jpgs:
            return None
        return Image.open(jpgs[0]).convert("RGB")


# Return status from extract_one
_CREATED = "created"
_SKIPPED = "skipped"


def extract_one(pdf_path: Path, book_type: str) -> Tuple[Optional[Path], str]:
    """Extract cover from one PDF. Returns (output_path, status)."""
    # Derive state slug from filename: <state_slug>_YYYY-MM-DD.pdf
    stem = pdf_path.stem  # e.g. "texas_2026-03-05"
    # Remove the date suffix
    parts = stem.rsplit("_", 1)
    state_slug = parts[0] if len(parts) == 2 else stem

    out_dir = COVERS_DIR / book_type
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{state_slug}.jpg"

    # Skip if already exists and newer than the PDF
    if out_path.exists() and out_path.stat().st_mtime >= pdf_path.stat().st_mtime:
        return out_path, _SKIPPED

    img = _pdf_first_page_to_image(pdf_path)
    if img is None:
        print(f"  WARN: failed to render {pdf_path.name}", file=sys.stderr)
        return None, _CREATED  # counts as failed in caller

    # Resize to target width, maintaining aspect ratio
    w, h = img.size
    new_h = int(h * COVER_WIDTH / w)
    img = img.resize((COVER_WIDTH, new_h), Image.LANCZOS)
    img.save(out_path, "JPEG", quality=JPEG_QUALITY)
    return out_path, _CREATED


def collect_pdfs() -> List[Tuple[Path, str]]:
    """Find all final PDFs (excluding preview/tpt) and return (path, book_type) pairs."""
    jobs = []
    for book_type in BOOK_TYPE_DIRS:
        folder = FINAL_OUTPUT_DIR / book_type
        if not folder.is_dir():
            continue
        for pdf in sorted(folder.glob("*.pdf")):
            name = pdf.name
            if "_preview_" in name or "_tpt_" in name:
                continue
            jobs.append((pdf, book_type))
    return jobs


def main() -> None:
    # Parse --jobs flag
    max_workers = MAX_WORKERS
    for a in sys.argv[1:]:
        if a.startswith("--jobs="):
            max_workers = int(a.split("=", 1)[1])
        elif a in ("--jobs", "-j"):
            idx = sys.argv.index(a)
            if idx + 1 < len(sys.argv):
                max_workers = int(sys.argv[idx + 1])
        elif a in ("--help", "-h"):
            print(__doc__)
            return

    jobs = collect_pdfs()
    print(f"Found {len(jobs)} PDFs across {len(BOOK_TYPE_DIRS)} book types")
    print(f"Output: {COVERS_DIR}/")
    print(f"Workers: {max_workers}")
    print()

    t0 = time.monotonic()
    created = 0
    skipped = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(extract_one, pdf, bt): (pdf, bt)
            for pdf, bt in jobs
        }
        for i, future in enumerate(as_completed(futures), 1):
            pdf, bt = futures[future]
            try:
                path, status = future.result()
                if path is None:
                    failed += 1
                elif status == _SKIPPED:
                    skipped += 1
                else:
                    created += 1
            except Exception as exc:
                failed += 1
                print(f"  ERROR: {bt}/{pdf.name}: {exc}", file=sys.stderr)

            if i % 50 == 0 or i == len(jobs):
                print(f"  [{i}/{len(jobs)}] created={created} skipped={skipped} failed={failed}")

    elapsed = time.monotonic() - t0
    print(f"\nDone in {elapsed:.1f}s — {created} created, {skipped} skipped, {failed} failed")
    if created or skipped:
        print(f"Covers saved to: {COVERS_DIR}/")


if __name__ == "__main__":
    main()
