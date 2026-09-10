# M182: Claim audit at implement time for user-facing prose; release-walk changelog claim-read

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the two skills edited are what the plugin does for adopting repos
- **Branch/PR:** m182-claim-audit · https://github.com/jmgirard/cairn/pull/189

## Goal

A user-facing milestone whose branch adds behavior claims to prose has those claims read against the code before review, so review confirms a recorded audit instead of being the first claim-versus-code pass and the return floor's only exit.

## Scope

**In:** (1) a claim-audit step in `/milestone-implement`, between the last task and completion, run by a fresh-context [O] reader over the branch's added prose lines, with a stopping rule and a fixed work-log line; (2) a claim-read clause in `/cairn-release` step 2; (3) the D-entry recording D-090/D-108's trigger as satisfied and the rules shipped.

**Out:** the diff-scoped second [O] review after a prose-claim return (the tidymedia proposal's part (b)) → ROADMAP candidate row, promoted only when a milestone with a recorded claim-audit pass still takes a return on branch-added prose claims; new prose guards under `skills/tests` → none (D-109: the suite gates nothing; existing guards are hand-run at T4); any change to the thrash rule, return floor, or lens routing → untouched (D-064, D-097, D-112 stand); tidymedia M120's own gate disposition → tidymedia.

## Acceptance criteria

- [x] AC1: `skills/milestone-implement/SKILL.md` carries a claim-audit step, numbered between the plan-amendments step and the completion step, whose text states: it is owed when the milestone file's `Surface tier:` slot reads `user-facing` and `git diff <default-branch>...HEAD -- . ':!cairn/'` adds lines, and otherwise not owed; a fresh-context [O] reader that authored none of those lines reads every added line of that diff and reports each claim it finds there about what an artifact does, each read against that artifact in the same session (a spawn refused under a spawn-restricting harness instruction stops the step with a close block posing it, per tracking-rules' freshness-spawns clause, never an unlogged author-inline run); its stopping rule is one pass, a claim the pass corrects re-read once by the same reader, no second pass; and its work-log line takes the fixed shape `claim audit: <N> claims read, <K> corrected — <files>` with N the claims the reader reported, or `claim audit: not owed — <reason>` with the reason the first that applies of `internal tier`, `no added lines outside cairn/`; an absent line means the reader did not run.
- [x] AC2: `skills/cairn-release/SKILL.md` step 2 carries a claim-read clause stating that each behavior claim in the consolidated release section is read against the artifact it describes before the release-prep commit, a false one corrected in that commit, and that a "none" changelog declaration skips the clause with the rest of step 2.
- [x] AC3: `cairn/DECISIONS.md` carries one new D-entry stating that D-090/D-108's trigger clause is satisfied — the shipped `/milestone-review` has no exit from the return floor on a user-facing prose milestone — citing the tidymedia M119 and M120 milestone files for the measurement and carrying no count, naming the two rules shipped and the candidate row holding part (b), and stating a falsifier for each rule.
- [x] AC4: `python3 -m unittest discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests` each exit 0, and a hand run of `python3 -m unittest discover -s skills/tests` shows no red beyond the one pre-existing lesson-graduation red the ROADMAP hygiene line records.

## Coverage

- AC1 → T2
- AC2 → T3
- AC3 → T1
- AC4 → T4

## Tasks

- [x] T1: Append the D-entry (AC3) to `cairn/DECISIONS.md` and add the part-(b) candidate row to `cairn/ROADMAP.md` if the plan commit did not; the entry lands first so T2 and T3 are inside the door.
- [x] T2: Insert the claim-audit step in `skills/milestone-implement/SKILL.md` after step 6 (plan amendments) and before completion (currently step 8, `skills/milestone-implement/SKILL.md:169`), renumbering the steps that follow; keep step 4's derived-claims pointer sentence byte-identical (pinned by `skills/tests/test_derived_claims.py:72`).
- [x] T3: Add the claim-read clause to `skills/cairn-release/SKILL.md` step 2 (`skills/cairn-release/SKILL.md:54`).
- [x] T4: Run both gating suites; hand-run `skills/tests` and compare its reds to the ROADMAP hygiene line; `git grep -n "three-lens\|derived-claims" README.md docs` to confirm no restated doctrine went stale (M112 lesson).

