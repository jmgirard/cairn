<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M80: References-page authoring — the ingestion trigger and the synthesis-note template

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m80-references-authoring` · https://github.com/jmgirard/cairn/pull/78   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make authoring a `cairn/references/` page a triggered act with a template for
either page type, instead of a recipe only numeric sessions ever meet.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The authoring trigger — when consulting a source obliges a committed
page — stated in `tracking-rules.md` "References pages" (`:588-630`), the
universal section every skill already reads whole, with both template paths
named there (today neither is). A shipped
`skills/shared/templates/synthesis-note.md`, drawn from the six synthesis pages
already in this repo. Registration of the new template in the inventories that
enumerate templates. Guard tests, mutation-registered.
Also fixes the shipped `source-note.md` template, whose `Extraction:` line
wraps and carries no `— observed` stamp, so a page authored from it fails the
dated-extraction guard M78 shipped alongside it (proven at the M80 implement
gate, 2026-07-18). Same defect class and same one-line fix as the synthesis
template's.

**Out:**
- The staleness advisory → M81 (planned now, depends on this).
- Per-skill read directives → **refused** at the plan gate, not deferred:
  D-031 forbids them and is not being superseded. Moving the trigger into core
  is the D-031-compatible shape, matching the boundary D-031 itself drew.
- Citekey resolution / dependent discovery → the existing ROADMAP candidate
  row; still blocked on an M56 supersession.
- Source-shelf rename migration → the existing ROADMAP candidate row.
- Re-verifying this repo's own pages → M81 AC5.
- Rewriting `validation-doctrine.md`'s numeric ingestion recipe beyond
  reconciling its pointer, so the module keeps the numeric instance and core
  keeps the universal trigger.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: `tracking-rules.md` "References pages" states the authoring trigger
      and names both template paths; the trigger sentence is absent from
      `validation-doctrine.md`. A guard asserts both the presence in core and
      the absence from the conditional module (LESSONS `:49` placement test).
- [ ] AC2: `skills/shared/templates/synthesis-note.md` exists carrying: an H1
      naming the owning milestone; a `**Provenance.**` block using the literal
      field words `Ingested` and `Extraction: `; a scope paragraph disclaiming
      tracking authority; an evidence snapshot; a ledger with stable row IDs
      and a stated tag vocabulary; a Disposition section.
- [ ] AC3: a test reads the **real** shipped synthesis template, instantiates
      it (placeholder dates substituted for real ones) as a page in a temporary
      `cairn/references/` tree with its `INDEX.md` line, and runs the **real**
      `check_references` (`cairn_validate.py:304`) and the **real**
      extraction-date assertion (`test_source_note_template.py:213-227`, whose
      glob is type-blind and already binds synthesis notes) over it — both
      clean. The template is read from disk, never copied into the test
      (M77 pairing rule, LESSONS `:46`). Amended at the implement gate
      2026-07-18: the original wording required the template *itself* to pass,
      which its `YYYY-MM-DD` placeholders make impossible.
- [ ] AC4: the template inventories naming the shipped set are updated:
      `cairn/DESIGN.md:38-39` and `README.md:136`.
- [ ] AC5: every new positive prose assertion is registered in
      `skills/tests/test_mutation_harness.py`, and its completeness meta-test
      is green (registration is per file *and* per new assertion — LESSONS `:20`).
- [ ] AC6: verify clean — `python3 -m unittest discover` for `skills/tests`,
      `scripts/tests`, `hooks/tests` each exit 0, checked individually and
      never through a pipe (LESSONS `:23`); `cairn_validate` exit 0.
- [ ] AC7: a page instantiated from `skills/shared/templates/source-note.md`
      passes the same real `check_references` and real dated-extraction guard
      as AC3's synthesis page — the pairing test covers **both** shipped
      templates, so neither can regress alone. Added at the implement gate
      2026-07-18; the defect was proven, not suspected.

## Coverage
<!-- owner: plan · create/amend-via-gate; review reads to fence evidence. -->

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5
- AC5 → T6
- AC6 → T6
- AC7 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Author the trigger and both template pointers into
      `tracking-rules.md` "References pages"; reconcile
      `validation-doctrine.md:75-91` so its numeric recipe defers to core for
      the trigger without restating it. Watch the always-read line budget —
      this adds to the file GP1 caps.
- [x] T2: Write `skills/shared/templates/synthesis-note.md` from the common
      shape of the six existing synthesis pages (`competitive-landscape`,
      `migration-pilot-notes`, `oracle-discipline-notes`,
      `oracle-doctrine-intraclass-notes`, `design-interview-notes`,
      `desktop-toc-mechanism`). Reuse the literal field words `Ingested` and
      `Extraction: ` — `cairn_validate.py:227` and
      `test_source_note_template.py:221` hard-require them, so any other
      wording is a coordinated validator + guard change.
- [x] T3: Extend `skills/tests/test_references_pages.py` with a
      `TestShippedSynthesisTemplate` reading the real shipped file (mirror
      `test_source_note_template.py:139-188`), plus the AC1 core-vs-module
      placement asserts. Author every anchor phrase on its own physical line
      (LESSONS `:27`).
- [x] T4: Add the pairing test required by AC3 — the real checker and the real
      extraction guard over the real shipped template, not a fixture copy.
- [x] T5: Update the `cairn/DESIGN.md` templates bullet and the `README.md`
      references line (the latter is also stale on `pdf/` → `sources/`; fix in
      passing, D-047).
- [x] T6: Register the new assertions in the mutation harness; run the three
      suites and `cairn_validate`, checking each exit code.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-18: created by /milestone-plan; promoted the M78/M79 grouped candidate row ahead of its "promote once M78's template is in use" gate — the gate is self-blocking, since nothing triggers the template's use and that is the very gap being fixed.
- 2026-07-18: /milestone-implement started; branch `m80-references-authoring` cut from synced main.
- 2026-07-18: T1 — trigger + both template paths into tracking-rules "References pages"; validation-doctrine's parenthetical now defers the trigger instead of restating it. Gate answers: a page is owed when the repo relies on the source; a synthesis note when the analysis outlives its milestone.
- 2026-07-18: T4 — pairing test instantiates the shipped template into a temp tree and runs the real check_references + real dated-extraction guard; AC3 amended at the implement gate (placeholder dates cannot satisfy the date regex, so the criterion tested the wrong subject). Extracted DATED_EXTRACTION/extraction_line into one shared definition so template and repo-page checks cannot drift.
- 2026-07-18: /milestone-review started; draft PR #78 opened; branch confirmed current with origin/main (0 behind). Consistency gate clean: cairn_validate exit 0, generic profile names no toolchain checks, no IP/GP text changed so cairn_impact skipped. Three review lenses spawned; Review section pending their findings.
- 2026-07-18: T6 — four Mutation entries registered (three on the rulebook, one on the module) with a DOCTRINE target constant added; each block verified to occur exactly once. Suites: skills 336, scripts 128, hooks 72, each exit 0 checked individually; cairn_validate exit 0. Status → review. (AC boxes left unticked: fencing makes those review's verification marks, not implement's.)
- 2026-07-18: T5 — DESIGN templates bullet gains the synthesis note; README's references line fixed from the stale `PDFs gitignored` to `sources/ gitignored` (D-047). Repo-wide sweep (LESSONS :18): CHANGELOG's template list is a shipped release entry and stays as history; remaining `references/pdf` hits are the D-047 deprecation path and history.
- 2026-07-18: scope amended at the implement gate — AC7 added after the pairing test proved M78's shipped source-note template emits a page failing M78's own dated-extraction guard (wrapped line, no `— observed` stamp). Same fix; the pairing test now covers both templates.
- 2026-07-18: T4 caught a live defect in the template T2 had just shipped — the wrapped `Extraction:` status lost its `— observed` stamp, so every page authored from it would have failed the repo's own guard; fixed to one physical line, exactly the M77 pairing failure this test exists to catch.
- 2026-07-18: T3 — added TestAuthoringTrigger (core-vs-module placement, positive defer-assert paired with the negative absence-assert per M54) and TestShippedSynthesisTemplate (12 fields, read from the shipped file); skills suite 324 → 333, exit 0.
- 2026-07-18: T2 — shipped `skills/shared/templates/synthesis-note.md`; sections drawn from the six existing synthesis pages, `Ingested`/`Extraction:` field words kept verbatim so the references check and the dated-observation guard both still parse.
- 2026-07-18: T1 hit LESSONS :27 live — the reflow duplicated a mutation-registered anchor in validation-doctrine.md; reworded the new prose rather than re-anchoring the guard (LESSONS :32).

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive; EXEMPT from the 150-line cap (M55). -->
