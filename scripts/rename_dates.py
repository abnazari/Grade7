#!/usr/bin/env python3
"""
rename_dates.py — Rename files by replacing a date string in their filenames.

Before renaming, the script scans the folder for files whose names contain
any YYYY-MM-DD date string that is neither <old_date> nor <new_date>.  For
each such group it asks whether you want to delete those files first.
Use --yes to auto-confirm all deletions, or --no-delete to skip the step.

Usage examples:
  # Rename all files in final_output/workbook from 2026-02-25 to 2026-02-27
  python3 scripts/rename_dates.py final_output/workbook 2026-02-25 2026-02-26

  # Only rename PDF files
  python3 scripts/rename_dates.py final_output/workbook 2026-02-25 2026-02-26 --ext pdf

  # Only rename files whose name contains "preview"
  python3 scripts/rename_dates.py final_output/workbook 2026-02-25 2026-02-26 --contains preview

  # Multiple extensions
  python3 scripts/rename_dates.py final_output/workbook 2026-02-25 2026-02-26 --ext pdf html

  # Dry-run (show what would be renamed without actually doing it)
  python3 scripts/rename_dates.py final_output/workbook 2026-02-25 2026-02-26 --dry-run

  # Recurse into subdirectories
  python3 scripts/rename_dates.py final_output 2026-02-25 2026-02-26 --recursive

  # Auto-delete older dated files without prompting
  python3 scripts/rename_dates.py final_output/workbook 2026-02-25 2026-03-01 --yes

  # Skip the delete-older step entirely
  python3 scripts/rename_dates.py final_output/workbook 2026-02-25 2026-03-01 --no-delete
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rename files by replacing a date string in their filenames.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=None,
        help="Folder to search for files (relative to workspace root or absolute).",
    )
    parser.add_argument(
        "--folder", "-f",
        dest="folder",
        metavar="FOLDER",
        help="Named alias for the positional folder argument.",
    )
    parser.add_argument(
        "old_date",
        nargs="?",
        default=None,
        help="Date string to replace, e.g. 2026-02-25",
    )
    parser.add_argument(
        "new_date",
        nargs="?",
        default=None,
        help="New date string, e.g. 2026-02-26",
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        metavar="EXT",
        help="Only rename files with these extension(s), e.g. --ext pdf html",
    )
    parser.add_argument(
        "--contains",
        nargs="+",
        metavar="WORD",
        help="Only rename files whose name contains all of these word(s), e.g. --contains preview",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search subdirectories recursively.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be renamed without making any changes.",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Auto-confirm deletion of older-dated files without prompting.",
    )
    parser.add_argument(
        "--no-delete",
        action="store_true",
        help="Skip the step that offers to delete files with other date strings.",
    )
    return parser.parse_args()


def matches_filters(
    filename: str,
    ext_filter: list[str] | None,
    contains_filter: list[str] | None,
) -> bool:
    """Return True if filename passes all active filters."""
    if ext_filter:
        suffix = Path(filename).suffix.lstrip(".").lower()
        if suffix not in {e.lower().lstrip(".") for e in ext_filter}:
            return False
    if contains_filter:
        name_lower = filename.lower()
        if not all(word.lower() in name_lower for word in contains_filter):
            return False
    return True


def collect_files(folder: Path, recursive: bool) -> list[Path]:
    if recursive:
        return [p for p in folder.rglob("*") if p.is_file()]
    else:
        return [p for p in folder.iterdir() if p.is_file()]


def find_files_by_date(
    folder: Path,
    recursive: bool,
    ext_filter: list[str] | None,
    contains_filter: list[str] | None,
) -> dict[str, list[Path]]:
    """Return {date_string: [paths]} for all files whose name contains a YYYY-MM-DD date."""
    dated: dict[str, list[Path]] = {}
    for f in collect_files(folder, recursive):
        if not matches_filters(f.name, ext_filter, contains_filter):
            continue
        m = DATE_PATTERN.search(f.name)
        if m:
            dated.setdefault(m.group(), []).append(f)
    return dated


def delete_older_files(
    folder: Path,
    dated: dict[str, list[Path]],
    old_date: str,
    new_date: str,
    dry_run: bool,
    yes: bool,
) -> int:
    """List all files with dates other than old_date/new_date, ask once, then delete.

    Returns the total number of files deleted (or that would be deleted).
    """
    # Collect all files to delete, grouped by date for display
    to_delete: list[tuple[str, Path]] = []
    for date_str in sorted(dated):
        if date_str == old_date or date_str == new_date:
            continue
        for f in sorted(dated[date_str]):
            to_delete.append((date_str, f))

    if not to_delete:
        return 0

    # Show everything that would be deleted
    print(f"\nThe following {len(to_delete)} file(s) have other dates and can be deleted:")
    current_date = None
    for date_str, f in to_delete:
        if date_str != current_date:
            print(f"  --- {date_str} ---")
            current_date = date_str
        print(f"    {f.relative_to(folder.parent)}")

    if yes:
        answer = "y"
    elif dry_run:
        answer = "y"
    else:
        try:
            answer = input(f"\nDelete all {len(to_delete)} file(s)? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            answer = "n"

    if answer != "y":
        print("  Skipped — no files deleted.")
        return 0

    for date_str, f in to_delete:
        if dry_run:
            print(f"  [dry-run] DELETE  {f.relative_to(folder.parent)}")
        else:
            f.unlink()
            print(f"  deleted   {f.relative_to(folder.parent)}")

    return len(to_delete)


def _ask(prompt: str) -> str:
    """Read a line from stdin, exiting cleanly on Ctrl+C / Ctrl+D."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def _resolve_folder(raw: str) -> Path:
    """Return an absolute, validated folder Path."""
    p = Path(raw)
    if not p.is_absolute():
        workspace_root = Path(__file__).resolve().parent.parent
        p = workspace_root / p
    p = p.resolve()
    if not p.exists():
        print(f"Error: folder not found: {p}", file=sys.stderr)
        sys.exit(1)
    if not p.is_dir():
        print(f"Error: not a directory: {p}", file=sys.stderr)
        sys.exit(1)
    return p


