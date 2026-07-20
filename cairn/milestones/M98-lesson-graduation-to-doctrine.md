<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M98: Lesson graduation to doctrine — a matured lesson family leaves LESSONS.md whole

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m98-lesson-graduation`   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] T1: Classify every item in `cairn/LESSONS.md` (32 items, 49 lines,
      21,085 chars at 2026-07-19) against the maturation bar; record the
      result here, deciding whether the records-hygiene items form a second
      family or join the guard-craft module.
- [ ] T2: Author `skills/shared/guard-doctrine.md` from the classified family
      — distilled principles with their failure modes, never concatenated
      lesson lines. Shape precedent: `validation-doctrine.md`, 93 lines /
      6,036 chars. Record each lesson's inversion result as it is folded in.
- [ ] T3: Wire the pointer into `tracking-rules.md` "What gets a test" beside
      the validation-doctrine reference (`:664-670` is the shape).
      Rulebook-reference only — no per-skill read directives (D-031).
- [ ] T4: Retire the graduated lessons from `cairn/LESSONS.md` — delete
      whole, trim partial coverage to its remainder, no breadcrumb. Targeted
      Edit replacements, never an ad-hoc string script (M61). Re-measure both
      axes from command output.
- [ ] T5: Author the D-entry annotating D-051 (maturation as the third
      outflow; the divergence-vector distinction; D-031 as module precedent).
- [ ] T6: Author the guards and register them in the mutation harness —
      registration is per file, and a new `assertIn` in an already-registered
      file still needs its own entry (M53). After adding module prose, grep
      every word an existing guard anchors on (M85).
- [ ] T7: Run `cairn_validate` and all three suites from the repo root,
      checking each exit code separately — never piped (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-19: created by /milestone-plan. Gate: module home over synthesis note; T1 re-derives the family boundary rather than inheriting RR03's 63%; fidelity proven by recorded inversion per lesson; the D-entry distinguishes rather than supersedes D-051's rejected graduated-lessons file.
- 2026-07-19: in-progress, branch `m98-lesson-graduation` cut from main at e684c39.
- 2026-07-20: T1's record blew the 150-line body cap (165, shed ≥16) and T1 was checked off against a red gate — corrected here. Two single-pass compressions: Decisions 42→33, Tasks 34→26. The Tasks pass also removed `LESSONS.md:NN` citations that T4 is about to invalidate by deleting those very lines. Further live evidence for the budget-first-drafting candidate row.
- 2026-07-20: T1 done — boundary re-derived independently (M98-D1); guard family is 18 items / 13,316 chars / 66% of item mass, differing from RR03 on six members. Records-hygiene items are a real second family, deferred to a candidate row rather than folded in: the guard family alone leaves 19 lines and 12,749 chars of headroom.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

### M98-D1 (2026-07-20): the maturation bar, and the family boundary re-derived

**Bar** (conjunctive): (a) **principle, not incident** — transferable craft
about authoring or verifying, not a fact about this repo's tools or runtime;
(b) **stabilized** — extended or consolidated ≥2×, later milestones adding
instances rather than changing the principle; (c) **no existing exit** —
fails D-051 enforcement (no test fails on the mistake) and ownership (no
tracking-file slot holds it).

**GRADUATE — guard-authoring craft** (18 items, 13,316 chars, 66% of item
mass): `LESSONS.md` lines 20, 22, 23, 24, 26, 27, 31, 33, 35, 36, 40, 41,
42, 43, 45, 47, 48, 49.

**STAY — tool/runtime quirk**, D-015's charter, fails (a) (6 items, 3,351
chars): 21, 25, 28, 30, 34, 46 — Bash cwd persistence, hook registration
snapshotting, `Edit --replace_all`, the `gh` quota, hook shipping surfaces.

**STAY — records/process-hygiene craft**, a real second family, deferred
(8 items, 3,493 chars): 18, 19, 29, 32, 37, 38, 39, 44. They pass (a) but
fire at a hygiene or plan gate, not at guard-authoring, so they need their
own read-trigger, not a seat here; 29 and 37 may instead be D-051 ownership
retirements scoped to the milestone shipping those surfaces. Candidate row.

**Not inherited:** RR03 named 20, 22, 24, 26-28, 33, 35, 36, 38, 40-43,
45-48; this differs on six (admits 23, 31, 49; excludes 28, 38, 46).

**Sufficiency:** the guard family alone leaves 31/50 lines and 7,751/20,500
chars — 19 lines and 12,749 of headroom, so deferring the second costs
nothing.

## Review
<!-- owner: review · exclusive -->
