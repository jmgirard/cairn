# M240: Measure medium effort on the history reviewers, and state each spawned role's effort level

**Status:** done (2026-10-10, PR #250 https://github.com/jmgirard/cairn/pull/250)

**Goal:** The rulebook states the reasoning-effort level each spawned role uses, backed by a committed measurement of `medium` effort on the history reviewers.

**Outcome:** `cairn/references/effort-review-medium.md` runs M228's three
history-review tasks (Sonnet) at `medium` and with `effort` unset, beside
M239's default runs, one blind Opus judge per task. Scores: M239 default 3,
new default 3, `medium` 2. Costs: $0.88, $0.98, $0.67. Verdict `default`.
Tracking-rules "Model and agent strategy" gains "Leave effort unset on
every spawn", citing both effort notes. The review skill is unchanged. The
rulebook mass baseline is re-seeded, and the page is pinned `ok`.

**Decisions:** D-157 (no subagent role sets `effort`), and D-158, which
corrects three of its clauses. The question set narrowed the plan to a
`medium` test on history review only.

**Review:** no return. Three-lens fan-out, 14 findings: 8 fixed, 3 to
hygiene (the effort row narrowed to the Opus and Fable roles), 3 rejected
(no changelog entry, twice, since no spawn's behavior changes; an older
figure in the append-only work log). Copilot (Lite): 1 fixed. Claim audit:
13 claims, 1 corrected. No lesson added or retired.
