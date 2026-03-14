---
name: tikz-improve-graphic
description: "Improve, fix, or beautify a TikZ graphic inside a practiceQuestion LaTeX block. Use when asked to improve, fix, beautify, redesign, or redraw a graph, dot plot, box plot, histogram, or number-line diagram in a question bank file. Accepts a dragged file + question ID (e.g. 8-3-q27) or a natural-language locator (e.g. 'first dot plot in ch08-03'). Rewrites the TikZ code in-place, then compiles an audit-review PDF and opens it for visual confirmation."
---

# Improve TikZ Graphic

## Overview

Locate a specific `\begin{tikzpicture}` block inside a `practiceQuestion`, rewrite it to be visually correct and polished, then compile a one-question audit-review PDF using `scripts/build_audit_review.py` so the user can inspect the result immediately.

## When to Use

- User drags/attaches a `.tex` file and says "improve the graphic for q27"
- User says "first graph in ch08-03", "the dot plot in question 8-3-q22", "fix the box plot", etc.
- User pastes a screenshot of a bad-looking TikZ diagram and asks for it to be redrawn

## Step 1 — Locate the Question

### From a question ID (most common)
User provides a file path + ID like `8-3-q27`.  
Read the file and find `\begin{practiceQuestion}{8-3-q27}`.

### From a natural-language locator
User says something like "the first histogram" or "the dot plot that shows push-ups".  
- Scan the file for `gmc` / `gsa` type questions containing relevant keywords.
- Confirm the match with the user if ambiguous.

## Step 2 — Understand the Graphic's Content (ACCURACY IS TOP PRIORITY)

This is a **math book**. Every number, data point, and label in the graphic **must be mathematically correct**. A beautiful graph with wrong data is worse than an ugly graph with correct data. Never trade accuracy for aesthetics.

Before touching any code, read the full `practiceQuestion` block carefully:

- **Question text**: what data, context, axis labels, and groups are described?
- **`\correctAnswer`**: what values / conclusions are expected? Use these to verify data accuracy.
- **`\explanation`**: contains the actual data values (means, medians, IQRs, individual values). This is the ground truth. **Never invent data. Never change data. Never approximate data.**
- **Question type**:
  - `gmc` — graphical multiple choice (student reads the graph to pick an answer)
  - `gsa` — graphical short answer (student reads the graph to compute/write an answer)

Extract every number that must appear in the graphic from the explanation. Cross-check every value twice before writing TikZ code.

## Step 3 — Identify the Graphic Type and Quality Issues

Common graphic types:

| Type | TikZ pattern |
|------|-------------|
| Dot plot | `\fill[color] (x,y) circle (4pt)` on a number line |
| Box plot | `\draw rectangle` + whiskers on a number line |
| Histogram | `\fill rectangle` bars above a horizontal axis |
| Side-by-side | Two copies of the same type stacked vertically using `\begin{scope}[yshift=...]` |

Common quality problems to fix:

- Labels (group names) overlapping dots, bars, or axes
- `\node[below]` "Hours" / axis label buried under the number line tick labels
- Second plot positioned using raw negative y offsets instead of a `\begin{scope}[yshift=...]`
- Dots starting at `y=0` so the lowest dot sits on the axis line
- Inconsistent dot spacing (`\y*0.4` off-by-one — first dot should clear the axis)
- Number line too short or too long for the data range
- Missing or misplaced axis-label ("Hours", "Temperature (°F)", etc.)
- Group labels placed `[below]` when there is already tick text below — prefer `[above]`
- Box plot whisker caps missing or misaligned

## Step 4 — Rewrite the TikZ Block

### Design philosophy

Create **beautiful, compact, and print-ready** graphics. You have creative freedom to choose the best visual representation — don't just patch the old code, redesign it if needed. Aim for graphs that a student would find clear and inviting.

Keep graphs compact — they share the page with question text, answer choices, and explanations. Avoid wasting vertical or horizontal space.

### Black-and-white accessibility

These books are often printed in **black and white**. Graphics must remain fully readable without color:

- **Differentiate groups by shape, not just color.** For example, use `\fill` (solid circles) for one group and open circles (`\draw ... circle`) for the other, or use different marker sizes, or squares vs circles.
- **Box plots**: use different fill patterns (solid fill vs hatched or lighter fill) so they're distinguishable in grayscale.
- **Histograms**: use different fill patterns (e.g., `funBlue!60` solid fill vs `funRed!60` with a drawn pattern or clearly different shade).
- **Labels** near each group's data are more important than a color legend — always label directly.

### General quality standards

