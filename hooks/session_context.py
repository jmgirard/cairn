#!/usr/bin/env python3
"""SessionStart hook: inject cairn tracking context.

Injects cairn/ROADMAP.md plus every active (in-progress / blocked /
review) milestone file as additionalContext, so a fresh session starts
oriented without relying on the skill remembering to read the files.
No-op outside cairn repos.

Wired to SessionStart only. Claude Code honors additionalContext on
`source` startup/resume and ignores it on clear/compact — there is no
hook that re-injects context on compaction (PreCompact is block-only),
so we don't pretend to. Emitting on an ignored source is harmless.
The event field is read generically so the script stays event-agnostic.

The read-bound (M113 / D-063). A milestone file is an always-read surface,
and two of its sections — `## Work log` and `## Review` — are exempt from
the 150-line cap (D-046, M55), so nothing bounds their growth. IP4/D-045
forbid trimming them on disk: they are history. The injection therefore
reads less of them instead, taking each cap-exempt section's NEWEST content
within a budget and saying what it left out. Newest matters: this replaces
a flat `[:MAX_CHARS]` tail chop that cut the newest work-log entries first,
so a resuming session was told what a milestone finished days ago and never
what it was blocked on. Sections the cap governs are injected whole — the
cap is already their bound.
"""

import os
import re
import sys

import cairn_common as cc

_PROFILE_HEADER = re.compile(r"#\s*Toolchain profile:\s*(\S+)")

MAX_CHARS = 30000

# Per cap-exempt section, per milestone. 6,000 clears the measured p90 of
# both section types (work log 3,740, review 5,866, over the 111 milestone
# files this repo has had live, measured 2026-07-25), so ≥90% of each type
# injects whole and only outliers meet the bound.
SECTION_MAX_CHARS = 6000

# The newest N entries survive however tight the budget: a milestone that
# shows nothing of its recent state is worse than one that shows a little.
MIN_TAIL_BLOCKS = 3

# The sections the 150-line cap exempts (tracking-rules "Weight caps"),
# normalized the way the cap's own counters normalize them
# (`scripts/cairn_scripts.py`: `line[3:].strip().lower()`, fence-aware).
# That file shares its heading rules with the wrapped-entry advisory ON
# PURPOSE — "or the exemption would open a hole the advisory never looks at"
# — and the same reasoning binds here: a heading the cap exempts but this
# hook does not recognize is injected whole, which is the gap the read-bound
# exists to close. Matched by equality, never prefix: `## Reviewers` must not
# read as `## Review` (the boundary bug M55 hit).
CAP_EXEMPT_SECTIONS = ("work log", "review")

# Injection order, so that shedding from the end sheds the least-current
# milestone first when the total budget binds.
STATUS_ORDER = {"in-progress": 0, "review": 1, "blocked": 2}

PREAMBLE = (
    "# cairn tracking context (auto-injected by the cairn plugin)\n\n"
    "This repo is cairn-tracked. The files below are authoritative for\n"
    "project status (ROADMAP) and current work (active milestones); they\n"
    "are re-read from disk at injection time. Obey the repo's CLAUDE.md\n"
    "cairn section; start milestone work via the cairn skills.\n"
)


def profile_name(root):
    """Active toolchain profile name from cairn/PROFILE.md's
    `# Toolchain profile: <name>` header, or None when the file is absent or
    headerless. A repo that predates profiles has no PROFILE.md — the skills
    infer from DESCRIPTION at point of use, so the hook stays silent (no-op)
    rather than guessing here."""
    path = os.path.join(root, "cairn", "PROFILE.md")
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = _PROFILE_HEADER.match(line)
                if m:
                    return m.group(1)
    except Exception:
        return None
    return None


def heading_name(line):
    """A `## ` heading's normalized name, or None. Same normalization the cap
    counters use, so the two agree on what a cap-exempt section is."""
    return line[3:].strip().lower() if line.startswith("## ") else None


