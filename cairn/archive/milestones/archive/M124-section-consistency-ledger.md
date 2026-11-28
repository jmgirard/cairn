# M124: A section-consistency ledger, so a contradicted or renamed rule reds

**Status:** done (2026-07-30, PR #124 https://github.com/jmgirard/cairn/pull/124)

**Goal:** Give a doctrine section a guard that reds when a rule inside it is
contradicted, renamed, or relocated, deriving what it checks from the section's own text.

**Outcome:** `skills/tests/section_ledger.py` — heading-scoped sentence extraction, no
content terms, callers pass the FULL heading — plus the committed 56-unit §8 ledger and
an alignment-based guard; `ledgers/extractor-contract.md`/`.expected.txt` pin the
extractor itself, which the ledger structurally cannot (it is invariant under
co-regeneration); guard-doctrine §9 (presence-vs-consistency, three defeating shapes,
detect-never-judge, remedy as operation the author runs); §8's two routing enumerations
name §9. M123's mutations (a)/(b), green through all 777 pre-milestone tests, now red
the ledger guard and nothing else.

**Decisions:** none milestone-local. D-088 (D-083 part 3(a) superseded), D-089 (D-088's
precedent list corrected). Seven §8 certification rounds (reopening 11, 9, 2, 3, 2, 2,
2) ended by maintainer override at round 7; M125 and D-090 own the rule that replaces it.

**Review:** 33 findings, 3 actioned, all fixed: F1 92 (AC1 scan defeated by a multi-line
list — now statement-derived), F2 85 (stale `moved` figures re-derived by procedure),
F12 88 (evidence count). Sub-80 logged in the file's Review section; git holds it.
Hygiene retired the M110 invocation-path lesson (ownership: PROFILE.md's verify slot).
