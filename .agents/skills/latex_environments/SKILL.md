---
name: latex_environments
description: Complete reference of all custom LaTeX environments for Grade 7 math topics
---

# Grade 7 LaTeX Environments Reference

This project uses a custom LaTeX class (`studyGuide.cls`) with 15 `.sty` packages in `VM_packages/`. You can use any of the environments defined in these packages when writing topics.

You have a large toolkit — choose whichever environments best serve the topic. There is no required ordering or mandatory checklist of environments per topic. Use your judgment to create engaging, varied content.

## Creating New Environments

If a topic genuinely needs a visual or interactive element that no existing environment provides, you may create new LaTeX environments or commands. New environments should be added to the appropriate `.sty` file in `VM_packages/` (or a new `.sty` file if none fits).

When creating new environments:
- Study the existing `.sty` files to match the coding style, color conventions, and `tcolorbox` patterns.
- Use the project's color palette (`funBlue`, `funGreen`, `funOrange`, etc.) — don't introduce random colors.
- New environments should be self-contained and not depend on or modify existing environment internals.
- Add a clear header comment block with the environment name, usage signature, and description.

**CRITICAL RULE: Never modify existing environments or commands.** They are used across many topics and book types. Even a small change can break other sections. If an existing environment doesn't do exactly what you want, create a new one instead.

## Teaching & Concepts (VMfunTeaching.sty)

### Topic Title Banner
```latex
\topicTitle{Multiply by a One-Digit Number}
```
Light blue banner with blue border. One per topic, placed right after `\section{...}`.

### Learning Goals
```latex
\begin{learningGoals}
\begin{itemize}
    \item Multiply a multi-digit number by a one-digit number
    \item Use area models, partial products, and the standard algorithm
\end{itemize}
\end{learningGoals}
```
Blue box with bullseye icon, left accent bar, and subtle watermark. Always the first content box after topicTitle.

### Concept Box (main teaching content)
```latex
\begin{conceptBox}{Steps to Add}          % default green
\begin{conceptBox}[funTeal]{Division}      % custom color
```
Colors: `funGreen` (default), `funBlue`, `funOrange`, `funTeal`, `funPurple`.

### Steps Box (numbered steps)
```latex
\begin{stepsBox}{How to Multiply}
    \funStep Multiply the ones
    \funStep Multiply the tens
    \funStep Add the results
\end{stepsBox}
```
Steps auto-number with colored circles (green, blue, red, orange, purple). For manual control:
```latex
\namedStep{3}{stepThree}  % explicit number and color
```

### Remember Box
```latex
\begin{rememberBox}
    Always start from the RIGHT (ones column)!
\end{rememberBox}
```

### Math Rule Box
```latex
\begin{mathRuleBox}{Commutative Property}
    $a \times b = b \times a$
\end{mathRuleBox}
```

### Vocabulary Box
```latex
\begin{vocabBox}[Division Vocabulary]       % optional custom title
    \vocabWord{Dividend}{The number being divided.}
    \vocabWord{Divisor}{The number you divide by.}
\end{vocabBox}
```

### Key Idea (inline highlight)
```latex
The answer is \keyIdea{always positive}.
```

### Definition Spotlight (centered prominent text)
```latex
\definitionSpotlight{Division = Sharing Equally!}
\definitionSpotlight[funGreenDark]{Custom color}
```

### Side-by-side Comparison
```latex
\begin{compareBox}{Sharing}{Grouping}
    Left content...
\tcblower
    Right content...
\end{compareBox}
```

### Box Subtitle (inside any box)
```latex
\boxSubtitle{Steps to Add}
\boxSubtitle[funOrange]{Another subtitle}
```

### Explore Box (guided discovery / investigation)
```latex
\begin{exploreBox}                          % default "Explore"
\begin{exploreBox}{Try Different Numbers}   % custom title
    Try multiplying these pairs. What do you notice?
    \begin{itemize}
        \item $3 \times 4 = $ \answerBlank[1.5cm]
        \item $4 \times 3 = $ \answerBlank[1.5cm]
    \end{itemize}
    What pattern do you see? \answerBlank[5cm]
\end{exploreBox}
```
Green box with dashed bottom border. Great for hands-on discovery activities where students try things and draw conclusions.

### Pattern Box (pattern recognition)
```latex
\begin{patternBox}                          % default "Find the Pattern"
\begin{patternBox}{What Comes Next?}        % custom title
    Look at this pattern: $2, 4, 6, 8, $ \answerBlank[1cm], \answerBlank[1cm]

    The rule is: \answerBlank[4cm]
\end{patternBox}
```
Purple box with dot motif. Ideal for pattern recognition, number sequences, and extending patterns.

### Quick Review (compact concept refresher)
```latex
\begin{quickReview}{Place Value}           % default funOrange
\begin{quickReview}[funTeal]{Fractions}     % custom color
    Brief recap of a previously taught concept...
\end{quickReview}
```
Lighter than `conceptBox` — use when students need a quick reminder of a prerequisite concept before new material.

### Proof / Justification Box
```latex
\begin{proofBox}                            % default "Justify Your Reasoning"
\begin{proofBox}{Show Why It Works}         % custom title
    Explain why $a \times (b + c) = a \times b + a \times c$...
\end{proofBox}
```
Indigo box with pen-nib icon and left accent bar. For introducing basic mathematical reasoning and justifications. Ideal for Grade 7 students beginning formal reasoning skills.

