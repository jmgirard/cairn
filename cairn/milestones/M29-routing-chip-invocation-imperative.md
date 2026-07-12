<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M29: Make routing-chip invocation an imperative on the orchestrator

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** —

## Goal

Rewrite the routing-chip rule so selecting a chip is an imperative to invoke
the target skill (never hand back to the user to type the command), clarify
the `→ /skill` notation, lock the imperative wording with a guard, and record
the mechanism clarification as a D-entry annotating D-003.

## Scope

**In:**
- Rewrite the "Question gates and routing chips" paragraph
  (`skills/shared/tracking-rules.md:279-281`): turn the descriptive
  "Selecting a chip invokes that skill in the same session" into an
  imperative aimed at the orchestrator — on selecting a routing-chip option,
  immediately invoke the target skill via the Skill tool; never stop to have
  the user type the command. Preserve the existing "chip is an explicit user
  stop — never auto-proceed" clause without contradiction (the stop is
  *before* selection; the selection is the go).
- Add a clause clarifying the `→ /skill` chip-option notation names the skill
  the orchestrator invokes on selection, not a command for the user to run.
- Add a rule-wording guard (in `test_gate_wording.py`) asserting tracking-rules
  carries the imperative sentence and the notation clause.
- Append D-022 annotating D-003 (mechanism clarification + M28-slip / D-011-GP4
  rationale).

**Out:**
- Per-skill invoke-on-selection tokens (guarded per skill) → decided against
  at the plan gate; the invocation rule is uniform conduct stated once
  centrally. Revisit only if the central rule proves insufficient.
- Changing the `→ /skill` notation across the eight skills' example menus →
  rejected at the gate (keep the arrows; clarify their meaning in the rule).
- Review's chip-less exception (D-019) and the merge-approval chip → untouched.

## Acceptance criteria

- [ ] The routing-chip rule states an imperative: on selecting a routing-chip
      option the orchestrator immediately invokes the target skill (via the
      Skill tool) and does not stop to have the user type the command.
      Evidence: rule text + guard assertion.
- [ ] The rule preserves the "chip is a user stop — never auto-proceed"
      clause without contradicting the imperative (stop before selection;
      selection is the go). Evidence: rule text.
- [ ] The rule clarifies that the `→ /skill` chip-option notation names the
      skill the orchestrator invokes, not a command for the user to run.
      Evidence: rule text + guard assertion.
- [ ] A guard in `test_gate_wording.py` locks the imperative + notation
      phrasing and fails if the rule reverts to the descriptive form.
      Evidence: the new test passes; asserted phrases are single-line
      (M23) and matched case-insensitively (M26).
- [ ] D-022 (annotating D-003) records the mechanism clarification with its
      rationale. Evidence: the D-entry in `cairn/DECISIONS.md`.
- [ ] Full guard suite (`python3 -m unittest discover -s skills/tests`) and
      `cairn_validate` audit both clean. Evidence: command output.

## Coverage

- AC1 → T2, T1
- AC2 → T2
- AC3 → T2, T1
- AC4 → T1
- AC5 → T3
- AC6 → T3

## Tasks

- [ ] T1: Add `TestChipInvocationImperative` to
      `skills/tests/test_gate_wording.py` — assert tracking-rules carries the
      imperative sentence (invoke on selection; never hand back) and the
      notation clause. Single-line, case-insensitive assertions (M23/M26).
      Red until T2.
- [ ] T2: Rewrite the routing-chip paragraph in
      `skills/shared/tracking-rules.md:279-281` to the imperative + preserved
      stop clause + notation clarification; green T1. Keep asserted phrases
      on single physical lines.
- [ ] T3: Append D-022 annotating D-003 to `cairn/DECISIONS.md`; run the full
      guard suite + `cairn_validate`; record evidence.

## Work log

- 2026-07-12: created by /milestone-plan.

## Decisions

## Review
