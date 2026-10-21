<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M310: Check and explain changed snapshots before a PR leaves

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing — skill conduct that adopting repos run at the merge, handoff, and hotfix gates
- **Branch/PR:** m310-snapshot-explain, https://github.com/jmgirard/cairn/pull/324

## Goal

The review and hotfix gates list each snapshot file that the branch changes, and a guest PR says what changed in each one and why.

## Scope

**In:** A changed snapshot file is a path with a directory named `_snaps`
(testthat) or `__snapshots__` (Jest, syrupy) among the paths that the
gate's diff command prints. `/milestone-review` step 7 lists each one in
both modes and settles a change that the work does not call for. Step 8's
guest arm names each one in a new PR's body, or in one comment on a PR
that is already open. `/hotfix` step 6 lists each one at the approval gate
in both modes, and its guest arm names each one in the PR body. A
D-entry, the CHANGELOG, and the README follow.

**Out:**
- A snapshot directory with another name (for example a plain
  `snapshots/`). The rule names only the two directory names above.
- Snapshot files that change after a guest PR is open by a path other
  than a review handoff: the guest hotfix change route (M266), and a
  guest Copilot round's fix commits after the create. The merged-PR
  re-entry of `/hotfix` also lists none. These go to the new candidate
  row "List snapshots changed after a PR opens".
- An owner-mode hotfix resume on an open PR that merges on the earlier
  approval with no chip lists nothing, because that PR was already
  approved with its list.
- CI failures on the maintainers' side after a guest handoff (performance
  #974, parameters #1275). These go to the new candidate row "Read guest
  PR checks while they wait".

## Acceptance criteria

- [x] AC1: `skills/milestone-review/SKILL.md` step 7 says that, in both
      modes, the presentation lists each changed snapshot file. The step
      defines one as a path with a directory named `_snaps` or
      `__snapshots__`, among the paths that
      `git diff --name-only <base>/<default-branch>...HEAD` prints on the
      head the chip is posed on, after any fix-now commits. A stacked guest
      milestone whose stack base's PR is `OPEN` diffs against
      `<base>/<stack-base-branch>`. Resume route (b) uses the paths that
      `gh pr diff <N> --name-only` prints. Each file gets one plain line.
      The line says what changed in its stored output, or that the file is
      new or deleted, and whether the Goal or acceptance criteria call for
      that change. Step 5's rule settles a change that they do not call
      for as fix now or follow-up, before the chip. A Review line
      `snapshot: <path> — <disposition>` records it, also when a fix-now
      revert removes the path from the list. An empty list is stated in
      one line.
- [x] AC2: Step 8's guest arm says that the body of a PR it opens names
      each changed snapshot file, with one plain line on what changed and
      why. The list is recomputed with AC1's command and base on the head
      that step 8 pushes. The sentence "The `edge` list and the series
      sentence below follow" names the snapshot lines first, and the
      "Beyond those items" sentence makes an exception for them. When there
      is no such file, the body has no snapshot line. When the PR is
      already open, no body edit is made, and the handoff posts the same
      lines in one PR comment. That comment is the `edge` list's comment
      when both have lines. When there is no such file, the comment has no
      snapshot line.
- [x] AC3: `skills/hotfix/SKILL.md` step 6 says that, in both modes, the
      approval gate lists each changed snapshot file of the head the gate
      shows. Where the gate shows a PR's `headRefOid`, the paths are the
      ones that `gh pr diff <N> --name-only` prints. Otherwise they are
      the ones that `git diff --name-only <base>/<default-branch>...HEAD`
      prints after `git fetch <base>`. Each file gets one plain line on
      what changed, or that it is new or deleted, and whether the fix
      needs it. The chip's question text names each change that the fix
      does not need, and the recommended option does not approve while one
      stands. The guest arm's PR body names each file with one plain line
      on what changed and why. The lines go after the failing-calls list
      where one is owed, else after the prose, and before the `Fixes #N`
      line. The sentence "The body's prose is a short description" names
      them. When there is no such file, the body has no snapshot line.
- [x] AC4: The Unreleased section of `CHANGELOG.md` has an entry on the
      snapshot list. The entry covers the review and hotfix gates and guest
      PR bodies and comments. The sweep is
      `grep -n -E 'PR body|the PR lists|guest PR' README.md cairn/DESIGN.md`
      at the review head. Each sentence among its hits that names an item
      that a guest PR body or comment includes also names the snapshot
      lines. Hits that only say what a guest body leaves out are out of
      the sweep's scope.
