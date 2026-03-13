---
name: writing_tests_questions_bank
description: How to write standard test question bank files for math topics used in state standard tests
---

# Writing Tests Question Bank Files

## Overview

For every topic in the study guide, we need a corresponding **question bank file** containing 27 **realistic standard test questions** (15 multiple choice + 6 short answer + 6 graphical). These questions must read and feel like questions students would encounter on an actual state standardized math test (e.g., SBAC, PARCC, STAAR, FSA). The question banks feed into `scripts/generate_practice_tests.py`, which selects questions randomly to build unique per-state standard tests.

There are **two independent question bank sets**:

| Bank | Directory | Practice tests output | Books that use it |
|---|---|---|---|
| Bank 1 (existing) | `tests_questions_bank/` | `practice_tests/` | 3, 5, 7, 10 practice tests |
| Bank 2 (new) | `tests_questions_bank_2/` | `practice_tests_2/` | 6, 9, 12 practice tests |

The two banks are completely independent — different questions, different tests, different books. A student who buys books from both sets gets entirely unique questions.

## Directory Structure

New question bank files go in `tests_questions_bank_2/`:

```
tests_questions_bank_2/
    topics/              # Questions for core CCSS topics (mirrors topics/)
    topics_additional/   # Questions for additional state-specific topics (mirrors topics_additional/)
    topics_modified/     # Questions for modified topics (mirrors topics_modified/)
```

Each question bank file corresponds **one-to-one** to a topic file:

| Topic file location | Question bank file location |
|---|---|
| `topics/ch01-01-unit-rates-with-fractions.tex` | `tests_questions_bank_2/topics/ch01-01-unit-rates-with-fractions.tex` |
| `topics_additional/ch02-08-personal-financial-literacy.tex` | `tests_questions_bank_2/topics_additional/ch02-08-personal-financial-literacy.tex` |
| `topics_modified/ch02-06-simple-interest.tex` | `tests_questions_bank_2/topics_modified/ch02-06-simple-interest.tex` |

**Use the exact same filename** as the topic file it corresponds to.

## Workflow: How to Write Question Banks

### Step 0: Discover Topics with the Script

Before writing any question bank files, run `scripts/get_chapter_topic_facts.py` to get the list of topics for the chapter you are working on:

```bash
python3 scripts/get_chapter_topic_facts.py --chapter <N>
```

This returns a structured report listing all **core topics**, **additional topics**, and **modified topics** for that chapter, along with:
- Topic IDs, names, and file paths
- Which states use additional/modified topics

Use this output to determine which question bank files need to be created. You must write question banks for **every** topic returned by the script — core, additional, and modified.

To see all available chapters:
```bash
python3 scripts/get_chapter_topic_facts.py --list-chapters
```

### Step 1: Read the Topic File

Before writing questions, **always read the corresponding topic file first**. The topic file tells you:
- What concepts are taught
- What vocabulary is introduced
- What difficulty level is appropriate
- What types of problems students have already seen
- What visual representations are used (number lines, coordinate planes, fraction bars, etc.)

Your questions must test the content taught in that specific topic — not content from other topics. Stay within scope.

### Step 2: Create the Question Bank File

Write questions that are **realistic and test-like** — they should mirror the tone, structure, and rigor of actual state standardized math assessments. Avoid overly simplistic "drill" questions that just swap numbers. Instead, use the kinds of multi-step reasoning, real-world contexts, and precise academic language that students encounter on real tests.

Use the exact format shown below. Every file has:
- A header comment block with metadata
- 15 multiple choice questions (IDs: `X-Y-q01` through `X-Y-q15`)
- 6 short answer questions (IDs: `X-Y-q16` through `X-Y-q21`)
- 6 graphical questions (IDs: `X-Y-q22` through `X-Y-q27`) — 3 graphical MC + 3 graphical SA
- For modified files, the ID should reflect the modified topic (e.g., `m-X-Y-q01` instead of `X-Y-q01`)

### Step 3: Verify Correctness

Double-check every answer. An incorrect answer in a realistic test destroys student trust and undermines the book's credibility. Compute each answer carefully.

## File Format

### Header Block

