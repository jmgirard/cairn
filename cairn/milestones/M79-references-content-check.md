<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M79: References content check — the lint stops being a filename census

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M78   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m79-references-content-check` · https://github.com/jmgirard/cairn/pull/77   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create/amend-via-gate -->

Make `check_references` verify that a committed references page carries
provenance and a citation, and close the two enforcement gaps that let pages
escape the check entirely.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `cairn_validate.check_references` (`cairn_validate.py:177-202`) gains
content checks over M78's shipped shape — a page must carry a `**Provenance.**`
block naming both an ingested date and a source pointer. Plus the two gaps
found in the M78 audit: the flat `os.listdir` at `:189`, which makes any
nesting under `references/` silently unenforced, and the outright PASS at
`:185-186` when `INDEX.md` is absent. Advisory-vs-hard placement is decided in
T1 against D-023's no-false-positive doctrine and D-029's precedent that the
oracle registry stays review-judgment, never a CHECK.

Folded in at the implement gate (2026-07-18): the `cairn/references/pdf/` →
`cairn/references/sources/` rename. The name is under-general now that M78
ships non-PDF provenance (a URL plus retrieval record), and it is cairn's own
scaffold name, not an adopting repo's choice. Post-1.0, the legacy `pdf/`
gitignore entry stays accepted with a deprecation notice rather than failing
an adopting repo.

**Out:** citekey resolution and dependent discovery — un-excluding
`references/` from `cairn_impact.py:45` so a corrected page surfaces its
consumers → candidate row, blocked on M56's standing rejection of "a formal
query op" and "graph tooling". Re-verification scheduling (a page declaring
when it was last checked against its PDF) → candidate row. Any change to the
doctrine or template shape → M78 owns those.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] `check_references` reports a committed `references/` page that carries
      no `**Provenance.**` block, one whose provenance names no ingested date,
      and one whose provenance names no source pointer, at the severity T1
      selects, with the emitted label used verbatim in any prose that names it
      (M64).
- [x] The check reads `references/` recursively, so a page in a subdirectory
      is enforced exactly as a top-level page is — proven by a fixture with a
      nested page that currently passes and must not.
- [x] A `references/` directory holding committed pages but no `INDEX.md` no
      longer renders PASS from this check.
- [x] The parser tolerates cosmetic decoration on every semantic token it
      reads — backticks, markdown links, bold — pinned by fixtures for the
      decorated variants, not only the bare format (M57 / D-023).
- [x] Every existing page in this repo's own `cairn/references/` passes the
      new check, or is corrected in place under D-045 with the correction
      marked; no page is grandfathered silently.
- [x] `scripts/tests/test_scripts.py`'s shared `Tree.build()` fixture is
      extended so the stricter check does not fail unrelated validate tests
      (M24), and the full suite is green.
- [x] Verify clean per `cairn/PROFILE.md`: `python3 -m unittest discover` over
      `skills/tests`, `scripts/tests`, and `hooks/tests`, each exit 0, run from
      the repo root and not tail-piped (M56/M65).
- [x] `cairn/references/pdf/` is renamed to `cairn/references/sources/`
      everywhere cairn writes it — scaffold dirs, the required `.gitignore`
      entry, the rulebook file map and dated-observations rule, the ingestion
      recipe, the source-note template, and `cairn-init`'s tree — with no live
      `references/pdf` string left in the plugin outside history
      (`DECISIONS.md`, `milestones/archive/`, `legacy/`, and existing
      `references/` pages, which IP4 and D-045 govern); and an adopting repo
      carrying only the legacy `pdf/` gitignore entry still passes
      `check_scaffold` with a deprecation notice, pinned by a fixture.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T3
- AC4 → T2, T4
- AC5 → T5
- AC6 → T4
- AC7 → T6
- AC8 → T7, T8

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1. Decide hard-CHECK vs ADVISORY for the content conditions and record
      it as a milestone-local decision: D-023 tolerates a miss over a false
      positive, and D-029 kept the oracle registry out of the validator
      entirely. Human-authored markdown argues advisory; the shipped M78
      template argues enforceable. (RB tripwire: ip-touching — the answer sets
      whether a repo can be blocked by its own reference prose.)
- [x] T2. Implement the citation and ingested-date content checks against
      M78's template shape, decoration-tolerant per D-023.
- [x] T3. Replace the flat `os.listdir` (`cairn_validate.py:189`) with a
      recursive walk, and remove the absent-`INDEX.md` PASS (`:185-186`) —
      keeping the M45 no-op only where it is genuinely a not-adopted signal.
- [x] T4. Extend `scripts/tests/test_scripts.py`: fixtures for the nested
      page, the missing-INDEX directory, the decorated variants, and each new
      failing condition. Extend the shared `Tree.build()` fixture first (M24).
- [x] T5. Run the new check over this repo's real `cairn/references/` pages;
      correct any failing page in place with the correction marked (D-045).
- [x] T6. Run the three suites from the repo root, check each exit code
      explicitly before any commit; append the work-log line.
- [x] T7. Rename `pdf/` → `sources/` across the plugin:
      `cairn_scripts.REQUIRED_GITIGNORE` + the scaffold-dirs comment,
      `cairn-init` §1 tree + gitignore bullet, `tracking-rules.md` file map +
      dated-observations rule, `validation-doctrine.md` source ingestion,
      `source-note.md` template, and this repo's own `.gitignore`. Record as
      D-047 (post-1.0 scaffold-contract change).
- [x] T8. Add the legacy-`pdf/` deprecation path to `check_scaffold`, with
      fixtures in `scripts/tests/test_scaffold_check.py`; re-point
      `skills/tests/test_source_note_template.py`'s source-pointer assertion.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-18: created by /milestone-plan. Gaps sourced from the M78-planning audit of `cairn_validate.py:177-202` — the check is a filename census, so an empty page with an INDEX line passes clean.
- 2026-07-18: /milestone-implement started; branch `m79-references-content-check` cut from main. Baseline verify green (skills 324, scripts 111, hooks 72; each exit 0).
- 2026-07-18: review — the 2026-07-18 audit line below says "17 committed pages"; the correct count is 16 (17 files in `references/`, of which `INDEX.md` is not a page). Superseded here rather than edited, per IP4. The 16/16 provenance figures and the AC5 conclusion are unaffected.
- 2026-07-18: review — [O] diff-bug lens returned 5 findings (F1 80, F2 95, F3 92, F4 90, F5 85), all fixed on the branch with regression fixtures; blame-history and prior-PR lenses returned none. Post-fix: skills 324, scripts 128, hooks 72, each exit 0; validate exit 0.
- 2026-07-18: T6 done — final verify from the repo root, each suite's exit code read explicitly and not tail-piped: skills 324 exit 0, scripts 123 exit 0, hooks 72 exit 0. Status → review.
- 2026-07-18: T7-T8 done — source shelf renamed `references/pdf/` → `references/sources/` across scaffold, gitignore, rulebook, ingestion recipe, template and cairn-init; recorded as D-047. Legacy entry accepted by `check_scaffold` with a new non-failing `scaffold deprecations` advisory (post-1.0 deprecation cycle); `check_references` skips both shelf names when walking.
- 2026-07-18: T2-T5 done — `check_references` now walks `references/` recursively, parses M78's provenance block (ingested date + `from` source pointer) decoration-tolerantly, and reports an absent INDEX.md over real pages instead of passing. Word-boundary note: `_` is a word char in Python regex, so `__Provenance__` needs non-alnum lookarounds, not `\b`.
- 2026-07-18: T5 evidence — all 16 committed pages in this repo pass the new check unmodified; no page needed a D-045 in-place correction, so nothing is grandfathered.
- 2026-07-18: T1 done — hard CHECK, user-selected at the implement gate; recorded as M79-D1 (milestone-local: the severity is this check's, not cairn-wide doctrine).
- 2026-07-18: AMENDMENT (gated) — AC1 now checks a Provenance source pointer, not a citation line: M78's template scopes `**Citation.**` to published primary sources, so a blanket check contradicts it. Goal's "and a citation" clause is narrowed by this AC, not re-cut; Goal text left untouched (plan-owned, no amend mode).
- 2026-07-18: AMENDMENT (gated) — `references/pdf/` → `references/sources/` rename folded into Scope In as AC8 / T7-T8, user-chosen at the implement gate. 8 ACs sits at the ~7 split tripwire; accepted as one coherent change rather than a split.
- 2026-07-18: audit of this repo's 17 committed pages — 17/17 carry Provenance + an ingested date, 1/17 carries a labelled Citation. AC1's citation half fires on 16 pages; surfaced at the question gate.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

### M79-D1 (2026-07-18): The references content conditions are a hard CHECK

**Context:** T1 was tagged `(RB tripwire: ip-touching)` — the answer sets
whether a repo can be blocked by its own reference prose. D-029 kept the
oracle registry out of the validator; M33/M42/M49 made advisory doctrine never
a validate gate.
**Decision:** Hard CHECK, user-selected at the M79 implement gate. D-029 does
not transfer: a registry entry is a *judgment* about evidence quality, while a
`**Provenance.**` block naming an ingested date and a source pointer is a
*structural* field of a shipped template — the class of thing this check
already hard-fails on for `INDEX.md`. D-023's no-false-positive doctrine is
honoured in the parser, not the severity (AC4's decoration tolerance).
Rejected advisory WARN (an unenforced check is one nobody fixes) and a split
CHECK-block/WARN-fields form (two severities for one template; an empty block
is as broken as an absent one).
**Consequences:** A committed page without provenance fails `cairn_validate`;
adopting repos with pre-M78 pages hit one FAIL on upgrade — the migration cost
D-040 accepted for the `changelog` slot. If a semantically sound page ever
fails, fix the parser; if the severity is wrong, supersede here.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->

**Reviewed 2026-07-18 · PR https://github.com/jmgirard/cairn/pull/77 · branch `m79-references-content-check` @ bfdb7c5.**

### Acceptance-criteria evidence

- **AC1** — `test_scripts.TestReferencesCheck`, 13/13 ok. Three dedicated
  cases fire one condition each and assert the emitted text:
  `test_missing_provenance_block_fails` → "has no provenance block",
  `test_missing_ingested_date_fails` → "provenance names no ingested date",
  `test_missing_source_pointer_fails` → "provenance names no source pointer".
  Severity is hard CHECK per M79-D1: each case asserts `returncode == 1` and
  `FAIL  references index<->disk`. The emitted label is used verbatim
  wherever prose names it (M64).
- **AC2** — proven differentially, not by assertion alone. The same nested
  fixture was run against `main`'s `check_references` and this branch's:
  pre-M79 returned no findings (the page passed); post-M79 returns
  `cairn/references/topic/nested.md has no provenance block`. Pinned by
  `test_nested_page_is_enforced` + `test_nested_page_with_index_line_passes`.
- **AC3** — same differential method. A `references/` dir holding one page and
  no `INDEX.md`: pre-M79 no findings (rendered PASS); post-M79
  `cairn/references/ holds 1 page(s) but no INDEX.md`. The M45 no-op is kept
  where it is a genuine not-adopted signal, pinned by
  `test_absent_index_over_empty_dir_no_ops` (still PASS, scaffold-present
  owns the failure).
- **AC4** — `test_decorated_provenance_variants_pass` subtests four forms:
  `**bold**`, `__underscored__`, a bare heading with a bolded date and a
  markdown-linked pointer, and a blockquoted heading with a backticked date.
  All PASS. Implementation note found during work: `\b` is the wrong boundary
  because `_` is a word character in Python regex, so the parser uses
  non-alphanumeric lookarounds.
- **AC5** — `cairn_validate` on this repo: `PASS  references index<->disk`
  over all 16 committed pages, unmodified. No page needed a D-045 in-place
  correction; nothing is grandfathered.
- **AC6** — the shared `Tree.build()` fixture ships an empty INDEX and no
  pages, so it stays valid under the stricter check; a module-level `page()`
  helper supplies the provenance block to the dedicated fixtures. Full
  `scripts/tests` suite 123 ok, up from 111.
- **AC7** — run from the repo root, each exit code read explicitly, not
  tail-piped: `skills/tests` 324 exit 0 · `scripts/tests` 123 exit 0 ·
  `hooks/tests` 72 exit 0.
- **AC8** — second clause verified: `test_scaffold_check.TestGitignoreDeprecation`,
  4/4 ok — a repo carrying only the legacy entry passes `check_scaffold`, WARNs
  with the successor name, and a migrated or both-entries repo is silent.
  **First clause fails as written** — see the send-back note below.

### Consistency gate

- `cairn_validate` exit 0 — every CHECK PASS. One advisory: `sizing (split
  tripwires)` WARNs that M79 carries 8 acceptance criteria (>7), accepted
  deliberately at the amendment gate and exit-code neutral.
- Profile `generic`: the `consistency-gate` slot names no toolchain checks —
  clean no-op.
- `DESIGN.md` is untouched by the diff (no IPn/GPn changed), so
  `cairn_impact --changed` does not apply.
- `test_mutation_harness` 9/9 ok — `test_source_note_template` stays
  registered and its guards still fail under mutation; the M79 edit changed an
  existing assertion's string rather than adding one, so no new registration
  is owed.
- No CI is configured on this repo (`gh pr checks 77` → "no checks reported"),
  so the three verify suites are the whole mechanical gate.

### Independent review — three lenses + scorer

**[S] blame-history: no findings.** Traced M57 (`b5a57cd`, the F1/85
decoration fix), M24 (`707c684`, the `pdf/` gitignore entry) and M60
(`ab4cdef`, the pending marker). Confirmed the M45 no-op narrowing is the
planned AC3/T3 supersede with the genuine not-adopted case preserved, the
decoration capture is strictly more permissive than M57's, `DECISIONS.md` is a
pure append, and the milestone file's history sections are append-only.

**[S] prior-PR-comments: no findings.** No inline GitHub review comments exist
on this repo's merged PRs; the lens fell back to the `## Review` sections of
`milestones/archive/`. Every prior lesson touching these files is complied
with, not regressed — M57 F1/85, M78 F1/87 and F3/90, M24's shared-fixture
rule. It also found that the `\b`-vs-`_` regex trap is **already recorded** in
`LESSONS.md` from M60, so it is not a new lesson to capture at hygiene.

