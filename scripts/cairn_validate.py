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
        path = os.path.join(root, "cairn", r["relpath"])
        if "archive/" in r["relpath"]:
            n = cs.line_count(path)
            if n is not None and n > cs.ARCHIVE_CAP:
                bad.append(f"cairn/{r['relpath']}: {n} lines (archive cap {cs.ARCHIVE_CAP})")
        else:
            # Live milestone: cap the plan-owned body only; the review-exclusive
            # `## Review` section is exempt so review evidence never scrambles
            # plan-owned content (M55).
            n = cs.milestone_body_line_count(path)
            if n is not None and n >= cs.MILESTONE_CAP:
                bad.append(
                    f"cairn/{r['relpath']}: {n} plan-owned lines (cap <{cs.MILESTONE_CAP})"
                )
    return bad


def check_terminal_retention(rows):
    terminal = [r["id"] for r in rows if r["status"] in ("done", "dropped")]
    if len(terminal) > cs.TERMINAL_ROW_RETENTION:
        return [
            f"{len(terminal)} terminal rows (retention {cs.TERMINAL_ROW_RETENTION}): "
            f"{', '.join(terminal)}"
        ]
    return []


def check_vocab(rows):
    return [
        f"{r['id']}: unknown status '{r['status']}'"
        for r in rows
        if r["status"] not in cs.STATUSES
    ]