```latex
% ============================================================
% Question Bank: chXX-YY Topic Title
% Topic Title: Full Topic Title
% CCSS: 7.XX.X.X (or "Supplementary" for non-CCSS topics)
% Questions: 27 (15 MC + 6 SA + 6 Graphical)
% ============================================================
```

### Question ID Convention

IDs follow the pattern `{chapter}-{section}-q{number}`:
- `ch01-01` → IDs are `1-1-q01` through `1-1-q27` (q01–q15 MC, q16–q21 SA, q22–q27 Graphical)
- `ch03-05` → IDs are `3-5-q01` through `3-5-q27`
- `ch09-07` → IDs are `9-7-q01` through `9-7-q27`
- For additional topics, use the same chapter-section pattern (e.g., `ch02-08` → IDs are `2-8-q01` through `2-8-q27`)
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
\explanation{A negative times a positive gives a negative: $(-4) \times 7 = -28$.}
\end{practiceQuestion}
```

### Short Answer Question Format

```latex
\begin{practiceQuestion}{X-Y-q16}{sa}
\begin{questionText}
Question text goes here.
\end{questionText}
\correctAnswer{$42$}
\explanation{Multiply the base by the height: $6 \times 7 = 42$.}
\end{practiceQuestion}
```

### Graphical Multiple Choice Question Format (`gmc`)

Graphical questions include a TikZ figure or visual command as a core part of the question. The graphic is essential — students must interpret it to answer.

```latex
\begin{practiceQuestion}{X-Y-q22}{gmc}
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
\begin{practiceQuestion}{X-Y-q25}{gsa}
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
5. **`\correctAnswer{}`** for MC/GMC is the letter (A, B, C, or D). For SA/GSA it is the actual answer which must be very short (usually one or two words or numbers).
6. **`\explanation{}`** is required for every question. Write **2–3 sentences** that (a) name the concept, rule, or formula being used, (b) show the key computation, and (c) arrive at the correct answer. Students have just learned these topics — a bare equation is not enough. Always name the mathematical concept so the student connects the problem to what they studied.
7. **All math must be in `$...$`**. Use `\times` for multiplication, `\div` for division.
8. **No blank lines** between `\choiceA` through `\choiceD` lines.
9. **Separate questions** with a blank line between `\end{practiceQuestion}` and the next `\begin{practiceQuestion}`.
10. **Graphical questions** (`gmc`/`gsa`) must include a TikZ figure, visual command, or table inside `questionText`. The visual is the core of the question — not a decoration.

## Complete Example File

Note how the examples below use **real-world contexts** and **test-like phrasing** rather than bare computation. This is the standard to follow.

```latex
% ============================================================
% Question Bank: ch03-05 Multiplying Integers and Rational Numbers
% Topic Title: Multiplying Integers and Rational Numbers
% CCSS: 7.NS.A.2
% Questions: 27 (15 MC + 6 SA + 6 Graphical)
% ============================================================

% --- Multiple Choice Questions (15) ---

\begin{practiceQuestion}{3-5-q01}{mc}
\begin{questionText}
A scuba diver descends at a rate of $4$ feet per second. Which expression represents the diver's change in depth after $7$ seconds?
\end{questionText}
\choiceA{$4 \times 7 = 28$ feet}
\choiceB{$(-4) \times 7 = -28$ feet}
\choiceC{$4 + 7 = 11$ feet}
\choiceD{$(-4) + 7 = 3$ feet}
\correctAnswer{B}
\explanation{Descending means a negative rate: $(-4) \times 7 = -28$ feet (28 feet below the starting point).}
\end{practiceQuestion}

\begin{practiceQuestion}{3-5-q02}{mc}
\begin{questionText}
The temperature dropped $3^\circ$F each hour for $5$ hours. A student says the total change is $-8^\circ$F. Which statement best describes the student's error?
\end{questionText}
\choiceA{The student added instead of multiplied.}
\choiceB{The student forgot to make the product negative.}
\choiceC{The student multiplied correctly but dropped the negative sign.}
\choiceD{The student divided instead of multiplied.}
\correctAnswer{A}
\explanation{The correct change is $(-3) \times 5 = -15^\circ$F. The student computed $(-3) + (-5) = -8$, adding instead of multiplying.}
\end{practiceQuestion}

% ... (q03 through q15 follow the same pattern) ...

% --- Short Answer Questions (6) ---

\begin{practiceQuestion}{3-5-q16}{sa}
\begin{questionText}
A recipe calls for $\frac{3}{4}$ cup of sugar, but Maria wants to make only $\frac{2}{3}$ of the recipe. How many cups of sugar does Maria need?
\end{questionText}
\correctAnswer{$\frac{1}{2}$}
\explanation{Multiply: $\frac{2}{3} \times \frac{3}{4} = \frac{6}{12} = \frac{1}{2}$ cup.}
\end{practiceQuestion}

% ... (q17 through q21 follow the same pattern) ...

% --- Graphical Questions (3 GMC + 3 GSA) ---

\begin{practiceQuestion}{3-5-q22}{gmc}
\begin{questionText}
The number line below models a multiplication of two integers. Based on the diagram, which equation is represented?

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

% ... (q23-q24 are gmc, q25-q27 are gsa) ...
```

