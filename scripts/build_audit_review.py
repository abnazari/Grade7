#!/usr/bin/env python3
"""
Build an audit-review PDF containing only specific changed questions.

Two-step workflow used by the auditing agent:

  1. **add** — accumulate changed questions (call once per file or multiple times):

        python3 scripts/build_audit_review.py add \\
            --chapter "Ratios and Proportional Relationships" \\
            tests_questions_bank_2/topics/ch01-02-recognizing-proportional-relationships.tex \\
            1-2-q03 1-2-q15

        python3 scripts/build_audit_review.py add \\
            tests_questions_bank_2/topics_additional/ch01-07-proportional-reasoning-with-scale-models.tex \\
            1-7-q12

  2. **open** — compile all accumulated questions into a PDF and open it:

        python3 scripts/build_audit_review.py open

The --chapter flag is only required on the first `add` call; subsequent calls
inherit it.  The grade is read from config.py automatically.

State is stored in build/audit_review_data.json between calls.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Workspace & config helpers
# ---------------------------------------------------------------------------

def find_workspace() -> Path:
    """Walk up from this script to find the workspace root (contains studyGuide.cls)."""
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / "studyGuide.cls").is_file():
            return p
        p = p.parent
    print("ERROR: could not find workspace root (no studyGuide.cls found)", file=sys.stderr)
    sys.exit(1)


def _grade_number() -> int:
    """Return the grade number from config.py (via .env / environment)."""
    scripts_dir = str(Path(__file__).resolve().parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from config import GRADE_NUMBER  # noqa: E402
    return GRADE_NUMBER


# ---------------------------------------------------------------------------
# Persistent state (JSON sidecar in build/)
# ---------------------------------------------------------------------------

def _data_path(ws: Path) -> Path:
    return ws / "build" / "audit_review_data.json"


def _load_data(ws: Path) -> dict:
    dp = _data_path(ws)
    if dp.is_file():
        return json.loads(dp.read_text(encoding="utf-8"))
    return {"chapter": None, "questions": []}


def _save_data(ws: Path, data: dict) -> None:
    dp = _data_path(ws)
    dp.parent.mkdir(exist_ok=True)
    dp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# Question extraction
# ---------------------------------------------------------------------------

_Q_PATTERN = re.compile(
    r"(\\begin\{practiceQuestion\}\{([^}]+)\}\{[^}]+\}.*?\\end\{practiceQuestion\})",
    re.DOTALL,
)


def extract_questions_from_file(
    filepath: Path, target_ids: set[str]
) -> list[tuple[str, str]]:
    """Return list of (question_id, latex_block) for matching questions."""
    text = filepath.read_text(encoding="utf-8")
    results = []
    for match in _Q_PATTERN.finditer(text):
        block = match.group(1)
        qid = match.group(2)
        if qid in target_ids:
            results.append((qid, block))
    return results


# ---------------------------------------------------------------------------
# Positional arg parsing: FILE.tex QID1 QID2 ...
# ---------------------------------------------------------------------------

def parse_file_question_args(args: list[str]) -> list[tuple[str, list[str]]]:
    """Parse positional args into [(relative_path, [qid, ...]), ...]."""
    groups: list[tuple[str, list[str]]] = []
    for token in args:
        if token.endswith(".tex"):
            groups.append((token, []))
        else:
            if not groups:
                print(f"ERROR: question ID '{token}' given before any .tex file path", file=sys.stderr)
                sys.exit(1)
            groups[-1][1].append(token)
    for path, qids in groups:
        if not qids:
            print(f"ERROR: no question IDs given for {path}", file=sys.stderr)
            sys.exit(1)
    return groups


# ---------------------------------------------------------------------------
# LaTeX document generation
# ---------------------------------------------------------------------------

def _latex_escape(text: str) -> str:
    """Escape characters that are special in LaTeX."""
    text = text.replace("\\", r"\textbackslash{}")
    text = text.replace("_", r"\_")
    text = text.replace("&", r"\&")
    text = text.replace("%", r"\%")
    text = text.replace("#", r"\#")
    text = text.replace("{", r"\{")
    text = text.replace("}", r"\}")
    text = text.replace("~", r"\textasciitilde{}")
    text = text.replace("^", r"\textasciicircum{}")
    return text


def build_latex_document(data: dict, grade: int) -> str:
    """Build a full LaTeX document string from accumulated data."""
    chapter = data.get("chapter") or "Audit Review"
    grade_slug = f"grade{grade}"
    subtitle = f"Grade {grade} --- Ch {chapter} --- Changed Questions"

    preamble = rf"""\documentclass[12pt, fleqn, openany]{{studyGuide}}
