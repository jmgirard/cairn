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

- [x] Confirm tidymedia has nothing in flight (or carry over its one
      in-progress item explicitly).
- [x] Run `/cairn-init` migration (Jeff drives, in a tidymedia session);
      review the proposal gate carefully.
- [ ] Verify ledger, audit, and merge. (verify+audit done; merge awaits
      approval)
- [ ] Ship one milestone post-migration (tidymedia M08); log friction as
      cairn candidate rows.

## Work log

- 2026-07-11: planned as part of the v0.1 pilot plan (DRAFT_2 §11).
- 2026-07-11: implementation started; no cairn branch (M02 precedent —
  work happens in tidymedia, cairn tracks via docs-only commits on main).
- 2026-07-11: pre-flight check — tidymedia clean, nothing in flight (M08
  planned, M09/M10 ideas, M01–M07 done); one unpushed docs commit
  (3494379, plan M08) to push before migration branches.
- 2026-07-11: question gate — Jeff drives migration in tidymedia sessions
  (M02 precedent, truest plugin UX test); tidymedia M08 is the
  post-migration ship; task 4 amended issues→candidate rows (per M02).
- 2026-07-11: task 1 done; pushed tidymedia 3494379 so migration cuts
  from pushed master; legacy max ID M10 → new numbering starts M11.
- 2026-07-11: task 2 done — Jeff ran /cairn-init in tidymedia (PR #8,
  0f370a4); gate-approved deviation: adopt-in-place (1-day-old precursor
  near-identical to cairn → translate in place, no legacy tomb except the
  retired repo-local skill). Pilot finding → candidate row.
- 2026-07-11: task 3 verify+audit done — ledger complete (every diff path
  dispositioned; verbatim claims verified: 0-change renames, D001–D009
  untouched, D010 appended); manual /milestone audit clean on branch
  (mirrors agree, deps resolve, caps 23/51/105, no orphans/collisions,
  .claude/skills gone, ignore entries present); CI 7/7 green. Merge
  awaits user approval.

## Decisions

## Review
