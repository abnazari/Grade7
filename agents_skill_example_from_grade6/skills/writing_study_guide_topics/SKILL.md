---
name: writing_study_guide_topics
description: Guidelines for writing engaging Grade 6 math study guide topics
---

# Writing Grade 6 Math Study Guide Topics

## CRITICAL — Page Budget

The finished book MUST be **130–150 pages total** (including front matter, all topics, and the answer key). There are **44 topics**, so each topic averages roughly **2–3 printed pages**. That means:

- **Target: 80–120 lines of LaTeX per topic file.** This is the single most important constraint. If your file is over 120 lines, cut it down. Every sentence must earn its place.
- A simple topic (e.g., "What Is a Ratio?") might be 70–90 lines (~2 pages).
- A dense topic (e.g., "Dividing Fractions by Fractions") can go up to 130 lines (~3 pages) but no more.
- **Never exceed 3 printed pages for any single topic.**

When in doubt, cut. A short, clear explanation that a student actually reads beats a long one they skip.

## The Book

This is a single-edition Grade 6 math book. Each topic should teach ONE concept clearly and give students practice — nothing more. Keep it tight.

Topic files live in `topics/`. File naming: `ch01-01-slug-here.tex`

## Audience: 11–12 Year Olds (Grade 6)

Write for a smart, curious 11-year-old. These are young students — make every explanation **dead simple**.

- **Use very short sentences.** Aim for **8–12 words per sentence**. One idea per sentence. If a sentence has a comma, consider splitting it.
- **Use the simplest words possible.** Say "find" not "determine." Say "shows" not "demonstrates." Say "same" not "equivalent" (until you define it). Write how you would talk to a kid.
- **Simple first, formal second.** Say "flip and multiply" before "multiply by the reciprocal." Always teach the real math term too, but lead with the plain-English version.
- **Conversational, not textbook-stiff.** Use "you" and "let's" freely. Keep it warm but not babyish.
- **Connect to their world.** Sports scores, video games, cooking, shopping, phone plans — use things they know.
- **Be encouraging without overdoing it.** One "Nice work!" is plenty. Skip filler praise.
- **Cut any sentence that doesn't teach something.** If you remove a sentence and the topic still makes sense, remove it.

## Writing Style — Concise and Crystal Clear

Every word must earn its place. Here are concrete examples:

| Too wordy (DON'T) | Concise (DO) |
|---|---|
| "A ratio is a mathematical comparison that shows the relationship between two quantities or amounts." | "A ratio compares two amounts." |
| "In order to find the unit rate, you will need to divide both numbers so that the second one becomes 1." | "To find the unit rate, divide so the second number is 1." |
| "Let's take a look at an example to see how this works in practice." | (Just show the example — skip the transition.) |
| "Now that we've learned about ratios, let's practice what we've learned!" | (Just start the practice section — no need to announce it.) |

**Rules:**
- **Delete transition sentences.** "Let's see how this works" → just show it.
- **Delete summary filler.** "Now you know how to..." → cut it.
- **One sentence per idea.** If a sentence has "and" connecting two ideas, split it.
- **No redundancy.** If the `conceptBox` explains it, don't re-explain it in prose before the example.
- **Definitions: one sentence.** "A **rate** is a ratio that compares two different units." Done.

## Content Standards

Follow **Common Core State Standards (CCSS)** for Grade 6. The five domains are:

1. **Ratios and Proportional Relationships (6.RP)** — ratios, rates, unit rates, percents, measurement conversion
2. **The Number System (6.NS)** — fraction division, multi-digit operations, decimals, GCF/LCM, integers, absolute value, coordinate plane
3. **Expressions and Equations (6.EE)** — exponents, order of operations, algebraic expressions, one-step equations, inequalities, dependent/independent variables
4. **Geometry (6.G)** — area of triangles/parallelograms/trapezoids, volume, nets and surface area, polygons on the coordinate plane
5. **Statistics and Probability (6.SP)** — statistical questions, center/spread/shape, mean/median, dot plots, histograms, box plots

Numbers at this level: multi-digit whole numbers, decimals, fractions (any denominator), positive AND negative numbers (integers and rationals). This is much broader than Grade 4 — students are expected to work fluently with all rational numbers.

## Creative Freedom

You have access to **100+ environments and commands** (see the toolkit reference below). There is no rigid template. Your job is to pick the combination that best serves each topic.

**General principles:**
- **Teach the concept, then let them practice.** That's the only hard structure rule.
- **Be ruthlessly concise.** Every environment, every sentence, every example must pull its weight. If something is "nice to have" but not essential — cut it.
- **Limit teaching environments to 2–3 per topic.** For example: one `conceptBox` + one `workedExample` + one `tipBox`. That's usually enough. Don't stack five boxes.
- **One worked example is usually enough.** Add a second only if the concept has two clearly different cases (e.g., proper vs. improper fractions). Never more than two.
- **Vary the flow between topics.** If the last topic opened with a conceptBox, try a real-world scenario or a bold definition.
- **Don't force environments.** Only include a `riddleBox` if you have a great riddle. An empty filler environment is worse than nothing.
- **Prefer compact environments.** `mascotSays`, `tipBox`, and `keyIdea` take less space than `exploreBox` or `activityBox`. Use the lighter option when both work.

**Things that tend to work well (use freely when they fit):**
- `\mascotSays{}` — the owl giving a memorable shortcut or insight. Students love this.
- `\tipBox{}` — practical tricks ("To check your answer, multiply back!")
- Visual math commands — `\fractionBar`, `\numberLine`, `\barGraph`, etc. A good visual is worth a page of explanation.
- `\begin{workedExample}` and `\begin{sideBySideExample}` — showing HOW to solve is the core of teaching.
- `\begin{errorBox}` — "find the mistake" is surprisingly effective for learning. Great for topics where common errors exist (negative numbers, order of operations, fraction division).
- `\begin{realWorld}` — connecting math to life makes it stick. Especially powerful for ratios, percents, and statistics topics.
- `\sayLeft` / `\sayRight` — dialogue-style explanations can break up dense content.

**Things to use sparingly (they take lots of space):**
- `\begin{codeBreaker}` — engaging but space-heavy. Use rarely, maybe 2–3 times in the whole book.
- `\begin{mathTrail}` — connected problem sequences. Reserve for review/capstone topics only.
- `\begin{activityBox}` — hands-on activities. This is a book, not a classroom. Use very rarely.
- `\begin{storyProblem}` — 1–2 sentences max for setup. Keep it short.
- `\begin{riddleBox}` — only if the riddle is genuinely good and short.
- `\encouragement{}` — a short motivational closer. Use on maybe half the topics, not all.

**Opening ideas (pick what fits, vary between topics):**
- A `conceptBox` that gets straight to the point
- A `\begin{realWorld}` scenario that motivates WHY this topic matters
- A conversation (`\sayLeft` / `\sayRight`) that introduces the key idea
- A `\definitionSpotlight` for a bold, clean definition
- An `\begin{exploreBox}` for discovery-based learning
- A `\mascotSays{}` that poses an intriguing question
- A `\begin{riddleBox}` that hooks the reader

## Topic Structure (Guidelines, Not Rules)

A typical topic might flow like this — but feel free to deviate:

```latex
% ============================================================================
% Section X.Y — Topic Title
% CCSS 6.XX.X.X
% ============================================================================
\section{Topic Title}
\topicTitle{Topic Title}

\begin{learningGoals}
\begin{itemize}
    \item Goal 1
    \item Goal 2
    \item Goal 3 (2–4 goals is typical)
\end{itemize}
\end{learningGoals}

% --- Teaching (keep to 2–3 environments total) ---
% e.g., one conceptBox + one workedExample + one mascotSays

% --- Practice ---
\newpage
\begin{practiceBox}{Title}
\resetProblems
% 4–6 problems with answers
\end{practiceBox}
```

**Target: entire file = 80–120 lines.**

**Firm structural rules:**
1. Start with `\section{Title}` and `\topicTitle{Title}`.
2. Include `\begin{learningGoals}` near the top (2–4 goals, not 4+).
3. End with a practice section (usually `practiceBox`).
4. Every problem MUST have an answer (see Answer Rules below).
5. Put `\newpage` before the practice section.
6. **keep it concise.** As a guide, aim for the file to be 80–120 lines of LaTeX. 

Everything in between is up to you — but keep it lean.

## Practice Sections

**Problem count:** Aim for **4–6 problems** per topic. Quality over quantity. A few well-chosen problems teach more than a long list.
- A computation topic might have 6 short drill problems.
- A conceptual topic might have 4 thoughtful ones.
- **Never exceed 8 problems.** Space is limited.

**Difficulty progression:** Start easy, end harder:
- **Basic** (2–3 problems): straightforward application
- **Applied** (1–2 problems): word problems or multi-step
- **Challenge** (0–1 problem): harder reasoning or error analysis

**Problem types to mix and match:**
- `\prob` — standard numbered problem
- `\trueOrFalse` — quick true/false statement
- `\multiChoice` — multiple choice
- `\circleAnswer` — circle the correct option
- `\wordProblem` — word problem with answer line
- `\wrongAnswer` — fix the mistake (inside `errorBox`)
- `\sortCategory` / `\sortItem` — sorting/classifying (inside `sortBox`)
- `\codeClue` — code breaker clues (inside `codeBreaker`)
- `\trailStop` — connected problems (inside `mathTrail`)
- Fill-in-the-blank with `\answerBlank`
- Input/output tables with `fillTable`
- Use `\begin{multicols}{2}` or `{3}` for compact layouts when problems are short.

**Practice section structure:**
- Start with `\resetProblems` inside the `practiceBox`.
- Use `\practiceHeader[color]{Title}` to organize subsections when you have different types (e.g., "Computation", "Word Problems", "Challenge").
- You can include standalone environments OUTSIDE the `practiceBox` too (like a `challengeBox` or `codeBreaker` after the main practice).

## Answer Rules

**Every single problem must have an answer.** Place the answer command immediately after the problem.

| Answer type | Command | When to use |
|---|---|---|
| Simple answer | `\answer{42}` | Most problems |
| With explanation | `\answerExplain{42}{Divide 84 by 2}` | When a worked solution adds value |
| True/False | `\answerTF{True}` | `\trueOrFalse` problems |
| Multiple choice | `\answerMC{C}` | `\multiChoice` problems |

**Use `\answerExplain` for word problems and multi-step problems.** For simple drill problems, `\answer{}` is fine. Don't over-explain — keep answer explanations to one sentence.

## Visual Math Commands

Include at least one visual per topic. Choose based on the concept:

**Ratios & Rates:** `\barGraph`, `\fillTable`, `\numberLine`
**Fractions:** `\fractionBar`, `\fractionCircle`, `\numberLineFraction`
**Integers & Number Line:** `\numberLine`, `\funCompare`
**Operations:** `\columnAdd`, `\columnSub` (and variants), `\placeValueTable`
**Geometry:** `\areaGrid`, `\perimeterRect`
**Data & Graphs:** `\barGraph`, `\begin{picGraph}` with `\picRow`
**Multiplication/Division:** `\dotGroups`, `\arrayGrid`, `\equalSharing`, `\factFamily`
**Number Sense:** `\baseTenBlocks`, `\numberBond`, `\tallyMarks`
**Quick Facts:** `\multFact`, `\skipCountArc`

These are recommended but not every one needs to appear. Use the visuals that genuinely help explain the concept.

## LaTeX Conventions

- Use `$...$` for ALL math, even simple numbers in equations: `$12 \div 3 = 4$`.
- Use `\times` for multiplication, `\div` for division. Never use `×` or `÷` directly.
- Use `\textbf{...}` to bold key terms on first use.
- Use `\begin{itemize}[leftmargin=*]` for tighter bullet lists.
- Use `\hspace` and `\vspace` sparingly — the environments handle spacing.
- Use `\setcounter{funProblem}{N}` if you need to continue numbering across sections.

## Complete Environment & Command Toolkit

This is your full toolkit. You don't need to memorize it — scan for what fits each topic.

### Teaching & Concepts
| Environment / Command | Brief Description |
|---|---|
| `\begin{conceptBox}[color]{Title}` | Main teaching box (default: green) |
| `\begin{stepsBox}[color]{Title}` | Numbered steps with `\funStep` |
| `\begin{rememberBox}` | Key points to remember |
| `\begin{mathRuleBox}{Title}` | Math rule or formula |
| `\begin{vocabBox}[Title]` | Vocabulary with `\vocabWord{Term}{Def}` |
| `\begin{learningGoals}` | Lesson objectives |
| `\begin{compareBox}[color]{Left}{Right}` | Side-by-side comparison |
| `\begin{exploreBox}[Title]` | Guided discovery activity |
| `\begin{quickReview}[color]{Topic}` | Compact concept refresher |
| `\begin{patternBox}[Title]` | Pattern recognition |
| `\topicTitle{Text}` | Topic banner |
| `\definitionSpotlight[color]{Text}` | Prominent definition |
| `\keyIdea[color]{text}` | Inline highlight |
| `\boxSubtitle[color]{Text}` | Subtitle inside boxes |

### Examples & Solutions
| Environment / Command | Brief Description |
|---|---|
| `\begin{workedExample}[color]{Title}` | Worked example |
| `\begin{sideBySideExample}[color]{Title}` | Two-column: work left, explanation right |
| `\begin{solutionSteps}` | Steps with `\solStep` |
| `\begin{showMeBox}[Title]` | Detailed walkthrough |
| `\begin{numberedExample}` | Auto-numbered example |
| `\begin{errorBox}[Title]` | Find the mistake |
| `\answerHighlight[color]{equation}` | Prominent final answer |
| `\miniAnswer[color]{value}` | Small inline answer |
| `\tryIt{content}` | "Your Turn!" prompt |
| `\wrongAnswer{work}` | Crossed-out wrong work |
| `\answerBlank[width]` | Blank for answers (default: 3cm) |
| `\answerLine[width]` | Full-width ruled answer line |
| `\solutionLabel[text]` | Styled "Solution:" label |

### Practice & Assessment
| Environment / Command | Brief Description |
|---|---|
| `\begin{practiceBox}[color]{Title}` | Practice section |
| `\begin{showWorkBox}[color]{Title}` | "Show Your Work" section |
| `\begin{findMissingBox}[color]{Title}` | Fill-in-the-blank problems |
| `\begin{challengeBox}[Title]` | Harder challenge problems |
| `\begin{quickCheck}[Title]` | Fast assessment |
| `\begin{matchBox}[color]{Title}` | Matching exercise |
| `\begin{sortBox}[color]{Title}` | Sorting/classifying |
| `\begin{fillTable}[color]{Title}` | Input/output table |
| `\begin{codeBreaker}[Title]` | Solve-to-decode puzzle |
| `\begin{mathTrail}[Title]` | Connected problem journey |
| `\begin{picGraph}[color]{Title}` | Pictograph |
| `\prob` | Auto-numbered problem |
| `\probInline` | Inline numbered problem |
| `\resetProblems` | Reset counter |
| `\practiceHeader[color]{Text}` | Section header inside practice |
| `\wordProblem{text}{unit}` | Word problem with answer line |
| `\trueOrFalse{statement}` | True/False |
| `\multiChoice{Q}{A}{B}{C}{D}` | Multiple choice (inline row) |
| `\multiChoiceGrid{Q}{A}{B}{C}{D}` | Multiple choice (2×2 grid) |
| `\circleAnswer{Q}{a}{b}{c}{d}` | Circle the answer |
| `\codeClue{Letter}{Problem}` | Code breaker clue |
| `\secretMessage{format}` | Decoder line |
| `\trailStop` | Math trail stop |
| `\selfCheck` | Self-assessment confidence scale |
| `\answerSpace[height]` | Vertical space for work |
| `\sortItem` | Sortable item tag |

### Engagement & Extras
| Environment / Command | Brief Description |
|---|---|
| `\mascotSays{text}` | Owl mascot tip |
| `\tipBox{text}` | Pencil character trick |
| `\begin{funFact}` | Interesting math tidbit |
| `\didYouKnow{text}` | Quick fact |
| `\begin{realWorld}[Title]` | Real-world connection |
| `\begin{storyProblem}[color]{Title}` | Story/word problem scene |
| `\begin{riddleBox}[Title]` | Math riddle |
| `\begin{activityBox}[Title]` | Activity |
| `\begin{warningBox}[Title]` | Common mistakes |
| `\begin{thinkAboutIt}[Title]` | Thought-provoking question |
| `\begin{proofBox}[Title]` | Justify reasoning |
| `\begin{strategyBox}[Title]` | Problem-solving strategy |
| `\formulaCard{Title}{Formula}` | Formula reference card |
| `\begin{summaryBox}[Title]` | End-of-topic summary |
| `\sayLeft{name}{text}` | Left speech bubble |
| `\sayRight{name}{text}` | Right speech bubble |
| `\encouragement{text}` | Motivational closer |

### Math Visuals
| Command | Brief Description |
|---|---|
| `\numberLine[step]{start}{end}` | Number line with ticks |
| `\numberLineFraction[color]{parts}` | 0-to-1 fraction line |
| `\fractionBar[color]{shaded}{total}` | Fraction bar |
| `\fractionCircle[color]{shaded}{total}` | Fraction circle |
| `\barGraph[color]{Title}{Label/Val,...}{max}` | Bar chart |
| `\dotGroups[color]{groups}{dots}` | Grouped dots |
| `\arrayGrid[color]{rows}{cols}` | Multiplication array |
| `\equalSharing[color]{total}{groups}` | Division sharing visual |
| `\columnAdd{a}{b}` | Vertical addition |
| `\columnAddFull{a}{b}{carries}{sum}` | Addition with carries and answer |
| `\columnAddWork{a}{b}` | Addition workspace (blank) |
| `\columnSub{a}{b}` | Vertical subtraction |
| `\columnSubFull{a}{b}{answer}` | Subtraction with answer |
| `\columnSubWork{a}{b}` | Subtraction workspace (blank) |
| `\placeValueTable{H}{T}{O}` | Place value grid |
| `\baseTenBlocks{flats}{rods}{units}` | Base-ten blocks |
| `\numberBond[color]{whole}{part1}{part2}` | Part-whole diagram |
| `\factFamily{a}{b}{product}` | Fact family triangle |
| `\funCompare{left}{op}{right}` | Comparison visual |
| `\areaGrid[color]{rows}{cols}` | Area tiling |
| `\perimeterRect[color]{w}{h}{unit}` | Labeled rectangle |
| `\skipCountArc[color]{start}{end}{step}` | Skip counting arcs |
| `\clockFace{hour}{minute}` | Analog clock |
| `\ruler{length}{unit}` | Ruler |
| `\coin[color]{label}` | Coin |
| `\tallyMarks{count}` | Tally marks |
| `\multFact{a}{b}{product}` | Multiplication fact |


### Answers
| Command | Brief Description |
|---|---|
| `\answer{value}` | Simple answer |
| `\answerExplain{value}{explanation}` | Answer with solution steps |
| `\answerTF{True/False}` | True/False answer |
| `\answerMC{letter}` | Multiple choice answer |
| `\printAnswerKey` | Render answer key (in main file) |

## Creating New LaTeX Environments

If a topic genuinely needs a visual or interactive element that no existing environment provides, you may create new environments. Add them to the appropriate `.sty` file in `VM_packages/` (or create a new `.sty` file if needed).

When creating new environments:
- Study existing `.sty` files to match the coding style, color conventions, and `tcolorbox` patterns.
- Use the project's color palette (`funBlue`, `funGreen`, `funOrange`, etc.).
- New environments should be self-contained and not depend on or modify existing environment internals.
- Add a clear header comment with name, usage signature, and description.

**CRITICAL: Never modify existing environments or commands.** They are shared across many topics and book types. Even a small change can break other sections. If an existing environment doesn't do exactly what you want, create a new one instead.

For the full environment reference with usage examples and code samples, see `.agents/skills/latex_environments/SKILL.md`.


## Checklist (Sanity Check)

Before finishing a topic, verify:

- [ ] **File is 80–120 lines of LaTeX** (the #1 most important check)
- [ ] File is named `ch<CC>-<SS>-slug.tex` and placed in `topics/`
- [ ] Starts with `\section{Title}` + `\topicTitle{Title}`
- [ ] Has `\begin{learningGoals}` with 2–4 bullet points
- [ ] Teaching uses at most 2–4 environments (e.g., one conceptBox + one workedExample + one tipBox)
- [ ] At most 1–2 worked examples
- [ ] Includes at least one visual math command
- [ ] Practice section has 4–6 problems with `\resetProblems` and `\newpage` before it
- [ ] Every problem has a corresponding `\answer{}`, `\answerExplain{}{}`, `\answerTF{}`, or `\answerMC{}`
- [ ] Math is wrapped in `$...$`
- [ ] Sentences average 8–12 words — dead simple language
- [ ] No filler sentences — every sentence teaches something
