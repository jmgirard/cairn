#!/usr/bin/env python3
"""PreToolUse(Bash) hook: deny merges to main without recorded approval.

Nothing reaches main without the user's explicit approval at the review
gate. /milestone-review (or /hotfix) records that approval by writing a
single-use marker file, cairn/.merge-approved (gitignored); this hook
denies `gh pr merge` and `git merge`-into-main when the marker is
absent, and consumes it when present. Consumption is a rename to
cairn/.merge-approved.pending: merge_guard_post.py then restores the
marker if the merge attempt fails (nonzero exit) and deletes the pending
file when it succeeds, so one approval survives failed retries but never
outlives a successful merge (M60; ends the M33 rewrite-the-marker manual
step). No-op outside cairn repos.

Known limitations (documented, accepted): this is defense-in-depth behind
the skill approval-gate + single-use marker, not an airtight sandbox, so
the `git merge` detection is deliberately conservative rather than
exhaustive. Known `git merge` bypasses: a compound `git checkout main &&
git merge X` sees the pre-checkout branch; backtick command substitution
isn't a command-position separator; `git -C <path> merge` merges in a repo
the in-cwd branch check doesn't inspect. The covered, enforced path is the
`gh pr merge` squash-merge convention, which the guard always catches.
The merge-detection regexes and is_guarded_merge live in cairn_common so
merge_guard_post keys on the identical detection.
"""

import os
import sys

import cairn_common as cc


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
    if not cc.is_guarded_merge(command, cwd):
        return
    marker = os.path.join(root, cc.MARKER_RELPATH)
    if os.path.isfile(marker):
        # Consume by rename — single-use: one approval, one merge attempt.
        # merge_guard_post resolves the pending file by outcome (restore on
        # failure, delete on success). Fall back to plain removal if the
        # rename fails, so consumption never silently doesn't happen.
        pending = os.path.join(root, cc.PENDING_RELPATH)
        try:
            os.replace(marker, pending)
        except Exception:
            try:
                os.remove(marker)
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
                    "consumes per merge attempt (a failed attempt's marker "
                    "is restored automatically by merge_guard_post). If the "
                    "user has just approved in chat and the marker is "
                    "missing anyway, recreate it and rerun."
                ),
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
