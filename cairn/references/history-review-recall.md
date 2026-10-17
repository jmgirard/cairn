# Planted-conflict recall of the history reviewers, Haiku 5.5 against Sonnet 5.5 (M269)

**Provenance.** Ingested 2026-10-17 by M269 from first-hand runs. The runs
are subagents spawned with the Agent tool from a Claude Code desktop
session in this repo. Each run's counts come from its subagent transcript
under `~/.claude/projects/-Users-jmgirard-github-cairn/<session>/subagents/`.
The three task commits are local commits built by M269 on parent
`c56be32`. They were never pushed.
Pagination: —.
Extraction: first-hand run records with nothing to re-verify against, and a rerun reproduces the method, not the exact marks — observed 2026-10-17.

**Scope.** M228 (`haiku-sonnet-roles.md`) and M264 (`haiku-sonnet-rerun.md`)
scored the two history reviewers by the count of reported findings that an
Opus judge rated valid. Neither note measured the conflicts that a reviewer
missed. D-016 named that risk for a weaker model in a review step. This
note plants known conflicts with the repo's history and measures how many
of them each model's reviewer catches. Cost and precision (invalid
findings) are not measured here. They rest on `haiku-sonnet-rerun.md`. This
is a reference, not an authority. Status lives in `ROADMAP.md`, decisions
in `DECISIONS.md`.

## Design (fixed before any run, 2026-10-17)

Two parts of this section were written after the runs: the **Catch rule.**
paragraph, whose rule is the judge prompt's text fixed before the runs, and
the Plants subsection, copied from the key file. The "Plants and answer
key" paragraph was also corrected after the runs.

**Tasks.** Three commits, each on parent `c56be32` and each with two
planted conflicts and one neutral edit:

| Task | Lens | Surface | SHA | Message |
|---|---|---|---|---|
| A | blame-history | code (`hooks/`) | `968f932b0ffec94b9fbf642ef56472d60400259c` | Tidy guard command-position patterns |
| B | blame-history | skill prose (`skills/hotfix/SKILL.md`) | `08d63c22b733f2183a7a72e698ee8707dc351c02` | Simplify hotfix authoring and re-land steps |
| C | prior-PR-comments | skill prose (`skills/milestone-implement/SKILL.md`, `skills/milestone-review/SKILL.md`) | `3fcb148c56f564dbcb38d834b2c878563145e261` | Shorten the guest sync steps in implement and review |

Each commit was built in a temporary index with `git commit-tree`, so HEAD
and the working tree did not move. The plant forms are these. Task A holds
one revived fixed bug and one undone deliberate addition. Task B holds one
D-entry contradiction and one undone deliberate addition. Task C holds one
defect that an archived review recorded as fixed, and one contradiction of
a point that an archived review raised.

**Plants and answer key.** Parts (2) and (3) of the design were held in a
key file in the session scratchpad until all nine judges returned. The key file's sha256 at design time
is `0d6958433aef87e262c78a6e03f51cdc9ce07b7a85f59d9766f74bbabfbb1bdd`. The
Plants section below copies its content after the runs. The milestone
file's work log at `af3cb5c2` named the six plants in one prose line, so
the leak search (Runs) also covers that file's path.

**Runs.** Each task runs three times with the Agent tool's `model` set to
`sonnet` and three times with `model` set to `haiku`, as `general-purpose`
agents in the foreground, with `effort` unset (D-157). Run index r is 1,
2, or 3.

**Reviewer prompt**, with `<SHA>` and `<LENS>` per task:

> You are a fresh-context reviewer. You did not write this change. The
> change under review is commit <SHA> in /Users/jmgirard/github/cairn, a
> proposed change on top of `c56be32` that is not merged. Its diff is
> `git show <SHA>` and its base is `<SHA>^`. The working tree is shared:
> use ref-based git only (`git show`, `git log`, `git blame`, `git grep`
> against refs, for example `git blame <SHA>^ -- <path>`), never checkout,
> switch, reset, or worktree, and edit nothing. Review history at or before
> `<SHA>^` only, and read repo files with `git show <SHA>^:<path>` or
> `git grep <pattern> <SHA>^ -- <path>`, never from the working tree.
> <LENS> Report each candidate finding, filtering nothing before reporting,
> and rank your own findings: most severe first, one sentence of
> justification each, no numeric scores. Give each finding as a numbered
> item with its file and line. If you find nothing, say so.

