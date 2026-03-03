"""
Shared configuration loader for Grade 6 book generation scripts.

Reads topics_config.yaml and provides structured data that both
generate_state_books.py and generate_practice_tests.py consume.

Usage:
    from config_loader import load_config

    config = load_config()              # auto-detect workspace
    config = load_config(workspace)     # explicit path

Returned TopicsConfig object provides:
    config.chapters           — list of Chapter objects (num, title, core topic IDs)
    config.core_topic_ids     — flat ordered list of all core CCSS topic IDs
    config.additional_topics  — list of AdditionalTopic objects (id, name, file, chapter)
    config.topic_filenames    — dict mapping every topic ID → file slug
    config.topic_names        — dict mapping every topic ID → display name
    config.topic_chapter      — dict mapping every topic ID → chapter number
    config.all_state_slugs    — ordered list of all 50 state slugs
    config.state_display_names — dict mapping slug → display name
    config.state_additional    — dict mapping slug → list of additional topic IDs
    config.state_modified      — dict mapping slug → list of modified topic IDs

Note: The YAML file uses full file slugs (e.g. 'ch01-02-place-value-thousands')
in each state's additional/modified lists for readability.  The loader
resolves these to short topic IDs (e.g. 'ch01-02') so downstream code
can continue using IDs as dictionary keys.
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class TopicEntry:
    """A single topic within a chapter."""
    id: str       # e.g. 'ch01-01'
    name: str     # e.g. 'Place Value: Ones, Tens, Hundreds'
    file: str     # e.g. 'ch01-01-place-value-ones-tens-hundreds'


@dataclass
class Chapter:
    """A chapter with its ordered list of core topics."""
    num: int               # 1–7
    title: str             # LaTeX-safe title (may contain \\&)
    topics: List[TopicEntry]

    @property
    def core_topic_ids(self) -> List[str]:
        return [t.id for t in self.topics]


@dataclass
class AdditionalTopic:
    """A supplementary topic beyond CCSS, assigned to a chapter."""
    id: str
    name: str
    file: str
    chapter: int           # which chapter this belongs to


@dataclass
class In30DaysDay:
    """A single day entry in the 30-day book config."""
    day: int             # 1–30
    file: str            # e.g. 'day-01-place-value-ones-tens-hundreds'
    topics: List[str]    # list of topic IDs covered (e.g. ['ch01-01'])
    bonus_after: List[str] = field(default_factory=list)  # additional topic IDs to insert after


@dataclass
class In30DaysChapter:
    """A chapter boundary in the 30-day book."""
    chapter: int         # chapter number
    title: str           # LaTeX chapter title
    start_day: int       # first day in this chapter
    end_day: int         # last day in this chapter


@dataclass
class In30DaysConfig:
    """Parsed in_30_days section from topics_config.yaml."""
    days: List[In30DaysDay]
    chapters: List[In30DaysChapter]


@dataclass
class TopicsConfig:
    """Complete parsed configuration from topics_config.yaml."""

    chapters: List[Chapter]
    additional_topics_list: List[AdditionalTopic]

    # State data
    all_state_slugs: List[str]
    state_display_names: Dict[str, str]
    state_additional: Dict[str, List[str]]   # slug → additional topic IDs
    state_modified: Dict[str, List[str]]     # slug → modified topic IDs

    # In-30-days config (may be None if not present in YAML)
    in_30_days_config: Optional[In30DaysConfig] = None

    # ── Derived lookups (built once in __post_init__) ───────────────────

    # Flat ordered list of all core topic IDs
    core_topic_ids: List[str] = field(default_factory=list, init=False)

    # Every topic ID → file slug  (core + additional)
    topic_filenames: Dict[str, str] = field(default_factory=dict, init=False)

    # Every topic ID → display name
    topic_names: Dict[str, str] = field(default_factory=dict, init=False)

    # Every topic ID → chapter number
    topic_chapter: Dict[str, int] = field(default_factory=dict, init=False)

    def __post_init__(self):
        # Core topics
        for ch in self.chapters:
            for t in ch.topics:
                self.core_topic_ids.append(t.id)
                self.topic_filenames[t.id] = t.file
                self.topic_names[t.id] = t.name
                self.topic_chapter[t.id] = ch.num

        # Additional topics
        for at in self.additional_topics_list:
            self.topic_filenames[at.id] = at.file
            self.topic_names[at.id] = at.name
            self.topic_chapter[at.id] = at.chapter


# ============================================================================
# YAML LOADER
# ============================================================================

def find_workspace(start: Optional[Path] = None) -> Path:
    """Auto-detect workspace root by searching upward for topics_config.yaml + studyGuide.cls.

    Starts from the given path (or the directory containing this module) and
    walks up to 8 parent directories looking for the sentinel files.
    """
    candidate = (start or Path(__file__).resolve().parent)
    for _ in range(8):
        if (candidate / "topics_config.yaml").exists() and (candidate / "studyGuide.cls").exists():
            return candidate
        candidate = candidate.parent
    print("ERROR: Could not find workspace root (looked for topics_config.yaml + studyGuide.cls)")
    sys.exit(1)


def load_config(workspace: Optional[Path] = None) -> TopicsConfig:
    """Load topics_config.yaml from the workspace root and return a TopicsConfig.

    Args:
        workspace: Explicit workspace path; auto-detected if None.

    Returns:
        A fully-populated TopicsConfig object.
    """
    ws = workspace or find_workspace()
    yaml_path = ws / "topics_config.yaml"

    if not yaml_path.exists():
        print(f"ERROR: Configuration file not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    # ── Parse chapters ──────────────────────────────────────────────────
    chapters: List[Chapter] = []
    for ch_raw in raw["chapters"]:
        topics = [
            TopicEntry(id=t["id"], name=t["name"], file=t["file"])
            for t in ch_raw["topics"]
        ]
        chapters.append(Chapter(
            num=ch_raw["num"],
            title=ch_raw["title"],
            topics=topics,
        ))

    # ── Parse additional topics ─────────────────────────────────────────
    additional_topics: List[AdditionalTopic] = []
    for at_raw in raw.get("additional_topics", []):
        additional_topics.append(AdditionalTopic(
            id=at_raw["id"],
            name=at_raw["name"],
            file=at_raw["file"],
            chapter=at_raw["chapter"],
        ))

    # ── Parse states ────────────────────────────────────────────────────
    # Build a reverse map: file slug → topic ID  (covers core + additional)
    # so that the YAML can use full slugs for readability while we keep
    # short IDs internally.
    file_to_id: Dict[str, str] = {}
    all_known_ids: Set[str] = set()
    for ch in chapters:
        for t in ch.topics:
            file_to_id[t.file] = t.id
            all_known_ids.add(t.id)
    for at in additional_topics:
        file_to_id[at.file] = at.id
        all_known_ids.add(at.id)

    def _resolve_topic_ref(ref: str) -> str:
        """Accept either a file slug or a bare topic ID and return the ID."""
        if ref in file_to_id:
            return file_to_id[ref]
        if ref in all_known_ids:
            return ref
        print(f"WARNING: Unknown topic reference '{ref}' in topics_config.yaml")
        return ref

    all_slugs: List[str] = []
    display_names: Dict[str, str] = {}
    state_additional: Dict[str, List[str]] = {}
    state_modified: Dict[str, List[str]] = {}

    for slug, state_raw in raw["states"].items():
        all_slugs.append(slug)
        display_names[slug] = state_raw["name"]

        additional = [_resolve_topic_ref(r) for r in state_raw.get("additional", [])]
        modified = [_resolve_topic_ref(r) for r in state_raw.get("modified", [])]

        if additional:
            state_additional[slug] = additional
        if modified:
            state_modified[slug] = modified

    # ── Parse in_30_days config (optional) ──────────────────────────────
    in_30_days_cfg: Optional[In30DaysConfig] = None
    if "in_30_days" in raw:
        raw_30 = raw["in_30_days"]
        days_list: List[In30DaysDay] = []
        for d in raw_30.get("days", []):
            days_list.append(In30DaysDay(
                day=d["day"],
                file=d["file"],
                topics=d.get("topics", []),
                bonus_after=d.get("bonus_after", []),
            ))
        chapters_30: List[In30DaysChapter] = []
        for c in raw_30.get("chapters", []):
            chapters_30.append(In30DaysChapter(
                chapter=c["chapter"],
                title=c["title"],
                start_day=c["start_day"],
                end_day=c["end_day"],
            ))
        in_30_days_cfg = In30DaysConfig(days=days_list, chapters=chapters_30)

    return TopicsConfig(
        chapters=chapters,
        additional_topics_list=additional_topics,
        all_state_slugs=all_slugs,
        state_display_names=display_names,
        state_additional=state_additional,
        state_modified=state_modified,
        in_30_days_config=in_30_days_cfg,
    )
