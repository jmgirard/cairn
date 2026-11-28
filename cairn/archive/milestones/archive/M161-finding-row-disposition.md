# M161: Finding-absorbing candidate rows get a disposition trigger at hygiene

**Status:** done (2026-08-26, PR #162 https://github.com/jmgirard/cairn/pull/162)

**Goal:** A candidate row that keeps absorbing deferred review findings is
dispositioned at a hygiene pass rather than extended indefinitely.

**Outcome:** `skills/shared/records-hygiene.md` gains §7: a row carrying
deferred review findings from two or more distinct milestones (per its
provenance/weighed notes) is never silently extended — the extending pass
poses a disposition chip (promote a bounded milestone / route accepted items
to Known issues / prune / extend once explicitly); compression never
substitutes; "extended" = a new provenance/weighed note, no disposition.
Both surfaces defer to §7 rather than restating it: `/milestone`'s audit
triage clause and `/milestone-review` step 9, each at its extension moment.
Ledger compressed 8→5 lines; module 54 lines / 3,187 bytes, under 55/4,000.
Walked D-108's records-conduct door (per D-098) on measured adopter evidence
(quarto-index, circumplex) — the fourth conduct-rule walk of 2026-08;
falsifier in the work log.

**Decisions:** none.

**Review:** user-facing tier → three-lens fan-out; 14 findings: O2 (step-9
ordering) and O8 (dual-trigger precedence) fixed at gate, O13 satisfied by
the door-walk line above, eleven rejected with reasons. Nothing retired.
