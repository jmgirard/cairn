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
models do not fully catch is the natural next test, and the Harder set
section below runs it. A rerun that flips the
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

### (3) Diffs

Each task's full `git diff c56be32 <SHA>`. By `--numstat`, task D changes
214 lines, of which its two plants hold fewer than 30 (the rest is the
helper split and the comment rewrap). Task E changes 389, of which its
plants hold the 8 in `skills/milestone-implement/SKILL.md`. Task F changes
534, of which its plants hold the 7 in the two skill files. Each is above
100 once the plant lines are taken out. The README hunks in tasks E and F rewrap whole
sections with the same words, and the `scripts/cairn_scripts.py` hunks in
task D rewrap comments with the same words.

Task D (`6556b980`):

```diff
diff --git a/scripts/cairn_scripts.py b/scripts/cairn_scripts.py
index b3e77cad..75f40a51 100644
--- a/scripts/cairn_scripts.py
+++ b/scripts/cairn_scripts.py
@@ -36,66 +36,76 @@ STATUSES = {
 ACTIVE = {"in-progress", "blocked", "review"}
 PRIORITY_ORDER = {"high": 0, "normal": 1, "low": 2}
 
-# Weight caps (tracking-rules): file -> max line count. A live milestone
-# file is < 150; an archived summary is <= 25 (handled separately by path).
-# CLAUDE.md is NOT whole-file capped (D-018): a mature repo's own dev doctrine
-# is not cairn's to police. Only the appended cairn section is capped, via
-# CLAUDE_SECTION_CAP + claude_section_line_count (handled separately).
+# Weight caps (tracking-rules): file -> max line count. A live
+# milestone file is < 150; an archived summary is <= 25 (handled
+# separately by path). CLAUDE.md is NOT whole-file capped (D-018):
+# a mature repo's own dev doctrine is not cairn's to police. Only
+# the appended cairn section is capped, via CLAUDE_SECTION_CAP +
+# claude_section_line_count (handled separately).
 LINE_CAPS = {"cairn/ROADMAP.md": 60, "cairn/LESSONS.md": 50, "cairn/PROFILE.md": 120}
 MILESTONE_CAP = 150
 ARCHIVE_CAP = 25
 
 TERMINAL_ROW_RETENTION = 3  # done + dropped rows share one ROADMAP cap
 
-# Cap on the cairn-owned `## Project tracking (cairn)` block appended to a
-# repo's CLAUDE.md (D-018). The shipped template stays under this cap.
+# Cap on the cairn-owned `## Project tracking (cairn)` block
+# appended to a repo's CLAUDE.md (D-018). The shipped template
+# stays under this cap.
 CLAUDE_SECTION_CAP = 30
 CLAUDE_SECTION_HEADING = "## Project tracking"
 
-# The two plan-owned milestone sections the weight cap does not measure. Both
-# are exempt for one reason — D-045 classifies them as history, never edited, so
-# counting them could leave an over-cap file fixable only by an edit IP4 forbids
-# (the work log at D-046/M77, the milestone-local decisions at D-074/M118, which
-# supersedes D-046's choice (3)). `## Review` is the third member of the
-# cap-exempt set and is exempt by a different route and for a different reason
-# (M55 — it is review-owned): the body boundary itself ends the counted region
-# there, so it is never subtracted. All matched exactly, lowercased.
+# The two plan-owned milestone sections the weight cap does not
+# measure. Both are exempt for one reason — D-045 classifies them
+# as history, never edited, so counting them could leave an
+# over-cap file fixable only by an edit IP4 forbids (the work log
+# at D-046/M77, the milestone-local decisions at D-074/M118, which
+# supersedes D-046's choice (3)). `## Review` is the third member
+# of the cap-exempt set and is exempt by a different route and for
+# a different reason (M55 — it is review-owned): the body boundary
+# itself ends the counted region there, so it is never subtracted.
+# All matched exactly, lowercased.
 WORKLOG_HEADING = "work log"
 DECISIONS_HEADING = "decisions"
 REVIEW_HEADING = "review"
-# What both cap counters SUBTRACT, so the count and its heaviest-first breakdown
-# can never disagree about the set — the invariant preamble+sections==body
-# depends on them dropping exactly the same sections.
+# What both cap counters SUBTRACT, so the count and its
+# heaviest-first breakdown can never disagree about the set — the
+# invariant preamble+sections==body depends on them dropping
+# exactly the same sections.
 EXEMPT_HEADINGS = (WORKLOG_HEADING, DECISIONS_HEADING)
-# The counters' EFFECTIVE exempt set: the two subtracted above plus the one the
-# body boundary excludes. Two routes, one set — which is why this is derived
-# here rather than retyped, and why the `## Review` member is not in
-# `EXEMPT_HEADINGS` (subtracting a section already outside the boundary would
-# double-count it).
+# The counters' EFFECTIVE exempt set: the two subtracted above
+# plus the one the body boundary excludes. Two routes, one set —
+# which is why this is derived here rather than retyped, and why
+# the `## Review` member is not in `EXEMPT_HEADINGS` (subtracting
+# a section already outside the boundary would double-count it).
 #
-# `hooks/session_context.py` carries a MIRROR of this tuple: the hook imports
-# only `cairn_common`, so no shared constant is reachable across the two
-# packages, and a heading the cap exempts but the hook does not recognize is
-# injected whole — the gap the read-bound exists to close (D-063). The mirror is
-# held to this original by a two-sided test (RR08 §BC2), which reds whichever
+# `hooks/session_context.py` carries a MIRROR of this tuple: the
+# hook imports only `cairn_common`, so no shared constant is
+# reachable across the two packages, and a heading the cap exempts
+# but the hook does not recognize is injected whole — the gap the
+# read-bound exists to close (D-063). The mirror is held to this
+# original by a two-sided test (RR08 §BC2), which reds whichever
 # side drifts.
 CAP_EXEMPT_SECTIONS = EXEMPT_HEADINGS + (REVIEW_HEADING,)
 
