#!/usr/bin/env python3
"""GRC AI OS utility. Standard library only.

Deterministic checks that keep a GRC AI OS honest. No AI calls, no network.

    python scripts/grc_os.py status            # sources pending review, placeholders, register counts
    python scripts/grc_os.py lint              # broken links, fabricated quotes, missing sources, bad dates, duplicate IDs
    python scripts/grc_os.py pulse             # program health: overdue actions, expired exceptions, stale evidence
    python scripts/grc_os.py accept SOURCE     # record a reviewed source fingerprint
    python scripts/grc_os.py review            # status + lint + pulse, saved to audits/ (use for scheduled runs)

Exit codes: 0 = ok, 1 = validation errors (lint/accept/review), 2 = usage error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SKIP_DIRS = {".git", "archives", "audits", "brainstorms", "node_modules", "__pycache__", ".grc-os", "tests"}
SOURCES_DIR = "sources"
MANIFEST = Path(".grc-os") / "manifest.json"
SOURCE_PROVENANCE_FIELDS = ("title", "owner", "origin", "version_date", "captured")

DONE_STATUSES = {"done", "closed", "complete", "completed", "cancelled", "canceled", "resolved", "met", "retired"}
INACTIVE_EXCEPTION_STATUSES = DONE_STATUSES | {"revoked", "expired", "rejected"}
BLANK_VALUES = {"", "-", "—", "–", "tbd", "n/a", "na", "none", "unknown", "?"}

FREQUENCY_DAYS = {
    "continuous": 7, "daily": 1, "weekly": 7, "biweekly": 14, "monthly": 31,
    "quarterly": 92, "semiannual": 183, "semi-annual": 183, "biannual": 183,
    "annual": 366, "annually": 366, "yearly": 366,
}

# Register name -> (file, required columns). Column matching is case-insensitive.
REGISTERS = {
    "obligations": ("program/obligations.md", ["ID", "Obligation", "Owner", "Deadline", "Status"]),
    "risks": ("program/risks.md", ["ID", "Risk", "Owner", "Status", "Next review"]),
    "controls": ("program/controls.md", ["ID", "Control", "Owner", "Evidence location", "Last evidence", "Frequency", "Status"]),
    "vendors": ("program/vendors.md", ["ID", "Vendor", "Tier", "Owner", "Next review", "Status"]),
    "actions": ("program/actions.md", ["ID", "Action", "Type", "Owner", "Due", "Status"]),
    "exceptions": ("program/exceptions.md", ["ID", "Exception", "Approved by", "Expires", "Status"]),
}
DATE_COLUMNS = {"deadline", "next review", "last evidence", "due", "expires", "approved on", "last assessed", "first seen"}

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
QUOTE_RE = re.compile(r"^>\s*[\"“](.+?)[\"”]\s*[-—–]\s*(\S+?\.md)\s*$")
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Issue:
    level: str  # "error" or "warning"
    path: str
    line: int
    message: str

    def render(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line else self.path
        return f"[{self.level.upper()}] {loc} - {self.message}"


@dataclass
class Table:
    header: list[str]
    rows: list[tuple[int, dict[str, str]]] = field(default_factory=list)  # (line number, row)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_markdown(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.lower().endswith(".md"):
                yield Path(dirpath) / name


def is_source(root: Path, path: Path) -> bool:
    r = rel(root, path)
    return r.startswith(SOURCES_DIR + "/") and Path(r).name.lower() != "readme.md"


def parse_frontmatter(text: str) -> dict[str, object]:
    """Minimal YAML subset: `key: value`, `key: [a, b]`, and `key:` followed by `- item` lines."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, object] = {}
    current: str | None = None
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if re.match(r"^\s+-\s+", line) and current:
            value = line.split("-", 1)[1].strip().strip("'\"")
            existing = data.get(current)
            if not isinstance(existing, list):
                existing = []
            existing.append(value)
            data[current] = existing
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        current = key
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()] if inner else []
        else:
            data[key] = value.strip("'\"")
    return {}  # unterminated frontmatter is ignored


