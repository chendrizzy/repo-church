#!/usr/bin/env python3
"""Deterministic helper CLI for repo-bible.

The goal is to move repetitive repo inspection and packet validation out of the
LLM context window. The CLI intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import fnmatch
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import deque
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "templates"

DOC_NAMES = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTEXT.md",
    "DESIGN.md",
    "PRD.md",
    "SPEC.md",
    "ROADMAP.md",
    "REQUIREMENTS.md",
    "SYSTEM-MAP.md",
    "MARKET-ANALYSIS.md",
}

DOC_KEYWORDS = (
    "planning",
    "spec",
    "prd",
    "roadmap",
    "requirement",
    "research",
    "market",
    "architecture",
    "system-map",
    "design",
    "brand",
    "persona",
    "gtm",
    "go-to-market",
    "validation",
    "audit",
    "commandment",
    "bible",
    "doctrine",
)

SOURCE_EXTS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".py",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".swift",
    ".rb",
    ".php",
    ".cs",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
}

TEST_HINTS = ("test", "spec", "__tests__", "tests/")
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQ_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*-\d{2,}\b")

CHURCH_README_TEMPLATE = """# Repo Church

Operator map for **Repo Church** outputs in this repository. All **Repo Bible** packet artifacts default under **`bible/`** here. Override locations with `repo_bible.py` `--church-root`, `--bible-dir`, or the `CHURCH_ROOT` environment variable when you intentionally use a non-standard layout.

## Directory layout

| Path | Purpose |
|------|---------|
| `bible/` | Markdown packet (requirements, roadmap, audits), `_repo-bible-*.md` tool reports, `vision-intake.html`, and optional `html/` rendered bundle for human review. |
| `runs/` | Local scratch and throwaway exports (typically gitignored). |
| `index.json` | Small manifest updated by `repo_bible.py scaffold` (paths relative to the repository root). |

## Quick commands (from repository root)

```bash
python path/to/repo_bible.py inventory --root .
python path/to/repo_bible.py scaffold --root .
python path/to/repo_bible.py validate --root .
python path/to/repo_bible.py render-html --root .
python path/to/repo_bible.py intake-html --root .
```

