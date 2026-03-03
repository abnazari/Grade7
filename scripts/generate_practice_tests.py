#!/usr/bin/env python3
"""
Generate practice tests for each US state from the question bank.

For each state, this script:
  1. Determines which topics apply (core CCSS + state-specific additions)
  2. Loads raw question blocks from question bank files
  3. When a state has more than 30 topics, randomly selects 30
  4. Generates 25 practice tests (3+5+7+10), each with 30 questions
  5. Ensures every question is unique across ALL tests for the same state
  6. Outputs one .tex file per test containing ONLY the question blocks

Book types use non-overlapping test ranges:
    3_practice_tests  → tests  1–3
    5_practice_tests  → tests  4–8
    7_practice_tests  → tests  9–15
    10_practice_tests → tests 16–25

Output structure:
    practice_tests/<state>/practice_test_01.tex
    practice_tests/<state>/practice_test_02.tex
    ...
    practice_tests/<state>/practice_test_25.tex

Each file contains raw \\begin{practiceQuestion}...\\end{practiceQuestion}
blocks that can be \\input'd into a main.tex file later.

Question bank format (in tests_questions_bank/topics/):
    \\begin{practiceQuestion}{ID}{TYPE}
    \\begin{questionText}
    ...
    \\end{questionText}
    \\choiceA{...}          % MC only
    \\choiceB{...}          % MC only
    \\choiceC{...}          % MC only
    \\choiceD{...}          % MC only
    \\correctAnswer{...}
    \\explanation{...}
    \\end{practiceQuestion}

Usage:
    # Generate 25 practice tests for all 50 states
    python3 scripts/generate_practice_tests.py

    # Specific states
    python3 scripts/generate_practice_tests.py --states texas,california

    # Custom number of tests
    python3 scripts/generate_practice_tests.py --num-tests 10

    # Custom number of questions per test
    python3 scripts/generate_practice_tests.py --questions-per-test 5

    # Limit topics per state
    python3 scripts/generate_practice_tests.py --max-topics 25

    # Custom random seed (for reproducibility)
    python3 scripts/generate_practice_tests.py --seed 42
"""

import argparse
import re
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from config import prompt_states
from config_loader import TopicsConfig, find_workspace, load_config


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class RawQuestion:
    """A question stored as its raw LaTeX block text."""
    id: str             # e.g., '1-1-q01'
    type: str           # 'mc' or 'sa'
    raw_block: str      # Full text from \begin{practiceQuestion} to \end{...}
    topic_id: str       # e.g., 'ch01-01'


# ============================================================================
# QUESTION BANK PARSER — extracts raw blocks
# ============================================================================

BLOCK_PATTERN = re.compile(
    r'(\\begin\{practiceQuestion\}\s*\{([^}]+)\}\s*\{([^}]+)\}'
    r'.*?'
    r'\\end\{practiceQuestion\})',
    re.DOTALL,
)


def parse_raw_questions(filepath: Path, topic_id: str) -> List[RawQuestion]:
    """Parse a question bank file and extract raw question blocks verbatim.

    Returns a list of RawQuestion objects containing the exact source text.
    """
    text = filepath.read_text(encoding="utf-8")
    questions = []

    for match in BLOCK_PATTERN.finditer(text):
        raw_block = match.group(1)
        qid = match.group(2).strip()
        qtype = match.group(3).strip()

        questions.append(RawQuestion(
            id=qid,
            type=qtype,
            raw_block=raw_block,
            topic_id=topic_id,
        ))

    return questions


