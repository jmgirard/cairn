# M08: Skill-less routing guardrails

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- high | normal | low -->
- **Depends on:** —   <!-- M07 hooks already shipped; no hard dep -->
- **Branch/PR:** m08-skill-less-routing · https://github.com/jmgirard/cairn/pull/5

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

**Out:** (all decided at the plan gate, 2026-07-11)
- Mechanical "no code commits on main" PreToolUse guard → `candidate` row
  (false-positive-prone; trivial edits are legitimately allowed on main).
- Live empirical test of the router in openac → `candidate` row (separate
  repo; no automated evidence lands here).
- Embedding full conduct (chips, output discipline) into the router → not
  done: conduct stays in `tracking-rules.md`, loaded when a skill fires; the
  router's job is to make a skill fire, not to restate conduct.

## Acceptance criteria

(Evidence for each in the Review section.)

- [x] **Classify-first + tiers + never-on-main.** `claude-md-section.md`
      opens with an imperative to classify before acting, and names every
      tier→destination mapping (trivial → main; bug → `/hotfix`; new
      work/design/>1 sitting → `/milestone-plan`; status/unsure →
      `/milestone`) plus "never implement code on main outside a branch."
- [x] **Delivery-path rule.** Router says milestone-ish talk must invoke the
      skill so the full rulebook loads, and does NOT restate conduct — points
      to the skills instead.
- [x] **Within cap.** Template section body ≤ ~25 lines.
- [x] **Dogfooded.** This repo's own `CLAUDE.md` cairn section matches the
      router (same mappings, same never-on-main rule).
- [x] **Rubric + dry-runs.** This file records a rubric mapping each router
      element to its location, plus ≥3 dry-run scenarios with intended
      routing outcomes.

## Tasks

- [x] Draft the classify-first router content and the acceptance rubric
      checklist up front, so the prose is written to the rubric.
- [x] Rewrite `skills/shared/templates/claude-md-section.md` to the router,
      within the cap.
- [x] Update this repo's `CLAUDE.md` cairn section to match; confirm
      `skills/cairn-init/SKILL.md` §1 references to the section (it appends
      the template) still read correctly.
- [x] Record the rubric-to-text mapping and ≥3 dry-run scenarios in this file.
- [x] Add `candidate` ROADMAP rows for the deferred on-main commit-guard
      hook and the live-openac empirical test (done at plan time, 454ba58).
- [x] Verify: grep the router for each rubric element; confirm line count.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. Promotes the "Skill-less routing
  guardrails" candidate (lineage: M02 openac pilot). Scope set at a 3-question
  gate: route-to-skill only, defer on-main hook, rubric + in-repo dry-runs.
- 2026-07-11: rewrote claude-md-section.md as classify-first router (20 body
  lines, under cap). Tasks 1–2 done.
- 2026-07-11: dogfooded this repo's CLAUDE.md to the router form; cairn-init
  §1 references still accurate. Task 3 done.
- 2026-07-11: added rubric + 5 dry-run scenarios; verified all rubric
  elements present and conduct not restated. Tasks 4–6 done; status → review.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- The router carries routing only, not conduct: the CLAUDE.md section makes a
  skill fire; `tracking-rules.md` delivers conduct once it does. Candidate for
  promotion to a D-entry at review (it's a cross-cutting delivery decision).

## Router rubric & dry-runs (deliverable for criterion 5)

Rubric — each required router element and where it lives in
`skills/shared/templates/claude-md-section.md`:

| Element | Location in template |
|---|---|
| Classify-first imperative | Opening: "Before acting on any request, classify it and route" |
| Trivial → main | Bullet 1 |
| User-visible bug → `/hotfix` | Bullet 2 |
| New work / design decision / >1 sitting → `/milestone-plan` | Bullet 3 |
| Status / "what's next" / unsure → `/milestone` | Bullet 4 |
| Never implement code on main outside a branch | Bullet 5 |
| Approval required at review gate | Bullet 5 |
| Delivery-path rule (invoke skill first; rulebook + conduct load) | Closing paragraph |
| Does NOT restate conduct — points to `tracking-rules.md` | Closing paragraph (no chip/output-discipline prose inlined) |
| Boundary rule + memory-never-holds-state retained | Closing paragraph |

Dry-run scenarios — the routing the router is intended to produce:

1. *"Fix the bug where scoring returns NA for empty input."* → user-visible
   bug → `/hotfix` (regression test first, branch, PR). Without the router,
   plain conversation risks editing on main with no test.
2. *"Let's add batch scoring."* → new work / more than one sitting →
   `/milestone-plan`. Router stops code being written on main.
3. *"Where do things stand — what should I do next?"* → status/unsure →
   `/milestone`.
4. *"Fix this typo in a code comment."* → trivial (no runtime surface) →
   commit directly to main; the router keeps the fast path fast, not
   everything funneled into ceremony.
5. *"Quick, just change this threshold on main real fast."* → not trivial
   (behavior change) → the never-implement-on-main rule fires; classify as
   bug (`/hotfix`) or new work (`/milestone-plan`), branch first.

## Review

**Fresh evidence (2026-07-11, /milestone-review):**
- C1 (classify-first + tiers + never-on-main): all present in
  `claude-md-section.md` — classify-first opener, four tier→destination
  mappings, "Never implement code on main", approval-at-review. Grep-verified.
- C2 (delivery-path rule; conduct not restated): "invoke the skill *first*
  so the full rulebook loads" present; 0 matches for chip/output-discipline
  prose. Verified.
- C3 (within cap): 20 non-blank body lines (≤ ~25). `wc -l`.
- C4 (dogfooded): repo `CLAUDE.md` carries the same router elements
  (classify, /hotfix, /milestone-plan, never-on-main, tracking-rules ptr).
- C5 (rubric + dry-runs): "Router rubric & dry-runs" section present; 5
  dry-run scenarios.

**Consistency gate:** R gates N/A (no DESCRIPTION — plugin repo). CHANGELOG
is release-scoped (updated at /cairn-release, as for M04–M07); no entry due.
Main in sync with origin; no CI workflows.

**Independent review (Opus, fresh context):** change judged sound — taxonomy
matches tracking-rules, caps met, dogfood consistent, all criteria satisfied.
Findings triaged:
- F1 (low) — router dropped "the plugin's" before `tracking-rules.md`; in an
  adopted foreign repo there's no `skills/` at root. **Fixed** in template +
  repo CLAUDE.md.
- F2 (trivial) — C3 parenthetical named the old "~20-line" header after it
  was loosened to ~25. **Fixed.**
- F3 (trivial) — "20 body lines" vs 19 non-blank (heading counting).
  Immaterial (under cap either way); **left as-is.**
- Note (not a defect): rewrite intentionally drops the eight-skill
  enumeration and the "add to candidates" intake line to hit the cap;
  candidate-adding is a trivial tracking edit. Accepted trade-off.
