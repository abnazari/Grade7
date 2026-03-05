#!/usr/bin/env python3
"""
Generate 50 unique TPT product descriptions for 7_practice_tests (all 50 US states).
Each description is unique in structure, headings, prose, and presentation.
"""

import os

# ============================================================================
# STATE DATA
# ============================================================================

STANDARD_CHAPTERS = [
    ("Ratios and Proportional Relationships", 6),
    ("Percents in Everyday Life", 7),
    ("Operations with Rational Numbers", 8),
    ("Algebraic Expressions", 6),
    ("Equations and Inequalities", 6),
    ("Scale Drawings, Geometric Figures, and Angle Relationships", 6),
    ("Circles, Area, Surface Area, and Volume", 6),
    ("Statistics: Sampling and Comparing Populations", 4),
    ("Probability and Compound Events", 7),
]

STATES = [
    {"slug": "alabama", "name": "Alabama", "exam": "ACAP",
     "title": "7 Alabama ACAP Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "alaska", "name": "Alaska", "exam": "AK STAR",
     "title": "7 Alaska AK STAR Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 58, "chapters": [
         ("Ratios and Proportional Relationships", 6),
         ("Percents in Everyday Life", 7),
         ("Operations with Rational Numbers", 9),
         ("Algebraic Expressions", 6),
         ("Equations and Inequalities", 6),
         ("Scale Drawings, Geometric Figures, and Angle Relationships", 6),
         ("Circles, Area, Surface Area, and Volume", 6),
         ("Statistics: Sampling and Comparing Populations", 5),
         ("Probability and Compound Events", 7),
     ]},
    {"slug": "arizona", "name": "Arizona", "exam": "AASA",
     "title": "7 Arizona AASA Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "arkansas", "name": "Arkansas", "exam": "ATLAS",
     "title": "7 Arkansas ATLAS Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "california", "name": "California", "exam": "CAASPP",
     "title": "7 California CAASPP Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "colorado", "name": "Colorado", "exam": "CMAS",
     "title": "7 Colorado CMAS Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "connecticut", "name": "Connecticut", "exam": "SBAC",
     "title": "7 Connecticut SBAC Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "delaware", "name": "Delaware", "exam": "DeSSA",
     "title": "7 Delaware DeSSA Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "florida", "name": "Florida", "exam": "FAST",
     "title": "7 Florida FAST Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 60, "chapters": [
         ("Ratios and Proportional Relationships", 6),
         ("Percents in Everyday Life", 7),
         ("Operations with Rational Numbers", 8),
         ("Algebraic Expressions", 7),
         ("Equations and Inequalities", 6),
         ("Scale Drawings, Geometric Figures, and Angle Relationships", 6),
         ("Circles, Area, Surface Area, and Volume", 7),
         ("Statistics: Sampling and Comparing Populations", 6),
         ("Probability and Compound Events", 7),
     ]},
    {"slug": "georgia", "name": "Georgia", "exam": "Georgia Milestones",
     "title": "7 Georgia Georgia Milestones Grade 7 Math Practice Tests: Answers & Explanations",
     "topics": 56, "chapters": None},
    {"slug": "hawaii", "name": "Hawaii", "exam": "SBA",
     "title": "7 Hawaii SBA Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "idaho", "name": "Idaho", "exam": "ISAT",
     "title": "7 Idaho ISAT Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "illinois", "name": "Illinois", "exam": "IAR",
     "title": "7 Illinois IAR Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "indiana", "name": "Indiana", "exam": "ILEARN",
     "title": "7 Indiana ILEARN Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 58, "chapters": [
         ("Ratios and Proportional Relationships", 6),
         ("Percents in Everyday Life", 7),
         ("Operations with Rational Numbers", 8),
         ("Algebraic Expressions", 6),
         ("Equations and Inequalities", 6),
         ("Scale Drawings, Geometric Figures, and Angle Relationships", 7),
         ("Circles, Area, Surface Area, and Volume", 6),
         ("Statistics: Sampling and Comparing Populations", 5),
         ("Probability and Compound Events", 7),
     ]},
    {"slug": "iowa", "name": "Iowa", "exam": "ISASP",
     "title": "7 Iowa ISASP Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "kansas", "name": "Kansas", "exam": "KAP",
     "title": "7 Kansas KAP Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "kentucky", "name": "Kentucky", "exam": "KSA",
     "title": "7 Kentucky KSA Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "louisiana", "name": "Louisiana", "exam": "LEAP 2025",
     "title": "7 Louisiana LEAP 2025 Grade 7 Math Practice Tests: Test Prep & Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "maine", "name": "Maine", "exam": "MTYA",
     "title": "7 Maine MTYA Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "maryland", "name": "Maryland", "exam": "MCAP",
     "title": "7 Maryland MCAP Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "massachusetts", "name": "Massachusetts", "exam": "MCAS",
     "title": "7 Massachusetts MCAS Grade 7 Math Practice Tests: Test Prep & Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "michigan", "name": "Michigan", "exam": "M-STEP",
     "title": "7 Michigan M-STEP Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "minnesota", "name": "Minnesota", "exam": "MCA",
     "title": "7 Minnesota MCA Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 58, "chapters": [
         ("Ratios and Proportional Relationships", 6),
         ("Percents in Everyday Life", 8),
         ("Operations with Rational Numbers", 8),
         ("Algebraic Expressions", 6),
         ("Equations and Inequalities", 6),
         ("Scale Drawings, Geometric Figures, and Angle Relationships", 6),
         ("Circles, Area, Surface Area, and Volume", 6),
         ("Statistics: Sampling and Comparing Populations", 5),
         ("Probability and Compound Events", 7),
     ]},
    {"slug": "mississippi", "name": "Mississippi", "exam": "MAAP",
     "title": "7 Mississippi MAAP Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "missouri", "name": "Missouri", "exam": "MAP",
     "title": "7 Missouri MAP Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "montana", "name": "Montana", "exam": "MontCAS",
     "title": "7 Montana MontCAS Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "nebraska", "name": "Nebraska", "exam": "NSCAS",
     "title": "7 Nebraska NSCAS Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "nevada", "name": "Nevada", "exam": "SBAC",
     "title": "7 Nevada SBAC Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "new-hampshire", "name": "New Hampshire", "exam": "NH SAS",
     "title": "7 New Hampshire NH SAS Grade 7 Math Practice Tests: Test Prep & Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "new-jersey", "name": "New Jersey", "exam": "NJSLA",
     "title": "7 New Jersey NJSLA Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "new-mexico", "name": "New Mexico", "exam": "NM-MSSA",
     "title": "7 New Mexico NM-MSSA Grade 7 Math Practice Tests: Test Prep & Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "new-york", "name": "New York", "exam": "NYS Math Test",
     "title": "7 New York NYS Math Test Grade 7 Math Practice Tests: Answers & Explanations",
     "topics": 56, "chapters": None},
    {"slug": "north-carolina", "name": "North Carolina", "exam": "NC EOG",
     "title": "7 North Carolina NC EOG Grade 7 Math Practice Tests: Answers & Explanations",
     "topics": 56, "chapters": None},
    {"slug": "north-dakota", "name": "North Dakota", "exam": "NDSA",
     "title": "7 North Dakota NDSA Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "ohio", "name": "Ohio", "exam": "OST",
     "title": "7 Ohio OST Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "oklahoma", "name": "Oklahoma", "exam": "OSTP",
     "title": "7 Oklahoma OSTP Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 60, "chapters": [
         ("Ratios and Proportional Relationships", 7),
         ("Percents in Everyday Life", 8),
         ("Operations with Rational Numbers", 8),
         ("Algebraic Expressions", 6),
         ("Equations and Inequalities", 6),
         ("Scale Drawings, Geometric Figures, and Angle Relationships", 6),
         ("Circles, Area, Surface Area, and Volume", 6),
         ("Statistics: Sampling and Comparing Populations", 6),
         ("Probability and Compound Events", 7),
     ]},
    {"slug": "oregon", "name": "Oregon", "exam": "OSAS",
     "title": "7 Oregon OSAS Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "pennsylvania", "name": "Pennsylvania", "exam": "PSSA",
     "title": "7 Pennsylvania PSSA Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "rhode-island", "name": "Rhode Island", "exam": "RICAS",
     "title": "7 Rhode Island RICAS Grade 7 Math Practice Tests: Test Prep & Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "south-carolina", "name": "South Carolina", "exam": "SC READY",
     "title": "7 South Carolina SC READY Grade 7 Math Practice Tests: Answers & Explanations",
     "topics": 56, "chapters": None},
    {"slug": "south-dakota", "name": "South Dakota", "exam": "SBA",
     "title": "7 South Dakota SBA Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "tennessee", "name": "Tennessee", "exam": "TCAP",
     "title": "7 Tennessee TCAP Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "texas", "name": "Texas", "exam": "STAAR",
     "title": "7 Texas STAAR Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 62, "chapters": [
         ("Ratios and Proportional Relationships", 6),
         ("Percents in Everyday Life", 10),
         ("Operations with Rational Numbers", 8),
         ("Algebraic Expressions", 6),
         ("Equations and Inequalities", 6),
         ("Scale Drawings, Geometric Figures, and Angle Relationships", 7),
         ("Circles, Area, Surface Area, and Volume", 6),
         ("Statistics: Sampling and Comparing Populations", 6),
         ("Probability and Compound Events", 7),
     ]},
    {"slug": "utah", "name": "Utah", "exam": "RISE",
     "title": "7 Utah RISE Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "vermont", "name": "Vermont", "exam": "SBAC",
     "title": "7 Vermont SBAC Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 56, "chapters": None},
    {"slug": "virginia", "name": "Virginia", "exam": "SOL",
     "title": "7 Virginia SOL Grade 7 Math Practice Tests: Comprehensive Test Prep with Answers",
     "topics": 64, "chapters": [
         ("Ratios and Proportional Relationships", 6),
         ("Percents in Everyday Life", 7),
         ("Operations with Rational Numbers", 10),
         ("Algebraic Expressions", 7),
         ("Equations and Inequalities", 6),
         ("Scale Drawings, Geometric Figures, and Angle Relationships", 8),
         ("Circles, Area, Surface Area, and Volume", 7),
         ("Statistics: Sampling and Comparing Populations", 6),
         ("Probability and Compound Events", 7),
     ]},
    {"slug": "washington", "name": "Washington", "exam": "SBA",
     "title": "7 Washington SBA Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "west-virginia", "name": "West Virginia", "exam": "WVGSA",
     "title": "7 West Virginia WVGSA Grade 7 Math Practice Tests: Test Prep & Detailed Answers",
     "topics": 56, "chapters": None},
    {"slug": "wisconsin", "name": "Wisconsin", "exam": "Forward Exam",
     "title": "7 Wisconsin Forward Exam Grade 7 Math Practice Tests: Answers & Explanations",
     "topics": 56, "chapters": None},
    {"slug": "wyoming", "name": "Wyoming", "exam": "WY-TOPP",
     "title": "7 Wyoming WY-TOPP Grade 7 Math Practice Tests: Test Prep with Detailed Answers",
     "topics": 56, "chapters": None},
]

