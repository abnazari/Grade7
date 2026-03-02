---
name: grade6_states_curriculum_research
description: Complete research on Grade 6 math standards across all 50 US states — which states need additional or modified topics beyond Common Core, and what exactly to add
---

# Grade 6 Math: US State Standards Research

## Purpose

This document is the **single source of truth** for state-by-state Grade 6 math curriculum alignment decisions.
It was compiled from three independent deep-research reports (OpenAI, Perplexity, Gemini) plus direct web research on official state standards sites (Florida B.E.S.T., Texas TEKS, Virginia SOL, Minnesota 2022, Nebraska CCR, Indiana IAS 2023, Oklahoma OAS, etc.).

The corresponding configuration lives in `topics_config.yaml` under the `states:` and `additional_topics:` sections.

---

## How the System Works

- **Core chapters** (ch01–ch05) cover Common Core State Standards (CCSS) and ship to every state.
- **Additional topics** (add-01 through add-13) are state-specific supplements. A state that lists `add-04` in its `additional:` field gets the "Introduction to Probability" topic appended to the relevant chapter.
- **Modified topics** are core topics that need a variant for certain states. The variant lives in `topics_modified/` instead of `topics/`.
- States with **no** `additional:` or `modified:` fields receive pure CCSS content.

---

## Classification of All 50 States

### States Fully Aligned with CCSS (No Modifications Needed) — 39 States

These states either adopted CCSS directly or rebranded it with negligible Grade 6 content changes:

Alabama, Arizona, Arkansas, California, Connecticut, Delaware, Hawaii, Idaho, Illinois, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Mississippi, Missouri, Montana, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oregon, Pennsylvania, Rhode Island, South Dakota, Tennessee, Utah, Vermont, Washington, West Virginia, Wisconsin, Wyoming

**Notes on "close call" states that remain pure CCSS:**

| State | Why it was considered | Why it stays CCSS |
|-------|----------------------|-------------------|
| Alabama | Gemini report: PFL legislation for HS | Grade 6 content unchanged; PFL mandate is for high school courses |
| Arizona | Gemini: rebranded as "Arizona Math Standards" | Content identical to CCSS; only branding changed |
| Idaho | Gemini: HS financial literacy | Mandate is HS, not Grade 6 |
| Louisiana | Gemini: LSSM simplified CCSS language | Language changes, not content additions |
| Missouri | Gemini: cursive integration | ELA/handwriting requirement, not math content |
| New York | Gemini: "Next Generation" branding | Content remains CCSS; "explore" vs "master" is pedagogy |
| Pennsylvania | Gemini: domain reorganization | Same content reorganized into 4 instead of 5 domains |
| Tennessee | Gemini: wording from "know" to "explain" | Depth-of-knowledge change, not topic content |

### States Requiring Additional/Modified Topics — 11 States

| State | Standards Name | Key Divergences from CCSS |
|-------|---------------|--------------------------|
| Alaska | Alaska GL | Integer context emphasis, extended data displays |
| Colorado | Colorado Academic Standards (CAS) | Mandatory Personal Financial Literacy at Grade 6 |
| Florida | B.E.S.T. 2023 | Integer ops, financial literacy, probability, stem-and-leaf |
| Georgia | Georgia K-12 Math 2023 | Probability introduced at Grade 6 |
| Indiana | IAS 2023 | Transformations, data displays, probability, circles |
| Minnesota | MN 2022 | Probability, PFL, circle graphs, proportional reasoning, circles |
| Nebraska | NE CCR 2022 | Probability, circle geometry |
| Oklahoma | OAS-M 2022 | PFL, stem-and-leaf, integer ops, scale drawings, probability |
| South Carolina | SCCCR 2023 | Integer operations in Grade 6 |
| Texas | TEKS §111.26 | Integer ops, PFL, proportional/non-proportional, stem-and-leaf |
| Virginia | 2023 SOL | Integer ops, probability, circle graphs, transformations, circles |

---

## Available Additional Topics (add-01 through add-13)

These 13 topics cover **every** content gap identified across all 50 states. No new additional topics are needed.

