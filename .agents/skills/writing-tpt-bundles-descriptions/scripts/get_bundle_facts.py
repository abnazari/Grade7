#!/usr/bin/env python3
"""
Return every fact an AI agent needs to write a TPT bundle description.

Usage:
    python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py <bundle_type> <state_slug>

Example:
    python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py practice_tests_bundle texas
    python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py complete_series_bundle california

List helpers:
    python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py --list-bundles
    python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py --list-states

Prints a structured plain-text report with all data the agent needs.
No Jinja, no HTML — just facts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
from config import GRADE_DISPLAY  # noqa: E402


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
    path = WORKSPACE / "titles.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_title_entry(book_type: str, state_slug: str) -> Optional[dict]:
    titles = load_titles()
    for entry in titles:
        if entry.get("book_type") == book_type and entry.get("state_slug") == state_slug:
            return entry
    return None


# ============================================================================
# TOPIC / CHAPTER HELPERS
# ============================================================================

def get_state_topics(state_slug: str, config: TopicsConfig) -> List[str]:
    topics = list(config.core_topic_ids)
    additional = config.state_additional.get(state_slug, [])
    if not additional:
        return topics

    by_chapter: Dict[str, List[str]] = {}
    for tid in additional:
        ch = tid[:4]
        by_chapter.setdefault(ch, []).append(tid)

    result: List[str] = []
    current_ch = ""
    for tid in topics:
        ch = tid[:4]
        if ch != current_ch:
            if current_ch and current_ch in by_chapter:
                result.extend(by_chapter[current_ch])
            current_ch = ch
        result.append(tid)
    if current_ch in by_chapter:
        result.extend(by_chapter[current_ch])

    remaining = set(additional) - {t for t in result if t in additional}
    result.extend(sorted(remaining))
    return result


def build_chapter_summaries(
    state_slug: str, config: TopicsConfig
) -> Tuple[List[Tuple[int, str, int]], int]:
    all_topics = get_state_topics(state_slug, config)
    ch_counts: Dict[int, int] = {}
    for tid in all_topics:
        ch_num = int(tid[2:4])
        ch_counts[ch_num] = ch_counts.get(ch_num, 0) + 1

    summaries = []
    for ch in config.chapters:
        count = ch_counts.get(ch.num, 0)
        if count > 0:
            summaries.append((ch.num, ch.title, count))

    for ch_num in sorted(ch_counts):
        if ch_num not in [c.num for c in config.chapters]:
            summaries.append((ch_num, f"Chapter {ch_num}", ch_counts[ch_num]))

    total = sum(c for _, _, c in summaries)
    return summaries, total


# ============================================================================
# BUNDLE DEFINITIONS
# ============================================================================

QUESTIONS_PER_TEST = 30

BUNDLE_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "practice_tests_bundle": {
        "display_name": "Practice Tests Bundle",
        "book_types": ["3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"],
        "num_books": 4,
        "total_tests": 25,
        "total_questions": 750,
        "price_tier": "Mid",
        "what_it_is": "All four practice test editions in one package — 25 unique, non-overlapping full-length tests with 750 questions.",
        "value_proposition": "The most comprehensive test prep available — 25 different tests means weekly test-prep sessions for the entire school year without repeating.",
        "includes_practice_tests": True,
        "key_selling_points": [
            "25 unique, non-overlapping full-length tests (3 + 5 + 7 + 10)",
            "750 total questions — every one with a detailed step-by-step answer explanation",
            "No repeated questions across any of the four books",
            "Realistic test-day format: question types, difficulty, and coverage match the real state exam",
            "Score tracking so students can measure growth across attempts",
            "Colorful, kid-friendly design with a friendly owl mascot",
            "Print-ready — download, print, and go",
        ],
        "use_cases": [
            "Weekly test-prep sessions throughout the school year — you won't run out",
            "Pre-test and post-test comparisons to measure student growth",
            "Diagnostic assessments to find skill gaps early",
            "Homework packets — assign one test per week",
            "Tutoring and after-school programs — a fresh test for every session",
            "Homeschool families — simulate real testing conditions at home",
            "Summer review before the next grade",
        ],
        "cross_sell_exclude": {"3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"},
        "cross_sell_note": "Practice tests work best when students already know the material. Pair this bundle with:",
    },
    "study_practice_bundle": {
        "display_name": "Study & Practice Bundle",
        "book_types": ["study_guide", "workbook", "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"],
        "num_books": 6,
        "total_tests": 25,
        "total_questions": 750,
        "price_tier": "Premium",
        "what_it_is": "Study Guide + Workbook + all four practice test editions. Review concepts, build skills, then test under real conditions.",
        "value_proposition": "The complete learn-practice-test cycle. Students review with the Study Guide, build fluency with the Workbook, then prove mastery across 25 unique practice tests.",
        "includes_practice_tests": True,
        "how_books_work_together": {
            "study_guide": "Each topic gets a focused explanation, a key example, and a quick practice check. Compact enough to review the whole curriculum in a week.",
            "workbook": "Once students understand a concept, they work through scaffolded problems — from straightforward to challenging. Multiple question formats: fill-in, multiple choice, short answer, word problems.",
            "practice_tests": "Full-length exams with 30 questions each. Detailed answer explanations show exactly where students went right and where they need more work. With 25 unique tests, you can run weekly test-prep sessions the entire school year without repeating.",
        },
        "key_selling_points": [
            "Study Guide for focused concept review — key concepts, essential examples, quick practice",
            "Workbook with hundreds of practice problems organized by topic, progressing from easy to challenging",
            "25 unique, non-overlapping full-length practice tests (3 + 5 + 7 + 10 editions)",
            "750 total test questions — every one with a detailed step-by-step answer explanation",
            "Complete learn → practice → test cycle in one bundle",
            "Answer keys with explanations for every book",
            "Colorful, kid-friendly design with a friendly owl mascot",
            "Print-ready — download, print, and go",
        ],
        "use_cases": [
            "Classroom use — Study Guide for teaching, Workbook for daily practice, tests for assessment",
            "Homeschool families who want a structured curriculum with built-in testing",
            "Tutoring programs — review, practice, and test in one bundle",
            "Parents helping at home — clear materials with answer keys for every book",
            "State exam prep — 25 unique practice tests give more than enough test simulation",
            "Summer bridge — review, reinforce, and assess before the next grade",
        ],
        "cross_sell_exclude": {"study_guide", "workbook", "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"},
        "cross_sell_note": "This bundle covers study, practice, and testing. For additional resources, explore:",
    },
    "test_prep_bundle": {
        "display_name": "Test Prep Bundle",
        "book_types": ["in_30_days", "quiz", "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"],
        "num_books": 6,
        "total_tests": 25,
        "total_questions": 750,
        "price_tier": "Premium",
        "what_it_is": "Math in 30 Days + Quizzes + all four practice test editions. A structured test prep system: study plan, progress checkpoints, and 25 unique tests.",
        "value_proposition": "A complete test prep system. The 30-day plan is the study schedule. Quizzes are the checkpoints. 25 unique practice tests are the final step.",
        "includes_practice_tests": True,
        "how_books_work_together": {
            "in_30_days": "The plan. It tells students exactly what to study each day — teaching, practice, and review built into every session. Follow the 30-day calendar and the whole curriculum gets covered without cramming.",
            "quiz": "The checkpoints. After covering a topic, students take a quick 15-minute quiz. Score well? Move on. Need more work? Go back and review. Simple progress tracking.",
            "practice_tests": "The final step. Once the review is done, students take full-length tests under real conditions: 30 questions per test, same format as the state exam. Detailed answer explanations for every question. With 25 unique tests, you can run test-prep sessions for months without repeating.",
        },
        "key_selling_points": [
            "Math in 30 Days — a day-by-day study plan covering the full curriculum in one month",
            "Quizzes — one 15-minute quiz per topic to check understanding along the way",
            "25 unique, non-overlapping full-length practice tests (3 + 5 + 7 + 10 editions)",
            "750 total test questions with detailed step-by-step answer explanations",
            "Plan → check → test: a structured test prep system",
            "Answer keys with explanations for every book",
            "Colorful, kid-friendly design with a friendly owl mascot",
            "Print-ready — no prep needed",
        ],
        "use_cases": [
            "Teachers running state exam prep units — the 30-day plan does the scheduling for you",
            "Tutors who need structured plans with built-in assessments and plenty of test material",
            "Homeschool families preparing for state testing",
            "Parents who want a clear, day-by-day approach at home",
            "After-school programs focused on math intervention and test readiness",
            "Students who need to cover a lot of ground in a short time",
        ],
        "cross_sell_exclude": {"in_30_days", "quiz", "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"},
        "cross_sell_note": "This bundle is focused on test prep. For concept instruction and more practice, explore:",
    },
    "classroom_bundle": {
        "display_name": "Classroom Bundle",
        "book_types": ["step_by_step", "workbook", "quiz", "worksheet", "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"],
        "num_books": 8,
        "total_tests": 25,
        "total_questions": 750,
        "price_tier": "High",
        "what_it_is": "Step-by-Step Guide + Workbook + Quizzes + Worksheets + all four practice test editions. The daily teaching toolkit plus serious test prep.",
        "value_proposition": "Everything a teacher needs for daily instruction, practice, assessment, and test prep — in one bundle.",
        "includes_practice_tests": True,
        "how_books_work_together": {
            "step_by_step": "For teaching. Every problem type gets clear, numbered instructions: \"Step 1, Step 2, Step 3.\" Road maps at the start of each topic. Common mistakes highlighted. Especially useful for struggling learners and differentiated instruction.",
            "workbook": "Where students build fluency. Problems progress from easy to challenging — fill-in, multiple choice, short answer, word problems. Assign a page for homework or use during independent practice.",
            "quiz": "Fast, low-stress assessments. One quiz per topic, 15 minutes each. Use them as exit tickets, bell-ringers, or weekly checks. The scoring guide makes it easy to track who needs help.",
            "worksheet": "The flexible option. Each is standalone — no sequence required. Pull one for any topic when you need a sub plan, a math center activity, a small-group handout, or quick homework.",
            "practice_tests": "Handles test prep. Full-length exams with detailed answer explanations. Run weekly test-prep sessions the entire year without repeating a single test.",
        },
        "key_selling_points": [
            "Step-by-Step Guide — numbered instructions for every problem type with road maps and common-mistake alerts",
            "Workbook — hundreds of practice problems organized by topic, easy to challenging",
            "Quizzes — one 15-minute quiz per topic with scoring guide and answer key",
            "Worksheets — standalone printable pages for any topic, usable in any order",
            "25 unique, non-overlapping full-length practice tests (3 + 5 + 7 + 10 editions)",
            "750 total test questions with detailed answer explanations",
            "Answer keys with explanations for every book",
            "Colorful, kid-friendly design with a friendly owl mascot",
            "Print-ready — download, print, and use immediately",
        ],
        "use_cases": [
            "Full-year instruction — Step-by-Step for teaching, Workbook for practice, Quizzes for assessment, tests for exam prep",
            "Differentiated instruction — Step-by-Step for scaffolding, Worksheets for independent work",
            "Math centers — rotate students through Worksheets, Workbook pages, and Quizzes",
            "Homeschool families — structured teaching with built-in practice and 25 unique tests",
            "Tutoring programs — instruction, practice, and assessment all in one bundle",
            "Sub plans — grab a Worksheet or Quiz for zero-prep coverage",
        ],
        "cross_sell_exclude": {"step_by_step", "workbook", "quiz", "worksheet", "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"},
        "cross_sell_note": "This bundle covers instruction, practice, assessment, and testing. For additional resources:",
    },
    "activities_assessments_bundle": {
        "display_name": "Activities & Assessments Bundle",
        "book_types": ["puzzles", "worksheet", "quiz"],
        "num_books": 3,
        "total_tests": 0,
        "total_questions": 0,
        "price_tier": "Budget",
        "what_it_is": "Puzzles & Brain Teasers + Worksheets + Quizzes. Three books for flexible classroom use: engagement, standalone practice, and quick assessment.",
        "value_proposition": "The flexible classroom bundle. Puzzles for engagement, Worksheets for practice, Quizzes for assessment — all curriculum-aligned.",
        "includes_practice_tests": False,
        "how_books_work_together": {
            "puzzles": "Keep students engaged. Code breakers where solving math reveals a secret message. Mystery number challenges. Math riddles. Every puzzle is aligned to a real standard — the math is rigorous, but the format keeps students motivated.",
            "worksheet": "Flexible practice. Each covers a single topic with a clean layout and mixed question types. Use them in any order — as homework, math center rotation, warm-up, or independent practice. No sequence required.",
            "quiz": "Quick, focused assessment data. 15-minute quizzes for each topic — use them as exit tickets, bell-ringers, or weekly checks. The scoring guide shows who's on track and who needs more time.",
        },
        "key_selling_points": [
            "Puzzles & Brain Teasers — 6–8 unique puzzles per topic: code breakers, mystery numbers, riddles, mazes, and more",
            "Worksheets — one standalone, printable worksheet per topic with mixed question formats",
            "Quizzes — one 15-minute quiz per topic with answer key and scoring guide",
            "All three books are curriculum-aligned — real math, fun format",
            "Answer keys included for every book",
            "Colorful, engaging pages with illustrations, themes, and a friendly owl mascot",
            "Print-ready — download, print, done",
        ],
        "use_cases": [
            "Math centers and station rotations — puzzles at one table, worksheets at another, quizzes for assessment",
            "Early finisher activities — puzzles that build real skills, not just time-fillers",
            "Homework — especially the puzzles and worksheets",
            "Sub plans — grab a worksheet or quiz for zero-prep coverage",
            "Homeschool enrichment — keep math engaging without sacrificing rigor",
            "Tutoring sessions — mix puzzles with worksheets to keep energy up",
            "Formative assessment — quizzes give you quick data on every topic",
            "Math anxiety intervention — puzzles reduce stress while building confidence",
        ],
        "cross_sell_exclude": {"puzzles", "worksheet", "quiz"},
        "cross_sell_note": "This bundle focuses on activities and assessment. For instruction and test prep, explore:",
    },
    "complete_series_bundle": {
        "display_name": "Complete Series Bundle",
        "book_types": ["study_guide", "workbook", "step_by_step", "in_30_days", "quiz", "puzzles", "worksheet", "3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"],
        "num_books": 11,
        "total_tests": 25,
        "total_questions": 750,
        "price_tier": "Ultimate",
        "what_it_is": "Every book in the series — study guides, workbooks, step-by-step instruction, daily plans, quizzes, puzzles, worksheets, and 25 unique full-length practice tests.",
        "value_proposition": "The ultimate collection. Teaching, practice, assessment, enrichment, and 25 unique practice tests — all in one bundle.",
        "includes_practice_tests": True,
        "key_selling_points": [
            "Study Guide — key concepts, essential examples, and quick practice for every topic",
            "Workbook — hundreds of practice problems organized by topic, easy to challenging",
            "Step-by-Step Guide — numbered instructions for every problem type with road maps and common-mistake alerts",
            "Math in 30 Days — a day-by-day study plan covering the full curriculum in one month",
            "Quizzes — one 15-minute quiz per topic with scoring guide and answer key",
            "Puzzles & Brain Teasers — 6–8 curriculum-aligned puzzles per topic",
            "Worksheets — standalone printable pages for any topic, usable in any order",
            "25 unique, non-overlapping full-length practice tests (3 + 5 + 7 + 10 editions) with 750 total questions",
            "Answer keys with explanations for every book",
            "Professional, full-color design with a friendly owl mascot",
            "Print-ready — download, print, and use. No prep, no assembly, no extra materials",
        ],
        "use_cases": [
            "Run a full-year math program — Study Guide for concepts, Workbook for daily practice, Quizzes for assessment, tests for exam prep",
            "Differentiate instruction — Step-by-Step for students who need scaffolding, Puzzles for enrichment, Worksheets for independent work",
            "Prepare for the state exam — Math in 30 Days for a structured review plan, then 25 unique practice tests",
            "Set up math centers — rotate between Puzzles, Worksheets, Workbook pages, and Quizzes",
            "Support homeschool families — complete curriculum plus assessments and enrichment activities",
            "Stock a tutoring program — the right resource for any student, any session",
            "Cover sub days — Worksheets and Quizzes need zero prep",
            "Send materials home — parents get study guides, practice, and tests to support learning at home",
        ],
        "cross_sell_exclude": set(),
        "cross_sell_note": None,
    },
}


# ============================================================================
# CROSS-SELL DESCRIPTIONS (for books NOT in the bundle)
# ============================================================================

SERIES_DESCRIPTIONS: Dict[str, str] = {
    "study_guide": "Study Guide — A concise review of key concepts, essential examples, and quick practice",
    "workbook": "Workbook — Hundreds of scaffolded practice problems organized by topic",
    "step_by_step": "Step-by-Step Guide — Numbered instructions for every problem type, great for students who need more structure",
    "in_30_days": "Math in 30 Days — A structured daily plan covering the full curriculum in one month",
    "quiz": "Quizzes — Quick 15-minute assessments for every topic to track progress",
    "puzzles": "Puzzles & Brain Teasers — Curriculum-aligned games and challenges that make math fun",
    "worksheet": "Worksheets — Standalone printable activities for any topic, any order",
    "practice_tests": "Practice Tests (3, 5, 7, or 10 editions) — Full-length, unique tests with detailed answer explanations — every edition contains different, non-overlapping tests",
}


def get_cross_sell(bundle_type: str) -> List[str]:
    """Return cross-sell descriptions for books NOT in this bundle."""
    bundle = BUNDLE_DEFINITIONS[bundle_type]
    exclude = bundle["cross_sell_exclude"]
    result = []
    for key, desc in SERIES_DESCRIPTIONS.items():
        if key in exclude:
            continue
        # Skip individual PT keys if any PT is excluded
        if key == "practice_tests" and any(k.endswith("_practice_tests") for k in exclude):
            continue
        result.append(desc)
    return result


# ============================================================================
# BOOK DISPLAY NAMES (for the "What's in the Bundle" section)
# ============================================================================

BOOK_DISPLAY_NAMES: Dict[str, str] = {
    "study_guide": "Study Guide",
    "workbook": "Workbook",
    "step_by_step": "Step-by-Step Guide",
    "in_30_days": "Math in 30 Days",
    "quiz": "Quizzes",
    "puzzles": "Puzzles & Brain Teasers",
    "worksheet": "Worksheets",
    "3_practice_tests": "3 Practice Tests",
    "5_practice_tests": "5 Practice Tests",
    "7_practice_tests": "7 Practice Tests",
    "10_practice_tests": "10 Practice Tests",
}

BOOK_ONE_LINERS: Dict[str, str] = {
    "study_guide": "Key concepts, essential examples, and quick practice for every topic",
    "workbook": "Hundreds of practice problems organized by topic, progressing from easy to challenging",
    "step_by_step": "Numbered instructions for every problem type, road maps, and common-mistake alerts",
    "in_30_days": "A day-by-day study plan covering the full curriculum in one month",
    "quiz": "One 15-minute quiz per topic with scoring guide and answer key",
    "puzzles": "6–8 curriculum-aligned puzzles per topic: code breakers, mystery numbers, riddles, mazes, and more",
    "worksheet": "Standalone printable pages for any topic, usable in any order",
    "3_practice_tests": "Three unique full-length tests with detailed answer explanations",
    "5_practice_tests": "Five more unique tests for extra practice",
    "7_practice_tests": "Seven unique tests with detailed answers",
    "10_practice_tests": "Ten unique tests with answer explanations",
}


# ============================================================================
# TPT BUNDLE TITLE TIERS  (max 80 characters)
# ============================================================================
#
# Same approach as book_tpt_title() in config.py — for each bundle type we
# define progressively shorter title and subtitle variants.  bundle_tpt_title()
# tries every title × subtitle combination and picks the longest one that
# fits within 80 characters, maximising keyword coverage.

TPT_TITLE_MAX_LENGTH: int = 80

_BUNDLE_TPT_TIERS: Dict[str, Dict[str, list]] = {
    "practice_tests_bundle": {
        "titles": [
            "{state_exam} {grade} Practice Tests Bundle",
        ],
        "subtitles": [
            "25 Unique Full-Length Tests",
            "25 Full-Length Tests",
            "25 Unique Tests",
            "25 Tests",
        ],
    },
    "study_practice_bundle": {
        "titles": [
            "{state_exam} {grade} Study & Practice Bundle",
        ],
        "subtitles": [
            "Study Guide, Workbook & 25 Practice Tests",
            "Study Guide, Workbook & 25 Tests",
            "Guide, Workbook & 25 Tests",
            "6 Books & 25 Tests",
        ],
    },
    "test_prep_bundle": {
        "titles": [
            "{state_exam} {grade} Test Prep Bundle",
        ],
        "subtitles": [
            "30-Day Plan, Quizzes & 25 Practice Tests",
            "30-Day Plan, Quizzes & 25 Tests",
            "30-Day Plan & 25 Tests",
            "Quizzes & 25 Tests",
        ],
    },
    "classroom_bundle": {
        "titles": [
            "{state_exam} {grade} Classroom Bundle",
        ],
        "subtitles": [
            "Step-by-Step, Workbook, Quizzes & 25 Tests",
            "Workbook, Quizzes & 25 Tests",
            "8 Books & 25 Tests",
            "8 Books with 25 Tests",
        ],
    },
    "activities_assessments_bundle": {
        "titles": [
            "{state_exam} {grade} Activities & Assessments Bundle",
            "{state_exam} {grade} Activities & Assessments",
        ],
        "subtitles": [
            "Puzzles, Worksheets & Quizzes",
            "Puzzles & Worksheets",
        ],
    },
    "complete_series_bundle": {
        "titles": [
            "{state_exam} {grade} Complete Series Bundle",
            "{state_exam} {grade} Complete Bundle",
        ],
        "subtitles": [
            "11 Books with 25 Practice Tests",
            "11 Books & 25 Tests",
            "All 11 Books",
        ],
    },
}

# Keep the old name around as an alias so existing callers don't break.
# Each value is the *first* (longest) title pattern — suitable for non-TPT
# contexts where the 80-char limit doesn't apply.
BUNDLE_TITLE_PATTERNS: Dict[str, str] = {
    bt: tiers["titles"][0]
    + (": " + tiers["subtitles"][0] if tiers["subtitles"] else "")
    for bt, tiers in _BUNDLE_TPT_TIERS.items()
}


def _fill_bundle_template(template: str, state_exam: str, grade: str) -> str:
    """Fill a bundle title/subtitle template, collapsing extra whitespace."""
    result = template.format(state_exam=state_exam, grade=grade)
    while "  " in result:
        result = result.replace("  ", " ")
    return result.strip()


def bundle_tpt_title(
    bundle_type: str,
    state_slug: str,
    state_name: str,
) -> str:
    """Generate a TPT-friendly bundle title (≤ 80 chars).

    Uses the same tiered approach as ``book_tpt_title()`` in config.py:
    tries every title × subtitle combination from ``_BUNDLE_TPT_TIERS``
    and picks the **longest** one that fits within 80 characters.

    Fallback order:
      1. Longest "title: subtitle" combination that fits ≤ 80 chars
      2. Title only (if no subtitle combination fits)
      3. Truncated title (absolute last resort)
    """
    tiers = _BUNDLE_TPT_TIERS.get(bundle_type)

    # Build state_exam prefix (e.g. "Texas STAAR")
    exams = load_state_exams()
    exam = exams.get(state_slug, {})
    exam_acronym = exam.get("exam_acronym", "")
    state_exam = f"{state_name} {exam_acronym}".strip()
    grade = GRADE_DISPLAY

    if not tiers:
        # Unknown bundle type — simple fallback
        fallback = f"{state_exam} {grade} {bundle_type.replace('_', ' ').title()}"
        return fallback[:TPT_TITLE_MAX_LENGTH]

    title_templates = tiers["titles"]
    subtitle_tiers = sorted(tiers["subtitles"], key=len, reverse=True)

    resolved_titles = [
        _fill_bundle_template(t, state_exam, grade) for t in title_templates
    ]

    best: Optional[str] = None
    for title_str in resolved_titles:
        for sub in subtitle_tiers:
            candidate = f"{title_str}: {sub}"
            if len(candidate) <= TPT_TITLE_MAX_LENGTH:
                if best is None or len(candidate) > len(best):
                    best = candidate
                break  # Best subtitle for this title found

    if best is not None:
        return best

    # No subtitle fits — use the shortest title variant that fits
    for title_str in resolved_titles:
        if len(title_str) <= TPT_TITLE_MAX_LENGTH:
            return title_str

    # Absolute last resort — truncate
    return resolved_titles[0][:TPT_TITLE_MAX_LENGTH]


# ============================================================================
# MAIN: PRINT FACTS
# ============================================================================

SUPPORTED_BUNDLES = list(BUNDLE_DEFINITIONS.keys())


def print_facts(bundle_type: str, state_slug: str) -> None:
    config = load_config(WORKSPACE)

    # Validate
    if bundle_type not in SUPPORTED_BUNDLES:
        print(f"ERROR: Unknown bundle type '{bundle_type}'.", file=sys.stderr)
        print(f"Supported: {', '.join(SUPPORTED_BUNDLES)}", file=sys.stderr)
        sys.exit(1)
    if state_slug not in config.all_state_slugs:
        print(f"ERROR: Unknown state '{state_slug}'.", file=sys.stderr)
        print(f"Example states: {', '.join(config.all_state_slugs[:5])}...", file=sys.stderr)
        sys.exit(1)

    state_name = config.state_display_names[state_slug]
    bundle = BUNDLE_DEFINITIONS[bundle_type]

    # Exam & curriculum
    exams = load_state_exams()
    curriculums = load_state_curriculums()
    exam = exams.get(state_slug, {})
    curr = curriculums.get(state_slug, {})

    exam_name = exam.get("exam_name", "")
    exam_acronym = exam.get("exam_acronym", "")
    curr_name = curr.get("curriculum_name", "")
    curr_acronym = curr.get("curriculum_acronym", "")

    # Build the state_exam prefix for titles (e.g. "Texas STAAR")
    state_exam_prefix = state_name
    if exam_acronym:
        state_exam_prefix = f"{state_name} {exam_acronym}"

    # Chapter summaries
    chapter_summaries, num_topics = build_chapter_summaries(state_slug, config)
    num_chapters = len(chapter_summaries)

    # Title entries for each book in the bundle
    book_titles = {}
    for bt in bundle["book_types"]:
        entry = find_title_entry(bt, state_slug)
        if entry:
            book_titles[bt] = entry.get("tpt_title", entry.get("title", ""))

    # Bundle TPT title (≤ 80 chars)
    bundle_title = bundle_tpt_title(bundle_type, state_slug, state_name)

    # Cross-sell
    cross_sell = get_cross_sell(bundle_type)

    # ── Print report ────────────────────────────────────────────────────
    print("=" * 70)
    print(f"BUNDLE FACTS: {bundle_type} × {state_slug}")
    print("=" * 70)

    print()
    print("--- BUNDLE TITLE ---")
    print(f"Book Title:          {bundle_title}")
    print(f"Display Name:       {bundle['display_name']}")
    print(f"Price Tier:         {bundle['price_tier']}")
    print(f"Number of Books:    {bundle['num_books']}")

    print()
    print("--- WHAT IT IS ---")
    print(f"  {bundle['what_it_is']}")

    print()
    print("--- VALUE PROPOSITION ---")
    print(f"  {bundle['value_proposition']}")

    if bundle["includes_practice_tests"]:
        print()
        print("--- PRACTICE TESTS ---")
        print(f"  Total Tests:      {bundle['total_tests']}")
        print(f"  Questions/Test:   {QUESTIONS_PER_TEST}")
        print(f"  Total Questions:  {bundle['total_questions']}")
        print(f"  *** All four practice test editions contain completely different tests.")
        print(f"  *** No repeated questions across any of the four books.")
        print(f"  *** Always mention that the 25 tests are unique and non-overlapping.")

    print()
    print("--- BOOKS IN THE BUNDLE ---")
    for bt in bundle["book_types"]:
        name = BOOK_DISPLAY_NAMES.get(bt, bt)
        liner = BOOK_ONE_LINERS.get(bt, "")
        title_str = ""
        if bt in book_titles:
            title_str = f"  (Book title: {book_titles[bt]})"
        print(f"  • {name} — {liner}{title_str}")

    if "how_books_work_together" in bundle:
        print()
        print("--- HOW THE BOOKS WORK TOGETHER ---")
        for key, desc in bundle["how_books_work_together"].items():
            name = BOOK_DISPLAY_NAMES.get(key, key)
            print(f"  {name}: {desc}")
            print()

    print()
    print("--- STATE ---")
    print(f"State:              {state_name}")

    print()
    print("--- CURRICULUM ---")
    if curr_name:
        print(f"Curriculum Name:    {curr_name}")
        print(f"Curriculum Acronym: {curr_acronym}")
    else:
        print("Curriculum Name:    (not available)")

    print()
    print("--- EXAM ---")
    if exam_name:
        print(f"Exam Name:          {exam_name}")
        print(f"Exam Acronym:       {exam_acronym}")
    else:
        print("Exam Name:          (none)")

    print()
    print("--- CHAPTERS & TOPICS ---")
    print(f"Total Topics:       {num_topics}")
    print(f"Total Chapters:     {num_chapters}")
    print()
    for ch_num, ch_title, ch_count in chapter_summaries:
        print(f"  Chapter {ch_num}: {ch_title} — {ch_count} topic{'s' if ch_count != 1 else ''}")

    print()
    print("--- KEY SELLING POINTS ---")
    for sp in bundle["key_selling_points"]:
        print(f"  • {sp}")

    print()
    print("--- USE CASES ---")
    for uc in bundle["use_cases"]:
        print(f"  • {uc}")

    if cross_sell:
        print()
        print("--- CROSS-SELL (other books / bundles to mention) ---")
        if bundle.get("cross_sell_note"):
            print(f"  Note: {bundle['cross_sell_note']}")
        for desc in cross_sell:
            print(f"  • {desc}")

    print()
    print("--- FILE SAVE PATH ---")
    print(f"  final_output/bundles/{bundle_type}/{state_slug}_tpt_bundle.html")

    print()
    print("=" * 70)
    print("END OF FACTS")
    print("=" * 70)


# ============================================================================
# CLI
# ============================================================================

def main() -> None:
    if len(sys.argv) == 2:
        flag = sys.argv[1]
        if flag == "--list-bundles":
            for b in SUPPORTED_BUNDLES:
                info = BUNDLE_DEFINITIONS[b]
                print(f"  {b:40s} {info['num_books']} books — {info['display_name']}")
            return
        if flag == "--list-states":
            config = load_config(WORKSPACE)
            for slug in config.all_state_slugs:
                print(f"  {slug}")
            return

    if len(sys.argv) != 3:
        print("Usage: get_bundle_facts.py <bundle_type> <state_slug>", file=sys.stderr)
        print("       get_bundle_facts.py --list-bundles", file=sys.stderr)
        print("       get_bundle_facts.py --list-states", file=sys.stderr)
        sys.exit(1)

    bundle_type = sys.argv[1]
    state_slug = sys.argv[2]
    print_facts(bundle_type, state_slug)


if __name__ == "__main__":
    main()
