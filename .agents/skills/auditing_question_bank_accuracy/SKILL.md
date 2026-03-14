---
name: auditing_question_bank_accuracy
description: "Audit math question bank files for answer-key and explanation accuracy. Use when asked to check, verify, review, or audit answers, correct answers, explanations, or calculations in test question bank files (bank 1 or bank 2). Covers locating source files, verifying every \\correctAnswer and \\explanation, fixing errors, and compiling to validate."
---

# Auditing Question Bank Accuracy

## Overview

This skill guides you through a rigorous chapter-by-chapter accuracy audit of the Grade 7 math question bank LaTeX files. The goal is to catch wrong answer keys (`\correctAnswer`) and incorrect math in explanations (`\explanation`), then fix them with minimal changes.

## When to Use

- User asks to "check", "verify", "audit", or "review" question bank answers or explanations
- User mentions "calculations", "accuracy", "correct answer", or "miscalculations" in the context of test questions
- User references a specific chapter's question bank

## Question Bank Structure

There are **two independent question bank sets**:

| Bank | Source directory | Assembled review docs | Books that use it |
|---|---|---|---|
| Bank 1 | `tests_questions_bank/` | `tests/grade7_test_questions_bank_ch{N}.tex` | 3, 5, 7, 10 practice tests |
| Bank 2 | `tests_questions_bank_2/` | `tests/grade7_test_questions_bank_2_ch{N}.tex` | 6, 9, 12 practice tests |

Within each bank directory, source files live in three subdirectories:

```
tests_questions_bank_2/
    topics/              # Core CCSS topic question files
    topics_additional/   # Additional state-specific topic questions
    topics_modified/     # Modified topic questions
```

Each source file contains 27 questions: 15 multiple choice (`mc`), 6 short answer (`sa`), and 6 graphical (`gmc`/`gsa`).

## Procedure

### Step 1: Identify the Exact Source Files

First, run the chapter-facts Python script to discover the topic IDs and relative file paths for that chapter:

```bash
p scripts/get_chapter_topic_facts.py --chapter {N}
```

This prints the chapter's:
- core topic files under `topics/`
- additional topic files under `topics_additional/`
- modified topic files under `topics_modified/`

Use that output to build the exact bank-specific source file list:

- For **bank 1**, prepend `tests_questions_bank/` to each printed file path.
- For **bank 2**, prepend `tests_questions_bank_2/` to each printed file path.

Then read the assembled chapter review document to confirm the exact `\input{}` lines:

```
tests/grade7_test_questions_bank_2_ch{N}.tex   # for bank 2
tests/grade7_test_questions_bank_ch{N}.tex      # for bank 1
```

The script tells you what topic files exist for the chapter, and the assembled review file confirms which ones are actually included in that bank/chapter build. Do not guess.

### Step 2: Read Every Source File

Read each source file in full. Do not skim or sample. Every question must be checked.

### Step 3: Verify Each Question

For every question, perform these checks:

#### Multiple Choice (`mc` and `gmc`)

1. **Independently compute the correct answer first.** Solve the problem yourself before looking at any choices. This prevents anchoring bias.
2. **Expand / evaluate EVERY choice.** Do not just check the keyed answer — work out what each choice (A, B, C, D) actually equals. For factoring questions, expand each factored form by distributing. For scientific notation, convert each choice to standard form. For equations, substitute each proposed answer back in. This is the single most important step: many bugs are only visible when you verify that the *wrong* choices really are wrong.
3. **Confirm the keyed answer is correct.** Verify that `\correctAnswer{X}` matches the only choice that equals the right value.
4. **Check the explanation math step by step.** Walk through the arithmetic or algebra in `\explanation{}` and confirm every intermediate step is correct. Watch for sign errors, exponent mistakes, and wrong arithmetic.
5. **Check for contradictions.** Does the explanation arrive at the same answer as `\correctAnswer`? If the explanation derives one answer but the key says another, that's a bug.

#### Short Answer (`sa` and `gsa`)

1. **Solve the problem independently** and compare your result with `\correctAnswer{}`.
2. **Walk through the explanation** to verify each step matches the stated answer.

#### Graphical Questions

1. **Read the TikZ code carefully** to understand what the graphic actually shows (coordinates, labels, plotted points).
2. **Verify the answer matches the graphic**, not just the text description. A common bug is the explanation describing one thing while the TikZ code draws another.

### Step 4: Classify What You Find

