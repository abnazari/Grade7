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
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

# Regex to extract a date like 2026-02-26 from a filename
_DATE_RE = re.compile(r'(\d{4}-\d{2}-\d{2})')

# Add scripts/ to path so we can import config
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from config import BOOK_TYPES, BOOK_DISPLAY_NAMES, GRADE_NUMBER, find_workspace


class RequestLogger:
    """Append structured request events to a JSONL log file."""

    def __init__(self, workspace: Path):
        log_dir = workspace / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        self.path = log_dir / "tpt_upload_server_requests.jsonl"

    def write(self, **payload) -> None:
        event = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            **payload,
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")


# ============================================================================
# GRADE ORDINAL HELPER
# ============================================================================

def _ordinal(n: int) -> str:
    """Return ordinal string: 1→'1st', 2→'2nd', 3→'3rd', 7→'7th', etc."""
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


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

        # Load bundles from bundles.json
        self.bundles: Dict[str, List[dict]] = self._load_bundles()

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

    def get_book_entry(self, book_type: str, state_slug: str) -> Optional[dict]:
        for entry in self.books.get(book_type, []):
            if entry.get("state_slug") == state_slug:
                return entry
        return None

    def get_book_entry_by_filename(self, book_type: str, filename: str) -> Optional[dict]:
        for entry in self.books.get(book_type, []):
            if filename in {
                entry.get("product_filename"),
                entry.get("preview_filename"),
                entry.get("description_filename"),
            }:
                return entry
        return None

    def lookup_by_tpt_title(self, tpt_title: str) -> Optional[dict]:
        """Find a book entry by its TPT title (exact or fuzzy match).

        Returns the enriched entry (with product_filename, etc.) if found.
        """
        tpt_title = tpt_title.strip()
        # Exact match first
        for bt, entries in self.books.items():
            for entry in entries:
                if entry.get("tpt_title", "").strip() == tpt_title:
                    return entry
        # Fallback: case-insensitive match
        lower = tpt_title.lower()
        for bt, entries in self.books.items():
            for entry in entries:
                if entry.get("tpt_title", "").strip().lower() == lower:
                    return entry
        return None

    # ── Bundle helpers ─────────────────────────────────────────────────

    def _load_bundles(self) -> Dict[str, List[dict]]:
        """Load bundles from bundles.json grouped by bundle_type."""
        bundles_path = self.workspace / "bundles.json"
        if not bundles_path.is_file():
            return {}

        with open(bundles_path) as f:
            all_bundles = json.load(f)

        # Enrich each entry with file availability
        grouped: Dict[str, List[dict]] = {}
        for entry in all_bundles:
            bt = entry.get("bundle_type", "")
            files = entry.get("files", {})

            # Check file existence
            desc_path = self.workspace / files.get("description_html", "")
            preview_path = self.workspace / files.get("preview_pdf", "")
            thumbnails = files.get("thumbnails", [])

            entry["has_description"] = desc_path.is_file()
            entry["has_preview_pdf"] = preview_path.is_file()
            entry["thumbnail_count"] = sum(
                1 for t in thumbnails
                if (self.workspace / t).is_file()
            )
            entry["has_all_thumbnails"] = (
                entry["thumbnail_count"] == len(thumbnails) and len(thumbnails) > 0
            )

            if bt not in grouped:
                grouped[bt] = []
            grouped[bt].append(entry)

        return grouped

    def available_bundle_types(self) -> list:
        """Return [{key, display_name, count}, …] for loaded bundle types."""
        result = []
        for bt, entries in self.bundles.items():
            display = entries[0].get("display_name", bt) if entries else bt
            result.append({
                "key": bt,
                "display_name": display,
                "count": len(entries),
            })
        result.sort(key=lambda x: x["key"])
        return result

    def get_bundles(self, bundle_type: str) -> Optional[List[dict]]:
        return self.bundles.get(bundle_type)

    def get_bundle_entry(self, bundle_type: str, state_slug: str) -> Optional[dict]:
        for entry in self.bundles.get(bundle_type, []):
            if entry.get("state_slug") == state_slug:
                return entry
        return None

    def get_bundle_entry_by_filename(self, bundle_type: str, filename: str) -> Optional[dict]:
        for entry in self.bundles.get(bundle_type, []):
            files = entry.get("files", {})
            known_names = {
                Path(files.get("description_html", "")).name,
                Path(files.get("preview_pdf", "")).name,
            }
            known_names.update(Path(path).name for path in files.get("thumbnails", []))
            if filename in known_names:
                return entry
        return None


# ============================================================================
# HTTP REQUEST HANDLER
# ============================================================================