### Formula Card
```latex
\formulaCard{Area of a Triangle}{$A = \frac{1}{2} \times b \times h$}
```
Centered, prominently bordered green card for key formulas. Use for the one or two most important formulas a student should memorize from a topic.

## Examples & Solutions (VMfunExamples.sty)

### Worked Example
```latex
\begin{workedExample}{Add 347 + 285}
    Show the work here...
    \answerHighlight{$347 + 285 = 632$}
\end{workedExample}
```

### Side-by-side Example (work left, explanation right)
```latex
\begin{sideBySideExample}{Another Example}
    Left: visual / work
\tcblower
    Right: step-by-step explanation
\end{sideBySideExample}
```

### Auto-numbered Example
```latex
\begin{numberedExample}
    Content...
\end{numberedExample}
```

### Solution Steps (inside any example)
```latex
\solutionLabel              % prints "Solution:"
\solutionLabel[Step by Step:]

\begin{solutionSteps}
    \solStep Ones: $6 + 8 = 14$, write 4, carry 1
    \solStep Tens: $5 + 7 + 1 = 13$
\end{solutionSteps}
```

### Answer Highlight
```latex
\answerHighlight{$456 + 278 = 734$}
\answerHighlight[funOrange]{Custom color answer}
```

### Mini Answer (inline)
```latex
So the answer is \miniAnswer{42}.
```

### Try It Yourself
```latex
\tryIt{Now you try: $300 + 250 = $ \answerBlank}
```

### Answer Blank
```latex
\answerBlank         % 3cm default
\answerBlank[2cm]    % custom width
```

### Answer Line (full-width)
```latex
\answerLine          % default: \linewidth
\answerLine[10cm]    % custom width
```

### Show Me Box
```latex
\begin{showMeBox}[Walkthrough]
    Detailed walkthrough...
\end{showMeBox}
```

### Error Box (find and fix the mistake)
```latex
\begin{errorBox}                           % default "Spot the Error"
\begin{errorBox}{What Went Wrong?}         % custom title
    Sam says $4 \times 6 = 20$. Is Sam correct?

    What is the real answer? \answerBlank[2cm]

    Explain what went wrong: \answerBlank[5cm]
\end{errorBox}
```
Red-themed box with warning icon. Shows intentionally wrong work for students to analyze and correct. Builds critical thinking. Use `\wrongAnswer` inside for crossed-out wrong work with a correction blank:
```latex
\wrongAnswer{$3 \times 5 = 20$}    % shows crossed-out wrong answer → blank
```

## Practice & Assessment (VMfunPractice.sty)

### Practice Box (main practice section)
```latex
\begin{practiceBox}{Addition Practice}
    \resetProblems
    \practiceHeader{Add These Numbers}
    \prob $234 + 152 = $ \answerBlank[2cm]
    \prob $456 + 328 = $ \answerBlank[2cm]
\end{practiceBox}
```

### Practice Subsection Headers
```latex
\practiceHeader{Basic Problems}
\practiceHeader[funOrange]{Show Your Work}
\practiceHeader[funGreen]{Find the Missing Number}
```

### Show Your Work Box
```latex
\begin{showWorkBox}{Add. Show Your Work.}
    Column addition workspace...
\end{showWorkBox}
```

### Find the Missing Number Box
```latex
\begin{findMissingBox}{Find the Missing Number}
    \prob $245 + $ \answerBlank[1.5cm] $= 500$
\end{findMissingBox}
```

### Challenge Box
```latex
\begin{challengeBox}              % default title "Challenge!"
\begin{challengeBox}[Super Challenge!]   % custom title
```
Purple box with trophy and star icons, outer glow border, and subtle star watermark. Feels premium and rewarding.

### Quick Check
```latex
\begin{quickCheck}
    Fast problems to check understanding...
\end{quickCheck}
```

### Problem Numbering
```latex
\resetProblems           % reset counter to 0
\prob                    % auto-numbered: "1.", "2.", ...
\probInline              % inline version for grid layouts
\setcounter{funProblem}{9}  % manually set counter
```

### Word Problem (with answer line)
```latex
\wordProblem{A library has 375 math books and 248 science books. How many in total?}{books}
```

### True or False
```latex
\trueOrFalse{$15 \div 3 = 5$}
```

### Multiple Choice
```latex
\multiChoice{What is $12 \div 3$?}{2}{3}{4}{6}      % inline row layout
\multiChoiceGrid{What is $12 \div 3$?}{2}{3}{4}{6}  % 2×2 grid layout
```

### Circle the Answer
```latex
\circleAnswer{Which is correct?}{15}{20}{25}{30}
```

### Match Box
```latex
\begin{matchBox}{Match the Pairs}
    matching content...
\end{matchBox}
```

### Sort Box (classification / sorting activity)
```latex
\begin{sortBox}{Sort These Numbers Into Two Groups}
    Numbers to sort: $12, 15, 18, 21, 24, 25, 27, 30$

    \begin{multicols}{2}
    \sortCategory[funBlue]{Multiples of 3}
    \sortCategory[funOrange]{NOT Multiples of 3}
    \end{multicols}
\end{sortBox}
```
Orange-themed box for sorting/classifying activities. Use `\sortCategory[color]{Label}` to create labeled bins, and `\sortItem` for inline item tags:
```latex
\sortItem  % inline sortable item tag
```

