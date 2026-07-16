<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M62: Release docs — LICENSE, README worked example + framing, DRAFT removal

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M61   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m62-release-docs · https://github.com/jmgirard/cairn/pull/60   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make the repo publicly presentable for v1.0: MIT LICENSE, a README with a
worked example and the governed-LLM-Wiki framing, and DRAFT_2.md removed.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- `LICENSE` (MIT) at the repo root (DRAFT_2 §11 step 4).
- README worked example: one milestone walked end-to-end (idea →
  plan gate → implement → review → merge chip), short and concrete.
- README intro adopts the governed-LLM-Wiki framing (M56 verdict,
  `references/llm-wiki.md` — "a governed LLM Wiki for project state").
- Tighten the human-facing "what cairn does without asking" surface (RR01
  §10.5): the existing "expects from you" / "does NOT do" sections gain the
  missing pieces — chips are stops, merges need explicit approval, and how
  to bail out (pause/drop a milestone, uninstall).
- Remove `DRAFT_2.md`; repo-wide sweep for references (README Status ¶
  cites it today) — history files exempt (DECISIONS/CHANGELOG/legacy/
  reviews archive only — M58 lesson); reword the README status paragraph
  off "piloting"/DRAFT framing.
- Depends on M61 so the README documents the shipped env check and dry-run
  honestly.

**Out:** version bump, CHANGELOG consolidation, and the v1.0 tag →
`/cairn-release` run after this merges (generic release-walk); marketplace
promotion beyond what D-007 already ships → post-1.0, stays with D-007;
external de-risking → M61.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] `LICENSE` exists at the repo root containing the MIT license text
      with the correct holder and year.
- [x] README contains a worked example section walking one milestone
      end-to-end through the three gates.
- [x] README intro carries the governed-LLM-Wiki framing traceable to
      `references/llm-wiki.md`; `test_positioning_guard.py` (extended)
      stays green.
- [x] README states what cairn does and won't do without asking, including
      an explicit bail-out path (RR01 §10.5).
- [x] `DRAFT_2.md` is deleted and `git grep -i draft_2` over live files
      returns only history-file hits (DECISIONS/CHANGELOG/legacy/reviews
      archive/milestone archives) and tracking lines recording this
      removal (the M62 file, the ROADMAP lineage citation).
- [x] Verify clean: both unittest suites green from the repo root; any
      new/extended prose-guards mutation-registered.

## Coverage
<!-- owner: plan · create/amend-via-gate; AC/Task counted top-to-bottom -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Add the MIT `LICENSE` (holder: Jeffrey Girard, year 2026).
- [x] T2: Write the README worked-example section (one milestone,
      three gates, chip-driven flow).
- [x] T3: Weave the governed-LLM-Wiki framing into the README intro;
      extend `skills/tests/test_positioning_guard.py` so the framing and
      the existing language-agnostic positioning are both locked.
- [x] T4: Tighten the "without asking" surface + bail-out story in the
      README's expectations/non-goals sections.
- [x] T5: Delete `DRAFT_2.md`; repo-wide `git grep` sweep (M48/M58
      lessons — exempt history files only); reword the README status
      paragraph.
- [x] T6: Mutation-register new guard blocks; run both suites from the
      repo root.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan (carved from the "Public release
  prep" candidate row with M61; v1.0 tag stays a /cairn-release run).
- 2026-07-16: implement started; branch m62-release-docs.
- 2026-07-16: gate: AC5 amended (exempt milestone archives + tracking lines
  recording the removal — the grep otherwise hits its own record); worked
  example = fictional generic repo; status ¶ drops version claims (points at
  CHANGELOG); DRAFT_2 disposition = skim, port true gaps only, drop the
  DESIGN.md "content moves here" promise sentence.
- 2026-07-16: T1 done — MIT LICENSE at root (Jeffrey Girard, 2026).
- 2026-07-16: T2 done — worked example (fictional CLI --dry-run milestone,
  three gates, chips) added after "The core loop".
- 2026-07-16: T3 done — LLM-Wiki framing in README ¶1; new
  test_readme_carries_the_llm_wiki_framing guard; skills suite 185 OK.
- 2026-07-16: T4 done — chips-are-stops bullet, merge-guard-backed
  approval wording, no-lock-in bail-out bullet (pause/drop/uninstall).
- 2026-07-16: T5 done — DRAFT_2.md deleted; skim found one true gap, ported
  to DESIGN Conventions (repos never pin plugin versions; breaking
  state-format changes ship with /cairn-init migration handling); DESIGN
  promise sentence + README status ¶/piloting framing reworded; sweep
  clean bar the AC5-exempt tracking lines.
- 2026-07-16: T6 done — two Mutation entries for the LLM-Wiki framing
  guard; skills (185) + scripts suites OK from repo root; validate passes.
  All tasks complete → status review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive; EXEMPT from the 150-line cap (M55) -->

Evidence gathered fresh 2026-07-16 on m62-release-docs (PR #60):

- AC1: LICENSE present at root; MIT grant text; "Copyright (c) 2026
  Jeffrey Girard".
- AC2: `## A worked example` at README:77; three numbered gate steps
  (plan / build / ship) walking one milestone end-to-end.
- AC3: framing line at README:7 ("governed LLM Wiki for project state —
  the agent maintains it, you gate it"); test_positioning_guard OK
  including the new test_readme_carries_the_llm_wiki_framing.
- AC4: chips-are-stops bullet (README:147), guard-backed merge approval
  (README:151), no-lock-in bail-out pause/drop/uninstall (README:182).
- AC5: DRAFT_2.md absent; `git grep -li draft_2` hits only history files
  (CHANGELOG, DECISIONS, milestone/reviews archives) plus the two
  exempted tracking lines (ROADMAP lineage citation, this file) per the
  gated 2026-07-16 amendment.
- AC6: skills suite 185 OK + scripts suite OK from repo root; two
  Mutation entries registered for the new framing guard.
- Consistency gate: cairn_validate exit 0 (15 PASS, 2 OK advisories);
  generic profile consistency-gate slot names no toolchain checks; no
  IPn/GPn change → cairn_impact skipped.