## Work log

- 2026-09-10: created by /milestone-plan from the tidymedia session's cross-session proposal (M119/M120 review-loop failure).
- 2026-09-10: criteria audit (full): five findings — AC3 bound a reading act, AC1 used grep-as-evidence and a recall-defined file family, AC2 (the part-(b) criterion) had a two-referent clause and contradicted the [O] lens definition and D-112, AC4 directed counts into the D-entry (D-116 part 2), and the set sits behind D-108's door; the first four fixed at the gate, the fifth posed and answered proceed; the part-(b) criterion then left the milestone for a candidate row at the gate.
- 2026-09-10: re-audit: AC1 (full) — four findings: the claim domain was recall-defined (repaired: the reader sweeps every added line and N is what it reported), a refused spawn had no gate to surface at (repaired: the step stops with a close block per freshness-spawns), the not-owed reasons could both apply (repaired: first-that-applies order), and the step is owed at N=0 for a user-facing diff adding only code (accepted: one cheap spawn beats a recall-defined file filter); the instrument observation stands as the skill text being the deliverable. Further churn on AC1 goes to the user.
- 2026-09-10: plan gate chose a fresh-context [O] reader for the claim audit over the author's own re-read because the author's read is the instrument measured to fail (M114; tidymedia M120 passed its criteria twice under it); falsified by a claim-audit pass whose reader clears a claim review then returns on.
- 2026-09-10: plan gate chose a candidate row for the diff-scoped second review over shipping it now because (a) removes most of its need and its safety is unmeasured; falsified by a milestone with a recorded claim-audit pass still taking a return on branch-added prose claims.
- 2026-09-10: T1 — D-136 appended (door passed on the retained trigger, two rules named, part (b) left on its candidate row, a falsifier per rule); the part-(b) candidate row already landed with the plan commit, so ROADMAP was not touched.
- 2026-09-10: T2 — claim-audit step inserted as `/milestone-implement` step 7, Blocked and Completion renumbered 8 and 9; no other skill or test cites those two numbers; step 4's derived-claims sentence untouched; scripts + hooks suites exit 0.
- 2026-09-10: T3 — claim-read clause added to `/cairn-release` step 2, keyed to the release-prep commit, skipped with the step on a "none" declaration; scripts + hooks suites exit 0.
- 2026-09-10: T4 — scripts and hooks suites exit 0; skills/tests hand-run: 661 tests, one red, `test_lesson_graduation.TestFamilyActuallyLeft.test_partial_coverage_was_trimmed_not_deleted`, the pre-existing lesson-graduation red the ROADMAP hygiene line records; README.md's one `three-lens` mention (line 116) still matches the review skill and no `docs/` directory exists.
- 2026-09-10: claim audit: 12 claims read, 1 corrected — skills/milestone-implement/SKILL.md, skills/cairn-release/SKILL.md (step 7 run on this branch as it now reads: user-facing tier, two skill files added outside `cairn/`; the corrected claim was step 7's closing sentence, which said review confirms the recorded audit while the branch changes nothing in the review skill).
- 2026-09-10: the corrected claim's one re-read went to a second fresh [O] reader, not the same one — SendMessage is unavailable in this session, so the original reader could not be continued; deviation logged, not silent. The re-read held on placement and returned on the word "first" (step 4's derived-claims rule already has the author read the artifact at writing time); reworded to "the first read … by a reader other than their author"; no further reader spawned, per the stopping rule.

- 2026-09-10: review found `skills/tests/test_positional_labels.py:153` still anchoring on the old `7. **Blocked?**` heading (the `section()` helper ran to EOF silently, so the suite stayed green); anchor moved to `8.` at the gate. This supersedes T2's line saying no test cites those numbers.

## Decisions

## Review