### Fill Table (input/output table for patterns)
```latex
\begin{fillTable}{Find the Rule}
    \begin{tabular}{|C{2cm}|C{2cm}|}
        \hline
        \textbf{In} & \textbf{Out} \\
        \hline
        3 & 9 \\
        \hline
        5 & 15 \\
        \hline
        7 & \answerBlank[1cm] \\
        \hline
        \answerBlank[1cm] & 27 \\
        \hline
    \end{tabular}

    \bigskip
    The rule is: \answerBlank[4cm]
\end{fillTable}
```
Teal-themed centered box for "function machine" and input/output pattern problems.

### Code Breaker (solve problems to decode a secret message)
```latex
\begin{codeBreaker}                         % default "Code Breaker"
\begin{codeBreaker}{Secret Agent Math!}     % custom title
    Solve each clue. Match your answers to the letters below!

    \codeClue{M}{$3 \times 4$}
    \codeClue{A}{$20 \div 5$}
    \codeClue{T}{$2 \times 5$}
    \codeClue{H}{$18 \div 3$}

    \secretMessage{\answerBlank[1cm] \answerBlank[1cm] \answerBlank[1cm] \answerBlank[1cm]}
\end{codeBreaker}
```
Purple spy-themed box with key icon. Students solve math problems to decode a secret message. Extremely engaging for kids — use for variety in practice sections. `\codeClue{letter}{problem}` creates a circled letter + problem + answer blank. `\secretMessage{...}` creates the decoder area.

### Pictograph Environment (picture graph)
```latex
\begin{picGraph}{Favorite Fruits}           % default blue
\begin{picGraph}[funGreen]{Pet Survey}      % custom color
    \picRow{Dog}{5}
    \picRow{Cat}{3}
    \picRow[\faHeart]{Fish}{2}              % custom symbol
    \picRow{Bird}{4}
    \picKey{2 students}                     % key/legend
    \picKey[\faHeart]{1 vote}               % custom symbol in key
\end{picGraph}
```
Chart box for picture graphs (Ch 6). `\picRow[symbol]{label}{count}` draws repeated symbols. `\picKey[symbol]{unit}` adds the key legend. Default symbol is `\faStar` in yellow.

### Math Trail (connected problem sequence)
```latex
\begin{mathTrail}                           % default "Math Trail"
\begin{mathTrail}{Number Adventure!}        % custom title
    \trailStop Start with $5$. Double it! \answerBlank
    \trailStop Add $3$ to your answer. \answerBlank
    \trailStop Multiply by $2$. \answerBlank
    \trailStop Subtract $6$. What did you get? \answerBlank
\end{mathTrail}
```
Green trail-themed box with map marker icon. Problems are auto-numbered stops with arrows. Each answer feeds the next step — creates a "journey" through math. Great for building multi-step reasoning.

### Self Check (confidence scale)
```latex
\selfCheck
```

### Strategy Box (problem-solving approaches)
```latex
\begin{strategyBox}                         % default "Problem-Solving Strategy"
\begin{strategyBox}{Working Backwards}      % custom title
    1. Start with the final answer
    2. Reverse each operation
    3. Check by working forward
\end{strategyBox}
```
Teal box with lightbulb icon and left accent bar. For teaching problem-solving strategies and systematic approaches. Ideal for Grade 7 students developing independent problem-solving skills.

### Answer Space
```latex
\answerSpace        % 2cm default
\answerSpace[4cm]   % custom height
```

### Practice Test Questions
Used in practice test books. Each question is wrapped in `practiceQuestion` with a type (`mc`, `sa`, `gsa`):
```latex
\begin{practiceQuestion}{Q1}{mc}
    What is $3 + 4$?
    \choiceA{5}
    \choiceB{6}
    \choiceC{7}
    \choiceD{8}    % \choiceD renders all four options
    \correctAnswer{C}
    \explanation{$3 + 4 = 7$}
\end{practiceQuestion}
```
Use `\practiceTestSASection` to insert a divider between MC and short-answer blocks.

## Fun Extras (VMfunExtras.sty)

### Mascot Says (owl speech bubble)
```latex
\mascotSays{Division means fair sharing! Everyone gets the same amount!}
```

### Tip Box (pencil character)
```latex
\tipBox{Line up your numbers by place value!}
```

### Fun Fact
```latex
\begin{funFact}
    The ancient Egyptians were adding numbers over 4,000 years ago!
\end{funFact}
```

### Warning Box (common mistakes)
```latex
\begin{warningBox}                    % default "Watch Out!"
\begin{warningBox}[Common Mistake!]   % custom title
    Don't forget to carry the 1!
\end{warningBox}
```

### Think About It
```latex
\begin{thinkAboutIt}
    Why does $5 \times 6$ give the same answer as $6 \times 5$?
\end{thinkAboutIt}
```

### Real World Connection
```latex
\begin{realWorld}
    We use division when sharing pizza equally!
\end{realWorld}
```

### Story Problem
```latex
\begin{storyProblem}{At the Bakery}
    Word problem in a real-world scene...
\end{storyProblem}
```

### Encouragement Banner
```latex
\encouragement{Great work --- you've mastered the basics!}
```
Yellow banner. Use at the end of most topics.

### Did You Know
```latex
\didYouKnow{Zero is neither odd nor even!}
```

### Conversation Bubbles
```latex
\sayLeft{Owl}{I have 12 cookies!}
\sayRight{You}{How do we share them?}
```

