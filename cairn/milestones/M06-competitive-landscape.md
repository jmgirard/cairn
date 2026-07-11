# M06: Competitive-landscape research

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** —
- **Branch/PR:** m06-competitive-landscape

## Goal

Survey the neighboring skills/plugins/frameworks cairn competes with, and
produce a defensible written case for what cairn uniquely offers (or an
honest refocus recommendation if it doesn't).

## Scope

**In:** Eight systems — Anthropic official plugins (feature-dev,
claude-md-management, code-review) and community systems (ccpm, GitHub
spec-kit, Task Master, BMAD-METHOD, Backlog.md + Meridian as one
"enforced-scaffolding" note). Hands-on trial of the closest rivals
(feature-dev, claude-md-management, ccpm); repo/doc study for the rest.
Per-system notes in `references/`, a steal-list, and a positioning
paragraph in DESIGN.md.

**Out:** Acting on any stolen idea (each becomes a candidate row);
README "why cairn" pitch (→ public-release-prep candidate); generalizing
cairn beyond R (→ toolchain-profiles candidate — this milestone only
supplies evidence); broad long-tail survey beyond the eight named systems
(new candidate row if the research surfaces a must-study system).

## Acceptance criteria

- [ ] A `references/<system>.md` note exists for each of the 8 scoped
      systems (Backlog.md+Meridian may share one), each covering: what it
      does, its tracking/workflow model, what cairn should steal, what
      cairn does that it doesn't — with repo/doc URLs cited.
- [ ] The three hands-on systems' notes contain firsthand usage
      observations (commands run, artifacts produced), not just doc reads.
- [ ] `references/INDEX.md` has one line per new note.
- [ ] A comparative-analysis note (`references/competitive-landscape.md`)
      states the uniqueness case or refocus recommendation, addressing:
      markdown-native tracking, status gatekeeping, review/approval gates,
      R-toolchain doctrine — each either defended as differentiating or
      conceded as commodity.
- [ ] DESIGN.md Purpose & Scope contains a positioning paragraph (≤5
      lines) distilled from that analysis.
- [ ] Every "steal" item has a ROADMAP candidate row (or an explicit
      user-approved drop noted in the work log).
- [ ] Any installed trial plugins are uninstalled afterward; the cairn
      symlink install is untouched (verify it still resolves).

## Tasks

- [x] Study Anthropic official plugins from source
      (anthropics/claude-plugins-official): feature-dev,
      claude-md-management, code-review → three notes.
- [x] Hands-on trial: feature-dev and claude-md-management in a scratch
      repo; record what the workflow actually does.
- [x] Study + hands-on trial ccpm (GitHub-Issues PM, worktree parallel
      agents) → note.
- [x] Study from repos/docs: spec-kit, Task Master, BMAD-METHOD,
      Backlog.md/Meridian → three or four notes.
- [ ] Write competitive-landscape.md synthesis: steal-list + uniqueness
      case; update INDEX.md.
- [ ] Add candidate rows for steal-list items; write DESIGN.md
      positioning paragraph; uninstall trial plugins and verify the cairn
      symlink.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan (promoted from same-day candidate
  row; comparanda scoped at question gate to Anthropic + 5 community,
  hands-on top 3, deliverable DESIGN.md + references note).

- 2026-07-11: task 1 done — cloned claude-plugins-official @ dc72937,
  read all three plugins' full source, wrote three references/ notes +
  INDEX rows; flagged never-Haiku doctrine challenge for synthesis.
- 2026-07-11: task 3 done — ccpm full skill source read; local flow
  (PRD→epic→tasks) + 3 status scripts executed hands-on in scratch repo;
  GitHub sync/execute from source only; note + INDEX row written;
  deterministic-status-scripts flagged as biggest steal.
- 2026-07-11: task 4 done — four [S] study agents fanned out (spec-kit,
  Task Master, BMAD, Backlog.md+Meridian); load-bearing claims verified
  against clones (spec-kit gates, Meridian blocking hook, BMAD ledger);
  four notes + INDEX rows written. Task Master agent self-reported
  deleting its own scratch clone (harmless, logged for honesty).
- 2026-07-11: task 2 done — feature-dev all 7 phases executed on scratch
  repo (6 [S] agents); claude-md-improver run end-to-end + read-only
  rubric score of cairn's CLAUDE.md (~70/100); headline finding:
  cross-trial artifact contamination (agents treat any tracked planning
  file as binding) — empirical support for the one-tracking-system rule;
  hands-on sections written into both notes.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- 2026-07-11: hands-on trials run by source-execution in a scratch repo
  (clone plugin source, execute its command workflows directly), not by
  installing into the user's plugin config; ccpm GitHub-sync step
  verified from docs only. (question gate)

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
