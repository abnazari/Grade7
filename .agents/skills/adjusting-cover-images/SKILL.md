---
name: adjusting-cover-images
description: How to adjust state name positions on cover images for new states, new book types, or when cover images change.
---
# Adjusting Cover Page State Name Positions

## Overview

Each book type has a cover image with a label area where the state name is overlaid using TikZ. The state name position, font size, and other styling are controlled by `\StateNameXOffset`, `\StateNameYOffset`, `\StateNameFontSize`, and related commands in the main template `.tex` files. When a new cover image is added or an existing one changes, the offsets must be re-tuned so the state name fits perfectly inside the label area.

## When to Use This Skill

- A new cover image is added to `images/covers/`
- An existing cover image is replaced or resized
- A new book type is created and needs cover tuning
- The user asks to fix/adjust cover page labels

## Architecture

### Cover System

- **`VM_packages/VMfunCover.sty`** — Defines `\makeCoverPage`, which places a full-bleed background image and overlays the state name as a TikZ node.
- **Coordinate system** — `(xshift, yshift)` from the **south-west corner** (bottom-left) of the page. The node is **center-anchored**.
- **Page size** — US Letter: 8.5in × 11in.

### Key Commands (set before `\makeCoverPage`)

| Command | Default | Description |
|---------|---------|-------------|
| `\StateName{...}` | (empty) | The state display name |
| `\CoverImage{...}` | `images/cover-blank.png` | Path to the cover image |
| `\StateNameXOffset{...}` | `4in` | Horizontal offset from left edge |
| `\StateNameYOffset{...}` | `10in` | Vertical offset from bottom edge |
| `\StateNameRotation{...}` | `2` | Counter-clockwise rotation in degrees |
| `\StateNameFontSize{...}` | `45` | Font size in pt |
| `\StateNameBaselineSkip{...}` | `54` | Baseline skip in pt |
| `\StateNameColor{...}` | `black` | Any xcolor color name |
| `\StateNameFontStyle{...}` | `bold-sans` | Font style token |
| `\StateNameCustomFont{...}` | (empty) | Raw LaTeX font commands (when style = custom) |

### File Locations

| File | Role |
|------|------|
| `images/covers/` | Cover image files (`.png` or `.jpeg`) |
| `*_main.tex` (workspace root) | Main template files — **source of truth** for cover settings |
| `state_books/<state>/*.tex` | Generated per-state files (created by `generate_state_books.py`) |
| `scripts/generate_state_books.py` | Generates state `.tex` files from main templates |
| `scripts/compile_state_books.py` | Compiles state `.tex` files to PDF |

### Book Types and Their Templates

| Book Type Key | Main Template | Cover Image Reference |
|---------------|--------------|----------------------|
| `all_in_one` | `all_in_one_main.tex` | `images/covers/all_in_one.*` |
| `study_guide` | `study_guide_main.tex` | `images/covers/study_guide.*` |
| `workbook` | `workbook_main.tex` | `images/covers/workbook.*` |
| `step_by_step` | `steps_main.tex` | `images/covers/step_by_step.*` |
| `in_30_days` | `in30days_main.tex` | `images/covers/in_30_daysr.*` |
| `quiz` | `quiz_main.tex` | `images/covers/quiz.*` |
| `puzzles` | `puzzles_main.tex` | `images/covers/puzzle.*` |
| `worksheet` | `worksheet_main.tex` | `images/covers/worksheet.*` |
| `3_practice_tests` | `3_practice_tests_main.tex` | `images/covers/3_practice_tests.*` |
| `5_practice_tests` | `5_practice_tests_main.tex` | `images/covers/5_practice_tests.*` |
| `7_practice_tests` | `7_practice_tests_main.tex` | `images/covers/7_practice_tests.*` |
| `10_practice_tests` | `10_practice_tests_main.tex` | `images/covers/10_practice_tests.*` |

## Step-by-Step Workflow

### Step 1: Check Which Cover Images Exist

```bash
ls -la images/covers/
```

Compare with the `\CoverImage{...}` paths in each `*_main.tex`. Fix any mismatched extensions (e.g. `.jpeg` in template but `.png` on disk). Only book types with existing cover images can be compiled.

### Step 2: Choose the Test State

Use the **longest state name** so it fits the label area for all states. Currently that is **North Carolina** (14 characters). The slug is `north-carolina`.

To verify:
```bash
grep 'name:' topics_config.yaml | awk -F': ' '{print length($2), $2}' | sort -rn | head -5
```

### Step 3: Generate State Books

```bash
python3 scripts/generate_state_books.py --book-type all --states north-carolina --verbose
```

This creates 12 `.tex` files in `state_books/north-carolina/`.

### Step 4: Patch Files for Cover-Only Compilation

Insert `\end{document}` immediately after `\makeCoverPage` in every generated file so only the cover page is produced (1-page PDF, fast compilation):

