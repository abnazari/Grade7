#!/usr/bin/env python3
"""
TPT Listing Description Generator — Grade 7 Math Books.

Generates HTML product descriptions for Teachers Pay Teachers (TPT) listings.
Each description is tailored to a specific (book_type × state) combination,
using standalone Jinja2 templates — one per book type.

Templates live in  html_templates/tpt/<book_type>.html.jinja
Each template is fully self-contained (no shared base or block includes).

Usage:
    # All states, all supported book types
    python3 scripts/generate_tpt_listings.py

    # Specific states
    python3 scripts/generate_tpt_listings.py --states texas,california

    # Specific book types
    python3 scripts/generate_tpt_listings.py --book-types study_guide,all_in_one

    # Preview without writing files
    python3 scripts/generate_tpt_listings.py --dry-run

    # Print a single listing to stdout
    python3 scripts/generate_tpt_listings.py --states texas --book-types study_guide --preview

    # Write directly into final_output/<book_type>/ (skips listings/tpt/ prefix)
    python3 scripts/generate_tpt_listings.py --book-folder

Output (default):
    final_output/listings/tpt/<book_type>/<state>_tpt_<date>.html

Output (--ai-rewrite):
    final_output/listings/tpt/<state>/<book_type>_<state>-grade7_<date>_tpt.html
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from jinja2 import Environment, FileSystemLoader

from config import BOOK_TYPES, BOOK_PRICES, find_workspace, prompt_book_type, prompt_states
from config_loader import TopicsConfig, load_config
from listing_data import (
    BOOK_TYPE_CONTENT,
    VARIATION_POOLS,
    get_book_content,
    pick_variation,
)


# ============================================================================
# CONSTANTS
# ============================================================================

TEMPLATE_DIR = "html_templates"
OUTPUT_DIR = "final_output/listings/tpt"
WEBSITE = "tpt"  # Used for variation pool hashing


# ============================================================================
# PDF HELPERS
# ============================================================================

def find_latest_pdf(workspace: Path, book_type: str, state_slug: str) -> Optional[Path]:
    """Return the most-recently-dated non-preview PDF for a state × book type.

    Looks in  final_output/<output_subdir>/<state>_<YYYY-MM-DD>.pdf
    and returns the lexicographically latest match (newest date).
    Returns None if no PDF exists.
    """
    bt_cfg = BOOK_TYPES.get(book_type, {})
    output_subdir = bt_cfg.get("output_subdir", book_type)
    pdf_dir = workspace / "final_output" / output_subdir
    if not pdf_dir.is_dir():
        return None
    candidates = sorted(
        pdf_dir.glob(f"{state_slug}_[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].pdf")
    )
    return candidates[-1] if candidates else None


def get_pdf_page_count(pdf_path: Path) -> str:
    """Return the page count of a PDF as a string, or '' on any error."""
    try:
        result = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=15,
        )
        for line in result.stdout.splitlines():
            if line.startswith("Pages:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return ""

# Book types with TPT templates.  Add new ones here as templates are created.
SUPPORTED_BOOK_TYPES: List[str] = [
    "all_in_one",
    "study_guide",
    "workbook",
    "step_by_step",
    "in_30_days",
    "quiz",
    "puzzles",
    "worksheet",
    "3_practice_tests",
    "5_practice_tests",
    "7_practice_tests",
    "10_practice_tests",
]


# ============================================================================
# TPT-SPECIFIC TAGLINE POOLS — no page counts or exam months
# ============================================================================
# These replace the shared tagline pools from listing_data.py which contain
# {page_count} and {exam_months} placeholders not suitable for TPT listings.

TPT_TAGLINE_POOLS: Dict[str, List[str]] = {
    "all_in_one": [
        "The complete Grade 7 math curriculum: teach it, practice it, master it",
        "Everything from place value to geometry — one cohesive, beautifully designed resource",
        "Stop juggling five different resources. This one book covers it all",
        "Full lessons with worked examples and practice for all {num_topics} {state_name} Grade 7 topics",
        "From the first day of school to the last — the Grade 7 math curriculum in one place",
        "Teaches every concept, shows how to solve every problem type, and lets students practice immediately",
        "The only Grade 7 math book you need: clear lessons, step-by-step examples, and hundreds of problems",
        "Lessons, examples, and practice for every single Grade 7 math topic — in one book",
    ],
    "study_guide": [
        "Every key concept, explained simply — the ultimate review companion",
        "Concise, focused, and perfect for quick review sessions",
        "All the important stuff, none of the fluff — Grade 7 math distilled",
        "When students need to review fast, this is the book they reach for",
        "Core concepts, key examples, and focused practice in one compact guide",
        "The quick-reference guide to Grade 7 math — clear, concise, and exactly what students need",
        "Don't re-teach the whole curriculum — just review what matters most",
        "A focused review of every {state_name} Grade 7 math standard — nothing extra, nothing missing",
    ],
    "workbook": [
        "Practice, practice, practice — the proven path to math mastery",
        "Hundreds of problems covering every {state_name} Grade 7 math standard",
        "The practice workbook that turns 'I don't get it' into 'I've got this!'",
        "Repetition builds mastery — and this workbook has problems to spare",
        "From easy warm-ups to challenging word problems — scaffolded practice for every skill",
        "Students learn math by doing math. This workbook gives them plenty to do",
        "Organized by topic so you can assign exactly the practice your students need",
        "The workbook {state_name} fourth graders need — problems for every standard, answers for every question",
    ],
    "step_by_step": [
        "Math made simple: clear, numbered steps for every Grade 7 problem type",
        "When students get stuck, this book shows them exactly what to do — step by step",
        "The math tutor that never gets frustrated: patient, step-by-step instructions",
        "No more 'I don't know how to start' — every problem type has a clear road map",
        "Turn confusion into clarity with guided, step-by-step instructions for every skill",
        "Like having a patient tutor sitting next to every student",
        "Break every problem into small, doable pieces — that's the power of step-by-step learning",
        "For students who need structure and guidance, this book is a game-changer",
    ],
    "in_30_days": [
        "30 days. Every topic. Total confidence. Let's go",
        "Master the entire Grade 7 math curriculum in just one month",
        "A day-by-day plan that transforms overwhelmed students into confident math learners",
        "Structure eliminates stress — 30 daily lessons with zero guesswork",
        "One day at a time. One topic at a time. 30 days to Grade 7 math mastery",
        "The most focused 30 days of math your students will ever experience",
        "For students who need to catch up, keep up, or get ahead — in 30 days flat",
        "Daily lessons with built-in practice — just follow the plan and watch students grow",
    ],
    "quiz": [
        "Quick, focused quizzes that tell you exactly where students stand",
        "15 minutes per quiz, one per topic — the fastest way to assess Grade 7 math skills",
        "Know what your students know (and don't know) — without giving up an entire class period",
        "Short, targeted assessments that drive real instructional decisions",
        "One quiz per topic = one clear picture of what each student has mastered",
        "The assessment tool that saves time and gives teachers actionable data",
        "Quick checks that catch gaps before they become problems",
        "Assessment doesn't have to be stressful — these fun, colorful quizzes prove it",
    ],
    "puzzles": [
        "Students beg to do these puzzles — and they're secretly mastering math the whole time",
        "Math that doesn't feel like math — puzzles, games, and brain teasers aligned to real standards",
        "The book students fight over at the math center",
        "Critical thinking, problem-solving, and curriculum-aligned fun — all in one resource",
        "For the student who says 'I hate math' — this book changes minds",
        "Engagement is the first step to mastery — and these puzzles deliver both",
        "When students ask 'Can we do the puzzle book today?' — you'll know it's working",
        "Curriculum-aligned puzzles that make {state_name} Grade 7 math genuinely fun",
    ],
    "worksheet": [
        "One worksheet per topic — print exactly what you need, when you need it",
        "The most flexible math resource in your toolkit: standalone worksheets for every Grade 7 skill",
        "Need a worksheet for tomorrow? Pick a topic, print, done",
        "Targeted, topic-specific worksheets that reinforce exactly what you taught today",
        "Standalone activities that work for homework, classwork, assessment, or sub plans",
        "Every topic, one clean worksheet — organized, professional, and ready to go",
        "Flexible, focused, and beautifully designed worksheets for every Grade 7 math standard",
        "Print-and-go worksheets for every {state_name} Grade 7 math topic — no prep required",
    ],
    "3_practice_tests": [
        "3 realistic practice tests that mirror exactly what students face on the {exam_acronym}",
        "Give students 3 full dress rehearsals before the real test — every question explained",
        "3 tests, 90 questions, every answer explained step by step",
        "Students who take 3 practice tests score higher. Give yours the advantage",
        "Not worksheets — 3 full-length, {exam_acronym}-format assessments with complete explanations",
        "Focused test prep that fits any schedule — 3 complete practice tests with full solutions",
        "The starter test prep package: 3 realistic tests covering every Grade 7 math standard",
        "3 practice tests built specifically for {state_name} — real format, real rigor, real results",
    ],
    "5_practice_tests": [
        "5 realistic practice tests that mirror exactly what students face on the {exam_acronym}",
        "Give students 5 full dress rehearsals before the real test — every question explained",
        "5 tests, 150 questions, every answer explained step by step",
        "The 5-test edition: enough practice to build real, lasting test-day confidence",
        "Not worksheets — 5 full-length, {exam_acronym}-format assessments with complete explanations",
        "The most popular test prep edition — 5 balanced practice tests for {state_name} students",
        "5 complete practice tests: the sweet spot between focused and comprehensive preparation",
        "5 unique tests covering every {state_name} Grade 7 math standard — no two tests alike",
    ],
    "7_practice_tests": [
        "7 realistic practice tests that mirror exactly what students face on the {exam_acronym}",
        "Give students 7 full dress rehearsals before the real test — every question explained",
        "7 tests, 210 questions, every answer explained step by step",
        "From test anxiety to test confidence — 7 practice tests make the real one feel familiar",
        "Not worksheets — 7 full-length, {exam_acronym}-format assessments with complete explanations",
        "Go deeper with 7 practice tests — thorough preparation for {state_name} Grade 7 students",
        "7 comprehensive practice tests: enough depth to see real, measurable growth",
        "Thorough test prep for {state_name} — 7 unique tests, 210 detailed answer explanations",
    ],
    "10_practice_tests": [
        "10 realistic practice tests that mirror exactly what students face on the {exam_acronym}",
        "Give students 10 full dress rehearsals before the real test — every question explained",
        "10 tests, 300 questions, every answer explained step by step",
        "Students who take 10 practice tests score higher. Give yours the advantage",
        "10 tests × 30 questions = 300 fully explained problems. Total preparation",
        "The ultimate test prep resource — 10 complete practice tests for {state_name} students",
        "Maximum practice, maximum confidence — 10 unique tests covering every standard",
        "Leave nothing to chance: 10 full-length {exam_acronym} practice tests with complete solutions",
    ],
}


def _pick_tpt_tagline(
    book_type: str,
    state_slug: str,
    format_vars: Dict[str, str] | None = None,
) -> str:
    """Pick a tagline from the TPT-specific pool, deterministic per product."""
    pool = TPT_TAGLINE_POOLS.get(book_type, ["Grade 7 math — aligned to {state_name} standards"])
    raw = f"{book_type}|{state_slug}|tpt|tagline"
    digest = hashlib.sha256(raw.encode()).hexdigest()
    idx = int(digest[:8], 16) % len(pool)
    phrase = pool[idx]
    if format_vars:
        try:
            phrase = phrase.format(**format_vars)
        except KeyError:
            pass
    return phrase


# ============================================================================
# DATA LOADERS
# ============================================================================

def load_state_exams(workspace: Path) -> Dict[str, dict]:
    """Load state exam data from state_exams.yaml."""
    path = workspace / "state_exams.yaml"
    if not path.exists():
        print(f"WARNING: state_exams.yaml not found at {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return raw.get("states", {})


def load_state_curriculums(workspace: Path) -> Dict[str, dict]:
    """Load state curriculum data from state_curriculums.yaml."""
    path = workspace / "state_curriculums.yaml"
    if not path.exists():
        print(f"WARNING: state_curriculums.yaml not found at {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return raw.get("states", {})


def load_titles(workspace: Path) -> Dict[Tuple[str, str], dict]:
    """Load titles.json and index by (state_slug, book_type).

    Returns a dict mapping (state_slug, book_type) → title entry.
    """
    path = workspace / "titles.json"
    if not path.exists():
        print(f"WARNING: titles.json not found at {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        entries = json.load(f)
    return {
        (e["state_slug"], e["book_type"]): e
        for e in entries
    }


# ============================================================================
# TOPIC HELPERS  (adapted from generate_listings.py)
# ============================================================================

def get_state_topics(state_slug: str, config: TopicsConfig) -> List[str]:
    """Get the full ordered list of topic IDs for a state (core + additional)."""
    topics = list(config.core_topic_ids)
    additional = config.state_additional.get(state_slug, [])

    if additional:
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
    """Build per-chapter (num, title, topic_count) summaries."""
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


def build_topic_highlights(
    state_slug: str, config: TopicsConfig, max_highlights: int = 12
) -> str:
    """Build a comma-separated string of representative topic names."""
    topic_ids = get_state_topics(state_slug, config)
    all_names = [
        config.topic_names[tid] for tid in topic_ids if tid in config.topic_names
    ]

    if len(all_names) <= max_highlights:
        return ", ".join(all_names)

    step = len(all_names) / max_highlights
    selected = [all_names[int(i * step)] for i in range(max_highlights)]
    return ", ".join(selected) + ", and more"


# ============================================================================
# TEMPLATE CONTEXT BUILDER
# ============================================================================

def _safe_format(text: str, fmt: Dict[str, str]) -> str:
    """Format a string with fmt dict, leaving unknown keys as-is."""
    try:
        return text.format(**fmt)
    except KeyError:
        for k, v in fmt.items():
            text = text.replace(f"{{{k}}}", v)
        return text


def build_template_context(
    book_type: str,
    state_slug: str,
    config: TopicsConfig,
    state_exams: Dict[str, dict],
    state_curriculums: Dict[str, dict],
    titles_index: Dict[Tuple[str, str], dict],
) -> Dict[str, Any]:
    """Build the complete Jinja2 template context for a single TPT listing."""

    state_name = config.state_display_names[state_slug]
    content = get_book_content(book_type)

    # Exam info
    exam_info = state_exams.get(state_slug, {})
    exam_name = exam_info.get("exam_name", "")
    exam_acronym = exam_info.get("exam_acronym", "")
    exam_months = exam_info.get("exam_months", "")

    # Curriculum info
    curr_info = state_curriculums.get(state_slug, {})
    curriculum_name = curr_info.get("curriculum_name", "")
    curriculum_acronym = curr_info.get("curriculum_acronym", "")

    # Title info from titles.json
    title_entry = titles_index.get((state_slug, book_type), {})
    tpt_title = title_entry.get("tpt_title", f"{state_name} Grade 7 Math {content['display_name']}")
    subtitle = title_entry.get("subtitle", content.get("subtitle", ""))
    page_count = title_entry.get("page_count", "")
    price = title_entry.get("price", BOOK_PRICES.get(book_type, ""))

    # Chapter & topic data
    chapter_summaries, num_topics = build_chapter_summaries(state_slug, config)
    num_chapters = len(chapter_summaries)
    topic_highlights = build_topic_highlights(state_slug, config)

    chapter_first = chapter_summaries[0][1] if chapter_summaries else ""
    chapter_last = chapter_summaries[-1][1] if chapter_summaries else ""

    # Practice test extras from content
    num_tests = content.get("num_tests", 0)
    questions_per_test = content.get("questions_per_test", 0)
    total_questions = content.get("total_questions", 0)

    # Format variables for variation pools
    fmt: Dict[str, str] = {
        "state_name": state_name,
        "exam_name": exam_name,
        "exam_acronym": exam_acronym or "state test",
        "num_topics": str(num_topics),
        "num_chapters": str(num_chapters),
        "page_count": "",  # intentionally blank for TPT listings
        "exam_months": "",  # intentionally blank for TPT listings
        "chapter_first": chapter_first,
        "chapter_last": chapter_last,
        "num_tests": str(num_tests),
        "questions_per_test": str(questions_per_test),
        "total_questions": str(total_questions),
    }

    # Pick all variation phrases (pre-formatted)
    variations: Dict[str, str] = {}
    for pool_key in VARIATION_POOLS:
        variations[pool_key] = pick_variation(
            pool_key, book_type, state_slug, WEBSITE, format_vars=fmt
        )

    # Pick tagline (TPT-specific pool — no page counts or exam months)
    tagline = _pick_tpt_tagline(book_type, state_slug, format_vars=fmt)

    # Format features and use_cases with state/exam data
    features = [_safe_format(f, fmt) for f in content.get("features", [])]
    use_cases = [_safe_format(uc, fmt) for uc in content.get("use_cases", [])]

    ctx: Dict[str, Any] = {
        # Identity
        "book_type": book_type,
        "state_slug": state_slug,
        "state_name": state_name,
        "topic": "Grade 7 Math",

        # Titles
        "tpt_title": tpt_title,
        "subtitle": subtitle,
        "display_name": content["display_name"],
        "page_count": page_count,
        "price": price,

        # Tagline
        "tagline": tagline,

        # Exam info
        "exam_name": exam_name,
        "exam_acronym": exam_acronym,

        # Curriculum info
        "curriculum_name": curriculum_name,
        "curriculum_acronym": curriculum_acronym,

        # Topic data
        "chapter_summaries": chapter_summaries,
        "num_topics": num_topics,
        "num_chapters": num_chapters,
        "topic_highlights": topic_highlights,

        # Book content
        "features": features,
        "use_cases": use_cases,

        # Practice test extras
        "num_tests": num_tests,
        "questions_per_test": questions_per_test,
        "total_questions": total_questions,

        # All variation pool phrases (pre-formatted)
        **variations,
    }

    return ctx


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TPT listing descriptions for Grade 7 math books."
    )
    parser.add_argument(
        "--states", type=str, default=None,
        help="Comma-separated state slugs (default: all 50)",
    )
    parser.add_argument(
        "--book-types", type=str, default=None,
        help=f"Comma-separated book types (default: all supported). "
             f"Currently supported: {', '.join(SUPPORTED_BOOK_TYPES)}",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be generated without writing files",
    )
    parser.add_argument(
        "--preview", action="store_true",
        help="Print generated HTML to stdout (useful with --states and --book-types)",
    )
    parser.add_argument(
        "--book-folder", action="store_true",
        help=(
            "Write files directly into final_output/<book_type>/ "
            "instead of the default final_output/listings/tpt/<book_type>/."
        ),
    )
    args = parser.parse_args()

    # ── Setup ───────────────────────────────────────────────────────────
    workspace = find_workspace()
    config = load_config(workspace)
    state_exams = load_state_exams(workspace)
    state_curriculums = load_state_curriculums(workspace)
    titles_index = load_titles(workspace)

    template_dir = workspace / TEMPLATE_DIR
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # ── Parse filters ───────────────────────────────────────────────────
    if args.states:
        state_slugs = [s.strip() for s in args.states.split(",")]
        for s in state_slugs:
            if s not in config.all_state_slugs:
                print(f"ERROR: Unknown state '{s}'. Available: {', '.join(config.all_state_slugs[:5])}...")
                sys.exit(1)
    else:
        states_input = prompt_states(config.all_state_slugs)
        if states_input is None:
            state_slugs = config.all_state_slugs
        else:
            state_slugs = [s.strip() for s in states_input.split(",")]

    if args.book_types:
        book_types = [b.strip() for b in args.book_types.split(",")]
        for b in book_types:
            if b not in SUPPORTED_BOOK_TYPES:
                print(f"ERROR: Unknown or unsupported book type '{b}'. "
                      f"Supported: {', '.join(SUPPORTED_BOOK_TYPES)}")
                sys.exit(1)
    else:
        descs = {k: BOOK_TYPES.get(k, {}).get("description", "") for k in SUPPORTED_BOOK_TYPES}
        selected = prompt_book_type(
            SUPPORTED_BOOK_TYPES,
            descriptions=descs,
            allow_all=True,
            allow_all_previews=False,
        )
        if selected == "all":
            book_types = SUPPORTED_BOOK_TYPES
        else:
            book_types = [selected]

    # ── Banner ──────────────────────────────────────────────────────────
    total = len(state_slugs) * len(book_types)
    book_folder: bool = args.book_folder
    output_label = (
        "final_output/<book_type>/" if book_folder
        else "final_output/listings/tpt/<book_type>/"
    )
    print("=" * 70)
    print("TPT Listing Description Generator — Grade 7 Math")
    print("=" * 70)
    print(f"  States:     {len(state_slugs)}")
    print(f"  Book Types: {len(book_types)} ({', '.join(book_types)})")
    print(f"  Total:      {total} listings")
    print(f"  Output:     {output_label}")
    if args.dry_run:
        print("  Mode:       DRY RUN (no files written)")
    if args.preview:
        print("  Mode:       PREVIEW (output to stdout)")
    print()

    # ── Pre-load templates ──────────────────────────────────────────────
    templates: Dict[str, Any] = {}
    for bt in book_types:
        tpl_path = f"tpt/{bt}.html.jinja"
        try:
            templates[bt] = env.get_template(tpl_path)
        except Exception as e:
            print(f"ERROR: Could not load template '{tpl_path}': {e}")
            sys.exit(1)

    # ── Generate ────────────────────────────────────────────────────────
    generated = 0
    output_base = workspace / "final_output" if book_folder else workspace / OUTPUT_DIR

    for state_slug in state_slugs:
        state_name = config.state_display_names[state_slug]

        for book_type in book_types:
            ctx = build_template_context(
                book_type, state_slug, config,
                state_exams, state_curriculums, titles_index,
            )

            # Page count — prefer title_entry value, fall back to live PDF
            if not ctx["page_count"]:
                pdf = find_latest_pdf(workspace, book_type, state_slug)
                if pdf:
                    ctx["page_count"] = get_pdf_page_count(pdf)

            template = templates[book_type]
            page_count_str = f"Pages: {ctx['page_count']}" if ctx['page_count'] else "Pages: "
            price_str = f"Price: ${ctx['price']}" if ctx['price'] else "Price: "
            meta_comment = f"<!-- {page_count_str} | {price_str} -->"
            html = f"<!-- {ctx['tpt_title']} -->\n{meta_comment}\n" + template.render(**ctx)

            if args.preview:
                print(f"\n{'─' * 70}")
                print(f"  {state_name} — {book_type}")
                print(f"{'─' * 70}\n")
                print(html)
                print()

            if not args.dry_run:
                today = date.today().isoformat()
                out_dir = output_base / book_type
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / f"{state_slug}_tpt_{today}.html"
                out_file.write_text(html, encoding="utf-8")

            generated += 1

        if not args.dry_run and not args.preview:
            print(f"  {state_name}: {len(book_types)} listing(s)")

    # ── Summary ─────────────────────────────────────────────────────────
    print()
    print("=" * 70)
    action = "Would generate" if args.dry_run else "Generated"
    print(f"{action} {generated} TPT listing descriptions")
    if not args.dry_run:
        print(f"Output directory: {output_base}")
    print("=" * 70)


if __name__ == "__main__":
    main()
