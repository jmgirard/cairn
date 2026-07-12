<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M29: Make routing-chip invocation an imperative on the orchestrator

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m29-routing-chip-invocation-imperative · https://github.com/jmgirard/cairn/pull/27

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

- [x] The routing-chip rule states an imperative: on selecting a routing-chip
      option the orchestrator immediately invokes the target skill (via the
      Skill tool) and does not stop to have the user type the command.
      Evidence: rule text + guard assertion.
- [x] The rule preserves the "chip is a user stop — never auto-proceed"
      clause without contradicting the imperative (stop before selection;
      selection is the go). Evidence: rule text.
- [x] The rule clarifies that the `→ /skill` chip-option notation names the
      skill the orchestrator invokes, not a command for the user to run.
      Evidence: rule text + guard assertion.
- [x] A guard in `test_gate_wording.py` locks the imperative + notation
      phrasing and fails if the rule reverts to the descriptive form.
      Evidence: the new test passes; asserted phrases are single-line
      (M23) and matched case-insensitively (M26).
- [x] D-022 (annotating D-003) records the mechanism clarification with its
      rationale. Evidence: the D-entry in `cairn/DECISIONS.md`.
- [x] Full guard suite (`python3 -m unittest discover -s skills/tests`) and
      `cairn_validate` audit both clean. Evidence: command output.

## Coverage

- AC1 → T2, T1
- AC2 → T2
- AC3 → T2, T1
- AC4 → T1
- AC5 → T3
- AC6 → T3

## Tasks

- [x] T1: Add `TestChipInvocationImperative` to
      `skills/tests/test_gate_wording.py` — assert tracking-rules carries the
      imperative sentence (invoke on selection; never hand back) and the
      notation clause. Single-line, case-insensitive assertions (M23/M26).
      Red until T2.
- [x] T2: Rewrite the routing-chip paragraph in
      `skills/shared/tracking-rules.md:279-281` to the imperative + preserved
      stop clause + notation clarification; green T1. Keep asserted phrases
      on single physical lines.
- [x] T3: Append D-022 annotating D-003 to `cairn/DECISIONS.md`; run the full
      guard suite + `cairn_validate`; record evidence.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: T1 — added `TestChipInvocationImperative` (3 assertions:
  imperative, never-hand-back, notation clause); red until T2 as planned.
- 2026-07-12: T2 — rewrote the routing-chip paragraph to the imperative
  (invoke via Skill tool on selection; never hand back) + preserved
  never-auto-proceed stop + `→ /skill` notation clause; full 11-test
  `test_gate_wording` suite green.
- 2026-07-12: T3 — appended D-022 (annotates D-003); full guard suite
  (74 tests) + `cairn_validate` audit both clean. Status → review.

## Decisions

## Review

2026-07-12 · PR #27 · branch `m29-routing-chip-invocation-imperative`.
R gates waived (this repo is the plugin, not an R package); the equivalent
gate is the guard suite + `cairn_validate`.

**Acceptance-criteria evidence (fresh):**
- AC1 (imperative): `tracking-rules.md:281–282` — "the orchestrator
  immediately invokes the target skill via the Skill tool … does not stop to
  have the user type the command"; guard
  `TestChipInvocationImperative` (2 of 3 assertions) green.
- AC2 (preserved stop): `tracking-rules.md:283` — "a chip is an explicit user
  stop — never auto-proceed — but the stop is *before* selection".
- AC3 (notation): `tracking-rules.md:286` — "names the skill the orchestrator
  invokes on selection, not a command for the user to run"; guard assertion
  green.
- AC4 (guard): `TestChipInvocationImperative` runs 3/3 OK; phrases asserted
  case-insensitively (`.lower()`) on single physical lines (M23/M26); a revert
  to the descriptive form drops the imperative phrase → red.
- AC5 (D-022): `DECISIONS.md:346` — D-022 present, annotates D-003, records
  rationale (M28 slip, D-011/GP4).
- AC6 (suites): `python3 -m unittest discover -s skills/tests` → 74 tests OK;
  `cairn_validate.py` → exit 0, all 10 checks PASS.

**Consistency gate:** `cairn_validate` exit 0. Coverage completeness — all six
ACs map to existing tasks (AC1→T2,T1 · AC2→T2 · AC3→T2,T1 · AC4→T1 · AC5→T3 ·
AC6→T3). No DESIGN principle changed (impact scan skipped). No R/README/pkgdown/
NEWS surface in this repo.

**Independent review (two lenses + scorer):**
- [O] diff-bug (Opus): 1 finding — D-022 Context misattributed the quote
  "selecting a chip invokes that skill in the same session" to D-003, when it
  was the pre-M29 `tracking-rules.md` wording D-003 produced.
- [S] blame-history (Sonnet): no findings — M29 is a strict tightening of the
  M26/D-019 mandate; no prior work undone, no guard masking.
- [S] scorer (Sonnet): scored the finding **93** (≥80 → actioned). Below-80
  findings: 0.
- Triage: **fixed now** — reworded D-022 Context to frame the quote as the
  rulebook rule D-003 produced (not a quote from D-003 itself). Pre-merge
  correction on the branch, not a rewrite of merged history.

