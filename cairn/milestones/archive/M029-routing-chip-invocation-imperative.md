# M29: Make routing-chip invocation an imperative on the orchestrator

**Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/27 · 2026-07-12

**Goal.** Turn the routing-chip rule from descriptive into an imperative on
the orchestrator, so selecting a chip option invokes the target skill rather
than handing back to the user to type the command.

**Outcome.** Rewrote the "Question gates and routing chips" paragraph in
`skills/shared/tracking-rules.md`: on selecting a routing-chip option the
orchestrator immediately invokes the target skill via the Skill tool and does
not stop to have the user type the command. Clarified that the `→ /skill`
notation names the skill the orchestrator invokes, not a user command.
Preserved the "never auto-proceed" stop (stop is *before* selection). New
guard `TestChipInvocationImperative` in `skills/tests/test_gate_wording.py`
locks the imperative + notation phrasing (3 assertions, single-line,
case-insensitive). All 74 guard tests + `cairn_validate` clean.

**Key decision.** D-022 (annotates D-003) — records the descriptive→imperative
mechanism clarification and its M28-slip / D-011-GP4 rationale.

**Review.** Two-lens fresh review: blame-history clean; diff-bug found D-022
misquoting D-003 (scored 93), fixed on the branch pre-merge.
