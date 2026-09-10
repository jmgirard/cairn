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
or in a leading assignment value (`MSG=--all git commit …`) may over-count
modified files; `git commit --amend` with nothing staged sees
an empty set (the original commit was the catchable event). No-op outside
cairn repos; fail-permissive.
"""

import os
import re
import sys

import cairn_common as cc

# Command position — the shared `cc.CMD_POS`: start of string or right after
# a shell separator, then any leading `VAR=value` assignment words, so
# `GIT_AUTHOR_NAME=x git commit …` is seen like the plain spelling. A plain
# space before "git" means it's an argument (`echo git commit`), not a command.
GIT_COMMIT = re.compile(cc.CMD_POS + r"git(?:\s+-\S+)*\s+commit(?!\S)")

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
    "stop, cut a branch ({branch} via /milestone-plan, or hotfix-<slug> "
    "via /hotfix), and commit there instead."
)
# Guest mode names its milestone branches `<slug>` alone — no `M<NNN>` or
# cairn vocabulary reaches the repo the operator does not own (M184, D-137).
BRANCH_SHAPE = {"owner": "m<nnn>-<slug>", "guest": "<slug>"}


def guest_deny_reason(paths):
    listed = ", ".join(sorted(paths))
    return (
        "cairn guest-mode guard: this commit would carry cairn/ into the "
        f"repository ({listed}). In guest collaboration mode cairn/ is "
        "local-only — listed in .git/info/exclude, never committed "
        "(tracking-rules 'Collaboration mode'). Unstage the cairn/ path(s) "
        "and commit without them; tracking stays on disk."
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
    mode = cc.collaboration_mode(root)
    paths = None
    if mode == "guest":
        # Guest deny arm, ahead of the default-branch early return: on ANY
        # branch a commit carrying a cairn/ path is the one hard stop this
        # guard has — the only lever that keeps a guest's tracking out of
        # someone else's repo (envelope as merge_guard.deny).
        paths = committed_paths(command, root)
        cairn_paths = [p for p in paths if p.startswith("cairn/")]
        if cairn_paths:
            cc.emit(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": guest_deny_reason(cairn_paths),
                    }
                }
            )
            return
    if not cc.on_default_branch(root):
        return
    if paths is None:
        paths = committed_paths(command, root)
    non_cairn = [p for p in paths if not p.startswith("cairn/")]
    if not non_cairn:
        return
    cc.emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": REMINDER.format(
                    branch=BRANCH_SHAPE.get(mode, BRANCH_SHAPE["owner"])
                ),
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
