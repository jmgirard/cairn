# M02: Pilot — fresh adoption in one package repo

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** M01
- **Branch/PR:** — (work happens in the pilot repo; this file tracks it)

## Goal

Prove the system end-to-end in a package repo with no existing tracking system.

## Scope

**In:** `/cairn-init` fresh scaffold; ≥3 full milestones (plan → implement →
review); one `/milestone-brief` RB/RR escalation; one `/cairn-release` walk;
friction captured as candidate rows on this repo (issues also accepted).

**Out:** migration testing → M03. Fixing the friction found → v0.2 planning
after both pilots.

## Acceptance criteria

- [ ] Scaffold created by `/cairn-init` with no manual fixes needed.
- [ ] 3 milestones shipped through all three phase skills, chips used at
      each transition.
- [ ] One RB/RR cycle completed and ingested.
- [ ] One release walk completed to the handoff checklist.
- [ ] Every friction point captured as a candidate row on cairn (or filed
      as an issue).

## Tasks

- [x] Choose the pilot repo (a package without an existing system).
- [x] Run `/cairn-init`; note anything manual.
- [x] Ship 3 milestones; log friction as candidates.
- [x] Run one RB/RR escalation; one release walk. (RB01/RR01 ingested +
      archived; release walk → openac 0.1.0, tagged, no-CRAN handoff.)
- [x] Summarize findings in this file's Review section.

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
- 2026-07-11: resumed via /milestone-implement; status in-progress.
  Catch-up from openac git: scaffold complete and functioning; openac M01
  (os_read) and M02 (of_read) shipped through full plan→implement→review
  cycles (2 of ≥3); M03–M05 planned; no RB/RR or release walk yet.
- 2026-07-11: friction: openac scaffold predates D-008, uses project/ not
  cairn/ — rename disposition pending user decision.
- 2026-07-11: gate: user approved renaming openac project/ → cairn/ now;
  executed in openac (its D-007, commit 3c81c7b, pushed).
- 2026-07-11: plan amendment (gate-approved): friction criterion changed
  from "filed as issues" to "captured as candidate rows (or issues)" —
  matches established practice (5 candidates banked, 0 issues).
- 2026-07-11: gate: Jeff drives remaining pilot work (3rd milestone, RB/RR,
  release walk) in openac Desktop sessions for pilot fidelity; openac M04
  (check hygiene) chosen next. This session tracks; catch-up from openac
  git on resume.
- 2026-07-11: friction (openac + tidymedia): chip option descriptions too
  technical — unclear what's being chosen and why it matters → folded into
  output-discipline candidate. Also: Desktop chips can be minimized without
  closing, softening the earlier chip-layout concern.
- 2026-07-11: catch-up from openac git: M04 (check hygiene) shipped through
  full plan→implement→review (PR #3, archived) — 3rd milestone criterion
  met. Remaining: one RB/RR cycle, one release walk.
- 2026-07-11: catch-up: openac M03 (whisper reader) at review; no RB/RR
  artifacts yet.
- 2026-07-11: friction (Jeff's deliberate experiment): skills never
  self-solicited an RB during openac M03 despite an RB-worthy question —
  escalation hook is confidence-triggered → RB self-solicitation candidate
  banked (category tripwires + plan-time tagging + gate chip option).
- 2026-07-11: catch-up from openac git: M03 merged (PR #4, archived);
  RB01/RR01 (reader-family-api) spawned via gated Fable subagent, ingested,
  archived — RB/RR criterion met. Release walk still missing (no
  cran-comments, version unbumped); M02 stays in-progress.
- 2026-07-11: gate: Jeff runs /cairn-release in openac (walk to handoff
  checklist, no submission; stale vignettes may surface — acceptable pilot
  signal). Last open criterion; M02 → review on its completion.
- 2026-07-11: catch-up from openac git: M05 (vignettes) shipped first
  (PR #5, archived — 5 milestones total), then /cairn-release walked
  0.0.0.9000 → 0.1.0 (NEWS consolidated, README rewritten, tag v0.1.0,
  deliberate no-CRAN, dev re-bump). All criteria have evidence; findings
  summarized in Review; status → review.

## Decisions

## Review

### Criteria evidence (2026-07-11, fresh by command)

1. **Scaffold, no manual fixes** — PASS w/ judgment call: nothing manual
   recorded at scaffold time (only a Desktop install-path doc gap). The
   later `project/`→`cairn/` rename (openac 3c81c7b, 13 files) was
   upstream design change D-008, not a scaffold repair — but the shipping
   post-D-008 init has not itself been executed: verified mechanically
   (grep: zero non-legacy `project/` refs in cairn-init/templates); M03
   (tidymedia) exercises it for real. Flagged to approval gate.
2. **≥3 milestones, three phase skills, chips** — PASS: 5 archives on disk
   (openac M01–M05), PRs #1–#5 all merged, plan/review commits per
   milestone; chip use attested (user + screenshot; no disk artifact).
3. **RB/RR cycle** — PASS: RB01/RR01 archived; ingested as openac D-entry
   with consequences landed in code (speaker column, colClasses fix, test).
4. **Release walk** — PASS: 0.0.0.9000→0.1.0 (d14e8e8), NEWS consolidated,
   README rewritten, tag v0.1.0, no-CRAN call, dev re-bump 78a380e.
5. **Friction → candidates** — PASS: 8 rows tagged M02 pilot + 2 derived
   from pilot notes; every friction work-log line maps to a row; 0 issues.

Consistency gate (adapted; R gates waived per CLAUDE.md): caps OK
(CLAUDE.md 17/80, ROADMAP 34/60, this file /150); status mirror = ROADMAP;
no README.Rmd/NEWS.md obligations (plugin repo). No branch/PR: docs-only
meta-milestone on main (deviation logged 2026-07-11, planning).

### Independent review (2026-07-11, fresh-context Opus)

Approve-with-fixes; all criteria verified on disk; RB/RR called exemplary
(RR01 caught a real csv-parity defect). Triage — fixed: F1 untested
shipping init (mechanical grep above; M03 closes it empirically), F2 PR
evidence understated (#1–#5 all merged), F3 candidate count (8+2 wording).
Accepted: F4 chip use rests on attestation — noted for approver. Rejected:
F5 "Fable-orchestrator rename breaches D-004" — D-004 governs spawned
subagents; the orchestrator model is the user's Desktop choice and the
rename was gate-approved (work log). Observations F6 (cap headroom →
findings compressed), F7 (openac scaffold committed inside its M01
commit; openac-internal): logged, no action.

### Pilot findings (implementation summary, 2026-07-11)

The system worked end-to-end: /cairn-init scaffold, five openac milestones
through plan→implement→review with chips at every transition, one gated
Fable RB/RR cycle, one /cairn-release walk. Friction became candidate rows
(8 tagged + 2 derived) rather than issues. Highest-signal: RB
self-solicitation gap (confidence-triggered hook never fired; deliberate
experiment); Fable > Opus elicitation quality; output discipline (stage
orientation, plain-language chips); contextual-chip construction
validated; structural gaps (skill-less routing, cross-repo IDs, toolchain
profiles — core proved ~80% language-agnostic). All banked as candidates.
