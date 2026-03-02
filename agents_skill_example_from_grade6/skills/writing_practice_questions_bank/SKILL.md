---
name: writing_tests_questions_bank
description: How to write standard test question bank files for Grade 6 math topics used in state standard tests
---

# Writing Tests Question Bank Files

## Overview

For every topic in the study guide, we need a corresponding **question bank file** containing 30 standard test questions (18 multiple choice + 7 short answer + 5 graphical). These question banks feed into `scripts/generate_practice_tests.py`, which selects questions randomly to build unique per-state standard tests.

## Directory Structure

```
tests_questions_bank/
    topics/              # Questions for core CCSS topics (mirrors topics/)
    topics_additional/   # Questions for additional state-specific topics (mirrors topics_additional/)
    topics_modified/     # Questions for modified topics (mirrors topics_modified/)
```

Each question bank file corresponds **one-to-one** to a topic file:

| Topic file location | Question bank file location |
|---|---|
| `topics/ch01-01-what-is-a-ratio.tex` | `tests_questions_bank/topics/ch01-01-what-is-a-ratio.tex` |
| `topics_additional/ch02-12-integer-addition-and-subtraction.tex` | `tests_questions_bank/topics_additional/ch02-12-integer-addition-and-subtraction.tex` |
| `topics_modified/ch01-04-finding-the-unit-rate.tex` | `tests_questions_bank/topics_modified/ch01-04-finding-the-unit-rate.tex` |

**Use the exact same filename** as the topic file it corresponds to.

## Workflow: How to Write Question Banks

### Step 1: Read the Topic File

Before writing questions, **always read the corresponding topic file first**. The topic file tells you:
- What concepts are taught
- What vocabulary is introduced
- What difficulty level is appropriate
- What types of problems students have already seen
- What visual representations are used (number lines, coordinate planes, fraction bars, etc.)

Your questions must test the content taught in that specific topic — not content from other topics. Stay within scope.

### Step 2: Create the Question Bank File

Use the exact format shown below. Every file has:
- A header comment block with metadata
- 18 multiple choice questions (IDs: `X-Y-q01` through `X-Y-q18`)
- 7 short answer questions (IDs: `X-Y-q19` through `X-Y-q25`)
- 5 graphical questions (IDs: `X-Y-q26` through `X-Y-q30`) — 3 graphical MC + 2 graphical SA
- For modified files, the ID should reflect the modified topic (e.g., `m-X-Y-q01` instead of `X-Y-q01`)

### Step 3: Verify Correctness

Double-check every answer. An incorrect answer in a standard test destroys student trust. Compute each answer carefully.

## File Format

### Header Block

```latex
% ============================================================
% Question Bank: chXX-YY Topic Title
% Topic Title: Full Topic Title
% CCSS: 6.XX.X.X (or "Supplementary" for non-CCSS topics)
% Questions: 30 (18 MC + 7 SA + 5 Graphical)
% ============================================================
```

### Question ID Convention

IDs follow the pattern `{chapter}-{section}-q{number}`:
- `ch01-01` → IDs are `1-1-q01` through `1-1-q30` (q01–q18 MC, q19–q25 SA, q26–q30 Graphical)
- `ch03-05` → IDs are `3-5-q01` through `3-5-q30`
- `ch05-07` → IDs are `5-7-q01` through `5-7-q30`
- For additional topics, use the same chapter-section pattern (e.g., `ch02-12` → IDs are `2-12-q01` through `2-12-q30`)
- For modified topics, prefix with `m-` to indicate modified content (e.g., `m-2-6-q01` for a question in the modified version of chapter 2, section 6)

Strip the leading zero from the chapter number. Keep the section number as-is (including leading zeros for single digits, but without the `ch` prefix).

### Multiple Choice Question Format

```latex
\begin{practiceQuestion}{X-Y-q01}{mc}
\begin{questionText}
Question text goes here. Can span multiple lines.
Supports any LaTeX content: math, tables, TikZ, etc.
\end{questionText}
\choiceA{First option}
\choiceB{Second option}
\choiceC{Third option}
\choiceD{Fourth option}
\correctAnswer{B}
\explanation{Brief explanation of why B is correct.}
\end{practiceQuestion}
```