### Summary Box
```latex
\begin{summaryBox}
\begin{itemize}
    \item Key point 1
    \item Key point 2
\end{itemize}
\end{summaryBox}
```

### Riddle Box (math riddle / brain teaser)
```latex
\begin{riddleBox}                           % default "Math Riddle"
\begin{riddleBox}{Can You Guess?}           % custom title
    I am a number less than $20$. I am odd.
    If you multiply my digits, you get $15$.
    What number am I? \answerBlank
\end{riddleBox}
```
Pink box with magic wand icon. Perfect for brain teasers, number riddles, and "Who am I?" puzzles. Sprinkle these throughout topics for engagement.

### Activity Box (hands-on / manipulatives)
```latex
\begin{activityBox}{Build It!}              % custom title
\begin{activityBox}                         % default "Activity"
    Get 12 blocks. Can you arrange them into 3 equal rows?
    How many are in each row? \answerBlank
\end{activityBox}
```
Orange box with pointing-hand icon and dashed bottom border. For activities that require physical objects: blocks, coins, rulers, cards, dice. Encourages kinesthetic learning.

## Math Visuals (VMfunMath.sty)

### Column Addition
```latex
\columnAdd{347}{285}                      % no answer
\columnAddFull{347}{285}{11}{632}         % with carries and answer
\columnAddWork{358}{467}                  % blank workspace for student
```

### Column Subtraction
```latex
\columnSub{532}{275}                      % no answer
\columnSubFull{532}{275}{257}             % with answer shown
\columnSubWork{600}{347}                  % blank workspace for student
\columnSubWorkFour{7246}{3589}            % 4-digit subtraction workspace
```

### Place Value
```latex
\placeValueTable{3}{4}{7}                % single number H-T-O
\placeValueAdd{3}{4}{7}{2}{8}{5}         % two-row addition chart
```

### Number Line
```latex
\numberLine{0}{10}          % 0 to 10, step 1
\numberLine[5]{0}{50}       % 0 to 50, step 5
```

### Dot Groups / Equal Sharing
```latex
\dotGroups{3}{4}                  % 3 groups of 4 dots (orange)
\dotGroups[funBlue]{4}{5}         % custom color
\equalSharing{12}{3}              % 12 shared among 3
\equalSharing[funBlue]{20}{4}     % custom color
```

### Array Grid (rows x columns for multiplication)
```latex
\arrayGrid{3}{4}                  % 3 rows, 4 columns (blue)
\arrayGrid[funGreen]{5}{2}        % custom color
```
Draws a neat grid of colored squares. More structured than `\dotGroups` — clearly shows rows x columns with labels. Ideal for teaching multiplication as area/arrays.

### Number Bond (part-part-whole)
```latex
\numberBond{12}{7}{5}             % 12 = 7 + 5  (all filled in)
\numberBond{12}{7}{}              % 12 = 7 + ?   (blank right part)
\numberBond{12}{}{5}              % 12 = ? + 5   (blank left part)
\numberBond[funGreen]{15}{8}{7}   % custom color
```
Draws three circles in a triangle: whole on top, two parts on bottom, with connecting lines. Essential for addition/subtraction fact relationships.

### Fraction Visuals
```latex
\fractionBar{3}{4}                % bar: 3 of 4 shaded
\fractionBar[funGreen]{2}{6}      % custom color
\fractionCircle{1}{4}             % pie: 1 of 4 shaded
```

### Fact Family Triangle
```latex
\factFamily{3}{4}{12}
```

### Bar Graph (vertical bar chart)
```latex
\barGraph{Favorite Fruits}{Apple/5,Banana/3,Orange/7,Grape/2}{8}
\barGraph[funGreen]{Pet Survey}{Dog/6,Cat/4,Fish/2,Bird/3}{7}
```
Draws a vertical bar chart with Y-axis labels and colored bars. Essential for Ch 6 (Data & Graphs). Arguments: `{title}{label/value pairs}{max Y value}`. Optional color parameter changes bar color.

### Area Grid (unit squares for measuring area)
```latex
\areaGrid{3}{5}                   % 3 rows × 5 columns
\areaGrid[funGreen]{4}{6}         % custom color
```
Draws a contiguous grid of unit squares with outer border and "1 unit" label. Different from `\arrayGrid` — this is specifically for area measurement (Ch 7). Shows true unit-square tiling.

### Perimeter Rectangle (labeled sides)
```latex
\perimeterRect{8}{5}{cm}          % 8cm × 5cm rectangle
\perimeterRect[funGreen]{6}{3}{in} % custom color
```
Draws a rectangle with all four sides labeled with their lengths. Corner dots mark vertices. Essential for perimeter problems (Ch 7).

### Skip Counting Arcs (number line with hop arcs)
```latex
\skipCountArc{0}{30}{5}           % skip count by 5 from 0 to 30
\skipCountArc[funGreen]{0}{20}{4} % custom color
```
Number line with colored arcs showing each skip counting jump, labeled with "+step". Perfect for teaching multiplication as repeated addition. Great visual for skip counting fluency.

### Fraction Number Line (0 to 1 with fraction labels)
```latex
\numberLineFraction{4}            % 0 to 1 divided into fourths
\numberLineFraction[funGreen]{6}  % custom color, sixths
```
Draws a number line from 0 to 1 with tick marks and fraction labels at each division point. Essential for Ch 4 (Fractions on a Number Line).

