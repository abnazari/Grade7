---
name: writing_workbook_topics
description: How to write practice-focused workbook topics for Grade 7 math
---

# Writing Workbook Topics

## Overview

Workbook topics are **practice-focused** companions to the study guide. They replace lengthy teaching with a brief concept refresher (`quickReview`) followed by structured, progressive practice. Each topic targets **25–31 total problems** so students stay engaged without fatigue.

## Important notice
- When the user asks you to write a the workbook topics for a chapter, you should look at topics/ and topics_additional/ and topics_modified/ folders to find the corresponding study guide topics. You should read those first to understand the concepts, vocabulary, problem types, and difficulty level before writing the workbook topics. For every topic file, you should write a corresponding workbook topic file with the same filename in the appropriate workbook folder (topics_workbook/, topics_workbook_additional/, or topics_workbook_modified/). 

## Workflow: Read the Study Guide Topic First

Before writing any workbook topic, **read the corresponding Study Guide topic** to understand:
- What concepts are taught
- What vocabulary is introduced
- What difficulty level and number range is used
- What types of problems appear in the practice section

The source topic determines which folder to write the workbook file into:

| Study Guide source folder | Workbook output folder |
|--------------------------|------------------------|
| `topics/` | `topics_workbook/` |
| `topics_additional/` | `topics_workbook_additional/` |
| `topics_modified/` | `topics_workbook_modified/` |

**The workbook file must use the same filename as the Study Guide file.** For example, if the Study Guide topic is `topics/ch03-07-decimal-word-problems.tex`, the workbook version goes in `topics_workbook/ch03-07-decimal-word-problems.tex`.

## File Naming

Format: `ch<CC>-<SS>-<slug>.tex`

Examples:
- `ch01-01-place-value-relationships.tex`
- `ch03-07-decimal-word-problems.tex`

Use the same section numbering and slug from the curriculum map in `.agents/skills/grade6_curriculum/SKILL.md`.

## Topic Structure

Every workbook topic needs these elements, but you have **creative freedom** in how you structure them:

### Required Elements
1. **Section header** — `\section{}` + `\topicTitle{}`
2. **Quick Review** — brief concept refresher using `quickReview` environment
3. **Warm-Up** — 5–6 easy confidence-building problems
4. **Practice sections** — the bulk of the problems, organized however fits the topic
5. **`\encouragement{}`** — motivational closing message

### Target Problem Counts
- **Warm-Up:** 5–6 problems (easy confidence builders)
- **Remaining practice (all other sections combined):** 20–25 problems
- **Total per topic:** ~25–31 problems

How you split the 20–25 practice problems is up to you. Some topics might work well with 3 small practice boxes, others with 2 larger ones. You might include true/false, word problems, a challenge section, or skip some of those if the topic calls for something different. **Choose the structure that best serves the concept.**

## Section Guide

### Section Header (required)

```latex
\section{Place Value Relationships}
\topicTitle{Place Value Relationships}
```

Use the exact title from the curriculum map.

### Quick Review (required)

The `quickReview` environment provides a compact concept refresher — just enough for students to recall the key idea before practicing. It is **not** a full teaching section.

```latex
\begin{quickReview}{Place Value Relationships}
Each place in a number is \textbf{10 times} the value of the place to its right and \textbf{one-tenth} the value of the place to its left.

\begin{itemize}[leftmargin=*]
    \item Whole-number places: $\dots$ thousands, hundreds, tens, ones.
    \item Decimal places: tenths, hundredths, thousandths.
    \item Moving left $\to$ multiply by $10$. \quad Moving right $\to$ divide by $10$.
\end{itemize}

\medskip
\textbf{Example:} In $\mathbf{4.735}$: \quad $4$ ones $= 4$, \quad $7$ tenths $= 0.7$, \quad $3$ hundredths $= 0.03$, \quad $5$ thousandths $= 0.005$.

\smallskip
\textbf{Key relationship:} The $7$ in the tenths place is $10$ times the $7$ in the hundredths place.
\end{quickReview}
```

Keep it to roughly 8–15 lines. Bold key terms. Include 1–2 worked examples. Default color is `funOrange`; optional color parameter: `\begin{quickReview}[funTeal]{Title}`.

### Warm-Up (required, 5–6 problems)

Start with easy problems to build confidence. Example:

```latex
\begin{practiceBox}[funGreen]{\faSun~Warm-Up}

\practiceHeader[funGreen]{Name the Place}
What place is the underlined digit in?

\begin{multicols}{2}
\prob $3.\underline{4}52$ \answerBlank[3cm]
\answerExplain{Tenths}{The underlined digit 4 is one place to the right of the decimal point, which is the tenths place.}
\prob $12.7\underline{8}1$ \answerBlank[3cm]
\answerExplain{Hundredths}{The underlined digit 8 is two places to the right of the decimal point, which is the hundredths place.}
% ... 5–6 total
\end{multicols}
\end{practiceBox}
```

### Practice Sections (flexible, 15–20 problems total)

This is where you have the most creative freedom. Organize the remaining problems in whatever way best fits the topic. Some ideas:

- **Multiple `practiceBox` environments** with different sub-skills (e.g., "Write the Value" then "Expanded Form" then "Standard Form")
- **True/False section** using `\trueOrFalse{}` + `\answerExplain{True/False}{explanation}`
- **Word Problems** using `\wordProblem{}{}` + `\answerExplain{}{}`
- **Challenge problems** in a `challengeBox`
- **Find the mistake** using `errorBox`
- **Classifying/sorting** using `sortBox` + `\sortCategory`
- **Fill-in-the-blank** using `findMissingBox`

Use different colors on practice boxes for visual variety. Available colors: `funBlue`, `funGreen`, `funOrange`, `funPurple`, `funRed`, `funYellow`, `funTeal`, `funPink` (each with `Dark`/`Light` variants).

Progress difficulty from straightforward to harder throughout the practice sections.

### Encouragement (required)

```latex
\encouragement{Great job practicing place value! You are building strong number sense!}
```

End every topic with a unique, motivating message related to the skill practiced.

## Enforced Rules

These rules are **non-negotiable** and must be followed in every workbook topic:

### No `\resetProblems`

**Never** use `\resetProblems` in workbook topics. Problem numbering must be continuous across all practice sections within a topic (1 through N). This ensures the answer key has unique problem numbers per section.

The study guide uses `\resetProblems` inside practiceBox — the workbook does **not**.

### Every Problem Needs a Short Answer AND an Explanation

Every numbered problem needs two things: a **short answer** (printed in the Answer Key at the back of the book) and an **explanation** (how the student can arrive at that answer — kept in the source file only, not printed).

This mirrors how practice test question banks work (see `practice_questions_bank/` files), where every question has `\correctAnswer{short}` + `\explanation{reasoning}`. In workbook topics, we use `\answerExplain{short answer}{explanation}` to achieve the same thing.

**Use `\answerExplain{}{}` for every problem type:**

| Problem type | Answer command |
|---|---|
| `\prob` | `\answerExplain{short answer}{explanation}` |
| `\trueOrFalse{...}` | `\answerExplain{True or False}{explanation}` |
| `\multiChoice{...}` | `\answerExplain{letter}{explanation}` |
| `\circleAnswer{...}` | `\answerExplain{letter}{explanation}` |
| `\wordProblem{...}` | `\answerExplain{short answer}{explanation}` |

**How it works:**
- **First argument** = the short answer. This is what gets printed in the Answer Key chapter at the back of the book. Keep it concise — just the answer itself.
- **Second argument** = the explanation. This is how a student can get to that answer. It stays in the source `.tex` file only (never printed). It helps authors verify correctness, and helps parents/teachers understand the solution path.

**Write meaningful, pedagogical explanations.** Remember that the student *just learned* this topic in the study guide — they don't fully understand it yet. The explanation should help them see *why* the answer is correct, not just *what* the answer is. Since explanations live only in the source file, there's no space cost in the printed book — use the full line.

**Explanation guidelines:**

1. **Target 1–2 lines.** Every explanation should be at least one full sentence. Bare formulas like `$5 \times 100$` are never enough.
2. **Name the concept or rule** being applied (e.g., "Order matters in a ratio," "To find the unit rate, divide," "Percent means per 100").
3. **Show the steps AND explain what each step does.** Don't just write `$36 \div 6 = 6$ apples per bag` — write `Divide the total by the number of groups: $36 \div 6 = 6$. Each bag holds $6$ apples.`
4. **Connect back to the topic.** If the problem is about unit rates, mention "unit rate" in the explanation. If it's about equivalent ratios, say "equivalent."
5. **Avoid one-word justifications** like "Multiply" or `$0.40 \times 85 = 34$` with no context.

```latex
% ✗ Too short — just a formula, doesn't help the student understand
\prob $\underline{5}73$ \answerBlank[2cm]
\answerExplain{$500$}{$5 \times 100$}

% ✗ Too short — restates the computation but doesn't explain WHY
\prob $36$ apples in $6$ bags \answerBlank[3cm]
\answerExplain{$6$ apples per bag}{$36 \div 6 = 6$ apples per bag.}

% ✓ Good — names the concept, shows the step, explains the result
\prob $\underline{5}73$ \answerBlank[2cm]
\answerExplain{$500$}{The digit 5 is in the hundreds place, so its value is $5 \times 100 = 500$.}

% ✓ Good — tells the student WHAT to do and WHY
\prob $36$ apples in $6$ bags \answerBlank[3cm]
\answerExplain{$6$ apples per bag}{To find the unit rate, divide the total by the number of groups: $36 \div 6 = 6$. This means each bag holds $6$ apples.}

% ✓ Good — true/false with explanation of why
\trueOrFalse{In $843$, the digit $8$ is in the tens place.}
\answerExplain{False}{The digit $8$ is in the hundreds place, not the tens place. The tens digit is $4$.}

% ✓ Good — word problem with full reasoning
\wordProblem{A store sold $183$ apples. Round to the nearest $10$.}{apples}
\answerExplain{$180$ apples}{The ones digit is $3$, which is less than $5$, so we round down. The tens digit stays $8$, giving us $180$.}

% ✓ Good — challenge with step-by-step reasoning
\prob I am a $3$-digit number. My hundreds digit is double my ones digit. My tens digit is $5$. My ones digit is $3$. What number am I? \answerBlank[2cm]
\answerExplain{$653$}{Ones digit is $3$. Hundreds digit is double the ones: $3 \times 2 = 6$. Tens digit is $5$. So the number is $653$.}
```

