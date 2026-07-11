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
- Design-interview skill: encode elicitation question-quality findings so DESIGN interviews improve on Opus; alternative/complement: Fable elevation behind a brief-style gate — added 2026-07-11 — references/design-interview-notes.md