### Short Answer Question Format

```latex
\begin{practiceQuestion}{X-Y-q19}{sa}
\begin{questionText}
Question text goes here.
\end{questionText}
\correctAnswer{$42$}
\explanation{Brief explanation of how to get the answer. You should end up with the correct answer}
\end{practiceQuestion}
```

### Graphical Multiple Choice Question Format (`gmc`)

Graphical questions include a TikZ figure or visual command as a core part of the question. The graphic is essential — students must interpret it to answer.

```latex
\begin{practiceQuestion}{X-Y-q26}{gmc}
\begin{questionText}
Look at the number line below. Which point represents $-3$?

\begin{center}
\numberLine[1]{-5}{5}
\end{center}
\end{questionText}
\choiceA{Point A}
\choiceB{Point B}
\choiceC{Point C}
\choiceD{Point D}
\correctAnswer{B}
\explanation{$-3$ is $3$ units to the left of $0$ on the number line.}
\end{practiceQuestion}
```

### Graphical Short Answer Question Format (`gsa`)

```latex
\begin{practiceQuestion}{X-Y-q29}{gsa}
\begin{questionText}
What is the area of the shaded triangle shown on the coordinate plane below?

\begin{center}
\begin{tikzpicture}[scale=0.5]
  \draw[step=1,gray!30,thin] (0,0) grid (8,6);
  \draw[thick,->] (0,0) -- (8.5,0) node[right]{$x$};
  \draw[thick,->] (0,0) -- (0,6.5) node[above]{$y$};
  \fill[funBlue!30] (1,1) -- (7,1) -- (4,5) -- cycle;
  \draw[thick,funBlue] (1,1) -- (7,1) -- (4,5) -- cycle;
  \node[below] at (1,1) {$(1,1)$};
  \node[below] at (7,1) {$(7,1)$};
  \node[above] at (4,5) {$(4,5)$};
\end{tikzpicture}
\end{center}
\end{questionText}
\correctAnswer{$12$ square units}
\explanation{Base $= 7 - 1 = 6$, height $= 5 - 1 = 4$. Area $= \frac{1}{2} \times 6 \times 4 = 12$ square units.}
\end{practiceQuestion}
```

### Visual Tools for Graphical Questions

You have **full creative freedom** to build graphics that serve the question. Use whichever approach produces the clearest, most relevant visual:

- **Built-in commands** from `VMfunMath.sty` (see reference table below) — quick and consistent
- **Custom inline TikZ** — for anything the built-in commands can't express
- **LaTeX tables, `tabular`, or `minipage`** — for structured data displays
- **Any combination** of the above within `\begin{center}...\end{center}`

Do NOT feel limited to the built-in commands. If a custom TikZ diagram better serves the question, write one. The goal is **clarity**, not using a specific command.

#### Built-in Visual Commands Reference

These are convenience commands from `VMfunMath.sty`. Use them when they fit naturally:

