````skill
---
name: grade7_states_curriculum_research
description: Complete research on Grade 7 math standards across all 50 US states — which states need additional or modified topics beyond Common Core, and what exactly to add
---

# Grade 7 Math: US State Standards Research

## Purpose

This document is the **single source of truth** for state-by-state Grade 7 math curriculum alignment decisions.
It was compiled from three independent deep-research reports (ChatGPT, Perplexity, Gemini) plus direct web research on official state standards sites (Florida B.E.S.T., Texas TEKS, Virginia SOL, Minnesota 2022, Oklahoma OAS-M 2022, Indiana IAS 2023, Alaska GL, etc.).

The corresponding configuration lives in `topics_config.yaml` under the `states:`, `additional_topics:`, and `modified_topics:` sections.

---

## How the System Works

- **Core chapters** (ch01–ch09) cover Common Core State Standards (CCSS) and ship to every state.
- **Additional topics** (ch01-07, ch02-08, ch02-09, etc.) are state-specific supplements. A state that lists `ch02-08-personal-financial-literacy` in its `additional:` field gets that topic appended after the last core topic in Chapter 2.
- **Modified topics** are core topics that need a variant for certain states. The variant lives in `topics_modified/` instead of `topics/`.
- States with **no** `additional:` or `modified:` fields receive pure CCSS content.
- Additional topic IDs use the format `chXX-YY` where XX is the chapter number and YY is the next available topic number after the last core topic in that chapter.

---

## Classification of All 50 States

### States Fully Aligned with CCSS (No Modifications Needed) — 43 States

These states either adopted CCSS directly or rebranded it with negligible Grade 7 content changes:

Alabama, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Georgia, Hawaii, Idaho, Illinois, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Utah, Vermont, Washington, West Virginia, Wisconsin, Wyoming

**Notes on "close call" states that remain pure CCSS:**

| State | Why it was considered | Why it stays CCSS |
|-------|----------------------|-------------------|
| Colorado | Grade 7 has PFL mandate | PFL requirement impacts Grade 7, not Grade 7 math content |
| Georgia | Grade 7 divergence for probability | Grade 7 aligns well with CCSS; probability fully covered in ch09 |
| Nebraska | Grade 7 divergence for probability/circles | Grade 7 CCSS covers probability (ch09) and circles (ch07) natively |
| South Carolina | Grade 7 integer ops | By Grade 7 CCSS already covers all integer/rational operations in ch03 |
| New York | "Next Generation" branding | Content remains CCSS; pedagogical language changes only |
| Pennsylvania | Domain reorganization | Same content reorganized; no topic additions |

### States Requiring Additional/Modified Topics — 7 States

| State | Standards Name | Key Divergences from CCSS |
|-------|---------------|--------------------------|
| Alaska | Alaska GL | Culturally responsive rational-number contexts, extended data displays |
| Florida | B.E.S.T. 2023 | Exponent laws, cylinder SA/volume, stem-and-leaf plots, circle graphs |
| Indiana | IAS 2023 | Transformations on coordinate plane, extended data displays |
| Minnesota | MN 2007/2022 | Personal financial literacy, circle graphs, percent emphasis |
| Oklahoma | OAS-M 2022 | PFL, stem-and-leaf plots, data displays, scale models |
| Texas | TEKS §111.27 | PFL, budgeting/investing, compound interest, stem-and-leaf, circle graphs, similar figures |
| Virginia | 2023 SOL | Transformations, square roots, exponent laws, scientific notation, cylinders, similar figures, stem-and-leaf, circle graphs |

---

## Available Additional Topics (14 topics)

These 14 topics cover **every** content gap identified across all 50 states. No new additional topics are needed.

