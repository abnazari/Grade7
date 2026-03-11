---
name: writing_steps_topics
description: How to write concise step-by-step topics (~130 pages total)
---

# Writing Step-by-Step Topics

## Overview

The **step-by-step book** is a concise book (~130 pages) that presents math concepts as **clear, numbered procedures**. The key design principle: **show ALL steps first**, then worked examples that apply those steps. This gives students a "recipe" they can follow.

## Important notes:
- When I ask for topics of one chapter, write all step_topics, steps_topics_additional, and steps_topics_modified for that chapter before creating test latex file and compiling pdf and submitting for review. 


**The step-by-step book should be the same size as the study guide (~130 pages).** Each topic should be **2–3 pages** (teaching + practice). This is NOT a big book — keep everything tight.

**Structure: Steps First, Examples Second**
1. List all steps up front in a brief `stepsCard`
2. Show 1–2 worked examples applying all steps together
3. Practice problems organized by step (5–6 problems)

## Step 0 — Discover Topics with the Script

Before writing anything, **run the discovery script** to learn what topics the chapter contains, the grade level, and the target audience:

```bash
python3 scripts/get_chapter_topic_facts.py --chapter <N>
```

The script output tells you:
- **Grade Info** — grade level, grade display name, and target student age range (read from `scripts/config.py` and `.env`). Use this to calibrate vocabulary, sentence complexity, and number difficulty.
- **Chapter title** — so you know the mathematical domain.
- **Core topics** — the list of topics in `topics/` you must write step-by-step versions for.
- **Additional topics** — state-specific topics in `topics_additional/` (with which states use them).
- **Modified topics** — state-specific variants in `topics_modified/` (with which states use them).
- **Summaries** — a brief content description for each topic, giving you a head start on understanding the math before you read the source file.

To list all available chapters:
```bash
python3 scripts/get_chapter_topic_facts.py --list-chapters
```

Use the script output to plan your work: note how many files you need to create (core + additional + modified) and read the summaries to understand the scope.

## Step 1 — Read the Study Guide Source Topics

For every topic listed by the script, **read the corresponding Study Guide source file** before writing:

| Script "File Path" prefix | Read from | Write to |
|---------------------------|-----------|----------|
| `topics/` | `topics/ch<CC>-<SS>-<slug>.tex` | `steps_topics/ch<CC>-<SS>-<slug>.tex` |
| `topics_additional/` | `topics_additional/ch<CC>-<SS>-<slug>.tex` | `steps_topics_additional/ch<CC>-<SS>-<slug>.tex` |
| `topics_modified/` | `topics_modified/ch<CC>-<SS>-<slug>.tex` | `steps_topics_modified/ch<CC>-<SS>-<slug>.tex` |

When reading each source file, extract:
- What concepts are taught
- What vocabulary is introduced
- What difficulty level and number range is used
- What types of problems appear in the practice section

**The step-by-step file must use the same filename as the Study Guide file.**

## Step 2 — Write High-Quality Step-by-Step Topics

Write each topic following the Topic Structure and Content Guidelines below. Focus on:
- **Mathematical accuracy** — double-check every calculation in examples and answers.
- **Clear procedural steps** — the stepsCard is the centerpiece. Steps must be concise, unambiguous, and cover the full procedure.
- **Age-appropriate language** — use the grade/age info from the script output (see "Writing for the Target Audience" below).
- **Variety in examples** — don't reuse the same numbers or problem types across examples. Use realistic contexts (money, sports, cooking, school supplies).
- **Correct LaTeX** — follow the LaTeX Conventions section exactly.

## Step 3 — Compile and Verify

After writing ALL topics for the chapter (core + additional + modified):
1. Create a test file `tests/test_steps_ch<N>.tex` that includes all the new topic files.
2. Compile with: `latexmk -xelatex -output-directory=build -interaction=nonstopmode -f tests/test_steps_ch<N>.tex`
3. Check the log for errors: `grep -i 'error\|undefined' build/test_steps_ch<N>.log | grep -v Warning | head -20`
4. Open the PDF for review.

