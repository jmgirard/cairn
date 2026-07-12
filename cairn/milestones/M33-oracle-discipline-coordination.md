# M33: Assess ackwards' oracle discipline and fold its generalizable core into cairn

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m33-oracle-discipline-coordination · https://github.com/jmgirard/cairn/pull/31
## Goal

Assess the oracle discipline ackwards built in its M57 ("Ossify oracles") and
fold the generalizable core into cairn's validation doctrine — capturing the
assessment as a reference file, strengthening the Validation doctrine section,
recording the maturation as a decision, and banking the structural pieces as
candidates.

## Scope

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

- [x] AC1 — `cairn/references/oracle-discipline-notes.md` exists, catalogues all
      four elements of ackwards' oracle system (registry, the four oracle types,
      the ≥2-types standard, the provenance guard), cites the `intraclass`
      lineage, contains a gap ledger with one `fix-here | candidate | out` tag
      per mapped element, and is registered with a one-line entry in
      `references/INDEX.md`.
- [x] AC2 — the tracking-rules.md "Validation doctrine" section names the four
      oracle types (frozen / live / invariant / closed-form) and states the
      "live independent-impl is stronger than a frozen pin" nuance.
- [x] AC3 — the same section states the "≥2 independent oracle *types* per
      numeric result" bar and the "no unsourced or unreproducible reference value
      ships" rule, with the pre-existing priority-ordered list still present.
- [x] AC4 — a new `DECISIONS.md` entry records the doctrine maturation, cites
      ackwards M57 and the assessment file, and states the two deferrals as
      candidates (not rejections).
- [x] AC5 — two ROADMAP candidate rows are added: `ORACLES.md` scaffold adoption
      (tied to toolchain-profiles) and the R-profile `provenance`-attr/guard slot.
- [x] AC6 — a guard test asserts the new Validation-doctrine anchors (the four
      type names + the ≥2-types bar), and the full guard suite
      (`python3 -m unittest discover -s skills/tests` and `-s scripts/tests`)
      passes.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T5

## Tasks

- [x] T1 — Write `references/oracle-discipline-notes.md` (catalogue + E1–E8 gap ledger) + INDEX line.
- [x] T2 — Amend tracking-rules "Validation doctrine" (four-type taxonomy, ≥2-types bar, reproducibility; priority list kept).
- [x] T3 — Append the doctrine-maturation D-entry to `cairn/DECISIONS.md`.
- [x] T4 — Add the two candidate rows to `cairn/ROADMAP.md`.
- [x] T5 — Add guard test `skills/tests/test_oracle_doctrine.py`; full unittest suite green.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: T1 — wrote references/oracle-discipline-notes.md (intraclass→ackwards lineage, 4-part system catalogue, E1–E8 gap ledger, disposition) + INDEX.md line. Finding: intraclass is not cairn-tracked — it originated the data-raw provenance-script practice; ackwards formalized the registry/taxonomy/guard.
- 2026-07-12: T2 — folded E1–E4 into tracking-rules Validation doctrine: added the frozen/live/invariant/closed-form vocabulary + "live stronger than frozen", the ≥2-independent-types bar, and the reproducibility hard-stop. Priority list preserved; kept the additions self-contained (no cross-repo citation — shared rulebook).
- 2026-07-12: T3 — appended D-024 (doctrine maturation; E5/E6 framed as candidates, not rejections). T4 — the two candidate rows (E5 ORACLES.md adoption, E6 R-profile provenance guard) already landed in the plan commit; verified present, no double-add.
- 2026-07-12: T5 — added skills/tests/test_oracle_doctrine.py (4 tests: four type names, ≥2-independent-types bar, live-is-stronger, reproducibility hard-stop). Suites green: 4 new + 78 skills/tests + 45 scripts/tests.

## Decisions

## Review

**Reviewed 2026-07-12 · PR #31 · branch `m33-oracle-discipline-coordination`.**
Docs-only milestone in the plugin repo; R-package gates (devtools/pkgdown/NEWS/
.Rbuildignore) waived per CLAUDE.md. Default branch `main` in sync with origin;
branch not behind — no re-merge needed.

### Acceptance-criteria evidence (fresh)

- **AC1 ✓** — notes file exists (85 ln); catalogues all 4 elements; `intraclass` lineage cited; E1–E8 ledger each tagged; INDEX line present.
- **AC2 ✓** — doctrine names all four types + the "stronger-form" nuance (grep-verified single-line anchors).
- **AC3 ✓** — states the "≥2 *independent* oracle types" bar + reproducibility hard-stop; priority list still present.
- **AC4 ✓** — D-024 present; cites M57 + the notes file; frames E5/E6 as deferred candidates, not rejections.
- **AC5 ✓** — two `M33 Out` candidate rows in ROADMAP (ORACLES.md adoption; R-profile provenance guard).
- **AC6 ✓** — `test_oracle_doctrine.py` (4 tests) + full suites green (78 skills + 45 scripts).

### Consistency gate

`cairn_validate.py` → exit 0, all 10 checks PASS. Coverage completeness: all six
criteria map to existing tasks (AC1→T1, AC2/AC3→T2, AC4→T3, AC5→T4, AC6→T5). No
`DESIGN.md` IP/GP changed (doctrine lives in tracking-rules, not a numbered
principle) → `cairn_impact` skipped. R gates waived (plugin repo). (The Review
section initially pushed this file to 158 lines > cap; reclaimed to <150 by
stripping the redundant `<!-- owner -->` scaffolding comments — M19/M22 remedy —
after which `cairn_validate` passes.)

### Independent fresh-context review

Two lenses (distinct evidence bases) + a Sonnet scorer. Two findings surfaced:

- **F2 (score 97, FIXED) — milestone-file cap violation + stale evidence.**
  Adding the Review section pushed the file to 158 lines, failing
  `cairn_validate` weight caps, while the section still asserted "all 10 checks
  PASS." The blame-history lens flagged it as the M19/M22 lesson recurring.
  Fixed on-branch by the M19 remedy (strip owner-scaffolding comments → 138
  lines); `cairn_validate` re-run clean.
- **F1 (score 68, FIXED at user request).** The ledger row E7 carried a `split`
  tag, a fourth value outside AC1's stated `fix-here | candidate | out`
  vocabulary. Below the 80 threshold (an AC-wording gap, not a work defect —
  E7's outcome was openly disclosed), so logged, not auto-actioned; the user
  then elected to resolve it. Retagged E7 → `fix-here` (its primary disposition;
  the R `data-raw/` mechanism-deferral stays as prose pointing at the E6
  candidate), so all 8 ledger rows now use the three-value vocabulary AC1
  specifies.

No correctness, self-containment, or section-ownership defects found; the
diff-bug lens confirmed the doctrine additions are self-contained and the guard
test's anchors all match single physical lines.
