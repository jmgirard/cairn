# M57: references/ + linking hardening — synthesis notes, INDEX lint, dangling-ID advisory

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m57-references-linking-hardening   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] AC1: the tracking-rules file map names both committed `references/`
      page types — source notes (`<citekey>.md`) and synthesis notes —
      locked by a mutation-registered prose guard (M53).
- [ ] AC2: `cairn_validate` FAILs a committed references note with no INDEX
      line AND an INDEX line pointing to a missing file (fixture-proven,
      both directions), PASSes when INDEX↔disk agree; registered in `CHECKS`.
- [ ] AC3: on a fixture with a gapped known-ID set, a bare unresolvable
      `M<NN>` or `D-<NNN>` token yields a WARN; registered in `ADVISORIES`
      (exit-code-neutral).
- [ ] AC4: fixtures prove both M56 hazard classes stay silent — an
      above-max example/forward token (the M99 class) and a repo-qualified
      cross-repo cite (the "ackwards M57" class, references/llm-wiki.md).
- [ ] AC5: full `cairn_validate` on this repo's tree at review: all CHECKS
      (existing + new) PASS and zero advisory WARNs — the zero-noise bar.
- [ ] AC6: the profile `verify` slot clean — all three unittest suites green
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
- [ ] T2: implement `check_references` in `scripts/cairn_validate.py`
      (top-level committed `*.md` only; skips `INDEX.md` itself; `pdf/` is
      gitignored) + register in `CHECKS`; dedicated fixture-builder tests
      (M34/M45 pattern) for orphan-note / missing-target / agreement; keep
      the shared `Tree.build()` valid for the new check (M24).
- [ ] T3: implement `check_dangling_ids`: known-ID set = ROADMAP row IDs ∪
      live/archive milestone-file IDs ∪ `### D-NNN` headers; scan
      `\bM\d{2,}\b` / `\bD-\d{3}\b` over committed `cairn/**/*.md` minus
      `legacy/`; register in `ADVISORIES`.
- [ ] T4: tolerance heuristics + hazard fixtures: skip tokens numerically
      above the repo's max assigned ID (M99 class); skip repo-qualified
      cites (qualifier heuristic — exact shape is implement's; the fixtures
      pin behavior, D-023: prefer a miss over an FP).
- [ ] T5: live-tree run — full validate PASS + zero WARNs; all three suites
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

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->
