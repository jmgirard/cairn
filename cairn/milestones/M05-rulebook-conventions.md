# M05: Rulebook conventions & protocol gaps

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** M04   <!-- edits the same rulebook/skill text M04 reshapes -->
- **Branch/PR:** m05-rulebook-conventions

## Goal

Close the protocol gaps the pilots exposed: codify the adopt-in-place
migration variant, add RB escalation tripwires, and land the convention
backlog from the M01/M02 reviews.

## Scope

**In:** cairn-init §2 adopt-in-place variant; RB self-solicitation
tripwires (rulebook categories + plan-time tagging + gated chip option);
cross-repo milestone-ID qualification; ROADMAP done-row retention remedy;
DESIGN principle ordering; the four M01-review nits.

**Out:** conduct/output rules → M04; README install docs (dev symlink vs
marketplace) → release-prep candidate; Lineage B migration stress test →
candidate (runs after this wave; exercises the entombment path
adopt-in-place bypasses); toolchain profiles, greenfield init flow,
design-interview skill, skill-less routing, hooks → candidates (v0.3).

## Acceptance criteria

- [ ] cairn-init §2 documents adopt-in-place as a named variant: when it
      applies (young precursor, structure near-identical to cairn), that
      choosing it is a question-gate decision, and that the ledger + audit
      acceptance (§2.7) applies unchanged. Lineage: M03 pilot, tidymedia
      PR #8. Evidence: file read.
- [ ] tracking-rules names the RB tripwire categories (stats/scoring
      without an oracle; irreversible exported API; IP-touching);
      milestone-plan instructs tagging RB-worthy questions in the plan;
      milestone-implement inherits the tag; an escalation chip option is
      offered only on a tripwire hit, never standing (cites D-004).
      Evidence: grep + read.
- [ ] tracking-rules states the cross-repo ID convention: qualify bare
      M<NN> with the repo name whenever more than one cairn-tracked repo
      is in scope. Evidence: file read.
- [ ] The weight-caps remedies name a sanctioned done-row retention rule
      (prune oldest done rows past a threshold; archive files + git stay
      authoritative), mirrored in the cairn-init ROADMAP skeleton comment.
      Evidence: file read.
- [ ] DESIGN principle ordering (IP block first, then GP; numbers within
      type; never reused/renumbered — retire via D-entry) specified in
      the rulebook and the cairn-init DESIGN skeleton. Evidence: file read.
- [ ] All four M01-review nits closed: RR-ingestion protocol reachable
      from the rulebook (section or path pointer); cairn-release and
      hotfix session starts read DECISIONS.md + `cairn/reviews/`;
      cairn-release ends with a routing chip; cairn-init ROADMAP skeleton
      notes status-grouping. Evidence: file reads.

## Tasks

- [x] Write the adopt-in-place variant into cairn-init §2 (detection,
      gate, unchanged ledger/audit bar).
- [ ] Add RB tripwires to tracking-rules; plan-time tagging to
      milestone-plan; tag inheritance + tripwire-gated chip option to
      milestone-implement.
- [ ] Add conventions to tracking-rules (+ cairn-init skeletons where
      noted): cross-repo IDs, done-row retention, DESIGN principle
      ordering.
- [ ] Close the four M01-review nits (rulebook RR pointer; session-start
      reads in cairn-release + hotfix; cairn-release closing chip;
      skeleton status-grouping note).
- [ ] Coherence pass across rulebook + touched skills; verify caps.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. Lineage: candidate rows absorbed
  (adopt-in-place; RB self-solicitation; cross-repo IDs; done-row
  retention; DESIGN ordering; v0.2 polish nits from M01 review).
- 2026-07-11: gate resolved: done-row retention = keep 5 newest; RB tags
  inline on the affected task/criterion. Task 1: adopt-in-place variant
  written into cairn-init §2.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review -->