# ============================================================================
# FOOTER (exact copy, never modify)
# ============================================================================

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

# ============================================================================
# VARIATION POOLS
# ============================================================================

# --- Opening style generators ---
# Each returns (heading_html, intro_paragraph_html)
# ALL include state name or exam for guaranteed uniqueness across 50 states.
def opening_style_0(s):
    return (
        f'<p><b>7 Full-Length {s["exam"]} Practice Tests for {s["name"]} — 210 Questions, Step-by-Step Answers</b></p>',
        f'<p><b>{s["title"]}</b> gives your students seven complete practice tests covering all {s["topics"]} Grade 7 math topics. Every question comes with a detailed explanation.</p>'
    )

def opening_style_1(s):
    return (
        f'<p><b>210 Practice Questions for {s["name"]} Grade 7 Math — 7 Complete Tests</b></p>',
        f'<p>This is <b>{s["title"]}</b>. Seven tests, 30 questions each, all aligned to {s["name"]}\'s Grade 7 math standards — with full answer explanations for every single problem.</p>'
    )

def opening_style_2(s):
    return (
        f'<p><b>Seven Complete {s["exam"]} Practice Tests for {s["name"]} Grade 7 Math</b></p>',
        f'<p><b>{s["title"]}</b> — 7 tests, 210 questions, and step-by-step answer explanations for all of them. Built specifically for {s["name"]} students.</p>'
    )

def opening_style_3(s):
    return (
        f'<p><b>The Practice Your {s["name"]} Students Need — 7 Full Tests, 210 Questions</b></p>',
        f'<p><b>{s["title"]}</b> packs seven full-length practice tests into one resource. Each test has 30 questions that cover every Grade 7 math skill, and every answer is explained step by step.</p>'
    )

def opening_style_4(s):
    return (
        f'<p><b>{s["name"]} Grade 7 Math: 7 Tests, 210 Questions, Every Answer Explained</b></p>',
        f'<p>That\'s what you get with <b>{s["title"]}</b>. Seven practice tests written for {s["name"]}\'s Grade 7 math curriculum, covering all {s["topics"]} topics your students need to know.</p>'
    )

def opening_style_5(s):
    return (
        f'<p><b>Serious {s["exam"]} Prep for {s["name"]} Grade 7 Math</b></p>',
        f'<p><b>{s["title"]}</b> includes 7 full-length practice tests with 30 questions each. That\'s 210 problems — every one with a detailed, step-by-step answer explanation.</p>'
    )

def opening_style_6(s):
    return (
        f'<p><b>7 Practice Tests Built for {s["name"]}\'s Grade 7 Math Standards</b></p>',
        f'<p><b>{s["title"]}</b> covers all {s["topics"]} topics across 9 chapters. Each of the 7 tests includes 30 questions with complete answer explanations so students learn from every problem.</p>'
    )

def opening_style_7(s):
    return (
        f'<p><b>Give Your {s["name"]} Students 210 Questions of Real {s["exam"]} Practice</b></p>',
        f'<p><b>{s["title"]}</b> — seven complete tests, each with 30 carefully written questions covering {s["name"]}\'s Grade 7 math standards. Every answer includes a full step-by-step explanation.</p>'
    )

def opening_style_8(s):
    return (
        f'<p><b>{s["name"]} Grade 7 Math — {s["topics"]} Topics, 7 Tests, 210 Problems, Full Explanations</b></p>',
        f'<p><b>{s["title"]}</b> is a complete practice test resource for {s["name"]} Grade 7 math. Students work through 7 full-length tests and learn from the detailed answer key after each one.</p>'
    )

def opening_style_9(s):
    return (
        f'<p><b>Everything {s["name"]} Students Need to Practice for the {s["exam"]}</b></p>',
        f'<p>This is <b>{s["title"]}</b>. It includes 7 full practice tests — 210 total questions — with step-by-step explanations for every answer. Covers all {s["topics"]} Grade 7 math topics.</p>'
    )

def opening_style_10(s):
    return (
        f'<p><b>Seven Full Practice Tests for {s["name"]} Grade 7 Math</b></p>',
        f'<p><b>{s["title"]}</b>. 210 questions across 7 complete tests, each one aligned to {s["name"]}\'s specific Grade 7 standards. Full answer explanations included for every problem.</p>'
    )

def opening_style_11(s):
    return (
        f'<p><b>{s["name"]} {s["exam"]} Test Prep — 210 Questions, 7 Tests, Every Answer Explained</b></p>',
        f'<p><b>{s["title"]}</b> is built for {s["name"]} students. Seven full-length tests covering {s["topics"]} topics — plus a complete answer key with detailed explanations.</p>'
    )

def opening_style_12(s):
    return (
        f'<p><b>Real {s["exam"]} Practice for {s["name"]} — 7 Complete Tests</b></p>',
        f'<p>Your students get 210 practice questions across 7 full-length tests. That\'s <b>{s["title"]}</b> — written for {s["name"]}\'s Grade 7 math curriculum with step-by-step answer explanations.</p>'
    )

def opening_style_13(s):
    return (
        f'<p><b>Prepare for the {s["exam"]} With 7 Full-Length {s["name"]} Grade 7 Math Tests</b></p>',
        f'<p><b>{s["title"]}</b> has everything your students need: 7 complete practice tests, 210 questions total, and step-by-step explanations for every answer.</p>'
    )

def opening_style_14(s):
    return (
        f'<p><b>{s["name"]}\'s Complete {s["exam"]} Practice — 7 Tests, 30 Questions Each</b></p>',
        f'<p><b>{s["title"]}</b> covers all {s["topics"]} Grade 7 math topics with 7 full-length tests. Every question comes with a clear, step-by-step explanation in the answer key.</p>'
    )

def opening_style_15(s):
    return (
        f'<p><b>7 {s["exam"]} Practice Tests — Made for {s["name"]} Grade 7</b></p>',
        f'<p>This is <b>{s["title"]}</b>. Seven full practice tests, 210 total questions, complete answer explanations — all aligned to {s["name"]}\'s Grade 7 math standards.</p>'
    )

def opening_style_16(s):
    return (
        f'<p><b>{s["name"]} Grade 7 Test Prep: 7 Full Practice Tests with 210 Questions</b></p>',
        f'<p><b>{s["title"]}</b>. Each test has 30 questions covering {s["name"]}\'s Grade 7 math curriculum. Every answer is fully explained so students learn as they go.</p>'
    )

def opening_style_17(s):
    return (
        f'<p><b>Get Your {s["name"]} Students {s["exam"]}-Ready — 7 Practice Tests Inside</b></p>',
        f'<p><b>{s["title"]}</b> delivers 210 practice questions across 7 tests, each with step-by-step answer explanations. Covers all {s["topics"]} topics in the Grade 7 math curriculum.</p>'
    )