Use `--legacy-planning-bible` to read or write the older `.planning/commandments` packet during migration. See the **repo-bible** `SKILL.md` for full workflows.
"""


def resolved_repo_root(ns: argparse.Namespace) -> Path:
    return Path(getattr(ns, "root", ".") or ".").resolve()


def resolve_church_bible_paths(repo_root: Path, ns: argparse.Namespace) -> tuple[Path, Path]:
    """Return (church_root, bible_dir)."""
    if getattr(ns, "legacy_planning_bible", False):
        church = (repo_root / ".church").resolve()
        bible = (repo_root / ".planning" / "commandments").resolve()
        return church, bible
    env = (os.environ.get("CHURCH_ROOT") or "").strip()
    cr_raw = getattr(ns, "church_root", None) or (env if env else None)
    if cr_raw:
        cr_path = Path(cr_raw)
        church_root = cr_path.resolve() if cr_path.is_absolute() else (repo_root / cr_path).resolve()
    else:
        church_root = (repo_root / ".church").resolve()
    bd_raw = getattr(ns, "bible_dir", None)
    if bd_raw:
        bd_path = Path(bd_raw)
        bible_dir = bd_path.resolve() if bd_path.is_absolute() else (church_root / bd_path).resolve()
    else:
        bible_dir = (church_root / "bible").resolve()
    return church_root, bible_dir


def inject_resolved_church_paths(ns: argparse.Namespace) -> tuple[Path, Path, Path]:
    repo_root = resolved_repo_root(ns)
    church_root, bible_dir = resolve_church_bible_paths(repo_root, ns)
    setattr(ns, "_repo_root", repo_root)
    setattr(ns, "_church_root", church_root)
    setattr(ns, "_bible_dir", bible_dir)
    return repo_root, church_root, bible_dir


def ensure_church_operator_artifacts(church_root: Path, bible_dir: Path, repo_root: Path) -> None:
    church_root.mkdir(parents=True, exist_ok=True)
    readme = church_root / "README.md"
    if not readme.exists():
        readme.write_text(CHURCH_README_TEMPLATE, encoding="utf-8")
    idx = church_root / "index.json"
    payload = {
        "version": 1,
        "church_root": rel(church_root, repo_root),
        "bible_dir": rel(bible_dir, repo_root),
    }
    idx.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def add_church_cli_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--church-root",
        metavar="PATH",
        help="Repo Church umbrella directory (default: <root>/.church, or set CHURCH_ROOT)",
    )
    p.add_argument(
        "--bible-dir",
        metavar="PATH",
        help="Bible packet directory (default: <church-root>/bible; absolute or relative to church-root)",
    )
    p.add_argument(
        "--legacy-planning-bible",
        action="store_true",
        help="Use legacy packet path <root>/.planning/commandments instead of .church/bible",
    )


def requirement_prefix_pattern(csv: str | None) -> re.Pattern[str] | None:
    if not csv or not str(csv).strip():
        return None
    parts = [p.strip().upper() for p in csv.split(",") if p.strip()]
    parts = [p for p in parts if re.fullmatch(r"[A-Z][A-Z0-9]*", p)]
    if not parts:
        return None
    parts_sorted = sorted(set(parts), key=len, reverse=True)
    alt = "|".join(re.escape(p) for p in parts_sorted)
    return re.compile(rf"\b(?:{alt})-\d{{2,}}\b")


HTML_STYLE = """
:root {
  color-scheme: light;
  --ink: #0b0f14;
  --muted: #52606d;
  --rule: #d7dee8;
  --paper: #f8fafc;
  --panel: #ffffff;
  --blue: #1d4ed8;
  --green: #15803d;
  --amber: #b45309;
  --red: #b91c1c;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--paper);
  color: var(--ink);
  line-height: 1.55;
}
header {
  position: sticky;
  top: 0;
  z-index: 2;
  padding: 18px 28px;
  background: rgba(248, 250, 252, 0.92);
  border-bottom: 1px solid var(--rule);
  backdrop-filter: blur(10px);
}
main { max-width: 1180px; margin: 0 auto; padding: 28px; }
nav { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.panel, section {
  background: var(--panel);
  border: 1px solid var(--rule);
  border-radius: 8px;
  padding: 20px;
  margin: 18px 0;
}
table { width: 100%; border-collapse: collapse; background: var(--panel); }
th, td { border: 1px solid var(--rule); padding: 8px 10px; vertical-align: top; }
th { background: #eef2f7; text-align: left; }
code, pre, textarea, input {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
}
pre { overflow: auto; background: #0b0f14; color: #f8fafc; padding: 14px; border-radius: 8px; }
blockquote { border-left: 4px solid var(--blue); margin-left: 0; padding-left: 14px; color: var(--muted); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }
.field { display: grid; gap: 6px; margin-bottom: 14px; }
label { font-weight: 650; }
textarea, input, select {
  width: 100%;
  border: 1px solid var(--rule);
  border-radius: 8px;
  padding: 10px;
  background: #fff;
  color: var(--ink);
}
textarea { min-height: 110px; resize: vertical; }
button {
  border: 1px solid var(--blue);
  background: var(--blue);
  color: #fff;
  padding: 10px 12px;
  border-radius: 8px;
  font-weight: 650;
  cursor: pointer;
}
button.secondary { background: #fff; color: var(--blue); }
.status { color: var(--muted); font-size: 14px; }
.pill { display: inline-flex; padding: 3px 8px; border: 1px solid var(--rule); border-radius: 999px; font-size: 12px; color: var(--muted); }
""".strip()


@dataclass
class FileSummary:
    path: str
    lines: int
    bytes: int
    headings: list[str]


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


@dataclass(frozen=True)
class WalkOptions:
    """Path filtering while walking a directory tree."""

    use_default_excludes: bool = True
    extra_excludes: tuple[str, ...] = ()
    walk_base: Path | None = None


def effective_walk_options(opts: WalkOptions | None) -> WalkOptions:
    return opts if opts is not None else WalkOptions()


def _basename_spill_excluded(name: str) -> bool:
    lower = name.lower()
    if lower in ("_inventory.md", "_validation.md", "_sources.md", "vision-intake.html", "_claim-scan.md"):
        return True
    if lower.endswith(".md") and "claim" in lower and "scan" in lower:
        return True
    return False


def _segment_excluded(segment: str) -> bool:
    if segment.startswith("_repo-bible-"):
        return True
    if segment.endswith("-html"):
        return True
    return False


def path_matches_excludes(rel_posix: str, basename: str, opts: WalkOptions) -> bool:
    """True if this relative path (to walk_base) or basename should be skipped."""
    opts = effective_walk_options(opts)
    if opts.use_default_excludes:
        if _basename_spill_excluded(basename):
            return True
        for segment in rel_posix.split("/"):
            if segment and _segment_excluded(segment):
                return True
    for pattern in opts.extra_excludes:
        if fnmatch.fnmatch(rel_posix, pattern) or fnmatch.fnmatch(basename, pattern):
            return True
    return False


def _is_church_runs_dir(rel_posix: str) -> bool:
    p = rel_posix.replace("\\", "/")
    return p == ".church/runs" or p.startswith(".church/runs/")


def iter_files(root: Path, include_hidden: bool = False, walk_options: WalkOptions | None = None) -> Iterable[Path]:
    opts = effective_walk_options(walk_options)
    base = opts.walk_base if opts.walk_base is not None else root
    skip_dirs = {
        ".git",
        "node_modules",
        ".next",
        "dist",
        "build",
        "coverage",
        ".venv",
        "venv",
        "__pycache__",
        ".turbo",
        ".cache",
    }
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        pruned: list[str] = []
        for d in dirnames:
            if d in skip_dirs:
                continue
            if not include_hidden and d.startswith(".") and d not in (".planning", ".church"):
                continue
            candidate = current / d
            try:
                rel_dir = rel(candidate, base)
            except ValueError:
                rel_dir = candidate.as_posix()
            if _is_church_runs_dir(rel_dir):
                continue
            if path_matches_excludes(rel_dir, d, opts):
                continue
            pruned.append(d)
        dirnames[:] = pruned
        for name in filenames:
            if not include_hidden and name.startswith(".") and current.name not in (".planning", ".church"):
                continue
            full = current / name
            try:
                rel_file = rel(full, base)
            except ValueError:
                rel_file = full.as_posix()
            if path_matches_excludes(rel_file, name, opts):
                continue
            yield full


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def line_count(path: Path) -> int:
    text = read_text(path)
    return text.count("\n") + (1 if text else 0)


def is_doc(path: Path, root: Path) -> bool:
    name = path.name
    r = rel(path, root).lower()
    return (
        path.suffix.lower() in {".md", ".mdx", ".txt"}
        and (name in DOC_NAMES or any(k in r for k in DOC_KEYWORDS))
    )


def summarize_doc(path: Path, root: Path, max_headings: int = 8) -> FileSummary:
    text = read_text(path)
    headings = []
    for line in text.splitlines():
        if line.startswith("#"):
            headings.append(line.strip())
        if len(headings) >= max_headings:
            break
    return FileSummary(
        path=rel(path, root),
        lines=text.count("\n") + (1 if text else 0),
        bytes=path.stat().st_size if path.exists() else 0,
        headings=headings,
    )


def git_output(root: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return ""
    return result.stdout.strip()


def walk_options_from_args(args: argparse.Namespace, walk_base: Path | None = None) -> WalkOptions:
    extra: list[str] = []
    for raw in getattr(args, "exclude", None) or []:
        extra.extend(p for p in raw.split("|") if p)
    return WalkOptions(
        use_default_excludes=not getattr(args, "no_default_excludes", False),
        extra_excludes=tuple(extra),
        walk_base=walk_base,
    )


def build_inventory(root: Path, walk_options: WalkOptions | None = None) -> dict:
    opts = effective_walk_options(walk_options)
    opts = WalkOptions(
        use_default_excludes=opts.use_default_excludes,
        extra_excludes=opts.extra_excludes,
        walk_base=opts.walk_base if opts.walk_base is not None else root,
    )
    files = list(iter_files(root, walk_options=opts))
    docs = [summarize_doc(p, root) for p in files if is_doc(p, root)]
    docs.sort(key=lambda d: d.path)

    source_files = [p for p in files if p.suffix.lower() in SOURCE_EXTS]
    test_files = [
        p
        for p in source_files
        if any(hint in rel(p, root).lower() for hint in TEST_HINTS)
        or p.name.lower().endswith((".test.ts", ".spec.ts", ".test.tsx", ".spec.tsx", "_test.py"))
    ]
    source_lines = sum(line_count(p) for p in source_files)
    test_lines = sum(line_count(p) for p in test_files)

    package_files = [
        rel(p, root)
        for p in files
        if p.name
        in {
            "package.json",
            "pyproject.toml",
            "Cargo.toml",
            "go.mod",
            "requirements.txt",
            "pom.xml",
            "build.gradle",
            "schema.prisma",
        }
    ]
    package_files.sort()

    return {
        "root": str(root),
        "git_branch": git_output(root, ["branch", "--show-current"]),
        "git_status_short": git_output(root, ["status", "--short"]).splitlines(),
        "counts": {
            "total_files_scanned": len(files),
            "documents": len(docs),
            "source_files": len(source_files),
            "source_lines": source_lines,
            "test_files": len(test_files),
            "test_lines": test_lines,
        },
        "package_files": package_files,
        "documents": [asdict(d) for d in docs],
    }


def markdown_inventory(data: dict) -> str:
    lines = [
        "# Repo Bible Inventory",
        "",
        f"- Root: `{data['root']}`",
        f"- Git branch: `{data.get('git_branch') or 'unknown'}`",
        "",
        "## Counts",
        "",
    ]
    for key, value in data["counts"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Package And Schema Files", ""])
    for path in data["package_files"] or ["(none found)"]:
        lines.append(f"- `{path}`")
    lines.extend(["", "## Candidate Evidence Documents", ""])
    for doc in data["documents"]:
        lines.append(f"- `{doc['path']}` ({doc['lines']} lines)")
        for heading in doc["headings"][:5]:
            lines.append(f"  - {heading}")
    lines.extend(["", "## Git Status", ""])
    for status in data["git_status_short"] or ["clean or unavailable"]:
        lines.append(f"- `{status}`")
    return "\n".join(lines) + "\n"


def command_inventory(args: argparse.Namespace) -> int:
    repo_root, _, bible_dir = inject_resolved_church_paths(args)
    root = repo_root
    data = build_inventory(root, walk_options_from_args(args, walk_base=root))
    output = json.dumps(data, indent=2) if args.format == "json" else markdown_inventory(data)
    out_target = args.output
    if out_target is None:
        bible_dir.mkdir(parents=True, exist_ok=True)
        ext = ".json" if args.format == "json" else ".md"
        out_target = str(bible_dir / f"_repo-bible-inventory{ext}")
    write_or_print(output, out_target)
    return 0


def template_map() -> dict[str, str]:
    return {
        "packet-index.md": "README.md",
        "success-requirements.md": "success-requirements.md",
        "market-watchlist.md": "market-watchlist.md",
        "principles-doctrine.md": "principles-doctrine.md",
        "architecture-map.md": "architecture-map.md",
        "design-doctrine.md": "design-doctrine.md",
        "ux-workflows.md": "ux-workflows.md",
        "persona-gtm.md": "persona-gtm.md",
        "roadmap.md": "roadmap.md",
        "alignment-audit.md": "alignment-audit.md",
        "validation-report.md": "validation-report.md",
    }


def command_scaffold(args: argparse.Namespace) -> int:
    repo_root, church_root, bible_dir = inject_resolved_church_paths(args)
    output_dir = Path(args.output).resolve() if args.output else bible_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    created = []
    skipped = []
    for src_name, dest_name in template_map().items():
        src = TEMPLATES / src_name
        dest = output_dir / dest_name
        if dest.exists() and not args.force:
            skipped.append(dest_name)
            continue
        shutil.copyfile(src, dest)
        created.append(dest_name)
    ensure_church_operator_artifacts(church_root, output_dir, repo_root)
    result = {
        "repo_root": str(repo_root),
        "church_root": str(church_root),
        "output_dir": str(output_dir),
        "created": created,
        "skipped": skipped,
    }
    write_or_print(json.dumps(result, indent=2) + "\n", args.report)
    return 0


def extract_urls(paths: Iterable[Path], root: Path) -> list[dict]:
    rows = []
    for path in paths:
        text = read_text(path)
        for match in URL_RE.finditer(text):
            rows.append({"path": rel(path, root), "url": match.group(0).rstrip(".,;")})
    return rows


def is_under_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_local_md_link(from_file: Path, target: str, repo_root: Path) -> Path | None:
    if target.startswith(("http://", "https://", "#", "mailto:")):
        return None
    clean = target.split("#", 1)[0].split(":", 1)[0]
    if not clean or clean.startswith("<"):
        clean = clean.strip("<>")
    if not clean:
        return None
    candidate = (from_file.parent / clean).resolve()
    if not candidate.exists() or not candidate.is_file():
        return None
    if candidate.suffix.lower() not in {".md", ".mdx"}:
        return None
    if not is_under_root(candidate, repo_root):
        return None
    return candidate


def collect_markdown_closure(
    seed_files: list[Path],
    repo_root: Path,
    walk_options: WalkOptions | None,
    follow: bool,
    max_depth: int,
) -> tuple[list[Path], dict]:
    seeds = sorted({p.resolve() for p in seed_files if p.exists() and p.suffix.lower() in {".md", ".mdx"}})
    opts_in = effective_walk_options(walk_options)
    walk_base = opts_in.walk_base if opts_in.walk_base is not None else repo_root
    opts = WalkOptions(
        use_default_excludes=opts_in.use_default_excludes,
        extra_excludes=opts_in.extra_excludes,
        walk_base=walk_base,
    )

    def excluded_path(p: Path) -> bool:
        try:
            rel_p = rel(p, walk_base)
        except ValueError:
            rel_p = p.as_posix()
        return path_matches_excludes(rel_p, p.name, opts)

    traversal: dict = {
        "mode": "expanded" if follow else "packet_local_only",
        "max_depth": max_depth,
        "seed_files": [rel(p, repo_root) for p in seeds],
        "expanded_files": [],
    }
    if not follow:
        out = sorted(seeds, key=lambda x: rel(x, repo_root))
        traversal["expanded_files"] = [rel(p, repo_root) for p in out]
        return out, traversal

    visited: set[Path] = set()
    ordered: list[Path] = []
    q: deque[tuple[Path, int]] = deque((s, 0) for s in seeds)

    while q:
        path, depth = q.popleft()
        rp = path.resolve()
        if rp in visited:
            continue
        if excluded_path(rp):
            continue
        visited.add(rp)
        ordered.append(rp)
        if depth >= max_depth:
            continue
        text = read_text(rp)
        for target in MD_LINK_RE.findall(text):
            nxt = resolve_local_md_link(rp, target, repo_root)
            if nxt is None:
                continue
            nxt = nxt.resolve()
            if nxt not in visited and not excluded_path(nxt):
                q.append((nxt, depth + 1))

    ordered = sorted(ordered, key=lambda x: rel(x, repo_root))
    traversal["expanded_files"] = [rel(p, repo_root) for p in ordered]
    return ordered, traversal


def command_sources(args: argparse.Namespace) -> int:
    repo_root, _, bible_dir = inject_resolved_church_paths(args)
    root = repo_root
    base = Path(args.path).resolve() if args.path else bible_dir
    if not base.exists():
        print(f"repo-bible: sources: path does not exist: {base}", file=sys.stderr)
        return 2
    walk_opts = walk_options_from_args(args, walk_base=base)
    seed_paths = [
        p
        for p in iter_files(base, include_hidden=True, walk_options=walk_opts)
        if p.suffix.lower() in {".md", ".mdx"}
    ]
    follow = getattr(args, "follow_local_md", False)
    max_depth = max(0, int(getattr(args, "link_depth", 3) or 3))
    paths, link_traversal = collect_markdown_closure(seed_paths, root, walk_opts, follow, max_depth)
    rows = extract_urls(paths, root)
    if args.format == "json":
        payload = {"link_traversal": link_traversal, "urls": rows}
        output = json.dumps(payload, indent=2) + "\n"
    else:
        lines = ["# Source URL Inventory", "", "## Link Traversal", ""]
        lines.append(f"- mode: `{link_traversal['mode']}`")
        lines.append(f"- max_depth: {link_traversal['max_depth']}")
        lines.append(f"- seeds: {len(link_traversal['seed_files'])}")
        lines.append(f"- files: {len(link_traversal['expanded_files'])}")
        lines.append("")
        lines.append("## URLs")
        lines.append("")
        for row in rows:
            lines.append(f"- `{row['path']}`: {row['url']}")
        output = "\n".join(lines) + "\n"
    out_target = args.output
    if out_target is None:
        bible_dir.mkdir(parents=True, exist_ok=True)
        ext = ".json" if args.format == "json" else ".md"
        out_target = str(bible_dir / f"_repo-bible-sources{ext}")
    write_or_print(output, out_target)
    return 0


def validate_markdown_file(path: Path, root: Path) -> dict:
    text = read_text(path)
    errors = []
    warnings = []
    if text.count("```") % 2:
        errors.append("unbalanced fenced code blocks")
    trailing = [i + 1 for i, line in enumerate(text.splitlines()) if line.rstrip() != line]
    if trailing:
        errors.append(f"trailing whitespace lines: {trailing[:10]}")
    for target in MD_LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0].split(":", 1)[0]
        if not clean or clean.startswith("<"):
            clean = clean.strip("<>")
        candidate = (path.parent / clean).resolve()
        if clean and not candidate.exists():
            warnings.append(f"missing local link target: {target}")
    return {
        "path": rel(path, root),
        "errors": errors,
        "warnings": warnings,
        "requirement_ids": sorted(set(REQ_ID_RE.findall(text))),
        "urls": sorted(set(URL_RE.findall(text))),
    }


def command_validate(args: argparse.Namespace) -> int:
    repo_root, _, bible_dir = inject_resolved_church_paths(args)
    root = repo_root
    packet = Path(args.path).resolve() if args.path else bible_dir
    if not packet.exists():
        print(f"repo-bible: validate: packet directory does not exist: {packet}", file=sys.stderr)
        return 2
    walk_opts = walk_options_from_args(args, walk_base=packet)
    seed_paths = [
        p
        for p in iter_files(packet, include_hidden=True, walk_options=walk_opts)
        if p.suffix.lower() in {".md", ".mdx"}
    ]
    follow = getattr(args, "follow_local_md", False)
    max_depth = max(0, int(getattr(args, "link_depth", 3) or 3))
    paths, link_traversal = collect_markdown_closure(seed_paths, root, walk_opts, follow, max_depth)

    results = [validate_markdown_file(p, root) for p in paths]
    required = [
        "success-requirements",
        "market",
        "principles",
        "architecture",
        "design",
        "ux",
        "persona",
        "roadmap",
        "audit",
        "validation",
    ]
    names_and_text = " ".join(
        [p.name.lower() for p in paths] + [read_text(p).lower() for p in paths]
    )
    missing_sections = [r for r in required if r not in names_and_text]
    all_ids = sorted({rid for result in results for rid in result["requirement_ids"]})
    prefix_re = requirement_prefix_pattern(getattr(args, "requirement_prefixes", None))
    allowed_ids = sorted({rid for rid in all_ids if prefix_re and prefix_re.fullmatch(rid)})
    unknown_ids = sorted({rid for rid in all_ids if prefix_re and not prefix_re.fullmatch(rid)})
    if prefix_re is None:
        allowed_ids = []
        unknown_ids = []

    error_count = sum(len(r["errors"]) for r in results)
    warning_count = sum(len(r["warnings"]) for r in results)
    id_policy_errors = len(unknown_ids)
    data = {
        "root": str(root),
        "packet": str(packet),
        "files_checked": len(results),
        "error_count": error_count,
        "warning_count": warning_count,
        "missing_expected_artifact_terms": missing_sections,
        "requirement_id_count": len(all_ids),
        "requirement_ids": all_ids,
        "requirement_ids_allowed": allowed_ids,
        "requirement_ids_unknown": unknown_ids,
        "link_traversal": link_traversal,
        "results": results,
    }
    if args.format == "json":
        output = json.dumps(data, indent=2) + "\n"
    else:
        output = markdown_validation(data)
    out_target = args.output
    if out_target is None:
        bible_dir.mkdir(parents=True, exist_ok=True)
        ext = ".json" if args.format == "json" else ".md"
        out_target = str(bible_dir / f"_repo-bible-validation{ext}")
    write_or_print(output, out_target)
    return 1 if error_count or id_policy_errors else 0


def markdown_validation(data: dict) -> str:
    lines = [
        "# Repo Bible Packet Validation",
        "",
        f"- Packet: `{data['packet']}`",
        f"- Files checked: {data['files_checked']}",
        f"- Errors: {data['error_count']}",
        f"- Warnings: {data['warning_count']}",
        f"- Requirement IDs: {data['requirement_id_count']}",
        "",
    ]
    lt = data.get("link_traversal") or {}
    lines.extend(
        [
            "## Link Traversal",
            "",
            f"- mode: `{lt.get('mode', '')}`",
            f"- max_depth: {lt.get('max_depth', 0)}",
            f"- seed_files: {len(lt.get('seed_files') or [])}",
            f"- expanded_files: {len(lt.get('expanded_files') or [])}",
            "",
        ]
    )
    unk = data.get("requirement_ids_unknown") or []
    if unk:
        lines.extend(["## Unknown Requirement IDs", ""])
        for rid in unk:
            lines.append(f"- `{rid}`")
        lines.append("")
    if data["missing_expected_artifact_terms"]:
        lines.append("## Missing Expected Artifact Terms")
        lines.append("")
        for item in data["missing_expected_artifact_terms"]:
            lines.append(f"- `{item}`")
        lines.append("")
    lines.append("## File Results")
    lines.append("")
    for result in data["results"]:
        status = "FAIL" if result["errors"] else "PASS"
        lines.append(f"- `{result['path']}`: {status}")
        for err in result["errors"]:
            lines.append(f"  - error: {err}")
        for warn in result["warnings"][:5]:
            lines.append(f"  - warning: {warn}")
    return "\n".join(lines) + "\n"


CLAIM_SCAN_EXTENSIONS = {".md", ".mdx", ".tsx", ".ts", ".jsx", ".js"}


def load_claim_config(path: Path | None) -> dict:
    if path is None:
        return {}
    p = path.resolve()
    if not p.exists():
        return {}
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError:
        return {}


def quote_and_tick_intervals(line: str) -> list[tuple[int, int]]:
    """Balanced ASCII double-quoted spans (honors \\ escapes) and inline `...` (not ```)."""
    intervals: list[tuple[int, int]] = []
    i = 0
    while i < len(line):
        if line[i] == '"':
            start = i
            j = i + 1
            while j < len(line):
                if line[j] == "\\" and j + 1 < len(line):
                    j += 2
                    continue
                if line[j] == '"':
                    intervals.append((start, j + 1))
                    i = j + 1
                    break
                j += 1
            else:
                i += 1
            continue
        i += 1
    i = 0
    while i < len(line):
        if line[i] == "`":
            if i + 2 < len(line) and line[i : i + 3] == "```":
                i += 3
                continue
            j = i + 1
            while j < len(line) and line[j] != "`":
                j += 1
            if j < len(line):
                intervals.append((i, j + 1))
                i = j + 1
                continue
        i += 1
    return intervals


def occurrence_in_quote_or_tick(line: str, start: int, end: int) -> bool:
    for lo, hi in quote_and_tick_intervals(line):
        if start < hi and end > lo:
            return True
    return False


def iter_case_insensitive_occurrences(line: str, needle: str) -> Iterable[tuple[int, int]]:
    if not needle:
        return
    h, n = line.lower(), needle.lower()
    pos = 0
    while True:
        i = h.find(n, pos)
        if i < 0:
            break
        yield i, i + len(needle)
        pos = i + max(len(needle), 1)


def command_claim_scan(args: argparse.Namespace) -> int:
    repo_root, _, bible_dir = inject_resolved_church_paths(args)
    root = repo_root
    path = Path(args.path).resolve() if args.path else bible_dir
    if not path.exists():
        print(f"repo-bible: claim-scan: path does not exist: {path}", file=sys.stderr)
        return 2
    walk_opts = walk_options_from_args(args, walk_base=path)
    code_files = [
        p
        for p in iter_files(path, include_hidden=True, walk_options=walk_opts)
        if p.suffix.lower() in CLAIM_SCAN_EXTENSIONS
    ]
    md_seeds = [p for p in code_files if p.suffix.lower() in {".md", ".mdx"}]
    follow = getattr(args, "follow_local_md", False)
    max_depth = max(0, int(getattr(args, "link_depth", 3) or 3))
    md_extra, link_traversal = collect_markdown_closure(md_seeds, root, walk_opts, follow, max_depth)
    files = sorted(set(code_files) | set(md_extra), key=lambda p: rel(p, root))

    banned = [p for raw in args.banned for p in raw.split("|") if p]
    required = [p for raw in args.required for p in raw.split("|") if p]
    cc = getattr(args, "claim_config", None)
    cfg = load_claim_config(Path(cc).resolve() if cc else None)
    allow_substrings: list[str] = list(cfg.get("allow_substrings") or [])
    use_quote = not getattr(args, "no_quote_allowlist", False)

    banned_hits: list[dict] = []
    quote_skipped = 0
    config_skipped = 0
    corpus: list[str] = []

    for file in files:
        text = read_text(file)
        corpus.append(text.lower())
        for pattern in banned:
            for i, line in enumerate(text.splitlines(), start=1):
                if any(s and s.lower() in line.lower() for s in allow_substrings):
                    for _ in iter_case_insensitive_occurrences(line, pattern):
                        config_skipped += 1
                    continue
                for start, end in iter_case_insensitive_occurrences(line, pattern):
                    if use_quote and occurrence_in_quote_or_tick(line, start, end):
                        quote_skipped += 1
                        continue
                    banned_hits.append(
                        {
                            "path": rel(file, root),
                            "line": i,
                            "pattern": pattern,
                            "text": line.strip(),
                        }
                    )

    all_text = "\n".join(corpus)
    missing_required = [p for p in required if p.lower() not in all_text]
    data = {
        "banned_hits": banned_hits,
        "missing_required": missing_required,
        "files_scanned": len(files),
        "quote_skipped_hits": quote_skipped,
        "config_skipped_hits": config_skipped,
        "link_traversal": link_traversal,
    }
    output = json.dumps(data, indent=2) + "\n" if args.format == "json" else markdown_claim_scan(data)
    out_target = args.output
    if out_target is None:
        bible_dir.mkdir(parents=True, exist_ok=True)
        ext = ".json" if args.format == "json" else ".md"
        out_target = str(bible_dir / f"_repo-bible-claim-scan{ext}")
    write_or_print(output, out_target)
    return 1 if banned_hits or missing_required else 0


def markdown_claim_scan(data: dict) -> str:
    lines = ["# Claim Scan", "", f"- Files scanned: {data['files_scanned']}", ""]
    lt = data.get("link_traversal") or {}
    lines.extend(
        [
            "## Link Traversal",
            "",
            f"- mode: `{lt.get('mode', '')}`",
            f"- max_depth: {lt.get('max_depth', 0)}",
            f"- seed_files: {len(lt.get('seed_files') or [])}",
            f"- expanded_files: {len(lt.get('expanded_files') or [])}",
            "",
        ]
    )
    lines.append(f"- quote_skipped_hits: {data.get('quote_skipped_hits', 0)}")
    lines.append(f"- config_skipped_hits: {data.get('config_skipped_hits', 0)}")
    lines.append("")
    lines.append("## Banned Phrase Hits")
    lines.append("")
    if not data["banned_hits"]:
        lines.append("- None")
    for hit in data["banned_hits"]:
        lines.append(f"- `{hit['path']}:{hit['line']}` matched `{hit['pattern']}`: {hit['text']}")
    lines.extend(["", "## Missing Required Phrases", ""])
    if not data["missing_required"]:
        lines.append("- None")
    for phrase in data["missing_required"]:
        lines.append(f"- `{phrase}`")
    return "\n".join(lines) + "\n"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "section"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def table_to_html(rows: list[str]) -> str:
    parsed = []
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        parsed.append(cells)
    if len(parsed) >= 2 and all(set(cell) <= {"-", ":", " "} for cell in parsed[1]):
        header = parsed[0]
        body = parsed[2:]
    else:
        header = []
        body = parsed
    out = ["<table>"]
    if header:
        out.append("<thead><tr>")
        for cell in header:
            out.append(f"<th>{inline_markdown(cell)}</th>")
        out.append("</tr></thead>")
    out.append("<tbody>")
    for row in body:
        out.append("<tr>")
        for cell in row:
            out.append(f"<td>{inline_markdown(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def markdown_to_html(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    output: list[str] = []
    headings: list[tuple[int, str, str]] = []
    in_code = False
    code_lines: list[str] = []
    para: list[str] = []
    list_items: list[str] = []
    table_rows: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if para:
            output.append(f"<p>{inline_markdown(' '.join(para))}</p>")
            para = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            output.append("<ul>")
            for item in list_items:
                output.append(f"<li>{inline_markdown(item)}</li>")
            output.append("</ul>")
            list_items = []

    def flush_table() -> None:
        nonlocal table_rows
        if table_rows:
            output.append(table_to_html(table_rows))
            table_rows = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                flush_para()
                flush_list()
                flush_table()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            flush_para()
            flush_list()
            flush_table()
            continue
        if line.startswith("|") and line.endswith("|"):
            flush_para()
            flush_list()
            table_rows.append(line)
            continue
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            flush_para()
            flush_list()
            flush_table()
            level = len(match.group(1))
            title = match.group(2).strip()
            anchor = slugify(title)
            headings.append((level, title, anchor))
            output.append(f'<h{level} id="{anchor}">{inline_markdown(title)}</h{level}>')
            continue
        if line.startswith(">"):
            flush_para()
            flush_list()
            flush_table()
            output.append(f"<blockquote>{inline_markdown(line.lstrip('> ').strip())}</blockquote>")
            continue
        item = re.match(r"^\s*[-*]\s+(.*)$", line)
        if item:
            flush_para()
            flush_table()
            list_items.append(item.group(1).strip())
            continue
        para.append(line.strip())

    flush_para()
    flush_list()
    flush_table()
    if in_code:
        output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(output), headings


def html_document(title: str, body: str, nav: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{HTML_STYLE}</style>
</head>
<body>
<header>
<strong>{html.escape(title)}</strong>
{nav}
</header>
<main>
{body}
</main>
</body>
</html>
"""


def command_render_html(args: argparse.Namespace) -> int:
    repo_root, _, bible_dir = inject_resolved_church_paths(args)
    root = repo_root
    source = Path(args.path).resolve() if args.path else bible_dir
    if not source.exists():
        print(f"repo-bible: render-html: path does not exist: {source}", file=sys.stderr)
        return 2
    output_dir = Path(args.output).resolve() if args.output else (bible_dir / "html").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    walk_opts = walk_options_from_args(args, walk_base=source)
    markdown_files = [
        p
        for p in iter_files(source, include_hidden=True, walk_options=walk_opts)
        if p.suffix.lower() in {".md", ".mdx"}
    ]
    pages = []
    for path in sorted(markdown_files):
        body, headings = markdown_to_html(read_text(path))
        title = headings[0][1] if headings else path.stem
        dest_name = path.with_suffix(".html").name
        nav = '<nav><a href="index.html">Index</a></nav>'
        (output_dir / dest_name).write_text(html_document(title, body, nav), encoding="utf-8")
        pages.append({"source": rel(path, root), "html": dest_name, "title": title, "headings": headings})
    index_items = ["<section><h1>Repo Bible HTML Index</h1><ul>"]
    for page in pages:
        index_items.append(
            f'<li><a href="{html.escape(page["html"])}">{html.escape(page["title"])}</a> '
            f'<span class="pill">{html.escape(page["source"])}</span></li>'
        )
    index_items.append("</ul></section>")
    (output_dir / "index.html").write_text(
        html_document(args.title, "\n".join(index_items)), encoding="utf-8"
    )
    result = {"output_dir": str(output_dir), "pages": pages}
    write_or_print(json.dumps(result, indent=2) + "\n", args.report)
    return 0


def parse_intake_markdown_export(text: str) -> dict:
    """Parse markdown produced by the intake export (`## section` / `### prompt` / body)."""
    data: dict = {"generated_at": "", "sections": {}}
    current_section: str | None = None
    current_prompt: str | None = None
    body: list[str] = []

    def flush() -> None:
        nonlocal current_prompt, body, current_section
        if current_section and current_prompt is not None:
            ans = "\n".join(body).strip()
            data["sections"].setdefault(current_section, []).append({"prompt": current_prompt, "answer": ans})
        body.clear()

    for line in text.splitlines():
        if line.startswith("Generated:"):
            data["generated_at"] = line.split(":", 1)[1].strip()
            continue
        m2 = re.match(r"^##\s+(.+?)\s*$", line)
        if m2:
            flush()
            current_prompt = None
            current_section = m2.group(1).strip().lower()
            continue
        m3 = re.match(r"^###\s+(.+?)\s*$", line)
        if m3:
            if current_section:
                flush()
                current_prompt = m3.group(1).strip()
            continue
        if current_prompt is not None:
            body.append(line)
    flush()
    return data


def load_intake_prefill(path: Path) -> dict:
    text = read_text(path)
    if path.suffix.lower() == ".json":
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else {}
    return parse_intake_markdown_export(text)


def lookup_prefill_answer(prefill: dict | None, section: str, prompt: str) -> str:
    if not prefill:
        return ""
    sections = prefill.get("sections") or {}
    entries = sections.get(section, [])
    for entry in entries:
        if entry.get("prompt") == prompt:
            return (entry.get("answer") or "").strip()
    return ""


def intake_html(title: str, prefill: dict | None = None) -> str:
    sections = [
        ("vision", "Vision", ["What must this become?", "What must it never become?", "What belief makes this project non-obvious?"]),
        ("market", "Market", ["Who else is solving this?", "What threats should be watched?", "What timing signal makes now viable?"]),
        ("persona", "Persona", ["Who is the first must-win user?", "What pain forces action?", "What would make them switch?"]),
        ("product", "Product", ["What is the core job?", "What is the smallest complete version?", "What proof must be visible?"]),
        ("ux", "UX", ["If the user does X, what must happen?", "What failure must be recoverable?", "What must be obvious without explanation?"]),
        ("architecture", "Architecture", ["What exists now?", "What must be added?", "What must be removed or constrained?"]),
        ("design", "Design", ["What should it feel like?", "What visual patterns are banned?", "Which surfaces are non-negotiable?"]),
        ("gtm", "GTM", ["How do we create pre-launch pull?", "What launch motion fits the persona?", "What growth loop compounds?"]),
        ("success", "Success Requirements", ["What metrics prove it works?", "What gates block launch?", "What should be automated?"]),
        ("evidence", "Evidence", ["Local docs/assets to cite", "External sources to verify", "Known assumptions and open questions"]),
    ]
    section_html = []
    for key, label, prompts in sections:
        fields = [f"<h2>{html.escape(label)}</h2>"]
        for idx, prompt in enumerate(prompts, start=1):
            fid = f"{key}_{idx}"
            answer = lookup_prefill_answer(prefill, key, prompt)
            fields.append(
                f'<div class="field"><label for="{fid}">{html.escape(prompt)}</label>'
                f'<textarea id="{fid}" data-section="{key}" data-prompt="{html.escape(prompt)}">'
                f"{html.escape(answer)}</textarea></div>"
            )
        section_html.append(f'<section id="{key}">' + "\n".join(fields) + "</section>")
    nav = "<nav>" + "".join(f'<a href="#{key}">{html.escape(label)}</a>' for key, label, _ in sections) + "</nav>"
    script = r"""
const key = "repo-bible-intake-v1";
const fields = Array.from(document.querySelectorAll("textarea"));
function collect() {
  const data = { generated_at: new Date().toISOString(), sections: {} };
  for (const field of fields) {
    const section = field.dataset.section;
    data.sections[section] ||= [];
    data.sections[section].push({ prompt: field.dataset.prompt, answer: field.value.trim() });
  }
  return data;
}
function save() {
  localStorage.setItem(key, JSON.stringify(collect()));
  updateProgress();
}
function applyPrefill(data) {
  if (!data || !data.sections) return;
  for (const field of fields) {
    const entries = data.sections[field.dataset.section] || [];
    const found = entries.find(x => x.prompt === field.dataset.prompt);
    if (found) field.value = found.answer || "";
  }
  updateProgress();
}
function load() {
  const raw = localStorage.getItem(key);
  if (raw) {
    applyPrefill(JSON.parse(raw));
    return;
  }
  const prefillEl = document.getElementById("repo-bible-prefill");
  if (prefillEl && prefillEl.textContent.trim()) {
    try {
      const txt = prefillEl.textContent.trim();
      JSON.parse(txt);
      localStorage.setItem(key, txt);
      applyPrefill(JSON.parse(txt));
    } catch (e) {}
  }
}
function toMarkdown(data) {
  let out = "# Repo Bible Intake Export\n\n";
  out += `Generated: ${data.generated_at}\n\n`;
  for (const [section, entries] of Object.entries(data.sections)) {
    out += `## ${section}\n\n`;
    for (const entry of entries) {
      out += `### ${entry.prompt}\n\n${entry.answer || "[unanswered]"}\n\n`;
    }
  }
  return out;
}
function download(name, text, type) {
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = name; a.click();
  URL.revokeObjectURL(url);
}
function exportJSON() {
  download("repo-bible-intake.json", JSON.stringify(collect(), null, 2), "application/json");
}
function exportMarkdown() {
  download("repo-bible-intake.md", toMarkdown(collect()), "text/markdown");
}
function updateProgress() {
  const answered = fields.filter(f => f.value.trim()).length;
  document.getElementById("progress").textContent = `${answered}/${fields.length} answered`;
}
document.getElementById("save").addEventListener("click", save);
document.getElementById("json").addEventListener("click", exportJSON);
document.getElementById("markdown").addEventListener("click", exportMarkdown);
document.getElementById("clear").addEventListener("click", () => {
  if (confirm("Clear all local answers?")) {
    localStorage.removeItem(key);
    fields.forEach(f => f.value = "");
    updateProgress();
  }
});
document.getElementById("import").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  localStorage.setItem(key, await file.text());
  load();
});
fields.forEach(f => f.addEventListener("input", updateProgress));
load();
"""
    prefill_block = ""
    if prefill:
        dumped = json.dumps(prefill, ensure_ascii=True, separators=(",", ":"))
        dumped = dumped.replace("</", "<\\/")
        prefill_block = f'<script type="application/json" id="repo-bible-prefill">\n{dumped}\n</script>\n'

    body = f"""
<section>
<h1>{html.escape(title)}</h1>
<p class="status">Use this local workbench to capture the user's vision in structured form. Export JSON or Markdown and give that compact artifact to the agent instead of a long unstructured interview.</p>
<div class="grid">
<button id="save">Save locally</button>
<button id="json" class="secondary">Export JSON</button>
<button id="markdown" class="secondary">Export Markdown</button>
<button id="clear" class="secondary">Clear</button>
</div>
<p class="status">Progress: <span id="progress">0/0 answered</span></p>
<div class="field"><label for="import">Import prior JSON export</label><input id="import" type="file" accept="application/json,.json"></div>
</section>
{''.join(section_html)}
{prefill_block}<script>{script}</script>
"""
    return html_document(title, body, nav)


def command_intake_html(args: argparse.Namespace) -> int:
    _, _, bible_dir = inject_resolved_church_paths(args)
    output = Path(args.output).resolve() if args.output else (bible_dir / "vision-intake.html").resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    prefill = None
    if getattr(args, "prefill", None):
        prefill = load_intake_prefill(Path(args.prefill).resolve())
    output.write_text(intake_html(args.title, prefill), encoding="utf-8")
    write_or_print(json.dumps({"output": str(output)}, indent=2) + "\n", args.report)
    return 0


def write_or_print(text: str, output: str | None) -> None:
    if output is None or output == "-":
        print(text, end="")
        return
    out = Path(output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def add_walk_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help="Extra fnmatch patterns applied to paths relative to the walked directory",
    )
    parser.add_argument(
        "--no-default-excludes",
        action="store_true",
        help="Include _repo-bible-* paths, *-html directories, and spill artifacts such as _inventory.md",
    )


def add_link_follow_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--follow-local-md",
        action="store_true",
        help="Expand local .md/.mdx links from seeds (bounded by --link-depth, confined under --root)",
    )
    parser.add_argument(
        "--link-depth",
        type=int,
        default=3,
        help="Maximum depth when following local markdown links (default: 3)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Repo Bible deterministic helper CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    inv = sub.add_parser("inventory", help="Scan repo for Bible evidence and metrics")
    inv.add_argument("--root", default=".")
    inv.add_argument("--format", choices=["markdown", "json"], default="markdown")
    inv.add_argument(
        "--output",
        help="Write report here (default: <bible-dir>/_repo-bible-inventory.{md,json}; use - for stdout)",
    )
    add_walk_filters(inv)
    add_church_cli_args(inv)
    inv.set_defaults(func=command_inventory)

    scaf = sub.add_parser("scaffold", help="Create a Bible packet from templates")
    scaf.add_argument("--root", default=".")
    scaf.add_argument(
        "--output",
        help="Bible packet directory (default: <bible-dir> from --church-root / CHURCH_ROOT)",
    )
    scaf.add_argument("--force", action="store_true")
    scaf.add_argument("--report")
    add_church_cli_args(scaf)
    scaf.set_defaults(func=command_scaffold)

    src = sub.add_parser("sources", help="Extract source URLs from markdown files")
    src.add_argument("--root", default=".")
    src.add_argument(
        "--path",
        help="Directory to scan (default: <bible-dir>)",
    )
    src.add_argument("--format", choices=["markdown", "json"], default="markdown")
    src.add_argument(
        "--output",
        help="Write report here (default: <bible-dir>/_repo-bible-sources.{md,json}; use - for stdout)",
    )
    add_walk_filters(src)
    add_link_follow_args(src)
    add_church_cli_args(src)
    src.set_defaults(func=command_sources)

    val = sub.add_parser(
        "validate",
        help="Validate a Bible packet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="When --requirement-prefixes is set, requirement IDs found in the packet that do not match "
        "any allowed prefix (longest-prefix alternation) are reported as unknown and cause a non-zero exit, "
        "in addition to any markdown structural errors. Default packet path is <bible-dir>.",
    )
    val.add_argument("--root", default=".")
    val.add_argument(
        "--path",
        help="Packet directory (default: <bible-dir>)",
    )
    val.add_argument("--format", choices=["markdown", "json"], default="markdown")
    val.add_argument(
        "--output",
        help="Write report here (default: <bible-dir>/_repo-bible-validation.{md,json}; use - for stdout)",
    )
    val.add_argument(
        "--requirement-prefixes",
        help="Comma-separated allowed requirement ID prefixes before hyphen (e.g. S,E,C). Other IDs fail validation.",
    )
    add_walk_filters(val)
    add_link_follow_args(val)
    add_church_cli_args(val)
    val.set_defaults(func=command_validate)

    scan = sub.add_parser("claim-scan", help="Scan local files for banned and required phrases")
    scan.add_argument("--root", default=".")
    scan.add_argument(
        "--path",
        help="Directory or file tree root to scan (default: <bible-dir>)",
    )
    scan.add_argument("--banned", action="append", default=[])
    scan.add_argument("--required", action="append", default=[])
    scan.add_argument("--format", choices=["markdown", "json"], default="markdown")
    scan.add_argument(
        "--output",
        help="Write report here (default: <bible-dir>/_repo-bible-claim-scan.{md,json}; use - for stdout)",
    )
    scan.add_argument(
        "--claim-config",
        help="JSON file with keys such as allow_substrings (lines containing any skip all banned hits on that line)",
    )
    scan.add_argument(
        "--no-quote-allowlist",
        action="store_true",
        help="Do not skip banned matches inside ASCII double quotes or inline backticks",
    )
    add_walk_filters(scan)
    add_link_follow_args(scan)
    add_church_cli_args(scan)
    scan.set_defaults(func=command_claim_scan)

    render = sub.add_parser("render-html", help="Render a markdown Bible packet to browsable HTML")
    render.add_argument("--root", default=".")
    render.add_argument(
        "--path",
        help="Packet directory containing markdown (default: <bible-dir>)",
    )
    render.add_argument(
        "--output",
        help="HTML output directory (default: <bible-dir>/html)",
    )
    render.add_argument("--title", default="Repo Bible")
    render.add_argument("--report")
    add_walk_filters(render)
    add_church_cli_args(render)
    render.set_defaults(func=command_render_html)

    intake = sub.add_parser("intake-html", help="Create an interactive local HTML intake workbench")
    intake.add_argument("--root", default=".")
    intake.add_argument(
        "--output",
        help="Write HTML here (default: <bible-dir>/vision-intake.html)",
    )
    intake.add_argument("--title", default="Repo Bible Vision Intake")
    intake.add_argument(
        "--prefill",
        help="JSON or Markdown export matching the intake shape to pre-fill fields and embed as default data",
    )
    intake.add_argument("--report")
    add_church_cli_args(intake)
    intake.set_defaults(func=command_intake_html)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
