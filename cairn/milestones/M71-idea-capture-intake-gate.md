<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M71: Idea-capture intake gate — out-of-band ideas also land as candidates

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP3, GP2, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m71-idea-capture-intake-gate`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

An idea surfaced through a non-cairn capture channel also lands as a ROADMAP
candidate row, enforced by doctrine plus a non-blocking runtime nudge.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a channel-agnostic out-of-band idea-capture rule in the
`tracking-rules.md` Intake paragraph (adjacent to the M39 search-first rule);
`hooks/idea_guard.py`, a fail-permissive PreToolUse hook wired to the
background-task chip tool that injects a non-blocking `additionalContext`
reminder (the D-017 lever: no `permissionDecision`); its registration in
`hooks.json`; hook tests (emission + no-op + garbage stdin + registration);
a mutation-registered prose guard; D-042.

**Out:** forbidding or gating the chip itself — the chip stays a useful
affordance, only its record-of-record status is denied (settled at the plan
gate, recorded in D-042, not re-openable inside this milestone). Wiring a
second capture channel (scratch TODOs, other task tools) → the rule already
covers them channel-agnostically; a second hook needs its own candidate row
once such a channel exists. Live-fire confirmation that the hook actually
fires → post-merge in a brand-new conversation, since hook *registrations*
snapshot at process start (M60); this milestone's evidence is fixture-level.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] `skills/shared/tracking-rules.md`'s Intake paragraph states a
      channel-agnostic rule: an idea surfaced through any out-of-band capture
      channel also lands as a ROADMAP candidate row (search-first applies),
      and such a capture is never the record of record. Evidence: the rule
      text quoted from the file.
- [ ] `hooks/idea_guard.py`, given a chip-tool PreToolUse payload with a cwd
      inside a cairn repo, emits `hookSpecificOutput.additionalContext` naming
      the candidate-row requirement and emits **no** `permissionDecision`.
      Evidence: a passing hook test asserting both.
- [ ] The hook is fail-permissive: exit 0 with empty stdout/stderr for a
      non-cairn cwd, a non-matching tool name, and garbage stdin — proven by
      `idea_guard.py` entries in `TestNonCairnNoOp`'s two payload collections
      in `hooks/tests/test_hooks.py`.
- [ ] `hooks/hooks.json` registers `idea_guard.py` under PreToolUse with the
      matcher T1 establishes and the `python3 … || py -3 …` + `timeout`
      envelope, asserted by a new test in `TestHooksRegistration`.
- [ ] A prose guard locks the new rulebook rule, is registered in
      `skills/tests/test_mutation_harness.py`, and the completeness meta-test
      passes (the guard fails when its block is blanked).
- [ ] `verify` clean: `python3 -m unittest discover` green for `scripts/tests`,
      `skills/tests`, and `hooks/tests`, each run from the repo root with its
      exit code read directly (M56/M65).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2
- AC2 → T3, T5
- AC3 → T3, T5
- AC4 → T1, T4
- AC5 → T6
- AC6 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Establish from the official hooks docs whether a PreToolUse
      `matcher` matches an MCP tool name (`mcp__ccd_session__spawn_task`). If
      not, fall back to a broad matcher with in-hook `tool_name` filtering.
      Record the finding in one work-log line (the D-017 T1 pattern).
- [x] T2 — Write the rule into `skills/shared/tracking-rules.md`'s Intake
      paragraph (~line 199), next to search-first. Keep the guard's anchor
      phrase on ONE physical line (M59/M64 reflow trap).
- [x] T3 — Implement `hooks/idea_guard.py` on the `memory_guard.py` skeleton:
      `cairn_common.read_input` / `find_cairn_root`, `additionalContext` only,
      no `permissionDecision`, silent no-op on every other path.
- [x] T4 — Register the hook in `hooks/hooks.json` per T1; extend
      `TestHooksRegistration` with its assertion.
- [x] T5 — Hook tests: a `TestIdeaGuard` emission class, plus `idea_guard.py`
      added to BOTH `TestNonCairnNoOp` payload collections
      (`test_every_hook_is_silent_and_permissive` and
      `test_garbage_stdin_is_permissive`).
- [x] T6 — Prose guard for the rulebook rule + its `Mutation(...)` entry in
      `skills/tests/test_mutation_harness.py`; confirm by mutation, not by eye.
- [x] T7 — Run all three suites from the repo root, checking exit codes before
      any commit; update `cairn/DESIGN.md`'s hook inventory line (~line 49,
      which enumerates the shipped hooks) in the same commit.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan; four plan-gate choices recorded as D-042.
- 2026-07-18: branch `m71-idea-capture-intake-gate` cut from main; status in-progress.
- 2026-07-18: T1 — hooks docs confirm MCP tool names ARE matchable; a matcher of only word chars is compared as an EXACT string, so the server-agnostic `mcp__.*__spawn_task` regex is used rather than the bare tool name.
- 2026-07-18: T2–T7 landed in one checkpoint rather than per-task commits — deviation from the per-task cadence, recorded honestly; no task was skipped.
- 2026-07-18: minor amendment — T7 grew to include `skills/tests/test_positioning_guard.py`'s hardcoded `HOOKS` tuple (the M48 registered-kind trap: it is the only check that DESIGN's inventory tracks `hooks/`).
- 2026-07-18: verify clean — scripts 96, skills 234, hooks 60 (exit 0 each, read directly, no pipes); `cairn_validate` all-PASS.
- 2026-07-18: status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->
