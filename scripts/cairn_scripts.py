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

# The second weight axis (M84): file -> max character mass. LINE_CAPS counts
# ITEMS, because both files below are parsed one item per line (ROADMAP rows
# read positionally; D-015 defines LESSONS as one lesson per line) — so a line
# count cannot see prose accumulating INSIDE a line. cairn's LESSONS.md held 49
# lines, one under its <50 cap, across M78-M83 while its mass grew 16,567 ->
# 18,729 chars: the item cap was saturated and reported nothing. (That state is
# the ITEM axis's blind spot, and it is caught by the item cap it was one line
# from tripping — not by this advisory, which stays quiet there. The two axes
# divide labour; neither backstops the other's saturation — M87 review F3.)
#
# Each threshold is the mass its OWN line cap permits at MEASURED item length
# (M87, superseding M84-D1's item_cap x target_mean): non-item mass + capacity x
# measured mean item length, rounded up to the next 500, where capacity is
# (line cap - 1) - the file's fixed non-item lines. The -1 is because check_caps
# FAILs on `n >= cap`, so the permitted line counts are 49 and 59, not 50 and 60
# (M87 review F5). M84-D1 assumed target means instead of measuring — LESSONS
# 50 x 340 against a real mean of 581, ROADMAP 60 x 150 against a real blended
# mean of 497 (its 150 described the table rows; candidate rows run 4.3x that)
# — so both thresholds bound BEFORE their line caps (LESSONS at 83% of item
# capacity, ROADMAP at 40%) and the advisory fired at ordinary density.
# Re-derive by MEASURING, never by assuming a mean: the prescribed weight
# remedy is compression, and consolidating items RAISES the mean, so a mean
# copied from a previous milestone is stale by construction.
#
# ROADMAP's mean is blended over a BIMODAL population — table rows ~158,
# candidate rows ~683 — so it tracks composition as well as prose length, and a
# re-measurement checks the mix, not just the mean (M87 review F2; this is the
# mirror of the error M84-D1 made by describing only the rows). And because a
# threshold is capacity at FULL item count, a file below its item cap carries
# slack proportional to its unused slots.
#
# PROFILE.md is deliberately absent: surveyed at M84, no density problem, item
# cap alone. Advisory only (check_record_density WARNs, never FAILs): unlike an
# item count, "too dense" is a judgment about prose quality, not a structural
# fact.
CHAR_CAPS = {"cairn/ROADMAP.md": 21000, "cairn/LESSONS.md": 20500}
TERMINAL_ROW_RETENTION = 5  # done + dropped rows share one ROADMAP cap

# Per-line ceiling for NON-item lines only — headings, preamble, stamps, HTML
# comments (D-052, narrowing M84's blanket rejection of any per-line warn).
# M84's reason for that rejection is kept and still binds ITEM lines: pressure
# on a row, candidate, or lesson would reward splitting one across lines and
# corrode the one-item-per-line format both parsers depend on. A non-item line
# has no such format to corrode, and it is where prose hides from BOTH existing
# axes at once — the item cap counts lines and CHAR_CAPS counts whole-file mass,
# so cairn's `Last hygiene check` stamp reached 3,152 chars in one adopting repo
# (28% of that ROADMAP) with every gate green.
#
# 400 is measured, not assumed (M87). Survey of every non-item line in both
# capped files across all six cairn repos, 2026-07-19: healthy max 245 (a
# terminal-row-retention comment), then 230, 194, 141, 119, 105, 102, 101 —
# against two live defects at 1,870 (intraclass) and 2,568 (circumplex, down
# from a 3,152 peak after a same-day review pass rewrote it and still left it
# over). The comparison is `>=`, so 400 permits 399: 154 chars (63%) of headroom
# over the worst healthy line, and 4.7x/6.4x below both defects. Figures are
# dated because circumplex's moved mid-milestone, and every ratio here is
# against the CURRENT measurement, never the peak.
NON_ITEM_LINE_CAP = 400

