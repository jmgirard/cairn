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

- [ ] Study Anthropic official plugins from source
      (anthropics/claude-plugins-official): feature-dev,
      claude-md-management, code-review → three notes.
- [ ] Hands-on trial: feature-dev and claude-md-management in a scratch
      repo; record what the workflow actually does.
- [ ] Study + hands-on trial ccpm (GitHub-Issues PM, worktree parallel
      agents) → note.
- [ ] Study from repos/docs: spec-kit, Task Master, BMAD-METHOD,
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

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
