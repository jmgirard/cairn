# M09: Phase headers (H2/H3) replace inline stage banner — done

**Status:** done · approved 2026-07-11 · normal · Depends: — · PR #6 (squash
6d9d7ee). From Jeff's scannability feedback; extends M04 output discipline.

## Goal
Replace the inline `[cairn · … ]` stage banner with a two-level Markdown
heading (`## Milestone <NN>: <title>` → `### Plan`/`### Implement`/`### Review`)
so phase transitions are scannable in the terminal.

## Outcome
All 4 criteria passed with fresh grep evidence. Rewrote the "Stage banner"
rule in `tracking-rules.md` as a "Phase header" rule (renamed) and updated the
banner line in all 8 skills to the `## unit → ### phase` form, each mapped to
that skill's real phases/steps. Verified 0 stale banners / 0 "Stage banner" in
`skills/`, 8 `Phase header:` lines. Independent Opus review clean; F1 fixed —
the `##` is keyed to the **unit of work** (re-emit on a routing chip into the
next skill or a post-`/clear` session), not the session, since one session
spans multiple units via chips.

## Key decisions
- D-010: phase-header format (two-level `##` unit / `###` phase) supersedes
  the M04-era inline stage banner; `##` per unit of work.
