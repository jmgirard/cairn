# M02: Pilot — fresh adoption in one package repo — done

**Status:** done · approved 2026-07-11 · high · Depends: M01 · Footprint:
docs-only commits on main (2fa9f26..f317a52); no branch/PR (work in openac).

## Goal
Prove the system end-to-end in a package repo with no existing tracking
system (openac).

## Outcome
All five criteria passed with command-verified evidence: /cairn-init
scaffold (criterion 1 accepted at gate — the project/→cairn/ rename was
upstream D-008, not a scaffold repair; shipping init grep-verified, M03
tests it live); five openac milestones (M01–M05) through all three phase
skills, PRs #1–#5 merged, chips at every transition (attested); RB01/RR01
Fable cycle ingested with consequences landed in code (called exemplary by
the independent review); /cairn-release walk to 0.1.0 (tag v0.1.0,
no-CRAN); friction → 8 tagged + 2 derived candidate rows, 0 issues.

## Key decisions / findings
- Gate-approved mid-pilot: openac rename to cairn/ (D-008); friction
  criterion amended issues→candidates; Jeff drove pilot in openac sessions.
- Top findings banked as candidates: RB self-solicitation gap, Fable>Opus
  elicitation, output discipline/plain-language chips, contextual chips
  validated, toolchain-profile extraction (~80% language-agnostic core).
