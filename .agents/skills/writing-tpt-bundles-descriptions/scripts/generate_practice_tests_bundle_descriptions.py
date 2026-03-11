#!/usr/bin/env python3
"""Generate Practice Tests Bundle TPT HTML descriptions for all states."""

from __future__ import annotations

import html
from pathlib import Path

import get_bundle_facts as facts


BUNDLE_TYPE = "practice_tests_bundle"
BUNDLE_COMMENT = "3 + 5 + 7 + 10 Practice Tests = 25 Unique Tests, 750 Questions"
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

OPENINGS_WITH_EXAM = [
	"This 4-book bundle gives you serious {state} Grade 7 test prep in one set: the 3-test, 5-test, 7-test, and 10-test books. Together they deliver <b>25 unique, non-overlapping full-length tests</b> with <b>750 total questions</b>, all written with the <b>{exam_name} ({exam_acronym})</b> in mind.",
	"If you want enough fresh practice to keep test prep going all year, this {state} bundle does it. You get 4 books, <b>25 different full-length tests</b>, and <b>750 questions</b> with no repeated questions across the editions, built to match the <b>{exam_name} ({exam_acronym})</b>.",
	"This bundle pulls together all four {state} practice test editions into one place. That means <b>25 full-length tests</b>, <b>750 questions</b>, and no overlap from one book to the next, all aimed at the expectations of the <b>{exam_name} ({exam_acronym})</b>.",
	"For {state} Grade 7 math, this set gives you a long runway for test prep. The 4 books include <b>25 unique, non-overlapping tests</b> and <b>750 total questions</b>, so students can keep practicing for the <b>{exam_name} ({exam_acronym})</b> without seeing the same test again.",
	"Here is the full {state} practice-test set for Grade 7 math. It combines the 3, 5, 7, and 10 test editions into <b>25 unique full-length tests</b> with <b>750 questions</b>, designed around the style and coverage students need for the <b>{exam_name} ({exam_acronym})</b>.",
]

OPENINGS_NO_EXAM = [
	"This 4-book bundle gives you full {state} Grade 7 math test prep in one package: the 3-test, 5-test, 7-test, and 10-test books. Together they include <b>25 unique, non-overlapping full-length tests</b> with <b>750 total questions</b>, all aligned to {state} expectations.",
	"If you need enough fresh assessment practice to last, this {state} bundle does the job. You get 4 books, <b>25 different full-length tests</b>, and <b>750 questions</b> with no repeated questions across the editions.",
	"This bundle brings all four {state} practice test editions together in one set. That gives you <b>25 full-length tests</b>, <b>750 questions</b>, and no overlap from one book to the next, written for {state} Grade 7 math.",
	"For {state} Grade 7 math, this set gives you a lot of room for review and assessment. The 4 books include <b>25 unique, non-overlapping tests</b> and <b>750 total questions</b>, so students can keep practicing without seeing the same material again.",
	"Here is the full {state} practice-test set for Grade 7 math. It combines the 3, 5, 7, and 10 test editions into <b>25 unique full-length tests</b> with <b>750 questions</b>, built around state-specific standards instead of generic review.",
]

WHATS_HEADINGS = [
	"What You Get for {state}",
	"Inside the {state} Bundle",
	"The 4 Books in This Set",
	"What Is Included for {state} Math",
	"Everything in the {state} Practice Tests Bundle",
]

PRACTICE_HEADINGS = [
	"Why 25 Tests Matters",
	"What Makes These Tests Different",
	"Fresh Practice All Year",
	"How This Bundle Stays Useful",
	"A Bigger Test Bank for {state}",
]

CURRICULUM_HEADINGS = [
	"Built for {state}",
	"Aligned to {state} Math",
	"Written for {state} Standards",
	"Why This Fits {state}",
	"Made for {state} Grade 7 Math",
]

