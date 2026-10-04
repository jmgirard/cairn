<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M211: Run edge cases in the skills

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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

- [x] AC1: The rulebook-mass baseline in `skills/milestone/SKILL.md` and the
      two hand-run pins (`skills/tests/test_cost_audit_line.py`,
      `skills/tests/test_mutation_harness.py`) state the figures that
      `wc -l -m skills/shared/tracking-rules.md` prints on the milestone
      branch's final head, and the skill line names M211 and its date as the
      re-seed, catching up the deliberate rulebook changes made since M166.
- [x] AC2: `/milestone-review` step 10 puts `/milestone` first for a fired
      `release window` advisory only when the next action it would otherwise
      fence (the plan's next milestone, or `cairn_next.py`'s recommendation)
      names a milestone the advisory flagged. Otherwise that action stays
      first and `/milestone` is fenced after it, as `/milestone` §3 rules.
- [x] AC3: In `skills/`, only `/milestone-implement` step 6 instructs writing
      a work-log line opening `amendment return:`. `/milestone-review`'s
      amendment-return exit instructs a line opening `amendment routed:`,
      which neither the step-7 amendment count nor the amendment-return count
      reads. The hand-run pins in `skills/tests` that quote the changed text
      are updated to match.
- [x] AC4: `skills/shared/records-hygiene.md` §7 counts a candidate row and
      the rows that name its title in double quotes (direct references only)
      as one group, and a group whose rows together cite deferred review
      findings from two or more distinct milestones gets the disposition
      chip. `/milestone-review` step 9's cross-reference names the older row's
      title in double quotes, and the `/milestone` §2 bullet that cites §7
      says the same as §7. The module stays under 55 lines and 4,000 bytes
      (`wc -l -c`).
- [x] AC5: The `verify` slot of `cairn/PROFILE.md` is clean: all four commands
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
- 2026-10-04: claim audit: 31 claims read, 1 corrected — skills/tests/test_cost_audit_line.py (the seed comment said the re-seed followed the re-seed clause, but the branch does not change the rulebook). Also tightened from the reader's notes: skills/milestone/SKILL.md (the baseline is named a catch-up since M166) and skills/shared/records-hygiene.md (the row title leaves out the `- ` and any priority token, still 54 lines / 3,200 bytes). The same reader re-read all three once and found them TRUE. Verify clean, skills/tests at baseline.
- 2026-10-04: all tasks done and verify clean. Status set to review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->

Evidence, 2026-10-04, branch head 319a0be, main unmoved at c9d302d:

