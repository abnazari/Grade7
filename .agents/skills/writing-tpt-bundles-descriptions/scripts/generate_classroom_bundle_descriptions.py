#!/usr/bin/env python3
"""Generate Classroom Bundle TPT HTML descriptions for all states."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Dict, Iterable, List

import get_bundle_facts as facts

BUNDLE_TYPE = "classroom_bundle"
BUNDLE_COMMENT = "Step-by-Step + Workbook + Quizzes + Worksheets + 3+5+7+10 Practice Tests (8 books)"
FOOTER = """<p></p>★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★<p></p>

<p>
  Looking for more <b>Grade 7 Math</b> resources? Visit my
  <a href=\"https://www.teacherspayteachers.com/store/viewmath\" target=\"_blank\"><b>TPT store</b></a>
  for engaging, classroom-ready materials from <b>View Math</b> — a math education company dedicated to helping students succeed.
</p>

<p>
  Explore more teaching tools and learning materials at
  <a href=\"https://www.viewmath.com\" target=\"_blank\"><b>ViewMath.com</b></a>.
</p>

<p>
  Questions or suggestions? Reach out at
  <a href=\"mailto:dr.nazari@viewmath.com\">dr.nazari@viewmath.com</a>.
</p>

<p>
  <b>Follow me</b> to catch new releases — all <b>50% off</b> for the first 24 hours!
</p>

<p>
  <b>– Dr. A. Nazari</b>
