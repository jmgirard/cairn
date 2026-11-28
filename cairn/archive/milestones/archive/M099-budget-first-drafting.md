# M99: Budget-first drafting — a capped artifact's size is visible while it is written

**Status:** done (2026-07-20, PR #96 https://github.com/jmgirard/cairn/pull/96)

**Goal:** Make a capped artifact's size visible at drafting time, so first
drafts land under cap by construction rather than by compression afterward.

**Outcome:** `scripts/cairn_budget.py` reports any path against whichever cap
applies across six artifact classes, every cap read from `cairn_scripts` so
drafting and gate counters cannot diverge; measured per-section budgets in
`templates/milestone.md` (p75 over 99 milestone files from git history); a new
comment-free `templates/archive-summary.md`, also fixing label drift across 96
summaries. Counters wired into `/milestone-plan` 4 and `/milestone-review` 9.

**Decisions:** Archive template is comment-free — house-style comments would
spend a fifth of a 25-line budget. Budgets stay guidance: a per-section cap is
the split-budget shape D-030 declined. No cap number moved.

**Review:** 3 lenses + scorer. F1 (92) exit-verdict gap, F2 (88) section-less
CLAUDE.md exiting 2, F4 (85) step 9 dropping the live file's disposal, F6
(merge gate) self-referential template figures — all fixed; F3 (72)/F5 (35)
logged and fixed anyway (M73). Trimmed M51's lesson to its remainder (D-051).
