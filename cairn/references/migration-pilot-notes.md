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
still-governing decisions, D-001..D-015, each citing its DESIGN source anchor —
mostly §14, several §2–§12), `references/INDEX.md`.
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
| G6 | **~17 R-source comments across 9 files + 3 tests reference `DESIGN.md s.N` by name**; relocating strands them. §4/§6 silent on in-code refs. Left untouched (content/sections preserved at new path). | §4/§6 | candidate |
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

## Pilot 2 — circumplex (M21)

- **Repo:** `jmgirard/circumplex`, R package, default branch **`master`**, on CRAN.
- **Method:** invoked `/cairn-init` §2 live; branch `cairn-init-migration` → PR.
  Ran against the **M22+M23-hardened** protocol, so this pilot compounds the
  M20 fixes rather than re-finding them.
- **Migration PR:** https://github.com/jmgirard/circumplex/pull/31 (docs/tracking
  only; no package code). CI: full R-CMD-check matrix (7 jobs) exercised.
- **Health audit:** `cairn_validate` **9/9 clean** on the branch (after the G-C2
  workaround below).

### Ledger summary

Entombed → `cairn/legacy/` (100% renames): `MILESTONES.md`, `MILESTONES-ARCHIVE.md`
(2564 ln), old `ROADMAP.md`, 3 repo-local skills (next-task, release-checklist,
statistical-validation). Kept verbatim as `cairn/DESIGN.md`: `DESIGN.md` (315 ln,
Compromise A). Authored: `cairn/ROADMAP.md` (M7 v2.0.0 release-prep = **blocked**
on CRAN cadence; M6 + backlog → clustered candidates; IDs continue from legacy
max M6), `cairn/DECISIONS.md` (4 still-governing decisions, D-001..D-004, each
citing legacy anchors), `LESSONS.md`, `references/INDEX.md`. Redistributed
`CLAUDE.md` (dropped status/memory-file slots; swept entombed-skill refs; kept
commands + statistical invariants + style). `.Rbuildignore`: added `^cairn$`,
pruned 4 stale per-file entries.

### What the M22/M23 hardening got right (validated, not gaps)

| M2x fix | circumplex confirmation |
|---|---|
| M22 default-branch param | default is `master`; detection + branch/PR against `master` worked end-to-end. |
| M23 §0 Lineage B widening | status lived in a **forward-only ROADMAP + MILESTONES active slot**, *not* CLAUDE.md — the exact footprint M23 added; detected cleanly. |
| M23 §5 Compromise A | 315-line living DESIGN with embedded decision log mapped cleanly: kept verbatim, 4 decisions re-recorded, full extraction deferred. |
| M23 §6 reference sweep | CLAUDE.md named `/next-task`, `/statistical-validation`, `/release-checklist` (all entombed); swept — repointed to cairn equivalents, noted the entombed validation doctrine. |
| M23 §6 `.Rbuildignore` prune | 4 stale per-file entries pruned; `^CLAUDE\.md$`/`^\.claude$` correctly kept. |

### New gaps / friction (keyed to cairn-init §)

| # | Gap | § | Tag |
|---|---|---|---|
| G-C1 | **§1 fresh-scaffold omits `LESSONS.md`** — the scaffold tree lists DESIGN/ROADMAP/DECISIONS/dirs but not `LESSONS.md`, a top-level tracking file added in D-015 and present in the tracking-rules file-map. A fresh scaffold or migration never creates it. | §1 | **fix-here** |
| G-C2 | `cairn_validate` ISO-date scan **false-positives on `0/0/0`** (R CMD check "0 errors/0 warnings/0 notes" notation) — the `\d{1,4}/\d{1,2}/\d{1,4}` slash-date pattern matches it. Worked around by rewording; a clean regex fix is ambiguous (requiring a 4-digit year would regress on 2-digit-year dates). | scripts | candidate |
| G-C3 | **No-invention vs `planned`:** a legacy "planned" milestone with scope but no acceptance criteria/tasks (M6) can't become a valid cairn `planned` (which requires them) without invention → maps to `candidate`. §5's fixed mapping (`READY`→planned) is silent on this. | §5 | **fix-here** |
| G-C4 | **Mature backlog vs the <60-line ROADMAP cap:** a mature repo's parking-lot (continuous track + deferred review findings + pre-release items, ~20 items) blows the candidate budget if each is its own row. Handled by clustering related backlog into grouped candidate rows pointing at the entombed legacy ROADMAP. | §5/§6 | candidate |

### Disposition

The second pilot, run against the hardened protocol, surfaced **two small,
isolable `fix-here` gaps** (G-C1, G-C3) — a marked contrast with M20, where all
gaps were design-level and interconnected. That is itself the result: M22/M23
absorbed the design-level friction, leaving only mechanical residue. G-C1/G-C3
fixed this milestone (skill edit + guard test); G-C2/G-C4 → ROADMAP candidates.
