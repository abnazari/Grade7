---
name: writing-tpt-description
description: How to write unique, high-converting TPT product listing HTML descriptions for Grade 7 math books using the get_book_facts.py script. Use when asked to write or generate TPT descriptions, TPT listings, or product descriptions for any book type × state combination.
---

# Writing TPT Product Listing Descriptions

Write unique HTML product descriptions for Teachers Pay Teachers (TPT). Each description is for a specific Grade 7 math book for a specific US state. Every description must be **unique** — different structure, different phrasing, different hooks — while keeping all facts correct.

There are **12 book types × 50 states = 600 descriptions** total. No two should read the same.

---

## Step 1 — Get the Facts

Run this script to get every fact you need for a specific book × state:

```bash
python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py <book_type> <state_slug>
```

**Examples:**
```bash
python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py study_guide texas
python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py 3_practice_tests california
python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py all_in_one new-york
```

**Helpful flags:**
```bash
python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py --list-states
python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py --list-book-types
```

The script outputs everything: book title (from titles.json), state name, curriculum name & acronym, exam name & acronym, chapter summaries with topic counts, features, use cases, series cross-sell descriptions, and design/quality claims.

**Do not make up any facts.** Everything comes from the script output.

## Step 2 — Write the HTML Description

Using the facts from Step 1, write a complete HTML product description following the rules below.

## Step 3 — Save the File

Save the description to:
```
final_output/<book_type>/<state_slug>_tpt_<YYYY-MM-DD>.html
```
Example: `final_output/study_guide/texas_tpt_2026-03-03.html`

---

## HTML Formatting Rules

### Allowed elements
- `<p>` for paragraphs
- `<b>` for bold text (section headings, key phrases, book title, state names, CTAs)
- `<i>` for occasional emphasis
- `<ul>` and `<li>` for bullet lists
- `<a href="..." target="_blank">` for links (footer only)
- The star separator line (footer only): `★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★`

### Forbidden
- **No `<h1>`, `<h2>`, or `<h3>`** — TPT already shows the product title as the page heading.
- **No `<hr>` dividers.**
- **No `<br>` tags** — use `<p>` for spacing.
- **No inline CSS or style attributes.**
- **No `<div>`, `<span>`, or any block-level wrappers.**

### Emoji rule
- **✅** may **only** appear as the **first character inside `<li>` bullet points**.
- Example: `<li>✅ Full lessons with clear explanations for every topic</li>`
- Do not use ✅ anywhere else — not in paragraphs, not in headings, not in table cells.

### Spacing
- Use `<p></p>` (empty paragraph) before section headings to create visual space.
- Section headings go inside `<b>` tags within a `<p>`.

---

## Required Sections

Every description must include **all** of these sections. You have **complete freedom** over the order, heading text, and presentation — but don't omit any.

### 1. Opening — Book-Type Content
State what the book is. Be direct.

- Use the **Title** and **Subtitle** from the script output — these are the official book title.
- The `<b>` heading should describe the book plainly: "Full Lessons, Examples, and Practice for Every Grade 7 Topic", "5 Full-Length STAAR Practice Tests", etc.
- Write **1 sentence** (max 2) that says what the book is and why it matters. That's it.
- Then immediately the `<ul>` of features — use ✅ before each `<li>`
- Include 3 design/quality features (always true for all books):
  - Colorful pages with illustrations, diagrams, and a friendly owl mascot
  - Answer key with explanations
  - Print and go / no prep needed
- Get the features from the script output. Rephrase them — don't copy verbatim.

### 2. Chapter Coverage
Show what the book covers. Use either:
- A `<ul>` compact list (e.g., `<li><b>Ch. 1: Ratios, Rates, and Percents</b> — 13 topics</li>`)

Must include the total topic count. Chapter data must match the script output exactly.

### 3. Curriculum Alignment
State that the book matches the state's curriculum standards.

- **Must** mention the full curriculum name and acronym (in `<b>`)
- **Must** mention the exam name and acronym if the state has one (in `<b>`)
- Make it clear this is built for this specific state — not a generic national resource
- Keep the language casual: "This follows Texas's TEKS standards" not "This resource is comprehensively aligned with the Texas Essential Knowledge and Skills framework"

