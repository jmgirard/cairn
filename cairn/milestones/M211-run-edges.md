<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M211: Run edge cases in the skills

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the skills' conduct is what the plugin delivers to adopters   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m211-run-edges   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Four run edge cases from the M202 and M203 reviews stop giving wrong counts, a wrong first command, or a missed audit question.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** four items of the "Run edge cases" candidate row, promoted by the
2026-10-04 audit triage:

- the rulebook-mass baseline, not re-seeded since M166 in its three sites,
- the `release window` displacement in `/milestone-review` step 10, which puts
  `/milestone` first even when the next action is not the flagged release,
- the two writers of one `amendment return:` line, so one return can count
  twice and trip the second-occurrence stop,
- the records-hygiene §7 trigger, which never fires for findings spread over
  rows that cross-reference each other.

**Out:** the row's item about review step 10 chaining into a milestone from a
plan that never ran as a run. The D-148 hotfix (#216) removed that chaining,
and no milestone planned before M202 remains, so the item needs no work. The
row is pruned at post-merge hygiene.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: The rulebook-mass baseline in `skills/milestone/SKILL.md` and the
      two hand-run pins (`skills/tests/test_cost_audit_line.py`,
      `skills/tests/test_mutation_harness.py`) state the figures that
      `wc -l -m skills/shared/tracking-rules.md` prints on the milestone
      branch's final head, and the skill line names M211 and its date as the
      re-seed, catching up the deliberate rulebook changes made since M166.
- [ ] AC2: `/milestone-review` step 10 puts `/milestone` first for a fired
      `release window` advisory only when the next action it would otherwise
      fence (the plan's next milestone, or `cairn_next.py`'s recommendation)
      names a milestone the advisory flagged. Otherwise that action stays
      first and `/milestone` is fenced after it, as `/milestone` §3 rules.
- [ ] AC3: In `skills/`, only `/milestone-implement` step 6 instructs writing
      a work-log line opening `amendment return:`. `/milestone-review`'s
      amendment-return exit instructs a line opening `amendment routed:`,
      which neither the step-7 amendment count nor the amendment-return count
      reads. The hand-run pins in `skills/tests` that quote the changed text
      are updated to match.
- [ ] AC4: `skills/shared/records-hygiene.md` §7 counts a candidate row and
      the rows that name its title in double quotes (direct references only)
      as one group, and a group whose rows together cite deferred review
      findings from two or more distinct milestones gets the disposition
      chip. `/milestone-review` step 9's cross-reference names the older row's
      title in double quotes, and the `/milestone` §2 bullet that cites §7
      says the same as §7. The module stays under 55 lines and 4,000 bytes
      (`wc -l -c`).
- [ ] AC5: The `verify` slot of `cairn/PROFILE.md` is clean: all four commands
      exit 0, each exit code checked.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T4
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T1, T2, T3, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: One writer for `amendment return:`. The review exit
      (`skills/milestone-review/SKILL.md:366-372`) writes
      `amendment routed: AC<N> — <finding>` instead. Implement step 6
      (`skills/milestone-implement/SKILL.md:193-196`) stays the writer. Check
      that the step-7 count (`milestone-review:410`) and the thrash stop read
      only `amendment return:`. Update the pins in `test_thrash_rule.py` and
      `test_mutation_harness.py`, then hand-run `skills/tests` and compare
      with the 4 reds and 1 error of the last hygiene pass.
- [x] T2: Release-window displacement. Align step 10's displacement
      (`milestone-review:700-706`) with `/milestone` §3: `/milestone` leads
      only when the next action names a flagged milestone.
- [x] T3: Linked-row groups. Rewrite records-hygiene §7 for groups and compress
      elsewhere in the module to stay under its budget. Make step 9's
      cross-reference (`milestone-review:629`) quote the older row's title.
      Update the `/milestone` §2 bullet. Write the D-entry for the trigger
      change. Grep README and DESIGN for the old wording (LESSONS M112).
- [x] T4: Re-seed the baseline last, after every other edit, from
      `wc -l -m` on the final head, in all three sites (LESSONS M149). Run
      the four verify commands.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-04: created by /milestone-plan from the `/milestone` audit triage of the "Run edge cases" row (user chose "Plan a milestone").
- 2026-10-04: question set: how the audit catches findings spread over linked rows — count a row and the rows that name it in quotes as one group.
- 2026-10-04: criteria audit (full): a fresh Opus reader returned 4 findings on M211 (AC1's re-seed clause, AC2's "the" flagged release, AC3's grep-as-promise and missed test pins, AC4's undefined grouping and the module's one spare line), each fixed toward the narrower wording above.
- 2026-10-04: plan gate chose linked-row groups over filing unfixed findings in DESIGN.md Known issues, because Known issues would move the growth and drop the promotion triggers; falsified by an audit where findings from two milestones sit in rows that never quote each other's titles.
- 2026-10-04: plan chose `/milestone-implement` as the one writer of `amendment return:` over review, because only the amendment knows the amended clause verbatim; falsified by a return whose amendment never runs yet must count toward the stop.
- 2026-10-04: implement started on branch m211-run-edges, cut from main in sync with origin. The untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-04: the simple-english lint hook counts every existing hit in each edited file (353 in the review skill, 120 in the implement skill). Rewriting the skills to that style is outside M211's scope and would break the prose pins, so only the edited text changes.
- 2026-10-04: T1 done. Review's exit writes `amendment routed: AC<N> — <finding>` and reads the work log for a prior `amendment return: AC<N>` before it routes. Implement step 6 names itself the one writer. The step-7 count and the thrash rule read `amendment return:` only (unchanged). Pins updated in `test_thrash_rule.py` (2 fixtures, 4 tests) and `test_mutation_harness.py` (5 entries). skills/tests is back to the baseline 4 reds and 1 error. Verify is clean: 397 and 174 OK, validate passes, plugin test 1024 pass.
- 2026-10-04: T2 done. Review step 10 always fences `/milestone` when the `release window` advisory fired, and puts it first only when the next action it would fence names a flagged id. Step 9's sentence now says the signal includes which ids. No pin quoted the old text. Verify clean, skills/tests at baseline.
- 2026-10-04: T3 done. records-hygiene §7 now defines a row's title (text before the first `: `) and its group (the row and each row that quotes that title, direct references only), and a group with findings from two or more milestones gets the chip. §1, §2, the budget note, and the ledger were compressed to fit: 54 lines, 3,154 bytes. Review step 9 tests the group and quotes the older title. The `/milestone` §2 bullet matches. D-149 records the change and the D-108 door walk.
- 2026-10-04: minor amendment: T3 also updated `/cairn-triage`'s restated definition of a finding-absorbing row, found by the old-wording grep. README and DESIGN carry no old wording. The pinned §1 and §2 phrases are kept, and skills/tests is at baseline.
- 2026-10-04: T4 done. `wc -l -m skills/shared/tracking-rules.md` prints 626 lines / 59,322 chars, and the branch does not change that file. The `/milestone` baseline (now "M211, 2026-10-04"), `test_cost_audit_line.py`, and the `test_mutation_harness.py` block carry those figures. No other site quotes the old seed. Verify clean (397 and 174 OK, validate passes, plugin test 1024 pass), skills/tests at baseline. If a review fix changes the rulebook, re-seed the three sites again.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
