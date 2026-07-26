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

# Exactly the sections the 150-line cap exempts (tracking-rules "Weight
# caps"). Matched by equality, never prefix: `## Reviewers` must not read as
# `## Review` (the boundary bug M55 hit).
CAP_EXEMPT_SECTIONS = ("## Work log", "## Review")

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


def split_sections(body):
    """[(heading, lines)] in file order; the first pair's heading is None
    (everything above the first `## `)."""
    out, heading, buf = [], None, []
    for line in body.splitlines():
        if line.startswith("## "):
            out.append((heading, buf))
            heading, buf = line, []
        else:
            buf.append(line)
    out.append((heading, buf))
    return out


def _blocks(lines):
    """(preamble, blocks, unit) — the elidable units of a section body.

    A section holding `- ` entries blocks by entry, so a hard-wrapped entry
    keeps its continuation lines with it (the one-line-per-entry mandate is
    an advisory, not a guarantee — D-046). Anything else blocks by line.
    Lines above the first entry are the section's own preamble (an HTML
    ownership comment, a blank) and never elide.
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
    """(kept_lines, kept, total, unit) — the section's NEWEST blocks that fit
    in `budget`, never fewer than MIN_TAIL_BLOCKS."""
    head, blocks, unit = _blocks(lines)
    kept, size = [], 0
    for block in reversed(blocks):
        cost = sum(len(line) + 1 for line in block)
        if size + cost > budget and len(kept) >= MIN_TAIL_BLOCKS:
            break
        kept.append(block)
        size += cost
    kept.reverse()
    return (
        head + [line for block in kept for line in block],
        len(kept),
        len(blocks),
        unit,
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
        if heading.strip() in CAP_EXEMPT_SECTIONS:
            kept_lines, kept, total, unit = bounded_tail(section, budget)
            if kept < total:
                lines.append("")
                lines.append(
                    f"_cairn: newest {kept} of {total} {unit} shown — read "
                    f"cairn/{relpath} for the rest._"
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
            if heading is not None and heading.strip() in CAP_EXEMPT_SECTIONS
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

    context = "\n\n".join(parts)
    if len(context) > MAX_CHARS:
        notice = (
            f"\n\n_cairn: injection truncated at the {MAX_CHARS}-character "
            "budget._"
        )
        context = context[: MAX_CHARS - len(notice)] + notice
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
