#!/usr/bin/env python3
"""
Generate bundles.json for all bundle × state combinations.

Produces a JSON file that tells the Chrome extension:
  - How to name each bundle (TPT title)
  - Which books (by tpt_title) belong to it
  - Where thumbnails, description HTML, and preview PDF files are

Usage:
    # Generate for all states and all bundles
    python3 scripts/generate_bundles_json.py

    # Filter by state or bundle type
    python3 scripts/generate_bundles_json.py --states texas,california
    python3 scripts/generate_bundles_json.py --bundles practice_tests_bundle,test_prep_bundle

    # Custom output path
    python3 scripts/generate_bundles_json.py --output bundles.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add the skills scripts dir and workspace scripts dir to path
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import from the bundle facts module
BUNDLE_SCRIPTS = (
    WORKSPACE
    / ".agents"
    / "skills"
    / "writing-tpt-bundles-descriptions"
    / "scripts"
)
sys.path.insert(0, str(BUNDLE_SCRIPTS))

from config import (
    find_workspace,
    load_book_titles,
    default_titles_json_path,
)
from config_loader import load_config
from get_bundle_facts import (
    BUNDLE_DEFINITIONS,
    BOOK_DISPLAY_NAMES,
    bundle_tpt_title,
    load_state_exams,
    load_state_curriculums,
)

BUNDLES_JSON_FILENAME = "bundles.json"
NUM_THUMBNAILS = 4


def build_bundle_entry(
    bundle_type: str,
    state_slug: str,
    state_name: str,
    titles_by_key: Dict[str, dict],
    exams: Dict[str, dict],
    curriculums: Dict[str, dict],
) -> Dict[str, Any]:
    """Build one entry for bundles.json."""
    bundle = BUNDLE_DEFINITIONS[bundle_type]

    # Exam / curriculum info
    exam = exams.get(state_slug, {})
    curr = curriculums.get(state_slug, {})
    exam_acronym = exam.get("exam_acronym", "")
    exam_name = exam.get("exam_name", "")
    curr_acronym = curr.get("curriculum_acronym", "")
    curr_name = curr.get("curriculum_name", "")

    # Bundle TPT title (≤ 80 chars, tiered like book_tpt_title)
    tpt_title = bundle_tpt_title(bundle_type, state_slug, state_name)

    # Books in this bundle with their TPT titles
    books: List[Dict[str, str]] = []
    for bt in bundle["book_types"]:
        key = f"{state_slug}:{bt}"
        entry = titles_by_key.get(key)
        book_info: Dict[str, str] = {
            "book_type": bt,
            "display_name": BOOK_DISPLAY_NAMES.get(bt, bt),
        }
        if entry:
            book_info["tpt_title"] = entry.get("tpt_title", "")
        books.append(book_info)

    # File paths (relative to workspace root)
    bundle_dir = f"final_output/bundles/{bundle_type}"
    description_html = f"{bundle_dir}/{state_slug}_tpt_bundle.html"
    preview_pdf = f"{bundle_dir}/{state_slug}_tpt_bundle_preview.pdf"
    thumbnails = [
        f"{bundle_dir}/{state_slug}_thumbnail_{i}.jpeg"
        for i in range(1, NUM_THUMBNAILS + 1)
    ]

    return {
        "bundle_type": bundle_type,
        "display_name": bundle["display_name"],
        "tpt_title": tpt_title,
        "num_books": bundle["num_books"],
        "price_tier": bundle["price_tier"],
        "state_slug": state_slug,
        "state_name": state_name,
        "exam_name": exam_name,
        "exam_acronym": exam_acronym,
        "curriculum_name": curr_name,
        "curriculum_acronym": curr_acronym,
        "books": books,
        "files": {
            "description_html": description_html,
            "preview_pdf": preview_pdf,
            "thumbnails": thumbnails,
        },
    }


def generate_all_bundles(
    state_slugs: List[str],
    bundle_types: List[str],
    config,
) -> List[Dict[str, Any]]:
    """Generate bundle data for every bundle × state combination."""
    titles_by_key = load_book_titles(default_titles_json_path())
    exams = load_state_exams()
    curriculums = load_state_curriculums()

    results: List[Dict[str, Any]] = []
    for state_slug in sorted(state_slugs):
        state_name = config.state_display_names.get(
            state_slug, state_slug.replace("-", " ").title()
        )
        for bt in bundle_types:
            entry = build_bundle_entry(
                bt, state_slug, state_name, titles_by_key, exams, curriculums
            )
            results.append(entry)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate bundles.json for all bundle × state combinations."
    )
    parser.add_argument(
        "--states",
        help="Comma-separated state slugs (default: all)",
    )
    parser.add_argument(
        "--bundles",
        help="Comma-separated bundle type keys (default: all)",
    )
    parser.add_argument(
        "--output", "-o",
        help=f"Output file path (default: <workspace>/{BUNDLES_JSON_FILENAME})",
    )
    args = parser.parse_args()

    config = load_config(find_workspace())

    # Resolve states
    if args.states:
        state_slugs = [s.strip() for s in args.states.split(",")]
        for s in state_slugs:
            if s not in config.all_state_slugs:
                print(f"Error: unknown state '{s}'", file=sys.stderr)
                sys.exit(1)
    else:
        state_slugs = sorted(config.all_state_slugs)

    # Resolve bundle types
    all_bundle_types = list(BUNDLE_DEFINITIONS.keys())
    if args.bundles:
        bundle_types = [b.strip() for b in args.bundles.split(",")]
        for b in bundle_types:
            if b not in BUNDLE_DEFINITIONS:
                print(f"Error: unknown bundle type '{b}'", file=sys.stderr)
                print(f"Available: {', '.join(all_bundle_types)}", file=sys.stderr)
                sys.exit(1)
    else:
        bundle_types = all_bundle_types

    results = generate_all_bundles(state_slugs, bundle_types, config)

    output_str = json.dumps(results, indent=2, ensure_ascii=False)

    out_path = Path(args.output) if args.output else (WORKSPACE / BUNDLES_JSON_FILENAME)
    out_path.write_text(output_str, encoding="utf-8")
    print(f"Wrote {len(results)} entries to {out_path}")


if __name__ == "__main__":
    main()
