---
name: writing_study_guide_topics
description: Guidelines for writing engaging Grade 7 math study guide topics
---

# Writing Grade 7 Math Study Guide Topics

## CRITICAL — Page Budget

The finished book MUST be **150–170 pages total** (including front matter, all topics, and the answer key). There are **56 topics**, so each topic averages roughly **2–3 printed pages**. That means:

- **Target: 60–90 lines of LaTeX per topic file.** This is the single most important constraint. If your file is over 90 lines, cut it down. Every sentence must earn its place.
- A simple topic (e.g., "What Is Probability?") might be 55–70 lines (~1.5 pages).
- A dense topic (e.g., "Solving Equations with the Distributive Property") can go up to 100 lines (~2 pages) but no more.
- **Never exceed 2 printed pages for any single topic.**

When in doubt, cut. A short, clear explanation that a student actually reads beats a long one they skip.

## The Book

This is a single-edition Grade 7 math book. Each topic should teach ONE concept clearly and give students practice — nothing more. Keep it tight.

Topic files live in `topics/`. File naming: `ch01-01-slug-here.tex`

## Audience: 12–13 Year Olds (Grade 7)

Write for a smart, curious 12-year-old. These students have Grade 7 foundations — make every explanation **dead simple** but don't talk down to them.

- **Use very short sentences.** Aim for **8–12 words per sentence**. One idea per sentence. If a sentence has a comma, consider splitting it.
- **Use the simplest words possible.** Say "find" not "determine." Say "shows" not "demonstrates." Say "same" not "equivalent" (until you define it). Write how you would talk to a kid.
- **Simple first, formal second.** Say "undo the operations backward" before "apply inverse operations." Always teach the real math term too, but lead with the plain-English version.
- **Conversational, not textbook-stiff.** Use "you" and "let's" freely. Keep it warm but not babyish.
- **Connect to their world.** Sports stats, video games, online shopping, cooking, phone plans, social media — use things they know.
- **Be encouraging without overdoing it.** One "Nice work!" is plenty. Skip filler praise.
- **Cut any sentence that doesn't teach something.** If you remove a sentence and the topic still makes sense, remove it.

## Writing Style — Concise and Crystal Clear

Every word must earn its place. Here are concrete examples:

| Too wordy (DON'T) | Concise (DO) |
|---|---|
| "A proportional relationship is a mathematical relationship where two quantities maintain a constant ratio to each other at all times." | "In a proportional relationship, two quantities always have the same ratio." |
| "In order to solve a two-step equation, you will need to undo the operations in reverse order." | "To solve a two-step equation, undo operations backward." |
| "Let's take a look at an example to see how this works in practice." | (Just show the example — skip the transition.) |
| "Now that we've learned about integers, let's practice what we've learned!" | (Just start the practice section — no need to announce it.) |

**Rules:**
- **Delete transition sentences.** "Let's see how this works" → just show it.
- **Delete summary filler.** "Now you know how to..." → cut it.
- **One sentence per idea.** If a sentence has "and" connecting two ideas, split it.
- **No redundancy.** If the `conceptBox` explains it, don't re-explain it in prose before the example.
- **Definitions: one sentence.** "The **constant of proportionality** is the value of $k$ in $y = kx$." Done.

## Content Standards

Follow **Common Core State Standards (CCSS)** for Grade 7. The five domains are:

1. **Ratios and Proportional Relationships (7.RP)** — unit rates with fractions, proportional relationships, constant of proportionality, equations/graphs, percent problems, percent increase/decrease, markups/discounts, simple interest, percent error
2. **The Number System (7.NS)** — integers and opposites, adding/subtracting integers, rational number operations (all four), converting rationals to decimals, multi-step real-world problems with rational numbers
3. **Expressions and Equations (7.EE)** — writing/evaluating expressions, combining like terms, distributive property, factoring, adding/subtracting linear expressions, two-step equations, equations with distributive property, inequalities
4. **Geometry (7.G)** — scale drawings, geometric figures with given conditions, constructing triangles, cross-sections of 3D figures, angle relationships, circles (circumference, area), composite shapes, surface area, volume of prisms
5. **Statistics and Probability (7.SP)** — populations/samples, random sampling, comparing populations visually and with measures, probability concepts, theoretical/experimental probability, probability models, sample spaces, compound events, simulations

Numbers at this level: all rational numbers (positive and negative integers, fractions, decimals), proportional reasoning, two-step and multi-step problems, probability (0 to 1). This builds on Grade 7 — students work with signed rationals, proportional relationships, and basic probability.

## Creative Freedom

You have access to **100+ environments and commands** (see the toolkit reference below). There is no rigid template. Your job is to pick the combination that best serves each topic.

**General principles:**
- **Teach the concept, then let them practice.** That's the only hard structure rule.
- **Be ruthlessly concise.** Every environment, every sentence, every example must pull its weight. If something is "nice to have" but not essential — cut it.
- **Limit teaching environments to 2–3 per topic.** For example: one `conceptBox` + one `workedExample` + one `mascotSays`. That's usually enough. Don't stack four or five boxes.
- **One worked example is usually enough.** Add a second only if the concept has two clearly different cases (e.g., percent increase vs. percent decrease). Never more than two.
- **Vary the flow between topics.** If the last topic opened with a conceptBox, try a real-world scenario or a bold definition.
- **Don't force environments.** Only include a `riddleBox` if you have a great riddle. An empty filler environment is worse than nothing.
- **Prefer compact environments.** `mascotSays`, `tipBox`, and `keyIdea` take less space than `exploreBox` or `activityBox`. Use the lighter option when both work.

**Things that tend to work well (use freely when they fit):**
- `\mascotSays{}` — the owl giving a memorable shortcut or insight. Students love this.
- `\tipBox{}` — practical tricks ("To check a proportion, cross-multiply!")
- Visual math commands — `\numberLine`, `\fractionBar`, `\fractionCircle`, `\barGraph`, etc. A good visual is worth a page of explanation.
- `\begin{workedExample}` and `\begin{sideBySideExample}` — showing HOW to solve is the core of teaching.
- `\begin{errorBox}` — "find the mistake" is surprisingly effective for learning. Great for topics where common errors exist (integer signs, proportion setup, equation solving, percent increase/decrease).
- `\begin{realWorld}` — connecting math to life makes it stick. Especially powerful for percents, proportions, statistics, and probability topics.
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
% CCSS 7.XX.X.X
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

% --- Practice (NO \newpage — let content flow naturally) ---
\begin{practiceBox}{Title}
\resetProblems
% 4–5 problems with answers
\end{practiceBox}
```

**Target: entire file = 60–90 lines.**

**Firm structural rules:**
1. Start with `\section{Title}` (**DO NOT** add `\topicTitle{}` — the class file’s `\section` already renders a blue banner; adding `\topicTitle` creates a duplicate).
2. Include `\begin{learningGoals}` near the top (2 goals is ideal).
3. End with a practice section (usually `practiceBox`).
4. Every problem MUST have an answer (see Answer Rules below).
5. **DO NOT** put `\newpage` before the practice section. The `\section` command already forces a page break for each topic. Adding `\newpage` before practice wastes half a page of whitespace. Let content flow naturally — boxes are breakable and will split across pages.
6. **keep it concise.** Aim for 60–90 lines of LaTeX.

Everything in between is up to you — but keep it lean.

## Practice Sections

**Problem count:** Aim for **4–5 problems** per topic. Quality over quantity. A few well-chosen problems teach more than a long list.
- A computation topic might have 5 short drill problems.
- A conceptual topic might have 4 thoughtful ones.
- **Never exceed 6 problems.** Space is limited.

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
| Simple answer | `\answer{42}` | Only for `\multiChoice` key or trivially obvious one-step answers |
| With explanation | `\answerExplain{42}{...}` | **Most problems — the default choice** |
| True/False | `\answerTF{True}` | `\trueOrFalse` problems |
| Multiple choice | `\answerMC{C}` | `\multiChoice` problems |

### Writing Good Answer Explanations (CRITICAL)

**Use `\answerExplain` for nearly every problem.** The student just learned this topic — if they couldn't solve a problem, a bare calculation won't help them either. The explanation is their mini-tutor.

**Length:** Each explanation should be **1–2 full printed lines** (~80–200 characters). Walk the student through the reasoning step by step, not just the arithmetic.

**What a good explanation includes:**
1. **What to do first** — name the operation or strategy ("Find the unit rate by dividing…", "Set up a proportion…")
2. **The key calculation** — show the math with intermediate steps
3. **Why it makes sense** — a brief sanity check or connection back to the concept ("…which is the cost for one pound", "…this matches because a larger percent means a bigger discount")

| BAD (too short) | GOOD (teaches) |
|---|---|
| `$\frac{2}{3} \div \frac{1}{3} = 2$` | `Divide the wall covered by the time: $\frac{2}{3} \div \frac{1}{3}$. Flip and multiply: $\frac{2}{3} \times \frac{3}{1} = 2$ walls per hour.` |
| `$36 \div 90 = 0.4 = 40\%$` | `Divide the part by the whole: $36 \div 90 = 0.4$. Convert to a percent by multiplying by $100$: $0.4 \times 100 = 40\%$.` |
| `$180 \times 0.75 = 135$` | `A $25\%$ discount means you pay $75\%$. Multiply: $180 \times 0.75 = \$135$.` |
| `$(15 - 12) \div 12 = 0.25$` | `Subtract to find the change: $15 - 12 = 3$ cm. Divide by the original: $3 \div 12 = 0.25$. Multiply by $100$ to get $25\%$.` |

**Rules:**
- **Always prefer `\answerExplain` over `\answer`.** Use bare `\answer{}` only when the answer is self-evident (e.g., "Write the equation" → `\answer{$c = 8h$}`).
- **Name the strategy.** Don't just show numbers — say "Divide…", "Set up…", "Multiply by the multiplier…".
- **Show intermediate steps.** If there are two operations, show both, not just the final result.
- **Keep the tone simple.** Same 8–12 word sentences as the teaching sections.
- **For `\answerTF{}` problems, add a brief reason** in the text before or after if the answer isn't obvious.

## Visual Math Commands

Include at least one visual per topic. Choose based on the concept:

**Ratios & Proportional Relationships:** `\barGraph`, `\fillTable`, `\numberLine` — tape diagrams, ratio tables, coordinate graphs for proportional relationships
**Percents:** `\barGraph`, `\fractionBar`, `\areaGrid` — percent bars, 10×10 grids, comparison visuals
**Integers & Rational Numbers:** `\numberLine`, `\funCompare` — number lines with negative numbers, comparison visuals
**Expressions & Equations:** `\fillTable` — balance diagrams (custom TikZ), algebra tile models, input/output tables
**Geometry & Angles:** `\areaGrid`, `\perimeterRect`, `\ruler` — scale drawings, angle diagrams, cross-sections (custom TikZ)
**Circles, Area, SA, Volume:** `\fractionCircle`, `\areaGrid`, `\perimeterRect` — circle diagrams, composite shapes, nets of 3D figures (custom TikZ)
**Statistics:** `\barGraph`, `\begin{picGraph}` with `\picRow` — dot plots, box plots, side-by-side comparisons
**Probability:** `\fillTable`, custom TikZ — tree diagrams, sample space tables, spinners

These are recommended but not every one needs to appear. Use the visuals that genuinely help explain the concept.

## LaTeX Conventions

- Use `$...$` for ALL math, even simple numbers in equations: `$2x + 3 = 11$`.
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

- [ ] **File is 60–90 lines of LaTeX** (the #1 most important check)
- [ ] File is named `ch<CC>-<SS>-slug.tex` and placed in `topics/`
- [ ] Starts with `\section{Title}` (NO `\topicTitle` — the section banner handles it)
- [ ] Has `\begin{learningGoals}` with 2–4 bullet points
- [ ] Teaching uses at most 2–3 environments (e.g., one conceptBox + one workedExample + one mascotSays)
- [ ] At most 1–2 worked examples
- [ ] Includes at least one visual math command
- [ ] Practice section has 4–5 problems with `\resetProblems` and **NO** `\newpage` before it
- [ ] Every problem has a corresponding `\answer{}`, `\answerExplain{}{}`, `\answerTF{}`, or `\answerMC{}`
- [ ] Math is wrapped in `$...$`
- [ ] Sentences average 8–12 words — dead simple language
- [ ] No filler sentences — every sentence teaches something

## Conciseness Lessons (Learned from Chapter 1 Rewrites)

These are concrete, tested techniques that cut topic files from 100–150 lines down to 60–90 without losing teaching quality.

### What to cut

| Cut this | Saves | Why it's safe |
|---|---|---|
| 4-line header comment blocks | 3 lines | One-liner (`% CCSS 7.RP.A.1 — Topic Title`) carries the same info |
| `\renewcommand{\arraystretch}{1.3}` in tables | 1 line/table | Default spacing is fine for study guides |
| `\bigskip` between elements inside environments | 1–3 lines | Environments already have internal spacing |
| `\solutionLabel` when solution is inline | 1 line | Obvious from context; only use when steps follow |
| `\begin{solutionSteps}` wrapper with `\solStep` | 3–5 lines | Inline math (`$k = 10 \div 4 = 2.5$`) is shorter and just as clear |
| `\practiceHeader` subsections in practice | 2–3 lines | Unnecessary when there are only 4–5 problems |
| Redundant teaching environments (e.g., tipBox repeating what conceptBox said) | 3–5 lines | One clear explanation > two overlapping ones |
| Transition sentences ("Let's see...", "Now let's...") | 1–2 lines | Just show the next thing |

### Structure rules for compact files

1. **One header comment line.** `% CCSS 7.RP.A.1 — Topic Title`
2. **Two learning goals, not three or four.** Two goals ≈ 5 lines. Four goals ≈ 8 lines. The extra goals rarely add value.
3. **One conceptBox + one workedExample = enough teaching.** Add a `mascotSays` or `tipBox` only if it adds a genuinely new insight, not repetition.
4. **Inline solutions over solutionSteps.** Write `$k = 13.50 \div 3 = 4.50$` on one line instead of 3 `\solStep` lines.
5. **Compact tables.** Put table rows on one line: `$2$ & $\$3.50$ \\ $4$ & $\$7.00$ \\`. Skip `\arraystretch`.
6. **4–5 practice problems, not 6.** Fewer, well-chosen problems beat a longer list. Cut the "medium" problems; keep easy + hard.
7. **Use `\answerExplain{}{}` for nearly every problem.** Write 1–2 full lines that walk the student through the reasoning. Only use bare `\answer{}` when the answer is self-evident.
8. **No blank lines between `\prob` entries** unless switching problem types.

### The "earn its place" test

Before adding any environment, sentence, or problem, ask: *If I remove this, does the student lose something important?* If the answer is no, cut it. A 65-line file that teaches clearly is better than a 90-line file with padding.

### Page-flow rules (critical for page budget)

- **Never use `\topicTitle{}`** in topic files. The `\section{}` command already renders a styled blue banner via the class file. Adding `\topicTitle` creates a duplicate header and wastes ~1cm of vertical space.
- **Never use `\newpage` before practice sections.** Each `\section` already forces a page break. A second `\newpage` before practice leaves half a page blank. Let content flow naturally into the practice box.
- **All major boxes are breakable.** `conceptBox`, `workedExample`, `practiceBox`, `errorBox`, `warningBox`, `realWorld` — they all break across pages automatically. Don’t try to prevent breaks; embrace them.
- **Prefer inline content over boxed content when possible.** A `\mascotSays{}` (minipage-based, ~3 lines) is lighter than an `errorBox` (tcolorbox, ~5+ lines) for the same message.
- **Use `\setstretch{1.25}`** in test/main files, not `1.4`. The tighter line spacing saves ~10% vertical space across the book.
- **Blank-page bug — page breaks must happen OUTSIDE `\titleformat`.** Issuing `\clearpage` or `\newpage` inside `\sectionBanner` (which runs inside titlesec's `\titleformat` callback) causes a phantom blank page. The page break is shipped after the current page, but titlesec's internal state then ships an extra empty page before placing the banner. **Fix:** The page-break logic (`\ifdim\pagetotal<50pt\else\newpage\fi`) is placed in `\AddToHook{cmd/section/before}` in `studyGuide.cls`, which fires BEFORE titlesec processes the section. The `\sectionBanner` command itself must NOT contain any page-break commands.