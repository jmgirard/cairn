#!/usr/bin/env python3
"""SessionStart hook: print the status script's listing for this repo.

The listing holds the home-folder path, the work in flight with its phase
and what blocks it, the `[high]` and `[blocked]` candidate rows, the
candidate count, any file the script could not read, and the path of the
current branch's plan. In a repo that still has cairn v2 files, the hook
says so and points to `/cairn setup`.

It injects no ROADMAP text and no plan body, and it makes no network call.
Outside a cairn repo it prints nothing. It never fails the session: any
error ends in exit 0 with no output.
"""

import json
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
)

LEAD = "cairn status for this repo, from the session-start hook:\n\n"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    import cairn_status

    text = cairn_status.render(cairn_status.resolve(data.get("cwd") or os.getcwd()))
    if not text:
        return
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": data.get("hook_event_name") or "SessionStart",
                "additionalContext": LEAD + text,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
