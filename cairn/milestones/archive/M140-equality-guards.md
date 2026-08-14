# M140: Whole-slice equality guards for the M139 rules

**Status:** done (2026-08-14, PR #140 https://github.com/jmgirard/cairn/pull/140)

**Goal:** The four M139 rule slices get whole-slice equality guards against
verbatim in-test fixtures, closing D-103's recorded exposure.

**Outcome:** four equality methods (`assertEqual(normalize(<slice>),
<fixture>)`) replace the twelve fragment regexes in `test_thrash_rule.py`; an
implement-side sub-slice bounds the M139 sentence at its own boundary; eight
marker-uniqueness asserts; the harness repointed (8 slice + 4 doctrine
registrations); guard-doctrine §1 gains the totality/granularity invariants
and §2 the inserting and whitespace blind spots. Probe evidence at b81ba07:
81 runs, 81 red, 0 green (matrix 35, insertion 9, relocation 24,
permutation 9, stale-fixture 4).

**Decisions:** none milestone-local — executes D-103 under RR12's BC1–BC7
with three recorded deviations (domain-command rebase; BC6 scoped for the
mandated doctrine edit; the strict-reading row for BC1/BC5).

**Review:** one pass, no return; 14 findings scored, two actioned and fixed
(O-F1/88, the sub-slice's end marker inside the next rule; O-F2/82, its
degenerate pair count); 12 logged sub-80, O-F5's caller-less
`implement_substantive()` promoted to a candidate row. M56's lesson line
extended: probe restores discard uncommitted edits.
