# M09: Phase headers (H2/H3) replace the inline stage banner

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- high | normal | low -->
- **Depends on:** —   <!-- extends M04 output discipline; no hard dep -->
- **Branch/PR:** m09-phase-headers · https://github.com/jmgirard/cairn/pull/6

## Goal

Replace the inline `[cairn · … ]` stage banner with a two-level Markdown
heading (`## Milestone <NN>: <title>` → `### Plan`/`### Implement`/`### Review`)
so phase transitions are scannable in the terminal.

## Scope

**In:**
- Rewrite the **Stage banner** rule in `skills/shared/tracking-rules.md`
  ("Output & interaction discipline") as a **Phase header** rule: an `##`
  names the unit of work + title, a `###` names the phase; emit the `##`
  once at the first phase entered in a session (a fresh post-`/clear`
  session re-emits it), a `###` at each phase entry (usually coincident with
  a chapter marker); replies within a phase run as plain deltas — never a
  heading per reply.
- Update the banner line in all 8 skills (`plan`, `implement`, `review`,
  `milestone`, `hotfix`, `milestone-brief`, `cairn-init`, `cairn-release`)
  from `Stage banner: [cairn · …]` to `Phase header: ## … → ### …`, each
  mapped to that skill's real phases/steps.
- Rename the rule "Stage banner" → "Phase header" including any
  cross-references in `tracking-rules.md`.

**Out:**
- Changing the chapter-marker rule → not touched; phase headers coincide
  with chapter markers but the marker mechanism is unchanged.
- Any change to the deltas/outcome-first/chip rules → unchanged (this only
  swaps the orientation-line format).

## Acceptance criteria

(Evidence for each recorded in the Review section.)

- [x] **Phase-header rule.** `tracking-rules.md` states a "Phase header" rule
      specifying the `##` unit + `###` phase hierarchy, `##`-once-per-session
      and `###`-per-phase-entry cadence, and plain-deltas-otherwise. The
      words "Stage banner" no longer appear anywhere in the rulebook.
- [x] **All 8 skills updated.** Every skill's banner line reads
      `Phase header: …` with an `##`/`###` mapping to its actual phases; a
      grep for the old bracket banner (`[cairn ·`) across `skills/` returns
      zero matches.
- [x] **Correct per-skill mapping.** Milestone skills map to
      `## Milestone <NN>: <title>` → `### Plan|Implement|Review`;
      non-milestone skills map to their own units/steps
      (`## Hotfix: <slug>` → `### <step>`; `## cairn-init` → `### Scaffold|
      Repair|Migration §n`; `## Release <version>` → `### <step>`;
      `## Status` → `### Snapshot|Audit|Route`;
      `## Review brief RB<NN>` → `### Draft|Gate|Ingest`).
- [x] **Rubric recorded.** This milestone file's Review section records a
      rubric mapping each required element to its location, per the M08
      precedent.

## Tasks

- [x] Rewrite the Stage-banner bullet in `tracking-rules.md` as the Phase
      header rule; grep for stray "Stage banner" references and rename.
- [x] Update all 8 skills' banner lines to the `Phase header:` form; grep to
      confirm zero `[cairn ·` bracket banners remain in `skills/`.
- [x] Record the verification rubric in the Review section; adopt the new
      header form in this session's remaining replies (dogfood).

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. From Jeff's scannability feedback;
  extends M04 output discipline. Shape set at a 2-round gate: two-level
  hierarchy (phase word only), rename to "Phase header", `##` once/session +
  `###` per phase entry.
- 2026-07-11: rewrote the rule in tracking-rules.md and all 8 skill banner
  lines; verified 0 "Stage banner" / 0 bracket banners in skills/, 8 Phase
  header lines. Tasks 1–3 done; status → review.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- Two-level header (`##` unit / `###` phase) over a flat single `##`: groups a
  milestone's phases within a session while degrading gracefully across
  `/clear` (each session re-emits the `##`). Supersedes the M04-era inline
  stage banner (which was set in tracking-rules, not a D-entry).

## Verification rubric (deliverable for criterion 4)

| Element | Location / evidence |
|---|---|
| "Phase header" rule with `##`/`###` hierarchy + cadence | `tracking-rules.md` "Output & interaction discipline" (replaces the Stage-banner bullet) |
| "Stage banner" gone from rulebook | `grep -c "Stage banner" tracking-rules.md` → 0 |
| 8 skills carry `Phase header:` lines | `grep -rc "Phase header:" skills/*/SKILL.md` → 8 non-zero |
| No bracket banners left in skills/ | `grep -rn "\[cairn ·" skills/` → 0 |
| Milestone skills → `## Milestone <NN>: <title>` → `### Plan/Implement/Review` | plan/implement/review SKILL.md banner lines |
| Non-ms skills → own units/steps | hotfix/init/release/milestone/brief SKILL.md banner lines |

## Review

**Fresh evidence (2026-07-11, /milestone-review):**
- C1: `tracking-rules.md` has the "Phase header" rule (grep 1); "Stage
  banner" gone (grep 0); ##/### hierarchy + once-per-session/per-phase
  cadence + plain-deltas language present.
- C2: 8 skills carry `Phase header:` lines; `[cairn ·` in `skills/` → 0;
  "Stage banner" in `skills/` → 0.
- C3: mappings correct — plan/implement/review → `## Milestone <NN>: <title>`
  → `### Plan|Implement|Review`; hotfix/init/release/status/brief → their own
  units/steps (verified against each SKILL.md banner line).
- C4: "Verification rubric" section present with per-element locations.
- Live-doc sweep: no stray "Stage banner"/bracket refs outside the M09 file
  (DESIGN, README, CLAUDE, other skills clean).

**Consistency gate:** R gates N/A (no DESCRIPTION). CHANGELOG release-scoped;
no entry due. Main in sync with origin; no CI workflows.

**Independent review (Opus, fresh context):** change judged sound; mappings
verified against each skill's real workflow. Triage:
- F1 (medium) — "emit the `##` once per session" misfires when one session
  spans multiple units via routing chips (this very session did). **Fixed:**
  reworded to once-per-unit, re-emitting on a chip into the next skill or a
  post-`/clear` session.
- F2 (low) — a plan run can create several milestones; header names one.
  **Fixed:** rule now says a multi-milestone plan run stays under one
  `## Planning`.
- F3 (nit) — the session's first header has no chapter marker (session start
  is implicit). **Fixed:** noted in the rule.
- F4 (nit) — `## cairn-init` is bare (no title) unlike the other units.
  **Left:** one init per repo, no meaningful title; accepted inconsistency.
