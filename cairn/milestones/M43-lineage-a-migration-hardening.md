# M43: Lineage A migration hardening (cairn-init §2)

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP4, IP2, IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m43-lineage-a-migration-hardening · PR #41   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

Harden `/cairn-init` §2 with the four Lineage A migration gaps the M41
intraclass pilot surfaced, so a multi-file `project/` precursor migrates as
cleanly as the M22/M23-hardened Lineage B path.

## Scope

**In:** Four prose additions to `skills/cairn-init/SKILL.md` §2, each locked by
a guard test, closing the M41 pilot's design-level Lineage A gaps
(`references/migration-pilot-notes.md` Pilot 3):

- **G-I1 — concern-split precursor.** A Lineage A repo has no single
  `DESIGN.md`; it splits DESIGN concerns across dedicated files
  (PRINCIPLES/DECISIONS/REFERENCES/COVERAGE/spec dirs). §2 gains a mapping
  case beside Compromise A: integrate concern-files where cairn has a home,
  keep repo-specific where it doesn't, author a thin `DESIGN.md` seed pointing
  to them.
- **G-I2 (HEADLINE) — numbered-principle note-and-leave.** When package code
  cites principles by number (intraclass: `PRINCIPLES.md #N`, 70× / 29 files),
  keep the principles file with numbering + basename intact rather than folding
  into `DESIGN.md` IP/GP (which renumbers → strands refs or touches code,
  breaking docs-only); defer IP/GP formalization *and* the in-code repoint to
  `/design-interview` + a target-repo code milestone.
- **G-I4 — coupled-vs-clean skill classification.** §6 distinguishes
  tracking-coupled repo-local skills (drive the old board/gate → entomb) from
  clean domain skills (estimator/oracle workflows → keep or ask); clean domain
  skills are surfaced at the step-3 question gate for an explicit keep/entomb
  user decision.
- **G-I5 — pointer-only DECISIONS.** Name **pointer-only** (re-record nothing;
  `DECISIONS.md` is a pure pointer at the entombed legacy log) as an explicit
  disposition for large decision logs, beside "re-record still-governing".

**Out:**
- **G-I3 (oracle-registry home)** → the existing `ORACLES.md` candidate
  (ROADMAP), which M42 assessed and kept deferred behind toolchain-profiles.
- **`/design-interview` enhancement** (ingest a preserved numbered-principles
  file → drive IP/GP formalization + in-code repoint) → new candidate row; a
  target repo's own `/design-interview` run already formalizes principles.
- **Any target-repo in-code repoint / code milestone** → the target repo's own
  work, not cairn's (this milestone only writes the *guidance* that defers it).
- **A fresh live Lineage A re-pilot** → not run; guidance derives from the
  completed M41 pilot, verified by prose-guard + suite-green (per M22/M23).
- **Any `cairn_validate`/scripts change** → none; this is pure skill prose.

## Acceptance criteria

- [x] **AC1 (G-I1):** §2 gives concern-split guidance — for a precursor with no
      single `DESIGN.md`, map concern-files to cairn homes where they exist,
      keep repo-specific where none, and author a thin `DESIGN.md` seed that
      points to them; presented as a sibling to Compromise A, not a
      replacement. Evidence: the §2 prose + its guard assertion.
- [x] **AC2 (G-I2):** §2 gives numbered-principle note-and-leave guidance — when
      package code cites principles by number, keep the principles file
      (numbering + basename intact) rather than folding into IP/GP at migration,
      and defer formalization + the in-code repoint to `/design-interview` + a
      code milestone. Evidence: the §2 prose + its guard assertion.
- [x] **AC3 (G-I4):** §6 distinguishes tracking-coupled skills (entomb) from
      clean domain skills, and §2 step 3 surfaces clean domain skills at the
      question gate for an explicit keep/entomb decision. Evidence: the §6/step-3
      prose + its guard assertion.
- [x] **AC4 (G-I5):** §2 step 5 names **pointer-only** as an explicit DECISIONS
      disposition for large decision logs. Evidence: the §2 prose + its guard
      assertion.
- [x] **AC5:** `test_migration_guidance.py` is extended with one assertion per
      addition (AC1–AC4), each anchored on a phrase the feature *uniquely*
      introduces on a single line (M23 newline trap + M39/M40 false-coverage
      trap avoided — deleting an addition fails its assertion); the full
      `python3 -m unittest discover -s skills/tests` suite passes green.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] **T1 (G-I1):** In `skills/cairn-init/SKILL.md` §2 step 5, add a
      concern-split case beside the "Rich pre-existing `DESIGN.md`?" paragraph:
      Lineage A precursors have no single DESIGN; map concern-files to cairn
      homes (references → `references/`, decisions → `DECISIONS.md` pointer),
      keep repo-specific where cairn has none (coverage matrices, spec dirs) as
      declared repo-specific files, author a thin `DESIGN.md` seed that points
      to them. Cite the M41 intraclass lineage.
