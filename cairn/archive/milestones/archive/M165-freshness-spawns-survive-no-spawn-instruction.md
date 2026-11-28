# M165: Freshness spawns survive a no-unrequested-subagents harness instruction

**Status:** done (2026-08-30, PR #166 https://github.com/jmgirard/cairn/pull/166)

**Goal:** Sessions under a harness instruction restricting subagent spawns to
ones the user requested resolve the conflict with cairn's freshness-mandated
readers and reviewers by asking the user at the pending gate, never by
silently degrading to an author-inline run.

**Outcome:** tracking-rules "Model and agent strategy" gains the
freshness-spawns clause (D-127): skill invocation is the user's request for
the skill-mandated spawns; a still-blocked session asks at its phase's
pending gate with the review declared degraded; author-inline runs only as
user-accepted, logged deviations. Pointers at the four spawn-mandating
sites; hand-run guard `test_freshness_spawn_instruction.py` with six
mutation entries; README sweep clean (6 hits, no edits); second harness
line (workflows/deep-research) left Out.

**Decisions:** D-127 (cross-cutting; narrows the review fan-out's and
D-067's fresh-context absolutes to admit the logged-deviation path).

**Review:** full three-lens fan-out; both [S] lenses clean; [O] returned 13
findings — 3 fixed at the gate (D-127; trigger-subject pins; clause name
made greppable), 10 rejected with logged reasons. Hygiene retired the M99
rewrite-disposal lesson (enforcement: validate's roadmap<->disk orphans).
