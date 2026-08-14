# M139: The narrowing repair for a defeated promise is reachable at a review return

- **Status:** blocked
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** `m139-narrowing-at-the-return` · https://github.com/jmgirard/cairn/pull/139

## Goal

A review return whose only available repair widens an author-recalled
enumeration is classified and repaired at the return as a narrowing of the
promise, without routing through `/milestone-plan` for a full re-cut.

## Scope

**In:** `/milestone-review`'s return classification gains the widening test,
routing that return onto the existing amendment-return track; the two clauses
it collides with — the amendment return's "only outside the domain of the
procedure it names", and the return floor's inside-the-domain clause — are
amended in the same edit to carve the case out. `/milestone-implement` step 6
gains the repair direction such an amendment takes, citing
`/milestone-plan` step 4 rather than repeating it. Guards for the added
sentences in `skills/tests/`, registered in the mutation harness. A D-entry
recording the classification change and its counting disposition.

**Out:**
- The criteria audit's three questions at plan and brief-ingest → owned by
  M132/D-098, unchanged here; this milestone touches the return surface only.
- The amendment-return counting track, its fixed work-log shape, and its
  second-occurrence stop → owned by D-097, reused unchanged.
- `/milestone-plan` step 4's bounded-promise rule itself → its single source,
  cited from the two new surfaces and edited by neither.
- Any new instrument, certification step, `cairn_validate` check, or committed
  verification ledger → refused at D-090's door and on D-095's ground.
- The amendment-time audit record → the standing ROADMAP candidate (M138
  review F1/F8), not folded in here.

## Acceptance criteria

- [x] AC1. `/milestone-review` states the widening test: a finding that
      demonstrates an acceptance criterion failing inside the domain its
      promise quantifies over is an amendment return rather than a defect
      return when the only repair available to it widens an enumeration whose
      membership is fixed by author recall rather than decided by a procedure
      over that domain. The existing "only outside the domain of the procedure
      it names" clause and the return floor's inside-the-domain clause are
      amended in the same edit so that each names this case as its explicit
      carve-out. The added sentence names `/milestone-plan` step 4 as its
      source; it uses that rule's recall-vs-procedure discriminator as its
      classifier but restates neither the rule's "however long its list"
      elaboration, its worked example, nor its narrowing repair. Evidence: the
      three sentences read verbatim from `skills/milestone-review/SKILL.md` at
      the review commit, beside `/milestone-plan` step 4's text.
- [x] AC2. A return reclassified under AC1 carries the amendment return's fixed
      work-log shape, counts on the amendment-return track under its
      second-occurrence stop, and does not increment the defect-return count
      the thrash rule reads. Evidence: the sentence(s) naming the
      AC1-reclassified case as carrying these three properties, read verbatim
      from the added lines of `git diff main...HEAD --
      skills/milestone-review/SKILL.md` at the review commit.
- [x] AC3. `/milestone-implement` step 6 states the repair direction an
      amendment executing such a return takes: the amendment takes the
      narrowing repair `/milestone-plan` step 4's bounded-promise rule states,
      and a wider enumeration is not an admissible amendment. The sentence
      names step 4 as its source and restates neither that rule's proxy test
      nor its worked example. Evidence: the sentence read verbatim from
      `skills/milestone-implement/SKILL.md` at the review commit, beside
      `/milestone-plan` step 4's text.
- [ ] AC4. Every sentence this milestone adds to
      `skills/milestone-review/SKILL.md` and `skills/milestone-implement/SKILL.md`
      reds the `skills/tests` suite under five probe runs across four forms —
      relabel, negation, subject transposition, and relocation run twice (once
      into a different section of the host file, once into the other of the two
      files) — and the file is restored with `git diff` shown clean after each
      run. A sentence carrying no rule (a cross-reference, lead-in, or pointer)
      is exempt from the negation form alone and is listed by number in the
      evidence line. Domain enumerated by the added lines of
      `git diff -w main...HEAD -- skills/milestone-review/SKILL.md
      skills/milestone-implement/SKILL.md`, split at sentence boundaries — the
      split is the step mapping added lines to added sentences, and a sentence
      whose text is unchanged from `main` is excluded by that comparison.
      Evidence: one `## Review` line per file naming that command, the sentence
      count it enumerated, the commit measured at, and the probe matrix result
      (sentences × forms attempted, the count that redded, exemptions by
      number).
