# M155: Mandated substance moves to guaranteed-rendered positions

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Branch/PR:** m155-rendered-substance

## Goal

Chat substance the rules require the user to see — gate evidence, durable-record previews, handoff commands — moves to positions the harness is guaranteed to render, so no chip choice is made blind.

## Scope

**In:** A rendering-reliability doctrine in `skills/shared/tracking-rules.md`: text emitted before a tool call in the same turn is not reliably displayed, so mandated substance lives only in guaranteed-rendered positions — the chip's own question/option text where it fits the accessible-language limits, a turn's final rendered text otherwise (chip posed after the user responds), post-resolution restatement for previews and handoffs. The four rules currently mandating above-the-chip or before-the-commit chat text are amended ("Chips carry choices, not evidence", "Acceptance chips show what's accepted", "Accessible language on the decision surface", "Durable-record preview"); every doctrine restatement across the skills is reconciled; the hand-run prose guards and the three-place rulebook-mass baseline follow; a D-entry narrowly supersedes D-037's placement clause (its verbatim bar and five-skill wiring stand).

Surface tier: **user-facing** — the rulebook and skill directives ship to every adopting repo. D-108/D-090 door: passed via the retained shipped-behavior trigger — the shipped chip rules made the 1.7.0 release session's version rationale and tag/push handoff invisible to the user (the 2026-08-22 candidate row this milestone promotes; the row graduates at post-merge hygiene, records-hygiene §1).

**Out:** any harness-side rendering fix (not cairn's to make — the candidate row's own framing); the review-side reclassification candidate row (separate, untouched); any new gated checker (prose guards stay hand-run, D-109).

## Acceptance criteria

- [x] AC1: `skills/shared/tracking-rules.md` states the hybrid placement doctrine: (a) text emitted before a tool call in the same turn is not reliably displayed, so substance a rule requires the user to see never relies on pre-tool-call rendering alone; (b) chip-decision substance rides in the chip's own question text and option descriptions where it passes the accessible-language rule's limits, and otherwise ends the preceding turn as its final rendered text with the chip posed after the user responds; (c) a durable-record preview or handoff command either ends the turn's rendered text or is restated verbatim in the first rendered text after the tool call resolves; (d) the amended "Chips carry choices, not evidence", "Acceptance chips show what's accepted", "Accessible language on the decision surface", and "Durable-record preview" rules each state placements consistent with (a)–(c), with no rule mandating above-the-chip chat text as the sole carrier of decision substance. Evidence: the shipped lines quoted at review.
- [x] AC2: On the milestone branch at review, every line returned by `grep -rnE '\*?above\*? the|before the commit|verbatim in chat' --include='*.md' skills/ README.md`, and every rule in tracking-rules.md's "Question gates and routing chips" and "Output & interaction discipline" sections read whole (the read covers spellings the grep misses, e.g. emphasis-broken ones), is consistent with the AC1 doctrine — no sentence in that domain mandates pre-tool-call chat text as the sole carrier of substance the user must see. Evidence: the sweep output and section read with a per-hit disposition.

## Coverage

- AC1 → T1
- AC2 → T2

## Tasks

- [x] T1: Amend `skills/shared/tracking-rules.md`: add the rendering-reliability sentence and the hybrid placement rule; amend the four rules AC1(d) names; re-seed the rulebook-mass baseline in its three sites (`skills/milestone/SKILL.md` cost line, `skills/tests/test_cost_audit_line.py` seeded-baseline test, `skills/tests/test_mutation_harness.py` baseline entry — the M149 lesson).
- [x] T2: Run the AC2 sweep and whole-section read; reconcile every hit — the per-skill directives (`milestone-plan` step 3, `milestone-implement` gates, `milestone-review` gates, `milestone-brief` gates, `milestone` route triage, `skills/shared/migration-protocol.md`) restate the hybrid placement; log per-hit dispositions in the work log.
- [x] T3: Update the hand-run prose guards whose pinned phrases the amendments change (`skills/tests/test_gate_conclusion_preview.py:44,65`, `test_issue_triage.py:154`, `test_mutation_harness.py:920,944`, plus any red the suite surfaces); extend guard asserts and mutation entries to pin the new doctrine (M152 convention); hand-run `skills/tests` to zero reds.
- [x] T4: Draft the D-entry narrowly superseding D-037's above-the-chip placement clause (verbatim bar and five-skill wiring stand); preview verbatim in chat before its commit.
- [x] T5: Run both gating suites (`python3 -m unittest discover -s scripts/tests`, `... -s hooks/tests`) and `cairn_validate`; all green.

