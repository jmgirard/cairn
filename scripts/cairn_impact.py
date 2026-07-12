#!/usr/bin/env python3
"""cairn impact — a Sync Impact Report for DESIGN.md principle changes.

When a DESIGN.md principle (IPn/GPn) is added, changed, or retired, list every
tracked cairn/ file:line that cites it, so the edit can reconcile its
downstream references in the same change. Read-only; reuses the cairn_scripts
root resolver. Exits 0 on success, 2 outside a cairn repo (or on a usage
error), matching the other reporters.

    python3 scripts/cairn_impact.py IP2 GP4     # named principles
    python3 scripts/cairn_impact.py --changed   # derive from DESIGN.md diff

A match is any whole-word occurrence of the id (`IP2` matches `IP2:` and
`IP2)` but not `IP20`). The principle's own DESIGN.md definition line counts
as a reference — showing it alongside the citations is exactly what reconciling
a change wants; a principle that appears nowhere reports "no references".
"""

import os
import re
import subprocess
import sys

import cairn_scripts as cs

_PRINCIPLE = re.compile(r"\b[IG]P\d+\b")


def scan_files(root):
    """Tracked files where a principle may be cited: DESIGN/DECISIONS/ROADMAP
    plus every milestone file (live + archive). Excludes references/, legacy/,
    reviews/ — mirroring cairn_validate's date scan."""
    cairn = os.path.join(root, "cairn")
    files = []
    for name in ("DESIGN.md", "DECISIONS.md", "ROADMAP.md"):
        p = os.path.join(cairn, name)
        if os.path.isfile(p):
            files.append(p)
    for dirpath, _dirs, names in os.walk(os.path.join(cairn, "milestones")):
        files.extend(
            os.path.join(dirpath, n) for n in sorted(names) if n.endswith(".md")
        )
    return files


def references(root, pid):
    """Sorted 'cairn/rel:line' strings for every line citing principle pid."""
    pat = re.compile(r"\b" + re.escape(pid) + r"\b")
    hits = []
    for path in scan_files(root):
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except Exception:
            continue
        rel = os.path.relpath(path, root)
        for i, line in enumerate(lines, 1):
            if pat.search(line):
                hits.append(f"{rel}:{i}")
    return hits


def changed_principles(root):
    """Principle ids on added/removed lines of DESIGN.md vs HEAD, in order."""
    try:
        diff = subprocess.run(
            ["git", "-C", root, "diff", "HEAD", "--", "cairn/DESIGN.md"],
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout
    except Exception:
        return []
    ids = []
    for line in diff.splitlines():
        if line[:1] in ("+", "-") and line[:3] not in ("+++", "---"):
            for m in _PRINCIPLE.finditer(line):
                if m.group(0) not in ids:
                    ids.append(m.group(0))
    return ids


def report(root, principles):
    out = [f"cairn impact — {root}", ""]
    for pid in principles:
        refs = references(root, pid)
        if refs:
            out.append(f"{pid} — {len(refs)} reference(s)")
            out.extend(f"  {r}" for r in refs)
        else:
            out.append(f"{pid} — no references")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def parse_args(argv):
    principles, changed, root = [], False, None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--changed":
            changed = True
        elif a == "--root":
            i += 1
            root = argv[i] if i < len(argv) else None
        else:
            principles.append(a.upper())
        i += 1
    return principles, changed, root


def main(argv):
    principles, changed, root_arg = parse_args(argv)
    try:
        root = cs.resolve_root(["cairn_impact"] + ([root_arg] if root_arg else []))
    except cs.NotCairn as e:
        cs.die_not_cairn(str(e))
        return 2
    if changed:
        for pid in changed_principles(root):
            if pid not in principles:
                principles.append(pid)
        if not principles:
            print(f"cairn impact — {root}\n\nno changed principles in cairn/DESIGN.md (vs HEAD)")
            return 0
    if not principles:
        sys.stderr.write("usage: cairn_impact.py [--changed] [IPn|GPn ...]\n")
        return 2
    print(report(root, principles), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