- [x] AC5. Every positive assert this milestone adds under `skills/tests/` has
      its own mutation-harness registration whose named test method contains
      that assert and no other assertion, so the blanked block and the
      reacting assert are one-to-one. Domain enumerated from
      `git diff -w main...HEAD -- skills/tests/`, split at `self.assert*` call
      boundaries — the split is the step mapping added lines to added asserts,
      and an assert whose text is unchanged from `main` is excluded by that
      comparison. Each added negative assert is paired with a positive framing
      assert, and that phrase is the registered block. Each registered block is
      proven by `python3 -m unittest discover -s skills/tests -k
      mutation_harness` (the `discover` form is required: `PROFILE.md` records
      that the dotted module name dies on the harness's bare
      `import mutation_engine`): the harness blanks the block and requires its
      guard to fail, and the run reports `OK`. Each added assert is
      individually re-run against the AC4 mutation of the sentence it pins and
      required to fail; an assert whose pinned sentence lies outside AC4's
      domain is re-run against a relabel of the phrase it anchors on instead,
      since blanking verifies one axis only. Evidence: one `## Review` line
      naming the enumeration command, the added-assert count it enumerated, the
      commit measured at, and the harness run's reported test count and result
      (`Ran N tests … OK`).
- [x] AC6. `skills/tests`, `scripts/tests` and `hooks/tests` pass and
      `python3 scripts/cairn_validate.py` is green at the review commit.

## Coverage

- AC1 → T2, T5
- AC2 → T3, T5
- AC3 → T4, T5
- AC4 → T6
- AC5 → T5, T6
- AC6 → T7

## Tasks

- [x] T1. Read the three colliding clauses in place and draft the carve-out
      wording against their actual bytes: `/milestone-review`'s amendment
      return and return floor (`skills/milestone-review/SKILL.md`, the step-5
      block around the return floor and amendment return) and step 6 of
      `skills/milestone-implement/SKILL.md`. Grep every phrase the nearby
      guards anchor on before editing, so an edit does not reflow an adjacent
      anchor (M104) or repeat a short phrase an existing assert binds bare
      (M113).
- [x] T2. Write the widening test into `/milestone-review` and amend the two
      colliding clauses to carry the carve-out.
- [x] T3. Write the counting disposition — fixed shape, amendment track,
      second-occurrence stop, defect count untouched.
- [x] T4. Write the repair direction into `/milestone-implement` step 6.
- [x] T5. Add the guards to `skills/tests/test_thrash_rule.py`, pairing each
      absence assert with a positive framing assert, and register each
      positive block in `skills/tests/test_mutation_harness.py`.
- [x] T6. Run the AC4 probe matrix over the enumerated sentences and the AC5
      blanking run; restore and `git diff` clean after each probe.
- [x] T7. Append the D-entry (classification change + counting disposition,
      annotating D-097, citing D-098's host reading and D-090's satisfied
      trigger); run the three suites and `cairn_validate`.

## Work log

