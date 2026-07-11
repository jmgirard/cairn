#!/usr/bin/env python3
"""Stop hook: block ending a turn with uncommitted cairn/ tracking.

Enforces "stop points are commit points" for the tracking files only —
code elsewhere in the tree is the skills' business, but tracking that
diverges from disk breaks stateless resume. Honors stop_hook_active to
avoid infinite block loops. No-op outside cairn repos.
"""

import sys

import cairn_common as cc


def main():
    data = cc.read_input()
    if data.get("stop_hook_active"):
        return
    root = cc.find_cairn_root(data.get("cwd"))
    if not root:
        return
    rc, out = cc.git(["status", "--porcelain", "--", "cairn/"], root)
    if rc != 0:
        return
    dirty = [line for line in out.splitlines() if line.strip()]
    if not dirty:
        return
    files = ", ".join(line[3:].strip() for line in dirty[:10])
    cc.emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "decision": "block",
                "reason": (
                    "Uncommitted cairn tracking changes: "
                    f"{files}. Stop points are commit points — commit the "
                    "tracking update (work-log line + checkboxes) together "
                    "with the work before ending the turn. If stopping "
                    "half-done is intended, commit an honest checkpoint "
                    "marked as such."
                ),
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
