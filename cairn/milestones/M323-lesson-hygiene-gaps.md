# M323: Close the leftover lesson hygiene gaps

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — review hygiene, `/cairn-triage lessons`, and the `/milestone` audit run in adopters' repos, guest repos included
- **Branch/PR:** m323-lesson-hygiene-gaps

## Goal

Review hygiene, `/cairn-triage lessons`, and the `/milestone` audit stop losing lesson text, use marks, and waiting lines in either mode, and D-221's false rejection reason is corrected.

## Scope

**In:** (1) Review step 9 deletes the live milestone file and then sets the ROADMAP row `done` at the end of the pass, so the use marks, the unpark check, retirement, and eviction read the live file on disk in both modes, and the `git show HEAD:` read goes. Step 9 says the milestone under review is not a live milestone in its own pass. (2) In guest mode, the triage lessons pass and review hygiene quote in their close blocks the pre-edit text of each lesson they compress, split, correct, shorten, or trim. (3) The `/milestone` audit's weight-cap check names each `- waiting` line. (4) One D-entry corrects D-221's Rejected clause and records the quoting. (5) The CHANGELOG, DESIGN.md's Known issues entry, and the hand-run prose guards follow.

**Out:** the parked row "Match lesson citations after use marks" stays a candidate row. The other `/cairn-triage` gaps in DESIGN.md's Known issues entry stay there. A pin search that finds tests building the `LESSONS.md` path stays in that entry.

## Acceptance criteria

- [ ] AC1: In `skills/milestone-review/SKILL.md` step 9 (from its `9. **Post-merge hygiene pass` line to the `10.` step), the instruction that deletes the live `cairn/milestones/M<NNN>-<slug>.md`, and after it the instruction that sets the ROADMAP row to `done` with the archive path, come after the `**Capture durable lessons:**`, `**Unpark the rows this merge readied:**`, and `**Retire what this milestone covered:**` run-ins and the rank eviction, and before the `cairn_validate.py` run. Step 9 holds no sentence saying the live file is already deleted before that point, and it states that the milestone under review is not a live milestone in its own pass. `git grep -n 'git show HEAD:' -- skills/milestone-review/SKILL.md` returns no match.
- [ ] AC2: In guest mode, two close blocks quote pre-edit lesson text in full. `/cairn-triage lessons` (`skills/cairn-triage/SKILL.md` step 5) quotes each lesson's line as it stood before the pass compressed, split, or corrected it, and each merge survivor's line before the merge changed it, beside its quotes of dropped and merged-away lines. Review hygiene (`skills/milestone-review/SKILL.md` step 9) quotes each lesson's line as it stood before a `used` mark forced its shortening or a partial retirement trimmed it, beside its quotes of retired and evicted lessons.
- [ ] AC3: The weight-cap check in `skills/milestone/SKILL.md` §2 names each line of `cairn/LESSONS.md` that opens with `- waiting ` and a `YYYY-MM-DD` date, by its date and provenance, as a finding for the user, with one fenced `/cairn-triage lessons` for all of them, and names no waiting-line finding when the file holds none.
- [ ] AC4: `cairn/DECISIONS.md` gains one entry, and `git diff main...HEAD -- cairn/DECISIONS.md` shows only added lines. The entry (a) states that D-221's Rejected premise is false, because review writes a waiting line whenever too few lessons can go to leave 25, and gives a rejection rationale that does not depend on that premise, superseding that clause; (b) extends D-221 (4) and D-219 (5) to the pre-edit quoting AC2 adds; (c) annotates D-159 for step 9's new order.
- [ ] AC5: The CHANGELOG `## Unreleased` lessons entry names AC2's guest pre-edit quotes in its sentence that begins "In guest mode `cairn/LESSONS.md` has no git copy", and names AC3's waiting-line report. The `cairn/DESIGN.md` Known issues entry on `/cairn-triage` gaps, which says the close block quotes each dropped or merged-away lesson, names the pre-edit quotes too. Each hit of `git grep -n -e 'merges away' -e 'quotes each removed lesson' -e 'git show HEAD:cairn' -- README.md CHANGELOG.md skills cairn/DESIGN.md ':!skills/tests'` states the rule as this milestone leaves it.

## Coverage