See `.agents/skills/writing_answers/SKILL.md` for the full answer command reference.

### Math Mode

All numerical answers must be in `$...$`:
```latex
\answerExplain{$500$}{...}    % ✓
\answerExplain{500}{...}      % ✗ — no math mode
\answerExplain{True}{...}     % ✓ (text, not math)
```

### Environment Matching

Every `\begin{env}` must have a matching `\end{env}`:
```latex
\begin{practiceBox}    → \end{practiceBox}
\begin{challengeBox}   → \end{challengeBox}
\begin{findMissingBox} → \end{findMissingBox}
```

### Correct Math

**Always verify every answer is mathematically correct.** Incorrect answers in an answer key destroy student trust.

## Available Environments & Commands

For the complete environment reference, see `.agents/skills/latex_environments/SKILL.md`. Here are the most relevant ones for workbook topics:

### Environments
- `quickReview` — concept refresher (required, one per topic)
- `practiceBox` — main practice container with optional color: `\begin{practiceBox}[funTeal]{Title}`
- `challengeBox` — star-themed harder problems
- `findMissingBox` — fill-in-the-blank style
- `errorBox` — "find the mistake"
- `sortBox` / `sortCategory` — classifying

### Problem Commands
- `\prob` — numbered problem
- `\trueOrFalse{}` — true/false statement
- `\wordProblem{question}{unit}` — word problem with answer line
- `\multiChoice{question}{A}{B}{C}{D}` — multiple choice
- `\circleAnswer{question}{A}{B}{C}{D}` — circle correct answer
- `\answerBlank[width]` — blank line for student answer

### Layout & Helpers
- `\begin{multicols}{2}` / `{3}` — multi-column layout
- `\practiceHeader[color]{Title}` — subsection header within a practiceBox
- `\mascotSays{}` — owl character tip (use sparingly in workbook)
- `\encouragement{}` — closing motivational message

## Example Topic

Here's one way to structure a workbook topic (not the only way):

```latex
% ============================================================================
% WORKBOOK — Section 1.1: Place Value Relationships
% CCSS 5.NBT.A.1
% Practice-focused reinforcement for the study guide topic
% ============================================================================
\section{Place Value Relationships}
\topicTitle{Place Value Relationships}

\begin{quickReview}{Place Value}
\textbf{Place value} tells us how much a digit is worth based on where it sits.
% ... brief recap with example
\end{quickReview}

\begin{practiceBox}[funGreen]{\faSun~Warm-Up}
% 5–6 easy problems
\end{practiceBox}

\begin{practiceBox}{What Is the Value?}
% 6 value-of-digit problems + 4 expanded form problems
\end{practiceBox}

\begin{practiceBox}[funTeal]{Write the Standard Form}
% 4 problems
\end{practiceBox}

\begin{practiceBox}[funPurple]{True or False?}
% 4 true/false problems
\end{practiceBox}

\begin{practiceBox}[funTeal]{\faGlobe~Word Problems}
% 3 word problems
\end{practiceBox}

\begin{challengeBox}
% 2 challenge problems
\end{challengeBox}

\encouragement{Great job practicing place value!}
```

## Workbook vs Study Guide — Key Differences

| Aspect | Study Guide | Workbook |
|--------|------------|----------|
| Teaching content | Extensive (conceptBox, stepsBox, vocabBox, etc.) | Minimal (quickReview only) |
| Practice problems | 15–25 in one practiceBox | 25–31 across multiple boxes |
| `\resetProblems` | Yes (inside practiceBox) | **No** (continuous numbering) |
| Creative environments | Many (codeBreaker, riddleBox, mathTrail, etc.) | Optional, use if it fits |
| Visual math (TikZ) | Frequent | Only inside quickReview if useful |
| Primary goal | Teach + practice | Practice + reinforce |
| Typical page count | 5–10 pages per topic | 2–4 pages per topic |

## Checklist Before Submitting

- [ ] Read the corresponding Study Guide topic first
- [ ] File placed in the correct workbook folder matching the source folder
- [ ] Filename matches the Study Guide topic file
- [ ] `\section{}` and `\topicTitle{}` match curriculum map title
- [ ] `quickReview` present with brief recap
- [ ] Warm-Up has 5–6 problems
- [ ] Total problems: 25–31
- [ ] **No `\resetProblems` anywhere in file**
- [ ] Every problem uses `\answerExplain{short answer}{explanation}` — short answer for the key, explanation of how to get there
- [ ] All answers are mathematically correct
- [ ] Answers use math mode where appropriate
- [ ] All `\begin{}` have matching `\end{}`
- [ ] `\encouragement{}` at end
- [ ] Create a test latex file inside tests/ folder, include all crteated files, compile and open the pdf for review. Use same style as the workbook main latex file. 
