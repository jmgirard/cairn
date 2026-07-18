# M71: Idea-capture intake gate — out-of-band ideas also land as candidates

**Goal.** An idea surfaced through a non-cairn capture channel also lands as a
ROADMAP candidate row — doctrine plus a non-blocking runtime nudge.

**Outcome.** New "Out-of-band idea capture" rule in `tracking-rules.md`'s Intake
section: a chip / scratch TODO / ad-hoc note is a pointer, never the record of
record; the idea lands as a `candidate` row in the same turn. Runtime arm:
`hooks/idea_guard.py`, a fail-permissive PreToolUse hook on `mcp__.*__spawn_task`
emitting `additionalContext` and no `permissionDecision` — the eighth hook, third
advisory nudge. Guards: `TestIdeaGuard`, no-op / garbage-stdin / registration
coverage, `test_idea_intake_gate.py` (3 mutation-registered), `HOOKS` + DESIGN.

**Decisions.** D-042 — rule *and* hook (prose alone missed the circumplex case:
no skill was loaded); chip paired, not forbidden; channel-agnostic rule, one
wired channel; D-017's lever.

**Review.** All 6 AC verified fresh; scripts 96 / skills 234 / hooks 60 exit 0;
`cairn_validate` all-PASS. Fan-out: diff-bug 3, blame clean, prior-PR no-op.
**F1 (87) fixed** — the rule's justification ("nothing outside `cairn/` is read
at plan time") overclaimed and contradicted the Intake inbox rule; narrowed to
"authoritative tracking state". F2 (55) / F3 (63) logged below threshold; F3 →
candidate. Deviation: T2–T7 landed in one commit, not per-task checkpoints.

**PR.** https://github.com/jmgirard/cairn/pull/69
