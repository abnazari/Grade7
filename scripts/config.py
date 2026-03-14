"""
Centralized configuration for all Grade 7 book generation and compilation scripts.

Single source of truth for:
  - Book type definitions (templates, output dirs, test ranges, topic dirs)
  - Book display names and title generation (with state exam & curriculum info)
  - Preview book type definitions
  - Filename helpers (tex, pdf, preview)
  - Workspace detection (re-exported from config_loader)

Every script in scripts/ imports from here instead of defining its own
BOOK_TYPES, TOPIC_DIR_MAP, ALL_STATE_SLUGS, filename helpers, etc.
"""

import os
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Re-export workspace finder so callers don't need two imports
from config_loader import find_workspace  # noqa: F401


# ============================================================================
# .env FILE LOADER  (no external dependencies)
# ============================================================================

def _load_dotenv() -> None:
    """Load .env file from workspace root into os.environ.

    Real environment variables take priority — .env only fills in missing keys.
    The parser handles blank lines, ``#`` comments, and optional quotes.
    Silently skips if the workspace or .env file can't be found.
    """
    try:
        ws = find_workspace()
    except SystemExit:
        return
    env_path = ws / ".env"
    if not env_path.is_file():
        return
    with open(env_path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Strip surrounding quotes
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            # Real env vars take priority over .env values
            os.environ.setdefault(key, value)


_load_dotenv()


# ============================================================================
# BOOK TYPE DEFINITIONS  — single source of truth
# ============================================================================
# Each entry maps a book-type key to ALL metadata used by any script:
#
#   template      — main .tex template file in workspace root
#   output_subdir — sub-folder under final_output/ for compiled PDFs
#   description   — human-readable description (for CLI help & logs)
#   test_range    — (start, end) test numbers (practice-test books only)
#   topic_dirs    — (core, modified, additional) directory names
#                   for chapter/topic-based template generators
#
# Fields may be None/absent when not applicable to a book type.

BOOK_TYPES: Dict[str, dict] = {
    "all_in_one": {
        "template": "all_in_one_main.tex",
        "output_subdir": "all_in_one",
        "description": "Comprehensive all-in-one with lessons, warmups & practice (~450 pages)",
        "topic_dirs": ("topics", "topics_modified", "topics_additional"),
    },
    "study_guide": {
        "template": "study_guide_main.tex",
        "output_subdir": "study_guide",
        "description": "Brief study guide focused on core concepts (~130 pages)",
        "topic_dirs": ("topics", "topics_modified", "topics_additional"),
    },
    "workbook": {
        "template": "workbook_main.tex",
        "output_subdir": "workbook",
        "description": "Practice workbook with problems for every topic",
        "topic_dirs": ("topics_workbook", "topics_workbook_modified", "topics_workbook_additional"),
    },
    "step_by_step": {
        "template": "steps_main.tex",
        "output_subdir": "step_by_step",
        "description": "Step-by-step study guide — learn math one step at a time",
        "topic_dirs": ("steps_topics", "steps_topics_modified", "steps_topics_additional"),
    },
    "3_practice_tests": {
        "template": "3_practice_tests_main.tex",
        "output_subdir": "3_practice_tests",
        "description": "3 full-length practice tests",
        "test_range": (1, 3),
    },
    "5_practice_tests": {
        "template": "5_practice_tests_main.tex",
        "output_subdir": "5_practice_tests",
        "description": "5 full-length practice tests",
        "test_range": (4, 8),
    },
    "7_practice_tests": {
        "template": "7_practice_tests_main.tex",
        "output_subdir": "7_practice_tests",
        "description": "7 full-length practice tests",
        "test_range": (9, 15),
    },
    "10_practice_tests": {
        "template": "10_practice_tests_main.tex",
        "output_subdir": "10_practice_tests",
        "description": "10 full-length practice tests",
        "test_range": (16, 25),
    },
    "6_practice_tests": {
        "template": "6_practice_tests_main.tex",
        "output_subdir": "6_practice_tests",
        "description": "6 full-length practice tests (bank 2)",
        "test_range": (1, 6),
        "practice_dir": "practice_tests_2",
    },
    "9_practice_tests": {
        "template": "9_practice_tests_main.tex",
        "output_subdir": "9_practice_tests",
        "description": "9 full-length practice tests (bank 2)",
        "test_range": (7, 15),
        "practice_dir": "practice_tests_2",
    },
    "12_practice_tests": {
        "template": "12_practice_tests_main.tex",
        "output_subdir": "12_practice_tests",
        "description": "12 full-length practice tests (bank 2)",
        "test_range": (16, 27),
        "practice_dir": "practice_tests_2",
    },
    "in_30_days": {
        "template": "in30days_main.tex",
        "output_subdir": "in_30_days",
        "description": "30-day calendar-based study guide",
        "topic_dirs": ("topics_in30days", "topics_in30days_modified", "topics_in30days_additional"),
    },
    "quiz": {
        "template": "quiz_main.tex",
        "output_subdir": "quiz",
        "description": "Quick 15-minute quizzes — one per topic",
        "topic_dirs": ("topics_quiz", "topics_quiz_modified", "topics_quiz_additional"),
    },
    "puzzles": {
        "template": "puzzles_main.tex",
        "output_subdir": "puzzles",
        "description": "Puzzles, games & brain teasers aligned to the curriculum",
        "topic_dirs": ("topics_puzzles", "topics_puzzles_modified", "topics_puzzles_additional"),
    },
    "worksheet": {
        "template": "worksheet_main.tex",
        "output_subdir": "worksheet",
        "description": "Standalone printable worksheet activities for every topic",
        "topic_dirs": ("topics_worksheet", "topics_worksheet_modified", "topics_worksheet_additional"),
    },
}


# ============================================================================
# PREVIEW BOOK TYPE DEFINITIONS
# ============================================================================
# Preview variants share the same output_subdir as their full counterparts
# (preview PDFs get a "preview_" filename prefix instead).
# Generated automatically from BOOK_TYPES — no manual duplication.

PREVIEW_BOOK_TYPES: Dict[str, dict] = {
    f"preview_{key}": {
        "output_subdir": cfg["output_subdir"],
        "description": f"Preview — {cfg['description'].split('—')[0].strip() if '—' in cfg['description'] else cfg['description']}",
        **({"test_range": cfg["test_range"]} if "test_range" in cfg else {}),
    }
    for key, cfg in BOOK_TYPES.items()
}

# Combined dict used by compile_state_books.py for PDF routing
ALL_BOOK_TYPES: Dict[str, dict] = {**BOOK_TYPES, **PREVIEW_BOOK_TYPES}


# ============================================================================
# DERIVED HELPERS
# ============================================================================

# Book types that use the generic chapter/topic template generator
# (as opposed to in_30_days or practice tests which have special generators)
CHAPTER_TEMPLATE_TYPES = {
    key for key, cfg in BOOK_TYPES.items()
    if "topic_dirs" in cfg and key != "in_30_days"
}

# Practice test editions — derived from BOOK_TYPES so they stay in sync
PRACTICE_TEST_EDITIONS: List[int] = sorted(
    int(key.split("_")[0])
    for key in BOOK_TYPES
    if key.endswith("_practice_tests")
)

# All non-preview book type keys
NON_PREVIEW_KEYS: List[str] = list(BOOK_TYPES.keys())

# All preview book type keys
PREVIEW_KEYS: List[str] = list(PREVIEW_BOOK_TYPES.keys())


# ============================================================================
# RUNTIME SETTINGS  (overridable via .env or environment variables)
# ============================================================================
# These provide sensible defaults.  CLI flags (e.g. --jobs) always win;
# env vars / .env let you change defaults without touching code.

# Maximum concurrent pdflatex processes
MAX_WORKERS: int = int(os.environ.get(
    "MAX_WORKERS", str(max(1, (os.cpu_count() or 4) - 1))
))

# Default number of pdflatex passes per book
PDFLATEX_PASSES: int = int(os.environ.get("PDFLATEX_PASSES", "2"))

# Backward-compat alias used by compile_preview_books / validate_topic_compilation
XELATEX_PASSES: int = PDFLATEX_PASSES

# TeX Live year — used to locate TEXMFCNF system paths.
# Auto-detect from the installed texlive directory if not set explicitly.
def _detect_texlive_year() -> str:
    """Return the TeX Live year from env, or auto-detect from /usr/local/texlive/."""
    explicit = os.environ.get("TEXLIVE_YEAR")
    if explicit:
        return explicit
    texlive_base = Path("/usr/local/texlive")
    if texlive_base.is_dir():
        # Find the highest numeric year directory
        years = sorted(
            (d.name for d in texlive_base.iterdir()
             if d.is_dir() and d.name.isdigit()),
            reverse=True,
        )
        if years:
            return years[0]
    return "2025"  # fallback

TEXLIVE_YEAR: str = _detect_texlive_year()


# ============================================================================
# INTERACTIVE PROMPTS  — for running scripts with no CLI arguments
# ============================================================================
# These helpers let any script present a numbered menu when the user omits
# required arguments (e.g. --book-type).  They read from stdin so they work
# in any terminal.

def prompt_choice(
    prompt_text: str,
    choices: List[str],
    *,
    descriptions: Optional[Dict[str, str]] = None,
    allow_all: bool = True,
    all_label: str = "all",
) -> str:
    """Display a numbered menu and return the user's choice string.

    Parameters
    ----------
    prompt_text : str
        Header text printed before the menu.
    choices : list[str]
        Selectable option keys (e.g. book type keys or state slugs).
    descriptions : dict[str, str] | None
        Optional mapping of choice key → description shown beside it.
    allow_all : bool
        If True, an "all" option is prepended to the list.
    all_label : str
        Label used for the "all" option (e.g. "all", "all_previews").

    Returns the selected choice string (or *all_label* if the user picks "all").
    """
    menu: List[Tuple[int, str, str]] = []
    idx = 1
    if allow_all:
        menu.append((idx, all_label, "All options"))
        idx += 1
    for key in choices:
        desc = (descriptions or {}).get(key, "")
        menu.append((idx, key, desc))
        idx += 1

    print(f"\n{prompt_text}")
    print("-" * 50)
    for num, key, desc in menu:
        label = f"  {num:>3}) {key}"
        if desc:
            label += f"  — {desc}"
        print(label)
    print()

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
        match = [m for m in menu if m[0] == num]
        if match:
            selected = match[0][1]
            print(f"  → {selected}")
            return selected
        print(f"  Invalid choice. Enter 1–{len(menu)}.")


def prompt_states(all_state_slugs: List[str]) -> Optional[str]:
    """Ask the user whether to compile all states or pick specific ones.

    Returns
    -------
    None   — user chose "all states" (caller should use the full list)
    str    — comma-separated slugs the user typed
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
        return ",".join(slugs)


def prompt_book_type(
    choices: List[str],
    *,
    descriptions: Optional[Dict[str, str]] = None,
    allow_all: bool = True,
    allow_all_previews: bool = False,
) -> str:
    """Interactively ask the user to pick a book type.

    Returns the selected book type key (or "all" / "all_previews").
    """
    meta: List[str] = []
    if allow_all:
        meta.append("all")
    if allow_all_previews:
        meta.append("all_previews")

    menu: List[Tuple[int, str, str]] = []
    idx = 1
    for label in meta:
        menu.append((idx, label, "All book types" if label == "all" else "All preview variants"))
        idx += 1
    descs = descriptions or {k: v.get("description", "") for k, v in BOOK_TYPES.items()}
    for key in choices:
        desc = descs.get(key, "")
        menu.append((idx, key, desc))
        idx += 1

    print("\nBook type:")
    print("-" * 50)
    for num, key, desc in menu:
        label = f"  {num:>3}) {key}"
        if desc:
            label += f"  — {desc}"
        print(label)
    print()

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
        match = [m for m in menu if m[0] == num]
        if match:
            selected = match[0][1]
            print(f"  → {selected}")
            return selected
        print(f"  Invalid choice. Enter 1–{len(menu)}.")


# ============================================================================
# TOPIC DIRECTORY HELPERS
# ============================================================================

def get_topic_dirs(book_type: str) -> Tuple[str, str, str]:
    """Return (core_dir, modified_dir, additional_dir) for a book type.

    Raises KeyError if the book type has no topic directories
    (e.g. practice test books).
    """
    cfg = BOOK_TYPES[book_type]
    dirs = cfg.get("topic_dirs")
    if dirs is None:
        raise KeyError(f"Book type '{book_type}' has no topic_dirs")
    return dirs


# ============================================================================
# FILENAME HELPERS
# ============================================================================

def tex_filename(book_type: str, state_slug: str) -> str:
    """e.g. study_guide_texas-grade7.tex"""
    return f"{book_type}_{state_slug}-grade7.tex"


def pdf_filename_dated(book_type: str, state_slug: str) -> str:
    """e.g. study_guide_texas-grade7_2026-02-10.pdf"""
    today = date.today().isoformat()
    return f"{book_type}_{state_slug}-grade7_{today}.pdf"


def preview_tex_filename(book_type: str, state_slug: str) -> str:
    """e.g. preview_study_guide_texas-grade7.tex"""
    return f"preview_{book_type}_{state_slug}-grade7.tex"


# ============================================================================
# BOOK DISPLAY NAMES  — single source of truth
# ============================================================================
# Human-readable short names for each book type.  Used in product titles,
# WooCommerce listings, TPT descriptions, and marketing copy.  Every script
# should import from here instead of maintaining its own copy.

BOOK_DISPLAY_NAMES: Dict[str, str] = {
    "all_in_one": "All-in-One",
    "study_guide": "Study Guide",
    "workbook": "Workbook",
    "step_by_step": "Step-by-Step",
    "3_practice_tests": "3 Practice Tests",
    "5_practice_tests": "5 Practice Tests",
    "7_practice_tests": "7 Practice Tests",
    "10_practice_tests": "10 Practice Tests",
    "6_practice_tests": "6 Practice Tests",
    "9_practice_tests": "9 Practice Tests",
    "12_practice_tests": "12 Practice Tests",
    "in_30_days": "Math in 30 Days",
    "quiz": "Quizzes",
    "puzzles": "Puzzles & Brain Teasers",
    "worksheet": "Worksheets",
}


# ============================================================================
# GENERIC BOOK TITLES  — single source of truth for copyright pages
# ============================================================================
# These are the non-state-specific titles and subtitles used on the copyright
# pages of the main template .tex files (before state customisation).
# Subtitles use raw strings — LaTeX line-breaks (\\) are added by the
# template .tex files themselves for visual formatting.
#
# State-specific titles (with exam names) come from _TITLE_TEMPLATES below.
# The generate_state_books.py pipeline replaces \VMBookTitle / \VMBookSubtitle
# in each state .tex file via inject_titles_into_tex().

GENERIC_BOOK_TITLES: Dict[str, Tuple[str, str]] = {
    "all_in_one": (
        "Grade 7 Math Made Clear",
        "The Complete All-in-One Guide with Lessons, Examples, and Practice",
    ),
    "study_guide": (
        "Grade 7 Math Made Easy",
        "Study Guide with Key Concepts, Review & Practice",
    ),
    "workbook": (
        "Grade 7 Math Workbook",
        "Practice Problems & Exercises with Answer Key",
    ),
    "step_by_step": (
        "Grade 7 Math Step by Step",
        "A Beginner Friendly Guide to Learning Math",
    ),
    "3_practice_tests": (
        "3 Full-Length Grade 7 Math Practice Tests",
        "Test Prep with Detailed Answer Explanations",
    ),
    "5_practice_tests": (
        "5 Full-Length Grade 7 Math Practice Tests",
        "Extra Practice for Test Day Success",
    ),
    "7_practice_tests": (
        "7 Full-Length Grade 7 Math Practice Tests",
        "Comprehensive Test Prep with Detailed Answers",
    ),
    "10_practice_tests": (
        "10 Full-Length Grade 7 Math Practice Tests",
        "The Ultimate Test Prep Collection with Answer Explanations",
    ),
    "6_practice_tests": (
        "6 Full-Length Grade 7 Math Practice Tests",
        "Guided Test Prep with Tips, Strategies & Detailed Answers",
    ),
    "9_practice_tests": (
        "9 Full-Length Grade 7 Math Practice Tests",
        "Test Prep with Tips, Strategies & Answer Explanations",
    ),
    "12_practice_tests": (
        "12 Full-Length Grade 7 Math Practice Tests",
        "The Complete Guided Test Prep with Tips & Detailed Answer Keys",
    ),
    "in_30_days": (
        "Grade 7 Math in 30 Days",
        "A Day-by-Day Study Plan to Master Grade 7 Math",
    ),
    "quiz": (
        "Grade 7 Math Quizzes",
        "Quick Topic Assessments with Answer Key",
    ),
    "puzzles": (
        "Grade 7 Math Puzzles & Brain Teasers",
        "Fun Math Games, Activities & Challenges",
    ),
    "worksheet": (
        "Grade 7 Math Worksheets",
        "Printable Practice Pages with Answer Key",
    ),
}


def generic_book_title(book_type: str) -> str:
    """Return the generic (non-state) title for a book type.

    Used on copyright pages and for standalone (non-state) compilations.

    Examples:
        >>> generic_book_title("study_guide")
        'Grade 7 Math Made Easy'
        >>> generic_book_title("all_in_one")
        'Grade 7 Math Made Clear'
    """
    title, _ = GENERIC_BOOK_TITLES.get(
        book_type,
        (f"Grade 7 Math {book_type.replace('_', ' ').title()}", ""),
    )
    return title


def generic_book_subtitle(book_type: str) -> str:
    """Return the generic (non-state) subtitle for a book type.

    Used on copyright pages and for standalone (non-state) compilations.

    Examples:
        >>> generic_book_subtitle("study_guide")
        'Study Guide with Key Concepts, Review & Practice'
        >>> generic_book_subtitle("all_in_one")
        'The Complete All-in-One Guide with Lessons, Examples, and Practice'
    """
    _, subtitle = GENERIC_BOOK_TITLES.get(book_type, ("", ""))
    return subtitle


# ============================================================================
# GRADE-LEVEL SETTINGS  (from .env)
# ============================================================================

GRADE_NUMBER: int = int(os.environ.get("GRADE_NUMBER", "6"))
GRADE_SLUG: str = os.environ.get("GRADE_SLUG", "grade7")
GRADE_DISPLAY: str = os.environ.get("GRADE_DISPLAY", "Grade 7 Math")


# ============================================================================
# BOOK PRICES  (from .env — PRICE_<BOOK_TYPE_UPPER>=xx.xx)
# ============================================================================
# Example .env entries:
#   PRICE_ALL_IN_ONE=19.99
#   PRICE_3_PRACTICE_TESTS=5.99

BOOK_PRICES: Dict[str, str] = {
    book_type: os.environ.get(f"PRICE_{book_type.upper()}", "")
    for book_type in BOOK_TYPES
}


# ============================================================================
# STATE EXAM & CURRICULUM LOADERS
# ============================================================================

@lru_cache(maxsize=1)
def load_state_exams() -> Dict[str, Dict[str, str]]:
    """Load state_exams.yaml → {state_slug: {exam_name, exam_acronym, exam_months}}."""
    ws = find_workspace()
    path = ws / "state_exams.yaml"
    if not path.is_file():
        return {}
    with open(path) as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("states", {})


@lru_cache(maxsize=1)
def load_state_curriculums() -> Dict[str, Dict[str, str]]:
    """Load state_curriculums.yaml → {state_slug: {curriculum_name, curriculum_acronym}}."""
    ws = find_workspace()
    path = ws / "state_curriculums.yaml"
    if not path.is_file():
        return {}
    with open(path) as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("states", {})


def get_state_exam_info(state_slug: str) -> Dict[str, str]:
    """Return exam info dict for a state (exam_name, exam_acronym, exam_months).

    Returns empty dict if state not found.
    """
    return load_state_exams().get(state_slug, {})


def get_state_curriculum_info(state_slug: str) -> Dict[str, str]:
    """Return curriculum info dict for a state (curriculum_name, curriculum_acronym).

    Returns empty dict if state not found.
    """
    return load_state_curriculums().get(state_slug, {})


# ============================================================================
# BOOK TITLE GENERATION
# ============================================================================
# Generates SEO-optimised book titles modelled on top-selling competitor
# patterns from Amazon / TPT search results.
#
# Design principles:
#   - No "Edition" suffix — sounds generic
#   - No curriculum references in titles (curriculum info stays in subtitles)
#   - No em dashes separating title parts
#   - Alternate "Grade 7" vs "5th Grade" across book types for keyword variety
#   - Each of the 4 practice-test books uses a distinct keyword pattern
#   - Title + subtitle never repeat the same information
#
# Title examples:
#   "Texas STAAR Grade 7 Math All-in-One"
#   "5 Full-Length Texas STAAR Grade 7 Math Practice Tests"
#   "Alabama ACAP 5th Grade Math Workbook"
#   "10 California CAASPP Grade 7 Math Practice Tests"
#
# On TPT/Amazon, displayed as  "title: subtitle"  — so together they must
# read naturally and cover different keyword clusters.

# Per-book-type title templates.
# Placeholders: {state}, {exam}, {grade_n}, {ordinal}
# Each entry: (title_template, subtitle_template)
_TITLE_TEMPLATES: Dict[str, Tuple[str, str]] = {
    "all_in_one": (
        "{state} {exam} Grade {grade_n} Math All-in-One",
        "Complete Lessons, Examples, Practice & Answer Key",
    ),
    "study_guide": (
        "{state} {exam} Grade {grade_n} Math Made Easy",
        "Study Guide with Key Concepts, Review & Practice",
    ),
    "workbook": (
        "{state} {exam} Grade {grade_n} Math Workbook",
        "Practice Problems & Exercises with Answer Key",
    ),
    "step_by_step": (
        "{state} {exam} Grade {grade_n} Math Step by Step",
        "A Beginner Friendly Guide to Learning Math",
    ),
    "3_practice_tests": (
        "3 {state} {exam} Grade {grade_n} Math Practice Tests",
        "Full-Length Test Prep with Detailed Answer Explanations",
    ),
    "5_practice_tests": (
        "5 Full-Length {state} {exam} Grade {grade_n} Math Practice Tests",
        "Extra Practice for Test Day Success",
    ),
    "7_practice_tests": (
        "7 {state} {exam} Grade {grade_n} Math Practice Tests",
        "Comprehensive Test Prep with Detailed Answers",
    ),
    "10_practice_tests": (
        "10 {state} {exam} Grade {grade_n} Math Practice Tests",
        "The Ultimate Test Prep Collection with Answer Explanations",
    ),
    "6_practice_tests": (
        "6 {state} {exam} {ordinal} Grade Math Practice Tests",
        "Guided Test Prep with Tips, Strategies & Detailed Answers",
    ),
    "9_practice_tests": (
        "9 Full-Length {state} {exam} Grade {grade_n} Math Practice Tests",
        "Test Prep with Tips, Strategies & Answer Explanations",
    ),
    "12_practice_tests": (
        "12 {state} {exam} Grade {grade_n} Math Practice Tests",
        "The Complete Guided Test Prep with Tips & Detailed Answer Keys",
    ),
    "in_30_days": (
        "{state} {exam} Grade {grade_n} Math in 30 Days",
        "Day by Day Study Plan for Test Prep",
    ),
    "quiz": (
        "{state} {exam} Grade {grade_n} Math Quizzes",
        "Quick Topic Assessments with Answer Key",
    ),
    "puzzles": (
        "{state} {exam} Grade {grade_n} Math Puzzles and Brain Teasers",
        "Fun Math Games, Activities & Challenges",
    ),
    "worksheet": (
        "{state} {exam} Grade {grade_n} Math Worksheets",
        "Printable Practice Pages with Answer Key",
    ),
}

# ---------------------------------------------------------------------------
# TPT (Teachers Pay Teachers) title tiers — max 80 characters
# ---------------------------------------------------------------------------
# On TPT, the product title is displayed as "title: subtitle" but has an
# 80-character limit.  For each book type we define:
#
#   titles     — ordered title template variants (original first, then
#                progressively shorter alternatives where applicable)
#   subtitles  — progressively shorter subtitle variants (full first)
#
# book_tpt_title() tries every title × subtitle combination and picks the
# longest one that fits within 80 characters, maximising keyword coverage.
# If no "title: subtitle" combination fits, it falls back to title only.

_TPT_TIERS: Dict[str, Dict[str, list]] = {
    "all_in_one": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math All-in-One",
        ],
        "subtitles": [
            "Complete Lessons, Examples, Practice & Answer Key",  # 49
            "Lessons, Examples, Practice & Answer Key",           # 40
            "Lessons, Examples, Practice & Answers",              # 37
            "Lessons, Practice & Answer Key",                     # 30
            "Lessons, Practice & Answers",                        # 27
        ],
    },
    "study_guide": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math Made Easy",
        ],
        "subtitles": [
            "Study Guide with Key Concepts, Review & Practice",   # 49
            "Study Guide with Key Concepts & Practices",          # 42
            "Study Guide with Key Concepts & Practice",           # 40
            "Study Guide with Key Concepts",                      # 29
            "Study Guide & Practice",                             # 22
        ],
    },
    "workbook": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math Workbook",
        ],
        "subtitles": [
            "Practice Problems & Exercises with Answer Key",      # 46
            "Practice Problems & Exercises with Answers",         # 43
            "Practice & Exercises with Answer Key",               # 36
            "Practice Problems with Answer Key",                  # 33
            "Practice Problems & Answer Key",                     # 30
            "Practice with Answer Key",                           # 24
        ],
    },
    "step_by_step": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math Step by Step",
        ],
        "subtitles": [
            "A Beginner Friendly Guide to Learning Math",         # 43
            "Beginner Friendly Guide to Learning Math",           # 41
            "A Beginner's Guide to Learning Math",                # 35
            "Beginner's Guide to Learning Math",                  # 33
            "A Guide to Learning Math",                           # 24
        ],
    },
    "3_practice_tests": {
        "titles": [
            "3 {state} {exam} Grade {grade_n} Math Practice Tests",
        ],
        "subtitles": [
            "Full-Length Test Prep with Detailed Answer Explanations",  # 55
            "Full-Length Test Prep with Answer Explanations",           # 47
            "Test Prep with Detailed Answer Explanations",             # 44
            "Test Prep with Answer Explanations",                      # 34
            "Test Prep & Detailed Answers",                            # 28
            "Answers & Explanations",                                  # 22
        ],
    },
    "5_practice_tests": {
        "titles": [
            "5 Full-Length {state} {exam} Grade {grade_n} Math Practice Tests",
            "5 {state} {exam} Grade {grade_n} Math Practice Tests",
        ],
        "subtitles": [
            "Extra Practice for Test Day Success",                # 35
            "Extra Practice for Test Day",                        # 27
            "Extra Practice & Test Prep",                         # 26
            "Answers & Explanations",                             # 22
            "Answer Key Included",                                # 19
        ],
    },
    "7_practice_tests": {
        "titles": [
            "7 {state} {exam} Grade {grade_n} Math Practice Tests",
        ],
        "subtitles": [
            "Comprehensive Test Prep with Detailed Answers",      # 46
            "Comprehensive Test Prep with Answers",               # 36
            "Test Prep with Detailed Answers",                    # 31
            "Test Prep & Detailed Answers",                       # 28
            "Answers & Explanations",                             # 22
        ],
    },
    "10_practice_tests": {
        "titles": [
            "10 {state} {exam} Grade {grade_n} Math Practice Tests",
        ],
        "subtitles": [
            "The Ultimate Test Prep Collection with Answer Explanations",  # 58
            "Test Prep Collection with Answer Explanations",              # 46
            "Ultimate Test Prep with Answer Explanations",                # 43
            "Test Prep with Answer Explanations",                         # 34
            "Complete Test Prep with Answers",                            # 31
            "Answers & Explanations",                                     # 22
            "Answer Key Included",                                        # 19
        ],
    },
    "6_practice_tests": {
        "titles": [
            "6 {state} {exam} {ordinal} Grade Math Practice Tests",
        ],
        "subtitles": [
            "Guided Test Prep with Tips, Strategies & Detailed Answers",  # 55
            "Guided Test Prep with Tips & Detailed Answers",              # 44
            "Test Prep with Tips, Strategies & Answers",                  # 40
            "Test Prep with Tips & Answers",                              # 27
            "Tips, Strategies & Answers",                                 # 26
        ],
    },
    "9_practice_tests": {
        "titles": [
            "9 Full-Length {state} {exam} Grade {grade_n} Math Practice Tests",
            "9 {state} {exam} Grade {grade_n} Math Practice Tests",
        ],
        "subtitles": [
            "Test Prep with Tips, Strategies & Answer Explanations",      # 52
            "Test Prep with Tips & Answer Explanations",                  # 42
            "Guided Test Prep with Tips & Answers",                       # 35
            "Test Prep with Tips & Answers",                              # 29
            "Answers & Explanations",                                     # 22
        ],
    },
    "12_practice_tests": {
        "titles": [
            "12 {state} {exam} Grade {grade_n} Math Practice Tests",
        ],
        "subtitles": [
            "The Complete Guided Test Prep with Tips & Detailed Answer Keys",  # 61
            "Complete Guided Test Prep with Tips & Answer Keys",               # 49
            "Guided Test Prep with Tips & Answer Keys",                        # 39
            "Complete Test Prep with Tips & Answers",                          # 37
            "Test Prep with Tips & Answers",                                   # 29
            "Answers & Explanations",                                          # 22
            "Answer Key Included",                                             # 19
        ],
    },
    "in_30_days": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math in 30 Days",
        ],
        "subtitles": [
            "Day by Day Study Plan for Test Prep",                # 35
            "Day by Day Study Plan",                              # 21
            "Daily Study Plan",                                   # 16
        ],
    },
    "quiz": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math Quizzes",
        ],
        "subtitles": [
            "Quick Topic Assessments with Answer Key",            # 39
            "Topic Assessments with Answer Key",                  # 33
            "Assessments with Answer Key",                        # 27
            "Assessments & Answer Key",                           # 24
        ],
    },
    "puzzles": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math Puzzles and Brain Teasers",
            "{state} {exam} Grade {grade_n} Math Puzzles & Brain Teasers",
        ],
        "subtitles": [
            "Fun Math Games, Activities & Challenges",            # 39
            "Math Games, Activities & Challenges",                # 35
            "Fun Games, Activities & Challenges",                 # 34
            "Games, Activities & Challenges",                     # 30
            "Fun Games & Challenges",                             # 22
            "Games & Challenges",                                 # 18
            "Fun Activities",                                     # 14
        ],
    },
    "worksheet": {
        "titles": [
            "{state} {exam} Grade {grade_n} Math Worksheets",
        ],
        "subtitles": [
            "Printable Practice Pages with Answer Key",           # 40
            "Practice Pages with Answer Key",                     # 30
            "Printable Practice with Answers",                    # 31
            "Practice with Answer Key",                           # 24
        ],
    },
}

# Maximum allowed TPT title length
TPT_TITLE_MAX_LENGTH: int = 80


def book_tpt_title(
    book_type: str,
    state_slug: str,
    state_name: str,
) -> str:
    """Generate a TPT-friendly title (≤ 80 chars) for a state × book type.

    The algorithm tries every valid title × subtitle combination from the
    tier lists in ``_TPT_TIERS`` and picks the **longest** one that fits
    within 80 characters — maximising keyword coverage per state.

    Fallback order:
      1. Longest "title: subtitle" combination that fits ≤ 80 chars
      2. Title only (if no subtitle combination fits)

    Examples:
        >>> book_tpt_title("study_guide", "alabama", "Alabama")
        'Alabama ACAP Grade 7 Math Made Easy: Study Guide with Key Concepts & Practices'
        >>> len(book_tpt_title("study_guide", "alabama", "Alabama")) <= 80
        True
        >>> book_tpt_title("puzzles", "georgia", "Georgia")
        'Georgia Georgia Milestones Grade 7 Math Puzzles & Brain Teasers'
        >>> len(book_tpt_title("puzzles", "georgia", "Georgia")) <= 80
        True
    """
    tiers = _TPT_TIERS.get(book_type)
    if not tiers:
        # Unknown book type — simple fallback
        title = book_title(book_type, state_slug, state_name)
        subtitle = book_subtitle(book_type, state_slug)
        return f"{title}: {subtitle}"[:TPT_TITLE_MAX_LENGTH]

    title_templates = tiers["titles"]
    # Sort subtitles longest-first to guarantee the break optimisation
    # selects the best (longest fitting) subtitle for each title variant
    subtitle_tiers = sorted(tiers["subtitles"], key=len, reverse=True)

    resolved_titles = [
        _fill_template(t, state_slug, state_name) for t in title_templates
    ]

    # Try every title × subtitle combination; keep the longest that fits
    best: Optional[str] = None
    for title_str in resolved_titles:
        for sub in subtitle_tiers:
            candidate = f"{title_str}: {sub}"
            if len(candidate) <= TPT_TITLE_MAX_LENGTH:
                if best is None or len(candidate) > len(best):
                    best = candidate
                break  # Best subtitle for this title found
        # Also consider title-only as a candidate (for very long titles)
        if len(title_str) <= TPT_TITLE_MAX_LENGTH:
            if best is None or len(title_str) > len(best):
                # Don't prefer title-only over a title+subtitle of same length
                pass

    if best is not None:
        return best

    # No subtitle fits — use the shortest title variant that fits
    for title_str in resolved_titles:
        if len(title_str) <= TPT_TITLE_MAX_LENGTH:
            return title_str

    # Absolute last resort — truncate
    return resolved_titles[0][:TPT_TITLE_MAX_LENGTH]


def book_title(
    book_type: str,
    state_slug: str,
    state_name: str,
    *,
    grade_display: Optional[str] = None,
) -> str:
    """Generate an SEO-friendly book title for a state-specific edition.

    Examples:
        >>> book_title("all_in_one", "texas", "Texas")
        'Texas STAAR Grade 7 Math All-in-One'
        >>> book_title("5_practice_tests", "texas", "Texas")
        '5 Full-Length Texas STAAR Grade 7 Math Practice Tests'
        >>> book_title("workbook", "alabama", "Alabama")
        'Alabama ACAP Grade 7 Math Workbook'
        >>> book_title("study_guide", "texas", "Texas")
        'Texas STAAR Grade 7 Math Made Easy'
        >>> book_title("10_practice_tests", "california", "California")
        '10 California CAASPP Grade 7 Math Practice Tests'
    """
    template, _ = _TITLE_TEMPLATES.get(
        book_type,
        ("{state} {exam} Grade {grade_n} Math " + book_type.replace("_", " ").title(), ""),
    )
    return _fill_template(template, state_slug, state_name)


def book_subtitle(
    book_type: str,
    state_slug: str,
    *,
    grade_number: Optional[int] = None,
) -> str:
    """Generate a short subtitle for use on covers and listings.

    The subtitle complements the title without repeating its content.

    Examples:
        >>> book_subtitle("all_in_one", "texas")
        'Complete Lessons, Examples, Practice & Answer Key'
        >>> book_subtitle("study_guide", "texas")
        'Study Guide with Key Concepts, Review & Practice'
        >>> book_subtitle("workbook", "alabama")
        'Practice Problems & Exercises with Answer Key'
        >>> book_subtitle("5_practice_tests", "texas")
        'Extra Practice for Test Day Success'
    """
    _, template = _TITLE_TEMPLATES.get(book_type, ("", "Test Prep for {ordinal} Graders"))
    gn = grade_number or GRADE_NUMBER
    ordinal = _ordinal(gn)
    return template.format(
        state="", exam="", grade_n=gn, ordinal=ordinal,
    ).strip()


def book_title_data(
    book_type: str,
    state_slug: str,
    state_name: str,
) -> Dict[str, Any]:
    """Return all title-related data for a state × book type combination.

    Useful for scripts that need individual components (e.g., LaTeX macros,
    marketing copy, or AI review).

    Returns a dict with keys:
        title, subtitle, tpt_title, tpt_title_length,
        grade_display, display_name, state_name,
        exam_name, exam_acronym, exam_months,
        curriculum_name, curriculum_acronym
    """
    exam = get_state_exam_info(state_slug)
    curr = get_state_curriculum_info(state_slug)

    tpt = book_tpt_title(book_type, state_slug, state_name)

    return {
        "title": book_title(book_type, state_slug, state_name),
        "subtitle": book_subtitle(book_type, state_slug),
        "tpt_title": tpt,
        "tpt_title_length": len(tpt),
        "grade_display": GRADE_DISPLAY,
        "display_name": BOOK_DISPLAY_NAMES.get(
            book_type, book_type.replace("_", " ").title()
        ),
        "state_name": state_name,
        "state_slug": state_slug,
        "book_type": book_type,
        "exam_name": exam.get("exam_name", ""),
        "exam_acronym": exam.get("exam_acronym", ""),
        "exam_months": exam.get("exam_months", ""),
        "curriculum_name": curr.get("curriculum_name", ""),
        "curriculum_acronym": curr.get("curriculum_acronym", ""),
    }


# ============================================================================
# TITLES JSON — default path, loader, and LaTeX injector
# ============================================================================
# Workflow:
#   1. Generate titles.json once:
#        python3 scripts/generate_book_titles.py --format json \
#                --output titles.json
#   2. generate_state_books.py reads it to stamp each .tex with the correct
#      \VMBookTitle / \VMBookSubtitle for that state × book type.

import re as _re
import json as _json

_VMBookTitle_re   = _re.compile(r'\\renewcommand\{\\VMBookTitle\}\{[^}]*\}')
_VMBookSubtitle_re = _re.compile(r'\\renewcommand\{\\VMBookSubtitle\}\{[^}]*\}')


def default_titles_json_path() -> Path:
    """Return the default path for the generated titles JSON file.

    Generates to ``<workspace_root>/titles.json``.
    Produced by:
        python3 scripts/generate_book_titles.py --format json \\
                --output titles.json
    """
    return find_workspace() / "titles.json"


def load_book_titles(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load titles from a JSON file generated by generate_book_titles.py.

    Args:
        path: Path to the JSON file.  Defaults to ``titles.json`` in the
              workspace root (see :func:`default_titles_json_path`).

    Returns:
        Dict keyed by ``"state_slug:book_type"`` → title data dict
        (keys: title, subtitle, tpt_title, tpt_title_length, …).

    Raises:
        FileNotFoundError: if the file does not exist — call
            ``generate_book_titles.py --format json --output titles.json``
            first.
    """
    resolved = Path(path) if path else default_titles_json_path()
    if not resolved.is_file():
        raise FileNotFoundError(
            f"Titles file not found: {resolved}\n"
            "  ➜  Generate it first with:\n"
            "       python3 scripts/generate_book_titles.py "
            "--format json --output titles.json"
        )
    with open(resolved, encoding="utf-8") as fh:
        entries = _json.load(fh)
    return {f"{e['state_slug']}:{e['book_type']}": e for e in entries}


def _escape_latex(text: str) -> str:
    """Escape characters that are special in LaTeX prose contexts.

    Handles the subset likely to appear in book titles / subtitles:
    ``& % $ # _ { } ~ ^ \\``
    """
    # Order matters — backslash first so we don't double-escape later replacements
    text = text.replace("\\", r"\textbackslash{}")
    text = text.replace("&", r"\&")
    text = text.replace("%", r"\%")
    text = text.replace("$", r"\$")
    text = text.replace("#", r"\#")
    text = text.replace("_", r"\_")
    text = text.replace("~", r"\textasciitilde{}")
    text = text.replace("^", r"\textasciicircum{}")
    return text


def inject_titles_into_tex(
    content: str,
    book_type: str,
    state_slug: str,
    state_name: str,
    titles: Optional[Dict[str, Any]] = None,
) -> str:
    r"""Replace ``\VMBookTitle`` and ``\VMBookSubtitle`` in a .tex file.

    If *titles* is provided (from :func:`load_book_titles`), the
    pre-generated title/subtitle for this state × book type are used.
    Otherwise the values are computed on the fly from
    :func:`book_title` / :func:`book_subtitle`.

    Only lines that already contain ``\renewcommand{\VMBookTitle}{…}`` or
    ``\renewcommand{\VMBookSubtitle}{…}`` are touched.  If the template has
    no such line the function is a no-op.

    Returns the modified content string.
    """
    key = f"{state_slug}:{book_type}"
    if titles is not None and key in titles:
        title_str    = _escape_latex(titles[key]["title"])
        subtitle_str = _escape_latex(titles[key]["subtitle"])
    else:
        title_str    = _escape_latex(book_title(book_type, state_slug, state_name))
        subtitle_str = _escape_latex(book_subtitle(book_type, state_slug))

    content = _VMBookTitle_re.sub(
        lambda _: f'\\renewcommand{{\\VMBookTitle}}{{{title_str}}}',
        content,
    )
    content = _VMBookSubtitle_re.sub(
        lambda _: f'\\renewcommand{{\\VMBookSubtitle}}{{{subtitle_str}}}',
        content,
    )
    return content


def _fill_template(template: str, state_slug: str, state_name: str) -> str:
    """Fill a title/subtitle template with state + grade info.

    Collapses extra whitespace so titles read cleanly even when a state
    has no exam acronym.
    """
    gn = GRADE_NUMBER
    ordinal = _ordinal(gn)
    exam_acr = get_state_exam_info(state_slug).get("exam_acronym", "")

    result = template.format(
        state=state_name,
        exam=exam_acr,
        grade_n=gn,
        ordinal=ordinal,
    )
    # Collapse any double spaces left when exam acronym is empty
    while "  " in result:
        result = result.replace("  ", " ")
    return result.strip()


def _ordinal(n: int) -> str:
    """Return ordinal string for a number: 1→'1st', 2→'2nd', 3→'3rd', etc."""
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