| ID | Name | Chapter | Required By |
|----|------|---------|-------------|
| ch01-07 | Proportional Reasoning with Scale Models | 1 | OK |
| ch02-08 | Personal Financial Literacy | 2 | MN, OK, TX |
| ch02-09 | Financial Literacy — Budgeting, Saving, and Investing | 2 | TX |
| ch02-10 | Compound Interest Introduction | 2 | TX |
| ch03-09 | Introduction to Square Roots | 3 | VA |
| ch03-10 | Rational Number Operations in Extended Contexts | 3 | AK |
| ch03-11 | Introduction to Scientific Notation | 3 | VA |
| ch04-07 | Laws of Exponents | 4 | FL, VA |
| ch06-07 | Transformations on the Coordinate Plane | 6 | IN, VA |
| ch06-08 | Similar Figures and Proportions | 6 | TX, VA |
| ch07-07 | Cylinder Surface Area and Volume | 7 | FL, VA |
| ch08-05 | Stem-and-Leaf Plots | 8 | FL, OK, TX, VA |
| ch08-06 | Circle Graphs | 8 | FL, MN, TX, VA |
| ch08-07 | Data Displays Extended | 8 | AK, IN, OK |

---

## Available Modified Topics (11 entries)

These are core topics that use a variant file for certain states, loaded from `topics_modified/` instead of `topics/`.

| Core ID | File Slug | States | What Changed |
|---------|-----------|--------|--------------|
| ch01-06 | ch01-06-applying-proportional-reasoning | OK | OAS-M estimation emphasis — adds estimation as a fifth strategy; estimate-first step and reasonableness check in every problem |
| ch02-01 | ch02-01-solving-percent-problems | MN | MN percent-application emphasis — adds financial contexts for percent problems (discount, markup, tax, tip) |
| ch02-06 | ch02-06-simple-interest | FL, TX | Financial literacy emphasis — expands I = Prt with savings account comparisons, loan interest, real-world financial decisions |
| ch03-01 | ch03-01-integers-and-their-opposites | VA | VA SOL rational number emphasis — expands ordering, comparison, and number-line contexts with inequality symbols |
| ch03-08 | ch03-08-solving-real-world-problems-with-rational-numbers | AK | Culturally responsive Alaskan contexts — Alaska temperatures, fisheries data, elevation changes, subsistence economy |
| ch06-03 | ch06-03-drawing-geometric-figures | IN | IAS 2023 construction emphasis — justifying each step in geometric constructions; technology-based methods |
| ch06-06 | ch06-06-angle-relationships | VA | VA SOL extended angle emphasis — adds congruence/similarity connections, multi-step algebraic angle problems |
| ch08-01 | ch08-01-populations-and-samples | OK, TX | Experimental design emphasis — adds designing experiments and collecting data as precursors to sampling |
| ch08-03 | ch08-03-comparing-two-populations-visually | FL, IN, MN, VA | Multiple display emphasis — adds stem-and-leaf plots, circle graphs, frequency tables to visual comparisons |
| ch08-04 | ch08-04-comparing-populations-with-measures | AK, OK, TX | Extended measures emphasis — de-emphasises MAD in favour of IQR and range; localised/financial data contexts |
| ch09-03 | ch09-03-experimental-probability | FL, TX | Simulation emphasis — adds simulation design, random-number generators, frequency tables for comparing experimental vs theoretical |

---

## Detailed State Profiles

### Alaska (AK)
**Standards:** Alaska English/Language Arts and Mathematics Standards (never adopted CCSS)
**Key differences:** Culturally responsive Alaskan contexts for rational number applications; extended data displays; emphasis on estimation and verbal justification.

```yaml
alaska:
  name: Alaska
  modified:
    - ch03-08-solving-real-world-problems-with-rational-numbers
    - ch08-04-comparing-populations-with-measures
  additional:
    - ch03-10-rational-number-operations-in-extended-contexts
    - ch08-07-data-displays-extended
```

**Sources:** OpenAI report (Alaska Dept. of Ed.); Gemini report; Alaska standards comparison documents

---

### Florida (FL)
**Standards:** Benchmarks for Excellent Student Thinking (B.E.S.T.) 2023 — replaced CCSS in 2020.
**Key differences:** Laws of exponents (MA.7.NSO.1.1); cylinder surface area and volume (MA.7.GR.2.1–2.3); stem-and-leaf plots (MA.7.DP.1.1); circle graphs (MA.7.DP.1.4); simulation design for probability (MA.7.DP.2.4). Note: transformations are B.E.S.T. Grade 8, NOT Grade 7. Compound interest is NOT required at Grade 7.

