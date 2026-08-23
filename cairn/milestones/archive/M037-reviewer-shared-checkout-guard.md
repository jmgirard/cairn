# M37: Fence cairn subagents off the shared checkout (ref-based git only)
- **Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/35

## Goal

Stop any cairn-spawned subagent from moving the shared primary checkout's HEAD,
closing the M36-review disruption.

## Outcome

Three prose+guard edits (no runtime surface): (1) `tracking-rules.md` — new
general rule "Subagents share the primary checkout": every spawned subagent
uses ref-based git only (`diff`/`show`/`log`/`blame`), never a HEAD-moving
command (`checkout`/`switch`/`worktree add`/`reset`) in the shared tree; binds
every agent, not just reviewers. (2) `milestone-review/SKILL.md` — pointed
reminder at the step-5 reviewer fan-out. (3) `test_review_fanout.py` —
`TestSharedCheckoutGuard` locking both wordings, single-line-anchored (M23/M26).
Verified: suite 85/85, `cairn_validate` 11/11; two-lens review (both ref-based,
dogfooding the new rule) → zero findings.

## Key decisions

Scope generalized at the plan gate from the review fan-out to all shared-tree
subagents. Worktree-isolation spawn flag rejected (non-portable, unlockable by
a prose guard). No D-entry — operationalizes existing review discipline.
