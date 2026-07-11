# M08: Skill-less routing guardrails

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- high | normal | low -->
- **Depends on:** —   <!-- M07 hooks already shipped; no hard dep -->
- **Branch/PR:** m08-skill-less-routing   <!-- PR URL once opened -->

## Goal

Turn the always-loaded CLAUDE.md cairn section into an imperative
classify-first router so plain conversation in a cairn repo gets routed to
the right tier/skill instead of bypassing the rulebook.

## Scope

**In:**
- Rewrite `skills/shared/templates/claude-md-section.md` from a passive
  description into an imperative classify-first router: classify every
  request first, apply the work tiers, never implement code on main outside
  a milestone branch, and get a skill to fire early so the full rulebook
  (`tracking-rules.md`) loads.
- Dogfood: update this repo's own top-level `CLAUDE.md` cairn section to the
  router form and keep it consistent with the template.
- A rubric checklist the router text must satisfy, plus ≥3 documented
  dry-run scenarios, recorded in this milestone file.

**Out:**
- Mechanical "no code commits on main" PreToolUse guard → `candidate` row
  (false-positive-prone; trivial edits are legitimately allowed on main;
  deserves its own design). Decided at plan gate 2026-07-11.
- Live empirical test of the router in openac → `candidate` row (openac is a
  separate repo and can't produce automated evidence here). Decided at plan
  gate 2026-07-11.
- Embedding full conduct (contextual chips, output discipline) into the
  router → not done: conduct stays in `tracking-rules.md`, loaded when a
  skill fires; the router's job is to make a skill fire, not to restate
  conduct (keeps the ~20-line cap). Decided at plan gate 2026-07-11.

## Acceptance criteria

- [ ] **Classify-first + tiers + never-on-main.** `claude-md-section.md`
      opens with an imperative to classify every request before acting, and
      names every tier→destination mapping: trivial (no runtime surface) →
      commit to main; user-visible bug → `/hotfix`; new work / design
      decision / more-than-a-sitting → `/milestone-plan`; status or unsure →
      `/milestone`. It states "never implement code on main outside a
      milestone branch." (Evidence: read/grep the template for each element.)
- [ ] **Delivery-path rule.** The router instructs that milestone-ish
      conversation must invoke the relevant skill so the full rulebook loads,
      and does NOT restate conduct itself — it points to the skills.
      (Evidence: the instruction is present; no chip/output-discipline prose
      is duplicated into the section.)
- [ ] **Within cap.** The template's section body stays within the weight
      cap (≤ ~25 lines, per the ~20-line guidance in the template header).
      (Evidence: `wc -l`.)
- [ ] **Dogfooded.** This repo's own `CLAUDE.md` cairn section is updated to
      the router form and is consistent with the template (same mappings,
      same never-on-main rule). (Evidence: read both; diff of intent.)
- [ ] **Rubric + dry-runs.** This milestone file's Review section records a
      rubric checklist mapping each router element to its location in the
      text, plus ≥3 dry-run scenarios (e.g. "fix this on main", "add feature
      X", "where do things stand?") each stating the router's intended
      routing outcome. (Evidence: the section exists and is filled.)

## Tasks

- [x] Draft the classify-first router content and the acceptance rubric
      checklist up front, so the prose is written to the rubric.
- [x] Rewrite `skills/shared/templates/claude-md-section.md` to the router,
      within the cap.
- [x] Update this repo's `CLAUDE.md` cairn section to match; confirm
      `skills/cairn-init/SKILL.md` §1 references to the section (it appends
      the template) still read correctly.
- [ ] Record the rubric-to-text mapping and ≥3 dry-run scenarios in this
      file's Review section.
- [ ] Add `candidate` ROADMAP rows for the deferred on-main commit-guard
      hook and the live-openac empirical test.
- [ ] Verify: grep the router for each rubric element; confirm line count is
      under cap.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. Promotes the "Skill-less routing
  guardrails" candidate (lineage: M02 openac pilot). Scope set at a 3-question
  gate: route-to-skill only, defer on-main hook, rubric + in-repo dry-runs.
- 2026-07-11: rewrote claude-md-section.md as classify-first router (20 body
  lines, under cap). Tasks 1–2 done.
- 2026-07-11: dogfooded this repo's CLAUDE.md to the router form; cairn-init
  §1 references still accurate. Task 3 done.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- The router carries routing only, not conduct: the CLAUDE.md section makes a
  skill fire; `tracking-rules.md` delivers conduct once it does. Candidate for
  promotion to a D-entry at review (it's a cross-cutting delivery decision).

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
