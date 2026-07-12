# Migration stress-test — pilot notes

Findings from running `/cairn-init` §2 (migration) for real against mature
Lineage B repos, to harden the protocol. Captured per milestone; each gap is
tagged `fix-here | candidate | out` and (where promoted) linked to a ROADMAP
candidate. This is a repo-specific reference file (declares its own scope).

---

## Pilot 1 — ackwards (M20)

- **Repo:** `jmgirard/ackwards`, R package, 256 commits, default branch **`master`**.
- **Method:** invoked `/cairn-init` live; real branch `cairn-init-migration` → PR.
- **Migration PR:** https://github.com/jmgirard/ackwards/pull/53 (docs/tracking only; no package code touched).
- **Health audit:** `cairn_validate` 8/9 — one FAIL (CLAUDE.md over the `<80` cap, see G8), accepted as a documented exception.

### Ledger summary

Entombed → `cairn/legacy/`: `MILESTONES.md` (1880 lines, M1–M53), old
`ROADMAP.md`, 3 repo-local skills. Kept as canonical `cairn/DESIGN.md`:
`DESIGN.md` verbatim (§14 decision log embedded). Authored: `cairn/ROADMAP.md`
(no live milestones; IDs continue from M54), `cairn/DECISIONS.md` (15
still-governing decisions, D-001..D-015, each citing DESIGN §14), `references/INDEX.md`.
Redistributed `CLAUDE.md` (deleted milestone index + status slot; git model →
cairn; defaults/deps/scope → DESIGN pointers; cairn section appended). Live
state (release tail + 2 extension ideas) → candidate rows.

### Gaps / friction (keyed to cairn-init §)

| # | Gap | § | Tag |
|---|---|---|---|
| G1 | §2 step 2 says "cut from up-to-date **main**"; ackwards' default is `master`. | §2.2 | candidate (part of G9) |
| G2 | Lineage B detection assumes "status inside CLAUDE.md"; ackwards also had a forward-only ROADMAP + explicit `Current focus` slot — mapped cleaner than described. | §0/§2.3 | candidate |
| G3 | Rich living `DESIGN.md` (885 lines, embedded §14 decision log + known issues) doesn't fit the entomb/translate binary; §5 only anticipates a thin DESIGN. Resolved at gate (Compromise A: keep verbatim, re-record still-governing decisions, defer full §14 extraction). | §5 | candidate |
| G4 | No live milestones (all done/dropped) — clean; live state was only release tail + 2 ideas. | §3 | (clean) |
| G5 | Invariants placement — hard constraints stayed as CLAUDE rules; IP/GP formalization routed to `/design-interview`. | §6 | candidate |
| G6 | **15 R-source comments + 2 tests reference `DESIGN.md s.N` by name**; relocating strands them. §4/§6 silent on in-code refs. Left untouched (content/sections preserved at new path). | §4/§6 | candidate |
| G7 | Stale per-file `.Rbuildignore` entries (`^DESIGN\.md$` etc.) after the move; §1 only says "add `^cairn$`", not "prune stale". Cleaned by hand. | §1/§6 | candidate |
| G8 | **HEADLINE: cairn's `<80` CLAUDE.md cap doesn't survive a mature repo.** After deleting index+slot and collapsing DESIGN-duplicative sections, CLAUDE.md is still 187 lines — its legit dev doctrine (Dev workflow, DoD, Invariants, guardrails) plus the ~26-line appended cairn section floor well above 80. Audit FAILS. | weight-caps | candidate |
| G9 | **cairn's git model + CLAUDE template are `main`-hardcoded** — no adaptation for a `master` repo; appending verbatim contradicts the repo. Adapted by hand. Old CLAUDE Git section's merge-mechanics also conflicted with cairn's approval-gate (rewrote to defer + keep repo-specifics). | §6 + tracking-rules | candidate |
| G10 | Redistributed `CLAUDE.md` still referenced the just-entombed repo-local skills ("/plan-milestone step 8a…"); §6 should sweep prose for refs to skills it entombs. | §6 | candidate |

### Disposition

No small, safe, isolable `fix-here` skill edit emerged: the gaps are
predominantly **design-level and interconnected** (default-branch
parameterization, cap recalibration, guidance for a rich pre-existing DESIGN,
in-code reference handling). Promoted to ROADMAP candidates for a deliberate
hardening milestone rather than reflexive mid-pilot edits. That the migration
protocol's gaps are design-level (not one-liners) is itself a pilot result.

<!-- Pilot 2 — circumplex (M21) appended here -->