| Command | Description | Example |
|---|---|---|
| `\numberLine[step]{start}{end}` | Number line with ticks | `\numberLine[1]{-5}{5}` |
| `\fractionBar[color]{num}{den}` | Shaded fraction bar | `\fractionBar{3}{4}` |
| `\fractionCircle[color]{num}{den}` | Shaded fraction circle | `\fractionCircle{1}{4}` |
| `\numberLineFraction[color]{den}` | Fraction number line (0 to 1) | `\numberLineFraction{6}` |
| `\barGraph[color]{labels}{values}{ylabel}` | Bar graph | (see VMfunMath.sty) |
| `\areaGrid[color]{rows}{cols}` | Area model (filled squares) | `\areaGrid{3}{5}` |
| `\perimeterRect[color]{length}{width}{unit}` | Rectangle with labeled sides | `\perimeterRect{8}{5}{cm}` |
| `\arrayGrid[color]{rows}{cols}` | Dot array (rows × columns) | `\arrayGrid{3}{4}` |
| `\dotGroups[color]{groups}{per}` | Grouped dots | `\dotGroups{5}{3}` |
| `\numberBond[color]{whole}{part1}{part2}` | Number bond diagram | `\numberBond{12}{4}{8}` |
| `\baseTenBlocks{hundreds}{tens}{ones}` | Base-10 block drawing | `\baseTenBlocks{2}{3}{5}` |
| `\factFamily{a}{b}{c}` | Fact family triangle | `\factFamily{3}{7}{21}` |
| `\skipCountArc[color]{start}{end}{step}` | Skip counting on number line | `\skipCountArc{0}{20}{4}` |
| `\columnAdd{num1}{num2}` | Column addition layout | `\columnAdd{345}{278}` |
| `\columnSub{num1}{num2}` | Column subtraction layout | `\columnSub{503}{278}` |
| `\placeValueTable{headers}{row1}{row2}` | Place value chart | (see VMfunMath.sty) |
| `\tallyMarks{count}` | Tally mark drawing | `\tallyMarks{13}` |
| `\ruler{length}{unit}` | Ruler drawing | `\ruler{12}{cm}` |
| `\funCompare{left}{symbol}{right}` | Comparison display | `\funCompare{3.5}{>}{3.05}` |
| `\equalSharing[color]{total}{groups}` | Equal sharing diagram | `\equalSharing{12}{3}` |

#### Custom TikZ Example

```latex
\begin{center}
\begin{tikzpicture}
  % Custom graphic — use whatever TikZ you need
\end{tikzpicture}
\end{center}
```

### Key Format Rules

1. **`questionText` is an environment**, not a command. Always use `\begin{questionText}...\end{questionText}`, never `\questionText{...}`. This allows complex multi-line content including TikZ, tables, and graphs inside the question.
2. **Type is `mc`, `sa`, `gmc`, or `gsa`** — the second argument to `practiceQuestion`.
3. **MC/GMC questions have exactly 4 choices**: `\choiceA{}` through `\choiceD{}`.
4. **SA/GSA questions have NO choices** — only `\correctAnswer{}` and `\explanation{}`.
5. **`\correctAnswer{}`** for MC/GMC is the letter (A, B, C, or D). For SA/GSA it is the actual answer.
6. **`\explanation{}`** is required for every question. Keep it to 1–2 sentences.
7. **All math must be in `$...$`**. Use `\times` for multiplication, `\div` for division.
8. **No blank lines** between `\choiceA` through `\choiceD` lines.
9. **Separate questions** with a blank line between `\end{practiceQuestion}` and the next `\begin{practiceQuestion}`.
10. **Graphical questions** (`gmc`/`gsa`) must include a TikZ figure, visual command, or table inside `questionText`. The visual is the core of the question — not a decoration.

## Complete Example File

```latex
% ============================================================
% Question Bank: ch02-04 GCF and LCM
% Topic Title: Greatest Common Factor and Least Common Multiple
% CCSS: 6.NS.B.4
% Questions: 30 (18 MC + 7 SA + 5 Graphical)
% ============================================================

% --- Multiple Choice Questions (18) ---

\begin{practiceQuestion}{2-4-q01}{mc}
\begin{questionText}
What is the greatest common factor (GCF) of $18$ and $24$?
\end{questionText}
\choiceA{$3$}
\choiceB{$6$}
\choiceC{$12$}
\choiceD{$18$}
\correctAnswer{B}
\explanation{Factors of $18$: $1, 2, 3, 6, 9, 18$. Factors of $24$: $1, 2, 3, 4, 6, 8, 12, 24$. The largest they share is $6$.}
\end{practiceQuestion}

\begin{practiceQuestion}{2-4-q02}{mc}
\begin{questionText}
What is the least common multiple (LCM) of $4$ and $6$?
\end{questionText}
\choiceA{$2$}
\choiceB{$12$}
\choiceC{$24$}
\choiceD{$6$}
\correctAnswer{B}
\explanation{Multiples of $4$: $4, 8, 12, \ldots$ Multiples of $6$: $6, 12, \ldots$ The smallest they share is $12$.}
\end{practiceQuestion}

% ... (q03 through q18 follow the same pattern) ...

% --- Short Answer Questions (7) ---

\begin{practiceQuestion}{2-4-q19}{sa}
\begin{questionText}
Find the GCF of $36$ and $48$.
\end{questionText}
\correctAnswer{$12$}
\explanation{$36 = 2^2 \times 3^2$ and $48 = 2^4 \times 3$. GCF $= 2^2 \times 3 = 12$.}
\end{practiceQuestion}

% ... (q20 through q25 follow the same pattern) ...

% --- Graphical Questions (3 GMC + 2 GSA) ---

\begin{practiceQuestion}{2-4-q26}{gmc}
\begin{questionText}
The Venn diagram below shows the prime factors of two numbers. What is the GCF of the two numbers?

\begin{center}
\begin{tikzpicture}
  \draw (0,0) circle (1.4) node[above=1.2cm] {$30$};
  \draw (2,0) circle (1.4) node[above=1.2cm] {$42$};
  \node at (-0.7,0) {$5$};
  \node at (1,0.3) {$2$};
  \node at (1,-0.3) {$3$};
  \node at (2.7,0) {$7$};
\end{tikzpicture}
\end{center}
\end{questionText}
\choiceA{$5$}
\choiceB{$6$}
\choiceC{$7$}
\choiceD{$35$}
\correctAnswer{B}
\explanation{The shared (overlapping) prime factors are $2$ and $3$, so GCF $= 2 \times 3 = 6$.}
\end{practiceQuestion}

% ... (q27–q28 are gmc, q29–q30 are gsa) ...
```

