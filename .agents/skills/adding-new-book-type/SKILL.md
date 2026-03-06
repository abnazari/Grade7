---
name: adding-new-book-type
description: How to add a new book type to the Grade N math book publishing system. Covers initial pages, config entries, main .tex template, and build pipeline setup. Use when asked to create, add, or set up a new book type.
---

# Adding a New Book Type

This skill guides you through adding a new book type (e.g. study_guide, workbook, quiz) to the Grade N math book publishing system. The process is grade-independent — the same steps apply to Grade 3 through Grade 8.


## Step 0 — Gather Facts

**Before doing anything else**, run the facts script to get all the information you need:

```bash
python3 .agents/skills/adding-new-book-type/scripts/get_new_book_type_facts.py <book_type>
```

Example:
```bash
python3 .agents/skills/adding-new-book-type/scripts/get_new_book_type_facts.py study_guide
```

This prints a structured report with:
- **Grade & audience** — grade number, age range, tone guide, math level, design notes
- **Book type status** — whether config entries already exist
- **Files to create/edit** — exact paths and what's missing
- **Initial page specs** — what pages are required and design guidance for each
- **Common pages** — reusable pages that already exist (formula reference, vocabulary, etc.)
- **Chapter & topic structure** — all chapters and topics for content reference
- **Color palette** — every available color with hex values
- **Existing book types** — what other book types include, for cross-reference

Use `--list-types` to see all existing book types:
```bash
python3 .agents/skills/adding-new-book-type/scripts/get_new_book_type_facts.py --list-types
```

## Step 1 — Add Config Entries

Edit `scripts/config.py` and add entries to these dictionaries (if not already present):

### 1a. `BOOK_TYPES` dictionary

```python
"my_book": {
    "template": "my_book_main.tex",
    "output_subdir": "my_book",
    "description": "Human-readable description for CLI help",
    # For topic-based books:
    "topic_dirs": ("topics_my_book", "topics_my_book_modified", "topics_my_book_additional"),
    # For practice test books:
    # "test_range": (1, 3),
},
```

### 1b. `BOOK_DISPLAY_NAMES`

```python
"my_book": "My Book",
```

### 1c. `GENERIC_BOOK_TITLES`

```python
"my_book": (
    "Grade N Math My Book",           # title
    "Subtitle Goes Here",              # subtitle
),
```

### 1d. `_TITLE_TEMPLATES` (state-specific title templates)

```python
"my_book": (
    "{state} {exam} Grade {grade_n} Math My Book",
    "Subtitle with Keywords",
),
```

### 1e. `_TPT_TIERS` (TPT title variants, max 80 chars)

```python
"my_book": {
    "titles": [
        "{state} {exam} Grade {grade_n} Math My Book",
    ],
    "subtitles": [
        "Full Subtitle Here",        # longest first
        "Shorter Subtitle",           # progressively shorter
    ],
},
```

### 1f. `TOPIC_DIR_MAP` in `scripts/generate_state_books.py`

If the book type uses topics (not practice tests), also add to `TOPIC_DIR_MAP`:

```python
"my_book": ("topics_my_book", "topics_my_book_modified", "topics_my_book_additional"),
```

**Important**: If the new book type reuses the same topic files as another type (e.g. study_guide reuses the same `topics/` as all_in_one), point to the same directories.

### 1g. Pricing in `.env`

Add a line to the `.env` file:
```
PRICE_MY_BOOK=12.99
```

## Step 2 — Create Topic Directories (if applicable)

