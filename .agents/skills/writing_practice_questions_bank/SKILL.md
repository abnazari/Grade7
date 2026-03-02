````skill
---
name: writing_tests_questions_bank
description: How to write standard test question bank files for Grade 7 math topics used in state standard tests
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
| `topics/ch01-01-unit-rates-with-fractions.tex` | `tests_questions_bank/topics/ch01-01-unit-rates-with-fractions.tex` |
| `topics_additional/ch02-08-personal-financial-literacy.tex` | `tests_questions_bank/topics_additional/ch02-08-personal-financial-literacy.tex` |
| `topics_modified/ch02-06-simple-interest.tex` | `tests_questions_bank/topics_modified/ch02-06-simple-interest.tex` |

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
% CCSS: 7.XX.X.X (or "Supplementary" for non-CCSS topics)
% Questions: 30 (18 MC + 7 SA + 5 Graphical)
% ============================================================
```

### Question ID Convention

IDs follow the pattern `{chapter}-{section}-q{number}`:
- `ch01-01` → IDs are `1-1-q01` through `1-1-q30` (q01–q18 MC, q19–q25 SA, q26–q30 Graphical)
- `ch03-05` → IDs are `3-5-q01` through `3-5-q30`
- `ch09-07` → IDs are `9-7-q01` through `9-7-q30`
- For additional topics, use the same chapter-section pattern (e.g., `ch02-08` → IDs are `2-8-q01` through `2-8-q30`)
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
Look at the number line below. Which point represents $-\frac{3}{2}$?

\begin{center}
\numberLine[1]{-3}{3}
\end{center}
\end{questionText}
\choiceA{Point A}
\choiceB{Point B}
\choiceC{Point C}
\choiceD{Point D}
\correctAnswer{B}
\explanation{$-\frac{3}{2} = -1.5$ is halfway between $-2$ and $-1$ on the number line.}
\end{practiceQuestion}
```

### Graphical Short Answer Question Format (`gsa`)

