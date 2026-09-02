# M171: Chapter markers follow stretches, not phases

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Branch/PR:** —

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

- [ ] AC1: The tracking-rules "Chapter markers" rule states (a) a chapter
      is marked at each phase transition and at each stretch boundary a
      skill's `Chapter markers:` directive names, (b) the session-start-
      implicit carve-out stays, and (c) a chapter's title opens with the
      item's positional label (`Tn:` / `ACn:`) where the stretch is a task
      or criterion, and is a short noun phrase otherwise.
- [ ] AC2: Each of the nine phase skills' `Chapter markers:` directive
      names that skill's stretches, this set and no other: plan —
      investigation, question gate, solidify-and-commit; implement — the
      question gate, each task, each plan amendment; review — each
      acceptance criterion in step 3, then the consistency gate, the
      independent review, the approval gate, post-merge hygiene; hotfix
      and cairn-release — each numbered step; milestone-brief, cairn-init,
      milestone, design-interview — each phase its `Phase header:`
      directive names.
- [ ] AC3: The tracking-rules "Phase header" rule's bullet states that the
      `#`/`##` pair is emitted at each session start before the first
      delta, a post-`/clear` session included.
- [ ] AC4: A D-entry supersedes D-021's per-phase cadence, annotates D-020
      and D-027 item (1), states the per-stretch cadence and the
      session-start re-emit, and names a falsifier.
- [ ] AC5: Both gating suites (`python3 -m unittest discover -s
      scripts/tests`; `python3 -m unittest discover -s hooks/tests`) exit 0
      from the repo root.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T1
- AC4 → T4
- AC5 → T3, T4

## Tasks

- [ ] T1: Rulebook (`skills/shared/tracking-rules.md`, "Output &
      interaction discipline"): rewrite the "Chapter markers" bullet to the
      per-stretch mandate with the carve-out and title-shape clauses (AC1),
      and add the session-start re-emit clause to the "Phase header" bullet
      (AC3). Keep the phrase "mark a chapter at each phase transition" so
      the mutation-harness block still matches or update that entry in T3.
- [ ] T2: Rewrite the nine `Chapter markers:` directives (`skills/*/SKILL.md`,
      the line after `Phase header:`) to name each skill's stretches per
      AC2's list. Sweep README, templates, and DESIGN.md for the old
      per-phase-only phrasing (`grep -rn "each phase transition"`) and
      update any restatement (lesson M112).
- [ ] T3: Retarget `skills/tests/test_chapter_marker_mandate.py`: pin the
      rulebook's three AC1 clauses and, per skill, a stretch token from its
      directive (nine entries replace the shared `DIRECTIVE_TOKEN`); update
      the `test_mutation_harness.py` entry near line 272 to the new block.
      Hand-run `python3 -m unittest discover -s skills/tests` (D-109; lesson
      M148 — guard pins near edited prose) and record the result in the work
      log; run both gating suites (lesson: any `skills/*/SKILL.md` edit runs
      them).
- [ ] T4: Append the D-entry (AC4) with a durable-record preview; run
      `python3 scripts/cairn_validate.py` and both gating suites, each exit
      code checked explicitly.

## Work log

- 2026-09-02: created by /milestone-plan.
- 2026-09-02: criteria audit ran in full mode ([O] fresh reader, user-facing tier); returned 10 findings — 8 fixed at the gate (guard/validator clauses moved to tasks per D-118/D-120; `skills/tests` dropped from AC5 per D-109; cairn-release given "each numbered step"; implement stretches gained the gate and amendments; AC1 clauses enumerated and non-task titles freed; AC3's grep window replaced by a prose location; AC4 now requires content and a falsifier and annotates rather than supersedes D-027), 2 posed as gate questions (review grain; session-start chapter).
- 2026-09-02: plan gate chose per-criterion review chapters (then per later step) over one chapter per numbered step because the evidence run is the bulk of a review session and criteria are where a reader navigates; falsified by review sessions whose TOC exceeds what the runtime renders usefully (observed clutter, not a count).
- 2026-09-02: plan gate chose positional-label titles (`T3: …`, `AC2: …`) over free noun phrases because M169's labels let the TOC read against the milestone file; falsified by titles the runtime truncates past the label.
- 2026-09-02: plan gate chose keeping the session-start-implicit carve-out over marking the opening phase because the runtime supplies a "Session Start" node and its docs discourage first-message marking (M31, D-027); falsified by a live probe showing no implicit node.
- 2026-09-02: plan gate chose retargeting the hand-run guard per skill over deleting it because the guard stays ungated (D-109) and per-skill tokens are what AC2 promises; falsified by the guard needing re-seeding on every wording edit.

## Decisions

## Review
