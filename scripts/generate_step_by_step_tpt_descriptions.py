#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import subprocess
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
TITLES_PATH = WORKSPACE / "titles.json"
FACTS_SCRIPT = WORKSPACE / ".agents" / "skills" / "writing-tpt-description" / "scripts" / "get_book_facts.py"
OUTPUT_DIR = WORKSPACE / "final_output" / "step_by_step"
BOOK_TYPE = "step_by_step"
TODAY = date.today().isoformat()

FOOTER = """★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

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

FEATURE_REPHRASES = [
    "Numbered directions show students exactly what to do for each kind of Grade 7 problem.",
    "Topic road maps help students see the path from the first move to the final answer.",
    "Worked examples walk through each instruction with a full problem, not just a short hint.",
    "Common errors are pointed out early so students can catch them before they repeat them.",
    "Guided practice follows the same procedure that was just taught, which makes the routine stick.",
    "Visual layouts and diagrams break the process into smaller, easier-to-follow parts.",
]

OPENING_HEADINGS = [
    "A Clear Step-by-Step Math Guide for {state}",
    "Procedural Help for {state} Grade 7 Math",
    "A Beginner-Friendly {state} Math Guide",
    "Step-by-Step Support for {state} Grade 7",
    "A Practical {state} Grade 7 Problem-Solving Guide",
    "Clear Directions for {state} Grade 7 Math",
    "A Guided Way Through {state} Grade 7 Math",
    "Structured Math Help for {state} Students",
]

OPENING_LINES = [
    "<b>{title}</b> <i>{subtitle}</i> gives students a direct path through Grade 7 math with numbered procedures they can actually follow.",
    "<b>{title}</b> <i>{subtitle}</i> is built for students who understand more when every problem type is broken into clear, ordered moves.",
    "<b>{title}</b> <i>{subtitle}</i> keeps Grade 7 math from feeling scattered by showing students what to do first, next, and last.",
    "<b>{title}</b> <i>{subtitle}</i> helps {state} students work through Grade 7 math one step at a time instead of guessing where to begin.",
]

FEATURE_HEADINGS = [
    "What You Get in the {state} Edition",
    "What Makes This {state} Guide Useful",
    "Inside This Step-by-Step Book for {state}",
    "A Quick Look Inside the {state} Guide",
    "What Students Will Find in This {state} Book",
    "What Is Included for {state} Grade 7 Math",
    "What This {state} Step-by-Step Guide Adds",
    "Why This Format Helps in {state}",
]

CHAPTER_HEADINGS = [
    "All {topics} Topics in the {state} Book",
    "What This {state} Step-by-Step Guide Covers",
    "The Full Topic Breakdown for {state}",
    "How the {state} Edition Is Organized",
    "Every Chapter Included for {state}",
    "The {state} Coverage Snapshot",
    "What Students Work Through in {state}",
    "The Chapter Map for {state}",
]

CURRICULUM_HEADINGS = [
    "Built for {state} Standards",
    "Made to Match {state}",
    "Why This Fits {state} Math",
    "A State-Specific Guide for {state}",
    "Written Around {state} Expectations",
    "How This Lines Up in {state}",
    "The Standards Match for {state}",
    "Created for {state} Grade 7 Math",
]

CURRICULUM_LINES = [
    "This book follows <b>{curriculum_name} ({curriculum_acronym})</b>, so it is built for {state} classrooms rather than a generic middle school sequence.",
    "Because it is organized around <b>{curriculum_name} ({curriculum_acronym})</b>, the examples and procedures stay tied to what {state} students are actually expected to learn.",
    "It matches <b>{curriculum_name} ({curriculum_acronym})</b>, which makes it a {state}-specific support tool instead of a broad one-size-fits-all supplement.",
    "The instruction is aligned to <b>{curriculum_name} ({curriculum_acronym})</b>, so the step order and problem types make sense for {state} Grade 7 math.",
]

EXAM_HEADINGS = [
    "Helpful Before the {exam_acronym}",
    "Also Useful for {exam_acronym} Prep",
    "When {exam_acronym} Review Starts",
    "A Straightforward Way to Review for the {exam}",
    "Built-In Support for {exam_acronym}",
    "This Helps with {exam_acronym} Too",
    "Procedural Review Before {exam_acronym}",
    "Extra Practice Before the {exam}",
]

EXAM_LINES = [
    "If students are preparing for <b>{exam_name} ({exam_acronym})</b>, this guide helps them rehearse the procedures behind the skills they need to show.",
    "It also works well before <b>{exam_name} ({exam_acronym})</b> because students can review the process for each problem type without getting lost in long explanations.",
    "For <b>{exam_name} ({exam_acronym})</b> prep, this book gives students a way to revisit methods step by step before they move into full-length practice tests.",
    "When <b>{exam_name} ({exam_acronym})</b> is coming up, this resource helps students tighten up the procedures that often slow them down on test day.",
]

USE_CASE_HEADINGS = [
    "Who This Works Well For in {state}",
    "Practical Ways to Use This in {state}",
    "Where This Guide Fits Best in {state}",
    "Good Uses for the {state} Edition",
    "How Teachers and Families Use This in {state}",
    "Who Gets the Most from This {state} Guide",
    "When This Book Helps Most in {state}",
    "Easy Ways to Put This to Work in {state}",
]

SERIES_HEADINGS = [
    "More {state} Grade 7 Math Resources",
    "If You Want More Than Step-by-Step Help in {state}",
    "Other {state} Books in the Series",
    "What to Pair with This {state} Guide",
    "Keep Building Your {state} Math Set",
    "More Options for {state} Grade 7 Math",
    "Need a Full {state} Series?",
    "Other {state} Titles to Add Next",
]

CLOSING_HEADINGS = [
    "A Simple Next Step for {state} Math",
    "Clearer Problem Solving for {state}",
    "One More Way to Support {state} Students",
    "A Practical Finish for {state} Review",
    "Why This Helps in {state}",
    "A Confident Choice for {state} Grade 7",
    "Keep {state} Math Practice Moving",
    "An Easy Win for {state} Families and Teachers",
]

CLOSING_LINES = [
    (
        "Students do better when they know how to begin, what comes next, and how to check their work at the end.",
        "<b>Add this {state} step-by-step guide when you want Grade 7 math to feel more manageable and more independent.</b>",
    ),
    (
        "This book gives students a repeatable process they can return to across the full course.",
        "<b>Choose the {state} edition if you want a clear, state-specific guide that helps students solve problems with less guesswork.</b>",
    ),
    (
        "It keeps math support concrete, organized, and easy to use in real classrooms and real homes.",
        "<b>Use this {state} guide when your students need more than answers and need to see the actual steps.</b>",
    ),
    (
        "The goal is simple: less freezing, less guessing, and more confident problem solving.",
        "<b>Pick up the {state} edition to give your students a step-by-step path through Grade 7 math.</b>",
    ),
]


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def load_titles() -> list[dict]:
    return json.loads(TITLES_PATH.read_text(encoding="utf-8"))


def load_entries() -> list[dict]:
    entries = [entry for entry in load_titles() if entry.get("book_type") == BOOK_TYPE]
    entries.sort(key=lambda entry: entry["state_slug"])
    if len(entries) != 50:
        raise SystemExit(f"Expected 50 {BOOK_TYPE} entries, found {len(entries)}")
    return entries


def run_facts(state_slug: str) -> str:
    result = subprocess.run(
        [str(WORKSPACE / ".venv" / "bin" / "python"), str(FACTS_SCRIPT), BOOK_TYPE, state_slug],
        capture_output=True,
        text=True,
        cwd=WORKSPACE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get facts for {state_slug}: {result.stderr.strip()}")
    return result.stdout


def extract_field(text: str, label: str) -> str:
    pattern = rf"^{re.escape(label)}:\s*(.*)$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_section(text: str, section_name: str) -> str:
    pattern = rf"--- {re.escape(section_name)}.*?---\n(.*?)(?:\n--- |\n=+\nEND OF FACTS)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_bullets(section_text: str) -> list[str]:
    bullets = []
    for line in section_text.splitlines():
        line = line.strip()
        if line.startswith("•"):
            bullets.append(line[1:].strip())
    return bullets


def parse_chapters(section_text: str) -> list[tuple[str, str]]:
    chapters = []
    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if line.startswith("Chapter ") and " — " in line:
            left, right = line.split(" — ", 1)
            chapters.append((left.strip(), right.strip()))
    return chapters


def parse_cross_sell_item(item: str) -> tuple[str, str]:
    if " — " in item:
        name, desc = item.split(" — ", 1)
        return name.strip(), desc.strip()
    return item.strip(), ""


def section_heading(text: str) -> str:
    return f"<p></p>\n<p><b>{esc(text)}</b></p>"


def render_ul(items: list[str]) -> str:
    body = "\n".join(f"  <li>✅ {item}</li>" for item in items)
    return f"<ul>\n{body}\n</ul>"


def build_feature_items(index: int) -> list[str]:
    rotated = FEATURE_REPHRASES[index % len(FEATURE_REPHRASES):] + FEATURE_REPHRASES[: index % len(FEATURE_REPHRASES)]
    selected = rotated[:3]
    return [
        esc(selected[0]),
        esc(selected[1]),
        esc(selected[2]),
        "Colorful pages with illustrations, diagrams, and a friendly owl mascot",
        "Answer key with explanations",
        "Print and go / no prep needed",
    ]


def build_use_cases(state_name: str, exam_name: str, exam_acronym: str, index: int) -> list[str]:
    exam_label = f"{exam_name} ({exam_acronym})" if exam_name and exam_acronym else f"{state_name} math assessments"
    variants = [
        [
            f"Classroom reteaching, small-group support, or intervention time when students need the procedure broken down more clearly",
            "Homeschool lessons when you want a full-year math guide with clear directions instead of long lectures",
            "Tutoring sessions where students can follow the same method together and then try it independently",
            "Parent-guided homework help when students need to see the order of the steps, not just the final answer",
            f"Test prep before {exam_label} or other state math checks when students need to tighten up their process",
            "Summer review that keeps problem-solving routines fresh before Grade 8 starts",
        ],
        [
            "Classroom support for students who know some of the math but still need help getting started on each problem",
            "Homeschool planning when you want a resource that shows exactly how one problem type turns into the next",
            "Tutoring that focuses on confidence-building and repeated routines instead of rushed shortcuts",
            "Parent-guided practice on homework nights when students need a calm, readable model to follow",
            f"Test prep leading into {exam_label} when students need the steps behind common Grade 7 question types",
            "Summer practice for students who benefit from steady structure and guided review",
        ],
        [
            "Classroom intervention blocks, math workshop, or extra-help periods",
            "Homeschool use when you want a procedural guide that students can return to on their own",
            "Tutoring sessions where every topic needs a clear beginning, middle, and end",
            "Parent-guided support for students who freeze unless the work is broken into smaller moves",
            f"Test prep for {exam_label} when students need to review how to solve, not only what to remember",
            "Summer catch-up or back-to-school refreshers before new math content arrives",
        ],
        [
            "Classroom use for reteaching and guided practice after the main lesson",
            "Homeschool routines that benefit from explicit steps and worked examples",
            "Tutoring plans for learners who need a dependable method they can reuse",
            "Parent-guided review when students need help seeing what to do first and what to do next",
            f"Test prep before {exam_label} or benchmark testing when procedure matters as much as accuracy",
            "Summer math review to keep skills active without overwhelming students",
        ],
    ]
    return variants[index % len(variants)]


def build_series_items(cross_sell: list[str]) -> list[str]:
    items = []
    for entry in cross_sell:
        name, description = parse_cross_sell_item(entry)
        items.append(f"<b>{esc(name)}</b> - {esc(description)}")
    return items


def build_html(entry: dict, facts_text: str, index: int) -> str:
    state_name = entry["state_name"]
    title = extract_field(facts_text, "Book Title") or entry["tpt_title"]
    subtitle = entry["subtitle"]
    curriculum_name = extract_field(facts_text, "Curriculum Name") or entry.get("curriculum_name", "")
    curriculum_acronym = extract_field(facts_text, "Curriculum Acronym") or entry.get("curriculum_acronym", "")
    exam_name = extract_field(facts_text, "Exam Name") or entry.get("exam_name", "")
    exam_acronym = extract_field(facts_text, "Exam Acronym") or entry.get("exam_acronym", "")
    total_topics = extract_field(facts_text, "Total Topics")
    total_chapters = extract_field(facts_text, "Total Chapters")

    chapters = parse_chapters(extract_section(facts_text, "CHAPTERS & TOPICS"))
    cross_sell = parse_bullets(extract_section(facts_text, "SERIES CROSS-SELL"))

    blocks = [
        section_heading(OPENING_HEADINGS[index % len(OPENING_HEADINGS)].format(state=state_name)),
        f"<p>{OPENING_LINES[index % len(OPENING_LINES)].format(title=esc(title), subtitle=esc(subtitle), state=state_name)}</p>",
        section_heading(FEATURE_HEADINGS[index % len(FEATURE_HEADINGS)].format(state=state_name)),
        render_ul(build_feature_items(index)),
        section_heading(CHAPTER_HEADINGS[index % len(CHAPTER_HEADINGS)].format(state=state_name, topics=total_topics)),
        f"<p>This {state_name} edition covers <b>{esc(total_topics)}</b> topics across <b>{esc(total_chapters)}</b> chapters.</p>",
        render_ul([f"<b>{esc(name)}</b> - {esc(count)}" for name, count in chapters]),
        section_heading(CURRICULUM_HEADINGS[index % len(CURRICULUM_HEADINGS)].format(state=state_name)),
        f"<p>{CURRICULUM_LINES[index % len(CURRICULUM_LINES)].format(state=state_name, curriculum_name=esc(curriculum_name), curriculum_acronym=esc(curriculum_acronym))}</p>",
    ]

    if exam_name and exam_name.lower() not in {"(none)", ""}:
        blocks.extend([
            section_heading(EXAM_HEADINGS[index % len(EXAM_HEADINGS)].format(state=state_name, exam=exam_name, exam_acronym=exam_acronym)),
            f"<p>{EXAM_LINES[index % len(EXAM_LINES)].format(exam_name=esc(exam_name), exam_acronym=esc(exam_acronym))}</p>",
        ])

    blocks.extend([
        section_heading(USE_CASE_HEADINGS[index % len(USE_CASE_HEADINGS)].format(state=state_name)),
        render_ul([esc(item) for item in build_use_cases(state_name, exam_name, exam_acronym, index)]),
        section_heading(SERIES_HEADINGS[index % len(SERIES_HEADINGS)].format(state=state_name)),
        render_ul(build_series_items(cross_sell)),
        section_heading(CLOSING_HEADINGS[index % len(CLOSING_HEADINGS)].format(state=state_name)),
    ])

    closing_first, closing_second = CLOSING_LINES[index % len(CLOSING_LINES)]
    blocks.append(f"<p>{closing_first}</p>")
    blocks.append(f"<p>{closing_second.format(state=state_name)}</p>")
    blocks.append(FOOTER)

    return "\n\n".join(blocks) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for index, entry in enumerate(load_entries()):
        facts_text = run_facts(entry["state_slug"])
        html_text = build_html(entry, facts_text, index)
        output_path = OUTPUT_DIR / f"{entry['state_slug']}_tpt_{TODAY}.html"
        output_path.write_text(html_text, encoding="utf-8")
        print(output_path.relative_to(WORKSPACE))


if __name__ == "__main__":
    main()
