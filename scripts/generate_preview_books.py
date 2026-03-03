#!/usr/bin/env python3
"""
Generate preview .tex files for Grade 4 math books.

For each state × book type, this script generates a lightweight preview PDF
that contains:
  1. Cover page
  2. Key initial pages (copyright, how-to-use, table of contents)
  3. 2 sample topics from different chapters (or partial content for tests)
  4. A "Get the Full Book" call-to-action page
  5. A diagonal "PREVIEW" watermark on every page

Preview PDFs are intended for Teachers Pay Teachers listings and the
ViewMath.com website. They are saved alongside the full book PDFs in
final_output/<book_type>/ as <state>_preview_<date>.pdf.

Book Types Supported:
  - all_in_one
  - study_guide
  - workbook
  - step_by_step
  - in_30_days
  - 3_practice_tests, 5_practice_tests, 7_practice_tests, 10_practice_tests
  - quiz

Usage:
    # Generate preview for all book types, all states
    python3 scripts/generate_preview_books.py --book-type all

    # Same as 'all' (alias used by compile script terminology)
    python3 scripts/generate_preview_books.py --book-type all_previews

    # Generate preview for a specific book type
    python3 scripts/generate_preview_books.py --book-type study_guide

    # Specific states only
    python3 scripts/generate_preview_books.py --book-type all --states texas,california

    # Dry-run
    python3 scripts/generate_preview_books.py --book-type all --dry-run --verbose
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

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

BOOK_TYPES: Dict[str, dict] = {
    "all_in_one": {
        "description": "All-in-One preview (cover + initial pages + 2 sample topics)",
    },
    "study_guide": {
        "description": "Study Guide preview (cover + initial pages + 2 sample topics)",
    },
    "workbook": {
        "description": "Workbook preview (cover + initial pages + 2 sample topics)",
    },
    "step_by_step": {
        "description": "Step-by-Step preview (cover + initial pages + 2 sample topics)",
    },
    "3_practice_tests": {
        "description": "3 Practice Tests preview (cover + initial pages + 1 partial test)",
        "test_range": (1, 3),
    },
    "5_practice_tests": {
        "description": "5 Practice Tests preview (cover + initial pages + 1 partial test)",
        "test_range": (4, 8),
    },
    "7_practice_tests": {
        "description": "7 Practice Tests preview (cover + initial pages + 1 partial test)",
        "test_range": (9, 15),
    },
    "10_practice_tests": {
        "description": "10 Practice Tests preview (cover + initial pages + 1 partial test)",
        "test_range": (16, 25),
    },
    "in_30_days": {
        "description": "30-Day preview (cover + initial pages + 2 sample days)",
    },
    "quiz": {
        "description": "Quiz Book preview (cover + initial pages + 2 sample quizzes)",
    },
    "puzzles": {
        "description": "Puzzles & Brain Teasers preview (cover + initial pages + 2 sample topics)",
    },
    "worksheet": {
        "description": "Worksheet preview (cover + initial pages + 2 sample topics)",
    },
}

# Which sample topics to include in previews (by index into chapter topics).
# We pick topics from chapters 1 and 3 to show variety.
# Format: list of (chapter_index, topic_index_within_chapter)
SAMPLE_TOPIC_PICKS = [
    (0, 0),   # First topic of Chapter 1
    (2, 0),   # First topic of Chapter 3
]

# For in_30_days: which day numbers to include
SAMPLE_DAY_PICKS = [1, 9]  # Day 1 (Ch1) and Day 9 (Ch2)


# ============================================================================
# PREVIEW PREAMBLE — common across all studyGuide-based books
# ============================================================================

def _preview_preamble_studyguide() -> List[str]:
    """Return preamble lines for preview books using studyGuide class."""
    return [
        r"\documentclass[12pt, fleqn, openany]{studyGuide}",
        "",
        "% Line spacing for young readers",
        r"\setstretch{1.4}",
        "",
        "% PREVIEW watermark on every page",
        r"\usepackage{VM_packages/VMfunPreview}",
        "",
    ]


def _preview_preamble_in30days() -> List[str]:
    """Return preamble lines for preview books using in30Days class."""
    return [
        r"\documentclass[12pt, fleqn, openany]{in30Days}",
        "",
        "% Line spacing for young readers",
        r"\setstretch{1.4}",
        "",
        "% PREVIEW watermark on every page",
        r"\usepackage{VM_packages/VMfunPreview}",
        "",
    ]


# ============================================================================
# TOPIC INPUT LINE HELPERS (reused from generate_state_books.py logic)
# ============================================================================

def _topic_input(
    topic_id: str,
    modified_dict: Dict[str, str],
    additional_set: Set[str],
    config: TopicsConfig,
    base_dir: str,
    modified_dir: str,
    additional_dir: str,
) -> str:
    """Return the \\input{...} line for a single topic, selecting the right directory."""
    filename = config.topic_filenames[topic_id]
    if topic_id in modified_dict:
        mod_filename = modified_dict[topic_id]
        return f"\\input{{{modified_dir}/{mod_filename}}}"
    elif topic_id in additional_set:
        return f"\\input{{{additional_dir}/{filename}}}"
    else:
        return f"\\input{{{base_dir}/{filename}}}"


def _all_in_one_input(tid, mod, add, cfg):
    return _topic_input(tid, mod, add, cfg, "topics", "topics_modifed", "topics_additional")

def _study_guide_input(tid, mod, add, cfg):
    return _topic_input(tid, mod, add, cfg, "topics_study_guide", "topics_study_guide_modifed", "topics_study_guide_additional")

def _workbook_input(tid, mod, add, cfg):
    return _topic_input(tid, mod, add, cfg, "topics_workbook", "topics_workbook_modifed", "topics_workbook_additional")

def _steps_input(tid, mod, add, cfg):
    return _topic_input(tid, mod, add, cfg, "steps_topics", "steps_topics_modifed", "steps_topics_additional")

def _quiz_input(tid, mod, add, cfg):
    return _topic_input(tid, mod, add, cfg, "topics_quiz", "topics_quiz_modifed", "topics_quiz_additional")

def _puzzles_input(tid, mod, add, cfg):
    return _topic_input(tid, mod, add, cfg, "topics_puzzles", "topics_puzzles_modifed", "topics_puzzles_additional")

def _worksheet_input(tid, mod, add, cfg):
    return _topic_input(tid, mod, add, cfg, "topics_worksheet", "topics_worksheet_modifed", "topics_worksheet_additional")


# ============================================================================
# SAMPLE TOPIC PICKER
# ============================================================================

def _pick_sample_topics(
    config: TopicsConfig,
    modified_set: Set[str],
    additional_set: Set[str],
) -> List[dict]:
    """Pick 2 sample topics from different chapters.

    Returns list of dicts: [{'chapter': Chapter, 'topic_id': str}, ...]
    """
    picks = []
    for ch_idx, topic_idx in SAMPLE_TOPIC_PICKS:
        if ch_idx < len(config.chapters):
            chapter = config.chapters[ch_idx]
            all_topic_ids = list(chapter.core_topic_ids)
            # Also include additional topics for this chapter
            ch_prefix = f"ch{chapter.num:02d}-"
            additional_for_ch = sorted(
                [t for t in additional_set if t.startswith(ch_prefix)]
            )
            all_topic_ids.extend(additional_for_ch)

            if topic_idx < len(all_topic_ids):
                picks.append({
                    "chapter": chapter,
                    "topic_id": all_topic_ids[topic_idx],
                })
    return picks


# ============================================================================
# PREVIEW GENERATORS — one per book type
# ============================================================================

def generate_preview_all_in_one(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for All-in-One book."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    lines: List[str] = []

    # Header
    lines.append("% PREVIEW — Grade 4 Math Made Clear - All-in-One")
    lines.append("% This is a sample preview. Get the full book for all topics!")
    lines.extend(_preview_preamble_studyguide())
    lines.append(r"\begin{document}")
    lines.append("")

    # Initial pages
    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math Made Clear}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{The Complete All-in-One Guide with Lessons,\\Examples, and Practice}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/all_in_one/00-welcome}")
    lines.append(r"\input{initial_pages/all_in_one/01-how-to-use}")
    lines.append(r"\input{initial_pages/all_in_one/08-whats-inside}")
    lines.append(r"\input{initial_pages/all_in_one/03-math-symbols-words}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    # Sample topics
    picks = _pick_sample_topics(config, modified_set, additional_set)
    for pick in picks:
        ch = pick["chapter"]
        tid = pick["topic_id"]
        lines.append(f"\\chapter{{{ch.title}}}")
        lines.append(_all_in_one_input(tid, modified_dict, additional_set, config))
        lines.append("")

    # CTA page
    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_study_guide(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for Study Guide."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    lines: List[str] = []
    lines.append("% PREVIEW \u2014 Grade 4 Math Made Easy - Study Guide")
    lines.extend(_preview_preamble_studyguide())
    lines.append(r"\begin{document}")
    lines.append("")

    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math Made Easy}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{Study Guide with Key Concepts,\\Review \\& Practice}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/study_guide/00-welcome}")
    lines.append(r"\input{initial_pages/study_guide/01-how-to-use}")
    lines.append(r"\input{initial_pages/study_guide/02-math-symbols-words}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    picks = _pick_sample_topics(config, modified_set, additional_set)
    for pick in picks:
        ch = pick["chapter"]
        tid = pick["topic_id"]
        lines.append(f"\\chapter{{{ch.title}}}")
        lines.append(_study_guide_input(tid, modified_dict, additional_set, config))
        lines.append("")

    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_workbook(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for Workbook."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    lines: List[str] = []
    lines.append("% PREVIEW \u2014 Grade 4 Math Workbook")
    lines.extend(_preview_preamble_studyguide())
    lines.append(r"\begin{document}")
    lines.append("")

    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math Workbook}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{Practice Problems \\& Exercises\\with Answer Key}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/workbook/00-welcome}")
    lines.append(r"\input{initial_pages/workbook/01-how-to-use}")
    lines.append(r"\input{initial_pages/workbook/03-math-reference}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    picks = _pick_sample_topics(config, modified_set, additional_set)
    for pick in picks:
        ch = pick["chapter"]
        tid = pick["topic_id"]
        lines.append(f"\\chapter{{{ch.title}}}")
        lines.append(_workbook_input(tid, modified_dict, additional_set, config))
        lines.append("")

    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_step_by_step(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for Step-by-Step."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    lines: List[str] = []
    lines.append("% PREVIEW \u2014 Grade 4 Math Step by Step")
    lines.extend(_preview_preamble_studyguide())
    lines.append(r"\begin{document}")
    lines.append("")

    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math Step by Step}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{A Beginner Friendly Guide\\to Learning Math}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/step_by_step/00-welcome}")
    lines.append(r"\input{initial_pages/step_by_step/01-how-to-use}")
    lines.append(r"\input{initial_pages/step_by_step/02-how-every-topic-works}")
    lines.append(r"\input{initial_pages/all_in_one/03-math-symbols-words}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    picks = _pick_sample_topics(config, modified_set, additional_set)
    for pick in picks:
        ch = pick["chapter"]
        tid = pick["topic_id"]
        lines.append(f"\\chapter{{{ch.title}}}")
        lines.append(_steps_input(tid, modified_dict, additional_set, config))
        lines.append("")

    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_practice_tests(
    state_slug: str,
    state_name: str,
    num_tests: int,
    test_start: int,
    test_end: int,
    workspace: Path,
    config: TopicsConfig,
) -> str:
    """Generate preview .tex for Practice Tests.

    Includes the first practice test's cover page + first 10 questions only.
    We truncate by using \\previewTestEnd after including the test file.
    """
    # Find the first available test
    practice_dir = workspace / "practice_tests" / state_slug
    first_test_num = None
    for i in range(test_start, test_end + 1):
        test_file = practice_dir / f"practice_test_{i:02d}.tex"
        if test_file.exists():
            first_test_num = i
            break

    lines: List[str] = []
    lines.append(f"% PREVIEW — Grade 4 Math — {num_tests} Practice Tests")
    lines.extend(_preview_preamble_studyguide())

    # Number of practice tests (used by tracker page)
    lines.append(f"\\newcommand{{\\NumPracticeTests}}{{{num_tests}}}")
    lines.append("")
    lines.append("% Enable answer & explanation collection for practice test questions")
    lines.append(r"\enablePracticeTestAnswers")
    lines.append("")
    lines.append(r"\begin{document}")
    lines.append("")

    # Initial pages (subset)
    lines.append(r"\pagenumbering{roman}")
    lines.append(rf"\renewcommand{{\VMBookTitle}}{{{num_tests} Full-Length Grade 4 Math Practice Tests}}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{Test Prep with Detailed\\Answer Explanations}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(rf"\input{{initial_pages/practice_tests_{num_tests}/00-welcome}}")
    lines.append(rf"\input{{initial_pages/practice_tests_{num_tests}/01-how-to-use}}")
    lines.append(rf"\input{{initial_pages/practice_tests_{num_tests}/02-test-taking-tips}}")
    lines.append(r"\input{initial_pages/practice_tests/04-math-reference}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    # Include the first practice test (full — the watermark deters copying)
    if first_test_num is not None:
        lines.append("% ============================================================================")
        lines.append("% SAMPLE PRACTICE TEST")
        lines.append("% ============================================================================")
        lines.append(f"\\practiceTestPage{{1}}{{{30}}}")
        lines.append("")
        lines.append(f"\\input{{practice_tests/{state_slug}/practice_test_{first_test_num:02d}}}")
        lines.append("")
        lines.append(f"\\testScorePage{{1}}{{{30}}}")
        lines.append("")
    else:
        lines.append("% No practice test files found for preview")
        lines.append("")

    # CTA page
    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_in_30_days(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for In 30 Days."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)

    if config.in_30_days_config is None:
        return ""

    days_config = config.in_30_days_config

    lines: List[str] = []
    lines.append("% PREVIEW — Grade 4 Math in 30 Days")
    lines.extend(_preview_preamble_in30days())
    lines.append(r"\begin{document}")
    lines.append("")

    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math in 30 Days}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{A Day-by-Day Study Plan\\to Master Grade 4 Math}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/in_30_days/00-welcome}")
    lines.append(r"\input{initial_pages/in_30_days/01-how-to-use}")
    lines.append(r"\input{initial_pages/in_30_days/05-your-30-day-plan}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    # Build chapter boundaries lookup
    day_to_chapter: Dict[int, dict] = {}
    for ch in days_config.chapters:
        for d in range(ch.start_day, ch.end_day + 1):
            day_to_chapter[d] = {"num": ch.chapter, "title": ch.title}

    # Include 2 sample days from different chapters
    emitted_chapters: set = set()
    for target_day_num in SAMPLE_DAY_PICKS:
        for day_entry in days_config.days:
            if day_entry.day == target_day_num:
                ch_info = day_to_chapter.get(target_day_num, {})
                ch_num = ch_info.get("num", 0)
                ch_title = ch_info.get("title", f"Chapter {ch_num}")

                if ch_num not in emitted_chapters:
                    lines.append(f"\\chapter{{{ch_title}}}")
                    lines.append("")
                    emitted_chapters.add(ch_num)

                # Decide directory
                modified_in_day = [t for t in day_entry.topics if t in modified_set]
                if modified_in_day:
                    lines.append(f"\\input{{topics_in30days_modifed/{day_entry.file}}}")
                else:
                    lines.append(f"\\input{{topics_in30days/{day_entry.file}}}")
                lines.append("")
                break

    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_quiz(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for Quiz Book."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    lines: List[str] = []
    lines.append("% PREVIEW \u2014 Grade 4 Math Quizzes")
    lines.extend(_preview_preamble_studyguide())
    lines.append("% Enable quiz-specific answer key")
    lines.append(r"\enableQuizAnswers")
    lines.append("")
    lines.append(r"\begin{document}")
    lines.append("")

    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math Quizzes}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{Quick Topic Assessments\\with Answer Key}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/quiz/00-welcome}")
    lines.append("")
    lines.append(r"\cleardoublepage")
    lines.append(r"\friendlyTOC")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    # 2 sample quizzes from different chapters
    picks = _pick_sample_topics(config, modified_set, additional_set)
    for pick in picks:
        ch = pick["chapter"]
        tid = pick["topic_id"]
        lines.append(f"\\chapter{{{ch.title}}}")
        lines.append(f"\\setcounter{{quizChapter}}{{{ch.num}}}")
        lines.append(_quiz_input(tid, modified_dict, additional_set, config))
        lines.append("")

    # Answer key for the sample quizzes
    lines.append(r"\printAnswerKey")
    lines.append("")

    # CTA page
    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_puzzles(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for Puzzles & Brain Teasers book."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    lines: List[str] = []
    lines.append("% PREVIEW \u2014 Grade 4 Math Puzzles & Brain Teasers")
    lines.extend(_preview_preamble_studyguide())
    lines.append(r"\begin{document}")
    lines.append("")

    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math Puzzles \\& Brain Teasers}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{Fun Math Games, Activities\\\\& Challenges}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/puzzles/00-welcome}")
    lines.append(r"\input{initial_pages/puzzles/01-how-to-use}")
    lines.append(r"\input{initial_pages/puzzles/03-math-symbols-words}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    picks = _pick_sample_topics(config, modified_set, additional_set)
    for pick in picks:
        ch = pick["chapter"]
        tid = pick["topic_id"]
        lines.append(f"\\chapter{{{ch.title}}}")
        lines.append(_puzzles_input(tid, modified_dict, additional_set, config))
        lines.append("")

    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


def generate_preview_worksheet(
    state_slug: str, state_name: str, config: TopicsConfig,
) -> str:
    """Generate preview .tex for Worksheet book."""
    modified_dict = config.state_modified.get(state_slug, {})
    modified_set = set(modified_dict)
    additional_set = set(config.state_additional.get(state_slug, []))

    lines: List[str] = []
    lines.append("% PREVIEW \u2014 Grade 4 Math Worksheets")
    lines.extend(_preview_preamble_studyguide())
    lines.append(r"\begin{document}")
    lines.append("")

    lines.append(r"\pagenumbering{roman}")
    lines.append(r"\renewcommand{\VMBookTitle}{Grade 4 Math Worksheets}")
    lines.append(r"\renewcommand{\VMBookSubtitle}{Printable Practice Pages\\with Answer Key}")
    lines.append(r"\input{initial_pages/common/copyright_page}")
    lines.append(r"\input{initial_pages/worksheet/00-welcome}")
    lines.append(r"\input{initial_pages/worksheet/01-how-to-use}")
    lines.append(r"\input{initial_pages/worksheet/03-math-symbols-words}")
    lines.append("")
    lines.append(r"\tableofcontents")
    lines.append(r"\cleardoublepage")
    lines.append(r"\pagenumbering{arabic}")
    lines.append("")

    picks = _pick_sample_topics(config, modified_set, additional_set)
    for pick in picks:
        ch = pick["chapter"]
        tid = pick["topic_id"]
        lines.append(f"\\chapter{{{ch.title}}}")
        lines.append(_worksheet_input(tid, modified_dict, additional_set, config))
        lines.append("")

    lines.append(r"\input{initial_pages/common/preview-cta-page}")
    lines.append("")
    lines.append(r"\end{document}")
    lines.append("")
    return "\n".join(lines)


# ============================================================================
# OUTPUT HELPERS
# ============================================================================

def preview_tex_filename(book_type: str, state_slug: str) -> str:
    """e.g. preview_study_guide_texas-grade4.tex"""
    return f"preview_{book_type}_{state_slug}-grade4.tex"


def write_preview(
    workspace: Path,
    state_slug: str,
    book_type: str,
    content: str,
    dry_run: bool = False,
) -> Path:
    """Write a generated preview .tex file to state_books/<state>/."""
    out_dir = workspace / "state_books" / state_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / preview_tex_filename(book_type, state_slug)

    if not dry_run:
        out_path.write_text(content, encoding="utf-8")

    return out_path


# ============================================================================
# CLI
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate preview .tex files for Grade 4 math books.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s --book-type all                        # all book types, all states
    %(prog)s --book-type all_previews               # alias of all
  %(prog)s --book-type study_guide                # study guide previews
  %(prog)s --book-type all --states texas,florida
  %(prog)s --book-type quiz --dry-run --verbose
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
        choices=list(BOOK_TYPES.keys()) + ["all", "all_previews"],
        default=None,
        help="Book type to generate preview for, or 'all'/'all_previews' (interactive if omitted)",
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
        help="Skip title injection — use the generic titles baked into each preview generator.",
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

    # ── Load config ─────────────────────────────────────────────────────
    config = load_config(workspace)

    # ── Load titles JSON ────────────────────────────────────────────────
    titles = None
    if not args.no_titles:
        titles_path = args.titles_file or default_titles_json_path()
        try:
            titles = load_book_titles(titles_path)
            print(f"📋 Titles: loaded {len(titles)} entries from {titles_path.name}")
        except FileNotFoundError:
            print(
                f"⚠️  Titles file not found: {titles_path}\n"
                "   Preview titles will use the generic defaults.\n"
                "   To use state-specific SEO titles, generate first:\n"
                "     python3 scripts/generate_book_titles.py "
                "--format json --output titles.json"
            )

    # ── Interactive prompts when arguments are omitted ──────────────────
    book_type = args.book_type
    if book_type is None:
        descs = {k: v.get("description", "") for k, v in BOOK_TYPES.items()}
        book_type = prompt_book_type(
            list(BOOK_TYPES.keys()),
            descriptions=descs,
            allow_all=True,
            allow_all_previews=True,
        )

    # ── Resolve book types ──────────────────────────────────────────────
    if book_type in {"all", "all_previews"}:
        book_types = list(BOOK_TYPES.keys())
    else:
        book_types = [book_type]

    # ── Resolve states ──────────────────────────────────────────────────
    if args.states:
        requested = [s.strip().lower() for s in args.states.split(",")]
        unknown = [s for s in requested if s not in config.all_state_slugs]
        if unknown:
            print(f"ERROR: Unknown state(s): {', '.join(unknown)}")
            sys.exit(1)
        state_slugs = requested
    else:
        states_input = prompt_states(config.all_state_slugs)
        if states_input is None:
            state_slugs = config.all_state_slugs
        else:
            state_slugs = [s.strip().lower() for s in states_input.split(",")]

    # ── Generate previews ───────────────────────────────────────────────
    total = 0

    for bt_key in book_types:
        bt_cfg = BOOK_TYPES[bt_key]
        bt_pretty = bt_key.replace("_", " ").title()
        print(f"\n{'='*60}")
        print(f"👁  Generating Preview: {bt_pretty}")
        print(f"   {bt_cfg['description']}")
        print(f"{'='*60}")

        for slug in state_slugs:
            state_name = config.state_display_names[slug]

            if bt_key == "all_in_one":
                content = generate_preview_all_in_one(slug, state_name, config)
            elif bt_key == "study_guide":
                content = generate_preview_study_guide(slug, state_name, config)
            elif bt_key == "workbook":
                content = generate_preview_workbook(slug, state_name, config)
            elif bt_key == "step_by_step":
                content = generate_preview_step_by_step(slug, state_name, config)
            elif bt_key.endswith("_practice_tests"):
                num_tests = int(bt_key.split("_")[0])
                test_start, test_end = bt_cfg["test_range"]
                content = generate_preview_practice_tests(
                    slug, state_name, num_tests, test_start, test_end,
                    workspace, config,
                )
            elif bt_key == "in_30_days":
                content = generate_preview_in_30_days(slug, state_name, config)
            elif bt_key == "quiz":
                content = generate_preview_quiz(slug, state_name, config)
            elif bt_key == "puzzles":
                content = generate_preview_puzzles(slug, state_name, config)
            elif bt_key == "worksheet":
                content = generate_preview_worksheet(slug, state_name, config)
            else:
                print(f"  🚫 Unknown book type: {bt_key}")
                continue

            if not content:
                if args.verbose:
                    print(f"  ⚠️  Skipped {slug} (empty content)")
                continue

            # Inject state-specific title / subtitle (same as full books)
            content = inject_titles_into_tex(
                content, bt_key, slug, state_name, titles,
            )

            out_path = write_preview(
                workspace, slug, bt_key, content, dry_run=args.dry_run,
            )
            total += 1

            if args.verbose or args.dry_run:
                rel = out_path.relative_to(workspace)
                action = "Would write" if args.dry_run else "Wrote"
                print(f"  ✅ {action}: {rel}")

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    action = "Would generate" if args.dry_run else "Generated"
    print(f"✅ {action} {total} preview .tex files")


if __name__ == "__main__":
    main()
