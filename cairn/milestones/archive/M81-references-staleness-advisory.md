# M81 — References staleness advisory: the provenance block gets a reader

**Status:** done · approved 2026-07-18 · PR https://github.com/jmgirard/cairn/pull/79

**Goal.** Give the extraction-verified status a reader, so a page never checked against its source says so out loud.

**Outcome.** `check_references_staleness`, a WARN-tier `ADVISORIES` entry (never `CHECKS`), reads each committed page's `**Provenance.**` block and flags one recording no verified re-check, or last verified over 180 days ago, leaving the exit code untouched. It strips the `— observed` write stamp before reading any date (left in, it is always the freshest, and the advisory would read its own freshness), ages an undated "verified at ingestion" from the ingested date, takes the freshest of several, and exempts a status saying "nothing to re-verify against". The rulebook's "Re-verification." paragraph states the expectation and pins the record inline in the block; two anchors mutation-registered. Completes the `Adopt` verdict M56 banked and M57 half-shipped.

**First run.** 16 pages → 13 ok, 2 exempt, 1 flagged (`task-master.md`, never checked against its source → candidate row). `migration-pilot-notes.md` aligned to the sanctioned exemption phrase, heading off a false positive due in ~174 days.

**Decisions.** M81-D1: WARN tier, never a CHECK — block *presence* is structural, "too old" is a judgment about evidence quality (D-029, M79-D1); milestone-local because both precedents it argues from are. M81-D2: the three parse decisions — 180 days, undated ages from ingested, exemption earned by saying so.

**Review.** 3 lenses + scorer; 2 findings ≥80, both fixed on the branch. F1/93: the widened continuation test, shared with M79's hard CHECK, *erased* failures rather than creating them — the defended invariant was the wrong one; widening is now advisory-only (`for_extraction=True`). F2/87: a wrapped status invented staleness on re-verified pages (17 days old reported as 929 days); the status is now read to the end of its paragraph. 4 regression tests added. F3–F5 (68/63/62) logged, grouped into one candidate row.
