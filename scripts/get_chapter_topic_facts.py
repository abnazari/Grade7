#!/usr/bin/env python3
"""
Return chapter topic facts from topics_config.yaml for AI agents.

Usage:
    python3 scripts/get_chapter_topic_facts.py --chapter <chapter>

Examples:
    python3 scripts/get_chapter_topic_facts.py --chapter 1
    python3 scripts/get_chapter_topic_facts.py --chapter ch02
    python3 scripts/get_chapter_topic_facts.py --chapter 05

Prints a structured plain-text report with:
  - Grade level, target audience, and age range
  - Core topics for the chapter
  - Additional topics for the chapter
  - Modified topic variants for the chapter
    - File paths for each topic
  - The YAML "content" summary for each topic

The output is intentionally lightweight so multiple skills can use it as a
shared lookup script without loading the full .tex file contents.
"""

from __future__ import annotations

import signal
import sys
from pathlib import Path
from typing import Dict, List

import yaml

# Add scripts/ to sys.path so we can import config.py
_scripts_dir = str(Path(__file__).resolve().parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from config import GRADE_NUMBER, GRADE_DISPLAY  # noqa: E402


# Grade-to-age mapping: typical student age range for each US grade level
_GRADE_AGE_RANGES: Dict[int, str] = {
    1: "6-7",   2: "7-8",   3: "8-9",   4: "9-10",
    5: "10-11", 6: "11-12", 7: "12-13", 8: "13-14",
    9: "14-15", 10: "15-16", 11: "16-17", 12: "17-18",
}


def _find_workspace() -> Path:
    """Walk up from this file to find the workspace root."""
    candidate = Path(__file__).resolve().parent
    for _ in range(10):
        if (candidate / "topics_config.yaml").exists() and (candidate / "studyGuide.cls").exists():
            return candidate
        candidate = candidate.parent
    print("ERROR: Could not find workspace root.", file=sys.stderr)
    sys.exit(1)


WORKSPACE = _find_workspace()


def _load_topics_yaml() -> dict:
    path = WORKSPACE / "topics_config.yaml"
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _parse_chapter(value: str) -> int:
    raw = value.strip().lower()
    if raw.startswith("chapter"):
        raw = raw.replace("chapter", "", 1).strip()
    if raw.startswith("ch"):
        raw = raw[2:]
    raw = raw.lstrip("0") or "0"

    if not raw.isdigit():
        print(f"ERROR: Invalid chapter '{value}'. Use values like 1, 01, or ch01.", file=sys.stderr)
        sys.exit(1)

    chapter_num = int(raw)
    if chapter_num < 1:
        print(f"ERROR: Invalid chapter '{value}'. Chapter must be >= 1.", file=sys.stderr)
        sys.exit(1)
    return chapter_num


def _get_chapter_record(raw_config: dict, chapter_num: int) -> dict:
    for chapter in raw_config.get("chapters", []):
        if int(chapter["num"]) == chapter_num:
            return chapter
    print(f"ERROR: Chapter {chapter_num} was not found in topics_config.yaml.", file=sys.stderr)
    sys.exit(1)


def _get_additional_topics_for_chapter(raw_config: dict, chapter_num: int) -> List[dict]:
    return [
        topic
        for topic in raw_config.get("additional_topics", [])
        if int(topic.get("chapter", 0)) == chapter_num
    ]


def _build_modified_lookup(raw_config: dict) -> Dict[str, dict]:
    modified_by_core_id: Dict[str, dict] = {}
    for topic in raw_config.get("modified_topics", []):
        modified_by_core_id[str(topic["core_id"])] = topic
    return modified_by_core_id


def _build_state_memberships(raw_config: dict) -> tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    additional_memberships: Dict[str, List[str]] = {}
    modified_memberships: Dict[str, List[str]] = {}

    states = raw_config.get("states", {})
    for state_slug, state_info in states.items():
        for topic_ref in state_info.get("additional", []):
            topic_id = topic_ref.split("-", 2)[0] + "-" + topic_ref.split("-", 2)[1]
            additional_memberships.setdefault(topic_id, []).append(state_slug)
        for topic_ref in state_info.get("modified", []):
            topic_id = topic_ref.split("-", 2)[0] + "-" + topic_ref.split("-", 2)[1]
            modified_memberships.setdefault(topic_id, []).append(state_slug)

    return additional_memberships, modified_memberships


def _relative_topic_path(directory: str, file_slug: str) -> str:
    return f"{directory}/{file_slug}.tex"


def _build_topic_entry(
    *,
    topic_id: str,
    name: str,
    file_slug: str,
    summary: str,
    category: str,
    target_dir: str,
    state_slugs: List[str] | None = None,
) -> Dict[str, object]:
    return {
        "topic_id": topic_id,
        "name": name,
        "file_slug": file_slug,
        "summary": summary,
        "category": category,
        "target_rel_path": _relative_topic_path(target_dir, file_slug),
        "state_slugs": state_slugs or [],
    }


def _format_states(state_slugs: List[str]) -> str:
    if not state_slugs:
        return "(none listed)"
    return ", ".join(state_slugs)


def _print_topic_block(index: int, entry: Dict[str, object]) -> None:
    print(f"Topic {index}")
    print(f"  Topic ID:        {entry['topic_id']}")
    print(f"  Name:            {entry['name']}")
    print(f"  File Path:       {entry['target_rel_path']}")
    print(f"  Summary:         {entry['summary']}")

    if entry["category"] == "additional":
        print(f"  Included States: {_format_states(entry['state_slugs'])}")
    elif entry["category"] == "modified":
        print(f"  Modified States: {_format_states(entry['state_slugs'])}")

    print()


def _print_section(title: str, entries: List[Dict[str, object]]) -> None:
    print(title)
    if not entries:
        print("  (none)")
        print()
        return

    for index, entry in enumerate(entries, start=1):
        _print_topic_block(index, entry)


def print_chapter_topic_facts(chapter_value: str) -> None:
    raw_config = _load_topics_yaml()

    chapter_num = _parse_chapter(chapter_value)
    chapter_record = _get_chapter_record(raw_config, chapter_num)
    chapter_title = str(chapter_record.get("title", "")).replace("\\&", "&")

    additional_memberships, modified_memberships = _build_state_memberships(raw_config)
    modified_lookup = _build_modified_lookup(raw_config)

    core_entries: List[Dict[str, object]] = []
    for topic in chapter_record.get("topics", []):
        core_entries.append(
            _build_topic_entry(
                topic_id=topic["id"],
                name=topic["name"],
                file_slug=topic["file"],
                summary=topic.get("content", ""),
                category="core",
                target_dir="topics",
            )
        )

    additional_entries: List[Dict[str, object]] = []
    for topic in _get_additional_topics_for_chapter(raw_config, chapter_num):
        additional_entries.append(
            _build_topic_entry(
                topic_id=topic["id"],
                name=topic["name"],
                file_slug=topic["file"],
                summary=topic.get("content", ""),
                category="additional",
                target_dir="topics_additional",
                state_slugs=additional_memberships.get(topic["id"], []),
            )
        )

    modified_entries: List[Dict[str, object]] = []
    for topic in chapter_record.get("topics", []):
        topic_id = str(topic["id"])
        modified_topic = modified_lookup.get(topic_id)
        if not modified_topic:
            continue
        modified_entries.append(
            _build_topic_entry(
                topic_id=topic_id,
                name=topic["name"],
                file_slug=modified_topic["file"],
                summary=modified_topic.get("content", ""),
                category="modified",
                target_dir="topics_modified",
                state_slugs=modified_memberships.get(topic_id, []),
            )
        )

    age_range = _GRADE_AGE_RANGES.get(GRADE_NUMBER, "unknown")

    print("=" * 70)
    print(f"CHAPTER TOPIC FACTS: chapter {chapter_num}")
    print("=" * 70)
    print()
    print("--- GRADE INFO ---")
    print(f"Grade:             {GRADE_DISPLAY}")
    print(f"Grade Number:      {GRADE_NUMBER}")
    print(f"Target Audience:   {age_range} year-old students")
    print()
    print("--- REQUEST ---")
    print(f"Chapter Number:    {chapter_num}")
    print(f"Chapter Title:     {chapter_title}")
    print()
    print("--- COUNTS ---")
    print(f"Topics:            {len(core_entries)}")
    print(f"Additional Topics: {len(additional_entries)}")
    print(f"Modified Topics:   {len(modified_entries)}")
    print()

    _print_section("--- TOPICS ---", core_entries)
    _print_section("--- ADDITIONAL TOPICS ---", additional_entries)
    _print_section("--- MODIFIED TOPICS ---", modified_entries)

    print("=" * 70)
    print("END OF FACTS")
    print("=" * 70)


def print_usage() -> None:
    print("Usage: python3 scripts/get_chapter_topic_facts.py --chapter <chapter>")
    print()
    print("Chapter values: 1, 01, ch01, chapter 1, ...")
    print()
    print("Examples:")
    print("  python3 scripts/get_chapter_topic_facts.py --chapter 1")
    print("  python3 scripts/get_chapter_topic_facts.py --chapter ch02")
    print("  python3 scripts/get_chapter_topic_facts.py --chapter 05")


def print_chapters() -> None:
    raw_config = _load_topics_yaml()
    for chapter in raw_config.get("chapters", []):
        title = str(chapter.get("title", "")).replace("\\&", "&")
        print(f"  {int(chapter['num']):02d}  {title}")
if __name__ == "__main__":
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    if len(sys.argv) == 2 and sys.argv[1] in ("--help", "-h"):
        print_usage()
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--list-chapters":
        print_chapters()
        sys.exit(0)

    if len(sys.argv) != 3 or sys.argv[1] != "--chapter":
        print_usage()
        sys.exit(1)

    try:
        print_chapter_topic_facts(sys.argv[2])
    except BrokenPipeError:
        sys.exit(0)