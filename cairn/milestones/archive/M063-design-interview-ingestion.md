# M63: /design-interview note-and-leave ingestion

- **Status:** done · **Priority:** normal · **Depends on:** — · **PR:** #61 · **Principles:** IP3/IP4 (worked-under; none changed)

## Outcome

Closed the M43 note-and-leave deferral: `/design-interview` now detects a
migration-preserved numbered-principles file at session start (a `cairn/`-path
doc kept with numbering + basename intact because package code cites it as
`PRINCIPLES.md #N` — intraclass: 70×/29 files) and runs an "Ingesting a
note-and-leave principles file" section on top of its two phases:

- Every `#N` enters Phase 2 pre-classified (IP/GP/skip, marked
  recommendation) carrying its lineage; other candidate sources still run.
- Conservation: every `#N` ends with an explicit disposition (IP3).
- Write-out records an old-`#N` → new-id mapping in the target DESIGN.md;
  the preserved file stays intact until the repoint ships (IP4).
- The in-code repoint is banked as a target-repo code-milestone candidate;
  the interview performs no code edits.

`migration-protocol.md`'s deferral now names the ingestion step. Guards:
`TestNoteAndLeaveIngestion` (7 tests) + 7 mutation registrations.
Verification: 6/6 ACs fresh evidence; `cairn_validate` all-pass; suites
192/84 OK; 3-lens fan-out 0 findings (prior-PR lens: no evidence, expected);
no CI on this repo. Graduates the 2026-07-12 ingestion candidate row.