**[O] diff-bug: five findings, all scored ≥80 by the [S] scorer, all fixed on
the branch.** Nothing scored below threshold, so nothing was excluded. Each
was reproduced against the shipped code before and after the fix.

- **F1 (80) — orphaned rationale comment.** `check_gitignore_deprecations` was
  inserted between the M77-review-F1 comment explaining `_LOG_ENTRY` and
  `_LOG_ENTRY` itself, misdocumenting one function and stripping the other's
  explanation. *Fixed:* function relocated above the comment block.
- **F2 (95) — decoy heading swallowed the block.** `_provenance_block`
  committed to the first heading-like line with no fallback, so a `## Provenance`
  section heading above a textbook-correct block hard-FAILed the page.
  *Fixed:* every provenance-headed run is collected, not just the first.
- **F3 (92) — label on its own line lost its body.** The run ended at the
  first blank line, so `**Provenance.**\n\nIngested … from …` failed on both
  fields. *Fixed:* a run carrying neither field pulls in the next paragraph.
- **F4 (90) — the literal token `from` was required.** M78's template
  sanctions "the URL plus how it was retrieved and by whom" for a non-PDF
  source, so a template-compliant page hard-FAILed. The AC4 fixtures varied
  decoration only, never phrasing, so they passed vacuously here. *Fixed:*
  the pointer test accepts an attribution verb (from/via/retrieved/downloaded/
  accessed/source) or a bare URL/path locator, with a new fixture varying
  phrasing.
