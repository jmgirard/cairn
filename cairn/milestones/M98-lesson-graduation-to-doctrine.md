<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M98: Lesson graduation to doctrine — a matured lesson family leaves LESSONS.md whole

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give `LESSONS.md` a third outflow — graduation to doctrine — by distilling
its matured guard-craft family into a conditionally-read
`skills/shared/guard-doctrine.md` module and retiring the covered lessons.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** re-deriving which `LESSONS.md` items form a matured family (the
classification is the milestone's own evidence, never RR03's inherited 63%);
authoring `skills/shared/guard-doctrine.md` as distilled doctrine; a one-line
rulebook pointer beside the existing `validation-doctrine.md` pointer;
retiring the covered lessons whole from `cairn/LESSONS.md`; a D-entry
annotating D-051 with maturation as a third outflow beside enforcement and
ownership, and distinguishing it from D-051's rejected "separate
graduated-lessons file"; guards over the module and the new criterion, with
mutation registration.

**Out:**
- The anchor-choice discipline for the mutation harness (RR03 rec 8 — "anchor
  on rules, not on scaffolding") → candidate row; M98 builds the home, the
  content waits on rec 8's stated trigger (a pass where re-anchoring cost
  proves material).
- Re-deriving D-049's `LESSONS.md` weight threshold from a post-graduation
  mean → deferred to a later hygiene pass. RR03 rec 12 rejects re-derivation
  from the *pre*-graduation mean as ratifying accretion; a fresh measurement
  becomes legitimate only once the family has left, and it is not this
  milestone's job to bank it.
- Any change to `LESSONS.md`'s caps, one-line format, or capture/harvest
  wiring (D-015, standing) → not in scope; this milestone adds an exit, not a
  ceiling.
- The always-read audit frame (RR03 rec 7) → already banked in M95's work log.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: The milestone file records a classification of **every** current
      `LESSONS.md` item as graduating or staying, each with its reason, derived
      in this milestone and not carried over from RR03. Items RR03 flagged as a
      possible second tier (`LESSONS.md:19` M51, `:44` M87) are classified
      explicitly either way.
- [ ] AC2: `skills/shared/guard-doctrine.md` exists, stating the graduated
      craft as doctrine rather than a paste of dated lesson lines, and is
      reachable from `skills/shared/tracking-rules.md` "What gets a test" by a
      pointer naming what it covers and when to read it.
- [ ] AC3: Every graduated lesson has a recorded inversion result — where its
      behavioral content landed in the module, and confirmation that deleting
      or inverting that text would change what a compliant agent does. A lesson
      whose content survives only in part is trimmed to its uncovered
      remainder, per D-051.
- [ ] AC4: Each graduated lesson is gone from `cairn/LESSONS.md` — no line, no
      breadcrumb — and the archive summary names what was graduated (D-051's
      tombstone form).
- [ ] AC5: A D-entry annotates D-051 naming maturation as a third outflow, and
      states why graduation is not the "separate graduated-lessons file"
      D-051 rejected as a divergence vector.
- [ ] AC6: New prose-guards pin the module's pointer and the maturation
      criterion, each on one physical line per the label→rule rule, registered
      in `skills/tests/test_mutation_harness.py`; the harness completeness
      meta-test is green.
- [ ] AC7: `cairn_validate` reports `record density` clean for
      `cairn/LESSONS.md` on both axes, and the `verify` slot (all three
      `python3 -m unittest` suites, run from the repo root with exit codes
      checked individually) is clean.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T2, T3
- AC3 → T2, T4
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [ ] T1: Classify every item in `cairn/LESSONS.md` (32 items, 49 lines,
      21,085 chars as of 2026-07-19) against the maturation bar — consolidated
      repeatedly, teaching a principle rather than an incident, failing both
      D-051 criteria by construction. Record the table in this file. Decide
      whether the records-hygiene items (`:19`, `:44`) form a second family
      with a different home or join the guard-craft module.
- [ ] T2: Author `skills/shared/guard-doctrine.md` from the classified family
      — distilled principles with their failure modes, not concatenated lesson
      lines. Budget the file up front against no cap of its own but against
      the read cost GP1 names (`validation-doctrine.md` is 93 lines / 6,036
      chars as the shape precedent). Record each source lesson's inversion
      result as it is folded in (AC3).
- [ ] T3: Wire the pointer into `skills/shared/tracking-rules.md` "What gets a
      test", beside the existing validation-doctrine reference
      (`tracking-rules.md:664-670` is the pointer's shape). Rulebook-reference
      only — no per-skill read directives (D-031).
- [ ] T4: Retire the graduated lessons from `cairn/LESSONS.md` — delete whole,
      trim partial coverage to its remainder, no breadcrumb. Use targeted Edit
      replacements, never an ad-hoc string script (`LESSONS.md:28`, M61).
      Re-measure both axes from command output.
- [ ] T5: Author the D-entry annotating D-051 (maturation as the third
      outflow; the divergence-vector distinction; D-031 cited as the module
      precedent).
- [ ] T6: Author the guards and register them in the mutation harness.
      Registration is per file and a new `assertIn` in an already-registered
      file needs its own entry (`LESSONS.md:20`, M53). Grep every word an
      existing guard anchors on after adding module prose (`LESSONS.md:26`,
      M85).
- [ ] T7: Run `cairn_validate` and all three suites from the repo root,
      checking each exit code separately — never piped (`LESSONS.md:21`).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-19: created by /milestone-plan. Gate: module home over synthesis note; T1 re-derives the family boundary rather than inheriting RR03's 63%; fidelity proven by recorded inversion per lesson; the D-entry distinguishes rather than supersedes D-051's rejected graduated-lessons file.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->