USE_CASE_HEADINGS = [
	"Good Fits for This Bundle",
	"How Teachers and Families Use It",
	"Where This Set Helps Most",
	"Who This Bundle Works For",
	"Ways to Put the Tests to Work",
]

QUALITY_HEADINGS = [
	"What Every Book Includes",
	"What You Can Count On in Every Book",
	"Across All 4 Books",
	"Shared Features in the Bundle",
	"What Comes with Every Test Book",
]

CROSS_HEADINGS = [
	"Need More Than Test Prep?",
	"Also in the Series",
	"Want to Add Lessons Too?",
	"More Grade 7 Math Resources",
	"If You Want to Build Beyond Tests",
]

CLOSINGS = [
	(
		"It is a simple way to keep {state} test prep going without running out of fresh material.",
		"<b>Pick up the bundle and give your students 25 unique chances to practice before test day.</b>",
	),
	(
		"You get enough full-length practice here to track growth, spot gaps, and keep review moving.",
		"<b>Choose the bundle when you want real {state} test prep with depth.</b>",
	),
	(
		"This set keeps assessment practice broad instead of repetitive.",
		"<b>Grab the bundle and put 750 {state}-aligned questions to work.</b>",
	),
	(
		"For ongoing review, intervention, and exam prep, this bundle gives you plenty to work with.",
		"<b>Add the bundle and keep your {state} test prep fresh from start to finish.</b>",
	),
	(
		"When you need a lot of practice and you do not want duplicates, this is the set to reach for.",
		"<b>Get the bundle and give your students 25 non-overlapping full-length tests.</b>",
	),
]

ORDERS = [
	["whats", "practice", "curriculum", "use_cases", "quality", "cross_sell"],
	["curriculum", "whats", "use_cases", "practice", "quality", "cross_sell"],
	["whats", "curriculum", "practice", "cross_sell", "use_cases", "quality"],
	["practice", "whats", "curriculum", "quality", "use_cases", "cross_sell"],
	["curriculum", "practice", "whats", "use_cases", "cross_sell", "quality"],
]

BOOK_LINE_VARIANTS = {
	"3 Practice Tests": [
		"three full-length practice tests with detailed answer explanations",
		"three unique full-length tests for the first round of serious prep",
		"three complete tests with answer explanations students can learn from",
	],
	"5 Practice Tests": [
		"five more full-length tests for extra practice",
		"five additional unique tests that expand the practice pool",
		"five fresh full-length tests when students need more reps",
	],
	"7 Practice Tests": [
		"seven full-length tests with detailed answers",
		"seven more unique tests for deeper review",
		"seven complete tests that keep practice going without repeats",
	],
	"10 Practice Tests": [
		"ten full-length tests with answer explanations",
		"ten more unique tests for the biggest share of the bundle",
		"ten complete tests that give you the longest stretch of fresh prep",
	],
}

PRACTICE_PARAGRAPHS = [
	"The four books are not recycled versions of the same material. Each edition adds its own tests, so you get 25 different full-length assessments and 750 questions altogether.",
	"This bundle lasts because the tests do not overlap. Students can move from one edition to the next without running into repeated questions.",
	"There is real depth here, not repackaged practice. Across the 3, 5, 7, and 10 test books, every test is distinct.",
	"If you use one test each week, this set stretches a long way. The questions stay fresh across all four books instead of repeating from edition to edition.",
	"The main value here is range. You are getting 25 separate full-length tests, not the same few items rearranged into different books.",
]

PRACTICE_BULLETS = [
	[
		"25 unique tests x 30 questions each = 750 total questions",
		"no repeated questions across the 3, 5, 7, and 10 test editions",
		"detailed answer explanations for every single question",
		"score tracking so students can measure growth over time",
	],
	[
		"25 non-overlapping full-length tests for ongoing review",
		"750 total questions to support diagnostics, practice, and reassessment",
		"step-by-step answer explanations that make review easier",
		"realistic test-day style and coverage",
	],
	[
		"enough fresh tests to run weekly prep without repeating the same material",
		"750 questions spread across four different practice test books",
		"answer explanations that show students how to fix mistakes",
		"state-specific coverage instead of generic national test prep",
	],
]

