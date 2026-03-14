---
name: writing-coaching-pages
description: How to write motivational pre-test and post-test coaching pages for Grade 8 math practice test books (6, 9, and 12 test variants). Covers the narrative arc, file structure, LaTeX template, integration into main .tex files, and creative guidelines. Use when asked to create, rewrite, or update coaching pages for any practice test book.
---

# Writing Coaching Pages for Practice Test Books

## What Are Coaching Pages?

Each practice test in the book is sandwiched between two **single-page coaching inserts**:

- **Pre-test page** — appears *before* the test. Motivates the student, teaches a test-taking strategy, and sets a positive mindset.
- **Post-test page** — appears *after* the score page. Guides the student to reflect on their results, categorize mistakes, and plan next steps.

Together they create a **narrative arc**: the student progresses from nervous beginner to confident test-taker by the final test.

## Audience

Grade 7 students (11–12 years old) preparing for state math tests. These are kids who may feel anxious about tests. The tone is:

- **Warm and encouraging** — like a friendly coach, not a textbook
- **Conversational** — use "you" and "let's" freely
- **Simple vocabulary** — short sentences, plain words
- **Never condescending** — respect their intelligence while keeping it accessible

## File Locations

```
coaching_pages/
├── 6_practice_tests/       ← 6-test book (tests 01–06)
│   ├── pre_test_01.tex
│   ├── post_test_01.tex
│   ├── pre_test_02.tex
│   ├── ...
│   └── post_test_06.tex
├── 9_practice_tests/       ← 9-test book (tests 07–15)
│   ├── pre_test_07.tex
│   ├── post_test_07.tex
│   ├── ...
│   └── post_test_15.tex
└── 12_practice_tests/      ← 12-test book (tests 16–27)
    ├── pre_test_16.tex
    ├── post_test_16.tex
    ├── ...
    └── post_test_27.tex
```

**Naming convention:** `pre_test_NN.tex` and `post_test_NN.tex` where `NN` matches the practice test number in the `practice_tests_2/` directory.

**Practice test numbering by book type:**

| Book | Tests | Files |
|---|---|---|
| 6 practice tests | 01–06 | `pre/post_test_01` through `pre/post_test_06` |
| 9 practice tests | 07–15 | `pre/post_test_07` through `pre/post_test_15` |
| 12 practice tests | 16–27 | `pre/post_test_16` through `pre/post_test_27` |




## The Narrative Arcs

Each book type has its own narrative arc. The arcs below define the **theme and focus** for each test position. You have creative freedom in the actual content—different words, different examples, different structures—but the **progression of themes** should be followed.

### 6-Test Book Arc (Tests 01–06)

A compact journey: build confidence fast across 6 tests and 180 questions.

#### Pre-Test Arc

| Test | Theme | Focus |
|---|---|---|
| 1 | Foundation | First test. No pressure. Just try everything. Establish a baseline. |
| 2 | Strategy | Introduce time management. Plan how to use 30 questions' worth of time. |
| 3 | Techniques | Problem-solving tricks: process of elimination, working backward, estimation. |
| 4 | Precision | Avoiding careless mistakes. Read carefully, check your work, watch for traps. |
| 5 | Resilience | Pushing through hard problems. Confidence when stuck. Power of skipping and returning. |
| 6 | Test Day Confidence | The final simulation. Treat it like the real exam. You're ready. |

#### Post-Test Arc

| Test | Theme | Focus |
|---|---|---|
| 1 | Baseline Analysis | Understand your starting score. Categorize what you know vs. what needs work. |
| 2 | Error Categorization | Diagnose mistakes: careless errors vs. knowledge gaps vs. misread questions. |
| 3 | Cross-Test Patterns | Look across Tests 1–3. Which topics keep showing up as weak spots? |
| 4 | Growth Tracking | Compare scores. Celebrate improvement. Identify remaining gaps. |
| 5 | Targeted Review | Deep focus on lingering weak areas before the final test. |
| 6 | Complete Journey | 180 questions done. Celebrate the full arc. Final readiness reflection. |

---

### 9-Test Book Arc (Tests 07–15)

A longer journey with room to develop strategies thoroughly over 270 questions.

#### Pre-Test Arc

| Test | Theme | Focus |
|---|---|---|
| 7 (1st) | Setting the Foundation | First test. No time limit. Just try every question. |
| 8 (2nd) | Two-Pass Method | Teach the strategy: easy questions first, hard ones second. |
| 9 (3rd) | Working Smarter | Problem-solving techniques: estimation, elimination, back-solving. |
| 10 (4th) | Focus & Precision | Avoiding traps. Reading questions carefully. Checking answers. |
| 11 (5th) | Time Management | Racing the clock. Pacing strategies for timed conditions. |
| 12 (6th) | Multi-Step Problems | Breaking complex problems into smaller steps. |
| 13 (7th) | Resilience | Pushing through challenges. Dealing with frustration. |
| 14 (8th) | Speed + Accuracy | Balancing pace and precision. Getting faster without getting sloppy. |
| 15 (9th) | Test Day Confidence | Final simulation. You've trained hard. Trust your preparation. |

#### Post-Test Arc

