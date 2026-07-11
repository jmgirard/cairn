# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-11_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M01 | Build plugin v0.1 from DRAFT_2 spec | review | — | high | milestones/M01-build-v0-1.md |
| M02 | Pilot: fresh adoption in one package repo | planned | M01 | high | milestones/M02-pilot-fresh.md |
| M03 | Pilot: migrate tidymedia | planned | M01 | high | milestones/M03-pilot-migrate-tidymedia.md |

## Candidates

- Stress-test migration on a Lineage B repo (ackwards or circumplex) — added 2026-07-11 — DRAFT_2 §11
- Plugin hooks for immediate guardrail feedback (e.g., README.Rmd edit reminder) — added 2026-07-11 — DRAFT_2 §9.2
- Marketplace one-command install: marketplace.json shipped 2026-07-11 (validates); remaining: document install paths in README (incl. Desktop Customize → Plugins) — added 2026-07-11 — DRAFT_2 §2.3
- Public release prep: LICENSE (MIT), README worked example, remove DRAFT files, tag v1.0 — added 2026-07-11 — DRAFT_2 §11
- Design-interview skill: one interview, two phases (facts → principles) with banked proto-principles and a chip-gated seam; proposed gold standard — encode question-quality + reconciliation findings so interviews improve on Opus; complement: elevate phase 2 to Fable behind a gate — added 2026-07-11 — references/design-interview-notes.md
- DESIGN principle ordering: specify IP block first then GP, numeric within type, numbers never reused/renumbered (retire via D-entry) — in cairn-init skeleton + rulebook — added 2026-07-11 — M02 pilot (openac DESIGN interview)
- Skill-less routing guardrails: rulebook only loads when a skill fires, so plain conversation can bypass tiers/git model; make claude-md-section an imperative classify-first router ("not trivial → invoke the skill; unsure → /milestone; never implement on main"), pair with guardrail hooks (existing candidate); test empirically in openac first — added 2026-07-11 — M02 pilot
- Toolchain profiles (generalize beyond R): core is ~80% language-agnostic (this repo runs it sans R); concentrate R-ness into a profile with 5 slots (verify commands, consistency gate, test doctrine, release walk, init detection), chosen at init, recorded in CLAUDE.md section; extraction method: diff what this repo waives vs what openac uses; keep domain doctrine (oracles) orthogonal to language profile; target v0.3 after pilots harden the R slots — added 2026-07-11 — M02 pilot
- Output discipline & stage orientation: stage-banner line on all skill output ([cairn · implement · M01 · task 3/7]); between-gate chat reports deltas not dumps; chip weight caps (evidence in chat above the chip, option text lean, ≤4 options); chapter markers at phase transitions where harness supports (Desktop floating TOC) — added 2026-07-11 — M02 pilot (chip-layout minimize/side-by-side itself is Desktop app feedback, not cairn)
