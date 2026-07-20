<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M95: Rulebook editorial slimming — the rulebook states rules, not their legislative history

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Enforce `tracking-rules.md:11-13`'s own ownership boundary against the rulebook
itself: state the rule, cite the D-entry that decided it, and delete the
restated rationale — so the always-read core stops carrying history
`DECISIONS.md` already owns.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A section-by-section editorial pass over `skills/shared/tracking-rules.md`
removing restated decision context — dates, measured values, incident
anecdotes, rejected alternatives — that its cited D-entry already records,
leaving the rule plus a parenthetical citation; completing RR01 rec 7's
unfinished prune (the default-branch recipe, `tracking-rules.md:322-337`, and
the phase-header per-skill enumeration); re-anchoring every guard the rewording
touches.

**Out:**
- **Writing anything into `cairn/DECISIONS.md`.** The rationale is *already*
  there — RR02 Q1(c) verified it block by block. This milestone deletes
  restatements; it never edits history (IP4). A block with no existing D-entry
  home is left in place, or gains a new D-entry through the normal gate.
- Removing, weakening, or merging any rule. Zero rules leave the rulebook;
  a slimming that loses a rule is a failed milestone, not a cheaper one.
- Splitting or sectioning the rulebook → rejected, RR01 rec 15 upheld by RR02
  Q5; not revisitable here.
- A size threshold or cap on the result → M96.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: Every block removed is evidenced as **already recorded** in a named
      D-entry, quoted from that entry, before removal — a per-block ledger in
      the work log. A block whose content has no D-entry home is not removed.
      Nothing is written to `DECISIONS.md` (IP4).
- [ ] AC2: **No rule is lost.** Every rule surviving as a shortened statement
      keeps a guard that reddens when the rule is deleted or inverted, proven
      by inversion — relabel, negate, or transpose the rule in place, run the
      suite, require red, restore and diff (M74). A rule whose guard cannot be
      made to redden is restored to full statement rather than left unpinned.
- [ ] AC3: The mutation harness is green with every reworded anchor
      re-registered: a `block` that reflowed, duplicated, or lost trailing
      punctuation self-reports as "found 0" — the fix is the WRAP, never the
      assert (M65/M78). Registration is per file, so a guard file whose
      anchors all changed still needs its entries checked, not assumed (M53).
- [ ] AC4: RR01 rec 7's prune is completed: the canonical default-branch
      recipe is stated once and the per-skill phase-header enumeration is
      replaced by the two-level convention plus the skills' own directives.
- [ ] AC5: The resulting line and character count is **recorded as evidence,
      never as a gate** — no line target is a pass condition (user call at the
      M95 plan gate; RR02's ~550-600 was explicitly an estimate). The section
      breakdown before/after is recorded for M96's first stamp.
- [ ] AC6: The active profile's `verify` slot is clean — all three suites
      green, run from the repo root with exit codes checked individually and
      never behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2, T3
- AC2 → T3, T4
- AC3 → T4
- AC4 → T5
- AC5 → T6
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: Inventory. For each rulebook section, list candidate blocks and the
      D-entry that already records each. Produces the removal ledger AC1 checks
      against. No edits in this task.
- [ ] T2: Verify the ledger — read each cited D-entry and confirm it carries
      the content, quoting it. Drop from the ledger anything not actually
      recorded elsewhere (M75: a restatement is unverified until read out of
      the source; M92 extends this to relocation).
- [ ] T3: Edit section by section, heaviest first (Weight caps 80 → References
      pages 66 → Output discipline 97 → Universal rules 71 → Git model 76).
      **Targeted `Edit` calls only — never an ad-hoc string script over a
      tracking file (M61), and never `replace_all` on a line whose correct
      indentation or context differs between occurrences (M90).** Run the
      skills suite after each section, not at the end.
- [ ] T4: Re-anchor and re-register guards; run the mutation harness; prove
      AC2's inversion for each shortened rule.
- [ ] T5: Complete RR01 rec 7's prune.
- [ ] T6: Record before/after counts and the section breakdown; run all three
      suites from the repo root with exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan, re-cutting M94 per RR02 rec 1. Absorbs the "Rulebook read-cost reduction" candidate row (graduates at completion, M35). RR02 Q1 verified the growth mode: no new domain doctrine entered after M58, yet the file grew 44% — the inflow is rationale, not rules.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