- **F5 (85) — widened INDEX capture admitted non-entries.** A "see also"
  prose bullet beginning with a path became a phantom catalog entry and a
  spurious FAIL; worse, a `..` path was joined unnormalized, so a real file
  *outside* `cairn/references/` silently satisfied a catalog entry (verified:
  the check returned PASS). *Fixed:* a new `_catalog_entries` drops any entry
  resolving outside the references tree or naming a directory that does not
  exist under it.

F2, F3 and F4 are the false-positive class M79-D1 explicitly promised to
absorb in the parser rather than the severity — the decision's own remedy
clause ("if a semantically sound page ever fails, fix the parser") is what was
applied, so the hard-CHECK severity stands unchanged.

Post-fix re-verify: `skills/tests` 324 exit 0 · `scripts/tests` 128 exit 0 ·
`hooks/tests` 72 exit 0 · `cairn_validate` exit 0.

### Note for the approval gate — AC8's first clause

AC8 requires "no live `references/pdf` string left in the plugin outside
history", and the deprecation path the same criterion mandates necessarily
keeps that string in code: `cairn_scripts.DEPRECATED_GITIGNORE`,
`cairn_validate._reference_pages`'s shelf-skip list, and the deprecation
test's docstring. None is a history file. Both independent lenses that
examined the question read the clause as satisfied ("the only surviving
occurrences are … test fixtures that intentionally exercise the legacy
string"); the criterion was written at the amendment gate before the
deprecation path was designed, which is what created the tension. Recorded
rather than resolved review-side — the criterion's wording is plan-owned and
was put to the user at the merge gate.