- AC1: `wc -l -m skills/shared/tracking-rules.md` prints 626 / 59322. `skills/milestone/SKILL.md:102`, `test_cost_audit_line.py:67`, and `test_mutation_harness.py:120` carry "626 lines / 59,322 chars". The skill line names "M211, 2026-10-04, a catch-up of the changes since M166". No site still quotes 467 / 43,454. Pass.
- AC2: `skills/milestone-review/SKILL.md:707-718` fences `/milestone` when the advisory fired, puts it first only when the plan's next milestone or `cairn_next.py`'s recommendation names a flagged id, and otherwise keeps that action first with `/milestone` after it, citing `/milestone` §3 (`skills/milestone/SKILL.md:258-263`, which agrees). Pass.
- AC3: `grep -rn 'amendment return:' skills --include='*.md'` finds the one write instruction at `milestone-implement/SKILL.md:193-198`. Review lines 369, 376, 388, and 416 describe implement's line, the stop's read, and the step-7 count. Review's exit instructs `amendment routed: AC<N> — <finding>` (:367), and the step-7 count (:416) and the thrash rule read only `amendment return:`/`substantive amendment:`. `test_thrash_rule` and the mutation entries quoting the changed text pass. Pass.
- AC4: §7 defines the title and group, direct references only, two or more distinct milestones, and the chip for the group. Review step 9 (:632-637) tests the group and names the older title in double quotes. The `/milestone` §2 bullet (:120-125) states the same group and trigger and cites §7 for the rest. `wc -l -c` prints 54 / 3200, under 55 and 4,000. Pass.
- AC5: `python3 -m unittest discover -s scripts/tests` exit 0 (397, OK, 21 skipped); `-s hooks/tests` exit 0 (174 OK); `claude plugin validate` exit 0 (passed with warnings); `claude plugin test .` exit 0 (1024 pass, 0 fail). Pass.
- Gate: `cairn_validate.py` all checks passed. `generic` profile has no toolchain checks. No principle changed, so no impact report. skills/tests (hand-run, non-gating) holds the baseline 4 reds and 1 error.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: a group forms only when a row quotes the exact title, and only step 9's already-absorbing branch said to quote it, so rows filed earlier never group (ROADMAP's "Band follow-ons" quotes "Desktop track follow-ons" without its "(M204 review)") — fix now: step 9 now has every cross-referencing row it files quote the exact title after its own `: `, fixed 2ef61b7. Judged not floor-qualifying: AC4 holds as written and the gap is one missing instruction.
- diff-bug #2: the second-occurrence stop now reads only executed amendments, so a routed return whose amendment never runs does not count — follow-up: this is the falsifier the plan gate recorded and D-150 states. It goes to the new candidate row at hygiene.
- diff-bug #3: implement step 1 reads only `review return <n>:`, so a cold resume does not read `amendment routed:` — follow-up (the gap predates M211; review invokes implement in the same session), new candidate row.
- diff-bug #4: step 9 and triage tested only a row's own group, but §7 bars extending any row of a firing group, and overlapping groups can draw several chips over the same rows — fix now for membership (step 9 and triage now say "belongs to a finding-absorbing group"), fixed 2ef61b7. Overlapping chips go to the new candidate row as a follow-up.
- diff-bug #5: a quoted reference placed before the new row's own `: ` puts quotes in its title — fix now: §7 and step 9 place it after the row's own `: `, fixed 2ef61b7.
- diff-bug #6: §7 did not say "exact" — fix now, fixed 2ef61b7.
- diff-bug #7: the stop matches on `AC<N>` alone, which a renumbering amendment shifts — follow-up (predates M211), new candidate row.
- diff-bug #8: no D-entry records T1's or T2's narrowing — fix now: D-150 annotates D-097 and narrows D-144's lead clause, fixed 2ef61b7.
- diff-bug #9: no CHANGELOG entry for a user-facing milestone — fix now: Unreleased Fixes entry, fixed 2ef61b7.
- diff-bug #10: the module budget header dropped the stated headroom and the retrofit date — fix now: both restored, ledger compressed to stay at 54 lines / 3,175 bytes, fixed 2ef61b7.
- diff-bug #11: "`/milestone` goes first" was unclear next to the `/clear` fence — fix now: "first after `/clear`", fixed 2ef61b7.
- diff-bug #12: the `/milestone` §2 bullet omitted "direct references only" and mixed row and group — fix now, fixed 2ef61b7.
- diff-bug #13: a row with no `: ` has no defined title — follow-up, new candidate row.
- blame-history #1: two behavior changes had no D-entry, against D-097's and D-144's wording — fix now, same as diff-bug #8, fixed 2ef61b7.
- blame-history #2: `amendment routed:` adds a line type where M130 already meant implement to be the writer — reject (planned change): the plan gate chose one writer plus a routed line, with its falsifier logged.
- blame-history #3: exact-quote grouping misses real rows, and triage rewrites can change a title and dissolve a group — fix now for the filing gap (as diff-bug #1), fixed 2ef61b7. Triage rewrites go to the new candidate row as a follow-up.
- blame-history #4: the baseline re-seed sits oddly beside the retained "only when a later pass changes the file" clause — reject (planned change): AC1 calls for this catch-up, and the skill line and test comment name it as one.
- blame-history #5: step 10 cited `/milestone` §3 for the plan-next case §3 does not state — fix now: the cite is scoped to `cairn_next`'s recommendation, fixed 2ef61b7.
- blame-history #6: the budget header lost D-122's headroom wording — fix now, same as diff-bug #10, fixed 2ef61b7.
- blame-history #7: the §2 compression left the IP4 rationale thinner — reject (style): the rule and its scope are unchanged.
- prior-review #1: the new step 9, step 10, and §7 rules have no prose pins — reject (planned change): the plan scoped pin work to the pins that quote changed text, and the suite gates nothing (D-109).
- prior-review #2: the Review section lacked a per-finding list — reject (false): this list is that record.
- prior-review #3: "review poses no chip for it" disagrees with M160's parking chip — reject (false): D-144 moved the parking offer to the close block, and the text is not changed by this branch.
- Re-check after fixes: verify clean (397 and 174 OK, validate passes, plugin test 1024 pass), `cairn_validate.py` all checks passed, `wc -l -m` of the rulebook still 626 / 59322 (AC1 holds), records-hygiene 54 / 3175 (AC4 holds), skills/tests at baseline.
