<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M28: Harden the output-discipline mandate guards

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** —

## Goal

Promote the chapter-marker rule to a hard per-phase mandate guarded across
all nine skills, and bring `milestone-brief`'s routing chip under the
existing routing-chip guard the M26 lock missed.

## Scope

**In:**
- Rewrite the tracking-rules "Chapter markers" rule from "where the harness
  supports it" to a per-phase mandate (mark a chapter at each phase
  transition), with a no-mechanism fallback clause (headers are the visual
  fallback; nothing breaks). Executes the promotion D-020 banked as a
  candidate; records a new D-entry annotating D-020.
- A one-line chapter-marker directive in all nine phase skills (review
  included — chapter markers are orthogonal to the routing-chip exception),
  plus a guard test locking the mandate wording + per-skill directives.
- Fix `milestone-brief` step 5 to name the routing chip as `AskUserQuestion`,
  add `milestone-brief` to `NON_REVIEW_CHIP_SKILLS`, and correct the stale
  guard comment that claims it has no terminal routing-chip step.

**Out:**
- Live-firing the chapter mechanism in the harness → not needed; M27 already
  characterized the chapter-marker→TOC behavior live (D-020). Guards here are
  prose-guards (the M19/M27 lesson: prose guards prove wording, not runtime).
- Extending the mandate to any client-observable TOC behavior beyond Claude
  Code → out of scope; D-020 left other surfaces unverified.
- `hotfix`'s end-of-phase behavior → it carries no standalone terminal
  routing-chip step; untouched here.

## Acceptance criteria

- [ ] The tracking-rules "Chapter markers" rule states a per-phase mandate:
      a chapter is marked at each phase transition (session start implicit).
      Evidence: rule text + guard assertion.
- [ ] The same rule states the no-mechanism fallback: where the runtime
      provides no chapter mechanism the H1/H2 phase headers are the visual
      fallback and no marker is emitted (nothing breaks). Evidence: rule
      text + guard assertion.
- [ ] All nine phase skills carry a one-line chapter-marker directive.
      Evidence: `test_chapter_marker_mandate.py` iterating the nine skills
      passes.
- [ ] `milestone-brief` step 5 names its routing chip as `AskUserQuestion`
      (carries the single-line `routing chip (AskUserQuestion)` token).
      Evidence: `TestRoutingChipMandate` passes with it in the list.
- [ ] `milestone-brief` is in `NON_REVIEW_CHIP_SKILLS` and the stale
      "no standalone terminal routing-chip step" comment is corrected.
      Evidence: guard-list membership + the corrected comment in the test.
- [ ] Full guard suite (`python3 -m unittest discover -s skills/tests`) and
      `cairn_validate` audit both clean; the mandate-promotion D-entry
      (annotating D-020) is appended to `cairn/DECISIONS.md`. Evidence:
      command output + the D-entry.

## Coverage

- AC1 → T4, T3
- AC2 → T4, T3
- AC3 → T5, T3
- AC4 → T2, T1
- AC5 → T1
- AC6 → T6

## Tasks

- [ ] T1: Extend `TestRoutingChipMandate` — add `milestone-brief` to
      `NON_REVIEW_CHIP_SKILLS` and correct the stale comment at
      `skills/tests/test_gate_wording.py:51` (test goes red: the SKILL lacks
      the token).
- [ ] T2: Add the single-line `**Routing chip (AskUserQuestion)**` token to
      `milestone-brief` step 5 (`skills/milestone-brief/SKILL.md:65`),
      greening T1. Token inside the bold, one line (M26 lesson).
- [ ] T3: Write `skills/tests/test_chapter_marker_mandate.py` — assert all
      nine skills carry the chapter-marker directive token, and that
      tracking-rules declares both the per-phase mandate and the
      no-mechanism fallback (red until T4/T5). Assert phrases on single
      lines (M23 lesson).
- [ ] T4: Rewrite the tracking-rules "Chapter markers" rule
      (`skills/shared/tracking-rules.md:337`) to the per-phase mandate with
      the no-mechanism fallback clause; name the runtime mechanism
      (Claude Code `mark_chapter`) and cite D-020.
- [ ] T5: Add the one-line chapter-marker directive to all nine skills
      (parallel to each `Phase header:` directive), greening T3.
- [ ] T6: Append the D-entry recording the mandate promotion (annotates
      D-020) to `cairn/DECISIONS.md`; run the full guard suite +
      `cairn_validate`; record evidence.

## Work log

- 2026-07-12: created by /milestone-plan.

## Decisions

## Review