### 4. Exam/Test Prep
If the state has an exam (most do), include a short section about test preparation.

- Reference the exam by name and acronym
- Be straightforward — don't oversell
- Skip this section entirely if the state has no exam

### 5. Use Cases
A bullet list showing who this book is for and how to use it.

- Use ✅ before each `<li>`
- Always include: classroom, homeschool, tutoring, parent-guided, test prep, and summer use cases
- Make the heading sound natural — "Who's This For?", "Great For", "Works Well For", etc.

### 6. Series Cross-Sell
Promote the other books in the state's series.

- The script already excludes the current book type — use the list it provides
- Each bullet should name the book in **bold** and give a one-line description
- Always use ✅ before each `<li>`
- Use a natural heading like "Want More?", "Looking for More?", "Need Lessons Too?" etc.

### 7. Closing CTA
1–2 short paragraphs. Keep it simple and confident.
- First: a brief outcome statement
- Second: a bold call to action (wrapped in `<b>`)

### 8. Footer (NEVER MODIFY)
Copy this footer **exactly** into every description. It starts with the `★★★★★` line and ends with the `– Dr. A. Nazari` paragraph. Never change any word, link, or punctuation.

```html
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

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
</p>
```

---

## Uniqueness Requirements

**Every description must be unique.** This is the most important part.

### Vary the structure
- Change the **order** of sections (except: opening is always first, footer always last)
- Sometimes lead with curriculum alignment, sometimes with features, sometimes with use cases
- Some descriptions might merge sections (e.g., combine test prep into curriculum alignment)

### Vary the headings
Never use the same `<b>` heading twice across descriptions for the same book type. Examples:

| Section | Example Headings (create your own too) |
|---|---|
| Features | "Here's What You're Getting", "What's Inside", "What You'll Find", "A Quick Look Inside" |
| Chapters | "All 44 Topics, Covered", "What's Covered", "50 Topics, 5 Chapters", "Here's the Breakdown" |
| Curriculum | "Made for Texas", "Follows TEKS Standards", "Written for Texas", "Matches Texas's Standards" |
| Test Prep | "Built-In STAAR Prep", "When Test Day Comes", "Helps With the STAAR Too" |
| Use Cases | "Who's This For?", "Great For", "Works Well For", "Who'll Get the Most Out of This" |
| Series | "Want More?", "Looking for More?", "Need Lessons Too?", "Check Out the Full Series" |

### Vary the prose
- Use contractions everywhere ("it's", "you'll", "don't", "here's")
- Keep sentences short. Mix short punchy statements with slightly longer ones.
- Be direct. "This book teaches every Grade 7 math skill" not "This comprehensive resource provides students with a complete learning experience."
- Talk to the reader. Use "you" and "your students".
- Vary paragraph lengths — some sections one sentence, others 2–3.
- Rephrase the features — don't copy them verbatim from the script.

---

## Grade 7 Math — Context

Grade 7 is the bridge to middle school math. The curriculum introduces abstract reasoning through algebra, deepens work with the number system (including negative numbers), and develops statistical thinking.

Five core chapters:
1. **Ratios, Rates, and Percents** — ratios, unit rates, percents, ratio tables, proportional reasoning
2. **The Number System** — fraction division, decimal operations, GCF/LCM, positive & negative numbers, absolute value, coordinate plane
3. **Expressions and Equations** — exponents, order of operations, writing/evaluating/simplifying expressions, one-step equations, inequalities
4. **Geometry: Area, Surface Area, and Volume** — area of triangles/parallelograms/trapezoids, volume, nets, surface area, coordinate geometry
5. **Statistics and Data** — statistical questions, mean/median, spread, dot plots, histograms, box plots

**Target audience:** Teachers, homeschool parents, tutors, and after-school coordinators working with 11–12 year old students.

---

## Book Type Quick Reference