```yaml
florida:
  name: Florida
  modified:
    - ch02-06-simple-interest
    - ch08-03-comparing-two-populations-visually
    - ch09-03-experimental-probability
  additional:
    - ch04-07-laws-of-exponents
    - ch07-07-cylinder-surface-area-and-volume
    - ch08-05-stem-and-leaf-plots
    - ch08-06-circle-graphs
```

**Sources:** All 34 B.E.S.T. Grade 7 benchmarks verified (MA.7.NSO, MA.7.AR, MA.7.GR, MA.7.DP); CPALMS; mathtechconnections.com; Perplexity report; Gemini report

**Critical corrections from web research:**
- Transformations (previously included) are B.E.S.T. Grade 8 — removed
- Compound interest (previously included) is not in B.E.S.T. Grade 7 — removed
- PFL is not a separate B.E.S.T. strand at Grade 7 — removed as standalone additional topic

---

### Indiana (IN)
**Standards:** Indiana Academic Standards (IAS) 2023 — repealed CCSS in 2014.
**Key differences:** Transformations on coordinate plane earlier than CCSS Grade 8; extended data displays (frequency tables, double bar graphs, line graphs); construction emphasis in geometry.

```yaml
indiana:
  name: Indiana
  modified:
    - ch06-03-drawing-geometric-figures
    - ch08-03-comparing-two-populations-visually
  additional:
    - ch06-07-transformations-on-the-coordinate-plane
    - ch08-07-data-displays-extended
```

**Sources:** Perplexity report; Gemini report; IAS 2023 Grade 7 Mathematics standards; IAS-CCSS Correlation Guide

---

### Minnesota (MN)
**Standards:** Minnesota K-12 Academic Standards in Mathematics 2022 — rejected CCSS math.
**Key differences:** Four-strand structure (Number/Operation, Algebra, Geometry/Measurement, Data Analysis/Probability); personal financial literacy integrated into percent applications; circle graphs for data display; stronger percent-to-money context connections.

```yaml
minnesota:
  name: Minnesota
  modified:
    - ch02-01-solving-percent-problems
    - ch08-03-comparing-two-populations-visually
  additional:
    - ch02-08-personal-financial-literacy
    - ch08-06-circle-graphs
```

**Sources:** Perplexity report; Gemini report; MN 2022 Mathematics Standards Final Version; stemtc.scimathmn.org

---

### Oklahoma (OK)
**Standards:** Oklahoma Academic Standards (OAS-M) 2022 — repealed CCSS.
**Key differences:** Personal financial literacy (context emphasis in percent applications); stem-and-leaf plots; extended data displays; proportional reasoning with scale models; estimation emphasis throughout proportional reasoning.

```yaml
oklahoma:
  name: Oklahoma
  modified:
    - ch01-06-applying-proportional-reasoning
    - ch08-01-populations-and-samples
    - ch08-04-comparing-populations-with-measures
  additional:
    - ch01-07-proportional-reasoning-with-scale-models
    - ch02-08-personal-financial-literacy
    - ch08-05-stem-and-leaf-plots
    - ch08-07-data-displays-extended
```

**Sources:** Gemini report; OAS-M Grade 7 standards; Oklahoma family guide documents

**Note:** PFL is technically a separate Grades 10–12 subject in Oklahoma, but financial contexts ARE emphasised in OAS-M percent and proportional reasoning applications at Grade 7.

---

### Texas (TX)
**Standards:** Texas Essential Knowledge and Skills (TEKS) §111.27 — never adopted CCSS. Adopted 2012, revised 2024.
**Key differences:** Robust Personal Financial Literacy strand (sales tax, income tax, budgeting, saving, net worth); compound interest; similar figures and triangles; stem-and-leaf plots; circle graphs; experimental design emphasis in statistics.