### Other Visuals
```latex
\tallyMarks{7}                   % draws |||||  ||
\coin{25c}                       % coin circle
\clockFace{3}{30}                % analog clock showing 3:30
\baseTenBlocks{2}{3}{5}          % 2 flats, 3 rods, 5 units
\funCompare{5}{>}{3}             % visual comparison
\ruler{6}{inches}                % measurement ruler
\multFact{3}{4}{12}              % inline multiplication fact box
```

## Color Names for Optional Parameters

`funBlue`, `funGreen`, `funOrange`, `funPurple`, `funRed`, `funYellow`, `funTeal`, `funPink` and their `Dark`/`Light` variants (e.g. `funBlueDark`, `funBlueLight`).

## Answer Key Commands (VMfunAnswers.sty)

Answers are hidden by default and shown with the `showanswers` class option. Place answers **immediately after** each problem.

```latex
% Simple answer (most common)
\prob $3 \times 4 = $ \answerBlank[2cm]
\answer{$12$}

% Answer with explanation (for word/challenge problems)
\wordProblem{Sam has $5$ bags with $3$ apples each. How many apples?}{apples}
\answerExplain{$15$ apples}{$5 \times 3 = 15$}

% True/False answer
\trueOrFalse{$5 + 3 = 8$}
\answerTF{True}

% Multiple choice answer
\multiChoice{What is $12 \div 3$?}{2}{3}{4}{6}
\answerMC{C}
```

Answer key infrastructure commands (used in `study_guide_main.tex`, not in topics):
```latex
\printAnswerKey                  % renders the full answer key at end of book
\enablePracticeTestAnswers       % activates practice-test answer collection mode
\enableQuizAnswers               % activates per-quiz answer grouping mode
\enableDayAnswers                % activates day-based answer grouping mode
\writeAnsDay{1}{Topic Title}     % inserts day marker in answer stream
\writeAnsQuiz{1}{Quiz Title}     % inserts quiz marker in answer stream
```

## Day-Based Environments (VMfunDays.sty)

Used exclusively in the "Math in 30 Days" book type (`topics_in30days/`). These environments use an orange color scheme and day-based structure rather than the standard topic title/learning goals flow.

### Day Page Header
```latex
\dayPage{1}{Multiplication as a Comparison}{Understand and solve multiplicative comparison problems}
```
Full-page orange header with day number circle, title, and goals summary. One per day file, placed at the very top.

### Today's Goals
```latex
\begin{todaysGoals}
\begin{itemize}
    \item Understand what "times as many" means
    \item Write and solve multiplicative comparison equations
\end{itemize}
\end{todaysGoals}
```
Orange goal box with bullseye icon. Placed right after `\dayPage`.

### Quick Lesson
```latex
\begin{quickLesson}{Place Value Basics}    % custom title
\begin{quickLesson}                         % default: "Key Concept"
```
Orange teaching box for concise concept explanations. Equivalent of `conceptBox` but styled for the 30-day format.

### Daily Practice
```latex
\begin{dailyPractice}{Practice Time!}       % custom title
\begin{dailyPractice}                        % default title
\resetProblems
% problems here...
\end{dailyPractice}
```
Practice section with pencil icon. Use `\resetProblems` inside.

### Daily Challenge
```latex
\begin{dailyChallenge}{Brain Buster!}       % custom title
\begin{dailyChallenge}                       % default: "Daily Challenge!"
```
Purple challenge box with trophy icon for harder problems.

### Bonus Lesson
```latex
\begin{bonusLesson}{Place Value: Ten-Thousands}
% condensed teaching content for state-specific bonus topics
\end{bonusLesson}
```
Teal box with star icon for state-specific additional content. Used in `topics_in30days_additional/` files.

### Day Complete
```latex
\dayComplete
```
End-of-day celebration banner with checkmark. Place at the very end of each day file.

### Day Topic Separator
```latex
\dayTopic{Comparing Numbers}
```
Orange divider banner used in double-topic days to visually separate the two topics.

### Key Takeaway
```latex
\keyTakeaway{Every digit's value depends on its \textbf{position} in the number!}
```
Inline highlight box with lightbulb icon for key concepts.

### Minute Timer
```latex
\minuteTimer{5}
```
Small inline badge showing "5 min" with clock icon. Used to suggest time targets for practice sections.

### Progress Tracker
```latex
\progressTracker
```
A visual 30-day progress grid that students can color in. Typically placed in initial pages.

### Weekly Review (deprecated)
```latex
\begin{weeklyReview}[Week 1 Review]
% review content
\end{weeklyReview}
```
Blue review box. Defined in VMfunDays.sty but **not used** in the current 30-day curriculum plan (all 30 days are teaching days).

**Note:** Day files also use shared environments from other packages (e.g., `conceptBox`, `workedExample`, `mascotSays`, `\prob`, `\answer`, etc.). VMfunDays environments add the day-based structure on top.

## Step-by-Step System (VMfunSteps.sty)

Used for step-by-step book types. These provide a structured "recipe card" approach to teaching procedures.

### Step-by-Step Title Banner
```latex
\stepByStepTitle{Long Division}
```
Large topic banner styled for step-by-step pages.

### Step Goal (objectives box)
```latex
\begin{stepGoal}
\begin{itemize}
    \item Divide multi-digit numbers step by step
    \item Check your answer with multiplication
\end{itemize}
\end{stepGoal}
```
"What You'll Learn" objectives box for step-by-step topics.