def content_lines(text: str):
    """Yield (line_no, line) outside fenced code blocks, with inline code removed."""
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i, INLINE_CODE_RE.sub("", line)


def normalize(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def resolve_ref(root: Path, from_file: Path, target: str) -> Path | None:
    """Resolve a cited path relative to the file first, then the repo root."""
    for base in (from_file.parent, root):
        candidate = (base / target).resolve()
        if candidate.exists():
            return candidate
    return None


def parse_date(value: str) -> dt.date | None:
    value = value.strip()
    if not DATE_RE.match(value):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def is_blank(value: str) -> bool:
    v = value.strip().strip("*_").strip().lower()
    return v in BLANK_VALUES or v.startswith("filled by")


def parse_tables(text: str) -> list[Table]:
    tables: list[Table] = []
    lines = text.splitlines()
    i = 0
    in_fence = False
    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            in_fence = not in_fence
            i += 1
            continue
        if (not in_fence and line.strip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1])):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            table = Table(header=header)
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                cells += [""] * (len(header) - len(cells))
                row = {header[j]: cells[j] for j in range(len(header))}
                if not all(is_blank(c) for c in cells):
                    table.rows.append((i + 1, row))
                i += 1
            tables.append(table)
            continue
        i += 1
    return tables


def find_register(root: Path, name: str) -> tuple[Path, Table | None]:
    file, required = REGISTERS[name]
    path = root / file
    if not path.exists():
        return path, None
    wanted = {c.lower() for c in required}
    for table in parse_tables(read_text(path)):
        if wanted.issubset({h.lower() for h in table.header}):
            return path, table
    return path, None


def cell(row: dict[str, str], column: str) -> str:
    for k, v in row.items():
        if k.lower() == column.lower():
            return v.strip()
    return ""


def load_manifest(root: Path) -> dict:
    path = root / MANIFEST
    if not path.exists():
        return {"sources": {}}
    try:
        data = json.loads(read_text(path))
        data.setdefault("sources", {})
        return data
    except json.JSONDecodeError:
        return {"sources": {}, "_corrupt": True}


def save_manifest(root: Path, data: dict) -> None:
    path = root / MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Citation graph
# ---------------------------------------------------------------------------

def citations(root: Path, path: Path) -> set[str]:
    """Return repo-relative source paths a page cites (frontmatter, quotes, links)."""
    text = read_text(path)
    found: set[str] = set()
    fm = parse_frontmatter(text)
    srcs = fm.get("sources", [])
    if isinstance(srcs, str):
        srcs = [srcs] if srcs else []
    candidates = list(srcs)
    for _, line in content_lines(text):
        q = QUOTE_RE.match(line.strip())
        if q:
            candidates.append(q.group(2))
        candidates.extend(LINK_RE.findall(line))
    for c in candidates:
        c = c.split("#", 1)[0]
        if not c or c.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = resolve_ref(root, path, c)
        if resolved and is_source(root, resolved):
            found.add(rel(root, resolved))
    return found


def citing_pages(root: Path, source_rel: str) -> list[str]:
    pages = []
    for md in iter_markdown(root):
        if is_source(root, md):
            continue
        if source_rel in citations(root, md):
            pages.append(rel(root, md))
    return sorted(pages)


# ---------------------------------------------------------------------------
# Lint
# ---------------------------------------------------------------------------

