#!/usr/bin/env python3
"""
Generate 50 unique TPT HTML descriptions for the practice_tests_bundle.
One per state. Every description has a different structure, headings, and phrasing.

Usage:
    python3 scripts/generate_practice_tests_bundle_descriptions.py
    python3 scripts/generate_practice_tests_bundle_descriptions.py --state texas
    python3 scripts/generate_practice_tests_bundle_descriptions.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Resolve workspace ──────────────────────────────────────────────────

WORKSPACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / ".agents/skills/writing-tpt-bundles-descriptions/scripts"))

import yaml
from config_loader import load_config, TopicsConfig
from config import GRADE_DISPLAY

# ── Data loaders (same as get_bundle_facts.py) ─────────────────────────

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

def load_titles() -> list:
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

# ── Bundle TPT title builder ──────────────────────────────────────────

TPT_TITLE_MAX_LENGTH = 80

def bundle_tpt_title(state_slug: str, exam_acronym: str, grade_short: str) -> str:
    titles_pool = [f"{exam_acronym} {grade_short} Math Practice Tests Bundle"]
    subtitles_pool = [
        "25 Unique Full-Length Tests",
        "25 Full-Length Tests",
        "25 Unique Tests",
        "25 Tests",
    ]
    for t in titles_pool:
        for s in subtitles_pool:
            candidate = f"{t}: {s}"
            if len(candidate) <= TPT_TITLE_MAX_LENGTH:
                return candidate
    return titles_pool[0]

# ── State data collector ──────────────────────────────────────────────

def get_state_data(state_slug: str) -> Dict[str, Any]:
    exams = load_state_exams()
    currs = load_state_curriculums()
    config: TopicsConfig = load_config(WORKSPACE)

    exam_info = exams.get(state_slug, {})
    curr_info = currs.get(state_slug, {})

    state_name = curr_info.get("name", state_slug.replace("-", " ").title())
    curr_name = curr_info.get("curriculum_name", "")
    curr_acronym = curr_info.get("curriculum_acronym", "")
    exam_name = exam_info.get("exam_name", "")
    exam_acronym = exam_info.get("exam_acronym", "")

    grade = GRADE_DISPLAY  # e.g. "Grade 7"

    # Book titles
    book_types = ["3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"]
    book_titles = {}
    for bt in book_types:
        entry = find_title_entry(bt, state_slug)
        if entry:
            book_titles[bt] = entry.get("full_title", "")
        else:
            book_titles[bt] = ""

    # GRADE_DISPLAY is "Grade 7 Math" — use it for titles but not in prose (to avoid "Grade 7 Math math")
    grade_short = grade.replace(" Math", "")  # "Grade 7"
    bundle_title_raw = f"{state_name} {exam_acronym} {grade} Practice Tests Bundle: 25 Unique Full-Length Tests"
    tpt_title = bundle_tpt_title(state_slug, exam_acronym, grade_short)

    return {
        "state_slug": state_slug,
        "state_name": state_name,
        "curriculum_name": curr_name,
        "curriculum_acronym": curr_acronym,
        "exam_name": exam_name,
        "exam_acronym": exam_acronym,
        "grade": grade_short,
        "bundle_title": bundle_title_raw,
        "tpt_title": tpt_title,
        "book_titles": book_titles,
    }


# ============================================================================
# VARIATION POOLS
# ============================================================================

# --- Section orderings (everything between opening and CTA+footer) ---
# Sections: included, curriculum, usecases, quality, crosssell
SECTION_ORDERS = [
    ["included", "curriculum", "usecases", "quality", "crosssell"],
    ["curriculum", "included", "usecases", "quality", "crosssell"],
    ["included", "usecases", "curriculum", "quality", "crosssell"],
    ["included", "curriculum", "quality", "usecases", "crosssell"],
    ["curriculum", "included", "quality", "usecases", "crosssell"],
    ["included", "usecases", "quality", "curriculum", "crosssell"],
    ["usecases", "included", "curriculum", "quality", "crosssell"],
    ["curriculum", "usecases", "included", "quality", "crosssell"],
    ["included", "quality", "curriculum", "usecases", "crosssell"],
    ["included", "quality", "usecases", "curriculum", "crosssell"],
]

# --- Heading pools ---
HEADINGS_INCLUDED = [
    "What's in the Bundle",
    "Here's What You Get",
    "Books Included",
    "Everything in This Bundle",
    "The Four Books",
    "What's Inside",
    "Bundle Contents",
    "Your Four Test Books",
    "The Bundle Includes",
    "What You're Getting",
    "Inside the Bundle",
    "Four Books, 25 Tests",
    "What This Bundle Includes",
    "The Full Set",
    "All Four Practice Test Books",
    "Here's What's Included",
    "Included in This Bundle",
    "The Lineup",
    "What You Get",
    "The Practice Test Collection",
    "Your Test Prep Toolkit",
    "What's in the Box",
    "Test Prep Books Included",
    "Here's the Full Bundle",
    "The Complete Test Prep Set",
    "What Comes With This Bundle",
    "Bundle Breakdown",
    "Inside This Bundle",
    "The Complete Package",
    "Four Books, Zero Repeated Questions",
    "All 25 Tests, All Yours",
    "Here's Your Bundle",
    "Your Practice Tests",
    "What's Waiting Inside",
    "Everything You Get",
    "Break It Down",
    "Books Inside",
    "Here's the Rundown",
    "What's Packed In",
    "The Test Prep Lineup",
    "Your 750-Question Bundle",
    "What This Includes",
    "The Full Test Prep Set",
    "Included Books",
    "Test Books in This Bundle",
    "Here's Every Book",
    "Everything Included",
    "Inside: Four Books, 25 Tests",
    "The Pack",
    "Tests Included",
]

HEADINGS_CURRICULUM = [
    "Built for {state}",
    "Aligned to {acronym}",
    "Written for {state}",
    "Matches {state} Standards",
    "{state}-Specific Content",
    "Aligned with {state} Standards",
    "Standards Match: {acronym}",
    "{state} Math Standards",
    "Made for {state} Students",
    "Designed for {state}",
    "Covers the {acronym}",
    "{state} Curriculum Alignment",
    "Follows the {acronym}",
    "Built Around {state} Standards",
    "{state}-Aligned",
    "Matches {state}'s {acronym}",
    "Written Around {acronym}",
    "Every Test Matches {state} Standards",
    "Standards-Aligned for {state}",
    "Tuned to {state}'s Curriculum",
    "Created for {state} Classrooms",
    "Tracks the {acronym}",
    "{state} Standards? Covered.",
    "Fits {state}'s {acronym}",
    "Built on {state}'s {acronym}",
    "Mapped to {acronym}",
    "For {state} Math Classrooms",
    "{state}-Ready",
    "Follows {state}'s Standards",
    "Curriculum Fit: {state}",
    "Matches What {state} Tests",
    "Reflects {state}'s {acronym}",
    "Rooted in {state} Standards",
    "Aligned to What {state} Expects",
    "Covers {state}'s Full Curriculum",
    "{acronym}-Aligned Content",
    "Written to Match {state}",
    "{state} Standards Built In",
    "Matches the {acronym} Framework",
    "Built for {state} Math",
    "Test Content Matches {state}",
    "Follows What {state} Teaches",
    "Mirrors {state}'s {acronym}",
    "Designed Around {acronym}",
    "Fully Aligned to {state}",
    "Content Tracks {acronym}",
    "{state} Standards, Front to Back",
    "Grounded in {state}'s Curriculum",
    "Every Question Follows {acronym}",
    "Made for {state}'s {acronym}",
]

HEADINGS_USECASES = [
    "Works For",
    "Who Uses This Bundle",
    "Great For",
    "How to Use It",
    "Who'll Get the Most Out of This",
    "Perfect For",
    "Ideal For",
    "Who Benefits",
    "How Teachers Use This",
    "Use It For",
    "Made For",
    "Who's This For?",
    "Best Uses",
    "Put It to Work",
    "How It Gets Used",
    "Ways to Use This Bundle",
    "Who This Is For",
    "Great Ways to Use It",
    "Useful For",
    "How You'll Use It",
    "Here's Who It's For",
    "Intended For",
    "Top Uses",
    "This Works Great For",
    "Designed For",
    "Here's How People Use It",
    "Built For These Situations",
    "Who Needs This",
    "When to Reach for This Bundle",
    "How It Helps",
    "Classroom-Tested Uses",
    "The Right Fit For",
    "This Bundle Fits",
    "Use Cases",
    "Where This Bundle Shines",
    "Get the Most From It",
    "Who Should Grab This",
    "Grab This If You're…",
    "Here's When You'll Want This",
    "How It Works in the Classroom",
    "What People Use It For",
    "Try It For",
    "Here's Where It Helps",
    "The Rundown: Who It's For",
    "This Bundle Helps With",
    "Real-World Uses",
    "It's Great For",
    "Give It To",
    "Reach for This When…",
    "This One's For",
]

HEADINGS_QUALITY = [
    "Every Book Includes",
    "What You Can Expect",
    "In Every Book",
    "Design & Quality",
    "In All Four Books",
    "What to Expect",
    "Quality Details",
    "Look & Feel",
    "About These Books",
    "The Details",
    "Standard in Every Book",
    "Production Quality",
    "What's in Every Book",
    "You'll Also Get",
    "Quick Notes on Quality",
    "Good to Know",
    "Features Across All Books",
    "A Few More Details",
    "About the Books",
    "Across All Four Books",
    "Built-In Features",
    "Here's What Comes Standard",
    "Worth Mentioning",
    "Bonus Details",
    "Each Book Features",
    "Noted in Every Book",
    "Format & Design",
    "Things Worth Noting",
    "What Sets These Apart",
    "The Fine Print (the Good Kind)",
    "A Quick Note on Every Book",
    "In Every Single Book",
    "Always Included",
    "You Can Count On",
    "Shared Features",
    "Quality Across the Board",
    "These Books All Feature",
    "Built-In Extras",
    "Inside Every Book",
    "Don't Overlook",
    "Here's What's Standard",
    "Included Everywhere",
    "Design Features",
    "All Books Share",
    "You Should Know",
    "This Applies to All Four",
    "A Note on Quality",
    "Format Details",
    "In Each Book",
    "Common to All Four",
]

HEADINGS_CROSSSELL = [
    "Also in the Series",
    "Want More?",
    "Need Lessons Too?",
    "Looking for More?",
    "More from the Series",
    "Add to Your Collection",
    "Pair It With",
    "More Grade 7 Math Resources",
    "Explore the Series",
    "Beyond Practice Tests",
    "Other Books Available",
    "Need Teaching Materials Too?",
    "Complete Your Set",
    "Don't Stop at Tests",
    "Go Further",
    "Expand Your Toolkit",
    "Also Available",
    "Round Out Your Resources",
    "More in the Series",
    "Still Need More?",
    "Take It Further",
    "Level Up",
    "For Even More Support",
    "Teaching Tools That Go With This",
    "What Pairs Well With This",
    "Fill in the Gaps",
    "Get Even More",
    "Ready for More?",
    "More Resources to Check Out",
    "What Else Is Out There",
    "Complement This Bundle With",
    "Worth Adding",
    "Other Resources Available",
    "Build On This Bundle",
    "What About Instruction?",
    "Supplement With",
    "The Rest of the Series",
    "Grab These Too",
    "More from View Math",
    "Keep Going",
    "Check Out the Rest",
    "Still Looking?",
    "Also Worth a Look",
    "Goes Great With",
    "You Might Also Like",
    "Pair These Tests With",
    "Extend the Learning",
    "Full Series Options",
    "What Comes Next?",
    "If You Need Instruction",
]

# --- Opening paragraph templates ---
# {state}, {exam}, {exam_acronym}, {grade}
OPENINGS = [
    "This bundle packs all four {grade} math practice test editions into one download — 25 unique, non-overlapping tests with 750 questions total. Every test is different. No repeated questions across any of the four books. It's built specifically for {state}'s <b>{exam_acronym}</b>.",
    "Four books. 25 full-length practice tests. 750 questions. Not a single repeated question across any of the editions. This bundle gives your {grade} students everything they need to prepare for the <b>{exam_acronym}</b> in {state}.",
    "Here's what you get: 25 completely unique {grade} math practice tests — that's 750 questions, and none of them repeat across the four books. Designed for {state} students preparing for the <b>{exam_acronym}</b>.",
    "Twenty-five unique practice tests for {state}'s <b>{exam_acronym}</b>, all in one bundle. That's 750 questions across four books — no overlapping content, no repeated problems. Just fresh test prep material from start to finish.",
    "If you're looking for serious {grade} math test prep in {state}, this is it. Four practice test books, 25 unique full-length tests, 750 questions — every single one different. Built for the <b>{exam_acronym}</b>.",
    "This is the complete practice test package for {state} {grade} math. You're getting 25 unique full-length tests across four books — 750 questions total with zero overlap. Aligned to the <b>{exam_acronym}</b>.",
    "One bundle. Four books. Twenty-five full-length {grade} math tests — every test unique, every question different. That's 750 questions total for {state}'s <b>{exam_acronym}</b> prep with no repeated content.",
    "Need a lot of test practice for {state}'s <b>{exam_acronym}</b>? This bundle has 25 unique {grade} math practice tests across four books. 750 questions, all different — zero repeats between editions.",
    "This is 25 unique tests in one bundle. Four books of {grade} math practice, 750 total questions, zero repeated content. Made for {state} and aligned to the <b>{exam_acronym}</b>.",
    "The {state} <b>{exam_acronym}</b> Practice Tests Bundle puts 25 unique full-length {grade} math tests in your hands. 750 questions across four books, not a single one repeated. That's enough test prep to last the entire school year.",
    "Everything you need for {state} <b>{exam_acronym}</b> test prep in {grade} math — 25 full-length practice tests, 750 questions, four books. Every test is unique. No questions repeat across editions.",
    "Get 25 completely different practice tests for {state}'s <b>{exam_acronym}</b> — all in one {grade} math bundle. Four books, 750 questions, zero overlap. Enough material to run weekly test prep all year long.",
    "This bundle covers {grade} math test prep for {state} with 25 unique full-length practice tests. That's 750 questions across four separate books — no duplicates, no repeated problems anywhere.",
    "Four practice test books. Twenty-five tests. Seven hundred fifty questions. Every single one unique. This {grade} math bundle is built for {state}'s <b>{exam_acronym}</b> — and it doesn't recycle a single question.",
    "You won't find a bigger practice test set for {state}'s <b>{exam_acronym}</b>. This {grade} math bundle has 25 unique full-length tests across four books — that's 750 fresh questions with no repeats.",
    "Twenty-five tests. 750 questions. Four books. Nothing repeats. This {grade} math practice test bundle is made for {state} students taking the <b>{exam_acronym}</b>.",
    "Looking for {grade} math practice for the <b>{exam_acronym}</b>? This {state} bundle has 25 unique full-length tests spread across four books — 750 total questions with absolutely no overlap.",
    "This {state} bundle includes every practice test edition — 3, 5, 7, and 10 — for a total of 25 unique {grade} math tests. That's 750 questions with no repeats. Designed for the <b>{exam_acronym}</b>.",
    "Here's 25 brand-new practice tests for {state}'s <b>{exam_acronym}</b> — all unique, all different, all in one {grade} math bundle. Four books, 750 questions, and not a single repeat.",
    "Your students get 25 unique full-length practice tests for {state}'s <b>{exam_acronym}</b>. That's 750 {grade} math questions across four books — every question different from every other.",
    "Four {grade} math practice test books for {state}, bundled together. That gives you 25 unique tests and 750 questions — no overlap between any of the editions. Aligned to the <b>{exam_acronym}</b>.",
    "This bundle is pure test prep. 25 unique {grade} math practice tests for {state}'s <b>{exam_acronym}</b>, split across four books. 750 questions total. Not one repeat.",
    "If your {grade} students in {state} are getting ready for the <b>{exam_acronym}</b>, this bundle has them covered. Four books, 25 unique tests, 750 questions — zero overlap.",
    "One download, four books, 25 full-length tests, 750 questions — all unique. This {grade} math practice test bundle is designed for {state}'s <b>{exam_acronym}</b>.",
    "This is 25 different practice tests for {state}'s <b>{exam_acronym}</b>. Each one is unique. Four books, 750 questions, no shared content across any edition. {grade} math, start to finish.",
    "All four {grade} math practice test editions for {state}, together in one bundle. You get 25 unique tests with 750 questions — every last one different. Aligned to the <b>{exam_acronym}</b>.",
    "Prep for {state}'s <b>{exam_acronym}</b> with 25 full-length {grade} math tests — four books, 750 questions, and absolutely zero repeated content between any edition.",
    "25 full-length, non-overlapping {grade} math practice tests for {state}'s <b>{exam_acronym}</b>. 750 questions across four books. No repeats. Enough test prep to fill a school year.",
    "What's in here? Four books of {grade} math practice tests for {state}, totaling 25 unique tests and 750 questions. Nothing repeats. Everything's aligned to the <b>{exam_acronym}</b>.",
    "This bundle gives {state} {grade} math students 25 unique practice tests to prepare for the <b>{exam_acronym}</b>. Four books, 750 questions, no overlap — every edition is completely different.",
    "For {state}'s <b>{exam_acronym}</b>: four {grade} math practice test books bundled together. 25 unique tests. 750 questions. Not a single repeat across any edition.",
    "All the practice tests your {state} {grade} math students will need for the <b>{exam_acronym}</b> — 25 unique tests, 750 questions, four books, zero repeats.",
    "This {grade} math bundle brings together 25 unique practice tests for the <b>{exam_acronym}</b> in {state}. Four books, 750 questions, all completely different. Nothing overlaps.",
    "25 unique practice tests designed for {state}'s {grade} math <b>{exam_acronym}</b>. Each edition contains different tests — 750 questions total with no overlap across the four books.",
    "Practice tests, and lots of them. This {state} {grade} math bundle delivers 25 unique full-length tests across four books — 750 questions with zero repeats, built for the <b>{exam_acronym}</b>.",
    "Serious test prep for {state}'s <b>{exam_acronym}</b>. This {grade} math bundle includes 25 unique practice tests — that's 750 questions split across four books with no repeated content.",
    "Here's your {state} <b>{exam_acronym}</b> test prep: 25 unique {grade} math practice tests, 750 total questions, four books. Every edition contains completely different tests.",
    "{State} {grade} math students can practice for the <b>{exam_acronym}</b> with 25 unique tests — four books, 750 questions, nothing repeated. This bundle has it all.",
    "Four books. 25 unique {grade} math tests. 750 questions. Zero repeats. That's what this {state} <b>{exam_acronym}</b> practice test bundle delivers.",
    "This is the practice test bundle for {state}'s {grade} math <b>{exam_acronym}</b>. Four books with 25 completely different tests — 750 questions and no content overlap.",
    "For {state} {grade} math: a bundle of 25 unique practice tests across four books. 750 questions total, none repeated. All aligned to the <b>{exam_acronym}</b>.",
    "Everything in this bundle is about test practice for {state}'s <b>{exam_acronym}</b>. 25 unique {grade} math tests, 750 questions, four books — with zero overlap between editions.",
    "This {state} bundle packs 25 unique full-length tests for {grade} math — 750 questions across four books. Not one question repeats. Designed for the <b>{exam_acronym}</b>.",
    "Test prep for {state}'s <b>{exam_acronym}</b> starts here. 25 unique {grade} math practice tests across four books. 750 questions, and none of them overlap.",
    "One bundle, 25 tests, 750 questions — all unique. This is {grade} math test prep made for {state}'s <b>{exam_acronym}</b>. Four books, no repeated content.",
    "25 unique practice tests covering {state}'s <b>{exam_acronym}</b> {grade} math standards. Four books, 750 total questions, and every single test is different from the rest.",
    "Need {grade} math test prep for {state}? This bundle gives you 25 unique <b>{exam_acronym}</b> practice tests. That's 750 questions in four books — every one completely different.",
    "This bundle has 25 full-length {grade} math practice tests for {state}'s <b>{exam_acronym}</b>. Four books. 750 questions. No overlapping content whatsoever.",
    "Ready for the <b>{exam_acronym}</b>? This {state} {grade} math bundle has 25 unique tests across four books. 750 questions, and not a single one is repeated.",
    "Your {state} <b>{exam_acronym}</b> prep, sorted. 25 unique full-length {grade} math practice tests across four separate books. 750 questions. Zero repeats.",
]

# --- "Included" book list intro sentences ---
INCLUDED_INTROS = [
    "You get all four practice test editions:",
    "This bundle includes:",
    "Here's what's inside:",
    "The bundle contains:",
    "Four books, each with unique tests:",
    "All four editions are included:",
    "Every practice test edition in the series:",
    "Included in this bundle:",
    "You're getting these four books:",
    "The four books in this bundle:",
    "Here's the full set:",
    "Your bundle includes:",
    "Inside you'll find:",
    "It comes with:",
    "Each edition has its own unique tests:",
    "",  # No intro, just the list
    "",
    "",
    "",
    "",
    "What's in the bundle:",
    "All four books:",
    "The test books:",
    "Four books with 25 unique tests:",
    "Everything in one bundle:",
    "Every edition, zero overlap:",
    "Here's exactly what you'll get:",
    "The full practice test lineup:",
    "What comes in this bundle:",
    "This includes all four books:",
    "Packed inside:",
    "Four separate books:",
    "Each one has different tests:",
    "No repeated content across any of them:",
    "The complete test prep set:",
    "You'll receive:",
    "These four books make up the bundle:",
    "Here are your four books:",
    "All four editions, all in one download:",
    "Your test prep library:",
    "From start to finish:",
    "Every book is unique:",
    "The bundle's four books:",
    "Full list of included books:",
    "Every edition is accounted for:",
    "What you're downloading:",
    "This is what's in the box:",
    "Four practice test books, each unique:",
    "One bundle, four books:",
    "Here's the package:",
]

# --- Post-list reinforcement sentences ---
POST_LIST_REINFORCEMENTS = [
    "Every edition contains completely different tests — no repeated questions across any of the four books.",
    "None of these tests overlap. Each book has its own unique set of questions.",
    "There's zero overlap between any of the editions. Every question in every book is different.",
    "All 25 tests are unique. None of the 750 questions appear in more than one book.",
    "No duplicates. No recycled questions. Each edition stands on its own.",
    "These aren't the same tests repackaged — every single question across all four books is different.",
    "You can use all four books knowing there's no overlap. Every test is fresh material.",
    "Each book was written independently. No shared questions, no shared tests.",
    "Every book has its own unique content. None of the questions repeat across editions.",
    "Total count: 25 unique tests, 750 unique questions, zero overlap.",
    "That's 25 tests and 750 questions — not one of them appears in more than one edition.",
    "No question shows up twice. Every edition is completely independent.",
    "All four books are different. You'll never give the same test twice.",
    "The four editions don't share a single question — every test is unique.",
    "Zero repeated problems. Each edition was written from scratch.",
    "Nothing is duplicated. The 750 questions across these four books are all distinct.",
    "You can assign all 25 tests and your students will never see the same question twice.",
    "Each of the 25 tests is unique — from the first question to the last.",
    "The four books together give you 750 fresh, non-overlapping questions.",
    "All tests are unique. All questions are unique. Nothing recycles.",
    "The 25 tests don't share any content. Each book is its own complete set.",
    "There's no reused content. Every single question is original to its book.",
    "These 750 questions are all different — every edition contains brand-new tests.",
    "No overlap. 25 tests, 750 questions, all completely unique.",
    "Not a single question repeats between any of the four editions.",
    "The bottom line: 25 unique tests, 750 unique questions, four separate books.",
    "Every test in every book is a completely new assessment.",
    "No repackaging. Each book was built from the ground up with unique content.",
    "Use them all — the tests never repeat across editions.",
    "You won't find any duplicate questions, no matter how many books you assign.",
    "That means 25 fresh tests for your classroom. No overlap anywhere.",
    "Four books, zero shared content. Every test is its own thing.",
    "The 750 questions span all four books without a single repeat.",
    "You could assign a different test every week and never reuse a question.",
    "Each edition was designed to be completely independent — no overlap whatsoever.",
    "It bears repeating: none of the 750 questions appear in more than one book.",
    "Your students get 25 unique test experiences across these four books.",
    "Nothing repeats. All 25 tests and 750 questions are one-of-a-kind.",
    "That's 25 full-length assessments, each with 30 completely unique questions.",
    "All tests are non-overlapping. You can use every single one.",
    "The editions don't borrow from each other — every question is fresh.",
    "No shared material between books. Every test stands alone.",
    "With 750 unique questions, you won't run out of fresh practice material.",
    "Each of the four books brings entirely new tests to the table.",
    "It's all unique. 25 tests. 750 questions. Four books. Zero repeats.",
    "Every last question is unique — across all four practice test editions.",
    "The four editions combined deliver 25 non-repeating tests.",
    "All 25 tests are completely original — no shared content between books.",
    "You'll never accidentally assign the same questions twice.",
    "These are 25 genuinely different tests — overlap between editions is zero.",
]

# --- Book one-liner variations (per book type) ---
BOOK_ONELINERS = {
    "3_practice_tests": [
        "Three unique full-length tests with detailed answer explanations",
        "Three complete practice tests, each with step-by-step answer explanations",
        "3 full-length tests — every answer explained in detail",
        "Three unique tests with comprehensive answer keys",
        "A set of three practice tests with detailed answer breakdowns",
        "Three full-length exams with explained answers",
    ],
    "5_practice_tests": [
        "Five more unique tests for extra practice",
        "Five additional full-length tests — all completely different",
        "5 full-length tests with detailed answer explanations",
        "Five unique practice tests for deeper preparation",
        "Five more complete tests to build confidence",
        "Another five unique tests with explained answers",
    ],
    "7_practice_tests": [
        "Seven unique tests with detailed answers",
        "Seven full-length practice tests with step-by-step solutions",
        "7 unique tests — every answer thoroughly explained",
        "Seven complete tests with comprehensive answer keys",
        "Seven more full-length assessments with answer explanations",
        "A set of seven unique tests with detailed explanations",
    ],
    "10_practice_tests": [
        "Ten unique tests with answer explanations",
        "Ten full-length tests — the largest edition in the series",
        "10 unique tests with step-by-step answers",
        "Ten complete practice tests with detailed explanations",
        "The biggest edition: ten unique tests with full answer keys",
        "Ten more tests to round out your practice set",
    ],
}

# --- Curriculum section templates ---
CURRICULUM_TEMPLATES = [
    "Every test in this bundle aligns with the <b>{curr_name}</b> (<b>{curr_acronym}</b>). Questions match the types, difficulty, and topic coverage your students will see on the <b>{exam_name}</b> (<b>{exam_acronym}</b>). This isn't a generic resource — it's written specifically for {state}.",
    "These tests follow the <b>{curr_name}</b> (<b>{curr_acronym}</b>). The format, question types, and content match what {state} students will face on the <b>{exam_name}</b> (<b>{exam_acronym}</b>). It's {state}-specific, not a national product relabeled.",
    "All 25 tests are aligned to the <b>{curr_acronym}</b> — {state}'s <b>{curr_name}</b>. That means the questions cover exactly what the <b>{exam_acronym}</b> (<b>{exam_name}</b>) tests. The content was written for {state}.",
    "This bundle follows the <b>{curr_name}</b> (<b>{curr_acronym}</b>) and matches the format of the <b>{exam_acronym}</b>. It's not a one-size-fits-all product — the content was written for {state} students taking the <b>{exam_name}</b>.",
    "The questions are built around {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>). Each test mirrors the <b>{exam_acronym}</b> in format and difficulty. {state}-specific from the first question to the last.",
    "Content follows the <b>{curr_acronym}</b> — the <b>{curr_name}</b>. Tests are formatted like the real <b>{exam_name}</b> (<b>{exam_acronym}</b>). Written for {state}, not adapted from a generic template.",
    "All test content aligns with what {state} teaches under the <b>{curr_name}</b> (<b>{curr_acronym}</b>). The <b>{exam_acronym}</b> format is matched: question types, coverage, difficulty. Built for {state} classrooms.",
    "These tests were written around the <b>{curr_acronym}</b> — {state}'s <b>{curr_name}</b>. The content, format, and difficulty level are designed to prepare students for the <b>{exam_name}</b> (<b>{exam_acronym}</b>).",
    "Aligned to the <b>{curr_name}</b> (<b>{curr_acronym}</b>), every test in this bundle prepares {state} students for the <b>{exam_acronym}</b>. Question formats mirror the real <b>{exam_name}</b>.",
    "{state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>) drives every test in this bundle. The content matches what students will see on the <b>{exam_name}</b> (<b>{exam_acronym}</b>) — not a generic version.",
    "This isn't generic math — it's built on {state}'s <b>{curr_acronym}</b> (<b>{curr_name}</b>). Test content and question formats match the <b>{exam_name}</b> (<b>{exam_acronym}</b>) your students will actually take.",
    "Every question follows the <b>{curr_name}</b> (<b>{curr_acronym}</b>). The <b>{exam_acronym}</b> format is replicated: same question styles, same coverage areas. Written from the ground up for {state}.",
    "The content is tied to {state}'s <b>{curr_acronym}</b>. Tests mirror the <b>{exam_name}</b> (<b>{exam_acronym}</b>) in structure and difficulty. This is {state}-specific test prep, not a relabeled national workbook.",
    "These aren't generic practice tests. They follow {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>) and match the <b>{exam_acronym}</b> format. {state} students, {state} standards, {state} exam.",
    "Built on the <b>{curr_name}</b> (<b>{curr_acronym}</b>). Tests follow the <b>{exam_acronym}</b> format — the <b>{exam_name}</b> your students actually take. Written specifically for {state}.",
    "Every test aligns with {state}'s <b>{curr_acronym}</b>. The <b>{exam_name}</b> (<b>{exam_acronym}</b>) format is matched throughout. This was made for {state} — that's it.",
    "Questions track the <b>{curr_name}</b> (<b>{curr_acronym}</b>) and follow the <b>{exam_acronym}</b> format. Written for {state} students, not adapted from something generic.",
    "{state}-specific. Tests follow the <b>{curr_acronym}</b> — the <b>{curr_name}</b> — and mirror the <b>{exam_name}</b> (<b>{exam_acronym}</b>) in format and coverage.",
    "The content matches {state}'s <b>{curr_acronym}</b> standards. The test format matches the <b>{exam_name}</b> (<b>{exam_acronym}</b>). Two things that matter for real test prep.",
    "All 25 tests follow the <b>{curr_name}</b> (<b>{curr_acronym}</b>). They're designed to feel like the real <b>{exam_acronym}</b> — same types of questions, same level of difficulty. It's {state}-only content.",
    "Tests are aligned to {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>) and formatted to match the <b>{exam_acronym}</b>. The questions reflect what {state} students actually need to know.",
    "Written to match {state}'s <b>{curr_acronym}</b> and the <b>{exam_name}</b> (<b>{exam_acronym}</b>). This bundle isn't one-size-fits-all — it's {state}-focused.",
    "The questions follow {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>). The format mirrors the <b>{exam_name}</b> (<b>{exam_acronym}</b>). It's designed for {state} classrooms.",
    "This is {state}-specific test prep. All content aligns with the <b>{curr_name}</b> (<b>{curr_acronym}</b>) and mirrors the <b>{exam_acronym}</b> format.",
    "Topics, question types, and difficulty match the <b>{curr_acronym}</b> and the <b>{exam_name}</b> (<b>{exam_acronym}</b>). It's written for {state} — not a generic version with a state name on it.",
    "Aligned to {state}'s <b>{curr_acronym}</b>. Formatted like the <b>{exam_name}</b> (<b>{exam_acronym}</b>). Every test was built from the ground up for this state.",
    "Each test reflects {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>) and the <b>{exam_acronym}</b> format. The content matches what's actually taught and tested in {state}.",
    "The 25 tests are built around what {state} teaches — the <b>{curr_name}</b> (<b>{curr_acronym}</b>). Format follows the <b>{exam_name}</b> (<b>{exam_acronym}</b>).",
    "Standards alignment: <b>{curr_name}</b> (<b>{curr_acronym}</b>). Exam format: <b>{exam_name}</b> (<b>{exam_acronym}</b>). All {state}, all the way through.",
    "Made for {state}. Tests follow the <b>{curr_acronym}</b> standards and match the <b>{exam_name}</b> (<b>{exam_acronym}</b>) format. Nothing generic here.",
    "Follows {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>). The <b>{exam_acronym}</b> format is replicated across all 25 tests. Purpose-built for {state}.",
    "Tests mirror what {state} students face on the <b>{exam_name}</b> (<b>{exam_acronym}</b>), aligned to the <b>{curr_acronym}</b>. Designed for this state specifically.",
    "This bundle is rooted in {state}'s own standards — the <b>{curr_name}</b> (<b>{curr_acronym}</b>). Test format mirrors the actual <b>{exam_acronym}</b>.",
    "Every question was written with {state}'s <b>{curr_acronym}</b> in mind. The <b>{exam_name}</b> (<b>{exam_acronym}</b>) format is matched. This is state-specific test prep.",
    "All content follows the <b>{curr_acronym}</b> for {state}. Tests resemble the real <b>{exam_name}</b> (<b>{exam_acronym}</b>) in structure and content.",
    "Written for {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>). Formatted after the actual <b>{exam_acronym}</b>. No generic ingredients.",
    "From question types to topic coverage, everything matches {state}'s <b>{curr_acronym}</b> and the <b>{exam_name}</b> (<b>{exam_acronym}</b>).",
    "This bundle covers {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>) and uses the <b>{exam_acronym}</b> format. It's not adapted — it was written for {state}.",
    "Your {state} students get test prep that actually matches their state standards. Aligned to the <b>{curr_acronym}</b>, formatted like the <b>{exam_acronym}</b>.",
    "Curriculum match: <b>{curr_name}</b> (<b>{curr_acronym}</b>). Exam match: <b>{exam_name}</b> (<b>{exam_acronym}</b>). Built for {state} from scratch.",
    "Designed around {state}'s <b>{curr_acronym}</b>. Tests follow the <b>{exam_name}</b> (<b>{exam_acronym}</b>) format. This is purpose-built {state} content.",
    "All 25 practice tests in this bundle align with {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>). The <b>{exam_acronym}</b> format is reflected throughout.",
    "Each test covers {state}'s <b>{curr_acronym}</b> standards and follows the <b>{exam_name}</b> (<b>{exam_acronym}</b>) test format. Made for {state} classrooms only.",
    "This is {state} test prep at its core — aligned to the <b>{curr_name}</b> (<b>{curr_acronym}</b>), formatted like the <b>{exam_acronym}</b>.",
    "Tests track {state}'s <b>{curr_acronym}</b> and replicate the <b>{exam_name}</b> (<b>{exam_acronym}</b>) format. Content was written for this state.",
    "Content aligns with {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>). Tests mirror the <b>{exam_acronym}</b>. It was designed for {state}, plain and simple.",
    "{State}'s <b>{curr_acronym}</b> standards guide every question. The <b>{exam_name}</b> (<b>{exam_acronym}</b>) format is matched. State-specific test prep.",
    "These 25 tests reflect {state}'s <b>{curr_name}</b> (<b>{curr_acronym}</b>) and take the shape of the <b>{exam_acronym}</b>. Written exclusively for {state}.",
    "What makes this bundle {state}-specific: standards follow the <b>{curr_acronym}</b>, question format follows the <b>{exam_name}</b> (<b>{exam_acronym}</b>).",
    "Aligned with {state}'s own <b>{curr_name}</b> (<b>{curr_acronym}</b>) and designed to reflect the real <b>{exam_acronym}</b>. {State}-focused content, not filler.",
]

# --- Use case variations ---
USE_CASE_POOLS = [
    [
        "Weekly test-prep sessions throughout the school year — 25 tests means you won't run out",
        "Pre- and post-test comparisons to track student growth over time",
        "Diagnostic assessments to find skill gaps early on",
        "Homework — assign one test per week",
        "Tutoring and after-school programs — a fresh test every session",
        "Homeschool families who want realistic testing conditions at home",
        "Summer review before the next grade",
    ],
    [
        "Weekly practice tests all year — one per week, you'll still have leftovers",
        "Measure growth by comparing scores across tests",
        "Spot skill gaps early with diagnostic runs",
        "Use as homework packets — one test at a time",
        "Tutoring sessions — never reuse a test",
        "Home testing practice for homeschool families",
        "Summer prep to stay sharp",
    ],
    [
        "Enough tests for the whole school year — use them weekly and still have spares",
        "Track student improvement from test to test",
        "Diagnose weak spots with early-year assessment runs",
        "Assign individual tests as weekend homework",
        "After-school and tutoring programs that need fresh material every session",
        "Homeschool assessment — simulate real exam conditions at the kitchen table",
        "End-of-summer readiness check",
    ],
    [
        "Run weekly test-prep sessions the entire school year without repeating",
        "Compare early-year and late-year scores to measure progress",
        "Use a test early on to figure out where students need help",
        "Hand out a test as a take-home assignment",
        "Small-group tutoring — a new test every time",
        "Homeschool families prepping for the state exam",
        "Keep skills fresh over the summer",
    ],
    [
        "Weekly practice — 25 tests gives you enough for almost the entire year",
        "Before-and-after assessments to track growth",
        "Pinpoint weak areas before they become problems",
        "Use individual tests as structured homework",
        "Fresh assessment material for every tutoring session",
        "Realistic practice for homeschool students",
        "Summer math review and retention",
    ],
]

# --- Quality section variations ---
QUALITY_SECTIONS = [
    [
        "Colorful, kid-friendly design with illustrations, diagrams, and a friendly owl mascot",
        "Complete answer keys with step-by-step explanations for every question",
        "Print-ready — download, print, and use right away",
    ],
    [
        "Engaging, full-color pages with illustrations and the View Math owl mascot",
        "Detailed answer explanations for every single question",
        "Ready to print — just download and go",
    ],
    [
        "Professional, kid-friendly design — colorful pages, diagrams, and the View Math owl",
        "Every question comes with a step-by-step answer explanation",
        "Download, print, use. No extra prep needed.",
    ],
    [
        "Colorful design with diagrams, illustrations, and the friendly owl mascot kids love",
        "Answer keys with full explanations — every question, every test",
        "Print-ready format — download it, print it, hand it out",
    ],
    [
        "Full-color, engaging design with illustrations, diagrams, and the View Math owl",
        "Step-by-step answer explanations included for all 750 questions",
        "Print and use — no prep, no assembly, no extras needed",
    ],
    [
        "Eye-catching design with colorful pages, helpful diagrams, and the View Math owl mascot",
        "All questions come with thorough answer explanations",
        "Print-ready — download, print, and start using immediately",
    ],
    [
        "Clean, colorful layout with diagrams and the View Math owl students recognize",
        "Complete answer keys with clear, detailed explanations",
        "Download and print — ready to use with zero prep",
    ],
    [
        "Bright, student-friendly pages with illustrations and the owl mascot",
        "Answer explanations walk through every question step by step",
        "Just print it — that's all the prep you need",
    ],
    [
        "Colorful pages, helpful diagrams, and the signature owl mascot throughout",
        "Detailed answer keys explain every question, every test",
        "Print-ready — no prep, no setup, no hassle",
    ],
    [
        "Kid-friendly design with full-color pages, diagrams, and the View Math owl",
        "Step-by-step explanations for every answer across all 25 tests",
        "Print, hand out, done. It's that simple.",
    ],
]

# --- Cross-sell intro variations ---
CROSSSELL_INTROS = [
    "Practice tests work best when students already know the material. Pair this bundle with:",
    "Tests check understanding — but students need to learn the material first. Consider adding:",
    "For the best results, pair these tests with resources that teach the content:",
    "Practice tests show what students know. If they need to learn or review, check out:",
    "These tests assess skills — they don't teach them. For instruction and practice, grab:",
    "Got the tests? Now make sure students are ready for them:",
    "25 tests is a lot of assessment. Make sure students have the tools to succeed:",
    "Tests are the end of the process. For everything that comes before:",
    "Pair your practice tests with instruction materials:",
    "For teaching, daily practice, or enrichment — here are the companions:",
    "Practice tests measure progress. These resources build the skills:",
    "These tests assess — these other books teach and reinforce:",
    "To complete your math toolkit, add:",
    "Students do better on tests when they've practiced the content. Try:",
    "Before the tests, make sure students are prepared with:",
    "Test prep works best with learning materials alongside it:",
    "If your students need to learn the material before testing:",
    "Add instruction and practice to go with your test prep:",
    "Tests are great for assessment — pair them with tools for learning:",
    "The tests handle assessment. For everything else, explore:",
    "Ready to go beyond practice tests? The series also includes:",
    "For a fuller experience, check out these books from the same series:",
    "Fill in the gaps before test day with these companions:",
    "These tests cover assessment. The rest of the series covers learning:",
    "Students learn best when they practice and test. Add these for the practice side:",
    "Prep doesn't stop at tests. Here's what else can help:",
    "Build skills first, then test them. Here are the skill-building books:",
    "To round out the test prep, consider adding:",
    "Tests alone don't teach. Pair them with one of these:",
    "These books round out your test prep toolkit:",
    "For instruction, enrichment, or daily practice, browse the rest of the series:",
    "Test day goes better when students have practiced with these:",
    "Assessment is just one piece. For the others:",
    "Supplement your test prep with any of these:",
    "Looking for the teaching side of things? The series includes:",
    "Assessment handled? Now handle instruction:",
    "There's more in the series — here's what pairs well with practice tests:",
    "To make the most of these tests, make sure students have studied with:",
    "Comprehensive prep means more than just tests. Consider:",
    "The practice tests cover assessment — these cover everything else:",
    "For instruction, review, and enrichment alongside your tests:",
    "Build skills before you assess them. Check out:",
    "Students who study first score better on tests. Here's what helps:",
    "The rest of the series covers instruction, practice, and fun. Take a look:",
    "Round out your lineup with these teaching resources:",
    "Cover all the bases — tests plus instruction:",
    "Test prep is one part of the journey. For the rest:",
    "Support test practice with learning resources:",
    "Want to pair instruction with assessment? Add:",
    "From the same series — teaching and practice materials:",
]

# --- Cross-sell book descriptions ---
CROSSSELL_DESCRIPTIONS = {
    "study_guide": [
        "<b>Study Guide</b> — A concise review of key concepts, essential examples, and quick practice",
        "<b>Study Guide</b> — Key concepts and worked examples for every topic",
        "<b>Study Guide</b> — Quick concept review with examples and practice checks",
        "<b>Study Guide</b> — Compact review covering every topic in the curriculum",
    ],
    "workbook": [
        "<b>Workbook</b> — Hundreds of scaffolded practice problems organized by topic",
        "<b>Workbook</b> — Practice problems from easy to challenging, organized by topic",
        "<b>Workbook</b> — Structured practice with hundreds of problems per chapter",
        "<b>Workbook</b> — Topic-by-topic practice that builds from basic to advanced",
    ],
    "step_by_step": [
        "<b>Step-by-Step Guide</b> — Numbered instructions for every problem type",
        "<b>Step-by-Step Guide</b> — Clear, numbered procedures for every math skill",
        "<b>Step-by-Step Guide</b> — Road maps and step-by-step instructions for every topic",
        "<b>Step-by-Step Guide</b> — Great for students who need structured walkthroughs",
    ],
    "in_30_days": [
        "<b>Math in 30 Days</b> — A structured daily plan covering the full curriculum in one month",
        "<b>Math in 30 Days</b> — Day-by-day study plan to cover everything before the exam",
        "<b>Math in 30 Days</b> — Full curriculum review on a 30-day schedule",
        "<b>Math in 30 Days</b> — One month, every topic, daily structure",
    ],
    "quiz": [
        "<b>Quizzes</b> — Quick 15-minute assessments for every topic",
        "<b>Quizzes</b> — One quiz per topic, 15 minutes each, with scoring guides",
        "<b>Quizzes</b> — Short, focused checks for every topic in the curriculum",
        "<b>Quizzes</b> — Fast topic assessments with answer keys",
    ],
    "puzzles": [
        "<b>Puzzles & Brain Teasers</b> — Curriculum-aligned games and challenges that make math fun",
        "<b>Puzzles & Brain Teasers</b> — Code breakers, riddles, mazes — fun math that's standards-aligned",
        "<b>Puzzles & Brain Teasers</b> — Engaging math puzzles for every topic",
        "<b>Puzzles & Brain Teasers</b> — Make math fun with curriculum-aligned puzzle activities",
    ],
    "worksheet": [
        "<b>Worksheets</b> — Standalone printable activities for any topic, any order",
        "<b>Worksheets</b> — One-page printable activities, usable in any sequence",
        "<b>Worksheets</b> — Grab-and-go printables for any topic",
        "<b>Worksheets</b> — Individual topic worksheets — use them in any order",
    ],
}

# --- CTA (closing) variations ---
CTAS = [
    ("<p>25 tests, 750 questions, zero repeats. That's the bundle.</p>",
     "<p><b>Grab it now and give your students the test prep they need.</b></p>"),
    ("<p>Your students get 25 unique tests — enough practice to last the whole year.</p>",
     "<p><b>Download the bundle and get started today.</b></p>"),
    ("<p>750 unique questions. 25 unique tests. One download.</p>",
     "<p><b>Get the bundle now.</b></p>"),
    ("<p>Everything your students need for test practice — in one bundle.</p>",
     "<p><b>Download it today and start prepping.</b></p>"),
    ("<p>25 full-length tests. No repeats. One click.</p>",
     "<p><b>Add to cart and get your students ready.</b></p>"),
    ("<p>Serious test prep doesn't have to be complicated. 25 tests. Done.</p>",
     "<p><b>Download the bundle and start using it this week.</b></p>"),
    ("<p>That's 25 tests and 750 questions — all unique, all ready to print.</p>",
     "<p><b>Get it now and give your students the practice they deserve.</b></p>"),
    ("<p>From first test to last — 25 fresh assessments, zero overlap.</p>",
     "<p><b>Download today.</b></p>"),
    ("<p>The most test prep you'll find in one bundle. 25 unique tests. 750 questions.</p>",
     "<p><b>Grab it now.</b></p>"),
    ("<p>Everything here. Nothing repeated. 25 practice tests.</p>",
     "<p><b>Add it to your classroom resources today.</b></p>"),
    ("<p>25 tests is a lot of test prep. And it's all unique.</p>",
     "<p><b>Download the bundle now.</b></p>"),
    ("<p>Fresh test prep, from test 1 to test 25. No recycled content.</p>",
     "<p><b>Get it for your students today.</b></p>"),
    ("<p>750 questions across 25 tests — none repeated. One bundle.</p>",
     "<p><b>Download and start this week.</b></p>"),
    ("<p>Your {exam_acronym} practice, sorted. 25 tests. One download.</p>",
     "<p><b>Get the bundle now.</b></p>"),
    ("<p>All the test prep. None of the repeats.</p>",
     "<p><b>Add it to your cart and get started.</b></p>"),
    ("<p>25 tests. 750 questions. Zero overlap. One bundle.</p>",
     "<p><b>Download it today.</b></p>"),
    ("<p>Your students deserve fresh practice tests every time. Here they are.</p>",
     "<p><b>Grab the bundle now.</b></p>"),
    ("<p>Nothing recycled. 25 tests. 750 questions. All ready for your classroom.</p>",
     "<p><b>Get it today.</b></p>"),
    ("<p>The math practice is done. Now just print and go.</p>",
     "<p><b>Download the practice test bundle now.</b></p>"),
    ("<p>This is test prep that lasts all year. 25 unique tests in one download.</p>",
     "<p><b>Add to cart.</b></p>"),
    ("<p>25 unique assessments — enough to keep your students practicing all year.</p>",
     "<p><b>Download this bundle today.</b></p>"),
    ("<p>25 tests. All unique. All explained. All print-ready.</p>",
     "<p><b>Get it now and prep with confidence.</b></p>"),
    ("<p>25 tests in one place. No repeat questions. No hassle.</p>",
     "<p><b>Download and put them to work.</b></p>"),
    ("<p>Enough test prep for the whole year — all in one download.</p>",
     "<p><b>Get the bundle today.</b></p>"),
    ("<p>750 questions. 25 tests. Four books. Zero overlap. All yours.</p>",
     "<p><b>Download now.</b></p>"),
    ("<p>Fresh tests, explained answers, and nothing repeated.</p>",
     "<p><b>Add the bundle to your resources.</b></p>"),
    ("<p>25 tests ready to be printed and used. Every one unique.</p>",
     "<p><b>Download it now.</b></p>"),
    ("<p>Test prep sorted for the year. 25 unique assessments, one click.</p>",
     "<p><b>Get the bundle.</b></p>"),
    ("<p>25 complete, unique practice tests — that's a lot of prep.</p>",
     "<p><b>Download today and get started.</b></p>"),
    ("<p>The whole test prep package. No duplicates. No filler.</p>",
     "<p><b>Grab it now.</b></p>"),
    ("<p>All the practice, none of the repetition. 25 tests, one bundle.</p>",
     "<p><b>Download it today.</b></p>"),
    ("<p>Your test prep is right here. 25 tests. Zero overlap. One download.</p>",
     "<p><b>Get it now.</b></p>"),
    ("<p>One bundle covers the entire year's test practice. 25 unique tests.</p>",
     "<p><b>Add to cart and start prepping.</b></p>"),
    ("<p>750 fresh questions. 25 completely unique tests. One file.</p>",
     "<p><b>Download the bundle now.</b></p>"),
    ("<p>25 tests means 25 opportunities for real practice. Don't settle for less.</p>",
     "<p><b>Get the bundle today.</b></p>"),
    ("<p>25 full-length tests. Detailed explanations. Zero repeats.</p>",
     "<p><b>Download it.</b></p>"),
    ("<p>Fresh practice tests for the whole year. That's what this bundle is.</p>",
     "<p><b>Get it now.</b></p>"),
    ("<p>Twenty-five tests waiting to be used. All unique. All explained.</p>",
     "<p><b>Download this bundle today.</b></p>"),
    ("<p>Enough test prep to fill a school year — and then some.</p>",
     "<p><b>Download it now.</b></p>"),
    ("<p>The bottom line: 25 unique tests, 750 questions, no overlap.</p>",
     "<p><b>Grab the bundle and help your students succeed.</b></p>"),
    ("<p>All the tests your students need — and none of the repetition.</p>",
     "<p><b>Download now and start prepping.</b></p>"),
    ("<p>Twenty-five unique tests. That's what's inside.</p>",
     "<p><b>Get the bundle and start practicing today.</b></p>"),
    ("<p>750 questions. Every one unique. Every one explained. Ready to print.</p>",
     "<p><b>Download it today.</b></p>"),
    ("<p>Test prep for the full year — one download, 25 tests, zero repeats.</p>",
     "<p><b>Get it now.</b></p>"),
    ("<p>All the practice your students could need for one state test.</p>",
     "<p><b>Download the bundle today.</b></p>"),
    ("<p>From start to finish, every test is fresh. 25 assessments. One bundle.</p>",
     "<p><b>Grab it now.</b></p>"),
    ("<p>25 tests, all unique, all ready. That's the deal.</p>",
     "<p><b>Download and get started.</b></p>"),
    ("<p>Your {exam_acronym} prep, handled. 25 tests. One download.</p>",
     "<p><b>Add to cart now.</b></p>"),
    ("<p>25 completely different tests for your students — all in one bundle.</p>",
     "<p><b>Download it and start prepping.</b></p>"),
    ("<p>750 unique questions. 25 unique tests. Ready to go.</p>",
     "<p><b>Get the bundle today.</b></p>"),
]

# --- Footer (exact, never modify) ---
FOOTER = """<p></p>★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★<p></p>