### Steps Card (the core procedure)
```latex
\begin{stepsCard}{How to Divide}             % custom title
\begin{stepsCard}                             % default: "The Steps"
    \stepItem{Write the problem in long division format.}
    \stepItem{Divide the first digit.}
    \stepItem{Multiply and subtract.}
    \stepItem{Bring down the next digit.}
    \stepItem{Repeat until done.}
\end{stepsCard}
```
A numbered "recipe card" with color-coded steps. `\stepItem{description}` auto-numbers each step with colored circles.

### Step Example (worked example applying the steps)
```latex
\begin{stepExample}{Divide 156 by 12}
    \stepShow{1} Write: $156 \div 12$ ...
    \stepShow{2} Divide: $15 \div 12 = 1$ ...
    \stepResult{$156 \div 12 = 13$}
\end{stepExample}
```
Use `\stepShow{N}` to label which step you're demonstrating and `\stepResult{answer}` for the final answer display with checkmark.

### Step Try It (guided practice with blanks)
```latex
\begin{stepTryIt}{Now Try: $208 \div 16$}
    \stepShow{1} Write the problem: \answerBlank[4cm]
    \stepShow{2} Divide: \answerBlank[4cm]
\end{stepTryIt}
```
"Your Turn" guided practice where students fill in blanks following the steps.

### Step Practice (independent practice)
```latex
\begin{stepPractice}{Division Practice}       % custom title
\begin{stepPractice}                           % default: blue theme
    \resetProblems
    \stepPracticeHeader{Basic Division}
    \prob $144 \div 12 = $ \answerBlank
    \answer{12}
\end{stepPractice}
```
Independent practice section. Use `\stepPracticeHeader[color]{text}` for subsections.

### Step Vocabulary Box
```latex
\begin{stepVocabBox}{Division Words}          % custom title
\begin{stepVocabBox}                           % default: "Words to Know"
    \vocabItem{Quotient}{The answer to a division problem.}
    \vocabItem{Remainder}{The amount left over.}
\end{stepVocabBox}
```

### Step Utility Commands
```latex
\watchOut{Don't forget to bring down the next digit!}   % common mistake warning
\mascotStepTip{Always estimate first — it saves time!}  % owl tip
\stepReminder{Remember: multiply to check your answer.} % inline reminder
```

## Puzzles & Brain Teasers (VMfunPuzzles.sty)

Puzzle environments for brain teasers, logic puzzles, and math games. Great for engagement.

### Puzzle Page Title
```latex
\puzzlePageTitle{Math Puzzles}
```
Full-width purple banner with puzzle-piece icons.

### Puzzle Goals
```latex
\begin{puzzleGoals}
\begin{itemize}
    \item Practice multiplication facts
    \item Use logical reasoning
\end{itemize}
\end{puzzleGoals}
```
Skills summary box for puzzle pages.

### Puzzle Box (generic container)
```latex
\begin{puzzleBox}{Number Challenge}            % custom title
\begin{puzzleBox}[funTeal]{Logic Time}        % custom color + title
    Any puzzle content...
\end{puzzleBox}
```
General-purpose puzzle container. Default color: purple.

### Mystery Number Box
```latex
\begin{mysteryNumberBox}                       % default: "Mystery Number!"
\begin{mysteryNumberBox}{Who Am I?}            % custom title
    \mysteryClue{I am a two-digit number.}
    \mysteryClue{I am even.}
    \mysteryClue{My digits add up to $7$.}
    \mysteryClue{I am less than $30$.}
    What number am I? \answerBlank
\end{mysteryNumberBox}
```
Magenta-themed box. `\mysteryClue{text}` auto-numbers clues. Use `\resetClues` to reset the counter.

### Odd One Out Box
```latex
\begin{oddOneOutBox}                           % default: "Which Doesn't Belong?"
    \puzzleCircles{12, 15, 20, 18, 24}
    Which number doesn't belong? \answerBlank
    Why? \answerBlank[5cm]
\end{oddOneOutBox}
```
Orange-themed box. `\puzzleCircles[color]{val1,val2,...}` draws numbers in circles.

### Target Number Box
```latex
\begin{targetNumberBox}{Make 24!}              % custom title
\begin{targetNumberBox}[funRed]{Hit the Target!} % custom color
    \targetRing{24}
    Use the numbers $3$, $4$, $6$, $8$ and any operations to make $24$.
    \answerBlank[6cm]
\end{targetNumberBox}
```
Bullseye-themed challenge. `\targetRing[color]{number}` draws the target visual.

### Scramble Box (equation scramble)
```latex
\begin{scrambleBox}                            % default: "Equation Scramble!"
    Arrange these tiles to make a true equation:
    \scrTile{3} \scrTile{+} \scrTile{5} \scrTile{=} \scrTile{8}
\end{scrambleBox}
```
Gold-themed box. `\scrTile{symbol}` creates individual movable-looking tiles.

### Brain Teaser Box
```latex
\begin{brainTeaserBox}                         % default: "Brain Teaser!"
\begin{brainTeaserBox}{Think Hard!}            % custom title
    If $3$ cats catch $3$ mice in $3$ minutes,
    how many cats catch $100$ mice in $100$ minutes?
    \answerBlank
\end{brainTeaserBox}
```
Teal-themed box with brain icon.

