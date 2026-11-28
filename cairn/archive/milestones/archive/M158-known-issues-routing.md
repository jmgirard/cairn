# M158: DESIGN.md Known issues gains a lifecycle — review hygiene routes accepted limitations there

**Status:** done (2026-08-23, PR #159 https://github.com/jmgirard/cairn/pull/159)

**Goal:** Add one routing clause to `/milestone-review`'s post-merge hygiene step so an accepted durable limitation lands in `cairn/DESIGN.md`'s Known issues section.

**Outcome:** Step 9 of `skills/milestone-review/SKILL.md` gains a "Route accepted limitations:" block between the lessons-capture and retirement blocks: a durable limitation the milestone surfaced, the user chose to live with, and no candidate row or fix covers, gets a Known issues entry written in the same hygiene commit. At review direction, the Known issues entry joined the durable-record preview enumerations in both that skill and `skills/shared/tracking-rules.md`.

**Decisions:** none.

**Review:** Three-lens fan-out (user-facing tier). Prior-review lens: no prior-review evidence, zero findings. Blame-history: no blocking issues; its self-assessed-door flag on the conduct-rule trigger was noted and rejected (the reviewer's own scrutiny found the trigger genuine). Diff-bug: nine findings — F1 (new record type escaped the durable-record preview enumerations) fixed on both surfaces at the gate, F9 (work-log blank line; snapshot-time uncommitted edits) fixed/resolved, seven rejected with reasons (routing-trigger misreading, plan-gate-decided outflow, hardening beyond scope, deferral-vs-decision ownership, scaffold repair out of scope, lessons-capture-equivalent epistemics, deliberate placement). No return-floor crossing; nothing graduated or retired.
