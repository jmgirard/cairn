# M67: Narration discipline — outcomes, not deliberation (done 2026-07-16)

**Goal:** Add a guard-locked "Narrate outcomes, not deliberation" rule to
the rulebook's output discipline so sessions stop emitting an italic
running readout of reasoning between tool calls.

**Outcome:** Rule shipped in tracking-rules.md "Output & interaction
discipline", adjacent to "Deltas, not dumps" (D-039): interstitial chat
carries findings, decisions, and mandated previews; a one-line signpost
and a compact summary where a question needs context are fine; a running
readout of reasoning (italicized play-by-play included) is never emitted.
Explicit carve-out: D-036/D-037 verbatim previews stay mandated substance.
Guard `skills/tests/test_narration_discipline.py` (3 tests) + 2 mutation
entries. Prompted live by the hitop cairn-init/design-interview session.

**Decisions:** D-039 (bar, central-rule-only wiring — deliberate deviation
from the D-036/D-037 per-skill pattern — and carve-outs).

**Review:** all ACs evidenced; validate 15 PASS; fan-out: 1 sub-threshold
finding (F1/78, mutation block omits trailing colon vs the M65 guidance —
logged, not actioned; registration sound today), other lenses clean.

**PR:** https://github.com/jmgirard/cairn/pull/65