```latex
\begin{practiceQuestion}{X-Y-q29}{gsa}
\begin{questionText}
What is the area of the composite figure shown below?

\begin{center}
\begin{tikzpicture}[scale=0.5]
  \draw[step=1,gray!30,thin] (0,0) grid (8,6);
  \draw[thick,->] (0,0) -- (8.5,0) node[right]{$x$};
  \draw[thick,->] (0,0) -- (0,6.5) node[above]{$y$};
  \fill[funBlue!30] (1,1) -- (7,1) -- (7,4) -- (4,5) -- (1,4) -- cycle;
  \draw[thick,funBlue] (1,1) -- (7,1) -- (7,4) -- (4,5) -- (1,4) -- cycle;
  \node[below] at (1,1) {$(1,1)$};
  \node[below] at (7,1) {$(7,1)$};
  \node[right] at (7,4) {$(7,4)$};
  \node[above] at (4,5) {$(4,5)$};
  \node[left] at (1,4) {$(1,4)$};
\end{tikzpicture}
\end{center}
\end{questionText}
\correctAnswer{$21$ square units}
\explanation{Rectangle base: $6 \times 3 = 18$. Triangle on top: $\frac{1}{2} \times 6 \times 1 = 3$. Total: $18 + 3 = 21$ square units.}
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
% Question Bank: ch03-05 Multiplying Integers and Rational Numbers
% Topic Title: Multiplying Integers and Rational Numbers
% CCSS: 7.NS.A.2
% Questions: 30 (18 MC + 7 SA + 5 Graphical)
% ============================================================

% --- Multiple Choice Questions (18) ---

\begin{practiceQuestion}{3-5-q01}{mc}
\begin{questionText}
What is $(-4) \times 7$?
\end{questionText}
\choiceA{$28$}
\choiceB{$-28$}
\choiceC{$-11$}
\choiceD{$11$}
\correctAnswer{B}
\explanation{A negative times a positive gives a negative: $(-4) \times 7 = -28$.}
\end{practiceQuestion}

\begin{practiceQuestion}{3-5-q02}{mc}
\begin{questionText}
What is $(-3) \times (-5)$?
\end{questionText}
\choiceA{$-15$}
\choiceB{$-8$}
\choiceC{$15$}
\choiceD{$8$}
\correctAnswer{C}
\explanation{A negative times a negative gives a positive: $(-3) \times (-5) = 15$.}
\end{practiceQuestion}

% ... (q03 through q18 follow the same pattern) ...

% --- Short Answer Questions (7) ---

\begin{practiceQuestion}{3-5-q19}{sa}
\begin{questionText}
What is $\left(-\frac{2}{3}\right) \times \frac{3}{4}$?
\end{questionText}
\correctAnswer{$-\frac{1}{2}$}
\explanation{Multiply numerators: $(-2)(3) = -6$. Multiply denominators: $(3)(4) = 12$. Simplify: $-\frac{6}{12} = -\frac{1}{2}$.}
\end{practiceQuestion}

% ... (q20 through q25 follow the same pattern) ...

% --- Graphical Questions (3 GMC + 2 GSA) ---

\begin{practiceQuestion}{3-5-q26}{gmc}
\begin{questionText}
The number line shows the product of two integers. Which multiplication does the arrow represent?

\begin{center}
\begin{tikzpicture}
  \draw[thick,->] (-4.5,0) -- (4.5,0);
  \foreach \x in {-4,...,4} \draw (\x,0.1) -- (\x,-0.1) node[below] {$\x$};
  \draw[thick,->,funBlue] (0,0.4) -- (-3,0.4);
  \node[above,funBlue] at (-1.5,0.4) {$3$ jumps of $-1$};
\end{tikzpicture}
\end{center}
\end{questionText}
\choiceA{$3 \times 1 = 3$}
\choiceB{$3 \times (-1) = -3$}
\choiceC{$(-3) \times (-1) = 3$}
\choiceD{$(-1) \times (-3) = 3$}
\correctAnswer{B}
\explanation{The arrow shows $3$ groups of $-1$, moving left on the number line to $-3$.}
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
- [ ] **Grade-appropriate**: Numbers and language suitable for 12–13 year olds
- [ ] **Unique**: No two questions test the exact same thing with different numbers
- [ ] **Plausible distractors**: MC wrong answers should be common mistakes (not random numbers)
- [ ] **Correct answers**: Triple-check every answer is mathematically correct
- [ ] **Clear wording**: Short sentences, everyday language, no ambiguity
- [ ] **Math in `$...$`**: All numbers in equations use math mode
- [ ] **Explanation provided**: Every question has a brief, helpful explanation
- [ ] **Graphical clarity** (for `gmc`/`gsa`): The graphic shows ALL relevant info, is labeled, and a 12-year-old can instantly understand what it represents and how it connects to the question

### Writing Good Distractors (multiple choice wrong answers)

Wrong answers should reflect real student mistakes:
- **Sign errors**: e.g., $(-3) \times (-5) = -15$ instead of $15$
- **Operation confusion**: e.g., adding instead of multiplying, confusing percent increase and decrease
- **Fraction/decimal errors**: e.g., forgetting to find a common denominator, incorrect rational number operations
- **Partial computation**: e.g., only doing the first step of a two-step equation
- **Common misconceptions**: e.g., thinking $|-5| = -5$, or that dividing by a fraction makes smaller, or confusing proportional and non-proportional relationships
- **Order-of-operations errors**: e.g., distributing before simplifying, incorrect inverse operations
- **Percent errors**: e.g., confusing percent increase with percent of original, computing on the wrong base
- **Geometry errors**: e.g., confusing area and perimeter, wrong formula for circles, surface area vs volume

**Never** use obviously absurd distractors. Every option should look plausible to a student who has a specific misconception.

### Writing Good Short Answer Questions

SA questions should require the student to produce an answer, usually a very short one (a number, expression, or short phrase).

Keep `\correctAnswer{}` brief — a number, expression, or short phrase.

### Numbers and Scope by Chapter

Follow these constraints to stay aligned with Grade 7 standards:

| Chapter | Number Range | Key Constraints |
|---|---|---|
| Ch 1 (Ratios and Proportional Relationships) | Fractions, decimals, unit rates with fraction quantities | Unit rates with fractions; proportional relationships via tables, graphs, equations; constant of proportionality; graphing proportions; multi-step ratio problems |
| Ch 2 (Percents in Everyday Life) | Percents, decimals, fractions; money amounts | Percent problems (part, whole, percent); percent-proportion connection; percent increase/decrease (1.05a pattern); markups/discounts/tax; tips/commissions; simple interest (I = Prt); percent error |
| Ch 3 (Operations with Rational Numbers) | All rational numbers: integers, fractions, decimals (positive and negative) | Opposites and absolute value; adding/subtracting integers and rationals; multiplying/dividing signed numbers; converting rationals to decimals (terminating/repeating); multi-step rational number problems |
| Ch 4 (Algebraic Expressions) | Rational coefficients (fractions and decimals); single variable | Writing and evaluating expressions; combining like terms; distributive property; factoring; adding/subtracting linear expressions; rewriting expressions for insight |
| Ch 5 (Equations and Inequalities) | Rational number coefficients; two-step and multi-step | Two-step equations (px + q = r); equations with distributive property p(x + q) = r; multi-step problems with rationals; writing/solving/graphing inequalities (px + q > r) |
| Ch 6 (Scale Drawings, Geometry, Angles) | Lengths may be fractions/decimals; angle measures in degrees | Scale drawings and scale factors; reproducing at different scales; drawing figures with given conditions; constructing triangles (uniqueness); cross-sections of 3D figures; supplementary/complementary/vertical angles |
| Ch 7 (Circles, Area, Surface Area, Volume) | Decimals and fractions for lengths; π ≈ 3.14 or 22/7 | Circle parts, circumference (C = πd), area (A = πr²); composite shapes; surface area of prisms; volume (V = Bh) with various bases |
| Ch 8 (Statistics: Sampling and Comparing Populations) | Data sets of 10–25 values; means, medians, MAD, IQR | Populations vs samples; random sampling; comparative inferences; visual overlap as multiples of MAD; comparing two populations using measures of center and variability |
| Ch 9 (Probability and Compound Events) | Probabilities as fractions, decimals, percents (0 to 1) | Probability concepts (0–1 scale); theoretical probability (favorable/total); experimental probability (relative frequency); probability models (uniform/non-uniform); sample spaces (lists, tables, tree diagrams); compound event probabilities; simulations |

### Using Complex Content in `questionText`

The `\begin{questionText}...\end{questionText}` environment supports any LaTeX content. For topics that benefit from visuals, you can include tables, TikZ graphics, or other environments inside the question text.

### Writing Good Graphical Questions (`gmc` / `gsa`)

Graphical questions use a visual element (TikZ diagram, chart, coordinate plane, number line, etc.) as the **core** of the question. The student must interpret the visual to answer — the graphic is not decoration.

**Structure**: 5 graphical questions per file (IDs q26–q30), placed after the SA questions:
- **q26, q27, q28** → graphical multiple choice (`gmc`) — same structure as `mc` but with a visual in `questionText`
- **q29, q30** → graphical short answer (`gsa`) — same structure as `sa` but with a visual in `questionText`

#### Clarity is Everything

The #1 rule for graphical questions: **a 12-year-old must instantly understand what the graphic shows and how it relates to the question.** If there is any ambiguity, rewrite the question or redesign the graphic.

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
Question: "A student says the constant of proportionality is 3. Is the student correct?"
Graphic: [a table showing only input values, no output values]
Problem: The question asks about proportionality but the graphic doesn't show
         both quantities. The student has no way to verify the constant.
```

