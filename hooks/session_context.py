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
"""

import os
import re
import sys

import cairn_common as cc

_PROFILE_HEADER = re.compile(r"#\s*Toolchain profile:\s*(\S+)")

MAX_CHARS = 30000

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
    for mid, status, relpath in cc.parse_roadmap_rows(roadmap):
        if status not in cc.ACTIVE_STATUSES:
            continue
        path = os.path.join(cairn_dir, relpath)
        try:
            with open(path, encoding="utf-8") as f:
                body = f.read()
        except Exception:
            body = f"(listed in ROADMAP as {status}, but cairn/{relpath} could not be read)"
        parts.append(f"## cairn/{relpath} ({mid}, {status})\n\n" + body)
    return "\n\n".join(parts)[:MAX_CHARS]


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
