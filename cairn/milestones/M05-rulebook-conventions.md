# M05: Rulebook conventions & protocol gaps

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** M04   <!-- edits the same rulebook/skill text M04 reshapes -->
- **Branch/PR:** m05-rulebook-conventions · https://github.com/jmgirard/cairn/pull/2

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
- [x] Add RB tripwires to tracking-rules; plan-time tagging to
      milestone-plan; tag inheritance + tripwire-gated chip option to
      milestone-implement.
- [x] Add conventions to tracking-rules (+ cairn-init skeletons where
      noted): cross-repo IDs, done-row retention, DESIGN principle
      ordering.
- [x] Close the four M01-review nits (rulebook RR pointer; session-start
      reads in cairn-release + hotfix; cairn-release closing chip;
      skeleton status-grouping note).
- [x] Coherence pass across rulebook + touched skills; verify caps.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. Lineage: candidate rows absorbed
  (adopt-in-place; RB self-solicitation; cross-repo IDs; done-row
  retention; DESIGN ordering; v0.2 polish nits from M01 review).
- 2026-07-11: gate resolved: done-row retention = keep 5 newest; RB tags
  inline on the affected task/criterion. Task 1: adopt-in-place variant
  written into cairn-init §2.
- 2026-07-11: Task 2: RB tripwire categories + gated-chip rule in
  tracking-rules (also RR-ingestion pointer, part of nit 1); tagging in
  milestone-plan; inheritance + escalation option in milestone-implement.
- 2026-07-11: Task 3: cross-repo ID qualification, done-row retention
  (keep 5 newest), DESIGN IP-then-GP ordering — in tracking-rules and the
  cairn-init skeleton comments (ROADMAP comment also closes nit 4).
- 2026-07-11: Task 4: nits 2+3 closed — DECISIONS/reviews session-start
  reads in cairn-release + hotfix; cairn-release step-9 routing chip
  (nits 1 and 4 closed in tasks 2 and 3).
- 2026-07-11: Task 5: coherence pass — tag format identical across 3
  files; bare D-004 in milestone-implement glossed for consumer repos;
  caps verified (ROADMAP 28/60, this file <150, CLAUDE.md 17/80). All
  tasks done; status → review (R check gate waived: plugin repo).

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review -->

- 2026-07-11 criteria evidence (fresh reads/greps, PR #2):
  - C1 adopt-in-place: cairn-init:90–99 — named variant, applicability,
    step-3 gate, ledger/audit unchanged, M03/PR#8 lineage. PASS.
  - C2 tripwires: tracking-rules:252–259 (3 categories, gated chip,
    D-004); plan:67–70 (tagging); implement:42–46 (inheritance + option).
    PASS.
  - C3 cross-repo IDs: tracking-rules:85–87. PASS.
  - C4 retention: tracking-rules:51–53 + cairn-init:61–62 mirror. PASS.
  - C5 DESIGN ordering: tracking-rules:37–39 + cairn-init:37–41. PASS.
  - C6 nits: RR pointer tracking-rules:251; session reads hotfix:11–13,
    cairn-release:16–18; release chip :69–72; grouping note :61. PASS.
- Consistency gate: R items waived (plugin repo); caps OK (ROADMAP 28/60,
  this file <150, CLAUDE.md 17/80). CHANGELOG: per-release compilation by
  precedent (M04 had no entry) — raised at approval gate, user to decide.
- 2026-07-11 independent [O] review (PR #2 diff): all 6 criteria pass; no
  blockers. Triage: (1) repo's own DESIGN.md ordered GP-before-IP,
  contradicting the new convention — FIXED (reordered IP-first); (2) no
  canonical tripwire tokens — FIXED (no-oracle | irreversible-api |
  ip-touching, defined in tracking-rules, referenced in both skills);
  (3) dangling mid-work cross-ref in implement — FIXED (rulebook now
  covers mid-implementation hits). Adjacent pre-existing skeleton/DESIGN
  section-list mismatch REJECTED: skeleton targets scaffolded package
  repos; this repo's DESIGN legitimately deviates (plugin, not R pkg).