def lint_file(root: Path, path: Path) -> list[Issue]:
    issues: list[Issue] = []
    r = rel(root, path)
    text = read_text(path)

    # Frontmatter sources must exist.
    fm = parse_frontmatter(text)
    srcs = fm.get("sources", [])
    if isinstance(srcs, str):
        srcs = [srcs] if srcs else []
    for s in srcs:
        if s and not s.startswith(("http://", "https://")) and resolve_ref(root, path, s) is None:
            issues.append(Issue("error", r, 1, f"frontmatter source not found: {s}"))

    # Source documents need provenance.
    if is_source(root, path):
        missing = [f for f in SOURCE_PROVENANCE_FIELDS if is_blank(str(fm.get(f, "")))]
        if missing:
            issues.append(Issue("warning", r, 1, "source provenance missing: " + ", ".join(missing)))

    for line_no, line in content_lines(text):
        # Relative links must resolve.
        for target in LINK_RE.findall(line):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if any(ch in target for ch in "<>{}*"):
                continue  # placeholder or example
            clean = target.split("#", 1)[0]
            if clean and not (path.parent / clean).exists():
                issues.append(Issue("error", r, line_no, f"broken link: {target}"))

        # Formatted quotations must appear verbatim in the cited source.
        q = QUOTE_RE.match(line.strip())
        if q:
            quote, cited = q.group(1), q.group(2)
            if "<" in cited or "{" in cited:
                continue
            src = resolve_ref(root, path, cited)
            if src is None:
                issues.append(Issue("error", r, line_no, f"quoted source not found: {cited}"))
            elif normalize(quote) not in normalize(read_text(src)):
                issues.append(Issue("error", r, line_no, f"quotation not found in {cited}: \"{quote[:60]}\""))

    return issues


