#!/usr/bin/env python3
"""
ViewMath.com Book Uploader — manage WooCommerce products from the CLI.

Grade-agnostic: reads grade info from .env, book types from config.py.
Copy this file to any grade project's scripts/ folder.

Required .env keys (in project root):
    GRADE_NUMBER, GRADE_SLUG, GRADE_DISPLAY
    WC_SITE_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET
    WP_SSH_HOST, WP_PATH

Commands:
    runx setup-category [STATE]        # one state, or all 50 if omitted
    runx create-landing-page [--content-file FILE]
    runx upload-book BOOK_TYPE STATE [--price 9.99]
    runx upload-all-books STATE [--price 9.99]
    runx check-books STATE
    runx list-products STATE
    runx show-book-types
    runx show-states
    runx show-pdfs STATE
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

import typer
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from woocommerce import API

# ── Ensure scripts/ is importable ────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (  # noqa: E402
    BOOK_DISPLAY_NAMES,
    BOOK_TYPES,
    book_title,
    find_workspace,
    load_state_curriculums,
    load_state_exams,
)
from config_loader import load_config  # noqa: E402

console = Console()


# ── YAML data loaders (state exams & curriculums) ────────────────────────────
# Delegates to config.py's cached loaders.

def _load_state_exams() -> dict[str, dict]:
    """Load state_exams.yaml → {slug: {exam_name, exam_acronym, exam_months}}."""
    return load_state_exams()


def _load_state_curriculums() -> dict[str, dict]:
    """Load state_curriculums.yaml → {slug: {curriculum_name, curriculum_acronym}}."""
    return load_state_curriculums()


# ── WC store tracker (wc_store.yaml) ─────────────────────────────────────────

def _store_path() -> Path:
    return find_workspace() / "wc_store.yaml"


def _store_load() -> dict:
    p = _store_path()
    if not p.exists():
        return {"categories": {}, "products": {}}
    with open(p) as f:
        return yaml.safe_load(f) or {"categories": {}, "products": {}}


def _store_save(data: dict) -> None:
    with open(_store_path(), "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _store_record_category(state: str, *, id: int, name: str, slug: str, url: str) -> None:
    """Persist a category entry to wc_store.yaml."""
    data = _store_load()
    data.setdefault("categories", {})[state] = {
        "name": name, "slug": slug, "id": id, "url": url,
    }
    _store_save(data)


def _store_record_product(state: str, book_type: str, product: dict) -> None:
    """Persist a product entry to wc_store.yaml."""
    data = _store_load()
    data.setdefault("products", {}).setdefault(state, {})[book_type] = {
        "id": product["id"],
        "name": product.get("name", ""),
        "sku": product.get("sku", ""),
        "url": product.get("permalink", ""),
        "price": product.get("regular_price", ""),
        "status": product.get("status", ""),
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    _store_save(data)


# ── Default price lookup ──────────────────────────────────────────────────────

def _default_price(book_type: str) -> str:
    """Return the configured default price for a book type."""
    key = f"price_{book_type}"
    return getattr(get_settings(), key, "9.99")


app = typer.Typer(
    name="wc-uploader",
    help="ViewMath.com Book Uploader — manage WooCommerce products.",
    no_args_is_help=True,
)


# ============================================================================
# SETTINGS
# ============================================================================

class WCSettings(BaseSettings):
    """WooCommerce / WordPress settings loaded from .env in the project root."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Grade info — makes the script reusable across grade projects
    grade_number: int = Field(description="Grade number (e.g. 3)")
    grade_slug: str = Field(description="URL/filename slug (e.g. grade7)")
    grade_display: str = Field(description="Human-readable name (e.g. Grade 7 Math)")

    # WooCommerce REST API
    wc_site_url: str = Field(description="Site URL")
    wc_consumer_key: str = Field(description="REST API consumer key")
    wc_consumer_secret: str = Field(description="REST API consumer secret")

    # WordPress SSH
    wp_ssh_host: str | None = Field(default=None, description="SSH host (e.g. root@1.2.3.4)")
    wp_path: str | None = Field(default=None, description="WP install path on server")
    wp_upload_dir: str = Field(
        default="/var/www/html/viewmath/wp-content/uploads/books",
        description="Remote dir for uploaded PDFs",
    )

    # Product defaults
    default_status: str = "publish"
    default_catalog_visibility: str = "visible"

    # Default prices per book type (override via .env or --price flag)
    price_all_in_one: str = "14.99"
    price_study_guide: str = "9.99"
    price_workbook: str = "9.99"
    price_step_by_step: str = "9.99"
    price_3_practice_tests: str = "5.99"
    price_5_practice_tests: str = "7.99"
    price_7_practice_tests: str = "9.99"
    price_10_practice_tests: str = "12.99"
    price_in_30_days: str = "9.99"
    price_quiz: str = "7.99"
    price_puzzles: str = "7.99"
    price_worksheet: str = "7.99"


