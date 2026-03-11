---
name: writing_worksheet_topics
description: How to write standalone, printable worksheet activities for the Grade 6–8 Math Worksheet book
---

# Writing Worksheet Topics — Math Worksheet Activity Book

## Overview

The **Worksheet** book is a collection of **standalone, printable math activities** aligned to the grade-level curriculum. Each topic contains **5 worksheets**, each a different activity type — speed drills, matching, data analysis, error hunts, real-world scenarios, graph challenges, table tasks, code crackers, and more. Every worksheet is a **self-contained, 1-page activity** that a teacher can pull out and use independently.

**This book is fundamentally different from drill-style practice.** It does not teach concepts or present rows of identical problems. Instead, it uses **varied, visually distinct activity formats** to make students *practice* math skills in engaging, creative ways. Think of it as the "fun printable activities" companion to the study guide.

**Key characteristics:**

| Aspect | Worksheet Book |
|--------|---------------|
| Purpose | Practice math skills through varied, engaging activities |
| Teaching content | None — students should already know the concept |
| Worksheets per topic | 5 varied worksheets (each is a different activity type) |
| Visual elements | Heavy — every worksheet has a different look and feel |
| Answer format | `\worksheetAnswer{}` — one comprehensive answer per worksheet (Worksheet Solutions chapter) |
| Page length | 5–8 pages per topic (each worksheet is ~1 page) |
| Color palette | Lime-green primary, with each activity type having its own accent color |
| B&W printing | All content-area backgrounds are white — prints clean in B&W |
| Personality | Engaging, analytically stimulating, classroom-ready |

### How It Differs from Other Book Types

| Aspect | Study Guide | Workbook | Puzzles | **Worksheet** |
|--------|-------------|----------|---------|--------------|
| Purpose | Teach + practice | Drill practice | Brain teasers | **Activity-based practice** |
| Teaching | Extensive | Quick review | None | **None** |
| Problem format | `\prob` drill | `\prob` drill | Puzzle environments | **Activity environments (no `\prob`)** |
| Visual variety | Moderate | Low | Very high | **Very high (every activity different)** |
| Answer system | `\answer{}` | `\answerExplain{}{}` | `\puzzleAnswer{}` | **`\worksheetAnswer{}`** |
| Student experience | "Learn this" | "Practice this" | "Can you crack this?" | **"Try this activity!"** |
| Tone | Encouraging teacher | Steady coach | Playful challenger | **Activity leader** |
| Standalone pages | No | No | No | **Yes — each worksheet is independent** |
| Ideal for | Study time | Homework | Math centers | **Classwork, centers, subs, homework, homeschool** |

### Target Use Cases

Worksheets are designed to be ideal for:
- **Whole-class instruction** — teacher picks one activity for the class
- **Independent learning** — student works alone on a standalone page
- **Math centers** — different worksheets at different stations
- **Homeschooling** — parent picks a topic-appropriate activity
- **Sub plans** — substitute teacher grabs a self-contained worksheet
- **Math intervention** — targeted practice on a specific skill
- **Early finishers** — fast students get a different activity type
- **Test prep** — varied formats keep review from feeling repetitive

---

## File Structure

```
VM_packages/VMfunWorksheet.sty           # Worksheet environments and color palette
worksheet_main.tex                        # Master document (template)

topics_worksheet/                         # Core worksheet topic files (CCSS baseline)
    ch01-01-what-is-a-ratio.tex
    ch01-02-using-ratio-language.tex
    ...

topics_worksheet_additional/              # State-specific supplementary worksheets
    ch02-05-prime-and-composite-numbers.tex
    ...

topics_worksheet_modified/                # Modified worksheets for specific states
    ...
```

---

## Workflow

### Step 0 — Discover Topics with the Script

Before writing anything, **run the discovery script** to learn what topics the chapter contains, the grade level, and the target audience:

```bash
python3 scripts/get_chapter_topic_facts.py --chapter <N>
```

The script output tells you:
- **Grade Info** — grade level, grade display name, and target student age range (e.g., "11-12 year-old students" for Grade 6, "12-13" for Grade 7, "13-14" for Grade 8). **Use this to calibrate vocabulary, complexity, contexts, and number difficulty.**
- **Chapter title** — the mathematical domain the chapter covers.
- **Core topics** — the list of topics in `topics/` you must write worksheet versions for (→ `topics_worksheet/`).
- **Additional topics** — state-specific topics in `topics_additional/` (→ `topics_worksheet_additional/`), with which states use them.
- **Modified topics** — state-specific variants in `topics_modified/` (→ `topics_worksheet_modified/`), with which states use them.
- **Summaries** — a brief content description for each topic, giving you a head start before reading the full source file.

To list all available chapters:
```bash
python3 scripts/get_chapter_topic_facts.py --list-chapters
```

Use the script output to **plan your work**: note how many files you need to create (core + additional + modified) and read the summaries to understand the scope. Write **all** worksheet topics for the entire chapter before compiling.

### Step 1 — Read the Study Guide Source Topics

For every topic listed by the script, **read the corresponding Study Guide source file** before writing:

| Script "File Path" prefix | Read from | Write to |
|---------------------------|-----------|----------|
| `topics/` | `topics/ch<CC>-<SS>-<slug>.tex` | `topics_worksheet/ch<CC>-<SS>-<slug>.tex` |
| `topics_additional/` | `topics_additional/ch<CC>-<SS>-<slug>.tex` | `topics_worksheet_additional/ch<CC>-<SS>-<slug>.tex` |
| `topics_modified/` | `topics_modified/ch<CC>-<SS>-<slug>.tex` | `topics_worksheet_modified/ch<CC>-<SS>-<slug>.tex` |

When reading each source file, extract:
- What concepts and vocabulary the topic covers
- What difficulty level and number ranges are appropriate
- What types of problems and visuals are used

**The worksheet file must use the same filename as the Study Guide file.**

### Step 2 — Plan and Write 5 Varied Activities per Topic

