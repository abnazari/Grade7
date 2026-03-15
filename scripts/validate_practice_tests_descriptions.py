#!/usr/bin/env python3
"""Validate all practice_tests_bundle HTML descriptions."""

import os
import re
import glob

base = "final_output/bundles/practice_tests_bundle"
htmls = sorted(glob.glob(os.path.join(base, "*_tpt_bundle.html")))
print(f"Total HTML files: {len(htmls)}")

errors = []
for f in htmls:
    slug = os.path.basename(f).replace("_tpt_bundle.html", "")
    with open(f, "r") as fh:
        content = fh.read()

    # Check forbidden elements
    for tag in ["<h1", "<h2", "<h3", "<hr", "<br", "<div", "<span"]:
        if tag in content.lower():
            errors.append(f"{slug}: contains forbidden {tag}")

    # Check HTML comments at top
    lines = content.strip().split("\n")
    if not lines[0].startswith("<!--"):
        errors.append(f"{slug}: missing HTML comments at top")

    comment_count = sum(1 for l in lines[:3] if l.strip().startswith("<!--"))
    if comment_count < 3:
        errors.append(f"{slug}: fewer than 3 HTML comment lines at top")

    # Check footer
    if "\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605\u2605" not in content:
        errors.append(f"{slug}: missing star footer")
    if "dr.nazari@viewmath.com" not in content:
        errors.append(f"{slug}: missing email in footer")
    if "Dr. A. Nazari" not in content:
        errors.append(f"{slug}: missing Dr. A. Nazari")

    # Check practice test uniqueness mentioned at least twice
    unique_mentions = len(
        re.findall(
            r"unique|non-overlapping|no repeat|zero repeat|no overlap|not.*repeat|zero overlap|never repeat",
            content,
            re.IGNORECASE,
        )
    )
    if unique_mentions < 2:
        errors.append(
            f"{slug}: practice test uniqueness mentioned only {unique_mentions} times"
        )

    # Check 750 mentioned
    if "750" not in content:
        errors.append(f"{slug}: missing 750 questions mention")

    # Check 25 tests mentioned
    if "25" not in content:
        errors.append(f"{slug}: missing 25 tests mention")

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(f"  X {e}")
else:
    print("\nAll 50 files passed validation!")