</p>
"""

WHATS_HEADINGS = [
    "What Comes in the {state} Set",
    "Everything in This {state} Bundle",
    "The 8 Books in the {state} Bundle",
    "What You Get for {state} Math",
    "Inside the {state} Classroom Bundle",
    "Books Included for {state}",
]

HOW_HEADINGS = [
    "How the {state} Books Split the Work",
    "How Each {state} Book Pulls Its Weight",
    "How This {state} System Works Day to Day",
    "How the Pieces Fit for {state} Math",
    "How to Use the {state} Bundle Across the Week",
    "How the {state} Resources Work Together",
]

CHAPTER_HEADINGS = [
    "{topics} Topics Across {chapters} {state} Chapters",
    "What the {state} Books Cover",
    "The {state} Math Scope at a Glance",
    "Full {state} Grade 7 Coverage",
    "Your {state} Topic Map",
    "Chapter Coverage for {state}",
]

CURRICULUM_HEADINGS = [
    "Built for {state} Standards",
    "Written for {state} Math",
    "Why This Fits {state}",
    "Aligned to {state} Expectations",
    "Made for {state} Grade 7 Math",
    "The {state} Standards Match",
]

USE_CASE_HEADINGS = [
    "Where This Bundle Helps in {state}",
    "Who Uses This Bundle in {state}",
    "Strong Fits for {state} Classrooms",
    "When the {state} Set Earns Its Spot",
    "Ways to Use It in {state}",
    "Good Uses for the {state} Bundle",
]

QUALITY_HEADINGS = [
    "What Shows Up in Every {state} Book",
    "What You Can Count on in Every Book",
    "Shared Features Across the {state} Set",
    "What Every Book Includes for {state}",
    "Across All 8 {state} Books",
    "Common Features in the Whole {state} Bundle",
]

CROSS_HEADINGS = [
    "If You Want More Than the {state} Classroom Set",
    "Other {state} Resources in the Series",
    "Still Need a Few Extras for {state}?",
    "Want to Round Out Your {state} Shelf?",
    "More {state} Math Books to Pair With This",
    "If You Need Even More for {state}",
]

OPENING_TEMPLATES = [
    "This 8-book bundle gives you daily teaching tools for {state} Grade 7 math: Step-by-Step lessons, Workbook practice, Quizzes, Worksheets, and 25 unique, non-overlapping full-length tests with 750 total questions.{exam_sentence}",
    "If you want one set that handles instruction, practice, quick checks, flexible printables, and serious test prep for {state} Grade 7 math, this is it. You get 8 books and 25 different full-length tests, with no repeated questions across the 750-question set.{exam_sentence}",
    "This bundle is built for teachers who need more than one kind of math resource. For {state} Grade 7, it brings together 8 books for teaching, independent work, assessment, and 25 unique, non-overlapping tests totaling 750 questions.{exam_sentence}",
    "Here is the full classroom toolkit for {state} Grade 7 math. It combines teaching support, practice, quizzes, worksheets, and 25 full-length tests that stay unique across all four practice test editions, for 750 questions altogether.{exam_sentence}",
    "This classroom bundle covers the whole routine for {state} Grade 7 math: teach it, practice it, check it, assign it, and test it. The four practice test books alone give you 25 unique tests and 750 questions without any overlap.{exam_sentence}",
    "For {state} Grade 7 math, this set keeps the day-to-day work practical. You get 8 books for instruction, follow-up practice, quick assessments, flexible worksheets, and 25 different full-length tests with 750 total questions.{exam_sentence}",
]

PRACTICE_REINFORCEMENTS = [
    "The practice test books are not recycled versions of each other. All 25 tests are different, non-overlapping, and together they give you 750 questions to work with.",
    "Those four test books are meant to last. Every edition has different questions, so you get 25 unique tests and 750 total questions with zero repeat problems.",
    "The test-prep portion is genuinely broad: 25 separate full-length tests, 750 questions, and no duplicated questions from one edition to the next.",
    "You are not getting the same test in different packaging. The 3, 5, 7, and 10 test editions are all different, for 25 unique tests and 750 questions in total.",
    "Across the four practice test books, the questions do not repeat. That gives you 25 unique tests and 750 questions for ongoing test prep.",
    "All four practice test editions stay distinct, so the bundle gives you 25 non-overlapping tests and 750 total questions instead of repeated practice.",
]

STEP_PARAGRAPHS = [
    "The <b>Step-by-Step Guide</b> handles direct teaching. Each problem type is broken into clear numbered moves, with road maps up front and common mistakes called out before students get stuck.",
    "Start with the <b>Step-by-Step Guide</b> when students need structure. It lays out each problem type in numbered steps, adds road maps at the start of topics, and points out the mistakes that usually cause trouble.",
    "Use the <b>Step-by-Step Guide</b> for instruction and reteaching. The format is plain on purpose: Step 1, Step 2, Step 3, plus quick road maps and reminders about common errors.",
]

WORKBOOK_PARAGRAPHS = [
    "The <b>Workbook</b> is where students put that teaching to work. The practice moves from simpler questions into more demanding ones and mixes formats like fill-in, multiple choice, short answer, and word problems.",
    "After the teaching piece, the <b>Workbook</b> gives students room to build fluency. The problems are organized by topic and progress from easier work to more challenging formats.",
    "The <b>Workbook</b> covers the practice load. It is topic-based, moves from easy to challenging, and gives you a mix of question types instead of one repetitive format.",
]

QUIZ_PARAGRAPHS = [
    "The <b>Quizzes</b> keep assessment light and frequent. They are short enough for exit tickets, bell-ringers, or weekly checks, and the scoring guide helps you see who needs another pass.",
    "The <b>Quizzes</b> give you fast checkpoints without taking over the lesson. They work well for quick progress checks, and the scoring guide makes follow-up decisions easier.",
    "Use the <b>Quizzes</b> when you want quick data. Each one is short, topic-focused, and easy to slide into the week as a bell-ringer, exit ticket, or small assessment.",
]

WORKSHEET_PARAGRAPHS = [
    "The <b>Worksheets</b> give you the flexible pages. Each one stands alone, so you can pull a sheet for homework, centers, small-group work, a sub plan, or a quick extra assignment.",
    "The <b>Worksheets</b> are the easy-grab option. They do not depend on sequence, which makes them useful for homework, station work, review packets, or emergency plans.",
    "The <b>Worksheets</b> are built for flexibility. Because each page works on its own, you can drop one into centers, homework, intervention, or no-prep substitute work.",
]

TEST_PARAGRAPHS = [
    "The <b>Practice Tests</b> cover the longer assessment piece. You can run weekly test-prep sessions across the year because the four editions stay separate from each other instead of recycling the same questions.",
    "The <b>Practice Tests</b> take care of exam practice. With 25 full-length tests and no overlap from one edition to the next, you can keep testing without running out of fresh material.",
    "The <b>Practice Tests</b> are there for the serious prep stage. They give you full-length assessments, detailed answer explanations, and enough unique material to keep test practice going for months.",
]

CURRICULUM_WITH_EXAM = [
    "Every book in this bundle is aligned to the <b>{curriculum_name} ({curriculum_acronym})</b>. The practice test side is also written with the <b>{exam_name} ({exam_acronym})</b> in view, so this reads like a {state}-specific resource instead of a generic national one.",
    "This bundle matches the <b>{curriculum_name} ({curriculum_acronym})</b> and supports the content students are expected to handle on the <b>{exam_name} ({exam_acronym})</b>. It is written for {state}, not just relabeled for {state}.",
    "The alignment is state-specific from the start. The books follow the <b>{curriculum_name} ({curriculum_acronym})</b>, and the test-prep pieces are built around the expectations of the <b>{exam_name} ({exam_acronym})</b>.",
]

CURRICULUM_NO_EXAM = [
    "Every book in this bundle is aligned to the <b>{curriculum_name} ({curriculum_acronym})</b>. This is written for {state} Grade 7 math specifically, not as a generic one-size-fits-all resource.",
    "The bundle is built around the <b>{curriculum_name} ({curriculum_acronym})</b>, so the scope and sequence match what {state} students are expected to learn.",
    "This set follows the <b>{curriculum_name} ({curriculum_acronym})</b> and stays grounded in {state} expectations all the way through the bundle.",
]

USE_CASE_VARIANTS = [
    [
        "full-year instruction, with Step-by-Step for teaching, Workbook pages for practice, Quizzes for checks, and the test books for longer assessment",
        "differentiated instruction, especially when some students need more structure and others need independent pages",
        "math centers, where you can rotate students through worksheets, workbook practice, and quick quizzes",
        "homeschool learning that needs built-in teaching support plus 25 unique tests",
        "tutoring programs that want instruction, practice, and assessment in one place",
        "sub plans, because a worksheet or quiz can cover a block without extra prep",
    ],
    [
        "daily classroom use, since the books split teaching, practice, checking, and test prep into separate tools",
        "small-group reteaching, where the Step-by-Step format gives struggling learners a clearer path",
        "independent work time, using worksheets and workbook pages without building a new packet from scratch",
        "home support or homeschool routines that benefit from answer keys and a clear sequence of materials",
        "test-prep cycles that need a lot of fresh practice instead of the same test repeated",
        "emergency planning, when you need a no-fuss page or quiz ready to go",
    ],
    [
        "teachers who want one bundle to cover direct teaching, follow-up practice, short checks, and bigger assessments",
        "intervention blocks, where step-by-step modeling and flexible worksheets both matter",
        "station rotations, mixing workbook pages, quizzes, and worksheets across the week",
        "families teaching at home who want structure without having to assemble materials from multiple places",
        "tutors who need a clean path from explanation to practice to full test simulation",
        "backup lessons and sub days, thanks to the standalone worksheet and quiz options",
    ],
]

QUALITY_VARIANTS = [
    [
        "full-color, kid-friendly pages with illustrations, diagrams, and the friendly owl mascot throughout the series",
        "complete answer keys with explanations, so checking work and reviewing mistakes takes less time",
        "print-ready files that you can download, print, and put to work right away",
    ],
    [
        "bright, student-friendly design with visuals and the owl mascot to keep the pages approachable",
        "answer keys for every book, including explanation support where students need it",
        "ready-to-print materials that do not need extra formatting before you use them",
    ],
    [
        "colorful layouts with diagrams, illustrations, and a familiar owl guide across the bundle",
        "built-in answer keys and explanations to make review simpler for teachers and families",
        "printable files that are ready to use as soon as you download them",
    ],
]

CROSS_INTROS = [
    "This bundle already covers instruction, practice, assessment, and testing. If you want to extend it, these are the next books to look at:",
    "There is a lot here already, but these books can round out the series if you want more review or enrichment:",
    "If you want to add a few more kinds of support around this bundle, start with these titles:",
]

CROSS_SELL_VARIANTS: Dict[str, List[str]] = {
    "Study Guide": [
        "a concise review book with key ideas, worked examples, and quick practice",
        "short, focused concept review with essential examples and quick checks",
        "compact review for the core ideas students need to revisit",
    ],
    "Math in 30 Days": [
        "a day-by-day review plan that walks through the full curriculum in one month",
        "a 30-day schedule for students who need a structured review path",
        "a month-long review plan when you want the curriculum broken into daily pieces",
    ],
    "Puzzles & Brain Teasers": [
        "curriculum-aligned puzzles and games that add enrichment without dropping the math",
        "extra challenge pages that keep practice lively while staying tied to standards",
        "math games and puzzle-style activities for students who need more variety",
    ],
}

CLOSINGS = [
    (
        "It is a practical way to cover teaching, practice, quick checks, flexible assignments, and test prep without juggling separate resources.",
        "Choose the Classroom Bundle when you want the whole {state} Grade 7 math routine in one place.",
    ),
    (
        "This bundle keeps the moving parts of {state} math instruction together instead of scattering them across different products.",
        "Pick up the Classroom Bundle if you want one set that can carry the year.",
    ),
    (
        "You get a tool for direct instruction, a tool for practice, a tool for quick data, a tool for flexible assignments, and enough unique tests to stay fresh.",
        "Add the Classroom Bundle when you want your {state} math resources to feel complete.",
    ),
    (
        "For day-to-day teaching and longer test prep, this bundle does the heavy lifting.",
        "Get the Classroom Bundle and set up {state} Grade 7 math with less patchwork.",
    ),
]

ORDERS = [
    ["whats", "how", "chapters", "curriculum", "use_cases", "quality", "cross_sell"],
    ["curriculum", "whats", "use_cases", "how", "chapters", "quality", "cross_sell"],
    ["whats", "curriculum", "how", "quality", "chapters", "use_cases", "cross_sell"],
    ["whats", "how", "use_cases", "curriculum", "chapters", "cross_sell", "quality"],
    ["curriculum", "whats", "how", "chapters", "cross_sell", "use_cases", "quality"],
]


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def normalize_latex_text(text: str) -> str:
    """Convert the few LaTeX escapes used in config data into plain text."""
    return text.replace("\&", "&")


def cycle_pick(options: List[str], idx: int, step: int = 1) -> str:
    return options[(idx * step) % len(options)]


def join_paragraph(lines: Iterable[str]) -> str:
    return "\n\n".join(lines)


def format_heading(template: str, state_name: str, total_topics: int, total_chapters: int) -> str:
    return template.format(
        state=state_name,
        topics=total_topics,
        chapters=total_chapters,
    )


def bundle_comment_title(state_name: str, exam_acronym: str) -> str:
    prefix = f"{state_name} {exam_acronym}".strip()
    return f"{prefix} Grade 7 Math Classroom Bundle: Step-by-Step, Workbook, Quizzes, Worksheets & 25 Tests"


def get_book_li(book_name: str, text: str) -> str:
    return f"  <li>✅ <b>{esc(book_name)}</b> - {esc(text)}</li>"


def render_whats_section(state_name: str, idx: int) -> str:
    heading = format_heading(cycle_pick(WHATS_HEADINGS, idx, 3), state_name, 0, 0)
    book_texts = {
        "Step-by-Step Guide": [
            "numbered directions for each problem type, plus road maps and common-mistake alerts",
            "clear step-by-step teaching for each problem type, with road maps and error warnings",
            "structured teaching pages with numbered steps, road maps, and mistake reminders",
        ][idx % 3],
        "Workbook": [
            "topic-based practice that moves from easier work to more challenging problems",
            "hundreds of practice problems organized by topic and level of difficulty",
            "scaffolded practice pages arranged by topic, from straightforward to challenging",
        ][(idx + 1) % 3],
        "Quizzes": [
            "one 15-minute quiz per topic with an answer key and scoring guide",
            "short topic quizzes that make quick checks easy and come with scoring support",
            "fast topic-based quizzes with answer keys and simple scoring guidance",
        ][(idx + 2) % 3],
        "Worksheets": [
            "standalone printable pages you can use in any order",
            "flexible printable worksheets for any topic, with no sequence required",
            "independent practice sheets that work as homework, centers, or review",
        ][idx % 3],
        "3 Practice Tests": [
            "three full-length tests with detailed answer explanations",
            "three unique full-length tests for early test-prep rounds",
            "three separate practice tests with answer support",
        ][(idx + 1) % 3],
        "5 Practice Tests": [
            "five more full-length tests for additional practice",
            "five extra full-length tests that expand the test-prep pool",
            "five separate practice tests for continued review",
        ][(idx + 2) % 3],
        "7 Practice Tests": [
            "seven full-length tests with detailed answers",
            "seven additional tests that keep the practice fresh",
            "seven more unique tests with answer explanations",
        ][idx % 3],
        "10 Practice Tests": [
            "ten full-length tests with answer explanations",
            "ten more full-length tests to finish out the test-prep set",
            "ten separate practice tests with detailed answer support",
        ][(idx + 1) % 3],
    }

    lines = [f"<p></p><b>{esc(heading)}</b>", "", "<ul>"]
    for book_name in [
        "Step-by-Step Guide",
        "Workbook",
        "Quizzes",
        "Worksheets",
        "3 Practice Tests",
        "5 Practice Tests",
        "7 Practice Tests",
        "10 Practice Tests",
    ]:
        lines.append(get_book_li(book_name, book_texts[book_name]))
    lines.append("</ul>")
    reinforcement = cycle_pick(PRACTICE_REINFORCEMENTS, idx, 5)
    lines.append("")
    lines.append(f"<p>{esc(reinforcement)}</p>")
    return join_paragraph(lines)


def render_how_section(state_name: str, idx: int) -> str:
    heading = format_heading(cycle_pick(HOW_HEADINGS, idx, 5), state_name, 0, 0)
    lines = [f"<p></p><b>{esc(heading)}</b>"]
    lines.append(f"<p>{cycle_pick(STEP_PARAGRAPHS, idx, 2)}</p>")
    lines.append(f"<p>{cycle_pick(WORKBOOK_PARAGRAPHS, idx, 3)}</p>")
    lines.append(f"<p>{cycle_pick(QUIZ_PARAGRAPHS, idx, 4)}</p>")
    lines.append(f"<p>{cycle_pick(WORKSHEET_PARAGRAPHS, idx, 5)}</p>")
    lines.append(f"<p>{cycle_pick(TEST_PARAGRAPHS, idx, 6)}</p>")
    return "\n\n".join(lines)


def render_chapters_section(state_name: str, idx: int, chapter_summaries: List[tuple], total_topics: int) -> str:
    heading = format_heading(cycle_pick(CHAPTER_HEADINGS, idx, 2), state_name, total_topics, len(chapter_summaries))
    lines = [f"<p></p><b>{esc(heading)}</b>"]
    lines.append(
        f"<p>Across the bundle, you get {total_topics} topics organized in a consistent order, so teaching, practice, quizzes, worksheets, and tests all point at the same content.</p>"
    )
    lines.append("<ul>")
    for ch_num, ch_title, ch_count in chapter_summaries:
        topic_word = "topic" if ch_count == 1 else "topics"
        plain_title = normalize_latex_text(ch_title)
        lines.append(
            f"  <li><b>Chapter {ch_num}: {esc(plain_title)}</b> - {ch_count} {topic_word}</li>"
        )
    lines.append("</ul>")
    return "\n\n".join(lines)


def render_curriculum_section(state_name: str, idx: int, curriculum_name: str, curriculum_acronym: str, exam_name: str, exam_acronym: str) -> str:
    heading = format_heading(cycle_pick(CURRICULUM_HEADINGS, idx, 4), state_name, 0, 0)
    lines = [f"<p></p><b>{esc(heading)}</b>"]
    if exam_name and exam_acronym:
        template = cycle_pick(CURRICULUM_WITH_EXAM, idx, 2)
        paragraph = template.format(
            state=state_name,
            curriculum_name=esc(curriculum_name),
            curriculum_acronym=esc(curriculum_acronym),
            exam_name=esc(exam_name),
            exam_acronym=esc(exam_acronym),
        )
    else:
        template = cycle_pick(CURRICULUM_NO_EXAM, idx, 2)
        paragraph = template.format(
            state=state_name,
            curriculum_name=esc(curriculum_name),
            curriculum_acronym=esc(curriculum_acronym),
        )
    lines.append(f"<p>{paragraph}</p>")
    return "\n\n".join(lines)


def render_use_cases_section(state_name: str, idx: int) -> str:
    heading = format_heading(cycle_pick(USE_CASE_HEADINGS, idx, 3), state_name, 0, 0)
    variant = USE_CASE_VARIANTS[idx % len(USE_CASE_VARIANTS)]
    lines = [f"<p></p><b>{esc(heading)}</b>", "", "<ul>"]
    for item in variant:
        lines.append(f"  <li>✅ {esc(item)}</li>")
    lines.append("</ul>")
    return join_paragraph(lines)


def render_quality_section(state_name: str, idx: int) -> str:
    heading = format_heading(cycle_pick(QUALITY_HEADINGS, idx, 5), state_name, 0, 0)
    variant = QUALITY_VARIANTS[idx % len(QUALITY_VARIANTS)]
    lines = [f"<p></p><b>{esc(heading)}</b>", "", "<ul>"]
    for item in variant:
        lines.append(f"  <li>✅ {esc(item)}</li>")
    lines.append("</ul>")
    return join_paragraph(lines)


def render_cross_sell_section(state_name: str, idx: int) -> str:
    heading = format_heading(cycle_pick(CROSS_HEADINGS, idx, 2), state_name, 0, 0)
    intro = cycle_pick(CROSS_INTROS, idx, 4)
    lines = [f"<p></p><b>{esc(heading)}</b>", "", f"<p>{esc(intro)}</p>", "", "<ul>"]
    cross_items = [
        ("Study Guide", CROSS_SELL_VARIANTS["Study Guide"][idx % 3]),
        ("Math in 30 Days", CROSS_SELL_VARIANTS["Math in 30 Days"][(idx + 1) % 3]),
        ("Puzzles & Brain Teasers", CROSS_SELL_VARIANTS["Puzzles & Brain Teasers"][(idx + 2) % 3]),
    ]
    for name, desc in cross_items:
        lines.append(f"  <li>✅ <b>{esc(name)}</b> - {esc(desc)}</li>")
    lines.append("</ul>")
    return join_paragraph(lines)


def render_closing(state_name: str, idx: int) -> str:
    summary, cta = CLOSINGS[idx % len(CLOSINGS)]
    return "\n\n".join([
        f"<p>{esc(summary.format(state=state_name))}</p>",
        f"<p><b>{esc(cta.format(state=state_name))}</b></p>",
    ])


def render_description(state_slug: str, idx: int, config, exams, curriculums) -> str:
    state_name = config.state_display_names[state_slug]
    bundle_title = facts.bundle_tpt_title(BUNDLE_TYPE, state_slug, state_name)
    chapter_summaries, total_topics = facts.build_chapter_summaries(state_slug, config)
    curriculum = curriculums.get(state_slug, {})
    exam = exams.get(state_slug, {})
    exam_name = exam.get("exam_name", "")
    exam_acronym = exam.get("exam_acronym", "")
    curriculum_name = curriculum.get("curriculum_name", "")
    curriculum_acronym = curriculum.get("curriculum_acronym", "")

    if exam_name and exam_acronym:
        exam_sentence = f" It is also built with the {exam_name} ({exam_acronym}) in mind."
    else:
        exam_sentence = ""

    opening = cycle_pick(OPENING_TEMPLATES, idx, 4).format(
        state=state_name,
        exam_sentence=exam_sentence,
    )

    sections = {
        "whats": render_whats_section(state_name, idx),
        "how": render_how_section(state_name, idx),
        "chapters": render_chapters_section(state_name, idx, chapter_summaries, total_topics),
        "curriculum": render_curriculum_section(
            state_name,
            idx,
            curriculum_name,
            curriculum_acronym,
            exam_name,
            exam_acronym,
        ),
        "use_cases": render_use_cases_section(state_name, idx),
        "quality": render_quality_section(state_name, idx),
        "cross_sell": render_cross_sell_section(state_name, idx),
    }

    ordered_sections = [sections[name] for name in ORDERS[idx % len(ORDERS)]]
    top_comment = bundle_comment_title(state_name, exam_acronym)

    parts = [
        f"<!-- {esc(top_comment)} -->",
        f"<!-- Bundle: {esc(BUNDLE_COMMENT)} -->",
        f"<!-- TPT Title: {esc(bundle_title)} -->",
        f"<p>{esc(opening)}</p>",
        *ordered_sections,
        render_closing(state_name, idx),
        FOOTER.rstrip(),
    ]
    return "\n\n".join(parts) + "\n"


def main() -> None:
    config = facts.load_config(facts.WORKSPACE)
    exams = facts.load_state_exams()
    curriculums = facts.load_state_curriculums()
    out_dir = facts.WORKSPACE / "final_output" / "bundles" / BUNDLE_TYPE
    out_dir.mkdir(parents=True, exist_ok=True)

    for idx, state_slug in enumerate(config.all_state_slugs):
        html_text = render_description(state_slug, idx, config, exams, curriculums)
        out_path = out_dir / f"{state_slug}_tpt_bundle.html"
        out_path.write_text(html_text, encoding="utf-8")
        print(out_path.relative_to(facts.WORKSPACE))


if __name__ == "__main__":
    main()
