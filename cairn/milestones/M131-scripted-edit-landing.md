<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M131: A scripted edit is verified to have landed before the record claiming it did

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Branch/PR:** m131-scripted-edit-landing

## Goal

Close the three-instance class where a batched or scripted edit lands somewhere
other than its aimed site — or does not land at all — while the record claiming
it landed is written anyway.

## Scope

**In:** a three-clause conduct rule in `skills/shared/tracking-rules.md`, sited
once per the rulebook's step-0 one-home check, covering (i) verifying a batched
or scripted edit landed before writing the record that claims it did, (ii)
anchoring a section-targeted edit on text unique in the target file, and (iii)
sequencing a tick write strictly after its evidence write succeeds. Prose-guards
pinning each clause, registered in the mutation harness and inversion-proven.

**Out:** any mechanism that diffs intended against actual edit sites — the
candidate row rules it out ("never a mechanism") and D-090 keeps the apparatus
door shut; if wanted later it takes a fresh row. A `cairn/LESSONS.md` line
recording the incidents → this milestone's single review-time capture lesson,
authored at post-merge hygiene, not planned here. Widening clause (ii) into an
absolute ban on bare-header anchors → declined at the plan gate; a candidate row
only if a unique-header anchor is later found to have misfired.

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md` states the conduct rule in three
      clauses: (i) a batched or scripted edit is verified to have landed at its
      aimed site before any record claiming it landed is written; (ii) an edit
      targeting a document section anchors on text that occurs exactly once in
      the target file; (iii) a check-off or tick write is sequenced strictly
      after the write of the evidence it depends on has succeeded. The rule
      occupies exactly one site in the rulebook.
- [ ] AC2: each of AC1's three clauses has its anchored phrase registered as its
      own block in `skills/tests/test_mutation_harness.py`, and the harness run
      reports all three blocks reddening; an anchor the harness cannot see takes
      guard-doctrine §2's by-hand blanking check instead, recorded per anchor.
      Sweeping this branch's diff of `skills/tests/` for added `assertIn` and
      `assertRegex` calls returns no assertion pinning an AC1 clause that is
      absent from that record.
- [ ] AC3: each of AC1's three clauses is inversion-proven per guard-doctrine
      §1 — relabelled, negated, or transposed in place; the three verify
      commands run; at least one exits non-zero; the file restored and
      `git diff` over it empty. Recorded as a three-row table in Review.
- [ ] AC4: run from the repo root with each exit code checked explicitly,
      `python3 -m unittest discover -s skills/tests`,
      `python3 -m unittest discover -s scripts/tests`,
      `python3 -m unittest discover -s hooks/tests` and
      `python3 scripts/cairn_validate.py` each exit 0.

## Coverage

- AC1 → T1
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5

## Tasks

- [x] T1: author the three-clause rule in `skills/shared/tracking-rules.md`,
      one site only (step-0 one-home check run against the existing
      "Append, don't rewrite" and "Correcting a record proven false" text).
- [x] T2: author or extend the prose-guards under `skills/tests/` pinning each
      clause's anchored phrase; copy anchors from the shipped bytes, never from
      the draft (M95), and keep each on one physical line.
- [x] T3: register each anchored phrase as its own mutation-harness block; run
      the harness; run the by-hand blanking check for any anchor it cannot see;
      sweep this branch's `skills/tests/` diff for added asserts and reconcile.
- [x] T4: inversion sweep — per clause, mutate in place, run the three verify
      commands, require red in at least one, restore, diff clean; record the
      three-row table.
- [x] T5: run the three verify commands and `cairn_validate` from the repo root
      with exit codes checked explicitly; resolve any cap or advisory fallout.

## Work log

- 2026-08-02: created by /milestone-plan.
- 2026-08-02: criteria audit ([O], fresh context) returned 8 findings — 5 clear-fix applied before writing (AC2 assertion-vs-block conflation, AC2's two unbounded universals, AC3 red-in-each-vs-one, AC4 commands quoted verbatim from the profile verify slot, LESSONS cap arithmetic); 3 judgment findings taken to the gate.
- 2026-08-02: plan gate chose the rulebook as the rule's home over a `cairn/LESSONS.md` line because no suite asserts that file's lesson content, which would leave AC2 and AC3 unreachable; falsified by a guard class that pins dogfood-repo lesson content proving cheap and stable.
- 2026-08-02: plan gate chose uniqueness alone for clause (ii) over also banning bare-header anchors because the M130 instance was non-uniqueness and the ban forbids a unique header that would have been fine; falsified by a unique header anchor later found to have misfired.
- 2026-08-02: plan gate chose one `cairn/LESSONS.md` line doing both jobs over retiring an older lesson because the file is at 48 of 50 and a capture line lands at 49; falsified by a second line proving necessary before review.
- 2026-08-02: thrash assessment at user request — AC2/AC3 sit in the repo's thrashiest class (the guard-reddening lesson extended 5x), but the three past generators are closed: domain bounded to 3 enumerated clauses (M130's bounded-promise rule), the multi-round certification generator retired (M127), returns floored (M130/D-097); residual risk is reflow re-anchoring, a one-shot fix. No plan change; D-064 counting + D-097's second-occurrence stop are the stop condition.
- 2026-08-02: /milestone-implement — status in-progress, branch m131-scripted-edit-landing cut from pushed main.
- 2026-08-02: T1 — three-clause rule authored in `tracking-rules.md` "Universal tracking rules", sited after "Append, don't rewrite" and cross-referencing "Correcting a record proven false"; step-0 one-home check found no existing home. All three anchor phrases verified unique corpus-wide and each on one physical line; skills suite green (726), no neighbour reflow.
- 2026-08-02: T2 — `skills/tests/test_scripted_edit_landing.py` authored, 3 tests / 4 asserts, anchors copied from the shipped bytes; the harness completeness meta-test fired on the unregistered file exactly as documented.
- 2026-08-02: T3 — 4 blocks registered (one per assert). Per-entry check: all 4 red when blanked, green unblanked, errors=0, so none is a crash counted as a pass (M117/M122). AC2 sweep of this branch's `skills/tests/` diff: 4 added assert calls, 4 registered blocks, every block present in the diff — no assert pinning an AC1 clause is absent from the record.
- 2026-08-02: T4 — inversion sweep, all 4 subjects (3 clauses + the tick prohibition) negated in place: each reddened skills/tests (exit 1) with scripts/hooks green; script restored in a `finally:` (M124), sha256 matches the original and `git diff` is empty. AC3's three-row table is review-owned evidence, recorded when review re-runs the sweep.
- 2026-08-02: T5 — from the repo root, exit codes captured separately, never piped (M56): skills/tests 729 exit 0, scripts/tests 337 exit 0, hooks/tests 103 exit 0, cairn_validate exit 0. Rulebook 955->966 lines, 68,103->68,986 chars. All tasks done; status review.

## Decisions

## Review