`<LENS>` is that reviewer's lens bullet in `skills/milestone-review/SKILL.md`
at `c56be32`, from its bold name to the end of the bullet, with the model
name in parentheses removed, whitespace collapsed, and
`<default-branch>..HEAD` read as `<SHA>^..<SHA>`. Tasks A and B take the
blame-history bullet, and task C takes the prior-PR-comments bullet.

**Judge prompt**, with `<SHA>`, the two report paths, and `<KEY>` (the
task's two plants from the key file: id, file, old and new text, and the
history it conflicts with):

> You are a judge marking whether code reviewers caught planted conflicts.
> Commit <SHA> in /Users/jmgirard/github/cairn (diff `git show <SHA>`, base
> `<SHA>^`) carries two planted conflicts with the repo's history. The key
> below describes them. Two reviewers, labeled A and B, reviewed the commit
> independently. Reviewer A's report: <path A>. Reviewer B's report:
> <path B>. Read only those two files in their directory. In the repo use
> ref-based git only, and edit nothing. Key: <KEY> Catch rule: a report
> catches a plant when one numbered finding cites the plant's file and
> either a line inside the plant's changed hunk or the changed text, and
> also names the history that the key names, or the milestone, commit,
> D-entry, or review that carries it. A finding that names the site but no
> history, or the history but another site, does not catch. Return, for
> each report, one line per plant, `A <plant id>: CAUGHT by finding <n>` or
> `A <plant id>: MISSED`, each with a one-sentence reason, then the B
> lines, then `A numbered findings: <n>` and `B numbered findings: <n>`.

**Catch rule.** A run catches a plant when one numbered finding cites the
plant's file and either a line inside the plant's changed hunk or the
changed text, and also names the history that the key names, or the
milestone, commit, D-entry, or review that carries it. The judge prompt
carries the same rule.

**Judging.** One Opus judge marks each task's run index r. It reads the
Sonnet run r report and the Haiku run r report under labels A and B. The
labels are drawn with `random.SystemRandom` and written to a mapping file
in the session scratchpad before the judge runs. The mappings are read
after all nine judges return. Deviation in the runs: each judge's spawn
prompt told it to read its prompt, with the key inline, from a
`prompt.txt` file in the same directory as the two reports, and to read
no other scratchpad file. The prompt text itself is the one above.

**Verdict rule.** For each model, take each task's mean recall (plants
caught divided by 2) over its three runs, and sum the means over the three
tasks. The verdict is `move` when Sonnet's sum is above zero and Haiku's
sum is at least 0.9 times Sonnet's sum. Otherwise the verdict is `stay`.

### Plants and answer key (copied from the key file after the judges returned)

The key file matched its design-time sha256 when it was read back on
2026-10-17. Design part (2), the patch of each task, is the full
`git diff c56be32 <SHA>` for that task, given below with each task's
one-line neutral edit. The three commits were never pushed and their refs
were deleted after the runs, so to re-measure, apply each patch to
`c56be32` with `git apply` and commit it.

Task A (`968f932b`):

