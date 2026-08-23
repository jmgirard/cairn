# M78: Source-note shape — dated observations and page provenance (done 2026-07-18)

**Goal:** Give `cairn/references/` pages an authored shape — provenance plus
dated observations in place of standing claims about the repo's own state.

**Origin:** heavy PDF ingestion in `intraclass`. Not registry drift (all four
registries reconcile); the recurring mode is a note asserting REPO state,
false by merge time — M65 F1/95 + F7/92, literal repeats of `LESSONS.md:45`
(M63) and `:48` (M64).
**Outcome:** `tracking-rules.md` "References pages" splits a page's claims into
**standing facts** (about the source) and **dated observations** (about the
repo's state, marked `— observed YYYY-MM-DD` inline), and mandates a
`**Provenance.**` block. Ships `skills/shared/templates/source-note.md` (cairn
had none), whose load-bearing field is extraction-verified status. All 16 of
this repo's pages backfilled, additive only (+64/−0), dates re-derived from git.
**Decisions:** D-M78-1 — observations mark inline, not in a section (M65's
failures were written inline by authors who believed they were stating facts).
AC2 amended at the implement gate: source field generalized beyond PDFs, all
16 local pages being non-PDF. Sizing WARN at 8 ACs accepted, not split.
**Review:** 8/8 ACs fresh-evidenced, two by live mutation (label swap, field
deletion). Three lenses + scorer, 5 findings. Actioned: F1/87 (rule written
into the domain-conditional module, violating D-031 — moved to core), F3/90
(the backfill introduced 16 undated repo-state claims, the exact failure the
rule forbids), F2/74 (over threshold per M73). Logged: F4/52, F5/22.
**PR:** https://github.com/jmgirard/cairn/pull/76
