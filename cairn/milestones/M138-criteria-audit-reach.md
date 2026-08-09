# M138: The criteria audit reaches amended wording and one-exemplar verification clauses

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m138-criteria-audit-reach   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Close the criteria audit's two measured escape paths: amended wording that
never re-enters the audit, and verification clauses whose one exemplar stands
in for the family.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** one clause cluster in `/milestone-implement` step 6 (criterion-wording
changes are Substantive by definition; amended wording is re-audited by a
fresh reader before it is written, with an ingest-audit exemption and a
per-criterion one-re-entry bound); one byte-identical sentence extending the
audit's third question at `/milestone-plan` step 3 and `/milestone-brief`'s
ingest audit; prose-guards, mutation-registry entries, and an inversion-probe
pass over every added sentence.

**Out:** re-measuring the record-defect share → stays a candidate row
(ROADMAP). Any mechanical check or validator of audit conduct → rejected at
D-067, standing (the instrument is a reader, never a check). Amendment
auditing for Goal/Scope wording → the existing step-6 mini gate, unchanged
(the audit's subject is acceptance criteria; the Minor-arm narrowing merely
stops criterion edits masquerading as minor). Guard-doctrine §4 changes →
none; the new sentence cites it, the module is untouched.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `/milestone-implement` step 6 states that a change to
      acceptance-criterion wording is *Substantive* by definition, and its
      *Minor* arm's "refine wording" is narrowed to text outside the
      amendment-gated sections (Goal, Scope, Acceptance criteria).
- [ ] AC2: `/milestone-implement` step 6's *Substantive* path states that
      amended acceptance-criterion wording — an amendment return from
      `/milestone-review` included — is asked the criteria audit's three
      questions as `/milestone-plan` step 3 states them, by a fresh-context
      **[O]** reader that did not author the amended wording, before the
      amended text is written to the milestone file; wording whose clearance
      the `/milestone-brief` ingest audit's work-log line already covers is
      exempt; per criterion, wording fixed at the mini gate re-enters the
      questions once with its own fresh reader, and further churn on that
      criterion goes to the user.
- [ ] AC3: `/milestone-plan` step 3's audit block and `/milestone-brief`'s
      ingest audit each carry, starting on its own line in both files, a
      byte-identical sentence extending the third question: where a criterion
      cites a mutation, inversion, or planted-defect verification, the audit
      asks whether the probes vary every axis the verified domain is free in
      — form as well as location — or stand one exemplar in for the family
      (guard-doctrine §1's inversion protocol and §4's fixture rule applied
      to criteria).
- [ ] AC4: Every sentence this branch adds to `/milestone-implement` step 6
      and the audit blocks of `/milestone-plan` step 3 and `/milestone-brief`
      — membership decided by normalized-text absence from the merge-base
      version of the file, so reflow-only lines are excluded — is pinned by a
      prose-guard registered in the mutation harness that reds when its block
      is blanked, and reds under both a negation probe and, where the
      sentence pairs two terms that can be swapped, a transposition probe;
      probe results are recorded as one aggregate work-log line naming forms
      and counts, cross-checkable against the registry; AC3's byte-identity
      is asserted by a guard counting exactly one occurrence of the sentence
      in each of the two files.
- [ ] AC5: The three suites of the profile's verify slot — `skills/tests`,
      `scripts/tests`, `hooks/tests` — pass from the repo root with each
      suite's exit code checked individually (M56 lesson) on the branch at
      review time.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3, T4
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Author the step-6 clause cluster in
      `skills/milestone-implement/SKILL.md` (lines 78–98): Substantive-by-
      definition for criterion wording, Minor-arm narrowing, the re-audit
      sentence (pointer to `/milestone-plan` step 3's questions), the
      ingest-clearance exemption, and the per-criterion one-re-entry bound.
- [ ] T2: Author the third-question extension byte-identically in
      `skills/milestone-plan/SKILL.md` (step 3 audit block, lines 86–109) and
      `skills/milestone-brief/SKILL.md` (ingest audit), each starting on its
      own line.
- [ ] T3: Guards: a step-6 class plus extensions to
      `skills/tests/test_fresh_context_readers.py` (both surfaces + a
      count-exactly-one identity guard for the new sentence); a mutation-
      registry entry per added sentence, anchors copied from shipped bytes
      (M95), wrap-spanning regexes (M105).
- [ ] T4: Probe pass: negation and transposition probes over every added
      sentence (relocation/dispersal probes per the M136 lesson where a
      bullet hosts the sentence); one aggregate work-log line; run the three
      suites from the repo root, each exit code checked individually.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-09: created by /milestone-plan, absorbing two ROADMAP candidate rows (gate-amended criteria re-audit — circumplex M79 return-3 thrash; mutation clauses sample the domain's forms — circumplex M81 review F1); D-090's apparatus door cleared and recorded: the trigger is shipped skill prose causing three defect returns for a downstream user, the D-098 host path M134/M136/M137 already walked.
- 2026-08-09: criteria audit ran twice (fresh [O] reader both rounds). Round 1: 15 findings — 8 clear-answer fixes applied (Minor-path escape, question single-home pointer, ingest exemption, loop bound, probe-form conjunction, inversion in the trigger list, subject naming, suites named), 2 settled at the gate, rest disposed. Round 2 over the revised bytes: 10 findings — 6 fixed (gated-sections narrowing, work-log-line exemption condition, per-criterion units, fresh reader per re-entry, §1+§4 citation, merge-base membership), 2 tightened (step-6 domain, swappable-terms qualifier), 1 flagged-kept (aggregate probe line, cross-checkable against the registry), set-level pointer design confirmed closed. One re-entry consumed; further churn goes to the user.
- 2026-08-09: plan gate chose a fresh-reader amendment audit over session-inline (the candidate row's cheaper form) because self-reading just-authored wording is the measured failure the instrument exists to replace (D-067); falsified by a fresh-reader-audited amendment again failing review on a defect the three questions name.
- 2026-08-09: plan gate chose one milestone over two because both rules amend the same instrument and each is about one clause plus guards; falsified by the branch outgrowing the sizing tripwires mid-implementation.
- 2026-08-09: step 2 chose extending the third question over adding a fourth because every surface counts "three questions" and the amendment path inherits by pointer; falsified by a verification-clause finding the extended third question cannot host.
- 2026-08-09: T1 done — step 6's Minor arm narrowed to non-amendment-gated wording, Substantive-by-definition clause, re-audit sentence (pointer to plan step 3), ingest-clearance exemption, per-criterion one-re-entry bound; inserted as whole lines so no guarded phrase reflowed; skills suite green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->
