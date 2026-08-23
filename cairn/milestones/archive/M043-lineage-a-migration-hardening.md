# M43: Lineage A migration hardening (cairn-init §2)

- **Status:** done · **Priority:** normal · **Depends on:** — · **PR:** #41 · **Principles:** GP4/IP2/IP3 (worked-under; none changed)

## Outcome

Hardened `/cairn-init` §2 with the four Lineage A migration gaps the M41
intraclass pilot surfaced (`references/migration-pilot-notes.md` Pilot 3), so a
multi-file `project/` precursor migrates as cleanly as the M22/M23-hardened
Lineage B path. Four prose additions to `skills/cairn-init/SKILL.md`, each locked
by a `TestLineageAGuidance` case in `skills/tests/test_migration_guidance.py`:

- **G-I1** (step 5): concern-split precursor (no single `DESIGN.md`) → map
  concern-files to cairn homes, keep repo-specific else, thin DESIGN seed.
- **G-I2** (step 6, headline): numbered-principle **forced note-and-leave** —
  keep the principles file (numbering intact); defer IP/GP + in-code repoint to
  `/design-interview` + a code milestone.
- **G-I4** (§6 + step 3): coupled skills entomb; clean domain skills gated for
  keep/entomb ("coupling wins" tiebreaker).
- **G-I5** (step 5): **pointer-only** DECISIONS named for large ADR logs.

Pure skill prose. G-I3 (oracle registry) stays the `ORACLES.md` candidate;
`/design-interview` note-and-leave ingestion banked as a new candidate.
Verification: 5/5 ACs; guard locks (anchors 0 on `main`); `cairn_validate` 12/12;
3-lens fan-out 0 findings; no CI on this repo.
