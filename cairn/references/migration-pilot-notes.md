# Migration stress-test — pilot notes

**Provenance.** Citekey `migration-pilot-notes` · ingested 2026-07-12 by M20 from synthesis note — first-hand findings from running `/cairn-init` §2 against mature Lineage B repos (Pilot 1: ackwards, M20).
Pagination: —.
Extraction: first-hand pilot record, not an extraction — nothing to re-verify against; each gap is tagged and traced to its ROADMAP disposition — observed 2026-07-18.

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
| G-C3 | **No-invention vs `planned`:** a legacy "planned" milestone with scope but no acceptance criteria/tasks (M6) can't become a valid cairn `planned` (which requires them) without invention → maps to `candidate`. §2 step 3's fixed mapping (`READY`→planned) is silent on this; fixed with a step-3 forward-ref + a step-5 note. | §3/§5 | **fix-here** |
| G-C4 | **Mature backlog vs the <60-line ROADMAP cap:** a mature repo's parking-lot (continuous track + deferred review findings + pre-release items, ~20 items) blows the candidate budget if each is its own row. Handled by clustering related backlog into grouped candidate rows pointing at the entombed legacy ROADMAP. | §5/§6 | candidate |

### Disposition

The second pilot, run against the hardened protocol, surfaced **two small,
isolable `fix-here` gaps** (G-C1, G-C3) — a marked contrast with M20, where all
gaps were design-level and interconnected. That is itself the result: M22/M23
absorbed the design-level friction, leaving only mechanical residue. G-C1/G-C3
fixed this milestone (skill edit + guard test); G-C2/G-C4 → ROADMAP candidates.

## Pilot 3 — intraclass (M41) — first **Lineage A**

- **Repo:** `jmgirard/intraclass`, R package, default branch **`main`**, pre-CRAN
  (`0.0.0.9000`). Far larger precursor than M20/M21: **47 milestones**, a
  **4959-line ADR log** (ADR-001..058), **34 `data-raw/oracle-*.R` scripts**, 4
  estimation engines.
- **First Lineage A pilot.** M20/M21 were Lineage B (status in CLAUDE.md / a
  forward-only ROADMAP). intraclass has a full multi-file `project/` board —
  `STATUS`/`MILESTONES`/`ROADMAP`/`DECISIONS`/`PRINCIPLES`/`COVERAGE`/`REFERENCES`
  + `estimand-specs/` + 6 repo-local `.claude/skills/`. §2's mapping was hardened
  against B, not A.
- **Migration PR:** https://github.com/jmgirard/intraclass/pull/54 (docs/tracking
  only — **0 package files touched**, verified `git diff main..HEAD`).
- **Health audit:** `cairn_validate` **12/12 clean** on the branch — no documented
  exception (contrast M20's 8/9; the D-018 cap fix + later hardening let a mature
  Lineage A repo pass clean).

### Ledger summary

Entombed → `cairn/legacy/` (100% renames): `STATUS`, `MILESTONES` (M1–M47),
`ROADMAP`, `DECISIONS` (ADR-001..058), `fable-brief-m32-s2`, the 6 repo-local
skills. Relocated live (100% renames): `PRINCIPLES.md` → `cairn/PRINCIPLES.md`
(numbering intact), `REFERENCES.md` → `cairn/references/`, `COVERAGE.md` +
`estimand-specs/` → `cairn/` (repo-specific). Authored: `DESIGN.md` (seed),
`ROADMAP.md` (legacy pointer + 3 candidates, IDs from **M48**), `DECISIONS.md`
(**pointer-only**), `LESSONS.md`, `references/INDEX.md`. Live state: 0 in-progress
(M47 shipped); release consolidation + parking lot + design/power question →
candidates. Redistributed `CLAUDE.md`; repointed the README roadmap ref.

### Gaps / friction (keyed to cairn-init §)

| # | Gap | § | Tag |
|---|---|---|---|
| G-I1 | **Concern-split precursor.** Lineage A has *no* `DESIGN.md`; it splits DESIGN concerns across dedicated files (PRINCIPLES/DECISIONS/REFERENCES/COVERAGE/estimand-specs). §2/§5 assume a single (thin or rich-Compromise-A) DESIGN. Resolved at gate: integrate where cairn has a home (references → `references/`), keep repo-specific where it doesn't (COVERAGE, estimand-specs), author a thin `DESIGN.md` seed that *points* to the others. | §2/§5 | candidate |
| G-I2 | **HEADLINE: principles cited by number in 70 in-code comments across 29 files** (`PRINCIPLES.md #N`). Folding them into `DESIGN.md`'s IP/GP (renumbering) strands all 70, or requires touching package code — breaking the docs-only rule. Forces **note-and-leave with numbering + basename preserved**; IP/GP formalization *and* the eventual in-code repoint defer to `/design-interview` + a **code** milestone. A bigger, blocking version of M20 G6. | §2/§6 | candidate |
| G-I3 | **No cairn-canonical oracle-registry home.** intraclass ships a mature oracle registry (`REFERENCES.md`); cairn has the *doctrine* (D-024) but not a registry *file*. Migration parks it repo-specific. Directly the deferred `ORACLES.md` candidate — **cairn M42 assesses fit**. | §5 | candidate (existing) |
| G-I4 | **§6 "entomb all repo-local skills" is too blunt — but right here.** 2 of 6 skills (`new-estimator`, `verify-estimator`) are *domain* workflow, yet tracking-**coupled** (they drive the `project/MILESTONES.md` board + old gate model), so entombing is correct. Their domain *value* (estimator scaffold, oracle-verification) has no cairn home → reinforces G-I3 + the R-provenance-guard candidate. §6 should distinguish coupled-tracking skills (entomb) from clean domain skills (keep/ask). | §6 | candidate |
| G-I5 | **`pointer-only` DECISIONS is unnamed but worked.** §2 step 5 frames the disposition as "re-record only still-governing"; for a 58-ADR log, **pointer-only** (re-record nothing; cite `ADR-0nn` into legacy) was cleanest + most no-invention-safe. Name it as an explicit option for large decision logs. | §5 | candidate |

### Disposition

Like **M20** (not M21): the gaps are **predominantly design-level and
interconnected** — Lineage A protocol guidance (concern-split mapping, numbered-
principle handling, skill classification, pointer-only) is a coherent addition to
`/cairn-init`, not a set of one-liners. Per the M22/M23 precedent (pilot findings →
a dedicated hardening milestone), all five promote to a single **grouped ROADMAP
candidate** for a deliberate Lineage A hardening milestone; **no `fix-here`
emerged** (a valid outcome, as in M20). The oracle-registry gap (G-I3) is the
existing `ORACLES.md` candidate, fed by cairn M42.