| ID | Name | Chapter | Required By |
|----|------|---------|-------------|
| add-01 | Integer Addition and Subtraction | 2 | FL, MN, OK, SC, TX, VA |
| add-02 | Integer Multiplication and Division | 2 | FL, OK, SC, TX, VA |
| add-03 | Personal Financial Literacy | 1 | CO, FL, MN, OK, TX |
| add-04 | Introduction to Probability | 5 | FL, GA, IN, MN, NE, OK, VA |
| add-05 | Stem-and-Leaf Plots | 5 | FL, OK, TX |
| add-06 | Circle Graphs | 5 | MN, VA |
| add-07 | Proportional vs. Non-Proportional | 1 | MN, TX |
| add-08 | Transformations on the Coordinate Plane | 4 | IN, VA |
| add-09 | Financial Literacy — Budgeting and Saving | 1 | CO, TX |
| add-10 | Compute with Integers in Context | 2 | AK |
| add-11 | Data Displays Extended | 5 | AK, IN, OK |
| add-12 | Area of Circles Introduction | 4 | IN, MN, NE, VA |
| add-13 | Ratios with Scale Drawings | 1 | OK |

---

## Detailed State Profiles

### Alaska (AK)
**Standards:** Alaska English/Language Arts and Mathematics Standards (never adopted CCSS)
**Key differences:** Heavier measurement emphasis; integer context; extended data displays; culturally responsive Alaskan contexts.

```yaml
alaska:
  name: Alaska
  modified:
    - ch02-06-understanding-positive-and-negative-numbers
    - ch05-03-mean-and-median
    - ch05-07-summarizing-data-and-making-comparisons
  additional:
    - add-10-compute-with-integers-in-context
    - add-11-data-displays-extended
```

**Sources:** OpenAI report (Alaska Dept. of Ed.); Gemini report (ref 21: Alaska standards comparison doc)

---

### Colorado (CO)
**Standards:** Colorado Academic Standards (CAS) 2020 — adopted CCSS but integrated unique "21st Century Skills" including mandatory PFL.
**Key differences:** Grade 6 has a dedicated Personal Financial Literacy standard (Standard 4) covering insurance, interest on savings, budgeting, and ethical financial decision-making.

```yaml
colorado:
  name: Colorado
  additional:
    - add-03-personal-financial-literacy
    - add-09-financial-literacy-budgeting-and-saving
```

**Sources:** Gemini report (refs 10, 13: CDE math standards Grade 6); CDE 2020 CAS Standard 4 documentation

---

### Florida (FL)
**Standards:** Benchmarks for Excellent Student Thinking (B.E.S.T.) — replaced CCSS in 2020.
**Key differences:** All four integer operations at Grade 6; financial literacy with simple interest; probability; stem-and-leaf plots; prime factorization emphasis.

```yaml
florida:
  name: Florida
  modified:
    - ch02-06-understanding-positive-and-negative-numbers
    - ch02-07-opposites-and-absolute-value
    - ch05-05-dot-plots-and-histograms
    - ch05-07-summarizing-data-and-making-comparisons
  additional:
    - add-01-integer-addition-and-subtraction
    - add-02-integer-multiplication-and-division
    - add-03-personal-financial-literacy
    - add-04-introduction-to-probability
    - add-05-stem-and-leaf-plots
```

**Sources:** Florida B.E.S.T. standards document (MA.6.NSO.4, MA.6.DP); Perplexity (refs 12-16); Gemini (ref 11); mathtechconnections.com 6th grade B.E.S.T. breakdown confirming MA.6.NSO.4.1 (integer add/sub) and MA.6.NSO.4.2 (integer mult/div)

---

### Georgia (GA)
**Standards:** Georgia K-12 Mathematics Standards (revised 2021, implemented 2023) — "Georgia-owned and grown."
**Key differences:** Statistical Reasoning Framework; simple theoretical probability added to Grade 6.

```yaml
georgia:
  name: Georgia
  additional:
    - add-04-introduction-to-probability
```

**Sources:** Perplexity report ("Simple theoretical probability is required in 6th grade"); Gemini report (refs 19, 24: Georgia standards changes, Progress Learning analysis)

---

### Indiana (IN)
**Standards:** Indiana Academic Standards (IAS) 2023 — repealed CCSS in 2014.
**Key differences:** Transformations on coordinate plane (6.GM.5); data displays extended; probability and mutually exclusive events; circumference and area of circles (6.GM.4); fraction-decimal-percent conversion without calculator.

```yaml
indiana:
  name: Indiana
  modified:
    - ch04-04-polygons-on-the-coordinate-plane
    - ch05-05-dot-plots-and-histograms
    - ch05-07-summarizing-data-and-making-comparisons
  additional:
    - add-04-introduction-to-probability
    - add-08-transformations-on-the-coordinate-plane
    - add-11-data-displays-extended
    - add-12-area-of-circles-introduction
```

