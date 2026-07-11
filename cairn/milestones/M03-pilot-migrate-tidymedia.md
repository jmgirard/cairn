# M03: Pilot — migrate tidymedia

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** M01
- **Branch/PR:** none in cairn — docs-only tracking commits on main (M02
  precedent); the migration branch/PR lives in tidymedia

## Goal

Prove the §2.4 migration protocol on tidymedia — the precursor format
nearest the canonical one.

## Scope

**In:** full migration via `/cairn-init` (entomb legacy files, translate live
state, deactivate the repo-local `/milestone` skill, ledger + audit-gated
PR); then ≥1 milestone shipped post-migration to confirm normal operation.

**Out:** Lineage B stress test (ackwards/circumplex) → candidate, before
broad rollout.

## Acceptance criteria

- [ ] Migration lands as one PR with a complete ledger (every legacy file
      and live item dispositioned).
- [ ] `/milestone` health audit passes clean on the migration branch.
- [ ] Legacy `/milestone` skill deactivated; no skill-name collisions with
      the plugin.
- [ ] Legacy IDs remain citable; new numbering continues from the legacy max.
- [ ] One post-migration milestone ships normally.

## Tasks

- [ ] Confirm tidymedia has nothing in flight (or carry over its one
      in-progress item explicitly).
- [ ] Run `/cairn-init` migration; review the proposal gate carefully.
- [ ] Verify ledger, audit, and merge.
- [ ] Ship one milestone post-migration; log friction as issues.

## Work log

- 2026-07-11: planned as part of the v0.1 pilot plan (DRAFT_2 §11).
- 2026-07-11: implementation started; no cairn branch (M02 precedent —
  work happens in tidymedia, cairn tracks via docs-only commits on main).
- 2026-07-11: pre-flight check — tidymedia clean, nothing in flight (M08
  planned, M09/M10 ideas, M01–M07 done); one unpushed docs commit
  (3494379, plan M08) to push before migration branches.

## Decisions

## Review
