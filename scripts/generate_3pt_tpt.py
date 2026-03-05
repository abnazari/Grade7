#!/usr/bin/env python3
"""Generate 50 unique TPT product descriptions for 3_practice_tests (Grade 7 Math).

Each state gets a genuinely unique description through varied:
- Section ordering
- Heading text
- Prose templates
- Chapter presentation (table vs list)
- Opening and CTA styles
"""

import os
from datetime import date

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TODAY = date.today().isoformat()  # e.g. "2026-03-05"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "final_output", "3_practice_tests")

CHAPTER_NAMES = [
    "Ratios and Proportional Relationships",
    "Percents in Everyday Life",
    "Operations with Rational Numbers",
    "Algebraic Expressions",
    "Equations and Inequalities",
    "Scale Drawings, Geometric Figures, and Angle Relationships",
    "Circles, Area, Surface Area, and Volume",
    "Statistics: Sampling and Comparing Populations",
    "Probability and Compound Events",
]

FOOTER = """★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

<p>
  Looking for more <b>Grade 7 Math</b> resources? Visit my
  <a href="https://www.teacherspayteachers.com/store/viewmath" target="_blank"><b>TPT store</b></a>
  for engaging, classroom-ready materials from <b>View Math</b> — a math education company dedicated to helping students succeed.
</p>

<p>
  Explore more teaching tools and learning materials at
  <a href="https://www.viewmath.com" target="_blank"><b>ViewMath.com</b></a>.
</p>

<p>
  Questions or suggestions? Reach out at
  <a href="mailto:dr.nazari@viewmath.com">dr.nazari@viewmath.com</a>.
</p>

<p>
  <b>Follow me</b> to catch new releases — all <b>50% off</b> for the first 24 hours!
</p>

<p>
  <b>– Dr. A. Nazari</b>
</p>"""

# ---------------------------------------------------------------------------
# State data  (slug -> dict)
# ---------------------------------------------------------------------------
# Default chapters for 43 states: [6,7,8,6,6,6,6,4,7] = 56 topics
DEFAULT_CHAPTERS = [6, 7, 8, 6, 6, 6, 6, 4, 7]

