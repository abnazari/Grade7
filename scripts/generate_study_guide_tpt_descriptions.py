#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

from config_loader import TopicsConfig, load_config

WORKSPACE = Path(__file__).resolve().parents[1]
TITLES_PATH = WORKSPACE / "titles.json"
OUTPUT_DIR = WORKSPACE / "final_output" / "study_guide"
BOOK_TYPE = "study_guide"
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

FEATURES = [
    "Focused explanations of every key idea, so students get the core math without extra filler",
    "Important worked examples that show the kinds of Grade 7 problems students are most likely to see",
    "Short practice right after each topic, which makes it easy to check understanding fast",
    "Helpful visuals like diagrams, number lines, and charts that make review sessions easier to follow",
    "Compact enough for a quick review plan, but broad enough to cover the full Grade 7 course",
    "Clear learning goals that tell students what they should understand before they move on",
]

SERIES = [
    ("All-in-One", "The complete resource with full lessons, worked examples, and practice for every topic"),
    ("Workbook", "Hundreds of scaffolded practice problems organized by topic for extra practice"),
    ("Step-by-Step Guide", "A guided approach with clear, numbered instructions so students can work more independently"),
    ("Math in 30 Days", "A structured daily plan that walks through the full curriculum in one month"),
    ("Quizzes", "Quick 15-minute assessments for every topic when you want fast progress checks"),
    ("Puzzles & Brain Teasers", "Curriculum-aligned games, riddles, and challenges that add variety to math time"),
    ("Worksheets", "Standalone printable activities you can assign in any order"),
    ("Practice Tests (3, 5, 7, or 10 editions)", "Full-length test prep with answer explanations, and every edition includes different tests"),
]

SECTION_ORDERS = [
    ["chapters", "curriculum", "exam", "use_cases", "series", "closing"],
    ["curriculum", "chapters", "use_cases", "exam", "series", "closing"],
    ["use_cases", "chapters", "curriculum", "series", "exam", "closing"],
    ["chapters", "use_cases", "series", "curriculum", "exam", "closing"],
    ["curriculum", "exam", "chapters", "use_cases", "series", "closing"],
    ["series", "chapters", "curriculum", "use_cases", "exam", "closing"],
]

OPENING_HEADINGS = [
    "Key Concepts and Quick Practice for {state} Grade 7 Math",
    "A Compact {state} Grade 7 Math Study Guide",
    "Fast Review for {state} Grade 7 Math",
    "Essential Grade 7 Math Review for {state}",
    "A Quick-Reference {state} Math Study Guide",
    "Short, Clear Grade 7 Math Review for {state}",
    "Core Grade 7 Math Review for {state} Students",
    "A Focused {state} Grade 7 Math Refresher",
]

CHAPTER_HEADINGS = [
    "How the {state} Topics Break Down",
    "All {topics} Topics in the {state} Edition",
    "What This {state} Book Covers",
    "The Full Topic Map for {state}",
    "Every Chapter Included for {state}",
    "The {state} Coverage Snapshot",
    "What Students Review in {state}",
    "The Chapter List for {state}",
]

CURRICULUM_HEADINGS = [
    "Built Around {state}'s Standards",
    "Written for {state} Standards",
    "Made for {state} Math Class",
    "Why This Fits {state}",
    "This One Matches {state}",
    "A {state}-Specific Review Book",
    "The Standards Match for {state}",
    "How This Lines Up in {state}",
]

EXAM_HEADINGS = [
    "Extra Help for the {exam}",
    "When {exam_acronym} Prep Matters",
    "A Simple Way to Review for {exam_acronym}",
    "Also Useful Before the {exam}",
    "Built-In {exam_acronym} Review",
    "How This Supports {exam_acronym}",
    "For {state} Test Prep Too",
    "Review That Works Before {exam_acronym}",
]