def _pick_date(
    prompt_label: str,
    dated: dict[str, list[Path]],
    folder: Path,
    exclude: str | None = None,
) -> str:
    """Show a numbered list of dates found in the folder and let the user pick one.

    The user can type a number to select from the list, or type any date string
    directly.  ``exclude`` hides a date already chosen (e.g. old_date when
    picking new_date).
    """
    choices = sorted(d for d in dated if d != exclude)
    if choices:
        print(f"\nDates found in {folder.name}/:")
        for i, d in enumerate(choices, 1):
            count = len(dated[d])
            print(f"  [{i}] {d}  ({count} file{'s' if count != 1 else ''})")
        print()

    while True:
        raw = _ask(f"{prompt_label}: ")
        if not raw:
            print("  (required — please enter a date or pick a number)")
            continue
        # numeric selection
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
            print(f"  Please enter a number between 1 and {len(choices)}.")
            continue
        # validate looks like a date
        if not DATE_PATTERN.fullmatch(raw):
            print("  Expected format YYYY-MM-DD (e.g. 2026-03-01).")
            continue
        return raw


def _interactive_delete(folder: Path, dated: dict[str, list[Path]], dry_run: bool) -> None:
    """Interactive delete flow: pick a date → list files → confirm → delete."""
    date_to_delete = _pick_date("Which date do you want to delete", dated, folder)

    files = sorted(dated.get(date_to_delete, []))
    if not files:
        print(f"  No files found with date {date_to_delete}.")
        return

    print(f"\nThe following {len(files)} file(s) will be deleted:")
    for f in files:
        print(f"    {f.relative_to(folder.parent)}")

    answer = _ask(f"\nConfirm delete all {len(files)} file(s)? [y/N] ").lower()
    if answer != "y":
        print("  Cancelled — no files deleted.")
        return

    for f in files:
        if dry_run:
            print(f"  [dry-run] DELETE  {f.relative_to(folder.parent)}")
        else:
            f.unlink()
            print(f"  deleted   {f.relative_to(folder.parent)}")
    label = "Would delete" if dry_run else "Deleted"
    print(f"\n{label}: {len(files)} file(s)")