If the book type has its own topic files (not reusing another type's), create:

```
topics_my_book/           # core topic files
topics_my_book_modified/  # state-specific overrides
topics_my_book_additional/ # state-specific extras
```

Each topic file is a `.tex` file named like `ch01-01-what-is-a-ratio.tex`.

If reusing topics from another book type, just point `topic_dirs` at those existing directories.

## Step 3 — Write Initial Pages

This is the most important creative step. Initial pages serve as **TPT product thumbnails** — the first 3 pages are what buyers see in the online listing. They must be visually stunning.

### Directory structure

Create `initial_pages/<book_type>/` with numbered `.tex` files:

```
initial_pages/my_book/
├── 00-welcome.tex          # REQUIRED — full-page splash
├── 01-how-to-use.tex       # REQUIRED — book structure guide
└── 02-<specific>.tex       # REQUIRED — varies by type
```

### Common pages (reuse these — do NOT recreate)

These already exist in `initial_pages/common/` and can be `\input`'d by any book type:

| File | Purpose | Used by |
|------|---------|---------|
| `copyright_page.tex` | Legal title/copyright page | ALL book types (always first) |
| `formula-reference.tex` | Two-column formula reference sheet | Most types |
| `key-vocabulary.tex` | Math vocabulary glossary | study_guide, workbook, step_by_step, in_30_days |
| `what-youll-need.tex` | Supplies checklist | workbook, step_by_step |
| `preview-cta-page.tex` | "Get the Full Book" CTA for previews | Preview variants only |

### Design Rules — CRITICAL

**Print-friendly design** (teachers print these):
- Use **very light** background colors: `funTealLight`, `funBlueLight`, `funOrangeLight`, etc.
- Use **dark** colored fonts: `funTealDark`, `funBlueDark`, `funOrangeDark`, etc.
- **NEVER** use `black!N` patterns (e.g. `black!15`, `black!50`) — use the fun* color variants instead
- White card backgrounds (`colback=white`) with very light color frames (`colframe=funTeal!25`)
- Shadows should be barely visible (`shadow={1mm}{-1mm}{0mm}{funTeal!6}`)

**Brand colors**: Each book type gets a primary brand color. Check the facts script output for existing assignments and pick an unused or appropriate color.

**Content must be grade-appropriate**: The facts script reports the audience age, tone, and math level. Write welcome text, tips, and reference content that match the grade — NOT generic boilerplate.

### Page 1: Welcome (00-welcome.tex)

Full-page splash design using `tikzpicture[remember picture, overlay]`.

**Must include:**
- Colored header band across the top (dark brand color)
- Small-caps subtitle in the band (e.g. "YOUR GRADE 6 STUDY GUIDE")
- Large bold title in white (e.g. "Math Made Easy")
- Bullet-separated tagline (e.g. "Key Concepts • Worked Examples • Practice with Answers")
- Welcome message card (white `tcolorbox` with light frame)
- 3 feature cards at the bottom (each with an icon, title, and description)

**Structure:**
```latex
\thispagestyle{empty}
\begin{tikzpicture}[remember picture, overlay]
    % Light background fill
    \fill[funTealLight] (current page.south west) rectangle (current page.north east);
    % Dark header band
    \fill[funTealDark] (current page.north west) rectangle ([yshift=-6.5cm]current page.north east);
    % Title, tagline, welcome card, feature cards...
\end{tikzpicture}
\clearpage
```

### Page 2: How to Use (01-how-to-use.tex)

3–4 numbered steps, each in a `tcolorbox` card with a different accent color.

**Structure:**
```latex
\thispagestyle{empty}
{
\sffamily
% Header
\begin{center}
    {\fontsize{24}{28}\selectfont\bfseries\color{funTealDark} How to Use This Book}
    \smallskip
    {\normalsize\color{funGray} Brief description.}
\end{center}
\vspace{3mm}
{\centering\color{funTeal!30}\rule{0.55\textwidth}{1pt}\par}
\vspace{8mm}

% Step cards (cycle: Teal → Blue → Orange → Purple)
\begin{tcolorbox}[enhanced, colback=funTealLight, colframe=funTeal!20, arc=5pt, boxrule=0.5pt,
    left=10mm, right=6mm, top=3mm, bottom=3mm,
    overlay={\node[circle, fill=funTeal, inner sep=0pt, minimum size=24pt,
        text=white, font=\bfseries\small] at ([xshift=5mm]frame.west) {1};}]
    {\large\bfseries\color{funTealDark}Step title}\\[2pt]
    {\color{funGrayDark}Description text.}
\end{tcolorbox}
% ... more steps ...

% Suggestions box at bottom
\begin{tcolorbox}[enhanced, colback=funTeal!5, colframe=funTeal!25, arc=6pt, boxrule=0.6pt]
    {\bfseries\color{funTealDark}Ways to use this book:}
    % Two-column minipage with bullet points
\end{tcolorbox}
}
\clearpage
```

### Page 3: Type-Specific Page (02-*.tex)

This varies by book type:

| Book Type | Page Name | Content |
|-----------|-----------|---------|
| study_guide | 02-math-quick-reference.tex | 8 formula/fact cards in 2-column multicols |
| workbook | 02-whats-inside.tex | Chapter overview with topic lists in tcolorbox per chapter |
| step_by_step | 02-how-every-topic-works.tex | Visual breakdown of topic structure |
| in_30_days | 02-your-30-day-plan.tex | 30-row schedule table with Day/Topic/Checkbox |
| quiz | 02-quiz-tracker.tex | Score tracking table: Topic / Score / % / Retake |
| puzzles | 02-puzzle-tracker.tex | Grid of completion checkboxes |
| worksheet | (uses common formula-reference) | — |
| practice_tests | 02-test-strategies.tex | Test-taking strategy cards in 2 columns |

### Additional Pages (optional, varies by type)

Some book types have extra pages:

| Page | Purpose | Used by |
|------|---------|---------|
| `03-my-progress.tex` | Chapter-by-chapter progress tracker | workbook |
| `03-progress-tracker.tex` | Daily progress tracker | in_30_days |
| `03-what-youll-need.tex` | Supplies checklist | practice_tests |
| `06-my-test-tracker.tex` | Test score tracker | practice_tests |

## Step 4 — Create the Main Template File

Create `<book_type>_main.tex` in the workspace root. This is the master template that the build pipeline transforms into state-specific variants.

**Use this structure:**

```latex
% ============================================================================
% Grade N Math <Book Display Name>
% <Subtitle>
% ============================================================================
\documentclass[12pt, fleqn, openany]{studyGuide}
% Add optional packages here (e.g. \usepackage{VM_packages/VMfunWorkbook})

\setstretch{1.4}

\begin{document}

% ============================================================================
% COVER PAGE
% ============================================================================
\StateName{INSERT-STATE-NAME-HERE}
\CoverImage{images/covers/<book_type>.png}
\StateNameXOffset{4.1in}
\StateNameYOffset{6.2in}
\StateNameRotation{3}
\StateNameFontSize{40}
\StateNameColor{NavyBlue}
\makeCoverPage

% ============================================================================
% INITIAL PAGES
% ============================================================================
\pagenumbering{roman}

\renewcommand{\VMBookTitle}{Grade N Math <Title>}
\renewcommand{\VMBookSubtitle}{<Subtitle with \\ line breaks>}
\renewcommand{\VMFooterURL}{https://viewmath.com/gradeN}
\renewcommand{\VMFooterURLDisplay}{ViewMath.com/GradeN}
\input{initial_pages/common/copyright_page}

\input{initial_pages/<book_type>/00-welcome}
\input{initial_pages/<book_type>/01-how-to-use}
\input{initial_pages/<book_type>/02-<specific>}
% Optional: \input{initial_pages/common/formula-reference}
% Optional: \input{initial_pages/common/key-vocabulary}

\friendlyTOC
\pagenumbering{arabic}

% ============================================================================
% CHAPTERS
% ============================================================================
\chapter{Chapter Title}
\input{topics_<book_type>/ch01-01-topic-name}
% ... more topics ...

% ============================================================================
\printAnswerKey
\end{document}
```

**Key placeholders** (replaced by `generate_state_books.py`):
- `INSERT-STATE-NAME-HERE` → replaced with state display name
- Topic `\input` lines → adjusted per state (modified/additional topics swapped)

## Step 5 — Test the Build

Generate and compile for a single state to verify:

```bash
python3 scripts/generate_state_books.py --book-type <book_type> --states alabama --verbose
python3 scripts/compile_state_books.py --book-type <book_type> --states alabama
```

Check for:
1. **No LaTeX `!` errors** in the log: `grep '^\!' build/<book_type>_alabama-grade6/<book_type>_alabama-grade6.log`
2. **PDF opens correctly**: `open build/<book_type>_alabama-grade6/<book_type>_alabama-grade6.pdf`
3. **Page count is reasonable** for the book type
4. **Initial pages look correct** — especially the first 3 (TPT thumbnails)
5. **Column balance** on vocabulary/reference pages (no large empty spaces)

## Step 6 — Compile All States

Once the single-state test passes:

```bash
python3 scripts/generate_state_books.py --book-type <book_type> --verbose
python3 scripts/compile_state_books.py --book-type <book_type>
```

## Checklist

- [ ] `scripts/config.py` — `BOOK_TYPES` entry
- [ ] `scripts/config.py` — `BOOK_DISPLAY_NAMES` entry
- [ ] `scripts/config.py` — `GENERIC_BOOK_TITLES` entry
- [ ] `scripts/config.py` — `_TITLE_TEMPLATES` entry
- [ ] `scripts/config.py` — `_TPT_TIERS` entry
- [ ] `scripts/generate_state_books.py` — `TOPIC_DIR_MAP` entry (if topic-based)
- [ ] `.env` — `PRICE_<BOOK_TYPE>` pricing
- [ ] `images/covers/<book_type>.png` — cover image (graphic designer dependency)
- [ ] `initial_pages/<book_type>/00-welcome.tex` — welcome splash page
- [ ] `initial_pages/<book_type>/01-how-to-use.tex` — how to use guide
- [ ] `initial_pages/<book_type>/02-*.tex` — type-specific page
- [ ] `<book_type>_main.tex` — main template file
- [ ] Topic directories created (if new topics needed)
- [ ] Single-state test compile passes
- [ ] PDF visual review — initial pages look stunning
- [ ] All-state compile passes