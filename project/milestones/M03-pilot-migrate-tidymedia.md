# M03: Pilot — migrate tidymedia

- **Status:** planned   <!-- mirror; project/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** M01
- **Branch/PR:** — (work happens in tidymedia; this file tracks it)

## Goal

Prove the §2.4 migration protocol on tidymedia — the precursor format
nearest the canonical one.

## Scope

**In:** full migration via `/rpkg-init` (entomb legacy files, translate live
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
- [ ] Run `/rpkg-init` migration; review the proposal gate carefully.
- [ ] Verify ledger, audit, and merge.
- [ ] Ship one milestone post-migration; log friction as issues.

## Work log

- 2026-07-11: planned as part of the v0.1 pilot plan (DRAFT_2 §11).

## Decisions

## Review
