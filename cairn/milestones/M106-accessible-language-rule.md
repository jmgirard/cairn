# M106: Accessible-language rule — the decision surface leads in plain words, glossing jargon rather than assuming it

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m106-accessible-language-rule / https://github.com/jmgirard/cairn/pull/104

## Goal

A new central Output & interaction discipline rule requires the user-facing decision surface — AskUserQuestion question text, the prose framing a chip, and option labels/descriptions — to lead in plain language and gloss technical terms rather than assume them, extending "Chips carry choices, not evidence" without displacing its above-the-chip justification clause.

## Scope

**In:**
- A standalone "Accessible language" rule added to `tracking-rules.md` Output & interaction discipline, adjacent to "Chips carry choices, not evidence" (`tracking-rules.md:507`).
- The rule governs the **decision surface**: AskUserQuestion question text, the prose that frames a chip, and option labels/descriptions.
- Reconciliation with the existing clause (gate choice): technical detail may still live above the chip, but must **lead with its plain-language meaning and define jargon at first use** rather than banish it — the existing clause stays intact and gains a cross-reference.
- Central-rule-only wiring (parallel to D-039's narration discipline): no per-skill directive.
- One mutation-registered prose-guard pinning the new rule's load-bearing wording.

**Out:**
- Per-skill gate-step directives (the D-036/D-037 pattern) → not this milestone; a future milestone only if central-only drifts (the D-039 supersede path).
- A `cairn_validate` mechanical readability/jargon advisory → rejected at the plan gate as off-model (judgment is an advisory at most, never a gate — density/staleness precedent); not planned.
- Superseding D-014's Fable steer for `/design-interview` → out; the model steer stands, this rule complements it.
- Changing the substance of the existing "Chips carry choices" clause → out; it is preserved, only cross-referenced.

## Acceptance criteria

- [x] A new standalone "Accessible language" rule exists in `tracking-rules.md` Output & interaction discipline, adjacent to "Chips carry choices, not evidence," governing the decision surface (question text, chip-framing prose, option labels/descriptions) with a lead-in-plain-language bar.
- [x] The rule mandates glossing/defining a technical term at first use rather than assuming it, and names jargon-led framing as the failure it prevents.
- [x] The rule reconciles with the existing clause: technical justification may remain above the chip but must lead with its plain-language meaning; the existing "Chips carry choices, not evidence" wording is preserved and cross-references the new rule.
- [x] The rule is wired central-only: no per-skill accessible-language directive is added, confirmed by the diff touching only `tracking-rules.md` and test files.
- [x] A mutation-registered prose-guard pins the new rule's load-bearing wording and reddens when its block is blanked; the mutation-harness completeness meta-test passes.
- [x] The dogfood verify is clean: all three unittest suites (`skills/tests`, `scripts/tests`, `hooks/tests`) green and `cairn_validate` exits 0.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1, T2
- AC4 → T1, T4
- AC5 → T3
- AC6 → T4

## Tasks

- [x] T1 — Draft the "Accessible language" rule block in `tracking-rules.md` adjacent to "Chips carry choices, not evidence" (`tracking-rules.md:507`): decision-surface scope, the lead-in-plain-language + gloss-jargon-at-first-use bar, the named failure (jargon-led framing), and the reconciliation clause that keeps technical justification above the chip but plain-led.
- [x] T2 — Add a cross-reference from "Chips carry choices, not evidence" to the new rule; leave that rule's existing wording otherwise intact.
- [x] T3 — Author a mutation-registered prose-guard on the new rule's load-bearing wording (extend `test_gate_conclusion_preview.py` or a sibling): copy anchors byte-exact from the committed rule, use `\s+` matchers to span line-wraps (M105 lesson), and register the block in `test_mutation_harness.py`.
- [x] T4 — Run all three suites + `cairn_validate` from the repo root, checking each exit code; confirm green, that the new guard reddens under mutation, and that the diff touched only `tracking-rules.md` + test files.

## Work log

- 2026-07-20: created by /milestone-plan.
- 2026-07-20: T1–T4 done — new "Accessible language on the decision surface" rule added to tracking-rules.md after "Chips carry choices"; cross-ref added into that rule; TestAccessibleLanguageRule (4 tests) + 6 mutation registrations; all three suites green, cairn_validate exit 0, no SKILL.md touched. Status → review.

## Decisions

## Review

**AC evidence (fresh, PR #104):**
- AC1 → PASS. `tracking-rules.md:515-525` carries the new "Accessible language on the decision surface." rule; `TestAccessibleLanguageRule.test_rule_present_and_scopes_the_decision_surface` green (title + the "AskUserQuestion question's text, the prose framing a" scope).
- AC2 → PASS. `test_rule_glosses_jargon_and_names_the_failure` green ("glossed at first use, never assumed" + "jargon-led framing, where the user must already know the").
- AC3 → PASS. `test_rule_reconciles_with_chips_carry_choices` + `test_cross_reference_from_chips_carry_choices` green; existing rule intact — `TestAcceptanceChipsRule.test_chips_carry_choices_rule_present` still green (`tracking-rules.md:507-514`).
- AC4 → PASS. `git diff --name-only origin/main..HEAD` → 0 `SKILL.md`; touched: tracking-rules.md, 2 test files, + M106 file & ROADMAP bookkeeping only.
- AC5 → PASS. Mutation harness green via discover (9 tests OK); `REGISTRY` holds 6 AccessibleLanguage entries, each blanked → its guard reddens.
- AC6 → PASS. skills 562 / scripts / hooks 72 all exit 0; `cairn_validate` exit 0 (1 pre-existing references-staleness advisory WARN, untouched by the diff).

**Consistency gate:** `cairn_validate` exit 0. Generic profile → no toolchain consistency-gate checks (no-op). No principle change (Principles touched: —) → `cairn_impact` skipped.

**Fan-out (3 lenses + scorer):** diff-bug [O], blame-history [S], prior-review [S] — all **no findings**. Verified independently: all 6 guard anchors occur exactly once in `tracking-rules.md` (no false coverage), each sits inside the new rule, mutation blocks byte-exact, existing "Chips carry choices" wording preserved, no contradiction with D-036/D-037/D-038/D-039/D-014, central-only wiring confirmed (no SKILL.md). Prior-review probe `gh api …/pulls/comments` → `[]` (no GitHub threads). Scorer no-op on an empty finding set. Actioned list empty.
Review-side fix: the rule's self-reference "reference staleness" → "references staleness" to match the actual advisory name (one word; touches no guard/anchor; blame lens noted it as style, corrected for accuracy). skills suite 562 green + `cairn_validate` exit 0 after the fix.