- [x] **T2 (G-I2):** In §2 step 6 (the repoint/note-and-leave reference sweep),
      add the numbered-principle case: when package code cites principles by
      number, keep the principles file at a `cairn/` path with numbering +
      basename intact (note-and-leave), do not fold into IP/GP at migration, and
      defer both IP/GP formalization and the eventual in-code repoint to
      `/design-interview` + a target-repo code milestone. Cross-reference the
      smaller ackwards G6 version.
- [x] **T3 (G-I4):** In §6, distinguish tracking-coupled skills (drive the old
      board/gate model → entomb) from clean domain skills (domain workflow value
      → keep or ask), and note the domain value may have no cairn home yet
      (feeds the toolchain-profiles / oracle-registry candidates); in §2 step 3,
      surface clean domain skills at the question gate for an explicit
      keep/entomb decision.
- [x] **T4 (G-I5):** In §2 step 5's decisions disposition, name **pointer-only**
      (re-record nothing; `DECISIONS.md` is a pure pointer at the entombed
      legacy log) as an explicit option for large decision logs, beside
      "only still-governing decisions are re-recorded".
- [x] **T5 (AC5):** Extend `skills/tests/test_migration_guidance.py` with a
      `TestLineageAGuidance` class — one assertion per T1–T4 addition, each
      anchored on feature-unique single-line phrasing (mentally delete the
      addition → its assertion must fail); run
      `python3 -m unittest discover -s skills/tests` and confirm green.

## Work log

- 2026-07-12: created by /milestone-plan. Promotes the M41-pilot "Lineage A
  migration guidance" candidate; scope set to G-I1/G-I2/G-I4/G-I5 (G-I3 →
  existing ORACLES.md candidate; /design-interview enhancement → new candidate).
- 2026-07-12: implement start; branch m43. No question gate (plan left no open
  implementation choices, no dep/RB tripwires). T1 (G-I1): concern-split case
  added to §2 step 5.
- 2026-07-12: T2 (G-I2, headline): numbered-principle forced note-and-leave
  added to the §2 step 6 reference sweep.
- 2026-07-12: T3 (G-I4): §6 coupled-vs-clean skill classification + step-3
  keep/entomb gate for clean domain skills.
- 2026-07-12: T4 (G-I5): pointer-only DECISIONS option named in §2 step 5.
- 2026-07-12: T5: TestLineageAGuidance added (4 tests, feature-unique
  single-line anchors); full skills/tests suite green (99 tests). All tasks
  done → status review.

## Decisions

## Review

PR #41. Fresh evidence gathered 2026-07-12 on branch (main is ancestor, no
divergence). Diff scoped to `skills/` + `cairn/` only (`git diff --name-only`).

**Acceptance criteria (AC fencing — evidence then tick):**

- AC1 (G-I1): §2 step 5 concern-split case present ("Concern-split precursor",
  "thin `DESIGN.md` seed"); `test_concern_split_precursor_mapping` passes; both
  anchors absent on `main` (branch-introduced). ✓
- AC2 (G-I2): §2 step 6 "forced note-and-leave" + "the eventual in-code repoint"
  present; `test_numbered_principle_forced_note_and_leave` passes; anchor absent
  on `main`. ✓
- AC3 (G-I4): §6 "classify, then entomb or ask" + step-3 "surfaced here too" /
  "an explicit keep-or-entomb decision" present;
  `test_coupled_vs_clean_skill_classification` passes; anchor absent on `main`. ✓
- AC4 (G-I5): §2 step 5 "pointer-only" + "pure pointer at the entombed legacy
  log" present; `test_pointer_only_decisions_for_large_logs` passes; anchor
  absent on `main`. ✓
- AC5: `TestLineageAGuidance` (4 tests) + full `skills/tests` suite green (99
  tests). Each primary anchor is single-line (M23) and feature-unique (0 on
  `main` → deleting the addition fails its assertion; M39/M40 trap proven
  avoided). ✓

**Consistency gate:**

- `cairn_validate.py` → 12/12 PASS, exit 0.
- Coverage completeness: AC1→T1, AC2→T2, AC3→T3, AC4→T4, AC5→T5 — every
  criterion maps to an existing task.
- Principle impact: Principles-touched (GP4/IP2/IP3) are *worked-under*, not
  changed — `cairn/DESIGN.md` untouched, so `cairn_impact --changed` is N/A;
  "principles slot valid" PASS.
- R-package gates (document/README/pkgdown/NEWS/`.Rbuildignore`): waived —
  plugin repo, no R machinery, diff touches no R files (CLAUDE.md).

**Independent fresh-context review:** (below)