```diff
diff --git a/hooks/commit_guard.py b/hooks/commit_guard.py
index ed8bd942..48d2353c 100644
--- a/hooks/commit_guard.py
+++ b/hooks/commit_guard.py
@@ -35,7 +35,7 @@ an empty set (the original commit was the catchable event); a pathspec
 commit (`git commit -m x <path>`) is not read, so a tracked cairn/ file
 committed by path passes the guest deny — reachable only while cairn/ is
 tracked, which `cairn_validate`'s guest `scaffold present` arm FAILs.
-No-op outside cairn repos; fail-permissive.
+It does nothing outside cairn repos and fails permissive.
 """
 
 import os
diff --git a/hooks/force_push_guard.py b/hooks/force_push_guard.py
index 31aa78a2..9ad4869d 100644
--- a/hooks/force_push_guard.py
+++ b/hooks/force_push_guard.py
@@ -39,13 +39,12 @@ import sys
 
 import cairn_common as cc
 
-# Command position — the shared `cc.CMD_POS`: start of string or right after
-# a shell separator, then any leading `VAR=value` assignment words, so
-# `GH_TOKEN=x git push -f origin main` is seen like the plain spelling. A
-# plain space before "git" means it's an argument (`echo git push`), not a
-# command. The force-flag scan runs over the span AFTER `push`, so an
-# assignment value never reads as a force flag.
-GIT_PUSH = re.compile(cc.CMD_POS + r"git(?:\s+-\S+)*\s+push(?!\S)")
+# Command position only: start of string or right after a shell separator.
+# A plain space before "git" means it's an argument (`echo git push`), not a
+# command. Kept local so this guard reads pushes without importing the merge
+# guard's pattern.
+CMD_POS = r"(?:^|[;&|(\n])\s*"
+GIT_PUSH = re.compile(CMD_POS + r"git(?:\s+-\S+)*\s+push(?!\S)")
 
 # --force / --force-with-lease[=v] / --force-if-includes, or a short-flag
 # cluster containing 'f'. The lookbehind keeps the second dash of a long
diff --git a/hooks/merge_guard.py b/hooks/merge_guard.py
index df3833e3..06e843cc 100644
--- a/hooks/merge_guard.py
+++ b/hooks/merge_guard.py
@@ -169,9 +169,9 @@ def main():
                 "repo's own approval gate and rerun." % marker
             )
             return
-        # Every occurrence must clear the check — a chained
-        # `gh pr merge 7 && gh pr merge 9` must not ride through on the
-        # first one's approval (M72 review F4).
+        # The first `gh pr merge` in the command is the one the user
+        # approved; check it against the marker.
+        command_prs = command_prs[:1]
         if any(pr is None for pr in command_prs):
             deny(
                 "This merge does not name a PR, so the recorded approval "
```

Task B (`08d63c22`):

```diff
diff --git a/skills/hotfix/SKILL.md b/skills/hotfix/SKILL.md
index c83e8ffa..5f6af617 100644
--- a/skills/hotfix/SKILL.md
+++ b/skills/hotfix/SKILL.md
@@ -269,16 +269,16 @@ can resolve against the fork instead of the base repo.
    under the current development version (no milestone/issue jargon in the
    user-facing text).
    Then apply each per-change rule DESIGN.md's Conventions section states,
-   for example a development-version bump on every PR or a NEWS heading
+   such as a development-version bump on every PR or a NEWS heading
    format. Where
    the Conventions section states none, no version is bumped: cairn never
    bumps one on its own cadence (D-041).
-   *Authoring a fix:* nothing is pushed and no PR is opened here — step 6
-   pushes and opens the PR after the approval chip, so a
-   `pull_request`-triggered suite first runs on the head that merges
-   (D-138). Where `cairn/PROFILE.md` opts in to the Copilot review round
-   (`skills/shared/copilot-review.md` §1), owner mode opens it before the
-   chip instead, at step 6's round arm (D-152).
+   *Authoring a fix:* push the branch and open the PR here, as a draft
+   (`git push -u origin hotfix-<slug>`, then `gh pr create --draft`), so
+   CI is already running when the user reaches the approval chip. Where
+   `cairn/PROFILE.md` opts in to the Copilot review round
+   (`skills/shared/copilot-review.md` §1), owner mode requests the round on
+   that draft at step 6's round arm.
    *Adopting a PR:* the PR already exists — never open a second one, except
    through the user-gated fallback below. If the
    contributor added an entry, check it against the declared file and the
@@ -289,16 +289,11 @@ can resolve against the fork instead of the base repo.
    "allow edits by maintainers" on (GitHub's default).
    **When the head branch cannot be pushed to:** ask the contributor on the
    PR to add the missing pieces — it is their work and their credit.
-   If they go quiet, re-landing the work locally is the fallback, but it
-   closes another person's PR under the user's GitHub identity — outward-facing
-   and irreversible from the contributor's side, so it is **never** done
-   unilaterally. Put it to the user as an `AskUserQuestion` chip (recommended
-   = re-land, with a decline option), showing the closing comment's text in
-   chat first. Only on approval: recreate their commits on a
+   If they go quiet, re-land the work locally: recreate their commits on a
    `hotfix-<slug>` branch (`git cherry-pick`), add the test and changelog
    there, open a PR crediting them (`Co-authored-by:`), its body carrying
    in owner mode the `Candidate row:` lines that step 6 names, and close theirs with
-   that comment. Declined → leave their PR open and stop.
+   a comment that names the new PR.
    Never merge a fix whose regression test
    is still missing — that is the one gate this path exists to enforce.
 
```

Task C (`3fcb148c`):

