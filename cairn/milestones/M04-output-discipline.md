# M04: Skill conduct & output discipline

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** —
- **Branch/PR:** m04-output-discipline

## Goal

Encode the pilot-validated conduct findings — stage orientation, delta
reporting, outcome-first recaps, plain-language contextual chips — in the
rulebook and every skill, so cairn's output orients the user instead of
dumping mechanics.

## Scope

**In:** a new "Output & interaction discipline" section in
`skills/shared/tracking-rules.md` (single source of conduct rules); a
stage-banner convention instructed by all eight skills; hardcoded routing
chip menus recast as contextual construction with the fixed menus as
examples; outcome-first recap guidance at phase completions; [S]/[O]/[F]
model prefixes on spawned-subagent descriptions.

**Out:** rule *content* changes (adopt-in-place, RB tripwires, ID
conventions) → M05; plugin hooks for guardrail feedback → candidate;
skill-less routing guardrails (claude-md-section router) → candidate;
README install docs → release-prep candidate.

## Acceptance criteria

- [ ] `tracking-rules.md` has an output-discipline section covering: stage
      banners, delta-not-dump reporting between gates, outcome-first
      recaps (substance before hygiene mechanics), chip weight caps with
      plain-language option text (technical detail in chat above the
      chip), contextual chip construction (options composed from session
      findings; invariants fixed: recommended-first, ≤4 options, Stop
      present, never auto-proceed), chapter markers where the harness
      supports them. Evidence: file read.
- [ ] All eight SKILL.md files instruct the stage banner
      (`[cairn · <skill> · M<NN> · <phase>]`), consistently formatted.
      Evidence: grep across `skills/*/SKILL.md`.
- [ ] No skill presents a hardcoded chip menu as mandatory; fixed menus
      read as examples and contextual composition is licensed (the
      `/milestone` "single most sensible next action, e.g." phrasing is
      the model). Evidence: read of every `Routing chip` passage.
- [ ] Skills that spawn subagents (milestone-implement, milestone-review,
      milestone-brief) instruct the [S]/[O]/[F] description prefix, and
      the rulebook model-strategy section states the rule. Evidence: grep.
- [ ] Weight caps hold after edits (tracking-rules stays one coherent
      rulebook; no skill contradicts the new section). Evidence: caps
      check + coherence read in review.

## Tasks

- [x] Draft the "Output & interaction discipline" section in
      `skills/shared/tracking-rules.md` (banners, deltas, recaps, chip
      rules, contextual construction, chapter markers).
- [x] Add the stage-banner instruction to all eight `skills/*/SKILL.md`
      files (one consistent line each).
- [x] Recast hardcoded routing-chip menus (grep `Routing chip` — at least
      cairn-init:75,139 and milestone-brief) as contextual construction
      with examples; align with `/milestone`'s phrasing (milestone:60–69).
- [x] Add outcome-first recap guidance to the completion steps of
      milestone-implement (step 8), milestone-review (step 7/10), and
      cairn-release.
- [x] Add the [S]/[O]/[F] prefix rule to the rulebook model-strategy
      section and the three spawning skills.
- [ ] Coherence pass: reread rulebook + all skills for contradictions
      with the new section; verify caps.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. Lineage: M02/M03 pilot friction
  (candidate rows: output discipline & stage orientation; contextual chip
  construction; subagent title prefix — absorbed).
- 2026-07-11: implementation started on m04-output-discipline; question
  gate skipped — the plan pins format, placement, and file list; the only
  open choice (new rulebook section vs. folding into the chips section) is
  minor wording structure, resolved as a new section cross-referenced from
  the gates section.
- 2026-07-11: task 1 done — "Output & interaction discipline" section in
  tracking-rules (banners, deltas, outcome-first recaps, chip rules,
  contextual construction, chapters, [S]/[O]/[F]); gates-section chip
  paragraph now defers to it.
- 2026-07-11: task 2 done — banner line in all eight SKILL.md openings,
  each with its skill token and phase slot (grep-verified 8/8).
- 2026-07-11: task 3 done — six chip menus recast as contextual
  construction with e.g. menus (cairn-init ×2, brief, plan, implement,
  review); /milestone unchanged as the model.
- 2026-07-11: task 4 done — outcome-first clauses at implement step 8
  recap, review approval gate (step 7) + done recap (step 9), and the
  cairn-release handoff.
- 2026-07-11: task 5 done — tier-tag rule in model-strategy section;
  [S]/[O] at implement delegation, [O] at review step 5, [F] at brief
  spawn gate.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review -->
