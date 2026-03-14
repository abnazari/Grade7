#!/usr/bin/env python3
"""
Generate and review book titles for all state × book type combinations.

Produces a JSON or Markdown report of every title so an AI agent (or human)
can review them for readability, SEO quality, and correctness.

Usage:
    # Generate titles for all states and book types (Markdown table)
    python3 scripts/generate_book_titles.py

    # JSON output (for programmatic consumption or AI review)
    python3 scripts/generate_book_titles.py --format json

    # Filter by state or book type
    python3 scripts/generate_book_titles.py --states texas,california
    python3 scripts/generate_book_titles.py --book-types study_guide,all_in_one

    # Show only titles that may need review (long titles, missing exam info, etc.)
    python3 scripts/generate_book_titles.py --flag-issues

    # Write output to a file
    python3 scripts/generate_book_titles.py --format json --output titles.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from config import (
    BOOK_DISPLAY_NAMES,
    BOOK_TYPES,
    GRADE_DISPLAY,
    TPT_TITLE_MAX_LENGTH,
    book_title,
    book_subtitle,
    book_tpt_title,
    book_title_data,
    default_titles_json_path,
    find_workspace,
    load_state_exams,
    load_state_curriculums,
)
from config_loader import load_config

# Maximum title length before flagging (Amazon has ~200 char limit)
MAX_TITLE_LENGTH = 120


def generate_all_titles(
    state_slugs: List[str],
    book_types: List[str],
    config,
) -> List[Dict[str, Any]]:
    """Generate title data for every state × book type combination."""
    results: List[Dict[str, Any]] = []

    for state_slug in sorted(state_slugs):
        state_name = config.state_display_names.get(
            state_slug, state_slug.replace("-", " ").title()
        )
        for bt in book_types:
            data = book_title_data(bt, state_slug, state_name)

            # Flag potential issues
            issues: List[str] = []
            if len(data["title"]) > MAX_TITLE_LENGTH:
                issues.append(f"title too long ({len(data['title'])} chars)")
            if data["tpt_title_length"] > TPT_TITLE_MAX_LENGTH:
                issues.append(
                    f"tpt_title too long ({data['tpt_title_length']} chars)"
                )
            if not data["exam_acronym"]:
                issues.append("missing exam acronym")
            if not data["curriculum_acronym"]:
                issues.append("missing curriculum acronym")

            data["issues"] = issues
            data["title_length"] = len(data["title"])
            results.append(data)

    return results


def format_markdown(results: List[Dict[str, Any]], flag_issues: bool) -> str:
    """Format results as a readable Markdown report."""
    lines: List[str] = []
    lines.append(f"# Book Titles Report — {GRADE_DISPLAY}")
    lines.append("")
    lines.append(f"Total combinations: {len(results)}")
    lines.append("")

    if flag_issues:
        flagged = [r for r in results if r["issues"]]
        lines.append(f"**Flagged for review: {len(flagged)}**")
        lines.append("")
        results = flagged

    # Group by state
    by_state: Dict[str, List[Dict[str, Any]]] = {}
    for r in results:
        by_state.setdefault(r["state_name"], []).append(r)

    for state_name in sorted(by_state):
        lines.append(f"## {state_name}")
        lines.append("")

        state_results = by_state[state_name]
        first = state_results[0]
        if first["exam_acronym"]:
            lines.append(
                f"- **Exam**: {first['exam_name']} ({first['exam_acronym']})"
                + (f" — {first['exam_months']}" if first["exam_months"] else "")
            )
        if first["curriculum_acronym"]:
            lines.append(
                f"- **Curriculum**: {first['curriculum_name']} "
                f"({first['curriculum_acronym']})"
            )
        lines.append("")

        lines.append("| Book Type | Title | Subtitle | Len | TPT Title | TPT Len | Issues |")
        lines.append("|-----------|-------|----------|-----|-----------|---------|--------|") 

        for r in state_results:
            issues_str = "; ".join(r["issues"]) if r["issues"] else "\u2713"
            lines.append(
                f"| {r['display_name']} "
                f"| {r['title']} "
                f"| {r['subtitle']} "
                f"| {r['title_length']} "
                f"| {r['tpt_title']} "
                f"| {r['tpt_title_length']} "
                f"| {issues_str} |"
            )
        lines.append("")

    return "\n".join(lines)


def format_json(results: List[Dict[str, Any]], flag_issues: bool) -> str:
    """Format results as JSON."""
    if flag_issues:
        results = [r for r in results if r["issues"]]
    return json.dumps(results, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate and review book titles for all state × book type combinations."
    )
    parser.add_argument(
        "--states",
        help="Comma-separated state slugs (default: all)",
    )
    parser.add_argument(
        "--book-types",
        help="Comma-separated book type keys (default: all)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--flag-issues",
        action="store_true",
        help="Show only entries that may need review",
    )
    parser.add_argument(
        "--output", "-o",
        help="Write output to file instead of stdout",
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

    # Resolve book types
    if args.book_types:
        book_types = [b.strip() for b in args.book_types.split(",")]
        for b in book_types:
            if b not in BOOK_TYPES:
                print(f"Error: unknown book type '{b}'", file=sys.stderr)
                sys.exit(1)
    else:
        book_types = list(BOOK_TYPES.keys())

    results = generate_all_titles(state_slugs, book_types, config)

    if args.format == "json":
        output = format_json(results, args.flag_issues)
    else:
        output = format_markdown(results, args.flag_issues)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(output, encoding="utf-8")
        print(f"✅ Generated JSON for review: {out_path.resolve()}")
    elif args.format == "json":
        out_path = default_titles_json_path()
        out_path.write_text(output, encoding="utf-8")
        print(f"✅ Generated JSON for review: {out_path}")
    else:
        print(output)


if __name__ == "__main__":
    main()
