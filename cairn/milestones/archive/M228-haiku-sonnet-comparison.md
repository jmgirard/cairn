# M228: Compare Haiku 5.5 with Sonnet 5.5 on cairn's Sonnet roles

**Status:** done (2026-10-10, PR #236 https://github.com/jmgirard/cairn/pull/236)

**Goal:** A committed note measures whether Haiku 5.5 does the work of each Sonnet role group for less money and with no loss of quality.

**Outcome:** `cairn/references/haiku-sonnet-roles.md` runs nine replayed
tasks, each once on Sonnet 5.5 and once on Haiku 5.5. Costs come from
subagent transcripts, and are lower bounds because the transcripts record
output at stream start. Verdicts under a 0.9 score margin: search `stay`
(S2's missing `.py` is the whole gap), edit work `move` (both 1.0, Haiku at
8% of the cost), history review `move` (4 against 4 judged findings, Haiku
at 71% of the cost, a cost comparison the undercount can reverse; it does
not test D-016's missed-bug risk). `session-cost-notes.md` row A4 is
marked `corrected M228`. M229 stops for the user on these mixed verdicts.

**Decisions:** milestone-local: the measurement's Haiku spawns are a scoped
exception to "Never Haiku"; D-016 stands until M229. AC3 was amended once to
take final-call output from the Agent tool result.

**Review:** two returns, both on AC4 as written (a broader judge rule than
the note stated, then key procedures given as prose). Two three-lens rounds:
36 findings fixed, 3 rejected, and `cairn_cost.py`'s session-store reading
sent to a new `[high]` candidate row. The user stopped a third reviewer
round as churn; pass 3 re-ran the evidence only. Nothing retired.
