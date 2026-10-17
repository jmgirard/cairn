# Planted-conflict recall of the history reviewers, Haiku 5.5 against Sonnet 5.5 (M269)

**Provenance.** Ingested 2026-10-17 by M269 from first-hand runs. The runs
are subagents spawned with the Agent tool from a Claude Code desktop
session in this repo. Each run's counts come from its subagent transcript
under `~/.claude/projects/-Users-jmgirard-github-cairn/<session>/subagents/`.
The three task commits are local commits built by M269 on parent
`c56be32`. They were never pushed.
Pagination: —.
Extraction: first-hand run records of 2026-10-17 with nothing to re-verify against. A rerun reproduces the method, not the exact marks.

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
key file in the session scratchpad until all nine judges returned. This
kept them out of the repo, where the reviewers read. The key file's sha256 at design time
is `0d6958433aef87e262c78a6e03f51cdc9ce07b7a85f59d9766f74bbabfbb1bdd`. The
Plants section below copies its content after the runs.

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
