# M160: Phase-close routing recommends implement for already-planned work

**Status:** done (2026-08-24, PR #161 https://github.com/jmgirard/cairn/pull/161)

**Goal:** Phase-close blocks route an already-planned workable milestone to
`/milestone-implement`, taking their next command from `cairn_next.py`.

**Outcome:** `/milestone-review` step 9 explicitly runs `cairn_validate.py`
over the hygiene edits before the docs-only commit, its `release window`
advisory named as step 10's displacement signal. Step 10 runs `cairn_next.py`
after the hygiene commit and leads the close block's fenced next command with
its recommendation; the D-050 release-parking offer fires whenever the
advisory fired, keeps its decision chip (the one carve-out from the no-chip
close), and displaces the lead only when the recommendation names the flagged
release milestone, per `/milestone` §3. `/milestone` §3 gains a distinct
implement entry for a workable planned milestone; the plan entry's condition
drops planned items and the candidate clause.

**Decisions:** none.

**Review:** user-facing tier, three-lens fan-out. Two lenses clean; diff-bug
lens returned 11 findings — F1/F2 (displacement clause carried only §3's
"lead" half, chip mechanism unnamed) and F4 (§3 plan entry's candidate
condition contradicted `cairn_next`) fixed at the gate, eight rejected with
logged reasons. Nothing graduated or retired.