**Sources:** Perplexity report (circle geometry, transformations, probability); Gemini report (refs 25-27: IAS-CCSS correlation guide, Indiana standards comparison); IN.gov Grade 6 Math 2023 IAS-CCSS Correlation Guide

---

### Minnesota (MN)
**Standards:** Minnesota K-12 Academic Standards in Mathematics 2022 — rejected CCSS math, kept CCSS ELA.
**Key differences:** Four strands (Number/Operation, Algebra, Geometry/Measurement, Data Analysis/Probability); probability at Grade 6; circle area/circumference; financial literacy; proportional reasoning; circle graphs.

```yaml
minnesota:
  name: Minnesota
  modified:
    - ch01-07-what-is-a-percent
    - ch02-06-understanding-positive-and-negative-numbers
    - ch05-05-dot-plots-and-histograms
    - ch05-07-summarizing-data-and-making-comparisons
  additional:
    - add-01-integer-addition-and-subtraction
    - add-03-personal-financial-literacy
    - add-04-introduction-to-probability
    - add-06-circle-graphs
    - add-07-proportional-vs-non-proportional
    - add-12-area-of-circles-introduction
```

**Sources:** Perplexity (refs 17-20: MN standards PDFs, grade guides); Gemini (refs 30-31: MN academic standards); MN 2022 Mathematics Standards Final Version; stemtc.scimathmn.org

---

### Nebraska (NE)
**Standards:** Nebraska College and Career Ready Standards for Mathematics 2022 — never adopted CCSS.
**Key differences:** Probability (theoretical, experimental, sample spaces) at Grade 6; circle geometry (circumference, area); strong number sense emphasis.

```yaml
nebraska:
  name: Nebraska
  additional:
    - add-04-introduction-to-probability
    - add-12-area-of-circles-introduction
```

**Sources:** Perplexity ("Theoretical probability, experimental probability, and sample spaces must be explicitly taught"; "Geometry must include circle formulas"); Gemini (ref 35: Nebraska standards comparison); OpenAI report (NE alignment study)

---

### Oklahoma (OK)
**Standards:** Oklahoma Academic Standards (OAS) 2022 — repealed CCSS.
**Key differences:** Financial literacy; stem-and-leaf plots; integer operations; scale drawings; probability (likelihood as fraction/decimal/percent).

```yaml
oklahoma:
  name: Oklahoma
  modified:
    - ch01-09-solving-rate-and-ratio-word-problems
    - ch02-06-understanding-positive-and-negative-numbers
    - ch05-05-dot-plots-and-histograms
    - ch05-07-summarizing-data-and-making-comparisons
  additional:
    - add-01-integer-addition-and-subtraction
    - add-02-integer-multiplication-and-division
    - add-03-personal-financial-literacy
    - add-04-introduction-to-probability
    - add-05-stem-and-leaf-plots
    - add-11-data-displays-extended
    - add-13-ratios-with-scale-drawings
```

**Sources:** Gemini (refs 39-40: OAS Grade 6 standards, Oklahoma family guide); Perplexity ("Probability is heavily featured"); OK Academic Standards official doc

---

### South Carolina (SC)
**Standards:** South Carolina College- and Career-Ready Standards (SCCCR) 2023 — repealed CCSS.
**Key differences:** Integer operations (all four) required at Grade 6; heavy emphasis on fraction-decimal-percent conversion fluency.

```yaml
south-carolina:
  name: South Carolina
  additional:
    - add-01-integer-addition-and-subtraction
    - add-02-integer-multiplication-and-division
```

**Sources:** Perplexity ("Adding, subtracting, multiplying, and dividing integers are all expected in 6th grade"); Gemini (refs 43-44: SC assessment specs, Progress Learning analysis)

---

### Texas (TX)
**Standards:** Texas Essential Knowledge and Skills (TEKS) §111.26 — never adopted CCSS.
**Key differences:** Robust Personal Financial Literacy strand (checking accounts, debit vs credit, credit history); integer operations; proportional vs non-proportional reasoning; stem-and-leaf plots; seven Mathematical Process Standards.

```yaml
texas:
  name: Texas
  modified:
    - ch01-04-finding-the-unit-rate
    - ch01-07-what-is-a-percent
    - ch01-08-solving-percent-problems
    - ch02-06-understanding-positive-and-negative-numbers
    - ch02-07-opposites-and-absolute-value
    - ch05-05-dot-plots-and-histograms
    - ch05-06-box-plots
    - ch05-07-summarizing-data-and-making-comparisons
  additional:
    - add-01-integer-addition-and-subtraction
    - add-02-integer-multiplication-and-division
    - add-03-personal-financial-literacy
    - add-05-stem-and-leaf-plots
    - add-07-proportional-vs-non-proportional
    - add-09-financial-literacy-budgeting-and-saving
```

