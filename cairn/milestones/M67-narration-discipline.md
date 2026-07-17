<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M67: Narration discipline — outcomes, not deliberation

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Add a guard-locked "Narrate outcomes, not deliberation" rule to the
rulebook's output discipline so sessions stop emitting an italic running
readout of reasoning between tool calls, while the D-036/D-037 verbatim
previews stay untouched.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** one new rule in `skills/shared/tracking-rules.md` "Output &
interaction discipline" (adjacent to "Deltas, not dumps"), per D-039: the
signpost + summaries-for-questions allowance, the no-deliberation-readout
bar, and the explicit D-036/D-037 preview carve-out; a prose-guard test;
mutation registration.

**Out:** per-skill wiring of the rule (rejected in D-039 — re-open by
superseding it); any change to the D-036/D-037/D-038 preview mandates
themselves; harness-level thinking-display behavior (not cairn's surface —
cairn governs what the orchestrator writes, not what the client renders).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: The "Output & interaction discipline" section of
      `skills/shared/tracking-rules.md` contains a rule named
      **Narrate outcomes, not deliberation** (name on one physical line —
      M59/M64 reflow lesson) stating: interstitial chat carries findings,
      decisions, and mandated previews; a one-line signpost before a long
      step is fine; a compact summary where a question needs context is
      fine; a running readout of reasoning is not — and naming the
      Durable-record preview and Acceptance chips rules as mandated
      substance this rule never licenses compressing.
- [ ] AC2: A prose-guard (`skills/tests/test_narration_discipline.py`)
      locks the rule's name and its load-bearing phrases, and is registered
      in the mutation harness — blanking the rule block makes the guard
      fail.
- [ ] AC3: All three verify suites green from the repo root
      (`python3 -m unittest discover -s skills/tests | scripts/tests |
      hooks/tests`), exit codes checked explicitly (M56/M65: never
      tail-piped).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. Review reads to fence
     evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: Author the rule in `skills/shared/tracking-rules.md`, placed
      immediately after "Deltas, not dumps"; keep the rule name and each
      guard-anchor phrase on one physical line.
- [ ] T2: Add `skills/tests/test_narration_discipline.py` (pattern:
      `test_gate_conclusion_preview.py`) + a `Mutation(...)` entry in
      `skills/tests/test_mutation_harness.py` anchoring a unique block of
      the new rule (M58: anchor a phrase unique in the file; M65: block
      includes trailing punctuation).
- [ ] T3: Run the three verify suites from the repo root; confirm green by
      exit code.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan (with D-039); prompted by the
  hitop cairn-init/design-interview session's italic running commentary.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->