def check_priority_vocab(rows):
    """Every ROADMAP row's Priority is one of the known values (the
    `PRIORITY_ORDER` keys — high/normal/low), parallel to `check_vocab` for
    status. A typo'd priority silently mis-sorts `cairn_next` (unknown falls
    back to `normal`), so catch it at the declaration point."""
    return [
        f"{r['id']}: unknown priority '{r['priority']}'"
        for r in rows
        if r["priority"] not in cs.PRIORITY_ORDER
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


# An INDEX.md catalog line: `- <name>.md — one-line summary`.
_INDEX_LINE = re.compile(r"^\s*[-*]\s+(\S+\.md)\b")


def check_references(root):
    """Every committed top-level cairn/references/*.md (except INDEX.md) has
    an INDEX.md line, and every INDEX.md line's target exists on disk — the
    references sibling of the roadmap<->disk orphan check (M57). No-ops when
    references/INDEX.md is absent (scaffold-present owns that failure)."""
    bad = []
    refdir = os.path.join(root, "cairn", "references")
    index = os.path.join(refdir, "INDEX.md")
    if not os.path.isfile(index):
        return bad
    with open(index, encoding="utf-8") as f:
        listed = [m.group(1) for line in f if (m := _INDEX_LINE.match(line))]
    for name in sorted(os.listdir(refdir)):
        if (
            name.endswith(".md")
            and name != "INDEX.md"
            and os.path.isfile(os.path.join(refdir, name))
            and name not in listed
        ):
            bad.append(f"cairn/references/{name} has no INDEX.md line")
    for name in listed:
        if not os.path.isfile(os.path.join(refdir, name)):
            bad.append(
                f"INDEX.md lists {name} but no such file in cairn/references/"
            )
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


_AC_ITEM = re.compile(r"^\s*-\s*\[[ xX]\]")
_AC_REF = re.compile(r"\bAC(\d+)\b")


def _section_body(text, heading):
    """Lines under the first `## <heading>` H2, up to the next H2 or EOF."""
    out = []
    in_sec = False
    for line in text.splitlines():
        if line.startswith("## "):
            if in_sec:
                break
            in_sec = line[3:].strip().lower().startswith(heading.lower())
            continue
        if in_sec:
            out.append(line)
    return out


def check_coverage_complete(root):
    """Every acceptance criterion in a live milestone file is referenced in
    that file's Coverage section, and no Coverage line cites a criterion that
    does not exist. The runtime arm of M18's skill-text traceability
    (test_ac_traceability.py owns the prose side). Live files only — archived
    summaries are compressed and carry no Coverage section by design."""
    bad = []
    for mid, path in sorted(cs.live_files(root).items(), key=lambda kv: cs.id_num(kv[0])):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        n = sum(1 for line in _section_body(text, "Acceptance criteria") if _AC_ITEM.match(line))
        if n == 0:
            continue  # nothing to map (e.g. a stub); not this check's concern
        refs = {int(m) for line in _section_body(text, "Coverage") for m in _AC_REF.findall(line)}
        for k in range(1, n + 1):
            if k not in refs:
                bad.append(f"{mid}: AC{k} not referenced in Coverage")
        for r in sorted(refs):
            if r > n:
                bad.append(f"{mid}: Coverage references AC{r} but file has {n} criteria")
    return bad


_PRINCIPLE_ID = re.compile(r"\b[IG]P\d+\b")
_SLOT_LINE = re.compile(r"^\s*-\s*\*\*Principles touched:\*\*\s*(.*)$", re.IGNORECASE)
_PRINCIPLE_DEF = re.compile(r"^\s*-\s*([IG]P\d+):")
_HTML_COMMENT = re.compile(r"<!--.*?-->")


def _design_principles(root):
    """Ids of principles defined in DESIGN.md — lines like `- IP1: …`."""
    ids = set()
    try:
        with open(os.path.join(root, "cairn", "DESIGN.md"), encoding="utf-8") as f:
            for line in f:
                m = _PRINCIPLE_DEF.match(line)
                if m:
                    ids.add(m.group(1))
    except Exception:
        pass
    return ids


def check_principles_slot(root):
    """Each live milestone's `Principles touched:` slot names only current
    DESIGN.md principles. No-op when the slot is absent or `—` (validate-if-
    present, mirroring coverage — archived and pre-slot files carry none), so
    a typo'd or retired-principle id is caught at the declaration point (M38)
    rather than misattributing a Sync Impact Report line (M17)."""
    defined = _design_principles(root)
    bad = []
    for mid, path in sorted(cs.live_files(root).items(), key=lambda kv: cs.id_num(kv[0])):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        for line in text.splitlines():
            m = _SLOT_LINE.match(line)
            if not m:
                continue
            body = _HTML_COMMENT.sub("", m.group(1)).strip()
            if body and body != "—":
                for pid in _PRINCIPLE_ID.findall(body):
                    if pid not in defined:
                        bad.append(f"{mid}: Principles touched cites {pid}, not a DESIGN.md principle")
            break  # only the first slot line in the header
    return bad


_REQUIRED_SLOTS = (
    "verify",
    "consistency-gate",
    "test-doctrine",
    "release-walk",
    "init-detection",
    "greenfield-openers",
)


def _profile_slots(text):
    """Map each `## <slot>` H2 in a PROFILE.md to its (stripped) body lines.
    Fence-aware: a `## ` line inside a ``` or ~~~ fenced code block is body
    content, not a slot heading — the schema sanctions a command-block slot
    body, and a shell `## comment` inside one must not be misread as a new
    slot (review finding, scored 91)."""
    slots = {}
    cur = None
    fence = None  # the open fence marker (``` or ~~~), or None outside a fence
    for line in text.splitlines():
        marker = line.lstrip()[:3]
        if marker in ("```", "~~~"):
            fence = None if fence == marker else (fence or marker)
            if cur is not None:
                slots[cur].append(line)
            continue
        if fence is None and line.startswith("## "):
            cur = line[3:].strip().lower()
            slots[cur] = []
        elif cur is not None:
            slots[cur].append(line)
    return slots


def check_profile(root):
    """cairn/PROFILE.md, when present, defines exactly the six known toolchain
    slots, each non-empty. No-op when absent — a repo that adopted cairn before
    profiles keeps working, and the skills infer the profile from DESCRIPTION at
    point of use (tracking-rules "Toolchain profiles"). Validate-if-present,
    mirroring the coverage/principles checks: a missing, empty, or misspelled
    slot is caught at the declaration point rather than misfiring a skill."""
    path = os.path.join(root, "cairn", "PROFILE.md")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return []
    slots = _profile_slots(text)
    bad = []
    for slot in _REQUIRED_SLOTS:
        if slot not in slots:
            bad.append(f"PROFILE.md missing slot '## {slot}'")
        elif not any(line.strip() for line in slots[slot]):
            bad.append(f"PROFILE.md slot '## {slot}' is empty")
    for slot in slots:
        if slot not in _REQUIRED_SLOTS:
            bad.append(f"PROFILE.md has unrecognized slot '## {slot}'")
    return bad


# Split tripwires (tracking-rules "Sizing"): a milestone probably wants
# splitting past these. Advisory, not hard limits — a milestone may exceed
# them with stated justification — so check_sizing_advisory only WARNs.
_CRIT_TRIPWIRE = 7
_TASK_TRIPWIRE = 10


def check_sizing_advisory(root):
    """Advisory: a live milestone file whose acceptance-criteria count exceeds
    7, or whose task count exceeds 10 (the tracking-rules "Sizing" split
    tripwires), probably wants splitting. Advisory rather than a gate — the
    tripwires are advisory (exceed-with-justification is legitimate) — so this
    feeds ADVISORIES (WARN, exit-code-neutral), never CHECKS. Archived
    summaries carry neither section and are skipped (live_files only)."""
    out = []
    for mid, path in sorted(cs.live_files(root).items(), key=lambda kv: cs.id_num(kv[0])):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        n_crit = sum(1 for line in _section_body(text, "Acceptance criteria") if _AC_ITEM.match(line))
        n_task = sum(1 for line in _section_body(text, "Tasks") if _AC_ITEM.match(line))
        if n_crit > _CRIT_TRIPWIRE:
            out.append(f"{mid}: {n_crit} acceptance criteria (>{_CRIT_TRIPWIRE} tripwire) — consider splitting")
        if n_task > _TASK_TRIPWIRE:
            out.append(f"{mid}: {n_task} tasks (>{_TASK_TRIPWIRE} tripwire) — consider splitting")
    return out


CHECKS = [
    ("mirror agreement", lambda root, rows: check_mirror(root, rows)),
    ("at most one in-progress", lambda root, rows: check_single_in_progress(rows)),
    ("weight caps", lambda root, rows: check_caps(root, rows)),
    ("terminal-row retention", lambda root, rows: check_terminal_retention(rows)),
    ("status vocabulary", lambda root, rows: check_vocab(rows)),
    ("priority vocabulary", lambda root, rows: check_priority_vocab(rows)),
    ("dependency resolution", lambda root, rows: check_dependencies(root, rows)),
    ("roadmap<->disk orphans", lambda root, rows: check_orphans(root, rows)),
    ("references index<->disk", lambda root, rows: check_references(root)),
    ("id uniqueness", lambda root, rows: check_id_uniqueness(root, rows)),
    ("iso date format", lambda root, rows: check_dates(root)),
    ("scaffold present", lambda root, rows: check_scaffold(root)),
    ("coverage complete", lambda root, rows: check_coverage_complete(root)),
    ("principles slot valid", lambda root, rows: check_principles_slot(root)),
    ("profile valid", lambda root, rows: check_profile(root)),
]

# Advisories are non-failing: they surface a judgment-call worth a look but
# never fail the gate (exit code neutral), so they render WARN/OK, separate
# from the PASS/FAIL CHECKS above.
ADVISORIES = [
    ("sizing (split tripwires)", lambda root, rows: check_sizing_advisory(root)),
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
    warnings = 0
    for name, fn in ADVISORIES:
        findings = fn(root, rows)
        if findings:
            warnings += len(findings)
            lines.append(f"WARN  {name} ({len(findings)})")
            for f in findings:
                lines.append(f"        {f}")
        else:
            lines.append(f"OK    {name}")
    lines.append("")
    if failures:
        lines.append(f"{failures} check(s) failed")
    else:
        lines.append("all checks passed")
    if warnings:
        lines.append(f"{warnings} advisory warning(s) — not gate failures")
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
