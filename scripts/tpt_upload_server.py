#!/usr/bin/env python3
"""Local HTTP server for the TPT Upload Helper Chrome extension.

Serves book metadata (titles, descriptions) and PDF files for all book types.
Navigation state (done / skipped / current position) is managed entirely by
the Chrome extension via chrome.storage.local, so the server is stateless.

Usage:
    python scripts/tpt_upload_server.py                 # serve all book types
    python scripts/tpt_upload_server.py --book-type 10_practice_tests
    python scripts/tpt_upload_server.py --port 9000

Endpoints:
    GET  /api/book-types              → available book types
    GET  /api/books?type=<bt>         → all states for a book type
    GET  /api/description/<bt>/<slug> → description HTML
    GET  /api/file/<bt>/<filename>    → serve a PDF file
"""

import argparse
import json
import mimetypes
import os
import re
import subprocess
import sys
from datetime import date
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

# Regex to extract a date like 2026-02-26 from a filename
_DATE_RE = re.compile(r'(\d{4}-\d{2}-\d{2})')

# Add scripts/ to path so we can import config
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from config import BOOK_TYPES, BOOK_DISPLAY_NAMES, find_workspace


# ============================================================================
# PDF PAGE COUNT HELPER
# ============================================================================

def _pdf_page_count(pdf_path: Path) -> Optional[int]:
    """Return the number of pages in a PDF file.

    Tries pdfinfo first (fast, reliable), then falls back to
    scanning the raw PDF bytes for /Type /Page entries.
    """
    if not pdf_path.is_file():
        return None
    # Method 1: pdfinfo (poppler)
    try:
        out = subprocess.check_output(
            ["pdfinfo", str(pdf_path)],
            stderr=subprocess.DEVNULL, timeout=10,
        ).decode()
        m = re.search(r"Pages:\s+(\d+)", out)
        if m:
            return int(m.group(1))
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    # Method 2: regex scan (works for most PDFs)
    try:
        data = pdf_path.read_bytes()
        # Look for /Type /Pages ... /Count N  (the root pages dict)
        matches = re.findall(rb"/Type\s*/Pages.*?/Count\s+(\d+)", data, re.S)
        if matches:
            return max(int(c) for c in matches)
    except Exception:
        pass
    return None


# ============================================================================
# BOOK DATA STORE  (read-only — no queue state)
# ============================================================================