def opening_style_18(s):
    return (
        f'<p><b>{s["name"]} — 7 Grade 7 Math Practice Tests with Full Answer Explanations</b></p>',
        f'<p><b>{s["title"]}</b>. 30 questions per test, 7 tests total, 210 questions — every answer explained. Written for {s["name"]}\'s specific Grade 7 standards.</p>'
    )

def opening_style_19(s):
    return (
        f'<p><b>Seven Tests. 210 Questions. Built for {s["name"]}.</b></p>',
        f'<p><b>{s["title"]}</b> is the practice resource your {s["name"]} Grade 7 students need. Every question has a detailed explanation so they learn from every problem.</p>'
    )

def opening_style_20(s):
    return (
        f'<p><b>Practice Makes Confident — 7 {s["exam"]} Tests for {s["name"]} Grade 7</b></p>',
        f'<p>With <b>{s["title"]}</b>, your students work through 7 full-length practice tests — 210 questions with complete answer explanations, all aligned to {s["name"]}\'s standards.</p>'
    )

def opening_style_21(s):
    return (
        f'<p><b>{s["name"]} Grade 7 Students: Here Are 7 Full Practice Tests</b></p>',
        f'<p><b>{s["title"]}</b>. This is 210 practice questions with detailed step-by-step answers — built around {s["name"]}\'s Grade 7 math curriculum, covering all {s["topics"]} topics.</p>'
    )

def opening_style_22(s):
    return (
        f'<p><b>The {s["exam"]} Test Prep Book for {s["name"]} — 7 Complete Practice Tests</b></p>',
        f'<p>Inside <b>{s["title"]}</b> you\'ll find 210 questions across 7 full tests, with step-by-step explanations for every answer. Aligned to {s["name"]}\'s Grade 7 math standards.</p>'
    )

def opening_style_23(s):
    return (
        f'<p><b>All the {s["exam"]} Practice Your {s["name"]} Grade 7 Students Need</b></p>',
        f'<p><b>{s["title"]}</b>. Seven tests, 30 questions each, covering {s["topics"]} topics — with a full answer key that explains every problem step by step.</p>'
    )

def opening_style_24(s):
    return (
        f'<p><b>{s["name"]} {s["exam"]} Prep: 210 Grade 7 Math Questions with Answers</b></p>',
        f'<p>This is <b>{s["title"]}</b>. Seven complete practice tests — each with 30 questions — covering every Grade 7 math skill your {s["name"]} students need. Every answer is explained.</p>'
    )

def opening_style_25(s):
    return (
        f'<p><b>7 Full Tests for {s["name"]}: {s["topics"]} Topics, 210 Questions, All Answers Explained</b></p>',
        f'<p><b>{s["title"]}</b> gives your students exactly what they need for the {s["exam"]}: seven comprehensive practice tests with detailed step-by-step answer explanations.</p>'
    )

def opening_style_26(s):
    return (
        f'<p><b>Prep for the {s["exam"]} — 7 Practice Tests for {s["name"]} Grade 7 Math</b></p>',
        f'<p><b>{s["title"]}</b> includes 210 questions across 7 full tests. Every question has a detailed answer explanation, and every test covers {s["name"]}\'s Grade 7 math standards.</p>'
    )

def opening_style_27(s):
    return (
        f'<p><b>{s["name"]}: Seven Grade 7 Math Tests, 210 Questions, Complete Explanations</b></p>',
        f'<p>That\'s <b>{s["title"]}</b>. Seven full-length tests covering all {s["topics"]} topics in {s["name"]}\'s Grade 7 math curriculum, with step-by-step answer explanations for every problem.</p>'
    )

def opening_style_28(s):
    return (
        f'<p><b>210 Questions Worth of {s["exam"]} Practice for {s["name"]} Grade 7</b></p>',
        f'<p><b>{s["title"]}</b> — 7 complete practice tests, each shaped around {s["name"]}\'s specific Grade 7 math standards. Full answer explanations included.</p>'
    )

def opening_style_29(s):
    return (
        f'<p><b>7 Practice Tests for the {s["exam"]} — {s["name"]} Grade 7 Math</b></p>',
        f'<p><b>{s["title"]}</b> covers {s["topics"]} topics in 9 chapters. 210 total questions, 7 tests, and every answer explained step by step.</p>'
    )

def opening_style_30(s):
    return (
        f'<p><b>{s["name"]} Grade 7 Math Test Prep Done Right — 7 Full Practice Tests</b></p>',
        f'<p>This is <b>{s["title"]}</b>. Your students get 210 practice questions with step-by-step answers, all aligned to {s["name"]}\'s Grade 7 standards.</p>'
    )

def opening_style_31(s):
    return (
        f'<p><b>For {s["name"]} Teachers: 7 Grade 7 Math Practice Tests, 210 Questions</b></p>',
        f'<p><b>{s["title"]}</b>. Each test has 30 questions, and every single answer is explained in detail. Covers all {s["topics"]} topics in {s["name"]}\'s curriculum.</p>'
    )

def opening_style_32(s):
    return (
        f'<p><b>7 Tests. 210 Questions. Every Answer Explained. Made for {s["name"]}.</b></p>',
        f'<p><b>{s["title"]}</b> is written for {s["name"]}\'s Grade 7 math students. Seven full-length practice tests with clear, step-by-step explanations for every problem.</p>'
    )

def opening_style_33(s):
    return (
        f'<p><b>{s["name"]} {s["exam"]}: 7 Full-Length Grade 7 Math Practice Tests</b></p>',
        f'<p><b>{s["title"]}</b> — 210 questions, 7 tests, step-by-step answer explanations. Built for {s["name"]}\'s specific Grade 7 math standards.</p>'
    )

def opening_style_34(s):
    return (
        f'<p><b>Full {s["exam"]} Practice for {s["name"]} — Seven Tests, 210 Questions</b></p>',
        f'<p><b>{s["title"]}</b>. Seven complete, full-length practice tests covering every Grade 7 math topic your {s["name"]} students need — with detailed answer explanations.</p>'
    )

def opening_style_35(s):
    return (
        f'<p><b>{s["name"]}\'s {s["topics"]} Grade 7 Math Topics — Practiced Across 7 Full Tests</b></p>',
        f'<p>This is <b>{s["title"]}</b>. 210 questions with step-by-step answer explanations — the practice your students need for {s["name"]}\'s Grade 7 math standards.</p>'
    )

def opening_style_36(s):
    return (
        f'<p><b>Seven {s["exam"]} Tests for {s["name"]} Grade 7 Math — 210 Questions Total</b></p>',
        f'<p><b>{s["title"]}</b> gives your students real test prep: 7 full-length practice tests, step-by-step answers, and coverage of all {s["topics"]} Grade 7 topics.</p>'
    )

def opening_style_37(s):
    return (
        f'<p><b>{s["name"]} Students: Get Ready With 7 Grade 7 Math Practice Tests</b></p>',
        f'<p><b>{s["title"]}</b>. 210 practice questions across 7 tests — every answer explained, every topic covered. Written specifically for {s["name"]}.</p>'
    )

def opening_style_38(s):
    return (
        f'<p><b>210 Practice Problems for {s["name"]}\'s {s["exam"]} — All in 7 Tests</b></p>',
        f'<p><b>{s["title"]}</b> covers all {s["topics"]} Grade 7 math topics in 7 full-length practice tests with detailed, step-by-step answer explanations.</p>'
    )

def opening_style_39(s):
    return (
        f'<p><b>Your Complete {s["exam"]} Practice Resource — 7 Tests for {s["name"]} Grade 7</b></p>',
        f'<p><b>{s["title"]}</b>. This book delivers 210 questions, 7 complete tests, and full answer explanations — all for {s["name"]}\'s Grade 7 math standards.</p>'
    )

def opening_style_40(s):
    return (
        f'<p><b>{s["name"]} Grade 7 Math: Practice the Way It Counts — 7 Full Tests</b></p>',
        f'<p><b>{s["title"]}</b>. Seven practice tests with 30 questions each, step-by-step answer explanations, and coverage of all {s["topics"]} topics in the curriculum.</p>'
    )

def opening_style_41(s):
    return (
        f'<p><b>7 {s["name"]} Grade 7 Math Practice Tests — Answers and Explanations Included</b></p>',
        f'<p>This is <b>{s["title"]}</b>. 210 total questions across 7 full-length tests, each aligned to {s["name"]}\'s Grade 7 math standards. Full answer explanations for every problem.</p>'
    )

def opening_style_42(s):
    return (
        f'<p><b>Test Prep for {s["name"]}: 7 Full {s["exam"]} Grade 7 Math Practice Tests</b></p>',
        f'<p><b>{s["title"]}</b> — 7 tests, 210 questions, every answer explained step by step. Designed to match {s["name"]}\'s specific Grade 7 math curriculum.</p>'
    )