- 2026-09-10 AC1: `skills/milestone-implement/SKILL.md` read on the branch: step 7 **Claim audit** sits between step 6 (Plan amendments) and step 9 (Completion), Blocked renumbered 8. Its text states the owed condition (`Surface tier:` = `user-facing` and `git diff <default-branch>...HEAD -- . ':!cairn/'` adds lines; otherwise not owed), the fresh-context [O] reader authoring none of the lines, every added line read, each claim reported and read against its artifact in the same session, the refused-spawn stop with a close block per freshness-spawns, the one-pass/one-re-read stopping rule, and both fixed work-log shapes with the first-that-applies reason order and the absent-line meaning. `grep` over skills/hooks/scripts/README finds no other file citing the old step numbers. Verified.
- 2026-09-10 AC2: `skills/cairn-release/SKILL.md` step 2 read on the branch: a **Claim-read** clause reads each behavior claim in the consolidated release section against the artifact it describes before the release-prep commit, corrects a false one in that commit, and is skipped by a "none" declaration with the rest of the step. Verified.
- 2026-09-10 AC3: D-136 read whole: states D-090/D-108's trigger satisfied (the review has no exit from the return floor on a user-facing prose milestone), cites tidymedia M119 and M120 milestone files for the measurement, names the two rules and the "Diff-scoped second review after a prose-claim return" candidate row for part (b), gives a falsifier per rule; a digit scan of the entry finds only record ids and dates, no count. Verified.
- 2026-09-10 AC4: scripts suite 379 tests exit 0; hooks suite 126 tests exit 0; skills/tests hand-run 661 tests, one red (`test_lesson_graduation.TestFamilyActuallyLeft.test_partial_coverage_was_trimmed_not_deleted`), the pre-existing red the ROADMAP hygiene line records. Verified.
- 2026-09-10 Driving RR: none; projection-vs-outcome no-ops.
- 2026-09-10 consistency gate: `cairn_validate.py` exit 0, all checks pass; no DESIGN principle changed, `cairn_impact` skipped; profile `generic` names no toolchain checks.
- 2026-09-10 correction: the AC1 evidence line's "no other file citing the old step numbers" was wrong — `skills/tests/test_positional_labels.py:153` anchored on the old heading; fixed at the gate (below), the AC1 verdict stands since AC1 names no cross-reference condition.
- 2026-09-10 independent review (three lenses, user-facing tier): [O] diff-bug 10 findings; [S] blame-history 2 findings (3 no-conflict notes); [S] prior-review-record: no regression, PR-comment probe empty. Triage:
- O1 stale test anchor `test_positional_labels.py:153` — fix now (anchor → `8. **Blocked?**`; skills/tests hand-run: same single pre-existing red; scripts + hooks exit 0).
- O2 same-reader re-read unexecutable without agent continuation; O3 "release-prep commit" anchored only by the generic release-walk; O5 unfilled `Surface tier:` slot fits neither not-owed reason — follow-up: one candidate row "Claim-audit and claim-read edge cases" (search-first: none existed).
- O4 "M120 twice over the same prose" in D-136 as a count against AC3 — put to the maintainer at the gate.
- O6 audit work-log line carries a parenthetical past `<files>` — reject: the line is history (append-only); the promotion condition reads the `claim audit:` prefix and N, both intact.
- O7 audit numbered before Blocked — reject: AC1 places it between plan amendments and completion, the plan's placement.
- O8 D-entries 2107/2642 cite the old step 8 — reject: history, append-only, and the cited module is retired.
- O9 "first read by a reader other than their author" arguable under step 5 — reject: step 5 verifies subagent diffs, not claims against code.
- O10 "none" skip restated inside the clause — reject: AC2 requires the clause to state it.
- S1/S2 D-136's measurement cites tidymedia files a reader of this repo cannot check; door passed on an argument about review's control flow — reject: AC3 mandates citing those files; D-136 discloses the repo and date; the door's terms are unchanged.
- 2026-09-10 PR conversation read (PR #189): 0 reviews, 0 comments, 0 unresolved threads.