**GOOD** — graphic shows exactly what the question asks about:
```
Question: "Look at the graph below. What is the constant of proportionality?"
Graphic: [coordinate plane with a line through origin, points labeled]
Why it works: The student can SEE the line, read coordinates, and compute k.
```

**BAD** — graphic is decorative, not essential:
```
Question: "What is |-7|?"
Graphic: [a number line from -10 to 10 with -7 marked]
Problem: The number line doesn't add anything — the student still has to
         recall the definition. The graphic is decoration.
```

**GOOD** — graphic is the core of the problem:
```
Question: "Look at the number line. What is the distance between point A
          and point B?"
Graphic: [number line with A at -3.5 and B at 4.5, clearly labeled]
Why it works: The student must read both coordinates and find the distance.
```

#### Topic-to-visual Suggestions (not exhaustive — use creative judgment)

| Topic Area | Natural Visual Types |
|---|---|
| Ratios & Proportional (Ch 1) | Coordinate graphs of proportional relationships, ratio tables, tape diagrams, unit rate slopes |
| Percents (Ch 2) | Bar models (part/whole), percent comparison diagrams, 10×10 grids, simple interest timelines |
| Rational Numbers (Ch 3) | Number lines with integers/fractions/decimals, comparison visuals, temperature/elevation contexts |
| Algebraic Expressions (Ch 4) | Algebra tile diagrams, expression area models, input/output tables |
| Equations & Inequalities (Ch 5) | Balance/scale diagrams, inequality number lines with open/closed circles, word problem diagrams |
| Geometry & Angles (Ch 6) | Scale drawings, triangles with given measurements, cross-section diagrams, angle diagrams with intersecting lines |
| Circles, Area, SA, Volume (Ch 7) | Circle diagrams with radius/diameter, composite shapes on grids, nets of 3D shapes, prism volume diagrams |
| Statistics (Ch 8) | Dot plots, box plots, histograms, side-by-side comparison displays, sampling diagrams |
| Probability (Ch 9) | Tree diagrams, sample space tables, spinner/dice diagrams, frequency tables, simulation results |


