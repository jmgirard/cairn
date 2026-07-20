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

import datetime
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
            # Live milestone: cap the plan-owned body only. Two sections are
            # exempt — the review-exclusive `## Review`, so review evidence never
            # scrambles plan-owned content (M55), and the `## Work log`, which
            # D-045 makes history so the cap must never demand an edit IP4
            # forbids (D-046). Both are absent from the breakdown below.
            n = cs.milestone_body_line_count(path)
            if n is not None and n >= cs.MILESTONE_CAP:
                # Report which plan-owned section carries the weight, heaviest
                # first, so trimming is one targeted pass, not a nibble-and-
                # recount loop (M69). `shed` is the lines to drop to pass (<cap).
                shed = n - cs.MILESTONE_CAP + 1
                finding = (
                    f"cairn/{r['relpath']}: {n} plan-owned lines "
                    f"(cap <{cs.MILESTONE_CAP}; shed ≥{shed})"
                )
                sections = cs.milestone_section_line_counts(path)
                if sections:
                    ranked = sorted(sections, key=lambda s: s[1], reverse=True)
                    breakdown = " · ".join(f"{h} {c}" for h, c in ranked)
                    finding += f"\n        heaviest first: {breakdown}"
                bad.append(finding)
    return bad


def check_record_density(root):
    """Advisory: an item-list file whose character mass exceeds its threshold
    (M84). The weight axis, orthogonal to check_caps' item axis over the same
    whole file — `cairn/ROADMAP.md` and `cairn/LESSONS.md` are parsed one item
    per line, so their line count measures ITEMS and is structurally blind to
    prose accumulating inside a line. cairn's LESSONS.md sat at 49 lines (item
    cap <50) across M78-M83 while its mass grew 16,567 -> 18,729 bytes and the
    audit reported nothing.

    Two reports, one advisory. The second is a per-line ceiling on NON-item
    lines (D-052, narrowing M84's original blanket rejection of any per-line
    warn). That rejection is kept for ITEM lines and still holds there:
    pressure on individual line length would reward splitting an item across
    lines and corrode the one-item-per-line format both parsers depend on. A
    heading, preamble, stamp, or comment has no such format to corrode, and it
    is exactly where prose hides from both whole-file axes at once — cairn's
    hygiene stamp reached 3,152 chars in an adopting repo while the item cap
    (35 of 60 lines) and the mass threshold (11,410 of 21,000) both read green
    (2026-07-19; a review pass later rewrote that stamp to 2,568, still over).

    WARN, never FAIL, on both axes — D-018 wanted a hard signal for the
    CLAUDE.md section cap, where cairn owns the whole content, but density is a
    judgment about prose quality, the same call the references-staleness
    advisory already makes.

    The whole-file finding names both axes, because the item count looking fine
    is the whole point, and prescribes the weight remedy (compress) rather than
    the item remedy (evict/graduate). The per-line finding names the line, since
    a file-level number cannot point at the one line responsible."""
    out = []
    for rel, cap in cs.CHAR_CAPS.items():
        path = os.path.join(root, rel)
        n = cs.char_count(path)
        if n is None or n < cap:
            continue
        lines = cs.line_count(path)
        item_cap = cs.LINE_CAPS.get(rel)
        axis = f"{lines} lines" if lines is not None else "line count unknown"
        if lines is not None and item_cap is not None:
            axis += f", item cap <{item_cap}"
        # `threshold <N`, not a bare N: every neighbouring cap prints its
        # strictness marker (`cap <60`), and the comparison here is `>=`, so a
        # bare number would tell an author 9,000 was the permitted ceiling
        # while a 9,000-char file WARNs with `shed ≥1` (M84 review F5).
        out.append(
            f"{rel}: {n:,} chars over {axis} "
            f"(threshold <{cap:,}; shed ≥{n - cap + 1:,}) — compress entries, "
            f"don't evict them"
        )
    # The per-line axis. Same files, same WARN severity, same `>=` comparison
    # as every neighbouring cap — so `<400` permits 399 and the shed figure is
    # derived through the operator rather than assumed from the cap (M87).
    line_cap = cs.NON_ITEM_LINE_CAP
    for rel in cs.CHAR_CAPS:
        path = os.path.join(root, rel)
        for lineno, length in cs.non_item_lines(path):
            if length < line_cap:
                continue
            out.append(
                f"{rel}:{lineno}: non-item line is {length:,} chars "
                f"(cap <{line_cap:,}; shed ≥{length - line_cap + 1:,}) — "
                f"replace it, don't append to it; git holds the older text"
            )
    return out


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


# An INDEX.md catalog line: `- <name>.md — one-line summary`. The name may be
# decorated (backticks, a [name](name) markdown link) and, since M79, may be a
# path into a subdirectory — a semantically correct entry must never trip a
# hard CHECK on formatting alone (D-023; review F1/85), so the capture excludes
# decoration characters.
_INDEX_LINE = re.compile(r"^\s*[-*]\s+[\[`]*([\w./-]+\.md)\b")


def _catalog_entries(refdir, index):
    """The INDEX.md lines that are catalog entries for committed pages.

    Widening the capture to accept subdirectory paths (M79) also let two
    non-entries through, both closed here (review F5):

    - A path escaping the references tree (`../../DESIGN.md`) is dropped. It
      is not a catalog entry, and joining it unnormalized let a file OUTSIDE
      cairn/references/ silently satisfy the existence check below.
    - A path whose directory does not exist under refdir (`cairn/DESIGN.md`
      in a "see also" bullet) is dropped rather than reported as a missing
      target — an INDEX.md may carry prose, and a hard CHECK must not fire on
      a bullet that was never a page reference (D-023). The cost is a miss:
      deleting a whole subdirectory hides its entries instead of flagging
      them, which is the tolerated side of the doctrine.
    """
    entries = []
    with open(index, encoding="utf-8") as f:
        for line in f:
            m = _INDEX_LINE.match(line)
            if not m:
                continue
            rel = m.group(1)
            target = os.path.normpath(os.path.join(refdir, rel))
            if os.path.commonpath(
                [os.path.abspath(refdir), os.path.abspath(target)]
            ) != os.path.abspath(refdir):
                continue
            if not os.path.isdir(os.path.dirname(target)):
                continue
            entries.append(rel)
    return entries