def load_all_question_banks(
    workspace: Path,
) -> tuple[Dict[str, List[RawQuestion]], Dict[str, List[RawQuestion]]]:
    """Load all question banks from the workspace.

    Scans three question-bank directories:
      - tests_questions_bank/topics/           (core CCSS)
      - tests_questions_bank/topics_additional/ (supplementary)
      - tests_questions_bank/topics_modifed/    (state-modified)

    Modified banks are kept separate because they share topic IDs with core
    banks — they must only replace core questions for states that actually
    require the modification (listed in the YAML config).

    Returns:
        (core_banks, modified_banks) — each mapping topic_id → list of RawQuestion
    """
    core_banks: Dict[str, List[RawQuestion]] = {}
    modified_banks: Dict[str, List[RawQuestion]] = {}
    bank_root = workspace / "tests_questions_bank"

    # ── Core + additional (shared by all states) ────────────────────────
    for scan_dir in [bank_root / "topics", bank_root / "topics_additional"]:
        if not scan_dir.exists():
            continue
        for filepath in sorted(scan_dir.glob("*.tex")):
            m = re.match(r'(ch\d{2}-\d{2})', filepath.stem)
            if not m:
                print(f"  WARNING: Skipping {filepath.name} — cannot extract topic ID")
                continue
            topic_id = m.group(1)

            questions = parse_raw_questions(filepath, topic_id)
            if questions:
                core_banks[topic_id] = questions
                mc = sum(1 for q in questions if q.type in ("mc", "gmc"))
                sa = sum(1 for q in questions if q.type in ("sa", "gsa"))
                print(f"  Loaded {len(questions):2d} questions ({mc} MC + {sa} SA) "
                      f"for {topic_id} ({filepath.name})")
            else:
                print(f"  WARNING: No questions parsed from {filepath.name}")

    # ── Modified banks (state-specific replacements) ────────────────────
    mod_dir = bank_root / "topics_modifed"
    if mod_dir.exists():
        for filepath in sorted(mod_dir.glob("*.tex")):
            m = re.match(r'(ch\d{2}-\d{2})', filepath.stem)
            if not m:
                print(f"  WARNING: Skipping {filepath.name} — cannot extract topic ID")
                continue
            topic_id = m.group(1)

            questions = parse_raw_questions(filepath, topic_id)
            if questions:
                modified_banks[topic_id] = questions
                mc = sum(1 for q in questions if q.type in ("mc", "gmc"))
                sa = sum(1 for q in questions if q.type in ("sa", "gsa"))
                print(f"  Loaded {len(questions):2d} questions ({mc} MC + {sa} SA) "
                      f"for {topic_id} [modified] ({filepath.name})")
            else:
                print(f"  WARNING: No questions parsed from {filepath.name}")

    return core_banks, modified_banks


def build_state_banks(
    core_banks: Dict[str, List[RawQuestion]],
    modified_banks: Dict[str, List[RawQuestion]],
    state_slug: str,
    config: TopicsConfig,
) -> Dict[str, List[RawQuestion]]:
    """Build question banks for a specific state.

    Starts with core banks, then swaps in modified banks for topics
    that this state requires in modified form.
    """
    state_banks = dict(core_banks)           # shallow copy
    for tid in config.state_modified.get(state_slug, {}):
        if tid in modified_banks:
            state_banks[tid] = modified_banks[tid]
    return state_banks


# ============================================================================
# STATE TOPIC RESOLUTION
# ============================================================================

def get_state_topics(state_slug: str, config: TopicsConfig) -> List[str]:
    """Get the full ordered list of topic IDs for a state.

    Starts with the core CCSS topics (from YAML) and inserts any
    state-specific additional topics immediately after the last core
    topic of the same chapter.
    """
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


# ============================================================================
# TOPIC SELECTION — prioritize state-specific topics when capping
# ============================================================================

