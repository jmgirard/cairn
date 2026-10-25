# M323: Close the leftover lesson hygiene gaps

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — review hygiene, `/cairn-triage lessons`, and the `/milestone` audit run in adopters' repos, guest repos included
- **Branch/PR:** m323-lesson-hygiene-gaps https://github.com/jmgirard/cairn/pull/336

## Goal

Review hygiene, `/cairn-triage lessons`, and the `/milestone` audit stop losing lesson text, use marks, and waiting lines in either mode, and D-221's false rejection reason is corrected.

## Scope

**In:** (1) Review step 9 deletes the live milestone file and then sets the ROADMAP row `done` at the end of the pass, so the use marks, the unpark check, retirement, and eviction read the live file on disk in both modes, and the `git show HEAD:` read goes. Step 9 says the milestone under review is not a live milestone in its own pass. (2) In guest mode, the triage lessons pass and review hygiene quote in their close blocks the pre-edit text of each lesson they compress, split, correct, shorten, or trim. (3) The `/milestone` audit's weight-cap check names each `- waiting` line. (4) One D-entry corrects D-221's Rejected clause and records the quoting. (5) The CHANGELOG, DESIGN.md's Known issues entry, and the hand-run prose guards follow.

**Out:** the parked row "Match lesson citations after use marks" stays a candidate row. The other `/cairn-triage` gaps in DESIGN.md's Known issues entry stay there. A pin search that finds tests building the `LESSONS.md` path stays in that entry.

## Acceptance criteria

- [x] AC1: In `skills/milestone-review/SKILL.md` step 9 (from its `9. **Post-merge hygiene pass` line to the `10.` step), the instruction that deletes the live `cairn/milestones/M<NNN>-<slug>.md`, and after it the instruction that sets the ROADMAP row to `done` with the archive path, come after the `**Capture durable lessons:**`, `**Unpark the rows this merge readied:**`, and `**Retire what this milestone covered:**` run-ins and the rank eviction, and before the `cairn_validate.py` run. Step 9 holds no sentence saying the live file is already deleted before that point, and it states that the milestone under review is not a live milestone in its own pass. `git grep -n 'git show HEAD:' -- skills/milestone-review/SKILL.md` returns no match.
- [x] AC2: In guest mode, two close blocks quote pre-edit lesson text in full. `/cairn-triage lessons` (`skills/cairn-triage/SKILL.md` step 5) quotes each lesson's line as it stood before the pass compressed, split, or corrected it, and each merge survivor's line before the merge changed it, beside its quotes of dropped and merged-away lines. Review hygiene (`skills/milestone-review/SKILL.md` step 9) quotes each lesson's line as it stood before a `used` mark forced its shortening or a partial retirement trimmed it, beside its quotes of retired and evicted lessons.
- [x] AC3: The weight-cap check in `skills/milestone/SKILL.md` §2 names each line of `cairn/LESSONS.md` that opens with `- waiting ` and a `YYYY-MM-DD` date, by its date and provenance, as a finding for the user, with one fenced `/cairn-triage lessons` for all of them, and names no waiting-line finding when the file holds none.
- [x] AC4: `cairn/DECISIONS.md` gains one entry, and `git diff main...HEAD -- cairn/DECISIONS.md` shows only added lines. The entry (a) states that D-221's Rejected premise is false, because review writes a waiting line whenever too few lessons can go to leave 25, and gives a rejection rationale that does not depend on that premise, superseding that clause; (b) extends D-221 (4) and D-219 (5) to the pre-edit quoting AC2 adds; (c) annotates D-159 for step 9's new order.
- [x] AC5: The CHANGELOG `## Unreleased` lessons entry names AC2's guest pre-edit quotes in its sentence that begins "In guest mode `cairn/LESSONS.md` has no git copy", and names AC3's waiting-line report. The `cairn/DESIGN.md` Known issues entry on `/cairn-triage` gaps, which says the close block quotes each dropped or merged-away lesson, names the pre-edit quotes too. Each hit of `git grep -n -e 'merges away' -e 'quotes each removed lesson' -e 'git show HEAD:cairn' -- README.md CHANGELOG.md skills cairn/DESIGN.md ':!skills/tests'` states the rule as this milestone leaves it.

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