def _interactive_rename(
    folder: Path,
    dated: dict[str, list[Path]],
    args: argparse.Namespace,
) -> None:
    """Interactive rename flow: pick FROM date → pick TO date → rename."""
    # FROM date
    if args.old_date is None:
        args.old_date = _pick_date("Rename FROM date", dated, folder)

    # TO date
    if args.new_date is None:
        args.new_date = _pick_date(
            "Rename TO date (or type a new date)",
            dated,
            folder,
            exclude=args.old_date,
        )

    # Offer to delete any other dates first
    if not args.no_delete:
        dated_fresh = find_files_by_date(folder, args.recursive, args.ext, args.contains)
        deleted = delete_older_files(
            folder, dated_fresh, args.old_date, args.new_date,
            dry_run=args.dry_run, yes=args.yes,
        )
        if deleted:
            print()

    # Rename
    files = collect_files(folder, args.recursive)
    renamed = 0
    conflicts = 0

    for file_path in sorted(files):
        original_name = file_path.name
        if args.old_date not in original_name:
            continue
        if not matches_filters(original_name, args.ext, args.contains):
            continue

        new_name = original_name.replace(args.old_date, args.new_date)
        new_path = file_path.parent / new_name

        if new_path.exists():
            print(f"  CONFLICT  {file_path.relative_to(folder.parent)} → {new_name} (target already exists, skipping)")
            conflicts += 1
            continue

        if args.dry_run:
            print(f"  [dry-run]  {file_path.relative_to(folder.parent)}  →  {new_name}")
        else:
            file_path.rename(new_path)
            print(f"  renamed    {file_path.relative_to(folder.parent)}  →  {new_name}")
        renamed += 1

    print()
    label = "Would rename" if args.dry_run else "Renamed"
    print(f"{label}: {renamed} file(s)")
    if conflicts:
        print(f"Conflicts (skipped): {conflicts} file(s)")
    if renamed == 0 and conflicts == 0:
        print(f"No files found containing '{args.old_date}'.")


def main() -> None:
    args = parse_args()

    # --- resolve folder ---
    if args.folder is None:
        args.folder = _ask("Folder (relative or absolute): ")
        if not args.folder:
            print("Error: folder is required.", file=sys.stderr)
            sys.exit(1)

    folder = _resolve_folder(args.folder)

    # Scan all dates in the folder upfront
    dated = find_files_by_date(folder, args.recursive, args.ext, args.contains)

    if not dated:
        print(f"No dated files found in {folder.name}/.")
        sys.exit(0)

    # --- if old_date was given on CLI, go straight to rename ---
    if args.old_date is not None:
        _interactive_rename(folder, dated, args)
        return

    # --- interactive: ask what the user wants to do ---
    print(f"\nDates found in {folder.name}/:")
    all_dates = sorted(dated)
    for i, d in enumerate(all_dates, 1):
        count = len(dated[d])
        print(f"  [{i}] {d}  ({count} file{'s' if count != 1 else ''})")

    print()
    print("What do you want to do?")
    print("  [1] Delete files for a specific date")
    print("  [2] Rename files (replace one date with another)")
    action = _ask("Choice [1/2]: ")

    if action == "1":
        _interactive_delete(folder, dated, dry_run=args.dry_run)
    elif action == "2":
        _interactive_rename(folder, dated, args)
    else:
        print("  Invalid choice — exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
