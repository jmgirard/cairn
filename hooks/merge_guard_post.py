#!/usr/bin/env python3
"""PostToolUse/PostToolUseFailure(Bash) hook: resolve the merge-approval
marker's pending state by outcome.

merge_guard.py (PreToolUse) consumes cairn/.merge-approved by renaming it
to cairn/.merge-approved.pending when it lets a guarded merge through.
This companion resolves that attempt (M60, RR01 rec 13): on
PostToolUseFailure — for Bash, the documented event when the command
exits nonzero (references/claude-code-hooks.md) — it renames the pending
file back, restoring the approval a *failed* attempt consumed (ends the
M33 rewrite-the-marker manual step); on PostToolUse (success) it deletes
the pending file, keeping the marker single-use. It can never mint
approval: it only renames back a pending file that a real approval
created and a real merge attempt consumed — with no pending file both
paths are strict no-ops. A PreToolUse-denied call fires neither event,
so a deny never reaches this hook.

Known, accepted limitations: a compound command whose guarded merge
succeeds but whose trailing step fails (`gh pr merge 7 && git pull`)
fires PostToolUseFailure and restores a marker the merge did spend —
the skills run merges as standalone commands, and the restored marker
still only survives until the next guarded attempt. Stale pending files
(a session dying mid-attempt) are overwritten by the next consumption,
ignored by stop_guard, and gitignored in scaffolded repos. No-op outside
cairn repos; fail-permissive.
"""

import os
import sys

import cairn_common as cc


def main():
    data = cc.read_input()
    event = data.get("hook_event_name")
    if event not in ("PostToolUse", "PostToolUseFailure"):
        return
    if data.get("tool_name") != "Bash":
        return
    command = (data.get("tool_input") or {}).get("command") or ""
    if not command:
        return
    cwd = data.get("cwd") or os.getcwd()
    root = cc.find_cairn_root(cwd)
    if not root:
        return
    if not cc.is_guarded_merge(command, cwd):
        return
    pending = os.path.join(root, cc.PENDING_RELPATH)
    if not os.path.isfile(pending):
        return
    try:
        if event == "PostToolUseFailure":
            os.replace(pending, os.path.join(root, cc.MARKER_RELPATH))
            cc.emit(
                {
                    "hookSpecificOutput": {
                        "hookEventName": event,
                        "additionalContext": (
                            "cairn merge-guard: the failed merge attempt's "
                            "consumed approval marker was restored "
                            "(cairn/.merge-approved) — the user's approval "
                            "still stands for one retry; fix the failure "
                            "and rerun the merge without re-asking."
                        ),
                    }
                }
            )
        else:
            os.remove(pending)  # success: the approval is spent for good
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)