# Cap on the cairn-owned `## Project tracking (cairn)` block appended to a
# repo's CLAUDE.md (D-018). Template target is ~25 lines; 30 gives headroom.
CLAUDE_SECTION_CAP = 30
CLAUDE_SECTION_HEADING = "## Project tracking"

# The plan-owned milestone section the weight cap does not measure (D-046/M77).
# `## Review` is already outside the cap by the body boundary itself (M55, a
# different reason: it is review-owned). The work log is exempt because D-045
# classifies it as history — never edited — so counting it could leave an
# over-cap file fixable only by an edit IP4 forbids. Matched exactly, lowercased.
WORKLOG_HEADING = "work log"

# §1 scaffold pieces that must exist once a repo is on cairn (cairn-init §1).
# Single source of truth for the machine-side drift check
# (cairn_validate.check_scaffold): a missing piece means the repo predates a
# later scaffold addition — route the user to /cairn-init repair. Only
# always-tracked pieces are listed: git does not preserve empty dirs, so the
# empty scaffold dirs (milestones/archive, reviews/archive, references/sources)
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
    "cairn/references/sources/",
    "cairn/.merge-approved",
    "cairn/.merge-approved.pending",
)
# Superseded .gitignore entries, old -> new. cairn is post-1.0, so a scaffold
# rename follows the deprecation cycle (tracking-rules "Universal tracking
# rules"): a repo still carrying only the old entry satisfies check_scaffold
# and gets a non-failing deprecation advisory naming the new one, rather than
# a hard FAIL it did nothing to earn. Renamed at M79 (D-047) because the shelf
# holds any source, not only PDFs.
DEPRECATED_GITIGNORE = {
    "cairn/references/pdf/": "cairn/references/sources/",
}
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


def non_item_lines(path):
    """Every NON-item line of a tracking file, as (lineno, length) pairs.

    An item line is one a parser reads positionally as a single record: a
    table row (`|…`) or a bullet (`- …`). Everything else — headings, italic
    preamble, the hygiene stamp, HTML comments — is prose, and is what
    NON_ITEM_LINE_CAP measures (D-052).

    Classification is by line SHAPE, not by threshold, so an item line is
    never merely under-measured: it is not measured at all, and no length
    can ever make it warn. That is what keeps M84's rejection intact —
    there is no incentive to split a row, because splitting a row buys
    nothing here.

    Blank lines are dropped; they carry no prose and would only pad output.
    Returns [] if the file is unreadable, matching the other measures."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except Exception:
        return []
    out = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("|") or stripped.startswith("- "):
            continue
        out.append((i, len(line)))
    return out


def char_count(path):
    """Character mass of a file, or None if unreadable — the weight axis's
    measure, paired with line_count's item axis (M84). Counts characters, not
    bytes, so a page of em-dashes is not penalised over a page of hyphens."""
    try:
        with open(path, encoding="utf-8") as f:
            return len(f.read())
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


def _plan_owned_scan(path):
    """Shared fence-aware scan behind both milestone cap counters. Returns
    `(boundary, sections)` where `boundary` is the end of the plan-owned region
    (the index of the first real `## Review` heading, else the file length) and
    `sections` is `[(heading, line_count)]` for every `## ` section before it,
    **work log included** — the callers decide what to exempt. Fenced ``` / ~~~
    blocks are tracked so a `## ` inside one is content, and a fenced
    `## Review` is not the boundary (M45). Only an exact `## Review` heading
    ends the region, so `## Reviewers` cannot truncate it (M55 review).
    Returns None if the file is unreadable."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:
        return None
    sections = []
    fence = None
    start = None  # index of the current open section's `## ` heading
    heading = None
    boundary = len(lines)
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
        if not line.startswith("## "):
            continue
        title = line[3:].strip()
        if title.lower() == "review":
            boundary = i
            if start is not None:
                sections.append((heading, i - start))
                start = None
            break
        if start is not None:
            sections.append((heading, i - start))
        start, heading = i, title
    if start is not None:  # close the final open section at the boundary
        sections.append((heading, boundary - start))
    return boundary, sections