| Book Type | Display Name | What It Is |
|---|---|---|
| `all_in_one` | All-in-One | Full lessons, worked examples, and practice for every topic |
| `study_guide` | Study Guide | Key concepts, essential examples, and quick practice |
| `workbook` | Workbook | Hundreds of practice problems organised by topic |
| `step_by_step` | Step-by-Step Guide | Numbered steps for every problem type |
| `in_30_days` | Math in 30 Days | Full curriculum in 30 daily lessons |
| `quiz` | Quizzes | One 15-minute quiz per topic |
| `puzzles` | Puzzles & Brain Teasers | Curriculum-aligned games and challenges |
| `worksheet` | Worksheets | Standalone printable activities by topic |
| `3_practice_tests` | 3 Practice Tests | 3 × 30 = 90 questions, full answer explanations |
| `5_practice_tests` | 5 Practice Tests | 5 × 30 = 150 questions, full answer explanations |
| `7_practice_tests` | 7 Practice Tests | 7 × 30 = 210 questions, full answer explanations |
| `10_practice_tests` | 10 Practice Tests | 10 × 30 = 300 questions, full answer explanations |

Practice test editions contain **different, non-overlapping tests**. Each edition is unique — the 3-test and 5-test books don't share any questions.

---

## Tone & Voice

**This should read like a real human wrote it.** Not a marketing team, not a chatbot, not a press release. Think of a teacher telling a colleague about a resource they actually like.

### Do This
- **Be brief.** Opening paragraphs: 1 sentence, max 2. People scan product listings.
- **Use contractions.** "It's", "you'll", "they're", "don't", "here's".
- **Keep sentences short.** If a sentence has a semicolon and two subordinate clauses, rewrite it.
- **Be direct.** "This book teaches every Grade 7 math skill."
- **Talk to the reader.** Use "you" and "your students".
- **State what the book does, plainly.** Good resources speak for themselves.

### Don't Do This
- **No storytelling.** Don't write "You know that student..." Just state what the book does.
- **No padding.** If a sentence adds no information, cut it.
- **No corporate buzzwords.** Never write "proven learning sequence", "carefully crafted", "drives instruction", "transforms mistakes into learning moments", "nothing left to chance".
- **No flowery filler.** Cut "something priceless", "exceptional", "unparalleled".
- **No marketing formulas.** Don't open with "pain point → solution → call to action".
- **Never use "proven".** Say what the book does and let people decide.
- **No robotic parallel structure.** "Learn → See → Do" sounds manufactured.

---

## Facts You Must Get Right

| Fact | Source |
|---|---|
| Book title | Script output (from titles.json) |
| State name | Script output |
| Curriculum name & acronym | Script output |
| Exam name & acronym | Script output (may be absent) |
| Chapter names, numbers, topic counts | Script output |
| Total topic count | Script output |
| Practice test count / questions | Script output |
| Features, use cases | Script output (rephrase, don't copy verbatim) |
| Series cross-sell | Script output |
| Footer HTML | Copy from SKILL.md (section 8 above) |

**Do not make up page counts.** If you want to mention length, use "~450 pages" for All-in-One, "~130 pages" for Study Guide, etc. — but it's better to just omit page counts.

**Do not invent exam testing months.** The script provides exam_months — if it says "(none)", don't guess.

---

## Checklist Before Saving

- [ ] All section headings use `<b>` tags (no `<h1>`, `<h2>`, etc.)
- [ ] All `<li>` bullets start with **✅**
- [ ] Chapter data (names, numbers, topic counts) matches script output exactly
- [ ] Curriculum name, acronym, exam name, and exam acronym are correct
- [ ] Total topic count is correct
- [ ] No `<h1>`, `<h2>`, `<hr>`, `<br>`, `<div>`, or `<span>` tags
- [ ] `<p></p>` before section headings for spacing
- [ ] Footer copied exactly from SKILL.md section 8 (from `★★★` to `– Dr. A. Nazari`)
- [ ] Description is genuinely **unique** — different from every other description you've written
- [ ] Read it out loud — does it sound like a real person wrote it?

---

## Example Workflow

```
User: "Write TPT descriptions for texas study_guide and texas workbook"

Agent:
1. Run: python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py study_guide texas
2. Read the facts output
3. Write the HTML description (unique structure, unique headings, unique prose)
4. Save to: final_output/study_guide/texas_tpt_2026-03-03.html
5. Run: python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py workbook texas
6. Read the facts output
7. Write the HTML description (different structure from the previous one!)
8. Save to: final_output/workbook/texas_tpt_2026-03-03.html
```