def weighted_topic_selection(
    available: List[str],
    state_specific_ids: Set[str],
    max_topics: int,
    rng: random.Random,
) -> List[str]:
    """Select topics with state-specific topics receiving 2x selection weight.

    When a state has more available topics than max_topics, this function
    performs a weighted random selection where additional and modified topics
    are twice as likely to be picked as regular core topics.

    Args:
        available:          All topic IDs with question banks for this state.
        state_specific_ids: Additional + modified topic IDs for this state.
        max_topics:         Maximum number of topics to select.
        rng:                Random number generator for reproducibility.

    Returns:
        Sorted list of selected topic IDs (preserves chapter order).
    """
    weights = [2.0 if t in state_specific_ids else 1.0 for t in available]
    selected = []
    remaining = list(range(len(available)))
    remaining_weights = list(weights)

    for _ in range(min(max_topics, len(available))):
        chosen_idx = rng.choices(remaining, weights=remaining_weights, k=1)[0]
        pos = remaining.index(chosen_idx)
        selected.append(available[chosen_idx])
        remaining.pop(pos)
        remaining_weights.pop(pos)

    return sorted(selected)


# ============================================================================
# PRACTICE TEST GENERATION
# ============================================================================

def _weighted_shuffle(topics: List[str], rng: random.Random) -> List[str]:
    """Shuffle topics within a chapter, biased so earlier topics appear first.

    Uses exponentially decaying weights: topic at index 0 in the chapter is
    ~4x more likely to be picked first than the last topic. This keeps the
    natural difficulty progression (earlier = easier) mostly intact while
    adding variety across tests.
    """
    remaining = list(enumerate(topics))  # (original_index, topic_id)
    result = []
    while remaining:
        weights = [4.0 ** (1 - idx / max(len(topics) - 1, 1))
                   for idx, _ in remaining]
        chosen = rng.choices(remaining, weights=weights, k=1)[0]
        remaining.remove(chosen)
        result.append(chosen[1])
    return result


def _build_chapter_rotation(
    topic_ids: List[str],
    question_banks: Dict[str, List[RawQuestion]],
    rng: random.Random,
) -> List[str]:
    """Build a topic rotation that preserves chapter order.

    1. Groups available topics by chapter (ch01, ch02, ...).
    2. Within each chapter, does a weighted shuffle (earlier topics favoured).
    3. Interleaves chapters round-robin so questions cycle through all chapters
       before revisiting one.

    Example with 3 chapters of varying sizes:
        ch01: [A, B]  ch02: [C, D, E]  ch03: [F]
        → [A, C, F, B, D, E]  (round-robin, then leftover from ch02)
    """
    # Group by chapter, preserving input order within each chapter
    chapter_order: List[str] = []       # e.g. ["ch01", "ch03", "ch05"]
    chapter_topics: Dict[str, List[str]] = {}
    for tid in topic_ids:
        if tid not in question_banks:
            continue
        ch = tid[:4]
        if ch not in chapter_topics:
            chapter_order.append(ch)
            chapter_topics[ch] = []
        chapter_topics[ch].append(tid)

    # Weighted shuffle within each chapter
    for ch in chapter_order:
        chapter_topics[ch] = _weighted_shuffle(chapter_topics[ch], rng)

    # Interleave: round-robin across chapters in chapter order
    rotation: List[str] = []
    pointers = {ch: 0 for ch in chapter_order}
    max_len = max((len(chapter_topics[ch]) for ch in chapter_order), default=0)
    for slot in range(max_len):
        for ch in chapter_order:
            topics = chapter_topics[ch]
            if slot < len(topics):
                rotation.append(topics[slot])

    return rotation