## File Location & Naming

Place topic files in:
- **Core topics:** `steps_topics/`
- **State-specific additional:** `steps_topics_additional/`
- **State-specific modified:** `steps_topics_modified/`

**Naming:** Same filenames as the Study Guide source files — `ch<CC>-<SS>-<slug>.tex`

Examples: `ch01-01-what-is-a-ratio.tex`, `ch02-03-divide-multi-digit-numbers.tex`

## Key Differences from the Study Guide

| Aspect | Study Guide (~130 pp) | Step-by-Step (~130 pp) |
|--------|-----------------------|------------------------|
| Teaching | Focused: 1 conceptBox + 1–2 worked examples | Procedural: 1 stepsCard + 1–2 stepExamples |
| Practice | 5–6 problems per topic | 5–6 problems per topic |
| Engagement | Minimal: 1 mascotSays (optional) | Minimal: 1 mascotStepTip (optional) |
| Answers | `\answer{}` final answer only | `\answer{}` final answer only |
| Extras | None | None |
| Page count | 2–3 pages per topic | 2–3 pages per topic |

## Topic Structure (2–3 pages)

Every step-by-step topic follows this flow:

### Required Elements
1. **Section header** — `\section{}` only (do NOT use `\stepByStepTitle{}`)
2. **Step Goal** — brief learning objectives in `stepGoal` (2–3 items)
3. **Vocabulary** — key terms grouped in `stepVocabBox` with `\vocabItem` entries (2–4 terms)
4. **Steps Card** — ALL steps listed concisely in `stepsCard` with `\stepItem`, with a **clear descriptive title**
5. **Worked Examples** — 1–2 examples using `stepExample` with `\stepShow` and `\stepResult`
6. **Practice** — 5–6 problems organized by step in `stepPractice`

### Optional Elements (use at most 1 per topic to save space)
- `\watchOut{}` for a common mistake
- `\mascotStepTip{}` for an owl character tip
- `stepTryIt` for guided practice with blanks (only if space allows — skip if topic already has 2 examples)

### Elements to OMIT
These should NOT appear in step-by-step topics:
- `\encouragement{}` — no motivational closers
- `challengeBox` — no bonus challenges
- `\stepReminder{}` — use sparingly, prefer cutting to save space
- `conceptBox` — use stepsCard instead
- `vocabBox` — use stepVocabBox instead
- `exploreBox`, `errorBox`, `riddleBox`, `activityBox`, `warmUp` — none of these
- `realWorld`, `funFact`, `didYouKnow`, `storyProblem` — none of these
- `summaryBox` — no summaries
- `compareBox`, `patternBox`, `codeBreaker`, `mathTrail` — none of these

## Section Guide

### Section Header (required)

```latex
\section{Place Value Relationships}
```

**Do NOT use `\stepByStepTitle{}`** — it duplicates the section title and adds an unnecessary "Step-by-Step Guide" subtitle. The `\section{}` command already renders the numbered title (e.g., "1.1 Place Value Relationships").

### Step Goal (required)

```latex
\begin{stepGoal}
\begin{itemize}
    \item Explain how each digit's value is $10$ times the digit to its right
    \item Read the value of a digit based on its place
\end{itemize}
\end{stepGoal}
```

Brief — just 2–3 bullet points. Keep it tighter than the study guide's `learningGoals`.

### Vocabulary (before stepsCard)

Group all vocabulary in a single titled box using `stepVocabBox`:

```latex
\begin{stepVocabBox}
    \vocabItem{Place Value}{How much a digit is worth based on where it sits in a number.}
    \vocabItem{Expanded Form}{Writing a number as the sum of each digit's value.}
\end{stepVocabBox}
```

The box has a default title "Words to Know". You can customize it: `\begin{stepVocabBox}[New Words]`.

Keep to **2–4 terms** — only essential vocabulary for the procedure.

### Steps Card (required — the centerpiece)

