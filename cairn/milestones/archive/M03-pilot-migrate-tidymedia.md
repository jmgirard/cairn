# M03: Pilot — migrate tidymedia — done

**Status:** done · approved 2026-07-11 · high · Depends: M01 · Footprint:
docs-only commits on main (757ca16..7631d5d); migration work in tidymedia
(PRs #8–#9).

## Goal
Prove the §2.4 migration protocol on tidymedia — the precursor format
nearest the canonical one — then ship one milestone post-migration.

## Outcome
All five criteria passed with command-verified evidence: migration landed
as one PR (tidymedia #8, squash c5eb4bb) with a complete ledger (every
legacy file/item dispositioned, nothing dropped); health audit clean
on-branch and re-verified on the merged tree; legacy repo-local
`/milestone` skill retired outside the load path (no collisions); legacy
IDs citable (D001–D009 + M01–M07 verbatim, D010/D011 appended, next new
milestone M11); tidymedia M08 (verification & provenance) shipped normally
under cairn (PR #9, archived, done). Independent Opus review:
approve-with-fixes; its one should-fix (three 26-line migrated archives)
fixed in tidymedia 1eb4195.

## Key decisions / findings
- Gate-approved deviation: adopt-in-place (1-day-old precursor
  near-identical to cairn → translate in place, no legacy tomb) → banked
  as a cairn-init §2 candidate. Not yet exercised under cairn in
  tidymedia: the plan phase and M11 issuance (next milestone covers both).
