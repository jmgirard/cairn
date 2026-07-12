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

- [x] **T1 (G-I1):** §2 step 5 — concern-split case beside "Rich pre-existing
      `DESIGN.md`?": map concern-files to cairn homes, keep repo-specific else,
      thin DESIGN seed; cite M41.
- [x] **T2 (G-I2):** §2 step 6 — numbered-principle forced note-and-leave
      (keep file + numbering; defer IP/GP + in-code repoint to /design-interview
      + a code milestone); cross-ref ackwards G6.
- [x] **T3 (G-I4):** §6 — tracking-coupled (entomb) vs clean domain (keep/ask,
      "coupling wins" tiebreaker); §2 step 3 surfaces clean domain skills at the
      gate.
- [x] **T4 (G-I5):** §2 step 5 — name **pointer-only** as an explicit DECISIONS
      disposition for large decision logs.
- [x] **T5 (AC5):** `TestLineageAGuidance` (one assertion/addition, feature-unique
      single-line anchors); full `skills/tests` suite green.

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

PR #41. Fresh evidence 2026-07-12 on branch (main is ancestor; diff scoped to
`skills/` + `cairn/` only). Each AC's guard test passes and its anchor phrase is
absent on `main` (0 → deleting the addition fails its assertion; M39/M40
false-coverage trap proven avoided), each single-line (M23):

- AC1 (G-I1): §2 step 5 concern-split case — `test_concern_split_precursor_mapping`. ✓
- AC2 (G-I2): §2 step 6 forced note-and-leave — `test_numbered_principle_forced_note_and_leave`. ✓
- AC3 (G-I4): §6 classify + step-3 gate — `test_coupled_vs_clean_skill_classification`. ✓
- AC4 (G-I5): §2 step 5 pointer-only — `test_pointer_only_decisions_for_large_logs`. ✓
- AC5: `TestLineageAGuidance` + full `skills/tests` suite green (99 tests). ✓

**Consistency gate:** `cairn_validate` 12/12 (exit 0); Coverage AC1–AC5 → T1–T5
all map; principles GP4/IP2/IP3 are worked-under not changed (DESIGN untouched →
`cairn_impact --changed` N/A, slot PASS); R gates waived (plugin repo, no R files
in diff).

**Independent fan-out** (3 lenses, ref-based, shared tree) — **0 findings**:
- [O] diff-bug: AC fidelity + placement correct; guard genuinely locks; no
  principle/D-entry contradiction.
- [S] blame-history: §6 rewrite implements M41's own G-I4 recommendation and
  keeps collision-avoidance via the "coupling wins" tiebreaker (nothing
  weakened); existing `TestMigrationGuidance` intact.
- [S] prior-PR-comments: no prior-PR evidence (PRs #19–#33 on these files had
  empty review comments; M40 lesson).
- Scorer not run (no surviving findings). No fixes/follow-ups/rejections.
