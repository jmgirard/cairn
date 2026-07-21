# M103: Exploratory sources — supply-push ingestion

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Branch/PR:** —

## Goal

Legitimize reading a corpus of uncited sources to discover new oracles or
methods, so cairn triages them into candidates rather than dismissing them.

## Scope

**In:** Doctrine in `tracking-rules.md`'s "References pages" section naming
**supply-push exploration** as a legitimate activity distinct from the
demand-pull "owed" trigger: an uncited source dropped on the shelf
(`references/sources/`) is read to *discover*, never dismissed as irrelevant,
while a source merely consulted in passing still owes nothing. Its outputs:
ROADMAP **candidate rows** always (search-first, the D-042 discovery→candidate
pattern); a committed **survey synthesis note** only when the triage will
outlive its exploration (the section's existing "owed applied to time" test),
authored from the shipped `synthesis-note.md` template (no template change);
per-source `<citekey>.md` pages stay demand-pull. The M56 guardrail is
restated so exploration reuses existing machinery. `/milestone-plan` step 2
recognizes exploratory source ingestion as an investigation activity yielding
candidates + a conditional survey note. New doctrine clauses are pinned by
mutation-registered prose guards.

**Out:** A dedicated `/explore-sources` skill → candidate row (promote if
rulebook+plan routing proves insufficiently discoverable). New directories or
committed-raw-source / query-op / graph-tooling / references-log machinery →
the M56 rejection stands. Changes to the demand-pull primary-sources rule or
numeric oracle doctrine (`validation-doctrine.md`) → not this milestone.
Bidirectional citekey parsing → the existing "Citekey resolution" candidate.

## Acceptance criteria

- [ ] `tracking-rules.md`'s "References pages" section states supply-push
      exploration is legitimate and distinct from the demand-pull "owed"
      trigger — an uncited corpus source is triaged to discover, not dismissed
      as irrelevant, while consulted-in-passing still owes nothing. Evidence: a
      prose guard asserts the load-bearing clause and passes.
- [ ] The doctrine states exploration's three outputs: candidate rows always
      (search-first), a committed survey synthesis note only when the triage
      outlives its exploration, and per-source pages staying demand-pull.
      Evidence: a prose guard per clause passes.
- [ ] The doctrine restates the M56 guardrail — reuse candidate rows + the
      synthesis-note survey type; no query op, graph tooling, references log,
      or committed raw sources. Evidence: a prose guard passes.
- [ ] `/milestone-plan` step 2 recognizes exploratory source ingestion as an
      investigation activity yielding candidates + a conditional survey note.
      Evidence: a prose guard over the skill's `SKILL.md` passes.
- [ ] Each new prose guard is mutation-registered (one `Mutation` per positive
      `assertIn`) and the mutation harness reports each new anchor reddens.
      Evidence: `test_mutation_harness` green with the new entries.
- [ ] The generic profile's `verify` slot is clean: the three `unittest`
      suites and `cairn_validate` all pass.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3
- AC5 → T2, T3, T4
- AC6 → T4

## Tasks

- [x] T1 — Author the exploration doctrine paragraph in `tracking-rules.md`
      after "When a page is owed" (~:669): the reconciling clause (triaged
      corpus vs. consulted-in-passing), the three outputs, and the M56
      guardrail. Load-bearing clauses each on one physical line (M23).
- [x] T2 — Author prose guards for T1's clauses in a new
      `TestExploratorySources` class in `skills/tests/test_references_pages.py`,
      copying the committed bytes of each clause (M95/M100 — anchor on real
      bytes, never on text just drafted); one `Mutation` per positive
      `assertIn` in `test_mutation_harness.py`. Confirm each anchor sits on one
      line and reddens under the harness (guards use `Path.read_text`, M100).
- [ ] T3 — Add the exploratory-ingestion recognition to `/milestone-plan`
      `SKILL.md` step 2; guard it (copy committed bytes) + `Mutation` entry;
      confirm it reddens.
- [ ] T4 — Run all three `unittest` suites, `cairn_validate`, and the mutation
      harness from the repo root, checking each exit code (M56/M65); run
      `cairn_budget` on this file. Confirm green.

## Work log

- 2026-07-20: created by /milestone-plan.
- 2026-07-20: T1 — exploration doctrine added to tracking-rules "References pages" (5 single-line anchors); three suites green.
- 2026-07-20: T2 — TestExploratorySources (5 doctrine asserts + one-line check) + 5 Mutation registrations; skills suite 554 green, harness reddens each anchor.

## Decisions

## Review