```latex
\begin{stepsCard}[How to Find the Value of Each Digit in a Number]
    \stepItem{Find the digit's \textbf{place} — ones, tens, hundreds, thousands, etc.}
    \stepItem{Each place is \textbf{$10$ times} the place to its right and \textbf{$\frac{1}{10}$} of the place to its left.}
    \stepItem{Multiply the digit by its \textbf{place value} to find what it's worth.}
\end{stepsCard}
```

**Rules for the stepsCard:**
- **Always provide a clear descriptive title** that tells the student what they are learning to do (e.g., `[How to Multiply Multi-Digit Numbers]`, `[How to Compare Two Decimals]`). The default title "The Steps" is too vague — students must know *what* the steps are for.
- 2–5 steps maximum
- Each step is ONE concise sentence
- Steps auto-number with colored circles (step1Color, step2Color, etc.)
- This is shown ONCE — then examples demonstrate how to apply all steps

### Worked Examples (required, 1–2 per topic)

```latex
\begin{stepExample}{In $3{,}555$, how does the value of the $5$ in the hundreds place compare to the $5$ in the tens place?}
    \stepShow{1} Find each digit's place:\\
    The first $5$ is in the \textbf{hundreds} place. The second $5$ is in the \textbf{tens} place.

    \stepShow{2} Hundreds is one place to the left of tens, so it is $10$ times greater.

    \stepShow{3} Find the values: $5 \times 100 = 500$ and $5 \times 10 = 50$.
    \stepResult{The $5$ in the hundreds place is $10$ times the $5$ in the tens place ($500$ vs.\ $50$).}
\end{stepExample}
```

**Each worked example applies ALL steps to ONE problem:**
- Use `\stepShow{n}` to label which step is being applied (colored badge)
- Use `\stepResult{answer}` for the final answer (green checkmark box)
- Keep each step's application brief — 1–2 lines
- If you do 2 examples, the second should be more concise

### Your Turn (optional — only if space allows)

```latex
\begin{stepTryIt}{In $4{,}442$, compare the value of the $4$ in the thousands place to the $4$ in the hundreds place.}
    \stepShow{1} What place is each $4$ in?\par
    Thousands $4$: \answerBlank[2.5cm] \qquad Hundreds $4$: \answerBlank[2.5cm]

    \stepShow{2} Which place is to the left? It is \answerBlank[1.5cm] times greater.\par

    \stepShow{3} Values: $4 \times$ \answerBlank[1.5cm] $=$ \answerBlank[2cm] and $4 \times$ \answerBlank[1.5cm] $=$ \answerBlank[2cm]
\end{stepTryIt}
```

Same structure as `stepExample` but with blanks. **Skip this if the topic already has 2 examples** — it's better to stay within 2–3 pages than to include everything.

### Watch Out / Tips (optional, at most 1)

```latex
\watchOut{The same digit can mean very different things! The $7$ in $7{,}000$ is worth $7{,}000$, but the $7$ in $70$ is only worth $70$.}
```

Or:

```latex
\mascotStepTip{Move one place to the LEFT and the value gets $10$ times bigger. Move RIGHT and it gets $10$ times smaller!}
```

Pick ONE — not both. Many topics won't need either.

### Step Practice (required)

```latex
\newpage
\begin{stepPractice}{Place Value Practice}
    \resetProblems

    \stepPracticeHeader[step1Color]{Identify the Place}
    \begin{multicols}{2}
    \prob What place is the $6$ in $6{,}432$? \answerBlank[2.5cm]
    \answer{thousands}
    \prob What place is the $8$ in $3.482$? \answerBlank[2.5cm]
    \answer{hundredths}
    \end{multicols}

    \stepPracticeHeader[step2Color]{Compare Digit Values}
    \prob In $2{,}255$, the $2$ in the thousands place is how many times the $2$ in the hundreds place? \answerBlank[2cm]
    \answer{$10$ times}

    \stepPracticeHeader[step3Color]{Find the Value}
    \begin{multicols}{2}
    \prob Value of $9$ in $9{,}301$: \answerBlank[2cm]
    \answer{$9{,}000$}
    \prob Value of $4$ in $0.743$: \answerBlank[2cm]
    \answer{$0.003$}
    \end{multicols}

    \wordProblem{Mia says the $5$ in $5{,}500$ and the $5$ in $550$ are worth the same. Is she right? Explain.}{~}
    \answer{No. In $5{,}500$ the first $5$ is worth $5{,}000$; in $550$ the first $5$ is worth $500$. They are $10$ times different.}
\end{stepPractice}
```

