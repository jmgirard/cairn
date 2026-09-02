# M171: Chapter markers follow stretches, not phases

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Branch/PR:** m171-per-stretch-chapters · https://github.com/jmgirard/cairn/pull/174

## Goal

Make the navigable TOC useful in a session that holds one phase: chapters
mark the stretches inside a phase (tasks, criteria, gate steps), and the
H1/H2 phase header re-emits at every session start.

## Scope

Surface tier: user-facing — skill conduct rules are what an adopting
repo's operator runs under.

**In:** the tracking-rules "Chapter markers" rule moves from a per-phase
cadence (D-021) to a per-stretch one, each phase skill's `Chapter markers:`
directive names its own stretches, chapter titles carry the positional
label (M169) where the stretch is a task or criterion, and the "Phase
header" rule says the `#`/`##` pair is emitted at each session start
(a post-`/clear` session included). The hand-run guard
`skills/tests/test_chapter_marker_mandate.py` is retargeted to pin the
per-skill stretch lists and the rulebook's clauses; a D-entry supersedes
D-021's cadence and annotates D-020 and D-027 item (1).

**Out:** marking the session's opening message as a chapter — D-027 item
(1) rejected it on M31's evidence and the gate kept that rejection; a live
re-probe of the TOC mechanism (`cairn/references/desktop-toc-mechanism.md`
notes one is owed) — not needed here, since the user's report that a
single-phase session shows no chapters is the observed behaviour this plan
answers; any change to chip or close-block shape (D-124).

## Acceptance criteria

- [x] AC1: The tracking-rules "Chapter markers" rule states (a) a chapter
      is marked at each phase transition and at each stretch boundary a
      skill's `Chapter markers:` directive names, (b) the session-start-
      implicit carve-out stays, and (c) a chapter's title opens with the
      item's positional label (`Tn:` / `ACn:`) where the stretch is a task
      or criterion, and is a short noun phrase otherwise.
- [x] AC2: Each of the nine phase skills' `Chapter markers:` directive
      names that skill's stretches, this set and no other: plan —
      investigation, question gate, solidify-and-commit; implement — the
      question gate, each task, each plan amendment; review — each
      acceptance criterion in step 3, then the consistency gate, the
      independent review, the approval gate, post-merge hygiene; hotfix
      and cairn-release — each numbered step; milestone-brief, cairn-init,
      milestone, design-interview — each phase its `Phase header:`
      directive names.
- [x] AC3: The tracking-rules "Phase header" rule's bullet states that the
      `#`/`##` pair is emitted at each session start before the first
      delta, a post-`/clear` session included.
- [x] AC4: A D-entry supersedes D-021's per-phase cadence, annotates D-020
      and D-027 item (1), states the per-stretch cadence and the
      session-start re-emit, and names a falsifier.
- [x] AC5: Both gating suites (`python3 -m unittest discover -s
      scripts/tests`; `python3 -m unittest discover -s hooks/tests`) exit 0
      from the repo root.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T1
- AC4 → T4
- AC5 → T3, T4

## Tasks