-# §1 scaffold pieces that must exist once a repo is on cairn (cairn-init §1).
-# Single source of truth for the machine-side drift check
-# (cairn_validate.check_scaffold): a missing piece means the repo predates a
-# later scaffold addition — route the user to /cairn-init repair. Only
-# always-tracked pieces are listed: git does not preserve empty dirs, so the
-# empty scaffold dirs (milestones/archive, reviews/archive, references/sources)
-# are deliberately NOT checked — their absence is not drift. The CLAUDE.md
-# cairn section stays LLM-owned by the /milestone audit, not duplicated here.
+# §1 scaffold pieces that must exist once a repo is on cairn
+# (cairn-init §1). Single source of truth for the machine-side
+# drift check (cairn_validate.check_scaffold): a missing piece
+# means the repo predates a later scaffold addition — route the
+# user to /cairn-init repair. Only always-tracked pieces are
+# listed: git does not preserve empty dirs, so the empty scaffold
+# dirs (milestones/archive, reviews/archive, references/sources)
+# are deliberately NOT checked — their absence is not drift. The
+# CLAUDE.md cairn section stays LLM-owned by the /milestone audit,
+# not duplicated here.
 REQUIRED_SCAFFOLD_FILES = (
     "cairn/DESIGN.md",
-    # ROADMAP.md is also the cairn-repo marker: a missing one makes
-    # resolve_root raise NotCairn (exit 2) before check_scaffold ever runs, so
-    # this entry is belt-and-suspenders — kept so the tuple is the complete §1
-    # file set (the deferred cairn-init-repair-consumes-this candidate wants
-    # that), not because the CLI branch is reachable.
+    # ROADMAP.md is also the cairn-repo marker: a missing one
+    # makes resolve_root raise NotCairn (exit 2) before
+    # check_scaffold ever runs, so this entry is
+    # belt-and-suspenders — kept so the tuple is the complete §1
+    # file set (the deferred cairn-init-repair-consumes-this
+    # candidate wants that), not because the CLI branch is
+    # reachable.
     "cairn/ROADMAP.md",
     "cairn/DECISIONS.md",
     "cairn/LESSONS.md",
@@ -107,17 +117,18 @@ REQUIRED_GITIGNORE = (
     "cairn/.merge-approved",
     "cairn/.merge-approved.pending",
 )
-# Superseded .gitignore entries, old -> new. cairn is post-1.0, so a scaffold
-# rename follows the deprecation cycle (tracking-rules "Universal tracking
-# rules"): a repo still carrying only the old entry satisfies check_scaffold
-# and gets a non-failing deprecation advisory naming the new one, rather than
-# a hard FAIL it did nothing to earn. Renamed at M79 (D-047) because the shelf
+# Superseded .gitignore entries, old -> new. cairn is post-1.0, so
+# a scaffold rename follows the deprecation cycle (tracking-rules
+# "Universal tracking rules"): a repo still carrying only the old
+# entry satisfies check_scaffold and gets a non-failing
+# deprecation advisory naming the new one, rather than a hard FAIL
+# it did nothing to earn. Renamed at M79 (D-047) because the shelf
 # holds any source, not only PDFs.
 DEPRECATED_GITIGNORE = {
     "cairn/references/pdf/": "cairn/references/sources/",
 }
-# .Rbuildignore entry — package repos only (DESCRIPTION present); `^cairn$`
-# keeps the whole tracking dir out of the built package.
+# .Rbuildignore entry — package repos only (DESCRIPTION present);
+# `^cairn$` keeps the whole tracking dir out of the built package.
 REQUIRED_RBUILDIGNORE = ("^cairn$",)
 
 
diff --git a/scripts/cairn_status.py b/scripts/cairn_status.py
index 9bf4db87..9d58b531 100644
--- a/scripts/cairn_status.py
+++ b/scripts/cairn_status.py
@@ -2,53 +2,108 @@
 """cairn status — deterministic project snapshot over cairn/ROADMAP.md.
 
 Prints milestone counts by status, the active milestone(s), the next
-planned milestones by priority, the candidate count, and the last hygiene
-check date. Read-only; exits 0 on success, 2 outside a cairn repo.
+planned milestones by priority, the candidate count, the last hygiene
+check date, and the rulebook's size. Read-only; exits 0 on success, 2
+outside a cairn repo.
 
     python3 scripts/cairn_status.py [ROOT]
+
+The snapshot is built from small section helpers, one per block of the
+output, so each block can be read and tested on its own. Every helper takes
+the parsed rows (or the raw ROADMAP text, where the block reads text the
+row parser does not keep) and returns a list of output lines.
 """
 
+import os
 import sys
 
 import cairn_scripts as cs
 
+# The order the "Milestones by status" block lists the statuses in. The
+# `candidate` status is not here: candidate rows are counted on their own
+# line, since they have no milestone row in the table.
+STATUS_ORDER = ("in-progress", "review", "blocked", "planned", "done", "dropped")
+
+# The rulebook every cairn skill reads, relative to the repo root, and the
+# line budget it is held to. Over the budget, the snapshot says so, so the
+# growth is caught here before the next rule lands.
+RULEBOOK = os.path.join("skills", "shared", "tracking-rules.md")
+RULEBOOK_BUDGET = 650
 
-def render(root):
-    roadmap = cs.read_roadmap(root)
-    rows = cs.rows(roadmap)
-    lines = [f"cairn status — {root}", ""]
 
-    counts = {}
-    for r in rows:
-        counts.setdefault(r["status"], []).append(r["id"])
-    lines.append("Milestones by status:")
-    for status in ("in-progress", "review", "blocked", "planned", "done", "dropped"):
-        ids = counts.get(status, [])
+def _ids_by_status(rows):
+    """Map each status to the ids of its rows, in ROADMAP order."""
+    by_status = {}
+    for row in rows:
+        by_status.setdefault(row["status"], []).append(row["id"])
+    return by_status
+
+
+def status_block(rows, roadmap):
+    """The "Milestones by status" block: one line per status in
+    STATUS_ORDER with its count and ids, then the candidate count."""
+    by_status = _ids_by_status(rows)
+    lines = ["Milestones by status:"]
+    for status in STATUS_ORDER:
+        ids = sorted(by_status.get(status, []))
         suffix = f"   {', '.join(ids)}" if ids else ""
         lines.append(f"  {status:<12} {len(ids)}{suffix}")
     lines.append(f"  (candidates  {cs.candidate_count(roadmap)})")
-    lines.append("")
+    return lines
+
+
+def active_block(rows):
+    """One `Active:` line per active row, or `Active: none`."""
+    active = [row for row in rows if row["status"] in cs.ACTIVE]
+    if not active:
+        return ["Active: none"]
+    return [f"Active: {row['id']} ({row['status']}) — {row['title']}" for row in active]
 
-    active = [r for r in rows if r["status"] in cs.ACTIVE]
-    if active:
-        for r in active:
-            lines.append(f"Active: {r['id']} ({r['status']}) — {r['title']}")
-    else:
-        lines.append("Active: none")
 
-    planned = cs.sort_by_priority([r for r in rows if r["status"] == "planned"])
-    if planned:
-        nxt = ", ".join(f"{r['id']} ({r['priority']})" for r in planned)
-        lines.append(f"Next planned (by priority): {nxt}")
-    else:
-        lines.append("Next planned (by priority): none")
+def planned_block(rows):
+    """The planned rows by priority, then by numeric id, on one line."""
+    planned = cs.sort_by_priority([row for row in rows if row["status"] == "planned"])
+    if not planned:
+        return ["Next planned (by priority): none"]
+    listed = ", ".join(f"{row['id']} ({row['priority']})" for row in planned)
+    return [f"Next planned (by priority): {listed}"]
 
+
+def hygiene_block(roadmap):
+    """The date of the last hygiene check, or `unknown`."""
     hygiene = cs.last_hygiene_check(roadmap)
-    lines.append(f"Last hygiene check: {hygiene or 'unknown'}")
+    return [f"Last hygiene check: {hygiene or 'unknown'}"]
+
+
+def rulebook_block(root):
+    """The rulebook's line count, flagged when it is over RULEBOOK_BUDGET.
+    A repo with no rulebook at that path (an adopting repo, which reads the
+    plugin's copy) gets no line."""
+    path = os.path.join(root, RULEBOOK)
+    if not os.path.isfile(path):
+        return []
+    count = cs.line_count(path)
+    note = " — over budget, trim before adding rules" if count > RULEBOOK_BUDGET else ""
+    return [f"Rulebook: {count} lines{note}"]
+
+
+def render(root):
+    """The whole snapshot as one string."""
+    roadmap = cs.read_roadmap(root)
+    rows = cs.rows(roadmap)
+    lines = [f"cairn status — {root}", ""]
+    lines += status_block(rows, roadmap)
+    lines.append("")
+    lines += active_block(rows)
+    lines += planned_block(rows)
+    lines += hygiene_block(roadmap)
+    lines += rulebook_block(root)
     return "\n".join(lines)
 
 
 def main(argv):
+    """Resolve the repo root from argv, print the snapshot, and return the
+    exit code: 0 on success, 2 when the root is not a cairn repo."""
     try:
         root = cs.resolve_root(argv)
     except cs.NotCairn as e:
```

Task E (`fe3218fc`):

````diff
diff --git a/README.md b/README.md
index 1f36c168..a0f73868 100644
--- a/README.md
+++ b/README.md
@@ -85,192 +85,221 @@ repo, and the draft uses no cairn terms.
 
 ### The milestone band
 
-The plugin also ships a Claude Code mod: a band above the prompt that shows
-one row for the milestone in flight, or between milestones for the next one
-you can start, or a row to start planning when there is no such milestone. The milestone in flight is the first `in-progress` row of
-`cairn/ROADMAP.md`, else its first `review` row. While `/milestone-review`
-runs, it is the first `review` row when one exists. The row gives no sign
-of the other active milestones. The id in bold and the milestone's title
-sit at the left of the row. The flow track and the percent sit at its
-right edge. One of the band's test fixtures gives this row when M010 is
-its only active milestone, shown here with the track as `[track]`:
+The plugin also ships a Claude Code mod: a band above the prompt
+that shows one row for the milestone in flight, or between
+milestones for the next one you can start, or a row to start
+planning when there is no such milestone. The milestone in
+flight is the first `in-progress` row of `cairn/ROADMAP.md`,
+else its first `review` row. While `/milestone-review` runs, it
+is the first `review` row when one exists. The row gives no sign
+of the other active milestones. The id in bold and the
+milestone's title sit at the left of the row. The flow track and
+the percent sit at its right edge. One of the band's test
+fixtures gives this row when M010 is its only active milestone,
+shown here with the track as `[track]`:
 
 ```text
 M010 Nested tasks and a capital X  [track] 88%
 ```
 
-The track is one rounded bar of three equal parts: plan, implement, then
-review. On a milestone row, plan is full. Implement fills by the checked
-boxes of `## Tasks`, and it is full on a `review` row. Review fills by the
-checked boxes of `## Acceptance criteria`. Specks fill the track from its
-left end to the edge of the current phase's fill. They start sparse and
-gray, and they grow dense near the edge, where more of them take the
-phase's color: blue or teal for plan, orange for implement, and green for
-review (blue in the colorblind themes). A pill on that edge names the
-phase and its counts, such as `Implement 1/3` or `Review 1/2`, in the
-phase's color. A section with no boxes shows `no tasks` or `no criteria`
-in the pill. The percent of the whole flow follows the track. Each part counts
-for a third, and the percent rounds down. So it reads 100% only on a
-`review` row whose criteria are all checked, and a `review` row with no
-criteria reads 66%.
-
-In the desktop app, and on any other surface that can draw an image, the
-track is an image. Two thin marks divide the three
-parts. In the current part, a tick marks each item edge past the fill when
-the items are 6 pixels apart or more. The image cannot follow your theme's
-colors, so it draws from one fixed palette meant for a light or a dark
-background: translucent grays, and the phase colors `rgb(71,103,158)` blue,
-`rgb(152,85,57)` orange, and `rgb(68,113,81)` green. The pill's white text
-has a contrast of at least 4.5:1 on its color, the WCAG 2.2 minimum for
-text, whatever the background. In the terminal the track is a run of
-braille characters on your theme's `userMessageBackground` color. Its dots
-are the specks, a dim mark divides the parts past the fill, and the pill is
-bold text in your theme's `inverseText` color on the phase's color. There
-the phase colors are your Claude Code theme's own keys: `planMode` (teal)
-for plan, `claude` (orange) for implement, and `success` (green) for
-review. The colorblind themes draw `success` in blue, and the ANSI themes
-use your terminal's own colors.
-
-The desktop app draws the track at 7 pixels a column, up to 52 columns and
-at most 360 pixels. The terminal draws it at most 52 characters wide. In a narrower window the track gets shorter, so that the
-title keeps 10 columns, or its full width when the title is shorter. The
-track keeps at least 12 columns. When the whole pill would take more than
-a third of the track, the pill shows the counts alone, such as `1/3`, or
-`none` for a section with no boxes. The band counts one column per
-character, so a short title of wide characters, such as CJK characters or
-emoji, can get less room than it draws. A title too long for the width is
-cut at its end, and the right part stays at the right edge.
-
-A row whose `File/Archive` path names no regular file the band can read
-shows `no milestone file` in place of the track, or `no file` in a narrow
-window, in your theme's warning color. The rest of the row draws in the
-theme's gray. If another plugin draws a band in the same place, its rows
-show under cairn's.
-
-The band draws nothing of the running cairn skill. It keeps track of the
-skill for two things: the row it shows during `/milestone-review`, and
-when a hidden band shows again (below). A cairn skill counts from its
-start, by its plain name or its `cairn:` name. It stays until Claude stops
-with no background work in flight and no one-shot wakeup pending, such as
-after the skill's closing summary. A question chip the skill asks you waits
-inside the turn, so the skill stays while you answer it. A question asked
-in plain text ends the turn. With no background work in flight, the skill
-ends with it, and otherwise your typed answer ends it. When Claude ends a turn
-to wait for background work, such as the reviewers that
-`/milestone-review` starts, the skill stays through the wait and through
-the turns that the work's notices start. A prompt you type while Claude is
-idle ends the skill. A prompt you type while Claude works keeps it, and so
-does a message from another session. An interrupt with Esc keeps it too,
-because an interrupted turn has no stop, so the skill stays until your
-next prompt or until Claude next stops with no background work in flight.
-A cairn skill that starts again, the
-same one included, or a session end, a `/clear` included, also ends it.
-A subagent that loads a cairn skill also counts, because the skill event
-does not say which agent loaded it.
-
-When Claude stops while a one-shot wakeup (`ScheduleWakeup`) is pending,
-the skill stays. A prompt you type that a hook blocks or drops keeps the
-skill too.
-
-The rule has three limits. A recurring scheduled task, such as a `/loop`
-with a fixed interval, does not keep the skill, so a skill that waits on
-one ends when Claude stops. Background work that the skill did not start,
-such as a server or a monitor started earlier, keeps a finished skill
-until your next prompt, because the band does not tell the skill's own
-work from other work. A one-shot wakeup that the skill did not set also
-keeps a finished skill, for the same reason. A `/loop` with no interval
-schedules one-shot wakeups, so it keeps a finished skill this way.
-
-With no milestone active, the band shows an idle row for the next
-milestone you can start, whether or not a cairn skill runs. That milestone
-is the first `planned` row whose `Depends on` milestones are all done, by
-priority and then by id, the one `cairn_next.py` recommends. A dependency
-is done when its row is `done` or its file is in
-`cairn/milestones/archive/`. In guest mode with `# Push remote: base`,
-one dependency can instead be a change that waits for the maintainers'
-review (see "A milestone can build on one that waits for review" under
-guest mode). The idle row draws the id in bold and the
-title, then a track with plan full and the pill `Planned`:
+The track is one rounded bar of three equal parts: plan,
+implement, then review. On a milestone row, plan is full.
+Implement fills by the checked boxes of `## Tasks`, and it is
+full on a `review` row. Review fills by the checked boxes of `##
+Acceptance criteria`. Specks fill the track from its left end to
+the edge of the current phase's fill. They start sparse and
+gray, and they grow dense near the edge, where more of them take
+the phase's color: blue or teal for plan, orange for implement,
+and green for review (blue in the colorblind themes). A pill on
+that edge names the phase and its counts, such as `Implement
+1/3` or `Review 1/2`, in the phase's color. A section with no
+boxes shows `no tasks` or `no criteria` in the pill. The percent
+of the whole flow follows the track. Each part counts for a
+third, and the percent rounds down. So it reads 100% only on a
+`review` row whose criteria are all checked, and a `review` row
+with no criteria reads 66%.
+
+In the desktop app, and on any other surface that can draw an
+image, the track is an image. Two thin marks divide the three
+parts. In the current part, a tick marks each item edge past the
+fill when the items are 6 pixels apart or more. The image cannot
+follow your theme's colors, so it draws from one fixed palette
+meant for a light or a dark background: translucent grays, and
+the phase colors `rgb(71,103,158)` blue, `rgb(152,85,57)`
+orange, and `rgb(68,113,81)` green. The pill's white text has a
+contrast of at least 4.5:1 on its color, the WCAG 2.2 minimum
+for text, whatever the background. In the terminal the track is
+a run of braille characters on your theme's
+`userMessageBackground` color. Its dots are the specks, a dim
+mark divides the parts past the fill, and the pill is bold text
+in your theme's `inverseText` color on the phase's color. There
+the phase colors are your Claude Code theme's own keys:
+`planMode` (teal) for plan, `claude` (orange) for implement, and
+`success` (green) for review. The colorblind themes draw
+`success` in blue, and the ANSI themes use your terminal's own
+colors.
+
+The desktop app draws the track at 7 pixels a column, up to 52
+columns and at most 360 pixels. The terminal draws it at most 52
+characters wide. In a narrower window the track gets shorter, so
+that the title keeps 10 columns, or its full width when the
+title is shorter. The track keeps at least 12 columns. When the
+whole pill would take more than a third of the track, the pill
+shows the counts alone, such as `1/3`, or `none` for a section
+with no boxes. The band counts one column per character, so a
+short title of wide characters, such as CJK characters or emoji,
+can get less room than it draws. A title too long for the width
+is cut at its end, and the right part stays at the right edge.
+
+A row whose `File/Archive` path names no regular file the band
+can read shows `no milestone file` in place of the track, or `no
+file` in a narrow window, in your theme's warning color. The
+rest of the row draws in the theme's gray. If another plugin
+draws a band in the same place, its rows show under cairn's.
+
+The band draws nothing of the running cairn skill. It keeps
+track of the skill for two things: the row it shows during
+`/milestone-review`, and when a hidden band shows again (below).
+A cairn skill counts from its start, by its plain name or its
+`cairn:` name. It stays until Claude stops with no background
+work in flight and no one-shot wakeup pending, such as after the
+skill's closing summary. A question chip the skill asks you
+waits inside the turn, so the skill stays while you answer it. A
+question asked in plain text ends the turn. With no background
+work in flight, the skill ends with it, and otherwise your typed
+answer ends it. When Claude ends a turn to wait for background
+work, such as the reviewers that `/milestone-review` starts, the
+skill stays through the wait and through the turns that the
+work's notices start. A prompt you type while Claude is idle
+ends the skill. A prompt you type while Claude works keeps it,
+and so does a message from another session. An interrupt with
+Esc keeps it too, because an interrupted turn has no stop, so
+the skill stays until your next prompt or until Claude next
+stops with no background work in flight. A cairn skill that
+starts again, the same one included, or a session end, a
+`/clear` included, also ends it. A subagent that loads a cairn
+skill also counts, because the skill event does not say which
+agent loaded it.
+
+When Claude stops while a one-shot wakeup (`ScheduleWakeup`) is
+pending, the skill stays. A prompt you type that a hook blocks
+or drops keeps the skill too.
+
+The rule has three limits. A recurring scheduled task, such as a
+`/loop` with a fixed interval, does not keep the skill, so a
+skill that waits on one ends when Claude stops. Background work
+that the skill did not start, such as a server or a monitor
+started earlier, keeps a finished skill until your next prompt,
+because the band does not tell the skill's own work from other
+work. A one-shot wakeup that the skill did not set also keeps a
+finished skill, for the same reason. A `/loop` with no interval
+schedules one-shot wakeups, so it keeps a finished skill this
+way.
+
+With no milestone active, the band shows an idle row for the
+next milestone you can start, whether or not a cairn skill runs.
+That milestone is the first `planned` row whose `Depends on`
+milestones are all done, by priority and then by id, the one
+`cairn_next.py` recommends. A dependency is done when its row is
+`done` or its file is in `cairn/milestones/archive/`. In guest
+mode with `# Push remote: base`, one dependency can instead be a
+change that waits for the maintainers' review (see "A milestone
+can build on one that waits for review" under guest mode). The
+idle row draws the id in bold and the title, then a track with
+plan full and the pill `Planned`:
 
 ```text
 M021 Waiting to start  [track]
 ```
 
-After the track, an `Implement` button and a `Status` button show while no
-cairn skill runs and Claude is not working, where the row has room for
-them. After a cairn skill ends, a `Clear` button also shows before them.
-A press of `Implement` runs `/clear` and then, in the cleared
-conversation, `/cairn:milestone-implement` with the milestone's id, as if
-you typed both. It does not ask first, because the press is your consent
-to drop the conversation, as a press of `Clear` is. The second command
-starts when the session that `/clear` ends is over. Until then, a press of
-a next-step, `Status`, or `Clear` button does nothing. If the session refuses `/clear`, the
-second command does not run, and `/clear` goes after the text in the
-prompt box with a toast that says why. If the session ends for another
-reason first, such as a resume, the second command does not run, and its
-command line goes into the prompt box with a toast. If the session end
-itself fails, the same happens. The row draws no command as text, so
-while the buttons do not show, the row shows the id, the title, the track,
-and the `≡` and close buttons. In a narrow window the idle row drops its
-track, so that the title keeps room.
-
-With no active milestone and no workable planned milestone, the band shows
-the empty row: `No milestone ready` in gray, with no id and no track. A
-planned milestone that waits on a dependency, or a `blocked` one, does not
-make a milestone workable, so the empty row shows then too. The row
-carries two buttons before its `≡` and close buttons. They show while no
-cairn skill runs and Claude is not working, in a band 37 columns wide or
-more. `Plan` runs `/clear` and then `/cairn:milestone-plan` with no
-arguments in the cleared conversation, as `Implement` does with its
-command. `Status` runs `/cairn:milestone`. A press runs the command
-as if you typed it. A second press while the first run is going does
-nothing. So does a press while `Plan` waits for its `/clear` to end the
-session. If the run is refused, the command goes after the text in the
-prompt box, and a toast says why. If the session refuses `Plan`'s
-`/clear`, `/clear` goes there and planning does not run. If the planning
-run itself is refused, `/cairn:milestone-plan` goes there.
-
-When a cairn skill ends, a `Clear` button shows on any row that carries
-the next-step and `Status` buttons, before them. A press runs `/clear` at
-once and does not ask first. It does not check that the skill's work is
-committed. The button goes away when you send a prompt while Claude is
-idle and no hook drops it, when a cairn skill starts, or when the session
-ends. A `/clear` that the session refuses goes into the prompt box, as
-above. Where the row has no room for three buttons, it drops `Clear` first.
-
-The row ends in a close button: `×` in the terminal, and in the desktop
-app a `✕` that is dim at rest. On a row drawn from a ROADMAP, a `≡`
-button before it opens the cairn pane (below). Pressing the close button
-hides the band. Until the session ends, the band stays hidden while the
-list of active milestones stays the same: their ids, their statuses, and
-their ROADMAP order. For example, a milestone that moves from `implement`
-to `review`, or a milestone that becomes active or leaves both statuses,
-shows the band again. A cairn skill that starts or ends keeps it hidden,
-unless `/milestone-review` moves the band to another row, a `review` row
-when an `in-progress` row would show without it. A hidden idle row shows
-again when another milestone takes its place, or when no milestone is
-workable any more and the empty row takes its place. A hidden empty row
-shows again when a milestone becomes active or workable. A checked box or an edited title does not bring the band back. A
-session end shows a hidden band again, whatever its reason. In the desktop
-app, a `/clear` stops the session, and the band draws again at your next
-message. If the band finds the ROADMAP but cannot read it, or the file is
-empty, the band keeps its row. It keeps the row only when the row came from
-the same repo. The failed read alone does not hide or show it. After the
-session moves to another repo, a failed read shows no row. A working
-directory that cannot be read also shows no row. So the band never shows
-another repo's milestones. A press
-of the close button that lands as the session ends does nothing, so the
-band shows after the session end.
-
-The band finds the ROADMAP in the session's working directory or the nearest
-directory above it. On Windows, the search stops at a network share's root
-(`\\server\share`). It reads the files when the session starts and at the
-end of each turn. It also reads them when a cairn skill starts or ends,
-and after Claude edits or writes a file under a `cairn/` directory, so a
-box Claude checks moves the track inside a long turn. A box you check or a
-status you change shows after the next of these.
-Outside a cairn repo, it draws nothing. It also gives way while Claude Code shows a survey there. The band draws on
-the terminal and in the desktop app.
+After the track, an `Implement` button and a `Status` button
+show while no cairn skill runs and Claude is not working, where
+the row has room for them. After a cairn skill ends, a `Clear`
+button also shows before them. A press of `Implement` runs
+`/clear` and then, in the cleared conversation,
+`/cairn:milestone-implement` with the milestone's id, as if you
+typed both. It does not ask first, because the press is your
+consent to drop the conversation, as a press of `Clear` is. The
+second command starts when the session that `/clear` ends is
+over. Until then, a press of a next-step, `Status`, or `Clear`
+button does nothing. If the session refuses `/clear`, the second
+command does not run, and `/clear` goes after the text in the
+prompt box with a toast that says why. If the session ends for
+another reason first, such as a resume, the second command does
+not run, and its command line goes into the prompt box with a
+toast. If the session end itself fails, the same happens. The
+row draws no command as text, so while the buttons do not show,
+the row shows the id, the title, the track, and the `≡` and
+close buttons. In a narrow window the idle row drops its track,
+so that the title keeps room.
+
+With no active milestone and no workable planned milestone, the
+band shows the empty row: `No milestone ready` in gray, with no
+id and no track. A planned milestone that waits on a dependency,
+or a `blocked` one, does not make a milestone workable, so the
+empty row shows then too. The row carries two buttons before its
+`≡` and close buttons. They show while no cairn skill runs and
+Claude is not working, in a band 37 columns wide or more. `Plan`
+runs `/clear` and then `/cairn:milestone-plan` with no arguments
+in the cleared conversation, as `Implement` does with its
+command. `Status` runs `/cairn:milestone`. A press runs the
+command as if you typed it. A second press while the first run
+is going does nothing. So does a press while `Plan` waits for
+its `/clear` to end the session. If the run is refused, the
+command goes after the text in the prompt box, and a toast says
+why. If the session refuses `Plan`'s `/clear`, `/clear` goes
+there and planning does not run. If the planning run itself is
+refused, `/cairn:milestone-plan` goes there.
+
+When a cairn skill ends, a `Clear` button shows on any row that
+carries the next-step and `Status` buttons, before them. A press
+runs `/clear` at once and does not ask first. It does not check
+that the skill's work is committed. The button goes away when
+you send a prompt while Claude is idle and no hook drops it,
+when a cairn skill starts, or when the session ends. A `/clear`
+that the session refuses goes into the prompt box, as above.
+Where the row has no room for three buttons, it drops `Clear`
+first.
+
+The row ends in a close button: `×` in the terminal, and in the
+desktop app a `✕` that is dim at rest. On a row drawn from a
+ROADMAP, a `≡` button before it opens the cairn pane (below).
+Pressing the close button hides the band. Until the session
+ends, the band stays hidden while the list of active milestones
+stays the same: their ids, their statuses, and their ROADMAP
+order. For example, a milestone that moves from `implement` to
+`review`, or a milestone that becomes active or leaves both
+statuses, shows the band again. A cairn skill that starts or
+ends keeps it hidden, unless `/milestone-review` moves the band
+to another row, a `review` row when an `in-progress` row would
+show without it. A hidden idle row shows again when another
+milestone takes its place, or when no milestone is workable any
+more and the empty row takes its place. A hidden empty row shows
+again when a milestone becomes active or workable. A checked box
+or an edited title does not bring the band back. A session end
+shows a hidden band again, whatever its reason. In the desktop
+app, a `/clear` stops the session, and the band draws again at
+your next message. If the band finds the ROADMAP but cannot read
+it, or the file is empty, the band keeps its row. It keeps the
+row only when the row came from the same repo. The failed read
+alone does not hide or show it. After the session moves to
+another repo, a failed read shows no row. A working directory
+that cannot be read also shows no row. So the band never shows
+another repo's milestones. A press of the close button that
+lands as the session ends does nothing, so the band shows after
+the session end.
+
+The band finds the ROADMAP in the session's working directory or
+the nearest directory above it. On Windows, the search stops at
+a network share's root (`\\server\share`). It reads the files
+when the session starts and at the end of each turn. It also
+reads them when a cairn skill starts or ends, and after Claude
+edits or writes a file under a `cairn/` directory, so a box
+Claude checks moves the track inside a long turn. A box you
+check or a status you change shows after the next of these.
+Outside a cairn repo, it draws nothing. It also gives way while
+Claude Code shows a survey there. The band draws on the terminal
+and in the desktop app.
 
 ### The cairn pane
 
diff --git a/skills/milestone-implement/SKILL.md b/skills/milestone-implement/SKILL.md
index f64833af..513532eb 100644
--- a/skills/milestone-implement/SKILL.md
+++ b/skills/milestone-implement/SKILL.md
@@ -33,7 +33,10 @@ run ingestion first (see `/milestone-brief`).
 ## Workflow
 
 1. Verify status is `planned` (fresh start) or `in-progress` / `blocked`
-   with a resolved blocker (resume). A `blocked` stacked milestone whose
+   with a resolved blocker (resume).
+   When the previous milestone of the same plan merged earlier in this
+   session, start this one at once with no `/clear`, so the plan's
+   milestones run back to back in one run. A `blocked` stacked milestone whose
    stack base's PR is `MERGED` resumes for the restack (step 2's stacked
    sync). Verify all `Depends on:` milestones are
    `done`, except that in guest mode one of them may be a stack base