\setstretch{{1.4}}
\enableInlineReview
\renewcommand{{\VMBookTitle}}{{Audit Review}}
\renewcommand{{\VMBookSubtitle}}{{{subtitle}}}
\renewcommand{{\VMFooterURL}}{{https://viewmath.com/{grade_slug}}}
\renewcommand{{\VMFooterURLDisplay}}{{ViewMath.com/{grade_slug.title()}}}
\begin{{document}}

\begin{{center}}
\begin{{tcolorbox}}[
	enhanced,
	colback=white,
	colframe=funTeal!60,
	boxrule=1.5pt,
	arc=10pt,
	outer arc=10pt,
	width=0.9\linewidth,
	halign=center,
	top=5mm, bottom=5mm,
]
	{{\Large\bfseries\sffamily\color{{funTealDark}}Audit Review}}\\[2mm]
	{{\large\sffamily\color{{funGrayDark}}{subtitle}}}\\[2mm]
	{{\normalsize\sffamily\color{{funGrayDark}}Verify corrections below}}
\end{{tcolorbox}}
\end{{center}}
"""

    parts = [preamble]
    for entry in data["questions"]:
        qid = entry["qid"]
        source = entry["source"]
        block = entry["latex"]
        parts.append(r"\newpage")
        parts.append(
            rf"\section*{{{qid} \hfill \normalsize\texttt{{{_latex_escape(source)}}}}}"
        )
        parts.append(block)
        parts.append("")
    parts.append(r"\end{document}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_add(args: argparse.Namespace, extra: list[str]) -> None:
    """Handle the 'add' subcommand: extract questions and accumulate them."""
    if not extra:
        print("ERROR: no files/questions given. Pass: FILE.tex QID1 QID2 ...", file=sys.stderr)
        sys.exit(1)

    groups = parse_file_question_args(extra)
    ws = find_workspace()
    data = _load_data(ws)

    # Set or update chapter title
    if args.chapter:
        data["chapter"] = args.chapter
    elif data["chapter"] is None:
        print("ERROR: --chapter is required on the first 'add' call.", file=sys.stderr)
        sys.exit(1)

    existing_qids = {e["qid"] for e in data["questions"]}
    added = 0

    for rel_path, qids in groups:
        fpath = ws / rel_path
        if not fpath.is_file():
            print(f"ERROR: file not found: {rel_path}", file=sys.stderr)
            sys.exit(1)
        target_ids = set(qids)
        matches = extract_questions_from_file(fpath, target_ids)
        found_ids = {qid for qid, _ in matches}
        missing = target_ids - found_ids
        if missing:
            print(f"WARNING: question IDs not found in {rel_path}: {', '.join(sorted(missing))}", file=sys.stderr)
        for qid, block in matches:
            if qid in existing_qids:
                # Update existing entry (question was re-edited)
                data["questions"] = [
                    e for e in data["questions"] if e["qid"] != qid
                ]
            data["questions"].append({
                "qid": qid,
                "source": rel_path,
                "latex": block,
            })
            existing_qids.add(qid)
            added += 1

    _save_data(ws, data)
    total = len(data["questions"])
    print(f"Added {added} question(s). Total accumulated: {total}.")


def cmd_open(args: argparse.Namespace) -> None:
    """Handle the 'open' subcommand: generate LaTeX, compile, and open PDF."""
    ws = find_workspace()
    data = _load_data(ws)

    if not data["questions"]:
        print("ERROR: no questions accumulated yet. Use 'add' first.", file=sys.stderr)
        sys.exit(1)

    grade = _grade_number()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Write LaTeX
    out_dir = ws / "build"
    out_dir.mkdir(exist_ok=True)
    tex_path = ws / "tests" / f"audit_review_{timestamp}.tex"
    tex_path.parent.mkdir(exist_ok=True)

    latex_src = build_latex_document(data, grade)
    tex_path.write_text(latex_src, encoding="utf-8")
    print(f"Wrote {tex_path.relative_to(ws)} ({len(data['questions'])} questions)")

    # Compile
    cmd = [
        "latexmk",
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-outdir={out_dir}",
        str(tex_path),
    ]
    print(f"Compiling...")
    result = subprocess.run(cmd, cwd=ws, capture_output=True, text=True)
    if result.returncode != 0:
        print("COMPILATION FAILED", file=sys.stderr)
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout, file=sys.stderr)
        print(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr, file=sys.stderr)
        sys.exit(1)
    pdf_path = out_dir / f"audit_review_{timestamp}.pdf"
    print(f"PDF: {pdf_path.relative_to(ws)}")

    # Open
    if sys.platform == "darwin":
        subprocess.run(["open", str(pdf_path)])
    elif sys.platform == "linux":
        subprocess.run(["xdg-open", str(pdf_path)])
    else:
        print(f"Open manually: {pdf_path}")

    # Clean up the data file so next audit starts fresh
    _data_path(ws).unlink(missing_ok=True)
    print("Data file cleared for next audit.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build an audit-review PDF with only changed questions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- add ---
    add_parser = subparsers.add_parser(
        "add",
        help="Extract and accumulate changed questions.",
    )
    add_parser.add_argument(
        "--chapter",
        type=str,
        default=None,
        help="Chapter title (required on first call, inherited after).",
    )

    # --- open ---
    subparsers.add_parser(
        "open",
        help="Compile accumulated questions into a PDF and open it.",
    )

    args, extra = parser.parse_known_args()

    if args.command == "add":
        cmd_add(args, extra)
    elif args.command == "open":
        cmd_open(args)


if __name__ == "__main__":
    main()