_settings: WCSettings | None = None


def get_settings() -> WCSettings:
    global _settings
    if _settings is None:
        _settings = WCSettings()  # type: ignore[call-arg]
    return _settings


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class DownloadableFile(BaseModel):
    name: str
    file: str  # URL


class ProductCategory(BaseModel):
    id: int


class ProductCreate(BaseModel):
    name: str
    type: str = "simple"
    status: str = "draft"
    catalog_visibility: str = "visible"
    description: str = ""
    short_description: str = ""
    sku: str = ""
    regular_price: str = ""
    sale_price: str = ""
    virtual: bool = True
    downloadable: bool = True
    downloads: list[DownloadableFile] = Field(default_factory=list)
    download_limit: int = -1
    download_expiry: int = -1
    categories: list[ProductCategory] = Field(default_factory=list)
    images: list[dict] = Field(default_factory=list)


# ============================================================================
# WP CLIENT
# ============================================================================

class WPClient:
    """Unified WooCommerce REST API + WP-CLI over SSH client."""

    def __init__(self, cfg: WCSettings) -> None:
        self.site_url = cfg.wc_site_url.rstrip("/")
        self.ssh_host = cfg.wp_ssh_host
        self.wp_path = cfg.wp_path
        self.upload_dir = cfg.wp_upload_dir
        self._api = API(
            url=self.site_url,
            consumer_key=cfg.wc_consumer_key,
            consumer_secret=cfg.wc_consumer_secret,
            version="wc/v3",
            timeout=30,
        )

    # ── WooCommerce REST ─────────────────────────────────────────────────

    def wc_get(self, endpoint: str, **params: Any) -> Any:
        resp = self._api.get(endpoint, params=params)
        resp.raise_for_status()
        return resp.json()

    def wc_post(self, endpoint: str, data: dict) -> Any:
        resp = self._api.post(endpoint, data)
        resp.raise_for_status()
        return resp.json()

    def wc_put(self, endpoint: str, data: dict) -> Any:
        resp = self._api.put(endpoint, data)
        resp.raise_for_status()
        return resp.json()

    def wc_get_all(self, endpoint: str, **params: Any) -> list[dict]:
        """Paginate through all results."""
        params.setdefault("per_page", 100)
        page = 1
        results: list[dict] = []
        while True:
            resp = self._api.get(endpoint, params={**params, "page": page})
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break
            results.extend(batch)
            if page >= int(resp.headers.get("X-WP-TotalPages", 1)):
                break
            page += 1
        return results

    # ── SSH / WP-CLI ─────────────────────────────────────────────────────

    def _ssh(self, cmd: str) -> str:
        if not self.ssh_host:
            raise RuntimeError("WP_SSH_HOST must be set in .env for SSH commands.")
        result = subprocess.run(
            f"ssh {self.ssh_host} '{cmd}'",
            shell=True, capture_output=True, text=True,
        )
        if result.returncode != 0 and result.stderr.strip():
            raise RuntimeError(f"SSH error: {result.stderr.strip()}")
        return result.stdout.strip()

    def wp_cli(self, args: str) -> str:
        if not self.wp_path:
            raise RuntimeError("WP_PATH must be set in .env for WP-CLI commands.")
        return self._ssh(f"cd {self.wp_path} && wp {args} --allow-root 2>/dev/null")

    def scp_upload(self, local: Path, remote: str) -> None:
        if not self.ssh_host:
            raise RuntimeError("WP_SSH_HOST must be set in .env for SCP.")
        r = subprocess.run(
            f"scp '{local}' {self.ssh_host}:'{remote}'",
            shell=True, capture_output=True, text=True,
        )
        if r.returncode != 0:
            raise RuntimeError(f"SCP error: {r.stderr.strip()}")

    def ensure_remote_dir(self, path: str) -> None:
        self._ssh(f"mkdir -p '{path}'")

    def import_media(self, remote_path: str, title: str = "") -> tuple[int, str]:
        """Import file into WP media library. Returns (attachment_id, url)."""
        title_flag = f'--title="{title}"' if title else ""
        output = self.wp_cli(f'media import "{remote_path}" {title_flag} --porcelain')
        att_id = output.strip()
        if not att_id.isdigit():
            raise RuntimeError(f"Unexpected media import output: {output}")
        rel_path = self.wp_cli(f"post meta get {att_id} _wp_attached_file")
        return int(att_id), f"{self.site_url}/wp-content/uploads/{rel_path}"