@@ -326,3 +329,6 @@ run ingestion first (see `/milestone-brief`).
    the full outcome-first account. Review re-reads its state from the files
    and gathers its evidence by command, never from this session's recall
    (tracking-rules "Context hygiene").
+   A milestone whose diff outside `cairn/` adds only skill prose goes to
+   review without the step 7 claim audit, since review's diff reader
+   reads that prose anyway.
````

Task F (`5541bd8d`):

```diff
diff --git a/README.md b/README.md
index 1f36c168..f037c790 100644
--- a/README.md
+++ b/README.md
@@ -274,130 +274,144 @@ the terminal and in the desktop app.
 
 ### The cairn pane
 
-The `/cairn-pane` command opens a pane that shows more than the band. Run
-it again to close the pane, or use the pane's own close mark. The band's
-`≡` button also opens it. In the desktop app the pane docks beside the
-conversation. In the terminal it docks beside a fullscreen conversation
-of 110 columns or more, and otherwise it sits above the prompt.
-
-For each `in-progress` or `review` milestone, the pane shows the id, in
-the phase's color, and the title, with the band's percent for the milestone at the end of
-that line when its file reads, and the goal from the milestone file. It lists every task
-and acceptance criterion, `✓` for a checked box and `○` for an open one,
-and the five newest work-log lines. Each item takes one line, a long item
-ends in `…`, and the goal wraps. Each section starts after a blank row
-with a `▎` and its name in gray capitals. The `TASKS` and `CRITERIA`
-headings show their count and eight squares, `■` for the checked share
-and `□` for the rest. The next command sits in a pill. While no cairn
-skill runs or waits on its background work, a button after the pill reads `Implement`, `Resume`, `Review`, or
-`Plan`, the label of the band's next-step button, and a press runs the
-command as that button does, so `Plan` and `Implement` run `/clear` first. A press while Claude works outside a cairn
-skill runs the command when Claude is idle. At the same times, the Next
-line carries a `Status` button after that button, which runs
-`/cairn:milestone`. The Next line has no `Clear` button. The pane's `⌂`
-button, described below, clears the conversation. Each press runs the
-command of the band's button of the same name. As with the
-next-step button, a press while Claude works outside a cairn skill runs
-when Claude is idle. In a narrow pane, the pill is cut first. In the
-desktop app, a click on the pane while it does not have keyboard focus only
-gives it focus. Then press the button again. The id and the `▎` and `■`
-marks of a milestone draw in its phase's color, the theme's `claude`
-orange for implement and `success` green for review. The `▎` marks of the
-queue draw in the plan color, `planMode`, and the pill draws in the color
-of the phase that its command runs, with `inverseText` text. A
-high-priority candidate's `↑` draws in the implement color. The
-percent counts boxes as the band does, so a box inside an HTML
-comment counts there but not in the `TASKS` and `CRITERIA` counts, and
-the two can differ. A missing or unreadable
-milestone file shows `no milestone file`. Below the milestones, the pane
-shows the next command, the workable planned milestones, and the planned
-milestones that wait on others, as `scripts/cairn_next.py` gives them.
-When no milestone is `in-progress` or `review`, the pane also lists the
-ROADMAP's candidate rows under a `CANDIDATES` heading with their count.
-Each row takes one line: `↑` for a `[high]` row, `○` for a normal one, and
-`↓` for a `[low]` one, then the row's short title. Rows
-inside an HTML comment, such as the placeholders of a new ROADMAP, are not
-listed. A row's short title is its text after a leading `[high] ` or
-`[low] ` token with its space, up to its first `: `, with outer spaces
-removed. A row with no `: ` is cut at its first ` — ` (space, em dash,
-space), so its date and links stay out of the title. A row with neither
-shows all its text. Open each row with a few words that name it, then
-`: ` and the details, for example
-`- [high] Pane refresh lag: details — added 2026-10-15`. Name things in
-words and put no icon, such as an emoji or `⌂`, in a short title, because
-the pane draws its own marks and buttons with such glyphs.
-`/cairn-triage` offers a new short title for a row whose title is empty,
-is longer than 60 characters, is the same as another row's, or holds an
-icon. While no cairn skill
-runs or waits on its background work, each row whose short title is not
-empty carries a `✎` button at its right end.
-A press runs `/clear`, and then `/cairn:milestone-plan` with that short
-title in the cleared conversation. The band has no such button. As with
-the next-step button, a press while Claude works outside a cairn skill
-runs when Claude is idle. While another button's command runs or waits
-for its `/clear`, or a `⌂` press waits for its `/clear`, a press does
-nothing.
-
-Whenever a milestone is `blocked`, the pane lists it under a `BLOCKED`
-heading with the count, after the queue and before the candidates, with
-or without an active milestone. Each line shows the id and title, and
-then `#<n>`, the number of the first GitHub pull request URL in the
-milestone file's `Branch/PR` header, before any `companion:` entry. In
-guest mode, a milestone you handed to the maintainers is `blocked` with
-its PR in that header, so the section lists the PRs that wait on review.
-`scripts/cairn_next.py` prints the same number after each "Externally
-blocked" line, as `(PR #<n>)`.
-
-A cleanup after a merge can stop after it moves the milestone file to
-`cairn/milestones/archive/` and before it changes the ROADMAP row. The row
-then still says `blocked` and names a file that is gone. If exactly one
-archive file has the row's id and its `**Status:**` paragraph starts with
-`done`, the pane reads the PR from the first GitHub pull request URL in
-that paragraph and shows `archived` after the number, or alone when the
-paragraph has no URL. `cairn_next.py`
-prints `(PR #<n>, archived)`, or `(archived)` with no number. A merged PR
-then gets the Finish button, and an archived line gets no other button.
-In guest mode, `/milestone-review` then sets the row to `done`, runs the
-checks, and names the archive, lesson, and review-brief work it skipped
-and the issue comments still owed. It changes nothing in the archive
-file. In owner mode it says what it found and stops, and leaves the row
-as it is.
-
-The pane also shows each PR's state, which it reads from GitHub with one
-`gh api graphql` query for each PR. That query also gives the count
-below. It reads the states when the pane opens, by `/cairn-pane`, by the
-band's open button, or by the reopen at a session start. The reopen skips
-the read when that start already read the states. An open does not wait
-for the read. The words and counts appear together when the last GitHub
-call answers or times out.
-The pane also reads the states, and the tracking files, when you press
-the ↻ Button at the right end of the pane's first line: the first
-milestone's line, or `no active milestone`. The ↻ shows whenever the pane
-has a ROADMAP, and it reads `⋯` while a read runs. A press while an
-earlier ↻ press's read runs does nothing.
-While no cairn skill runs or waits on its background work, a `⌂` button
-sits just before the ↻. A press runs `/clear`, and when that `/clear` ends
-the session, the mod opens the pane again. A pane that is already shown
-stays as it is. Whether a pane behind another tab comes to the front was
-not checked. As with the next-step button, a press while Claude works
-outside a cairn skill runs when Claude is idle. A press does nothing while another
-button's command runs, while `Plan`, `Implement`, or `✎` waits for its
-`/clear`, or while an earlier `⌂` press waits for its `/clear`. A press is
-your consent to drop the conversation, as a press of the band's `Clear`
-is. When a `/clear` keeps the session's process, as a `⌂`, `Clear`,
-`Plan`, `Implement`, or `✎` press does, the pane stays open. The pane and the
-band then read the tracking files again, and so does a `/resume`. After
-either one, a placed pane reads the states again, also when it sits
-behind another tab. A pane that waits undrawn reads the states at its
-first draw. If the pane is placed while a `/clear` start lists the panes,
-the start reads the states with no further draw. A placed pane skips that read when the start's reopen
-already read the states. A pane that waits undrawn skips it when an open
-or the reopen read first. Neither reads when the start failed to list
-the pane. One start reads the states once, also when a reopen and a
-`/resume` both run in it. The pane never reads the states on a timer or
-at a turn's end, so a state can be out of date until the next open or ↻
-press. After a
-read, each line shows one word after its number:
+The `/cairn-pane` command opens a pane that shows more than the
+band. Run it again to close the pane, or use the pane's own
+close mark. The band's `≡` button also opens it. In the desktop
+app the pane docks beside the conversation. In the terminal it
+docks beside a fullscreen conversation of 110 columns or more,
+and otherwise it sits above the prompt.
+
+For each `in-progress` or `review` milestone, the pane shows the
+id, in the phase's color, and the title, with the band's percent
+for the milestone at the end of that line when its file reads,
+and the goal from the milestone file. It lists every task and
+acceptance criterion, `✓` for a checked box and `○` for an open
+one, and the five newest work-log lines. Each item takes one
+line, a long item ends in `…`, and the goal wraps. Each section
+starts after a blank row with a `▎` and its name in gray
+capitals. The `TASKS` and `CRITERIA` headings show their count
+and eight squares, `■` for the checked share and `□` for the
+rest. The next command sits in a pill. While no cairn skill runs
+or waits on its background work, a button after the pill reads
+`Implement`, `Resume`, `Review`, or `Plan`, the label of the
+band's next-step button, and a press runs the command as that
+button does, so `Plan` and `Implement` run `/clear` first. A
+press while Claude works outside a cairn skill runs the command
+when Claude is idle. At the same times, the Next line carries a
+`Status` button after that button, which runs
+`/cairn:milestone`. The Next line has no `Clear` button. The
+pane's `⌂` button, described below, clears the conversation.
+Each press runs the command of the band's button of the same
+name. As with the next-step button, a press while Claude works
+outside a cairn skill runs when Claude is idle. In a narrow
+pane, the pill is cut first. In the desktop app, a click on the
+pane while it does not have keyboard focus only gives it focus.
+Then press the button again. The id and the `▎` and `■` marks of
+a milestone draw in its phase's color, the theme's `claude`
+orange for implement and `success` green for review. The `▎`
+marks of the queue draw in the plan color, `planMode`, and the
+pill draws in the color of the phase that its command runs, with
+`inverseText` text. A high-priority candidate's `↑` draws in the
+implement color. The percent counts boxes as the band does, so a
+box inside an HTML comment counts there but not in the `TASKS`
+and `CRITERIA` counts, and the two can differ. A missing or
+unreadable milestone file shows `no milestone file`. Below the
+milestones, the pane shows the next command, the workable
+planned milestones, and the planned milestones that wait on
+others, as `scripts/cairn_next.py` gives them. When no milestone
+is `in-progress` or `review`, the pane also lists the ROADMAP's
+candidate rows under a `CANDIDATES` heading with their count.
+Each row takes one line: `↑` for a `[high]` row, `○` for a
+normal one, and `↓` for a `[low]` one, then the row's short
+title. Rows inside an HTML comment, such as the placeholders of
+a new ROADMAP, are not listed. A row's short title is its text
+after a leading `[high] ` or `[low] ` token with its space, up
+to its first `: `, with outer spaces removed. A row with no `: `
+is cut at its first ` — ` (space, em dash, space), so its date
+and links stay out of the title. A row with neither shows all
+its text. Open each row with a few words that name it, then `: `
+and the details, for example `- [high] Pane refresh lag: details
+— added 2026-10-15`. Name things in words and put no icon, such
+as an emoji or `⌂`, in a short title, because the pane draws its
+own marks and buttons with such glyphs. `/cairn-triage` offers a
+new short title for a row whose title is empty, is longer than
+60 characters, is the same as another row's, or holds an icon.
+While no cairn skill runs or waits on its background work, each
+row whose short title is not empty carries a `✎` button at its
+right end. A press runs `/clear`, and then
+`/cairn:milestone-plan` with that short title in the cleared
+conversation. The band has no such button. As with the next-step
+button, a press while Claude works outside a cairn skill runs
+when Claude is idle. While another button's command runs or
+waits for its `/clear`, or a `⌂` press waits for its `/clear`, a
+press does nothing.
+
+Whenever a milestone is `blocked`, the pane lists it under a
+`BLOCKED` heading with the count, after the queue and before the
+candidates, with or without an active milestone. Each line shows
+the id and title, and then `#<n>`, the number of the first
+GitHub pull request URL in the milestone file's `Branch/PR`
+header, before any `companion:` entry. In guest mode, a
+milestone you handed to the maintainers is `blocked` with its PR
+in that header, so the section lists the PRs that wait on
+review. `scripts/cairn_next.py` prints the same number after
+each "Externally blocked" line, as `(PR #<n>)`.
+
+A cleanup after a merge can stop after it moves the milestone
+file to `cairn/milestones/archive/` and before it changes the
+ROADMAP row. The row then still says `blocked` and names a file
+that is gone. If exactly one archive file has the row's id and
+its `**Status:**` paragraph starts with `done`, the pane reads
+the PR from the first GitHub pull request URL in that paragraph
+and shows `archived` after the number, or alone when the
+paragraph has no URL. `cairn_next.py` prints `(PR #<n>,
+archived)`, or `(archived)` with no number. A merged PR then
+gets the Finish button, and an archived line gets no other
+button. In guest mode, `/milestone-review` then sets the row to
+`done`, runs the checks, and names the archive, lesson, and
+review-brief work it skipped and the issue comments still owed.
+It changes nothing in the archive file. In owner mode it says
+what it found and stops, and leaves the row as it is.
+
+The pane also shows each PR's state, which it reads from GitHub
+with one `gh api graphql` query for each PR. That query also
+gives the count below. It reads the states when the pane opens,
+by `/cairn-pane`, by the band's open button, or by the reopen at
+a session start. The reopen skips the read when that start
+already read the states. An open does not wait for the read. The
+words and counts appear together when the last GitHub call
+answers or times out. The pane also reads the states, and the
+tracking files, when you press the ↻ Button at the right end of
+the pane's first line: the first milestone's line, or `no active
+milestone`. The ↻ shows whenever the pane has a ROADMAP, and it
+reads `⋯` while a read runs. A press while an earlier ↻ press's
+read runs does nothing. While no cairn skill runs or waits on
+its background work, a `⌂` button sits just before the ↻. A
+press runs `/clear`, and when that `/clear` ends the session,
+the mod opens the pane again. A pane that is already shown stays
+as it is. Whether a pane behind another tab comes to the front
+was not checked. As with the next-step button, a press while
+Claude works outside a cairn skill runs when Claude is idle. A
+press does nothing while another button's command runs, while
+`Plan`, `Implement`, or `✎` waits for its `/clear`, or while an
+earlier `⌂` press waits for its `/clear`. A press is your
+consent to drop the conversation, as a press of the band's
+`Clear` is. When a `/clear` keeps the session's process, as a
+`⌂`, `Clear`, `Plan`, `Implement`, or `✎` press does, the pane
+stays open. The pane and the band then read the tracking files
+again, and so does a `/resume`. After either one, a placed pane
+reads the states again, also when it sits behind another tab. A
+pane that waits undrawn reads the states at its first draw. If
+the pane is placed while a `/clear` start lists the panes, the
+start reads the states with no further draw. A placed pane skips
+that read when the start's reopen already read the states. A
+pane that waits undrawn skips it when an open or the reopen read
+first. Neither reads when the start failed to list the pane. One
+start reads the states once, also when a reopen and a `/resume`
+both run in it. The pane never reads the states on a timer or at
+a turn's end, so a state can be out of date until the next open
+or ↻ press. After a read, each line shows one word after its
+number:
 
 | Word | GitHub state | Button |
 |---|---|---|
