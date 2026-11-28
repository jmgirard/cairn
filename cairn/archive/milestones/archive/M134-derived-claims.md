# M134: Branch-added behavior claims are derived from the artifact, not the author's model

**Status:** done (2026-08-04, PR #134 https://github.com/jmgirard/cairn/pull/134)

**Goal:** Branch-added prose claims about an artifact's behavior are derived
from the artifact at write time, with the rule stated where every implement
session reads it.

**Outcome:** tracking-rules "Universal tracking rules" gains the
derived-claims rule — derive-don't-compose over tracking records, comments,
docstrings, changelog entries and docs; restatement-is-not-written;
pointer-over-enumeration — with a write-time pointer in /milestone-implement
step 4 and a changelog-claims sentence in the What-gets-a-test floor;
guard-doctrine §6's narrow evidence-counts copy trimmed to a cross-reference.
7 guards + 6 harness registrations; 14 inversion probes RED. Motivated by
intraclass M103's prose-only thrash, hosted per D-098; audit-style remedies
rejected (M127/RR06/M114).

**Decisions:** none promoted; the plan-gate approach choices are in the
work log with falsifiers.

**Review:** 25 candidates, 3 actioned and fixed inline (D10/80 restating
cross-reference, D14/88 stale work-log count, D15/80 evidence attribution),
22 logged. Graduated: the M116 lesson's remedy half into the rule; its
uncovered diagnostic half restored to LESSONS as a trimmed remainder.
