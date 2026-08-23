# M69: Cap-overrun diagnostic — per-section breakdown + single-pass compression

**Status:** done (2026-07-17, PR #67 https://github.com/jmgirard/cairn/pull/67)

**Goal:** Make trimming a milestone plan-body under the 150-line cap one
targeted step, not a nibble-and-recount loop.

**Outcome:** `check_caps` reports each over-cap milestone's plan-owned sections
heaviest-first + `shed ≥N` (lines to drop to pass), on a new fence-aware
`milestone_section_line_counts` helper (shares the `## Review` boundary with
`milestone_body_line_count`; `preamble+Σsections==body`). tracking-rules
"Weight caps" remedy now mandates: read the breakdown, compress the heaviest
section in one rewrite (never nibble), cross-reference a durable record rather
than restate it. 2 mutation-registered guards; scripts 96 / skills 221 green.

**Decisions (no D-entry — works under GP1):** work log stays counted (not
exempted like `## Review`; parallels D-030 keeping `## Decisions` counted);
prevention (budget-first drafting) → candidate; what's counted untouched (D-030).

**Review:** 3-lens fan-out; F1 (score 95, 2 lenses) — code emitted the better
`shed ≥N` vs. planned `+N over`; resolved by gated AC amendment to `shed ≥N`,
code unchanged. Prior-PR lens no-op.