- 2026-10-25 (pass 1, head c9e7ce7a, branch synced: 0 commits behind origin/main): copilot: request on PR #336 may not be recorded by GitHub (used-up Copilot credits are one cause); state query read `none` after a zero-exit request; no second request.
- AC1: step 9 read flat, positions in order Capture 2318 < Unpark 4515 < Retire 5444 < "When too few lessons can be removed to leave 25" 7182 < "**delete the live" 8215 < "then set its ROADMAP row → `done` + archive path" 8276 < "Then run `python3" 9060; not-live sentence present; no "already deleted" / "after the deletion" / "before the deletion" / "is deleted below" phrase in step 9; `git grep -n 'git show HEAD:' -- skills/milestone-review/SKILL.md` exit 1, no match.
- AC2: triage step 5 holds "It also quotes in full each lesson's line as it stood before the pass compressed, split, or corrected it, and each merge survivor's line as it stood before the merge changed it." beside "drops or merges away"; review step 9 holds "retired and evicted alike" and "It also quotes in full each lesson's line as it stood before a `used` mark forced its shortening or a partial retirement trimmed it."
- AC3: `skills/milestone/SKILL.md` §2 defines a waiting line ("opens with `- waiting ` and a `YYYY-MM-DD` date"), names each by date and provenance with one fenced `/cairn-triage lessons` for all, and "A file with no waiting line gets no such finding."
- AC4: `git diff main...HEAD -- cairn/DECISIONS.md`: 0 removed lines, 39 added; one new entry, D-223, whose Decision (3) states D-221's Rejected premise false and gives a reason that does not rest on it, (2) extends D-221 (4) and D-219 (5), and heading and Consequences annotate D-159.
- AC5: CHANGELOG sentence beginning "In guest mode `cairn/LESSONS.md` has no git copy" now adds "When they shorten, split, correct, trim, or merge a lesson, both also quote its old line. The `/milestone` audit names each waiting line…"; DESIGN.md Known issues entry adds "and each lesson's line before a compress, split, correct, or merge changed it"; AC5 grep: 3 hits (CHANGELOG.md:24, skills/cairn-triage/SKILL.md:289, skills/milestone-review/SKILL.md:988), each stating the new rule.
- gate: `cairn_validate` exit 0, all checks passed; coverage complete (in validate); no DESIGN principle changed, `cairn_impact` skipped.
- gate (profile): scripts/tests exit 0, hooks/tests exit 0, plugin validate exit 0, marketplace validate exit 0 with no `plugins[N].version` warning; `claude plugin test` running on the review head (pass-1 result line follows); CHANGELOG Unreleased carries the lessons-entry edit and a Fixes entry, no milestone numbers in that text.
- gate (profile, pass 1): `claude plugin test` on c9e7ce7a exit 0, 2466 pass, 0 fail.
- spawned: diff-bug, blame-history, prior-review, ripple
- blame-history #1: a stop between capture and the deletion reruns step 9 and could capture lessons twice — fix now (not load-bearing: a duplicate line after a mid-pass stop), fixed 648bb61a: a rerun captures no lesson and writes no waiting line the file already holds.
- blame-history #2: the ROADMAP byte re-measure after the row edit names no remedy — fix now, fixed 648bb61a: over budget, apply the tracking-rules remedy before the commit.
- diff-bug #1: a stop between the archive write (start) and the deletion (end) leaves both files, the arm does not fire, and a rerun rewrites the archive and repeats capture — fix now (not load-bearing: only a pass stopped mid-hygiene, recovered on rerun), fixed ad0cbf85: the archive summary is now written last of the edits, just before the deletion, so a stopped pass leaves only the live file; with blame-history #1's guard a rerun repeats no capture.
- diff-bug #2: the audit's mechanical fix of the live-plus-archived FAIL could delete a file mid-pass — fix now, fixed ad0cbf85 by #1's change (that state again lasts only between two adjacent edits).
- diff-bug #3: the byte re-measure names no remedy — fix now, fixed 648bb61a (same as blame-history #2).
- diff-bug #4: the arm's recap calls lesson, mark, and RB/RR work "skipped" though under the new order the earlier pass ran it — fix now, fixed ad0cbf85: the arm and README.md now say "not rerun".
- diff-bug #5: the arm's step-9 parts list runs the cap checks before its row update — fix now, fixed ad0cbf85: "the cap and budget checks, run after the row update".
- diff-bug #6: the CHANGELOG said "both" passes shorten, split, correct, trim, and merge — fix now, fixed ad0cbf85: triage's and review's edits named apart.
- diff-bug #7: DESIGN.md's triage Known issues entry does not name review's pre-edit quotes — reject (planned change: AC5 named that entry, which covers triage gaps).
- diff-bug #8: triage `promote` is not in the guest quote rule — reject (false: a promote graduates the family into a doctrine module, so its text survives on disk).
- diff-bug #9: the extended read-before-deletion test checks several orders with bare assertLess — reject (moot: the added order checks were removed under prior-review #1).
- diff-bug #10: the audit guard sits in a review class — reject (moot: the guard was removed under prior-review #1).
- diff-bug #11: two new mutation comments cite M323 — reject (moot: both entries were removed under prior-review #1).
- diff-bug #12: test_budget_first_drafting's docstring is narrative bug history — follow-up (pre-existing, unmodified line): absorbed into the parked row "Check bare milestone ids in tests" at hygiene.
- blame-history (pass 1): 2 findings, settled above as blame-history #1 and #2.
- prior-review #1: the diff added prose guards and mutation entries for new rules, which cairn/PROFILE.md's test-doctrine says a new skill rule does not owe (M144, D-109) — fix now, fixed ad0cbf85: removed the new tests (order loop, not-live, audit) and five new mutation entries; kept the edits that existing pins needed.
- prior-review #2: the guest quote of every pre-edit line has no count bound — reject (false: it is a chat close block with no line cap, the shape D-219 (5) and D-221 (4) already use).
- prior-review #3: the audit restated the waiting-line definition, a fifth site — fix now, fixed ad0cbf85: it now points at tracking-rules "Weight caps".
- prior-review #4: DESIGN.md restates the close-block quote rule — reject (planned change: AC5 asked for it).
- prior-review #5: long prose lines in DESIGN.md and the review skill — reject (style).
- ripple #1: the arm and README describe only the deleted-file stop state — fix now, fixed ad0cbf85 by diff-bug #1's change and the README "not rerun" edit.
- ripple #2: DESIGN.md omits review's guest quotes — reject (planned change, as diff-bug #7).
- ripple #3: triage's guest quote rule skips `admit` — reject (false: admit only removes the `waiting ` word, so the text stays on disk).
- ripple #4: ROADMAP's candidate row still lists the gaps — reject (planned change: step 9 hygiene graduates the row).
- ripple #5: /milestone's close-block examples do not name `/cairn-triage lessons` — reject (false: those are examples, and the audit text fences the command itself).
- AC1 (re-read after the fix-now commits, head 651af2d7): step 9 positions Capture 1921 < Unpark 4259 < Retire 5188 < "When too few lessons can be removed to leave 25" 6926 < archive summary write 7940 < "**delete the live" 8407 < row update 8468 < "Then run `python3" 9325; the only "before the deletion" phrase is the rerun guard's "after a stop before the deletion", which says nothing is deleted yet; not-live sentence present; `git grep 'git show HEAD:'` exit 1.
- AC5 (re-read, head 651af2d7): grep 3 hits (CHANGELOG.md:24, skills/cairn-triage/SKILL.md:289, skills/milestone-review/SKILL.md:982), each stating the new rule.
- gate (head 651af2d7): `cairn_validate` exit 0; scripts/tests and hooks/tests exit 0; both plugin validates exit 0, no version warning; no `hooks/` or `scripts/` change on the branch, so the pass-1 `claude plugin test` green stands; skills/tests OK.
- conversation: PR #336 — read empty (0 reviews, 0 comments, 0 unresolved threads).
- copilot: state query on PR #336 still reads `none`; no Copilot review exists, because GitHub did not record the request (the pass-1 not-recorded line); no comment, no resolves.
- 2026-10-25: step-7 approval: m323-lesson-hygiene-gaps approved for merge
