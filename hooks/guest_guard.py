#!/usr/bin/env python3
"""PreToolUse hook for guest repos: deny a push to the default branch, and
deny a merge unless the repo's profile says `Maintainer: yes`.

A guest repo is one other people share: its cairn files are in the home
folder and nothing of cairn is in the checkout. In such a repo this hook
denies:

- `git push` when it would update the default branch: a refspec that names
  it, or no refspec while the default branch is checked out. This holds for
  a maintainer too, since every change there goes through a PR.
- a merge of a pull request: `gh pr merge`, the merge endpoint through
  `gh api`, and a pull-request merge tool from an MCP server. With
  `Maintainer: yes` in the profile these are let through.

It keeps no record of approvals. Whether the user said to merge is held by
the skill's text, not here.

It judges by the repo the session is working in. A command that reaches
another repo, by `cd`, `-C`, `--repo`, or `GH_REPO`, is judged by the
session's repo all the same, so it can be wrongly denied or wrongly let
through. A `git` global option that takes a value, such as `-c name=value`,
hides the push from it. It reads the default branch from the base remote's local HEAD ref
and makes no network call; with no such ref it takes `main` and `master`.

In the user's own repos and outside cairn repos it does nothing. It never
fails the session: any error ends in exit 0 with no output.
"""

import json
import os
import re
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
)

# Command position: the start of the command or just after a shell
# separator, then any leading VAR=value words. A space before `git` means it
# is an argument to something else, such as `echo git push`.
CMD = r"(?:^|[;&|(\n])\s*(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*"
GIT_PUSH = re.compile(CMD + r"git(?:\s+-\S+)*\s+push(?!\S)")
GH_MERGE = re.compile(CMD + r"gh\s+pr\s+merge(?!\S)")
GH_API_MERGE = re.compile(CMD + r"gh\s+api\b[^;&|\n]*pulls/\d+/merge\b")
SPAN_END = re.compile(r"[;&|\n)]")
MERGE_TOOL = re.compile(r"^mcp__.+__pull_request_merge$")
VALUE_FLAGS = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}

PUSH_REASON = (
    "This is a guest repo, and this push would update its default branch. "
    "Every change to a guest repo goes through a pull request, a trivial "
    "edit included. Push a work branch and open a PR."
)
MERGE_REASON = (
    "This is a guest repo, and its profile does not say `Maintainer: yes`, "
    "so merging is the maintainers' act. Stop at the open PR. If the user "
    "maintains this repo, they add that line to the profile themselves."
)


def push_targets(command):
    """For each `git push` in the command: (refspec destinations, flags)."""
    found = []
    for match in GIT_PUSH.finditer(command):
        rest = command[match.end():]
        stop = SPAN_END.search(rest)
        span = rest[: stop.start()] if stop else rest
        args, skip, flags = [], False, set()
        for token in span.split():
            if skip:
                skip = False
            elif token.startswith("-"):
                skip = token in VALUE_FLAGS
                flags.add(token)
            else:
                args.append(token.strip("'\""))
        dests = []
        for spec in args[1:]:  # the first is the remote
            spec = spec.lstrip("+")
            dest = spec.split(":", 1)[1] if ":" in spec else spec
            dests.append(dest[len("refs/heads/"):] if dest.startswith("refs/heads/") else dest)
        found.append((dests, flags))
    return found


def default_branches(status, top):
    for remote in ("upstream", "origin"):
        code, out = status.git(["symbolic-ref", "--short", "refs/remotes/%s/HEAD" % remote], top)
        if code == 0 and "/" in out:
            return {out.split("/", 1)[1]}
    return {"main", "master"}


def pushes_default(command, status, repo):
    targets = push_targets(command)
    if not targets:
        return False
    defaults = default_branches(status, repo.top)
    on_default = repo.branch in defaults
    for dests, flags in targets:
        if flags & {"--all", "--mirror", "--branches"}:
            return True  # every local branch goes up, the default one included
        if not dests:
            if on_default and "--tags" not in flags:
                return True
            continue
        for dest in dests:
            if dest in defaults or (dest == "HEAD" and on_default):
                return True
    return False


def decide(data, status):
    """The reason to deny this tool call, or None to let it through."""
    tool = data.get("tool_name") or ""
    merge_tool = bool(MERGE_TOOL.match(tool))
    command = ""
    if tool == "Bash":
        command = (data.get("tool_input") or {}).get("command") or ""
    if not command and not merge_tool:
        return None
    merges = merge_tool or bool(GH_MERGE.search(command) or GH_API_MERGE.search(command))
    if not merges and not GIT_PUSH.search(command):
        return None  # nothing to judge, so no git call is made

    repo = status.resolve(data.get("cwd") or os.getcwd())
    if repo is None or repo.kind != "guest":
        return None
    if command and pushes_default(command, status, repo):
        return PUSH_REASON
    if merges:
        maintainer, _ = status.read_maintainer(repo.profile)
        if not maintainer:
            return MERGE_REASON
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(data, dict):
        return
    import cairn_status

    reason = decide(data, cairn_status)
    if reason:
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
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