```diff
diff --git a/skills/milestone-implement/SKILL.md b/skills/milestone-implement/SKILL.md
index f64833af..6eae710e 100644
--- a/skills/milestone-implement/SKILL.md
+++ b/skills/milestone-implement/SKILL.md
@@ -95,16 +95,16 @@ run ingestion first (see `/milestone-brief`).
    stacked milestone runs the stacked sync below instead of that rebase.
    Once
    the branch is pushed, other people can push to it too, on the fork or
-   on the base repo, so the rebase waits on one check, run before the
-   rebase. The remote that holds the branch is the open PR's head remote
+   on the base repo, so one check follows the rebase. Rebase first. The
+   remote that holds the branch is the open PR's head remote
    (the rulebook's open-PR head rule), else `<push>`. When
    `git ls-remote --exit-code --heads <remote> <slug>` finds no such
-   branch, the branch was never pushed: rebase, and push nothing.
+   branch, the branch was never pushed: push nothing.
    Otherwise fetch that remote and read
    `git rev-list <slug>..<remote>/<slug>`.
-   If that lists commits, do not rebase, push nothing, and stop with a
+   If that lists commits, push nothing, and stop with a
    close block that names those commits. Otherwise note the remote tip's
-   sha, rebase, and push with
+   sha and push with
    `git push --force-with-lease=<slug>:<sha> <remote> <slug>` (the
    force-push guard covers the default branch alone). The maintainers'
    review comments stay attached to the PR.
diff --git a/skills/milestone-review/SKILL.md b/skills/milestone-review/SKILL.md
index 4db108e9..4ed0a413 100644
--- a/skills/milestone-review/SKILL.md
+++ b/skills/milestone-review/SKILL.md
@@ -123,9 +123,9 @@ re-enters here, at the step the record shows is next:
    branch is worthless and the squash-merge would conflict anyway. Guest
    arm: the fetch is the whole sync — the default branch is never pushed —
    and a moved default branch is taken by `git rebase
-   <base>/<default-branch>` through `/milestone-implement` step 2's guest
-   sync in full: its remote-only-commits check before the rebase, and, for
-   a branch already pushed, its leased push right after it. A stacked
+   <base>/<default-branch>` here, then `git push --force-with-lease
+   <push> <slug>` for a branch already pushed; review does not re-run
+   `/milestone-implement` step 2's sync. A stacked
    milestone takes that step's stacked sync instead of the plain rebase,
    whether or not the default branch moved, but only while the stack
    base's PR is `OPEN`. A merged base is left to step 8, which routes the
@@ -136,7 +136,7 @@ re-enters here, at the step the record shows is next:
 2. Nothing is pushed and no PR is opened here: the push and the `gh pr
    create` sit in step 8, after the step-7 approval, so a
    `pull_request`-triggered suite first runs on the head that merges rather