## Question Writing Guidelines

### Difficulty Distribution

Aim for a mix across the 30 questions:
- **10–11 basic** — straightforward recall or single-step computation
- **9–10 applied** — word problems, multi-step, or conceptual understanding
- **4–5 challenging** — requires deeper thinking, combines sub-skills, or uses less obvious numbers
- **5 graphical** — questions where students interpret a diagram, chart, graph, or visual model

### Question Quality Checklist

- [ ] **On-topic**: Every question tests content from THIS topic file only
- [ ] **Grade-appropriate**: Numbers and language suitable for 11–12 year olds
- [ ] **Unique**: No two questions test the exact same thing with different numbers
- [ ] **Plausible distractors**: MC wrong answers should be common mistakes (not random numbers)
- [ ] **Correct answers**: Triple-check every answer is mathematically correct
- [ ] **Clear wording**: Short sentences, everyday language, no ambiguity
- [ ] **Math in `$...$`**: All numbers in equations use math mode
- [ ] **Explanation provided**: Every question has a brief, helpful explanation
- [ ] **Graphical clarity** (for `gmc`/`gsa`): The graphic shows ALL relevant info, is labeled, and an 11-year-old can instantly understand what it represents and how it connects to the question

### Writing Good Distractors (multiple choice wrong answers)

Wrong answers should reflect real student mistakes:
- **Sign errors**: e.g., $-3 + 5 = -2$ instead of $2$
- **Operation confusion**: e.g., adding instead of multiplying, confusing GCF and LCM
- **Fraction/decimal errors**: e.g., forgetting to find a common denominator
- **Partial computation**: e.g., only doing the first step of a two-step problem
- **Common misconceptions**: e.g., thinking $|-5| = -5$, or that dividing by a fraction makes smaller
- **Order-of-operations errors**: e.g., adding before multiplying

**Never** use obviously absurd distractors. Every option should look plausible to a student who has a specific misconception.

### Writing Good Short Answer Questions

SA questions should require the student to produce an answer, usually a very short one (a number, expression, or short phrase).

Keep `\correctAnswer{}` brief — a number, expression, or short phrase.

### Numbers and Scope by Chapter

Follow these constraints to stay aligned with Grade 6 standards:

