# M139: The narrowing repair for a defeated promise is reachable at a review return

- **Status:** planned
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** —

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

- [ ] AC1. `/milestone-review` states the widening test: a finding that
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
- [ ] AC2. A return reclassified under AC1 carries the amendment return's fixed
      work-log shape, counts on the amendment-return track under its
      second-occurrence stop, and does not increment the defect-return count
      the thrash rule reads. Evidence: the sentence(s) naming the
      AC1-reclassified case as carrying these three properties, read verbatim
      from the added lines of `git diff main...HEAD --
      skills/milestone-review/SKILL.md` at the review commit.
- [ ] AC3. `/milestone-implement` step 6 states the repair direction an
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
- [ ] AC5. Every positive assert this milestone adds under `skills/tests/` has
      its own mutation-harness registration, enumerated from the added asserts
      in `git diff main...HEAD -- skills/tests/` rather than from the harness
      run; each added negative assert is paired with a positive framing assert
      and that phrase is the registered block. Each registered block blanks RED
      under `python3 -m unittest skills.tests.test_mutation_harness -v`, and
      each added assert also survives the AC4 probe of the sentence it pins,
      since blanking verifies one axis only.
- [ ] AC6. `skills/tests`, `scripts/tests` and `hooks/tests` pass and
      `python3 scripts/cairn_validate.py` is green at the review commit.

## Coverage

- AC1 → T2, T5
- AC2 → T3, T5
- AC3 → T4, T5
- AC4 → T6
- AC5 → T5, T6
- AC6 → T7

## Tasks

- [ ] T1. Read the three colliding clauses in place and draft the carve-out
      wording against their actual bytes: `/milestone-review`'s amendment
      return and return floor (`skills/milestone-review/SKILL.md`, the step-5
      block around the return floor and amendment return) and step 6 of
      `skills/milestone-implement/SKILL.md`. Grep every phrase the nearby
      guards anchor on before editing, so an edit does not reflow an adjacent
      anchor (M104) or repeat a short phrase an existing assert binds bare
      (M113).
- [ ] T2. Write the widening test into `/milestone-review` and amend the two
      colliding clauses to carry the carve-out.
- [ ] T3. Write the counting disposition — fixed shape, amendment track,
      second-occurrence stop, defect count untouched.
- [ ] T4. Write the repair direction into `/milestone-implement` step 6.
- [ ] T5. Add the guards to `skills/tests/test_thrash_rule.py`, pairing each
      absence assert with a positive framing assert, and register each
      positive block in `skills/tests/test_mutation_harness.py`.
- [ ] T6. Run the AC4 probe matrix over the enumerated sentences and the AC5
      blanking run; restore and `git diff` clean after each probe.
- [ ] T7. Append the D-entry (classification change + counting disposition,
      annotating D-097, citing D-098's host reading and D-090's satisfied
      trigger); run the three suites and `cairn_validate`.

## Work log

- 2026-08-13: created by /milestone-plan.
- 2026-08-13: plan gate chose reclassifying onto the existing amendment-return track over a third counter and over leaving the returns on the defect count, because the tighter second-occurrence stop is the point and no evidence yet shows two tracks insufficient; falsified by an amendment-return loop churning across different AC ids on one milestone, which is D-097's own stated exit.
- 2026-08-13: plan gate chose running the probes and recording the outcome over committing per-sentence and per-probe ledgers, because D-095 deleted that artifact class as an instrument testing only itself; falsified by a review finding a probe claim unreproducible from the recorded evidence line.
- 2026-08-13: plan gate chose a diff-decided probe domain over an author-classified one, because a rule/non-rule column is the proxy this milestone exists to close; falsified by the exemption list growing to cover most added sentences, which would restore the classification under another name.
- 2026-08-13: plan chose citing `/milestone-plan` step 4 from both new surfaces over restating its rule, because the rulebook's one-home step-0 check forbids the second copy; falsified by an operator at a return needing step 4's text and not reaching it.
- 2026-08-13: criteria audit ran twice ([O], fresh context, authored none of the wording). Round 1 returned nine findings on the step-2 draft — seven fixed and reported (over-broad "the repair available", a classification collision with two standing clauses, a jointly unsatisfiable AC2/AC3 pair, an undecidable "restates", an unbound diff base, a probe set missing relabel and the cross-file axis, and a harness run read as evidence of per-file registration), two taken to the gate (the rule/non-rule proxy; the ledger against D-095/D-090). Round 2 on the gate-revised wording returned eleven — eight fixed (two self-contradicting no-restatement clauses, a universal over findings with sentence-level evidence, an AC satisfied by the pre-milestone state, a reflow-inflated domain, evidence recording no probe outcome, negative asserts unregisterable by blanking, a one-file proxy for the assert domain) and three judgment calls settled without a further round, the gate's three-marker budget being spent.

## Decisions

## Review