class BookStore:
    """Loads and caches book metadata for one or more book types."""

    def __init__(self, workspace: Path,
                 book_type_filter: Optional[str] = None,
                 date_filter: Optional[str] = None):
        self.workspace = workspace
        self.date_filter = date_filter  # e.g. "2026-02-26" or None (= newest)
        self._all_titles = self._load_all_titles()
        # book_type → list of enriched entries
        self.books: Dict[str, List[dict]] = {}

        types_to_load = (
            [book_type_filter] if book_type_filter
            else list(BOOK_TYPES.keys())
        )
        for bt in types_to_load:
            entries = self._build_entries(bt)
            if entries:
                self.books[bt] = entries

    def _load_all_titles(self) -> list:
        titles_path = self.workspace / "titles.json"
        with open(titles_path) as f:
            return json.load(f)

    def _build_entries(self, book_type: str) -> List[dict]:
        """Build enriched book entries for a single book type."""
        cfg = BOOK_TYPES.get(book_type)
        if not cfg:
            return []

        output_dir = self.workspace / "final_output" / cfg["output_subdir"]

        entries = [
            t for t in self._all_titles
            if t.get("book_type") == book_type
        ]
        entries.sort(key=lambda t: t.get("state_name", ""))

        for entry in entries:
            slug = entry["state_slug"]
            entry["product_filename"] = self._find_file(
                output_dir, slug, "_2", self.date_filter)
            entry["preview_filename"] = self._find_file(
                output_dir, slug, "_preview_", self.date_filter)
            entry["description_filename"] = self._find_file(
                output_dir, slug, "_tpt_", self.date_filter)
            entry["has_product_pdf"] = entry["product_filename"] is not None
            entry["has_preview_pdf"] = entry["preview_filename"] is not None
            entry["has_description"] = entry["description_filename"] is not None
            # Count pages in the product PDF
            entry["page_count"] = (
                _pdf_page_count(output_dir / entry["product_filename"])
                if entry["has_product_pdf"] else None
            )

        return entries

    @staticmethod
    def _find_file(output_dir: Path, state_slug: str,
                   pattern: str,
                   date_filter: Optional[str] = None) -> Optional[str]:
        """Find the best matching file for a state.

        When multiple files match (different dates), picks the newest
        by the embedded YYYY-MM-DD date.  If *date_filter* is given,
        only files containing that date string are considered.
        """
        if not output_dir.is_dir():
            return None
        candidates = []
        for f in output_dir.iterdir():
            name = f.name
            if not (name.startswith(state_slug) and pattern in name):
                continue
            # For product PDF pattern "_2", skip previews and descriptions
            if pattern == "_2" and ("_preview_" in name or "_tpt_" in name):
                continue
            # If a specific date is requested, skip non-matching files
            if date_filter and date_filter not in name:
                continue
            # Extract date for sorting
            m = _DATE_RE.search(name)
            file_date = m.group(1) if m else "0000-00-00"
            candidates.append((file_date, name))
        if not candidates:
            return None
        # Sort by date descending → newest first
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    # ── Public helpers ─────────────────────────────────────────────────

    def available_book_types(self) -> list:
        """Return [{key, display_name, count}, …] for loaded book types."""
        result = []
        for bt, entries in self.books.items():
            result.append({
                "key": bt,
                "display_name": BOOK_DISPLAY_NAMES.get(bt, bt),
                "count": len(entries),
            })
        # Sort to match BOOK_TYPES insertion order
        order = list(BOOK_TYPES.keys())
        result.sort(key=lambda x: order.index(x["key"])
                     if x["key"] in order else 999)
        return result

    def get_books(self, book_type: str) -> Optional[List[dict]]:
        return self.books.get(book_type)


# ============================================================================
# HTTP REQUEST HANDLER
# ============================================================================

