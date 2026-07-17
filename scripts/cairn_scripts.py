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

import glob
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
# CLAUDE.md is NOT whole-file capped (D-018): a mature repo's own dev doctrine
# is not cairn's to police. Only the appended cairn section is capped, via
# CLAUDE_SECTION_CAP + claude_section_line_count (handled separately).
LINE_CAPS = {"cairn/ROADMAP.md": 60, "cairn/LESSONS.md": 50, "cairn/PROFILE.md": 120}
MILESTONE_CAP = 150
ARCHIVE_CAP = 25
TERMINAL_ROW_RETENTION = 5  # done + dropped rows share one ROADMAP cap

# Cap on the cairn-owned `## Project tracking (cairn)` block appended to a
# repo's CLAUDE.md (D-018). Template target is ~25 lines; 30 gives headroom.
CLAUDE_SECTION_CAP = 30
CLAUDE_SECTION_HEADING = "## Project tracking"

# §1 scaffold pieces that must exist once a repo is on cairn (cairn-init §1).
# Single source of truth for the machine-side drift check
# (cairn_validate.check_scaffold): a missing piece means the repo predates a
# later scaffold addition — route the user to /cairn-init repair. Only
# always-tracked pieces are listed: git does not preserve empty dirs, so the
# empty scaffold dirs (milestones/archive, reviews/archive, references/pdf)
# are deliberately NOT checked — their absence is not drift. The CLAUDE.md
# cairn section stays LLM-owned by the /milestone audit, not duplicated here.
REQUIRED_SCAFFOLD_FILES = (
    "cairn/DESIGN.md",
    # ROADMAP.md is also the cairn-repo marker: a missing one makes
    # resolve_root raise NotCairn (exit 2) before check_scaffold ever runs, so
    # this entry is belt-and-suspenders — kept so the tuple is the complete §1
    # file set (the deferred cairn-init-repair-consumes-this candidate wants
    # that), not because the CLI branch is reachable.
    "cairn/ROADMAP.md",
    "cairn/DECISIONS.md",
    "cairn/LESSONS.md",
    "cairn/references/INDEX.md",
)
# .gitignore entries every cairn repo carries (cairn-init §1).
REQUIRED_GITIGNORE = (
    "cairn/references/pdf/",
    "cairn/.merge-approved",
    "cairn/.merge-approved.pending",
)
# .Rbuildignore entry — package repos only (DESCRIPTION present); `^cairn$`
# keeps the whole tracking dir out of the built package.
REQUIRED_RBUILDIGNORE = ("^cairn$",)


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


_ID_RE = re.compile(r"(M\d+)")


def _milestone_files(root, *parts):
    out = {}
    for path in glob.glob(os.path.join(root, "cairn", *parts, "M*.md")):
        m = _ID_RE.match(os.path.basename(path))
        if m:
            out[m.group(1)] = path
    return out


def archive_files(root):
    """{id: path} for milestone files under cairn/milestones/archive/."""
    return _milestone_files(root, "milestones", "archive")


def live_files(root):
    """{id: path} for milestone files under cairn/milestones/ (not archive/)."""
    return _milestone_files(root, "milestones")


def id_num(mid):
    """Numeric sort key for an ID; non-numeric IDs sort last, deterministically."""
    return int(mid[1:]) if mid[1:].isdigit() else 10**9


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
            in_section = line.strip().lower().startswith("## candidates")
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


def claude_section_line_count(path):
    """Line count of the cairn-owned `## Project tracking (cairn)` section in a
    CLAUDE.md — the heading line through the line before the next H2 (`## `) or
    EOF. Returns None if the file is unreadable or has no such section (e.g. a
    repo mid-migration, or one that never adopted cairn); those are not a cap
    failure here. See D-018."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:
        return None
    start = None
    for i, line in enumerate(lines):
        if line.startswith(CLAUDE_SECTION_HEADING):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return end - start


def milestone_body_line_count(path):
    """Line count of a live milestone file's plan-owned body — every line
    before the first `## Review` heading. The review-exclusive `## Review`
    section is exempt from the milestone weight cap (M55): review evidence
    accumulates there at review time and must never scramble plan-owned content
    (the recurring M19/M22/M33/M50 scramble). A file with no `## Review` section
    counts whole (back-compat). Fenced code blocks are tracked so a literal
    `## Review` inside a ``` or ~~~ block in the body is not mistaken for the
    section boundary (M45). Returns None if the file is unreadable."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:
        return None
    fence = None
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```"):
            fence = "```"
            continue
        if stripped.startswith("~~~"):
            fence = "~~~"
            continue
        if line.startswith("## ") and line[3:].strip().lower() == "review":
            return i
    return len(lines)


def milestone_section_line_counts(path):
    """Ordered `(heading, line_count)` for each plan-owned `## ` section of a
    live milestone file — the diagnostic companion to
    `milestone_body_line_count`: when a plan-owned body is over cap, the caller
    reports which section carries the weight so trimming is one targeted pass,
    not a nibble-and-recount loop (M69). A section spans its `## ` heading
    through the line before the next `## ` heading (or the plan-owned/`## Review`
    boundary, or EOF). Lines before the first `## ` heading (title + status
    block) are preamble, attributed to no section, so preamble + the section
    counts sum to `milestone_body_line_count`. Fence-aware like that function: a
    `## ` inside a ``` or ~~~ block is content, and a fenced `## Review` is not
    the boundary (M45); the review-exclusive `## Review` section is excluded
    (M55). Returns None if the file is unreadable, [] if it has no `## ` section."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:
        return None
    sections = []
    fence = None
    start = None  # index of the current open section's `## ` heading
    heading = None
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```"):
            fence = "```"
            continue
        if stripped.startswith("~~~"):
            fence = "~~~"
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            if title.lower() == "review":
                if start is not None:
                    sections.append((heading, i - start))
                    start = None
                break
            if start is not None:
                sections.append((heading, i - start))
            start, heading = i, title
    else:
        # No `## Review` boundary hit — close the final open section at EOF.
        if start is not None:
            sections.append((heading, len(lines) - start))
    return sections


def sort_by_priority(row_list):
    """Rows sorted high>normal>low, then by numeric ID (M9 before M10)."""
    return sorted(
        row_list, key=lambda r: (PRIORITY_ORDER.get(r["priority"], 1), id_num(r["id"]))
    )


def die_not_cairn(start):
    sys.stderr.write(
        f"not a cairn repo: no cairn/ROADMAP.md at or above {start}\n"
    )
