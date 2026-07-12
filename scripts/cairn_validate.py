#!/usr/bin/env python3
"""cairn validate — mechanized consistency gate over the cairn/ files.

Runs only the deterministic checks — the ones the /milestone health audit
would otherwise re-derive by LLM. Semantic checks (git reconciliation,
CLAUDE.md-section intact, staleness/triage-by-date judgment) stay LLM-owned
and are NOT attempted here.

Prints one PASS/FAIL line per check with an accurate finding count, then a
summary. Exits 0 when every check passes, 1 when any fails, 2 outside a
cairn repo.

    python3 scripts/cairn_validate.py [ROOT]
"""

import os
import re
import sys

import cairn_scripts as cs

# Non-ISO calendar-date patterns. Conservative by design (M13 Decisions):
# strong date signals only, so version numbers (4.8), page anchors (p. 12),
# IDs (M13, D-005), and fractions (1/2) don't trip. A missed weird format is
# preferred over a false positive that makes the gate cry wolf.
# The slash branch requires a 4-digit year on one end (year-first or
# year-last) so R CMD check count-notation (three slash-separated counts like
# 0/0/0, errors/warnings/notes) doesn't trip (D-023). The accepted cost: a
# 2-digit-year slash date (07/11/26) goes uncaught — structurally
# indistinguishable from a count-triple, and none exist in this repo's ISO format.
_MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
_NON_ISO_DATE = re.compile(
    r"\b(?:"
    r"\d{4}/\d{1,2}/\d{1,2}"                                         # 2026/07/11 (year-first)
    r"|\d{1,2}/\d{1,2}/\d{4}"                                        # 07/11/2026 (year-last)
    r"|\d{1,2}-\d{1,2}-\d{4}"                                        # 11-07-2026 (year-last dashed)
    r"|(?:" + _MONTHS + r")[a-z]*\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}"  # Jul 11, 2026
    r"|\d{1,2}(?:st|nd|rd|th)?\s+(?:" + _MONTHS + r")[a-z]*\.?\s+\d{4}"    # 11 July 2026
    r")\b",
    re.IGNORECASE,
)
# Year-first dashed tokens that look like ISO but aren't (missing zero-pad,
# e.g. 2026-7-11) — the most likely typo in this repo's own date format.
# Matched then compared against the canonical form so valid ISO never trips.
_ISO_LIKE = re.compile(r"\b\d{4}-\d{1,2}-\d{1,2}\b")
_CANON_ISO = re.compile(r"\d{4}-\d{2}-\d{2}")


def check_mirror(root, rows):
    """Each ROADMAP row's file header Status matches the ROADMAP status."""
    bad = []
    for r in rows:
        got = cs.milestone_status(root, r["relpath"])
        if got is None:
            continue  # missing file is the orphan check's job, not this one
        if got != r["status"]:
            bad.append(f"{r['id']}: ROADMAP={r['status']} file={got}")
    return bad


def check_single_in_progress(rows):
    ip = [r["id"] for r in rows if r["status"] == "in-progress"]
    return [f"multiple in-progress: {', '.join(ip)}"] if len(ip) > 1 else []


def check_caps(root, rows):
    bad = []
    for rel, cap in cs.LINE_CAPS.items():
        n = cs.line_count(os.path.join(root, rel))
        if n is not None and n >= cap:
            bad.append(f"{rel}: {n} lines (cap <{cap})")
    # CLAUDE.md: cap only the appended cairn section, not the whole file (D-018).
    sec = cs.claude_section_line_count(os.path.join(root, "CLAUDE.md"))
    if sec is not None and sec >= cs.CLAUDE_SECTION_CAP:
        bad.append(
            f"CLAUDE.md cairn section: {sec} lines (cap <{cs.CLAUDE_SECTION_CAP})"
        )
    for r in rows:
        n = cs.line_count(os.path.join(root, "cairn", r["relpath"]))
        if n is None:
            continue
        if "archive/" in r["relpath"]:
            if n > cs.ARCHIVE_CAP:
                bad.append(f"cairn/{r['relpath']}: {n} lines (archive cap {cs.ARCHIVE_CAP})")
        elif n >= cs.MILESTONE_CAP:
            bad.append(f"cairn/{r['relpath']}: {n} lines (cap <{cs.MILESTONE_CAP})")
    return bad


def check_done_retention(rows):
    done = [r["id"] for r in rows if r["status"] == "done"]
    if len(done) > cs.DONE_ROW_RETENTION:
        return [f"{len(done)} done rows (retention {cs.DONE_ROW_RETENTION}): {', '.join(done)}"]
    return []


def check_vocab(rows):
    return [
        f"{r['id']}: unknown status '{r['status']}'"
        for r in rows
        if r["status"] not in cs.STATUSES
    ]


def check_dependencies(root, rows):
    known = {r["id"] for r in rows}
    known |= set(cs.archive_files(root))
    known |= set(cs.live_files(root))
    dropped = {r["id"] for r in rows if r["status"] == "dropped"}
    bad = []
    for r in rows:
        for dep in r["depends"]:
            if dep not in known:
                bad.append(f"{r['id']} depends on {dep}, which does not exist")
            elif dep in dropped:
                bad.append(f"{r['id']} depends on {dep}, which is dropped (re-wire)")
    return bad


