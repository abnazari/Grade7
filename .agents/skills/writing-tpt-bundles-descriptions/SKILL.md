---
name: writing-tpt-bundles-descriptions
description: How to write unique, high-converting TPT product listing HTML descriptions for math book bundles. Use when asked to write or generate TPT bundle descriptions, bundle listings, or bundle product descriptions for any bundle type × state combination.
---


# Writing TPT Bundle Descriptions

Write unique HTML product descriptions for Teachers Pay Teachers (TPT) bundles. Each description is for a specific math **bundle** (a set of books) for a specific US state. Every description must be **unique** — different structure, different phrasing, different hooks — while keeping all facts correct.

There are **6 bundle types × 50 states = 300 descriptions** total. No two should read the same.

---

## The 6 Bundles

| Bundle Type | Display Name | Books | Price Tier |
|---|---|---|---|
| `practice_tests_bundle` | Practice Tests Bundle | 3+5+7+10 PT (4 books) | Mid |
| `study_practice_bundle` | Study & Practice Bundle | Study Guide + Workbook + 3+5+7+10 PT (6 books) | Premium |
| `test_prep_bundle` | Test Prep Bundle | Math in 30 Days + Quizzes + 3+5+7+10 PT (6 books) | Premium |
| `classroom_bundle` | Classroom Bundle | Step-by-Step + Workbook + Quizzes + Worksheets + 3+5+7+10 PT (8 books) | High |
| `activities_assessments_bundle` | Activities & Assessments Bundle | Puzzles + Worksheets + Quizzes (3 books) | Budget |
| `complete_series_bundle` | Complete Series Bundle | All 11 books (everything except All-in-One) | Ultimate |

**Key fact:** The four practice test books (3, 5, 7, and 10 editions) contain **25 completely different, non-overlapping tests** with **750 total questions**. No repeated questions across any edition. This must be mentioned prominently in every bundle that includes practice tests.

---

## Step 1 — Get the Facts

Run this script to get every fact you need for a specific bundle × state:

```bash
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py <bundle_type> <state_slug>
```

**Examples:**
```bash
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py practice_tests_bundle texas
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py complete_series_bundle california
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py activities_assessments_bundle new-york
```

**Helpful flags:**
```bash
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py --list-bundles
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py --list-states
```

The script outputs everything: bundle title, books included with one-liners, state name, curriculum & exam info, chapter summaries, key selling points, use cases, how books work together, cross-sell, and the save path.

**Do not make up any facts.** Everything comes from the script output.

## Step 2 — Write the HTML Description

Using the facts from Step 1, write a complete HTML product description following the rules below.

## Step 3 — Save the File

Save the description to the path shown in the script output:
```
final_output/bundles/<bundle_type>/<state_slug>_tpt_bundle.html
```
Example: `final_output/bundles/practice_tests_bundle/texas_tpt_bundle.html`

## Step 4 — Generate Thumbnails

Run this script to generate 4 composite thumbnail images showing the book covers:

```bash
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/generate_bundle_thumbnails.py <bundle_type> <state_slug>
```

**Examples:**
```bash
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/generate_bundle_thumbnails.py practice_tests_bundle texas
python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/generate_bundle_thumbnails.py complete_series_bundle california
```

**Requires:** Pillow (`pip install Pillow`)

The script creates 4 JPEG thumbnails (2048×2048) in the same folder as the HTML:
- `<state_slug>_thumbnail_1.jpeg` — All books in the bundle
- `<state_slug>_thumbnail_2.jpeg` — First subset of books
- `<state_slug>_thumbnail_3.jpeg` — Second subset
- `<state_slug>_thumbnail_4.jpeg` — Third subset

For example, the 11-book Complete Series bundle splits into: all 11 → first 4 → next 4 → last 3.

The cover images are in `images/covers/` and are shared across all states (not state-specific). The thumbnails are the same for every state within the same bundle type — but the script still takes a state slug to name the output files correctly.

## Step 5 — Generate Preview PDF

Run this script to generate a preview PDF showing sample pages from each book in the bundle:

```bash
python3 scripts/generate_bundle_preview.py <bundle_type> <state_slug>
```

**Examples:**
```bash
python3 scripts/generate_bundle_preview.py practice_tests_bundle texas
python3 scripts/generate_bundle_preview.py complete_series_bundle california
```

The script generates a `.tex` file, compiles it with xelatex (2 passes), and saves the PDF to:
```
final_output/bundles/<bundle_type>/<state_slug>_tpt_bundle_preview.pdf
```

The preview includes:
- A copyright page
- One sample topic from each book type in the bundle (all from Chapter 1)
- For practice test books, one full sample test
- For "Math in 30 Days", Day 1
- An answer key (if the bundle includes quizzes or practice tests)
- A "Get the Full Book" call-to-action page
- A diagonal "PREVIEW" watermark on every page

**Flags:**
- `--dry-run` — generate `.tex` without compiling
- `--passes N` — number of xelatex passes (default: 2)
- `--list-bundles` — list all bundle types

---

## HTML Formatting Rules

### Allowed elements
- `<p>` for paragraphs
- `<b>` for bold text (section headings, key phrases, book names, state names, CTAs)
- `<i>` for occasional emphasis
- `<ul>` and `<li>` for bullet lists
- `<a href="..." target="_blank">` for links (footer only)
- The star separator line (footer only): `<p></p>★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★<p></p>`

### Forbidden
- **No `<h1>`, `<h2>`, or `<h3>`** — TPT already shows the product title as the page heading.
- **No `<hr>` dividers.**
- **No `<br>` tags** — use `<p>` for spacing.
- **No inline CSS or style attributes.**
- **No `<div>`, `<span>`, or any block-level wrappers.**
- **No tables.**

### Emoji rule
- **✅** may **only** appear as the **first character inside `<li>` bullet points**.
- Example: `<li>✅ Full lessons with clear explanations for every topic</li>`
- Do not use ✅ anywhere else — not in paragraphs, not in headings.

### Spacing
- Use `<p></p>` (empty paragraph) before section headings to create visual space.
- Section headings go inside `<b>` tags within a `<p>` (or standalone `<b>` after `<p></p>`).

### HTML comments at the top
Start every description with 3 HTML comment lines:
```html
<!-- {Bundle Title} -->
<!-- Bundle: {list of books} -->
<!-- TPT Title: {TPT Title from script} -->
```

---

## Required Sections

Every description must include **all applicable** sections. You have **complete freedom** over the order, heading text, and phrasing — but don't omit any.

### 1. Opening Paragraph
State what the bundle is. Be direct.

- **Do NOT include the bundle title as a heading** — TPT already displays the product title.
- Write 1–2 sentences that say what the bundle contains and why it matters.
- Mention the number of books and, if applicable, "25 unique, non-overlapping tests" and "750 questions".
- Reference the state exam by name if the state has one.

### 2. What's in the Bundle
A `<ul>` listing every book in the bundle with ✅ bullets.

- Each `<li>` should bold the book name and give its one-liner description.
- After the list, include a sentence reinforcing that practice test editions contain completely different tests (if the bundle includes them).

### 3. How the Books Work Together (if provided by script)
For bundles with 2+ non-PT book types, explain how each book serves a different purpose.

- Use the "how_books_work_together" data from the script as a starting point.
- Show the logical flow: e.g., "Study Guide for concepts → Workbook for practice → Tests for assessment".
- Rephrase — don't copy verbatim from the script.
- For the Practice Tests bundle (only PTs), skip this section.
- For the Complete Series bundle, this section can be a high-level overview rather than per-book.

### 4. Chapter Coverage (optional, recommended for bundles with 4+ non-PT books)
Show what the books cover using a compact `<ul>` list of chapters with topic counts.

- Must match the script output exactly.
- Include total topic count.
- Skip for the Practice Tests bundle (test content is strand-based, not chapter-based).

### 5. Curriculum Alignment
State that the bundle matches the state's curriculum.

- **Must** mention the full curriculum name and acronym (in `<b>`)
- **Must** mention the exam name and acronym if the state has one (in `<b>`)
- Make it clear this is state-specific — not a generic national resource
- Keep the language casual