def lint_registers(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    for name, (file, required) in REGISTERS.items():
        path, table = find_register(root, name)
        r = file
        if not path.exists():
            issues.append(Issue("warning", r, 0, f"{name} register file missing"))
            continue
        if table is None:
            issues.append(Issue("error", r, 0, f"{name} register table missing required columns: {', '.join(required)}"))
            continue
        seen: dict[str, int] = {}
        for line_no, row in table.rows:
            rid = cell(row, "ID")
            if rid and not is_blank(rid):
                if rid in seen:
                    issues.append(Issue("error", r, line_no, f"duplicate ID {rid} (first on line {seen[rid]})"))
                else:
                    seen[rid] = line_no
            for col, value in row.items():
                if col.lower() in DATE_COLUMNS and not is_blank(value) and parse_date(value) is None:
                    issues.append(Issue("error", r, line_no, f"'{col}' must be YYYY-MM-DD (or blank/TBD): {value}"))
    return issues


def run_lint(root: Path, only: list[Path] | None = None) -> list[Issue]:
    files = only if only is not None else list(iter_markdown(root))
    issues: list[Issue] = []
    for f in files:
        issues.extend(lint_file(root, f))
    if only is None:
        issues.extend(lint_registers(root))
        manifest = load_manifest(root)
        if manifest.get("_corrupt"):
            issues.append(Issue("error", MANIFEST.as_posix(), 0, "manifest is not valid JSON"))
    return issues


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def source_states(root: Path) -> dict[str, list[str]]:
    manifest = load_manifest(root)["sources"]
    states: dict[str, list[str]] = {"new": [], "changed": [], "accepted": [], "missing": []}
    present = set()
    src_dir = root / SOURCES_DIR
    if src_dir.exists():
        for md in iter_markdown(src_dir):
            if not is_source(root, md):
                continue
            r = rel(root, md)
            present.add(r)
            entry = manifest.get(r)
            if entry is None:
                states["new"].append(r)
            elif entry.get("sha256") != sha256(md):
                states["changed"].append(r)
            else:
                states["accepted"].append(r)
    states["missing"] = sorted(set(manifest) - present)
    return states


def status_report(root: Path) -> str:
    out = ["## Status", ""]
    states = source_states(root)
    out.append(f"- Sources accepted: {len(states['accepted'])}")
    out.append(f"- Sources new (not yet reviewed/accepted): {len(states['new'])}")
    for s in states["new"]:
        out.append(f"  - {s}")
    out.append(f"- Sources changed since acceptance: {len(states['changed'])}")
    for s in states["changed"]:
        pages = citing_pages(root, s)
        out.append(f"  - {s} -> review: {', '.join(pages) if pages else '(no citing pages)'}")
    if states["missing"]:
        out.append(f"- Accepted sources no longer present: {', '.join(states['missing'])}")

    placeholders = []
    for md in iter_markdown(root):
        if rel(root, md).startswith(".claude/"):
            continue
        n = len(PLACEHOLDER_RE.findall(read_text(md)))
        if n:
            placeholders.append((rel(root, md), n))
    total = sum(n for _, n in placeholders)
    out.append(f"- Unfilled {{{{placeholders}}}}: {total}" + (" (run /start)" if total else ""))
    for p, n in placeholders[:12]:
        out.append(f"  - {p}: {n}")

    out.append("- Register rows:")
    for name in REGISTERS:
        _, table = find_register(root, name)
        out.append(f"  - {name}: {len(table.rows) if table else 'table missing'}")

    audits = sorted((root / "audits").glob("audit-*.md")) if (root / "audits").exists() else []
    out.append(f"- Latest /audit report: {rel(root, audits[-1]) if audits else 'none yet'}")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Pulse (program health)
# ---------------------------------------------------------------------------

def pulse_report(root: Path, today: dt.date) -> tuple[str, int]:
    findings: list[tuple[str, str, str]] = []  # (severity, register, message)

    def add(sev: str, reg: str, msg: str):
        findings.append((sev, reg, msg))

    def label(row):
        return f"{cell(row, 'ID')} {cell(row, list(row)[1]) if len(row) > 1 else ''}".strip()

    # Actions
    _, t = find_register(root, "actions")
    if t:
        for _, row in t.rows:
            st = cell(row, "Status").lower()
            if st in DONE_STATUSES:
                continue
            due = parse_date(cell(row, "Due"))
            if is_blank(cell(row, "Owner")):
                add("high", "actions", f"{label(row)}: no owner")
            if due and due < today:
                add("high", "actions", f"{label(row)}: overdue since {due} ({(today - due).days} days)")
            elif due and (due - today).days <= 14:
                add("info", "actions", f"{label(row)}: due {due}")
            elif due is None:
                add("medium", "actions", f"{label(row)}: no due date")

    # Risks
    _, t = find_register(root, "risks")
    if t:
        for _, row in t.rows:
            if cell(row, "Status").lower() in DONE_STATUSES:
                continue
            if is_blank(cell(row, "Owner")):
                add("high", "risks", f"{label(row)}: no risk owner")
            nr = parse_date(cell(row, "Next review"))
            if nr and nr < today:
                add("medium", "risks", f"{label(row)}: review overdue since {nr}")
            elif nr is None:
                add("medium", "risks", f"{label(row)}: no next review date")

    # Exceptions / accepted risks
    _, t = find_register(root, "exceptions")
    if t:
        for _, row in t.rows:
            if cell(row, "Status").lower() in INACTIVE_EXCEPTION_STATUSES:
                continue
            exp = parse_date(cell(row, "Expires"))
            if is_blank(cell(row, "Approved by")):
                add("high", "exceptions", f"{label(row)}: no recorded approver")
            if exp is None:
                add("high", "exceptions", f"{label(row)}: no expiry date (exceptions must expire)")
            elif exp < today:
                add("high", "exceptions", f"{label(row)}: expired {exp} but still active")
            elif (exp - today).days <= 30:
                add("medium", "exceptions", f"{label(row)}: expires {exp}")

    # Controls / evidence freshness
    _, t = find_register(root, "controls")
    if t:
        for _, row in t.rows:
            if cell(row, "Status").lower() in {"retired", "not applicable", "n/a"}:
                continue
            if is_blank(cell(row, "Owner")):
                add("medium", "controls", f"{label(row)}: no control owner")
            if is_blank(cell(row, "Evidence location")):
                add("medium", "controls", f"{label(row)}: evidence location not recorded (gap in evidence, not proof of control failure)")
                continue
            last = parse_date(cell(row, "Last evidence"))
            days = FREQUENCY_DAYS.get(cell(row, "Frequency").lower())
            if last is None:
                add("medium", "controls", f"{label(row)}: no dated evidence on record")
            elif days and (today - last).days > days:
                add("medium", "controls", f"{label(row)}: evidence stale (last {last}, expected {cell(row, 'Frequency').lower()})")

    # Vendors
    _, t = find_register(root, "vendors")
    if t:
        for _, row in t.rows:
            if cell(row, "Status").lower() in DONE_STATUSES | {"offboarded"}:
                continue
            nr = parse_date(cell(row, "Next review"))
            if nr and nr < today:
                add("medium", "vendors", f"{label(row)}: review overdue since {nr}")
            elif nr is None and cell(row, "Tier").lower() in {"1", "tier 1", "critical", "high"}:
                add("medium", "vendors", f"{label(row)}: critical vendor with no next review date")

    # Obligations
    _, t = find_register(root, "obligations")
    if t:
        for _, row in t.rows:
            if cell(row, "Status").lower() in DONE_STATUSES:
                continue
            dl = parse_date(cell(row, "Deadline"))
            if is_blank(cell(row, "Owner")):
                add("medium", "obligations", f"{label(row)}: no owner")
            if dl and dl < today:
                add("high", "obligations", f"{label(row)}: deadline {dl} passed, status '{cell(row, 'Status')}'")
            elif dl and (dl - today).days <= 60:
                add("info", "obligations", f"{label(row)}: deadline {dl} ({(dl - today).days} days)")

    order = {"high": 0, "medium": 1, "info": 2}
    findings.sort(key=lambda f: (order[f[0]], f[1], f[2]))
    out = [f"## Program pulse (as of {today})", "",
           "Deterministic date and ownership checks on the program registers. Not scored. "
           "A missing date or evidence pointer is a record-keeping gap, not proof that a control failed.", ""]
    if not findings:
        out.append("No overdue, expired, unowned, or stale items found in the registers.")
    else:
        counts = {s: sum(1 for f in findings if f[0] == s) for s in order}
        out.append(f"High: {counts['high']} | Medium: {counts['medium']} | Info: {counts['info']}")
        out.append("")
        out.append("| Severity | Register | Finding |")
        out.append("|---|---|---|")
        for sev, reg, msg in findings:
            out.append(f"| {sev} | {reg} | {msg.replace('|', '/')} |")
    return "\n".join(out), sum(1 for f in findings if f[0] == "high")


# ---------------------------------------------------------------------------
# Accept
# ---------------------------------------------------------------------------

def accept(root: Path, source: str, reviewed: list[str], today: dt.date) -> tuple[bool, list[str]]:
    msgs: list[str] = []
    path = (root / source).resolve()
    if not path.exists():
        return False, [f"source not found: {source}"]
    r = rel(root, path)
    if not is_source(root, path):
        return False, [f"only files under {SOURCES_DIR}/ can be accepted: {r}"]

    manifest = load_manifest(root)
    if manifest.get("_corrupt"):
        return False, [f"{MANIFEST.as_posix()} is not valid JSON; fix or restore it from Git first"]
    entry = manifest["sources"].get(r)
    digest = sha256(path)
    pages = citing_pages(root, r)
    reviewed_norm = {Path(p).as_posix().lstrip("./") for p in reviewed}

    if entry and entry.get("sha256") == digest:
        return True, [f"{r} already accepted and unchanged."]

    if entry:  # previously accepted, content changed
        missing = [p for p in pages if p not in reviewed_norm]
        if missing:
            return False, [f"{r} changed since it was accepted on {entry.get('accepted')}.",
                           "Review every page that cites it, then re-run with --reviewed for each:",
                           *[f"  --reviewed {p}" for p in missing]]

    unknown = [p for p in reviewed_norm if not (root / p).exists()]
    if unknown:
        return False, [f"--reviewed page not found: {p}" for p in unknown]

    check = [root / p for p in sorted(set(pages) | reviewed_norm)] + [path]
    errors = [i for i in run_lint(root, check) if i.level == "error"]
    if errors:
        return False, ["Acceptance refused: fix these errors first.", *[e.render() for e in errors]]

    manifest["sources"][r] = {"sha256": digest, "accepted": today.isoformat(),
                              "reviewed": sorted(reviewed_norm) or pages}
    save_manifest(root, manifest)
    msgs.append(f"Accepted {r} ({digest[:12]}). Citing pages: {', '.join(pages) if pages else 'none yet'}.")
    msgs.append("Commit the reviewed batch with Git when you are satisfied.")
    return True, msgs


# ---------------------------------------------------------------------------
# Review (scheduled-friendly)
# ---------------------------------------------------------------------------

def write_exclusive(directory: Path, prefix: str, content: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    for _ in range(10):
        path = directory / f"{prefix}-{stamp}-{secrets.token_hex(2)}.md"
        try:
            with open(path, "x", encoding="utf-8") as fh:
                fh.write(content)
            return path
        except FileExistsError:
            continue
    raise RuntimeError("could not create a unique report file")


def review(root: Path, today: dt.date, save: bool = True) -> tuple[int, str, Path | None]:
    issues = run_lint(root)
    errors = [i for i in issues if i.level == "error"]
    warnings = [i for i in issues if i.level == "warning"]
    pulse, highs = pulse_report(root, today)
    lint_section = ["## Lint", "", f"Errors: {len(errors)} | Warnings: {len(warnings)}", ""]
    lint_section += [f"- {i.render()}" for i in errors + warnings] or ["- No problems found."]
    body = "\n".join([
        "---", "report_kind: grc-os-review", f"generated_at: \"{dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}\"",
        f"as_of: {today}", f"lint_errors: {len(errors)}", f"pulse_high: {highs}", "---", "",
        f"# GRC OS review: {today}", "",
        "Mechanical review only. No AI was used. Run /audit for the evidence-based reliability score.", "",
        status_report(root), "", "\n".join(lint_section), "", pulse, "",
    ])
    path = write_exclusive(root / "audits", "review", body) if save else None
    return (1 if errors else 0), body, path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "CLAUDE.md").exists() and (p / "program").is_dir():
            return p
    return Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    parser = argparse.ArgumentParser(prog="grc_os", description="GRC AI OS deterministic checks")
    parser.add_argument("--root", type=Path, help="workspace root (default: auto-detect)")
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    lp = sub.add_parser("lint")
    lp.add_argument("paths", nargs="*", help="limit to these files")
    lp.add_argument("--strict", action="store_true", help="treat warnings as errors")
    sub.add_parser("pulse")
    ap = sub.add_parser("accept")
    ap.add_argument("source")
    ap.add_argument("--reviewed", action="append", default=[], help="page you reviewed against the changed source")
    rp = sub.add_parser("review")
    rp.add_argument("--no-save", action="store_true")
    args = parser.parse_args(argv)

    root = (args.root or find_root(Path.cwd())).resolve()
    today = parse_date(args.today) if args.today else dt.date.today()
    if today is None:
        print("--today must be YYYY-MM-DD", file=sys.stderr)
        return 2

    if args.cmd == "status":
        print(status_report(root))
        return 0
    if args.cmd == "lint":
        only = [(Path.cwd() / p).resolve() for p in args.paths] if args.paths else None
        issues = run_lint(root, only)
        for i in issues:
            print(i.render())
        errors = [i for i in issues if i.level == "error" or args.strict]
        print(f"\n{len([i for i in issues if i.level == 'error'])} error(s), "
              f"{len([i for i in issues if i.level == 'warning'])} warning(s).")
        return 1 if errors else 0
    if args.cmd == "pulse":
        print(pulse_report(root, today)[0])
        return 0
    if args.cmd == "accept":
        ok, msgs = accept(root, args.source, args.reviewed, today)
        print("\n".join(msgs))
        return 0 if ok else 1
    if args.cmd == "review":
        code, body, path = review(root, today, save=not args.no_save)
        print(body if path is None else f"Review saved: {rel(root, path)}\n\n{body}")
        return code
    return 2


if __name__ == "__main__":
    sys.exit(main())
