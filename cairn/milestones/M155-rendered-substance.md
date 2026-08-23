# M155: Mandated substance moves to guaranteed-rendered positions

- **Status:** planned
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Branch/PR:** —

## Goal

Chat substance the rules require the user to see — gate evidence, durable-record previews, handoff commands — moves to positions the harness is guaranteed to render, so no chip choice is made blind.

## Scope

**In:** A rendering-reliability doctrine in `skills/shared/tracking-rules.md`: text emitted before a tool call in the same turn is not reliably displayed, so mandated substance lives only in guaranteed-rendered positions — the chip's own question/option text where it fits the accessible-language limits, a turn's final rendered text otherwise (chip posed after the user responds), post-resolution restatement for previews and handoffs. The four rules currently mandating above-the-chip or before-the-commit chat text are amended ("Chips carry choices, not evidence", "Acceptance chips show what's accepted", "Accessible language on the decision surface", "Durable-record preview"); every doctrine restatement across the skills is reconciled; the hand-run prose guards and the three-place rulebook-mass baseline follow; a D-entry narrowly supersedes D-037's placement clause (its verbatim bar and five-skill wiring stand).

Surface tier: **user-facing** — the rulebook and skill directives ship to every adopting repo. D-108/D-090 door: passed via the retained shipped-behavior trigger — the shipped chip rules made the 1.7.0 release session's version rationale and tag/push handoff invisible to the user (the 2026-08-22 candidate row this milestone promotes; the row graduates at post-merge hygiene, records-hygiene §1).

**Out:** any harness-side rendering fix (not cairn's to make — the candidate row's own framing); the review-side reclassification candidate row (separate, untouched); any new gated checker (prose guards stay hand-run, D-109).

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md` states the hybrid placement doctrine: (a) text emitted before a tool call in the same turn is not reliably displayed, so substance a rule requires the user to see never relies on pre-tool-call rendering alone; (b) chip-decision substance rides in the chip's own question text and option descriptions where it passes the accessible-language rule's limits, and otherwise ends the preceding turn as its final rendered text with the chip posed after the user responds; (c) a durable-record preview or handoff command either ends the turn's rendered text or is restated verbatim in the first rendered text after the tool call resolves; (d) the amended "Chips carry choices, not evidence", "Acceptance chips show what's accepted", "Accessible language on the decision surface", and "Durable-record preview" rules each state placements consistent with (a)–(c), with no rule mandating above-the-chip chat text as the sole carrier of decision substance. Evidence: the shipped lines quoted at review.
- [ ] AC2: On the milestone branch at review, every line returned by `grep -rnE '\*?above\*? the|before the commit|verbatim in chat' --include='*.md' skills/ README.md`, and every rule in tracking-rules.md's "Question gates and routing chips" and "Output & interaction discipline" sections read whole (the read covers spellings the grep misses, e.g. emphasis-broken ones), is consistent with the AC1 doctrine — no sentence in that domain mandates pre-tool-call chat text as the sole carrier of substance the user must see. Evidence: the sweep output and section read with a per-hit disposition.

## Coverage

- AC1 → T1
- AC2 → T2

## Tasks

- [ ] T1: Amend `skills/shared/tracking-rules.md`: add the rendering-reliability sentence and the hybrid placement rule; amend the four rules AC1(d) names; re-seed the rulebook-mass baseline in its three sites (`skills/milestone/SKILL.md` cost line, `skills/tests/test_cost_audit_line.py` seeded-baseline test, `skills/tests/test_mutation_harness.py` baseline entry — the M149 lesson).
- [ ] T2: Run the AC2 sweep and whole-section read; reconcile every hit — the per-skill directives (`milestone-plan` step 3, `milestone-implement` gates, `milestone-review` gates, `milestone-brief` gates, `milestone` route triage, `skills/shared/migration-protocol.md`) restate the hybrid placement; log per-hit dispositions in the work log.
- [ ] T3: Update the hand-run prose guards whose pinned phrases the amendments change (`skills/tests/test_gate_conclusion_preview.py:44,65`, `test_issue_triage.py:154`, `test_mutation_harness.py:920,944`, plus any red the suite surfaces); extend guard asserts and mutation entries to pin the new doctrine (M152 convention); hand-run `skills/tests` to zero reds.
- [ ] T4: Draft the D-entry narrowly superseding D-037's above-the-chip placement clause (verbatim bar and five-skill wiring stand); preview verbatim in chat before its commit.
- [ ] T5: Run both gating suites (`python3 -m unittest discover -s scripts/tests`, `... -s hooks/tests`) and `cairn_validate`; all green.

## Work log

- 2026-08-22: created by /milestone-plan; promotes the 2026-08-22 chip-supporting-text candidate row (row graduates at post-merge hygiene, records-hygiene §1).
- 2026-08-22: criteria audit ran in full mode ([O] fresh reader, two rounds). Round 1: 4 findings — chip-case unsatisfiability (became the gate's design question), unqualified rule conflicts (fixed: AC1(d) names the amended rules), AC2 grep proxy (narrowed to the stated procedure), test-string hits (descoped to T3 per the instrument question). Round 2, on the gate-revised wording: 4 findings, all repaired — accessible-language rule joined AC1(d); grep widened for emphasis-broken spellings; "in that domain" bound added to AC2; guard pins routed to T3, not AC2.
- 2026-08-22: plan gate chose hybrid-by-length placement over post-hoc restatement because restatement cannot inform the choice it follows (user rejection + audit round 1); falsified by a harness guarantee that pre-tool-call text renders.
- 2026-08-22: plan gate chose hybrid-by-length over always-stop-before and always-inside-chip because a uniform stop adds an exchange for two-sentence evidence and inside-only truncates long finding lists; falsified by gate sessions showing the length judgment misapplied in either direction.
- 2026-08-22: plan chose amending the four existing rules over an additive qualifying clause because two rules pointing opposite ways was audit round 1's finding 2; falsified by a shipped amendment that still reads contradictory at review.

## Decisions

## Review