@@ -408,132 +422,147 @@ read, each line shows one word after its number:
 | `in review` | OPEN, any other review decision, or none | none |
 | `unknown` | the call failed, exited non-zero, or gave no known state | none |
 
-None of the `Finish`, `Revise`, or `Check` Buttons runs `/clear` first. A
-line not yet read shows no word.
-
-For a PR that GitHub reports as OPEN, the pane draws a line under the PR
-such as `3 unresolved threads`, from the same query. The count is the review threads not marked resolved,
-and a bot's threads, such as Copilot's, count too. A review or comment
-with no thread does not count, because GitHub does not link a reply to
-it, so the pane cannot tell whether you answered it. The count covers the
-newest 100 threads. With no unresolved thread there is no line.
-When the query fails, the PR's word is `unknown` and the line is left out.
-When the query answers but its thread list comes back in a shape the pane
-does not read, the count line is left out, and the PR keeps its state word
-and its Button.
-A hotfix PR whose URL is on a host other than github.com gets its word
-from one `gh pr view <url> --json state,reviewDecision` call instead, and
-no count line.
-
-A `/hotfix` run has no ROADMAP row, so the pane finds its open PR on
-GitHub. The same read runs one `gh pr list --repo <url> --state open
+None of the `Finish`, `Revise`, or `Check` Buttons runs `/clear`
+first. A line not yet read shows no word.
+
+For a PR that GitHub reports as OPEN, the pane draws a line
+under the PR such as `3 unresolved threads`, from the same
+query. The count is the review threads not marked resolved, and
+a bot's threads, such as Copilot's, count too. A review or
+comment with no thread does not count, because GitHub does not
+link a reply to it, so the pane cannot tell whether you answered
+it. The count covers the newest 100 threads. With no unresolved
+thread there is no line. When the query fails, the PR's word is
+`unknown` and the line is left out. When the query answers but
+its thread list comes back in a shape the pane does not read,
+the count line is left out, and the PR keeps its state word and
+its Button. A hotfix PR whose URL is on a host other than
+github.com gets its word from one `gh pr view <url> --json
+state,reviewDecision` call instead, and no count line.
+
+A `/hotfix` run has no ROADMAP row, so the pane finds its open
+PR on GitHub. The same read runs one `gh pr list --repo <url>
+--state open
 --author @me --limit 100` call beside the blocked PRs' reads. The URL is
-the base remote's: `upstream` in guest mode when the repo has that remote,
-else `origin`. An `http` or `https` URL goes to `gh` without any user name
-or token in it. The pane lists each PR from a `hotfix-` branch under a
-`HOTFIXES` heading with the count, after `BLOCKED` and before the
-candidates. Each line shows `#<n>` and the PR's title, and after a read
-the same word and count line that a blocked line shows. A hotfix line has
-no Button. A hotfix PR
-that is also a blocked milestone's PR shows only on the blocked line, and
-the count leaves it out. When the
-list call fails, the pane keeps the last list it read for the same repo.
-The call reads at most 100 of your open PRs, so with more than that, some
-hotfix PRs and some candidate-row marks (below) can be left out.
-When the base remote has no URL, or the call lists no open hotfix PR,
-there is no section.
-
-An open PR can name the candidate rows that it fixes. In owner mode,
-`/hotfix` and `/milestone-review` put one `Candidate row: <short title>`
-line in the PR body for each row that the merge removes or narrows. No
-other cairn skill writes such a line. Cairn writes none in a guest-mode
-PR, because guest mode puts no cairn terms in a PR body. In guest mode,
-the row's started token (below) does this job. The
-same `gh pr list` call reads the body of each listed PR, from any branch.
-A line counts when it opens with exactly `Candidate row: ` and the rest,
-with outer spaces removed, is a candidate row's short title, exactly. A line that you write by hand
-counts the same way. The pane leaves out of its Candidates list each
-candidate row whose short title such a line names, because that PR
-already works on it. The Candidates heading counts only the rows it
-shows, and the pane draws no heading when it hides every row. Only your
-own open PRs on the base remote count.
-
-A `Candidate row:` line inside a fenced code block does not count. A
-fence line opens with three backticks or three tildes after optional
-spaces. Such a block starts at a fence line and ends at the next fence
-line or at the end of the body.
-
-The PRs that hide rows change only when the pane reads its
-PRs: at an open, a ↻ press, or a `/clear` or `/resume` while the pane is
-open. The pane lists candidate rows only
-while no milestone is active, so while a milestone's branch is checked
-out, the row that milestone's PR names is hidden only in another checkout of
-the default branch. Without the opt-in Copilot round (below), a PR that
-`/milestone-review` or an authored `/hotfix` opens does so only after you
-approve the merge. After the merge, the row shows again at
-the pane's first successful PR read, unless another open PR also names
-the row or a counted started token (below) is on it. If `/milestone-review`'s hygiene commit or `/hotfix`'s step 7
-has not removed the row by then, the row shows with its priority mark.
-A row that they narrow also shows again after that read. A
-PR opened before these skills wrote `Candidate row:` lines has none.
-
-A candidate row can also carry a started token at its end:
-` — started M<NNN>` or ` — started #<n>`. `/milestone-plan` writes
-` — started M<NNN>` on each row that the plan absorbs, in owner and guest
-mode. In guest mode, `/hotfix` writes ` — started #<n>` on disk on each row
-it matched, after it opens the PR for the maintainers. Cairn writes no
-`Candidate row:` line in a guest-mode PR, so in guest mode the tokens are
-what usually hides a row. An `M<NNN>` token hides the row while the ROADMAP table
-holds that milestone as `planned` or `blocked`. A `#<n>` token hides the
-row while PR #n is among the open hotfix PRs of the pane's last good read.
-The row shows again when the milestone's row becomes `done` or `dropped`
-or leaves the table, or when PR #n is no longer open. In guest mode, an
-`M<NNN>` token keeps the row hidden after the maintainers merge, until
-review's hygiene sets the milestone `done`. Hygiene then removes the row,
-or narrows it and removes the token. A note after the token, such as
-`; narrowed …`, leaves it read. A token on a dropped milestone or on a PR
-closed without a merge hides nothing. `/cairn-triage` proposes removing a dead token: one whose
-milestone is `done`, `dropped`, gone from the table, or archived, or whose
-PR is merged or closed. A token on an in-progress or review milestone is
-not dead. Triage also proposes adding a missing ` — started M<NNN>` token to a
-row whose short title a planned, in-progress, blocked, or review
-milestone's file quotes in double quotes outside its Out list. Each change
-waits for your answer at its gate. A token opens with ` — `, so the row's
-short title stays the same.
-
-The read needs `gh` on the session's `PATH`, signed in to GitHub. The
-pane writes nothing to GitHub, and `/milestone` still sets a milestone's
-status.
-
-The pane reads the files at the same moments as the band. Outside a cairn
-repo, with no pane open, the command opens no pane and prints `no cairn
-ROADMAP found`. A pane that is already open says the same, and the command
-closes it.
-
-A cairn pane that is shown at a `/clear` is open after it. A press of the
-pane's `⌂` or the band's Clear, `Plan`, or `Implement` Button clears without restarting Claude Code,
-and the pane stays. A typed `/clear` in the desktop app starts a new
-session at your next message, and a pane that was shown opens again then,
-in the same folder. When that next message is `/cairn-pane`, the pane
-stays open, and the next `/cairn-pane` closes it. A pane behind another pane's tab, or waiting undrawn,
-does not open again. An app quit or a closed terminal that ends the session
-with reason `other` (not checked) also brings the pane back at the next
-session in that folder. In a terminal narrower than 110 columns, that pane
-waits undrawn until you open it. This was checked live in the desktop app
-only, for a typed `/clear` and the Clear Buttons that the band and the
-pane had then. A `⌂`, `Plan`, or `Implement` press clears through the same
-call as the band's Clear Button.
-
-Mods are on by default from Claude Code 2.1.287
-([Getting started with Claude Code mods](https://claude.dev/blog/getting-started-with-claude-code-mods/)),
-so that is the version the band needs with no setup. An earlier version
-loads the band only where hooks modules are turned on.
-On an older Claude Code the rest of the plugin still works. In a headless
-(`claude -p`) run of 2.1.284, the merge guard denied a merge and the
-session-start tracking context arrived. The band did not load, and the run
-printed one line that said hooks modules were not turned on in that process.
-That line names the early-access switch, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`
-in the environment.
+the base remote's: `upstream` in guest mode when the repo has
+that remote, else `origin`. An `http` or `https` URL goes to
+`gh` without any user name or token in it. The pane lists each
+PR from a `hotfix-` branch under a `HOTFIXES` heading with the
+count, after `BLOCKED` and before the candidates. Each line
+shows `#<n>` and the PR's title, and after a read the same word
+and count line that a blocked line shows. A hotfix line has no
+Button. A hotfix PR that is also a blocked milestone's PR shows
+only on the blocked line, and the count leaves it out. When the
+list call fails, the pane keeps the last list it read for the
+same repo. The call reads at most 100 of your open PRs, so with
+more than that, some hotfix PRs and some candidate-row marks
+(below) can be left out. When the base remote has no URL, or the
+call lists no open hotfix PR, there is no section.
+
+An open PR can name the candidate rows that it fixes. In owner
+mode, `/hotfix` and `/milestone-review` put one `Candidate row:
+<short title>` line in the PR body for each row that the merge
+removes or narrows. No other cairn skill writes such a line.
+Cairn writes none in a guest-mode PR, because guest mode puts no
+cairn terms in a PR body. In guest mode, the row's started token
+(below) does this job. The same `gh pr list` call reads the body
+of each listed PR, from any branch. A line counts when it opens
+with exactly `Candidate row: ` and the rest, with outer spaces
+removed, is a candidate row's short title, exactly. A line that
+you write by hand counts the same way. The pane leaves out of
+its Candidates list each candidate row whose short title such a
+line names, because that PR already works on it. The Candidates
+heading counts only the rows it shows, and the pane draws no
+heading when it hides every row. Only your own open PRs on the
+base remote count.
+
+A `Candidate row:` line inside a fenced code block does not
+count. A fence line opens with three backticks or three tildes
+after optional spaces. Such a block starts at a fence line and
+ends at the next fence line or at the end of the body.
+
+The PRs that hide rows change only when the pane reads its PRs:
+at an open, a ↻ press, or a `/clear` or `/resume` while the pane
+is open. The pane lists candidate rows only while no milestone
+is active, so while a milestone's branch is checked out, the row
+that milestone's PR names is hidden only in another checkout of
+the default branch. Without the opt-in Copilot round (below), a
+PR that `/milestone-review` or an authored `/hotfix` opens does
+so only after you approve the merge. After the merge, the row
+shows again at the pane's first successful PR read, unless
+another open PR also names the row or a counted started token
+(below) is on it. If `/milestone-review`'s hygiene commit or
+`/hotfix`'s step 7 has not removed the row by then, the row
+shows with its priority mark. A row that they narrow also shows
+again after that read. A PR opened before these skills wrote
+`Candidate row:` lines has none.
+
+A candidate row can also carry a started token at its end: ` —
+started M<NNN>` or ` — started #<n>`. `/milestone-plan` writes `
+— started M<NNN>` on each row that the plan absorbs, in owner
+and guest mode. In guest mode, `/hotfix` writes ` — started
+#<n>` on disk on each row it matched, after it opens the PR for
+the maintainers. Cairn writes no `Candidate row:` line in a
+guest-mode PR, so in guest mode the tokens are what usually
+hides a row. An `M<NNN>` token hides the row while the ROADMAP
+table holds that milestone as `planned` or `blocked`. A `#<n>`
+token hides the row while PR #n is among the open hotfix PRs of
+the pane's last good read. The row shows again when the
+milestone's row becomes `done` or `dropped` or leaves the table,
+or when PR #n is no longer open. In guest mode, an `M<NNN>`
+token keeps the row hidden after the maintainers merge, until
+review's hygiene sets the milestone `done`. Hygiene then removes
+the row, or narrows it and removes the token. A note after the
+token, such as `; narrowed …`, leaves it read. A token on a
+dropped milestone or on a PR closed without a merge hides
+nothing. `/cairn-triage` proposes removing a dead token: one
+whose milestone is `done`, `dropped`, gone from the table, or
+archived, or whose PR is merged or closed. A token on an
+in-progress or review milestone is not dead. Triage also
+proposes adding a missing ` — started M<NNN>` token to a row
+whose short title a planned, in-progress, blocked, or review
+milestone's file quotes in double quotes outside its Out list.
+Each change waits for your answer at its gate. A token opens
+with ` — `, so the row's short title stays the same.
+
+The read needs `gh` on the session's `PATH`, signed in to
+GitHub. The pane writes nothing to GitHub, and `/milestone`
+still sets a milestone's status.
+
+The pane reads the files at the same moments as the band.
+Outside a cairn repo, with no pane open, the command opens no
+pane and prints `no cairn ROADMAP found`. A pane that is already
+open says the same, and the command closes it.
+
+A cairn pane that is shown at a `/clear` is open after it. A
+press of the pane's `⌂` or the band's Clear, `Plan`, or
+`Implement` Button clears without restarting Claude Code, and
+the pane stays. A typed `/clear` in the desktop app starts a new
+session at your next message, and a pane that was shown opens
+again then, in the same folder. When that next message is
+`/cairn-pane`, the pane stays open, and the next `/cairn-pane`
+closes it. A pane behind another pane's tab, or waiting undrawn,
+does not open again. An app quit or a closed terminal that ends
+the session with reason `other` (not checked) also brings the
+pane back at the next session in that folder. In a terminal
+narrower than 110 columns, that pane waits undrawn until you
+open it. This was checked live in the desktop app only, for a
+typed `/clear` and the Clear Buttons that the band and the pane
+had then. A `⌂`, `Plan`, or `Implement` press clears through the
+same call as the band's Clear Button.
+
+Mods are on by default from Claude Code 2.1.287 ([Getting
+started with Claude Code
+mods](https://claude.dev/blog/getting-started-with-claude-code-mods/)),
+so that is the version the band needs with no setup. An earlier
+version loads the band only where hooks modules are turned on.
+On an older Claude Code the rest of the plugin still works. In a
+headless (`claude -p`) run of 2.1.284, the merge guard denied a
+merge and the session-start tracking context arrived. The band
+did not load, and the run printed one line that said hooks
+modules were not turned on in that process. That line names the
+early-access switch, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` in
+the environment.
 
 ## The core loop
 
diff --git a/skills/hotfix/SKILL.md b/skills/hotfix/SKILL.md
index c83e8ffa..a3c9fd73 100644
--- a/skills/hotfix/SKILL.md
+++ b/skills/hotfix/SKILL.md
@@ -304,6 +304,10 @@ can resolve against the fork instead of the base repo.
 
 6. **Approval gate:** in owner mode, the Copilot round arm runs first.
 
+   On a rerun whose PR head moved after an earlier approval, pose the
+   approval chip again at once; the step 5 checks run on the new head
+   after the user approves.
+
    **Copilot round arm** (owner mode, an authored fix, the round on per
    `skills/shared/copilot-review.md` §1; D-152). Before the approval
    gate below, push and open the PR the way this step states for an
diff --git a/skills/milestone-plan/SKILL.md b/skills/milestone-plan/SKILL.md
index 80283ebf..77f52aad 100644
--- a/skills/milestone-plan/SKILL.md
+++ b/skills/milestone-plan/SKILL.md
@@ -154,6 +154,9 @@ its own `D-0NN` id; the headings decide what to open, never what to report.
    subagents with specific focuses; require file:line
    citations. Draft scope, tasks,
    and the list of genuinely open decisions internally.
+   When the request names a GitHub issue, read its body with `gh issue
+   view` first, and take the tier and the steps it states as the plan's
+   starting tier and task list.
    **The acceptance criteria are drafted here to their final wording, not at
    step 4** — step 3's criteria audit reads the bytes step 4 will write, and an
    audit over a rougher draft certifies text that never ships.
```

### (4) Plants

| Plant | Task | Form | File | Planted text |
|---|---|---|---|---|
| D1 | D | bring back a fixed bug | `scripts/cairn_status.py` | ids = sorted(by_status.get(status, [])) |
| D2 | D | contradict a D-entry | `scripts/cairn_status.py` | RULEBOOK_BUDGET = 650 and rulebook_block(): a line-count budget on tracking-rules.md with an 'over budget, trim before adding rules' verdict |
| E1 | E | undo a deliberate past addition | `skills/milestone-implement/SKILL.md` | A milestone whose diff outside `cairn/` adds only skill prose goes to review without the step 7 claim audit, since review's diff reader reads that prose anyway. |
| E2 | E | contradict a D-entry | `skills/milestone-implement/SKILL.md` | When the previous milestone of the same plan merged earlier in this session, start this one at once with no `/clear`, so the plan's milestones run back to back in one run. |
| F1 | F | bring back a defect an archived review recorded as fixed | `skills/milestone-plan/SKILL.md` | When the request names a GitHub issue, read its body with `gh issue view` first, and take the tier and the steps it states as the plan's starting tier and task list. |
| F2 | F | contradict a point an archived review raised | `skills/hotfix/SKILL.md` | On a rerun whose PR head moved after an earlier approval, pose the approval chip again at once; the step 5 checks run on the new head after the user approves. |

D2 is the `RULEBOOK` and `RULEBOOK_BUDGET` constants with their comment, the
`rulebook_block` function, and its call in `render`, in task D's diff above.
E2 is one sentence inserted into the first line of implement step 1. The
plant forms meet the design: across D and E, the three blame-history forms
each occur at least once, and F holds one brought-back defect and one
contradicted review point.

### (5) Answer key, blame checks, and test runs

| Plant | History | Milestone | D-entry | `git log -S` text | Key commit |
|---|---|---|---|---|---|
| D1 | M157 made milestone ids sort numerically across zero-pad widths (`cs.id_num`); a plain `sorted` of ids sorts them as strings, so M57 lists after M100. | M157 | — | `then by numeric ID (M009 before M010)` (in `scripts/cairn_scripts.py`) | `a67bc6c5` M157: milestone IDs sort numerically — three-digit padding, numeric resolution (#158) |
| D2 | D-057 closed rulebook size governance: the rulebook's mass is reported with no threshold, no verdict, and no pass machinery; the plant adds a 650-line budget and a trim verdict. | — | D-057 | `no threshold, no verdict, no pass machinery` (in `skills/milestone/SKILL.md`) | `9f3586ac` M101: Decommissioning — machinery measured not to work is removed or repointed (#99) |
| E1 | M182 (D-136) added implement's claim audit, owed for every user-facing milestone that adds lines outside cairn/, skill prose included; the plant skips it for prose-only diffs. | M182 | D-136 | `claim audit: <N> claims read` (in `skills/milestone-implement/SKILL.md`) | `4982319f` M182: claim audit at implement time for user-facing prose; release-walk changelog claim-read |
| E2 | D-148: a merge ends the run, and the plan's next milestone starts from its typed command after a /clear; the plant starts it at once in the same run. | — | D-148 | `A merge ends the run` (in `skills/shared/tracking-rules.md`) | `36e03930` hotfix: a merge ends the run, so each milestone starts after a /clear (D-148) (#216) |
| F1 | M250 archive Review: its defect returns included routing an issue request to /hotfix and treating issue text as instructions; the fix plans an issue request as a milestone without the tier check. The plant reads the issue body and takes its tier and steps. | M250 | — | `not checked and is planned as a milestone, since` (in `skills/milestone-plan/SKILL.md`) | `ae284c24` M250: The plan checks that the work needs a milestone before it plans one (#261) |
| F2 | M262 archive Review: pass 1 found the first design re-posed the gate on untested commits; the fix resumes only when the marker's oid equals the PR head. The plant re-poses the chip on a moved head before the checks run. | M262 | — | `First, the marker's ` at <oid>` equals the PR's `headRefOid`` (in `skills/hotfix/SKILL.md`) | `5569253e` M262: A rerun of /hotfix on an open PR resumes the merge (#274) |

Blame at `c56be32` over each plant's range: the lines a plant replaces, or
for an inserted plant the three lines on each side of the insertion point.
A check passes when no listed commit is the plant's key commit and no
listed commit's subject names the plant's milestone id or D-entry id.

| Plant | File | Range | Listed commits | Result |
|---|---|---|---|---|
| D1 | `scripts/cairn_status.py` | 26,26 | `01df0557` M10: deterministic tracking scripts (#7) | pass |
| D2 | `scripts/cairn_status.py` | 44,50 | `01df0557` M10: deterministic tracking scripts (#7) | pass |
| E1 | `skills/milestone-implement/SKILL.md` | 324,330 | `d1698579` One question set, then the agent runs the milestone to the merge question (#209) | pass |
| E2 | `skills/milestone-implement/SKILL.md` | 33,39 | `03299445` M268: Let a guest milestone build on one that waits for the maintainers (#280); `2a82bb52` Build rpkg-tracking plugin v0.1 from DRAFT_2 spec | pass |
| F1 | `skills/milestone-plan/SKILL.md` | 153,159 | `2a82bb52` Build rpkg-tracking plugin v0.1 from DRAFT_2 spec; `2e4d9fb4` M04: skill conduct & output discipline (#1); `361713fb` M190: retire the subagent model-tier title tags (#197); `94b72370` M115: fresh-context reader instruments (RR06 recs 4-5) | pass |
| F2 | `skills/hotfix/SKILL.md` | 303,308 | `010f9bdd` M73: external-PR intake — /hotfix adopts a PR it did not author (#71); `2a82bb52` Build rpkg-tracking plugin v0.1 from DRAFT_2 spec; `4d04dcc7` M231: opt-in Copilot review round for hotfix and milestone PRs (#240) | pass |

Test runs, in a clone of this repository that fetched the three task
commits and checked each one out, with `PYTHONDONTWRITEBYTECODE=1 python3 -m
unittest discover -s <suite>`:

| Checkout | `scripts/tests` | `hooks/tests` | `skills/tests` |
|---|---|---|---|
| `c56be32` | exit 0, Ran 409 tests in 5.873s OK (skipped=22) | exit 0, Ran 179 tests in 18.167s OK | exit 0, Ran 822 tests in 0.935s OK |
| task D | exit 0, Ran 409 tests in 5.977s OK (skipped=22) | exit 0, Ran 179 tests in 17.599s OK | exit 0, Ran 822 tests in 0.787s OK |
| task E | exit 0, Ran 409 tests in 5.524s OK (skipped=22) | exit 0, Ran 179 tests in 19.542s OK | exit 0, Ran 822 tests in 0.788s OK |
| task F | exit 0, Ran 409 tests in 5.043s OK (skipped=22) | exit 0, Ran 179 tests in 15.805s OK | exit 0, Ran 822 tests in 0.792s OK |

Control: the same clone at the first set's task A commit (`968f932b`),
whose plants break hook tests, ran `hooks/tests` to exit 1 with 7 errors:
five subtests of `test_env_prefixed_force_push_to_default_is_denied`,
`test_chained_bare_merge_is_denied_too`, and
`test_chained_merge_cannot_ride_on_the_first_approval`.

### (6) Runs and verdict

Reviewer runs, all on 2026-10-17, in three parallel batches of six.
"Findings" is the count of numbered findings, which both judges of the pair
gave and which equals a count of lines that open with a number in the saved
report. Each plant column gives judge 1's mark, judge 2's mark, and the
plant-run's count (caught only when both judges mark it caught).

| Task | Model | Run | Agent id | Model id | Findings | Plant 1 (j1, j2 → count) | Plant 2 (j1, j2 → count) |
|---|---|---|---|---|---|---|---|
| D | sonnet | 1 | `a782cf862b9592c89` | claude-sonnet-5-5 | 7 | caught, caught → caught | caught, caught → caught |
| D | haiku | 1 | `ae118647a34c75f14` | claude-haiku-5-5 | 4 | caught, caught → caught | caught, caught → caught |
| D | sonnet | 2 | `ae68789a088ad8369` | claude-sonnet-5-5 | 5 | missed, missed → missed | caught, caught → caught |
| D | haiku | 2 | `a8bd8bac7cb26affe` | claude-haiku-5-5 | 4 | caught, caught → caught | caught, caught → caught |
| D | sonnet | 3 | `a9fc7c02c04738e1d` | claude-sonnet-5-5 | 5 | caught, caught → caught | caught, caught → caught |
| D | haiku | 3 | `a253fc4f0596d174d` | claude-haiku-5-5 | 3 | caught, caught → caught | caught, caught → caught |
| E | sonnet | 1 | `a8652d3f8ef7a59a9` | claude-sonnet-5-5 | 3 | caught, caught → caught | caught, caught → caught |
| E | haiku | 1 | `a404e833704ce154b` | claude-haiku-5-5 | 4 | caught, caught → caught | caught, caught → caught |
| E | sonnet | 2 | `a89da3c6c7766fd6a` | claude-sonnet-5-5 | 3 | caught, caught → caught | caught, caught → caught |
| E | haiku | 2 | `a6df380eef7b7f001` | claude-haiku-5-5 | 3 | caught, caught → caught | caught, caught → caught |
| E | sonnet | 3 | `ab4e19333638ff7c3` | claude-sonnet-5-5 | 4 | caught, caught → caught | caught, caught → caught |
| E | haiku | 3 | `ad77f29b9b2d5ebb5` | claude-haiku-5-5 | 3 | caught, caught → caught | caught, caught → caught |
| F | sonnet | 1 | `a3f16acf8f3d8c6c6` | claude-sonnet-5-5 | 3 | missed, missed → missed | caught, caught → caught |
| F | haiku | 1 | `a6d8b5bf50c889e42` | claude-haiku-5-5 | 2 | caught, caught → caught | caught, caught → caught |
| F | sonnet | 2 | `ac12cda9a5df6603a` | claude-sonnet-5-5 | 3 | missed, missed → missed | caught, caught → caught |
| F | haiku | 2 | `a80444169aa979d3d` | claude-haiku-5-5 | 2 | caught, caught → caught | caught, caught → caught |
| F | sonnet | 3 | `a11ba983487b91a94` | claude-sonnet-5-5 | 3 | caught, caught → caught | caught, caught → caught |
| F | haiku | 3 | `afc05634e8823d0b2` | claude-haiku-5-5 | 2 | missed, missed → missed | caught, caught → caught |

Judge runs. "Sonnet label" names the label the Sonnet report carried.

| Task | Run | Judge | Agent id | Model id | Sonnet label |
|---|---|---|---|---|---|
| D | 1 | 1 | `a02b44685444d908a` | claude-opus-5-5 | A |
| D | 1 | 2 | `ab445ee9e435bc4ef` | claude-opus-5-5 | B |
| D | 2 | 1 | `ae68d0deff8007dde` | claude-opus-5-5 | B |
| D | 2 | 2 | `a86c951e2c07b35e5` | claude-opus-5-5 | A |
| D | 3 | 1 | `aa8ed3385690baad6` | claude-opus-5-5 | B |
| D | 3 | 2 | `a25487491dddd9af0` | claude-opus-5-5 | B |
| E | 1 | 1 | `a9af067fe57fdb04a` | claude-opus-5-5 | B |
| E | 1 | 2 | `a734eb909cdddc615` | claude-opus-5-5 | A |
| E | 2 | 1 | `a7002b32b3bba33d1` | claude-opus-5-5 | A |
| E | 2 | 2 | `a3adb3c41e0a48b19` | claude-opus-5-5 | B |
| E | 3 | 1 | `a41b9b4b3e596b134` | claude-opus-5-5 | B |
| E | 3 | 2 | `a0c8882d03e1031c1` | claude-opus-5-5 | B |
| F | 1 | 1 | `a4bb57fca006317bf` | claude-opus-5-5 | B |
| F | 1 | 2 | `a9f82bc08e93150da` | claude-opus-5-5 | A |
| F | 2 | 1 | `a506616228da8e0cf` | claude-opus-5-5 | A |
| F | 2 | 2 | `a75c3559a6ad4ea37` | claude-opus-5-5 | B |
| F | 3 | 1 | `aebec5fa4f17ab564` | claude-opus-5-5 | A |
| F | 3 | 2 | `ac733ce34caa2dd30` | claude-opus-5-5 | B |

Disagreements: none. On every plant-run the two judges of a pair gave the same mark.

Every label mapping was read only after all 18 judges returned. Each
judge's transcript shows that it read the prompt file of its own task, run
index, and judge number.

Leak search. Over the tool calls and tool results of all 36 harder-set
transcripts (18 reviewers, 18 judges), a search for `history-review-recall`,
`M269-history-reviewer-recall`, `key.json`, and `mapping.json` found 0 hits.
The same reader found 38 hits for `report_A.md` in the judges' tool calls.
A wider search of the 18 reviewer transcripts for `harder`, `refs/probe`,
`m269` in any case, `planted`, and `edbcf431` found five hits. Task D Haiku
run 3 ran `git grep -i M269` at `c56be32`, which predates the milestone.
Task E Sonnet run 1 listed the branches and saw this milestone's branch
name. Three task F runs read a test at `c56be32` whose variable is named
`planted`. None read the note, the milestone file, the key, or a mapping.

Misses: task D Sonnet run 2 on D1, task F Sonnet runs 1 and 2 on F1, and task
F Haiku run 3 on F1. Each missed finding named the plant's site but gave
other history (for D1, the current `cs.id_num` code without M157; for F1,
M232 or the missing `--repo` lesson without M250).

| Model | Task D mean | Task E mean | Task F mean | Sum |
|---|---|---|---|---|
| Sonnet | 0.8333 | 1.0000 | 0.6667 | 2.5000 |
| Haiku | 1.0000 | 1.0000 | 0.8333 | 2.8333 |

Haiku's sum is 1.1333 times Sonnet's sum, so the verdict is `move`.
Neither model caught all 18 of its plant-runs, so this set is not at the
ceiling. With Sonnet's count unchanged, one more Haiku miss gives 2.6667
against 2.5, still `move`, and four more give 2.1667, below 0.9 times 2.5,
which is `stay`. Cost and precision still rest on
`haiku-sonnet-rerun.md`.