CURRICULUM_WITH_EXAM = [
	"Every test is aligned to the <b>{curriculum_name} ({curriculum_acronym})</b> and written with the <b>{exam_name} ({exam_acronym})</b> in mind. It is made for {state}, not relabeled for {state}.",
	"This bundle matches the <b>{curriculum_name} ({curriculum_acronym})</b> and reflects the kind of coverage students need for the <b>{exam_name} ({exam_acronym})</b>. It is a {state}-specific resource from the ground up.",
	"The questions follow the <b>{curriculum_name} ({curriculum_acronym})</b> and stay focused on what students are expected to handle for the <b>{exam_name} ({exam_acronym})</b>. This is not generic test prep.",
]

CURRICULUM_NO_EXAM = [
	"Every test is aligned to the <b>{curriculum_name} ({curriculum_acronym})</b>. It is made for {state} specifically, not copied from a one-size-fits-all national set.",
	"This bundle follows the <b>{curriculum_name} ({curriculum_acronym})</b>, so the practice stays tied to what {state} students are actually expected to learn.",
	"The questions match the <b>{curriculum_name} ({curriculum_acronym})</b> and stay grounded in {state} Grade 7 expectations all the way through.",
]

USE_CASE_VARIANTS = [
	[
		"weekly test-prep sessions when you want fresh full-length practice across the year",
		"pre-test and post-test comparisons to track student growth",
		"diagnostic checks that help you spot gaps before the real exam",
		"homework packets when one full test per week makes sense",
		"tutoring or after-school programs that need new practice each session",
		"homeschool routines that want realistic testing practice at home",
		"summer review before students move into the next grade",
	],
	[
		"teachers who want enough assessment material to keep review going without repeats",
		"benchmark-style check-ins across the school year",
		"intervention groups that need extra full-length practice after reteaching",
		"home packets and independent review work",
		"tutors who want a fresh test ready for every meeting",
		"families preparing at home for state testing",
		"end-of-year review when you want lots of practice in reserve",
	],
	[
		"classrooms running regular test-prep Fridays or weekly review blocks",
		"growth checks from the start of the year to the weeks before testing",
		"small-group support after you identify weak strands",
		"make-up work or extra practice when students need another full test",
		"after-school and Saturday programs that need a deep bank of questions",
		"homeschool planning where realistic assessment practice matters",
		"summer refreshers that keep math skills active",
	],
]

QUALITY_VARIANTS = [
	[
		"colorful, student-friendly pages with illustrations, diagrams, and the owl mascot throughout",
		"complete answer keys with explanations so review is easier for teachers, tutors, and families",
		"print-ready files you can download, print, and use right away",
	],
	[
		"bright, kid-friendly design that keeps full-length practice from feeling dry",
		"answer explanations that help students understand mistakes instead of just seeing the correct choice",
		"ready-to-print materials with no extra setup needed",
	],
	[
		"approachable page design with visuals and a friendly owl guide across the series",
		"built-in answer keys and explanations for every book in the bundle",
		"printable files that are ready for classroom, tutoring, or home use",
	],
]

CROSS_INTROS = [
	"Practice tests work best when students already know the material. Pair this bundle with:",
	"If you want to add teaching or topic-by-topic practice around these tests, start here:",
	"This bundle covers assessment practice. To build out the teaching side too, look at:",
]


def esc(text: str) -> str:
	return html.escape(text, quote=False)


def normalize(text: str) -> str:
	return text.replace("\\&", "&")


def pick(options: list[str], idx: int, step: int = 1) -> str:
	return options[(idx * step) % len(options)]


def heading(template: str, state_name: str) -> str:
	return template.format(state=state_name)