def opening_style_43(s):
    return (
        f'<p><b>{s["name"]} — Seven Practice Tests With 210 Grade 7 Math Questions</b></p>',
        f'<p>Here\'s <b>{s["title"]}</b>. Every test has 30 questions, and every answer includes a detailed step-by-step explanation. Covers all {s["topics"]} topics.</p>'
    )

def opening_style_44(s):
    return (
        f'<p><b>Seven Full {s["exam"]} Practice Tests — {s["name"]} Grade 7 Math</b></p>',
        f'<p><b>{s["title"]}</b> packs 210 practice questions into 7 complete tests. All answers explained step by step. All {s["topics"]} Grade 7 topics covered.</p>'
    )

def opening_style_45(s):
    return (
        f'<p><b>{s["name"]} Grade 7 Math in 7 Practice Tests — 210 Questions, Full Answers</b></p>',
        f'<p><b>{s["title"]}</b>. Covers {s["name"]}\'s Grade 7 math standards across 7 full-length tests. Detailed answer explanations included for every question.</p>'
    )

def opening_style_46(s):
    return (
        f'<p><b>{s["exam"]} Practice for {s["name"]}: 7 Full Tests, 210 Questions</b></p>',
        f'<p><b>{s["title"]}</b>. That\'s seven full-length practice tests, 30 questions each, with step-by-step answer explanations for every problem — built for {s["name"]}.</p>'
    )

def opening_style_47(s):
    return (
        f'<p><b>For {s["name"]}: 210 Grade 7 Math Questions You Can Print and Use Today</b></p>',
        f'<p><b>{s["title"]}</b>. Seven full tests with step-by-step explanations for every answer, covering all {s["topics"]} topics in {s["name"]}\'s Grade 7 curriculum.</p>'
    )

def opening_style_48(s):
    return (
        f'<p><b>{s["name"]} {s["exam"]} Test Prep — Seven Practice Tests, 210 Questions</b></p>',
        f'<p><b>{s["title"]}</b> is 7 complete practice tests with 30 questions each. Every answer is explained step by step. Every topic in {s["name"]}\'s Grade 7 math curriculum is covered.</p>'
    )

def opening_style_49(s):
    return (
        f'<p><b>Grade 7 Math for {s["name"]} — 7 Complete {s["exam"]} Practice Tests</b></p>',
        f'<p><b>{s["title"]}</b>. 210 total questions with full step-by-step explanations. Covers {s["topics"]} topics across 9 chapters — written for {s["name"]}\'s Grade 7 students.</p>'
    )

OPENING_STYLES = [
    opening_style_0, opening_style_1, opening_style_2, opening_style_3,
    opening_style_4, opening_style_5, opening_style_6, opening_style_7,
    opening_style_8, opening_style_9, opening_style_10, opening_style_11,
    opening_style_12, opening_style_13, opening_style_14, opening_style_15,
    opening_style_16, opening_style_17, opening_style_18, opening_style_19,
    opening_style_20, opening_style_21, opening_style_22, opening_style_23,
    opening_style_24, opening_style_25, opening_style_26, opening_style_27,
    opening_style_28, opening_style_29, opening_style_30, opening_style_31,
    opening_style_32, opening_style_33, opening_style_34, opening_style_35,
    opening_style_36, opening_style_37, opening_style_38, opening_style_39,
    opening_style_40, opening_style_41, opening_style_42, opening_style_43,
    opening_style_44, opening_style_45, opening_style_46, opening_style_47,
    opening_style_48, opening_style_49,
]

# --- Feature section ---
# Feature headings use {name} and {exam} for uniqueness
FEATURE_HEADINGS = [
    "Here's What Your {name} Students Get",
    "What's Inside This {exam} Prep Book",
    "What You'll Find Inside",
    "A Quick Look Inside the {name} Edition",
    "What This {name} Book Includes",
    "Inside the {exam} Practice Tests",
    "Here's What's Included for {name}",
    "The {name} Rundown",
    "Quick Overview — {name} Edition",
    "Everything in the {name} {exam} Book",
    "At a Glance: {name} Grade 7",
    "What Makes the {name} Edition Different",
    "What {name} Students Get",
    "The Details — {name}",
    "Here's the Full {name} Picture",
    "What This {exam} Book Delivers",
    "Inside the {name} Grade 7 Practice Tests",
    "{name} {exam} Prep — Here's What's Included",
    "What's Packed Into the {name} Edition",
    "Features of the {name} {exam} Book",
    "A Closer Look — {name} Grade 7",
    "What's in the {name} Book",
    "The {name} {exam} Details",
    "{name}: Here's What You're Getting",
    "Everything Inside the {name} Edition",
    "What {name} Teachers Get",
    "The {name} Book — Feature by Feature",
    "{name} {exam} Practice: Here's What's Inside",
    "For {name} — Here's the Full Package",
    "Inside This {name} Resource",
    "What the {name} {exam} Book Includes",
    "{name} Grade 7 Math — Everything You Get",
    "Here's What's in the {name} Edition",
    "The Full {name} {exam} Package",
    "What's Included for {name} Students",
    "{name} — What This Book Delivers",
    "Inside the {name} {exam} Test Prep Book",
    "Feature List: {name} {exam} Edition",
    "What {name} Students Will Find Inside",
    "{name} Edition — Everything Included",
    "Your {name} {exam} Prep Book Includes",
    "Here's the {name} Edition at a Glance",
    "{name}: What You'll Find in This Book",
    "The {name} Practice Test Package",
    "Features — {name} {exam} Grade 7",
    "What {name} Classrooms Get",
    "{name} {exam} Book — What's Inside",
    "For {name}: Here's What It Includes",
    "The {name} {exam} Practice Resource",
    "Everything in This {name} Book",
]

# Feature bullet variations — each list is a set of 9 features (core + design)
# grouped as: [test_count, format, explanations, score, coverage, realistic, colorful, answer_key, print_ready]
FEATURE_SETS = [
    [
        "7 full practice tests — 30 questions per test, 210 total — with complete answer explanations",
        "Includes multiple-choice, short-answer, and extended-response questions",
        "Every answer comes with a detailed step-by-step explanation",
        "Score tracking sheets so students can measure their growth over all 7 tests",
        "Covers every Grade 7 math strand: ratios, number systems, algebra, geometry, and statistics",
        "Timed format with answer grids that mimic real test-day conditions",
        "Full-color pages with illustrations, diagrams, and a friendly owl mascot throughout",
        "Complete answer key with worked-out explanations",
        "Print and go — no prep, no assembly, just download and use",
    ],
    [
        "210 practice problems spread across 7 complete tests (30 questions each) with full explanations",
        "Question types match the real exam: multiple-choice, short-answer, and extended response",
        "Step-by-step explanations for every single question — students learn from every mistake",
        "Built-in score tracking after each test to show progress",
        "All {topics} Grade 7 math topics covered across 9 chapters",
        "Realistic test format — answer grids, timed sections, and scoring rubrics",
        "Engaging full-color design with diagrams, illustrations, and an owl mascot kids love",
        "Detailed answer key included for every question",
        "Download, print, use — zero prep needed",
    ],
    [
        "Seven tests × 30 questions = 210 problems with complete answer explanations",
        "Multiple-choice, short-answer, and extended-response formats — just like the real thing",
        "Detailed explanations walk students through every answer, step by step",
        "Track scores across all 7 tests to see improvement over time",
        "Covers ratios, percents, rational numbers, algebra, geometry, statistics, and probability",
        "Test-day format with answer grids and scoring rubrics included",
        "Colorful, illustrated pages with diagrams and a fun owl mascot",
        "Answer key with full explanations for every problem",
        "Ready to print — no cutting, no folding, no prep",
    ],
    [
        "7 complete practice tests with 30 questions each — that's 210 questions total",
        "Question formats mirror state assessments: multiple-choice, short-answer, extended response",
        "Every question has a step-by-step explanation so students understand the how and why",
        "Score-tracking tools built into each test for easy progress monitoring",
        "Spans all {topics} topics across 9 chapters of Grade 7 math",
        "Formatted to feel like the real test — timed, with answer grids and rubrics",
        "Professional full-color pages with illustrations and a friendly owl mascot",
        "Comprehensive answer key with explanations",
        "Just print and hand out — completely ready to use",
    ],
    [
        "210 total practice questions across 7 full-length tests with answer explanations",
        "Realistic question types: multiple-choice, short-answer, and extended response",
        "Clear, step-by-step explanations help students learn from every answer",
        "Progress tracking after each test shows exactly where students stand",
        "Every Grade 7 math topic is covered — from ratios to probability",
        "Timed tests with answer grids and scoring rubrics for a real-test feel",
        "Full-color, visually engaging pages with diagrams and an owl mascot",
        "Complete answer key with worked explanations",
        "No prep at all — print and it's ready to go",
    ],
    [
        "7 full tests, 30 questions per test, 210 questions total — each with a full explanation",
        "Covers multiple-choice, short-answer, and extended-response question types",
        "Step-by-step answer explanations turn every mistake into a learning opportunity",
        "Score sheets after each test let students track their own progress",
        "All {topics} topics across the full Grade 7 math curriculum",
        "Realistic format with timed sections, answer grids, and rubrics",
        "Bright, colorful pages with helpful diagrams and an owl mascot",
        "Full answer key with detailed explanations for every question",
        "Download once, print as many copies as you need — no extra prep",
    ],
    [
        "210 practice questions spread over 7 full-length tests — all with detailed answers",
        "Short-answer, multiple-choice, and extended-response questions just like the real assessment",
        "Each answer explanation walks through the solution one step at a time",
        "Track scores test by test to spot trends and measure improvement",
        "Covers every strand: ratios, number operations, algebra, geometry, stats, and probability",
        "Answer grids, timing guidelines, and rubrics make it feel like the real thing",
        "Full-color layout with engaging illustrations, diagrams, and an owl mascot",
        "Includes a complete, detailed answer key",
        "Print-ready — download and use immediately",
    ],
    [
        "7 practice tests with 30 questions each = 210 total, every answer fully explained",
        "Question formats include multiple-choice, short-answer, and extended response",
        "Detailed step-by-step explanations for every single problem",
        "Score-tracking tools included so students can see their growth",
        "Covers all {topics} Grade 7 math topics in 9 chapters",
        "Real-test format with answer grids and timing built in",
        "Colorful, illustrated pages featuring diagrams and a friendly owl mascot",
        "Full answer key with clear explanations",
        "Zero prep — print and use right away",
    ],
    [
        "210 questions across 7 complete practice tests, each with step-by-step answer explanations",
        "Includes all major question types: multiple-choice, short-answer, extended response",
        "Every explanation is written clearly so students learn the process, not just the answer",
        "Built-in score tracking helps students (and teachers) see real progress over 7 tests",
        "Covers all the big Grade 7 math topics: ratios, percents, integers, expressions, equations, geometry, and data",
        "Designed to match test-day conditions — timed sections, answer grids, scoring rubrics",
        "Engaging full-color pages with illustrations, diagrams, and an owl mascot on every test",
        "Answer key included — fully detailed for every question",
        "Print, copy, and use — no prep whatsoever",
    ],
    [
        "7 full tests × 30 questions each = 210 practice problems with full explanations",
        "Multiple-choice, short-answer, extended-response — all the formats your students need to practice",
        "Clear step-by-step solutions for every question in the answer key",
        "Score tracking across all 7 tests so you can measure growth over time",
        "All {topics} topics in the Grade 7 math curriculum, organized in 9 chapters",
        "Realistic test layout — timing, answer grids, and rubrics included",
        "Full-color pages with diagrams, illustrations, and a fun owl mascot",
        "Comprehensive answer key with worked examples",
        "Print-ready — download and start using today",
    ],
]