## Question Writing Guidelines

### Realistic Test Question Standards

Every question must feel like it belongs on a real state standardized math test. We need a variety of questions.

### Difficulty Distribution

Aim for a mix across the 27 questions that mirrors real standardized tests:
- **8–9 standard** — grade-level items testing core skills in context (not bare computation)
- **8–9 applied** — word problems, multi-step reasoning, or conceptual understanding
- **4–5 challenging** — requires deeper thinking, combines sub-skills, or uses less obvious numbers
- **6 graphical** — questions where students interpret a diagram, chart, graph, or visual model

### Question Quality Checklist

- [ ] **Realistic**: Each question reads like an actual state standardized test item
- [ ] **On-topic**: Every question tests content from THIS topic file only
- [ ] **Grade-appropriate**: Numbers and language suitable for the target audience (see Grade Info from the script output)
- [ ] **Unique**: No two questions test the exact same thing with different numbers
- [ ] **Plausible distractors**: MC wrong answers should be common mistakes (not random numbers)
- [ ] **Correct answers**: Triple-check every answer is mathematically correct
- [ ] **Clear wording**: Precise academic language, no ambiguity — match the tone of real standardized tests
- [ ] **Math in `$...$`**: All numbers in equations use math mode
- [ ] **Explanation provided**: Every question has a 2–3 sentence explanation that (1) names the concept/rule/formula, (2) shows the key computation, and (3) arrives at the correct answer. No bare equations without naming the concept. No paragraphs either.
- [ ] **Graphical clarity** (for `gmc`/`gsa`): The graphic shows ALL relevant info, is labeled, and students of the target age can instantly understand what it represents and how it connects to the question

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

**Never** use obviously absurd distractors. Every option should look plausible to a student who has a specific misconception. On real standardized tests, distractors are carefully engineered — yours should be too.

### Writing Good Short Answer Questions

SA questions should mirror the constructed-response or gridded-response items found on real standardized tests. The student produces an answer — usually a number, expression, or short phrase.

Keep `\correctAnswer{}` brief — a number, expression, or short phrase. Frame SA questions with the same real-world contexts and academic language used in the MC section.

### Writing Good Explanations

Explanations appear in the answer key and help students learn from their mistakes. Remember: these students have **just learned the topic** — they need explanations that name the concept or rule being used, show the key steps, and connect the reasoning to the answer. A bare computation like `$360 - 65 - 135 - 88 = 72$` is not an explanation — it's just arithmetic that the student could have done themselves.

Follow these rules:

1. **Length**: 2–3 sentences. Two sentences is ideal for most problems. Three sentences maximum for multi-step problems. Never write just a bare equation — and never write a full paragraph either.
2. **Name the concept or rule**: Always start by naming the mathematical concept, property, or formula being applied (e.g., "The interior angles of a quadrilateral always sum to $360°$", "Use the quotient rule for exponents", "Apply the Pythagorean theorem"). This is the most important teaching moment.
3. **Show the work**: After naming the concept, include the key computation or reasoning step that leads to the answer.
4. **Be direct**: Start with the concept/rule, not with filler like "The correct answer is B because...".
5. **End at the answer**: The explanation should naturally arrive at the correct answer so the student can follow the logic.