**Keep practice short** — aim for **5–6 problems** total. Use `\stepPracticeHeader[stepNColor]` to organize by step. Include 1–2 problems per step category plus 1 word problem.

## Full Template

```latex
% ============================================================================
% Section X.Y — Topic Title
% CCSS 5.XXX.X.X
% ============================================================================
\section{Topic Title}

\begin{stepGoal}
\begin{itemize}
    \item Goal 1 (keep to 2–3 goals)
    \item Goal 2
\end{itemize}
\end{stepGoal}

\begin{stepVocabBox}
    \vocabItem{Term 1}{Brief definition.}
    \vocabItem{Term 2}{Brief definition.}
\end{stepVocabBox}

\begin{stepsCard}[How to Do the Main Skill]
    \stepItem{Step 1 — one clear sentence.}
    \stepItem{Step 2 — one clear sentence.}
    \stepItem{Step 3 — one clear sentence.}
\end{stepsCard}

% --- 1–2 Worked Examples ---
\begin{stepExample}{Example problem statement.}
    \stepShow{1} Apply step 1...
    \stepShow{2} Apply step 2...
    \stepShow{3} Apply step 3...
    \stepResult{Final answer}
\end{stepExample}

% --- Optional: 1 tip or warning ---
\mascotStepTip{One helpful tip.}

% ============================================================================
% PRACTICE (4–5 problems)
% ============================================================================
\newpage
\begin{stepPractice}{Topic Practice}
    \resetProblems

    \stepPracticeHeader[step1Color]{Category 1}
    \prob Problem \answerBlank[2cm]
    \answer{answer}

    \stepPracticeHeader[step2Color]{Category 2}
    \begin{multicols}{2}
    \prob Problem \answerBlank[2cm]
    \answer{answer}
    \prob Problem \answerBlank[2cm]
    \answer{answer}
    \end{multicols}

    \stepPracticeHeader[step3Color]{Put It All Together}
    \prob Problem \answerBlank[2cm]
    \answer{answer}

    \wordProblem{Word problem text.}{unit}
    \answer{answer}
\end{stepPractice}
```

## Content Guidelines

### Keep It Brief — Target 2–3 Pages

The step-by-step book must match the study guide's page count (~130 pages). Every element must justify its space:

| Element | Budget |
|---------|--------|
| stepGoal + stepVocabBox | ~¼ page |
| stepsCard | ~¼ page |
| 1–2 stepExamples | ~½–¾ page |
| Optional tip/warning | 2–3 lines |
| stepPractice (5–6 problems) | ~¾–1 page |
| **Total** | **2–3 pages** |

If a topic runs to 3 pages, another should be 2 pages to compensate.

### Steps First, Examples Second

**Never** interleave step explanations with examples. The flow is always:
1. `stepsCard` — all steps listed
2. `stepExample` × 1–2 — worked examples applying all steps
3. Optional: `stepTryIt` (only if space allows)
4. `stepPractice` — independent practice

### Same Concepts, Procedural Approach

Step-by-step topics cover the **same math content** as the Study Guide but present it as a procedure-first lesson:

| Aspect | Study Guide | Step-by-Step |
|--------|-------------|--------------|
| Structure | conceptBox + worked examples | stepsCard + stepExamples |
| Title | `\section{}` + `\topicTitle{}` | `\section{}` only (no `\stepByStepTitle{}`) |
| Goals | `learningGoals` (2–3 items) | `stepGoal` (2–3 items) |
| Core element | conceptBox | `stepsCard` + `stepExample` |
| Vocabulary | inline in conceptBox | `stepVocabBox` with `\vocabItem` entries |
| Practice | `practiceBox` (flat list) | `stepPractice` with step headers |
| Practice count | 5–6 problems | 5–6 problems |
| Page count | 2–3 pages | 2–3 pages |