### 6. Use Cases
A bullet list showing who this bundle is for and how to use it.

- Use ✅ before each `<li>`
- Get them from the script output — rephrase, don't copy verbatim
- Make the heading sound natural

### 7. Every Book Includes (design/quality features)
A short `<ul>` with 3 bullet points that apply to every book:

- Colorful, kid-friendly design with illustrations, diagrams, and a friendly owl mascot
- Complete answer keys with explanations
- Print-ready — download, print, and use

Rephrase these — don't use the exact same wording every time.

### 8. Cross-Sell (skip for Complete Series)
Promote the other books/bundles NOT included in this bundle.

- Use the cross-sell list from the script output
- Each bullet should bold the book name and give a one-liner
- Always use ✅ before each `<li>`
- Include a natural intro sentence (from the script's cross_sell_note)
- For the Complete Series bundle, **skip this section** entirely — there's nothing left to cross-sell

### 9. Closing CTA
1–2 short lines:
- First: a brief, punchy summary
- Second: a bold call to action (wrapped in `<b>`)

### 10. Footer (NEVER MODIFY)
Copy this footer **exactly** into every description. Replace `{Grade}` with the actual grade (e.g., "Grade 3", "Grade 8"). Never change any other word, link, or punctuation.

```html
<p></p>★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★<p></p>

<p>
  Looking for more <b>{Grade} Math</b> resources? Visit my
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
</p>
```

---

## Critical Rules for Practice Tests

For **every bundle that includes practice tests** (5 out of 6 bundles), you MUST:

1. State that the 25 tests are **unique and non-overlapping** — no repeated questions across editions.
2. Mention the total: **25 tests × 30 questions = 750 questions**.
3. Reinforce this at least twice: once in the opening, once in the "What's in the Bundle" section or elsewhere.
4. Never imply the same questions appear in different editions.

The Activities & Assessments bundle is the only bundle without practice tests — don't mention them in that description.

---

## Uniqueness Requirements

**Every description must be unique.** This is the most important part.

### Vary the structure
- Change the **order** of sections (except: opening always first, footer always last)
- Sometimes lead with curriculum alignment, sometimes with the book breakdown
- Some descriptions might merge sections (e.g., combine curriculum into the opening)

### Vary the headings
Never use the same `<b>` heading twice across descriptions for the same bundle type. Examples:

| Section | Example Headings (create your own too) |
|---|---|
| What's Included | "What's in the Bundle", "Here's What You Get", "Books Included", "Everything in This Bundle" |
| How They Work | "How It Works Together", "How Each Book Fits", "The System", "Here's How to Use It" |
| Chapters | "51 Topics Across 7 Chapters", "What's Covered", "Full Curriculum Breakdown" |
| Curriculum | "Built for Texas", "Aligned to TEKS", "Written for Texas", "Matches Texas Standards" |
| Use Cases | "Works For", "Who Uses This Bundle", "Great For", "Who'll Get the Most Out of This" |
| Quality | "Every Book Includes", "What You Can Expect", "In Every Book" |
| Cross-sell | "Also in the Series", "Want More?", "Need Lessons Too?", "Looking for More?" |

### Vary the prose
- Use contractions everywhere ("it's", "you'll", "don't", "here's")
- Keep sentences short. Mix punchy statements with slightly longer ones.
- Be direct. State what the bundle does plainly.
- Talk to the reader. Use "you" and "your students".
- Vary paragraph lengths — some sections one sentence, others 2–3.
- Rephrase selling points and use cases — don't copy them verbatim from the script.

---

## Tone & Voice

**This should read like a real human wrote it.** Think of a teacher telling a colleague about a resource they actually like.

### Do This
- **Be brief.** Opening: 1–2 sentences max. People scan product listings.
- **Use contractions.** "It's", "you'll", "they're", "don't".
- **Keep sentences short.** No semicolons with two subordinate clauses.
- **Be direct.** "This bundle gives you everything for {grade} math."
- **Talk to the reader.** Use "you" and "your students".

### Don't Do This
- **No storytelling.** Don't write "Imagine walking into your classroom..." Just state what the bundle does.
- **No padding.** If a sentence adds no information, cut it.
- **No corporate buzzwords.** Never write "proven learning sequence", "carefully curated", "drives instruction", "transforms", "nothing left to chance".
- **No flowery filler.** Cut "something priceless", "exceptional", "unparalleled", "powerhouse".
- **No marketing formulas.** Don't open with "pain point → solution → call to action".
- **Never use "proven".** Say what the bundle does and let people decide.
- **No robotic parallel structure.** "Learn → See → Do" sounds manufactured.

---

## Facts You Must Get Right

| Fact | Source |
|---|---|
| Bundle title | Script output |
| State name | Script output |
| Curriculum name & acronym | Script output |
| Exam name & acronym | Script output (may be absent) |
| Chapter names, numbers, topic counts | Script output |
| Total topic count | Script output |
| Books in the bundle | Script output |
| Practice test count / total questions | Script output |
| Book one-liners | Script output (rephrase, don't copy verbatim) |
| Cross-sell list | Script output |
| Footer HTML | Copy exactly from this SKILL.md |

**Do not make up page counts.** If you want to mention length, omit page counts entirely for bundles.

**Do not invent exam testing months.** If the script doesn't show them, don't guess.

---

## Checklist Before Saving

- [ ] All section headings use `<b>` tags (no `<h1>`, `<h2>`, etc.)
- [ ] All `<li>` bullets start with **✅**
- [ ] 3 HTML comment lines at the top (title, bundle contents, TPT title)
- [ ] Practice test uniqueness mentioned at least twice (if bundle includes PTs)
- [ ] Chapter data (if included) matches script output exactly
- [ ] Curriculum name, acronym, exam name, and exam acronym are correct
- [ ] Total topic count is correct (if mentioned)
- [ ] No `<h1>`, `<h2>`, `<hr>`, `<br>`, `<div>`, `<span>`, or tables
- [ ] `<p></p>` before section headings for spacing
- [ ] Footer copied exactly from this SKILL.md (from `★★★` to `– Dr. A. Nazari`)
- [ ] Description is genuinely **unique** — different from every other description you've written
- [ ] Read it out loud — does it sound like a real person wrote it?
- [ ] Saved to correct path: `final_output/bundles/<bundle_type>/<state_slug>_tpt_bundle.html`
- [ ] Thumbnails generated via `generate_bundle_thumbnails.py`
- [ ] Preview PDF generated via `generate_bundle_preview.py`

---

## Example Workflow

```
User: "Write TPT bundle descriptions for texas practice_tests_bundle and texas classroom_bundle"

Agent:
1. Run: python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py practice_tests_bundle texas
2. Read the facts output
3. Write the HTML description (unique structure, unique headings, unique prose)
4. Save to: final_output/bundles/practice_tests_bundle/texas_tpt_bundle.html
5. Run: python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/generate_bundle_thumbnails.py practice_tests_bundle texas
6. Run: python3 scripts/generate_bundle_preview.py practice_tests_bundle texas
7. Run: python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/get_bundle_facts.py classroom_bundle texas
8. Read the facts output
9. Write the HTML description (different structure from the previous one!)
10. Save to: final_output/bundles/classroom_bundle/texas_tpt_bundle.html
11. Run: python3 .agents/skills/writing-tpt-bundles-descriptions/scripts/generate_bundle_thumbnails.py classroom_bundle texas
12. Run: python3 scripts/generate_bundle_preview.py classroom_bundle texas
```

```
User: "Write all 6 TPT bundle descriptions for california"

Agent:
1. For each of the 6 bundle types:
   a. Run get_bundle_facts.py with the bundle type and "california"
   b. Read the facts
   c. Write a unique HTML description
   d. Save to the correct subfolder
   e. Run generate_bundle_thumbnails.py for the bundle type
   f. Run generate_bundle_preview.py for the bundle type
2. Ensure every description has different structure, headings, and phrasing
```