| Test | Theme | Focus |
|---|---|---|
| 7 (1st) | Baseline Analysis | Your starting point. Score reflection and initial self-assessment. |
| 8 (2nd) | Error Diagnosis | Categorize every wrong answer: careless, conceptual, or misread. |
| 9 (3rd) | Pattern Finding | Look across Tests 1–3 for recurring weak topics. |
| 10 (4th) | Growth Measurement | Score comparison. Track your trajectory. |
| 11 (5th) | Mid-Point Check-In | Halfway through! Deep 5-test reflection. Strengths and weaknesses audit. |
| 12 (6th) | Targeted Deep Dive | Focus study plan for specific weak chapters/topics. |
| 13 (7th) | Strategy Audit | Evaluate which test-taking strategies are working and which aren't. |
| 14 (8th) | Fine-Tuning | Small adjustments. Polish weak spots before the final test. |
| 15 (9th) | Complete Journey | 270 questions done. Celebrate everything. Final readiness check. |

---

### 12-Test Book Arc (Tests 16–27)

The most comprehensive journey: 360 questions across 4 clear phases.

#### Pre-Test Arc — 4 Phases

**Phase 1: Foundation (Tests 1–3)**

| Test | Theme | Focus |
|---|---|---|
| 16 (1st) | Marathon Mindset | 12 tests is a marathon. Set expectations. No pressure on test 1. |
| 17 (2nd) | Read Like a Detective | Careful reading. Understand what the question is really asking. |
| 18 (3rd) | Two-Pass Method | Answer easy questions first, come back to hard ones. |

**Phase 2: Core Toolkit (Tests 4–6)**

| Test | Theme | Focus |
|---|---|---|
| 19 (4th) | Process of Elimination | Strategic guessing. Narrow choices before answering. |
| 20 (5th) | Show Your Work | Writing out steps catches errors and earns partial credit. |
| 21 (6th) | Visual Strategies | Drawing diagrams, number lines, and pictures to solve problems. |

**Phase 3: Advanced Strategies (Tests 7–9)**

| Test | Theme | Focus |
|---|---|---|
| 22 (7th) | Multi-Step Problems | Breaking complex problems into manageable pieces. |
| 23 (8th) | Time Management | Pacing yourself. Knowing when to move on. |
| 24 (9th) | Mid-Journey Checkpoint | Pause and reflect. How far you've come. Reset for the home stretch. |

**Phase 4: Mastery (Tests 10–12)**

| Test | Theme | Focus |
|---|---|---|
| 25 (10th) | Avoiding Common Traps | Error prevention. Recognizing trick questions and common pitfalls. |
| 26 (11th) | Speed + Precision | Balancing accuracy and pace for maximum performance. |
| 27 (12th) | Test Day Ready | Final simulation under real conditions. You've earned this confidence. |

#### Post-Test Arc — 4 Phases

**Phase 1: Understanding (Tests 1–3)**

| Test | Theme | Focus |
|---|---|---|
| 16 (1st) | Starting Point | Baseline score. Initial reflection. Setting goals. |
| 17 (2nd) | Celebrating Strengths | Focus on what went RIGHT. Build on existing strengths. |
| 18 (3rd) | Three Error Types | Categorize mistakes: careless, conceptual, misread. |

**Phase 2: Patterns (Tests 4–6)**

| Test | Theme | Focus |
|---|---|---|
| 19 (4th) | Topic Tracker | Map wrong answers to specific math topics across all tests so far. |
| 20 (5th) | Growth Measurement | Score comparison chart. Visualize improvement. |
| 21 (6th) | Halfway Review | Deep self-assessment at the midpoint. Comprehensive strengths/weaknesses. |

**Phase 3: Targeted Improvement (Tests 7–9)**

| Test | Theme | Focus |
|---|---|---|
| 22 (7th) | Deep Dive on Weak Spots | Create a focused study plan for weakest topics. |
| 23 (8th) | Strategy Report Card | Evaluate which test strategies are working. Adjust approach. |
| 24 (9th) | Three-Quarter Mark | Score trend analysis. Project growth. Motivational push. |

**Phase 4: Final Polish (Tests 10–12)**

| Test | Theme | Focus |
|---|---|---|
| 25 (10th) | Fine-Tuning | Final small adjustments. Target the last few weak spots. |
| 26 (11th) | Home Stretch | Comprehensive review of all progress. Almost there. |
| 27 (12th) | Complete Journey | 360 questions done. Full celebration. Readiness declaration. |

---

## Creative Freedom

The arcs above define **what** each page is about. You decide **how** to express it. You are encouraged to:

- **Write completely different content** than existing pages. Same theme, new words.
- **Use different metaphors and analogies.** Sports, cooking, video games, detective stories, building things — whatever resonates.
- **Vary the closing encouragement.** Don't repeat the same patterns.

**What must stay consistent:**
- The overall file skeleton (clearpage → sffamily → title → boxes → closing)
- One page per file, one printed page per coaching insert
- The theme/focus for each test position as defined in the arcs
- Warm, encouraging, age-appropriate tone
- Color-coded themes (use the color palette, vary across pages)
- FontAwesome icons in titles and content

**What you should NOT do:**
- Don't write identical content to existing coaching pages — always bring fresh language
- Don't write text walls — use structure (tables, lists, fill-in blanks)
- Don't be preachy or over-the-top with praise
- Don't reference specific answer keys or question numbers (content is state-specific)
