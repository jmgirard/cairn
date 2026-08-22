# M152: Chat and record prose gain a plain-style rule

**Status:** done (2026-08-22, PR #153 https://github.com/jmgirard/cairn/pull/153)

**Goal:** Give the rulebook a sentence-level plain-style rule for chat output and for durable records, so cairn sessions stop reading as verbose, jargon-laden, trope-filled prose.

**Outcome:** Two rulebook rules: "Plain style" (Output & interaction discipline — length matched to the turn, plain words over jargon, no filler/hype/padding, mandated-verbatim carve-out) and "Records are written plain" (Universal tracking rules — the enumerated `cairn/` record kinds state facts without characterizations, length by cross-reference); the derived-claims exemption sentence names the new governor. `prompting-opus-5.md` re-verified (page grew 11,225→12,483 bytes; no drift in extracted values) and extended with the § Response length and verbosity and § User-facing progress updates values; Traces-to moved to stable anchors. `test_plain_style.py` (8 asserts, 8 mutation entries, hand-run). Rulebook grew 404→413 lines / 36,532→37,567 chars; baselines re-seeded in all three sites. Skills-prose sweep: 119 hits, zero trims. D-108's door passed via its shipped-behavior trigger (maintainer-reported verbosity), recorded in Scope.

**Decisions:** none milestone-local. The T3 ownership-exit widening was reverted at review (see Review); no D-entry shipped.

**Review:** user-facing tier, three-lens fan-out: 18 findings, 10 fixed at the gate — most notably the lesson-retirement ownership-exit widening reverted (it collapsed D-055's maturation bar into D-051's weaker exit with no D-entry), a mandated-verbatim carve-out added to Plain style, and two under-pinned AC1 clauses gained guards — 6 rejected with logged reasons, prior-PR lens a clean no-op. No returns. M114's lesson stays whole: no retirement exit reaches the rulebook.