## Full Topic List — Files to Create

### Core Topics → `tests_questions_bank/topics/`

Create one question bank file for each of the 56 core topic files in `topics/`. These are derived directly from `topics_config.yaml`:

| File | Topic |
|---|---|
| `ch01-01-unit-rates-with-fractions.tex` | Unit Rates with Fractions |
| `ch01-02-recognizing-proportional-relationships.tex` | Recognizing Proportional Relationships |
| `ch01-03-finding-the-constant-of-proportionality.tex` | Finding the Constant of Proportionality |
| `ch01-04-writing-equations-for-proportional-relationships.tex` | Writing Equations for Proportional Relationships |
| `ch01-05-graphing-proportional-relationships.tex` | Graphing Proportional Relationships |
| `ch01-06-applying-proportional-reasoning.tex` | Applying Proportional Reasoning to Real-World Problems |
| `ch02-01-solving-percent-problems.tex` | Solving Percent Problems |
| `ch02-02-connecting-percents-and-proportions.tex` | Connecting Percents and Proportions |
| `ch02-03-percent-increase-and-decrease.tex` | Percent Increase and Decrease |
| `ch02-04-markups-discounts-and-sales-tax.tex` | Markups, Discounts, and Sales Tax |
| `ch02-05-tips-commissions-and-fees.tex` | Tips, Commissions, and Fees |
| `ch02-06-simple-interest.tex` | Simple Interest: Earning and Paying Interest |
| `ch02-07-percent-error.tex` | Percent Error: How Close Are Your Estimates? |
| `ch03-01-integers-and-their-opposites.tex` | Integers and Their Opposites |
| `ch03-02-adding-integers.tex` | Adding Integers |
| `ch03-03-subtracting-integers.tex` | Subtracting Integers |
| `ch03-04-adding-and-subtracting-rational-numbers.tex` | Adding and Subtracting Rational Numbers |
| `ch03-05-multiplying-integers-and-rational-numbers.tex` | Multiplying Integers and Rational Numbers |
| `ch03-06-dividing-integers-and-rational-numbers.tex` | Dividing Integers and Rational Numbers |
| `ch03-07-converting-rational-numbers-to-decimals.tex` | Converting Rational Numbers to Decimals |
| `ch03-08-solving-real-world-problems-with-rational-numbers.tex` | Solving Real-World Problems with Rational Numbers |
| `ch04-01-writing-and-evaluating-expressions.tex` | Writing and Evaluating Expressions |
| `ch04-02-simplifying-expressions-by-combining-like-terms.tex` | Simplifying Expressions by Combining Like Terms |
| `ch04-03-expanding-expressions-with-the-distributive-property.tex` | Expanding Expressions with the Distributive Property |
| `ch04-04-factoring-expressions.tex` | Factoring Expressions |
| `ch04-05-adding-and-subtracting-linear-expressions.tex` | Adding and Subtracting Linear Expressions |
| `ch04-06-rewriting-expressions-to-solve-problems.tex` | Rewriting Expressions to Solve Problems |
| `ch05-01-writing-two-step-equations.tex` | Writing Two-Step Equations from Word Problems |
| `ch05-02-solving-two-step-equations.tex` | Solving Two-Step Equations |
| `ch05-03-solving-equations-with-distributive-property.tex` | Solving Equations with the Distributive Property |
| `ch05-04-solving-multi-step-problems-with-rational-numbers.tex` | Solving Multi-Step Problems with Rational Numbers |
| `ch05-05-writing-and-solving-inequalities.tex` | Writing and Solving Inequalities |
| `ch05-06-graphing-solutions-to-inequalities.tex` | Graphing Solutions to Inequalities on a Number Line |
| `ch06-01-understanding-and-using-scale-drawings.tex` | Understanding and Using Scale Drawings |
| `ch06-02-reproducing-scale-drawings.tex` | Reproducing Scale Drawings at a Different Scale |
| `ch06-03-drawing-geometric-figures.tex` | Drawing Geometric Figures with Given Conditions |
| `ch06-04-constructing-triangles.tex` | Constructing Triangles from Three Measurements |
| `ch06-05-cross-sections-of-3d-figures.tex` | Cross-Sections of Three-Dimensional Figures |
| `ch06-06-angle-relationships.tex` | Angle Relationships: Supplementary, Complementary, and Vertical Angles |
| `ch07-01-parts-of-a-circle.tex` | Parts of a Circle |
| `ch07-02-circumference-of-a-circle.tex` | Circumference of a Circle |
| `ch07-03-area-of-a-circle.tex` | Area of a Circle |
| `ch07-04-area-of-composite-shapes.tex` | Area of Composite Shapes |
| `ch07-05-surface-area-of-3d-objects.tex` | Surface Area of Three-Dimensional Objects |
| `ch07-06-volume-of-prisms.tex` | Volume of Prisms |
| `ch08-01-populations-and-samples.tex` | Populations and Samples |
| `ch08-02-making-inferences-from-random-samples.tex` | Making Inferences from Random Samples |
| `ch08-03-comparing-two-populations-visually.tex` | Comparing Two Populations Visually |
| `ch08-04-comparing-populations-with-measures.tex` | Comparing Populations with Measures of Center and Variability |
| `ch09-01-what-is-probability.tex` | What Is Probability? |
| `ch09-02-theoretical-probability.tex` | Theoretical Probability |
| `ch09-03-experimental-probability.tex` | Experimental Probability |
| `ch09-04-probability-models.tex` | Probability Models |
| `ch09-05-sample-spaces-for-compound-events.tex` | Sample Spaces for Compound Events |
| `ch09-06-finding-probabilities-of-compound-events.tex` | Finding Probabilities of Compound Events |
| `ch09-07-simulating-compound-events.tex` | Simulating Compound Events |

