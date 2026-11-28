# M10: Deterministic tracking scripts — done

**Status:** done · approved 2026-07-11 · normal · Depends: — · PR #7 (squash
01df055). Promoted from the deterministic-scripts candidate.

## Goal
Read-only scripts over `cairn/` so `/milestone` stops re-deriving status by LLM each session.

## Outcome
Three python3-stdlib reporters under `scripts/`: `cairn_status` (snapshot),
`cairn_next` (Depends-on readiness), `cairn_validate` (8-check consistency
gate: mirror, single in-progress, caps, done-retention, vocab, dependency
resolution, orphans, ID uniqueness; exit 1 fail / 2 outside a cairn repo).
Parser shared via new `cairn_common.parse_roadmap_rows_full` (hooks
untouched). `/milestone` wired to them; semantic checks kept LLM-owned. 18
script + 18 hook tests green; all 6 criteria passed.

## Decisions
- python3-stdlib reusing `cairn_common`, not bash: reuses the tested parser + enforcement layer (supersedes the candidate's "bash").

## Review
Opus review: 1 med + 2 low, all fixed w/ regressions — archived (row-pruned)
done milestones resolve as satisfied deps, dropped-target deps flagged,
numeric ID sort past M99. Deferred→candidate: review-gate/plan wiring,
`--json`, date sweep.