### Logic Puzzle Box
```latex
\begin{logicPuzzleBox}                         % default: "Logic Puzzle!"
    Three friends each have a different pet...
\end{logicPuzzleBox}
```
Blue-themed box for deductive reasoning puzzles.

### Math Game Box
```latex
\begin{mathGameBox}                            % default: "Math Game!"
\begin{mathGameBox}{Race to 100}               % custom title
    \gameSupply{2 dice}
    \gameSupply{Paper and pencil}
    Rules: ...
\end{mathGameBox}
```
Green-themed box. `\gameSupply{item}` lists required materials.

### Number Pyramid
```latex
\numberPyramid{3}                  % 3-row pyramid
\pyramidCell{1}{1}{5}              % row 1, col 1, value 5
\pyramidCell{1}{2}{3}              % row 1, col 2, value 3
\pyramidBlank[funBlue]{2}{1}       % blank cell for student to fill
```
TikZ number pyramid where each cell is the sum of the two below it.

### Magic Grid (magic square)
```latex
\magicGrid{3}{15}{2,7,6,9,5,1,4,3,8}   % 3×3, target sum 15
\magicGrid{3}{15}{2,?,6,9,5,?,4,?,8}    % use ? for blanks
```
Draws a magic square grid with the target sum displayed.

### Number Cross
```latex
\numberCross{10}{3}{5}{7}{2}       % center, top, right, bottom, left
```
Cross-shaped number puzzle.

### Puzzle Utility Commands
```latex
\digitCard{7}                      % digit card visual
\digitCard[funBlue]{3}             % custom color
\puzzleHint{Think about factors!}  % inline hint with magnifying glass
\puzzleDifficulty{2}               % 1–3 level difficulty badge
\puzzleSep                         % decorative divider between puzzles
\puzzleComplete                    % "Puzzles Complete" banner
\puzzleAnswer{The answer is 42}    % records answer for puzzle answer key
\printPuzzleAnswers                % renders all puzzle answers (end of book)
```

## Quizzes (VMfunQuiz.sty)

Used for quiz/assessment book types. Provides quiz-specific formatting and question types.

### Quiz Chapter and Page Headers
```latex
\quizChapter{Chapter 3: Expressions}  % chapter-level quiz grouping
\quizPage{Ratios and Rates}           % quiz page banner (starts new page, resets counter)
```

### Quiz Info and Instructions
```latex
\quizInfo[10]                  % name/date/score strip, default total: 8
\quizInstructions              % default 15-min instruction bar
\quizInstructions[Read each question carefully. Show your work.]  % custom
```

### Quiz Questions
```latex
\resetQuiz                     % reset quiz question counter
\quizQ                         % auto-numbered question with indigo badge
    What is $3 \times 7$?
\quizBlank                     % answer underline (default: 3cm)
\quizBlank[5cm]                % custom width
\quizWorkSpace                 % dotted work area (default: 2cm)
\quizWorkSpace[4cm]            % custom height
```

### Quiz Multiple Choice and True/False
```latex
\quizMC{12}{15}{21}{24}        % 2×2 grid of MC options
\quizTF                        % True/False bubble pair
\quizCircle{5}{10}{15}{20}     % circle-bubble MC (works with 2 or 4 options)
```

### Quiz Matching
```latex
\begin{quizMatch}
    \quizMatchRow{$3 \times 4$}{12}
    \quizMatchRow{$5 \times 2$}{10}
    \quizMatchRow{$6 \times 3$}{18}
\end{quizMatch}
```

### Quiz Tables
```latex
\begin{quizTable}{3}            % 3-column equal-width table
    Col 1 & Col 2 & Col 3 \\
    ...
\end{quizTable}
```

### Quiz Visuals
```latex
\quizGroupPic{3}{4}                 % 3 groups of 4 dots
\quizGroupPic[star]{2}{5}           % shapes: dot, star, heart, circle, square, triangle
\quizSentence{+}                    % fill-in equation: ___ + ___ = ___
\quizCompare{15}{23}                % two values with empty circle for >, <, =
\quizAnswerLine{Answer}             % labeled answer line
```

### Quiz Structure Commands
```latex
\quizDivider                   % horizontal divider between question groups
\quizScoreBox                  % end-of-quiz self-assessment box

\begin{bonusChallenge}
    Harder bonus question...
\end{bonusChallenge}
\bonusNote                     % encouraging text for bonus section
```

## Worksheets (VMfunWorksheet.sty)

Standalone printable worksheet environments. Each worksheet type has its own themed box.

### Worksheet Header
```latex
\worksheetHeader{Multiplication Practice}
```
Full-width banner with name/date/score fields. Starts a new page.

### Worksheet Skills
```latex
\begin{worksheetSkills}
\begin{itemize}
    \item Multiply 2-digit by 1-digit numbers
    \item Use the standard algorithm
\end{itemize}
\end{worksheetSkills}
```
Green skills checklist box.

### Speed Drill (timed fluency)
```latex
\begin{speedDrill}                             % default: "Quick Math!"
\begin{speedDrill}{Beat the Clock!}            % custom title
    \timerBadge{3}                             % 3-minute timer badge
    \resetProblems
    \probInline $3 \times 4 = $ \answerBlank[1cm]
    \probInline $5 \times 6 = $ \answerBlank[1cm]
\end{speedDrill}
```
Orange-themed stopwatch box.

