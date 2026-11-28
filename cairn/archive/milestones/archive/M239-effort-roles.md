# M239: Compare low with default reasoning effort on cairn's Sonnet and Haiku roles

**Status:** done (2026-10-10, PR #249 https://github.com/jmgirard/cairn/pull/249)

**Goal:** A committed note measures, per role group, whether the group's model at `low` reasoning effort does its work for less money and with no loss of quality against the same model at default effort.

**Outcome:** `cairn/references/effort-roles.md` replays M228's nine tasks
with the Agent tool's `effort` unset (recorded `high`) and set to `low`:
Sonnet for search and history review, Haiku for edit work, search and edit
runs in `c023018` copies. Costs use M228's method, and a background run's
final-call output comes from its completion notification. Verdicts: search
`low` (equal scores, a 1.6% cost gap the undercount can reverse), edit
work `low` (both at the ceiling, 10% gap), history review `default` (2
judged-valid findings against 4, within M228's run-to-run spread). The
page is pinned `ok` in the shipped-page ledger test.

**Decisions:** none promoted. Question set: plan the effort dial, and
measure before naming any level. The verdict `untested` covers a model
that ignores the setting. No group was `untested`.

**Review:** no return. Three-lens fan-out, 23 findings: 21 fixed, 1
rejected (the cost amendment as an AC3 failure: same figure, shown by the
`subagent_tokens` = `totalTokens` identity), 1 to hygiene (the effort row
rewritten, re-rated normal). Copilot (Lite): 2 fixed. No lesson added
(the note owns the background-spawn record facts) or retired.
