#!/usr/bin/env python3
"""PreToolUse(Write) hook: nudge the memory->cairn/-files boundary (GP4).

Durable project knowledge belongs in cairn/ files and generalizable
conduct/plugin fixes belong in the plugin; per-user memory holds only
meta-context (GP4, D-011). When Claude writes to a per-user memory dir
while working in a cairn repo, this hook injects the softest reminder the
PreToolUse contract allows: a non-blocking `additionalContext` nudge and
NO permissionDecision, so the Write proceeds through the normal
permission flow untouched and Claude simply reads the reminder on its
next turn. No dialog, no auto-approve override.

Silent no-op otherwise (non-Write tool, non-memory path, non-cairn cwd,
malformed input) — fail-permissive like the other cairn hooks.
"""

import os
import re
import sys

import cairn_common as cc

# A per-user memory dir: .claude/projects/<slug>/memory/ with a file under
# it (the trailing segment is the file being written). Matches anywhere in
# an absolute or relative path.
MEMORY_DIR = re.compile(r"(?:^|/)\.claude/projects/[^/]+/memory/.")


def is_memory_write(file_path):
    """True when file_path targets a file under a per-user memory dir."""
    if not file_path:
        return False
    return bool(MEMORY_DIR.search(file_path.replace("\\", "/")))


REMINDER = (
    "cairn boundary check (GP4): you're writing to per-user memory while "
    "working in a cairn repo. Memory holds only per-user meta-context and "
    "must not hold project state. Durable project knowledge (decisions, "
    "conventions, architecture, status) belongs in cairn/ files; a "
    "generalizable conduct or plugin fix belongs in the plugin "
    "(skills / tracking-rules), not memory. If this write is genuinely "
    "per-user meta-context, proceed; otherwise redirect it to its durable "
    "home (tracking-rules: 'Tracking files outrank memory')."
)


def main():
    data = cc.read_input()
    if data.get("tool_name") != "Write":
        return
    file_path = (data.get("tool_input") or {}).get("file_path") or ""
    if not is_memory_write(file_path):
        return
    cwd = data.get("cwd") or os.getcwd()
    if not cc.find_cairn_root(cwd):
        return
    cc.emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": REMINDER,
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
