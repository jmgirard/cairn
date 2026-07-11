"""Shared helpers for cairn guardrail hooks.

Python 3 stdlib only. Every hook is a strict no-op (exit 0, no output)
outside cairn-tracked repos, and fails permissive: an unexpected error
must never block the user's session.
"""

import json
import os
import subprocess
import sys

# Statuses whose milestone files count as "active" for context injection.
ACTIVE_STATUSES = {"in-progress", "blocked", "review"}


def read_input():
    """Parse the hook's stdin JSON; permissive on garbage."""
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def find_cairn_root(cwd):
    """Walk up from cwd to the first dir containing cairn/ROADMAP.md.

    Returns the repo root path, or None (not a cairn-tracked repo).
    A missing cwd (malformed hook input) is None, never a fallback to
    the process cwd — guards must be deterministic, not guess.
    """
    if not cwd:
        return None
    try:
        path = os.path.abspath(cwd)
    except Exception:
        return None
    while True:
        if os.path.isfile(os.path.join(path, "cairn", "ROADMAP.md")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def git(args, cwd):
    """Run git; return (returncode, stdout). Never raises."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode, result.stdout
    except Exception:
        return 1, ""


def parse_roadmap_rows(roadmap_text):
    """Yield (id, status, relpath) for each milestone table row.

    Rows look like:
    | M07 | Title | in-progress | — | high | milestones/M07-....md |
    relpath is relative to the cairn/ directory.
    """
    for line in roadmap_text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")][1:-1]
        if len(cells) < 6 or not cells[0].startswith("M"):
            continue
        yield cells[0], cells[2].lower(), cells[5]


def emit(obj):
    json.dump(obj, sys.stdout)
    sys.stdout.write("\n")