def split_sections(body):
    """[(heading, lines)] in file order; the first pair's heading is None
    (everything above the first `## `). Fenced ``` / ~~~ blocks are tracked,
    so a `## ` quoted inside one is content and not a section boundary
    (M45) — otherwise a milestone quoting the template would gain a phantom
    cap-exempt section and get a marker injected into its code fence."""
    out, heading, buf, fence = [], None, [], None
    for line in body.splitlines():
        stripped = line.lstrip()
        if fence is not None:
            buf.append(line)
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = stripped[:3]
            buf.append(line)
            continue
        if heading_name(line) is not None:
            out.append((heading, buf))
            heading, buf = line, []
        else:
            buf.append(line)
    out.append((heading, buf))
    return out


def _blocks(lines):
    """(head, blocks, unit) — the elidable units of a section body.

    A section holding `- ` entries blocks by entry, so a hard-wrapped entry
    keeps its continuation lines with it (the one-line-per-entry mandate is
    an advisory, not a guarantee — D-046). Anything else blocks by line.
    `head` is whatever sits above the first entry — an ownership comment, a
    stamp, or a whole section of prose in a free-form `## Review`.
    """
    if any(line.startswith("- ") for line in lines):
        head, blocks = [], []
        for line in lines:
            if line.startswith("- "):
                blocks.append([line])
            elif blocks:
                blocks[-1].append(line)
            else:
                head.append(line)
        return head, blocks, "entries"
    return [], [[line] for line in lines], "lines"


def bounded_tail(lines, budget):
    """(kept_lines, kept, total, unit, dropped_head) — the section's NEWEST
    content within `budget`.

    Entries are taken newest-first, never fewer than MIN_TAIL_BLOCKS of them
    whatever the budget. The head is then kept only if it still fits, and
    `dropped_head` says whether it didn't: an unconditionally-kept head is
    charged to nothing and reported as nothing, so a `## Review` of prose
    closed by one bullet used to inject whole and claim nothing was elided
    (review round 1, F1). Trimming the head rather than the entries keeps the
    newest-wins guarantee intact — a budget tight enough to bite must never
    leave a section showing its preamble and none of its entries.
    """
    head, blocks, unit = _blocks(lines)
    kept, size = [], 0
    for block in reversed(blocks):
        cost = sum(len(line) + 1 for line in block)
        if size + cost > budget and len(kept) >= MIN_TAIL_BLOCKS:
            break
        kept.append(block)
        size += cost
    kept.reverse()
    head_fits = size + sum(len(line) + 1 for line in head) <= budget
    return (
        (head if head_fits else []) + [ln for block in kept for ln in block],
        len(kept),
        len(blocks),
        unit,
        any(line.strip() for line in head) and not head_fits,
    )


def milestone_part(mid, status, relpath, body, budget):
    """One milestone's injection: capped sections whole, cap-exempt sections
    bounded to their newest content with a marker naming the rest."""
    lines = []
    for heading, section in split_sections(body):
        if heading is None:
            lines.extend(section)
            continue
        lines.append(heading)
        if heading_name(heading) in CAP_EXEMPT_SECTIONS:
            kept_lines, kept, total, unit, cut_head = bounded_tail(
                section, budget
            )
            if kept < total or cut_head:
                what = (
                    f"newest {kept} of {total} {unit} shown"
                    if kept < total
                    else "prose above the first entry elided"
                )
                lines.append("")
                lines.append(
                    f"_cairn: {what} — read cairn/{relpath} for the rest._"
                )
            lines.extend(kept_lines)
        else:
            lines.extend(section)
    return part_header(mid, status, relpath) + "\n".join(lines)


def part_header(mid, status, relpath):
    return f"## cairn/{relpath} ({mid}, {status})\n\n"


def elided_part(mid, status, relpath):
    """A milestone the total budget cannot carry. It keeps its header and its
    path — AC4: no active milestone disappears without saying so."""
    return part_header(mid, status, relpath) + (
        f"_cairn: body elided for the injection budget — "
        f"read cairn/{relpath}._"
    )