| Chapter | Number Range | Key Constraints |
|---|---|---|
| Ch 1 (Ratios, Rates, and Percents) | Whole numbers, simple fractions, decimals, percents | Ratios in all three forms; unit rates with division; ratio tables and double number lines; percent as rate per 100; measurement unit conversions |
| Ch 2 (The Number System) | Integers, fractions, decimals (positive & negative); multi-digit whole numbers | Fraction ÷ fraction; multi-digit division; all four decimal operations; GCF (≤ 100), LCM (≤ 12); positive/negative numbers; absolute value; coordinate plane (all four quadrants) |
| Ch 3 (Expressions and Equations) | Whole-number exponents; one variable; coefficients may be fractions | Exponents and order of operations; translating words ↔ expressions; evaluating expressions; distributive property; one-step equations (x + p = q, px = q); inequalities on number lines; dependent/independent variables |
| Ch 4 (Geometry: Area, Surface Area, Volume) | Lengths may be fractions/decimals; coordinates may be negative | Area of triangles, parallelograms, trapezoids; volume V = lwh with fractional edges; polygons on coordinate plane; nets and surface area |
| Ch 5 (Statistics and Data) | Data sets of 10–25 values; values may be decimals or integers | Statistical questions; center (mean, median), spread (range, IQR, MAD); dot plots, histograms, box plots; summarize and compare data sets |

### Using Complex Content in `questionText`

The `\begin{questionText}...\end{questionText}` environment supports any LaTeX content. For topics that benefit from visuals, you can include tables, TikZ graphics, or other environments inside the question text.

### Writing Good Graphical Questions (`gmc` / `gsa`)

Graphical questions use a visual element (TikZ diagram, chart, coordinate plane, number line, etc.) as the **core** of the question. The student must interpret the visual to answer — the graphic is not decoration.

**Structure**: 5 graphical questions per file (IDs q26–q30), placed after the SA questions:
- **q26, q27, q28** → graphical multiple choice (`gmc`) — same structure as `mc` but with a visual in `questionText`
- **q29, q30** → graphical short answer (`gsa`) — same structure as `sa` but with a visual in `questionText`

#### Clarity is Everything

The #1 rule for graphical questions: **an 11-year-old must instantly understand what the graphic shows and how it relates to the question.** If there is any ambiguity, rewrite the question or redesign the graphic.

Before writing each graphical question, ask yourself:
1. Can a student answer this question ONLY by looking at the graphic? (If yes, good.)
2. Does the graphic show ALL the information the student needs? (If not, fix it.)
3. Would removing the graphic make the question unanswerable? (If yes, good.)
4. Is there any way a student could misread what the graphic represents? (If yes, add labels or redesign.)

#### Guidelines

1. **The visual IS the question** — the student MUST read the visual to answer. The question without the graphic should be incomplete or unanswerable.
2. **The visual must show ALL relevant information** — if a question compares two things, the graphic must show BOTH things. Showing only one side of a comparison is confusing and misleading.
3. **Label clearly** — add text labels, arrows, or annotations inside TikZ when the meaning isn't obvious. Never assume the student will guess what the shapes represent.
4. **Wrap visuals in `\begin{center}...\end{center}`** for proper alignment.
5. **Use any tool that works** — built-in commands, custom TikZ, tables, or combinations. Choose whatever produces the clearest visual for THIS specific question.
6. **Keep visuals compact** — they must fit neatly inside the question box. Avoid overly large diagrams.
7. **Match the topic** — the visual type should feel natural for the concept being tested.
8. **Vary the visual types** — don't use the same visual approach for all 5 questions in a file.

#### GOOD vs BAD Graphical Questions

**BAD** — graphic is unrelated or partially related to the question:
```
Question: "A student says the GCF of 12 and 18 is 3. Is the student correct?"
Graphic: [a Venn diagram showing only the factors of 12]
Problem: The question asks about common factors of TWO numbers, but the
         graphic only shows ONE number's factors. The student has no
         reference for 18. This is confusing, not helpful.
```

**GOOD** — graphic shows exactly what the question asks about:
```
Question: "Look at the Venn diagram of prime factors below. What is the GCF?"
Graphic: [Venn diagram with left circle for 12, overlap for shared factors,
         right circle for 18]
Why it works: The student can SEE the shared factors in the overlap.
```

**BAD** — graphic is decorative, not essential:
```
Question: "What is the absolute value of -7?"
Graphic: [a number line from -10 to 10 with -7 marked]
Problem: The number line doesn't add anything — the student still has to
         recall the definition. The graphic is decoration.
```