USE_CASE_HEADINGS = [
    "Who This Works Well For in {state}",
    "Easy Ways to Use It in {state}",
    "Where This Study Guide Fits Best",
    "Good Uses for the {state} Edition",
    "When This Book Helps Most",
    "Ways Families and Teachers Use This",
    "Who Will Get the Most from This",
    "Practical Uses for This Review Book",
]

SERIES_HEADINGS = [
    "More {state} Grade 7 Math Options",
    "If You Want More Than a Study Guide",
    "Other {state} Books in the Series",
    "Need More Practice in {state}?",
    "What to Pair with This {state} Guide",
    "More Ways to Build a {state} Math Set",
    "Keep Going with the Full Series",
    "Other Resources for {state} Grade 7",
]

CLOSING_HEADINGS = [
    "A Solid Next Step for {state} Review",
    "Keep {state} Math Review Simple",
    "A Clear Way to Finish Strong in {state}",
    "Ready for Better {state} Review Sessions?",
    "A Confident Wrap-Up for {state} Math",
    "A Straightforward Choice for {state} Families",
    "One Book, Clear Review for {state}",
    "An Easy Win for {state} Grade 7 Math",
]

INTRO_LINES = [
    "<b>{title}</b> gives your students a focused way to review Grade 7 math with the exact mix of key ideas, examples, and quick practice they need.",
    "<b>{title}</b> is a compact review book for {state} Grade 7 math, made for quick refreshers, steady homework support, and test-season review.",
    "<b>{title}</b> keeps Grade 7 math review clear and manageable for {state} students who need the main ideas, not a giant textbook.",
    "<b>{title}</b> helps you review the full {state} Grade 7 course in a format that's easy to use at school, at home, or in tutoring.",
]

CURRICULUM_LINES = [
    "This study guide follows <b>{curriculum_name} ({curriculum_acronym})</b>, so it's built for {state} students instead of using a generic national sequence.",
    "It lines up with <b>{curriculum_name} ({curriculum_acronym})</b>, which means the review stays centered on what {state} students are actually expected to learn.",
    "Because it matches <b>{curriculum_name} ({curriculum_acronym})</b>, you can use it as a real {state}-specific review tool, not just a broad middle school supplement.",
    "The content is organized around <b>{curriculum_name} ({curriculum_acronym})</b>, so the examples and review focus make sense for {state} classrooms.",
]

EXAM_LINES = [
    "If your students are getting ready for <b>{exam_name} ({exam_acronym})</b>, this book gives them a clean way to revisit the skills they need before test day.",
    "It's also useful in the weeks before <b>{exam_name} ({exam_acronym})</b>, especially when students need a fast refresher across the full course.",
    "For <b>{exam_name} ({exam_acronym})</b> prep, this works well as a skill-by-skill review book before students move into full practice tests.",
    "When <b>{exam_name} ({exam_acronym})</b> is coming up, this guide helps students tighten up the main concepts without getting buried in long lessons.",
]

CLOSING_LINES = [
    (
        "It gives students a clearer picture of the full course and helps them review with less stress.",
        "<b>If you want a focused, state-specific Grade 7 math review book, this {state} study guide is ready to use.</b>",
    ),
    (
        "It keeps review time practical, organized, and easy to fit into real school weeks.",
        "<b>Pick up the {state} edition if you want a study guide that's simple to use and built for the standards your students actually see.</b>",
    ),
    (
        "Students get the big ideas, the right examples, and enough practice to check what they really know.",
        "<b>Add this {state} study guide when you want quick review without losing standards coverage.</b>",
    ),
    (
        "This is the kind of book that helps review stay consistent from one topic to the next.",
        "<b>Use the {state} edition when you want a dependable Grade 7 math refresher for class, home, or tutoring.</b>",
    ),
]


def load_titles() -> list[dict]:
    return json.loads(TITLES_PATH.read_text(encoding="utf-8"))


