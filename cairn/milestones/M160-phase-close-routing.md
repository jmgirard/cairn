# M160: Phase-close routing recommends implement for already-planned work

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m160-phase-close-routing   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Phase-close blocks route an already-planned workable milestone to
`/milestone-implement`, taking their next command from `cairn_next.py`'s
recommendation instead of prose that lumps planned work with candidates.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**Tier:** user-facing — the deliverable is skill prose adopting repos
execute at every review close and status route.

**In:** `/milestone-review` step 9 (explicit post-hygiene `cairn_validate.py`
run, replacing the "fires later in this same step" allusion), step 10
(`cairn_next.py`-led next command with the D-050 release-parking
displacement), and `/milestone` §3's state-conditional example list. A
repo-wide grep found these as the only two skill files carrying the
plan-for-planned wording ("planned or candidate").

**Out:** `scripts/cairn_next.py` — already correct and test-pinned
(`scripts/tests/test_scripts.py:264`), untouched. A prose-guard test pinning
the new wording — declined at the plan gate (test-bar question), not
deferred anywhere.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `/milestone-review` step 9 explicitly instructs running
      `cairn_validate.py` over the completed hygiene edits before the
      docs-only commit, in place of the current allusion ("fires later in
      this same step"), and its `release window` advisory is named as the
      signal step 10 reads.
- [ ] AC2: `/milestone-review` step 10 instructs running `cairn_next.py`
      after the step-9 hygiene commit lands and leading the close block's
      fenced next command with its recommendation — displaced by the
      release-parking offer exactly as `/milestone` §3 prescribes when
      step 9's `cairn_validate.py` run fired the `release window` advisory
      and the recommendation names that same release milestone (D-050) —
      and step 10's text no longer names `/milestone-plan` as the route for
      existing planned work.
- [ ] AC3: `/milestone` §3's state-conditional example list offers
      `/milestone-implement M<NNN>` for a workable planned milestone as an
      entry distinct from the resume entry, and the `/milestone-plan`
      entry's stated condition no longer includes planned items.
- [ ] AC4: The active profile's `verify` slot clean — both gating unittest
      suites green — and `skills/tests` hand-run green (skill-file edits;
      LESSONS M56/M148).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1
- AC2 → T2, T4
- AC3 → T3, T4
- AC4 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: In `skills/milestone-review/SKILL.md` step 9 (~line 333), replace
      the "fires later in this same step" allusion with an explicit
      instruction to run `cairn_validate.py` over the completed hygiene
      edits before the docs-only commit, naming the `release window`
      advisory as step 10's signal.
- [ ] T2: Rewrite step 10's next-action clause (~line 382): run
      `cairn_next.py` after the hygiene commit lands, lead the fenced next
      command with its recommendation, add the D-050 displacement clause
      deferring to `/milestone` §3's prescription, and delete the
      "`/milestone-plan` when planned or candidate work exists" wording.
- [ ] T3: In `skills/milestone/SKILL.md` §3's example list (~line 156), add
      `/milestone-implement M<NNN>` — implement (a workable planned
      milestone exists) — as its own entry and narrow the `/milestone-plan`
      entry's condition to exclude planned items.
- [ ] T4: Sweep `grep -rn "planned or candidate" skills/` (expect zero
      hits), run both gating suites checking each exit code explicitly, and
      hand-run `skills/tests` (edits sit near guarded regions — LESSONS
      M148).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-24: created by /milestone-plan.
- 2026-08-24: criteria audit ran in full mode ([O] fresh reader, three rounds): round 1 flagged AC2's unconditional cairn_next lead colliding with D-050 (fixed with the §3 displacement clause); round 2 flagged the displacement condition's missing instrument (fixed by mandating step 9's explicit validate run, which became AC1); round 3 passed every criterion on all five questions.
- 2026-08-24: plan gate chose a cairn_next.py-led step 10 over a corrected prose enumeration because the script is the single test-pinned routing authority and prose enumerations re-drift; falsified by a review close where the script's recommendation misroutes or cannot be run.
- 2026-08-24: plan gate chose an explicit step-9 cairn_validate run as the D-050 displacement signal over prose judgment of release-shape because the condition needs the mechanical instrument §3 already uses; falsified by the run proving too heavy or firing spurious advisories at review close.
- 2026-08-24: plan gate chose no new prose-guard test over pinning the new wording because a two-span prose fix does not warrant guard upkeep (pinned slices are brittle near future edits — LESSONS M148); falsified by a later edit reintroducing plan-for-planned routing unnoticed.
- 2026-08-24: implement started; branch m160-phase-close-routing; question gate skipped (plan gate settled all three open choices, no tripwires).
- 2026-08-24: T1 done — step 9 now instructs an explicit cairn_validate.py run over the hygiene edits before the docs-only commit, naming the release-window advisory as step 10's signal; both gating suites green (324 + 103, OK).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->