# --- Chapter headings ---
# Chapter headings — {topics} varies by state, {name} ensures uniqueness
CHAPTER_HEADINGS = [
    "All {topics} {name} Topics, Covered",
    "What's Covered in {name}",
    "{topics} Topics Across 9 Chapters — {name}",
    "Here's the {name} Breakdown",
    "{name} Topics at a Glance",
    "The Full {name} Topic List",
    "Every {name} Topic, Every Chapter",
    "{name} — Chapter by Chapter",
    "{name} Content Coverage",
    "9 Chapters, {topics} Topics for {name}",
    "What {name} Students Will Practice",
    "{name} Topic Breakdown",
    "Inside the 9 {name} Chapters",
    "Full {name} Coverage: {topics} Topics",
    "Here's What {name} Students Cover",
    "All 9 {name} Chapters at a Glance",
    "{name}: {topics} Topics in 9 Chapters",
    "The {name} Grade 7 Math Breakdown",
    "{name} — All {topics} Topics Listed",
    "Chapter-by-Chapter: {name} Grade 7",
    "{topics} {name} Topics, 9 Chapters",
    "{name}: Here's Every Chapter",
    "What the {name} Book Covers",
    "All {topics} Topics for {name} Grade 7",
    "The Complete {name} Topic List",
    "{name} Math Topics — All 9 Chapters",
    "Topic Coverage for {name}",
    "{name} Grade 7: Every Topic Covered",
    "Chapters and Topics — {name}",
    "The {name} Breakdown: {topics} Topics",
    "What {name} Grade 7 Students Cover",
    "{name}: Chapter-by-Chapter Overview",
    "{topics} Topics Covered in the {name} Book",
    "Here's How {name}'s {topics} Topics Break Down",
    "All the {name} Topics in One Table",
    "{name} — Full Chapter Breakdown",
    "Topic Map: {name} Grade 7 Math",
    "For {name}: {topics} Topics in 9 Chapters",
    "{name} Edition — Topics at a Glance",
    "The {name} Curriculum, Chapter by Chapter",
    "{name} Grade 7 Math: Topics Overview",
    "Complete {name} Topic Coverage",
    "Every {name} Topic Across 9 Chapters",
    "What's in the {name} Edition: {topics} Topics",
    "{name} Students Practice These {topics} Topics",
    "{name} — All Topics, All Chapters",
    "The {name} {topics}-Topic Breakdown",
    "{name}'s 9 Chapters at a Glance",
    "Chapter Coverage: {name} Grade 7",
    "{name} Topics — The Full List",
]

# --- Alignment headings ---
ALIGNMENT_HEADINGS = [
    "Written for {name}",
    "Made for {name} Students",
    "Aligned to {name}'s Standards",
    "Follows {name}'s Grade 7 Math Standards",
    "Built for {name}",
    "Designed Around {name}'s Curriculum",
    "{name}-Specific Content",
    "Matches {name}'s Standards",
    "Tailored for {name}",
    "This Is a {name} Book",
    "Specifically for {name}",
    "Why {name}?",
    "Made With {name} in Mind",
    "Focused on {name}'s Requirements",
    "Not Generic — Made for {name}",
    "{name}'s Grade 7 Standards, Covered",
]

# --- Alignment paragraph variations ---
ALIGNMENT_PARAGRAPHS = [
    "This isn't a generic, one-size-fits-all test prep book. It's written specifically for <b>{name}</b>'s Grade 7 math standards. The {topics} topics match what your students are expected to know, and the questions reflect what they'll see on the <b>{exam}</b>.",
    "Every question in this book is built around <b>{name}</b>'s specific Grade 7 math curriculum. It covers all {topics} topics your students need, and the question styles match the <b>{exam}</b> format.",
    "This book targets <b>{name}</b>'s Grade 7 math standards — not some generic national curriculum. The {topics} topics are the ones <b>{name}</b> students actually need to learn, and the practice tests reflect the <b>{exam}</b> format.",
    "Your students aren't taking a generic math test — they're taking the <b>{exam}</b>. This book is built to match <b>{name}</b>'s specific standards, covering all {topics} topics in the Grade 7 curriculum.",
    "This resource is aligned to <b>{name}</b>'s Grade 7 math standards. All {topics} topics are included, and the test format mirrors what students will face on the <b>{exam}</b>.",
    "<b>{name}</b> has its own Grade 7 math standards, and this book follows them. The {topics} topics and the <b>{exam}</b>-style questions are designed to prepare your students for exactly what's ahead.",
    "Everything here matches <b>{name}</b>'s Grade 7 requirements. The {topics} topics, the question types, the test structure — it's all built around the <b>{exam}</b> and <b>{name}</b>'s math standards.",
    "This was written for <b>{name}</b> — not adapted from another state's book. It covers the {topics} topics your students need and mirrors the <b>{exam}</b> format throughout.",
    "The content lines up with <b>{name}</b>'s Grade 7 math standards from start to finish. {topics} topics, 9 chapters, and test questions that match the <b>{exam}</b> style.",
    "This is <b>{name}</b>'s book. The standards, the topics, the test format — all {topics} topics align to what <b>{name}</b> Grade 7 students need to know for the <b>{exam}</b>.",
    "Every chapter and topic is selected to match <b>{name}</b>'s Grade 7 math standards. The practice tests mirror the <b>{exam}</b> format, and the {topics} topics cover the full curriculum.",
    "Built from the ground up for <b>{name}</b>'s Grade 7 math curriculum. The questions follow the <b>{exam}</b> format, and all {topics} required topics are included.",
    "Not a repackaged national resource. This book was designed for <b>{name}</b>'s standards — {topics} topics, 9 chapters, and questions styled after the <b>{exam}</b>.",
]