Plan **5 worksheets per topic** with **maximum variety**. Never use the same activity type twice in a topic. Choose from the [Activity Type Catalog](#activity-type-catalog) below, **or invent new activity types** if the topic calls for it. Each activity should feel visually and structurally different from the others.

Follow the [Topic Structure](#topic-structure) and [Critical Rules](#critical-rules-non-negotiable) sections. Use the grade and age info from the script to calibrate difficulty and language.

### Step 3 — Compile and Verify

After writing ALL worksheet topics for the chapter (core + additional + modified):
1. Create a test file `tests/test_worksheet_ch<N>.tex` that includes all the new topic files.
2. Compile with: `latexmk -xelatex -output-directory=build -interaction=nonstopmode -f tests/test_worksheet_ch<N>.tex`
3. Check the log for errors: `grep -i 'error\|undefined' build/test_worksheet_ch<N>.log | grep -v Warning | head -20`
4. Open the PDF for review.

---

## File Naming

Format: `ch<CC>-<SS>-<slug>.tex` — same convention as all other book types.

| Study Guide source folder | Worksheet output folder |
|---------------------------|------------------------|
| `topics/` | `topics_worksheet/` |
| `topics_additional/` | `topics_worksheet_additional/` |
| `topics_modified/` | `topics_worksheet_modified/` |

---

## Topic Structure

Every worksheet topic file follows this structure:

```latex
% ============================================================================
% WORKSHEET — Section X.Y: Topic Title
% CCSS X.XXX.X.X
% ============================================================================
\section{Topic Title}
\setcounter{wsNumber}{0}

\begin{worksheetSkills}
\begin{itemize}
    \item Skill 1 these worksheets practice
    \item Skill 2
    \item Skill 3
\end{itemize}
\end{worksheetSkills}

% ── WORKSHEET 1: Activity Type ───────────────────────────────────────────────
\worksheetHeader{Catchy Activity Title}

\begin{activityEnvironment}{Title With Icon}
% ... activity content (questions asked directly, no \prob) ...
\end{activityEnvironment}
\worksheetAnswer{Comprehensive answer including both the final result and the method to get there.}

% ── WORKSHEET 2: Different Activity Type ─────────────────────────────────────
\worksheetHeader{Another Catchy Title}

\begin{differentEnvironment}{Title}
% ... activity content ...
\end{differentEnvironment}
\worksheetAnswer{Comprehensive answer for this worksheet.}

% ── WORKSHEET 3–5: More varied activities ────────────────────────────────────
% ... 3 more worksheets, each with \worksheetAnswer{} after \end{} ...

\worksheetDone
```

### Required Elements

1. **`\section{}`** — section title matching the curriculum map
2. **`\setcounter{wsNumber}{0}`** — reset worksheet counter at the start of each section
3. **`\begin{worksheetSkills}`** — green skills box listing 2–4 skills the worksheets practice
4. **5 worksheets** — each using `\worksheetHeader{title}` + an activity environment
5. **`\worksheetAnswer{}`** — one comprehensive answer per worksheet, placed immediately after `\end{environment}` (outside the environment)
6. **`\worksheetDone`** — celebration banner at the end

### Writing for the Target Audience 
The python script output gives you the grade level and target student age range for the chapter. Use this information to calibrate:
**Always check the script output** for the actual grade and adjust accordingly. Never hard-code assumptions about the grade level.

**Activities that are OFF-LIMITS (too young for grades 6–8):**
- Coloring pages / "color by answer" as a primary activity (the `colorByAnswer` environment exists but should be used sparingly and only with complex math — never for simple arithmetic)
- Drawing base-ten blocks
- Tracing numbers or shapes
- Baby-style cut-and-paste with clip art

**Activities that WORK WELL for grades 6–8:**
- Error analysis (find and fix mistakes) — analytically challenging
- Code crackers (solve → decode a word) — game-like engagement
- Data analysis with real-world data sets — intellectually stimulating
- Real-world scenarios with multi-step reasoning — relevant and practical
- Function machines / input-output tables — algebraic thinking
- Graph interpretation and construction — visual-analytical
- Sorting/classifying with mathematical justification — conceptual depth
- Explain-your-reasoning writing prompts — develops communication skills
- Table completion with pattern discovery — builds algebraic reasoning

---

## Critical Rules (Non-Negotiable)

### 1. One `\worksheetAnswer{}` Per Worksheet — Placed Outside the Environment

Each worksheet (activity environment) gets **exactly one** `\worksheetAnswer{}` placed **immediately after** `\end{environment}` (outside it, not inside). The answer is comprehensive — it includes **both the final result(s) and the method/reasoning** to arrive at them. This is the same pattern used by `\puzzleAnswer{}` in the Puzzles book.

```latex
% ✓ CORRECT — \worksheetAnswer after \end{environment}
\begin{speedDrill}{Ratio Speed Round!}
% ... table with 6 blanks ...
\end{speedDrill}
\worksheetAnswer{The six unit rates are: $\$3.50$ per lb ($\$14 \div 4$), $12$ mph ($48 \div 4$), \ldots{} To find a unit rate, divide both quantities so the second term equals $1$.}

% ✗ WRONG — \worksheetAnswer inside the environment
\begin{speedDrill}{Ratio Speed Round!}
% ...
\worksheetAnswer{...}    % ← NEVER DO THIS
\end{speedDrill}

% ✗ WRONG — missing \worksheetAnswer
\begin{matchIt}{Match!}
% ...
\end{matchIt}
% ← Every worksheet MUST have an answer
```

### 2. No `\prob`, `\answer{}`, or `\answerExplain{}{}` in Worksheets

Worksheets do **NOT** use the standard answer system. Questions are asked directly as text — no `\prob` prefix. Do not use `\answer{}`, `\answerExplain{}{}`, or `\resetProblems`. The only answer command is `\worksheetAnswer{}`.

```latex
% ✓ CORRECT — question asked directly, answer via \worksheetAnswer
\begin{errorDetective}{Find the Mistakes!}
Marcus says: ``$\frac{3}{4} \div \frac{1}{2} = \frac{3}{8}$.''
\errorWork{$\frac{3}{4} \times \frac{1}{2} = \frac{3}{8}$}
Correct or wrong? \answerBlank[2cm]
\end{errorDetective}
\worksheetAnswer{Wrong --- to divide fractions, multiply by the reciprocal: $\frac{3}{4} \times \frac{2}{1} = \frac{6}{4} = \frac{3}{2} = 1\frac{1}{2}$. Marcus multiplied instead of flipping the second fraction.}

% ✗ WRONG — using \prob and \answer
\begin{errorDetective}{Find the Mistakes!}
\prob Marcus says $\frac{3}{4} \div \frac{1}{2} = \frac{3}{8}$.   % ← NO
\answerExplain{Wrong}{explanation}                                   % ← NO
\end{errorDetective}
```

### 3. Comprehensive Answers

Each `\worksheetAnswer{}` must include **everything a student (or parent/teacher) needs** to verify correctness:
- The **final answer(s)** for every question in the worksheet
- The **method, reasoning, or calculation** that leads to each answer
- Use numbered items `(1)~`, `(2)~` etc. when covering multiple questions

```latex
\worksheetAnswer{All three are \textbf{wrong}. (1)~To find $\frac{3}{5}$ of $40$,
multiply: $\frac{3}{5} \times 40 = \frac{120}{5} = 24$, not $15$.
(2)~The ratio $3 : 5$ is equivalent to $9 : 15$, not $9 : 12$ --- both terms must
be multiplied by the same factor ($\times 3$). (3)~$|-7| = 7$, not $-7$ --- absolute
value is always non-negative.}
```

### 4. Keep Items Per Worksheet Low

Each worksheet is ONE activity on roughly ONE page. **Do not overload.** Target item counts:

| Activity type | Items per worksheet |
|---|---|
| Speed drill (table) | 8–10 cells |
| Matching | 5–6 pairs |
| Sort & cut | 8–10 cards into 2–3 bins |
| Error detective | 3–4 problems |
| Math scenario | 3–4 questions |
| Input/output | 2 machines with 3–4 blanks each |
| Explain it | 2 writing prompts |
| Data analysis | 1 data set with 3–4 questions |
| Graph it | 1 graph/coordinate plane with 3–4 tasks |
| Table challenge | 1–2 tables with 4–6 blanks |
| Code cracker | 6–8 problems mapping to letters |

### 5. All Backgrounds Must Be White or very light colours

The book must print cleanly in black and white. **All `colback` values in environments are `white`**. Only title bars and borders carry color. Never use `\rowcolor{}` on table rows (it produces dark gray patches in B&W).

### 6. Math in `$...$`

```latex
$3 \times 4 = 12$    % ✓
3 × 4 = 12           % ✗
```

Use `\times` for multiplication, `\div` for division. Bold key terms on first use.

---

## Activity Type Catalog (VMfunWorksheet.sty)

These are the available activity environments. **Every worksheet must use one.** You choose which fits the topic best.

### Speed Drill — `speedDrill`
**Icon:** Stopwatch | **Color:** Orange | **Best for:** Fluency practice, quick computation

Timed fluency grid. Students fill in blanks as fast as possible. Great for fraction operations, decimal computation, integer arithmetic, evaluating expressions, unit rate calculations.

```latex
\begin{speedDrill}{Unit Rate Speed Round}
\timerBadge{4}

Find the \textbf{unit rate} for each situation.

\bigskip
\renewcommand{\arraystretch}{2.0}
\begin{center}
\sffamily\large
\begin{tabular}{|C{5cm}|C{4cm}|}
\hline
\textbf{Situation} & \textbf{Unit Rate} \\
\hline
$\$18$ for $3$ lb & \answerBlank[3cm] \\
\hline
$240$ miles in $4$ hours & \answerBlank[3cm] \\
\hline
$\$45$ for $5$ tickets & \answerBlank[3cm] \\
\hline
$150$ words in $3$ min & \answerBlank[3cm] \\
\hline
$84$ points in $7$ games & \answerBlank[3cm] \\
\hline
$\$32.50$ for $5$ gallons & \answerBlank[3cm] \\
\hline
\end{tabular}
\end{center}
\end{speedDrill}
\worksheetAnswer{(1)~$\$6$ per lb ($18 \div 3$). (2)~$60$ mph ($240 \div 4$). (3)~$\$9$ per ticket ($45 \div 5$). (4)~$50$ words per min ($150 \div 3$). (5)~$12$ points per game ($84 \div 7$). (6)~$\$6.50$ per gallon ($32.50 \div 5$). To find a unit rate, divide both quantities so the second term equals $1$.}
```

### Match It — `matchIt`
**Icon:** Link | **Color:** Blue | **Best for:** Connecting related concepts (expression ↔ value, ratio ↔ equivalent ratio, equation ↔ solution)

Two-column matching. Use `\matchRow{left}{right}` for each pair.

```latex
\begin{matchIt}{Match Equivalent Expressions!}

Each expression on the left is equivalent to one on the right. Draw lines to connect them!

\matchRow{$3(x + 4)$}{$5x - 5$}
\matchRow{$2x + 2x + 6$}{$3x + 12$}
\matchRow{$5(x - 1)$}{$4x + 6$}
\matchRow{$7x - 2x + 3$}{$6x$}
\matchRow{$2 \cdot 3x$}{$5x + 3$}
\end{matchIt}
\worksheetAnswer{$3(x + 4) = 3x + 12$ (distribute the $3$). $2x + 2x + 6 = 4x + 6$ (combine like terms $2x + 2x$). $5(x - 1) = 5x - 5$ (distribute the $5$). $7x - 2x + 3 = 5x + 3$ (combine like terms). $2 \cdot 3x = 6x$ (multiply coefficients). Use the distributive property and combining like terms to simplify each side.}
```

### Error Detective — `errorDetective`
**Icon:** Magnifying glass | **Color:** Red | **Best for:** Critical thinking, analyzing common mistakes

Shows student work with intentional errors. Students find and fix mistakes. Use `\errorWork{shown work}` for each problem. This is one of the strongest activity types for grades 6–8 — students enjoy the analytical challenge of catching errors.

```latex
\begin{errorDetective}{Can You Catch the Mistakes?}

A student named Marcus solved these problems. \textbf{Some solutions are wrong!}
Find each mistake, explain what went wrong, and write the correct answer.

\bigskip

Marcus says: ``$\frac{2}{3} \div \frac{4}{5} = \frac{8}{15}$''
\errorWork{$\frac{2}{3} \times \frac{4}{5} = \frac{8}{15}$}
Correct or wrong? \answerBlank[2cm] \quad Fix it: \answerBlank[5cm]

\bigskip

Marcus says: ``If $x + 7 = 15$, then $x = 22$.''
\errorWork{$x = 15 + 7 = 22$}
Correct or wrong? \answerBlank[2cm] \quad Fix it: \answerBlank[5cm]

\bigskip

Marcus says: ``$|-12| = -12$''
\errorWork{The absolute value keeps the sign, so $|-12| = -12$.}
Correct or wrong? \answerBlank[2cm] \quad Fix it: \answerBlank[5cm]
\end{errorDetective}
\worksheetAnswer{All three are \textbf{wrong}. (1)~To divide fractions, multiply by the \textbf{reciprocal}: $\frac{2}{3} \times \frac{5}{4} = \frac{10}{12} = \frac{5}{6}$. Marcus multiplied straight across instead of flipping the divisor. (2)~To isolate $x$, \textbf{subtract} $7$ from both sides: $x = 15 - 7 = 8$. Marcus added instead of using the inverse operation. (3)~Absolute value is always non-negative: $|-12| = 12$, not $-12$. Absolute value measures distance from zero, which is always positive.}
```

### Sort & Cut — `sortCut`
**Icon:** Scissors | **Color:** Orange | **Best for:** Classification (rational vs. irrational, positive vs. negative, expression types, statistical measures)

Cards with dashed borders for cutting, plus labeled sorting bins. Use `\cutCard{item}` and `\wsSortBin[color]{label}`. Works well for classification tasks — sorting into mathematical categories requires genuine understanding.

```latex
\begin{sortCut}{Sort These into the Right Bin!}

Cut out the cards and sort them into the correct category.

\bigskip
\cutCard{$-3$} \cutCard{$4.5$} \cutCard{$0$} \cutCard{$\frac{-1}{2}$}
\cutCard{$7$} \cutCard{$-0.25$} \cutCard{$|-6|$} \cutCard{$-\frac{3}{4}$}

\begin{multicols}{3}
\wsSortBin[wsBlue]{Positive} \wsSortBin[wsPink]{Negative} \wsSortBin[wsSlate]{Zero}
\end{multicols}
\end{sortCut}
\worksheetAnswer{Positive: $4.5$, $7$, and $|-6| = 6$. Negative: $-3$, $\frac{-1}{2}$, $-0.25$, and $-\frac{3}{4}$. Zero: $0$. Key reasoning: absolute value $|-6|$ equals $6$ (positive), not $-6$. All numbers left of zero on the number line are negative; all numbers right of zero are positive.}
```

### Math Scenario — `mathScenario`
**Icon:** Globe | **Color:** Teal | **Best for:** Real-world application, multi-step word problems with data

Presents a realistic scenario with data (prices, measurements, statistics, rates), then asks multi-step questions. Use `\scenarioItem{name}{value}` for the data list. Scenarios should involve concepts appropriate for the grade level (from script output) — problems that mirror what students encounter in real life.

```latex
\begin{mathScenario}{Running a School Store!}

The student council tracks sales data for their school store this week:

\bigskip
\scenarioItem{Pencils sold}{$\mathbf{84}$ at $\$0.50$ each}
\scenarioItem{Notebooks sold}{$\mathbf{36}$ at $\$2.25$ each}
\scenarioItem{Erasers sold}{$\mathbf{60}$ at $\$0.75$ each}
\scenarioItem{Weekly goal}{$\$200$ total revenue}

\bigskip

What is the ratio of pencils to notebooks sold? Simplify.
\answerBlank[3cm]

\bigskip

How much total revenue did the store earn this week?
\answerBlank[4cm]

\bigskip

Did the store meet its weekly goal? By how much did it exceed or fall short?
\answerBlank[5cm]
\end{mathScenario}
\worksheetAnswer{(1)~The ratio of pencils to notebooks is $84 : 36$. The GCF of $84$ and $36$ is $12$, so the simplified ratio is $84 \div 12 : 36 \div 12 = \mathbf{7 : 3}$. (2)~Total revenue: pencils $= 84 \times 0.50 = \$42$; notebooks $= 36 \times 2.25 = \$81$; erasers $= 60 \times 0.75 = \$45$. Total $= 42 + 81 + 45 = \mathbf{\$168}$. (3)~The store fell short: $200 - 168 = \$32$ below the goal.}
```

### Input / Output — `inputOutput`
**Icon:** Gears | **Color:** Teal | **Best for:** Patterns, algebraic rules, expressions, dependent/independent variables

Function machine tables where students discover the rule or complete missing values. Students work with variables and algebraic rules in a concrete format — calibrate the complexity to the grade level from script output.

```latex
\begin{inputOutput}{Discover the Rule!}

Each machine follows a rule. Study the completed rows, then fill in the blanks and write the rule as an expression.

\bigskip
\textbf{Machine A:}

\renewcommand{\arraystretch}{1.6}
\begin{center}
\begin{tabular}{|C{2.5cm}|C{2.5cm}|}
\hline
\textbf{Input ($x$)} & \textbf{Output} \\
\hline
$2$ & $9$ \\
\hline
$5$ & $18$ \\
\hline
$10$ & \answerBlank[2cm] \\
\hline
$0$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}

Rule: Output $=$ \answerBlank[3cm]

\bigskip
\textbf{Machine B:}

\begin{center}
\begin{tabular}{|C{2.5cm}|C{2.5cm}|}
\hline
\textbf{Input ($x$)} & \textbf{Output} \\
\hline
$1$ & $-1$ \\
\hline
$4$ & $5$ \\
\hline
$7$ & \answerBlank[2cm] \\
\hline
$10$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}

Rule: Output $=$ \answerBlank[3cm]
\end{inputOutput}
\worksheetAnswer{Machine A: The rule is $\text{Output} = 3x + 3$. Check: $3(2) + 3 = 9$~\checkmark, $3(5) + 3 = 18$~\checkmark. Missing values: $3(10) + 3 = \mathbf{33}$ and $3(0) + 3 = \mathbf{3}$. Machine B: The rule is $\text{Output} = 2x - 3$. Check: $2(1) - 3 = -1$~\checkmark, $2(4) - 3 = 5$~\checkmark. Missing values: $2(7) - 3 = \mathbf{11}$ and $2(10) - 3 = \mathbf{17}$.}
```

### Explain It — `explainIt`
**Icon:** Speech bubble | **Color:** Blue | **Best for:** Mathematical reasoning, justification, constructing arguments

Students write mathematical explanations and justify their reasoning. This is a high-level activity that develops the communication skills emphasized in the standards (MP.3 — Construct viable arguments). Use `\writeLines{N}` for lined writing space.

```latex
\begin{explainIt}{Make Your Case!}

Mia says: ``A negative number is always less than a positive number.'' Is she right? Explain your reasoning using at least two examples.

\writeLines{5}

\bigskip

Leo claims: ``If you double both terms of any ratio, you get an equivalent ratio.'' Do you agree or disagree? Explain why, and give a specific example.

\writeLines{5}
\end{explainIt}
\worksheetAnswer{(1)~Mia is \textbf{correct}. Every negative number lies to the left of $0$ on the number line, and every positive number lies to the right. For example, $-100 < 1$ even though $100$ is ``larger'' --- the negative sign means it is left of zero. Similarly, $-0.5 < 0.001$. No matter how ``big'' the negative number looks, it is always less than any positive number. (2)~Leo is \textbf{correct}. Doubling both terms is the same as multiplying by $\frac{2}{2} = 1$, which does not change the value of the ratio. Example: $3 : 5$ becomes $6 : 10$; both simplify to $\frac{3}{5}$. In general, multiplying both terms by the \textbf{same} nonzero number produces an equivalent ratio.}
```

### Data Analysis — `dataAnalysis`
**Icon:** Chart bar | **Color:** Indigo | **Best for:** Interpreting data sets, computing statistics, drawing conclusions from tables or displays

Presents a data set (in a table, list, or pre-drawn display) and asks students to analyze it — compute mean, median, range, identify patterns, compare groups, or draw conclusions. This is a core activity type for data-focused chapters.

```latex
\begin{dataAnalysis}{Analyze the Results!}

Students in two classes took the same math quiz (out of $20$). Here are the scores:

\bigskip
\renewcommand{\arraystretch}{1.4}
\begin{center}
\begin{tabular}{|l|l|}
\hline
\textbf{Class A} & $12, \; 15, \; 18, \; 14, \; 16, \; 13, \; 17, \; 15, \; 19, \; 11$ \\
\hline
\textbf{Class B} & $10, \; 20, \; 8, \; 19, \; 11, \; 18, \; 9, \; 20, \; 12, \; 13$ \\
\hline
\end{tabular}
\end{center}

\bigskip

Find the \textbf{mean} of each class. \answerBlank[6cm]

\bigskip

Find the \textbf{median} of each class. \answerBlank[6cm]

\bigskip

Find the \textbf{range} of each class. \answerBlank[6cm]

\bigskip

Which class performed more consistently? Use the data to justify your answer.

\answerBlank[8cm]
\end{dataAnalysis}
\worksheetAnswer{(1)~Class A mean: $(12 + 15 + 18 + 14 + 16 + 13 + 17 + 15 + 19 + 11) \div 10 = 150 \div 10 = \mathbf{15}$. Class B mean: $(10 + 20 + 8 + 19 + 11 + 18 + 9 + 20 + 12 + 13) \div 10 = 140 \div 10 = \mathbf{14}$. (2)~Class A ordered: $11, 12, 13, 14, 15, 15, 16, 17, 18, 19$; median $= (15 + 15)/2 = \mathbf{15}$. Class B ordered: $8, 9, 10, 11, 12, 13, 18, 19, 20, 20$; median $= (12 + 13)/2 = \mathbf{12.5}$. (3)~Class A range: $19 - 11 = \mathbf{8}$. Class B range: $20 - 8 = \mathbf{12}$. (4)~Class A performed more consistently because its range ($8$) is much smaller than Class B's ($12$), meaning scores were more tightly clustered. Class B had extreme highs and lows.}
```

### Graph It — `graphIt`
**Icon:** Chart line | **Color:** Green | **Best for:** Coordinate plane plotting, interpreting graphs, graphing ratios and relationships

Students work with graphs — plotting ordered pairs, reading values from graphs, interpreting trends, or graphing a relationship from a table. Includes a pre-drawn coordinate grid or axes. Essential for topics involving the coordinate plane, ratio graphs, and representing relationships.

```latex
\begin{graphIt}{Plot and Analyze!}

A bakery tracks how many cupcakes it sells ($y$) based on the number of hours open ($x$):

\bigskip
\renewcommand{\arraystretch}{1.4}
\begin{center}
\begin{tabular}{|C{3cm}|C{3cm}|}
\hline
\textbf{Hours ($x$)} & \textbf{Cupcakes ($y$)} \\
\hline
$1$ & $15$ \\
\hline
$2$ & $30$ \\
\hline
$3$ & $45$ \\
\hline
$4$ & $60$ \\
\hline
$5$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}

\bigskip

Plot all five points on the coordinate plane below. Connect them with a straight line.

\begin{center}
\begin{tikzpicture}
\draw[step=0.5cm, gray!30, very thin] (0,0) grid (6,5);
\draw[thick, ->] (0,0) -- (6.3,0) node[right]{\small $x$ (Hours)};
\draw[thick, ->] (0,0) -- (0,5.3) node[above]{\small $y$ (Cupcakes)};
\foreach \x in {1,...,6} \draw (\x,0.05) -- (\x,-0.05) node[below]{\small \x};
\foreach \y in {1,...,5} \draw (0.05,\y) -- (-0.05,\y) node[left]{\small \pgfmathparse{int(\y*15)}\pgfmathresult};
\end{tikzpicture}
\end{center}

What is the unit rate (cupcakes per hour)? \answerBlank[3cm]

\bigskip

Write an equation relating $x$ and $y$: \answerBlank[4cm]

\bigskip

If the pattern continues, how many cupcakes after $8$ hours? \answerBlank[3cm]
\end{graphIt}
\worksheetAnswer{The missing value at $x = 5$ is $\mathbf{75}$ cupcakes. The five plotted points are $(1, 15)$, $(2, 30)$, $(3, 45)$, $(4, 60)$, $(5, 75)$ --- they form a straight line through the origin. The unit rate is $\mathbf{15}$ cupcakes per hour ($30 \div 2 = 15$, or $45 \div 3 = 15$). The equation is $\mathbf{y = 15x}$. After $8$ hours: $y = 15 \times 8 = \mathbf{120}$ cupcakes.}
```

### Table Challenge — `tableChallenge`
**Icon:** Table | **Color:** Purple | **Best for:** Completing ratio tables, function tables, proportional relationships, finding patterns in organized data

Presents partially-filled tables where students must identify the pattern or rule and fill in the missing values. This activity type makes tables the central object — students must read, analyze, extend, and sometimes create tables. Ideal for topics involving ratios, proportional relationships, and dependent/independent variables.

```latex
\begin{tableChallenge}{Complete the Ratio Tables!}

Each table shows a set of equivalent ratios. Find the pattern and fill in the missing values.

\bigskip
\textbf{Table 1:} A recipe uses flour and sugar in a fixed ratio.

\renewcommand{\arraystretch}{1.6}
\begin{center}
\begin{tabular}{|C{3cm}|C{3cm}|}
\hline
\textbf{Flour (cups)} & \textbf{Sugar (cups)} \\
\hline
$3$ & $2$ \\
\hline
$6$ & \answerBlank[2cm] \\
\hline
\answerBlank[2cm] & $8$ \\
\hline
$15$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}

\bigskip
\textbf{Table 2:} A map scale shows distance in inches and actual miles.

\begin{center}
\begin{tabular}{|C{3cm}|C{3cm}|}
\hline
\textbf{Map (in)} & \textbf{Actual (mi)} \\
\hline
$1$ & $25$ \\
\hline
$3$ & \answerBlank[2cm] \\
\hline
\answerBlank[2cm] & $125$ \\
\hline
$8$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}

What is the unit rate for the map scale? \answerBlank[4cm]
\end{tableChallenge}
\worksheetAnswer{Table 1: The ratio is $3 : 2$ (flour to sugar). Row 2: $6 \div 3 = 2$, so multiply sugar by $2$: $2 \times 2 = \mathbf{4}$. Row 3: $8 \div 2 = 4$, so flour $= 3 \times 4 = \mathbf{12}$. Row 4: $15 \div 3 = 5$, so sugar $= 2 \times 5 = \mathbf{10}$. Table 2: The ratio is $1 : 25$ (inches to miles). Row 2: $3 \times 25 = \mathbf{75}$ miles. Row 3: $125 \div 25 = \mathbf{5}$ inches. Row 4: $8 \times 25 = \mathbf{200}$ miles. The unit rate is $\mathbf{25}$ miles per inch.}
```

### Code Cracker — `codeCracker`
**Icon:** Lock | **Color:** Slate/Dark | **Best for:** Fluency wrapped in a decoding challenge — any topic where short-answer computations can be mapped to letters

Students solve a set of math problems. Each answer maps to a letter via a key. The correct answers spell out a secret word or phrase. This is an intellectually engaging, game-like format that works well for any topic where short-answer computations are involved.

```latex
\begin{codeCracker}{Crack the Secret Code!}

Solve each problem. Use the \textbf{code key} to convert your answers to letters, then unscramble the secret word!

\bigskip
\textbf{Code Key:}

\renewcommand{\arraystretch}{1.3}
\begin{center}
\small
\begin{tabular}{|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|C{1cm}|}
\hline
$6$ & $8$ & $12$ & $15$ & $20$ & $25$ & $30$ & $36$ & $50$ \\
\hline
R & A & T & I & O & S & E & D & N \\
\hline
\end{tabular}
\end{center}

\bigskip

Solve and decode:

\renewcommand{\arraystretch}{2.0}
\begin{center}
\begin{tabular}{|C{5cm}|C{1.8cm}|C{1.8cm}|}
\hline
\textbf{Problem} & \textbf{Answer} & \textbf{Letter} \\
\hline
$\frac{2}{3} \times 45$ & \answerBlank[1.2cm] & \answerBlank[1cm] \\
\hline
$|-8|$ & \answerBlank[1.2cm] & \answerBlank[1cm] \\
\hline
$12^2$ & \answerBlank[1.2cm] & \answerBlank[1cm] \\
\hline
$3^2 - 3$ & \answerBlank[1.2cm] & \answerBlank[1cm] \\
\hline
$\frac{48}{4}$ & \answerBlank[1.2cm] & \answerBlank[1cm] \\
\hline
$100 \div 2$ & \answerBlank[1.2cm] & \answerBlank[1cm] \\
\hline
\end{tabular}
\end{center}

\bigskip
Secret word: \answerBlank[6cm]
\end{codeCracker}
\worksheetAnswer{(1)~$\frac{2}{3} \times 45 = \frac{90}{3} = 30 \to$ \textbf{E}. (2)~$|-8| = 8 \to$ \textbf{A}. (3)~$12^2 = 144$... Wait, $144$ is not in the key --- let's re-check: actually $6^2 = 36 \to$ \textbf{D}. Correction: problem should be $6^2$. (4)~$3^2 - 3 = 9 - 3 = 6 \to$ \textbf{R}. (5)~$48 \div 4 = 12 \to$ \textbf{T}. (6)~$100 \div 2 = 50 \to$ \textbf{N}. The secret word is rearranged from E, A, D, R, T, N $=$ \textbf{TARDEN}... which unscrambles to \textbf{ARDENT} (or another word based on the problem design). \textit{Note: when writing codeCracker activities, pre-plan the word first, then build problems whose answers produce the correct letters.}}
```

**Important design note for `codeCracker`:** Always **start with the target word**, then work backward to create problems whose answers match the code key. Never design problems first and hope the letters spell something.

---

## Helper Commands

| Command | Purpose | Usage |
|---------|---------|-------|
| `\worksheetHeader{title}` | New-page banner with name/date/score fields | Start each worksheet |
| `\timerBadge{N}` | "N min" badge with stopwatch icon | Inside speed drills |
| `\matchRow{left}{right}` | Two-column matching pair | Inside `matchIt` |
| `\errorWork{text}` | Highlighted box showing wrong work | Inside `errorDetective` |
| `\cutCard{text}` | Dashed-border card for cutting | Inside `sortCut` |
| `\wsSortBin[color]{label}` | Labeled sorting bin area | Inside `sortCut` |
| `\scenarioItem{name}{value}` | Item in a data list | Inside `mathScenario` |
| `\writeLines{N}` | N lined rows for writing | Inside `explainIt` |
| `\worksheetSep` | Decorative divider within a worksheet | Between sections |
| `\worksheetDone` | Celebration banner | End of topic |
| `\answerBlank[width]` | Underlined blank for student answer | Anywhere |
| `\worksheetAnswer{text}` | Comprehensive answer for one worksheet | After `\end{environment}` |

---

## Creative Freedom & New Environments

### You Have Full Creative Freedom

There is **no rigid template** for worksheet content. The activity environments give you structure, but **what goes inside is entirely up to you**. The goal is to make a student (at the grade level reported by the script) engaged and practicing real math skills through varied, visually rich activity formats.

**You are encouraged to:**
- Choose activity types that **best fit the specific math topic** — not every topic needs every activity type
- **Invent entirely new activity formats** when the existing catalog doesn't serve the math concept well (see [Creating New Environments](#creating-new-environments) below)
- Use **realistic story contexts** and **diverse character names** (Mia, Leo, Zara, Marcus, Priya, Jordan, Kai, Aisha, etc.)
- Create **custom TikZ visuals** for graphs, coordinate planes, data displays, geometric figures, or any visual that serves the concept
- Use existing math helper commands from **VMfunMath.sty** inside worksheet activities:
  - `\numberLine{start}{end}` — number line diagram
  - `\fractionBar{num}{den}` — fraction bar visual
  - `\fractionCircle{num}{den}` — fraction circle visual
  - `\barGraph{labels}{values}{max}` — bar graph
  - `\areaGrid{rows}{cols}` — grid for area problems
  - `\perimeterRect{w}{h}` — labeled rectangle
  - `\numberLineFraction{marks}` — fraction number line
  - `\coordinatePlane` via TikZ — coordinate plane for graphing
- Design activities that work for **different learning styles** (visual, analytical, verbal)
- Create **tables, graphs, and data displays** as central activity elements
- Build activities around **real-world data** — sports statistics, recipe scaling, travel distances, budget planning, science experiments

### Activity Mix Planning

A good topic mix might include:
- 1 speed/fluency activity (speedDrill)
- 1 matching, sorting, or decoding activity (matchIt, sortCut, codeCracker)
- 1 analysis or problem-solving activity (errorDetective, dataAnalysis)
- 1 real-world or table-based activity (mathScenario, tableChallenge)
- 1 reasoning or graph-based activity (explainIt, graphIt, inputOutput)

This is just one possible mix. **Use your judgment** for what best fits the math concept. Data-heavy topics (statistics, ratios) should lean on `dataAnalysis`, `tableChallenge`, and `graphIt`. Algebra topics should lean on `inputOutput`, `errorDetective`, and `codeCracker`. Geometry topics might benefit from `drawSolve` or custom TikZ-based environments.

### Variety is Non-Negotiable

**All 5 worksheets in a topic must use different activity environments.** No two worksheets should have the same container. A topic with 5 speed drills is unacceptable. A topic with a speed drill, a table challenge, an error hunt, a graph activity, and a data analysis is excellent.

### Appropriate Difficulty

- Match the difficulty to the Study Guide source topic's level.
- Use a natural progression: first worksheet can be slightly easier, last can be slightly harder.
- The overall difficulty should be **practice-level** — students are reinforcing, not being challenged beyond their level. (Save that for the Puzzles book.)
- For grades 6–8, topics involve **multi-step reasoning** — don't oversimplify. A ratio problem should require simplifying or cross-multiplying, not just reading a number.
- **Always check the script output** for grade level and calibrate number ranges and concept depth accordingly.

---

## Answer System

Worksheets use the **worksheet answer system** (`\worksheetAnswer{}`), which is parallel to the puzzle answer system (`\puzzleAnswer{}`). Each worksheet gets **one comprehensive answer** that covers everything — both the final result(s) and the method to arrive at them.

### How It Works

1. `\worksheetAnswer{text}` is placed **immediately after** `\end{environment}` (outside the environment).
2. Each call is silently collected during compilation and written to a `.wsans` file.
3. The `\printWorksheetAnswers` command in the master document renders them as a "**Worksheet Solutions**" chapter at the end of the book.
4. Answers are automatically numbered and grouped by section with color-coded headings.

### Rules

1. **One `\worksheetAnswer{}` per worksheet** — placed outside `\end{environment}`, never inside.
2. **No `\prob`, `\answer{}`, or `\answerExplain{}{}`** — do NOT use the standard answer system.
3. **No `\resetProblems`** — the worksheet answer system uses its own counter (`wsAnsNum`).
4. **Comprehensive content** — include both the answers AND the reasoning/method.
5. **All numerical answers in `$...$`** — e.g., the answer is $500$.
6. **Number multiple items** — use `(1)~`, `(2)~`, `(3)~` when covering multiple questions.
7. **Verify every answer is mathematically correct.**

### Answer Style Reference

| Activity type | Answer style |
|---------|---------------|
| Speed drill | All values listed with computation shown for each |
| Matching | Each match stated with algebraic/arithmetic reasoning |
| Error detective | Each error identified, corrected, and explained with correct steps |
| Sort & cut | Groups listed with mathematical justification for each classification |
| Math scenario | Each question answered with multi-step calculation shown |
| Input/output | Missing values, rule expressed as an algebraic expression, verification shown |
| Explain it | Model written explanation demonstrating strong mathematical reasoning |
| Data analysis | Statistics computed step-by-step, conclusions supported by the data |
| Graph it | Points listed, equation/relationship identified, predictions justified |
| Table challenge | Pattern/rule identified, each missing value calculated with reasoning |
| Code cracker | Each problem solved, letter decoded, final word/phrase revealed |

---

## Creating New Environments

If a topic calls for an activity type that doesn't exist in the catalog, **you are encouraged to create new ones**. The existing 15 environments are a starting point, not a limit. Creativity is valued — if the math concept is best served by a format that doesn't exist yet, build it.

### Ideas for New Activity Types (Not Yet in VMfunWorksheet.sty)

These are suggestions — you can implement any of these or invent something entirely new:

- **Crossword / Word Search** — mathematical vocabulary crossword with clue-problems
- **True or False Card Sort** — statement cards students classify as true/false with justification
- **Two Truths and a Lie** — three math statements, one is false — students identify which
- **Step-by-Step Debugger** — a multi-step solution with ONE step wrong — students find which
- **Comparison Challenge** — two approaches/methods/answers side by side — students analyze which is correct or more efficient
- **Math Interview** — students write questions they'd ask to solve a problem, then answer them
- **Pattern Detective** — find the pattern in a sequence and predict the next terms
- **Quick Quiz** — rapid-fire multiple-choice or fill-in-the-blank on a single concept
- **Build Your Own** — students create their own example of a concept (e.g., "create a ratio table for a ratio of your choice")

### Where to Add New Environments

Add to **`VM_packages/VMfunWorksheet.sty`**. Follow the existing pattern:

```latex
%========================================================================================
% N. ENVIRONMENT NAME
%    Description of what it's for.
%    Usage: \begin{envName}{title} ... \end{envName}
%========================================================================================
\newtcolorbox{envName}[1][Default Title]{
    enhanced,
    colback=white,                          % MUST be white for B&W printing
    colframe=wsAccentColor,                 % Border color (choose from ws palette)
    colbacktitle=wsAccentColor,             % Title bar color
    coltitle=white,
    fonttitle=\Large\bfseries\sffamily,
    title={\raisebox{-0.1em}{\color{wsYellow}\faIconName}\hspace{3mm}#1},
    halign title=center,
    arc=8pt,
    outer arc=8pt,
    boxrule=1.5pt,
    top=5mm, bottom=5mm,
    left=5mm, right=5mm,
    toptitle=4mm, bottomtitle=4mm,
    before skip=8pt, after skip=8pt,
    breakable,
}
```

### Design Guidelines for New Environments

1. **`colback=white`** — mandatory. No colored backgrounds in content areas.
2. **Use the worksheet color palette:** `wsGreen`, `wsOrange`, `wsPink`, `wsBlue`, `wsTeal`, `wsPurple`, `wsRed`, `wsYellow`, `wsSlate`.
3. **Include a Font Awesome icon** in the title. Check that it exists in FA5 — avoid `Alt` suffix icons (e.g., use `\faPen` not `\faPencilAlt`).
4. **Keep it `tcolorbox`-based** with `breakable` for page-break safety.
5. **Use `8pt` arc and `1.5pt` boxrule** to match the visual style.
6. **Document with a comment block** showing usage.
7. **Each new environment should have a distinct accent color** from the existing ones.

### New TikZ Commands and Helpers

If your activity needs a custom visual (coordinate grid, graph template, geometric diagram, etc.), create a TikZ command or helper in `VMfunWorksheet.sty`:

```latex
\newcommand{\myHelper}[2][wsGreen]{%
    \tikz[baseline=-0.3ex]{%
        \node[draw=#1, fill=white, ...]{#2};
    }\hspace{1mm}%
}
```

### When to Create vs Reuse

- **Reuse** an existing environment when it fits the activity's purpose well.
- **Create new** when the activity has a distinctly different visual identity or interaction model.
- **Don't over-create** — if you need a one-off layout, use inline TikZ or `tcolorbox` inside an existing environment rather than creating a new one.
- When in doubt, create the new environment — it adds to the diversity of future worksheets.

---

## State-Specific Handling

The worksheet book follows the same state-specific system as other book types. The `get_chapter_topic_facts.py` script automatically lists which topics are additional (state-specific) and which are modified (state variants), along with which states use them.

| Study Guide source | Worksheet directory | Purpose |
|-------------------|---------------------|---------|
| `topics/` | `topics_worksheet/` | Core CCSS worksheets (all states) |
| `topics_additional/` | `topics_worksheet_additional/` | State-specific supplementary worksheets |
| `topics_modified/` | `topics_worksheet_modified/` | Modified worksheets for specific states |

### Additional Topics

State-specific additional topics get their own worksheet files in `topics_worksheet_additional/`. These typically have **4 worksheets** (shorter than core topics). Add a header comment documenting which states use them (this information comes from the script output "Included States" field).

### Modified Topics

When a state modifies a core topic (shown in the script output under "MODIFIED TOPICS"), create a variant in `topics_worksheet_modified/` with the same filename. Read the modified study guide source to understand what changed, and adjust worksheet content accordingly. Document which states use it (from the script output "Modified States" field).

---

## Complete Example

Here is a complete, well-structured worksheet topic:

```latex
% ============================================================================
% WORKSHEET — Section 1.5: Tables of Equivalent Ratios
% CCSS 6.RP.A.3a
% ============================================================================
\section{Tables of Equivalent Ratios}
\setcounter{wsNumber}{0}

\begin{worksheetSkills}
\begin{itemize}
    \item Use tables to find missing values in equivalent ratio pairs
    \item Identify and extend patterns in ratio tables
    \item Apply ratio reasoning to solve real-world problems using tables
\end{itemize}
\end{worksheetSkills}

% ── WORKSHEET 1: Speed Drill ─────────────────────────────────────────────────
\worksheetHeader{Equivalent Ratio Sprint}

\begin{speedDrill}{How Fast Can You Complete the Table?}
\timerBadge{4}

Fill in the missing values. Each row is an \textbf{equivalent ratio}.

\bigskip
\renewcommand{\arraystretch}{2.0}
\begin{center}
\sffamily\large
\begin{tabular}{|C{3cm}|C{3cm}||C{3cm}|C{3cm}|}
\hline
$x$ & $y$ & $x$ & $y$ \\
\hline
$2$ & $5$ & $3$ & $7$ \\
\hline
$4$ & \answerBlank[2cm] & $6$ & \answerBlank[2cm] \\
\hline
$6$ & \answerBlank[2cm] & $9$ & \answerBlank[2cm] \\
\hline
\answerBlank[2cm] & $25$ & \answerBlank[2cm] & $35$ \\
\hline
$14$ & \answerBlank[2cm] & $30$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}
\end{speedDrill}
\worksheetAnswer{Left table (ratio $2 : 5$): Row 2: $y = 10$ ($\times 2$). Row 3: $y = 15$ ($\times 3$). Row 4: $x = 10$ ($25 \div 5 = 5$, so $\times 5$, thus $x = 2 \times 5 = 10$). Row 5: $y = 35$ ($14 \div 2 = 7$, so $\times 7$, thus $y = 5 \times 7 = 35$). Right table (ratio $3 : 7$): Row 2: $y = 14$ ($\times 2$). Row 3: $y = 21$ ($\times 3$). Row 4: $x = 15$ ($35 \div 7 = 5$, so $x = 3 \times 5 = 15$). Row 5: $y = 70$ ($30 \div 3 = 10$, so $y = 7 \times 10 = 70$). To complete each row, find the multiplier by dividing the known value by the original ratio term.}

% ── WORKSHEET 2: Table Challenge ─────────────────────────────────────────────
\worksheetHeader{Recipe Ratio Tables}

\begin{tableChallenge}{Scale the Recipes!}

A smoothie recipe calls for fruit and yogurt in a fixed ratio. Complete each table and answer the question.

\bigskip
\textbf{Recipe A:} Strawberry Smoothie (ratio $4 : 3$, fruit cups to yogurt cups)

\renewcommand{\arraystretch}{1.6}
\begin{center}
\begin{tabular}{|C{3cm}|C{3cm}|}
\hline
\textbf{Fruit (cups)} & \textbf{Yogurt (cups)} \\
\hline
$4$ & $3$ \\
\hline
$8$ & \answerBlank[2cm] \\
\hline
\answerBlank[2cm] & $12$ \\
\hline
$20$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}

\bigskip
\textbf{Recipe B:} Mango Smoothie (ratio $5 : 2$, fruit cups to yogurt cups)

\begin{center}
\begin{tabular}{|C{3cm}|C{3cm}|}
\hline
\textbf{Fruit (cups)} & \textbf{Yogurt (cups)} \\
\hline
$5$ & $2$ \\
\hline
$15$ & \answerBlank[2cm] \\
\hline
\answerBlank[2cm] & $10$ \\
\hline
$35$ & \answerBlank[2cm] \\
\hline
\end{tabular}
\end{center}

\bigskip
If you have $24$ cups of fruit, which recipe uses more yogurt? \answerBlank[4cm]
\end{tableChallenge}
\worksheetAnswer{Recipe A ($4 : 3$): Row 2: yogurt $= 6$ ($\times 2$). Row 3: fruit $= 16$ ($12 \div 3 = 4$, so $\times 4$). Row 4: yogurt $= 15$ ($20 \div 4 = 5$, so $\times 5$). Recipe B ($5 : 2$): Row 2: yogurt $= 6$ ($\times 3$). Row 3: fruit $= 25$ ($10 \div 2 = 5$, so $\times 5$). Row 4: yogurt $= 14$ ($35 \div 5 = 7$, so $\times 7$). For $24$ cups of fruit --- Recipe A: $24 \div 4 = 6$, so yogurt $= 3 \times 6 = \mathbf{18}$. Recipe B: $24 \div 5 = 4.8$, so yogurt $= 2 \times 4.8 = \mathbf{9.6}$. \textbf{Recipe A} uses more yogurt ($18 > 9.6$).}

% ── WORKSHEET 3: Error Detective ─────────────────────────────────────────────
\worksheetHeader{Ratio Table Mistake Hunt}

\begin{errorDetective}{Can You Catch the Mistakes?}

Zara filled in these ratio tables. \textbf{Some entries are wrong!} Find each error, explain what went wrong, and write the correct value.

\bigskip

\textbf{Table 1:} Ratio $3 : 8$

\renewcommand{\arraystretch}{1.4}
\begin{center}
\begin{tabular}{|C{2cm}|C{2cm}|}
\hline
$3$ & $8$ \\
\hline
$6$ & $16$ \\
\hline
$9$ & $22$ \\
\hline
\end{tabular}
\end{center}

Error? \answerBlank[2cm] \quad If wrong, the correct value is: \answerBlank[3cm]

\bigskip

\textbf{Table 2:} Ratio $5 : 4$

\begin{center}
\begin{tabular}{|C{2cm}|C{2cm}|}
\hline
$5$ & $4$ \\
\hline
$10$ & $9$ \\
\hline
$20$ & $16$ \\
\hline
\end{tabular}
\end{center}

Error? \answerBlank[2cm] \quad If wrong, the correct value is: \answerBlank[3cm]

\bigskip

\textbf{Table 3:} Ratio $2 : 7$

\begin{center}
\begin{tabular}{|C{2cm}|C{2cm}|}
\hline
$2$ & $7$ \\
\hline
$4$ & $14$ \\
\hline
$8$ & $21$ \\
\hline
\end{tabular}
\end{center}

Error? \answerBlank[2cm] \quad If wrong, the correct value is: \answerBlank[3cm]
\end{errorDetective}
\worksheetAnswer{All three tables have errors. (1)~Table 1, Row 3: The second value should be $24$, not $22$. Zara added $6$ each time ($8, 16, 22$) instead of multiplying: $8 \times 3 = 24$. The correct pattern is $\times 3$ for the entire row. (2)~Table 2, Row 2: The second value should be $8$, not $9$. The multiplier is $\times 2$ ($5 \to 10$), so $4 \times 2 = 8$. Zara added $5$ to $4$ instead of multiplying by $2$. (3)~Table 3, Row 3: The second value should be $28$, not $21$. The multiplier is $\times 4$ ($2 \to 8$), so $7 \times 4 = 28$. Zara used $\times 3$ ($7 \times 3 = 21$) but the first column shows $\times 4$.}

% ── WORKSHEET 4: Graph It ────────────────────────────────────────────────────
\worksheetHeader{Plotting Equivalent Ratios}

\begin{graphIt}{From Table to Graph!}

The table shows equivalent ratios of lemonade mix (scoops) to water (cups):

\renewcommand{\arraystretch}{1.4}
\begin{center}
\begin{tabular}{|C{3cm}|C{3cm}|}
\hline
\textbf{Mix (scoops)} & \textbf{Water (cups)} \\
\hline
$1$ & $4$ \\
\hline
$2$ & $8$ \\
\hline
$3$ & $12$ \\
\hline
$4$ & $16$ \\
\hline
\end{tabular}
\end{center}

Plot all four ordered pairs on the coordinate plane below:

\begin{center}
\begin{tikzpicture}
\draw[step=0.5cm, gray!30, very thin] (0,0) grid (5,5);
\draw[thick, ->] (0,0) -- (5.3,0) node[right]{\small Scoops};
\draw[thick, ->] (0,0) -- (0,5.3) node[above]{\small Cups};
\foreach \x in {1,...,5} \draw (\x,0.05) -- (\x,-0.05) node[below]{\small \x};
\foreach \y in {1,...,5} \draw (0.05,\y) -- (-0.05,\y) node[left]{\small \pgfmathparse{int(\y*4)}\pgfmathresult};
\end{tikzpicture}
\end{center}

Do the points form a straight line? \answerBlank[2cm]

\bigskip

Does the line pass through the origin $(0, 0)$? Why does that make sense?
\answerBlank[6cm]

\bigskip

Using the graph or the table, how many cups of water for $6$ scoops? \answerBlank[3cm]
\end{graphIt}
\worksheetAnswer{The four ordered pairs are $(1, 4)$, $(2, 8)$, $(3, 12)$, $(4, 16)$. Yes, the points form a \textbf{straight line}. Yes, the line passes through the origin $(0, 0)$ because $0$ scoops requires $0$ cups of water --- the relationship is \textbf{proportional}. For $6$ scoops: the ratio is $1 : 4$, so $6 \times 4 = \mathbf{24}$ cups of water. Alternatively, extend the pattern: each additional scoop adds $4$ cups.}

% ── WORKSHEET 5: Explain It ──────────────────────────────────────────────────
\worksheetHeader{Ratio Table Reasoning}

\begin{explainIt}{Think It Through!}

Leo made this ratio table for a $2 : 5$ ratio and says it is correct:

\renewcommand{\arraystretch}{1.4}
\begin{center}
\begin{tabular}{|C{2cm}|C{2cm}|}
\hline
$2$ & $5$ \\
\hline
$4$ & $10$ \\
\hline
$5$ & $13$ \\
\hline
$6$ & $15$ \\
\hline
\end{tabular}
\end{center}

Is every row correct? If not, identify the error and explain what Leo likely did wrong. Then provide the correct table.

\writeLines{6}

\bigskip

Mia says, ``You can always add the same number to both sides of a ratio to get an equivalent ratio.'' For example, she says $3 : 4$ becomes $5 : 6$ (adding $2$ to each). Is Mia right or wrong? Explain why, and show a counterexample if she's wrong.

\writeLines{6}
\end{explainIt}
\worksheetAnswer{(1)~Row 3 is \textbf{wrong}: $5$ and $13$ is not a $2 : 5$ ratio. Leo went from Row 2 to Row 3 by adding $1$ to the first column and adding $3$ to the second --- but equivalent ratios require \textbf{multiplying} both terms by the same factor, not adding. The correct Row 3 with first term $6$: $6 \div 2 = 3$, so $5 \times 3 = 15$. The row should be $6$ and $15$ (which is Row 4 in Leo's table). The correct row for multiplier $2.5$ ($5 \div 2$): $5$ and $12.5$. A correct table: $(2, 5)$, $(4, 10)$, $(6, 15)$, $(8, 20)$. (2)~Mia is \textbf{wrong}. Adding the same number to both terms changes the ratio. $3 : 4 = 0.75$, but $5 : 6 \approx 0.83$ --- these are not equal. Equivalent ratios are made by \textbf{multiplying} (or dividing) both terms by the same nonzero number. For example, $3 : 4 = 6 : 8 = 9 : 12$.}

\worksheetDone
```

---

## What to Include

- `\section{}` + `\setcounter{wsNumber}{0}` — every topic
- `\begin{worksheetSkills}` — every topic
- **5 worksheets** using `\worksheetHeader{}` + activity environments
- `\worksheetAnswer{}` after each `\end{environment}` — one comprehensive answer per worksheet
- `\worksheetDone` at the end
- Visual elements (TikZ graphs, coordinate planes, tables, data displays)
- `\answerBlank[width]` for student answer spaces
- Math always in `$...$`
- Bold key terms with `\textbf{}`

## What to Omit

These should **never** appear in worksheet topic files:

- `\begin{conceptBox}` / `\begin{stepsBox}` / `\begin{vocabBox}` — no teaching
- `\begin{workedExample}` / `\begin{sideBySideExample}` — no worked examples
- `\begin{learningGoals}` — use `worksheetSkills` instead
- `\topicTitle{}` — worksheets use `\worksheetHeader{}` per activity
- `\begin{quickReview}` — no review content (that's for the workbook)
- `\puzzleAnswer{}` — worksheet uses `\worksheetAnswer{}`
- `\printPuzzleAnswers` — worksheet uses `\printWorksheetAnswers`
- `\resetProblems` — not needed (worksheet answer system uses its own counter)
- `\prob` — questions are asked directly as text, no `\prob` prefix
- `\answer{}` / `\answerExplain{}{}` — use `\worksheetAnswer{}` instead
- `\rowcolor{}` on tables — dark in B&W printing
- `\writeAnsQuiz` — not needed for worksheets

---

## After Creation is Complete

After writing all worksheet topics for the requested chapter:
1. Create a test LaTeX file in `tests/test_worksheet_ch<N>.tex` that includes all new topic files.
2. Compile with: `latexmk -xelatex -output-directory=build -interaction=nonstopmode -f tests/test_worksheet_ch<N>.tex`
3. Check the log for errors: `grep -i 'error\|undefined' build/test_worksheet_ch<N>.log | grep -v Warning | head -20`
4. Open the PDF so the user can give feedback on content and formatting.

**Test file template:**

```latex
% ============================================================================
% TEST BUILD — Worksheet Chapter N
% ============================================================================
\documentclass[12pt, fleqn, openany]{studyGuide}
\setstretch{1.4}

\begin{document}
\pagenumbering{arabic}

\chapter{Chapter Title}

% Core topics
\input{topics_worksheet/ch0N-01-slug.tex}
\input{topics_worksheet/ch0N-02-slug.tex}
% ... all core topics for the chapter ...

% Additional topics (if any)
\input{topics_worksheet_additional/ch0N-NN-slug.tex}

% Modified topics (if any)
\input{topics_worksheet_modified/ch0N-NN-slug.tex}

% Print collected answers
\printWorksheetAnswers

\end{document}
```

---

## Checklist

- [ ] Ran `python3 scripts/get_chapter_topic_facts.py --chapter <N>` to discover topics, grade, and audience
- [ ] Read every Study Guide source file listed by the script (core + additional + modified)
- [ ] File placed in correct folder (`topics_worksheet/`, `topics_worksheet_additional/`, or `topics_worksheet_modified/`)
- [ ] Filename matches: `ch<CC>-<SS>-<slug>.tex`
- [ ] Starts with `\section{}` → `\setcounter{wsNumber}{0}`
- [ ] `\begin{worksheetSkills}` present with 2–4 skills
- [ ] Contains **exactly 5 worksheets**, each with `\worksheetHeader{}`
- [ ] **All 5 worksheets use different activity environments** — no repeats
- [ ] Every worksheet has exactly one `\worksheetAnswer{}` placed after `\end{environment}`
- [ ] Each `\worksheetAnswer{}` is comprehensive (includes result + method)
- [ ] No `\prob`, `\answer{}`, `\answerExplain{}{}`, or `\resetProblems`
- [ ] `\worksheetDone` at the very end
- [ ] All content-area backgrounds are white (no `\rowcolor`, no colored `colback`)
- [ ] All math in `$...$`
- [ ] All answers are **mathematically correct** (verified by hand)
- [ ] Instructions are clear enough for the target age group (from script output) without help
- [ ] Activities feel age-appropriate — no coloring pages, simple mazes, drawing base-ten blocks, or other activities designed for younger children
- [ ] Difficulty matches the grade level from script output
- [ ] Tables and/or graphs are used where they fit the topic
- [ ] If new environments were created, they are in `VMfunWorksheet.sty` with documentation
- [ ] Create a test LaTeX file in `tests/` that includes all new topics, compile it, and open the PDF
