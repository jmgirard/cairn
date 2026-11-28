# M89: Partial verification is a state — the staleness advisory stops failing toward green (done 2026-07-19)

**Goal:** a references page reporting incomplete or undatable verification stays on the staleness backlog instead of silently reading as fully checked.

**Outcome:** two false-green defects in `cairn_validate.py` closed. *A — partiality was invisible:* `partly verified at ingestion` parsed as a plain affirmative verification and aged from the block's ingested date, so `spec-kit`, `bmad-method` and `backlog-meridian` read `ok` while their own words said most of them were never checked; a `partial` state now sits between `verified` and `never`, returned before any date is read. *B — the gate and the advisory disagreed on what an ingested date is:* `_PROV_INGESTED` tests the shape, so `2026-13-45` satisfied the CHECK while `_iso` refused to parse it and the advisory skipped it as `undated`, each deferring to the other; both now share `_ingested_date` and the CHECK names the malformed value. Both note templates teach the partiality set and its consequence (5 mutation entries). Advisory here: OK (0) → WARN (3), all true positives left standing — clearing them needs a re-read of three external clones.

**Key decisions:** M89-D1 — the lattice is never > partial > verified; `{never, partial}` → `never` (a page saying it was never checked must not be upgraded), `{partial, verified}` → `partial` (qualifying is not contradicting), M83's `{never, verified}` → `ambiguous` preserved. Qualifier set kept to four literals, rejecting scope hedges per the M79-F5 lesson.

**Review:** 7/7 criteria verified. AC5 initially failed — a fixture had abbreviated its shipped quote — caught by comparing against the live pages by command. One finding (95): `spot-checked` overlaps the `checked against` verb, so slicing at the verb's start cut the qualifier in half and the phrasing the templates teach classified `ok`; the guard had masked it by handing every fixture an independent verb. Fixed on the branch. Blame-history and prior-PR lenses clean.

**PR:** https://github.com/jmgirard/cairn/pull/88
