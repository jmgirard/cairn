#!/usr/bin/env python3
"""Stop hook: block ending a turn with uncommitted cairn/ tracking.

Enforces "stop points are commit points" for the tracking files only —
code elsewhere in the tree is the skills' business, but tracking that
diverges from disk breaks stateless resume. Honors stop_hook_active to
avoid infinite block loops. No-op outside cairn repos.
"""

import os
import sys

import cairn_common as cc

# The merge-approval marker (and its consumed-but-unresolved .pending
# state, M60) is intentionally ephemeral and single-use; both are
# gitignored in cairn-scaffolded repos, but never depend on that — a repo
# that adopted the marker workflow without re-running /cairn-init would
# have them un-ignored, and blocking turn-end on them would tempt the
# user to commit the very thing that must stay uncommitted. Exclude them
# regardless of .gitignore state.
MARKER_BASENAMES = (".merge-approved", ".merge-approved.pending")


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
    dirty = [
        line
        for line in out.splitlines()
        if line.strip()
        and os.path.basename(line[3:].strip()) not in MARKER_BASENAMES
    ]
    if not dirty:
        return
    files = ", ".join(line[3:].strip() for line in dirty[:10])
    # Stop/SubagentStop blocking uses TOP-LEVEL decision/reason — NOT nested
    # under hookSpecificOutput (that key carries additionalContext only, and
    # a nested decision is silently ignored). Verified against the official
    # hooks docs; see references/claude-code-hooks.md.
    cc.emit(
        {
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
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