<p>
  Looking for more <b>Grade 7 Math</b> resources? Visit my
  <a href="https://www.teacherspayteachers.com/store/viewmath" target="_blank"><b>TPT store</b></a>
  for engaging, classroom-ready materials from <b>View Math</b> — a math education company dedicated to helping students succeed.
</p>

<p>
  Explore more teaching tools and learning materials at
  <a href="https://www.viewmath.com" target="_blank"><b>ViewMath.com</b></a>.
</p>

<p>
  Questions or suggestions? Reach out at
  <a href="mailto:dr.nazari@viewmath.com">dr.nazari@viewmath.com</a>.
</p>

<p>
  <b>Follow me</b> to catch new releases — all <b>50% off</b> for the first 24 hours!
</p>

<p>
  <b>– Dr. A. Nazari</b>
</p>"""


# ============================================================================
# BUILDER
# ============================================================================

def build_description(state_data: Dict[str, Any], state_index: int) -> str:
    """Build a unique HTML description for one state."""
    rng = random.Random(state_index * 7 + 42)  # deterministic per state

    sd = state_data
    state = sd["state_name"]
    exam = sd["exam_name"]
    exam_acr = sd["exam_acronym"]
    curr = sd["curriculum_name"]
    curr_acr = sd["curriculum_acronym"]
    grade = sd["grade"]
    bundle_title = sd["bundle_title"]
    tpt_title = sd["tpt_title"]
    book_titles = sd["book_titles"]

    parts = []

    # --- HTML comments ---
    books_str = "3 Practice Tests + 5 Practice Tests + 7 Practice Tests + 10 Practice Tests"
    parts.append(f"<!-- {bundle_title} -->")
    parts.append(f"<!-- Bundle: {books_str} -->")
    parts.append(f"<!-- TPT Title: {tpt_title} -->")
    parts.append("")

    # --- Opening ---
    opening = rng.choice(OPENINGS)
    opening = opening.replace("{state}", state).replace("{State}", state)
    opening = opening.replace("{exam}", exam).replace("{exam_acronym}", exam_acr)
    opening = opening.replace("{grade}", grade)
    parts.append(f"<p>{opening}</p>")

    # --- Build each section ---
    order = SECTION_ORDERS[state_index % len(SECTION_ORDERS)]

    for section in order:
        parts.append("")  # spacing

        if section == "included":
            heading = rng.choice(HEADINGS_INCLUDED)
            intro = rng.choice(INCLUDED_INTROS)

            parts.append(f"<p></p>\n<p><b>{heading}</b></p>")
            if intro:
                parts.append(f"<p>{intro}</p>")
            parts.append("<ul>")

            book_types_ordered = ["3_practice_tests", "5_practice_tests", "7_practice_tests", "10_practice_tests"]
            for bt in book_types_ordered:
                oneliner = rng.choice(BOOK_ONELINERS[bt])
                bt_title = book_titles.get(bt, "")
                display_name = {"3_practice_tests": "3 Practice Tests", "5_practice_tests": "5 Practice Tests", "7_practice_tests": "7 Practice Tests", "10_practice_tests": "10 Practice Tests"}[bt]
                parts.append(f"  <li>✅ <b>{display_name}</b> — {oneliner}</li>")

            parts.append("</ul>")

            reinforcement = rng.choice(POST_LIST_REINFORCEMENTS)
            parts.append(f"<p>{reinforcement}</p>")

        elif section == "curriculum":
            heading = rng.choice(HEADINGS_CURRICULUM)
            heading = heading.replace("{state}", state).replace("{acronym}", curr_acr)
            curr_text = rng.choice(CURRICULUM_TEMPLATES)
            curr_text = curr_text.replace("{state}", state).replace("{State}", state)
            curr_text = curr_text.replace("{curr_name}", curr).replace("{curr_acronym}", curr_acr)
            curr_text = curr_text.replace("{exam_name}", exam).replace("{exam_acronym}", exam_acr)

            parts.append(f"<p></p>\n<p><b>{heading}</b></p>")
            parts.append(f"<p>{curr_text}</p>")

        elif section == "usecases":
            heading = rng.choice(HEADINGS_USECASES)
            use_pool = rng.choice(USE_CASE_POOLS)
            # pick 5-7 use cases
            n = rng.randint(5, min(7, len(use_pool)))
            selected = rng.sample(use_pool, n)

            parts.append(f"<p></p>\n<p><b>{heading}</b></p>")
            parts.append("<ul>")
            for uc in selected:
                parts.append(f"  <li>✅ {uc}</li>")
            parts.append("</ul>")

        elif section == "quality":
            heading = rng.choice(HEADINGS_QUALITY)
            quality = rng.choice(QUALITY_SECTIONS)

            parts.append(f"<p></p>\n<p><b>{heading}</b></p>")
            parts.append("<ul>")
            for q in quality:
                parts.append(f"  <li>✅ {q}</li>")
            parts.append("</ul>")

        elif section == "crosssell":
            heading = rng.choice(HEADINGS_CROSSSELL)
            intro = rng.choice(CROSSSELL_INTROS)

            parts.append(f"<p></p>\n<p><b>{heading}</b></p>")
            parts.append(f"<p>{intro}</p>")
            parts.append("<ul>")

            cross_sell_books = ["study_guide", "workbook", "step_by_step", "in_30_days", "quiz", "puzzles", "worksheet"]
            for csb in cross_sell_books:
                desc = rng.choice(CROSSSELL_DESCRIPTIONS[csb])
                parts.append(f"  <li>✅ {desc}</li>")

            parts.append("</ul>")

    # --- CTA ---
    parts.append("")
    cta_line1, cta_line2 = rng.choice(CTAS)
    cta_line1 = cta_line1.replace("{exam_acronym}", exam_acr)
    cta_line2 = cta_line2.replace("{exam_acronym}", exam_acr)
    parts.append(cta_line1)
    parts.append(cta_line2)

    # --- Footer ---
    parts.append("")
    parts.append(FOOTER)

    return "\n".join(parts)


# ============================================================================
# MAIN
# ============================================================================

ALL_STATES = [
    "alabama", "alaska", "arizona", "arkansas", "california",
    "colorado", "connecticut", "delaware", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa",
    "kansas", "kentucky", "louisiana", "maine", "maryland",
    "massachusetts", "michigan", "minnesota", "mississippi", "missouri",
    "montana", "nebraska", "nevada", "new-hampshire", "new-jersey",
    "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
    "south-dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west-virginia", "wisconsin", "wyoming",
]


def main():
    parser = argparse.ArgumentParser(description="Generate practice_tests_bundle descriptions for all states")
    parser.add_argument("--state", help="Generate for a single state only")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of saving")
    args = parser.parse_args()

    states_to_process = [args.state] if args.state else ALL_STATES
    output_dir = WORKSPACE / "final_output" / "bundles" / "practice_tests_bundle"
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, slug in enumerate(ALL_STATES):
        if slug not in states_to_process:
            continue

        sd = get_state_data(slug)
        html = build_description(sd, idx)

        if args.dry_run:
            print(f"=== {slug} ===")
            print(html[:500])
            print("...\n")
        else:
            out_path = output_dir / f"{slug}_tpt_bundle.html"
            out_path.write_text(html, encoding="utf-8")
            print(f"✓ {slug} → {out_path.relative_to(WORKSPACE)}")

    print(f"\nDone. {len(states_to_process)} description(s) generated.")


if __name__ == "__main__":
    main()