# --- Use case headings ---
USE_CASE_HEADINGS = [
    "Who's This {name} Book For?",
    "Great For {name} Classrooms",
    "Works Well For {name} Students",
    "Who'll Get the Most Out of the {name} Edition?",
    "Perfect Fit for {name}",
    "Ways to Use This in {name}",
    "How {name} Teachers Can Use It",
    "Ideal for {name} Grade 7",
    "This Works for {name}",
    "Who Can Use the {name} Book?",
    "Use It in {name} For",
    "Who Benefits in {name}?",
    "Fits Right In for {name}",
    "Made for These {name} Situations",
    "Here's Who This Helps in {name}",
    "When to Use This {name} Book",
    "{name}: Who's This For?",
    "Great for {name} Homes and Classrooms",
    "Perfect for {name} Grade 7 Students",
    "How to Use the {name} Edition",
    "For {name}: Who Benefits?",
    "The {name} Book Works For",
    "Who Uses the {name} Edition?",
    "{name} — Who's This For?",
    "Ways to Use This {name} Resource",
    "For {name} Teachers, Tutors, and Parents",
    "{name}: Perfect Fit For",
    "Use the {name} Edition For",
    "Great Uses for the {name} Book",
    "Ideal {name} Situations for This Book",
    "Who Needs the {name} Edition?",
    "How {name} Educators Can Use This",
    "This {name} Book Works For",
    "Put the {name} Edition to Work For",
    "For {name}: Here's Who Benefits",
    "How to Use the {name} Practice Tests",
    "{name} Classrooms, Homes, and Tutoring",
    "Perfect Scenarios for {name}",
    "{name}: Where This Book Fits In",
    "Who's Using the {name} Edition?",
    "For {name} — Works Well For",
    "Who'll Love the {name} Edition?",
    "Here's Who Benefits in {name}",
    "Get the Most Out of the {name} Book",
    "For {name}: Ideal Situations",
    "{name} Edition — Great For",
    "How to Use This {name} Resource",
    "Put It to Work in {name}",
    "Who Can Use the {name} Practice Tests?",
    "{name}: Here's How to Use It",
]

# --- Use case bullet sets ---
USE_CASE_SETS = [
    [
        "Classroom test-prep sessions — work through one test per week leading up to the exam",
        "Independent homework — students practice on their own and check the answer key",
        "Tutoring sessions — pinpoint gaps and focus on specific skills",
        "Homeschool assessment — gauge Grade 7 math readiness",
        "After-school programs and math camps",
        "Summer review to keep skills sharp before Grade 8",
    ],
    [
        "Weekly test prep in the classroom — one test each week",
        "Homework packets for independent practice with built-in answers",
        "Tutoring — use specific tests to target weak areas",
        "Homeschool families who need a standardized assessment tool",
        "Test-prep workshops and after-school math programs",
        "Summer skill retention before the next school year",
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
        "Preparing your class for the state assessment",
        "Homework that students can check themselves",
        "One-on-one or small-group tutoring",
        "Homeschool math evaluation",
        "After-school programs and math intervention groups",
        "Summer bridge work between Grade 7 and Grade 8",
    ],
    [
        "Whole-class test prep — one practice test per session",
        "Take-home practice with the answer key for self-checking",
        "Diagnostic tool — use the first test to find gaps, the last to measure growth",
        "Homeschool families looking for real assessment practice",
        "Math tutoring and intervention programs",
        "Keeping skills fresh over summer break",
    ],
    [
        "Structured classroom test prep — schedule one test each week",
        "Independent student practice with full answer explanations",
        "Targeted tutoring — each test reveals what still needs work",
        "Homeschool math assessment and progress tracking",
        "Community programs and after-school tutoring",
        "Year-end review or summer prep",
    ],
    [
        "In-class exam prep leading up to test day",
        "Self-paced homework with detailed answer explanations",
        "Tutoring — zero in on weak spots using individual test results",
        "Homeschool testing and benchmarking",
        "After-school practice and math enrichment",
        "Summer math review to stay ready for Grade 8",
    ],
    [
        "Classroom warm-up or review before assessments",
        "Homework practice that students can self-correct",
        "Tutoring sessions — work through tests one at a time",
        "Monitoring progress in a homeschool setting",
        "Supplemental practice for after-school programs",
        "End-of-year review or summer preparation",
    ],
    [
        "Full-class practice sessions in the weeks before testing",
        "Independent study — students work at their own pace with the answer key",
        "Small-group instruction and tutoring",
        "Homeschool math portfolio evidence",
        "After-school math help and test anxiety reduction",
        "Summer skill maintenance",
    ],
    [
        "Weekly test prep sessions in the classroom",
        "Homework that comes with its own answer key — no extra grading",
        "Diagnostic and progress monitoring tool for tutors",
        "Homeschool assessment — standardized format, real test feel",
        "Extra practice for after-school or weekend programs",
        "Summer review to bridge Grade 7 and Grade 8",
    ],
]

# --- Series cross-sell headings ---
SERIES_HEADINGS = [
    "Want More {name} Math?",
    "Looking for More {name} Resources?",
    "Need {name} Lessons Too?",
    "Check Out the Full {name} Series",
    "More From the {name} Series",
    "Build a Complete {name} Math Library",
    "Explore the Full {name} Collection",
    "Other {name} Books in the Series",
    "There's More for {name}",
    "See What Else We've Got for {name}",
    "Go Beyond {name} Practice Tests",
    "Pair This With Other {name} Books",
    "Complete the {name} Set",
    "The Rest of the {name} Collection",
    "Expand Your {name} Math Toolkit",
    "Related {name} Resources",
    "{name}: Want More?",
    "More {name} Grade 7 Math",
    "The {name} Companion Books",
    "Make It a Full {name} Math Library",
    "{name} — Other Books in the Series",
    "Looking for More {name} Math?",
    "Complement This {name} Book With",
    "The Rest of the {name} Grade 7 Series",
    "{name}: Explore the Full Series",
    "More {name} Resources to Explore",
    "Other {name} Grade 7 Books",
    "For {name}: See the Full Series",
    "Get More {name} Math Resources",
    "The {name} Series Has More",
    "{name} Edition — See What Else We've Got",
    "More for {name} — The Full Series",
    "Add to Your {name} Math Collection",
    "{name}: More Books Available",
    "Explore More {name} Grade 7 Resources",
    "Want the Complete {name} Set?",
    "For {name} — There's More",
    "More {name} Math for Your Students",
    "The Complete {name} Grade 7 Math Series",
    "Beyond Practice Tests: The {name} Series",
    "Want Lessons for {name} Too?",
    "Other {name} Books to Explore",
    "{name} — Build the Full Set",
    "Expand the {name} Math Toolkit",
    "Check Out the Rest of the {name} series",
    "Your {name} Math Library, Expanded",
    "Keep Going With the {name} Series",
    "For {name}: There's a Whole Series",
    "See All {name} Grade 7 Math Books",
    "{name} — The Full Math Series",
]

# --- Series bullet sets ---
SERIES_SETS = [
    [
        "<b>All-in-One</b> — Full lessons, worked examples, and practice for every topic",
        "<b>Study Guide</b> — Key concepts, essential examples, and quick practice for review",
        "<b>Workbook</b> — Hundreds of practice problems organized by topic",
        "<b>Step-by-Step Guide</b> — Numbered steps for every problem type so students learn at their own pace",
        "<b>Math in 30 Days</b> — The entire curriculum in a 30-day daily lesson plan",
        "<b>Quizzes</b> — Quick 15-minute quizzes for every topic to track progress",
        "<b>Puzzles & Brain Teasers</b> — Games, riddles, and challenges that make math fun",
        "<b>Worksheets</b> — Standalone printable activities for any topic",
    ],
    [
        "<b>All-in-One</b> — The complete package with lessons, examples, and practice",
        "<b>Study Guide</b> — A quick-reference review of every key concept and example",
        "<b>Workbook</b> — Extra practice organized topic by topic",
        "<b>Step-by-Step Guide</b> — Clear numbered instructions for every type of problem",
        "<b>Math in 30 Days</b> — A one-month plan that covers everything",
        "<b>Quizzes</b> — Short assessments for every single topic",
        "<b>Puzzles & Brain Teasers</b> — Curriculum-aligned math games and challenges",
        "<b>Worksheets</b> — Print-and-use activities for any topic, any time",
    ],
    [
        "<b>All-in-One</b> — Lessons, examples, and practice problems all in one resource",
        "<b>Study Guide</b> — Condensed review with essential examples for every topic",
        "<b>Workbook</b> — Topic-by-topic practice with hundreds of problems",
        "<b>Step-by-Step Guide</b> — Guided solutions that walk students through each problem type",
        "<b>Math in 30 Days</b> — A daily study schedule covering the whole curriculum in one month",
        "<b>Quizzes</b> — 15-minute assessments per topic for regular progress checks",
        "<b>Puzzles & Brain Teasers</b> — Fun, standards-aligned math games to keep students engaged",
        "<b>Worksheets</b> — Individual printable worksheets ready for immediate use",
    ],
    [
        "<b>All-in-One</b> — Full instruction plus practice for every Grade 7 math topic",
        "<b>Study Guide</b> — Fast-track review with key concepts and sample problems",
        "<b>Workbook</b> — Page after page of focused practice, organized by topic",
        "<b>Step-by-Step Guide</b> — Problem-solving steps laid out clearly for every skill",
        "<b>Math in 30 Days</b> — Cover the entire Grade 7 math curriculum in 30 daily lessons",
        "<b>Quizzes</b> — Short, targeted quizzes for each topic",
        "<b>Puzzles & Brain Teasers</b> — Math games and challenges tied to the curriculum",
        "<b>Worksheets</b> — Printable, no-prep worksheets for any topic",
    ],
    [
        "<b>All-in-One</b> — Complete lessons and practice for every topic in one book",
        "<b>Study Guide</b> — Concise review — just the essentials for each topic",
        "<b>Workbook</b> — Tons of practice problems, sorted by topic",
        "<b>Step-by-Step Guide</b> — Breaks every problem type into clear, numbered steps",
        "<b>Math in 30 Days</b> — A structured 30-day plan through the whole curriculum",
        "<b>Quizzes</b> — Quick quizzes per topic for ongoing assessment",
        "<b>Puzzles & Brain Teasers</b> — Challenges and games that reinforce math skills",
        "<b>Worksheets</b> — Ready-to-print worksheets for any topic",
    ],
]