### Additional Topics → `tests_questions_bank/topics_additional/`

Create one question bank file for each of the 14 additional topic files in `topics_additional/`. These map to the `additional_topics` list in `topics_config.yaml`:

| File | Topic | States That Use It |
|---|---|---|
| `ch01-07-proportional-reasoning-with-scale-models.tex` | Proportional Reasoning with Scale Models | OK |
| `ch02-08-personal-financial-literacy.tex` | Personal Financial Literacy | MN, OK, TX |
| `ch02-09-financial-literacy-budgeting-saving-and-investing.tex` | Financial Literacy — Budgeting, Saving, and Investing | TX |
| `ch02-10-compound-interest-introduction.tex` | Compound Interest Introduction | TX |
| `ch03-09-introduction-to-square-roots.tex` | Introduction to Square Roots | VA |
| `ch03-10-rational-number-operations-in-extended-contexts.tex` | Rational Number Operations in Extended Contexts | AK |
| `ch03-11-introduction-to-scientific-notation.tex` | Introduction to Scientific Notation | VA |
| `ch04-07-laws-of-exponents.tex` | Laws of Exponents | FL, VA |
| `ch06-07-transformations-on-the-coordinate-plane.tex` | Transformations on the Coordinate Plane | IN, VA |
| `ch06-08-similar-figures-and-proportions.tex` | Similar Figures and Proportions | TX, VA |
| `ch07-07-cylinder-surface-area-and-volume.tex` | Cylinder Surface Area and Volume | FL, VA |
| `ch08-05-stem-and-leaf-plots.tex` | Stem-and-Leaf Plots | FL, OK, TX, VA |
| `ch08-06-circle-graphs.tex` | Circle Graphs | FL, MN, TX, VA |
| `ch08-07-data-displays-extended.tex` | Data Displays Extended | AK, IN, OK |