def milestone_body_line_count(path):
    """Line count of a live milestone file's **capped** plan-owned body: every
    line before the first `## Review` heading, less the `## Work log` section.
    Two sections sit outside the milestone weight cap, for two different
    reasons. `## Review` is review-owned and accumulates evidence at review
    time, which must never scramble plan-owned content (M55, the recurring
    M19/M22/M33/M50 scramble). The **work log** is exempt because D-045
    classifies it as history — never edited — so counting it could leave an
    over-cap file fixable only by an edit IP4 forbids (D-046/M77); the
    wrapped-entry advisory in `cairn_validate`, not the cap, is what keeps the
    now-unbudgeted section honest. A file with no `## Review` section counts to
    EOF — still less its work log, which is exempt wherever it sits, so this is
    back-compatible only for the pre-M77 case of a file with no work log. A
    fenced `## Review` or `## Work log` is content, not a boundary (M45), and
    only exact headings match — `## Work log notes` stays counted. Returns None
    if the file is unreadable."""
    scan = _plan_owned_scan(path)
    if scan is None:
        return None
    boundary, sections = scan
    exempt = sum(n for h, n in sections if h.strip().lower() == WORKLOG_HEADING)
    return boundary - exempt


def milestone_worklog_lines(path):
    """`[(lineno, text)]` for the body of a milestone file's `## Work log`
    section, 1-indexed, heading excluded. Shares `WORKLOG_HEADING` and the
    fence rules with the cap counters **on purpose**: the section the cap stops
    measuring and the section the wrapped-entry advisory polices must be the
    same one, or the exemption would open a hole the advisory never looks at
    (D-046/M77). Returns [] when the file has no work log, None if unreadable."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:
        return None
    out = []
    fence = None
    in_log = False
    for i, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            if in_log:  # both delimiters belong to the section, like the
                out.append((i, line))  # cap counters count them (M77 review F2)
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = "```" if stripped.startswith("```") else "~~~"
            if in_log:
                out.append((i, line))
            continue
        if line.startswith("## "):
            in_log = line[3:].strip().lower() == WORKLOG_HEADING
            continue
        if in_log:
            out.append((i, line))
    return out


def milestone_section_line_counts(path):
    """Ordered `(heading, line_count)` for each plan-owned `## ` section of a
    live milestone file — the diagnostic companion to
    `milestone_body_line_count`: when a plan-owned body is over cap, the caller
    reports which section carries the weight so trimming is one targeted pass,
    not a nibble-and-recount loop (M69). A section spans its `## ` heading
    through the line before the next `## ` heading (or the plan-owned/`## Review`
    boundary, or EOF). Lines before the first `## ` heading (title + status
    block) are preamble, attributed to no section, so preamble + the section
    counts sum to `milestone_body_line_count`. Both cap-exempt sections are
    excluded, so the breakdown only ever names sections the operator may
    actually trim: the review-exclusive `## Review` (M55) and the `## Work log`,
    which D-045 makes history — naming it would aim the cap remedy at an edit
    IP4 forbids (D-046/M77). Dropping it here and from the body count together
    is what preserves the preamble+sections==body invariant. Fence-aware like
    that function: a `## ` inside a ``` or ~~~ block is content, and a fenced
    `## Review` is not the boundary (M45). Returns None if the file is
    unreadable, [] if it has no trimmable `## ` section."""
    scan = _plan_owned_scan(path)
    if scan is None:
        return None
    _, sections = scan
    return [(h, n) for h, n in sections if h.strip().lower() != WORKLOG_HEADING]


def sort_by_priority(row_list):
    """Rows sorted high>normal>low, then by numeric ID (M9 before M10)."""
    return sorted(
        row_list, key=lambda r: (PRIORITY_ORDER.get(r["priority"], 1), id_num(r["id"]))
    )


def die_not_cairn(start):
    sys.stderr.write(
        f"not a cairn repo: no cairn/ROADMAP.md at or above {start}\n"
    )