# --- CTA variations --- (use {name} and {exam} for uniqueness)
CTA_VARIATIONS = [
    ("Seven tests. 210 questions. Complete answer explanations. Your {name} students will be ready.",
     "Add this to your cart and give your students the practice they need."),
    ("With 7 full practice tests and detailed explanations, your {name} students will go into test day confident.",
     "Download it now — it's ready to print and use today."),
    ("By the time they finish all 7 tests, your {name} students will know exactly what to expect on test day.",
     "Get it now and start preparing your class."),
    ("210 questions of focused, {name}-aligned test prep. That's what this resource delivers.",
     "Add it to your cart and get started."),
    ("The more practice your {name} students get, the more confident they'll be. This book gives them plenty.",
     "Download, print, and put it to work in your classroom."),
    ("This is straightforward, effective {exam} test prep. No fluff, no filler — just 210 well-written practice questions.",
     "Start preparing your {name} students today."),
    ("Your {name} students deserve real practice. This gives them seven full tests to work through before the real thing.",
     "Add it to your library now."),
    ("Practice builds confidence. Seven tests and 210 questions later, your {name} students will be ready.",
     "Get it today — it's print-ready and waiting."),
    ("Seven chances to practice. 210 opportunities to learn. Every answer explained. That's what this gives your {name} students.",
     "Download it and give your students a head start."),
    ("If you want your {name} students prepared for test day, this book does the job.",
     "Add it to your cart — it's ready to go."),
    ("After seven practice tests, your {name} students will walk into the real exam knowing what to expect.",
     "Grab it now and give them that advantage."),
    ("This gives your {name} students the repetition and feedback they need to build real math confidence.",
     "Start today — download, print, and go."),
    ("Good {exam} test prep doesn't have to be complicated. Seven tests, clear explanations, and real questions.",
     "Download it now and let the practice begin."),
    ("Real practice for {name}. Seven full tests. Every answer explained. Your students will thank you.",
     "Get it now — it's ready to print."),
    ("Seven tests. 210 problems. Step-by-step explanations. That's effective {exam} test prep for {name}.",
     "Add it to your cart and start today."),
    ("This is the {exam} practice your {name} students need. Seven complete tests, 210 questions, full explanations.",
     "Download and start using it right away."),
    ("Your {name} Grade 7 students get seven full chances to practice before the real {exam}.",
     "Get it now and let the practice begin."),
    ("210 questions of real {exam} practice. That's a lot of chances to learn, grow, and build confidence.",
     "Download it today for your {name} classroom."),
    ("Give your {name} students the practice they're looking for. Seven tests, detailed answers, real preparation.",
     "Add it to your cart now."),
    ("Confidence comes from practice. This book gives your {name} students 210 questions worth of it.",
     "Download, print, and use today."),
    ("Seven {exam} practice tests. 210 questions. Detailed answer explanations. Your {name} students are covered.",
     "Get it and start preparing your class."),
    ("This is {name} {exam} prep that actually works. Seven full tests, clear explanations, real questions.",
     "Start today — add it to your cart."),
    ("After working through 7 tests, your {name} students will be more confident and better prepared.",
     "Download it now — no prep needed, just print and go."),
    ("210 questions. 7 tests. Step-by-step answers. This is what real {exam} prep looks like for {name}.",
     "Grab it today and get started."),
    ("Your {name} students need practice, and this gives them plenty — 210 questions across 7 full tests.",
     "Add it to your library and start today."),
    ("Seven tests, 210 questions, every answer explained — your {name} students will be ready for whatever comes next.",
     "Download it now."),
    ("This is the kind of practice that makes a difference. Seven full {exam} tests for your {name} students.",
     "Get it today — print-ready and waiting."),
    ("Prepare your {name} students for the {exam} with 210 real practice questions and full explanations.",
     "Add it to your cart and give your students a strong start."),
    ("Every answer explained. Every topic covered. Seven full tests for your {name} Grade 7 students.",
     "Download and start preparing today."),
    ("Practice, learn, repeat — that's the cycle this book creates. 7 {exam} tests for {name} students.",
     "Get it now and put it to work."),
    ("This is focused, no-nonsense {exam} prep. 210 questions across 7 tests for {name} Grade 7.",
     "Download it today."),
    ("Your {name} students get 210 questions of targeted {exam} practice with detailed explanations.",
     "Add it to your cart — it's ready to go."),
    ("Seven complete tests. 210 explained answers. That's solid {exam} preparation for any {name} Grade 7 student.",
     "Start today — download and print."),
    ("By test 7, your {name} students will know exactly what they're doing. Every answer explained along the way.",
     "Get it now and start practicing."),
    ("This is practice that matters. Seven {exam} tests for {name} — 210 questions with full answer explanations.",
     "Download it and let your students get to work."),
    ("Real questions, real explanations, real results. That's what 7 practice tests delivers for {name}.",
     "Add it to your cart today."),
    ("Seven tests. Every answer explained step by step. Your {name} Grade 7 students will be well-prepared.",
     "Download it now — print-ready and classroom-tested."),
    ("Give your {name} students 210 questions of solid {exam} practice. Every answer explained.",
     "Get it today and start preparing."),
    ("This is {name} {exam} test prep in its simplest form: 7 tests, 210 questions, full explanations.",
     "Add it to your cart and go."),
    ("Seven complete practice tests for {name} — that's 210 questions your students can learn from.",
     "Download and print it today."),
    ("210 practice questions. 7 full-length tests. Detailed explanations for every single answer. Made for {name}.",
     "Get it now — your students will thank you."),
    ("Your {name} students get seven shots at real {exam}-style practice. 210 questions, all answered step by step.",
     "Download it today and start."),
    ("The {exam} doesn't have to be a surprise. Give your {name} students 7 full practice tests.",
     "Get it and start preparing now."),
    ("Seven tests, 210 questions, and a complete answer key with explanations — that's {name} {exam} prep done right.",
     "Add it to your cart today."),
    ("This gives your {name} students exactly the practice they need. Seven full tests, every answer explained.",
     "Download it now and start preparing."),
    ("Good practice leads to good results. This book gives your {name} students 210 questions worth.",
     "Get it today — it's print-ready."),
    ("Seven full-length {exam} tests. 210 questions. Clear, step-by-step explanations. For {name} Grade 7.",
     "Add it to your cart and let the practice begin."),
    ("From the first question to the 210th, this book builds your {name} students' confidence one problem at a time.",
     "Download it and start today."),
    ("Real {exam} practice for {name}. 7 tests, 210 questions, every answer explained. That's what your students need.",
     "Get it now."),
    ("Your {name} students deserve good practice — and 210 questions across 7 tests gives them exactly that.",
     "Download, print, and go."),
]

