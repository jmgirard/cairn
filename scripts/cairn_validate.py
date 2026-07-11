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

import glob
import os
import re
import sys

import cairn_scripts as cs

_ID_RE = re.compile(r"(M\d+)")


def _archive_ids(root):
    ids = {}
    for path in glob.glob(os.path.join(root, "cairn", "milestones", "archive", "M*.md")):
        m = _ID_RE.match(os.path.basename(path))
        if m:
            ids[m.group(1)] = path
    return ids


def _live_files(root):
    """Live milestone files: cairn/milestones/M*.md, excluding archive/."""
    ids = {}
    for path in glob.glob(os.path.join(root, "cairn", "milestones", "M*.md")):
        m = _ID_RE.match(os.path.basename(path))
        if m:
            ids[m.group(1)] = path
    return ids


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
    known |= set(_archive_ids(root))
    known |= set(_live_files(root))
    bad = []
    for r in rows:
        for dep in r["depends"]:
            if dep not in known:
                bad.append(f"{r['id']} depends on {dep}, which does not exist")
    return bad


def check_orphans(root, rows):
    bad = []
    row_targets = {os.path.normpath(r["relpath"]) for r in rows}
    row_ids = {r["id"] for r in rows}
    # Every live milestone file has a row pointing at it.
    for mid, path in _live_files(root).items():
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
    live, arch = _live_files(root), _archive_ids(root)
    for mid in set(live) & set(arch):
        bad.append(f"{mid} exists as both a live and an archived file")
    return bad


CHECKS = [
    ("mirror agreement", lambda root, rows: check_mirror(root, rows)),
    ("at most one in-progress", lambda root, rows: check_single_in_progress(rows)),
    ("weight caps", lambda root, rows: check_caps(root, rows)),
    ("done-row retention", lambda root, rows: check_done_retention(rows)),
    ("status vocabulary", lambda root, rows: check_vocab(rows)),
    ("dependency existence", lambda root, rows: check_dependencies(root, rows)),
    ("roadmap<->disk orphans", lambda root, rows: check_orphans(root, rows)),
    ("id uniqueness", lambda root, rows: check_id_uniqueness(root, rows)),
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