1. **Alignment**: Both number lines in a side-by-side graphic must span the **same x range**.
2. **Separation**: Use `\begin{scope}[yshift=-Ncm]` for the second plot — never raw y-offsets like `-3.3`.
3. **Dot height**: First dot at `y = 0.5`, subsequent dots at `y = 0.1 + \y*0.4` for `\y in {1,2,...}`.
4. **Axis label**: Place the shared x-axis label (`Hours`, etc.) below the **lower** number line, with enough clearance that it doesn't overlap tick labels. Use `\node[below] at (midpoint, -1.2) {Label};` inside the lower scope.
5. **Group labels**: Use `\node[color, above] at (center_x, top_dot_y + 0.3) {\small Name};` — always above the dots, never below where tick labels live.
6. **Scale**: Use `scale=0.5` (or `0.45` for wide plots) consistently.
7. **Colors**: Use `funBlue` for the first group, `funRed` for the second group (project palette). But **never rely on color alone** — always pair with shape/pattern differences.
8. **Arrow**: Number line ends with `\draw[thick,->]`.
9. **Tick marks**: `\draw (\x, 0.15) -- (\x, -0.15) node[below, font=\tiny] {$\x$};`

### Dot plot recipe (side-by-side)

```latex
\begin{tikzpicture}[scale=0.5]
  % --- Group A ---
  \draw[thick,->] (xmin-0.5, 0) -- (xmax+0.5, 0);
  \foreach \x in {xmin,...,xmax}
    \draw (\x, 0.15) -- (\x, -0.15) node[below, font=\tiny] {$\x$};
  % dots: one \fill per value; stack multiples with \foreach \y in {1,...,N}
  \fill[funBlue] (val, 0.5) circle (4pt);           % single dot
  \foreach \y in {1,2} \fill[funBlue] (val, 0.1+\y*0.4) circle (4pt); % stack of 2
  \node[funBlue, above] at (center, topY+0.3) {\small Group A};

  % --- Group B (lower plot) ---
  \begin{scope}[yshift=-4cm]
    \draw[thick,->] (xmin-0.5, 0) -- (xmax+0.5, 0);
    \foreach \x in {xmin,...,xmax}
      \draw (\x, 0.15) -- (\x, -0.15) node[below, font=\tiny] {$\x$};
    % dots ...
    \node[funRed, above] at (center, topY+0.3) {\small Group B};
    \node[below] at (midpoint, -1.0) {Axis Label};
  \end{scope}
\end{tikzpicture}
```

### Box plot recipe (side-by-side)

```latex
% Box: \draw[thick, fill=color!30] (Q1, y-h) rectangle (Q3, y+h);
% Median: \draw[very thick, color] (med, y-h) -- (med, y+h);
% Whiskers: \draw[thick] (min, y) -- (Q1, y);  and  (Q3,y)--(max,y)
% Caps: \draw[thick] (min, y-cap) -- (min, y+cap);
```

### Histogram recipe

```latex
% Each bar: \fill[color!60] (left, 0) rectangle (right, height);
% Draw outline: \draw (left,0) rectangle (right, height);
% x-tick labels at mid-points of bins
```

## Step 5 — Edit the File

Use `replace_string_in_file` to replace only the `\begin{center} ... \end{center}` block that wraps the `tikzpicture`, keeping all other content in the `practiceQuestion` block unchanged.

Include at least 3 lines of unchanged context before and after the replaced block.

## Step 6 — Build and Open the PDF

Run the audit-review script to compile a single-question PDF:

```bash
python3 scripts/build_audit_review.py add \
    --chapter "Graphic Review" \
    PATH/TO/FILE.tex  QUESTION-ID

python3 scripts/build_audit_review.py open
```

- Use `"Graphic Review"` as the chapter title (keep it simple).
- Use the **relative** path from the workspace root.

## Step 7 — Report the Result

Tell the user:
- What quality issues were found and fixed (bullet list)
- What data values were plotted (so they can cross-check)
- Confirmation that the PDF is open

If the compilation fails, show the last 30 lines of the LaTeX error and fix the issue before retrying.

## Quality Checklist (self-check before completing)

### Accuracy (non-negotiable)
- [ ] Every data value in the graphic matches `\explanation` exactly — recount dots, recheck coordinates
- [ ] Axis range covers all data points with no value clipped or missing
- [ ] Tick labels match the values used in the question/explanation

### Visual quality
- [ ] Both number lines (if side-by-side) share the same x range
- [ ] Group labels are above their dots / bars, not overlapping tick labels
- [ ] Axis label is clearly visible below the lower number line
- [ ] Second group uses `\begin{scope}[yshift=-Ncm]` not raw y offsets
- [ ] Colors are `funBlue` / `funRed` (not default black or custom hex)
- [ ] Groups are distinguishable in **black-and-white** print (different shapes, fills, or sizes)
- [ ] Graph is compact — no excessive whitespace

### Build
- [ ] PDF compiled successfully and was opened
