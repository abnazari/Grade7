#!/usr/bin/env python3
"""
Build a PDF containing all graphical questions from the question bank.

A graphical question is defined as any practiceQuestion block containing either
\\begin{tikzpicture} or \\includegraphics.

Usage:
    python3 scripts/build_graphical_review.py --bank 1 --chapter 1
    python3 scripts/build_graphical_review.py --bank both --chapter all
"""

from __future__ import annotations

import argparse
import datetime
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
    try:
        from config import GRADE_NUMBER  # noqa: E402
        return GRADE_NUMBER
    except ImportError:
        return 7


# ---------------------------------------------------------------------------
# Question extraction
# ---------------------------------------------------------------------------

_Q_PATTERN = re.compile(
    r"(\\begin\{practiceQuestion\}\{([^}]+)\}\{[^}]+\}.*?\\end\{practiceQuestion\})",
    re.DOTALL,
)

def is_graphical(latex_block: str) -> bool:
    """Check if the question block contains graphical elements."""
    return "\\begin{tikzpicture}" in latex_block or "\\includegraphics" in latex_block

def extract_graphical_questions(filepath: Path) -> list[dict]:
    """Return list of graphical question dicts."""
    text = filepath.read_text(encoding="utf-8")
    results = []
    for match in _Q_PATTERN.finditer(text):
        block = match.group(1)
        qid = match.group(2)
        if is_graphical(block):
            results.append({
                "qid": qid,
                "latex": block,
            })
    return results


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

def build_latex_document(questions: list[dict], grade: int, bank: str, chapter: str) -> str:
    """Build a full LaTeX document string from accumulated data."""
    grade_slug = f"grade{grade}"
    subtitle = f"Grade {grade} --- Bank: {bank} --- Chapter: {chapter} --- Graphical Questions"

    preamble = rf"""\documentclass[12pt, fleqn, openany]{{studyGuide}}
\setstretch{{1.4}}
\enableInlineReview
\renewcommand{{\VMBookTitle}}{{Graphical Questions Review}}
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
	{{\Large\bfseries\sffamily\color{{funTealDark}}Graphical Questions}}\\[2mm]
	{{\large\sffamily\color{{funGrayDark}}{subtitle}}}\\[2mm]
	{{\normalsize\sffamily\color{{funGrayDark}}Audit visual elements below}}
\end{{tcolorbox}}
\end{{center}}
"""

    parts = [preamble]
    for entry in questions:
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
# Main Logic
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a PDF with all graphical questions from the question bank.",
    )
    parser.add_argument(
        "--bank",
        type=str,
        choices=["1", "2", "both"],
        help="Which question bank to search (1, 2, or both).",
    )
    parser.add_argument(
        "--chapter",
        type=str,
        help="Chapter number to search (e.g., '1', '2') or 'all'.",
    )

    args = parser.parse_args()

    # Interactive prompts if arguments are missing
    if args.bank is None:
        while True:
            bank_input = input("Select bank to search (1, 2, or both) [both]: ").strip().lower()
            if not bank_input:
                args.bank = "both"
                break
            if bank_input in ["1", "2", "both"]:
                args.bank = bank_input
                break
            print("Invalid choice. Please enter 1, 2, or both.")
            
    if args.chapter is None:
        chapter_input = input("Select chapter number to search (1, 2, etc.) or 'all' [all]: ").strip().lower()
        args.chapter = chapter_input if chapter_input else "all"

    ws = find_workspace()
    
    # Determine which banks to search
    banks_to_search = []
    if args.bank in ["1", "both"]:
        banks_to_search.append("tests_questions_bank")
    if args.bank in ["2", "both"]:
        banks_to_search.append("tests_questions_bank_2")

    print(f"Searching banks: {banks_to_search}")

    # Determine chapter filters
    ch_prefix = f"ch{int(args.chapter):02d}" if args.chapter != "all" else "ch"
    print(f"Searching for files starting with: {ch_prefix}")

    all_questions = []

    for bank_dir_name in banks_to_search:
        bank_path = ws / bank_dir_name
        if not bank_path.exists():
            continue
            
        for ext_dir in ["topics", "topics_additional", "topics_modified"]:
            topics_dir = bank_path / ext_dir
            if not topics_dir.exists():
                continue
                
            for file_path in topics_dir.glob(f"{ch_prefix}*.tex"):
                rel_path = file_path.relative_to(ws)
                q_list = extract_graphical_questions(file_path)
                for q in q_list:
                    q["source"] = str(rel_path)
                    all_questions.append(q)

    if not all_questions:
        print("No graphical questions found with the selected criteria.", file=sys.stderr)
        sys.exit(0)

    # Sort questions by file name (which starts with chXX-YY so it sorts sequentially), then bank, then QID
    all_questions.sort(key=lambda q: (Path(q["source"]).name, q["source"], q["qid"]))

    print(f"Found {len(all_questions)} graphical questions.")

    grade = _grade_number()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Write LaTeX
    out_dir = ws / "build"
    out_dir.mkdir(exist_ok=True)
    tex_path = ws / "tests" / f"graphical_review_{timestamp}.tex"
    tex_path.parent.mkdir(exist_ok=True)

    latex_src = build_latex_document(all_questions, grade, args.bank, args.chapter)
    tex_path.write_text(latex_src, encoding="utf-8")
    print(f"Wrote {tex_path.relative_to(ws)}")

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
        
    pdf_path = out_dir / f"graphical_review_{timestamp}.pdf"
    print(f"PDF Output: {pdf_path.relative_to(ws)}")

    # Open
    if sys.platform == "darwin":
        subprocess.run(["open", str(pdf_path)])
    elif sys.platform == "linux":
        subprocess.run(["xdg-open", str(pdf_path)])
    else:
        print(f"Open manually: {pdf_path}")

if __name__ == "__main__":
    main()
