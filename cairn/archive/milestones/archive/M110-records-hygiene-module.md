# M110: Records-hygiene doctrine module

**Status:** done (2026-07-23, PR #108 https://github.com/jmgirard/cairn/pull/108)

**Goal:** Graduate the gate-time records-hygiene lesson family from LESSONS.md
into a second conditionally-read doctrine module — maturation's second application (D-055).

**Outcome:** New module `skills/shared/records-hygiene.md` (6 sections) distils
8 lessons graduated whole from LESSONS.md — M35 candidate-lifecycle, M51+M87
compression, M69 AC-amendment, M73 scorer-judgment, M77 archive-sweep+supersede,
M78 rule-home, M78 own-artifacts — read at a hygiene or plan gate. Rulebook
pointer added beside the LESSONS retirement rule (pinnable one-line coverage
map). LESSONS.md 49→41 lines. Guard `test_records_hygiene_graduation.py`
(22 tests) with 17 mutation-harness registrations across module/pointer/D-061.

**Decisions:** D-061 (annotates D-055) — second maturation; M69/M77 graduate
rather than ownership-retire (D-051 ownership targets a tracking-file slot;
skill prose isn't one). All 8 graduated whole, 0 trims.

**Review:** Three fresh-context lenses clean (diff-bug/blame/prior-review — no
functional, history, or regression findings). 1 cosmetic finding (registry
comment "four"→"three surfaces"), scored ~70, fixed. cairn_validate exit 0;
suites green (skills 598 / scripts / hooks 72). Nothing retired beyond the 8.