def split_cross_sell(text: str) -> tuple[str, str]:
	if " - " in text:
		name, desc = text.split(" - ", 1)
		return name, desc
	if " — " in text:
		name, desc = text.split(" — ", 1)
		return name, desc
	return text, ""


def book_list_item(book_name: str, idx: int) -> str:
	variant = BOOK_LINE_VARIANTS[book_name][idx % len(BOOK_LINE_VARIANTS[book_name])]
	return f"  <li>✅ <b>{esc(book_name)}</b> - {esc(variant)}</li>"


def bullet_list(items: list[str]) -> str:
	lines = ["<ul>"]
	for item in items:
		lines.append(f"  <li>✅ {item}</li>")
	lines.append("</ul>")
	return "\n".join(lines)


def render_whats_section(state_name: str, idx: int) -> str:
	books = [
		"3 Practice Tests",
		"5 Practice Tests",
		"7 Practice Tests",
		"10 Practice Tests",
	]
	lines = [f"<p></p><p><b>{esc(heading(pick(WHATS_HEADINGS, idx, 2), state_name))}</b></p>", "<ul>"]
	for book_name in books:
		lines.append(book_list_item(book_name, idx))
	lines.append("</ul>")
	lines.append(
		"<p>All four editions stay distinct from each other, so the bundle gives you 25 unique, non-overlapping tests and 750 questions instead of repeated practice.</p>"
	)
	return "\n".join(lines)


def render_practice_section(state_name: str, idx: int, has_exam: bool, exam_acronym: str) -> str:
	bullets = [esc(item) for item in PRACTICE_BULLETS[idx % len(PRACTICE_BULLETS)]]
	if has_exam:
		bullets.append(f"aligned to the format and expectations students face on the <b>{esc(exam_acronym)}</b>")
	else:
		bullets.append(f"built around {esc(state_name)} Grade 7 math expectations")
	lines = [f"<p></p><p><b>{esc(heading(pick(PRACTICE_HEADINGS, idx, 3), state_name))}</b></p>"]
	lines.append(f"<p>{esc(PRACTICE_PARAGRAPHS[idx % len(PRACTICE_PARAGRAPHS)])}</p>")
	lines.append(bullet_list(bullets))
	return "\n".join(lines)


def render_curriculum_section(state_name: str, idx: int, curriculum_name: str, curriculum_acronym: str, exam_name: str, exam_acronym: str) -> str:
	if exam_name and exam_acronym:
		body = pick(CURRICULUM_WITH_EXAM, idx, 2).format(
			state=state_name,
			curriculum_name=esc(curriculum_name),
			curriculum_acronym=esc(curriculum_acronym),
			exam_name=esc(exam_name),
			exam_acronym=esc(exam_acronym),
		)
	else:
		body = pick(CURRICULUM_NO_EXAM, idx, 2).format(
			state=state_name,
			curriculum_name=esc(curriculum_name),
			curriculum_acronym=esc(curriculum_acronym),
		)
	return "\n".join(
		[
			f"<p></p><p><b>{esc(heading(pick(CURRICULUM_HEADINGS, idx, 2), state_name))}</b></p>",
			f"<p>{body}</p>",
		]
	)


def render_use_cases_section(state_name: str, idx: int) -> str:
	items = [esc(item) for item in USE_CASE_VARIANTS[idx % len(USE_CASE_VARIANTS)]]
	return "\n".join(
		[
			f"<p></p><p><b>{esc(heading(pick(USE_CASE_HEADINGS, idx, 3), state_name))}</b></p>",
			bullet_list(items),
		]
	)


def render_quality_section(state_name: str, idx: int) -> str:
	items = [esc(item) for item in QUALITY_VARIANTS[idx % len(QUALITY_VARIANTS)]]
	return "\n".join(
		[
			f"<p></p><p><b>{esc(heading(pick(QUALITY_HEADINGS, idx, 2), state_name))}</b></p>",
			bullet_list(items),
		]
	)


