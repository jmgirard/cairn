# M97 — Bounded DECISIONS read — the sweep scans headings and reads what it hits

**Status:** done · approved 2026-07-19 · PR #94

## Goal
Scan `DECISIONS.md`'s `### D-` headings instead of sweeping it whole, recording the IP2
recall trade as a D-entry rather than slipping it in as an optimization.

## Outcome
A typical sweep reads 9,141 chars instead of 100,678 — **90.9% less** on over half the
plan-time read. Stated once in `tracking-rules.md`, wired at both sweep sites. New
`decision heading quality` advisory (WARN, from D-054). IP4 untouched: pure append.

## Decisions
- D-054 annotates IP2, bounding the trade three ways: prospective heading advisory,
  back-reference by id, and the scan being a model read rather than a literal grep.
- AC2 amended (gated) to add the back-reference — D-012/D-014/D-019 hide a supersession
  IP4 forbids repairing, so the protocol closes the gap, not the headings. The advisory
  is scoped from D-054: one that cannot reach OK gets ignored.

## Review
One trip, gate green. 3 lenses + scorer: blame-history 0, prior-PR a clean no-op (28 PRs,
0 comments), diff-bug 7. Actioned F7/80 (an AC2 miss whose guard checked only half) and
F5/42 *despite* score (M73/M88) — a test named for the exit code that never asserted on
it, recurring after M84/M93×2/M94. Five sub-80 findings banked: they interact.
