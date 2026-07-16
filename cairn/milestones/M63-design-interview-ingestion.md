<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M63: /design-interview note-and-leave ingestion

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M43 is done -->
- **Principles touched:** IP3, IP4   <!-- owner: plan · worked-under (conservation of ingested principles; numbering never rewritten); none changed -->
- **Branch/PR:** m63-design-interview-ingestion   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Teach `/design-interview` to ingest a migration-preserved numbered-principles
file (M43's note-and-leave) into its Phase-2 formalization — closing the loop
the migration protocol defers to it.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** session-start detection of a preserved numbered-principles file (a
`cairn/`-path principles doc kept with numbering + basename intact per
`skills/shared/migration-protocol.md` note-and-leave); Phase-2 ingestion where
every numbered principle arrives as a pre-classified candidate carrying its
`#N` lineage; write-out of an old-`#N` → new-`IPn`/`GPn` mapping with the
preserved file kept intact until the in-code repoint ships; banking that
repoint as a target-repo ROADMAP candidate row (a code milestone there);
guard tests, mutation-registered.

**Out:** the actual intraclass formalization run (happens in that repo, on
Fable, user-driven — its ripeness is intraclass's call); the in-code
`PRINCIPLES.md #N` repoint itself (a target-repo code milestone, banked by
the skill at write-out); changes to migration-protocol note-and-leave
mechanics (M43 shipped them; only the cross-ref sweep here, T4).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: `/design-interview` session start detects a migration-preserved
      numbered-principles file at a `cairn/` path and states the ingestion
      path — prose present in `skills/design-interview/SKILL.md`, guard-locked.
- [ ] AC2: Phase-2 ingestion prose — every numbered principle arrives as a
      classified candidate (IP/GP/skip with a marked recommendation) carrying
      its `#N` lineage, with an explicit conservation line (no ingested
      principle silently dropped — IP3) — guard-locked.
- [ ] AC3: Write-out prose — an old-`#N` → new-id (`IPn`/`GPn`/retired)
      mapping is recorded in the target DESIGN.md, and the preserved file
      stays intact (numbering + basename) until the in-code repoint ships
      (IP4) — guard-locked.
- [ ] AC4: Repoint-banking prose — the in-code repoint is banked as a
      target-repo ROADMAP candidate row (a code milestone); the skill
      performs no code edits itself — guard-locked.
- [ ] AC5: New prose-guards registered in the mutation harness (per-block
      `Mutation(...)` entries, one-physical-line unique anchors — M53/M58/M59);
      `python3 -m unittest discover -s skills/tests` and
      `python3 -m unittest discover -s scripts/tests` both green (generic
      profile `verify`).
- [ ] AC6: Cross-ref agreement — repo-wide grep shows
      `skills/shared/migration-protocol.md`'s deferral text and the new
      ingestion step name the same handoff; tracking-record lines (this file,
      ROADMAP lineage, DECISIONS/archive history) exempt from the grep (M62).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Author session-start detection + Phase-2 ingestion prose in
      `skills/design-interview/SKILL.md` — detection keyed to the
      migration-protocol note-and-leave shape (numbered principles doc at a
      `cairn/` path, numbering + basename intact); ingestion feeds Phase 2's
      existing "every candidate arrives classified" discipline with `#N`
      lineage carried on each candidate and a conservation rule.
- [x] T2: Author the write-out additions — the `#N` → `IPn`/`GPn`/retired
      mapping table recorded in the target DESIGN.md, the
      preserved-file-stays-intact rule (until the repoint ships), and the
      target-repo repoint candidate-row banking.
- [ ] T3: Extend `skills/tests/test_design_interview.py` with a new TestCase
      for the ingestion path; mutation-register each new block; run both
      unittest suites from the repo root (M56).
- [ ] T4: Whole-repo grep sweep (M48) for the deferral phrasing; align
      `skills/shared/migration-protocol.md`'s cross-ref so the deferral lands
      on the now-real ingestion step.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan (promotes the 2026-07-12 candidate row; lineage M43 Out / migration-pilot-notes Pilot 3 G-I2).
- 2026-07-16: T1 — session-start detection + "Ingesting a note-and-leave principles file" section (ingestion + conservation) added to design-interview SKILL.md; question gate skipped (nothing open).
- 2026-07-16: T2 — write-out lineage map, preserved-file-intact rule, and target-repo repoint banking appended to the ingestion section.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->
