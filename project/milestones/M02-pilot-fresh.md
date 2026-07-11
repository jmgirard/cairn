# M02: Pilot — fresh adoption in one package repo

- **Status:** planned   <!-- mirror; project/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** M01
- **Branch/PR:** — (work happens in the pilot repo; this file tracks it)

## Goal

Prove the system end-to-end in a package repo with no existing tracking
system.

## Scope

**In:** `/cairn-init` fresh scaffold; ≥3 full milestones (plan → implement →
review); one `/milestone-brief` RB/RR escalation; one `/cairn-release` walk;
friction captured as issues on this repo.

**Out:** migration testing → M03. Fixing the friction found → v0.2 planning
after both pilots.

## Acceptance criteria

- [ ] Scaffold created by `/cairn-init` with no manual fixes needed.
- [ ] 3 milestones shipped through all three phase skills, chips used at
      each transition.
- [ ] One RB/RR cycle completed and ingested.
- [ ] One release walk completed to the handoff checklist.
- [ ] Every friction point filed as an issue on cairn.

## Tasks

- [x] Choose the pilot repo (a package without an existing system).
- [ ] Run `/cairn-init`; note anything manual.
- [ ] Ship 3 milestones; log friction as issues.
- [ ] Run one RB/RR escalation; one release walk.
- [ ] Summarize findings in this file's Review section.

## Work log

- 2026-07-11: planned as part of the v0.1 pilot plan (DRAFT_2 §11).
- 2026-07-11: openac chosen as pilot repo; installed in Claude Desktop via
  Customize → Plugins (skills load un-namespaced; `/plugin` and
  `--plugin-dir` are terminal-only — README should document this path).
- 2026-07-11: /cairn-init scaffold + DESIGN interview underway in openac;
  finding: DESIGN-elicitation question quality markedly better on Fable
  than Opus (same AskUserQuestion format) → candidate row + notes in
  references/design-interview-notes.md.
- 2026-07-11: second (principle-focused) Fable interview also judged
  excellent; pass-2 moves distilled into the notes; Jeff proposes two-pass
  interview (overall → principles) as gold standard → candidate updated.
- 2026-07-11: friction during first openac milestone implement: chat
  output volume disorienting (stage unclear) and oversized question chips
  crowd out chat context → output-discipline/stage-orientation candidate
  added; chip minimize/side-by-side flagged as Desktop app feedback.

## Decisions

## Review
