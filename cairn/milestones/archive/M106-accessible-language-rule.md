# M106: Accessible-language rule — the decision surface leads in plain words, glossing jargon rather than assuming it

**Status:** done (2026-07-20, PR #104 https://github.com/jmgirard/cairn/pull/104)

**Goal:** A new central Output & interaction discipline rule requires the user-facing decision surface — AskUserQuestion question text, chip-framing prose, and option labels/descriptions — to lead in plain language and gloss technical terms rather than assume them, extending "Chips carry choices, not evidence" without displacing its above-the-chip justification clause.

**Outcome:** `tracking-rules.md` gained the "Accessible language on the decision surface" rule (after "Chips carry choices, not evidence"): the question text, chip-framing prose, and option labels/descriptions lead in plain words, glossing a technical term at first use; the named failure is jargon-led framing. It reconciles with the sibling rule — technical justification may stay above the chip but must lead with its plain-language meaning — and that rule gained a cross-reference. Enforcement is authorial judgment, explicitly not a `cairn_validate` check ("too technical" is a judgment, like record density / references staleness). Central-only wiring, no per-skill directive (parallel to D-039). Pinned by `TestAccessibleLanguageRule` (4 tests) + 6 mutation registrations, all anchors single-occurrence (no false coverage).

**Decisions:** none — an additive conduct rule extending D-037's chip rule; complements D-014's Fable steer without superseding it; no D-entry.

**Review:** 6/6 ACs fresh + PASS. 3-lens fan-out (diff-bug [O], blame [S], prior-review [S]) — no findings on any lens; scorer no-op on empty set; actioned list empty. One review-side accuracy fix: rule self-reference "reference" → "references staleness". No lessons captured or retired.