- AC1 → T1, T6
- AC2 → T2, T6
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: Reorder `skills/milestone-review/SKILL.md` step 9 (~866-1000): move the live-file deletion, then the ROADMAP row update, to just before the `cairn_validate.py` run; rewrite the read-before-deletion sentence (~880) and the unpark read (~943) to read the live file; add the not-live sentence by the live-milestone definition (~980). Check that the archived-file arm (~41-62) stays true of the new order. Update the guards that pin the moved text: `skills/tests/test_lessons_loop.py` (~106-116), `skills/tests/test_mutation_harness.py` (~5153), `skills/tests/test_budget_first_drafting.py` (~86).
- [x] T2: Add the guest pre-edit quotes to `skills/cairn-triage/SKILL.md` step 5 (~286-289) and to review step 9's guest sentence (~990); update the pins in `skills/tests/test_triage_lessons.py` (~452) and `skills/tests/test_lessons_loop.py` (~194).
- [x] T3: Add the waiting-line report to the weight-cap hand check in `skills/milestone/SKILL.md` §2 (~83-89).
- [x] T4: Append the D-entry of AC4 to `cairn/DECISIONS.md`.
- [x] T5: Update the CHANGELOG Unreleased lessons entry (~7-27) and the DESIGN.md Known issues entry (~1019-1025); run AC5's grep and fix each stale hit.
- [x] T6: Run the `verify` slot (both gating suites, `claude plugin validate`, `claude plugin test`), hand-run `skills/tests`, and run `cairn_validate.py`.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: not run — work named at the question set.
- 2026-10-25: question set: work chosen — candidate row "Close the leftover lesson hygiene gaps"; run goes on to implement.
- 2026-10-25: idea vet: no concern found — each gap is a real loss or a failed read in shipped skill conduct, and each fix does what its name says in both modes.
- 2026-10-25: lessons used: 2026-07-16 (M56+M65), 2026-07-24 (M112), 2026-08-17 (M148), 2026-08-22 (M152), 2026-10-18 (M275).
- 2026-10-25: collision: candidate row "Close the leftover lesson hygiene gaps" absorbed in full; D-221's Rejected clause superseded by the AC4 entry; D-108's door passed on its retained trigger, since guest triage and review lose lesson text and a guest review's unpark read fails, defects in what the skills do for users; checker-regress shape not hit, since AC3 adds a report of pending work, not a check of an artifact's correctness.
- 2026-10-25: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-25: criteria audit (full, Opus): 6 findings, all taken — ROADMAP row update moves to the end with the deletion (else a new stop state commits half a pass and the archived-file arm cannot fire); AC2 adds the partial-retirement trim and names retired and evicted lessons; AC1 names its run-in anchors and bars a stale "already deleted" sentence; AC1 states the target is not live in its own pass; AC4 reworded and uses a three-dot diff; AC5 names the CHANGELOG sentence and greps `merges away`. AC3's fence made one for all lines.
- 2026-10-25: plan gate chose moving the deletion and row update to the end of step 9 over noting the unpark inputs before the deletion because the move also closes the lost-marks gap with no new state to carry; falsified by a hygiene pass that needs the live file gone before a later step 9 instruction.
- 2026-10-25: plan gate chose updating the existing prose guards over adding new guards because the changed sentences are already pinned and D-109 keeps `skills/tests` hand-run; falsified by a changed rule here that a later edit drops with every guard green.
- 2026-10-25: implement started on branch m323-lesson-hygiene-gaps; untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-25: T1 done: step 9 writes the archive first and deletes the live file, then sets the row `done`, last before validate; unpark reads the live file; not-live sentence added; guards in test_lessons_loop, test_budget_first_drafting, and the mutation registry updated, and new guards added for the order and the not-live sentence (a minor departure from the plan's no-new-guards choice, since both sit in the guarded lessons region).
- 2026-10-25: checkpoint: T3 (audit waiting-line report, with a guard) and T4 (D-223) written but not yet checked off; verify run 4 of 5 green (both suites, both plugin validates), `claude plugin test` still running at this commit.
- 2026-10-25: T2 done: guest pre-edit quotes added to triage step 5 and review step 9 (review names retired and evicted lessons); pins updated in test_triage_lessons and test_lessons_loop, two mutation entries added; mutation harness green.
- 2026-10-25: T5 done: CHANGELOG Unreleased lessons entry names the pre-edit quotes and the audit's waiting-line report, and a new Fixes entry names the step-9 order; DESIGN.md Known issues entry names the pre-edit quotes; AC5's grep returns 3 hits, each stating the new rule.
- 2026-10-25: T6 done: verify 5 of 5 green (`claude plugin test` green at 2d7a9377, no `hooks/` or `scripts/` change since; the other four rerun green at b2665df1); `skills/tests` 979 tests OK after the last edit; `cairn_validate` green.
- 2026-10-25: claim audit: 28 claims read, 2 corrected — skills/milestone-review/SKILL.md (ROADMAP byte check re-measured after the row edit), CHANGELOG.md (Fixes entry order), skills/tests/test_mutation_harness.py (comment); the corrected claims re-read true.
- 2026-10-25: open concern for review: a pass stopped after the archive write and before the deletion leaves both files and a row not yet `done`; the archived-file arm does not fire and a rerun of step 9 could capture lessons twice. Not filed as a row here: ROADMAP is at 23,923 of 24,000 bytes.

## Decisions

## Review
