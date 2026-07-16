#!/usr/bin/env python3
"""PreToolUse(Bash) hook: nudge when committing non-cairn files to the
default branch.

The default branch is a distribution channel; the git model forbids
implementing code on it outside a milestone/hotfix branch (tracking-rules
"Git and approval model"). But trivial edits (typos, comments) and docs-only
tracking commits ARE allowed there, and "trivial vs real code change" cannot
be decided mechanically from a file list. So this guard takes the softest
lever memory_guard.py established (D-017): when a `git commit` on the default
branch would include any path outside cairn/, it emits a non-blocking
`additionalContext` nudge and NO `permissionDecision` — the commit proceeds
through the normal permission flow and Claude simply reads the reminder next
turn. All-cairn/ commits (the plan/review/hygiene commits the git model
expects on the default branch) stay silent.

Silent allowlist is cairn/ ONLY — deliberately narrow. Top-level markdown is
NOT treated as docs: in a plugin repo the product itself is markdown, so a
markdown carve-out would stay silent on a real skill edit. Warn-only makes the
residual over-nudge (e.g. a trivial README fix) harmless — the message says so.

Known, accepted limitations (warn-only, so all low-stakes; conservative like
merge_guard.py): `git -C <path> commit` and `git -c k=v commit` (multi-token
global options) aren't matched; a `-a`-looking token inside an `-m` message
may over-count modified files; `git commit --amend` with nothing staged sees
an empty set (the original commit was the catchable event). No-op outside
cairn repos; fail-permissive.
"""

import os
import re
import sys

import cairn_common as cc

# Command position only: start of string or right after a shell separator —
# same discipline as merge_guard.py (a plain space before "git" means it's an
# argument, e.g. `echo git commit`, not a command).
CMD_POS = r"(?:^|[;&|(\n])\s*"
GIT_COMMIT = re.compile(CMD_POS + r"git(?:\s+-\S+)*\s+commit(?!\S)")

# `-a` / `--all` / a short-flag cluster containing 'a' (`-am`, `-va`). The
# lookbehind keeps the second dash of `--amend` and mid-word letters from
# matching, so `--amend` and `-m` alone do not count as "stage all".
STAGE_ALL = re.compile(r"(?<![-\w])(?:--all(?![-\w])|-[A-Za-z]*a[A-Za-z]*)")


def committed_paths(command, cwd):
    """Repo-root-relative paths the commit would include (best effort)."""
    files = set()
    rc, staged = cc.git(["diff", "--cached", "--name-only"], cwd)
    if rc == 0:
        files.update(p for p in staged.splitlines() if p.strip())
    if STAGE_ALL.search(command):
        rc, modified = cc.git(["ls-files", "-m"], cwd)
        if rc == 0:
            files.update(p for p in modified.splitlines() if p.strip())
    return files


REMINDER = (
    "cairn git-model check: you're committing files outside cairn/ to the "
    "default branch. The default branch is a distribution channel — never "
    "implement code on it outside a milestone/hotfix branch (tracking-rules: "
    "'Git and approval model'; CLAUDE.md router). A trivial edit (typo, "
    "comment) or a docs-only change is fine here; but if this is real work, "
    "stop, cut a branch (m<nn>-<slug> via /milestone-plan, or hotfix-<slug> "
    "via /hotfix), and commit there instead."
)


def main():
    data = cc.read_input()
    if data.get("tool_name") != "Bash":
        return
    command = (data.get("tool_input") or {}).get("command") or ""
    if not command or not GIT_COMMIT.search(command):
        return
    cwd = data.get("cwd") or os.getcwd()
    root = cc.find_cairn_root(cwd)
    if not root:
        return
    # Run git from the repo root so --name-only paths are repo-root-relative
    # (cwd-relative output in a subdir would break the cairn/ prefix test).
    if not cc.on_default_branch(root):
        return
    non_cairn = [p for p in committed_paths(command, root)
                 if not p.startswith("cairn/")]
    if not non_cairn:
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