**Sources:** Perplexity (refs 4-6: TEKS crosswalk, TEKS snapshot); Gemini (refs 47-49: TEKS process standards, Kaplinsky comparison); TEA Grade 6 TEKS documentation; Fordham Institute review (rated Texas math "Strong" — 9/10)

---

### Virginia (VA)
**Standards:** Standards of Learning (SOL) 2023 — long-standing non-adopter of CCSS.
**Key differences:** Integer operations (all four); probability (theoretical and experimental); circle graphs; transformations on coordinate plane; area of circles / circumference / pi; non-dictated methodology.

```yaml
virginia:
  name: Virginia
  modified:
    - ch02-06-understanding-positive-and-negative-numbers
    - ch02-07-opposites-and-absolute-value
    - ch04-04-polygons-on-the-coordinate-plane
    - ch05-05-dot-plots-and-histograms
    - ch05-07-summarizing-data-and-making-comparisons
  additional:
    - add-01-integer-addition-and-subtraction
    - add-02-integer-multiplication-and-division
    - add-04-introduction-to-probability
    - add-06-circle-graphs
    - add-08-transformations-on-the-coordinate-plane
    - add-12-area-of-circles-introduction
```

**Sources:** Perplexity (refs 7-11: VA SOL, IXL Virginia alignment, virginiaisforteachers.com); Gemini (refs 50-52: SOL documentation, ERIC comparison study); VA DOE 2023 SOL Grade 6

---

## Research Sources Summary

### Reports Used

1. **OpenAI Deep Research Report** (`deep-research-report-openai.md`) — Conservative analysis. Identified only AK, FL, NE as needing changes. Good for confirming which states are truly CCSS-aligned.
2. **Perplexity Deep Research Report** (`deep-research-report-openai-preplexity.md`) — Identified 9 outlier states (TX, VA, FL, IN, NE, OK, SC, MN, GA + AK). Most detailed on specific topic gaps.
3. **Gemini Deep Research Report** (`deep-research-report-openai-gemini.md`) — Broadest analysis. Identified 19 states with some form of deviation. Most detailed on FL B.E.S.T., IN IAS, and TX TEKS. Many of the 19 turned out to be pedagogy/branding changes, not content.

### Cross-Reference Methodology

A state was flagged for `additional` or `modified` topics only when:
- **At least 2 of 3 reports** agreed on a substantive content difference, OR
- **1 report** identified it AND official state standards documentation confirmed it via web research

States flagged by only one report for non-content differences (pedagogy, branding, organizational structure) were kept as pure CCSS.

### Key Official Sources Consulted (via web fetch)

- Florida B.E.S.T. Standards: `fldoe.org`, `mathtechconnections.com/florida-best-standards/6th-grade/`
- Texas TEKS: `tea.texas.gov` crosswalk documents
- Virginia SOL: `doe.virginia.gov` 2023 SOL Grade 6
- Nebraska CCR: `education.ne.gov/math/` (2022 standards)
- Minnesota: `stemtc.scimathmn.org` (2022 Mathematics Standards Final Version)
- Fordham Institute: `fordhaminstitute.org` — "State of State Standards Post-Common Core" (comparative ratings)

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-03-01 | Initial research and cross-referencing of 3 reports | Baseline state alignment |
| 2026-03-02 | Finalized plan: 11 states with modifications, 39 pure CCSS | Consensus across reports + web verification |

---

## Pending Changes to `topics_config.yaml`

The following changes have been **planned but not yet applied**:

### Updates to Existing States

| State | Current Additional | Add | Result |
|-------|-------------------|-----|--------|
| Indiana | add-08, add-11 | **add-04, add-12** | add-04, add-08, add-11, add-12 |
| Minnesota | add-01, add-03, add-04, add-06, add-07 | **add-12** | add-01, add-03, add-04, add-06, add-07, add-12 |
| Oklahoma | add-01, add-02, add-03, add-05, add-11, add-13 | **add-04** | add-01, add-02, add-03, add-04, add-05, add-11, add-13 |

### New State Configurations

| State | Additional Topics |
|-------|------------------|
| Colorado | add-03, add-09 |
| Georgia | add-04 |
| Nebraska | add-04, add-12 |
| South Carolina | add-01, add-02 |

### States Unchanged (already correct in config)

Alaska, Florida, Texas, Virginia — no changes needed.
