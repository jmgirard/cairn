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

**Judging.** One Opus judge marks each task's run index r. It reads the
Sonnet run r report and the Haiku run r report under labels A and B. The
labels are drawn with `random.SystemRandom` and written to a mapping file
in the session scratchpad before the judge runs. The mappings are read
after all nine judges return.

**Verdict rule.** For each model, take each task's mean recall (plants
caught divided by 2) over its three runs, and sum the means over the three
tasks. The verdict is `move` when Sonnet's sum is above zero and Haiku's
sum is at least 0.9 times Sonnet's sum. Otherwise the verdict is `stay`.

## Plants (copied from the key file after the judges returned)

The key file matched its design-time sha256 when it was read back on
2026-10-17. Design part (2), the patch of each task, is `git diff c56be32
<SHA>` for that task. Each task's neutral edit is one line: a docstring in
`hooks/commit_guard.py` (A), "for example" to "such as" in the hotfix skill
(B), and "proceeds on" to "runs on" in review step 2 (C).

Task A (`968f932b`):

```diff
--- a/hooks/force_push_guard.py
+++ b/hooks/force_push_guard.py
@@ -39,13 +39,12 @@ import sys
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
--- a/hooks/merge_guard.py
+++ b/hooks/merge_guard.py
@@ -169,9 +169,9 @@ def main():
-        # Every occurrence must clear the check — a chained
-        # `gh pr merge 7 && gh pr merge 9` must not ride through on the
-        # first one's approval (M72 review F4).
+        # The first `gh pr merge` in the command is the one the user
+        # approved; check it against the marker.
+        command_prs = command_prs[:1]
```

Task B (`08d63c22`, `skills/hotfix/SKILL.md`):

```diff
@@ -269,16 +269,16 @@
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
@@ -289,16 +289,11 @@
-   If they go quiet, re-landing the work locally is the fallback, but it
-   closes another person's PR under the user's GitHub identity — outward-facing
-   and irreversible from the contributor's side, so it is **never** done
-   unilaterally. Put it to the user as an `AskUserQuestion` chip (recommended
-   = re-land, with a decline option), showing the closing comment's text in
-   chat first. Only on approval: recreate their commits on a
+   If they go quiet, re-land the work locally: recreate their commits on a
@@
-   that comment. Declined → leave their PR open and stop.
+   a comment that names the new PR.
```

Task C (`3fcb148c`):

```diff
--- a/skills/milestone-implement/SKILL.md
+++ b/skills/milestone-implement/SKILL.md
@@ -95,16 +95,16 @@
-   on the base repo, so the rebase waits on one check, run before the
-   rebase. The remote that holds the branch is the open PR's head remote
+   on the base repo, so one check follows the rebase. Rebase first. The
+   remote that holds the branch is the open PR's head remote
-   branch, the branch was never pushed: rebase, and push nothing.
+   branch, the branch was never pushed: push nothing.
-   If that lists commits, do not rebase, push nothing, and stop with a
+   If that lists commits, push nothing, and stop with a
-   sha, rebase, and push with
+   sha and push with
--- a/skills/milestone-review/SKILL.md
+++ b/skills/milestone-review/SKILL.md
@@ -123,9 +123,9 @@
-   <base>/<default-branch>` through `/milestone-implement` step 2's guest
-   sync in full: its remote-only-commits check before the rebase, and, for
-   a branch already pushed, its leased push right after it. A stacked
+   <base>/<default-branch>` here, then `git push --force-with-lease
+   <push> <slug>` for a branch already pushed; review does not re-run
+   `/milestone-implement` step 2's sync. A stacked
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