_client: WPClient | None = None


def get_client() -> WPClient:
    global _client
    if _client is None:
        _client = WPClient(get_settings())
    return _client


# ============================================================================
# BOOK HELPERS
# ============================================================================

# BOOK_DISPLAY_NAMES imported from config.py (single source of truth)


def _validate_book_type(bt: str) -> None:
    if bt not in BOOK_TYPES:
        console.print(f"[red]Unknown book type: {bt}[/]")
        console.print(f"[dim]Valid: {', '.join(BOOK_TYPES)}[/]")
        raise typer.Exit(1)


def _validate_state(slug: str) -> None:
    cfg = load_config(find_workspace())
    if slug not in cfg.all_state_slugs:
        console.print(f"[red]Unknown state: {slug}[/]")
        raise typer.Exit(1)


def _state_name(slug: str) -> str:
    cfg = load_config(find_workspace())
    return cfg.state_display_names.get(slug, slug.replace("-", " ").title())


def _product_name(bt: str, state: str) -> str:
    """Full product title using centralized book_title() from config.py."""
    state_name = _state_name(state)
    return book_title(bt, state, state_name)


def _product_sku(bt: str, state: str) -> str:
    s = get_settings()
    return f"{s.grade_slug}-{bt.replace('_', '-')}-{state}"


def _product_short_description(bt: str, state: str) -> str:
    s = get_settings()
    desc = BOOK_TYPES[bt].get("description", "")
    state_name = _state_name(state)
    return (
        f"<p>{s.grade_display} {BOOK_DISPLAY_NAMES.get(bt, bt)} "
        f"for <strong>{state_name}</strong>. {desc}. "
        f"Aligned to {state_name} state standards and Common Core (CCSS).</p>"
    )


def _product_description(bt: str, state: str) -> str:
    s = get_settings()
    cfg = BOOK_TYPES[bt]
    display = BOOK_DISPLAY_NAMES.get(bt, bt)
    state_name = _state_name(state)
    tconfig = load_config(find_workspace())

    chapters_html = ""
    for ch in tconfig.chapters:
        topics_li = "".join(f"<li>{t.name}</li>" for t in ch.topics)
        title = ch.title.replace("\\&", "&amp;")
        chapters_html += f"<h4>Chapter {ch.num}: {title}</h4><ul>{topics_li}</ul>"

    additional_ids = tconfig.state_additional.get(state, [])
    additional_html = ""
    if additional_ids:
        items = "".join(
            f"<li>{tconfig.topic_names.get(tid, tid)}</li>" for tid in additional_ids
        )
        additional_html = f"<h4>Bonus {state_name}-Specific Topics</h4><ul>{items}</ul>"

    test_info = ""
    if "test_range" in cfg:
        start, end = cfg["test_range"]
        test_info = (
            f"<p>Includes <strong>{end - start + 1} full-length practice tests</strong>, "
            f"each covering all {s.grade_display} topics.</p>"
        )

    return f"""
<h2>{s.grade_display} {display} — {state_name} Edition</h2>
<p>A kid-friendly math resource aligned to <strong>{state_name}</strong>
state standards and Common Core (CCSS).</p>
{test_info}
<p>{cfg.get('description', '')}</p>
<h3>What's Inside</h3>
{chapters_html}
{additional_html}
<h3>Features</h3>
<ul>
  <li>Colorful, engaging design</li>
  <li>Step-by-step examples and worked solutions</li>
  <li>Practice problems with complete answer key</li>
  <li>Aligned to {state_name} standards</li>
  <li>Printable PDF format</li>
</ul>""".strip()


def _find_latest_pdf(bt: str, state: str) -> Path | None:
    s = get_settings()
    output_dir = find_workspace() / "final_output" / BOOK_TYPES[bt]["output_subdir"]
    if not output_dir.exists():
        return None
    pattern = f"{bt}_{state}-{s.grade_slug}_*.pdf"
    pdfs = sorted(output_dir.glob(pattern), reverse=True)
    return pdfs[0] if pdfs else None


def _find_preview_pdf(bt: str, state: str) -> Path | None:
    """Find the preview PDF for a book type (prefix preview_)."""
    s = get_settings()
    from config import ALL_BOOK_TYPES  # noqa: E402
    preview_key = f"preview_{bt}"
    if preview_key not in ALL_BOOK_TYPES:
        return None
    subdir = ALL_BOOK_TYPES[preview_key]["output_subdir"]
    output_dir = find_workspace() / "final_output" / subdir
    if not output_dir.exists():
        return None
    pattern = f"preview_{bt}_{state}-{s.grade_slug}_*.pdf"
    pdfs = sorted(output_dir.glob(pattern), reverse=True)
    return pdfs[0] if pdfs else None


