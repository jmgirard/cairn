"""Shared helpers for cairn guardrail hooks.

Python 3 stdlib only. Every hook is a strict no-op (exit 0, no output)
outside cairn-tracked repos, and fails permissive: an unexpected error
must never block the user's session.
"""

import json
import os
import re
import subprocess
import sys

# Statuses whose milestone files count as "active" for context injection.
ACTIVE_STATUSES = {"in-progress", "blocked", "review"}

# The single-use merge-approval marker and its consumed-but-unresolved
# state. merge_guard.py consumes the marker by renaming it to the pending
# path when it lets a guarded merge through; merge_guard_post.py restores
# it (failed attempt) or deletes it (successful merge). Both are ignored
# by stop_guard and gitignored in scaffolded repos.
MARKER_RELPATH = os.path.join("cairn", ".merge-approved")
PENDING_RELPATH = os.path.join("cairn", ".merge-approved.pending")

# Command position only: start of string or right after a shell separator
# (;, &, |, ( , newline) — a plain space before "git"/"gh" means it's an
# argument to something else (e.g. `echo git merge`), not a command.
CMD_POS = r"(?:^|[;&|(\n])\s*"
GH_PR_MERGE = re.compile(CMD_POS + r"gh\s+pr\s+merge(?!\S)")
GIT_MERGE = re.compile(CMD_POS + r"git(?:\s+-\S+)*\s+merge(?!\S)")
MERGE_HOUSEKEEPING = re.compile(r"--(?:abort|continue|quit)\b")


def is_guarded_merge(command, cwd):
    """True when the command would merge into main/master.

    Shared by merge_guard.py (PreToolUse deny/consume) and
    merge_guard_post.py (PostToolUse/PostToolUseFailure resolve), so both
    ends of the marker lifecycle key on the same detection.
    """
    if GH_PR_MERGE.search(command):
        return True
    if GIT_MERGE.search(command) and not MERGE_HOUSEKEEPING.search(command):
        # `git merge main` on a feature branch (syncing main into the
        # branch) is required by the git model — only guard merges made
        # while sitting on main/master.
        rc, branch = git(["branch", "--show-current"], cwd)
        return rc == 0 and branch.strip() in ("main", "master")
    return False


def read_input():
    """Parse the hook's stdin JSON; permissive on garbage."""
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def find_cairn_root(cwd):
    """Walk up from cwd to the first dir containing cairn/ROADMAP.md.

    Returns the repo root path, or None (not a cairn-tracked repo).
    A missing cwd (malformed hook input) is None, never a fallback to
    the process cwd — guards must be deterministic, not guess.
    """
    if not cwd:
        return None
    try:
        path = os.path.abspath(cwd)
    except Exception:
        return None
    while True:
        if os.path.isfile(os.path.join(path, "cairn", "ROADMAP.md")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def git(args, cwd):
    """Run git; return (returncode, stdout). Never raises."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode, result.stdout
    except Exception:
        return 1, ""


def default_branch(cwd):
    """The repo's default branch name, resolved via the remote HEAD.

    Prefers the local `refs/remotes/origin/HEAD` symbolic-ref (instant);
    falls back to `git ls-remote --symref origin HEAD` (network) when it is
    unset. Returns None when no remote resolves — the caller then treats
    main/master as the default (tracking-rules canonical recipe).
    """
    rc, out = git(["symbolic-ref", "--short", "refs/remotes/origin/HEAD"], cwd)
    if rc == 0 and out.strip():
        return out.strip().split("/", 1)[-1]  # strip leading "origin/"
    rc, out = git(["ls-remote", "--symref", "origin", "HEAD"], cwd)
    if rc == 0:
        for line in out.splitlines():
            m = re.match(r"ref:\s+refs/heads/(\S+)\s+HEAD", line.strip())
            if m:
                return m.group(1)
    return None


def on_default_branch(cwd):
    """True when the current branch is the repo's default branch."""
    rc, cur = git(["branch", "--show-current"], cwd)
    if rc != 0:
        return False
    cur = cur.strip()
    if not cur:
        return False  # detached HEAD — not a normal on-default state
    default = default_branch(cwd)
    if default is not None:
        return cur == default
    return cur in ("main", "master")  # no remote: canonical fallback


def parse_roadmap_rows_full(roadmap_text):
    """Yield (id, title, status, depends, priority, relpath) per milestone row.

    Rows look like:
    | M07 | Title | in-progress | — | high | milestones/M07-....md |
    relpath is relative to the cairn/ directory. This is the single
    row-splitter; parse_roadmap_rows is the (id, status, relpath) subset
    the hooks use.
    """
    for line in roadmap_text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")][1:-1]
        if len(cells) < 6 or not cells[0].startswith("M"):
            continue
        yield cells[0], cells[1], cells[2].lower(), cells[3], cells[4], cells[5]


def parse_roadmap_rows(roadmap_text):
    """Yield (id, status, relpath) for each milestone table row."""
    for mid, _title, status, _dep, _pri, relpath in parse_roadmap_rows_full(
        roadmap_text
    ):
        yield mid, status, relpath


def emit(obj):
    json.dump(obj, sys.stdout)
    sys.stdout.write("\n")