### Modified Topics → `tests_questions_bank/topics_modified/`

Create one question bank file for each modified topic file in `topics_modified/`. These are state-specific variants of core topics; each file replaces the standard version for the states listed. Read the **modified** file (not the original in `topics/`) before writing questions:

| File | Topic | States | What Changed |
|---|---|---|---|
| `ch01-06-applying-proportional-reasoning.tex` | Applying Proportional Reasoning | OK | OAS-M estimation emphasis — adds estimation as 5th strategy; estimate-first + reasonableness check |
| `ch02-01-solving-percent-problems.tex` | Solving Percent Problems | MN | MN percent-application emphasis — adds financial contexts (discount, markup, tax, tip) |
| `ch02-06-simple-interest.tex` | Simple Interest | FL, TX | Financial literacy emphasis — expands I = Prt with savings/loan comparisons, real-world financial decisions |
| `ch03-01-integers-and-their-opposites.tex` | Integers and Their Opposites | VA | VA SOL rational number emphasis — ordering, comparison, number-line contexts with inequality symbols |
| `ch03-08-solving-real-world-problems-with-rational-numbers.tex` | Solving Real-World Problems with Rational Numbers | AK | Culturally responsive Alaskan contexts — temperatures, fisheries, elevation, subsistence economy |
| `ch06-03-drawing-geometric-figures.tex` | Drawing Geometric Figures | IN | IAS 2023 construction emphasis — justifying construction steps; technology-based methods |
| `ch06-06-angle-relationships.tex` | Angle Relationships | VA | Extended angle emphasis — congruence/similarity connections, multi-step algebraic angle problems |
| `ch08-01-populations-and-samples.tex` | Populations and Samples | OK, TX | Experimental design emphasis — designing experiments and collecting data as precursors |
| `ch08-03-comparing-two-populations-visually.tex` | Comparing Two Populations Visually | FL, IN, MN, VA | Multiple display emphasis — stem-and-leaf, circle graphs, frequency tables alongside standard displays |
| `ch08-04-comparing-populations-with-measures.tex` | Comparing Populations with Measures | AK, OK, TX | Extended measures emphasis — IQR/range over MAD; localised/financial data contexts |
| `ch09-03-experimental-probability.tex` | Experimental Probability | FL, TX | Simulation emphasis — random-number generators, frequency tables, experimental vs theoretical comparison |

**Important for modified topics**: Read the **modified** version of the topic file (in `topics_modified/`), not the original in `topics/`. The questions should test the enhanced content that was added for state-specific standards.

## Execution Plan

When asked to write the question banks, follow this order:

1. **Read the topic file** from the source directory (`topics/`, `topics_additional/`, or `topics_modified/`)
2. **Write the question bank file** in the corresponding `tests_questions_bank/` subdirectory
3. **Work in chapter order** (Ch 1 → Ch 2 → ... → Ch 9), core topics first, then additional, then modified
4. **Verify** that all IDs are sequential and unique within each file
5. **Verify** all answers are mathematically correct

### Batch Size

Write question banks in batches of 5–8 topics at a time to maintain quality. After each batch:
- Confirm all files were created
- Run `python3 scripts/generate_practice_tests.py --states california --num-tests 3` to verify the parser picks up the new files
- Check that the question count matches expectations

### Progress Tracking

Track which topics have been completed. The full count is:
- 56 core topic files
- 14 additional topic files
- 11 modified topic files (state-specific variants)
- **Total: 81 question bank files** (81 × 30 = 2,430 questions)

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



````