Only flag issues where:
- The `\correctAnswer` is objectively wrong
- The `\explanation` contains a calculation error, wrong intermediate result, or a factually false statement
- The explanation contradicts the keyed answer

**Do NOT flag or change** (unless the user explicitly requests it):
- Distractor choices that happen to be equivalent to each other or to the correct answer — do not rewrite distractors
- Style or wording preferences
- Missing context that doesn't affect correctness

> **Hard rule — `\correctAnswer` changes:**
>
> - **Only change `\correctAnswer` when the current value is objectively, mathematically wrong.** If the existing answer is correct, leave it alone — even if you think additional words or context could be added.
> - For **multiple-choice** questions the correct answer must be a single letter (A, B, C, or D). Never expand it into words or a phrase.
> - For **short-answer / graphical** questions the correct answer should be the shortest correct response — typically one or two numbers, a single expression, or at most a few words. Do **not** pad a correct short answer with extra explanation, qualifiers, or reworded phrasing. If the existing text is mathematically correct and answers the question, it is good enough.
> - **Never** modify `\choiceA` / `\choiceB` / `\choiceC` / `\choiceD` text. If a distractor is identical to the keyed answer, change only the key and explanation to point to the right choice — do not rewrite the choice text.

### Step 5: Fix with Minimal Changes

For each confirmed issue:

1. **Change only what is necessary.** If the answer key is wrong but the explanation is right, change only `\correctAnswer`. If both are wrong, fix both.
2. **Do not rewrite surrounding questions** that are correct.
3. **Do not restructure distractors** unless the user specifically asks for it.
4. **Preserve the original phrasing** wherever possible — change numbers and math, not prose.

### Step 6: Validate with Audit Review PDF

After editing, build a review PDF containing **only the changed files** so the user can visually verify the corrections.

#### 6a. Copy the audit-review template

```bash
cp audit_review_template.tex tests/audit_review.tex
```

#### 6b. Insert the changed files

Edit `tests/audit_review.tex`: between the `%%% INSERT CHANGED FILES BELOW %%%` and `%%% INSERT CHANGED FILES ABOVE %%%` comment markers, add one `\input{}` block per changed file. Use the same pattern as the chapter review documents:

```latex
\newpage
\section*{1-1: Rational and Irrational Numbers}
\input{tests_questions_bank_2/topics/ch01-01-rational-and-irrational-numbers}
```

Include **every** file you edited — no more, no less. The `\section*{}` title should indicate the bank (1 or 2) and subdirectory (core `topics/`, `topics_additional/`, or `topics_modified/`) so the user can trace each fix to its source.

Question numbering resets automatically at each `\section*{}`.

#### 6c. Compile the review PDF

```bash
cd /path/to/Grade7
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build tests/audit_review.tex
```

If compilation fails, check editor diagnostics on every changed file and fix any LaTeX syntax errors before retrying.

#### 6d. Open the PDF for the user

```bash
open build/audit_review.pdf
```

This lets the user visually inspect every corrected question, its answer key, and explanation in rendered form.

#### 6e. Report what you fixed

List each question ID, the file it lives in, what was wrong, and what you changed.

## Common Error Patterns

These are the most frequent bugs found in past audits:

| Pattern | Example | Where to look |
|---|---|---|
| **Sign error in factoring** | `−4x(x + 2)` claimed to equal `−4x² + 8x` but actually gives `−4x² − 8x` (caught in 3-8-q15: key said "Both A and B" but expanding A shows it's wrong) | Factoring and expanding questions |
| **Explanation contradicts key** | Explanation derives answer A but `\correctAnswer{B}` | Any question type |
| **Wrong graph interpretation** | TikZ plots point at (3, 4) but explanation says "the point is at (3, 5)" | Graphical questions (`gmc`, `gsa`) |
| **Arithmetic slip in explanation** | "5 × 8 = 45" or "$3^{-2} = \frac{1}{6}$" | Scientific notation, exponents |
| **Financial formula error** | Interest calculated as $P \times r$ instead of $P \times r \times t$ | Financial literacy topics |

## Reporting Format

After completing the audit, summarize:

1. **How many source files were audited** (and list them).
2. **Issues found and fixed** — one bullet per fix with question ID, file, what was wrong, and what you changed.
3. **Compilation result** — confirm the chapter review document compiled successfully.
4. **Clean bill of health** — explicitly state if no other issues were found, so the user knows the audit is complete rather than abandoned.