```bash
for f in state_books/north-carolina/*.tex; do
  sed -i '' '/^\\makeCoverPage$/a\
\\end{document}\
% === COVER-ONLY: everything below is ignored ===
' "$f"
  echo "Patched: $f"
done
```

### Step 5: Initial Compilation

Compile all book types at once (only those with existing cover images will succeed):

```bash
python3 scripts/compile_state_books.py --book-type all --states north-carolina --passes 1
```

Output PDFs land in `final_output/<book_type>/north-carolina_<date>.pdf`.

### Step 6: Give the User Recompile Commands

After the initial compile, give the user **individual recompile commands** for each book type. The user will:
1. Open the PDF to check state name placement
2. Edit the offsets/font in `state_books/north-carolina/<book_type>_north-carolina-grade6.tex`
3. Recompile that single book type
4. Repeat until satisfied

**Recompile commands (copy-paste ready):**

```bash
# All-in-One
python3 scripts/compile_state_books.py --book-type all_in_one --states north-carolina --passes 1

# Study Guide
python3 scripts/compile_state_books.py --book-type study_guide --states north-carolina --passes 1

# Workbook
python3 scripts/compile_state_books.py --book-type workbook --states north-carolina --passes 1

# Step-by-Step
python3 scripts/compile_state_books.py --book-type step_by_step --states north-carolina --passes 1

# 3 Practice Tests
python3 scripts/compile_state_books.py --book-type 3_practice_tests --states north-carolina --passes 1

# 5 Practice Tests
python3 scripts/compile_state_books.py --book-type 5_practice_tests --states north-carolina --passes 1

# 7 Practice Tests
python3 scripts/compile_state_books.py --book-type 7_practice_tests --states north-carolina --passes 1

# 10 Practice Tests
python3 scripts/compile_state_books.py --book-type 10_practice_tests --states north-carolina --passes 1

# In 30 Days
python3 scripts/compile_state_books.py --book-type in_30_days --states north-carolina --passes 1

# Quiz
python3 scripts/compile_state_books.py --book-type quiz --states north-carolina --passes 1

# Puzzles
python3 scripts/compile_state_books.py --book-type puzzles --states north-carolina --passes 1

# Worksheet
python3 scripts/compile_state_books.py --book-type worksheet --states north-carolina --passes 1
```

**Recompile ALL at once:**

```bash
python3 scripts/compile_state_books.py --book-type all --states north-carolina --passes 1
```

### Step 7: Apply Confirmed Values to Main Templates

Once the user confirms the offsets are correct for all book types, read the final cover settings from each `state_books/north-carolina/*.tex` file and apply them to the corresponding `*_main.tex` template in the workspace root.

**What to copy:** The cover block between `% --- Cover layout options` and `\makeCoverPage`, specifically:
- `\CoverImage{...}` — especially the file extension
- `\StateNameXOffset{...}`
- `\StateNameYOffset{...}`
- `\StateNameRotation{...}`
- `\StateNameFontSize{...}`
- `\StateNameBaselineSkip{...}` (if uncommented)
- `\StateNameColor{...}` (if uncommented/changed)
- `\StateNameFontStyle{...}` (if uncommented/changed)

**Mapping from generated files to main templates:**

| Generated File | Main Template |
|---|---|
| `all_in_one_north-carolina-grade6.tex` | `all_in_one_main.tex` |
| `study_guide_north-carolina-grade6.tex` | `study_guide_main.tex` |
| `workbook_north-carolina-grade6.tex` | `workbook_main.tex` |
| `step_by_step_north-carolina-grade6.tex` | `steps_main.tex` |
| `in_30_days_north-carolina-grade6.tex` | `in30days_main.tex` |
| `quiz_north-carolina-grade6.tex` | `quiz_main.tex` |
| `puzzles_north-carolina-grade6.tex` | `puzzles_main.tex` |
| `worksheet_north-carolina-grade6.tex` | `worksheet_main.tex` |
| `3_practice_tests_north-carolina-grade6.tex` | `3_practice_tests_main.tex` |
| `5_practice_tests_north-carolina-grade6.tex` | `5_practice_tests_main.tex` |
| `7_practice_tests_north-carolina-grade6.tex` | `7_practice_tests_main.tex` |
| `10_practice_tests_north-carolina-grade6.tex` | `10_practice_tests_main.tex` |

## Important Notes

- **Only edit the main templates** — generated state files are overwritten by `generate_state_books.py`.
- **Always verify image extensions** — check what actually exists in `images/covers/` vs. what the template references. A `.jpeg` reference to a `.png` file will cause compilation failure.
- **The `\end{document}` patch is temporary** — it exists only in the test files under `state_books/north-carolina/`. After confirming and applying values to main templates, the NC files can be regenerated clean.
- **`--passes 1`** is sufficient for cover-only compilation (no cross-references needed for a single page).
- **Font size guidance** — "North Carolina" (14 chars) needs ~10-15% smaller font than short names like "Ohio" (4 chars). The system auto-centers, so font size is the main variable for fitting.