def check_orphans(root, rows):
    bad = []
    row_targets = {os.path.normpath(r["relpath"]) for r in rows}
    row_ids = {r["id"] for r in rows}
    # Every live milestone file has a row pointing at it.
    for mid, path in cs.live_files(root).items():
        rel = os.path.normpath(os.path.relpath(path, os.path.join(root, "cairn")))
        if rel not in row_targets:
            bad.append(f"live file cairn/{rel} has no ROADMAP row")
    # Every row's target file exists on disk.
    for r in rows:
        if not os.path.isfile(os.path.join(root, "cairn", r["relpath"])):
            bad.append(f"{r['id']} row points to missing file cairn/{r['relpath']}")
    return bad


def check_id_uniqueness(root, rows):
    bad = []
    seen = {}
    for r in rows:
        seen.setdefault(r["id"], 0)
        seen[r["id"]] += 1
    for mid, n in seen.items():
        if n > 1:
            bad.append(f"{mid} appears in {n} ROADMAP rows")
    # A milestone cannot be both live and archived.
    live, arch = cs.live_files(root), cs.archive_files(root)
    for mid in set(live) & set(arch):
        bad.append(f"{mid} exists as both a live and an archived file")
    return bad


def _date_scan_files(root):
    """Tracked status/decision files whose dates must be ISO (tracking-rules
    absolute-dates rule): the top-level tracking files plus every milestone
    file. Excludes references/ (external citation dates in many formats) and
    legacy/ (entombed verbatim, D-005 — must not be reformatted)."""
    cairn = os.path.join(root, "cairn")
    files = []
    for name in ("ROADMAP.md", "DECISIONS.md", "DESIGN.md", "LESSONS.md"):
        p = os.path.join(cairn, name)
        if os.path.isfile(p):
            files.append(p)
    for dirpath, _dirs, names in os.walk(os.path.join(cairn, "milestones")):
        files.extend(os.path.join(dirpath, n) for n in names if n.endswith(".md"))
    return files


def check_dates(root):
    """Flag non-ISO calendar dates in the tracked status/decision files.
    Catches misformatted dates only; prose relative dates ('yesterday') stay
    LLM-owned in the semantic audit."""
    bad = []
    for path in _date_scan_files(root):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        rel = os.path.relpath(path, root)
        for i, line in enumerate(text.splitlines(), 1):
            m = _NON_ISO_DATE.search(line)
            if m:
                bad.append(f"{rel}:{i}: non-ISO date '{m.group(0)}'")
            for m in _ISO_LIKE.finditer(line):
                if not _CANON_ISO.fullmatch(m.group(0)):
                    bad.append(f"{rel}:{i}: non-ISO date '{m.group(0)}'")
    return bad


def _ignore_entries(path):
    """Non-empty, non-comment lines of an ignore file as a set; empty set if
    the file is absent (so a missing .gitignore reads as 'no entries')."""
    if not os.path.isfile(path):
        return set()
    out = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if s and not s.startswith("#"):
                out.add(s)
    return out


def check_scaffold(root):
    """§1 scaffold presence (cairn-init §1), the deterministic arm of the
    drift audit: a repo that adopted cairn before a later scaffold addition
    is missing that piece. Findings route the user to /cairn-init repair
    (the /milestone audit owns that routing text). Only always-tracked pieces
    are checked — empty scaffold dirs are skipped (git drops empty dirs), and
    the CLAUDE.md cairn section stays LLM-owned. Required-piece lists live in
    cairn_scripts (single source of truth)."""
    bad = []
    for rel in cs.REQUIRED_SCAFFOLD_FILES:
        if not os.path.isfile(os.path.join(root, rel)):
            bad.append(f"missing scaffold file {rel}")
    gitignore = _ignore_entries(os.path.join(root, ".gitignore"))
    for entry in cs.REQUIRED_GITIGNORE:
        if entry not in gitignore:
            bad.append(f".gitignore missing entry '{entry}'")
    # `^cairn$` is a package concern — only required when a DESCRIPTION exists.
    if os.path.isfile(os.path.join(root, "DESCRIPTION")):
        rbuild = _ignore_entries(os.path.join(root, ".Rbuildignore"))
        for entry in cs.REQUIRED_RBUILDIGNORE:
            if entry not in rbuild:
                bad.append(f".Rbuildignore missing entry '{entry}'")
    return bad


CHECKS = [
    ("mirror agreement", lambda root, rows: check_mirror(root, rows)),
    ("at most one in-progress", lambda root, rows: check_single_in_progress(rows)),
    ("weight caps", lambda root, rows: check_caps(root, rows)),
    ("done-row retention", lambda root, rows: check_done_retention(rows)),
    ("status vocabulary", lambda root, rows: check_vocab(rows)),
    ("dependency resolution", lambda root, rows: check_dependencies(root, rows)),
    ("roadmap<->disk orphans", lambda root, rows: check_orphans(root, rows)),
    ("id uniqueness", lambda root, rows: check_id_uniqueness(root, rows)),
    ("iso date format", lambda root, rows: check_dates(root)),
    ("scaffold present", lambda root, rows: check_scaffold(root)),
]


def run(root):
    rows = cs.rows(cs.read_roadmap(root))
    lines = [f"cairn validate — {root}", ""]
    failures = 0
    for name, fn in CHECKS:
        findings = fn(root, rows)
        if findings:
            failures += 1
            lines.append(f"FAIL  {name} ({len(findings)})")
            for f in findings:
                lines.append(f"        {f}")
        else:
            lines.append(f"PASS  {name}")
    lines.append("")
    if failures:
        lines.append(f"{failures} check(s) failed")
    else:
        lines.append("all checks passed")
    return "\n".join(lines), failures


def main(argv):
    try:
        root = cs.resolve_root(argv)
    except cs.NotCairn as e:
        cs.die_not_cairn(str(e))
        return 2
    report, failures = run(root)
    print(report)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
