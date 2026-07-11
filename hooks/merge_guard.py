#!/usr/bin/env python3
"""PreToolUse(Bash) hook: deny merges to main without recorded approval.

Nothing reaches main without the user's explicit approval at the review
gate. /milestone-review (or /hotfix) records that approval by writing a
single-use marker file, cairn/.merge-approved (gitignored); this hook
denies `gh pr merge` and `git merge`-into-main when the marker is
absent, and consumes it when present. No-op outside cairn repos.

Known limitations (documented, accepted): this is defense-in-depth behind
the skill approval-gate + single-use marker, not an airtight sandbox, so
the `git merge` detection is deliberately conservative rather than
exhaustive. Known `git merge` bypasses: a compound `git checkout main &&
git merge X` sees the pre-checkout branch; backtick command substitution
isn't a command-position separator; `git -C <path> merge` merges in a repo
the in-cwd branch check doesn't inspect. The covered, enforced path is the
`gh pr merge` squash-merge convention, which the guard always catches.
"""

import os
import re
import sys

import cairn_common as cc

MARKER_RELPATH = os.path.join("cairn", ".merge-approved")

# Command position only: start of string or right after a shell separator
# (;, &, |, ( , newline) — a plain space before "git" means it's an
# argument to something else (e.g. `echo git merge`), not a command.
CMD_POS = r"(?:^|[;&|(\n])\s*"
GH_PR_MERGE = re.compile(CMD_POS + r"gh\s+pr\s+merge(?!\S)")
GIT_MERGE = re.compile(CMD_POS + r"git(?:\s+-\S+)*\s+merge(?!\S)")
MERGE_HOUSEKEEPING = re.compile(r"--(?:abort|continue|quit)\b")


def is_guarded_merge(command, cwd):
    """True when the command would merge into main/master."""
    if GH_PR_MERGE.search(command):
        return True
    if GIT_MERGE.search(command) and not MERGE_HOUSEKEEPING.search(command):
        # `git merge main` on a feature branch (syncing main into the
        # branch) is required by the git model — only guard merges made
        # while sitting on main/master.
        rc, branch = cc.git(["branch", "--show-current"], cwd)
        return rc == 0 and branch.strip() in ("main", "master")
    return False


def main():
    data = cc.read_input()
    if data.get("tool_name") != "Bash":
        return
    command = (data.get("tool_input") or {}).get("command") or ""
    if not command:
        return
    cwd = data.get("cwd") or os.getcwd()
    root = cc.find_cairn_root(cwd)
    if not root:
        return
    if not is_guarded_merge(command, cwd):
        return
    marker = os.path.join(root, MARKER_RELPATH)
    if os.path.isfile(marker):
        try:
            os.remove(marker)  # single-use: one approval, one merge attempt
        except Exception:
            pass
        return
    cc.emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "Merging to main requires explicit user approval at the "
                    "review gate (tracking-rules: nothing reaches main "
                    "without it). /milestone-review records that approval "
                    "by writing cairn/.merge-approved, which this guard "
                    "consumes per merge attempt. If the user has just "
                    "approved in chat (e.g., a failed merge is being "
                    "retried), recreate the marker and rerun."
                ),
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