- 2026-08-13: created by /milestone-plan.
- 2026-08-13: plan gate chose reclassifying onto the existing amendment-return track over a third counter and over leaving the returns on the defect count, because the tighter second-occurrence stop is the point and no evidence yet shows two tracks insufficient; falsified by an amendment-return loop churning across different AC ids on one milestone, which is D-097's own stated exit.
- 2026-08-13: plan gate chose running the probes and recording the outcome over committing per-sentence and per-probe ledgers, because D-095 deleted that artifact class as an instrument testing only itself; falsified by a review finding a probe claim unreproducible from the recorded evidence line.
- 2026-08-13: plan gate chose a diff-decided probe domain over an author-classified one, because a rule/non-rule column is the proxy this milestone exists to close; falsified by the exemption list growing to cover most added sentences, which would restore the classification under another name.
- 2026-08-13: plan chose citing `/milestone-plan` step 4 from both new surfaces over restating its rule, because the rulebook's one-home step-0 check forbids the second copy; falsified by an operator at a return needing step 4's text and not reaching it.
- 2026-08-13: T1 — mapped the guard anchors over the three colliding clauses; `test_thrash_rule.py` pins them with `\s+`-spanning regexes plus two bare one-line `assertIn`s, so edits were wrapped by hand to keep those two phrases contiguous (M104/M113). No collision: "widening test", "author recall", "narrowing repair" and "reclassified" occur in no existing guard anchor.
- 2026-08-13: T2 — widening test written into `/milestone-review` step 5; the return floor's inside-the-domain clause and the amendment return's "only outside" clause each amended in place to name it as their carve-out. skills/tests green, 766 tests.
- 2026-08-13: T3 — counting disposition written beside the widening test: fixed work-log shape, amendment-return track under its second-occurrence stop, defect-return count never incremented.
- 2026-08-13: T4 — repair direction written into `/milestone-implement` step 6, citing `/milestone-plan` step 4 rather than restating it. skills/tests green, 766 tests.
- 2026-08-13: AC5 amended at the implement mini gate (Substantive). Its named command `python3 -m unittest skills.tests.test_mutation_harness` is unsatisfiable here — verified, not assumed: it exits `ModuleNotFoundError: No module named 'mutation_engine'` on the harness's bare import, the failure `PROFILE.md` documents, while the control `discover -s skills/tests -k mutation_harness` runs 9 tests OK. Fresh-context [O] reader audited the amended wording and returned six FIX findings, all applied: a polarity inversion ("survives" where red is required), a per-assert universal enumerated only per-sentence, per-method registration masking a second assertion, an enumeration command missing `-w` and the unchanged-text exclusion, no evidence line plus a vacuous `-k` pass, and "blanks RED" describing output that reads `OK`. Further churn went to the user per the one-re-entry bound; user accepted the six-fix version including the one-assertion-per-method rule.
- 2026-08-13: T5 — eight rule guards plus four slice-marker guards in `TestWideningTest`, one assertion per method per the amended AC5, each registered in the mutation harness. Whole-file reads were replaced by a marker-bounded slice: relocating a sentence to another section leaves a whole-file anchor matching (M123), so the relocation probe AC4 requires could not have redded against the first design.
- 2026-08-13: T6 — probe matrix run by script (scratchpad `probe.py`), 8 units x 5 runs = 40 probe runs, 40 RED, each unit's own guard among the reacting tests in every run; suite size stable at 778 across all runs and `git diff` clean after each restore. The four marker asserts, whose pinned text lies outside AC4's domain, took the relabel probe instead: 4/4 red, each reacting its own test. Harness probed against a known-positive first — an absent block raises `ValueError: block locator must occur exactly once (found 0)`, so a green harness run is not silence.
- 2026-08-13: T7 — D-101 appended (widening test, counting disposition, both falsifiers with their owners). Three suites green at exit 0: skills 778, scripts 345, hooks 103; `cairn_validate` all checks passed, no advisories.
- 2026-08-13: return-1 repair — two guards pin the amendment-return sentence's subject ("A finding that shows the criterion itself is wrong") and its tail ("is evidence about the promise, not the work"), each one assertion in its own method and registered. Six-sentence probe matrix re-run: 30/30 RED, 0 GREEN, suite 781, files restored clean.
- 2026-08-14: RR12 delivered (`cairn/reviews/RR12-ac4-guard-instrument.md`) — diagnosis: totality+granularity under-determined by anchors; recommends whole-slice equality fixtures and route (iii) split, with BC1–BC7 for the child. Awaiting `/milestone-brief` ingest; still blocked.
- 2026-08-14: blocked on RB12 — the maintainer chose escalation from the three return-3 routes; the AC4 guard-instrument question goes to Fable via `cairn/reviews/RB12-ac4-guard-instrument.md` (committed to main, merged into the branch).
- 2026-08-13: parked `blocked` at the maintainer's decision after return 3. Blocker: an undecided instrument question — whether a prose guard can deliver AC4's promise at all, or whether a different mechanism is needed. Three narrowings each closed a demonstrated hole and opened an adjacent one, and the plan gate recorded no alternative on guard scoping, so neither a fourth repair nor a re-cut proceeds until the maintainer settles it. Unblocks on that decision; the routing options offered at return 3 were escalation via `/milestone-brief`, re-plan or split via `/milestone-plan`, or amending AC4 to what the guards demonstrably deliver. Branch `m139-narrowing-at-the-return` and draft PR #139 stay open; the two doctrine rules are written and verified by AC1-AC3, AC5 and AC6.
- 2026-08-13: review return 3 (defect) — AC4 NOT MET a third time: R1 (96) and R3 (93) reproduced green by two agents independently, both AC4 forms inside AC4's domain. Thrash trigger (a) fires; trigger (b) fired at pass 2 and composes. B1/C2 (92) repaired at this pass: D-101 restored to its appended bytes and D-102 appended, the in-place edit recorded as an IP4 violation rather than hidden. R2 (85) and R4 (80) actioned, carried. Status -> in-progress; no further retry queued under the current plan.
- 2026-08-13: return-2 repair verified implement-side — 18 added asserts, 18 methods each with exactly one assertion (AST-checked), 18 registrations, all 18 one-to-one under blanking; AC4 matrix 30/30 RED; cross-rule relocation 11/11 RED. Three suites exit 0: skills 784, scripts 345, hooks 103; validate exit 0. Status -> review.
- 2026-08-13: return-2 repair — slices narrowed from one step-wide block to four per-rule blocks (return floor / amendment return / widening test / the Substantive amendment bullet), six markers each asserted unique, and the amendment block's tail bound by its own routing sentence because the widening marker travels with the rule it heads. Cross-rule relocation probe: 11 moves, 11 RED, including all three FA demonstrated green. AC4 six-sentence matrix re-run 30/30 RED. FD fixed: D-101 now records three carved limbs, corrected in place as branch-added prose rather than superseded.
- 2026-08-13: review return 2 (defect) — AC4 NOT MET again: FA (95, reproduced by the scorer) shows intra-slice relocation green, the marker slice spanning all three step-5 rules. FD (85) actioned. Thrash trigger (b) fired: AC4 failed twice by one shape (anchor scope wider than the rule). No alternative recorded at the plan gate on guard scoping, so /milestone-brief escalation is offered. Status -> in-progress.
- 2026-08-13: return-1 repair verified implement-side before handback — 15 M139 asserts, each its own method with exactly one assertion (AST-checked), each registered, each failing when its own block is blanked, and each reacting to at least one AC4-domain mutation (the four marker asserts to a relabel, their pinned text sitting outside AC4's domain). 16/16 mutations red, tree clean after every restore. Three suites exit 0: skills 781, scripts 345, hooks 103; validate 16 PASS, 0 FAIL/WARN. Status -> review.
- 2026-08-13: review return 1 (defect) — AC4 NOT MET: 2 of 30 probe runs green, S2's subject and tail unpinned (M131 class). F1 (80) actioned and fixed on the branch; 22 findings logged below threshold. AC5 not evaluated. Status -> in-progress.
- 2026-08-13: all tasks complete, three suites and validate green; status -> review.
- 2026-08-13: criteria audit ran twice ([O], fresh context, authored none of the wording). Round 1 returned nine findings on the step-2 draft — seven fixed and reported (over-broad "the repair available", a classification collision with two standing clauses, a jointly unsatisfiable AC2/AC3 pair, an undecidable "restates", an unbound diff base, a probe set missing relabel and the cross-file axis, and a harness run read as evidence of per-file registration), two taken to the gate (the rule/non-rule proxy; the ledger against D-095/D-090). Round 2 on the gate-revised wording returned eleven — eight fixed (two self-contradicting no-restatement clauses, a universal over findings with sentence-level evidence, an AC satisfied by the pre-milestone state, a reflow-inflated domain, evidence recording no probe outcome, negative asserts unregisterable by blanking, a one-file proxy for the assert domain) and three judgment calls settled without a further round, the gate's three-marker budget being spent.

## Decisions

## Review

**Evidence, PR #139, branch `m139-narrowing-at-the-return`.**

- AC1 — MET. The three sentences read verbatim from the shipped
  `skills/milestone-review/SKILL.md`: the widening test states the
  inside-the-domain classification keyed on the *only* available repair; the
  return floor's limb now reads "criterion names one, save where the widening
  test below carves that failure out as an amendment return"; the amendment
  return's limb gains "or meeting the widening test below, which carves that
  third case out of this clause's \"only outside\"". No-restatement checked
  against step 4's text by substring: "however long its list", the M102 worked
  example, and the narrowing-repair clause each absent from the added block;
  `/milestone-plan` step 4 named as source, present.
- AC2 — MET. Read from the added lines of `git diff main...HEAD --
  skills/milestone-review/SKILL.md`: "A return reclassified this way carries
  the fixed work-log shape above, counts on the amendment-return track under
  its second-occurrence stop, and never increments the defect-return count the
  thrash rule reads." All three properties in the added text, not inherited
  from the pre-milestone state.
- AC3 — MET. Read verbatim from `skills/milestone-implement/SKILL.md` step 6:
  "An amendment executing a return reclassified under `/milestone-review`'s
  widening test takes the narrowing repair `/milestone-plan` step 4's
  bounded-promise rule states; a wider enumeration is not an admissible
  amendment." Step 4 named; proxy test and worked example absent by substring
  check.
- AC6 — MET. Three suites at exit 0: skills 779 (778 + the F1 fix guard),
  scripts 345, hooks 103. `cairn_validate` exit 0, 16 PASS and 8 advisory OK,
  no FAIL or WARN.

- AC4 — **NOT MET.** Probe matrix re-run at the review commit over the domain
  AC4 names — the added lines of `git diff -w main...HEAD` over the two skill
  files, split at sentence boundaries, unchanged sentences excluded, which
  yields six sentences S1-S6. 30 probe runs (6 sentences x 5 runs across four
  forms), 28 RED and **2 GREEN**: S2, the amended amendment-return sentence,
  survives the negation probe ("is evidence about the promise, not the work"
  inverted to "about the work, not the promise") and the subject-transposition
  probe ("A finding that shows" to "A maintainer who shows"). Cause: the M139
  guards pin only the clause this milestone added to S2, while the sentence's
  subject and tail are pinned by nothing — the M131 predicate-without-subject
  and prefix-without-tail class. Suite size stable at 779 across all runs and
  the two files restored clean after every probe (verified: the only pending
  diff is the F1 fix below). No exemption was claimed or needed: S4, the
  pointer sentence, redded under all four forms.
- AC5 — NOT EVALUATED. AC4's failure returns the milestone before AC5's
  evidence was gathered; recorded as unverified rather than assumed.

**Independent fresh-context review — three lenses, then a scorer.**
Diff-bug **[O]**, blame-history **[S]**, prior-PR-comments **[S]**; 23 findings
scored by a fresh **[S]** scorer holding the diff and the milestone file.
Prior-review lens found no regressed prior finding and its GitHub inline-comment
probe returned empty. One finding scored >=80.

- F1 (80) — ACTIONED, fixed on the branch. The return floor's `>=90`
  deliverables limb was not carved out, so the motivating case could satisfy
  both the floor and the widening test at once: two counters, two work-log
  shapes, two stops, no tiebreak. Fixed by carving limb 2 as well, with its own
  guard and mutation registration (13th).
- 22 findings scored below 80, logged not actioned (IP3): F6/76 and F7/60
  (guard gaps on clause adjacency and on the no-restatement claim), F15/65 and
  F16/40 (D-101 counterfactual and attribution), F9/60 and F12/50 (ordering and
  step-number marker fragility), F13/55 (the implement-time probe count was
  8 guard-spans, not 6 sentences — superseded by the re-run recorded above),
  F4/55, B3/50, F3/45, F10/45, F2/40, F8+F8b/35, F5/30, F11/30, B1/30, F14/30
  (premise no longer in the file), B2/25, F18/20, C1/20, B4/15, F17/8 (stale —
  the Review section and ticks landed together).

**Return.** AC4 fails inside the domain of the procedure it names, so this is a
defect return, not an amendment return: AC4 is not falsified only outside its
procedure's domain, it names a procedure, and the repair is to pin S2's subject
and tail rather than to widen any enumeration — the widening test this
milestone ships does not reach it. Defect returns for M139: 1.

**Pass 2 — evidence re-gathered at `823981c` after the return-1 repair.**

- AC1 — MET. Three sentences read verbatim from the shipped
  `skills/milestone-review/SKILL.md`: the widening test; the return floor's
  limb carrying "save where the widening test below carves that failure out as
  an amendment return"; the amendment return's limb carrying "or meeting the
  widening test below, which carves that third case out of this clause's
  \"only outside\"". No-restatement re-checked by substring against step 4's
  text: the "however long its list" elaboration, the M102 worked example and
  the narrowing-repair clause are each absent from the added block, and step 4
  is named as source.
- AC2 — MET. Read from the added lines of the diff: "A return reclassified this
  way carries the fixed work-log shape above, counts on the amendment-return
  track under its second-occurrence stop, and never increments the
  defect-return count the thrash rule reads."
- AC3 — MET. Read verbatim from `skills/milestone-implement/SKILL.md` step 6;
  step 4 named, proxy test and worked example absent by substring check.
- AC4 — MET. Probe matrix over the domain AC4 names — added lines of
  `git diff -w main...HEAD` over the two skill files, split at sentence
  boundaries, unchanged sentences excluded, six sentences S1-S6. **30 probe
  runs (6 x 5 across four forms), 30 RED, 0 GREEN**, suite stable at 781 across
  every run, both files restored with `git diff` clean after each. No exemption
  claimed or needed: S4, the pointer sentence, redded under all four forms.
  The two greens that returned this milestone at pass 1 (S2 negation, S2 subject
  transposition) are now red.
- AC5 — MET. Domain from `git diff -w main...HEAD -- skills/tests/`: 15 added
  asserts, all positive (zero negative asserts added, so the pairing clause is
  vacuous). 15 registrations, and 15 methods in `TestWideningTest` each holding
  exactly one assertion (checked by AST walk, not by eye). Blanking each
  registered block reds that block's own named test in all 15 cases — one-to-one,
  never via a sibling. Each added assert also reacted to an AC4-domain mutation
  of the sentence it pins; the four marker asserts, whose pinned text sits
  outside AC4's domain, took the relabel probe instead and each redded its own
  test. Harness run `python3 -m unittest discover -s skills/tests -k
  mutation_harness`: Ran 9 tests, OK.
- AC6 — MET. skills 781, scripts 345, hooks 103, all exit 0; `cairn_validate`
  exit 0 with no FAIL and no WARN.

**Consistency gate.** `cairn_validate` exit 0, every check PASS, all advisories
OK. `Principles touched:` is `—`, so `cairn_impact` is skipped. Profile is
`generic`, whose `consistency-gate` slot names no toolchain checks — that half
is a clean no-op.

**Pass 2 — fan-out and verdict.** Three lenses; 26 findings scored by a fresh
**[S]** scorer holding the diff and the milestone file. Prior-review lens: zero
findings, no regressed prior finding or lesson, GitHub inline-comment probe
empty. Two findings actioned.

- FA (95) — **RETURN.** ACTIONED. "Intra-slice relocation defeats the M139
  guards. The marker slice runs `**Return floor (M130).**` to `6. Final
  checkpoint commit`, i.e. all three rules of step 5. Every M139 sentence can be
  moved into a *different rule's paragraph* inside that slice with the whole
  suite green." Independently reproduced by the scorer: the AC2 counting
  sentence moved into the Amendment-return paragraph, 49/49 OK, file restored
  and `git diff` clean. One demonstrated green leaves the section
  self-contradicting — "returns under this floor" joining the defect count
  while "never increments the defect-return count" sits two paragraphs up.
  AC4's relocation form ("once into a different section of the host file") is
  not met under the bolded-block reading, which is the unit the guards were
  designed around. Repair: per-rule end markers, narrowing the slice — not a
  wording change.
- FD (85) — ACTIONED, fix-now, carried into the repair. "D-101 misdescribes the
  shipped surface: 'The two clauses it collides with are amended to name it as
  their explicit carve-out' — the shipped file carves out **three** limbs."
  D-101 is unmerged, so this is repaired in place rather than superseded.
- 24 findings below 80, logged not actioned (IP3): FE/78 (Scope and AC1 still
  say "two clauses" after F1 widened the edit to three, with no gated
  amendment), FB/72 (AC4's "section" undefined — subsumed by FA), FK/68 (stale
  "(13th)" ordinal), FC/58, FM/58 (work log not monotone at the tail), F-C/55
  (no guard enforces the widening test's "only repair available" gate), FN/55,
  FJ/45, FR/45, F-A/42, FL/40, FO/40, F-B/35, FG/35, FH/35, FP/35, FF/30,
  FS/30, FI/20 (unmodified line), FQ/15, plus the blame lens's verified-clean
  IP4 and D-101 cross-entry checks.
- AC5 stands on its own procedure — 15 asserts, 15 one-assertion methods, 15
  registrations, all one-to-one under blanking, all reacting to a mutation of
  what they pin — but its cross-reference to AC4's probe is re-verified after
  the repair.

**Return 2 (defect).** Defect returns for M139: 2. Thrash trigger (a) needs a
third and has not fired. **Trigger (b) HAS fired**: AC4 has now failed twice,
each by a new mechanism of the same shape — an anchor whose scope is wider than
the rule it claims to pin (pass 1: the amended sentence's subject and tail sat
outside the pinned clause; pass 2: the slice spans three rules, so a sentence
moves between them unseen). Its remedy is to reconsider the alternative the plan
gate recorded against, and the gate recorded none on guard scoping — the four
recorded alternatives concern evidence form, probe domain, counting track and
citation. Where none was recorded, escalation via `/milestone-brief` is offered,
per instance.

**Pass 3 — evidence re-gathered at `39a2b2f` after the return-2 repair.**

- AC1 — MET. Three sentences read verbatim from the shipped review skill; the
  no-restatement clause re-checked by substring against step 4 (the "however
  long its list" elaboration, the M102 example and the narrowing-repair clause
  each absent; step 4 named).
- AC2 — MET. The counting sentence read from the added lines of the diff.
- AC3 — MET. The repair-direction sentence read verbatim from
  `/milestone-implement` step 6; step 4 named, proxy test and example absent.
- AC4 — MET. Six-sentence matrix: **30 probe runs, 30 RED, 0 GREEN**, suite
  stable at 784, both files restored with `git diff` clean after each run.
  Beyond AC4's own forms, a cross-rule relocation probe moved every added
  sentence out of its rule block into each other rule block in the same step:
  **11 moves, 11 RED**, including all three the pass-2 lens demonstrated green.
- AC5 — MET. Domain from `git diff -w main...HEAD -- skills/tests/`: 18 added
  asserts, all positive (zero negative asserts, pairing clause vacuous), 18
  methods each holding exactly one assertion (AST-checked), 18 registrations,
  and 18/18 one-to-one under blanking. Harness run: Ran 9 tests, OK.
- AC6 — MET. skills 784, scripts 345, hooks 103, all exit 0; `cairn_validate`
  exit 0, 16 PASS, no FAIL and no WARN.

**Consistency gate.** `cairn_validate` exit 0, every check PASS, all advisories
OK. `Principles touched:` is `—`, so `cairn_impact` is skipped. Profile
`generic` names no toolchain checks — that half is a clean no-op.

**Pass 3 — fan-out and verdict.** Three lenses; findings scored by a fresh
**[S]** scorer that independently reproduced R1 and R3 green and restored the
tree. Four actioned.

- R1 (96) — **RETURN.** "The amendment-return rule can be fully inverted with
  the suite green; the pass-1 repair did not close its own class." Pass 1's two
  guards pin S2's subject and tail but nothing binds them to each other, so text
  inserted BETWEEN them inverts the rule while both asserts match. Reproduced by
  two agents independently: the shipped rule made to say the opposite of itself,
  784 OK.
- R3 (93) — **RETURN.** "`test_amendment_block_keeps_its_own_routing_sentence`
  does not do what its name and comment claim; the amendment slice's tail is
  still unbound." The routing sentence sits mid-paragraph, not at the tail.
  Hoisting the widening block into the middle of the amendment paragraph strands
  that rule's fixed-shape and second-occurrence-stop sentences below another
  rule's heading, 784 OK. FA's geometry surviving FA's fix, one level down.
- B1/C2 (92) — ACTIONED, repaired at this pass. Correcting D-101 in place was an
  IP4 violation: `DECISIONS.md` is history, superseded and never edited, with no
  unmerged-branch exception in D-045, IP4, the file's own header, or
  guard-doctrine. Reached independently by two lenses. D-101 restored to its
  appended bytes; **D-102** appended, carrying both the correction and the
  violation record.
- R2 (85) and R4 (80) — ACTIONED, carried into the repair. R2: the widening
  test's classification sentence can be negated green, because the "only repair
  available to it" phrase is pinned but its force is not. R4:
  `implement_substantive()` spans a bullet holding six distinct rules — pass 2's
  defect, never applied to the second file.
- Below 80, logged (IP3): R6/68 (Scope and AC1 still say two clauses where three
  ship, with no gated amendment), R8/58, R5/45, B3/45, R7/30, B2/25, C1/15,
  plus C3-C9 carried from earlier passes (FK, FL, FM, FN, FR, FP), and R9/B4
  which confirm no defect.

**Return 3 (defect). Thrash trigger (a) fires** — the third return and every one
after it. The work log records no re-plan or split spent on this milestone, so
the remedy is re-plan or split via `/milestone-plan`, and no further retry is
queued under the current plan. **Trigger (b) fired at pass 2 and its diagnosis
carries into that routing**: AC4 has now failed three times, each by a new
mechanism of one shape — the guard's anchor reach exceeds the rule it claims to
pin. The plan gate recorded no alternative on guard scoping, so
`/milestone-brief` escalation is offered, per instance.

**The criterion is not what is wrong.** Every repair that closed a demonstrated
AC4 gap has been a narrowing, never a wider enumeration of probe forms or
anchors, so this is not an amendment return and the widening test this milestone
ships does not reach it. What the evidence indicts is the instrument: a prose
guard pins a phrase, and a phrase can be relocated, detached from what binds it,
or negated by insertion between two pinned fragments. Three narrowings each
closed the demonstrated hole and reopened an adjacent one.