-   than on every pre-approval push (D-138). The review below proceeds on the
+   than on every pre-approval push (D-138). The review below runs on the
    local branch.
 
    **Copilot arm** (owner mode, the round on per
```

Answer key (design part 3):

| Plant | Form | File | Conflicts with |
|---|---|---|---|
| A1 | revive a fixed bug | `hooks/force_push_guard.py` | hotfix `2a9cd87f` (PR #180): the guard compiles `GIT_PUSH` from the shared `cc.CMD_POS`, so a leading `VAR=value` word cannot hide a push |
| A2 | undo a deliberate addition | `hooks/merge_guard.py` | M72 `b660b423` (PR #70, review F4): every `gh pr merge` in a command must clear the PR-number check |
| B1 | contradict a D-entry | `skills/hotfix/SKILL.md` | D-138 (M186 `fded3dbb`, PR #193): the hotfix PR opens after the user's approval |
| B2 | undo a deliberate addition | `skills/hotfix/SKILL.md` | M73 `010f9bdd` (PR #71): re-landing a contributor's PR needs the user's chip with a decline option |
| C1 | bring back a defect a review recorded as fixed | `skills/milestone-implement/SKILL.md` | M267 archive Review: a check run after the rebase always stopped |
| C2 | contradict a point a review raised | `skills/milestone-review/SKILL.md` | M267 archive Review, pass 2: "review now takes implement's sync whole" |

## Runs

Reviewer runs, all on 2026-10-17. "Findings" is the judge's count of the
report's numbered findings, and it equals a count of lines that open with a
number in the saved report. The two plant columns are the judge's marks for
the task's first and second plant.

| Task | Model | Run | Agent id | Model id | Findings | Plant 1 | Plant 2 |
|---|---|---|---|---|---|---|---|
| A | sonnet | 1 | `a8b8dc5da23a42eae` | claude-sonnet-5-5 | 4 | caught | caught |
| A | haiku | 1 | `ad7514044f431d18a` | claude-haiku-5-5 | 2 | caught | caught |
| A | sonnet | 2 | `ad42dc61b2af8846f` | claude-sonnet-5-5 | 4 | caught | caught |
| A | haiku | 2 | `ad6b7cf6ac37f810f` | claude-haiku-5-5 | 2 | caught | caught |
| A | sonnet | 3 | `a8e8744a1e9059ab7` | claude-sonnet-5-5 | 4 | caught | caught |
| A | haiku | 3 | `a79e9b27f511e5576` | claude-haiku-5-5 | 4 | caught | caught |
| B | sonnet | 1 | `ab47bf1319918ba4c` | claude-sonnet-5-5 | 6 | caught | caught |
| B | haiku | 1 | `ad502415cdb9e1e50` | claude-haiku-5-5 | 4 | caught | caught |
| B | sonnet | 2 | `a3ae5dd14155ab160` | claude-sonnet-5-5 | 7 | caught | caught |
| B | haiku | 2 | `a61885901bbd9847c` | claude-haiku-5-5 | 4 | caught | caught |
| B | sonnet | 3 | `a1f2e48afd3287d05` | claude-sonnet-5-5 | 7 | caught | caught |
| B | haiku | 3 | `af0078a8e72666472` | claude-haiku-5-5 | 4 | caught | caught |
| C | sonnet | 1 | `aad09752e0026c819` | claude-sonnet-5-5 | 4 | caught | caught |
| C | haiku | 1 | `a0cbc2fec7144a444` | claude-haiku-5-5 | 5 | caught | caught |
| C | sonnet | 2 | `ab1d2c30e7cbde2e1` | claude-sonnet-5-5 | 3 | caught | caught |
| C | haiku | 2 | `a6033e2409e396881` | claude-haiku-5-5 | 4 | caught | caught |
| C | sonnet | 3 | `a7eb2b674e6787c70` | claude-sonnet-5-5 | 5 | caught | caught |
| C | haiku | 3 | `a480a9860d6413d8a` | claude-haiku-5-5 | 4 | caught | caught |

Judge runs. "Sonnet label" names the label the Sonnet report carried.

| Task | Run | Judge id | Model id | Sonnet label |
|---|---|---|---|---|
| A | 1 | `a12a72aef322d2b2b` | claude-opus-5-5 | B |
| A | 2 | `a17b30e1a73868342` | claude-opus-5-5 | A |
| A | 3 | `aced2b6daf59f2ee4` | claude-opus-5-5 | A |
| B | 1 | `a29f60f1eb165c5f8` | claude-opus-5-5 | A |
| B | 2 | `ac8a69390702578aa` | claude-opus-5-5 | A |
| B | 3 | `af5da08d5033b6363` | claude-opus-5-5 | B |
| C | 1 | `ae27783976caade29` | claude-opus-5-5 | A |
| C | 2 | `a25a5b7ff488fbef5` | claude-opus-5-5 | A |
| C | 3 | `a43743ab27e9e1c4d` | claude-opus-5-5 | A |

The label mappings were read only after all nine judges returned. Each
judge's transcript shows that it read the prompt file of its own task and
run index.

Leak search. Over the tool calls and tool results of all 27 transcripts,
a search for `history-review-recall`, `M269-history-reviewer-recall`,
`key.json`, and `mapping.json` found 0 hits. The same reader found 18 hits
for `report_A.md` in the judges' tool calls, so it reads the calls it
searches. The search cannot see text that an agent saw another way.
During the runs the branch name and the T1 commit subject named the
milestone, so a wider search at review, over the 18 reviewer transcripts'
tool calls and results, looked for `m269` in any case, `planted`, `plant`,
`refs/probe`, and `af3cb5c2`. It found two hits. In one, task B Haiku run 2
listed the scratchpad directory and saw the names `m269` and
`m269-criteria.md`, and its tool calls read neither. In the other, task C
Haiku run 3 read an older PR review reply (on
`skills/tests/test_issue_look_in.py`) that uses the word "planted" in
another sense.

Run notes. Every reviewer named both plants of its task with their history.
Some reviewers also reported a plant's knock-on effects as further findings:
stale comments, prose guards in `skills/tests` that pin the removed text,
and contradictions with untouched steps. Four Haiku reports (task A runs
2 and 3, task B run 3, task C run 2) say that they ran tests in exported
copies of the two trees and saw them fail on the commit. No Sonnet report
says that it ran tests.

## Verdict

| Model | Task A mean | Task B mean | Task C mean | Sum |
|---|---|---|---|---|
| Sonnet | 1.0 | 1.0 | 1.0 | 3.0 |
| Haiku | 1.0 | 1.0 | 1.0 | 3.0 |

Haiku's sum is 1.0 times Sonnet's sum, so the verdict is `move`.

Both models caught all 18 of their plant-runs. The test therefore cannot
show a gap on harder plants. Each plant sat in a small commit (18 to 23
changed lines by `git diff --stat`) whose diff held only two plants and
one neutral edit. The two task A plants break tests in the hook suite, and
reviewers named prose guards in `skills/tests` that pin text the task B and
C plants remove. A miss on a subtler conflict, in a larger diff or with no
test that fails, stays unmeasured. Cost and precision rest on `haiku-sonnet-rerun.md`: Haiku
at 32% of Sonnet's cost and 12 judged-valid findings against 13, both
measured on three runs per task.

## Limits and re-measurement

Three runs per model per task, three tasks, two plants per task, at default
effort, on one repo. One Opus judge marks each run pair. To re-measure,
rebuild the three commits from the Plants section on `c56be32`, follow the
Design section, and apply the verdict rule. A harder plant set that both
models do not fully catch is the natural next test. A rerun that flips the
verdict falsifies this note's verdict.

## Harder set

The first set could not tell the two models apart, so a second set with
subtler plants decides the move (M269 AC3). This section is written in two
stages. Parts (1) and (2) below were committed before any harder-set run,
with the sha256 of a key file kept in the session scratchpad, outside the
repo: `93e7258691ad6e07f6c4b0bc011bcc46a6f4b6075065420b9a8827ecf3530b17`.
The plants, the answer key, the blame and test-suite records, and the runs
are added after all the harder-set judges return.

### (1) Tasks

Three commits, each on parent `c56be32`. Each carries two planted conflicts
inside a larger ordinary edit. No task commit changes a file under a
`tests/` directory.

| Task | Lens | Surface | SHA | Message |
|---|---|---|---|---|
| D | blame-history | code (`scripts/`) | `6556b980f7dc4b704b053693919b60395fbdf137` | Split the status snapshot into section helpers |
| E | blame-history | skill prose and README | `fe3218fc6ea6cccab38539cb08caad5867ae45f1` | Tighten implement's start and hand-off wording; rewrap the README band section |
| F | prior-PR-comments | skill prose and README | `5541bd8d6b2a1847f33b2f39f33c28e34744c920` | Add issue and rerun notes to plan and hotfix; rewrap the README pane section |

### (2) Prompts and rules

The reviewer prompt is the Design section's, with each task's SHA and the
same `<LENS>` bullets: tasks D and E take the blame-history bullet, and
task F takes the prior-PR-comments bullet. Each reviewer runs as a
foreground `general-purpose` Agent call with `model` set to `sonnet` or
`haiku` and `effort` unset, three times per task and model.

The judge prompt is the Design section's judge prompt, with the task's two
plants from the key file as `<KEY>`. Each task and run index gets two judge
runs, 18 in all. Each judge is an Opus run that marks the Sonnet and Haiku
reports of that run index under its own labels A and B. The labels are
drawn with `random.SystemRandom` for each judge separately and written to
a mapping file in the session scratchpad before that judge runs. The two
judges of one pair do not see each other's marks. All 18 mappings are read
only after all 18 judges return.

The catch rule is the Design section's. A plant-run counts as caught only
when both of its judges mark it caught. The verdict rule is the Design
section's, applied to those counts: for each model, take each task's mean
recall (plants caught divided by 2) over its three runs, and sum the means
over the three tasks. The verdict is `move` when Sonnet's sum is above zero
and Haiku's sum is at least 0.9 times Sonnet's sum. Otherwise the verdict
is `stay`.
