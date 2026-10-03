#!/usr/bin/env python3
"""PreToolUse(Bash) hook: deny merges to main without recorded approval.

Nothing reaches main without the user's explicit approval at a gate: the
merge question, or the plan question set for a milestone approved up front
(D-145). /milestone-review (or /hotfix) records that approval by writing a
single-use marker file, cairn/.merge-approved (gitignored); this hook
denies `gh pr merge` and `git merge`-into-main when the marker is
absent, and consumes it when present. Consumption is a rename to
cairn/.merge-approved.pending: merge_guard_post.py then restores the
marker if the merge attempt fails (nonzero exit) and deletes the pending
file when it succeeds, so one approval survives failed retries but never
outlives a successful merge (M60; ends the M33 rewrite-the-marker manual
step). No-op outside cairn repos.

The marker also names the PR it approves, and a `gh pr merge` must name the
same one (M72): a command naming a different PR is denied, and so is a bare
`gh pr merge` that names none, since an approval that cannot be checked is
not an approval. A marker with no PR reference predates the convention and
falls back to the bare existence check. Denials never consume the marker.

An up-front marker (`M<NNN> approved up front … for PR #<N>`, D-145) also
needs the milestone's `Merge approval:` slot to read `up front` in its file
at the local remote-tracking ref of the default branch, never the working
tree or the local default branch: the plan commit there is the record of
the user's answer. A missing ref, file, or slot denies, and so does any
other value. The read trusts that ref as last fetched.

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

False-positive side (M163): CMD_POS treats a newline as a command
separator, so a Bash heredoc or quoted script body whose text carries a
guarded merge command at line start is seen as that merge and denied.
Author such content (tests, docs) via the Write tool, not a heredoc.

Cross-repo limitations (M162; non-exhaustive): an approval binds the repo
whose cairn/.merge-approved records it, and the guard denies the cross-repo
`gh pr merge` forms its tokenization can see — repo-targeting flags
(--repo/-R, bundled clusters, --repo=) and leading GH_REPO= assignment
prefixes. The cd-compound spelling (M163, reread M188): the one form
`cairn_common.cd_target` accepts — a single command-position `cd` whose
one literal token names an existing directory, joined by `&&` to the
command's only `gh pr merge` — retargets the guard at that directory: a
target with no cairn tracking is let through after the M162 checks (the
rulebook gates such merges by chat approval alone), a tracked target is
gated on ITS marker, which must name the PR (no legacy no-PR fallback
across repos), and its consumption is resolved there by merge_guard_post.
Every other `cd` spelling before a merge is denied with the accepted forms
named. Limitations of the target read: a directory whose git toplevel is a
nested or stale clone of the session repo (a submodule, an old checkout)
resolves as the guard sees it — an untracked one merges the session repo's
PR ungated, a nested one under the session's cairn root consumes the
session marker; and a session cwd outside every cairn repo returns before
the target is read, so a `cd` INTO a cairn repo from there goes unchecked.
Redirections the detection does NOT see, among others: `pushd ../other &&
gh pr merge`, a bare `cd;` (the token check requires whitespace after
`cd`), a `cd` opening a brace group or an `if … then` body (`{ cd ../other
&& gh pr merge 5; }`, `if true; then cd ../other && gh pr merge 5; fi` —
`{` and `then` are not command separators, so the session cwd's marker
answers), command-substitution subshells (`$(…)`/backticks; parenthesized
subshells ARE seen — `(` is a command separator), alias or wrapper
invocations of gh (`env GH_REPO=o/r gh …` included), a prior `export
GH_REPO=…` in the same command, GH_HOST, and assignment values containing
whitespace, quoting, or substitution — those last spellings hide the merge
from the guard ENTIRELY (no denial, no marker check), since the prefix run
reads space-delimited `VAR=value` words only.
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
    # cd-compound spelling (M163, reread M188) — before every other check:
    # the guard resolves the repo from the `cd` target when the spelling is
    # the one it can read, and denies every other `cd` spelling with the
    # accepted forms named, the cwd repo's marker never consulted for it.
    if cc.cd_precedes_gh_merge(command):
        target = cc.cd_target(command, cwd)
        if target is None:
            deny(
                "This merge is spelled with a `cd` before it in a form the "
                "guard cannot read, so it cannot tell which repo the merge "
                "lands in and the current repo's approval marker must not "
                "answer for it. Accepted forms: exactly one `cd <dir> && gh "
                "pr merge <N> …`, the command's only merge, the directory "
                "an existing one named as an absolute path, an unquoted "
                "`~` path, or a path relative to the session cwd, bare or "
                "quoted, with no `$`, backtick, `*`, or `?`, joined by "
                "`&&` alone, outside any `( … )`. The "
                "guard then gates on that directory's own cairn approval "
                "marker, or steps aside when it has no cairn tracking "
                "(tracking-rules, Git and approval model)."
            )
            return
        root = cc.find_cairn_root(target)
    # Cross-repo denial (M162) — before the marker-existence check, so a
    # repo-targeting merge never reads as "just missing an approval" and
    # never touches the marker.
    occurrences = cc.gh_merge_occurrence_tokens(command)
    if any(
        cc.names_repo_target(tokens) for tokens in occurrences
    ) or cc.gh_merge_gh_repo_prefixed(command):
        deny(
            "This merge targets a repo through --repo/-R or a GH_REPO "
            "environment assignment. An approval "
            "binds the repo whose cairn/.merge-approved records it "
            "(tracking-rules, Git and approval model), so it cannot "
            "authorize a merge in another repo. Run the merge from a "
            "session cwd inside the target repo, or spell it "
            "`cd <target-checkout> && gh pr merge <N> …`, with no repo flag "
            "and no GH_REPO in the environment, after that repo's own "
            "approval gate."
        )
        return
    if not root:
        # The cd target has no cairn tracking: the guard has no marker to
        # check there and no say (tracking-rules: such merges are gated by
        # chat approval alone). Never reached without a cd — the session
        # root was checked above.
        return
    marker = os.path.join(root, cc.MARKER_RELPATH)
    if not os.path.isfile(marker):
        deny(
            "Merging to main requires explicit user approval, given at "
            "the merge question or up front in the plan question set "
            "(tracking-rules: nothing reaches main without it, D-145). "
            "/milestone-review records that approval "
            "by writing cairn/.merge-approved, which this guard "
            "consumes per merge attempt (a failed attempt's marker "
            "is restored automatically by merge_guard_post). If the "
            "user has just approved in chat and the marker is "
            "missing anyway, recreate it and rerun."
            + ("" if root == cc.find_cairn_root(cwd) else
               " The repo checked is the `cd` target, %s — the marker "
               "belongs at %s." % (root, marker))
        )
        return

    # The marker names the PR it approves; a `gh pr merge` must name the
    # same one. A `git merge` has no PR to name and is exempt from this
    # check — its guarded case (merging while sitting on main) is already
    # covered by the marker's existence.
    command_prs = cc.gh_merge_pr_numbers(command)
    if command_prs:
        marker_pr = cc.marker_pr_number(marker)
        if marker_pr is None and root != cc.find_cairn_root(cwd):
            # A marker in a cd-target repo naming no PR: cross-repo
            # approvals began with M188, so no legacy marker exists there
            # to fall back for (M188 plan).
            deny(
                "The approval marker at %s names no PR, so it cannot be "
                "checked against this merge into another repo. Rewrite it "
                "as `M<NNN> approved YYYY-MM-DD for PR #<N>` at that "
                "repo's own approval gate and rerun." % marker
            )
            return
        # Every occurrence must clear the check — a chained
        # `gh pr merge 7 && gh pr merge 9` must not ride through on the
        # first one's approval (M72 review F4).
        if any(pr is None for pr in command_prs):
            deny(
                "This merge does not name a PR, so the recorded approval "
                "cannot be checked against it (tracking-rules, Git and "
                "approval model: an approval that cannot be checked is not "
                "an approval). Spell the number out — "
                "`gh pr merge <N> --squash --delete-branch` — using the PR "
                "the user approved at the gate. Every `gh pr merge` in the "
                "command must name its PR, chained ones included. The "
                "approval marker is untouched; rerun with the number."
            )
            return
        unapproved = [pr for pr in command_prs if pr != marker_pr]
        if marker_pr is not None and unapproved:
            deny(
                "The recorded approval is for PR #%s, but this command "
                "merges PR %s. An approval authorizes exactly the PR it "
                "names (tracking-rules, Git and approval model). Either "
                "merge PR #%s alone, or take the other PR back to its own "
                "approval gate — never rewrite the marker to match the "
                "command."
                % (marker_pr, ", ".join("#" + pr for pr in unapproved), marker_pr)
            )
            return
        # marker_pr is None: a marker written before the PR-binding
        # convention. Fall through to the existence check it was written
        # under rather than rejecting it.

    # An up-front marker (D-145) stands only on the milestone's slot as the
    # default branch carries it; a slot that cannot be read denies.
    number = cc.marker_up_front_milestone(marker)
    if number is not None:
        if not number:
            deny(
                "The approval marker at %s claims an up-front approval but "
                "names no milestone, so the guard cannot read the "
                "`Merge approval:` slot it rests on. Approval comes at the "
                "merge question, or up front in the plan question set for a "
                "milestone whose slot on the default branch reads `up front` "
                "(D-145). Pose the merge question." % marker
            )
            return
        value, source, problem = cc.default_branch_merge_slot(root, number)
        if problem is not None or not value.lower().startswith("up front"):
            read = (
                "no slot value could be read (%s)" % problem
                if problem is not None
                else "the slot reads `%s`" % value
            )
            deny(
                "The approval marker claims an up-front approval for M%s, "
                "but the guard read its `Merge approval:` slot at %s and %s. "
                "Approval comes at the merge question, or up front in the "
                "plan question set, and only a slot that reads `up front` on "
                "the default branch carries the up-front approval (D-145). "
                "Pose the merge question; never rewrite the marker or the "
                "slot to match." % (number, source, read)
            )
            return

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


def deny(reason):
    cc.emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
