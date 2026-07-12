<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M33: Assess ackwards' oracle discipline and fold its generalizable core into cairn

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m33-oracle-discipline-coordination   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Assess the oracle discipline ackwards built in its M57 ("Ossify oracles") and
fold the generalizable core into cairn's validation doctrine — capturing the
assessment as a reference file, strengthening the Validation doctrine section,
recording the maturation as a decision, and banking the structural pieces as
candidates.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- A reference file `cairn/references/oracle-discipline-notes.md` that catalogues
  ackwards' oracle system (the `ORACLES.md` registry, the frozen/live/invariant/
  closed-form type taxonomy, the ≥2-independent-types standard, the
  `test-oracle-provenance.R` guard), notes the `intraclass` lineage (data-raw
  oracle generators, not yet a registry), and maps each element to cairn's
  current Validation doctrine with a per-row `fix-here | candidate | out` tag.
- A bounded amend to the tracking-rules.md "Validation doctrine" section: add
  the four-type oracle vocabulary and the "live independent-impl is stronger
  than a frozen pin" nuance; add the "≥2 independent oracle *types* per numeric
  result" bar; add "no unsourced or unreproducible reference value ships." The
  existing priority-ordered list is preserved, not replaced.
- A `DECISIONS.md` entry recording the doctrine maturation and framing the two
  deferrals as candidates (never as rejections).
- Two ROADMAP candidate rows for the deferred structural pieces.
- A guard test locking the new doctrine anchors.

**Out:**
- Adopting `ORACLES.md` into cairn's file-map / scaffold / weight-caps / date-scan
  → candidate this milestone (domain-specific; entangled with the toolchain-profiles
  split — the D-015/M16 four-wiring-points path).
- Generalizing the R-specific `provenance` attr + `test-oracle-provenance.R`
  guard → candidate this milestone (belongs on the R side of the toolchain-profiles
  domain/language split).
- Changing ackwards itself → out; M57 shipped, this is cairn-side coordination.
- Folding ackwards' Invariant #8 into an ackwards DESIGN IP/GP → out; that is
  ackwards-local, pending its own `/design-interview` pass.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `cairn/references/oracle-discipline-notes.md` exists, catalogues all
      four elements of ackwards' oracle system (registry, the four oracle types,
      the ≥2-types standard, the provenance guard), cites the `intraclass`
      lineage, contains a gap ledger with one `fix-here | candidate | out` tag
      per mapped element, and is registered with a one-line entry in
      `references/INDEX.md`.
- [ ] AC2 — the tracking-rules.md "Validation doctrine" section names the four
      oracle types (frozen / live / invariant / closed-form) and states the
      "live independent-impl is stronger than a frozen pin" nuance.
- [ ] AC3 — the same section states the "≥2 independent oracle *types* per
      numeric result" bar and the "no unsourced or unreproducible reference value
      ships" rule, with the pre-existing priority-ordered list still present.
- [ ] AC4 — a new `DECISIONS.md` entry records the doctrine maturation, cites
      ackwards M57 and the assessment file, and states the two deferrals as
      candidates (not rejections).
- [ ] AC5 — two ROADMAP candidate rows are added: `ORACLES.md` scaffold adoption
      (tied to toolchain-profiles) and the R-profile `provenance`-attr/guard slot.
- [ ] AC6 — a guard test asserts the new Validation-doctrine anchors (the four
      type names + the ≥2-types bar), and the full guard suite
      (`python3 -m unittest discover -s skills/tests` and `-s scripts/tests`)
      passes.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Write `cairn/references/oracle-discipline-notes.md`: read the ackwards
      sources (M57 archive, `cairn/ORACLES.md`, CLAUDE.md Invariant #8,
      `tests/testthat/test-oracle-provenance.R`) and the `intraclass` `data-raw/oracle-*.R`
      lineage; catalogue the system; build the gap ledger mapping each element to
      cairn's Validation doctrine (tracking-rules.md:396–411) with a
      `fix-here | candidate | out` tag per row. Add its `references/INDEX.md` line.
- [x] T2 — Amend the "Validation doctrine" section of
      `skills/shared/tracking-rules.md`: surgically add the four-type taxonomy +
      the "live stronger than frozen" nuance, the ≥2-independent-types bar, and the
      reproducibility rule, keeping the existing priority list intact.
- [x] T3 — Append the doctrine-maturation D-entry to `cairn/DECISIONS.md` (cites
      M57 + the assessment file; frames both deferrals as candidates).
- [x] T4 — Add the two candidate rows to `cairn/ROADMAP.md`.
- [x] T5 — Add a guard test (e.g. `skills/tests/test_oracle_doctrine.py`) locking
      the new anchors; run the full unittest suite green (M32 lesson: this repo is
      unittest, not pytest).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: T1 — wrote references/oracle-discipline-notes.md (intraclass→ackwards lineage, 4-part system catalogue, E1–E8 gap ledger, disposition) + INDEX.md line. Finding: intraclass is not cairn-tracked — it originated the data-raw provenance-script practice; ackwards formalized the registry/taxonomy/guard.
- 2026-07-12: T2 — folded E1–E4 into tracking-rules Validation doctrine: added the frozen/live/invariant/closed-form vocabulary + "live stronger than frozen", the ≥2-independent-types bar, and the reproducibility hard-stop. Priority list preserved; kept the additions self-contained (no cross-repo citation — shared rulebook).
- 2026-07-12: T3 — appended D-024 (doctrine maturation; E5/E6 framed as candidates, not rejections). T4 — the two candidate rows (E5 ORACLES.md adoption, E6 R-profile provenance guard) already landed in the plan commit; verified present, no double-add.
- 2026-07-12: T5 — added skills/tests/test_oracle_doctrine.py (4 tests: four type names, ≥2-independent-types bar, live-is-stronger, reproducibility hard-stop). Suites green: 4 new + 78 skills/tests + 45 scripts/tests.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
