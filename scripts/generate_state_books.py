#!/usr/bin/env python3
"""
Generate state-specific .tex files for all Grade 7 book types.

For each state × book type, this script:
  1. Reads topic and state configuration from topics_config.yaml
  2. Determines which topics apply (core CCSS + state-specific additions)
  3. Generates the .tex file with correct topic paths and ordering
  4. Writes the result to state_books/<state>/<book_type>_<state>-grade7.tex

Book Types Supported:
  - all_in_one:         Comprehensive all-in-one with lessons, warmups & practice (~450 pages)
  - study_guide:        Brief study guide focused on core concepts (~130 pages)
  - workbook:           Practice workbook with problems for every topic
  - step_by_step:       Step-by-step study guide with procedural approach
  - in_30_days:         30-day calendar-based study guide
  - 3_practice_tests:   3 full-length practice tests with answer keys
  - 5_practice_tests:   5 full-length practice tests with answer keys
  - 7_practice_tests:   7 full-length practice tests with answer keys
  - 10_practice_tests:  10 full-length practice tests with answer keys

State Customization:
  - 36 "CCSS-only" states use the base topic list unchanged
  - 14 states have modified topics (topics_modified/) and/or additional
    state-specific topics (topics_additional/) inserted at the correct
    chapter positions

All topic data and state customizations are read from topics_config.yaml
(single source of truth shared with generate_practice_tests.py).

Usage:
    # Generate all_in_one for all 50 states
    python3 scripts/generate_state_books.py --book-type all_in_one

    # Generate brief study_guide for all 50 states
    python3 scripts/generate_state_books.py --book-type study_guide

    # Generate all book types for all states
    python3 scripts/generate_state_books.py --book-type all

    # Specific states only
    python3 scripts/generate_state_books.py --book-type all_in_one --states texas,virginia

    # Dry-run (preview without writing files)
    python3 scripts/generate_state_books.py --book-type study_guide --dry-run

    # Verbose mode (print generated filenames)
    python3 scripts/generate_state_books.py --book-type all --verbose
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from config import (
    default_titles_json_path,
    inject_titles_into_tex,
    load_book_titles,
    prompt_book_type,
    prompt_states,
)
from config_loader import TopicsConfig, find_workspace, load_config


# ============================================================================
# BOOK TYPE CONFIGURATIONS
# ============================================================================
# Template files live in the workspace root.  The generator reads each
# *_main.tex template and transforms it for every state rather than
# hard-coding the .tex structure in Python.
#
# Naming convention for output files:
#   state_books/<state>/<book_type>_<state>-grade7.tex

BOOK_TYPES: Dict[str, dict] = {
    "all_in_one": {
        "template": "all_in_one_main.tex",
        "description": "Comprehensive all-in-one with lessons, warmups & practice (~450 pages)",
    },
    "study_guide": {
        "template": "study_guide_main.tex",
        "description": "Brief study guide focused on core concepts (~130 pages)",
    },
    "workbook": {
        "template": "workbook_main.tex",
        "description": "Practice workbook with problems for every topic",
    },
    "step_by_step": {
        "template": "steps_main.tex",
        "description": "Step-by-step study guide — learn math one step at a time",
    },
    "3_practice_tests": {
        "template": "3_practice_tests_main.tex",
        "description": "3 full-length practice tests",
        "test_range": (1, 3),      # practice_test_01 through 03
    },
    "5_practice_tests": {
        "template": "5_practice_tests_main.tex",
        "description": "5 full-length practice tests",
        "test_range": (4, 8),      # practice_test_04 through 08
    },
    "7_practice_tests": {
        "template": "7_practice_tests_main.tex",
        "description": "7 full-length practice tests",
        "test_range": (9, 15),     # practice_test_09 through 15
    },
    "10_practice_tests": {
        "template": "10_practice_tests_main.tex",
        "description": "10 full-length practice tests",
        "test_range": (16, 25),    # practice_test_16 through 25
    },
    "in_30_days": {
        "template": "in30days_main.tex",
        "description": "30-day calendar-based study guide",
    },
    "quiz": {
        "template": "quiz_main.tex",
        "description": "Quick 15-minute quizzes — one per topic",
    },
    "puzzles": {
        "template": "puzzles_main.tex",
        "description": "Puzzles, games & brain teasers aligned to the curriculum",
    },
    "worksheet": {
        "template": "worksheet_main.tex",
        "description": "Standalone printable worksheet activities for every topic",
    },
}


# ============================================================================
# TOPIC DIRECTORY MAPPINGS
# ============================================================================
# For each book type: (core_dir, modified_dir, additional_dir)

TOPIC_DIR_MAP: Dict[str, tuple] = {
    "all_in_one":   ("topics",             "topics_modified",              "topics_additional"),
    "study_guide":  ("topics",             "topics_modified",              "topics_additional"),
    "workbook":     ("topics_workbook",     "topics_workbook_modified",     "topics_workbook_additional"),
    "step_by_step": ("steps_topics",        "steps_topics_modified",        "steps_topics_additional"),
    "quiz":         ("topics_quiz",         "topics_quiz_modified",         "topics_quiz_additional"),
    "puzzles":      ("topics_puzzles",      "topics_puzzles_modified",      "topics_puzzles_additional"),
    "worksheet":    ("topics_worksheet",    "topics_worksheet_modified",    "topics_worksheet_additional"),
    "in_30_days":   ("topics_in30days",     "topics_in30days_modified",     "topics_in30days_additional"),
}


# ============================================================================
# TEMPLATE-BASED GENERATOR (generic, for chapter-based book types)
# ============================================================================

def _get_chapter_prefix(chapter_num: int) -> str:
    """Return the 2-digit chapter prefix, e.g. 'ch01'."""
    return f"ch{chapter_num:02d}"


def generate_from_template(
    template_path: Path,
    book_type_key: str,
    state_slug: str,
    state_name: str,
    config: TopicsConfig,
) -> str:
    r"""Generate a state-specific .tex by transforming a \*_main.tex template.

    The template file is the single source of truth for book structure
    (document class, cover parameters, initial pages, chapter ordering,
    extra LaTeX commands).  ``topics_config.yaml`` controls which topics
    appear and which are state-customized.

    Processing rules applied line-by-line:

    1. ``\StateName{...}`` → replaced with the target state's display name.
    2. Commented-out ``\chapter{...}`` lines → uncommented.
    3. Topic ``\input{<core_dir>/...}`` lines (commented or not):
       - Always uncommented.
       - Redirected to the *modified* directory when the topic is in
         the state's modified set.
    4. After each chapter's last core topic → additional state-specific
       topics are inserted (from the *additional* directory).
    5. A header edition note and standards line are injected for
       customized states.
    6. All other lines (initial pages, settings, comments, blank lines)
       are preserved **unchanged**.

    Args:
        template_path: Path to the ``*_main.tex`` template file.
        book_type_key: Key in ``BOOK_TYPES`` / ``TOPIC_DIR_MAP``.
        state_slug:    Slug like ``'texas'``.
        state_name:    Display name like ``'Texas'``.
        config:        Loaded ``TopicsConfig``.

    Returns:
        The full ``.tex`` content for the state book.
    """
    template = template_path.read_text(encoding="utf-8")
    lines = template.split("\n")

    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    core_dir, modified_dir, additional_dir = TOPIC_DIR_MAP[book_type_key]

    # Reverse map: filename slug → topic ID
    filename_to_id: Dict[str, str] = {v: k for k, v in config.topic_filenames.items()}

    is_customized = bool(modified_set or additional_set)
    edition_note = f" ({state_name} Edition)" if is_customized else ""
    standards_line = (
        f"% Customized for {state_name} State Standards"
        if is_customized
        else "% Common Core State Standards (CCSS) — no state-specific modifications"
    )

    # ── Compiled regex patterns ────────────────────────────────────────
    # Topic input:  \input{core_dir/filename}  or  % \input{core_dir/filename}
    topic_input_re = re.compile(
        r"^(\s*)(%\s*)?\\input\{" + re.escape(core_dir) + r"/([^}]+)\}(.*)$"
    )
    # Chapter:  \chapter{Title}  or  % \chapter{Title}
    chapter_re = re.compile(r"^(\s*)(%\s*)?\\chapter\{(.+)\}(.*)$")
    # Answer-key / puzzle-answers / worksheet-answers
    answer_key_re = re.compile(
        r"^(\s*)\\(printAnswerKey|printPuzzleAnswers|printWorksheetAnswers)\b"
    )
    # \StateName{...}
    state_name_re = re.compile(r"^(\s*)\\StateName\{[^}]*\}(.*)$")
    # Header title (line that starts with "% Grade 7")
    header_title_re = re.compile(r"^% Grade 7 ")

    # ── State ──────────────────────────────────────────────────────────
    output_lines: List[str] = []
    current_chapter_prefix: Optional[str] = None
    last_topic_output_idx: int = -1   # index of last topic \input in output_lines
    header_title_seen = False

    def _flush_additional() -> None:
        """Insert additional state-specific topics right after the last
        core topic input line (tracked by *last_topic_output_idx*) so they
        appear before any chapter separator comments that follow."""
        nonlocal current_chapter_prefix, last_topic_output_idx
        if not current_chapter_prefix or not additional_set:
            return
        additional_for_chapter = sorted(
            t for t in additional_set if t.startswith(current_chapter_prefix + "-")
        )
        if not additional_for_chapter:
            return
        # Determine insertion point — right after the last topic input
        insert_at = last_topic_output_idx + 1 if last_topic_output_idx >= 0 else len(output_lines)
        for offset, topic_id in enumerate(additional_for_chapter):
            filename = config.topic_filenames[topic_id]
            output_lines.insert(insert_at + offset, f"\\input{{{additional_dir}/{filename}}}")
        # Advance the index past the newly-inserted lines
        last_topic_output_idx = insert_at + len(additional_for_chapter) - 1

    # ── Line-by-line processing ────────────────────────────────────────
    for line in lines:
        stripped = line.strip()

        # ── 1. \StateName{...} ─────────────────────────────────────────
        sm = state_name_re.match(line)
        if sm:
            indent, trailing = sm.group(1), sm.group(2)
            output_lines.append(f"{indent}\\StateName{{{state_name}}}{trailing}")
            continue

        # ── 2. \chapter{...} (possibly commented) ─────────────────────
        cm = chapter_re.match(stripped)
        if cm:
            # Flush additional topics for the *previous* chapter
            _flush_additional()
            current_chapter_prefix = None

            ch_title = cm.group(3)
            trailing = cm.group(4)
            # Always output uncommented (leading whitespace from original line)
            leading_ws = line[: len(line) - len(line.lstrip())]
            output_lines.append(f"{leading_ws}\\chapter{{{ch_title}}}{trailing}")
            continue

        # ── 3. Answer-key / puzzle-answers / worksheet-answers ────────
        if answer_key_re.match(stripped):
            _flush_additional()
            current_chapter_prefix = None
            output_lines.append(line)
            continue

        # ── 4. Topic \input{core_dir/...} (possibly commented) ────────
        tm = topic_input_re.match(line)
        if tm:
            indent = tm.group(1)
            filename = tm.group(3)
            trailing = tm.group(4)

            topic_id = filename_to_id.get(filename)

            # Choose directory
            if topic_id and topic_id in modified_set:
                dir_to_use = modified_dir
            else:
                dir_to_use = core_dir

            output_lines.append(f"{indent}\\input{{{dir_to_use}/{filename}}}{trailing}")
            last_topic_output_idx = len(output_lines) - 1

            # Track chapter prefix for additional-topic injection
            pfx = re.match(r"(ch\d+)", filename)
            if pfx:
                current_chapter_prefix = pfx.group(1)
            continue

        # ── 5. Header edition note ─────────────────────────────────────
        if not header_title_seen and header_title_re.match(line):
            header_title_seen = True
            output_lines.append(line.rstrip() + edition_note)
            continue

        # ── 6. Everything else → pass through ─────────────────────────
        output_lines.append(line)

    # ── Post-processing: inject standards line into header ─────────────
    # Insert after the header subtitle (3rd line, which is a % comment),
    # right before the closing "% ===..." separator.
    for i, ol in enumerate(output_lines):
        if ol.startswith("% Grade 7"):
            # Next line is the subtitle; line after that is the separator
            insert_idx = i + 2
            if insert_idx < len(output_lines) and output_lines[insert_idx].startswith(
                "% ==="
            ):
                output_lines.insert(insert_idx, standards_line)
            break

    return "\n".join(output_lines)


# ============================================================================
# TEMPLATE-BASED GENERATOR — IN 30 DAYS (day-based structure)
# ============================================================================

def generate_in_30_days_from_template(
    template_path: Path,
    state_slug: str,
    state_name: str,
    config: TopicsConfig,
) -> str:
    r"""Generate a state-specific 30-day book by transforming ``in30days_main.tex``.

    The 30-day book uses day files (``day-NN-...``) instead of chapter/topic
    files.  State customization works differently:

    - **Modified days**: If any topic covered by a day is in the state's
      modified set, the day file is loaded from ``topics_in30days_modified/``.
    - **Bonus lessons**: After certain days, additional lessons are inserted
      from ``topics_in30days_additional/bonus-...``.

    All other lines (cover, initial pages, chapter headers, settings) are
    preserved unchanged from the template.
    """
    template = template_path.read_text(encoding="utf-8")
    lines = template.split("\n")

    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    core_dir, modified_dir, additional_dir = TOPIC_DIR_MAP["in_30_days"]

    if config.in_30_days_config is None:
        print("  🚫 in_30_days config not found in topics_config.yaml")
        return ""

    days_config = config.in_30_days_config

    is_customized = bool(modified_set or additional_set)
    edition_note = f" ({state_name} Edition)" if is_customized else ""
    standards_line = (
        f"% Customized for {state_name} State Standards"
        if is_customized
        else "% Common Core State Standards (CCSS) — no state-specific modifications"
    )

    # Build day-file lookup:  filename → In30DaysDay entry
    day_lookup: Dict[str, "In30DaysDay"] = {}  # noqa: F821
    for day_entry in days_config.days:
        day_lookup[day_entry.file] = day_entry

    # ── Compiled regex patterns ────────────────────────────────────────
    day_input_re = re.compile(
        r"^(\s*)(%\s*)?\\input\{" + re.escape(core_dir) + r"/([^}]+)\}(.*)$"
    )
    state_name_re = re.compile(r"^(\s*)\\StateName\{[^}]*\}(.*)$")
    header_title_re = re.compile(r"^% Grade 7 ")

    output_lines: List[str] = []
    header_title_seen = False

    for line in lines:
        stripped = line.strip()

        # ── \StateName{...} ───────────────────────────────────────────
        sm = state_name_re.match(line)
        if sm:
            indent, trailing = sm.group(1), sm.group(2)
            output_lines.append(f"{indent}\\StateName{{{state_name}}}{trailing}")
            continue

        # ── Day input: \input{topics_in30days/day-NN-...} ─────────────
        dm = day_input_re.match(line)
        if dm:
            indent = dm.group(1)
            was_commented = bool(dm.group(2))
            filename = dm.group(3)
            trailing = dm.group(4)

            day_entry = day_lookup.get(filename)

            # Check if any topic in this day is modified
            if day_entry:
                modified_in_day = [t for t in day_entry.topics if t in modified_set]
                dir_to_use = modified_dir if modified_in_day else core_dir
            else:
                dir_to_use = core_dir

            output_lines.append(f"{indent}\\input{{{dir_to_use}/{filename}}}{trailing}")

            # Insert bonus lessons after this day
            if day_entry:
                for bonus_id in day_entry.bonus_after:
                    if bonus_id in additional_set:
                        bonus_file = config.topic_filenames.get(bonus_id, bonus_id)
                        output_lines.append(
                            f"{indent}\\input{{{additional_dir}/bonus-{bonus_file}}}"
                        )
            continue

        # ── Header edition note ────────────────────────────────────────
        if not header_title_seen and header_title_re.match(line):
            header_title_seen = True
            output_lines.append(line.rstrip() + edition_note)
            continue

        # ── Everything else → pass through ─────────────────────────────
        output_lines.append(line)

    # ── Post-processing: inject standards line into header ─────────────
    for i, ol in enumerate(output_lines):
        if ol.startswith("% Grade 7"):
            insert_idx = i + 2
            if insert_idx < len(output_lines) and output_lines[insert_idx].startswith(
                "% ==="
            ):
                output_lines.insert(insert_idx, standards_line)
            break

    return "\n".join(output_lines)


# NOTE: Legacy per-book-type generators were removed in favor of the
# template-based generators above. See git history if needed.

# ============================================================================
# PRACTICE TEST TEMPLATE-BASED GENERATOR
# ============================================================================

def generate_practice_tests_from_template(
    template_path: Path,
    state_slug: str,
    state_name: str,
    num_tests: int,
    test_start: int,
    test_end: int,
    workspace: Path,
    config: TopicsConfig,
) -> str:
    r"""Generate a state-specific practice test book by transforming a template.

    The template file (e.g. ``3_practice_tests_main.tex``) is the single
    source of truth for document class, cover parameters, initial pages,
    and any extra LaTeX preamble.  This generator performs simple
    placeholder replacements:

    - ``INSERT-STATE-NAME-HERE``      → state display name
    - ``INSERT-STATE-SLUG-HERE``      → state directory slug
    - ``INSERT-STANDARDS-NOTE-HERE``  → customized / CCSS note

    It also verifies that the referenced ``practice_test_NN.tex`` files
    exist on disk and warns if any are missing.

    Test ranges are non-overlapping across book types so a student who
    buys multiple books always gets unique tests:

        3_practice_tests  → tests  1–3
        5_practice_tests  → tests  4–8
        7_practice_tests  → tests  9–15
        10_practice_tests → tests 16–25
    """
    # ── Verify that practice test files exist for this state ─────────
    practice_dir = workspace / "practice_tests" / state_slug
    available_count = 0
    for i in range(test_start, test_end + 1):
        test_file = practice_dir / f"practice_test_{i:02d}.tex"
        if test_file.exists():
            available_count += 1

    if available_count < num_tests:
        print(f"  ⚠️  {state_name}: only {available_count}/{num_tests} "
              f"practice test files found")

    # ── Standards note ──────────────────────────────────────────────────
    is_customized = (
        state_slug in config.state_additional
        or state_slug in config.state_modified
    )
    standards_note = (
        f"Customized for {state_name} State Standards"
        if is_customized
        else "Common Core State Standards (CCSS)"
    )

    # ── Read template and perform replacements ──────────────────────────
    content = template_path.read_text(encoding="utf-8")
    content = content.replace("INSERT-STATE-NAME-HERE", state_name)
    content = content.replace("INSERT-STATE-SLUG-HERE", state_slug)
    content = content.replace("INSERT-STANDARDS-NOTE-HERE", standards_note)

    return content


# ============================================================================
# IO HELPERS
# ============================================================================

def tex_filename(book_type: str, state_slug: str) -> str:
    """e.g. study_guide_texas-grade7.tex"""
    return f"{book_type}_{state_slug}-grade7.tex"


def write_state_book(
    workspace: Path,
    state_slug: str,
    book_type: str,
    content: str,
    dry_run: bool = False,
) -> Path:
    """Write a generated .tex file to state_books/<state>/.

    Returns the output path.
    """
    out_dir = workspace / "state_books" / state_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / tex_filename(book_type, state_slug)

    if not dry_run:
        out_path.write_text(content, encoding="utf-8")

    return out_path


# ============================================================================
# VALIDATION
# ============================================================================

def validate_topic_files(workspace: Path, config: TopicsConfig) -> List[str]:
    """Check that all referenced topic files exist on disk.

    Returns a list of warning messages (empty if everything is fine).
    """
    warnings: List[str] = []

    for topic_id, filename in config.topic_filenames.items():
        core_path = workspace / "topics" / f"{filename}.tex"
        additional_path = workspace / "topics_additional" / f"{filename}.tex"
        modified_path = workspace / "topics_modified" / f"{filename}.tex"

        if not (core_path.exists() or additional_path.exists() or modified_path.exists()):
            warnings.append(f"  ⚠️  Topic file not found for {topic_id}: {filename}.tex")

    return warnings


# ============================================================================
# CLI
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate state-specific .tex files for Grade 7 math books.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s --book-type all_in_one                   # all 50 states
  %(prog)s --book-type study_guide                  # all 50 states (brief)
  %(prog)s --book-type all                          # all book types, all states
  %(prog)s --book-type all_in_one --states texas,virginia
  %(prog)s --book-type 3_practice_tests --dry-run
""",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace root directory (auto-detected if omitted)",
    )
    parser.add_argument(
        "--book-type",
        choices=list(BOOK_TYPES.keys()) + ["all"],
        default=None,
        help="Book type to generate, or 'all' for all types (interactive if omitted)",
    )
    parser.add_argument(
        "--states",
        type=str,
        default=None,
        help="Comma-separated state slugs (default: all 50)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be generated without writing files",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print each generated filename",
    )
    parser.add_argument(
        "--titles-file",
        type=Path,
        default=None,
        metavar="PATH",
        help=(
            "Path to titles.json generated by generate_book_titles.py "
            "(default: titles.json in workspace root). "
            "Use --no-titles to skip title injection entirely."
        ),
    )
    parser.add_argument(
        "--no-titles",
        action="store_true",
        help="Skip title injection — use the default titles baked into each template.",
    )
    return parser.parse_args()


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    args = parse_args()

    # ── Workspace root ──────────────────────────────────────────────────
    workspace = args.workspace or find_workspace()
    workspace = workspace.resolve()
    print(f"📂 Workspace: {workspace}")

    # ── Load titles JSON ────────────────────────────────────────────────
    titles: Optional[Dict[str, Any]] = None
    if not args.no_titles:
        titles_path = args.titles_file or default_titles_json_path()
        try:
            titles = load_book_titles(titles_path)
            print(f"📋 Titles: loaded {len(titles)} entries from {titles_path.name}")
        except FileNotFoundError:
            print(
                f"⚠️  Titles file not found: {titles_path}\n"
                "   Book titles will use the generic template defaults.\n"
                "   To use state-specific SEO titles, generate first:\n"
                "     python3 scripts/generate_book_titles.py "
                "--format json --output titles.json"
            )

    # ── Load topic & state config from YAML ─────────────────────────────
    config = load_config(workspace)

    # ── Validate topic files ────────────────────────────────────────────
    warnings = validate_topic_files(workspace, config)
    for w in warnings:
        print(w)

    # ── Interactive prompts when arguments are omitted ──────────────────
    book_type = args.book_type
    if book_type is None:
        descs = {k: v.get("description", "") for k, v in BOOK_TYPES.items()}
        book_type = prompt_book_type(
            list(BOOK_TYPES.keys()),
            descriptions=descs,
            allow_all=True,
            allow_all_previews=False,
        )

    # ── Resolve which book types to generate ────────────────────────────
    if book_type == "all":
        book_types = list(BOOK_TYPES.keys())
    else:
        book_types = [book_type]

    # ── Resolve which states to generate ────────────────────────────────
    if args.states:
        requested = [s.strip().lower() for s in args.states.split(",")]
        unknown = [s for s in requested if s not in config.all_state_slugs]
        if unknown:
            print(f"ERROR: Unknown state(s): {', '.join(unknown)}")
            print(f"  Valid slugs: {', '.join(sorted(config.all_state_slugs))}")
            sys.exit(1)
        state_slugs = requested
    else:
        states_input = prompt_states(config.all_state_slugs)
        if states_input is None:
            state_slugs = config.all_state_slugs
        else:
            state_slugs = [s.strip().lower() for s in states_input.split(",")]

    # ── Generate ────────────────────────────────────────────────────────
    total_generated = 0
    total_skipped = 0

    # Book types that use the generic chapter/topic template generator
    CHAPTER_TEMPLATE_TYPES = {
        "all_in_one", "study_guide", "workbook", "step_by_step",
        "quiz", "puzzles", "worksheet",
    }

    for bt_key in book_types:
        bt_cfg = BOOK_TYPES[bt_key]
        bt_pretty = bt_key.replace("_", " ").title()
        print(f"\n{'='*60}")
        print(f"📖 Generating: {bt_pretty}")
        print(f"   {bt_cfg['description']}")
        print(f"{'='*60}")

        # Every book type now requires a template
        template_path = workspace / bt_cfg["template"]
        if not template_path.exists():
            print(f"  🚫 Template not found: {bt_cfg['template']}")
            print(f"     Skipping {bt_pretty}.")
            continue

        for slug in state_slugs:
            state_name = config.state_display_names[slug]

            if bt_key in CHAPTER_TEMPLATE_TYPES:
                # ── Chapter/topic template-based generation ─────────────
                content = generate_from_template(
                    template_path, bt_key, slug, state_name, config,
                )
            elif bt_key == "in_30_days":
                # ── 30-day template-based generation ────────────────────
                content = generate_in_30_days_from_template(
                    template_path, slug, state_name, config,
                )
            elif bt_key.endswith("_practice_tests"):
                # ── Practice tests (template-based) ─────────────────────
                num_tests = int(bt_key.split("_")[0])  # 3, 5, 7, etc.
                test_start, test_end = bt_cfg["test_range"]
                content = generate_practice_tests_from_template(
                    template_path, slug, state_name,
                    num_tests, test_start, test_end,
                    workspace, config,
                )
            else:
                print(f"  🚫 Unknown book type: {bt_key}")
                total_skipped += 1
                continue

            # ── Inject state-specific title / subtitle ───────────────────
            content = inject_titles_into_tex(
                content, bt_key, slug, state_name, titles,
            )

            out_path = write_state_book(
                workspace, slug, bt_key, content, dry_run=args.dry_run,
            )
            total_generated += 1

            if args.verbose or args.dry_run:
                rel = out_path.relative_to(workspace)
                action = "Would write" if args.dry_run else "Wrote"
                # Count customizations
                n_mod = len(config.state_modified.get(slug, {}))
                n_add = len(config.state_additional.get(slug, []))
                custom_info = ""
                if n_mod or n_add:
                    custom_info = f" [{n_mod} modified, {n_add} additional]"
                print(f"  ✅ {action}: {rel}{custom_info}")

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    action = "Would generate" if args.dry_run else "Generated"
    print(f"✅ {action} {total_generated} .tex files")
    if total_skipped:
        print(f"⚠️  Skipped {total_skipped} files")

    # List customized states
    customized = sorted(
        set(list(config.state_additional.keys()) + list(config.state_modified.keys()))
    )
    ccss_only = len(config.all_state_slugs) - len(customized)
    print(f"   • {len(customized)} customized states: "
          f"{', '.join(config.state_display_names[s] for s in customized)}")
    print(f"   • {ccss_only} CCSS-only states (identical content)")


if __name__ == "__main__":
    main()


# ============================================================================
# USAGE FROM PROJECT ROOT
# ============================================================================
#
# 1. Generate all-in-one for all 50 states:
#    $ python3 scripts/generate_state_books.py --book-type all_in_one
#
# 2. Generate brief study guides for all 50 states:
#    $ python3 scripts/generate_state_books.py --book-type study_guide
#
# 3. Generate all book types for all states:
#    $ python3 scripts/generate_state_books.py --book-type all
#
# 4. Generate for specific states only:
#    $ python3 scripts/generate_state_books.py --book-type all_in_one --states texas,virginia
#
# 5. Dry-run to preview what would be generated:
#    $ python3 scripts/generate_state_books.py --book-type all --dry-run --verbose
#
# 6. After generating, compile with:
#    $ python3 scripts/compile_state_books.py --book-type all_in_one
#
# ============================================================================
