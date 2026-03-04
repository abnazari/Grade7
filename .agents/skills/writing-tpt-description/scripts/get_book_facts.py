#!/usr/bin/env python3
"""
Return every fact an AI agent needs to write a TPT product description.

Usage:
    python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py <book_type> <state_slug>

Example:
    python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py study_guide texas
    python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py 3_practice_tests california

Prints a structured plain-text report with all data the agent needs.
No Jinja, no HTML — just facts.

Supported book types:
    all_in_one, study_guide, workbook, step_by_step, in_30_days,
    quiz, puzzles, worksheet,
    3_practice_tests, 5_practice_tests, 7_practice_tests, 10_practice_tests
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ── Resolve workspace & add scripts/ to sys.path ──────────────────────

def _find_workspace() -> Path:
    """Walk up from this file to find topics_config.yaml + studyGuide.cls."""
    candidate = Path(__file__).resolve().parent
    for _ in range(10):
        if (candidate / "topics_config.yaml").exists() and (candidate / "studyGuide.cls").exists():
            return candidate
        candidate = candidate.parent
    print("ERROR: Could not find workspace root.", file=sys.stderr)
    sys.exit(1)


WORKSPACE = _find_workspace()
sys.path.insert(0, str(WORKSPACE / "scripts"))

import yaml  # noqa: E402
from config_loader import load_config, TopicsConfig  # noqa: E402


# ============================================================================
# DATA LOADERS
# ============================================================================

def _load_yaml(name: str) -> dict:
    path = WORKSPACE / name
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_state_exams() -> Dict[str, dict]:
    return _load_yaml("state_exams.yaml").get("states", {})


def load_state_curriculums() -> Dict[str, dict]:
    return _load_yaml("state_curriculums.yaml").get("states", {})


def load_titles() -> List[dict]:
    """Load titles.json from the workspace root."""
    path = WORKSPACE / "titles.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_title_entry(book_type: str, state_slug: str) -> Optional[dict]:
    """Find the matching title entry for a book_type × state_slug pair."""
    titles = load_titles()
    for entry in titles:
        if entry.get("book_type") == book_type and entry.get("state_slug") == state_slug:
            return entry
    return None


# ============================================================================
# TOPIC / CHAPTER HELPERS
# ============================================================================

def get_state_topics(state_slug: str, config: TopicsConfig) -> List[str]:
    """Full ordered list of topic IDs for a state (core + additional)."""
    topics = list(config.core_topic_ids)
    additional = config.state_additional.get(state_slug, [])
    if not additional:
        return topics

    by_chapter: Dict[str, List[str]] = {}
    for tid in additional:
        ch = tid[:4]
        by_chapter.setdefault(ch, []).append(tid)

    for ch in sorted(by_chapter.keys()):
        extras = sorted(by_chapter[ch])
        last_idx = -1
        for i, t in enumerate(topics):
            if t.startswith(ch):
                last_idx = i
        if last_idx >= 0:
            for j, extra in enumerate(extras):
                topics.insert(last_idx + 1 + j, extra)
        else:
            topics.extend(extras)

    return topics


def build_chapter_summaries(
    state_slug: str, config: TopicsConfig
) -> Tuple[List[Tuple[int, str, int]], int]:
    """(chapter_num, title, topic_count) per chapter + total."""
    state_topic_ids = set(get_state_topics(state_slug, config))
    summaries: List[Tuple[int, str, int]] = []

    for ch in config.chapters:
        clean_title = ch.title.replace("\\&", "&")
        count = sum(1 for t in ch.topics if t.id in state_topic_ids)
        for at in config.additional_topics_list:
            if at.chapter == ch.num and at.id in state_topic_ids:
                count += 1
        if count > 0:
            summaries.append((ch.num, clean_title, count))

    total = sum(c for _, _, c in summaries)
    return summaries, total


def build_full_topic_list(state_slug: str, config: TopicsConfig) -> List[Tuple[int, str, str]]:
    """Return (chapter_num, topic_id, topic_name) for every topic in this state."""
    topic_ids = get_state_topics(state_slug, config)
    result = []
    for tid in topic_ids:
        ch_num = config.topic_chapter.get(tid, 0)
        name = config.topic_names.get(tid, tid)
        result.append((ch_num, tid, name))
    return result


# ============================================================================
# BOOK TYPE FEATURE DATA (self-contained, no listing_data import needed)
# ============================================================================

QUESTIONS_PER_TEST = 30

BOOK_TYPE_INFO: Dict[str, Dict[str, Any]] = {
    "all_in_one": {
        "display_name": "All-in-One",
        "subtitle": "Complete Lessons, Examples & Practice",
        "what_it_is": "The comprehensive resource. Full lessons, worked examples, and practice for every topic.",
        "features": [
            "Full lessons with clear explanations for every Grade 7 math topic — not just problems, but actual teaching",
            "Step-by-step worked examples showing students exactly how to approach each problem type",
            "Practice problems right after every lesson so students apply what they just learned",
            "Real-world word problems that connect math to everyday situations students encounter",
            "Visual models — number lines, ratio tables, coordinate grids, area models, bar diagrams — that make abstract concepts concrete",
            "Vocabulary in context so students build math language naturally as they learn",
            "Chapter reviews that pull together everything students learned across multiple topics",
        ],
        "use_cases": [
            "Full-year classroom instruction — use it as your primary Grade 7 math supplement",
            "Homeschool curriculum — complete enough to serve as your core math resource",
            "Tutoring programs — structured lessons make session planning effortless",
            "After-school enrichment — students work through topics at their own pace",
            "Summer bridge to Grade 8 — cover everything students need before the next year",
            "Parent-guided learning — clear enough for any parent to teach from",
        ],
    },
    "study_guide": {
        "display_name": "Study Guide",
        "subtitle": "Quick-Reference Review & Key Concepts",
        "what_it_is": "The compact review resource. Key concepts, essential examples, and quick practice.",
        "features": [
            "Focused explanations of every key concept — no padding, just the core math students need",
            "Key examples showing the most important problem types students will encounter",
            "Quick-review practice at the end of every topic to check understanding in minutes",
            "Visual aids — diagrams, number lines, charts — that make review sessions faster and more effective",
            "Compact enough to review in a week, thorough enough to cover every standard",
            "Clear learning goals so students know exactly what they should take away from each topic",
        ],
        "use_cases": [
            "Test prep review — cover all key concepts in the weeks before the state exam",
            "Quick reference during homework — look up any concept in seconds",
            "End-of-unit review before classroom assessments",
            "Tutoring — review key topics efficiently without wasting session time",
            "Parent-guided review at home — concise enough to fit into busy evenings",
            "Summer refresher before starting Grade 8",
        ],
    },
    "workbook": {
        "display_name": "Workbook",
        "subtitle": "Hundreds of Practice Problems by Topic",
        "what_it_is": "The practice-focused resource. Hundreds of problems organised by topic, progressing from easy to challenging.",
        "features": [
            "Problems that progress from easy to challenging — so every student starts with success",
            "Multiple question formats: fill-in, multiple choice, short answer, word problems — just like real tests",
            "Space to show work right on the page — no separate scratch paper needed",
            "Topic-organized sections so you can assign exactly what your class is studying",
            "Real-world application problems that show students why math matters outside the classroom",
            "Visual problems with graphs, shapes, and measurement tasks for hands-on engagement",
            "Step-by-step answer key so students learn from every mistake",
        ],
        "use_cases": [
            "Daily homework assignments — just print the pages you need",
            "Skill reinforcement after classroom lessons",
            "Math centers and station rotations — assign different topics to different groups",
            "Independent practice for early finishers",
            "Assessment preparation — the practice mirrors real test question formats",
            "Summer math practice to prevent the 'summer slide'",
        ],
    },
    "step_by_step": {
        "display_name": "Step-by-Step Guide",
        "subtitle": "Clear Instructions for Every Problem Type",
        "what_it_is": "The procedural resource. Numbered steps for every problem type, with road maps and guided practice.",
        "features": [
            "Numbered step-by-step instructions for every problem type in the Grade 7 curriculum",
            "Road maps at the start of each topic showing students the path from start to solution",
            "Detailed step examples that walk through each instruction with a real problem",
            "Common mistakes highlighted so students learn to avoid them before they happen",
            "Scaffolded practice organized by the exact steps taught — practice reinforces procedure",
            "Visual step breakdowns with diagrams and illustrations for visual learners",
        ],
        "use_cases": [
            "Students who need structured guidance to build confidence",
            "Learners who freeze when they don't know 'where to start'",
            "Tutoring sessions — follow the steps together for productive, focused practice",
            "Homework support — students (and parents) can follow the steps independently",
            "Differentiated instruction — pair with other resources for struggling learners",
            "Special education settings where procedural scaffolding is essential",
        ],
    },
    "in_30_days": {
        "display_name": "Math in 30 Days",
        "subtitle": "The Complete Grade 7 Curriculum in One Month",
        "what_it_is": "The structured daily plan. Covers the full curriculum in one month with daily lessons, practice, and progress tracking.",
        "features": [
            "30 structured daily lessons — each one teaches, practices, and reviews in a single session",
            "Clear daily goals so students know exactly what they're learning each day",
            "Built-in progress tracking — students see their improvement across all 30 days",
            "Paced to cover the full curriculum without overwhelming students",
            "Daily practice with answers — immediate feedback keeps students on track",
            "Calendar-based structure that students can follow independently or with guidance",
        ],
        "use_cases": [
            "Summer crash course — cover Grade 7 math before the new school year",
            "Pre-test intensive — 30 days before the state exam",
            "New student catch-up program for mid-year transfers",
            "Homeschool math module — one month, one subject, total coverage",
            "Holiday break review to prevent skill loss",
            "Tutoring schedule framework — one day per session, perfectly paced",
        ],
    },
    "quiz": {
        "display_name": "Quizzes",
        "subtitle": "Quick Assessments for Every Topic",
        "what_it_is": "The quick assessment resource. One 15-minute quiz per topic.",
        "features": [
            "One focused quiz per topic — covering every Grade 7 math standard",
            "15-minute format that fits into any class schedule without eating into lesson time",
            "Multiple question types: multiple choice, short answer, and word problems — real test practice",
            "Score tracking so students can monitor their own progress and take ownership",
            "Complete answer key with scoring guide — grade in minutes, not hours",
            "Colorful, low-stress design that reduces test anxiety while maintaining rigor",
        ],
        "use_cases": [
            "Warm-ups and bell-ringers to start class with purpose",
            "Exit tickets that show you who understood today's lesson",
            "Weekly assessment rotation to keep skills sharp",
            "Formative assessment data to drive small-group instruction",
            "Homework that's focused and manageable — not overwhelming",
            "Test prep in bite-sized chunks that don't stress students out",
        ],
    },
    "puzzles": {
        "display_name": "Puzzles & Brain Teasers",
        "subtitle": "Math Fun That Builds Real Skills",
        "what_it_is": "The engagement resource. Curriculum-aligned puzzles, games, and brain teasers.",
        "features": [
            "6–8 unique puzzles per topic — code breakers, mystery numbers, riddles, mazes, and more",
            "Every puzzle is aligned to a real Grade 7 math standard — curriculum, disguised as fun",
            "Develops critical thinking and problem-solving skills alongside mathematical fluency",
            "Progressive difficulty within each topic — accessible entry point, satisfying challenge",
            "Engaging themes and illustrations that motivate even the most reluctant math students",
            "Complete answer key so students can self-check and learn from tricky puzzles",
        ],
        "use_cases": [
            "Math centers and station rotations — the station every student wants to visit",
            "Early finisher activities that are actually educational, not just time-fillers",
            "Enrichment and gifted programs — challenges that stretch strong students",
            "Fun Friday rewards that reinforce the week's learning",
            "Homework students genuinely look forward to",
            "Math anxiety intervention — building positive math experiences through play",
        ],
    },
    "worksheet": {
        "display_name": "Worksheets",
        "subtitle": "Standalone Printable Activities by Topic",
        "what_it_is": "The flexible resource. Standalone printable worksheets — one per topic, usable in any order.",
        "features": [
            "One standalone worksheet per topic — use any page independently, in any order",
            "Clean, spacious layout with dedicated space for students to show their work",
            "Mixed question formats: computation, word problems, visual reasoning — mirrors real assessments",
            "Consistent, age-appropriate difficulty that matches Grade 7 expectations",
            "Each worksheet is self-contained — no need to photocopy anything else",
            "Complete answer key so grading takes minutes, not hours",
        ],
        "use_cases": [
            "Homework assignments — print one worksheet, send it home, done",
            "Substitute teacher plans — hand the sub a worksheet and know learning still happens",
            "Small-group targeted practice during intervention blocks",
            "Formative assessment — use worksheets as quick checks after lessons",
            "Tutoring session handouts — focused practice on one skill at a time",
            "Parent practice at home — print what your child needs help with",
        ],
    },
}

# Generate practice test entries
for _n in [3, 5, 7, 10]:
    _key = f"{_n}_practice_tests"
    _total = _n * QUESTIONS_PER_TEST
    BOOK_TYPE_INFO[_key] = {
        "display_name": f"{_n} Practice Tests",
        "subtitle": "Full-Length Practice Tests with Detailed Answer Explanations",
        "what_it_is": f"The test prep resource. {_n} full-length practice tests with {QUESTIONS_PER_TEST} questions each. Every answer explained step by step.",
        "num_tests": _n,
        "questions_per_test": QUESTIONS_PER_TEST,
        "total_questions": _total,
        "features": [
            f"{_n} complete tests × {QUESTIONS_PER_TEST} questions = {_total} problems with full answer explanations",
            "Question formats mirror the real state exam: multiple-choice, short-answer, and extended response",
            "Detailed step-by-step explanations for every question — students learn from every answer",
            f"Score tracking after each test so students see their growth across all {_n} attempts",
            "Covers every Grade 7 math strand: ratios and rates, the number system, expressions and equations, geometry, and statistics",
            "Realistic test-day conditions — timed format, answer grids, and scoring rubrics included",
        ],
        "use_cases": [
            "State exam preparation — the most realistic practice your students will get",
            "Classroom test-prep sessions — one test per week leading up to exam day",
            "Homework practice — students work through tests independently with the answer key",
            "Tutoring sessions — identify gaps and target weak areas with specific tests",
            "Homeschool assessment — gauge Grade 7 math proficiency with standardized-format tests",
            "Diagnostic tool — use the first test to find gaps, the last test to measure growth",
        ],
    }


# ============================================================================
# SERIES CROSS-SELL
# ============================================================================

SERIES_DESCRIPTIONS: Dict[str, str] = {
    "all_in_one": "All-in-One — The complete resource with full lessons, worked examples, and practice for every topic",
    "study_guide": "Study Guide — A concise review of key concepts, essential examples, and quick practice",
    "workbook": "Workbook — Hundreds of scaffolded practice problems organized by topic for extra practice",
    "step_by_step": "Step-by-Step Guide — A guided approach with clear, numbered instructions so students learn at their own pace",
    "in_30_days": "Math in 30 Days — A structured daily plan that covers the full curriculum in one month",
    "quiz": "Quizzes — Quick 15-minute assessments for every topic to track progress",
    "puzzles": "Puzzles & Brain Teasers — Curriculum-aligned games, riddles, and challenges that make math fun",
    "worksheet": "Worksheets — Standalone printable activities for any topic, ready to use in any order",
    "practice_tests": "Practice Tests (3, 5, 7, or 10 editions) — Full-length, realistic test prep with detailed answer explanations — every edition contains unique tests",
}


def get_series_list(current_book_type: str) -> List[str]:
    """Return series cross-sell descriptions, excluding the current book type."""
    result = []
    for key, desc in SERIES_DESCRIPTIONS.items():
        if key == current_book_type:
            continue
        # For practice tests, skip individual editions if current is any practice test
        if key == "practice_tests" and current_book_type.endswith("_practice_tests"):
            continue
        if key.endswith("_practice_tests"):
            continue
        result.append(desc)
    # Add practice tests as a combined entry (unless current is a practice test)
    if not current_book_type.endswith("_practice_tests") and "practice_tests" in SERIES_DESCRIPTIONS:
        pass  # already added above
    elif current_book_type.endswith("_practice_tests"):
        pass  # skip
    return result


# ============================================================================
# MAIN: PRINT FACTS
# ============================================================================

SUPPORTED_BOOK_TYPES = list(BOOK_TYPE_INFO.keys())


def print_facts(book_type: str, state_slug: str) -> None:
    config = load_config(WORKSPACE)

    # Validate inputs
    if book_type not in SUPPORTED_BOOK_TYPES:
        print(f"ERROR: Unknown book type '{book_type}'.", file=sys.stderr)
        print(f"Supported: {', '.join(SUPPORTED_BOOK_TYPES)}", file=sys.stderr)
        sys.exit(1)
    if state_slug not in config.all_state_slugs:
        print(f"ERROR: Unknown state '{state_slug}'.", file=sys.stderr)
        print(f"Example states: {', '.join(config.all_state_slugs[:5])}...", file=sys.stderr)
        sys.exit(1)

    state_name = config.state_display_names[state_slug]
    bt_info = BOOK_TYPE_INFO[book_type]

    # Exam & curriculum
    exams = load_state_exams()
    curriculums = load_state_curriculums()
    exam = exams.get(state_slug, {})
    curr = curriculums.get(state_slug, {})

    # Title entry from titles.json
    title_entry = find_title_entry(book_type, state_slug)

    # Chapter summaries
    chapter_summaries, num_topics = build_chapter_summaries(state_slug, config)
    num_chapters = len(chapter_summaries)

    # Full topic list
    full_topics = build_full_topic_list(state_slug, config)

    # Series cross-sell
    series = get_series_list(book_type)

    # ── Print the report ────────────────────────────────────────────────
    print("=" * 70)
    print(f"BOOK FACTS: {book_type} × {state_slug}")
    print("=" * 70)

    print()
    print("--- BOOK TITLE ---")
    if title_entry:
        print(f"Book Title:         {title_entry.get('tpt_title', '')}")
    else:
        print("Book Title:         (not found in titles.json)")

    print()
    print("--- BOOK TYPE ---")
    print(f"Book Type Key:      {book_type}")
    print(f"Display Name:       {bt_info['display_name']}")
    print(f"What It Is:         {bt_info['what_it_is']}")

    if "num_tests" in bt_info:
        print(f"Number of Tests:    {bt_info['num_tests']}")
        print(f"Questions Per Test: {bt_info['questions_per_test']}")
        print(f"Total Questions:    {bt_info['total_questions']}")

    print()
    print("--- STATE ---")
    print(f"State:              {state_name}")

    print()
    print("--- CURRICULUM ---")
    if curr:
        print(f"Curriculum Name:    {curr.get('curriculum_name', '')}")
        print(f"Curriculum Acronym: {curr.get('curriculum_acronym', '')}")
    else:
        print("Curriculum Name:    (not available)")
        print("Curriculum Acronym: (not available)")

    print()
    print("--- EXAM ---")
    if exam:
        print(f"Exam Name:          {exam.get('exam_name', '')}")
        print(f"Exam Acronym:       {exam.get('exam_acronym', '')}")
    else:
        print("Exam Name:          (none)")
        print("Exam Acronym:       (none)")

    print()
    print("--- CHAPTERS & TOPICS ---")
    print(f"Total Topics:       {num_topics}")
    print(f"Total Chapters:     {num_chapters}")
    print()
    for ch_num, ch_title, ch_count in chapter_summaries:
        print(f"  Chapter {ch_num}: {ch_title} — {ch_count} topic{'s' if ch_count != 1 else ''}")

    print()
    print("--- FEATURES (for this book type) ---")
    for f in bt_info["features"]:
        print(f"  • {f}")

    print()
    print("--- USE CASES ---")
    for uc in bt_info["use_cases"]:
        print(f"  • {uc}")

    print()
    print("--- SERIES CROSS-SELL (other books to mention) ---")
    for desc in series:
        print(f"  • {desc}")

    print()
    print("--- DESIGN & QUALITY (always true for all books) ---")
    print("  • Professional, full-color design with engaging illustrations and diagrams")
    print("  • Complete answer key with explanations")
    print("  • Print-ready — download, print, and use immediately. No prep, no assembly")
    print("  • Written by Dr. A. Nazari / View Math — a math education company")
    print(f"  • Aligned to {state_name}'s specific Grade 7 math standards")

    print()
    print("=" * 70)
    print("END OF FACTS")
    print("=" * 70)


# ============================================================================
# CLI
# ============================================================================

def print_usage():
    print("Usage: python3 get_book_facts.py <book_type> <state_slug>")
    print()
    print(f"Book types: {', '.join(SUPPORTED_BOOK_TYPES)}")
    print()
    print("State slugs: alabama, alaska, arizona, ... (50 US states, lowercase, hyphenated)")
    print()
    print("Examples:")
    print("  python3 get_book_facts.py study_guide texas")
    print("  python3 get_book_facts.py 3_practice_tests california")
    print("  python3 get_book_facts.py all_in_one new-york")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ("--help", "-h"):
        print_usage()
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--list-states":
        config = load_config(WORKSPACE)
        for slug in config.all_state_slugs:
            print(f"  {slug:20s}  {config.state_display_names[slug]}")
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--list-book-types":
        for bt in SUPPORTED_BOOK_TYPES:
            print(f"  {bt:25s}  {BOOK_TYPE_INFO[bt]['display_name']}")
        sys.exit(0)

    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    print_facts(sys.argv[1], sys.argv[2])
