<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M66: cairn-init migration gates show the proposal — D-037 wiring extension

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m66-init-gate-preview · https://github.com/jmgirard/cairn/pull/64   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A `/cairn-init` migration chip never asks the user to confirm a proposal
that hasn't appeared in chat — extend the D-037 acceptance-chips
discipline to the migration gates (D-038).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Extend the tracking-rules "Acceptance chips" rule enumeration to
name a proposed disposition or action plan awaiting confirmation; wire
per-step directives at migration-protocol step 3 (inventory +
proposed-disposition ledger verbatim in chat above the gate chip,
adopt-in-place variant included) and step 7 (migration ledger in chat
above the merge-approval chip, not only in the PR description); guard
tests, mutation-registered. D-038 (supersedes D-037's wiring scope)
lands with this plan.

**Out:** cairn-init's profile-confirmation, greenfield-opener, and
routing chips; `/cairn-release` version confirm; `/hotfix` merge chip;
`/design-interview` — all stay unwired (D-037's user-known-options /
reviewable-at-PR reasoning holds there; recorded in D-038 — re-raise by
superseding it on evidence). No runtime enforcement hook — prose +
guards, like M64/M65.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: the tracking-rules "Acceptance chips" rule names a proposed
      disposition or action plan awaiting confirmation as covered
      content — evidence: grep `skills/shared/tracking-rules.md`.
- [x] AC2: migration-protocol step 3 carries an
      `Acceptance chips (tracking-rules)` directive requiring the
      inventory + proposed-disposition ledger verbatim in chat above the
      chip — evidence: grep `skills/shared/migration-protocol.md`.
- [x] AC3: migration-protocol step 7 requires the migration ledger in
      chat above the merge-approval chip, not only in the PR
      description — evidence: grep `skills/shared/migration-protocol.md`.
- [x] AC4: guard tests lock AC1–AC3 and every new assert is
      mutation-registered — evidence: skills suite green; harness
      completeness meta-test green with the new `Mutation(...)` entries
      present.
- [x] AC5: both unittest suites pass from the repo root with explicit
      exit codes (no tail-piping) — evidence: command output.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: extend the Acceptance-chips rule enumeration in
      `skills/shared/tracking-rules.md` (keep D-037's guard-anchored
      phrases intact; new phrase on one physical line — M59/M64/M65
      reflow lessons).
- [x] T2: add the step-3 directive to
      `skills/shared/migration-protocol.md` (directive name unwrapped on
      one line).
- [x] T3: add the step-7 directive to
      `skills/shared/migration-protocol.md`.
- [x] T4: extend `skills/tests/test_gate_conclusion_preview.py` with a
      migration-gates class + the rule-enumeration assert; add
      `Mutation(...)` entries for each new assert (M53: per-assert, not
      per-file).
- [x] T5: run both suites from the repo root, exit-code-gated, before
      the final checkpoint commit (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan (evidence: hitop cairn-init
  migration fired the step-3 disposition chip with no proposal in chat).
- 2026-07-16: T1 — rule enumeration extended (proposed disposition/action
  plan, D-038 cite); skills suite 208 OK.
- 2026-07-16: T2+T3 — step-3 and step-7 acceptance-chips directives added
  to migration-protocol.md; skills suite 208 OK.
- 2026-07-16: T4 — 3 guard tests + 6 Mutation entries added; skills suite
  211 OK (harness blanks each new block and its guard fails).
- 2026-07-16: T5 — both suites green from repo root (scripts_exit=0,
  skills_exit=0); status → review.
- 2026-07-16: correction (review F1/92): T4 added 5 Mutation entries, not
  6 — the M28/M64 stale-count trap, recurred; count verified by command.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->

2026-07-16 — evidence, all fresh by command:

- AC1: grep hit at tracking-rules.md:386 — "a proposed disposition or
  action plan awaiting confirmation (D-038)".
- AC2: grep hit at migration-protocol.md:46 — "Acceptance chips
  (tracking-rules): the inventory and each item's" (step-3 gate).
- AC3: grep hits at migration-protocol.md:171–172 — ledger verbatim above
  the merge chip; "the PR description alone never carries it".
- AC4: skills suite Ran 211 (was 208 pre-M66), OK — includes the 3 new
  guards, the harness blank-and-assert on the 5 new Mutation entries
  (count by command: `git diff main..HEAD | grep -c "^+    Mutation("` →
  5), and the completeness meta-test.
- AC5: scripts suite Ran 84 OK (exit 0), skills suite Ran 211 OK (exit 0),
  run from the repo root, exit codes echoed separately.
- Consistency gate: cairn_validate exit 0, all checks passed (coverage
  complete included); no principle change → cairn_impact skipped; generic
  profile consistency-gate slot names none → toolchain half no-op.

Fan-out (3 lenses + scorer): diff-bug [O] 1 finding; blame-history [S]
clean; prior-PR [S] "no prior-PR evidence" (expected no-op). Sub-threshold
findings: none (nothing scored <80).

- F1 (scored 92, actioned → fixed now): the T4 work-log line and AC4
  evidence claimed "6 Mutation entries"; the diff adds 5 (verified by
  command). AC4 itself satisfied — record-accuracy defect only. Fixed:
  AC4 evidence corrected pre-commit; committed work-log line corrected by
  appended line (IP4 — never rewritten).
