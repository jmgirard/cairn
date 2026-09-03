# M174: A merged hotfix or adopted PR is verified to the hotfix bar post-hoc

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP2
- **Resolves:** —
- **Branch/PR:** m174-post-hoc-hotfix-bar · https://github.com/jmgirard/cairn/pull/178

## Goal

A hotfix or adopted PR merged outside the session re-enters `/hotfix` through
a post-hoc verification of the merged diff — regression test, gate-lite,
changelog — so the hotfix bar holds on every path to the default branch, not
only the one the session drove.

## Scope

**Surface tier: user-facing** — `/hotfix` ships to adopting repos, so the
route's conduct is a deliverable external consumers rely on.

**In:** the merged-PR re-entry paragraph of `/hotfix` step 1
(`skills/hotfix/SKILL.md:33-41`, M172) grows from "step 7 only" into a
post-hoc verification paralleling `/milestone-review`'s merged-unreviewed
route (b): the pre-fix baseline is the merged PR's `baseRefOid` (never the
current default branch, which already carries the fix); a test the merged
diff carries is proved two ways against that baseline, and a missing one is
authored on a follow-up `hotfix-<slug>` branch; the profile's `verify` slot
runs; the changelog entry is checked; anything owed reaches the default
branch only through step 5's PR and step 6's chip; a clean check pauses at
one acceptance chip that also carries the issue close; then step 7. The
hand-run guard pins move with the wording; the live restating surfaces are
swept; a D-entry annotates D-130 and records D-108's trigger as satisfied.

**Out:** a post-hoc bar for milestone PRs merged outside the session →
already `/milestone-review` route (b) (M172). Reverting a merged fix to
re-land it through the full path → rejected at the plan gate (work log). A
merged diff over the hotfix bar → step 1's existing over-the-bar
disposition, no test demanded (AC6). Prose-guard or mutation coverage as an
obligation → none owed (D-109, `PROFILE.md` test-doctrine); T2 only re-seeds
pins the wording change would red.

## Acceptance criteria

- [x] AC1: `skills/hotfix/SKILL.md` step 1's merged-PR re-entry — a PR whose
      `gh pr view <N> --json state,headRefName` reports `MERGED` with a head
      branch not matching `m<nnn>-*` — runs a post-hoc verification of the
      merged diff before step 7, and `git grep -n -e 'runs step 7 only' -e
      'steps 2–6 skipped' -- skills ':!skills/tests'` returns nothing.
- [x] AC2: The re-entry names the pre-fix baseline for the two-way
      regression-test check as the oid `gh pr view <N> --json baseRefOid`
      reports, with the merge commit's first parent (`<mergeCommit>^`) as a
      cross-check, and states that the current default branch is never the
      baseline because it already carries the fix.
- [x] AC3: The re-entry's regression-test move follows step 3's adopting
      sequence: a test the merged diff carries is run on the up-to-date
      default branch and in a throwaway `--detach` worktree of the baseline
      created outside the repo with only the test file copied in, and must
      pass on the default branch and fail on the baseline; when the merged
      diff carries no test, or its test passes on both, a test is authored on
      a `hotfix-<slug>` branch cut from the up-to-date default branch and
      proved the same two ways; the worktree is removed either way.
- [x] AC4: The re-entry states that the two owed items — the regression
      test, and a changelog entry when the profile's `changelog` slot declares
      a file the merged diff did not update — land on a `hotfix-<slug>` branch
      cut from the up-to-date default branch (cut here when AC3's authoring
      case did not) and reach the default branch only through step 5's
      authoring variant (a new PR) and step 6's approval chip, never by a
      commit to the default branch.
- [x] AC5: When the post-hoc check finds nothing owed — test present and
      two-way proven, the profile's `verify` slot green on the default branch,
      changelog entry present or the slot `none` — the re-entry poses one
      `AskUserQuestion` chip whose question text names acceptance of the
      post-hoc verification and, when the PR body carries `Fixes #N`, the
      issue close it authorizes (the existing issue-close chip is not posed
      separately), the recommended option accepting and a decline option
      present; step 7 runs only on acceptance, and a decline stops with a
      close block naming the decline and the reason where the user gave one,
      plus a candidate row (search-first).
