"""Shared helpers for the cairn deterministic tracking scripts.

Python 3 stdlib only, plus the hooks' ``cairn_common`` (the single home of
the ROADMAP row-splitter and the cairn-root finder — reused here, never
copy-pasted). These scripts are read-only reporters over a repo's ``cairn/``
files: instant, token-free, drift-proof status the skills would otherwise
re-derive by LLM each session.

Invocation: ``python3 scripts/<name>.py [ROOT]`` — ROOT defaults to the
current working directory, then walks up to the enclosing cairn repo. Run
outside a cairn repo, every script prints a clear message and exits 2.
"""

import os
import re
import sys

# Make the hooks' shared module importable without duplicating it.
_HOOKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks")
if _HOOKS not in sys.path:
    sys.path.insert(0, _HOOKS)

import cairn_common as cc  # noqa: E402  (after sys.path shim)

# The seven-status vocabulary (tracking-rules) and the two derived subsets.
STATUSES = {
    "candidate",
    "planned",
    "in-progress",
    "blocked",
    "review",
    "done",
    "dropped",
}
ACTIVE = {"in-progress", "blocked", "review"}
PRIORITY_ORDER = {"high": 0, "normal": 1, "low": 2}

# Weight caps (tracking-rules): file -> max line count. A live milestone
# file is < 150; an archived summary is <= 25 (handled separately by path).
LINE_CAPS = {"CLAUDE.md": 80, "cairn/ROADMAP.md": 60}
MILESTONE_CAP = 150
ARCHIVE_CAP = 25
DONE_ROW_RETENTION = 5


class NotCairn(Exception):
    """Raised when ROOT is not inside a cairn-tracked repo."""


def resolve_root(argv):
    """Return the cairn repo root from argv[1] or cwd, or raise NotCairn."""
    start = argv[1] if len(argv) > 1 else os.getcwd()
    root = cc.find_cairn_root(start)
    if not root:
        raise NotCairn(start)
    return root


def read_roadmap(root):
    """Return ROADMAP.md text (empty string if unreadable)."""
    try:
        with open(os.path.join(root, "cairn", "ROADMAP.md"), encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def rows(roadmap_text):
    """List of row dicts: id, title, status, depends (list), priority, relpath."""
    out = []
    for mid, title, status, depends, priority, relpath in cc.parse_roadmap_rows_full(
        roadmap_text
    ):
        out.append(
            {
                "id": mid,
                "title": title,
                "status": status,
                "depends": parse_depends(depends),
                "priority": priority.lower(),
                "relpath": relpath,
            }
        )
    return out


def parse_depends(cell):
    """Parse a 'Depends on' cell into a list of milestone IDs (— -> [])."""
    ids = []
    for tok in re.split(r"[,\s]+", cell.strip()):
        tok = tok.strip()
        if tok and tok.startswith("M") and tok[1:].isdigit():
            ids.append(tok)
    return ids


def candidate_count(roadmap_text):
    """Count '- ' bullets under the '## Candidates' section."""
    count = 0
    in_section = False
    for line in roadmap_text.splitlines():
        if line.startswith("## "):
            in_section = line.strip().lower() == "## candidates"
            continue
        if in_section and line.lstrip().startswith("- "):
            count += 1
    return count


def last_hygiene_check(roadmap_text):
    """Extract the YYYY-MM-DD from the '_Last hygiene check:' line, or None."""
    m = re.search(r"Last hygiene check:\s*(\d{4}-\d{2}-\d{2})", roadmap_text)
    return m.group(1) if m else None


def milestone_status(root, relpath):
    """First token after '**Status:**' in a milestone file, lowercased, or None.

    Handles both the live mirror line ('- **Status:** in-progress   <!--...')
    and the archived summary line ('**Status:** done · approved ...').
    """
    try:
        with open(os.path.join(root, "cairn", relpath), encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return None
    m = re.search(r"\*\*Status:\*\*\s*([A-Za-z-]+)", text)
    return m.group(1).lower() if m else None


def line_count(path):
    """Line count of a file, or None if unreadable."""
    try:
        with open(path, encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception:
        return None


def sort_by_priority(row_list):
    """Rows sorted high>normal>low, then by ID."""
    return sorted(
        row_list, key=lambda r: (PRIORITY_ORDER.get(r["priority"], 1), r["id"])
    )


def die_not_cairn(start):
    sys.stderr.write(
        f"not a cairn repo: no cairn/ROADMAP.md at or above {start}\n"
    )