**GOOD** explanations:
- `Descending means a negative rate of change. Multiply the rate by the time: $(-4) \times 7 = -28$ feet, meaning 28 feet below the starting point.`
- `Use cross-multiplication to solve a proportion: $3 \times 8 = 4x$, so $24 = 4x$ and $x = 6$.`
- `The slope formula is $m = \frac{y_2 - y_1}{x_2 - x_1}$. Substituting the points: $m = \frac{6-2}{4-1} = \frac{4}{3}$. Using point-slope form with $(1,2)$: $y = \frac{4}{3}x + \frac{2}{3}$.`
- `The interior angles of any quadrilateral sum to $360°$. Subtract the three known angles: $x = 360 - 65 - 135 - 88 = 72°$.`
- `Use the product rule for exponents: when multiplying powers with the same base, add the exponents. $4p^3 \times 3p^5 = 12p^{3+5} = 12p^8$.`

**BAD** explanations (too short / just computation, no concept named):
- `$360 - 65 - 135 - 88 = 72°$.` ← no concept named, just arithmetic
- `$12p^8$.` ← no reasoning at all
- `The answer is $-28$.` ← no reasoning shown
- `B` ← useless
- `$\frac{15}{5} = 3$ and $y^{7-3} = y^4$. Answer: $3y^4$.` ← just shows computation without naming the quotient rule

**BAD** explanations (too long):
- `First, we need to recall that when multiplying a negative number by a positive number, the result is always negative. This is because the signs are different. So we take the absolute values, which are 4 and 7, and multiply them to get 28. Then we apply the negative sign to get -28. Therefore the answer is -28.` ← way too wordy for a simple sign rule

### Numbers and Scope by Chapter

Run `python3 scripts/get_chapter_topic_facts.py --chapter <N>` to get the chapter title, topic names, and content summaries. Use that output to understand the scope, number ranges, and key constraints for the chapter you are writing. Stay within the scope described by each topic's summary — do not introduce content from other chapters or topics.

### Using Complex Content in `questionText`

The `\begin{questionText}...\end{questionText}` environment supports any LaTeX content. For topics that benefit from visuals, you can include tables, TikZ graphics, or other environments inside the question text.

### Writing Good Graphical Questions (`gmc` / `gsa`)

Graphical questions use a visual element (TikZ diagram, chart, coordinate plane, number line, etc.) as the **core** of the question. The student must interpret the visual to answer — the graphic is not decoration.

**Structure**: 6 graphical questions per file (IDs q22-q27), placed after the SA questions:
- **q22, q23, q24** → graphical multiple choice (`gmc`) — same structure as `mc` but with a visual in `questionText`
- **q25, q26, q27** → graphical short answer (`gsa`) — same structure as `sa` but with a visual in `questionText`

#### Clarity is Everything

The #1 rule for graphical questions: **a student of the target age (see script output) must instantly understand what the graphic shows and how it relates to the question.** If there is any ambiguity, rewrite the question or redesign the graphic.

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


## Discovering Topics — Use `get_chapter_topic_facts.py`

run the lookup script for each chapter to get the authoritative list of topics:

```bash
python3 scripts/get_chapter_topic_facts.py --chapter <N>
```

The script prints a structured report containing:
- **TOPICS** — core topics → question bank files go in `tests_questions_bank_2/topics/`
- **ADDITIONAL TOPICS** — state-specific topics → files go in `tests_questions_bank_2/topics_additional/`
- **MODIFIED TOPICS** — state-specific variants of core topics → files go in `tests_questions_bank_2/topics_modified/`

For each topic the script outputs: topic ID, name, file path (relative to workspace root), summary, and (for additional/modified) which states use it.

You must create a question bank file for **every** topic the script returns — core, additional, and modified.

**Important for modified topics**: Read the **modified** version of the topic file (in `topics_modified/`), not the original in `topics/`. The questions should test the enhanced content that was added for state-specific standards.

## Execution Plan

When asked to write question banks, process **one chapter at a time**:

1. **Run the script**: `python3 scripts/get_chapter_topic_facts.py --chapter <N>` to discover all topics for the chapter
2. **For each topic** returned (core, additional, modified):
   a. **Read the topic file** from the path shown in the script output
   b. **Write the question bank file** in the corresponding `tests_questions_bank_2/` subdirectory
