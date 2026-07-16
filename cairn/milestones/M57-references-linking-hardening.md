# M57: references/ + linking hardening — synthesis notes, INDEX lint, dangling-ID advisory

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m57-references-linking-hardening · https://github.com/jmgirard/cairn/pull/55   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Execute M56's three adopted dispositions (references/llm-wiki.md ledger):
name the synthesis-note page type in the file map, mechanize an INDEX↔disk
references check, and add an FP-tolerant dangling M/D-token advisory.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** (1) widen the tracking-rules file-map `cairn/references/` entry and
the Source-ingestion section to name synthesis notes (cross-source analyses
like competitive-landscape.md) as the second committed page type beside
source notes; (2) a new hard `cairn_validate` CHECK — every committed
`cairn/references/*.md` has an INDEX.md line and every INDEX line's target
exists (sibling of `check_orphans`); (3) a new WARN-tier ADVISORY (M44
two-tier architecture) scanning committed `cairn/**/*.md` (excluding
`legacy/`, D-005) for `M<NN>`/`D-<NNN>` tokens resolving to no ROADMAP row,
milestone file, or D-entry — tolerant of the two M56 hazard classes
(repo-qualified cross-repo cites; example/forward prose like M99), per the
D-023 missed-format-beats-false-positive doctrine.

**Out:** governed-LLM-Wiki README positioning → public-release-prep
candidate (absorbed there by M56); IP/GP-token tracing → already shipped
(`cairn_impact`, M15/M17), unchanged; `[[wikilinks]]`, a references
`log.md`, a formal query op, graph tooling → rejected with reasons in M56
(references/llm-wiki.md), not deferred.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: the tracking-rules file map names both committed `references/`
      page types — source notes (`<citekey>.md`) and synthesis notes —
      locked by a mutation-registered prose guard (M53).
- [x] AC2: `cairn_validate` FAILs a committed references note with no INDEX
      line AND an INDEX line pointing to a missing file (fixture-proven,
      both directions), PASSes when INDEX↔disk agree; registered in `CHECKS`.
- [x] AC3: on a fixture with a gapped known-ID set, a bare unresolvable
      `M<NN>` or `D-<NNN>` token yields a WARN; registered in `ADVISORIES`
      (exit-code-neutral).
- [x] AC4: fixtures prove both M56 hazard classes stay silent — an
      above-max example/forward token (the M99 class) and a repo-qualified
      cross-repo cite (the "ackwards M57" class, references/llm-wiki.md).
- [x] AC5: full `cairn_validate` on this repo's tree at review: all CHECKS
      (existing + new) PASS and zero advisory WARNs — the zero-noise bar.
- [x] AC6: the profile `verify` slot clean — all three unittest suites green
      from the repo root, exit-code-gated (M56 lesson: no `| tail`).

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: widen the file-map `references/` row + Source-ingestion section in
      `tracking-rules.md` to name synthesis notes; prose guard with its own
      `Mutation(...)` entry (M53/M54), single-line anchors (M23/M26).
- [x] T2: implement `check_references` in `scripts/cairn_validate.py`
      (top-level committed `*.md` only; skips `INDEX.md` itself; `pdf/` is
      gitignored) + register in `CHECKS`; dedicated fixture-builder tests
      (M34/M45 pattern) for orphan-note / missing-target / agreement; keep
      the shared `Tree.build()` valid for the new check (M24).
- [x] T3: implement `check_dangling_ids`: known-ID set = ROADMAP row IDs ∪
      live/archive milestone-file IDs ∪ `### D-NNN` headers; scan
      `\bM\d{2,}\b` / `\bD-\d{3}\b` over committed `cairn/**/*.md` minus
      `legacy/`; register in `ADVISORIES`.
- [x] T4: tolerance heuristics + hazard fixtures: skip tokens numerically
      above the repo's max assigned ID (M99 class); skip repo-qualified
      cites (qualifier heuristic — exact shape is implement's; the fixtures
      pin behavior, D-023: prefer a miss over an FP).