### Writing for the Target Audience

The script output includes the grade level and target student age range. Adapt your writing accordingly:
- **SHORT sentences** — one idea per sentence.
- **Everyday words** — "split", "share", "groups", "flip", "same as", "left over".
- **Address the student** — "you", "your".
- **Use relatable contexts** — school supplies, sports scores, recipes, sharing snacks, pocket money.
- **Match the math level to the grade** — use number ranges, operation types, and concept depth appropriate for the grade shown in the script output.

## TikZ Diagrams & Visual Aids
In some cases we might need to include a TikZ diagrams, shapes, or graphs to illustrate concepts (especially for geometry, coordinate plane, measurement, and circle topics).


## Page Budget

Target ~130 pages total for 44 core topics + initial pages + answer key:
- 44 topics × ~2.5 pages = ~110 pages
- Initial pages = ~4 pages
- Chapter openers (7) = ~7 pages
- Answer key = ~6 pages
- Running total = ~127 pages (leaves room for state additional topics)

This means each topic should average **2–3 pages**. If a topic runs to 3 pages, keep another at 2.

## Available Environments (VMfunSteps.sty)

| Environment/Command | Purpose |
|---|---|
| ~~`\stepByStepTitle{title}`~~ | **Do not use** — causes duplicate title |
| `stepGoal` | Learning objectives |
| `stepVocabBox` + `\vocabItem{word}{def}` | Grouped vocabulary box (title defaults to "Words to Know") |
| `stepsCard` + `\stepItem{text}` | Concise procedure listing (THE key element) |
| `stepExample{title}` | Worked example applying all steps |
| `\stepShow{n}` | Label which step is applied (inside example) |
| `\stepResult{answer}` | Final answer highlight (inside example) |
| `stepTryIt{title}` | Guided practice with blanks (optional — skip to save space) |
| `stepPractice{title}` + `\stepPracticeHeader[color]{title}` | Practice section |
| `\watchOut{text}` | Common mistake warning (at most 1 per topic) |
| `\mascotStepTip{text}` | Owl tip (at most 1 per topic) |

## LaTeX Conventions

- Use `$...$` for ALL math
- Use `\textbf{...}` to bold key terms on first use
- Use `\times` for multiplication, `\div` for division
- Every practice problem needs an answer: `\answer{}`, `\answerTF{}`, or `\answerMC{}`
- **Do NOT use `\answerExplain{}{}`** — explanations add too much volume. Use `\answer{}` instead to keep the book compact.
- Put `\newpage` before `stepPractice`

## Checklist

- [ ] Ran `python3 scripts/get_chapter_topic_facts.py --chapter <N>` to discover topics, grade, and audience
- [ ] Read every Study Guide source file listed by the script
- [ ] File placed in correct steps folder, filename matches the Study Guide source file
- [ ] `\section{}` present (NO `\stepByStepTitle{}`)
- [ ] `stepGoal` with 2–3 brief learning objectives
- [ ] `stepVocabBox` with 2–4 key terms
- [ ] `stepsCard` with clear descriptive title and 2–5 concise `\stepItem` entries
- [ ] 1–2 `stepExample` environments, each applying ALL steps
- [ ] `stepPractice` with **5–6 problems** organized by step
- [ ] Every problem has an answer (use `\answer{}`, NOT `\answerExplain{}{}`)
- [ ] All answers are mathematically correct
- [ ] NO `\encouragement{}`, `challengeBox`, `summaryBox`, or other extras
- [ ] At most 1 `\mascotStepTip{}` or `\watchOut{}` (not both)
- [ ] TikZ diagrams/shapes/graphs included when needed. 
- [ ] Topic is **2–3 pages** total
- [ ] Compile a test file in tests/ folder and open for my review and feedback