# The M78 provenance block's three semantic tokens, read decoration-tolerantly
# (M79-D1: D-023's no-false-positive doctrine is honoured in the parser, not
# the severity). Leading `>`/`*`/`_`/`#`/backticks are stripped before the
# heading match, so `**Provenance.**`, `__Provenance__`, and a bare
# `Provenance.` all read alike; the date and the `from` pointer tolerate
# bold/backtick decoration around them.
# `\b` is the wrong boundary here: `_` is a word character in Python regex, so
# `__Provenance__` would not match a trailing `\b`. Decoration boundaries are
# therefore "not alphanumeric" lookarounds, which read through `*`, `_`, and
# backticks alike.
_D = r"[\s*_`]*"  # inline decoration between a keyword and its value
# Both fields are searched across the whole block rather than pinned to the
# heading line: M78 calls the block "prose in the page's own idiom", so a
# hard-wrapped pointer must still read. The cost is a miss — an Extraction
# line that happens to name a source satisfies the pointer test — which is the
# right side of D-023's "a missed weird format beats a false positive".
# The heading token must read as a *label*, not merely as a line that starts
# with the word. `(?![A-Za-z0-9])` was too weak: hard-wrapped prose puts
# "provenance" at the start of a line by accident, and every such line opened a
# phantom block. That is not a cosmetic misread — prose discussing ingestion
# satisfies both field tests, so a page with NO provenance block passed the
# hard CHECK outright (reported from intraclass against its ORACLES.md). The
# label test: after the token, the line closes the token in strong emphasis
# (`**Provenance**`, `__Provenance__` — the M79 form whose body runs on with no
# punctuation), or continues past a `.`/`:`/dash terminator, or ends (a bare
# `## Provenance` section heading). Two deliberate exclusions: a bare `-` is
# not a terminator (`` `provenance`-attr `` is prose), and a lone backtick is
# not strong emphasis (`` `provenance` attr `` is a code-span mention, not a
# label) — both are live prose lines in cairn's own references/.
_PROV_HEAD = re.compile(
    r"^[\s>*_`#]*provenance(?:[*_]{2}|[*_`]*\s*[.:—–]|[*_`]*\s*$)", re.I
)
_PROV_INGESTED = re.compile(
    rf"(?<![A-Za-z0-9])ingested(?![A-Za-z0-9]){_D}(\d{{4}}-\d{{2}}-\d{{2}})",
    re.I,
)
# The source pointer is deliberately permissive (review F4): M78's template
# sanctions "the URL plus how it was retrieved and by whom" for a non-PDF
# source, which need not contain the word "from" — and a hard CHECK that
# fails a template-compliant page is the false positive M79-D1 promised the
# parser would absorb. This field's job is to catch a block naming no source
# at all; the ingested date is the crisp field.
_PROV_SOURCE = re.compile(
    rf"(?<![A-Za-z0-9])(?:from|via|retrieved|downloaded|accessed|source)"
    rf"(?![A-Za-z0-9]){_D}\S",
    re.I,
)
_PROV_LOCATOR = re.compile(r"https?://\S|[\w.-]+/[\w.-]")


def _provenance_block(path, for_extraction=False):
    """The provenance prose of a references page. M78 calls the block "prose
    in the page's own idiom, not frontmatter", so the parser is generous
    about layout (review F2/F3):

    - EVERY `**Provenance.**`-headed run is collected, not just the first, so
      a decoy line — a `## Provenance` section heading above the real block —
      cannot swallow the page's provenance and fail it.
    - A run is the heading line plus the following non-blank lines; when that
      yields neither semantic field the next paragraph is pulled in too, so a
      label alone on its own line still finds its body below the blank.

    `for_extraction` widens that continuation test by one field — the run also
    extends when it names no extraction status — and **only the M81 staleness
    advisory passes it.** The hard `references index<->disk` CHECK keeps M79's
    two-field test untouched, because the two callers need opposite
    protections and one shared rule cannot give both (M81 review F1, scored
    93). That CHECK asks only *existence* questions, so a wider block cannot
    make it FAIL — it ERASES FAILs: absorbing the next paragraph lets an
    unrelated `**Citation.**` line satisfy the source-pointer test, and
    `_PROV_LOCATOR`'s `[\\w.-]+/[\\w.-]` arm matches any slash, including the
    `volume/issue/pages` the source-note template itself prints. A page
    genuinely missing its source pointer would then pass. The advisory can
    afford the wider read because its own failure mode is the opposite one: a
    missed status there is a quiet WARN, not a silently-erased gate failure.

    Returns None when the page carries no provenance heading at all."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    blocks = []
    for i, line in enumerate(lines):
        if not _PROV_HEAD.match(line):
            continue
        run, j = [line], i + 1
        while j < len(lines) and lines[j].strip():
            run.append(lines[j])
            j += 1
        text = "\n".join(run)
        complete = _PROV_INGESTED.search(text) or _PROV_SOURCE.search(text)
        if for_extraction:
            complete = complete and _extraction_status(text)
        if not complete:
            while j < len(lines) and not lines[j].strip():
                j += 1
            while j < len(lines) and lines[j].strip():
                run.append(lines[j])
                j += 1
        blocks.append("\n".join(run))
    return "\n".join(blocks) if blocks else None


def _ingested_date(block):
    """The provenance block's `Ingested:` date, or None when it names none or
    names something that is not a date.

    The single definition of "this block has an ingested date", shared by the
    hard `references index<->disk` CHECK and the staleness advisory (M89
    defect B). They disagreed before: `_PROV_INGESTED` tests only the SHAPE
    `\\d{4}-\\d{2}-\\d{2}`, so `2026-13-45` matched and satisfied the CHECK,
    while `_iso` refused to build a date from it and left the advisory with
    nothing — which it then skipped, on the stated ground that the CHECK had
    already failed the block. Neither reported the page. One predicate, so a
    block is either dated for both readers or dated for neither."""
    m = _PROV_INGESTED.search(block)
    if not m:
        return None
    found = _iso(m.group(1))
    return found[0] if found else None


def _has_source_pointer(block):
    """A provenance block names a source when it carries an attribution verb
    with something after it, or a bare URL/path locator (review F4)."""
    return bool(_PROV_SOURCE.search(block) or _PROV_LOCATOR.search(block))


def _reference_pages(refdir):
    """Every committed .md page under cairn/references/, as paths relative to
    that directory, INDEX.md excluded. Walks recursively (M79): a page in a
    subdirectory is enforced exactly as a top-level page is. The gitignored
    source shelf holds PDFs, not pages, and is skipped along with its legacy
    `pdf/` name so an un-migrated repo's shelf is never walked."""
    pages = []
    for dirpath, dirnames, filenames in os.walk(refdir):
        if dirpath == refdir:
            dirnames[:] = [d for d in dirnames if d not in ("sources", "pdf")]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), refdir)
            if rel != "INDEX.md":
                pages.append(rel.replace(os.sep, "/"))
    return sorted(pages)