def build_context(root):
    cairn_dir = os.path.join(root, "cairn")
    parts = [PREAMBLE]
    name = profile_name(root)
    if name:
        parts.append(
            "## Active toolchain profile\n\n"
            f"`{name}` (from cairn/PROFILE.md) — the operational skills read its "
            "slots for language-specific commands (tracking-rules "
            '"Toolchain profiles").'
        )
    try:
        with open(os.path.join(cairn_dir, "ROADMAP.md"), encoding="utf-8") as f:
            roadmap = f.read()
    except Exception:
        return None
    roadmap_at = len(parts)
    parts.append("## cairn/ROADMAP.md\n\n" + roadmap)

    actives = [
        (mid, status, relpath)
        for mid, status, relpath in cc.parse_roadmap_rows(roadmap)
        if status in cc.ACTIVE_STATUSES
    ]
    # Stable, so same-status milestones keep their ROADMAP order.
    actives.sort(key=lambda row: STATUS_ORDER.get(row[1], len(STATUS_ORDER)))

    bodies, exempt_sections = {}, 0
    for mid, status, relpath in actives:
        try:
            with open(os.path.join(cairn_dir, relpath), encoding="utf-8") as f:
                body = f.read()
        except Exception:
            body = f"(listed in ROADMAP as {status}, but cairn/{relpath} could not be read)"
        bodies[relpath] = body
        exempt_sections += sum(
            1
            for heading, _ in split_sections(body)
            if heading is not None
            and heading_name(heading) in CAP_EXEMPT_SECTIONS
        )

    # What the injection costs with every cap-exempt section at its floor;
    # whatever the total budget has left over is shared among them.
    floor = sum(
        len(milestone_part(m, s, r, bodies[r], 0)) + 2 for m, s, r in actives
    )
    spare = MAX_CHARS - len("\n\n".join(parts)) - floor
    budget = (
        min(SECTION_MAX_CHARS, max(0, spare // exempt_sections))
        if exempt_sections
        else 0
    )
    parts += [
        milestone_part(m, s, r, bodies[r], budget) for m, s, r in actives
    ]

    # Still over: shed whole milestone bodies from the end (least-current
    # first), each leaving its header and path behind.
    first = len(parts) - len(actives)
    for i in range(len(actives) - 1, -1, -1):
        if len("\n\n".join(parts)) <= MAX_CHARS:
            break
        parts[first + i] = elided_part(*actives[i])

    # Still over with every milestone already shed to a pointer: the ROADMAP
    # is what is left to cut, so cut IT rather than tail-slicing the joined
    # context — the milestone parts sit at the end, so a tail slice took every
    # header and path with it and left a resuming session unable to name what
    # is in flight (review round 1, F2). The ROADMAP's own cap counts lines
    # and leaves line LENGTH uncapped (D-052), so it can reach this alone.
    over = len("\n\n".join(parts)) - MAX_CHARS
    if over > 0:
        lines = parts[roadmap_at].splitlines()
        total = len(roadmap.splitlines())
        notice = (
            "_cairn: ROADMAP truncated at {} of {} lines — read "
            "cairn/ROADMAP.md for the rest._"
        )
        # Reserve the notice at its WIDEST — formatted with the real numbers,
        # not with zero-width placeholders, or the rewritten part overshoots
        # its allowance by the digits it forgot to reserve and re-triggers the
        # whole-context slice this exists to avoid (review round 2).
        room = len(parts[roadmap_at]) - over - len(notice.format(total, total)) - 2
        kept, size = [], 0
        for line in lines:
            size += len(line) + 1
            if size > room:
                break
            kept.append(line)
        # `lines[0]` is `## cairn/ROADMAP.md` itself: a negative `room` would
        # otherwise drop the heading naming the file being truncated.
        parts[roadmap_at] = "\n".join(
            (kept or lines[:1]) + ["", notice.format(max(0, len(kept) - 2), total)]
        )

    context = "\n\n".join(parts)
    if len(context) > MAX_CHARS:
        notice = (
            f"\n\n_cairn: injection truncated at the {MAX_CHARS}-character "
            "budget._"
        )
        context = context[: max(0, MAX_CHARS - len(notice))] + notice
    return context


def main():
    data = cc.read_input()
    root = cc.find_cairn_root(data.get("cwd"))
    if not root:
        return
    context = build_context(root)
    if not context:
        return
    event = data.get("hook_event_name") or "SessionStart"
    cc.emit(
        {
            "hookSpecificOutput": {
                "hookEventName": event,
                "additionalContext": context,
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