class TPTHandler(BaseHTTPRequestHandler):
    """Stateless handler — serves book data and files."""

    store: BookStore  # set by the server factory

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/api/book-types":
            self._json_response(self.store.available_book_types())

        elif path == "/api/books":
            bt = params.get("type", [None])[0]
            if not bt:
                self._error(400, "Missing ?type= parameter")
                return
            books = self.store.get_books(bt)
            if books is None:
                self._error(404, f"Unknown book type: {bt}")
                return
            self._json_response({
                "book_type": bt,
                "book_type_display": BOOK_DISPLAY_NAMES.get(bt, bt),
                "count": len(books),
                "books": books,
            })

        elif path.startswith("/api/description/"):
            parts = path.split("/")
            if len(parts) >= 5:
                self._serve_description(parts[3], parts[4])
            else:
                self._error(400, "Invalid path")

        elif path.startswith("/api/file/"):
            parts = path.split("/", 4)
            if len(parts) >= 5:
                self._serve_file(parts[3], parts[4])
            else:
                self._error(400, "Invalid path")

        else:
            self._error(404, "Not found")

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    # ── Response helpers ───────────────────────────────────────────────

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json_response(self, data, status: int = 200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status: int, message: str):
        self._json_response({"error": message}, status)

    def _serve_description(self, book_type: str, state_slug: str):
        """Serve description HTML file, stripping the comment lines at the top."""
        bt_cfg = BOOK_TYPES.get(book_type)
        if not bt_cfg:
            self._error(404, f"Unknown book type: {book_type}")
            return

        output_dir = self.store.workspace / "final_output" / bt_cfg["output_subdir"]
        # Use _find_file to pick the newest description (respects --date)
        desc_name = BookStore._find_file(
            output_dir, state_slug, "_tpt_",
            date_filter=self.store.date_filter)
        desc_file = (output_dir / desc_name) if desc_name else None

        if not desc_file or not desc_file.is_file():
            self._error(404, f"Description not found for {book_type}/{state_slug}")
            return

        content = desc_file.read_text(encoding="utf-8")
        # Strip HTML comment lines at top
        lines = content.split("\n")
        filtered = [l for l in lines
                     if not (l.strip().startswith("<!--")
                             and l.strip().endswith("-->"))]
        content = "\n".join(filtered).strip()

        body = content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, book_type: str, filename: str):
        """Serve a file (PDF, etc.) from the final_output directory."""
        if ".." in filename or "/" in filename:
            self._error(400, "Invalid filename")
            return

        bt_cfg = BOOK_TYPES.get(book_type)
        if not bt_cfg:
            self._error(404, f"Unknown book type: {book_type}")
            return

        file_path = (self.store.workspace / "final_output"
                     / bt_cfg["output_subdir"] / filename)
        if not file_path.is_file():
            self._error(404, f"File not found: {filename}")
            return

        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            mime_type = "application/octet-stream"

        file_size = file_path.stat().st_size
        body = file_path.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(file_size))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Override to add color and brevity."""
        method = args[0] if args else ""
        status = args[1] if len(args) > 1 else ""
        if str(status).startswith("2"):
            color = "\033[32m"
        elif str(status).startswith("3"):
            color = "\033[33m"
        else:
            color = "\033[31m"
        reset = "\033[0m"
        print(f"  {color}{method}{reset}  {status}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Local server for the TPT Upload Helper Chrome extension",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/tpt_upload_server.py                        # all book types
  python scripts/tpt_upload_server.py --book-type study_guide
  python scripts/tpt_upload_server.py --port 9000
        """,
    )
    parser.add_argument(
        "--book-type",
        choices=list(BOOK_TYPES.keys()),
        default=None,
        help="Serve only this book type (default: all)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port to listen on (default: 8765)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Pin a specific date (YYYY-MM-DD) for file selection "
             "instead of auto-picking the newest",
    )

    args = parser.parse_args()

    workspace = find_workspace()
    store = BookStore(workspace, book_type_filter=args.book_type,
                      date_filter=args.date)

    if not store.books:
        print(f"\033[31mError:\033[0m No books found"
              + (f" for {args.book_type}" if args.book_type else ""))
        sys.exit(1)

    total_count = sum(len(v) for v in store.books.values())
    print(f"\n\033[1m📚 TPT Upload Server\033[0m")
    if args.book_type:
        display = BOOK_DISPLAY_NAMES.get(args.book_type, args.book_type)
        print(f"   Book type:  {display}")
    else:
        print(f"   Book types: {len(store.books)} loaded")
    print(f"   Books:      {total_count} total entries")
    if args.date:
        print(f"   Date:       {args.date}  (pinned)")
    else:
        print(f"   Date:       newest available")
    print(f"   Server:     http://localhost:{args.port}")
    print(f"\n   Open the TPT Upload Helper extension in Chrome to begin.\n")

    # Summarise missing files per book type
    for bt, entries in store.books.items():
        m_prod = sum(1 for t in entries if not t["has_product_pdf"])
        m_prev = sum(1 for t in entries if not t["has_preview_pdf"])
        m_desc = sum(1 for t in entries if not t["has_description"])
        if m_prod or m_prev or m_desc:
            display = BOOK_DISPLAY_NAMES.get(bt, bt)
            parts = []
            if m_prod:
                parts.append(f"product:{m_prod}")
            if m_prev:
                parts.append(f"preview:{m_prev}")
            if m_desc:
                parts.append(f"desc:{m_desc}")
            print(f"   \033[33m⚠ {display}:\033[0m missing {', '.join(parts)}")
    print()

    handler_class = type("Handler", (TPTHandler,), {"store": store})

    class ReusableHTTPServer(HTTPServer):
        allow_reuse_address = True

    server = ReusableHTTPServer(("localhost", args.port), handler_class)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\033[1mDone.\033[0m")
        server.server_close()


if __name__ == "__main__":
    main()