- [x] AC6: A merged diff the tier check finds over the hotfix bar takes step
      1's existing over-the-bar disposition with no regression test demanded
      and still runs step 7's close-out — the candidate row or
      `/milestone-plan` next command rides in that close block — and the
      re-entry says so.
- [x] AC7: The active profile's `verify` slot is clean: `python3 -m unittest
      discover -s scripts/tests` and `python3 -m unittest discover -s
      hooks/tests` each exit 0.

## Coverage

- AC1 → T1, T3
- AC2 → T1
- AC3 → T1
- AC4 → T1
- AC5 → T1
- AC6 → T1
- AC7 → T3

## Tasks

- [x] T1: Rewrite the merged-PR re-entry paragraph at
      `skills/hotfix/SKILL.md:33-41` — trigger; `baseRefOid` baseline with
      the parent cross-check; tier check with the over-the-bar close-out;
      two-way test per step 3 on the default branch and a detached
      outside-the-repo worktree, removed either way; `verify` slot; changelog
      check; follow-up branch → step 5's authoring variant → step 6's chip;
      the single acceptance chip carrying the issue close; then step 7 — and
      step 6's cross-reference at `:122`. Check each named step's
      preconditions where the route lands (M172 lesson: no PR head branch
      after `--delete-branch`, step 5's never-a-second-PR clause is about the
      merged PR). Rehearse the baseline derivation on merged hotfix PR #176 —
      `baseRefOid`, the parent cross-check, worktree add and remove — and
      record the oids in the work log. Add the `CHANGELOG.md` Unreleased
      entry.
- [x] T2: Re-seed `TestHotfixMergedPrReentry` at
      `skills/tests/test_resume_routing.py:149-175` and its two REGISTRY
      entries at `skills/tests/test_mutation_harness.py:3282-3291` to the
      shipped wording — pin the trigger, baseline, two-way check, follow-up
      path, and chip as whole lists with whitespace collapsed (M171 lesson),
      spelling no retired token (M169 lesson); hand-run `python3 -m unittest
      discover -s skills/tests` and the mutation harness (D-109: gating
      nothing).
- [x] T3: Sweep the live restating surfaces — `git grep -n -i -e 'step 7
      only' -e 'close-out step' -e 'steps 2–6 skipped' -- skills README.md
      cairn/DESIGN.md ':!skills/tests'` — and reconcile any hit (archives and
      DECISIONS are history, untouched); run both gating suites from the repo
      root and check each exit code.

## Work log

- 2026-09-03: created by /milestone-plan; absorbs the "Post-hoc hotfix bar for a PR merged outside the session" candidate row (M172 review F1); its promotion condition had not fired — promoted at user choice.
- 2026-09-03: criteria audit ran in full mode ([O] fresh reader): 8 findings — 1–7 fixed before the gate (baseline discriminator, deleted head branch, AC4 antecedent and domain, chip fold, over-the-bar close-out, grep tokens, door trigger statement); 8 (route rehearsal) placed in T1 as evidence on PR #176.
- 2026-09-03: plan gate chose a post-hoc route inside `/hotfix` step 1 over routing a merged hotfix through `/milestone-review` route (b) because a hotfix has no milestone file, criteria, or work log for that route to read; falsified by a hotfix that carries acceptance criteria.
- 2026-09-03: plan gate chose a follow-up `hotfix-<slug>` branch and PR for owed items over revert-and-redo (removes a shipped fix from the distribution channel; outward-facing) and over accept-with-candidate-row (leaves the bar unenforced); falsified by a merged diff whose test cannot be written without changing the fix.
- 2026-09-03: plan gate chose `baseRefOid` as the pre-fix baseline over the current default branch (already carries the fix, so a test passes on both and proves nothing) and over a merge-method case split (no `gh` field reports the method); falsified by a merged PR whose `baseRefOid` differs from its merge commit's first parent — equal on #170–#177 at plan time.
- 2026-09-03: plan gate chose one acceptance chip folding the issue close over none; falsified by a session where the chip carries nothing the user could decide on.
- 2026-09-03: D-108's door read as satisfied at the gate (user choice) — the route ships a hotfix without the regression test the skill's own description promises — recorded as D-131.
- 2026-09-03: T1 done — re-entry rewritten as a seven-move post-hoc verification (tier check with over-the-bar close-out; `baseRefOid` baseline with parent cross-check; two-way test on the default branch and a detached outside-the-repo worktree; `verify`; changelog; owed items via a follow-up `hotfix-<slug>` PR and step 6's chip; one acceptance chip folding the issue close, then step 7); step 6's cross-reference updated; CHANGELOG Unreleased entry added. Question gate skipped: nothing left open after the plan's criteria audit. Rehearsal on merged hotfix PR #176: `baseRefOid` 13be808f, merge commit 0a1b5b5c, `0a1b5b5c^` = 13be808f (equal); detached worktree of 13be808f added outside the repo, PR's test copied in fails there (2 failures) and passes on the default branch; worktree removed, `git worktree list` shows only the checkout.
- 2026-09-03: T2 done — `TestHotfixMergedPrReentry` re-seeded to six tests pinning trigger (plus the absence of the two retired phrases), baseline, two-way check, follow-up path, acceptance chip, and over-the-bar close-out as whole passages whitespace-collapsed; the two REGISTRY entries replaced by six, each block occurring once in `skills/hotfix/SKILL.md`; hand-run `skills/tests` (harness included) 604 OK.
- 2026-09-03: T3 done — sweep `git grep -n -i -e 'step 7 only' -e 'close-out step' -e 'steps 2–6 skipped' -- skills README.md cairn/DESIGN.md ':!skills/tests'` returns nothing (the only pre-T1 hit was the rewritten paragraph itself); both gating suites exit 0; `cairn_validate` run. Status → review.
- 2026-09-03: review checkpoint — PR #178 draft opened; AC1–AC7 evidenced and ticked; gate green; three review lenses spawned (blame-history: no findings), two lenses pending.
- 2026-09-03: review — three lenses reported (0 + 0 + 8 findings); six fixed at the gate (F1 F2 F3 F5 F6 F7), two rejected (F4 F8); pins re-seeded; suites green; approval gate next.
- 2026-09-03: step-7 approval: PR #178 approved for merge.

## Decisions

## Review

_Reviewed 2026-09-03 on branch tip 0b9d1ab, re-verified after the gate fixes, against origin/main c76146e (unmoved since the cut); PR #178 draft._

- AC1 — pass: `skills/hotfix/SKILL.md:33-37` opens the re-entry on `gh pr view <N> --json state,headRefName` reporting `MERGED` with a head not matching `m<nnn>-*` and says it "states in chat that the hotfix bar never ran before this merge, then runs a post-hoc verification of the merged diff before step 7"; `git grep -n -e 'runs step 7 only' -e 'steps 2–6 skipped' -- skills ':!skills/tests'` returns nothing (exit 1).
- AC2 — pass: the *Baseline* move (`:47-53`) names `gh pr view <N> --json baseRefOid` as the baseline, `gh pr view <N> --json mergeCommit --jq .mergeCommit.oid` then `git rev-parse <oid>^` as the cross-check with `baseRefOid` governing a disagreement, and states "The current default branch is never the baseline: it already carries the fix". Fresh run on merged hotfix PR #176: `baseRefOid` 13be808f, merge commit 0a1b5b5c, `0a1b5b5c^` = 13be808f (equal).
- AC3 — pass: the *Regression test* move (`:54-64`) follows step 3's adopting sequence — test run on the default branch, checked out and brought up to date (fetch, pull ff-only), and in `git worktree add --detach /tmp/<repo>-verify <baseRefOid>` outside the repo with only the test file copied in, pass on the default branch and fail on the baseline required; no test or passes-on-both → author on a `hotfix-<slug>` branch cut from the up-to-date default branch and prove the same two ways; `git worktree remove` either way, a failed check included.
- AC4 — pass: the *Owed items* move (`:71-80`) names the regression test and the changelog entry, lands them on the `hotfix-<slug>` branch ("cut here when the regression-test move did not"; the branch's cut point — the up-to-date default branch — is stated where the regression-test move defines it), and reaches the default branch "only through step 5's authoring variant — push, open a new PR … — and step 6's approval chip, never by a commit to the default branch".
- AC5 — pass: the *Nothing owed* move (`:81-93`) states the three clean conditions verbatim, poses one `AskUserQuestion` chip whose question text names acceptance of the post-hoc verification and the `Fixes #N` issue close (issue-close chip not posed separately), recommended option accepting, decline present; "Step 7 runs only on acceptance"; a decline "stops with a close block naming the decline and the reason where the user gave one, plus a `candidate` row (search-first)".
- AC6 — pass: the *Tier check* move (`:40-47`) sends an over-the-bar diff to "the over-the-bar disposition above with no regression test demanded, and step 7's close-out still runs — the candidate row or the `/milestone-plan` next command rides in that close block"; a `Fixes #N` close there is chip-gated before step 7 (F1 fix).
- AC7 — pass (re-run after the gate fixes): from the repo root, `python3 -m unittest discover -s scripts/tests` 329 tests OK exit 0; `python3 -m unittest discover -s hooks/tests` 121 tests OK exit 0. Hand-run (non-gating, D-109) `skills/tests` 604 OK.
- Driving RR: none — projection-vs-outcome no-ops.
- Consistency gate: `cairn_validate.py` all checks passed, exit 0 (advisories OK; `release window` silent); no DESIGN principle changed → `cairn_impact` skipped; profile `generic` names no toolchain checks. T3's sweep re-run returns nothing.
- Independent review (three lenses, fresh context): [S] blame-history — no findings (D-130 annotated not superseded, the stopped-CI-wait trigger retained, M169/M171 pin discipline kept). [S] prior-review record — probe `gh api repos/jmgirard/cairn/pulls/comments?per_page=1` returned `[]`, archive `## Review` sections and LESSONS read; no regression of M172 F1/F5/F9 or the M156/M169/M171 lessons; one soft observation, the clean-check chip does not itself say to present the verification results in chat first — rejected: the chip's question text carries the evidence per the Mandated-substance rule, and step 6's presentation clause already governs the follow-up path. [O] diff-bug — eight findings, ranked:
  - F1 (over-the-bar branch reaches step 7's unconditional `Fixes #N` close with no authorizing chip) — fix now: the *Tier check* move now chip-gates that close before step 7; outward-facing write, fixed regardless of rank.
  - F2 (a red `verify` on the default branch matched neither the owed-items nor the nothing-owed branch) — fix now: the *Gate-lite* move names a red run the merged diff introduced as a third owed item, one it did not as stated in chat and not this route's to fix.
  - F3 ("so step 7 poses no separate chip" — step 7 poses none at all) — fix now: reworded to "the re-entry poses no separate issue-close chip".
  - F4 (step 3's own worktree command lacks `--detach` and targets the default branch, so "per step 3's adopting sequence" over-claims) — rejected: an unmodified pre-existing line; step 3's command works there because the session sits on the PR head, and the re-entry carries the `--detach` form AC3 requires.
  - F5 (`gh pr view --json mergeCommit` returns an object, so `git rev-parse <mergeCommit>^` as written fails) — fix now: `--jq .mergeCommit.oid` then `git rev-parse <oid>^`.
  - F6 (the re-entry never says to check out the default branch) — fix now: "checked out and brought up to date (fetch, pull ff-only)".
  - F7 (no chat statement that the bar never ran before the merge, unlike route (b)) — fix now: added to the opening sentence.
  - F8 (`/tmp/<repo>-verify` shared with step 3 and unguarded against a stale directory) — rejected: existing step 3 conduct, guarded by the remove-either-way clause.
  Fix-now edits re-seeded four pins in `TestHotfixMergedPrReentry`; the six registry blocks each still occur once; `skills/tests` 604 OK, both gating suites exit 0, the AC1 grep still empty. No finding demonstrates a criterion failing — no return.

