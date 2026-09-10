# M182: Claim audit at implement time for user-facing prose; release-walk changelog claim-read

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the two skills edited are what the plugin does for adopting repos
- **Branch/PR:** m182-claim-audit

## Goal

A user-facing milestone whose branch adds behavior claims to prose has those claims read against the code before review, so review confirms a recorded audit instead of being the first claim-versus-code pass and the return floor's only exit.

## Scope

**In:** (1) a claim-audit step in `/milestone-implement`, between the last task and completion, run by a fresh-context [O] reader over the branch's added prose lines, with a stopping rule and a fixed work-log line; (2) a claim-read clause in `/cairn-release` step 2; (3) the D-entry recording D-090/D-108's trigger as satisfied and the rules shipped.

**Out:** the diff-scoped second [O] review after a prose-claim return (the tidymedia proposal's part (b)) → ROADMAP candidate row, promoted only when a milestone with a recorded claim-audit pass still takes a return on branch-added prose claims; new prose guards under `skills/tests` → none (D-109: the suite gates nothing; existing guards are hand-run at T4); any change to the thrash rule, return floor, or lens routing → untouched (D-064, D-097, D-112 stand); tidymedia M120's own gate disposition → tidymedia.

## Acceptance criteria

- [ ] AC1: `skills/milestone-implement/SKILL.md` carries a claim-audit step, numbered between the plan-amendments step and the completion step, whose text states: it is owed when the milestone file's `Surface tier:` slot reads `user-facing` and `git diff <default-branch>...HEAD -- . ':!cairn/'` adds lines, and otherwise not owed; a fresh-context [O] reader that authored none of those lines reads every added line of that diff and reports each claim it finds there about what an artifact does, each read against that artifact in the same session (a spawn refused under a spawn-restricting harness instruction stops the step with a close block posing it, per tracking-rules' freshness-spawns clause, never an unlogged author-inline run); its stopping rule is one pass, a claim the pass corrects re-read once by the same reader, no second pass; and its work-log line takes the fixed shape `claim audit: <N> claims read, <K> corrected — <files>` with N the claims the reader reported, or `claim audit: not owed — <reason>` with the reason the first that applies of `internal tier`, `no added lines outside cairn/`; an absent line means the reader did not run.
- [ ] AC2: `skills/cairn-release/SKILL.md` step 2 carries a claim-read clause stating that each behavior claim in the consolidated release section is read against the artifact it describes before the release-prep commit, a false one corrected in that commit, and that a "none" changelog declaration skips the clause with the rest of step 2.
- [ ] AC3: `cairn/DECISIONS.md` carries one new D-entry stating that D-090/D-108's trigger clause is satisfied — the shipped `/milestone-review` has no exit from the return floor on a user-facing prose milestone — citing the tidymedia M119 and M120 milestone files for the measurement and carrying no count, naming the two rules shipped and the candidate row holding part (b), and stating a falsifier for each rule.
- [ ] AC4: `python3 -m unittest discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests` each exit 0, and a hand run of `python3 -m unittest discover -s skills/tests` shows no red beyond the one pre-existing lesson-graduation red the ROADMAP hygiene line records.

## Coverage

- AC1 → T2
- AC2 → T3
- AC3 → T1
- AC4 → T4

## Tasks

- [x] T1: Append the D-entry (AC3) to `cairn/DECISIONS.md` and add the part-(b) candidate row to `cairn/ROADMAP.md` if the plan commit did not; the entry lands first so T2 and T3 are inside the door.
- [x] T2: Insert the claim-audit step in `skills/milestone-implement/SKILL.md` after step 6 (plan amendments) and before completion (currently step 8, `skills/milestone-implement/SKILL.md:169`), renumbering the steps that follow; keep step 4's derived-claims pointer sentence byte-identical (pinned by `skills/tests/test_derived_claims.py:72`).
- [ ] T3: Add the claim-read clause to `skills/cairn-release/SKILL.md` step 2 (`skills/cairn-release/SKILL.md:54`).
- [ ] T4: Run both gating suites; hand-run `skills/tests` and compare its reds to the ROADMAP hygiene line; `git grep -n "three-lens\|derived-claims" README.md docs` to confirm no restated doctrine went stale (M112 lesson).

## Work log

- 2026-09-10: created by /milestone-plan from the tidymedia session's cross-session proposal (M119/M120 review-loop failure).
- 2026-09-10: criteria audit (full): five findings — AC3 bound a reading act, AC1 used grep-as-evidence and a recall-defined file family, AC2 (the part-(b) criterion) had a two-referent clause and contradicted the [O] lens definition and D-112, AC4 directed counts into the D-entry (D-116 part 2), and the set sits behind D-108's door; the first four fixed at the gate, the fifth posed and answered proceed; the part-(b) criterion then left the milestone for a candidate row at the gate.
- 2026-09-10: re-audit: AC1 (full) — four findings: the claim domain was recall-defined (repaired: the reader sweeps every added line and N is what it reported), a refused spawn had no gate to surface at (repaired: the step stops with a close block per freshness-spawns), the not-owed reasons could both apply (repaired: first-that-applies order), and the step is owed at N=0 for a user-facing diff adding only code (accepted: one cheap spawn beats a recall-defined file filter); the instrument observation stands as the skill text being the deliverable. Further churn on AC1 goes to the user.
- 2026-09-10: plan gate chose a fresh-context [O] reader for the claim audit over the author's own re-read because the author's read is the instrument measured to fail (M114; tidymedia M120 passed its criteria twice under it); falsified by a claim-audit pass whose reader clears a claim review then returns on.
- 2026-09-10: plan gate chose a candidate row for the diff-scoped second review over shipping it now because (a) removes most of its need and its safety is unmeasured; falsified by a milestone with a recorded claim-audit pass still taking a return on branch-added prose claims.
- 2026-09-10: T1 — D-136 appended (door passed on the retained trigger, two rules named, part (b) left on its candidate row, a falsifier per rule); the part-(b) candidate row already landed with the plan commit, so ROADMAP was not touched.
- 2026-09-10: T2 — claim-audit step inserted as `/milestone-implement` step 7, Blocked and Completion renumbered 8 and 9; no other skill or test cites those two numbers; step 4's derived-claims sentence untouched; scripts + hooks suites exit 0.

## Decisions

## Review
