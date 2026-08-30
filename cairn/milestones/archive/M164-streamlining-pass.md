# M164: Streamlining pass over shipped code (RB14)

**Status:** done (2026-08-29, PR #165 https://github.com/jmgirard/cairn/pull/165)

**Goal:** Run the one-shot Fable streamlining audit (RB14, advisory) over the shipped code corpus and apply the accepted recommendations.

**Outcome:** RR14: 19 recommendations over the 22-file corpus; 15 applied,
4 rejected (R14 lambda registry kept uniform; R17 CMD_POS consolidation
already a candidate row; R18 `_provenance_block` flag load-bearing; R19
argparse rewords pinned stderr). Shipped: one cached test-module loader
replacing three mechanisms, four duplicate tests removed/merged, hooks-test
sys.path shims hoisted, `resolve_start(start)` replacing fabricated argv,
`_base_commit` on `cc.git` (10s-timeout silent fallthrough accepted → Known
issues), single-call/`slot` simplifications in status/next/cost/validate.
Suites: scripts 327 → 326 (−4 applied removals, +3 gate tests), hooks 121.

**Decisions:** milestone-local only — the R1–R19 triage; the env-prefix
fold-in not firing (no applied item touched either guard); the source-row
hypothesis TRUE: the pass returned accepted changes neither the diff-scoped
review lenses nor `/simplify` would have surfaced.

**Review:** three-lens fan-out; two lenses clean; [O] no correctness bug, 8
ranked findings — 5 fixed at the gate (timeout comment, two TestNext pins,
`TestMissingRRFileFailsLoud`, two tidies), 3 rejected; no return. Graduated
at hygiene: the streamlining-pass candidate row (added 2026-08-05).
