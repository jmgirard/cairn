# Oracle-discipline assessment — ackwards M57

An assessment of the oracle discipline `jmgirard/ackwards` built in its M57
("Ossify oracles"), and a ledger of what generalizes back into cairn's own
validation doctrine. Same idiom as `migration-pilot-notes.md`: catalogue the
real artifact, map each element to cairn's current doctrine, tag each
`fix-here | candidate | out`. This is a repo-specific reference file (declares
its own scope). Cross-cutting outcome recorded as D-024.

---

## Lineage — intraclass → ackwards

- **`jmgirard/intraclass` (origin).** Established the *practice*: committed
  `data-raw/oracle-*.R` scripts as first-class reproducible provenance
  artifacts — each reproduces a numeric claim "from scratch," cites the ADR /
  PRINCIPLES entry it backs, and is usually mirrored by a live test (e.g.
  `oracle-fixed-vs-random.R` → `test-icc-consistency.R`). intraclass is **not
  cairn-tracked** (no `cairn/` dir) and has **no registry or taxonomy** — the
  discipline lived only as a naming convention + prose in each script header.
- **`jmgirard/ackwards` (formalization, M57).** Took that practice and made it
  a **catalogued, classified, guarded system** under `cairn/`: a registry file,
  a named type taxonomy, a numeric standard (Invariant #8), and a fixture-layer
  guard test. This is the mature exemplar the ledger below is keyed to.

## What ackwards M57 built

1. **`cairn/ORACLES.md` registry** — one row per oracle: ID, type, what it pins,
   the asserting `test:line`, source, provenance. Governing rule: *asserted
   state is single-sourced to the test file* — the registry maps to the test
   that asserts each oracle; the grep-verifiable `test:line` is the truth, not
   the table. An oracle is listed only once asserted (never a planned one).
2. **Oracle-type taxonomy** (four types):
   - **frozen** — an external reference value computed once (network/expensive)
     and committed as a fixture *with* a reproducible `data-raw/` generator +
     structured `provenance` attr.
   - **live** — an *independent implementation* (`psych`, `lavaan`) recomputed
     at test time. Held to be the **stronger** form: a frozen copy is a
     regression pin, not a cross-check — freeze a live oracle only if it becomes
     expensive/network-bound.
   - **invariant** — two independent internal routes that must agree; the
     agreement itself is the oracle, no external source.
   - **closed-form** — a published/definitional formula recomputed in-test with
     deliberately dumb explicit code.
3. **The standard** (ackwards CLAUDE.md Invariant #8): every numeric result
   verified against **≥2 independent oracle *types***; **no unsourced or
   unreproducible reference value ships**; fixtures carry a structured
   `provenance` attr naming their `data-raw/` generator.
4. **The guard** (`tests/testthat/test-oracle-provenance.R`): mechanizes the
   "nothing unsourced/unreproducible ships" half at the fixture layer — every
   committed `fixtures/*.rds` must carry a `provenance` list attr whose
   `generator` matches `^data-raw/.*\.R$` and whose `source` is non-empty; the
   test proves it has teeth (rejects missing / partial / made-up provenance).

## Gap ledger — mapped to cairn's Validation doctrine

cairn's current doctrine (`tracking-rules.md` "Validation doctrine
(statistical/numeric packages)") has a priority-ordered oracle list —
(1) hand-computed fixtures, (2) published reference values cited,
(3) independent recomputation, (4) invariant tests — plus the primary-sources
rule and source-ingestion. Element-by-element against ackwards:

| # | ackwards element | cairn today | Tag |
|---|---|---|---|
| E1 | Four-type vocabulary (frozen/live/invariant/closed-form) | overlapping priority list, but **no named vocabulary and no frozen/live distinction** | **fix-here** (M33) |
| E2 | "live independent-impl is the *stronger* form; don't freeze unless expensive/network-bound" | absent | **fix-here** (M33) |
| E3 | ≥2 independent oracle *types* per numeric result | "every numeric result via an oracle" — ≥1, no type-independence bar | **fix-here** (M33) |
| E4 | "no **unreproducible** reference value ships" | primary-sources rule covers *sourced*, not *reproducible* (regenerable) | **fix-here** (M33) — the reproducibility half is new |
| E5 | `ORACLES.md` registry file (per-oracle catalogue; asserted-state single-sourced to the test) | no registry concept | **candidate** — scaffold adoption, tied to toolchain-profiles |
| E6 | `provenance` attr on fixtures + `test-oracle-provenance.R` guard | source-ingestion covers *reference* provenance, not fixture-object provenance; guard is R/testthat-specific | **candidate** — R toolchain-profile slot |
| E7 | committed `data-raw/` generator per frozen fixture | "hand-computed fixtures" implies but doesn't mandate a committed regenerator | **fix-here** — the reproducibility *principle* folds via E4; the R `data-raw/` *mechanism* is deferred to the E6 candidate |
| E8 | Invariant #8 as interim home, to fold into a DESIGN IP/GP later | ackwards-local (its own `/design-interview` pass) | **out** — not cairn's to move |

## Disposition

The generalizable core (E1–E4) is **doctrine**: cheap, transferable prose that
strengthens an already-domain-scoped section — folded into `tracking-rules.md`
this milestone (M33). The **structure** (E5–E6) is deferred: a registry *file*
means the D-015/M16 four-wiring-points path plus a cap and an opt-in decision,
and it is domain-specific and entangled with the toolchain-profiles split
(which wants domain doctrine — oracles — kept orthogonal to the language
profile). Promoting E5/E6 *with* that work, not standalone, avoids pre-empting
where domain files should live. Mirrors the M20 finding in reverse: there the
gaps were design-level so nothing folded now; here the principles fold cleanly
and only the file structure waits.
