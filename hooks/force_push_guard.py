#!/usr/bin/env python3
"""PreToolUse(Bash) hook: deny force-pushes to the default branch.

The default branch is a distribution channel and its history is never
rewritten (tracking-rules "Git and approval model": never force-push).
merge_guard.py gates what LANDS on the default branch; this guard
protects the history already on it. It denies a `git push` that would
force-update the default branch via any force form — `--force`,
`--force-with-lease[=...]`, `--force-if-includes`, a short-flag cluster
containing `f` (`-f`, `-uf`), or the flagless `+refspec` syntax
(`git push origin +main`) — in both the explicit-ref form
(`git push -f origin main` / `feature:main` / `+main` / `HEAD:main`)
and the on-default-branch form (`git push -f` with no refspec while
sitting on the default branch). Force-pushes to feature branches, plain
pushes, and non-push commands pass through untouched — false-positive-
free by design (D-023 doctrine: a missed weird form beats blocking
legitimate work).

Known, accepted limitations (conservative like merge_guard.py /
commit_guard.py): multi-token global options (`git -C <path> push`)
aren't matched; git push's known separate-value flags (`-o`, `--repo`,
…) have their values skipped during token parsing, but an *unknown*
future value-taking flag could still be misread as a refspec;
matching is remote-agnostic — a force-push to a same-named branch on a
secondary remote (`git push -f fork main`) is denied too (accepted:
mirrors of the default branch deserve the same protection, and the deny
is recoverable); a `)` ends a span, so a force-push whose refspec
literally contains `)` is missed; `--dry-run` force-pushes are denied
like real ones (harmless to deny — no legitimate workflow dry-runs a
force-push to the default branch); `push.default=upstream` mapping a
differently-named local branch onto the default branch is not resolved
(the current-branch check covers the conventional case). No-op outside
cairn repos; fail-permissive.
"""

import os
import re
import sys

import cairn_common as cc

# Command position only: start of string or right after a shell separator —
# same discipline as merge_guard.py (a plain space before "git" means it's
# an argument, e.g. `echo git push`, not a command).
CMD_POS = r"(?:^|[;&|(\n])\s*"
GIT_PUSH = re.compile(CMD_POS + r"git(?:\s+-\S+)*\s+push(?!\S)")

# --force / --force-with-lease[=v] / --force-if-includes, or a short-flag
# cluster containing 'f'. The lookbehind keeps the second dash of a long
# flag and mid-word letters from matching (so `--force`'s own dashes don't
# double-match and `-u` alone never does) — commit_guard's STAGE_ALL trick.
FORCE_FLAG = re.compile(
    r"(?<![-\w])(?:--force(?:-with-lease(?:=\S*)?|-if-includes)?(?![-\w])"
    r"|-[A-Za-z]*f[A-Za-z]*(?![-\w]))"
)
# `)` ends a span too: CMD_POS treats `(` as a command position (subshell),
# so the matching close-paren must not glue itself onto the last refspec
# token — `(git push -f origin main)` would otherwise tokenize `main)` and
# slip past the name match (M60 review F4a).
SPAN_END = re.compile(r"[;&|\n)]")

# git push flags that take a *separate* value token; the value must not be
# read as a refspec (`git push -f origin feat -o main` is a feature-branch
# push, not one targeting main — M60 review F4b).
VALUE_FLAGS = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}


def push_spans(command):
    """Yield each push command's argument substring (up to the next
    shell separator)."""
    for m in GIT_PUSH.finditer(command):
        rest = command[m.end():]
        stop = SPAN_END.search(rest)
        yield rest[: stop.start()] if stop else rest


def push_args(span):
    """The span's non-flag tokens (remote, then refspecs), with known
    separate-value flags' values skipped."""
    args = []
    skip_next = False
    for tok in span.split():
        if skip_next:
            skip_next = False
            continue
        if tok.startswith("-"):
            skip_next = tok in VALUE_FLAGS
            continue
        args.append(tok)
    return args


def refspec_dst(token):
    """The destination ref a push refspec updates, unqualified."""
    tok = token[1:] if token.startswith("+") else token
    dst = tok.split(":", 1)[1] if ":" in tok else tok
    if dst.startswith("refs/heads/"):
        dst = dst[len("refs/heads/"):]
    return dst


def is_guarded_force_push(span, root):
    """True when this push's arguments force-update the default branch."""
    has_force_flag = bool(FORCE_FLAG.search(span))
    refspecs = push_args(span)[1:]  # first non-flag token is the remote
    if not refspecs:
        # `git push [-f] [remote]`: targets the current branch.
        return has_force_flag and cc.on_default_branch(root)
    forced = refspecs if has_force_flag else [
        s for s in refspecs if s.startswith("+")
    ]
    if not forced:
        return False  # nothing forced: no branch detection, no git calls
        # (a plain push must stay zero-cost — default_branch can be a
        # network ls-remote when origin/HEAD is unset; M60 review F5)
    default = cc.default_branch(root)
    names = {default} if default else {"main", "master"}
    for spec in forced:
        dst = refspec_dst(spec)
        if dst in names:
            return True
        if dst == "HEAD" and cc.on_default_branch(root):
            return True  # `push -f origin HEAD` on the default branch
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
    if not any(is_guarded_force_push(s, root) for s in push_spans(command)):
        return
    cc.emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "Never force-push the default branch (tracking-rules: "
                    "'Git and approval model' — it is a distribution "
                    "channel; its history is never rewritten). This deny "
                    "has no override marker: if the default branch truly "
                    "needs history surgery, that is the user's own call, "
                    "made outside this session. Force-pushing a feature "
                    "branch is allowed and not what was denied here."
                ),
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
