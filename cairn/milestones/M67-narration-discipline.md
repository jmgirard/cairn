<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M67: Narration discipline — outcomes, not deliberation

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m67-narration-discipline · https://github.com/jmgirard/cairn/pull/65   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1: The "Output & interaction discipline" section of
      `skills/shared/tracking-rules.md` contains a rule named
      **Narrate outcomes, not deliberation** (name on one physical line —
      M59/M64 reflow lesson) stating: interstitial chat carries findings,
      decisions, and mandated previews; a one-line signpost before a long
      step is fine; a compact summary where a question needs context is
      fine; a running readout of reasoning is not — and naming the
      Durable-record preview and Acceptance chips rules as mandated
      substance this rule never licenses compressing.
- [x] AC2: A prose-guard (`skills/tests/test_narration_discipline.py`)
      locks the rule's name and its load-bearing phrases, and is registered
      in the mutation harness — blanking the rule block makes the guard
      fail.
- [x] AC3: All three verify suites green from the repo root
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

- [x] T1: Author the rule in `skills/shared/tracking-rules.md`, placed
      immediately after "Deltas, not dumps"; keep the rule name and each
      guard-anchor phrase on one physical line.
- [x] T2: Add `skills/tests/test_narration_discipline.py` (pattern:
      `test_gate_conclusion_preview.py`) + a `Mutation(...)` entry in
      `skills/tests/test_mutation_harness.py` anchoring a unique block of
      the new rule (M58: anchor a phrase unique in the file; M65: block
      includes trailing punctuation).
- [x] T3: Run the three verify suites from the repo root; confirm green by
      exit code.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan (with D-039); prompted by the
  hitop cairn-init/design-interview session's italic running commentary.
- 2026-07-16: T1–T3 done in one sitting — rule authored after "Deltas, not
  dumps", guard + 2 mutation entries added, all three suites green (214
  skills tests incl. harness); question gate skipped (nothing open).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->

2026-07-16 evidence (PR #65):

- AC1: `grep -in "Narrate outcomes, not deliberation" skills/shared/tracking-rules.md`
  → line 363, name on one physical line; rule states the bar (readout of
  reasoning, italicized play-by-play), both allowances (signpost;
  summary-for-questions, D-039), and the Durable-record/Acceptance-chips
  carve-out (lines 363–370). PASS.
- AC2: `test_narration_discipline.py` runs 3/3 OK; mutation harness green
  with the 2 new `Mutation(...)` entries ("never a running readout of
  reasoning", "This never licenses compressing mandated substance") —
  blanking each makes the guard fail (TestRegisteredGuardsFailWhenBlanked,
  part of the 214-test skills suite, exit 0 via pipefail). PASS.
- AC3: all three suites green from repo root, exit codes read via
  zsh `pipestatus[1]` (never tail's): skills 0, scripts 0, hooks 0. PASS.
- Consistency gate: `cairn_validate` exit 0 (15 PASS, 2 OK advisories);
  no principle changed (GP1 worked-under, not amended) → `cairn_impact`
  skipped; generic profile → no toolchain checks.
- Fan-out: [O] diff-bug 1 finding; [S] blame-history no findings (carve-out
  preserves M64–M66 mandates, purely additive); [S] prior-PR no evidence
  (zero review comments across candidate PRs — expected). Scored findings
  <80 (logged, not actioned): 1 — F1/78: mutation block at
  test_mutation_harness.py:205 omits its trailing colon, deviating from the
  M65 include-trailing-punctuation guidance T2 itself cites; registration
  is sound today (blanking fails the guard), risk is a low-probability
  future locator staleness.
