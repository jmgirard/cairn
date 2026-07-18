# Validation doctrine (statistical/numeric work)

<!-- The domain-verification doctrine — a *module* of the core rulebook
     (tracking-rules.md references it; M58 extracted it under the norm "new
     domain doctrine gets a module, not a rulebook section"). It is UNIVERSAL
     domain doctrine, never a toolchain-profile slot (D-024/D-025): it would
     read identically in an R package, a Python package, or a Rust numerical
     crate. Read it whenever a milestone touches a numeric result or
     scoring/algorithmic content; a repo with no numeric work never needs it. -->

Tests verify against ground truth, not against the code. Every
numeric-results suite includes, in priority order: (1) hand-computed
fixtures from published formulas, arithmetic in comments; (2) published
reference values, cited; (3) independent recomputation with deliberately
dumb explicit code; (4) invariant tests; (5) simulation from known population
parameters — the estimator must recover the known value and/or its interval
must cover it at the nominal rate. Items (1)–(4) are deterministic
numeric-agreement oracles; (5) is the probabilistic one, and the appropriate
primary oracle where no closed form or reference implementation exists and for
interval methods — it is a rung on this list, not a lesser choice. Snapshots
only on top, never as the sole oracle for a number.

**Oracle types & the ≥2-types bar.** Name each oracle by *type*: **frozen** (an
external/expensive reference value computed once and committed as a fixture
*with* a reproducible generator), **live** (an independent implementation
recomputed at test time), **invariant** (two independent internal routes that
must agree — the agreement itself is the oracle, no external source),
**closed-form** (a published/definitional formula recomputed with deliberately
dumb explicit code), **simulation-coverage** (data simulated from known
population parameters; the estimator must recover the known value (point) and/or
its interval must cover it at the nominal rate — the injected ground truth is
the oracle). The five types refine the priority list, they don't replace it —
(1)/(2) are frozen or closed-form, (3) is live, (4) is invariant, (5) is
simulation-coverage. Every numeric result is backed by
**≥2 *independent* oracle types**, never two instances of one type. A **live**
independent implementation is the *stronger* form; a frozen copy of it is a
regression pin, not a cross-check — prefer live, and freeze it only when it
becomes expensive or network-bound. **simulation-coverage** is the one
*probabilistic* oracle — a
sampling-distribution check, not deterministic pointwise agreement — and the
primary oracle for interval methods (**a CI method's oracle is coverage**) and
for any estimator with no closed form or reference implementation; it counts
toward the ≥2-types bar like any other type. Freeze a simulation-coverage
oracle (commit its summary as a fixture) only when the run is expensive — a live
refit or a many-replication sweep — else recompute it live.

**Oracle registry (auditability).** As oracles multiply across a suite, the
≥2-types bar can only be checked if each oracle is recorded by
**ID, type, asserting `test:line`, source, and provenance** — the asserting
test is the single source of truth the record maps to, never a restated value.
The record's **shape is the repo's choice** — a central registry file,
distributed generator headers, or fields embedded in the committed fixture
object all satisfy it — so long as the ≥2-types audit reads off it. Record an
oracle only once its asserting test exists, never a planned one.
**Registry pointer (auditability's address):** a repo with numeric work
declares *where* its oracle records live in one line of its DESIGN.md
Conventions (e.g. "Oracle records: provenance headers in
`data-raw/oracle-*.R`", or "central `cairn/ORACLES.md`") — the shape stays
free, but the location is declared, so every audit has a deterministic entry
point; absence of the line in a repo with numeric work is itself the audit
finding (RR01 §4). Still advisory prose enforced by review judgment, never a
`cairn_validate` CHECK (D-029).

**Reproducibility (hard stop):** no unsourced *or unreproducible* reference
value ships. A committed numeric fixture carries its regeneration recipe — a
committed generator that reproduces it from scratch — so a stale or mis-sourced
value fails a test rather than sitting as a silent pin. Sourcing is the
primary-sources rule below; reproducibility is its second, independent half.

**Primary sources rule (hard stop):** never substitute secondary
descriptions or model memory for a primary source on scoring/algorithmic
content. Search (DOI, publisher, OSF); if inaccessible, stop and ask the
user for the PDF.

**Source ingestion:** the source itself → `cairn/references/sources/`
(gitignored) — a PDF where there is one, otherwise whatever was retrieved
(the shelf was named `pdf/` before M79; it holds any source, not only PDFs).
Summary → `cairn/references/<citekey>.md` (committed), authored from
`skills/shared/templates/source-note.md`: full citation,
extracted values with page/table anchors, verbatim-critical values quoted
exactly, which tests/oracles trace to it, open questions. One line in
`INDEX.md`. Tests and milestones cite `citekey (p. N)`, never restate.
(The `references/` page *types* and the page⇒INDEX-line rule are universal
file-family rules and live in tracking-rules "References pages"; this
workflow is the numeric/scoring-source instance of them.)

The claim-ageing rules that govern every committed page — standing facts vs.
dated observations, and the `**Provenance.**` block —
are universal file-family rules and live in tracking-rules "References pages" (D-031).
A numeric source note is bound by them like any other page; the ingestion
workflow above is the numeric/scoring-source instance.