- [x] T1: Rulebook (`skills/shared/tracking-rules.md`, "Output &
      interaction discipline"): rewrite the "Chapter markers" bullet to the
      per-stretch mandate with the carve-out and title-shape clauses (AC1),
      and add the session-start re-emit clause to the "Phase header" bullet
      (AC3). Keep the phrase "mark a chapter at each phase transition" so
      the mutation-harness block still matches or update that entry in T3.
- [x] T2: Rewrite the nine `Chapter markers:` directives (`skills/*/SKILL.md`,
      the line after `Phase header:`) to name each skill's stretches per
      AC2's list. Sweep README, templates, and DESIGN.md for the old
      per-phase-only phrasing (`grep -rn "each phase transition"`) and
      update any restatement (lesson M112).
- [x] T3: Retarget `skills/tests/test_chapter_marker_mandate.py`: pin the
      rulebook's three AC1 clauses and, per skill, a stretch token from its
      directive (nine entries replace the shared `DIRECTIVE_TOKEN`); update
      the `test_mutation_harness.py` entry near line 272 to the new block.
      Hand-run `python3 -m unittest discover -s skills/tests` (D-109; lesson
      M148 — guard pins near edited prose) and record the result in the work
      log; run both gating suites (lesson: any `skills/*/SKILL.md` edit runs
      them).
- [x] T4: Append the D-entry (AC4) with a durable-record preview; run
      `python3 scripts/cairn_validate.py` and both gating suites, each exit
      code checked explicitly.

## Work log

- 2026-09-02: created by /milestone-plan.
- 2026-09-02: criteria audit ran in full mode ([O] fresh reader, user-facing tier); returned 10 findings — 8 fixed at the gate (guard/validator clauses moved to tasks per D-118/D-120; `skills/tests` dropped from AC5 per D-109; cairn-release given "each numbered step"; implement stretches gained the gate and amendments; AC1 clauses enumerated and non-task titles freed; AC3's grep window replaced by a prose location; AC4 now requires content and a falsifier and annotates rather than supersedes D-027), 2 posed as gate questions (review grain; session-start chapter).
- 2026-09-02: plan gate chose per-criterion review chapters (then per later step) over one chapter per numbered step because the evidence run is the bulk of a review session and criteria are where a reader navigates; falsified by review sessions whose TOC exceeds what the runtime renders usefully (observed clutter, not a count).
- 2026-09-02: plan gate chose positional-label titles (`T3: …`, `AC2: …`) over free noun phrases because M169's labels let the TOC read against the milestone file; falsified by titles the runtime truncates past the label.
- 2026-09-02: plan gate chose keeping the session-start-implicit carve-out over marking the opening phase because the runtime supplies a "Session Start" node and its docs discourage first-message marking (M31, D-027); falsified by a live probe showing no implicit node.
- 2026-09-02: plan gate chose retargeting the hand-run guard per skill over deleting it because the guard stays ungated (D-109) and per-skill tokens are what AC2 promises; falsified by the guard needing re-seeding on every wording edit.
- 2026-09-02: implement started on m171-per-stretch-chapters (cut from origin/main at 0e8adba); question gate skipped — the plan gate settled every open choice. T1 done: rulebook "Chapter markers" bullet now the per-stretch mandate (phase transitions plus directive-named stretches, session start implicit, `Tn:`/`ACn:` title shape); "Phase header" bullet gained the session-start re-emit clause; both gating suites exit 0.
- 2026-09-02: T2 done: nine `Chapter markers:` directives rewritten to name each skill's stretches per AC2; sweep (`grep -rn "each phase transition"` over README, templates, DESIGN.md, shared modules) found no restatement outside the rulebook and the skills; both gating suites exit 0.
- 2026-09-02: T3 done: `test_chapter_marker_mandate.py` retargeted — nine per-skill stretch tokens replace the shared `DIRECTIVE_TOKEN`, four rulebook asserts pin AC1 (a)(b)(c) and AC3, each registered in the mutation harness; hand-run `skills/tests` 587 tests OK (exit 0), discrimination checked by blanking a skill token and a rulebook clause (guard red both times); both gating suites exit 0.
- 2026-09-02: T4 done: D-129 appended (supersedes D-021's cadence, annotates D-020 and D-027 item (1), names the falsifier); `cairn_validate` all checks passed (exit 0); both gating suites exit 0; hand-run `skills/tests` exit 0. All tasks checked — status → review.

## Decisions

## Review

- 2026-09-02 AC1: read `skills/shared/tracking-rules.md` "Chapter markers (per-stretch mandate)" bullet (lines 356–360 at 43c06c4): (a) marks at each phase transition and at each stretch boundary the skill's `Chapter markers:` directive names; (b) "(session start implicit)" carve-out present; (c) title opens with `Tn:`/`ACn:` for a task or criterion, short noun phrase otherwise. PASS.
- 2026-09-02 AC2: grepped `Chapter markers:` in all nine `skills/*/SKILL.md`: plan names investigation, the question gate, solidify-and-commit; implement names the question gate, each task, each plan amendment; review names each acceptance criterion in step 3, then the consistency gate, the independent review, the approval gate, post-merge hygiene; hotfix and cairn-release name each numbered step; milestone-brief, cairn-init, milestone, design-interview name each phase their `Phase header:` directive names. No directive names any other stretch. PASS.
- 2026-09-02 AC3: read the "Phase header" bullet (`skills/shared/tracking-rules.md` lines 296–300): "The `#`/`##` pair is emitted at each session start, before the first delta — a post-`/clear` session included." PASS.
- 2026-09-02 AC4: `cairn/DECISIONS.md` D-129 (line 4727) heading names "supersedes D-021's per-phase cadence, annotates D-020 and D-027 item (1)"; the Decision paragraph states the per-stretch cadence (the nine skills' stretches) and the session-start re-emit; Consequences names the falsifier (a TOC the runtime renders unusably, or a live probe showing no implicit "Session Start" node). PASS.
- 2026-09-02 AC5: from the repo root, `python3 -m unittest discover -s scripts/tests` — 329 tests OK, exit 0; `python3 -m unittest discover -s hooks/tests` — 121 tests OK, exit 0. Hand-run `skills/tests` (non-gating, D-109) — 587 tests OK, exit 0. PASS.
- 2026-09-02 consistency gate: `cairn_validate.py` all checks passed (exit 0; `release window` advisory OK). Principles touched `—` → `cairn_impact --changed` skipped. Profile `generic` consistency-gate slot names no toolchain checks → no-op. Driving RR `—` → projection-vs-outcome no-op. Diff touches `skills/tests/*.py` (executable surface) and the tier is user-facing → full three-lens review.
- 2026-09-02 independent review: three fresh-context lenses ([O] diff-bug, [S] blame-history, [S] prior-review-record; the prior-review lens found archive evidence, GitHub probe empty). Findings, ranked by the reporting lens, and their disposition:
  - F1 [O]: the per-skill guard pinned only the head of each stretch list — blanking implement's "each plan amendment" or review's four later stretches left the guard green, so six of AC2's ten stretches were unpinned. Fix now: tokens widened to each skill's full list; discrimination re-checked in memory (both drops red).
  - F2 [O][S][S]: four tokens embedded a hard newline, pinning the SKILL.md line wrap rather than the prose (M23 lesson, restated in the file's own docstring). Fix now: the guard collapses whitespace on read; the docstring names this as a deliberate exception to the one-line convention.
  - F3 [O]: the guard's comments claimed one-physical-line matching the tokens contradicted. Fix now: comments rewritten with F2.
  - F4 [O]: the nine-skill scope (D-021 sub-choice 3, kept by D-129) was implicit in a dict literal. Fix now: `test_all_nine_phase_skills_are_pinned` asserts the count.
  - F5 [O]: mutation-registry comment said "one entry per rulebook assert" for four entries covering eight asserts (the M94 F8 overclaim shape). Fix now: comment says one per test method, by-hand check for the rest.
  - F6 [O][S]: the per-skill stretch test has no mutation-harness registration. Rejected: pre-existing gap the old shared-token test carried too, the suite is non-gating (D-109), and the by-hand discrimination check above is the M53 escape hatch.
  - F7 [O]: `at each stretch boundary the` pinned a wrap-dependent trailing article. Fix now: trailing "the" dropped.
  - F8 [O]: hotfix and cairn-release directives say "each phase transition and at each numbered step" though their phases are the steps. Rejected: the shared opening is what `DIRECTIVE_OPENING` pins across all nine; harmless redundancy AC2 does not forbid.
  - F9 [O]: D-129 says "the evidence step" where AC2 and the review skill say "step 3". Rejected: same referent, and the D-entry is append-only (IP4).
  - Return floor: no finding demonstrates a criterion failing (AC2 is about the directives, which all three lenses confirm match; the guard is T3's deliverable) — no status change. After fixes: hand-run `skills/tests` 588 OK exit 0; gating suites re-run below.
- 2026-09-02 post-fix re-verification: `scripts/tests` exit 0, `hooks/tests` exit 0, hand-run `skills/tests` 588 OK exit 0 — AC5 evidence holds after the gate fixes.