**GOOD** — graphic is the core of the problem:
```
Question: "Look at the number line. What is the distance between point A
          and point B?"
Graphic: [number line with A at -3 and B at 4, clearly labeled]
Why it works: The student must read both coordinates and find the distance.
```

**BAD** — graphic doesn't match the question's intent:
```
Question: "Find the area of a triangle with base 8 and height 5."
Graphic: [a rectangle labeled 8 × 5]
Problem: The question asks about a triangle but shows a rectangle.
         This is misleading.
```

**GOOD** — graphic makes the student think:
```
Question: "What is the area of the shaded region?"
Graphic: [a composite shape on a grid — rectangle with a triangle cut out,
         all vertices labeled]
Why it works: The student must decompose the shape and compute.
```

#### Topic-to-visual Suggestions (not exhaustive — use creative judgment)

| Topic Area | Natural Visual Types |
|---|---|
| Ratios & Rates (Ch 1) | Tape diagrams, ratio tables, double number lines, coordinate graphs of ratio pairs, bar models |
| Percents (Ch 1) | 10 × 10 grids, bar models showing part/whole, comparison bar diagrams |
| Number System (Ch 2) | Number lines with integers and fractions, coordinate planes (all four quadrants), Venn diagrams for GCF/LCM |
| Expressions & Equations (Ch 3) | Balance/scale diagrams for equations, input-output tables, inequality number lines with open/closed circles |
| Geometry (Ch 4) | Triangles/parallelograms/trapezoids on grids, nets of 3D shapes, coordinate plane polygons, unit-cube volume diagrams |
| Statistics & Data (Ch 5) | Dot plots, histograms, box plots, side-by-side comparison displays, frequency tables |


## Full Topic List — Files to Create

### Core Topics → `tests_questions_bank/topics/`

Create one question bank file for each of the 44 core topic files in `topics/`. These are derived directly from `topics_config.yaml`:

| File | Topic |
|---|---|
| `ch01-01-what-is-a-ratio.tex` | What Is a Ratio? |
| `ch01-02-using-ratio-language.tex` | Using Ratio Language |
| `ch01-03-what-is-a-rate.tex` | What Is a Rate? |
| `ch01-04-finding-the-unit-rate.tex` | Finding the Unit Rate |
| `ch01-05-tables-of-equivalent-ratios.tex` | Tables of Equivalent Ratios |
| `ch01-06-graphing-ratios.tex` | Graphing Ratios |
| `ch01-07-what-is-a-percent.tex` | What Is a Percent? |
| `ch01-08-solving-percent-problems.tex` | Solving Percent Problems |
| `ch01-09-solving-rate-and-ratio-word-problems.tex` | Solving Rate and Ratio Word Problems |
| `ch01-10-converting-measurement-units.tex` | Converting Measurement Units |
| `ch02-01-dividing-fractions-by-fractions.tex` | Dividing Fractions by Fractions |
| `ch02-02-multi-digit-division.tex` | Multi-Digit Division |
| `ch02-03-decimal-operations.tex` | Decimal Operations |
| `ch02-04-gcf-and-lcm.tex` | Greatest Common Factor and Least Common Multiple |
| `ch02-05-distributive-property-with-common-factors.tex` | The Distributive Property with Common Factors |
| `ch02-06-understanding-positive-and-negative-numbers.tex` | Understanding Positive and Negative Numbers |
| `ch02-07-opposites-and-absolute-value.tex` | Opposites and Absolute Value |
| `ch02-08-rational-numbers-on-the-number-line.tex` | Rational Numbers on the Number Line |
| `ch02-09-the-coordinate-plane.tex` | The Coordinate Plane |
| `ch02-10-comparing-and-ordering-rational-numbers.tex` | Comparing and Ordering Rational Numbers |
| `ch02-11-distance-on-the-coordinate-plane.tex` | Distance on the Coordinate Plane |
| `ch03-01-exponents-and-order-of-operations.tex` | Exponents and Order of Operations |
| `ch03-02-translating-words-into-expressions.tex` | Translating Words into Expressions |
| `ch03-03-terms-factors-and-coefficients.tex` | Terms, Factors, and Coefficients |
| `ch03-04-evaluating-expressions.tex` | Evaluating Expressions |
| `ch03-05-equivalent-expressions.tex` | Equivalent Expressions |
| `ch03-06-variables-in-real-world-problems.tex` | Variables in Real-World Problems |
| `ch03-07-solving-one-step-equations.tex` | Solving One-Step Equations |
| `ch03-08-writing-inequalities.tex` | Writing Inequalities |
| `ch03-09-graphing-inequalities-on-a-number-line.tex` | Graphing Inequalities on a Number Line |
| `ch03-10-two-quantities-that-change-together.tex` | Two Quantities That Change Together |
| `ch04-01-area-of-triangles.tex` | Area of Triangles |
| `ch04-02-area-of-parallelograms-and-trapezoids.tex` | Area of Parallelograms and Trapezoids |
| `ch04-03-volume-of-rectangular-prisms.tex` | Volume of Rectangular Prisms |
| `ch04-04-polygons-on-the-coordinate-plane.tex` | Polygons on the Coordinate Plane |
| `ch04-05-finding-area-on-the-coordinate-plane.tex` | Finding Area on the Coordinate Plane |
| `ch04-06-nets-and-surface-area.tex` | Nets and Surface Area |
| `ch05-01-statistical-questions.tex` | Statistical Questions |
| `ch05-02-describing-data-center-spread-shape.tex` | Describing Data: Center, Spread, and Shape |
| `ch05-03-mean-and-median.tex` | Mean and Median |
| `ch05-04-measures-of-spread.tex` | Measures of Spread |
| `ch05-05-dot-plots-and-histograms.tex` | Dot Plots and Histograms |
| `ch05-06-box-plots.tex` | Box Plots |
| `ch05-07-summarizing-data-and-making-comparisons.tex` | Summarizing Data and Making Comparisons |