def _extract_cover_jpeg(pdf: Path) -> Path | None:
    """Extract page 1 of a PDF as a JPEG using pdftoppm. Returns temp file path."""
    try:
        tmp_dir = Path(tempfile.mkdtemp())
        prefix = str(tmp_dir / "cover")
        r = subprocess.run(
            ["pdftoppm", "-jpeg", "-f", "1", "-l", "1", "-r", "150", str(pdf), prefix],
            capture_output=True,
        )
        if r.returncode != 0:
            return None
        candidates = sorted(tmp_dir.glob("cover*.jpg"))
        return candidates[0] if candidates else None
    except FileNotFoundError:
        return None  # pdftoppm not installed


def _state_category_slug(state: str) -> str:
    """SEO-friendly category slug, e.g. 'grade-4-math-texas-staar-teks'."""
    s = get_settings()
    exams = _load_state_exams()
    currs = _load_state_curriculums()
    parts = [s.grade_slug, "math", state]
    exam = exams.get(state, {})
    curr = currs.get(state, {})
    if exam.get("exam_acronym"):
        parts.append(exam["exam_acronym"].lower().replace(" ", "-").replace(".", ""))
    if curr.get("curriculum_acronym"):
        # avoid duplicating if exam and curriculum acronym are the same
        curr_slug = curr["curriculum_acronym"].lower().replace(" ", "-").replace(".", "")
        if curr_slug != parts[-1]:
            parts.append(curr_slug)
    return "-".join(parts)


def _state_category_name(state: str) -> str:
    """Human-readable category title, e.g. 'Grade 7 Math Texas – STAAR & TEKS'."""
    s = get_settings()
    state_name = _state_name(state)
    exams = _load_state_exams()
    currs = _load_state_curriculums()
    exam_acr = exams.get(state, {}).get("exam_acronym", "")
    curr_acr = currs.get(state, {}).get("curriculum_acronym", "")
    tags: list[str] = []
    if exam_acr:
        tags.append(exam_acr)
    if curr_acr and curr_acr != exam_acr:
        tags.append(curr_acr)
    suffix = f" – {' & '.join(tags)}" if tags else ""
    return f"{s.grade_display} {state_name}{suffix}"


def _state_category_description(state: str) -> str:
    """Short SEO-friendly description for a state's product category."""
    s = get_settings()
    state_name = _state_name(state)
    exams = _load_state_exams()
    currs = _load_state_curriculums()
    exam = exams.get(state, {})
    curr = currs.get(state, {})
    exam_acr = exam.get("exam_acronym", "")
    curr_acr = curr.get("curriculum_acronym", "")
    exam_name = exam.get("exam_name", "")
    exam_months = exam.get("exam_months", "")

    lines = [
        f"{s.grade_display} is a key year for building math foundations.",
    ]
    if curr_acr:
        lines.append(
            f"In {state_name}, the curriculum follows the {curr_acr} standards."
        )
    if exam_acr and exam_months:
        lines.append(
            f"Students take the {exam_acr} in {exam_months}."
        )
    lines.append(
        f"Boost your {s.grade_display} performance with our comprehensive "
        f"selection of study materials! From step-by-step guides to practice "
        f"tests, our books are designed to help students master every topic "
        f"and excel on the {exam_acr or 'state'} exam."
    )
    return " ".join(lines)


def _resolve_state_category_id(state: str) -> int | None:
    """Find the WC product category ID for a state. Returns None if missing."""
    cats = get_client().wc_get_all("products/categories")
    slug = _state_category_slug(state)
    for c in cats:
        if c["slug"] == slug:
            return c["id"]
    return None


# ============================================================================
# COMMANDS — Category
# ============================================================================