STATES = [
    ("alabama",        "Alabama",        "ACAP",              56, DEFAULT_CHAPTERS,              "3 Alabama ACAP Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("alaska",         "Alaska",         "AK STAR",           58, [6,7,9,6,6,6,6,5,7],          "3 Alaska AK STAR Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("arizona",        "Arizona",        "AASA",              56, DEFAULT_CHAPTERS,              "3 Arizona AASA Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("arkansas",       "Arkansas",       "ATLAS",             56, DEFAULT_CHAPTERS,              "3 Arkansas ATLAS Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("california",     "California",     "CAASPP",            56, DEFAULT_CHAPTERS,              "3 California CAASPP Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("colorado",       "Colorado",       "CMAS",              56, DEFAULT_CHAPTERS,              "3 Colorado CMAS Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("connecticut",    "Connecticut",    "SBAC",              56, DEFAULT_CHAPTERS,              "3 Connecticut SBAC Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("delaware",       "Delaware",       "DeSSA",             56, DEFAULT_CHAPTERS,              "3 Delaware DeSSA Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("florida",        "Florida",        "FAST",              60, [6,7,8,7,6,6,7,6,7],          "3 Florida FAST Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("georgia",        "Georgia",        "Georgia Milestones",56, DEFAULT_CHAPTERS,              "3 Georgia Georgia Milestones Grade 7 Math Practice Tests: Answers & Explanations"),
    ("hawaii",         "Hawaii",         "SBA",               56, DEFAULT_CHAPTERS,              "3 Hawaii SBA Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("idaho",          "Idaho",          "ISAT",              56, DEFAULT_CHAPTERS,              "3 Idaho ISAT Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("illinois",       "Illinois",       "IAR",               56, DEFAULT_CHAPTERS,              "3 Illinois IAR Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("indiana",        "Indiana",        "ILEARN",            58, [6,7,8,6,6,7,6,5,7],          "3 Indiana ILEARN Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("iowa",           "Iowa",           "ISASP",             56, DEFAULT_CHAPTERS,              "3 Iowa ISASP Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("kansas",         "Kansas",         "KAP",               56, DEFAULT_CHAPTERS,              "3 Kansas KAP Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("kentucky",       "Kentucky",       "KSA",               56, DEFAULT_CHAPTERS,              "3 Kentucky KSA Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("louisiana",      "Louisiana",      "LEAP 2025",         56, DEFAULT_CHAPTERS,              "3 Louisiana LEAP 2025 Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("maine",          "Maine",          "MTYA",              56, DEFAULT_CHAPTERS,              "3 Maine MTYA Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("maryland",       "Maryland",       "MCAP",              56, DEFAULT_CHAPTERS,              "3 Maryland MCAP Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("massachusetts",  "Massachusetts",  "MCAS",              56, DEFAULT_CHAPTERS,              "3 Massachusetts MCAS Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("michigan",       "Michigan",       "M-STEP",            56, DEFAULT_CHAPTERS,              "3 Michigan M-STEP Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("minnesota",      "Minnesota",      "MCA",               58, [6,8,8,6,6,6,6,5,7],          "3 Minnesota MCA Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("mississippi",    "Mississippi",    "MAAP",              56, DEFAULT_CHAPTERS,              "3 Mississippi MAAP Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("missouri",       "Missouri",       "MAP",               56, DEFAULT_CHAPTERS,              "3 Missouri MAP Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("montana",        "Montana",        "MontCAS",           56, DEFAULT_CHAPTERS,              "3 Montana MontCAS Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("nebraska",       "Nebraska",       "NSCAS",             56, DEFAULT_CHAPTERS,              "3 Nebraska NSCAS Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("nevada",         "Nevada",         "SBAC",              56, DEFAULT_CHAPTERS,              "3 Nevada SBAC Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("new-hampshire",  "New Hampshire",  "NH SAS",            56, DEFAULT_CHAPTERS,              "3 New Hampshire NH SAS Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("new-jersey",     "New Jersey",     "NJSLA",             56, DEFAULT_CHAPTERS,              "3 New Jersey NJSLA Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("new-mexico",     "New Mexico",     "NM-MSSA",           56, DEFAULT_CHAPTERS,              "3 New Mexico NM-MSSA Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("new-york",       "New York",       "NYS Math Test",     56, DEFAULT_CHAPTERS,              "3 New York NYS Math Test Grade 7 Math Practice Tests: Answers & Explanations"),
    ("north-carolina", "North Carolina", "NC EOG",            56, DEFAULT_CHAPTERS,              "3 North Carolina NC EOG Grade 7 Math Practice Tests: Answers & Explanations"),
    ("north-dakota",   "North Dakota",   "NDSA",              56, DEFAULT_CHAPTERS,              "3 North Dakota NDSA Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("ohio",           "Ohio",           "OST",               56, DEFAULT_CHAPTERS,              "3 Ohio OST Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("oklahoma",       "Oklahoma",       "OSTP",              60, [7,8,8,6,6,6,6,6,7],          "3 Oklahoma OSTP Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("oregon",         "Oregon",         "OSAS",              56, DEFAULT_CHAPTERS,              "3 Oregon OSAS Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("pennsylvania",   "Pennsylvania",   "PSSA",              56, DEFAULT_CHAPTERS,              "3 Pennsylvania PSSA Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("rhode-island",   "Rhode Island",   "RICAS",             56, DEFAULT_CHAPTERS,              "3 Rhode Island RICAS Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("south-carolina", "South Carolina", "SC READY",          56, DEFAULT_CHAPTERS,              "3 South Carolina SC READY Grade 7 Math Practice Tests: Answers & Explanations"),
    ("south-dakota",   "South Dakota",   "SBA",               56, DEFAULT_CHAPTERS,              "3 South Dakota SBA Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("tennessee",      "Tennessee",      "TCAP",              56, DEFAULT_CHAPTERS,              "3 Tennessee TCAP Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("texas",          "Texas",          "STAAR",             62, [6,10,8,6,6,7,6,6,7],         "3 Texas STAAR Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("utah",           "Utah",           "RISE",              56, DEFAULT_CHAPTERS,              "3 Utah RISE Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("vermont",        "Vermont",        "SBAC",              56, DEFAULT_CHAPTERS,              "3 Vermont SBAC Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("virginia",       "Virginia",       "SOL",               64, [6,7,10,7,6,8,7,6,7],         "3 Virginia SOL Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("washington",     "Washington",     "SBA",               56, DEFAULT_CHAPTERS,              "3 Washington SBA Grade 7 Math Practice Tests: Test Prep with Answer Explanations"),
    ("west-virginia",  "West Virginia",  "WVGSA",             56, DEFAULT_CHAPTERS,              "3 West Virginia WVGSA Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
    ("wisconsin",      "Wisconsin",      "Forward Exam",      56, DEFAULT_CHAPTERS,              "3 Wisconsin Forward Exam Grade 7 Math Practice Tests: Answers & Explanations"),
    ("wyoming",        "Wyoming",        "WY-TOPP",           56, DEFAULT_CHAPTERS,              "3 Wyoming WY-TOPP Grade 7 Math Practice Tests: Test Prep & Detailed Answers"),
]

# ---------------------------------------------------------------------------
# Section-ordering templates  (10 patterns, each used ~5 times)
# "features", "chapters", "state", "use_cases", "series"
# ---------------------------------------------------------------------------
SECTION_ORDERS = [
    ["features", "chapters", "state", "use_cases", "series"],
    ["state", "features", "chapters", "use_cases", "series"],
    ["use_cases", "state", "features", "chapters", "series"],
    ["chapters", "features", "state", "series", "use_cases"],
    ["features", "state", "use_cases", "chapters", "series"],
    ["state", "chapters", "features", "series", "use_cases"],
    ["use_cases", "features", "chapters", "state", "series"],
    ["chapters", "state", "use_cases", "features", "series"],
    ["features", "use_cases", "chapters", "state", "series"],
    ["state", "use_cases", "features", "series", "chapters"],
]

# ---------------------------------------------------------------------------
# Opening bold headings — 50 unique templates
# Placeholders: {state}, {exam}, {topics}
# ---------------------------------------------------------------------------
OPENING_HEADINGS = [
    "3 Full-Length {exam} Practice Tests for {state} — 90 Questions, Step-by-Step Answers",
    "Grade 7 Math Test Prep for {state}: 3 Complete {exam} Practice Tests",
    "{state} {exam} Prep — 3 Practice Tests With 90 Fully Explained Questions",
    "3 Practice Tests for the {state} {exam}: Every Answer Explained",
    "90 Questions, 3 Tests, All Answers — {state} {exam} Grade 7 Math",
    "Get {state} Students Ready: 3 Full {exam} Practice Tests",
    "{state} Grade 7 Math — 3 Complete Practice Tests With Detailed Answers",
    "Three {exam} Practice Tests for {state}: 90 Questions, 90 Explanations",
    "{exam} Test Prep for {state} — 3 Realistic Grade 7 Math Practice Tests",
    "3 {exam} Practice Tests for {state} Grade 7 Math — Full Answer Key Included",
    "Every Answer Explained: 3 Full {exam} Tests for {state}",
    "{state} {exam} Math Prep: 3 Tests, 30 Questions Each, All Explained",
    "Practice for the {exam}: 3 Grade 7 Math Tests for {state}",
    "3 Tests, 90 Questions, Complete Solutions — {state} {exam} Grade 7",
    "Full Test Prep for {state}: 3 Practice Tests With Step-by-Step Solutions",
    "{state}'s {exam} Doesn't Have to Be a Surprise — 3 Practice Tests",
    "Three Full-Length Grade 7 Math Tests for {state} — All Answers Included",
    "90 Practice Questions for the {state} {exam} — 3 Complete Tests",
    "3 Realistic {exam} Tests for {state} Grade 7 Students",
    "Your {state} Test Prep Starts Here: 3 Practice Tests, 90 Questions",
    "Grade 7 Math for {state}: 3 Full Practice Tests With Solutions",
    "All 90 Questions Explained — 3 {exam} Tests for {state}",
    "Prepare for the {exam}: 3 {state} Grade 7 Math Practice Tests",
    "3 Full Practice Tests for {state}'s Grade 7 Math Exam",
    "Step-by-Step Answers: 3 {exam} Practice Tests for {state}",
    "{state} — 3 Grade 7 Math Practice Tests With Detailed Answers",
    "3 {state} {exam} Tests: 90 Questions, Complete Explanations",
    "The {state} {exam} Practice Pack — 3 Tests, 90 Questions",
    "Give Your Students 3 Full {exam} Practice Tests — {state} Grade 7",
    "{state} Students Get 3 Full Practice Tests — 90 Questions Total",
    "Test Day Ready: 3 {exam} Practice Tests for {state}",
    "Three Chances to Practice: {state} {exam} Grade 7 Math",
    "Built for {state}: 3 Complete {exam} Practice Tests",
    "3 Tests × 30 Questions = 90 Practice Problems for {state}",
    "{state} {exam} — 3 Full-Length Grade 7 Math Tests to Practice",
    "Ninety Practice Questions for {state}: 3 Full {exam} Tests",
    "Real {exam} Practice: 3 Complete Tests for {state} Grade 7",
    "3 Complete {state} {exam} Practice Tests — All Answers Explained",
    "{exam} Ready: 3 Practice Tests for {state} Grade 7 Math",
    "Three Practice Tests, Every Answer Explained — {state} {exam}",
    "3 Grade 7 Practice Tests for {state} With Complete Solutions",
    "From Start to Finish: 3 {exam} Practice Tests for {state}",
    "Confidence Builder: 3 Full {exam} Practice Tests for {state}",
    "3 {state} Grade 7 Practice Tests — Answers and Step-by-Step Solutions",
    "{state}'s Guide to the {exam}: 3 Full Practice Tests",
    "All You Need: 3 {exam} Grade 7 Practice Tests for {state}",
    "90 Answered Questions — 3 {state} {exam} Practice Tests",
    "Practice for {state}'s {exam}: 3 Tests, Full Explanations",
    "3 Full Tests for {state} Grade 7 Math — Detailed Answer Key",
    "{state} + 3 Practice Tests = {exam} Readiness",
]

# ---------------------------------------------------------------------------
# Opening intro sentences — 10 templates (cycle through)
# Placeholders: {title}, {state}, {topics}
# ---------------------------------------------------------------------------
OPENING_INTROS = [
    '<p><b>{title}</b> gives your students three complete practice tests covering all {topics} Grade 7 math topics. Every question comes with a detailed explanation.</p>',
    '<p>Three full-length tests. Ninety questions. Every answer explained step by step. That\'s what <b>{title}</b> delivers for your <b>{state}</b> students.</p>',
    '<p>This resource gives your <b>{state}</b> students 90 practice questions across 3 full tests, with step-by-step solutions for every one. <b>{title}</b> covers all {topics} topics in the Grade 7 math curriculum.</p>',
    '<p>90 questions. 3 complete tests. Detailed answers for every problem. <b>{title}</b> is built specifically for <b>{state}</b> Grade 7 math.</p>',
    '<p>Your students get 3 complete practice tests — 90 questions total — with every answer broken down and explained. <b>{title}</b> covers all {topics} Grade 7 math topics for <b>{state}</b>.</p>',
    '<p>Three tests, 90 questions, all answers explained. <b>{title}</b> is the test prep resource your <b>{state}</b> students need for Grade 7 math.</p>',
    '<p>Here\'s a straightforward way to practice Grade 7 math: 3 full-length tests with 90 total questions and complete solutions. <b>{title}</b> is written for <b>{state}</b>.</p>',
    '<p><b>{title}</b> — 3 tests, 90 questions, every answer explained step by step. Designed to match <b>{state}</b>\'s specific Grade 7 math curriculum.</p>',
    '<p>Realistic test prep for <b>{state}</b> — 3 tests, 90 questions, every answer explained step by step. <b>{title}</b> covers all {topics} topics your students need.</p>',
    '<p><b>{title}</b> delivers exactly what the name says: three full practice tests with 90 questions, all answered and explained for <b>{state}</b> Grade 7 math.</p>',
]

# ---------------------------------------------------------------------------
# Feature headings — 50 unique
# ---------------------------------------------------------------------------
FEATURE_HEADINGS = [
    "What's Inside",
    "Here's What You Get",
    "What Your Students Get",
    "A Quick Look Inside",
    "Here's What's Included",
    "What You'll Find",
    "Inside This Resource",
    "Everything Included",
    "Here's the Rundown",
    "What's in the Box",
    "The Details",
    "What Makes This Different",
    "Here's What You're Getting",
    "Included in Every Test",
    "What Your {state} Students Get",
    "Quick Overview",
    "At a Glance",
    "Features That Matter",
    "Here's the Full Picture",
    "What to Expect",
    "Why This Works",
    "The Essentials",
    "Built-In Features",
    "Everything Your Students Need",
    "Here's What's Inside",
    "A Closer Look",
    "What This Covers",
    "What You're Working With",
    "Packed With",
    "Key Features",
    "What Sets This Apart",
    "The Good Stuff",
    "Inside These 3 Tests",
    "Details at a Glance",
    "Features for {state}",
    "What's Waiting Inside",
    "A Look at What's Included",
    "Highlights",
    "Here's the Breakdown",
    "Everything in One Place",
    "Designed With Purpose",
    "Inside the Tests",
    "Here's What Makes It Work",
    "Your Students Will Get",
    "Let's Talk Features",
    "What Comes With It",
    "Resource Details",
    "Three Tests, Loaded With",
    "What We've Built In",
    "All the Features",
]

# ---------------------------------------------------------------------------
# Feature bullet pools — 10 phrasings per feature, pick by (idx % 10)
# ---------------------------------------------------------------------------
FEAT_90Q = [
    "3 full practice tests — 30 questions each, 90 total — with complete answer explanations",
    "Three tests × 30 questions = 90 problems, every one with a full explanation",
    "90 Grade 7 math questions across 3 complete practice tests, all with step-by-step answers",
    "Three complete practice tests, 30 questions each, all 90 answered and explained",
    "3 tests, 30 questions per test, 90 problems total — and every answer is explained",
    "Ninety practice questions spread across 3 full-length tests, each with detailed solutions",
    "30 questions per test × 3 tests = 90 practice problems with full explanations",
    "Three full-length tests with 90 total questions — every single answer explained",
    "All 90 questions across 3 tests come with complete, worked-out solutions",
    "3 realistic practice tests, each with 30 questions, totaling 90 fully explained problems",
]

FEAT_FORMATS = [
    "Includes multiple-choice, short-answer, and extended-response questions",
    "Multiple-choice, short-answer, and extended-response formats — just like the real test",
    "Question types match the real state exam: multiple-choice, short-answer, and extended response",
    "Mirrors the actual test format with multiple-choice, short-answer, and open-ended questions",
    "Same question formats students will face on test day: MC, short-answer, and extended response",
    "A mix of multiple-choice, short-answer, and extended-response questions",
    "Every test includes the same question types as the real exam",
    "Multiple-choice, short-answer, and open-ended questions — all the formats students will see",
    "Real exam formats: multiple-choice, short-answer, and extended response",
    "Question types match what students will actually encounter on test day",
]

FEAT_EXPLANATIONS = [
    "Every answer comes with a detailed step-by-step explanation",
    "Detailed explanations walk students through every question, step by step",
    "Step-by-step answer explanations so students learn from every problem",
    "Full, detailed explanations for each of the 90 questions",
    "Every answer is explained — students don't just check right or wrong, they learn why",
    "Complete worked-out solutions for all 90 problems",
    "Each answer explanation breaks the problem down step by step",
    "Detailed solutions that show the reasoning behind every answer",
    "Every problem comes with a full explanation — not just the answer, but the process",
    "Step-by-step breakdowns for all 90 questions so students understand the method",
]

FEAT_SCORE = [
    "Score tracking sheets so students can measure their progress across all 3 tests",
    "Built-in score tracking to see improvement from test 1 to test 3",
    "Track scores after each test to watch growth over all 3 attempts",
    "Score tracking included — students can see how much they improve with each test",
    "Each test has a scoring section so students can chart their progress",
    "Progress tracking after every test — students see their scores improve over time",
    "Score-tracking pages let students compare results across all 3 tests",
    "Built-in scoring so students (and teachers) can track growth from test to test",
    "Chart progress from the first test to the third with built-in score tracking",
    "Score each test and track improvement across all 3 practice rounds",
]

FEAT_STRANDS = [
    "Covers every Grade 7 math strand: ratios, percents, rational numbers, algebra, geometry, and statistics",
    "All major math strands: ratios and rates, the number system, algebra, geometry, data, and probability",
    "Questions span every strand: proportional reasoning, rational numbers, expressions, geometry, and stats",
    "From ratios to probability — this covers the full Grade 7 math curriculum",
    "Every major area is included: ratios, percents, number operations, algebra, geometry, statistics, and probability",
    "All 9 chapters represented: ratios, percents, rational numbers, algebra, equations, geometry, measurement, statistics, probability",
    "Comprehensive coverage across all math strands — no gaps",
    "Questions pull from every chapter in the Grade 7 curriculum",
    "Ratios, percents, algebra, geometry, statistics, probability — it's all here",
    "Full coverage of Grade 7 math: from ratios and rates through statistics and probability",
]

FEAT_CONDITIONS = [
    "Realistic test-day conditions — timed format, answer grids, and scoring rubrics included",
    "Timed format with answer grids and rubrics to simulate real test conditions",
    "Test-day format: timed, with answer grids and scoring rubrics",
    "Feels like the real thing — timed tests with answer sheets and scoring guides",
    "Simulates actual testing conditions with timed format and answer grids",
    "Answer grids, timing guidelines, and scoring rubrics make this feel like the real test",
    "Designed to replicate real exam conditions: timed, with answer sheets and rubrics",
    "Real test-day experience with answer grids, time limits, and scoring rubrics",
    "Test format matches what students will see: timed, with answer grids",
    "Complete with answer grids and timing guidelines so students can practice under test conditions",
]

FEAT_COLOR = [
    "Colorful pages with illustrations, diagrams, and a friendly owl mascot",
    "Full-color design with illustrations, diagrams, and an engaging owl mascot",
    "Bright, illustrated pages featuring diagrams and a fun owl mascot",
    "Colorful, illustrated pages with diagrams and the View Math owl mascot",
    "Full-color pages packed with helpful diagrams and a friendly owl guide",
    "Engaging design with color illustrations, clear diagrams, and an owl mascot",
    "Professional full-color layout with engaging visuals and a fun owl mascot",
    "Color pages with illustrations and diagrams — plus an owl mascot students love",
    "Vibrant pages with clear diagrams, illustrations, and a friendly owl throughout",
    "Illustrated in full color with helpful diagrams and the View Math owl",
]

FEAT_ANSWERKEY = [
    "Complete answer key with full explanations for every problem",
    "Full answer key — every answer explained in detail",
    "Includes a complete answer key with worked-out explanations",
    "Comprehensive answer key with step-by-step solutions",
    "Answer key with detailed explanations included",
    "Every problem answered and explained in the included answer key",
    "Detailed answer key that explains the solution to every question",
    "Complete answer key with explanations — not just answers, but the reasoning",
    "Full answer key included, with every solution explained",
    "Answer key provides detailed, step-by-step solutions for all questions",
]

FEAT_PRINT = [
    "Print and go — no prep, no assembly, just download and use",
    "Ready to print — download, print, and start immediately",
    "No prep required — just print and hand it out",
    "Download, print, use. That's it. No setup needed",
    "Print-ready — no cutting, no folding, no prep work",
    "Instant use — download and print, no preparation needed",
    "Zero prep required — print it and you're ready to go",
    "Just download and print — it's ready to use as-is",
    "No prep, no assembly — download, print, done",
    "Print-ready format — no extra work on your end",
]

# ---------------------------------------------------------------------------
# Chapter section headings — 50 unique
# ---------------------------------------------------------------------------
CHAPTER_HEADINGS = [
    "All {topics} Topics, Covered",
    "What's Covered",
    "{topics} Topics, 9 Chapters",
    "Here's the Breakdown",
    "{state}'s Full Topic List",
    "Chapter by Chapter",
    "The {topics} Topics at a Glance",
    "What Students Will Practice",
    "Topics Covered in This Book",
    "Inside the 9 Chapters",
    "Here's What's in Each Chapter",
    "Every Chapter, Every Topic",
    "Full Chapter Coverage",
    "{topics} Topics Across 9 Chapters",
    "The Chapters",
    "Here's the Chapter Layout",
    "Topic Coverage",
    "A Look at the 9 Chapters",
    "What These Tests Cover",
    "All {topics} Grade 7 Math Topics",
    "{state} — All Topics Covered",
    "What's Inside Each Chapter",
    "Here's What Students Will See",
    "Complete Topic Breakdown",
    "The Full Picture: 9 Chapters",
    "All 9 Chapters at a Glance",
    "{state}'s Grade 7 Math Chapters",
    "Here's Every Topic",
    "Chapter Coverage",
    "The 9 Chapters",
    "Topics From Every Chapter",
    "Grade 7 Math Breakdown",
    "What Your Students Are Practicing",
    "{topics} Topics, Broken Down",
    "Chapter-by-Chapter Coverage",
    "{state}'s {topics} Topics",
    "From Ratios to Probability",
    "Nine Chapters of Grade 7 Math",
    "Full Math Coverage",
    "What These 3 Tests Cover",
    "Everything That's Tested",
    "Here's How It Breaks Down",
    "Full Chapter Breakdown",
    "Every Topic, Every Chapter",
    "Grade 7 — {topics} Topics Covered",
    "{state}'s Math Topics",
    "Here's the Scope",
    "9 Chapters, {topics} Topics",
    "The Entire Curriculum",
    "Covered from Start to Finish",
]

# ---------------------------------------------------------------------------
# State alignment headings — 50 unique
# ---------------------------------------------------------------------------
STATE_HEADINGS = [
    "Made for {state}",
    "Written for {state}",
    "Built Around {state}'s Curriculum",
    "Designed for {state}",
    "Matches {state}'s Standards",
    "Tailored to {state}",
    "{state}-Specific Content",
    "Why It Works for {state}",
    "Aligned to {state}'s Curriculum",
    "This Follows {state}'s Standards",
    "{state}'s Grade 7 Standards, Covered",
    "Built for {state} Students",
    "Specific to {state}",
    "Not Generic — Made for {state}",
    "Made With {state} in Mind",
    "Focused on {state}",
    "Follows {state}'s Math Standards",
    "Created for {state}",
    "For {state} Classrooms",
    "Matches What {state} Teaches",
    "Your {state} Students Deserve This",
    "{state}: This One's for You",
    "Designed Around {state}'s Expectations",
    "{state}-Ready Material",
    "Made Specifically for {state}",
    "This Isn't Generic — It's {state}",
    "{state}'s Standards, Front and Center",
    "Custom-Built for {state}",
    "Based on {state}'s Curriculum",
    "{state}: Aligned and Ready",
    "Written With {state} Standards in Mind",
    "This Matches {state}",
    "Shaped by {state}'s Math Standards",
    "From {state}, for {state}",
    "{state} Standards? Covered",
    "All About {state}",
    "Tuned to {state}'s Requirements",
    "{state}'s Math, {state}'s Way",
    "Curriculum Match: {state}",
    "This Is a {state} Book",
    "{state}'s Grade 7 Curriculum, Covered",
    "Specifically for {state}",
    "Targeted to {state}",
    "Mapped to {state}'s Standards",
    "{state} Grade 7 Math, Covered",
    "Aligned With What {state} Expects",
    "Fits {state}'s Curriculum",
    "Built to Match {state}",
    "One Hundred Percent {state}",
    "Rooted in {state}'s Standards",
]

# State alignment prose — 10 templates
STATE_PROSE = [
    '<p>This isn\'t a generic, one-size-fits-all test prep book. It\'s written specifically for <b>{state}</b>\'s Grade 7 math standards. The {topics} topics match what your students are expected to know.</p>',
    '<p>Every question in this resource is built around <b>{state}</b>\'s specific Grade 7 math curriculum. All {topics} topics are covered — nothing extra, nothing missing.</p>',
    '<p>This isn\'t pulled from a national question bank. It\'s designed for <b>{state}</b> students, covering the exact {topics} topics in the state\'s Grade 7 math standards.</p>',
    '<p><b>{state}</b> has its own Grade 7 math standards, and this resource matches them. All {topics} topics are here — the same content your students are learning in class.</p>',
    '<p>Your <b>{state}</b> students aren\'t taking a generic math test. This book matches their specific curriculum — {topics} topics, all aligned to what <b>{state}</b> expects.</p>',
    '<p>This is a <b>{state}</b> resource, not a national one. The {topics} topics covered match <b>{state}</b>\'s Grade 7 math standards from start to finish.</p>',
    '<p>Built from the ground up for <b>{state}</b>. Every one of the {topics} topics aligns with what <b>{state}</b> expects Grade 7 students to know.</p>',
    '<p>The math your <b>{state}</b> students are learning in class is exactly what\'s in these tests. All {topics} Grade 7 topics, aligned to <b>{state}</b>\'s standards.</p>',
    '<p>Not a generic resource. This is written for <b>{state}</b>\'s Grade 7 math curriculum — {topics} topics that match what your students are actually being taught.</p>',
    '<p>Every question reflects <b>{state}</b>\'s Grade 7 math expectations. {topics} topics, 9 chapters, all aligned to the state curriculum.</p>',
]

# ---------------------------------------------------------------------------
# Use cases headings — 50 unique
# ---------------------------------------------------------------------------
USE_CASE_HEADINGS = [
    "Who's This For?",
    "Great For",
    "Works Well For",
    "Perfect Situations",
    "Who'll Get the Most Out of This",
    "Ideal For",
    "Use It For",
    "When to Use This",
    "Who Benefits Most",
    "Made for These Situations",
    "Where This Fits",
    "Best Used For",
    "This Works For",
    "How Teachers Use This",
    "Who Needs This",
    "Designed For",
    "Ways to Use This",
    "Here's Who This Helps",
    "Real-World Uses",
    "Fits Right Into",
    "Who Should Grab This",
    "How to Use It",
    "Situations This Fits",
    "Built for These Students",
    "Use Cases",
    "This Is Great For",
    "Your Students Can Use It For",
    "When Does This Help?",
    "Practical Uses",
    "Effective For",
    "Works Everywhere",
    "Who It's For",
    "Where It Shines",
    "Versatile Enough For",
    "This Fits Perfectly",
    "Helpful For",
    "Useful Everywhere",
    "Who Wants This",
    "How It Helps",
    "Countless Ways to Use It",
    "Works In Any Setting",
    "Great in Many Situations",
    "Grab It If You're",
    "Here's Where It Fits",
    "Classroom and Beyond",
    "From Classroom to Home",
    "Teach, Tutor, or Homeschool",
    "Flexible Enough For",
    "Many Ways to Use This",
    "Who Gets the Most Value",
]

# Use case bullet pools — 10 phrasing sets
USE_CASE_SETS = [
    [
        "Classroom test-prep sessions — one test per week leading up to exam day",
        "Independent homework — students practice on their own and check the answer key",
        "Tutoring sessions — pinpoint gaps and focus on specific skills",
        "Homeschool assessment — gauge Grade 7 math readiness",
        "After-school programs and math camps",
        "Summer review to keep skills sharp before Grade 8",
    ],
    [
        "Weekly classroom practice leading up to test season",
        "Homework packets — students work independently, then check their answers",
        "One-on-one or small-group tutoring to target weak spots",
        "Homeschool families who want a standardized-format assessment",
        "Test-prep boot camps or after-school review sessions",
        "Summer bridge programs to keep math fresh",
    ],
    [
        "Teacher-led test prep — assign one test at a time",
        "Student-driven practice — work through tests independently",
        "Small-group tutoring — identify and address gaps",
        "Homeschool progress checks",
        "After-school math review and enrichment",
        "Summer practice to prevent skill loss",
    ],
    [
        "In-class test prep — hand out a test and let students work through it",
        "At-home practice — students use the answer key to self-correct",
        "Targeted tutoring — find weak areas and drill them",
        "Homeschool benchmarking — see where your student stands",
        "After-school enrichment or math club activities",
        "Pre-Grade 8 summer review",
    ],
    [
        "Whole-class test simulation — use timed format for realism",
        "Independent study — students use the answer key to learn from mistakes",
        "Tutoring tool — diagnose problems and track improvement",
        "Homeschool evaluation — standard test format without the pressure",
        "Math intervention groups or after-school help sessions",
        "Summer skill maintenance before the next grade",
    ],
    [
        "Classroom warm-up or end-of-unit review",
        "Homework — students take a test at home and study the explanations",
        "One-on-one tutoring — zero in on the hardest topics",
        "Homeschool curriculum supplement — standardized-format practice",
        "Extra credit or enrichment for advanced students",
        "Summer prep so students start Grade 8 strong",
    ],
    [
        "Prep sessions leading into state testing week",
        "Self-paced homework — students practice and self-check with the answer key",
        "Small-group review — work through tests together",
        "Homeschool families looking for exam-style assessments",
        "After-school or weekend math study groups",
        "Summer learning to prevent the summer slide",
    ],
    [
        "Weekly test-prep practice in the classroom",
        "Take-home practice tests for independent review",
        "Tutoring resource — use results to create a personalized plan",
        "Homeschool Grade 7 math assessment",
        "Supplementary material for math intervention programs",
        "End-of-year or beginning-of-year math review",
    ],
    [
        "Structured classroom practice — one test per session",
        "Independent practice — students test themselves and review explanations",
        "Diagnostic tool for tutors — find gaps fast",
        "Homeschool milestone check — see if your student is on track",
        "Math camp or enrichment program material",
        "Keep skills sharp over breaks and holidays",
    ],
    [
        "Pre-exam classroom drills — simulate test-day conditions",
        "At-home review — students learn from the detailed answer key",
        "Focused tutoring — use test results to guide instruction",
        "Homeschool readiness check for state-level math",
        "After-school academic support or homework help",
        "Summer practice to bridge Grade 7 and Grade 8",
    ],
]

# ---------------------------------------------------------------------------
# Series cross-sell headings — 50 unique
# ---------------------------------------------------------------------------
SERIES_HEADINGS = [
    "Want More?",
    "Looking for More?",
    "Need Lessons Too?",
    "Check Out the Full Series",
    "More From the {state} Series",
    "Explore the Full Series",
    "Other Books for {state}",
    "The Complete {state} Collection",
    "Keep Going With the {state} Series",
    "Pair This With",
    "Goes Great With",
    "Also Available for {state}",
    "Expand Your Resources",
    "Build the Full Set",
    "Add More to Your Collection",
    "Don't Stop Here",
    "More {state} Grade 7 Math",
    "See the Rest of the Series",
    "The {state} Series Has More",
    "Complete Your {state} Library",
    "What Else Is Available",
    "Students Need More? Try These",
    "Pair It Up",
    "Complement This With",
    "Looking for Something Different?",
    "More Options for {state}",
    "Grow Your Resource Library",
    "The Full {state} Lineup",
    "Other Resources for {state}",
    "There's More Where This Came From",
    "Grab More for {state}",
    "Round Out Your Collection",
    "Other {state} Grade 7 Resources",
    "Mix and Match With",
    "Extend the Learning",
    "Resources That Pair Well",
    "Need Something Else?",
    "Also in the {state} Series",
    "The Whole {state} Set",
    "Additional {state} Resources",
    "Browse the Full Collection",
    "Want the Complete Package?",
    "Here's What Else We Have",
    "Take It Further",
    "Supplement With These",
    "More Grade 7 Math for {state}",
    "Your Next Pick",
    "Ready for More?",
    "Stack More Resources",
    "Keep the Momentum Going",
]

# Series item phrasings — 5 sets of 8 items
SERIES_ITEM_SETS = [
    [
        ("<b>All-in-One</b>", "Full lessons, worked examples, and practice for every topic"),
        ("<b>Study Guide</b>", "Key concepts, essential examples, and quick practice for review"),
        ("<b>Workbook</b>", "Hundreds of practice problems organized by topic"),
        ("<b>Step-by-Step Guide</b>", "Numbered steps for every problem type so students learn at their own pace"),
        ("<b>Math in 30 Days</b>", "The entire curriculum in a 30-day daily lesson plan"),
        ("<b>Quizzes</b>", "Quick 15-minute quizzes for every topic to track progress"),
        ("<b>Puzzles & Brain Teasers</b>", "Games, riddles, and challenges that make math fun"),
        ("<b>Worksheets</b>", "Standalone printable activities for any topic"),
    ],
    [
        ("<b>All-in-One</b>", "Lessons, examples, and practice problems all in one resource"),
        ("<b>Study Guide</b>", "Condensed review with essential examples for every topic"),
        ("<b>Workbook</b>", "Topic-by-topic practice with hundreds of problems"),
        ("<b>Step-by-Step Guide</b>", "Guided solutions that walk students through each problem type"),
        ("<b>Math in 30 Days</b>", "A daily study schedule covering the whole curriculum in one month"),
        ("<b>Quizzes</b>", "15-minute assessments per topic for regular progress checks"),
        ("<b>Puzzles & Brain Teasers</b>", "Fun, standards-aligned math games to keep students engaged"),
        ("<b>Worksheets</b>", "Individual printable worksheets ready for immediate use"),
    ],
    [
        ("<b>All-in-One</b>", "The full package — lessons, examples, and practice for every topic"),
        ("<b>Study Guide</b>", "Quick review of every topic with key concepts and examples"),
        ("<b>Workbook</b>", "Extra practice organized by topic — hundreds of problems"),
        ("<b>Step-by-Step Guide</b>", "Clear, numbered instructions for every type of problem"),
        ("<b>Math in 30 Days</b>", "30 daily lessons covering the whole Grade 7 math curriculum"),
        ("<b>Quizzes</b>", "One quiz per topic — quick, focused, and 15 minutes each"),
        ("<b>Puzzles & Brain Teasers</b>", "Curriculum-aligned puzzles, riddles, and brain teasers"),
        ("<b>Worksheets</b>", "Printable activities by topic — use in any order"),
    ],
    [
        ("<b>All-in-One</b>", "Everything your students need: full lessons, worked examples, and practice"),
        ("<b>Study Guide</b>", "A focused review — key ideas and essential examples for each topic"),
        ("<b>Workbook</b>", "Hundreds of scaffolded problems for targeted practice"),
        ("<b>Step-by-Step Guide</b>", "Step-by-step instructions that let students learn independently"),
        ("<b>Math in 30 Days</b>", "Full curriculum in 30 days — one lesson per day"),
        ("<b>Quizzes</b>", "Track progress topic by topic with short 15-minute quizzes"),
        ("<b>Puzzles & Brain Teasers</b>", "Math puzzles and brain teasers that are actually fun"),
        ("<b>Worksheets</b>", "One worksheet per topic, ready to print and use"),
    ],
    [
        ("<b>All-in-One</b>", "Complete lessons and examples with practice for every Grade 7 math topic"),
        ("<b>Study Guide</b>", "The concise review: key concepts, examples, and quick practice"),
        ("<b>Workbook</b>", "Problem after problem, organized by topic, for extra practice"),
        ("<b>Step-by-Step Guide</b>", "A guided approach — numbered steps make every problem type manageable"),
        ("<b>Math in 30 Days</b>", "Daily lesson plan to cover everything in one month"),
        ("<b>Quizzes</b>", "Quick assessments for every topic, perfect for progress monitoring"),
        ("<b>Puzzles & Brain Teasers</b>", "Games and challenges tied to the curriculum — math that's enjoyable"),
        ("<b>Worksheets</b>", "Stand-alone printables for any topic, any order"),
    ],
]

# ---------------------------------------------------------------------------
# CTA closings — 50 unique (paragraph 1 + paragraph 2)
# ---------------------------------------------------------------------------
CTA_CLOSINGS = [
    ("Three tests. 90 questions. Complete answer explanations. Your {state} students will be ready.",
     "Add this to your cart and give your students the practice they need."),
    ("90 questions of real, focused practice — every answer explained.",
     "Grab this resource and start building confidence today."),
    ("Consistent practice builds confidence. Three tests gets your students there.",
     "Download it now and start prepping your {state} students."),
    ("Your students get 3 full tests to practice with. That's 90 chances to get stronger.",
     "Add it to your collection and let the practice begin."),
    ("Real test prep doesn't have to be complicated. 3 tests, 90 questions, full explanations.",
     "Get this resource today and give your students what they need."),
    ("Three practice tests, all the explanations, zero guesswork.",
     "Click add to cart and start your {state} test prep."),
    ("When your students have practiced 90 questions with full explanations, test day feels different.",
     "Add this to your cart now."),
    ("Practice changes everything. Give your {state} students 3 full tests to work through.",
     "Download this and get started."),
    ("Three tests worth of solid practice. Every answer explained. That's what this delivers.",
     "Grab it today and put your students on the path to success."),
    ("Your {state} students deserve real practice — not worksheets pulled from random sources. This is purpose-built.",
     "Add it to your cart and start preparing."),
    ("Realistic practice for realistic results. 3 tests, 90 questions, complete answers.",
     "Get it now and let your students start practicing."),
    ("The best way to prepare for a math test is to take math tests. Here are 3.",
     "Add this to your cart today."),
    ("Every explanation teaches something. 90 questions means 90 learning opportunities.",
     "Download it and watch your students improve."),
    ("No fluff. No filler. Just 3 solid practice tests with full answer explanations.",
     "Get it for your {state} students today."),
    ("Your students will walk into test day knowing what to expect. 3 practice tests make sure of it.",
     "Click add to cart and give them that edge."),
    ("Three tests. Every answer broken down. That's how you build readiness.",
     "Download this resource and start practicing with your {state} students."),
    ("90 fully explained questions. That's a lot of practice — and a lot of learning.",
     "Add this to your classroom resources today."),
    ("Give your {state} students the repetition they need. 3 complete tests, step-by-step answers.",
     "Get started — add this to your cart."),
    ("Test prep works best when it's realistic. These 3 tests deliver that.",
     "Grab this for your students and start preparing."),
    ("Confidence comes from practice. 90 questions of it.",
     "Add this resource to your cart and start tomorrow."),
    ("Three complete practice tests with answers that actually teach. That's the whole point.",
     "Get this for your {state} classroom now."),
    ("From the first test to the third, your students will get stronger. That's how practice works.",
     "Download today and see the difference."),
    ("90 problems with step-by-step solutions. Simple, focused, effective.",
     "Add it to your cart and let the practice speak for itself."),
    ("Your {state} Grade 7 students will thank you for the practice. Or at least their test scores will.",
     "Get it now."),
    ("Three full tests of real, aligned practice. That's not a lot of pages — but it's a lot of value.",
     "Add this to your cart and start your students' test prep."),
    ("Real practice. Real explanations. Real improvement.",
     "Download this resource for your {state} students today."),
    ("By test 3, your students will know exactly what to expect. That's the power of practice.",
     "Grab this resource and get started."),
    ("Every question. Every answer. Every explanation. All here.",
     "Get this for your {state} classroom and start practicing."),
    ("3 tests might not sound like a lot — but 90 fully explained questions is more practice than most students get.",
     "Add it to your cart now."),
    ("Don't let test day be the first time your students see these types of questions.",
     "Give them 3 full practice tests — add this to your cart today."),
    ("This is straightforward test prep. 3 tests, 90 questions, detailed answers.",
     "Download it now and start prepping."),
    ("Focused, realistic, and explained. That's what these 3 practice tests are.",
     "Get it for your students and start building confidence."),
    ("The more your students practice, the less they'll stress on test day. Start with 3 full tests.",
     "Add this to your cart."),
    ("90 questions across 3 tests — each one a learning opportunity.",
     "Download this resource and put it to work in your {state} classroom."),
    ("Three tests. All answers. All explanations. That's all it takes to make a difference.",
     "Click add to cart."),
    ("Give your {state} students 3 shots at perfecting their Grade 7 math skills.",
     "Get this resource today."),
    ("When students can learn from their mistakes, practice becomes powerful. Every answer is explained.",
     "Add it to your cart and start the process."),
    ("Test prep isn't magic. It's practice. These 3 tests are exactly that.",
     "Download it now."),
    ("Three tests' worth of practice, with nothing left unexplained.",
     "Grab this for your {state} students today."),
    ("Ninety questions. Step-by-step answers. Built for {state}. What else do you need?",
     "Add this to your cart."),
    ("This is the practice that makes the difference. 3 tests, full explanations, no guesswork.",
     "Get it for your students now."),
    ("Score tracking, answer explanations, and 90 real questions. Your {state} students are set.",
     "Add it to your cart and start prepping."),
    ("Let your students practice under real conditions. Three full tests, all explained.",
     "Download today."),
    ("Three tests can transform test-day anxiety into calm confidence.",
     "Get this resource for your {state} students."),
    ("Straightforward exam practice with answers that teach. That's what your students get.",
     "Add this to your cart today and start building confidence."),
    ("Three full practice tests. That's 90 real questions with detailed solutions.",
     "Grab it now for your {state} classroom."),
    ("Ninety questions of focused practice — from ratios to probability — with every answer explained.",
     "Download it and get your {state} students started."),
    ("This isn't busywork. Every question mirrors the real exam, and every answer teaches the concept.",
     "Add it to your cart and start preparing your students."),
    ("Your {state} students need practice that counts. Three full tests delivers exactly that.",
     "Get it today."),
    ("Three tests. Ninety questions. Full explanations. Ready to print.",
     "Add this to your cart and get started."),
]


# ---------------------------------------------------------------------------
# Helper generators
# ---------------------------------------------------------------------------

def make_features(idx, state):
    """Generate the features <ul> section."""
    v = idx % 10
    # Vary the order of feature bullets to add more uniqueness
    order_patterns = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        [0, 2, 1, 5, 3, 4, 6, 8, 7],
        [0, 5, 2, 3, 1, 4, 8, 7, 6],
        [0, 4, 1, 2, 3, 5, 7, 6, 8],
        [0, 1, 3, 5, 2, 4, 6, 7, 8],
        [0, 3, 2, 1, 5, 4, 7, 8, 6],
        [0, 2, 5, 4, 1, 3, 8, 6, 7],
        [0, 5, 1, 3, 4, 2, 6, 8, 7],
        [0, 4, 3, 2, 5, 1, 7, 6, 8],
        [0, 1, 5, 4, 2, 3, 8, 7, 6],
    ]
    bullets_raw = [
        FEAT_90Q[v],
        FEAT_FORMATS[v],
        FEAT_EXPLANATIONS[v],
        FEAT_SCORE[v],
        FEAT_STRANDS[v],
        FEAT_CONDITIONS[v],
        FEAT_COLOR[v],
        FEAT_ANSWERKEY[v],
        FEAT_PRINT[v],
    ]
    order = order_patterns[idx % len(order_patterns)]
    bullets = [bullets_raw[i] for i in order]

    heading = FEATURE_HEADINGS[idx].format(state=state)
    lines = [f'<p><b>{heading}</b></p>', '<ul>']
    for b in bullets:
        lines.append(f'<li>✅ {b}</li>')
    lines.append('</ul>')
    return '\n'.join(lines)


def make_chapters_table(idx, state, topics, chapters):
    """Chapters as a <table>."""
    heading = CHAPTER_HEADINGS[idx].format(state=state, topics=topics)
    lines = [f'<p><b>{heading}</b></p>', '<table>', '<tbody>']
    for i, (name, count) in enumerate(zip(CHAPTER_NAMES, chapters), 1):
        lines.append(f'<tr><td><b>Ch. {i}</b></td><td>{name}</td><td>{count} topics</td></tr>')
    lines.append(f'<tr><td></td><td><b>Total</b></td><td><b>{topics} topics</b></td></tr>')
    lines.append('</tbody>')
    lines.append('</table>')
    return '\n'.join(lines)


def make_chapters_list(idx, state, topics, chapters):
    """Chapters as a <ul> list."""
    heading = CHAPTER_HEADINGS[idx].format(state=state, topics=topics)
    lines = [f'<p><b>{heading}</b></p>',
             f'<p>This resource covers all {topics} Grade 7 math topics:</p>',
             '<ul>']
    for i, (name, count) in enumerate(zip(CHAPTER_NAMES, chapters), 1):
        lines.append(f'<li><b>Ch. {i}: {name}</b> — {count} topics</li>')
    lines.append('</ul>')
    return '\n'.join(lines)


def make_state_alignment(idx, state, topics):
    """State alignment paragraph."""
    heading = STATE_HEADINGS[idx].format(state=state)
    prose = STATE_PROSE[idx % len(STATE_PROSE)].format(state=state, topics=topics)
    return f'<p><b>{heading}</b></p>\n{prose}'


def make_use_cases(idx, state):
    """Use cases bullet list."""
    heading = USE_CASE_HEADINGS[idx].format(state=state)
    uc_set = USE_CASE_SETS[idx % len(USE_CASE_SETS)]
    lines = [f'<p><b>{heading}</b></p>', '<ul>']
    for item in uc_set:
        lines.append(f'<li>✅ {item}</li>')
    lines.append('</ul>')
    return '\n'.join(lines)


def make_series(idx, state):
    """Series cross-sell bullet list."""
    heading = SERIES_HEADINGS[idx].format(state=state)
    item_set = SERIES_ITEM_SETS[idx % len(SERIES_ITEM_SETS)]
    lines = [f'<p><b>{heading}</b></p>', '<ul>']
    for bold, desc in item_set:
        lines.append(f'<li>✅ {bold} — {desc}</li>')
    lines.append('</ul>')
    return '\n'.join(lines)


def make_cta(idx, state):
    """Closing CTA."""
    p1, p2 = CTA_CLOSINGS[idx]
    p1 = p1.format(state=state)
    p2 = p2.format(state=state)
    return f'<p>{p1}</p>\n<p><b>{p2}</b></p>'


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate(idx, slug, state, exam, topics, chapters, title):
    """Return the complete HTML description for one state."""
    parts = []

    # 1. Opening
    oh = OPENING_HEADINGS[idx].format(state=state, exam=exam, topics=topics)
    parts.append(f'<p><b>{oh}</b></p>')
    intro = OPENING_INTROS[idx % len(OPENING_INTROS)].format(
        title=title, state=state, topics=topics)
    parts.append(intro)

    # 2-6. Middle sections in varied order
    order = SECTION_ORDERS[idx % len(SECTION_ORDERS)]
    use_table = (idx % 2 == 0)

    section_builders = {
        "features": lambda: make_features(idx, state),
        "chapters": lambda: (make_chapters_table(idx, state, topics, chapters)
                             if use_table else
                             make_chapters_list(idx, state, topics, chapters)),
        "state": lambda: make_state_alignment(idx, state, topics),
        "use_cases": lambda: make_use_cases(idx, state),
        "series": lambda: make_series(idx, state),
    }

    for section_key in order:
        parts.append('<p></p>')
        parts.append(section_builders[section_key]())

    # 7. CTA
    parts.append('<p></p>')
    parts.append(make_cta(idx, state))

    # 8. Footer
    parts.append('\n')
    parts.append(FOOTER)

    return '\n\n'.join(parts) + '\n'


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for idx, (slug, state, exam, topics, chapters, title) in enumerate(STATES):
        html = generate(idx, slug, state, exam, topics, chapters, title)
        filename = f"{slug}_tpt_{TODAY}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✓ {filename}")
    print(f"\nDone — {len(STATES)} descriptions written to {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
