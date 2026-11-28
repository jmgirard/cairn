# M16: Lessons loop (capture → harvest) — done 2026-07-11

**Goal:** record what a milestone *taught* — durable repo lessons (build
quirks, testing tricks) — not just what happened; surface them at plan time.

**Outcome:** `cairn/LESSONS.md`, a fourth top-level tracking file —
append-only, one line per lesson (`- YYYY-MM-DD (M<NN>): …`), capped at 50
lines. The loop closes at both ends: `/milestone-review` post-merge hygiene
**captures** lessons in the same docs-only commit that archives; `/milestone-plan`
**harvests** them at session start and surfaces relevant ones before the
question gate (intake, not obedience). Lessons ≠ decisions (a choice with
rationale is a D-entry). Wired into tracking-rules (file-map, boundary,
weight-caps), CLAUDE.md boundary, `cairn_scripts.LINE_CAPS`, and the
`cairn_validate` ISO-date scan. Locked by `test_lessons_loop.py` (wiring +
stated↔enforced cap) and two `scripts/tests` fixtures (over-cap, non-ISO date).

**Decision:** D-015 — lessons home + capture/harvest loop (cross-cutting;
inherited by every adopting repo).

**Review:** no must-fix defects; all 5 ACs met with fresh evidence. 3 of 4
nice-to-haves fixed (substring locks → step-text anchors; date-scan lock
added; comment reworded); "50 lines" wording rejected (every cap is `< N`).
skills 27 · scripts 31 · cairn_validate exit 0.

PR #14 (squash-merged).