## Work log

- 2026-08-22: created by /milestone-plan; promotes the 2026-08-22 chip-supporting-text candidate row (row graduates at post-merge hygiene, records-hygiene §1).
- 2026-08-22: criteria audit ran in full mode ([O] fresh reader, two rounds). Round 1: 4 findings — chip-case unsatisfiability (became the gate's design question), unqualified rule conflicts (fixed: AC1(d) names the amended rules), AC2 grep proxy (narrowed to the stated procedure), test-string hits (descoped to T3 per the instrument question). Round 2, on the gate-revised wording: 4 findings, all repaired — accessible-language rule joined AC1(d); grep widened for emphasis-broken spellings; "in that domain" bound added to AC2; guard pins routed to T3, not AC2.
- 2026-08-22: plan gate chose hybrid-by-length placement over post-hoc restatement because restatement cannot inform the choice it follows (user rejection + audit round 1); falsified by a harness guarantee that pre-tool-call text renders.
- 2026-08-22: plan gate chose hybrid-by-length over always-stop-before and always-inside-chip because a uniform stop adds an exchange for two-sentence evidence and inside-only truncates long finding lists; falsified by gate sessions showing the length judgment misapplied in either direction.
- 2026-08-22: plan chose amending the four existing rules over an additive qualifying clause because two rules pointing opposite ways was audit round 1's finding 2; falsified by a shipped amendment that still reads contradictory at review.
- 2026-08-22: T1 done — Mandated-substance rule added; Durable-record preview, Chips-carry-choices, Accessible-language, and Acceptance-chips rules amended to guaranteed-rendered positions; rulebook 418/38,127 -> 433/39,624 (`wc -l -m`), baseline re-seeded in its three sites; scripts/hooks/skills suites all exit 0 (521 skills tests OK).
- 2026-08-22: T2 done — AC2 sweep returned 18 hits: 15 edited to guaranteed-rendered placements (milestone/SKILL.md 149,184; migration-protocol 54,179; milestone-plan 109,274; milestone-implement 47,70,86,90; milestone-review 287,364; milestone-brief 47,132,136), 2 are the amended tracking-rules preview rule itself (281,283 — consistent), 1 unrelated kept (synthesis-note 61, 'above the table'); whole-section read of the two tracking-rules sections found no other pre-tool-call placement mandate.
- 2026-08-22: T3 done — 6 guard reds fired exactly on the edited lines (fired-guard proof), pins updated in test_durable_record_preview, test_gate_conclusion_preview, test_issue_triage, test_finding_enforcement; 4 mutation blocks re-pointed; new TestMandatedSubstanceRule (4 asserts) + 4 RULES-target mutation entries added; skills/tests 525 tests exit 0; scripts/hooks suites and cairn_validate exit 0.
- 2026-08-22: T4 done — D-123 appended (narrowly supersedes D-037's placement clause; verbatim bar and wiring stand); previewed verbatim in the committing turn's final rendered text per the new rule.
- 2026-08-22: T5 done — scripts/tests, hooks/tests, skills/tests (525), cairn_validate all exit 0; status to review.
- 2026-08-22: review triage — 3-lens fan-out: 0+0+13 findings, 7 fixed at the gate, 6 rejected with logged reasons; no return-floor hit; baseline re-seeded 39,689 -> 39,744.
- 2026-08-22: review — fresh AC evidence recorded, both ACs pass; section-read residual (deltas-rule exception clause, tracking-rules 275) reworded and baseline re-seeded 39,624 -> 39,689; all suites green.

## Decisions

- 2026-08-22: D-123 (cross-cutting, promoted to `cairn/DECISIONS.md`): acceptance-chip substance moves to guaranteed-rendered positions; narrowly supersedes D-037's placement clause and D-038's placement wording in the same narrow scope; verbatim bar and wiring stand.

## Review

- AC1 — PASS. Shipped lines quoted from `skills/shared/tracking-rules.md` on the branch: the Mandated-substance rule at 294-300 carries (a) "Text emitted before a tool call in the same turn is not reliably displayed" (294), (b) "Chip-decision substance rides in the chip itself where it passes the Accessible-language limits below, and otherwise ends the preceding turn as that turn's final rendered text, the chip posed after the user responds" (297-298), (c) "A durable-record preview or a handoff command either ends its turn's rendered text or is restated verbatim in the first rendered text after the tool call resolves" (299-300); (d) the four amended rules state guaranteed-rendered placements — Durable-record preview 280-286 ("in the turn that lands its commit, in a guaranteed-rendered position"), Chips carry choices 301-305 ("never mid-turn chat before the chip's tool call"), Accessible language 306-313 ("live outside the chip, in a guaranteed-rendered position"), Acceptance chips 314-319 ("verbatim in a guaranteed-rendered position before the choice"); no rule mandates above-the-chip chat text as the sole carrier.
- AC2 — PASS. Sweep `grep -rnE '\*?above\*? the|before the commit|verbatim in chat' --include='*.md' skills/ README.md` on the branch returns 3 lines: tracking-rules 281 and 283 are the amended preview rule itself (they state the guaranteed position), synthesis-note.md 61 is "above the table" (unrelated to chips). Whole read of "Question gates and routing chips" and "Output & interaction discipline": one residual found — the deltas rule's exception clause still read "conclusion text above an acceptance chip" (line 275, permissive not mandating, invisible to the grep as "above an") — reworded in-review to "acceptance-chip conclusion text, each in its guaranteed-rendered position"; no sentence in the domain mandates pre-tool-call chat text as the sole carrier.
- Consistency gate: cairn_validate exit 0; generic-profile verify (scripts/tests, hooks/tests) exit 0; hand-run skills/tests 525 tests exit 0. Rulebook re-measured after the residual fix: 433 lines / 39,689 chars, baseline re-seeded in its three sites in the same commit.
- Fan-out (user-facing tier, three lenses): [S] prior-PR-comments — no findings (M152 archive points honored; PR-thread probe empty, walk skipped). [S] blame-history — no findings (D-037/D-038 substance verified intact by blame; M152 plain-style rule untouched; baseline triplet consistent; suites re-run independently, green). [O] diff-bug — 13 findings, triaged:
  - F1 cairn-release handoff unreconciled (the motivating 1.7.0 loss) — fixed: step 4 now mandates the rationale+checklist end the turn's rendered text before step 6's chip.
  - F2 plan/brief preview directives instructed an impossible flow — fixed: directives soften to "in a guaranteed-rendered position (Mandated-substance rule)" (plan 274, brief 132, review 364, implement 70/90), and the preview rule's prong reworded.
  - F3 review approval-gate presentation still same-turn pre-chip — fixed: step 7 states the presentation ends its turn's rendered text, chip posed after.
  - F4 D-038's operative placement wording left disagreeing with shipped wiring — fixed: D-123 (pre-merge, on-branch) now supersedes D-038's placement wording in the same narrow scope; heading updated.
  - F5 D-123 quoted a phrase D-037's entry does not contain — fixed: D-123 names it as the rule text D-037 shipped.
  - F6 "Chips carry choices, not evidence" name vs hybrid content; "fit" bound — rejected: the name still states the invariant (chips are not the evidence dump) and the fit bound is the cited Accessible-language limits, the bound the plan gate chose.
  - F7 question-gates section unreconciled — rejected: no sentence there mandates pre-tool-call placement; coexistence, not contradiction (the AC2 section read found the same).
  - F8 "at the chip/gate" names no position — rejected: "guaranteed-rendered position" is the defined term doing the naming; "at" locates the gate moment.
  - F9 preview rule's "restated there" antecedent + pre-commit license — fixed in the F2 reword.
  - F10 grammar splice implement 69-72 — fixed with F2; migration parenthetical — rejected as style (pinned line must stay single-line).
  - F11 wrap drift on long directive lines — rejected: prose-guard pins require asserted phrases on one source line (M23/M64), so those lines stay long deliberately; the brief 47-48 orphan wrap was cleaned.
  - F12 CHANGELOG 1.7.0 entry keeps old wording — rejected: released history; M155's change belongs to the next version's section at release time.
  - F13 milestone Decisions section empty despite D-123 — fixed: pointer entry added.
- Post-triage: rulebook re-measured 433 lines / 39,744 chars, baseline re-seeded in its three sites; all suites re-run green (skills 525, scripts, hooks, validate exit 0).