@app.command("setup-category")
def setup_category(
    state: str = typer.Argument(None, help="State slug (e.g. texas). Omit to create for ALL states."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be created."),
) -> None:
    """Create the WooCommerce product category for a state (or all states)."""
    if state is None:
        # All states
        config = load_config(find_workspace())
        created, skipped = 0, 0
        for slug in config.all_state_slugs:
            result = _create_state_category(slug, dry_run=dry_run)
            if result:
                created += 1
            else:
                skipped += 1
        console.print(f"\n[bold]Done:[/] {created} created, {skipped} already existed.")
    else:
        _validate_state(state)
        _create_state_category(state, dry_run=dry_run)


def _create_state_category(state: str, *, dry_run: bool = False) -> bool:
    """Create a single state category. Returns True if created, False if existed."""
    client = get_client()
    slug = _state_category_slug(state)
    name = _state_category_name(state)
    desc = _state_category_description(state)

    existing = client.wc_get_all("products/categories")
    for cat in existing:
        if cat["slug"] == slug:
            url = f"{get_settings().wc_site_url}/product-category/{slug}/"
            console.print(f"[dim]{name} — already exists (ID: {cat['id']})[/]")
            console.print(f"  [link={url}]{url}[/link]")
            _store_record_category(state, id=cat["id"], name=name, slug=slug, url=url)
            return False

    if dry_run:
        console.print(f"[yellow]Would create: {name}[/]")
        console.print(f"  [dim]slug: {slug}[/]")
        console.print(f"  [dim]desc: {desc[:80]}…[/]")
        return False

    cat = client.wc_post("products/categories", {
        "name": name, "slug": slug, "description": desc,
    })
    url = f"{get_settings().wc_site_url}/product-category/{slug}/"
    console.print(f"[green]Created: {name} (ID: {cat['id']})[/]")
    console.print(f"  [link={url}]{url}[/link]")
    _store_record_category(state, id=cat["id"], name=name, slug=slug, url=url)
    return True


# ============================================================================
# COMMANDS — Landing Page
# ============================================================================

@app.command("create-landing-page")
def create_landing_page(
    content_file: Optional[str] = typer.Option(None, "--content-file", help="HTML file with page content."),
    status: str = typer.Option("draft", "--status", help="Post status (draft/publish)."),
) -> None:
    """Create a WordPress post under 'Academy' category as the grade landing page.

    URL will be: {site}/academy/{grade_slug}/
    Pass --content-file to set the body, or update it later in wp-admin.
    """
    client = get_client()
    s = get_settings()

    # ── Ensure "Academy" post category exists ────────────────────────────
    output = client.wp_cli('term list category --slug=academy --format=json')
    cats = json.loads(output) if output.strip() else []
    if cats:
        academy_id = cats[0]["term_id"]
    else:
        academy_id = int(client.wp_cli(
            'term create category "Academy" --slug=academy --porcelain'
        ))
        console.print(f"[green]Created 'Academy' category (ID: {academy_id})[/]")

    # ── Check if landing page already exists ─────────────────────────────
    existing = client.wp_cli(
        f'post list --post_type=post --name={s.grade_slug} --format=json'
    )
    posts = json.loads(existing) if existing.strip() else []
    if posts:
        post_id = posts[0]["ID"]
        console.print(
            f"[dim]Landing page already exists (ID: {post_id}, slug: {s.grade_slug})[/]"
        )
        console.print(
            f"[dim]Edit: {client.site_url}/wp-admin/post.php?post={post_id}&action=edit[/]"
        )
        return

    # ── Create the post ──────────────────────────────────────────────────
    if content_file:
        local = Path(content_file)
        if not local.exists():
            console.print(f"[red]File not found: {content_file}[/]")
            raise typer.Exit(1)
        remote_tmp = f"/tmp/{s.grade_slug}-landing.html"
        client.scp_upload(local, remote_tmp)
        post_id = client.wp_cli(
            f'post create {remote_tmp} --post_type=post '
            f'--post_title="{s.grade_display}" --post_name="{s.grade_slug}" '
            f'--post_status={status} --post_category={academy_id} --porcelain'
        )
        client._ssh(f"rm -f {remote_tmp}")
    else:
        placeholder = f"Landing page for {s.grade_display}. Content coming soon."
        post_id = client.wp_cli(
            f'post create --post_type=post '
            f'--post_title="{s.grade_display}" --post_name="{s.grade_slug}" '
            f'--post_status={status} --post_category={academy_id} '
            f'--post_content="{placeholder}" --porcelain'
        )

    console.print(
        f"[green]Created landing page (ID: {post_id.strip()}, slug: {s.grade_slug})[/]"
    )
    console.print(f"[dim]URL: {client.site_url}/academy/{s.grade_slug}/[/]")


# ============================================================================
# COMMANDS — Upload & Product Creation
# ============================================================================

@app.command("upload-book")
def upload_book(
    book_type: str = typer.Argument(..., help="Book type key (use show-book-types to list)."),
    state: str = typer.Argument(..., help="State slug (e.g. texas)."),
    price: Optional[str] = typer.Option(None, "--price", help="Regular price. Defaults to per-book price from .env."),
    sale_price: Optional[str] = typer.Option(None, "--sale-price", help="Sale price."),
    status: Optional[str] = typer.Option(None, "--status", help="Product status override."),
    pdf_path: Optional[str] = typer.Option(None, "--pdf", help="Explicit PDF path."),
    skip_upload: bool = typer.Option(False, "--skip-upload", help="Create product without uploading PDF."),
) -> None:
    """Upload a single book: find PDF → SCP → media import → create/update WC product."""
    _validate_book_type(book_type)
    _validate_state(state)
    result = _upload_book_impl(
        book_type=book_type, state=state, price=price,
        sale_price=sale_price, status=status,
        pdf_path=pdf_path, skip_upload=skip_upload,
    )
    console.print(Panel(
        f"  ID:     {result['id']}\n"
        f"  Name:   {result['name']}\n"
        f"  SKU:    {result.get('sku', '')}\n"
        f"  Price:  ${result.get('regular_price', '')}\n"
        f"  Status: {result.get('status', '')}\n"
        f"  URL:    {result.get('permalink', 'N/A')}",
        title="[bold green]Done[/]",
    ))


@app.command("upload-all-books")
def upload_all_books(
    state: str = typer.Argument(..., help="State slug (e.g. texas)."),
    price: Optional[str] = typer.Option(None, "--price", help="Price applied to all books. Omit to use per-book defaults from .env."),
    sale_price: Optional[str] = typer.Option(None, "--sale-price"),
    status: Optional[str] = typer.Option(None, "--status"),
    types: Optional[str] = typer.Option(
        None, "--types", help="Comma-separated book types (default: all).",
    ),
    skip_upload: bool = typer.Option(False, "--skip-upload"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Upload all available book types for a state."""
    _validate_state(state)

    keys = [t.strip() for t in types.split(",")] if types else list(BOOK_TYPES)
    for k in keys:
        _validate_book_type(k)

    # Scan for PDFs
    available: list[tuple[str, Path | None]] = []
    for bt in keys:
        pdf = _find_latest_pdf(bt, state)
        if pdf or skip_upload:
            available.append((bt, pdf))

    if not available:
        console.print(f"[red]No PDFs found for {_state_name(state)}. Compile books first.[/]")
        raise typer.Exit(1)

    # Show plan
    table = Table(title=f"Books to upload for {_state_name(state)}")
    table.add_column("Book Type", style="green")
    table.add_column("PDF", style="dim")
    table.add_column("Size", justify="right")
    for bt, pdf in available:
        table.add_row(
            BOOK_DISPLAY_NAMES.get(bt, bt),
            pdf.name if pdf else "(skip upload)",
            f"{pdf.stat().st_size / (1024 * 1024):.1f} MB" if pdf else "—",
        )
    console.print(table)

    if dry_run:
        console.print(f"\n[yellow]Dry run — {len(available)} books would be uploaded.[/]")
        return

    if not typer.confirm(f"\nUpload {len(available)} books for {_state_name(state)}?"):
        raise typer.Abort()

    success, failed = 0, 0
    for bt, pdf in available:
        console.print(f"\n{'─' * 60}")
        console.print(f"[bold]{BOOK_DISPLAY_NAMES.get(bt, bt)}[/]")
        try:
            _upload_book_impl(
                book_type=bt, state=state, price=price or _default_price(bt),
                sale_price=sale_price, status=status,
                pdf_path=str(pdf) if pdf else None, skip_upload=skip_upload,
            )
            success += 1
        except Exception as e:
            console.print(f"[red]Failed: {e}[/]")
            failed += 1

    console.print(f"\n{'═' * 60}")
    console.print(f"[bold]Results:[/] {success} OK, {failed} failed (of {len(available)})")


def _upload_book_impl(
    book_type: str,
    state: str,
    price: str | None = None,
    sale_price: str | None = None,
    status: str | None = None,
    pdf_path: str | None = None,
    skip_upload: bool = False,
) -> dict:
    """Shared upload logic. Returns the WC product dict."""
    price = price or _default_price(book_type)
    client = get_client()
    settings = get_settings()
    download_url: str | None = None
    cover_image_id: int | None = None
    preview_download_url: str | None = None

    # ── Upload main PDF ──────────────────────────────────────────────────
    if not skip_upload:
        local_pdf = Path(pdf_path) if pdf_path else _find_latest_pdf(book_type, state)
        if not local_pdf or not local_pdf.exists():
            raise RuntimeError(f"PDF not found for {book_type}/{state}")

        client.ensure_remote_dir(client.upload_dir)
        remote = f"{client.upload_dir}/{local_pdf.name}"

        with console.status("Uploading PDF via SCP..."):
            client.scp_upload(local_pdf, remote)
        console.print("  [green]✓[/] Uploaded PDF")

        with console.status("Importing into media library..."):
            _, download_url = client.import_media(
                remote, title=_product_name(book_type, state),
            )
        console.print(f"  [green]✓[/] Media URL: {download_url}")

        # ── Extract + upload cover image (page 1) ────────────────────────
        with console.status("Extracting cover image..."):
            cover_jpeg = _extract_cover_jpeg(local_pdf)
        if cover_jpeg:
            remote_cover = f"{client.upload_dir}/{cover_jpeg.name}"
            with console.status("Uploading cover image..."):
                client.scp_upload(cover_jpeg, remote_cover)
            with console.status("Importing cover into media library..."):
                cover_image_id, _ = client.import_media(
                    remote_cover,
                    title=f"{_product_name(book_type, state)} — Cover",
                )
            console.print(f"  [green]✓[/] Cover image (ID: {cover_image_id})")
            client._ssh(f"rm -f '{remote_cover}'")
            shutil.rmtree(cover_jpeg.parent, ignore_errors=True)
        else:
            console.print("  [dim]Cover extraction skipped (pdftoppm not found)[/]")

        # ── Upload preview PDF ───────────────────────────────────────────
        preview_pdf = _find_preview_pdf(book_type, state)
        if preview_pdf and preview_pdf.exists():
            remote_preview = f"{client.upload_dir}/{preview_pdf.name}"
            with console.status("Uploading preview PDF..."):
                client.scp_upload(preview_pdf, remote_preview)
            with console.status("Importing preview into media library..."):
                _, preview_download_url = client.import_media(
                    remote_preview,
                    title=f"{_product_name(book_type, state)} — Free Preview",
                )
            console.print(f"  [green]✓[/] Preview URL: {preview_download_url}")
        else:
            console.print("  [dim]No preview PDF found — skipping[/]")

    # ── Resolve state category ────────────────────────────────────────────
    cat_id = _resolve_state_category_id(state)
    categories = [ProductCategory(id=cat_id)] if cat_id else []
    if not cat_id:
        console.print(
            f"[yellow]Warning: category not found for {state}. Run setup-category {state} first.[/]"
        )

    # ── Build description (append preview CTA if available) ──────────────
    description = _product_description(book_type, state)
    if preview_download_url:
        cta = (
            f'\n<p style="text-align:center;margin-top:16px;">'
            f'<a href="{preview_download_url}" target="_blank" '
            f'style="display:inline-block;padding:12px 24px;background:#f0a500;'
            f'color:#fff;font-weight:bold;border-radius:6px;text-decoration:none;">'
            f'📄 Download Free Preview</a></p>'
        )
        description += cta

    # ── Build images list ─────────────────────────────────────────────────
    images = [{"id": cover_image_id}] if cover_image_id else []

    # ── Create or update product ─────────────────────────────────────────
    sku = _product_sku(book_type, state)
    existing = client.wc_get("products", sku=sku)

    if existing:
        product_id = existing[0]["id"]
        update: dict[str, Any] = {
            "regular_price": price,
            "description": description,
            "short_description": _product_short_description(book_type, state),
        }
        if sale_price:
            update["sale_price"] = sale_price
        if status:
            update["status"] = status
        if images:
            update["images"] = images
        if download_url:
            downloads_list = [{"name": f"{_product_name(book_type, state)}.pdf", "file": download_url}]
            if preview_download_url:
                downloads_list.append({"name": "Free Preview.pdf", "file": preview_download_url})
            update["downloads"] = downloads_list
        if categories:
            update["categories"] = [c.model_dump() for c in categories]

        result = client.wc_put(f"products/{product_id}", update)
        console.print(f"  [green]✓[/] Updated product {product_id}")
    else:
        downloads: list[DownloadableFile] = []
        if download_url:
            downloads.append(DownloadableFile(
                name=f"{_product_name(book_type, state)}.pdf", file=download_url,
            ))
        if preview_download_url:
            downloads.append(DownloadableFile(
                name="Free Preview.pdf", file=preview_download_url,
            ))

        product = ProductCreate(
            name=_product_name(book_type, state),
            status=status or settings.default_status,
            catalog_visibility=settings.default_catalog_visibility,
            sku=sku,
            regular_price=price,
            sale_price=sale_price or "",
            description=description,
            short_description=_product_short_description(book_type, state),
            downloads=downloads,
            categories=categories,
            images=images,
        )
        result = client.wc_post("products", product.model_dump(exclude_none=True))
        console.print(f"  [green]✓[/] Created product {result['id']}")

    _store_record_product(state, book_type, result)
    return result


# ============================================================================
# COMMANDS — Check & List
# ============================================================================

@app.command("check-books")
def check_books(
    state: str = typer.Argument(..., help="State slug (e.g. texas)."),
) -> None:
    """Show upload status and URLs for all book types for a state."""
    _validate_state(state)
    client = get_client()
    state_name = _state_name(state)

    cat_id = _resolve_state_category_id(state)
    if not cat_id:
        console.print(f"[red]Category not found for {state_name}. Run setup-category {state} first.[/]")
        raise typer.Exit(1)

    products = client.wc_get_all("products", category=str(cat_id))
    by_sku: dict[str, dict] = {p.get("sku", ""): p for p in products}

    table = Table(title=f"Books for {state_name}")
    table.add_column("Book Type", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("DL", justify="right")
    table.add_column("Product URL", style="dim")

    uploaded = 0
    for bt in BOOK_TYPES:
        sku = _product_sku(bt, state)
        p = by_sku.get(sku)
        if p:
            uploaded += 1
            table.add_row(
                BOOK_DISPLAY_NAMES.get(bt, bt),
                p.get("status", "?"),
                str(p["id"]),
                f"${p.get('regular_price', '?')}",
                str(len(p.get("downloads", []))),
                p.get("permalink", ""),
            )
        else:
            table.add_row(
                BOOK_DISPLAY_NAMES.get(bt, bt),
                "[red]NOT UPLOADED[/]",
                "—", "—", "—", "—",
            )

    console.print(table)
    console.print(
        f"\n[bold]{uploaded}[/] of {len(BOOK_TYPES)} books uploaded for {state_name}."
    )


@app.command("list-products")
def list_products(
    state: str = typer.Argument(..., help="State slug (e.g. texas)."),
    per_page: int = typer.Option(20, help="Number of products."),
    all_pages: bool = typer.Option(False, "--all", help="Fetch all products."),
) -> None:
    """List all WooCommerce products in a state's category."""
    _validate_state(state)
    client = get_client()
    cat_id = _resolve_state_category_id(state)
    if not cat_id:
        console.print(f"[red]Category not found for {state}. Run setup-category {state} first.[/]")
        raise typer.Exit(1)

    params: dict[str, Any] = {"per_page": per_page, "category": str(cat_id)}
    products = (
        client.wc_get_all("products", **params)
        if all_pages
        else client.wc_get("products", **params)
    )

    table = Table(title=f"Products in '{_state_category_name(state)}' ({len(products)})")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("SKU", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Price", justify="right")
    table.add_column("DL", justify="right")
    for p in products:
        table.add_row(
            str(p.get("id", "")),
            p.get("sku", ""),
            p.get("name", ""),
            p.get("status", ""),
            p.get("price", ""),
            str(len(p.get("downloads", []))),
        )
    console.print(table)


# ============================================================================
# COMMANDS — Info
# ============================================================================

@app.command("show-book-types")
def show_book_types() -> None:
    """List all available book types and their descriptions."""
    table = Table(title="Available Book Types")
    table.add_column("Key", style="cyan")
    table.add_column("Display Name", style="green")
    table.add_column("Description")
    for key, cfg in BOOK_TYPES.items():
        table.add_row(key, BOOK_DISPLAY_NAMES.get(key, key), cfg.get("description", ""))
    console.print(table)


@app.command("show-states")
def show_states() -> None:
    """List all available state slugs from topics_config.yaml."""
    config = load_config(find_workspace())
    table = Table(title=f"Available States ({len(config.all_state_slugs)})")
    table.add_column("Slug", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Additional", justify="right")
    table.add_column("Modified", justify="right")
    for slug in config.all_state_slugs:
        table.add_row(
            slug,
            config.state_display_names.get(slug, ""),
            str(len(config.state_additional.get(slug, []))),
            str(len(config.state_modified.get(slug, {}))),
        )
    console.print(table)


@app.command("show-pdfs")
def show_pdfs(
    state: str = typer.Argument(..., help="State slug (e.g. texas)."),
) -> None:
    """Show all available PDFs in final_output/ for a state."""
    _validate_state(state)

    table = Table(title=f"Available PDFs for {_state_name(state)}")
    table.add_column("Book Type", style="green")
    table.add_column("PDF File", style="dim")
    table.add_column("Size", justify="right")
    table.add_column("Date", style="cyan")

    found = 0
    for bt in BOOK_TYPES:
        pdf = _find_latest_pdf(bt, state)
        if pdf:
            size_mb = pdf.stat().st_size / (1024 * 1024)
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})\.pdf$", pdf.name)
            table.add_row(
                BOOK_DISPLAY_NAMES.get(bt, bt),
                pdf.name,
                f"{size_mb:.1f} MB",
                date_match.group(1) if date_match else "?",
            )
            found += 1
        else:
            table.add_row(
                BOOK_DISPLAY_NAMES.get(bt, bt), "[dim]not found[/]", "—", "—",
            )

    console.print(table)
    console.print(f"\n[bold]{found}[/] of {len(BOOK_TYPES)} book types have PDFs ready.")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app()