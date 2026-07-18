#!/usr/bin/env python3
"""PreToolUse hook: nudge out-of-band idea capture toward a candidate row.

A background-task chip is a useful affordance — it spins an idea into its
own session — but it is not a tracking file, so an idea captured only there
is invisible to every cairn skill that reads `cairn/` at plan time (D-042).
When such a chip is created while working in a cairn repo, this hook injects
the softest reminder the PreToolUse contract allows: a non-blocking
`additionalContext` nudge and NO permissionDecision, so the chip is created
through the normal permission flow untouched and Claude simply reads the
reminder on its next turn. The chip is paired with a ROADMAP candidate row,
never forbidden.

Silent no-op otherwise (non-chip tool, non-cairn cwd, malformed input) —
fail-permissive like the other cairn hooks.
"""

import os
import re
import sys

import cairn_common as cc

# The chip-creating tool, as an MCP tool name (`mcp__<server>__<tool>`).
# Matched on the tool suffix rather than the full name so a server rename
# does not silently unwire the guard — the hooks.json matcher
# (`mcp__.*__spawn_task`) is the same shape.
CHIP_TOOL = re.compile(r"^mcp__.+__spawn_task$")


def is_chip_tool(tool_name):
    """True when tool_name creates a background-task chip."""
    if not tool_name:
        return False
    return bool(CHIP_TOOL.match(tool_name))


REMINDER = (
    "cairn intake check (D-042): you're surfacing an idea as a background-task "
    "chip while working in a cairn repo. A chip is not a tracking file, so an "
    "idea captured only there is invisible to every cairn skill that reads "
    "cairn/ at plan time. Pair it: add the same idea as a `candidate` row in "
    "cairn/ROADMAP.md this turn (sweeping existing candidates, "
    "milestones/archive/, and DECISIONS.md for overlap first — search-first "
    "candidate creation), and treat the chip as a pointer to that row. The "
    "chip itself is fine; being the only record of the idea is not "
    "(tracking-rules: 'Out-of-band idea capture')."
)


def main():
    data = cc.read_input()
    if not is_chip_tool(data.get("tool_name")):
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