def generate_practice_tests(
    topic_ids: List[str],
    question_banks: Dict[str, List[RawQuestion]],
    num_tests: int,
    questions_per_test: int,
    rng: random.Random,
) -> List[List[RawQuestion]]:
    """Generate practice tests with unique questions across all tests.

    Each test gets `questions_per_test` questions. Topics are assigned via
    chapter-aware round-robin: chapters appear in order (ch01 before ch07),
    and within each chapter earlier/easier topics are more likely to come
    first. Questions are never reused across tests for the same state.

    Returns a list of tests; each test is a list of RawQuestions in
    approximate chapter order.
    """
    # Build per-topic queues (shuffled for randomness within each topic)
    topic_queues: Dict[str, List[RawQuestion]] = {}
    for tid in topic_ids:
        if tid not in question_banks:
            continue
        pool = question_banks[tid].copy()
        rng.shuffle(pool)
        topic_queues[tid] = pool

    # Build chapter-aware rotation
    rotation = _build_chapter_rotation(topic_ids, question_banks, rng)
    if not rotation:
        return []

    tests = []
    topic_ptr = 0  # Global pointer into rotation

    for _ in range(num_tests):
        test_questions: List[RawQuestion] = []
        attempts = 0
        max_attempts = len(rotation)  # Prevent infinite loop

        while len(test_questions) < questions_per_test and attempts < max_attempts:
            tid = rotation[topic_ptr % len(rotation)]
            topic_ptr += 1
            attempts += 1

            if topic_queues[tid]:
                test_questions.append(topic_queues[tid].pop(0))

        # Sort questions: group by chapter, then by topic order within chapter
        # e.g., all ch01 questions first (in topic order), then ch02, etc.
        topic_order = {tid: i for i, tid in enumerate(topic_ids)}
        test_questions.sort(key=lambda q: (
            q.topic_id[:4],                          # primary: chapter group
            topic_order.get(q.topic_id, 999),        # secondary: topic order
        ))

        if not test_questions:
            break  # No more questions available anywhere

        tests.append(test_questions)

    return tests


# ============================================================================
# VISUAL INJECTION — topic-aware TikZ visuals for ~20-25% of questions
# ============================================================================

# Regex helpers for extracting numbers from question text
_FRAC_RE = re.compile(r'\\frac\{(\d+)\}\{(\d+)\}')
_TIMES_RE = re.compile(r'\$(\d+)\s*\\times\s*(\d+)\$')
_DOLLAR_NUM_RE = re.compile(r'\$(\d[\d,]*)\$')
_DEGREE_RE = re.compile(r'\$(\d+)\s*\\circ\$|\$(\d+)\^\{?\\circ\}?\$')
_DIM_PAIR_RE = re.compile(
    r'(?:length|long|wide|width|height)\s+(?:of\s+)?\$(\d+)\$'
    r'.*?'
    r'(?:length|long|wide|width|height)\s+(?:of\s+)?\$(\d+)\$',
    re.IGNORECASE | re.DOTALL,
)
_SQ_UNITS_DIM_RE = re.compile(
    r'\$(\d+)\$\s*(?:units?|cm|m|ft|in|inches|feet|meters?|centimeters?)'
    r'.*?'
    r'\$(\d+)\$\s*(?:units?|cm|m|ft|in|inches|feet|meters?|centimeters?)',
    re.IGNORECASE | re.DOTALL,
)


def _extract_question_text(raw_block: str) -> str:
    """Extract content between \\begin{questionText} and \\end{questionText}."""
    m = re.search(
        r'\\begin\{questionText\}(.*?)\\end\{questionText\}',
        raw_block, re.DOTALL,
    )
    return m.group(1) if m else raw_block


def _try_fraction_visual(qtext: str, rng: random.Random) -> Optional[str]:
    """Generate a fraction bar or circle for questions containing \\frac{N}{D}.

    When exactly one suitable fraction is found, shows it as a bar or circle.
    When two suitable fractions are found (comparison questions), shows them
    side-by-side so both values are visible — never just one of two.
    """
    fracs = _FRAC_RE.findall(qtext)
    if not fracs:
        return None

    # Filter to visually sensible fractions (denom ≤ 12, num ≤ denom)
    good: list[tuple[int, int]] = []
    for num_s, den_s in fracs:
        num, den = int(num_s), int(den_s)
        if 1 <= den <= 12 and 0 <= num <= den:
            good.append((num, den))

    if not good:
        return None

    # Two fractions → side-by-side comparison visual
    if len(good) >= 2:
        (n1, d1), (n2, d2) = good[0], good[1]
        use_bar = rng.random() < 0.5
        cmd = '\\fractionBar' if use_bar else '\\fractionCircle'
        return (
            f'\\begin{{center}}\n'
            f'{cmd}{{{n1}}}{{{d1}}}\n'
            f'\\hspace{{1cm}}\n'
            f'{cmd}{{{n2}}}{{{d2}}}\n'
            f'\\end{{center}}'
        )

    # Single fraction
    num, den = good[0]
    if rng.random() < 0.5:
        return f'\\fractionBar{{{num}}}{{{den}}}'
    else:
        return f'\\fractionCircle{{{num}}}{{{den}}}'