def check_references(root):
    """Every committed cairn/references/ page (except INDEX.md) has an
    INDEX.md line and a provenance block naming an ingested date and a source
    pointer; every INDEX.md line's target exists on disk. The references
    sibling of the roadmap<->disk orphan check (M57), given content teeth by
    M79 so the check stops being a filename census. No-ops only when the
    directory holds no pages at all — a genuinely not-adopted signal (M45);
    an INDEX.md missing beneath real pages is reported here, not passed."""
    bad = []
    refdir = os.path.join(root, "cairn", "references")
    if not os.path.isdir(refdir):
        return bad
    pages = _reference_pages(refdir)
    index = os.path.join(refdir, "INDEX.md")
    if not os.path.isfile(index):
        if pages:
            bad.append(
                f"cairn/references/ holds {len(pages)} page(s) but no INDEX.md"
            )
        return bad
    listed = _catalog_entries(refdir, index)
    for rel in pages:
        if rel not in listed:
            bad.append(f"cairn/references/{rel} has no INDEX.md line")
        block = _provenance_block(os.path.join(refdir, rel))
        if block is None:
            bad.append(f"cairn/references/{rel} has no provenance block")
            continue
        if _ingested_date(block) is None:
            # Named-but-unparseable is reported as its own thing (M89): a
            # block reading `Ingested 2026-13-45` does name a date field, and
            # telling its author it "names no ingested date" sends them
            # looking for a line that is right there.
            shaped = _PROV_INGESTED.search(block)
            bad.append(
                f"cairn/references/{rel} provenance ingested date "
                f"{shaped.group(1)} is not a real date"
                if shaped else
                f"cairn/references/{rel} provenance names no ingested date"
            )
        if not _has_source_pointer(block):
            bad.append(
                f"cairn/references/{rel} provenance names no source pointer"
            )
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
    superseded = {new: old for old, new in cs.DEPRECATED_GITIGNORE.items()}
    for entry in cs.REQUIRED_GITIGNORE:
        if entry in gitignore:
            continue
        # A repo still carrying only the pre-rename entry is not drifted, it
        # is un-migrated: the deprecation advisory names it, this check does
        # not fail it (post-1.0 deprecation cycle — D-047).
        if superseded.get(entry) in gitignore:
            continue
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
    "changelog",
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
    """cairn/PROFILE.md, when present, defines exactly the seven known toolchain
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


def check_gitignore_deprecations(root):
    """Advisory arm of the scaffold deprecation cycle: a repo carrying a
    superseded .gitignore entry is told its new name without being failed.
    Exit-code neutral by design — the rename is cairn's, not the repo's, so a
    hard FAIL would block a milestone over a scaffold change the maintainer
    never made (D-047; the D-040 migration-cost precedent, one severity
    softer because a rename has a mechanical successor a slot addition
    lacks)."""
    bad = []
    gitignore = _ignore_entries(os.path.join(root, ".gitignore"))
    for old, new in cs.DEPRECATED_GITIGNORE.items():
        if old in gitignore and new not in gitignore:
            bad.append(
                f".gitignore entry '{old}' is superseded by '{new}' — "
                f"rename the entry and the directory"
            )
    return bad


# A work-log entry opens with a `- ` bullet (tracking-rules: one line each,
# absolute dates). Anything else non-blank in the section is a continuation —
# except an HTML comment, which is structure carrying no entry text. Comment
# detection is stateful across lines, not a single-line regex: the milestone
# template's own owner comment spans three physical lines, so a one-line-only
# matcher made the shipped template warn three times on every milestone it
# created — the two halves of M77 contradicting each other (M77 review F1).
_LOG_ENTRY = re.compile(r"^\s*-\s")
_LOG_PREVIEW = 60


# --- references staleness (M81) ---------------------------------------------
# M78 gave every committed references page an `Extraction:` status; until now
# nothing read it, so a page recording an unchecked subagent pass rendered
# exactly like a confirmed one. These read that status the same
# decoration-tolerant way `_provenance_block` reads its heading.
_PROV_EXTRACTION = re.compile(
    rf"^[\s>*_`#]*extraction(?![A-Za-z0-9]){_D}:(.*)$", re.I
)
# The `— observed YYYY-MM-DD` stamp records when the STATUS was written, not
# when the source was re-read. It is stripped before any date is taken out of
# the line: left in, it is always the freshest date present, and the advisory
# would read its own write stamp and never fire.
_OBSERVED_STAMP = re.compile(
    rf"(?<![A-Za-z0-9])observed(?![A-Za-z0-9]){_D}\d{{4}}-\d{{2}}-\d{{2}}", re.I
)
_ISO_DATE = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
# An explicit assertion that the page was never checked against its source.
# The two states are mutually exclusive by template design — the shipped forms
# are `|`-separated alternatives — so this is read before any date.
# M83: a status is classified CLAUSE BY CLAUSE, and each clause's claim is read
# as the verb it uses plus whether that verb is negated. M81 scanned the whole
# status for one word, so a single `unverified` anywhere overrode a dated
# verification above it — a page reading "verified 2026-07-18 … (prior status:
# unverified)" reported no verified re-check at all (F3, hit live 2026-07-18).
# Testing dates first instead only mirrors the bug, so contradicting clauses are
# reported rather than silently resolved.
#
# The first cut of this fix matched an affirmative verb set and a separate
# never-phrase set, which the M83 review caught failing in both directions
# (F1/92, F2/92): the never-set negated only the word `verified`, so `no claim
# checked against the source` read as a VERIFICATION — inventing a
# contradiction on the very prose that motivated the milestone, and clearing a
# page that says in plain words it was never checked. Negation is a property of
# the clause, not a fixed phrase list, so it is detected as one.
_CLAUSE_BOUNDARY = re.compile(r"\s+—\s+|[;,]\s+")
# The verification verbs the shipped corpus actually uses, not just the two the
# templates sanction. The lookbehind keeps `verified` from matching inside
# `unverified`, which carries its own negation. A `re-` prefix is deliberately
# NOT excluded here (review F3/76): `re-verified against the source` is an
# affirmative re-verification, and the template's `not yet re-read against the
# source` is caught by its negator instead of by the hyphen.
_VERIFY_VERB = re.compile(
    r"(?<![A-Za-z0-9])(?:re-)?(?:verified|read\s+against|checked\s+against|"
    r"read\s+directly)(?![A-Za-z0-9])",
    re.I,
)
# `unverified` is a verb carrying its own negator.
_UNVERIFIED = re.compile(r"(?<![A-Za-z0-9])unverified(?![A-Za-z0-9])", re.I)
# Negators, matched only WITHIN the clause holding the verb and only BEFORE it.
# Clause-scoping is what keeps this narrow: three shipped `partly verified at
# ingestion` pages carry `not re-read since` in a LATER clause, and a status-wide
# negation search would sweep all three up — the M79-F5 trap the M81 row warned
# about (LESSONS: widening a capture class admits non-targets too).
_NEGATOR = re.compile(
    r"(?<![A-Za-z0-9])(?:never|not|nothing|none|no)(?![A-Za-z0-9])", re.I
)
# Partiality qualifiers, placed exactly like `_NEGATOR` — within the clause
# holding the verb and only BEFORE it. `partly verified at ingestion` parsed as
# a plain affirmative verification and then aged from the block's ingested
# date, so a page whose own words say most of it was never checked returned
# `ok` (M89 defect A; live on three pages here and four intraclass notes).
#
# The set is deliberately literal. Scope-limiting hedges — `some`, `key
# claims`, `a few` — read as partiality to a human but each one widens the
# capture class, and the M79-F5 lesson is that widening admits non-targets.
# These four cover every partial form the shipped corpus actually writes; a
# fifth is added when a page needing it appears, not in anticipation.
#
# `spot[-\s]check` takes a hyphen OR a space: both spellings are the same word,
# and the hyphen is not what makes it a qualifier.
_PARTIAL = re.compile(
    r"(?<![A-Za-z0-9])(?:partly|partially|in\s+part|spot[-\s]check(?:ed)?)"
    r"(?![A-Za-z0-9])",
    re.I,
)
# A first-hand record has no external source to re-read, so asking it to
# re-verify asks the impossible. The exemption is earned by the status SAYING
# so (the synthesis template's sanctioned phrase), never by page type — a
# synthesis note derived from other pages does age, and says so with a date.
_NOTHING_TO_VERIFY = re.compile(r"nothing to re-?verify", re.I)
# Where a status's paragraph ends: the next `Label:` field (`Pagination:`,
# `Citation:`) or a bolded field opener (`**Citation.**`). Without this the
# status would absorb the citation paragraph and read dates out of it.
_FIELD_START = re.compile(r"^[\s>*_`#]*(?:\*\*|[A-Za-z][A-Za-z -]{0,24}:)")
# 180 days ≈ six months: long enough that a page touched in a normal year of
# work never trips it, short enough that one nobody has looked at since is
# surfaced (M81 implement gate).
_STALE_DAYS = 180


def _iso(text):
    """Every well-formed ISO date in `text`, as date objects. A date-shaped
    run that is not a real date (2026-13-45) is skipped, not raised on."""
    out = []
    for y, m, d in _ISO_DATE.findall(text):
        try:
            out.append(datetime.date(int(y), int(m), int(d)))
        except ValueError:
            continue
    return out


def _extraction_status(block):
    """The `Extraction:` status text of a provenance block, or None when the
    block carries no such field. A label alone on its line takes the next
    paragraph as its body — M78 calls the block "prose in the page's own
    idiom", and `_provenance_block` reads a label-alone layout that same
    generous way, so the sub-field must not be stricter than its block.

    The status is read to the END of its own paragraph, not just the physical
    line it starts on. Reading one line looked like a safe D-023 miss and was
    not (M81 review F2, scored 87): a wrapped status loses whatever sits on
    the continuation, and the fallback is the INGESTED date — which for a
    re-verified page is by definition older than the verification. A page
    re-read 17 days ago was reported 929 days stale, a manufactured false
    positive, exactly what D-023 forbids. Collection stops at a blank line or
    at the next `Label:`/bolded field, so the status never swallows a
    neighbouring field or the citation paragraph below it."""
    lines = block.splitlines()
    for i, line in enumerate(lines):
        m = _PROV_EXTRACTION.match(line)
        if not m:
            continue
        parts, j = [], i + 1
        rest = m.group(1).strip(" *_`")
        if rest:
            parts.append(rest)
        else:
            # Label alone: its body is the next paragraph, whose first line is
            # the status itself and so is taken without the field-start test.
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                parts.append(lines[j].strip())
                j += 1
        while j < len(lines) and lines[j].strip():
            nxt = lines[j].strip()
            if _FIELD_START.match(nxt):
                break
            parts.append(nxt)
            j += 1
        return " ".join(parts)
    return None


def _clauses(status):
    """An extraction status split into its clauses, on em-dash, semicolon or
    comma — the separators every shipped page and both templates use between a
    state claim and its qualifications (`verified at ingestion — full source
    read`, `verified by live probe 2026-07-12; a re-probe would be needed`).

    Clause scope is what keeps negation detection narrow. Three shipped
    `partly verified at ingestion` pages carry `not re-read since` in a later
    clause; a status-wide negation search would read that as negating their
    verification and sweep all three up (the M79-F5 trap)."""
    return [c for c in _CLAUSE_BOUNDARY.split(status) if c.strip()]


def _clause_claims(clause):
    """Every claim one clause makes, as a set of "never" / "partial" /
    "verified".

    A claim is a verification verb plus how it is qualified, and the qualifier
    — a negator or a partiality marker — must sit in this clause BEFORE the
    verb. Reading a fixed list of negative PHRASES instead is what the M83
    review broke twice (F1/92, F2/92): the list covered only the word
    `verified`, so `no claim checked against the source` parsed as an
    affirmative verification.

    Clause scope is what lets partiality be read at all (M89). All three of
    this repo's `partly verified at ingestion` pages carry `not re-read since`
    in a LATER clause; searching the whole status for either qualifier
    collapses the distinction the state exists to draw.

    Negation outranks partiality within one clause: `not partly verified`
    claims no verification, not a qualified one.

    EVERY occurrence is read, not the first: a status hard-wrapped at its
    em-dash is rejoined by `_extraction_status` with the separator gone, so a
    contradiction that was written across two clauses arrives inside one. A
    first-match-wins read answers with whichever claim it happens to meet
    first — the F3 bug, one layer down. The boundary-wrap fixture caught this
    twice, once against each shape of the fix."""
    out = set()
    if _UNVERIFIED.search(clause):
        out.add("never")  # carries its own negator
    for verb in _VERIFY_VERB.finditer(clause):
        if _NEGATOR.search(clause[: verb.start()]):
            out.add("never")
        elif _qualified_partial(clause, verb):
            out.add("partial")
        else:
            out.add("verified")
    return out


def _qualified_partial(clause, verb):
    """Whether a partiality qualifier governs this verb occurrence.

    The qualifier may OVERLAP the verb rather than merely precede it, which is
    why this is not a search of `clause[: verb.start()]` (review F1, scored 95).
    `spot-checked` contains `checked`, and `_VERIFY_VERB` matches
    `checked against` starting inside it — the hyphen satisfies its lookbehind
    — so slicing at `verb.start()` cuts the qualifier in half and leaves
    `spot-`, which matches nothing. `spot-checked against the source` therefore
    read as a full verification, on the exact phrasing both templates teach as
    the partial form.

    So the search runs to `verb.end()` and a match counts when it BEGINS at or
    before the verb does. Beginning-at-or-before is what keeps this from
    widening: a qualifier wholly inside the verb text governs nothing, and no
    match after the verb is considered at all."""
    return any(
        m.start() <= verb.start()
        for m in _PARTIAL.finditer(clause[: verb.end()])
    )


def _status_claims(status):
    """The set of claims a status makes across all its clauses."""
    out = set()
    for clause in _clauses(status):
        out |= _clause_claims(clause)
    return out


def _resolve_claims(claims):
    """The one state a status's claims collapse to, or None when it makes no
    claim at all.

    The lattice runs never > partial > verified — most conservative wins, so
    no qualification anywhere in a status can be cleared by an unqualified
    clause elsewhere. Two rungs, two reasons:

    - `never` beside `partial` is `never`: the four intraclass notes that
      motivated this say both, leading `unverified` and then recording a
      spot-check. Letting partiality win there would UPGRADE a page that
      states plainly it was never checked — the same false-green direction
      one rung down.
    - `partial` beside `verified` is `partial`, not `ambiguous`. "The appendix
      was only partly checked" alongside "verified against the source" is a
      page qualifying itself, not contradicting itself.

    `never` beside `verified` stays `ambiguous` (M83, F3) — that pair IS a
    contradiction, and whichever one is tested first is the bug. Partiality
    does not dissolve it: a status claiming all three is still ambiguous."""
    if "never" in claims and "verified" in claims:
        return "ambiguous"
    for state in ("never", "partial", "verified"):
        if state in claims:
            return state
    return None


def _last_verified(block, today=None):
    """When this page's extraction was last checked against its source, as
    ("ok", date) / ("never", None) / ("partial", None) / ("exempt", None) /
    ("missing", None) / ("undated", None) / ("ambiguous", None) /
    ("unrecognized", None) / ("future", date).

    Precedence (M81 implement gate; restructured at M83; partial added M89):
      1. an explicit "nothing to re-verify" → exempt. Searched over the WHOLE
         status: two shipped pages put the phrase in a trailing clause;
      2. the claims its clauses make, each read as a verification verb plus
         how that verb is qualified in its own clause, collapsed by
         `_resolve_claims` — never > partial > verified, with a `never`/
         `verified` pair still ambiguous rather than a silent pick (M83, F3):
         whichever one is tested first, testing one first is the bug;
      3. `never` → never; `partial` → partial, before any date is read (M89:
         a partial pass is missing coverage, which no date repairs);
         `verified` → the freshest non-future date in the
         status, or the block's ingested date ("verified at ingestion", the
         commonest shipped form, literally names it, and demanding an explicit
         date there would falsely flag five template-sanctioned pages);
      4. no claim at all, but a date → ok on that date. This is how
         `derived — … none re-read since 2026-07-11` and `a 2026-07-12
         snapshot` classify: neither claims verification, both date themselves;
      5. no claim and no date → unrecognized (M83, F4). Before, this fell
         through to the ingested date and read as a confirmed verification, so
         `never verified against the source` classified `ok`.

    `future` (M83, F5) is returned only when EVERY date in the status is later
    than `today`. A future date made the age negative, which no threshold can
    exceed, so the page was exempt forever with nothing said — but a status may
    legitimately carry a forward-looking date beside its verification ("verified
    2026-07-01; next re-check due 2026-12-01"), and taking the max there
    reported a page verified weeks ago as dated in the future (review F4/83)."""
    raw = _extraction_status(block)
    if not raw:
        return "missing", None
    today = today or datetime.date.today()
    status = _OBSERVED_STAMP.sub("", raw)
    if _NOTHING_TO_VERIFY.search(status):
        return "exempt", None

    # Claims are gathered from every clause, not just the leading one: a status
    # hard-wrapped at its em-dash comes back from `_extraction_status` with the
    # lines joined by a space and the separator gone, so a lead-only read sees
    # both claims at once and answers with whichever is tested first — the F3
    # bug in wrapped form. Caught by the boundary-wrap fixture, which is the M81
    # lesson paying off: the midpoint-wrap axis could not reach it.
    claims = _status_claims(status)
    state = _resolve_claims(claims)
    if state == "ambiguous":
        return "ambiguous", None

    if state == "never":
        return "never", None
    if state == "partial":
        # Returned before any date is looked at, because what a partial status
        # is missing is COVERAGE, not freshness: part of the page has never
        # been checked, and no date — not even today's — makes that true. A
        # partial claim must therefore never reach the `ok` return below, which
        # is the only exit that can be cleared by a threshold.
        return "partial", None

    dates = _iso(status)
    past = [d for d in dates if d <= today]
    if past:
        when = max(past)
    elif dates:
        return "future", max(dates)
    else:
        when = None
    if when is None and state == "verified":
        when = _ingested_date(block)
    if when is not None:
        # `when` is already known to be <= today: a future-only status returned
        # above, and the ingested date is historical by construction.
        return "ok", when
    if state is None:
        return "unrecognized", None
    # A status naming no date over a block naming no usable ingested date: the
    # references CHECK FAILs that block, so the advisory stays quiet rather
    # than pile a second finding on one cause. That deference is only honest
    # because both readers now ask `_ingested_date` — before M89 the CHECK
    # tested the regex match alone while this function additionally required
    # the captured text to PARSE, so a block dated `2026-13-45` satisfied the
    # CHECK and arrived here `undated`, and was reported by neither.
    return "undated", None


def check_references_staleness(root, today=None):
    """Advisory: a committed references page whose extraction has never been
    checked against its source, or was last checked longer ago than
    `_STALE_DAYS`. M56 surveyed LLM Wiki's Lint op and adopted it; M57 shipped
    only the INDEX↔disk half, and the "stale claims" clause was lost in
    scoping — this is the remainder.

    WARN, never a CHECK (M81-D1): block *presence* is structural and fails the
    gate, but "this page is too old" is a judgment about evidence quality, and
    D-029 keeps judgment out of the validate gate."""
    out = []
    today = today or datetime.date.today()
    refdir = os.path.join(root, "cairn", "references")
    if not os.path.isdir(refdir):
        return out
    for rel in _reference_pages(refdir):
        block = _provenance_block(os.path.join(refdir, rel), for_extraction=True)
        if block is None:
            continue  # the references CHECK reports a missing block
        state, when = _last_verified(block, today=today)
        if state in ("exempt", "undated"):
            continue
        if state == "never":
            out.append(
                f"cairn/references/{rel}: extraction records no verified "
                f"re-check against the source"
            )
        elif state == "partial":
            # Distinct from the `never` message on purpose (M89): the page is
            # not unchecked, and telling its author it is invites a re-read
            # they already did. What it needs is the remainder checked, or the
            # status rewritten to say the partial pass is all this page will
            # ever claim.
            out.append(
                f"cairn/references/{rel}: extraction records only a partial "
                f"verification — the rest of the page has never been checked "
                f"against the source"
            )
        elif state == "missing":
            out.append(
                f"cairn/references/{rel}: provenance records no extraction status"
            )
        elif state == "ambiguous":
            out.append(
                f"cairn/references/{rel}: extraction status contradicts itself "
                f"— it claims a verification and also says it was never "
                f"verified; say which is current"
            )
        elif state == "unrecognized":
            out.append(
                f"cairn/references/{rel}: extraction status records neither a "
                f"verification nor a date, so nothing says whether this page "
                f"was ever checked against its source"
            )
        elif state == "future":
            out.append(
                f"cairn/references/{rel}: extraction is dated "
                f"{when.isoformat()}, in the future — a page cannot have been "
                f"verified later than today"
            )
        else:
            age = (today - when).days
            if age > _STALE_DAYS:
                out.append(
                    f"cairn/references/{rel}: last verified {when.isoformat()}, "
                    f"{age} days ago (threshold {_STALE_DAYS})"
                )
    return out


def check_worklog_format(root):
    """Advisory: a work-log line that is not a one-line `- ` entry — i.e. a
    hard-wrapped continuation. The rulebook has always mandated one line per
    entry, but nothing enforced it, and D-046 removed the budgetary pressure
    that used to surface violations indirectly: M76's work log measured 58
    lines wrapped versus 21 reflowed, which is what pushed that milestone over
    cap. Now that the section is cap-exempt (M77), this advisory is the only
    thing keeping it honest — so it WARNs rather than FAILs: an unbudgeted
    wrap is untidiness, and a gate failure over formatting would block a
    milestone for no correctness reason. Live files only; archived summaries
    are compressed narratives, not work logs."""
    out = []
    for mid, path in sorted(cs.live_files(root).items(), key=lambda kv: cs.id_num(kv[0])):
        lines = cs.milestone_worklog_lines(path)
        if not lines:
            continue
        in_comment = False
        for lineno, text in lines:
            stripped = text.strip()
            if in_comment:
                if "-->" in stripped:
                    in_comment = False
                continue
            if not stripped or _LOG_ENTRY.match(text):
                continue
            if stripped.startswith("<!--"):
                if "-->" not in stripped:
                    in_comment = True
                continue
            preview = text.strip()
            if len(preview) > _LOG_PREVIEW:
                preview = preview[:_LOG_PREVIEW].rstrip() + "…"
            out.append(
                f"{mid}:{lineno}: work-log line is not a one-line entry "
                f'— "{preview}"'
            )
    return out


# --- release window (M88) ---------------------------------------------------
# A release milestone's readiness is a maintainer judgment about when to ship,
# never a dependency graph going green — so once one exists in a routable
# status every routing surface nominates it forever off (status, priority,
# deps) alone. D-050 parks it as `blocked` instead; this advisory catches the
# drift back, which is what erased circumplex's M21 parking unnoticed.
#
# Detection needs BOTH signals. A release token alone matches milestones about
# release *tooling* (this repo's own "Release-walk slot", "Release positioning",
# "Release docs") — work that is ordinary milestone work and must stay silent.
# Pairing the token with a version pattern discriminates: shipping a version
# names the version.
_RELEASE_TOKEN = re.compile(
    r"\b(?:CRAN|releases?d?|(?:re)?submissions?|(?:re)?submit)\b", re.I
)
# A SHIPPING version, not any decimal. The goal is free prose, so a permissive
# `v?\d+\.\d+` matches "targets R 4.3", "section 2.1", "threshold 0.8" — which
# turns the version half of the pair into no discriminator at all and flips
# release-TOOLING milestones to release-shaped the moment their goal contains an
# ordinary number (M88 review F6). Either a `v` prefix or a full three-part
# version is required. Known and accepted miss: a bare two-part "2.0" with no
# `v`, which is indistinguishable from ordinary prose decimals.
_RELEASE_VERSION = re.compile(r"\bv\d+\.\d+(?:\.\d+)?\b|\b\d+\.\d+\.\d+\b")
# The statuses a routing surface will nominate. `blocked` is deliberately
# absent — it is the parked state this advisory exists to recommend, so a
# parked release is silent, which is the whole point.
_ROUTABLE = ("planned", "in-progress", "review")
_RELEASE_IDLE_DAYS = 14


def _release_shaped(title, goal):
    """True when the text names both a release act and a version. Both are
    required: the token alone over-matches release tooling."""
    text = f"{title}\n{goal}"
    return bool(_RELEASE_TOKEN.search(text) and _RELEASE_VERSION.search(text))


def _last_worklog_date(path):
    """The newest ISO date appearing on a `- ` work-log entry, or None when the
    log carries no dated entry. Entry lines only — a wrapped continuation is
    the `work-log format` advisory's business, not this one."""
    lines = cs.milestone_worklog_lines(path)
    if not lines:
        return None
    seen = []
    for _lineno, text in lines:
        if not _LOG_ENTRY.match(text):
            continue
        seen.extend(_iso(text))  # one owner for the date-tolerance rule (F4)
    return max(seen) if seen else None


def check_release_window(root, rows, today=None):
    """Advisory: a release-shaped milestone that a routing surface is
    nominating — the nag D-050 exists to stop.

    The trigger is status-dependent because idleness means different things at
    different statuses, and the naive "no work log in N days" rule gets the
    worst case exactly backwards. A `planned` release has never been worked, so
    its work log records only *queueing* — intraclass M48 sat planned for a
    week with all eight dependencies satisfied while every one of its entries
    was a Depends-on amendment saying another milestone had been slotted ahead
    of it, and each one refreshed the idle clock. So a `planned` release warns
    the moment its dependencies are satisfied, which is the moment
    `cairn_next` starts naming it. Work that has genuinely started is judged on
    idleness instead: `in-progress`/`review` warn only after
    `_RELEASE_IDLE_DAYS`, so a maintainer actively shipping a release is never
    warned at. A standing WARN on every routable release would itself be the
    nag fatigue D-017 rejected.

    WARN, never a CHECK: whether a window is open is the maintainer's call, and
    D-029 keeps judgment out of the validate gate."""
    out = []
    today = today or datetime.date.today()
    live = cs.live_files(root)
    # Dependency satisfaction mirrors cairn_next: a done row, or a done
    # milestone whose row was pruned under terminal-row retention but whose
    # archive file remains.
    done = {r["id"] for r in rows if r["status"] == "done"} | set(cs.archive_files(root))
    for row in sorted(rows, key=lambda r: cs.id_num(r["id"])):
        if row["status"] not in _ROUTABLE:
            continue
        path = live.get(row["id"])
        if path is None:
            continue  # roadmap<->disk orphans are a CHECK's business
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        goal = "\n".join(_section_body(text, "Goal"))
        if not _release_shaped(row["title"], goal):
            continue
        tail = (
            "park it as `blocked` (D-050) or declare the release window"
        )
        if row["status"] == "planned":
            if all(dep in done for dep in row["depends"]):
                out.append(
                    f"{row['id']}: release milestone is planned with every "
                    f"dependency satisfied, so it is being nominated as the "
                    f"next action — {tail}"
                )
            continue
        when = _last_worklog_date(path)
        if when is None:
            out.append(
                f"{row['id']}: release milestone in status '{row['status']}' "
                f"with no dated work-log entry — {tail}"
            )
            continue
        idle = (today - when).days
        if idle > _RELEASE_IDLE_DAYS:
            out.append(
                f"{row['id']}: release milestone in status '{row['status']}' "
                f"idle {idle} days since {when.isoformat()} (threshold "
                f"{_RELEASE_IDLE_DAYS}) — {tail}"
            )
    return out


# ID-token shapes (M57): zero-padded milestone/decision IDs as written in
# tracking prose. Unpadded forms (M7) don't occur in cairn's ID format.
_M_TOKEN = re.compile(r"\bM(\d{2,})\b")
_D_TOKEN = re.compile(r"\bD-(\d{3,})\b")
# An owner/repo-shaped slug — the cross-repo qualifier signal. Deliberately
# loose (also matches file paths): an unresolved token sharing a line with
# any slug is skipped, a preferred miss under the D-023 doctrine.
_REPO_SLUG = re.compile(r"\b[\w.-]+/[\w.-]+\b")
_D_HEADER = re.compile(r"^### (D-\d{3,})", re.MULTILINE)


def _known_ids(root, rows):
    """The resolvable ID universe: ROADMAP rows ∪ live/archive milestone
    files (M), and DECISIONS.md entry headers (D)."""
    m_ids = (
        {r["id"] for r in rows}
        | set(cs.live_files(root))
        | set(cs.archive_files(root))
    )
    d_ids = set()
    dpath = os.path.join(root, "cairn", "DECISIONS.md")
    if os.path.isfile(dpath):
        with open(dpath, encoding="utf-8") as f:
            d_ids = set(_D_HEADER.findall(f.read()))
    return m_ids, d_ids


# The bounded DECISIONS read (D-054) picks what to open from headings alone,
# so a heading hiding a supersession costs recall. Scoped from D-054 because
# D-012/D-014/D-019 hide one and IP4 forbids repairing them — an advisory that
# can never reach OK is one people learn to ignore.
HEADING_QUALITY_FROM = 54

_DQ_HEADING = re.compile(r"^### D-0*(\d+)\b.*$", re.M)
# A relationship CLAIM: the verb stem, then a D-id inside the same sentence.
# Excludes the shapes that produced false positives on the real file — a bare
# citation ("(D-005)"), "a symmetric move to D-028", "leaves D-049 untouched"
# (no verb), and the forward-looking "the entry to supersede" / "requires a
# superseding D-entry" (verb, but no D-id follows it in that sentence).
_DQ_CLAIM = re.compile(r"\b(supersed|annotat|narrow|refin)\w*\b([^.\n]*)", re.I)
_DQ_ID = re.compile(r"\bD-0*(\d+)\b")


def check_decision_heading_quality(root):
    """Advisory: a `### D-` heading that does not name an entry its own body
    claims to supersede, annotate, narrow, or refine (M97, D-054).

    The bounded read decides what to open from the headings, so the heading is
    the index and a hidden supersession is a recall hole. Scoped to entries
    from `HEADING_QUALITY_FROM` on: three legacy headings hide one and IP4
    forbids editing them, so the read protocol back-references by id to cover
    those instead (D-054 mitigation 2).

    WARN, never a CHECK: whether a heading "names its subject" is a judgment
    about prose, the same call `record density` and `references staleness`
    make (D-049/D-052). Findings name the offending entry and the omitted id,
    since a count cannot be acted on.

    KNOWN RECALL LIMITS (M97 review F1-F4, F6 — do not read a clean result as
    "every in-scope heading is complete"). The claim matcher is deliberately
    narrow, per D-023's "a missed weird format beats a false positive": it
    misses the noun form ("this supersession of D-031"), claims split across a
    line wrap (the window stops at the newline and this repo hard-wraps),
    reversed order ("D-031 is superseded here"), synonyms outside the rule's
    stated vocabulary ("replaces", "overrides", "retires"), and it does not
    exclude fenced or quoted content in either direction. These interact — the
    noun-form miss is safe to close ONLY while the wrap limit suppresses the
    false positive it would otherwise raise on D-054's own descriptive
    "headings hide a supersession" line — so they want a classifier redesign,
    not independent patches (ROADMAP candidate). Recall for the legacy and
    missed cases rests on the back-reference step of the read protocol, which
    does not depend on this matcher at all."""
    out = []
    path = os.path.join(root, "cairn", "DECISIONS.md")
    if not os.path.isfile(path):
        return out
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return out
    heads = list(_DQ_HEADING.finditer(text))
    for i, m in enumerate(heads):
        num = int(m.group(1))
        if num < HEADING_QUALITY_FROM:
            continue
        heading = m.group(0)
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end():end]
        named = {int(n) for n in _DQ_ID.findall(heading)}
        claimed = set()
        for c in _DQ_CLAIM.finditer(body):
            claimed |= {int(n) for n in _DQ_ID.findall(c.group(2))}
        missing = sorted(claimed - named - {num})
        if missing:
            ids = ", ".join("D-%03d" % n for n in missing)
            out.append(
                "D-%03d: body claims a relationship to %s but the heading "
                "does not name it — the bounded read (D-054) opens entries "
                "by heading, so this is invisible to the scan" % (num, ids)
            )
    return out