- [x] AC5: Run from the repo root, each of the five commands in the
      `verify` slot of `cairn/PROFILE.md` exits 0.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T5
- AC5 → T5

## Tasks

- [x] T1: Add the snapshot list to `/milestone-review` step 7 (near the
      presentation items before the PR-conversation read): the definition,
      the diff bases, the per-file line, the step-5 settling, and the
      `snapshot:` Review line.
- [x] T2: Add the snapshot lines to step 8's guest body sentences and to
      the open-PR comment beside the `edge` list.
- [x] T3: Add the snapshot list to `/hotfix` step 6's gate in both modes,
      and the snapshot lines to the guest arm's body sentence.
- [x] T4: Append a D-entry. It records the rule. Guest mode passes D-108's
      door on its retained trigger (easystats/see#486). Owner mode at both
      gates is excepted by name at the user's choice, with the door
      unchanged, as D-189 did. Its falsifier mirrors D-206's: maintainers
      who ask that such lines be left out of guest PRs.
- [x] T5: Add the CHANGELOG entry and run AC4's sweep. Hand-run
      `skills/tests` after the skill edits (lesson M148). Run the five
      `verify` commands.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — new gate conduct in two skills, not a bug fix and not a tracking-only edit.
- 2026-10-21: idea vet: (1) explaining a snapshot alone would not have caught easystats/see#486, whose change was a mistake — the user chose check then explain; (2) the row's other two PRs failed on the maintainers' CI, not on snapshots — the user chose a new candidate row.
- 2026-10-21: question set: owner mode — the user chose both modes for the gate check; the guest PR body and comment explain the changes.
- 2026-10-21: collision check: source row "Explain changed snapshots in guest PRs" absorbed in full, its CI half moved to the new row "Read guest PR checks while they wait"; M308 (archived) shipped the guest body shape this extends; D-206's `edge` list is the body and comment pattern; D-108's door applies (T4). No other ROADMAP, archive, or D-entry overlap.
- 2026-10-21: inbox sweep: jmgirard/cairn has 0 open issues and 0 open PRs.
- 2026-10-21: criteria audit (full, two passes): pass 1 returned 14 findings on the first draft, and pass 2 returned 11 on the wording revised after the question set; all are taken toward the narrower wording, except the open-PR comment's delta diff, which was not taken because the guest sync's push makes it empty, so the comment lists the full recomputed list.
- 2026-10-21: plan gate chose a fixed directory-name rule (`_snaps`, `__snapshots__`) in the skills over a new profile slot because a slot change does not reach adopted repos (lesson M274); falsified by a repo whose snapshot tool stores files under another directory name.
- 2026-10-21: plan gate chose the review gate (step 7) over the handoff (step 8) for the check, because an unneeded change must be fixable before approval; falsified by a run where the gate's list is stale at the push.
- 2026-10-21: implement started on m310-snapshot-explain, cut from main at 488fc5a4; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-21: T1 done — step 7 gains a "Changed snapshot files" paragraph before the PR-conversation read; verify green (five commands, each exit 0).
- 2026-10-21: T2 done — step 8's guest body names the snapshot lines first in the items sentence, the "Beyond those items" sentence gains an exception for them, and the open-PR comment carries them beside the `edge` list; T1's paragraph split into shorter sentences; verify green.
- 2026-10-21: T3 done — `/hotfix` step 6's gate gains a "Changed snapshot files" paragraph after the head note, and the guest body sentence puts the snapshot lines after the failing-calls list and before `Fixes #N`; implement chose "the recommended option does not approve and instead fixes that change first" for AC3's no-approve clause; verify green.
- 2026-10-21: T4 done — D-208 appended: the rule, the guest half through D-108's door on its retained trigger (easystats/see#486), the owner half excepted by name at the user's decision as D-189 did, and falsifiers for each half.
- 2026-10-21: T5 done — CHANGELOG Unreleased gains the snapshot-list entry first under "Changes that affect existing repos"; AC4 sweep hits README.md:574, 576, 736 and cairn/DESIGN.md:597, 598, 862, 984, 1146, of which only README.md:736 names items a guest body includes, and its paragraph now names the snapshot lines (the others say what a body omits or name no body item); `skills/tests` hand-run 954 tests OK; verify green.
- 2026-10-21: claim audit: 38 claims read, 1 corrected — CHANGELOG.md (the open-PR comment is review's only; `/hotfix` posts none)
- 2026-10-21: implement complete; status set to review.
- 2026-10-21: review step 3: AC2's "the comment has no snapshot line" clause was implied only; the sentence "With no such file, the comment has no snapshot line." added to step 8 before AC2's evidence line, a wording fix inside the planned change with no criterion change.

## Decisions

## Review

- 2026-10-21: copilot arm: PR #324 opened at review start; state query read `none`, request exit 0, re-query read `pending`.
- AC1 evidence (2026-10-21, head after ef316491): `skills/milestone-review/SKILL.md` lines 526-540, inside step 7 (step 7 at line 490, step 8 at 628), hold the "Changed snapshot files" paragraph: the `_snaps`/`__snapshots__` definition over `git diff --name-only <base>/<default-branch>...HEAD` (528), the `OPEN` stack-base diff (529), route (b)'s `gh pr diff <N> --name-only` (530), "In both modes" on the head after fix-now commits (531-532), one line with what changed or new/deleted and whether the Goal or criteria call for it (533-535), step 5's fix now or follow-up before the chip (535-538), the `snapshot: <path> — <disposition>` line also after a revert (539-540), and the one-line empty list (540). Read by grep for each clause.
- AC2 evidence (2026-10-21): step 8's guest arm, lines 756-778. The items sentence now reads "The snapshot lines, the `edge` list, and the series sentence below follow" (756-757), the "Beyond those items" sentence is followed by "The snapshot lines are the one exception for test files." (759), the lines are computed again with step 7's command and base on the pushed head, one plain line each on what changed and why, none when no file changed (760-764). On an already-open PR, no body edit, and one comment carries the `edge` list and the snapshot lines (771-777). The clause "With no such file, the comment has no snapshot line." was implied only and was added at review before this line (see the work log).
- AC3 evidence (2026-10-21): `skills/hotfix/SKILL.md` step 6 (line 344, step 7 at 541), lines 412-424: "In both modes, the gate lists each changed snapshot file of the head it shows", `gh pr diff <N> --name-only` where the gate shows a PR's `headRefOid` (with `--repo` in guest mode), else `git diff --name-only <base>/<default-branch>...HEAD` after `git fetch <base>`, one line with what changed or new/deleted and whether the fix needs it, the chip's question text names each unneeded change, and the recommended option does not approve while one stands. Guest arm lines 505-510: "The body's prose is a short description … then that list where one is owed, then the snapshot lines", before the `Fixes #N` line, one line each on what changed and why, none when no file changed.
- AC4 evidence (2026-10-21): `CHANGELOG.md` lines 7-19, first under Unreleased "Changes that affect existing repos", describe the list at the review and hotfix gates, the guest PR body, and review's open-PR comment. The sweep `grep -n -E 'PR body|the PR lists|guest PR' README.md cairn/DESIGN.md` hits README.md:574, 576, 736 and cairn/DESIGN.md:597, 598, 862, 984, 1146. Read in context, only README.md:736 names items a guest PR includes, and its paragraph (lines 731-738) names the snapshot lines ("It also says what changed in each snapshot file and why"). The other hits are about `Candidate row:` lines a guest body omits, the pane's PR read, or the triage token.
- AC5 evidence (2026-10-21): from the repo root, each exit code read on its own: `python3 -m unittest discover -s scripts/tests` 0, `python3 -m unittest discover -s hooks/tests` 0 (193 tests OK), `claude plugin validate .claude-plugin/plugin.json` 0, `claude plugin validate .claude-plugin/marketplace.json` 0, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` 0 (2444 pass, 0 fail).
- Consistency gate (2026-10-21, head 7fafbb87): `cairn_validate.py` exit 0, all checks passed; no DESIGN.md principle changed, so `cairn_impact` skipped; profile slot: verify green on this head (AC5), marketplace validate printed no `plugins[N].version` warning, CHANGELOG has the entry (AC4).
- spawned: diff-bug, blame-history, prior-review, ripple
