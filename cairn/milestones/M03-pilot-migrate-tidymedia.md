# M03: Pilot — migrate tidymedia

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
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

- [x] Migration lands as one PR with a complete ledger (every legacy file
      and live item dispositioned).
- [x] `/milestone` health audit passes clean on the migration branch.
- [x] Legacy `/milestone` skill deactivated; no skill-name collisions with
      the plugin.
- [x] Legacy IDs remain citable; new numbering continues from the legacy max.
- [x] One post-migration milestone ships normally.

## Tasks

- [x] Confirm tidymedia has nothing in flight (or carry over its one
      in-progress item explicitly).
- [x] Run `/cairn-init` migration (Jeff drives, in a tidymedia session);
      review the proposal gate carefully.
- [x] Verify ledger, audit, and merge.
- [x] Ship one milestone post-migration (tidymedia M08); log friction as
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
- 2026-07-11: task 3 done — PR #8 squash-merged (c5eb4bb) on user
  approval; branch deleted; tidymedia is live on cairn. Friction: first
  merge-gate recap was verification-mechanics-first, user couldn't tell
  what was being approved — re-asked in plain words (feeds the existing
  output-discipline candidate). Remaining: ship tidymedia M08 (task 4).
- 2026-07-11: task 4 done — tidymedia M08 shipped normally through the full
  pipeline (plan gate → branch → 5 tasks → fresh-evidence review →
  independent Opus review, 4 findings fixed on branch → PR #9 squash-merged
  → archived, done). Clean run; no new friction beyond the recap-wording
  item already banked. All tasks complete; status → review.

## Decisions

## Review

### Criteria evidence (2026-07-11, fresh by command)

1. **One PR + complete ledger** — PASS: tidymedia PR #8 MERGED (squash
   c5eb4bb, 24 files); body ledger dispositions every legacy path
   (ROADMAP, D001–D009, M08 planned, M09/M10→candidates, M01–M07
   archives, empty briefs/, retired skill); nothing dropped.
2. **Audit clean on migration branch** — PASS: on-branch clean run in the
   work log; branch deleted post-merge, so re-verified on the merged tree
   (= squash of it): mirrors agree, caps 51/23 OK, ignore entries
   present, `.claude/` gone. Letter-vs-spirit gap accepted (F4).
3. **Legacy skill deactivated, no collisions** — PASS: `.claude/` absent;
   skill retired to `cairn/legacy/milestone-skill/` (outside load path).
4. **Legacy IDs citable; numbering continues** — PASS: M01–M07 archives
   verbatim; D001–D009 verbatim, D010/D011 appended; M09/M10 keep IDs as
   candidate rows; next new milestone M11 (reserved; issuance untested, F3).
5. **Post-migration milestone ships normally** — PASS: tidymedia M08
   implement→review→merge (PR #9, 716c7d2)→archive→done under cairn.

Consistency gate (adapted; R gates waived per CLAUDE.md): caps OK
(CLAUDE.md 17/80, ROADMAP 35/60, this file /150); mirror = ROADMAP; main
in sync with origin; docs-only on main (M02 precedent, logged 2026-07-11).

### Independent review (2026-07-11, fresh-context Opus)

Approve-with-fixes; all five criteria independently re-verified by
command. Triage — fixed: F1 three migrated tidymedia archives at 26 lines
vs ≤25 cap (trimmed, tidymedia 1eb4195). Accepted, no action: F2 M08 was
planned by the legacy skill pre-migration — cairn drove
implement→review→merge→archive but not plan (next tidymedia milestone
exercises it); F3 M11 issuance reserved, not yet exercised (same); F4
criterion-2 letter (branch deleted; merged-tree re-audit adequate); F5
criteria boxes unchecked pre-review (expected; checked this pass).