def check_dangling_ids(root, rows):
    """Advisory: M<NN>/D-<NNN> tokens in committed cairn/ markdown that
    resolve to no ROADMAP row, milestone file, or D-entry (M57 — the link
    syntax is bare ID tokens, so a dangler is a broken wiki link). Two
    tolerance rules, per D-023 (a missed weird format beats a false
    positive): tokens numerically above the max assigned ID are skipped
    (example/forward prose — the M99 class), and unresolved tokens on a line
    carrying an owner/repo slug are skipped (repo-qualified cross-repo
    cites — the "ackwards M57" class). legacy/ is excluded (entombed
    verbatim, D-005). WARN tier: feeds ADVISORIES, never fails the gate."""
    out = []
    m_ids, d_ids = _known_ids(root, rows)
    m_max = max((cs.id_num(i) for i in m_ids), default=0)
    d_max = max((int(i.split("-")[1]) for i in d_ids), default=0)
    for dirpath, dirs, names in os.walk(os.path.join(root, "cairn")):
        dirs[:] = [d for d in dirs if d != "legacy"]
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            try:
                with open(path, encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception:
                continue
            for lineno, line in enumerate(lines, 1):
                hits = [
                    "M" + m.group(1)
                    for m in _M_TOKEN.finditer(line)
                    if "M" + m.group(1) not in m_ids
                    and int(m.group(1)) <= m_max
                ]
                hits += [
                    m.group(0)
                    for m in _D_TOKEN.finditer(line)
                    if m.group(0) not in d_ids and int(m.group(1)) <= d_max
                ]
                if not hits or _REPO_SLUG.search(line):
                    continue
                out.extend(
                    f"{rel}:{lineno}: {tok} resolves to no ROADMAP row, "
                    f"milestone file, or D-entry"
                    for tok in hits
                )
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
    # First among the advisories (M84). `run()` prints every CHECK before any
    # advisory, so this is NOT adjacent to the `weight caps` CHECK it is the
    # second axis of — the two measures cover the same files, one structural
    # and failing, one a judgment call and not, and the rulebook's weight-caps
    # section is what pairs them for a reader.
    ("record density", lambda root, rows: check_record_density(root)),
    ("sizing (split tripwires)", lambda root, rows: check_sizing_advisory(root)),
    (
        "scaffold deprecations",
        lambda root, rows: check_gitignore_deprecations(root),
    ),
    ("work-log format", lambda root, rows: check_worklog_format(root)),
    ("dangling id tokens", lambda root, rows: check_dangling_ids(root, rows)),
    (
        "decision heading quality",
        lambda root, rows: check_decision_heading_quality(root),
    ),
    (
        "references staleness",
        lambda root, rows: check_references_staleness(root),
    ),
    ("release window", lambda root, rows: check_release_window(root, rows)),
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