# --- Section orderings (middle sections only; opening first, footer last) ---
# Keys: F=features, C=chapters, A=alignment, U=use_cases, S=series
# 50 unique orderings — one per state
SECTION_ORDERS = [
    ["F", "C", "A", "U", "S"],  # 0
    ["C", "F", "U", "A", "S"],  # 1
    ["A", "F", "C", "U", "S"],  # 2
    ["F", "A", "U", "C", "S"],  # 3
    ["C", "A", "F", "S", "U"],  # 4
    ["A", "C", "U", "F", "S"],  # 5
    ["F", "U", "C", "A", "S"],  # 6
    ["U", "F", "A", "C", "S"],  # 7
    ["C", "F", "A", "U", "S"],  # 8
    ["A", "F", "U", "C", "S"],  # 9
    ["F", "C", "U", "A", "S"],  # 10
    ["U", "C", "F", "A", "S"],  # 11
    ["C", "A", "U", "F", "S"],  # 12
    ["F", "A", "C", "U", "S"],  # 13
    ["A", "U", "F", "C", "S"],  # 14
    ["C", "U", "A", "F", "S"],  # 15
    ["F", "C", "A", "S", "U"],  # 16
    ["A", "C", "F", "U", "S"],  # 17
    ["U", "A", "C", "F", "S"],  # 18
    ["C", "F", "U", "S", "A"],  # 19
    ["F", "U", "A", "C", "S"],  # 20
    ["A", "U", "C", "F", "S"],  # 21
    ["U", "C", "A", "F", "S"],  # 22
    ["C", "U", "F", "A", "S"],  # 23
    ["F", "A", "C", "S", "U"],  # 24
    ["A", "C", "F", "S", "U"],  # 25
    ["C", "A", "U", "S", "F"],  # 26
    ["U", "F", "C", "A", "S"],  # 27
    ["F", "C", "S", "A", "U"],  # 28
    ["A", "F", "S", "U", "C"],  # 29
    ["C", "F", "A", "S", "U"],  # 30
    ["U", "A", "F", "C", "S"],  # 31
    ["F", "U", "S", "C", "A"],  # 32
    ["A", "C", "U", "S", "F"],  # 33
    ["C", "U", "F", "S", "A"],  # 34
    ["U", "F", "C", "S", "A"],  # 35
    ["F", "A", "U", "S", "C"],  # 36
    ["A", "U", "F", "S", "C"],  # 37
    ["C", "A", "F", "U", "S"],  # 38
    ["U", "C", "A", "S", "F"],  # 39
    ["F", "S", "C", "A", "U"],  # 40
    ["A", "F", "C", "S", "U"],  # 41
    ["C", "F", "S", "U", "A"],  # 42
    ["U", "A", "F", "S", "C"],  # 43
    ["F", "S", "U", "C", "A"],  # 44
    ["A", "S", "F", "C", "U"],  # 45
    ["C", "S", "A", "F", "U"],  # 46
    ["U", "S", "F", "A", "C"],  # 47
    ["F", "S", "A", "U", "C"],  # 48
    ["A", "S", "C", "U", "F"],  # 49
]

# ============================================================================
# GENERATORS
# ============================================================================

def get_chapters(s):
    """Return the chapter list for a state."""
    return s["chapters"] if s["chapters"] else STANDARD_CHAPTERS


def gen_features(s, idx):
    """Generate the features section HTML."""
    heading_i = idx % len(FEATURE_HEADINGS)
    set_i = idx % len(FEATURE_SETS)
    heading = FEATURE_HEADINGS[heading_i].format(name=s["name"], exam=s["exam"], topics=s["topics"])
    bullets = FEATURE_SETS[set_i]
    # Replace {topics} placeholder in bullets
    bullets = [b.format(topics=s["topics"]) for b in bullets]
    
    lines = []
    lines.append("<p></p>")
    lines.append(f'<p><b>{heading}</b></p>')
    lines.append("<ul>")
    for b in bullets:
        lines.append(f"<li>✅ {b}</li>")
    lines.append("</ul>")
    return "\n".join(lines)


def gen_chapters_table(s, idx):
    """Generate chapters as an HTML table."""
    chapters = get_chapters(s)
    heading_i = (idx + 3) % len(CHAPTER_HEADINGS)
    heading = CHAPTER_HEADINGS[heading_i].format(topics=s["topics"], name=s["name"])
    total = s["topics"]
    
    lines = []
    lines.append("<p></p>")
    lines.append(f'<p><b>{heading}</b></p>')
    lines.append("<table>")
    lines.append("<tbody>")
    for i, (name, count) in enumerate(chapters, 1):
        lines.append(f"<tr><td><b>Ch. {i}</b></td><td>{name}</td><td>{count} topics</td></tr>")
    lines.append(f"<tr><td></td><td><b>Total</b></td><td><b>{total} topics</b></td></tr>")
    lines.append("</tbody>")
    lines.append("</table>")
    return "\n".join(lines)


def gen_chapters_bullets(s, idx):
    """Generate chapters as a bullet list."""
    chapters = get_chapters(s)
    heading_i = (idx + 7) % len(CHAPTER_HEADINGS)
    heading = CHAPTER_HEADINGS[heading_i].format(topics=s["topics"], name=s["name"])
    total = s["topics"]
    
    lines = []
    lines.append("<p></p>")
    lines.append(f'<p><b>{heading}</b></p>')
    lines.append("<ul>")
    for i, (name, count) in enumerate(chapters, 1):
        lines.append(f"<li>✅ <b>Ch. {i}: {name}</b> — {count} topics</li>")
    lines.append("</ul>")
    lines.append(f"<p><b>Total: {total} topics</b></p>")
    return "\n".join(lines)


def gen_chapters(s, idx):
    """Generate chapters section — alternates between table and bullet list."""
    if idx % 3 == 0:
        return gen_chapters_table(s, idx)
    else:
        return gen_chapters_bullets(s, idx)


def gen_alignment(s, idx):
    """Generate the alignment section."""
    heading_i = (idx + 5) % len(ALIGNMENT_HEADINGS)
    para_i = idx % len(ALIGNMENT_PARAGRAPHS)
    heading = ALIGNMENT_HEADINGS[heading_i].format(name=s["name"])
    para = ALIGNMENT_PARAGRAPHS[para_i].format(
        name=s["name"], exam=s["exam"], topics=s["topics"]
    )
    
    lines = []
    lines.append("<p></p>")
    lines.append(f'<p><b>{heading}</b></p>')
    lines.append(f"<p>{para}</p>")
    return "\n".join(lines)


def gen_use_cases(s, idx):
    """Generate the use cases section."""
    heading_i = (idx + 2) % len(USE_CASE_HEADINGS)
    set_i = idx % len(USE_CASE_SETS)
    heading = USE_CASE_HEADINGS[heading_i].format(name=s["name"], exam=s["exam"])
    bullets = USE_CASE_SETS[set_i]
    
    lines = []
    lines.append("<p></p>")
    lines.append(f'<p><b>{heading}</b></p>')
    lines.append("<ul>")
    for b in bullets:
        lines.append(f"<li>✅ {b}</li>")
    lines.append("</ul>")
    return "\n".join(lines)


def gen_series(s, idx):
    """Generate the series cross-sell section."""
    heading_i = (idx + 4) % len(SERIES_HEADINGS)
    set_i = idx % len(SERIES_SETS)
    heading = SERIES_HEADINGS[heading_i].format(name=s["name"], exam=s["exam"])
    bullets = SERIES_SETS[set_i]
    
    lines = []
    lines.append("<p></p>")
    lines.append(f'<p><b>{heading}</b></p>')
    lines.append("<ul>")
    for b in bullets:
        lines.append(f"<li>✅ {b}</li>")
    lines.append("</ul>")
    return "\n".join(lines)


def gen_cta(s, idx):
    """Generate the closing CTA."""
    cta_i = idx % len(CTA_VARIATIONS)
    line1_tmpl, line2_tmpl = CTA_VARIATIONS[cta_i]
    line1 = line1_tmpl.format(name=s["name"], exam=s["exam"])
    line2 = line2_tmpl.format(name=s["name"], exam=s["exam"])
    
    lines = []
    lines.append("<p></p>")
    lines.append(f"<p>{line1}</p>")
    lines.append(f"<p><b>{line2}</b></p>")
    return "\n".join(lines)


def gen_opening(s, idx):
    """Generate the opening section."""
    style_i = idx % len(OPENING_STYLES)
    heading_html, intro_html = OPENING_STYLES[style_i](s)
    return f"{heading_html}\n{intro_html}"


SECTION_GENERATORS = {
    "F": gen_features,
    "C": gen_chapters,
    "A": gen_alignment,
    "U": gen_use_cases,
    "S": gen_series,
}


def generate_description(idx, s):
    """Generate a complete TPT description for one state."""
    parts = []
    
    # Opening (always first)
    parts.append(gen_opening(s, idx))
    
    # Middle sections in varied order
    order_i = idx % len(SECTION_ORDERS)
    order = SECTION_ORDERS[order_i]
    for section_key in order:
        gen_fn = SECTION_GENERATORS[section_key]
        parts.append(gen_fn(s, idx))
    
    # CTA
    parts.append(gen_cta(s, idx))
    
    # Footer (always last)
    parts.append("")
    parts.append(FOOTER)
    
    return "\n\n".join(parts)


def main():
    out_dir = "final_output/7_practice_tests"
    os.makedirs(out_dir, exist_ok=True)
    
    date_str = "2026-03-04"
    
    for idx, s in enumerate(STATES):
        html = generate_description(idx, s)
        filename = f"{s['slug']}_tpt_{date_str}.html"
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w") as f:
            f.write(html)
        print(f"  ✓ {filename}")
    
    print(f"\nDone! Generated {len(STATES)} TPT descriptions.")


if __name__ == "__main__":
    main()