```yaml
texas:
  name: Texas
  modified:
    - ch02-06-simple-interest
    - ch08-01-populations-and-samples
    - ch08-04-comparing-populations-with-measures
    - ch09-03-experimental-probability
  additional:
    - ch02-08-personal-financial-literacy
    - ch02-09-financial-literacy-budgeting-saving-and-investing
    - ch02-10-compound-interest-introduction
    - ch06-08-similar-figures-and-proportions
    - ch08-05-stem-and-leaf-plots
    - ch08-06-circle-graphs
```

**Sources:** Khan Academy TX Grade 7 units; Perplexity report (TEKS crosswalk); Gemini report; TEA Grade 7 TEKS documentation

---

### Virginia (VA)
**Standards:** Standards of Learning (SOL) 2023 — long-standing non-adopter of CCSS.
**Key differences:** Transformations on coordinate plane (SOL Unit 5); similar figures and quadrilaterals (Unit 6); cylinder surface area and volume (Unit 7); square roots, exponent laws, and scientific notation (Unit 8); stem-and-leaf plots (Unit 9); rational number emphasis with ordering/comparison using inequality symbols.

```yaml
virginia:
  name: Virginia
  modified:
    - ch03-01-integers-and-their-opposites
    - ch06-06-angle-relationships
    - ch08-03-comparing-two-populations-visually
  additional:
    - ch03-09-introduction-to-square-roots
    - ch03-11-introduction-to-scientific-notation
    - ch04-07-laws-of-exponents
    - ch06-07-transformations-on-the-coordinate-plane
    - ch06-08-similar-figures-and-proportions
    - ch07-07-cylinder-surface-area-and-volume
    - ch08-05-stem-and-leaf-plots
    - ch08-06-circle-graphs
```

**Sources:** Khan Academy VA Grade 7 units (9 units confirmed); Perplexity report; Gemini report; VA DOE 2023 SOL Grade 7

---

## Research Sources Summary

### Reports Used

1. **ChatGPT Deep Research Report** (`deep-research-report-chatgpt.md`) — Conservative analysis. Identified only TX and VA as clearly divergent. Good for confirming which states are truly CCSS-aligned.
2. **Perplexity Deep Research Report** (`deep-research-report-perplexity.md`) — Moderate analysis. Identified AK, FL, IN, MN, OK, TX, VA as requiring changes. Most detailed on specific topic gaps.
3. **Gemini Deep Research Report** (`deep-research-report-gemini.md`) — Broadest analysis. Most aggressive in identifying divergences. Many flagged states turned out to be pedagogy/branding changes, not content.

### Cross-Reference Methodology

A state was flagged for `additional` or `modified` topics only when:
- **At least 2 of 3 reports** agreed on a substantive content difference, OR
- **1 report** identified it AND official state standards documentation confirmed it via web research

States flagged by only one report for non-content differences (pedagogy, branding, organizational structure) were kept as pure CCSS.

### Key Official Sources Consulted (via web research)

- Florida B.E.S.T. Standards: `fldoe.org`, CPALMS, mathtechconnections.com (all 34 Grade 7 benchmarks verified)
- Texas TEKS: `tea.texas.gov`, Khan Academy TX Grade 7
- Virginia SOL: `doe.virginia.gov`, Khan Academy VA Grade 7 (9 units verified)
- Minnesota: `stemtc.scimathmn.org` (2022 Mathematics Standards Final Version)
- Oklahoma: OAS-M 2022 official standards document
- Indiana: IAS 2023 Grade 7 Mathematics, IAS-CCSS Correlation Guide
- Alaska: Alaska Dept. of Education standards documentation

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-03-01 | Initial research and cross-referencing of 3 reports | Baseline state alignment |
| 2026-03-02 | Finalized: 7 states with modifications, 43 pure CCSS | Consensus across reports + web verification |
| 2026-03-02 | FL corrections: removed transformations, compound interest, PFL standalone | Verified against all 34 B.E.S.T. benchmarks |
| 2026-03-02 | Added modified_topics section (11 entries) | Match Grade 7 format |
| 2026-03-02 | Renamed additional topic IDs from add-XX to chXX-YY format | Script compatibility — Python scripts need chapter placement info encoded in ID |

````