def get_state_topics(state_slug: str, config: TopicsConfig) -> list[str]:
    topics = list(config.core_topic_ids)
    additional = config.state_additional.get(state_slug, [])
    if not additional:
        return topics

    by_chapter: dict[str, list[str]] = {}
    for topic_id in additional:
        by_chapter.setdefault(topic_id[:4], []).append(topic_id)

    for chapter_key in sorted(by_chapter):
        extras = sorted(by_chapter[chapter_key])
        last_index = -1
        for i, topic_id in enumerate(topics):
            if topic_id.startswith(chapter_key):
                last_index = i
        if last_index >= 0:
            for offset, extra in enumerate(extras, start=1):
                topics.insert(last_index + offset, extra)
        else:
            topics.extend(extras)

    return topics


def build_chapter_summaries(state_slug: str, config: TopicsConfig) -> tuple[list[tuple[int, str, int]], int]:
    state_topic_ids = set(get_state_topics(state_slug, config))
    summaries: list[tuple[int, str, int]] = []

    for chapter in config.chapters:
        clean_title = chapter.title.replace("\\&", "&")
        count = sum(1 for topic in chapter.topics if topic.id in state_topic_ids)
        for additional_topic in config.additional_topics_list:
            if additional_topic.chapter == chapter.num and additional_topic.id in state_topic_ids:
                count += 1
        if count > 0:
            summaries.append((chapter.num, clean_title, count))

    return summaries, sum(count for _, _, count in summaries)


def pick(pool: list[str] | list[tuple[str, str]], index: int):
    return pool[index % len(pool)]


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def section_heading(text: str) -> str:
    return f"<p></p>\n<p><b>{esc(text)}</b></p>"


def ul(items: list[str]) -> str:
    body = "\n".join(f"  <li>✅ {item}</li>" for item in items)
    return f"<ul>\n{body}\n</ul>"


def feature_items(index: int) -> list[str]:
    rotated = FEATURES[index % len(FEATURES):] + FEATURES[:index % len(FEATURES)]
    selected = rotated[:3]
    return [
        esc(selected[0]),
        esc(selected[1]),
        esc(selected[2]),
        "Colorful pages with illustrations, diagrams, and a friendly owl mascot",
        "Answer key with explanations",
        "Print and go, with no prep needed",
    ]


def build_chapter_section(state_name: str, total_topics: int, chapters: list[tuple[int, str, int]], index: int) -> str:
    heading = pick(CHAPTER_HEADINGS, index).format(state=state_name, topics=total_topics)
    items = [
        f"<b>Chapter {num}: {esc(title)}</b> - {count} topic{'s' if count != 1 else ''}"
        for num, title, count in chapters
    ]
    return "\n".join([
        section_heading(heading),
        f"<p>This {state_name} edition covers <b>{total_topics} topics</b> across <b>{len(chapters)} chapters</b>.</p>",
        ul(items),
    ])


def build_curriculum_section(state_name: str, curriculum_name: str, curriculum_acronym: str, exam_name: str, exam_acronym: str, index: int) -> str:
    heading = pick(CURRICULUM_HEADINGS, index).format(state=state_name)
    lines = [
        section_heading(heading),
        f"<p>{pick(CURRICULUM_LINES, index).format(state=state_name, curriculum_name=esc(curriculum_name), curriculum_acronym=esc(curriculum_acronym))}</p>",
    ]
    if exam_name and exam_acronym:
        lines.append(
            f"<p>It also stays connected to <b>{esc(exam_name)} ({esc(exam_acronym)})</b>, so your review work points toward the same skills students are expected to show on the state test.</p>"
        )
    return "\n".join(lines)


def build_exam_section(state_name: str, exam_name: str, exam_acronym: str, index: int) -> str:
    if not exam_name or not exam_acronym:
        return ""
    heading = pick(EXAM_HEADINGS, index).format(state=state_name, exam=exam_name, exam_acronym=exam_acronym)
    return "\n".join([
        section_heading(heading),
        f"<p>{pick(EXAM_LINES, index).format(exam_name=esc(exam_name), exam_acronym=esc(exam_acronym))}</p>",
    ])