### Additional Topics → `tests_questions_bank/topics_additional/`

Create one question bank file for each of the 13 additional topic files in `topics_additional/`. These map to the `additional_topics` list in `topics_config.yaml`:

| File | Topic | States That Use It |
|---|---|---|
| `ch01-11-personal-financial-literacy.tex` | Personal Financial Literacy | CO, FL, MN, OK, TX |
| `ch01-12-proportional-vs-non-proportional.tex` | Proportional vs. Non-Proportional Relationships | MN, TX |
| `ch01-13-financial-literacy-budgeting-and-saving.tex` | Financial Literacy — Budgeting and Saving | CO, TX |
| `ch01-14-ratios-with-scale-drawings.tex` | Ratios with Scale Drawings | OK |
| `ch02-12-integer-addition-and-subtraction.tex` | Integer Addition and Subtraction | FL, MN, OK, SC, TX, VA |
| `ch02-13-integer-multiplication-and-division.tex` | Integer Multiplication and Division | FL, OK, SC, TX, VA |
| `ch02-14-compute-with-integers-in-context.tex` | Compute with Integers in Context | AK |
| `ch04-07-transformations-on-the-coordinate-plane.tex` | Transformations on the Coordinate Plane | IN, VA |
| `ch04-08-area-of-circles-introduction.tex` | Area of Circles Introduction | IN, MN, NE, VA |
| `ch05-08-introduction-to-probability.tex` | Introduction to Probability | FL, GA, IN, MN, NE, OK, VA |
| `ch05-09-stem-and-leaf-plots.tex` | Stem-and-Leaf Plots | FL, OK, TX |
| `ch05-10-circle-graphs.tex` | Circle Graphs | MN, VA |
| `ch05-11-data-displays-extended.tex` | Data Displays Extended | AK, IN, OK |

### Modified Topics → `tests_questions_bank/topics_modified/`

Create one question bank file for each modified topic file in `topics_modified/`. These are state-specific variants of core topics; each file replaces the standard version for the states listed. Read the **modified** file (not the original in `topics/`) before writing questions:

| File | Topic | States | What Changed |
|---|---|---|---|
| `ch01-04-finding-the-unit-rate.tex` | Finding the Unit Rate | TX | TX financial literacy emphasis — unit pricing, grocery brand comparison, phone plans, streaming services |
| `ch01-07-what-is-a-percent.tex` | What Is a Percent? | MN, TX | Proportional + financial literacy — sales tax, discount, tip calculations; percent-as-ratio connection |
| `ch01-08-solving-percent-problems.tex` | Solving Percent Problems | TX | TX PFL emphasis — tax/tip/markup/markdown contexts; simple interest preview with I = P × r × t |
| `ch01-09-solving-rate-and-ratio-word-problems.tex` | Solving Rate and Ratio Word Problems | OK | OK estimation emphasis — adds estimation as 5th strategy; estimate-first + reasonableness check in every problem |
| `ch02-06-understanding-positive-and-negative-numbers.tex` | Understanding Positive and Negative Numbers | AK, FL, MN, OK, TX, VA | Integer addition preview — number-line addition model, same-sign/different-sign rules, bank-balance word problem |
| `ch02-07-opposites-and-absolute-value.tex` | Opposites and Absolute Value | FL, TX, VA | Financial absolute value — comparing account debts, profit-vs-loss distance from break-even |
| `ch04-04-polygons-on-the-coordinate-plane.tex` | Polygons on the Coordinate Plane | IN, VA | Reflection preview — x-axis flips y-sign, y-axis flips x-sign; point and triangle reflection practice |
| `ch05-03-mean-and-median.tex` | Mean and Median | AK | Culturally responsive Alaskan contexts — salmon catch, Fairbanks temperatures, moose survey, Anchorage snowfall |
| `ch05-05-dot-plots-and-histograms.tex` | Dot Plots and Histograms | FL, IN, MN, OK, TX, VA | Adds frequency tables and mode; restructured to "Three Ways to Display Data"; categorical-vs-numerical choice problem |
| `ch05-06-box-plots.tex` | Box Plots | TX | Interpretation/comparison focus — two-class box plot comparison; whisker interpretation; less raw IQR computation |
| `ch05-07-summarizing-data-and-making-comparisons.tex` | Summarizing Data and Making Comparisons | AK, FL, IN, MN, OK, TX, VA | De-emphasizes MAD; uses IQR and range as primary spread measures |

**Important for modified topics**: Read the **modified** version of the topic file (in `topics_modified/`), not the original in `topics/`. The questions should test the enhanced content that was added for state-specific standards.

## Execution Plan

When asked to write the question banks, follow this order:

1. **Read the topic file** from the source directory (`topics/`, `topics_additional/`, or `topics_modified/`)
2. **Write the question bank file** in the corresponding `tests_questions_bank/` subdirectory
3. **Work in chapter order** (Ch 1 → Ch 2 → ... → Ch 5), core topics first, then additional, then modified
4. **Verify** that all IDs are sequential and unique within each file
5. **Verify** all answers are mathematically correct

### Batch Size

Write question banks in batches of 5–8 topics at a time to maintain quality. After each batch:
- Confirm all files were created
- Run `python3 scripts/generate_practice_tests.py --states california --num-tests 3` to verify the parser picks up the new files
- Check that the question count matches expectations

### Progress Tracking

Track which topics have been completed. The full count is:
- 44 core topic files
- 13 additional topic files
- 11 modified topic files (state-specific variants)
- **Total: 68 question bank files** (68 × 30 = 2,040 questions)

## LaTeX Environment Definitions

The following environments and commands are defined in `VM_packages/VMfunPractice.sty` and are available when these files are compiled:

- `\begin{practiceQuestion}{ID}{type}...\end{practiceQuestion}` — wrapper (type: `mc`, `sa`, `gmc`, or `gsa`)
- `\begin{questionText}...\end{questionText}` — auto-numbered question text
- `\choiceA{}`...`\choiceD{}` — multiple choice options (for `mc` and `gmc`)
- `\correctAnswer{}` — correct answer (hidden in student version)
- `\explanation{}` — explanation (hidden in student version)

Types `sa` and `gsa` automatically render an answer box for students. Types `gmc` and `gsa` are identical to `mc` and `sa` in rendering — the type distinction exists only so the generation script can identify graphical questions.

### Important notes ####
- Just write the standard test questions. You don't need to compile or create a book. We will do this later.
- As summary, just give me a list of files created.


