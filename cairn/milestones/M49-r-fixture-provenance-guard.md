<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M49: R fixture-provenance guard fold-in

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** —
- **Branch/PR:** m49-r-fixture-provenance-guard

## Goal

Fold a reproducible-fixture-provenance requirement into the r-package
profile's test-doctrine, mandating the provenance *content* while leaving its
*shape* to the repo.

## Scope

**In:** Add to the r-package profile `test-doctrine` slot a requirement that
every committed test fixture carry reproducible provenance — its source and
the committed generator (e.g. a `data-raw/` script) that regenerates it from
scratch, plus any seed — with the required *content* fixed and the *shape*
(a `provenance` attr, embedded `.rds`/`.rda` fields, or a header) left to the
adopting repo. This is the R-mechanical concretization of the universal
Validation-doctrine "Reproducibility (hard stop)". A `DECISIONS.md` entry
records the content-not-shape choice with rationale and supersede path; a guard
test locks the mandate.

**Out:** Adopting `ORACLES.md` as a cairn tracking file → stays the separate
deferred candidate (domain doctrine, entangled with the registry work — not
this milestone). Any target-repo fixture migration → out (this ships doctrine,
not a code touch in an R package).

## Acceptance criteria

- [ ] The r-package profile `test-doctrine` slot
      (`skills/shared/profiles/r-package.md`) mandates reproducible fixture
      provenance: source + committed generator + any seed per fixture, with the
      content required and the shape explicitly left to the repo — verifiable
      by guard-test tokens.
- [ ] A `DECISIONS.md` entry records the decision to mandate provenance
      *content* while leaving the *shape* free, citing the two-exemplar
      variance (ackwards' `provenance`-attr+guard vs. intraclass's embedded
      `.rds` fields) as the rationale, with a stated supersede path.
- [ ] A guard test locks the provenance-content mandate in the r-package
      profile; the active profile's `verify` slot is clean (all three
      `unittest` suites green). The "R-profile provenance guard" candidate row
      is graduated (removed) in the post-merge hygiene pass at completion.

## Coverage

- AC1 → T1, T3
- AC2 → T2
- AC3 → T3

## Tasks

- [x] T1 — Add the reproducible-fixture-provenance requirement to the r-package
      profile `test-doctrine` slot (content mandated: source + committed
      generator + seed; shape — attr / embedded field / header — left to the
      repo). Keep the file under the 90-line PROFILE cap.
- [x] T2 — Append the `DECISIONS.md` entry (next free D-id): mandate provenance
      content, leave shape free; rationale = two-exemplar shape variance;
      lineage = the M42-revised "R-profile provenance guard" candidate;
      supersede path stated.
- [x] T3 — Add a guard test (`test_toolchain_profiles.py`) asserting the
      r-package profile mandates the provenance content (source / generator /
      seed, shape-free). Run all three suites green. (Candidate-row graduation
      happens in review hygiene, not here — M35 lesson.)

## Work log

- 2026-07-13: created by /milestone-plan (paired with M48; independent, no dependency; promotes the M42-revised "R-profile provenance guard" candidate).
- 2026-07-13: implement started; branch m49-r-fixture-provenance-guard cut from main (baseline 218 tests green).
- 2026-07-13: T1 — added the reproducible-fixture-provenance bullet to the r-package profile test-doctrine slot (content: source + committed generator + seed; shape left free — attr / embedded field / header). Profile 76 lines (< 90 cap).
- 2026-07-13: T2 — appended D-028 (mandate provenance content, leave shape free; rationale = ackwards-attr-guard vs. intraclass-embedded-fields variance; supersede path stated).
- 2026-07-13: T3 — added TestRPackageFixtureProvenance (2 tests) locking the content mandate + shape-freedom; all three verify suites green (skills 123 / scripts 65 / hooks 32).

## Decisions

## Review