def build_use_cases_section(state_name: str, exam_acronym: str, index: int) -> str:
    heading = pick(USE_CASE_HEADINGS, index).format(state=state_name)
    exam_label = exam_acronym if exam_acronym else f"{state_name} math assessments"
    items = [
        "Classroom review before a quiz, chapter test, or end-of-unit check",
        "Homeschool lessons when you want a shorter review resource that still covers the full course",
        "Tutoring sessions that need a quick reference and a few focused practice problems",
        "Parent-guided homework help on nights when students need a clean explanation fast",
        f"Test prep before the {esc(exam_label)} or other state math assessments",
        "Summer review before students head into Grade 8",
    ]
    return "\n".join([section_heading(heading), ul(items)])


def build_series_section(state_name: str, index: int) -> str:
    heading = pick(SERIES_HEADINGS, index).format(state=state_name)
    items = [f"<b>{esc(name)}</b> - {esc(description)}" for name, description in SERIES]
    return "\n".join([section_heading(heading), ul(items)])


def build_closing_section(state_name: str, index: int) -> str:
    heading = pick(CLOSING_HEADINGS, index).format(state=state_name)
    first, second = pick(CLOSING_LINES, index)
    return "\n".join([
        section_heading(heading),
        f"<p>{first}</p>",
        f"<p>{second.format(state=state_name)}</p>",
    ])


def build_html(entry: dict, chapters: list[tuple[int, str, int]], total_topics: int, index: int) -> str:
    state_name = entry["state_name"]
    title = entry["tpt_title"]
    subtitle = entry["subtitle"]
    curriculum_name = entry.get("curriculum_name") or ""
    curriculum_acronym = entry.get("curriculum_acronym") or ""
    exam_name = entry.get("exam_name") or ""
    exam_acronym = entry.get("exam_acronym") or ""

    opening_heading = pick(OPENING_HEADINGS, index).format(state=state_name)
    intro = pick(INTRO_LINES, index).format(title=esc(title), state=state_name, subtitle=esc(subtitle))
    intro = intro.replace("</b>", f"</b> <i>{esc(subtitle)}</i>", 1)
    blocks = [
        section_heading(opening_heading),
        f"<p>{intro}</p>",
        ul(feature_items(index)),
    ]

    section_map = {
        "chapters": build_chapter_section(state_name, total_topics, chapters, index),
        "curriculum": build_curriculum_section(state_name, curriculum_name, curriculum_acronym, exam_name, exam_acronym, index),
        "exam": build_exam_section(state_name, exam_name, exam_acronym, index),
        "use_cases": build_use_cases_section(state_name, exam_acronym, index),
        "series": build_series_section(state_name, index),
        "closing": build_closing_section(state_name, index),
    }

    for section_name in SECTION_ORDERS[index % len(SECTION_ORDERS)]:
        section_html = section_map[section_name]
        if section_html:
            blocks.append(section_html)

    blocks.append(FOOTER)
    return "\n\n".join(blocks) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    titles = load_titles()
    config = load_config(WORKSPACE)
    entries = sorted(
        [entry for entry in titles if entry.get("book_type") == BOOK_TYPE],
        key=lambda entry: entry["state_slug"],
    )

    if len(entries) != 50:
        raise SystemExit(f"Expected 50 {BOOK_TYPE} entries, found {len(entries)}")

    for index, entry in enumerate(entries):
        chapters, total_topics = build_chapter_summaries(entry["state_slug"], config)
        html_text = build_html(entry, chapters, total_topics, index)
        output_path = OUTPUT_DIR / f"{entry['state_slug']}_tpt_{TODAY}.html"
        output_path.write_text(html_text, encoding="utf-8")
        print(output_path.relative_to(WORKSPACE))


if __name__ == "__main__":
    main()
