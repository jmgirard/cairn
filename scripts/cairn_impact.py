#!/usr/bin/env python3
"""cairn impact — a Sync Impact Report for DESIGN.md principle changes.

When a DESIGN.md principle (IPn/GPn) is added, changed, or retired, list every
tracked cairn/ file:line that cites it, so the edit can reconcile its
downstream references in the same change. Read-only; reuses the cairn_scripts
root resolver. Exits 0 on success, 2 outside a cairn repo (or on a usage
error), matching the other reporters.

    python3 scripts/cairn_impact.py IP2 GP4     # named principles
    python3 scripts/cairn_impact.py --changed   # derive from DESIGN.md diff

`--changed` diffs DESIGN.md from the branch's merge-base with the default
branch (origin/HEAD, then main, then master; HEAD if none resolves), so it
sees principle edits already committed on the milestone branch — which is the
state at the review gate, where implement has checkpoint-committed each task.

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


class Usage(Exception):
    """Bad command-line arguments (exit 2, like the not-a-cairn-repo case)."""


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
    """'cairn/rel:line' strings for every line citing pid, in scan order
    (DESIGN, DECISIONS, ROADMAP, then milestones; deterministic)."""
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


def _base_commit(root):
    """Merge-base of HEAD with the default branch (origin/HEAD, then main,
    then master); HEAD if none resolves — e.g. on the default branch itself
    or a fresh repo — so --changed still sees the working tree."""
    for ref in ("origin/HEAD", "main", "master"):
        r = subprocess.run(
            ["git", "-C", root, "merge-base", "HEAD", ref],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    return "HEAD"


def changed_principles(root):
    """Principle ids on added/removed DESIGN.md lines since the branch base."""
    try:
        base = _base_commit(root)
        r = subprocess.run(
            ["git", "-C", root, "diff", base, "--", "cairn/DESIGN.md"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            sys.stderr.write("warning: git diff failed; --changed saw nothing\n")
            return []
        diff = r.stdout
    except Exception:
        sys.stderr.write("warning: git unavailable; --changed saw nothing\n")
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
            if i + 1 >= len(argv):
                raise Usage("--root requires a value")
            i += 1
            root = argv[i]
        elif a.startswith("-"):
            raise Usage(f"unknown option {a}")
        else:
            principles.append(a.upper())
        i += 1
    return principles, changed, root


def main(argv):
    try:
        principles, changed, root_arg = parse_args(argv)
    except Usage as e:
        sys.stderr.write(f"usage: cairn_impact.py [--changed] [IPn|GPn ...]\n{e}\n")
        return 2
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
            print(f"cairn impact — {root}\n\nno changed principles in cairn/DESIGN.md")
            return 0
    if not principles:
        sys.stderr.write("usage: cairn_impact.py [--changed] [IPn|GPn ...]\n")
        return 2
    print(report(root, principles), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