def _try_area_visual(qtext: str) -> Optional[str]:
    """Generate an areaGrid for area questions with two dimensions."""
    # Look for two dimensions in the question
    m = _DIM_PAIR_RE.search(qtext)
    if not m:
        m = _SQ_UNITS_DIM_RE.search(qtext)
    if m:
        d1, d2 = int(m.group(1)), int(m.group(2))
        # Keep grid reasonable (max 10×10 visually)
        if 1 <= d1 <= 10 and 1 <= d2 <= 10:
            return f'\\areaGrid{{{d1}}}{{{d2}}}'
    return None


def _try_perimeter_visual(qtext: str) -> Optional[str]:
    """Generate a perimeterRect for perimeter questions."""
    m = _DIM_PAIR_RE.search(qtext)
    if not m:
        m = _SQ_UNITS_DIM_RE.search(qtext)
    if m:
        length, width = int(m.group(1)), int(m.group(2))
        if 1 <= length <= 20 and 1 <= width <= 20:
            # Detect unit
            unit_m = re.search(
                r'\$\d+\$\s*(cm|m|ft|in|inches|feet|units?|meters?|centimeters?)',
                qtext, re.IGNORECASE,
            )
            unit = unit_m.group(1) if unit_m else 'units'
            # Normalise unit abbreviations
            unit = unit.rstrip('s').rstrip('e')  # "inches" → "inch" etc.
            short = {'centimeter': 'cm', 'meter': 'm', 'inch': 'in',
                     'foot': 'ft', 'feet': 'ft', 'unit': 'units'}
            unit = short.get(unit, unit)
            return f'\\perimeterRect{{{length}}}{{{width}}}{{{unit}}}'
    return None


def _try_multiplication_visual(qtext: str, rng: random.Random) -> Optional[str]:
    """Generate an arrayGrid or dotGroups for multiplication questions."""
    m = _TIMES_RE.search(qtext)
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2))
    # Keep visuals reasonable
    if a > 9 or b > 9:
        return None
    if rng.random() < 0.6:
        return f'\\arrayGrid{{{a}}}{{{b}}}'
    else:
        return f'\\dotGroups{{{a}}}{{{b}}}'


def _try_angle_visual(qtext: str) -> Optional[str]:
    """Generate a simple TikZ angle diagram for angle questions."""
    m = _DEGREE_RE.search(qtext)
    if not m:
        return None
    deg = int(m.group(1) or m.group(2))
    if deg <= 0 or deg > 360:
        return None
    # Simple angle diagram — two rays with an arc
    return (
        '\\begin{center}\n'
        '\\begin{tikzpicture}\n'
        f'  \\draw[thick] (0,0) -- (2,0);\n'
        f'  \\draw[thick] (0,0) -- ({deg}:2);\n'
        f'  \\draw[->, funBlue, thick] (0.6,0) arc (0:{deg}:0.6);\n'
        f'  \\node[font=\\small\\sffamily] at ({deg/2}:0.95) '
        f'{{${deg}^\\circ$}};\n'
        '\\end{tikzpicture}\n'
        '\\end{center}'
    )


