# M05: Rulebook conventions & protocol gaps (done 2026-07-11)

- **PR:** https://github.com/jmgirard/cairn/pull/2 (squash 00ea57c)
- **Goal:** close the protocol gaps the pilots exposed and land the
  convention backlog from the M01/M02 reviews.

Outcome:

- cairn-init §2 gained the **adopt-in-place** migration variant (young,
  cairn-shaped precursor; question-gated; ledger + audit bar unchanged).
  Lineage: M03 tidymedia pilot (PR #8).
- **RB tripwires**: tracking-rules names three categories with canonical
  tokens (no-oracle | irreversible-api | ip-touching); milestone-plan tags
  them inline `(RB tripwire: <token>)`; milestone-implement inherits tags
  and offers an escalation chip only on a hit (D-004).
- Conventions: cross-repo ID qualification; ROADMAP done-row retention
  (keep 5 newest; gate choice); DESIGN principle ordering (IP block first,
  numbers never reused) — mirrored in cairn-init skeletons.
- All four M01-review nits closed (rulebook RR-ingestion pointer;
  DECISIONS/reviews session-start reads in cairn-release + hotfix;
  cairn-release routing chip; skeleton status-grouping note).

Key review fixes: repo's own DESIGN.md reordered IP-first (it contradicted
the new convention); CHANGELOG stays per-release compilation (user choice).