- [x] T5: live-tree run — full validate PASS + zero WARNs; all three suites
      from the repo root; log the M57 self-resolution quirk (once this file
      exists, the live "ackwards M57" tokens resolve locally — the fixture
      carries the hazard case regardless).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan (promotes the "references/ +
  linking hardening" candidate, M56 dispositions).
- 2026-07-16: in-progress; branch cut. Gate: tolerance = above-max + slug
  check (both rules named, per-class fixtures).
- 2026-07-16: T1 done — file map + ingestion name synthesis notes; README
  tree comment updated (repo-wide sweep, M48); guard + 3 Mutation entries;
  3 suites green.
- 2026-07-16: T2 done — `check_references` in CHECKS (no-ops sans INDEX.md,
  M45 pattern); 4 fixture tests both directions + agreement + independence;
  live tree passes (INDEX already accurate).
- 2026-07-16: T3+T4 done (tolerance rules folded into T3's function — a few
  lines each, M46 fold-don't-defer; T4 = the 5 fixtures). Gate-chosen
  same-line slug rule is deliberately loose (skips path-bearing lines too —
  preferred miss, D-023). Gapped-set fixtures via archived M05 + gap M04.
- 2026-07-16: T5 done — live tree 15/15 PASS + zero WARNs; 3 suites green
  from repo root. Quirk logged: live "ackwards M57" now self-resolves (this
  milestone took M57), M99 skips via above-max; fixtures carry both hazard
  classes independently. Status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->

**Evidence (2026-07-16, fresh, by command):**

- AC1: `test_references_pages` 3/3 OK (file map both types, ingestion
  definition, page⇒INDEX-line rule); mutation harness 9/9 OK — all three
  new `Mutation(...)` entries driven (blank ⇒ guard fails), completeness
  meta-test covers the new file.
- AC2: `TestReferencesCheck` 4/4 OK — orphan-note FAIL, missing-target
  FAIL, agreement PASS, absent-INDEX independence (references check PASS
  while scaffold FAILs); registered in CHECKS.
- AC3: `TestDanglingIds::test_true_dangler_warns_but_stays_exit_neutral` OK
  (gapped set M05/gap-M04: bare M04 WARNs, exit 0) +
  `test_d_token_dangler_warns` OK (D-002 gap WARNs); registered in
  ADVISORIES.
- AC4: `test_above_max_example_token_is_silent` OK (M99 class) +
  `test_repo_qualified_cite_is_silent` OK (slug class, gapped M04);
  `test_legacy_is_excluded` OK (D-005).
- AC5: live-tree `cairn_validate`: 15/15 CHECKS PASS (references
  index<->disk among them), advisories 2/2 OK — zero WARNs.
- AC6: three suites green from repo root, exit-code-gated: skills 156,
  scripts 82, hooks 32.

**Consistency gate:** `cairn_validate` exit 0 (above); coverage complete
(mechanical check PASS; map read: AC1→T1, AC2→T2, AC3→T3, AC4→T4,
AC5/AC6→T5, all tasks present); no IPn/GPn text changed → `cairn_impact`
skipped; `generic` profile consistency-gate slot: none (clean no-op).

**Independent review (3 lenses + scorer):** diff-bug [O] — 1 finding;
blame-history [S] — none (additive diff, M44/M45/M53/D-005/D-023 intents
preserved); prior-PR [S] — no-op (53 merged PRs touching these files, zero
inline comments). Sub-80 findings: none. Triage:
- F1 (85, fixed): `_INDEX_LINE` captured markdown decoration
  (`` `notes.md` ``, `[name](name)`) so a correct decorated INDEX entry
  double-FAILed the hard CHECK — the D-023 cry-wolf class. Fixed: capture
  excludes decoration chars; regression test `test_decorated_index_lines_pass`.
  Post-fix: 3 suites green (scripts now 83), live tree 15/15 + zero WARNs.
