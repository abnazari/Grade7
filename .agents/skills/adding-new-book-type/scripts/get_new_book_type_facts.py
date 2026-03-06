#!/usr/bin/env python3
"""
Return every fact an AI agent needs to add a new book type.

Usage:
    python3 .agents/skills/adding-new-book-type/scripts/get_new_book_type_facts.py <book_type>

Example:
    python3 .agents/skills/adding-new-book-type/scripts/get_new_book_type_facts.py study_guide

Prints a structured plain-text report with:
  - Grade & audience info
  - What files the agent must create / edit
  - Initial pages required and design guidance
  - config.py entries needed
  - Chapter & topic structure
  - Existing book types for reference

No Jinja, no HTML — just facts.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Resolve workspace & add scripts/ to sys.path ──────────────────────

def _find_workspace() -> Path:
    """Walk up from this file to find topics_config.yaml + studyGuide.cls."""
    candidate = Path(__file__).resolve().parent
    for _ in range(10):
        if (candidate / "topics_config.yaml").exists():
            return candidate
        candidate = candidate.parent
    print("ERROR: Could not find workspace root.", file=sys.stderr)
    sys.exit(1)


WORKSPACE = _find_workspace()
sys.path.insert(0, str(WORKSPACE / "scripts"))

import yaml  # noqa: E402
from config_loader import load_config, TopicsConfig  # noqa: E402
from config import (  # noqa: E402
    BOOK_TYPES,
    BOOK_DISPLAY_NAMES,
    GENERIC_BOOK_TITLES,
    GRADE_NUMBER,
    GRADE_SLUG,
    GRADE_DISPLAY,
)


# ============================================================================
# DATA LOADERS
# ============================================================================

def _load_yaml(name: str) -> dict:
    path = WORKSPACE / name
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_dotenv_raw() -> Dict[str, str]:
    """Read .env file into a dict (simple key=value parsing)."""
    env_path = WORKSPACE / ".env"
    result: Dict[str, str] = {}
    if not env_path.exists():
        return result
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                result[key.strip()] = value.strip()
    return result


# ============================================================================
# INITIAL PAGES ANALYSIS
# ============================================================================

def _scan_initial_pages_dir() -> Dict[str, List[str]]:
    """Return {subdir_name: [filenames]} for initial_pages/."""
    ip_root = WORKSPACE / "initial_pages"
    if not ip_root.exists():
        return {}
    result: Dict[str, List[str]] = {}
    for child in sorted(ip_root.iterdir()):
        if child.is_dir():
            files = sorted(f.name for f in child.iterdir() if f.suffix == ".tex")
            result[child.name] = files
    return result


def _parse_initial_page_includes(main_tex_path: Path) -> List[str]:
    """Extract \\input{initial_pages/...} paths from a main .tex file."""
    if not main_tex_path.exists():
        return []
    includes: List[str] = []
    with open(main_tex_path, "r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"\\input\{(initial_pages/[^}]+)\}", line)
            if m:
                includes.append(m.group(1))
    return includes


def _get_all_book_type_includes() -> Dict[str, List[str]]:
    """For each book type, return the list of initial_pages includes."""
    result: Dict[str, List[str]] = {}
    for bt_key, bt_cfg in BOOK_TYPES.items():
        template = bt_cfg.get("template", "")
        if template:
            main_path = WORKSPACE / template
            result[bt_key] = _parse_initial_page_includes(main_path)
    return result


def _read_file_first_comment(path: Path) -> str:
    """Read the first LaTeX comment block from a file as a description."""
    if not path.exists():
        return ""
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("%"):
                content = stripped.lstrip("% ").strip("=").strip()
                if content:
                    lines.append(content)
            elif stripped:
                break
    return " — ".join(lines[:2]) if lines else ""


# ============================================================================
# INITIAL PAGE TYPE DEFINITIONS
# ============================================================================

# Maps book-type category → the initial pages it needs.
# Each page: (filename_pattern, purpose, is_required, design_notes)
# The agent uses this to know what files to create.

INITIAL_PAGE_SPECS: Dict[str, List[Dict[str, Any]]] = {
    "topic_based": [
        {
            "file": "00-welcome.tex",
            "purpose": "Welcome / splash page — the FIRST thing buyers see in the online preview",
            "required": True,
            "design": (
                "Full-page design using tikzpicture[remember picture, overlay]. "
                "Must include: book title, grade level, tagline with bullet-separated features, "
                "and a welcome message. Use the book type's brand color. "
                "This page becomes the first TPT thumbnail — make it visually stunning."
            ),
        },
        {
            "file": "01-how-to-use.tex",
            "purpose": "Explains how the book is structured and how to use it effectively",
            "required": True,
            "design": (
                "3–4 numbered steps in tcolorbox cards, each with a different accent color. "
                "Use numbered circles (tikz nodes) on the left of each card. "
                "Include a suggestions/tips box at the bottom."
            ),
        },
    ],
    "practice_tests": [
        {
            "file": "00-welcome.tex",
            "purpose": "Welcome / splash page for practice test book",
            "required": True,
            "design": (
                "Full-page tikzpicture design. Energetic theme with bold colors. "
                "Include the number of tests prominently. Use FontAwesome icons "
                "(\\faBolt, \\faStopwatch, etc.) for visual impact."
            ),
        },
        {
            "file": "01-how-to-use.tex",
            "purpose": "How to use the practice tests effectively",
            "required": True,
            "design": "Numbered steps for test-taking workflow. Include timing guidance.",
        },
        {
            "file": "02-test-strategies.tex",
            "purpose": "Test-taking strategies and tips",
            "required": True,
            "design": "Two-column layout with strategy cards. Use icons for visual appeal.",
        },
        {
            "file": "03-what-youll-need.tex",
            "purpose": "Supplies checklist for test day",
            "required": True,
            "design": "Checklist format with checkboxes. Include pencils, scratch paper, calculator policy.",
        },
        {
            "file": "06-my-test-tracker.tex",
            "purpose": "Score tracking table for all tests",
            "required": True,
            "design": "Table with columns: Test # | Score | % | Date. One row per test.",
        },
    ],
}


# Maps book_type → specific page 02 spec (so the agent gets only what it needs)
PAGE_02_BY_TYPE: Dict[str, Dict[str, Any]] = {
    "study_guide": {
        "file": "02-math-quick-reference.tex",
        "purpose": "Formula/fact reference cards for quick review",
        "required": True,
        "design": "8 formula/fact cards in 2-column multicols layout. Each card is a tcolorbox with a topic title and key formulas/facts.",
    },
    "step_by_step": {
        "file": "02-how-every-topic-works.tex",
        "purpose": "Visual breakdown of how each topic is structured",
        "required": True,
        "design": "Show the step-by-step format: concept → example → practice. Use numbered cards with different accent colors.",
    },
    "workbook": {
        "file": "02-math-quick-reference.tex",
        "purpose": "Formula reference cards for quick lookup during practice",
        "required": True,
        "design": "Formula cards in 2-column multicols. Focus on formulas students need while solving problems.",
    },
    "in_30_days": {
        "file": "02-your-30-day-plan.tex",
        "purpose": "30-day study schedule showing daily topic assignments",
        "required": True,
        "design": "30-row table with Day / Topic / Checkbox columns. Use alternating row colors from the brand palette.",
    },
    "quiz": {
        "file": "02-quiz-tracker.tex",
        "purpose": "Score tracking table for all quizzes",
        "required": True,
        "design": "Table with Topic / Score / % / Retake columns. One row per quiz topic.",
    },
    "puzzles": {
        "file": "02-puzzle-tracker.tex",
        "purpose": "Completion tracker for all puzzles",
        "required": True,
        "design": "Grid of completion checkboxes grouped by chapter. Use tcolorbox per chapter group.",
    },
    "worksheet": {
        "file": "02-formula-reference.tex",
        "purpose": "Formula reference sheet",
        "required": True,
        "design": "Two-column formula reference. Can reuse content from initial_pages/common/formula-reference.tex.",
    },
}

# Default page 02 spec for unknown book types
PAGE_02_DEFAULT: Dict[str, Any] = {
    "file": "02-<book-specific>.tex",
    "purpose": "Book-type-specific reference or overview page",
    "required": True,
    "design": "Content varies by type. Use multicols for dense content. Use tcolorbox for grouped sections. Never create a whats-inside page (chapter content is state-dependent).",
}


# ============================================================================
# COMMON PAGES THAT CAN BE REUSED
# ============================================================================

def _get_common_pages() -> List[Dict[str, str]]:
    """Return info about common initial pages available for reuse."""
    common_dir = WORKSPACE / "initial_pages" / "common"
    pages = []
    if common_dir.exists():
        for f in sorted(common_dir.iterdir()):
            if f.suffix == ".tex":
                desc = _read_file_first_comment(f)
                pages.append({"file": f.name, "description": desc})
    return pages


# ============================================================================
# CHAPTER & TOPIC SUMMARY
# ============================================================================

def _build_chapter_summary(config: TopicsConfig) -> List[Dict[str, Any]]:
    """Build chapter summary with topic names for the report."""
    chapters = []
    for ch in config.chapters:
        topics = []
        for t in ch.topics:
            topics.append({"id": t.id, "name": t.name, "file": t.file})
        chapters.append({
            "num": ch.num,
            "title": ch.title.replace("\\&", "&"),
            "topic_count": len(topics),
            "topics": topics,
        })
    return chapters


# ============================================================================
# COLOR PALETTE
# ============================================================================

def _get_color_palette() -> Dict[str, str]:
    """Read available color names from VMfunColors.sty."""
    colors_path = WORKSPACE / "VM_packages" / "VMfunColors.sty"
    palette: Dict[str, str] = {}
    if not colors_path.exists():
        return palette
    with open(colors_path, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\\definecolor\{(\w+)\}\{HTML\}\{(\w+)\}", line)
            if m:
                palette[m.group(1)] = f"#{m.group(2)}"
    return palette


# ============================================================================
# AUDIENCE & GRADE CONTEXT
# ============================================================================

GRADE_AUDIENCE: Dict[int, Dict[str, Any]] = {
    3: {
        "age_range": "8–9 years old",
        "description": "3rd graders",
        "tone": "Friendly, encouraging, playful. Use simple vocabulary. Kids at this level are building foundational skills.",
        "math_level": "Multiplication, division basics, fractions introduction, place value, measurement, basic geometry",
        "design_notes": "Bright colors, large fonts, lots of visual space. Consider fun characters or icons. Avoid dense text blocks.",
        "reference_pages": ["multiplication table (up to 12×12)", "number chart (1–120)", "place value chart"],
    },
    4: {
        "age_range": "9–10 years old",
        "description": "4th graders",
        "tone": "Encouraging and clear. Students are gaining independence. Use straightforward language with some math vocabulary.",
        "math_level": "Multi-digit operations, fractions, decimals introduction, factors & multiples, angles, area & perimeter",
        "design_notes": "Colorful but not childish. Clear structure with headers. Students can handle more text than Grade 3.",
        "reference_pages": ["multiplication table (up to 12×12)", "place value chart", "math symbols reference"],
    },
    5: {
        "age_range": "10–11 years old",
        "description": "5th graders",
        "tone": "Supportive and direct. Students are becoming more analytical. Use proper math vocabulary with brief explanations.",
        "math_level": "Decimal operations, fraction operations, volume, coordinate plane introduction, order of operations, algebraic thinking",
        "design_notes": "Professional but engaging. Students appreciate clean layouts. Can handle two-column formats and reference tables.",
        "reference_pages": ["multiplication table", "math symbols & vocabulary", "number chart", "place value chart"],
    },
    6: {
        "age_range": "11–12 years old",
        "description": "6th graders",
        "tone": "Confident and academic but approachable. Students are transitioning to middle school. Use standard math terminology.",
        "math_level": "Ratios & rates, the number system (integers, rational numbers), expressions & equations, geometry (area, volume, surface area), statistics & data",
        "design_notes": "Clean, modern design. Light colored backgrounds for print-friendliness. Students can handle dense reference pages. Two-column layouts work well.",
        "reference_pages": ["formula reference sheet", "key vocabulary", "math quick reference"],
    },
    7: {
        "age_range": "12–13 years old",
        "description": "7th graders",
        "tone": "Direct, academic, respectful. Students expect to be treated maturely. Use precise mathematical language.",
        "math_level": "Proportional relationships, operations with rational numbers, expressions & equations (multi-step), geometry (scale, circles, angles), probability & statistics",
        "design_notes": "Professional and mature. Minimal decoration. Focus on clear typesetting and information density.",
        "reference_pages": ["formula reference sheet", "key vocabulary"],
    },
    8: {
        "age_range": "13–14 years old",
        "description": "8th graders",
        "tone": "Academic and concise. Students preparing for high school. Formal mathematical register.",
        "math_level": "Linear equations, functions, systems of equations, transformations, Pythagorean theorem, volume of cones/cylinders/spheres, scatter plots",
        "design_notes": "Mature, textbook-quality design. Dense content is fine. Minimal illustration — focus on clarity.",
        "reference_pages": ["formula reference sheet", "key vocabulary"],
    },
}


# ============================================================================
# BOOK TYPE CATEGORY DETECTOR
# ============================================================================

def _book_type_category(book_type: str) -> str:
    """Classify a book type for initial page selection."""
    if book_type.endswith("_practice_tests"):
        return "practice_tests"
    return "topic_based"


def _book_type_has_topics(book_type: str) -> bool:
    """Whether this book type uses topic directories."""
    cfg = BOOK_TYPES.get(book_type, {})
    return "topic_dirs" in cfg


def _book_type_has_tests(book_type: str) -> bool:
    """Whether this book type uses practice test ranges."""
    cfg = BOOK_TYPES.get(book_type, {})
    return "test_range" in cfg


# ============================================================================
# EXISTING BOOK TYPES REFERENCE
# ============================================================================

def _summarise_existing_book_types() -> List[Dict[str, Any]]:
    """Return summary of all existing book types for cross-reference."""
    all_includes = _get_all_book_type_includes()
    summaries = []
    for bt_key, bt_cfg in BOOK_TYPES.items():
        includes = all_includes.get(bt_key, [])
        # Separate own pages from common/shared pages
        own_pages = [p for p in includes if f"initial_pages/{bt_key}/" in p
                     or f"initial_pages/{bt_key.replace('_practice_tests', '')}/" in p]
        common_pages = [p for p in includes if "initial_pages/common/" in p]
        shared_pages = [p for p in includes if p not in own_pages and p not in common_pages]

        summaries.append({
            "key": bt_key,
            "display_name": BOOK_DISPLAY_NAMES.get(bt_key, bt_key),
            "template": bt_cfg.get("template", ""),
            "has_topics": "topic_dirs" in bt_cfg,
            "has_tests": "test_range" in bt_cfg,
            "initial_pages": includes,
            "own_page_count": len(own_pages),
            "common_page_count": len(common_pages),
            "shared_page_count": len(shared_pages),
        })
    return summaries


# ============================================================================
# MAIN: PRINT FACTS
# ============================================================================

def print_facts(book_type: str) -> None:
    config = load_config(WORKSPACE)

    # Category
    category = _book_type_category(book_type)
    has_topics = _book_type_has_topics(book_type)
    has_tests = _book_type_has_tests(book_type)

    # Get existing config if book type already exists (partial setup)
    existing_cfg = BOOK_TYPES.get(book_type, {})
    already_exists = book_type in BOOK_TYPES

    # Grade & audience
    grade = GRADE_NUMBER
    audience = GRADE_AUDIENCE.get(grade, GRADE_AUDIENCE.get(6, {}))

    # Topic/chapter structure
    chapters = _build_chapter_summary(config)
    total_topics = sum(ch["topic_count"] for ch in chapters)

    # Common pages
    common_pages = _get_common_pages()

    # Existing book types for reference
    existing_types = _summarise_existing_book_types()

    # Initial page specs — build with type-specific page 02
    base_specs = INITIAL_PAGE_SPECS.get(category, INITIAL_PAGE_SPECS["topic_based"])
    page_02 = PAGE_02_BY_TYPE.get(book_type, PAGE_02_DEFAULT)
    # For practice_tests, page 02 is already in the base specs
    if category == "practice_tests":
        page_specs = base_specs
    else:
        page_specs = list(base_specs) + [page_02]

    # All includes across book types (for cross-reference)
    all_includes = _get_all_book_type_includes()

    # Current initial pages for this book type (if dir exists)
    ip_dir = WORKSPACE / "initial_pages"
    bt_folder = book_type
    # Handle practice test variants
    if book_type.endswith("_practice_tests"):
        num = book_type.split("_")[0]
        bt_folder = f"practice_tests_{num}"

    existing_ip_files: List[str] = []
    if (ip_dir / bt_folder).exists():
        existing_ip_files = sorted(
            f.name for f in (ip_dir / bt_folder).iterdir() if f.suffix == ".tex"
        )

    # ── Print the report ────────────────────────────────────────────────
    print("=" * 70)
    print(f"NEW BOOK TYPE SETUP FACTS: {book_type}")
    print("=" * 70)

    # --- GRADE & AUDIENCE ---
    print()
    print("=" * 70)
    print("GRADE & AUDIENCE")
    print("=" * 70)
    print(f"Grade Number:       {grade}")
    print(f"Grade Slug:         {GRADE_SLUG}")
    print(f"Grade Display:      {GRADE_DISPLAY}")
    print(f"Audience:           {audience.get('description', '')}")
    print(f"Age Range:          {audience.get('age_range', '')}")
    print(f"Tone Guide:         {audience.get('tone', '')}")
    print(f"Math Level:         {audience.get('math_level', '')}")
    print(f"Design Notes:       {audience.get('design_notes', '')}")
    print(f"Suggested Ref Pages: {', '.join(audience.get('reference_pages', []))}")

    # --- BOOK TYPE STATUS ---
    print()
    print("=" * 70)
    print("BOOK TYPE STATUS")
    print("=" * 70)
    print(f"Book Type Key:      {book_type}")
    print(f"Category:           {category}")
    print(f"Has Topics:         {has_topics}")
    print(f"Has Practice Tests: {has_tests}")
    print(f"Already in Config:  {already_exists}")
    if already_exists:
        print(f"Template File:      {existing_cfg.get('template', '')}")
        print(f"Output Subdir:      {existing_cfg.get('output_subdir', '')}")
        if has_topics:
            dirs = existing_cfg.get("topic_dirs", ())
            print(f"Topic Dirs:         {dirs}")
        if has_tests:
            print(f"Test Range:         {existing_cfg.get('test_range', '')}")
    display_name = BOOK_DISPLAY_NAMES.get(book_type, "(NOT SET)")
    print(f"Display Name:       {display_name}")
    titles = GENERIC_BOOK_TITLES.get(book_type)
    if titles:
        print(f"Generic Title:      {titles[0]}")
        print(f"Generic Subtitle:   {titles[1]}")
    else:
        print("Generic Title:      (NOT SET — must add to GENERIC_BOOK_TITLES)")
        print("Generic Subtitle:   (NOT SET — must add to GENERIC_BOOK_TITLES)")

    # --- FILES TO CREATE / EDIT ---
    print()
    print("=" * 70)
    print("FILES TO CREATE / EDIT")
    print("=" * 70)

    template_file = existing_cfg.get("template", f"{book_type}_main.tex")
    template_exists = (WORKSPACE / template_file).exists()

    print()
    print("1. MAIN TEMPLATE FILE")
    print(f"   Path: {template_file}")
    print(f"   Exists: {template_exists}")
    if not template_exists:
        print("   ACTION: Create this file. Use an existing *_main.tex as reference.")
        print("   It must include:")
        print("     - \\documentclass[12pt, fleqn, openany]{studyGuide}")
        print("     - Cover page section (\\StateName, \\CoverImage, \\makeCoverPage)")
        print("     - Initial pages section (\\input{initial_pages/...})")
        print("     - Chapter/topic inputs OR practice test inputs")
        print("     - \\printAnswerKey at the end")
    else:
        print("   STATUS: Already exists. Review initial pages section.")

    print()
    print("2. INITIAL PAGES DIRECTORY")
    print(f"   Path: initial_pages/{bt_folder}/")
    print(f"   Exists: {(ip_dir / bt_folder).exists()}")
    if existing_ip_files:
        print(f"   Existing files: {', '.join(existing_ip_files)}")
    else:
        print("   ACTION: Create this directory and all required initial page files.")

    # Show what initial pages to create
    print()
    print("   REQUIRED INITIAL PAGES TO WRITE:")
    for spec in page_specs:
        print(f"   ── {spec['file']} {'(REQUIRED)' if spec['required'] else '(OPTIONAL)'}")
        print(f"      Purpose: {spec['purpose']}")
        design_lines = spec["design"].split("\n")
        for dl in design_lines:
            print(f"      Design:  {dl.strip()}")

    print()
    print("3. COMMON PAGES (available for reuse — already exist)")
    for cp in common_pages:
        print(f"   • initial_pages/common/{cp['file']}")
        if cp["description"]:
            print(f"     {cp['description']}")

    print()
    print("4. COVER IMAGE")
    cover_path = WORKSPACE / "images" / "covers" / f"{book_type}.png"
    print(f"   Path: images/covers/{book_type}.png")
    print(f"   Exists: {cover_path.exists()}")
    if not cover_path.exists():
        print("   NOTE: Cover image must be provided by the graphic designer.")
        print("   The agent cannot create this — just note it as a dependency.")

    if not already_exists:
        print()
        print("5. CONFIG ENTRIES (scripts/config.py)")
        print("   ACTION: Add entries to the following dictionaries:")
        print(f"   a) BOOK_TYPES['{book_type}'] = {{")
        print(f'       "template": "{book_type}_main.tex",')
        print(f'       "output_subdir": "{book_type}",')
        print(f'       "description": "...",')
        if has_topics:
            print(f'       "topic_dirs": ("topics_{book_type}", "topics_{book_type}_modified", "topics_{book_type}_additional"),')
        if has_tests:
            print(f'       "test_range": (START, END),')
        print("   }")
        print(f'   b) BOOK_DISPLAY_NAMES["{book_type}"] = "..."')
        print(f'   c) GENERIC_BOOK_TITLES["{book_type}"] = ("...", "...")')
        print(f'   d) _TITLE_TEMPLATES["{book_type}"] = ("...", "...")')
        print(f'   e) _TPT_TIERS["{book_type}"] = {{"titles": [...], "subtitles": [...]}}')

    print()
    print("6. GENERATE_STATE_BOOKS.PY — TOPIC_DIR_MAP")
    if has_topics:
        print("   ACTION: Add entry to TOPIC_DIR_MAP in scripts/generate_state_books.py")
        print(f'   "{book_type}": ("topics_{book_type}", "topics_{book_type}_modified", "topics_{book_type}_additional"),')
    else:
        print("   Not applicable (practice test books don't use TOPIC_DIR_MAP).")

    if has_topics:
        print()
        print("7. TOPIC DIRECTORIES")
        topic_dirs = existing_cfg.get("topic_dirs", ())
        if topic_dirs:
            for td in topic_dirs:
                td_path = WORKSPACE / td
                exists = td_path.exists()
                count = len(list(td_path.glob("*.tex"))) if exists else 0
                print(f"   • {td}/ — {'exists' if exists else 'MISSING'}"
                      f"{f' ({count} .tex files)' if exists else ''}")
        else:
            print(f"   ACTION: Create topic directories:")
            print(f"     • topics_{book_type}/")
            print(f"     • topics_{book_type}_modified/  (for state-specific overrides)")
            print(f"     • topics_{book_type}_additional/  (for state-specific extras)")

    # --- CHAPTER & TOPIC STRUCTURE ---
    print()
    print("=" * 70)
    print("CHAPTER & TOPIC STRUCTURE")
    print("=" * 70)
    print(f"Total Chapters:     {len(chapters)}")
    print(f"Total Core Topics:  {total_topics}")
    print()
    for ch in chapters:
        print(f"  Chapter {ch['num']}: {ch['title']} — {ch['topic_count']} topics")
        for t in ch["topics"]:
            print(f"    • {t['id']}: {t['name']} (file: {t['file']})")

    # --- DESIGN GUIDANCE ---
    print()
    print("=" * 70)
    print("DESIGN GUIDANCE FOR INITIAL PAGES")
    print("=" * 70)
    print()
    print("TARGET: TeachersPayTeachers.com (TPT) listings")
    print("The first 3 initial pages (welcome, how-to-use, reference/overview)")
    print("become thumbnail images in the TPT product listing.")
    print("They MUST be visually stunning and sell the book at a glance.")
    print()
    print("PRINT-FRIENDLY RULES:")
    print("  • Use VERY LIGHT background colors (e.g. funTealLight, funBlueLight)")
    print("  • Use DARK colored fonts (e.g. funTealDark, funBlueDark)")
    print("  • NEVER use black!N patterns (e.g. black!15, black!50)")
    print("  • Backgrounds must look good when printed on standard white paper")
    print("  • Teachers will print these — ink-heavy designs are unacceptable")
    print()
    print("COLOR SCHEME:")
    print("  Each book type should have a PRIMARY brand color.")
    print("  Use that color's Light variant for backgrounds and Dark variant for text.")
    print("  Use 2–3 accent colors from the palette for variety.")

    print()
    print("PAGE STRUCTURE CONVENTIONS:")
    print("  • Every page starts with \\thispagestyle{empty}")
    print("  • Every page ends with \\clearpage")
    print("  • Use \\sffamily for sans-serif body text in initial pages")
    print("  • Headers: \\fontsize{22}{26}\\selectfont\\bfseries\\color{...}")
    print("  • Subtitles: \\normalsize\\color{funGray}")
    print("  • Accent rules: \\rule{0.55\\textwidth}{1pt} in light brand color")
    print("  • \\vspace{} for spacing (not blank lines)")

    # --- EXISTING BOOK TYPES REFERENCE ---
    print()
    print("=" * 70)
    print("EXISTING BOOK TYPES — INITIAL PAGE PATTERNS")
    print("=" * 70)
    for bt_info in existing_types:
        key = bt_info["key"]
        includes = bt_info["initial_pages"]
        print(f"\n  {key} ({bt_info['display_name']})")
        print(f"  Template: {bt_info['template']}")
        print(f"  Pages: {bt_info['own_page_count']} own + {bt_info['common_page_count']} common"
              f" + {bt_info['shared_page_count']} shared")
        for inc in includes:
            print(f"    \\input{{{inc}}}")

    print()
    print("=" * 70)
    print("END OF FACTS")
    print("=" * 70)


# ============================================================================
# CLI
# ============================================================================

KNOWN_TYPES = list(BOOK_TYPES.keys())


def print_usage():
    print("Usage: python3 get_new_book_type_facts.py <book_type>")
    print()
    print("Prints all facts an AI agent needs to add or complete a new book type.")
    print()
    print("Existing book types (for reference/completion):")
    for bt in KNOWN_TYPES:
        print(f"  {bt}")
    print()
    print("For a completely new book type, pass any key name:")
    print("  python3 get_new_book_type_facts.py my_new_book")
    print()
    print("Options:")
    print("  --list-types    List all existing book types")
    print("  --help, -h      Show this help")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ("--help", "-h"):
        print_usage()
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--list-types":
        for bt in KNOWN_TYPES:
            display = BOOK_DISPLAY_NAMES.get(bt, bt)
            print(f"  {bt:25s}  {display}")
        sys.exit(0)

    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    print_facts(sys.argv[1])
