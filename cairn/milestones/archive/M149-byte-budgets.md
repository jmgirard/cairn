# M149: The line caps gain byte budgets

**Status:** done (2026-08-17, PR #150 https://github.com/jmgirard/cairn/pull/150)

**Goal:** ROADMAP and LESSONS gain fixed byte budgets (< 24,000 / < 20,000
bytes), stated as prose and judgment-checked at hygiene passes, so an item
file cannot defeat its line cap by line width.

**Outcome:** Byte budgets in the rulebook's Weight caps (flat line-cap × 400
allowance; `wc -c`; no validator check — machinery declined at the
checker-regress gate) with a compress-widest-rows-first ROADMAP remedy and an
imported LESSONS retire-or-prune remedy; budgets propagated to all six
cap-stating surfaces (cairn-init ×2, migration-protocol, milestone-review,
LESSONS header, rulebook); `wc -c` check wired into the `/milestone` health
audit and `/milestone-review` post-merge hygiene; D-119 records the fired
D-058 falsifier, the D-108 and D-057/D-114 doors, and the prose form's own
falsifier; instrument-adoption row annotated (weighed, not fired); rulebook
mass baseline re-seeded (404/36,532) with its two hand-run pins.

**Decisions:** D-119; AC4 amended (narrowed) at a mini gate — D-116 part 2
conflict and a self-firing falsifier — two fresh readers plus user acceptance.

**Review:** three-lens fan-out (user-facing tier): 19 findings, 12 actioned
fix-now on the branch (D-119 hardening, remedy re-ordering, single-sourcing,
cite fixes, baseline re-seed), 2 rejected with reason, none at the return
floor; suites green throughout.