class TPTHandler(BaseHTTPRequestHandler):
    """Stateless handler — serves book data and files."""

    store: BookStore  # set by the server factory
    request_logger: RequestLogger

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/api/grade-info":
            ordinal = _ordinal(GRADE_NUMBER)
            self._log_request_event(200, "grade_info")
            self._json_response({
                "grade_number": GRADE_NUMBER,
                "grade_id": f"checkbox_{ordinal}-grade",
                "grade_label": f"{ordinal} grade",
            })

        elif path == "/api/book-types":
            self._log_request_event(200, "book_types")
            self._json_response(self.store.available_book_types())

        elif path == "/api/books":
            bt = params.get("type", [None])[0]
            if not bt:
                self._log_request_event(400, "books_list", error="missing type")
                self._error(400, "Missing ?type= parameter")
                return
            books = self.store.get_books(bt)
            if books is None:
                self._log_request_event(404, "books_list", book_type=bt, error="unknown book type")
                self._error(404, f"Unknown book type: {bt}")
                return
            self._log_request_event(
                200,
                "books_list",
                book_type=bt,
                book_type_display=BOOK_DISPLAY_NAMES.get(bt, bt),
                count=len(books),
            )
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

        elif path == "/api/lookup":
            title = params.get("title", [None])[0]
            if not title:
                self._log_request_event(400, "lookup", error="missing title")
                self._error(400, "Missing ?title= parameter")
                return
            entry = self.store.lookup_by_tpt_title(title)
            if not entry:
                self._log_request_event(404, "lookup", requested_title=title, error="not found")
                self._error(404, f"No book found for title: {title}")
                return
            self._log_request_event(
                200,
                "lookup",
                requested_title=title,
                book_type=entry.get("book_type"),
                state_slug=entry.get("state_slug"),
                state_name=entry.get("state_name"),
                tpt_title=entry.get("tpt_title"),
            )
            self._json_response(entry)

        elif path == "/api/bundle-types":
            self._log_request_event(200, "bundle_types")
            self._json_response(self.store.available_bundle_types())

        elif path == "/api/bundles":
            bt = params.get("type", [None])[0]
            if not bt:
                self._log_request_event(400, "bundles_list", error="missing type")
                self._error(400, "Missing ?type= parameter")
                return
            bundles = self.store.get_bundles(bt)
            if bundles is None:
                self._log_request_event(404, "bundles_list", bundle_type=bt, error="unknown bundle type")
                self._error(404, f"Unknown bundle type: {bt}")
                return
            self._log_request_event(
                200,
                "bundles_list",
                bundle_type=bt,
                display_name=bundles[0].get("display_name", bt) if bundles else bt,
                count=len(bundles),
            )
            self._json_response({
                "bundle_type": bt,
                "display_name": bundles[0].get("display_name", bt) if bundles else bt,
                "count": len(bundles),
                "bundles": bundles,
            })

        elif path.startswith("/api/bundle-description/"):
            # /api/bundle-description/<bundle_type>/<state_slug>
            parts = path.split("/")
            if len(parts) >= 5:
                self._serve_bundle_description(parts[3], parts[4])
            else:
                self._error(400, "Invalid path")

        elif path.startswith("/api/bundle-file/"):
            # /api/bundle-file/<bundle_type>/<filename>
            parts = path.split("/", 4)
            if len(parts) >= 5:
                self._serve_bundle_file(parts[3], parts[4])
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

    def _log_request_event(self, status: int, request_kind: str, **fields):
        self.request_logger.write(
            status=status,
            request_kind=request_kind,
            method=self.command,
            path=self.path,
            client_ip=self.client_address[0] if self.client_address else None,
            **fields,
        )

    def _serve_description(self, book_type: str, state_slug: str):
        """Serve description HTML file, stripping the comment lines at the top."""
        bt_cfg = BOOK_TYPES.get(book_type)
        if not bt_cfg:
            self._log_request_event(404, "description", book_type=book_type, state_slug=state_slug, error="unknown book type")
            self._error(404, f"Unknown book type: {book_type}")
            return

        output_dir = self.store.workspace / "final_output" / bt_cfg["output_subdir"]
        # Use _find_file to pick the newest description (respects --date)
        desc_name = BookStore._find_file(
            output_dir, state_slug, "_tpt_",
            date_filter=self.store.date_filter)
        desc_file = (output_dir / desc_name) if desc_name else None

        if not desc_file or not desc_file.is_file():
            self._log_request_event(404, "description", book_type=book_type, state_slug=state_slug, filename=desc_name, error="not found")
            self._error(404, f"Description not found for {book_type}/{state_slug}")
            return

        entry = self.store.get_book_entry(book_type, state_slug)
        self._log_request_event(
            200,
            "description",
            book_type=book_type,
            state_slug=state_slug,
            state_name=entry.get("state_name") if entry else None,
            tpt_title=entry.get("tpt_title") if entry else None,
            filename=desc_file.name,
        )

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
            self._log_request_event(400, "book_file", book_type=book_type, filename=filename, error="invalid filename")
            self._error(400, "Invalid filename")
            return

        bt_cfg = BOOK_TYPES.get(book_type)
        if not bt_cfg:
            self._log_request_event(404, "book_file", book_type=book_type, filename=filename, error="unknown book type")
            self._error(404, f"Unknown book type: {book_type}")
            return

        file_path = (self.store.workspace / "final_output"
                     / bt_cfg["output_subdir"] / filename)
        if not file_path.is_file():
            self._log_request_event(404, "book_file", book_type=book_type, filename=filename, error="not found")
            self._error(404, f"File not found: {filename}")
            return

        entry = self.store.get_book_entry_by_filename(book_type, filename)
        file_role = "product_pdf"
        if entry and filename == entry.get("preview_filename"):
            file_role = "preview_pdf"
        elif entry and filename == entry.get("description_filename"):
            file_role = "description_html"
        self._log_request_event(
            200,
            "book_file",
            book_type=book_type,
            state_slug=entry.get("state_slug") if entry else None,
            state_name=entry.get("state_name") if entry else None,
            tpt_title=entry.get("tpt_title") if entry else None,
            filename=filename,
            file_role=file_role,
        )

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

    def _serve_bundle_description(self, bundle_type: str, state_slug: str):
        """Serve bundle description HTML file."""
        bundles = self.store.get_bundles(bundle_type)
        if bundles is None:
            self._log_request_event(404, "bundle_description", bundle_type=bundle_type, state_slug=state_slug, error="unknown bundle type")
            self._error(404, f"Unknown bundle type: {bundle_type}")
            return

        # Find the bundle entry for this state
        entry = None
        for b in bundles:
            if b.get("state_slug") == state_slug:
                entry = b
                break
        if not entry:
            self._log_request_event(404, "bundle_description", bundle_type=bundle_type, state_slug=state_slug, error="bundle not found")
            self._error(404, f"Bundle not found for {bundle_type}/{state_slug}")
            return

        desc_rel = entry.get("files", {}).get("description_html", "")
        desc_path = self.store.workspace / desc_rel
        if not desc_path.is_file():
            self._log_request_event(404, "bundle_description", bundle_type=bundle_type, state_slug=state_slug, filename=Path(desc_rel).name, error="not found")
            self._error(404, f"Description not found for {bundle_type}/{state_slug}")
            return

        self._log_request_event(
            200,
            "bundle_description",
            bundle_type=bundle_type,
            state_slug=state_slug,
            state_name=entry.get("state_name"),
            title=entry.get("title"),
            filename=desc_path.name,
        )

        content = desc_path.read_text(encoding="utf-8")
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

    def _serve_bundle_file(self, bundle_type: str, filename: str):
        """Serve a file (PDF, JPEG, etc.) from a bundle's directory."""
        if ".." in filename or "/" in filename:
            self._log_request_event(400, "bundle_file", bundle_type=bundle_type, filename=filename, error="invalid filename")
            self._error(400, "Invalid filename")
            return

        file_path = (self.store.workspace / "final_output"
                     / "bundles" / bundle_type / filename)
        if not file_path.is_file():
            self._log_request_event(404, "bundle_file", bundle_type=bundle_type, filename=filename, error="not found")
            self._error(404, f"File not found: {filename}")
            return

        entry = self.store.get_bundle_entry_by_filename(bundle_type, filename)
        file_role = "bundle_file"
        if entry:
            files = entry.get("files", {})
            if filename == Path(files.get("preview_pdf", "")).name:
                file_role = "preview_pdf"
            elif filename == Path(files.get("description_html", "")).name:
                file_role = "description_html"
            elif filename in [Path(path).name for path in files.get("thumbnails", [])]:
                file_role = "thumbnail"
        self._log_request_event(
            200,
            "bundle_file",
            bundle_type=bundle_type,
            state_slug=entry.get("state_slug") if entry else None,
            state_name=entry.get("state_name") if entry else None,
            title=entry.get("title") if entry else None,
            filename=filename,
            file_role=file_role,
        )

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
    request_logger = RequestLogger(workspace)

    if not store.books:
        print(f"\033[31mError:\033[0m No books found"
              + (f" for {args.book_type}" if args.book_type else ""))
        sys.exit(1)

    total_count = sum(len(v) for v in store.books.values())
    total_bundles = sum(len(v) for v in store.bundles.values())
    print(f"\n\033[1m📚 TPT Upload Server\033[0m")
    if args.book_type:
        display = BOOK_DISPLAY_NAMES.get(args.book_type, args.book_type)
        print(f"   Book type:  {display}")
    else:
        print(f"   Book types: {len(store.books)} loaded")
    print(f"   Books:      {total_count} total entries")
    if total_bundles:
        print(f"   Bundles:    {total_bundles} total entries"
              f" ({len(store.bundles)} bundle types)")
    if args.date:
        print(f"   Date:       {args.date}  (pinned)")
    else:
        print(f"   Date:       newest available")
    print(f"   Server:     http://localhost:{args.port}")
    print(f"   Request log: {request_logger.path.relative_to(workspace)}")
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

    handler_class = type(
        "Handler",
        (TPTHandler,),
        {"store": store, "request_logger": request_logger},
    )

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