### Color by Answer
```latex
\begin{colorByAnswer}                          % default: "Solve & Color!"
    \colorKey{12}{Red}
    \colorKey{15}{Blue}
    \colorKey{18}{Green}
    Solve each problem, then color the matching region!
\end{colorByAnswer}
```
Pink-themed art activity. `\colorKey{answer}{color name}` builds the legend.

### Match It (worksheet matching)
```latex
\begin{matchIt}                                % default: "Match the Pairs!"
    \matchRow{$3 \times 4$}{12}
    \matchRow{$5 \times 2$}{10}
\end{matchIt}
```
Blue-themed matching. `\matchRow{left}{right}` draws a dotted line between items.

### Math Maze
```latex
\begin{mathMaze}                               % default: "Math Maze!"
    Start → \mazeChoice{$12$} or \mazeChoice[funRed]{$15$}?
\end{mathMaze}
```
Green-themed maze. `\mazeChoice[color]{value}` creates branching choice bubbles.

### Error Detective
```latex
\begin{errorDetective}                         % default: "Error Detective!"
    \errorWork{$24 \div 6 = 3$}
    What's wrong? \answerBlank[4cm]
    Fix it: \answerBlank[3cm]
\end{errorDetective}
```
Red-themed find-the-mistake. `\errorWork{wrong work}` highlights the incorrect work.

### Sort & Cut
```latex
\begin{sortCut}                                % default: "Cut & Sort!"
    Cut out these cards and sort them:
    \cutCard{$\frac{1}{2}$}
    \cutCard{$0.75$}
    \cutCard{$\frac{3}{4}$}

    \wsSortBin{Less than $\frac{1}{2}$}
    \wsSortBin[funBlue]{Equal to or greater than $\frac{1}{2}$}
\end{sortCut}
```
Orange-themed cut-out activity. `\cutCard{content}` creates dashed-border cards. `\wsSortBin[color]{label}` creates labeled sorting bins.

### Math Scenario (real-world)
```latex
\begin{mathScenario}                           % default: "Real-World Math!"
    You're planning a pizza party for 24 people...
    \scenarioItem{Pizza}{How many pizzas?}
    \scenarioItem{Drinks}{How many bottles?}
\end{mathScenario}
```
Teal-themed scenario box. `\scenarioItem{item}{question}` adds sub-questions.

### Draw & Solve
```latex
\begin{drawSolve}                              % default: "Draw & Solve!"
    Draw a picture to solve: $3 \times 4$
    \drawSpace                                 % default: 4cm
    \drawSpace[6cm]                            % custom height
    Answer: \answerBlank
\end{drawSolve}
```
Purple-themed drawing activity. `\drawSpace[height]` provides empty bordered area.

### Input/Output (function machine)
```latex
\begin{inputOutput}                            % default: "What's the Rule?"
    % Use tabular or fillTable inside
\end{inputOutput}
```
Teal-themed pattern table wrapper.

### Explain It (math journal)
```latex
\begin{explainIt}                              % default: "Explain Your Thinking!"
    Why does $5 \times 0 = 0$? Explain in your own words.
    \writeLines{4}                             % 4 ruled lines for writing
\end{explainIt}
```
Blue-themed writing prompt. `\writeLines{count}` creates ruled lines.

### Circle It
```latex
\begin{circleIt}                               % default: "Circle the Answer!"
    Circle all the prime numbers:
    \numberBubbles{2, 4, 7, 9, 11, 15, 13, 20}
\end{circleIt}
```
Pink-themed circling activity. `\numberBubbles[color]{values}` draws numbers in circles.

### Worksheet Utility Commands
```latex
\drawBox{3cm}                  % empty bordered drawing area
\answerLines{5}                % 5 blank ruled answer lines
\timerBadge{5}                 % inline "5 min" timer badge
\worksheetSep                  % decorative divider between sections
\worksheetDone                 % "Worksheets Complete" banner
\worksheetAnswer{42}           % records answer for worksheet answer key
\printWorksheetAnswers         % renders worksheet answer key (end of book)
```

## Colors & Icons (VMfunColors.sty)

### Color Palette
**Primary:** `funBlue`, `funBlueDark`, `funBlueLight`
**Teaching:** `funGreen`, `funGreenDark`, `funGreenLight`
**Examples:** `funOrange`, `funOrangeDark`, `funOrangeLight`
**Challenge:** `funPurple`, `funPurpleDark`, `funPurpleLight`
**Warning:** `funRed`, `funRedDark`, `funRedLight`
**Tips:** `funYellow`, `funYellowDark`, `funYellowLight`
**Vocabulary:** `funTeal`, `funTealDark`, `funTealLight`
**Fun Facts:** `funPink`, `funPinkDark`, `funPinkLight`
**Neutral:** `funGray`, `funGrayLight`, `funGrayDark`, `funCream`
**Steps:** `stepOne` (green), `stepTwo` (blue), `stepThree` (red), `stepFour` (orange), `stepFive` (purple)
**Place Value:** `pvOnes`, `pvTens`, `pvHundreds`, `pvThousands`

### Icon Commands
All icons accept an optional `[size]` parameter:
```latex
\iconStar        \iconPencil     \iconOwl         \iconLightbulb
\iconTrophy      \iconWarning    \iconBook         \iconBrain
\iconCheck       \iconExclamation \iconRocket      \iconGlobe
\iconTarget      \iconWritingPencil \iconHeart     \iconMedal
\iconMagnifier   \iconSort       \iconPattern
\stepCircle{3}{stepThree}        % colored number circle
```