def _try_number_line_visual(qtext: str) -> Optional[str]:
    """Generate a numberLine for rounding/comparison questions."""
    # Extract numbers and try to build a sensible range
    nums = [int(n.replace(',', '')) for n in _DOLLAR_NUM_RE.findall(qtext)]
    nums = [n for n in nums if 0 <= n <= 1_000_000]
    if len(nums) < 2:
        return None
    lo, hi = min(nums), max(nums)
    if lo == hi or hi - lo > 1000:
        return None
    # Round lo down and hi up to nice interval
    span = hi - lo
    if span <= 10:
        step = 1
    elif span <= 50:
        step = 5
    elif span <= 100:
        step = 10
    elif span <= 500:
        step = 50
    else:
        step = 100
    nice_lo = (lo // step) * step
    nice_hi = ((hi // step) + 1) * step
    num_ticks = (nice_hi - nice_lo) // step
    if num_ticks > 12 or num_ticks < 2:
        return None
    return f'\\numberLine[{step}]{{{nice_lo}}}{{{nice_hi}}}'


# Map topic_id prefixes → visual generator functions.
# Each function receives (qtext, rng) or (qtext,) and returns LaTeX or None.
_VISUAL_GENERATORS = {
    # Fractions  (ch04-01 through ch04-06)
    'ch04-01': ('frac',),
    'ch04-02': ('frac',),
    'ch04-03': ('frac',),
    'ch04-04': ('frac',),
    'ch04-05': ('frac',),
    'ch04-06': ('frac',),
    'ch04-07': ('frac',),       # tenths/hundredths might have fractions
    'ch04-08': ('frac',),
    # Area
    'ch05-04': ('area',),
    # Perimeter
    'ch05-05': ('perimeter',),
    # Angles
    'ch05-07': ('angle',),
    'ch05-08': ('angle',),
    'ch05-09': ('angle',),
    # Multiplication (single-digit)
    'ch01-01': ('mult',),
    'ch01-02': ('mult',),
    'ch03-03': ('mult',),
    # Place value / rounding / comparing — number line
    'ch02-03': ('numline',),
    'ch02-05': ('numline',),
}


def _generate_visual(topic_id: str, qtext: str, rng: random.Random) -> Optional[str]:
    """Try to generate a visual for a question based on its topic."""
    generators = _VISUAL_GENERATORS.get(topic_id)
    if not generators:
        return None
    for gen_key in generators:
        if gen_key == 'frac':
            result = _try_fraction_visual(qtext, rng)
        elif gen_key == 'area':
            result = _try_area_visual(qtext)
        elif gen_key == 'perimeter':
            result = _try_perimeter_visual(qtext)
        elif gen_key == 'mult':
            result = _try_multiplication_visual(qtext, rng)
        elif gen_key == 'angle':
            result = _try_angle_visual(qtext)
        elif gen_key == 'numline':
            result = _try_number_line_visual(qtext)
        else:
            result = None
        if result:
            return result
    return None


def inject_visuals(
    questions: List[RawQuestion],
    rng: random.Random,
    target_fraction: float = 0.22,
) -> List[RawQuestion]:
    """Inject topic-aware TikZ visuals into a subset of test questions.

    Modifies question raw_blocks in-place by inserting a LaTeX visual
    command just before \\end{questionText}.

    Args:
        questions:       List of questions for one test.
        rng:             Random instance for reproducibility.
        target_fraction: Approximate fraction of questions to enhance (~22%).

    Returns:
        The same list (modified in place) for convenience.
    """
    # Identify candidates: questions whose topic has a visual generator.
    # Skip questions that already contain a visual (gmc/gsa types, or any
    # question whose text already includes TikZ / visual commands).
    _HAS_VISUAL_RE = re.compile(
        r'\\begin\{tikzpicture\}|\\arrayGrid|\\dotGroups|\\numberLine'
        r'|\\fractionBar|\\fractionCircle|\\numberLineFraction'
        r'|\\skipCountArc|\\barGraph|\\baseTenBlocks|\\areaGrid'
        r'|\\perimeterRect|\\factFamily|\\numberBond',
    )
    candidates = []
    for i, q in enumerate(questions):
        if q.type in ('gmc', 'gsa'):
            continue  # already has a hand-crafted visual
        if _HAS_VISUAL_RE.search(q.raw_block):
            continue  # already contains a visual command
        if q.topic_id in _VISUAL_GENERATORS:
            candidates.append(i)

    if not candidates:
        return questions

    # Select how many to enhance (target ~22%, at least 1 if any candidates)
    target_count = max(1, round(len(questions) * target_fraction))
    # Don't exceed available candidates
    target_count = min(target_count, len(candidates))

    # Spread across chapters: pick at most 2 per chapter
    by_chapter: Dict[str, List[int]] = {}
    for idx in candidates:
        ch = questions[idx].topic_id[:4]
        by_chapter.setdefault(ch, []).append(idx)

    selected: List[int] = []
    # Round-robin pick from chapters
    chapter_keys = sorted(by_chapter.keys())
    rng.shuffle(chapter_keys)
    ch_ptrs = {ch: 0 for ch in chapter_keys}
    per_ch_limit = 2

    while len(selected) < target_count:
        made_progress = False
        for ch in chapter_keys:
            if len(selected) >= target_count:
                break
            idxs = by_chapter[ch]
            ptr = ch_ptrs[ch]
            if ptr < len(idxs) and ptr < per_ch_limit:
                selected.append(idxs[ptr])
                ch_ptrs[ch] = ptr + 1
                made_progress = True
        if not made_progress:
            break

    # For each selected question, try to inject a visual
    injected = 0
    for idx in selected:
        q = questions[idx]
        qtext = _extract_question_text(q.raw_block)
        visual = _generate_visual(q.topic_id, qtext, rng)
        if visual:
            # Insert visual just before \end{questionText}
            new_block = q.raw_block.replace(
                r'\end{questionText}',
                f'\n\n{visual}\n\\end{{questionText}}',
                1,
            )
            questions[idx] = RawQuestion(
                id=q.id, type=q.type,
                raw_block=new_block, topic_id=q.topic_id,
            )
            injected += 1

    return questions


# ============================================================================
# OUTPUT — one .tex file per practice test
# ============================================================================

def format_test_file(
    test_num: int,
    state_name: str,
    questions: List[RawQuestion],
) -> str:
    """Format a single practice test file.

    Contains only a header comment and raw question blocks — no preamble,
    no \\documentclass, no \\begin{document}. Designed to be \\input'd
    into a main.tex later.
    """
    lines = []

    # Header comment
    lines.append(f"% Practice Test {test_num:02d} — {state_name} Edition")
    lines.append(f"% Questions: {len(questions)} "
                 f"({sum(1 for q in questions if q.type in ('mc', 'gmc'))} MC "
                 f"+ {sum(1 for q in questions if q.type in ('sa', 'gsa'))} SA)")
    lines.append(f"% Generated by scripts/generate_practice_tests.py")
    lines.append("")

    # Question blocks — verbatim from the question bank
    # Output in natural chapter order (MC and SA interleaved, like a real test).
    for q in questions:
        lines.append(q.raw_block)
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate practice test files for US state Grade 4 math editions.",
    )
    parser.add_argument(
        "--states",
        type=str,
        default=None,
        help="Comma-separated state slugs (default: all 50 states)",
    )
    parser.add_argument(
        "--num-tests",
        type=int,
        default=25,
        help="Number of practice tests per state (default: 25)",
    )
    parser.add_argument(
        "--questions-per-test",
        type=int,
        default=30,
        help="Number of questions per practice test (default: 30)",
    )
    parser.add_argument(
        "--max-topics",
        type=int,
        default=30,
        help="Maximum topics per state; extras are randomly dropped (default: 30)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="Random seed for reproducibility (default: 2026)",
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help="Override workspace root path (default: auto-detect)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Detect workspace
    if args.workspace:
        workspace = Path(args.workspace)
    else:
        workspace = find_workspace()
    print(f"Workspace: {workspace}")

    # Load configuration from YAML
    config = load_config(workspace)

    # Determine which states to process
    if args.states:
        state_slugs = [s.strip().lower() for s in args.states.split(",")]
        for s in state_slugs:
            if s not in config.state_display_names:
                print(f"ERROR: Unknown state slug '{s}'")
                sys.exit(1)
    else:
        states_input = prompt_states(config.all_state_slugs)
        if states_input is None:
            state_slugs = config.all_state_slugs
        else:
            state_slugs = [s.strip().lower() for s in states_input.split(",")]

    # Load question banks
    print(f"\nLoading question banks...")
    core_banks, modified_banks = load_all_question_banks(workspace)
    print(f"  Total: {len(core_banks)} core/additional + "
          f"{len(modified_banks)} modified topic banks loaded")

    if not core_banks:
        print("ERROR: No question banks found. "
              "Create .tex files in tests_questions_bank/topics/")
        sys.exit(1)

    # Generate tests for each state
    print(f"\nGenerating {args.num_tests} practice tests "
          f"for {len(state_slugs)} state(s)...")

    total_files = 0
    for state_slug in state_slugs:
        state_name = config.state_display_names[state_slug]

        # Build state-specific question banks (core + modified swaps)
        question_banks = build_state_banks(
            core_banks, modified_banks, state_slug, config,
        )

        # Get this state's topic list
        state_topics = get_state_topics(state_slug, config)

        # Filter to topics with available question banks
        available = [t for t in state_topics if t in question_banks]
        missing = [t for t in state_topics if t not in question_banks]

        print(f"\n  {state_name}: {len(available)} topics with banks, "
              f"{len(missing)} missing")

        if not available:
            print(f"    SKIPPED — no question banks available")
            continue

        # Determine state-specific topic IDs (additional + modified)
        state_specific_ids = (
            set(config.state_additional.get(state_slug, []))
            | set(config.state_modified.get(state_slug, {}))
        )

        # Cap topics when state has more than max_topics.
        # State-specific topics get 2x selection weight (not guaranteed).
        rng = random.Random(args.seed)
        if len(available) > args.max_topics:
            available = weighted_topic_selection(
                available, state_specific_ids,
                args.max_topics, rng,
            )
            priority_in = len([t for t in available if t in state_specific_ids])
            print(f"    Capped: selected {args.max_topics} of "
                  f"{len(state_topics)} topics "
                  f"({priority_in} state-specific selected)")

        # Check if enough unique questions exist
        total_available = sum(len(question_banks[t]) for t in available)
        total_needed = args.num_tests * args.questions_per_test
        if total_needed > total_available:
            max_possible = total_available // args.questions_per_test
            print(f"    WARNING: Need {total_needed} unique questions but only "
                  f"{total_available} available. Can generate at most "
                  f"{max_possible} full tests.")

        # Generate tests
        tests = generate_practice_tests(
            available, question_banks, args.num_tests,
            args.questions_per_test, rng,
        )

        # Write one file per test (clean old files first)
        output_dir = workspace / "practice_tests" / state_slug
        output_dir.mkdir(parents=True, exist_ok=True)
        for old_file in output_dir.glob("practice_test_*.tex"):
            old_file.unlink()

        for test_num, test_questions in enumerate(tests, 1):
            # Inject topic-aware visuals into ~22% of questions
            inject_visuals(test_questions, random.Random(args.seed + test_num))
            content = format_test_file(test_num, state_name, test_questions)
            filename = f"practice_test_{test_num:02d}.tex"
            output_path = output_dir / filename
            output_path.write_text(content, encoding="utf-8")
            total_files += 1

        print(f"    Written {len(tests)} files to practice_tests/{state_slug}/")

    print(f"\nDone! Generated {total_files} practice test file(s).")


if __name__ == "__main__":
    main()