def render_cross_sell_section(state_name: str, idx: int, cross_sell: list[str]) -> str:
	lines = [f"<p></p><p><b>{esc(heading(pick(CROSS_HEADINGS, idx, 2), state_name))}</b></p>"]
	lines.append(f"<p>{esc(pick(CROSS_INTROS, idx, 2))}</p>")
	lines.append("<ul>")
	for item in cross_sell:
		name, desc = split_cross_sell(item)
		lines.append(f"  <li>✅ <b>{esc(name)}</b> - {esc(desc)}</li>")
	lines.append("</ul>")
	return "\n".join(lines)


def render_opening(state_name: str, idx: int, exam_name: str, exam_acronym: str) -> str:
	if exam_name and exam_acronym:
		template = pick(OPENINGS_WITH_EXAM, idx, 2)
		text = template.format(
			state=state_name,
			exam_name=esc(exam_name),
			exam_acronym=esc(exam_acronym),
		)
	else:
		template = pick(OPENINGS_NO_EXAM, idx, 2)
		text = template.format(state=state_name)
	return f"<p>{text}</p>"


def render_closing(state_name: str, idx: int) -> str:
	summary, cta = CLOSINGS[idx % len(CLOSINGS)]
	return "\n".join([
		f"<p>{esc(summary.format(state=state_name))}</p>",
		f"<p>{cta.format(state=esc(state_name))}</p>",
	])


def render_description(state_slug: str, idx: int, config) -> str:
	state_name = config.state_display_names[state_slug]
	exams = facts.load_state_exams()
	curriculums = facts.load_state_curriculums()
	exam = exams.get(state_slug, {})
	curriculum = curriculums.get(state_slug, {})

	exam_name = exam.get("exam_name", "")
	exam_acronym = exam.get("exam_acronym", "")
	curriculum_name = normalize(curriculum.get("curriculum_name", ""))
	curriculum_acronym = normalize(curriculum.get("curriculum_acronym", ""))
	bundle_title = facts.bundle_tpt_title(BUNDLE_TYPE, state_slug, state_name)
	cross_sell = facts.get_cross_sell(BUNDLE_TYPE)

	sections = {
		"whats": render_whats_section(state_name, idx),
		"practice": render_practice_section(state_name, idx, bool(exam_name and exam_acronym), exam_acronym),
		"curriculum": render_curriculum_section(
			state_name,
			idx,
			curriculum_name,
			curriculum_acronym,
			normalize(exam_name),
			normalize(exam_acronym),
		),
		"use_cases": render_use_cases_section(state_name, idx),
		"quality": render_quality_section(state_name, idx),
		"cross_sell": render_cross_sell_section(state_name, idx, cross_sell),
	}

	comment_lines = [
		f"<!-- {bundle_title} -->",
		f"<!-- Bundle: {BUNDLE_COMMENT} -->",
		f"<!-- TPT Title: {bundle_title} -->",
	]

	parts = comment_lines + [render_opening(state_name, idx, normalize(exam_name), normalize(exam_acronym))]
	for key in ORDERS[idx % len(ORDERS)]:
		parts.append(sections[key])
	parts.append(render_closing(state_name, idx))
	parts.append(FOOTER)
	return "\n\n".join(parts) + "\n"


def main() -> None:
	config = facts.load_config(facts.WORKSPACE)
	out_dir = facts.WORKSPACE / "final_output" / "bundles" / BUNDLE_TYPE
	out_dir.mkdir(parents=True, exist_ok=True)

	for idx, state_slug in enumerate(config.all_state_slugs):
		html_text = render_description(state_slug, idx, config)
		out_path = out_dir / f"{state_slug}_tpt_bundle.html"
		out_path.write_text(html_text, encoding="utf-8")
		print(f"Wrote {out_path.relative_to(facts.WORKSPACE)}")


if __name__ == "__main__":
	main()