3. **Work in chapter order** (Ch 1 → Ch 2 → ... → Ch 9), core topics first, then additional, then modified
4. **Verify** that all IDs are sequential and unique within each file
5. **Verify** all answers are mathematically correct

### Batch Size

Write question banks in batches of 5–8 topics at a time to maintain quality. After each batch:
- Confirm all files were created
- Run `python3 scripts/generate_practice_tests.py --bank 2 --states california --num-tests 3` to verify the parser picks up the new files
- Check that the question count matches expectations

### Progress Tracking

Track which topics have been completed per chapter. Use the script's COUNTS section to know how many files each chapter needs.

## LaTeX Environment Definitions

The following environments and commands are defined in `VM_packages/VMfunPractice.sty` and are available when these files are compiled:

- `\begin{practiceQuestion}{ID}{type}...\end{practiceQuestion}` — wrapper (type: `mc`, `sa`, `gmc`, or `gsa`)
- `\begin{questionText}...\end{questionText}` — auto-numbered question text
- `\choiceA{}`...`\choiceD{}` — multiple choice options (for `mc` and `gmc`)
- `\correctAnswer{}` — correct answer (hidden in student version)
- `\explanation{}` — explanation (hidden in student version)

Types `sa` and `gsa` automatically render an answer box for students. Types `gmc` and `gsa` are identical to `mc` and `sa` in rendering — the type distinction exists only so the generation script can identify graphical questions.

## Final Step: Create Practice Test-Style Review LaTeX File
After writing question bank files for a chapter, create a LaTeX file in `tests/` named `grade[number]_test_questions_bank_2_ch<N>.tex`.

The file must follow the **practice tests book pattern**, not a plain chapter handout:
- Enable practice-test answer collection with `\enablePracticeTestAnswers`
- Start the document with `\practiceTestPage{1}{<total question count>}` so the answer system groups the content as a real practice test
- Show the grade, chapter number, and chapter title near the front so the PDF clearly identifies what chapter review it is
- Include all new question bank files for that chapter from `tests_questions_bank_2/`
- Add `\testScorePage{1}{<total question count>}` before the answer key so the review feels like the practice test books
- End with `\printAnswerKey`

Important: the compiled PDF must print **both answers and detailed explanations** at the end, in the same grouped format used by the practice test books. Using only `\enablePracticeTestAnswers` without `\practiceTestPage` is not enough.

## Checklist

- [ ] Ran `python3 scripts/get_chapter_topic_facts.py --chapter <N>` to discover topics, grade, and audience
- [ ] Read every topic source file listed by the script (core + additional + modified)
- [ ] File placed in correct folder (`tests_questions_bank_2/topics/`, `tests_questions_bank_2/topics_additional/`, or `tests_questions_bank_2/topics_modified/`) and the header comment block present with topic title and question count
- [ ] Contains **exactly 27 questions**: 15 MC (`q01`-`q15`) + 6 SA (`q16`-`q21`) + 6 Graphical (`q22`-`q27`: 3 `gmc` + 3 `gsa`)
- [ ] Graphical questions (`gmc`/`gsa`) include a TikZ figure or visual command that IS the question — not decoration and graphical visuals show ALL relevant information and are clearly labeled and graphical questions use **varied visual types**
- [ ] All answers are **mathematically correct** (verified by hand)
- [ ] Content exactly stays within scope of THIS topic only
- [ ] Grade-appropriate language and numbers for the target audience (from script output)
- [ ] Every question reads like a **realistic state standardized test item** 
- [ ] Questions are **completely different** from any questions in `tests_questions_bank/` (bank 1) — no duplicate or near-duplicate questions across banks
- [ ] Create a practice-test-style review file in `tests/` named `grade[number]_test_questions_bank_2_ch<N>.tex` that uses `\practiceTestPage{1}{<total question count>}`, clearly shows the grade/chapter/title, `\input`s all new question bank files from `tests_questions_bank_2/`, adds `\testScorePage{1}{<total question count>}`, compiles successfully, and prints both answers and detailed explanations in the PDF
