# M65: Gate-time conclusion preview — acceptance chips show what's accepted

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Principles touched:** GP4
- **Branch/PR:** m65-gate-conclusion-preview · https://github.com/jmgirard/cairn/pull/63

## Goal

A chip that asks the user to accept or approve a produced conclusion —
review findings, a subagent's verdict, an audit result, amended text —
always has that conclusion's substance verbatim in chat above it.

## Scope

**In:** a new "Acceptance chips" rule in tracking-rules.md adjacent to
"Chips carry choices, not evidence" + a cross-reference from that rule
(verbatim bar per D-037: verdict + each actioned finding verbatim; long
artifacts show their conclusions section verbatim + the file path; a
paraphrase never stands in for the accepted text); one-line directives at
the five conclusion-feeding chip steps (/milestone-plan question gate,
/milestone-implement question gate + amendment mini-gates,
/milestone-review approval gate, /milestone-brief RB gate + RR routing,
/milestone audit triage); guard file + mutation registration, including
registering the previously-unguarded "Chips carry choices, not evidence"
block.

**Out:** the other four chip-emitting skills (cairn-init, cairn-release,
hotfix, design-interview) → D-037 rejected wiring them (their chips choose
among user-known options; extend by superseding D-037 if a conclusion chip
appears there). Commit-time preview → shipped in M64. Chip form/invariants
→ unchanged (D-003/D-019/D-022).

## Acceptance criteria

- [x] AC1: tracking-rules.md contains an Acceptance chips rule stating that
      a chip option accepting/approving a produced conclusion requires that
      conclusion's substance verbatim in chat above the chip — verdict +
      each actioned finding verbatim; long artifacts: conclusions section
      verbatim + file path; never a paraphrase in place of the accepted
      text (D-037).
- [x] AC2: the "Chips carry choices, not evidence" rule cross-references
      the Acceptance chips rule so the pair cannot be read as license to
      compress the text being accepted.
- [x] AC3: each of the five covered skills carries a one-line directive at
      its conclusion-chip step(s): plan step 3, implement steps 3 + 6,
      review step 7, brief RB gate + RR-ingestion routing, milestone
      route/triage — evidenced by file:line grep hits scoped to
      `skills/*/SKILL.md`.
- [x] AC4: `skills/tests/test_gate_conclusion_preview.py` exists, asserts
      AC1–AC3 with unique single-line anchors, is mutation-registered, and
      the "Chips carry choices, not evidence" block gains its own
      registered guard (harness + completeness meta-test green).
- [x] AC5: verify clean — all three suites (`skills/tests`, `scripts/tests`,
      `hooks/tests`) discover-run exit 0 from the repo root.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4

## Tasks

- [x] T1: Author the Acceptance chips rule + the cross-reference in "Chips
      carry choices, not evidence" — single-line anchors (M59/M64 lesson:
      multi-word names on ONE physical line), tokens inside bold (M26);
      re-run the suite after any reflow near registered blocks.
- [x] T2: Add the one-line directive at each conclusion-chip step:
      milestone-plan step 3; milestone-implement steps 3 + 6;
      milestone-review step 7; milestone-brief RB gate + ingestion step 5;
      milestone §3 Route (triage chips).
- [x] T3: Write skills/tests/test_gate_conclusion_preview.py (central-rule
      + five per-skill asserts, per-test reads — M61) and register
      Mutation(...) entries, including a new entry anchoring the existing
      "Chips carry choices, not evidence" block.
- [x] T4: Sweep live surfaces for phrasings that could be read as licensing
      compressed acceptance (e.g. summarize-results wording feeding gates) —
      exclusions may name only history files (M48/M58); run all three
      suites from the repo root with exit codes gating the chain (M56).

## Work log

- 2026-07-16: created by /milestone-plan (promotes the gate-time
  conclusion-preview candidate banked 2026-07-16 after the circumplex live
  hit; row graduates at completion per M35).
- 2026-07-16: T1 done — Acceptance chips rule + cross-ref in Chips carry
  choices; all three suites green.
- 2026-07-16: T2 done — directives at plan gate, implement gate + mini
  gate, review approval gate, brief RB gate + RR routing, milestone Route;
  suite green.
- 2026-07-16: T3 done — guard file (8 tests, count by command) + 12
  Mutation entries incl. the previously-unguarded chips-carry-choices
  block; skills suite 208 tests green.
- 2026-07-16: T4 done — sweep found one licensing phrase (delegation rule's
  "summarize results into one work-log line"), clarified log-line-only;
  all three suites + validate green; status → review.

## Decisions

## Review

PR: https://github.com/jmgirard/cairn/pull/63 (draft; base = origin/main).

- AC1 (2026-07-16): rule at tracking-rules.md:382–388 — substance
  requirement, D-037 verbatim bar, paraphrase prohibition all grepped;
  guard TestAcceptanceChipsRule green.
- AC2 (2026-07-16): cross-ref at tracking-rules.md:381 ("a summary never
  substitutes for the accepted text."); guard green.
- AC3 (2026-07-16): directive grep hits — plan:62, implement:46+80,
  review:151, brief:33+72, milestone:89. All names on one physical line
  (M64 lesson applied at authoring).
- AC4 (2026-07-16): guard file exists (8 tests, counted by command); 12
  Mutation entries incl. the chips-carry-choices block; harness +
  completeness green (skills suite 208 tests OK).
- AC5 (2026-07-16): skills/scripts/hooks suites all OK from repo root;
  cairn_validate all checks passed.
- Consistency gate (2026-07-16): validate exit 0; generic profile
  consistency-gate slot names no toolchain checks (clean no-op); no IP/GP
  changed → cairn_impact skipped.
- Fan-out (2026-07-16): diff-bug 1 finding; blame + prior-PR lenses clean
  (prior-PR: zero inline comments incl. fresh PR #62 — expected no-op).
  Scored: F1 65 ("Deltas, not dumps" still says "One exception" though M65
  adds a second verbatim-mandating rule; per-skill directives blunt any
  practical risk) → sub-threshold, logged not actioned; surfaced at the
  approval gate for an optional one-sentence fix. Gate: user directed the
  F1 fix — "One exception" → "Two exceptions" naming both rules; M64's
  registered block preserved intact; suite re-run green.
