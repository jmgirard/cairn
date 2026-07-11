# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-11 (audit clean; reviews/ scaffolded)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M04 | Skill conduct & output discipline | done | — | high | milestones/archive/M04-output-discipline.md |
| M05 | Rulebook conventions & protocol gaps | review | M04 | high | milestones/M05-rulebook-conventions.md |
| M03 | Pilot: migrate tidymedia | done | M01 | high | milestones/archive/M03-pilot-migrate-tidymedia.md |
| M02 | Pilot: fresh adoption in one package repo | done | M01 | high | milestones/archive/M02-pilot-fresh.md |
| M01 | Build plugin v0.1 from DRAFT_2 spec | done | — | high | milestones/archive/M01-build-v0-1.md |

## Candidates

- Stress-test migration on a Lineage B repo (ackwards or circumplex) — added 2026-07-11 — DRAFT_2 §11
- Plugin hooks for immediate guardrail feedback (e.g., README.Rmd edit reminder) — added 2026-07-11 — DRAFT_2 §9.2
- Marketplace one-command install: marketplace.json shipped 2026-07-11 (validates); remaining: document install paths in README (incl. Desktop Customize → Plugins) + contrast dev install (skills-dir symlink: live with checkout, no update step, branch-checkout footgun) vs marketplace snapshot (frozen copy, manual re-fetch per release) — dual-install ambiguity bit the pilot 2026-07-11 — added 2026-07-11 — DRAFT_2 §2.3
- Public release prep: LICENSE (MIT), README worked example, remove DRAFT files, tag v1.0 — added 2026-07-11 — DRAFT_2 §11
- Design-interview skill: one interview, two phases (facts → principles) with banked proto-principles and a chip-gated seam; proposed gold standard — encode question-quality + reconciliation findings so interviews improve on Opus; complement: elevate phase 2 to Fable behind a gate — added 2026-07-11 — references/design-interview-notes.md
- Skill-less routing guardrails: rulebook only loads when a skill fires, so plain conversation can bypass tiers/git model; make claude-md-section an imperative classify-first router ("not trivial → invoke the skill; unsure → /milestone; never implement on main"), pair with guardrail hooks (existing candidate); test empirically in openac first; also the sole delivery path for rulebook conduct (incl. contextual-chip principle) when milestone talk starts as plain conversation — persistent memory can't serve other cairn users — added 2026-07-11 — M02 pilot
- Toolchain profiles (generalize beyond R): core is ~80% language-agnostic (this repo runs it sans R); concentrate R-ness into a profile with 6 slots (verify commands, consistency gate, test doctrine, release walk, init detection, greenfield opener questions), chosen at init, recorded in CLAUDE.md section; extraction method: diff what this repo waives vs what openac uses; keep domain doctrine (oracles) orthogonal to language profile; target v0.3 after pilots harden the R slots — added 2026-07-11 — M02 pilot
- Greenfield init flow (builds on toolchain profiles): when cairn-init runs in a new/empty repo, open with a project-type chip → selects the toolchain profile → profile supplies fixed opener questions (R profile: CRAN intent, compiled code Rcpp/RcppArmadillo, statistical calcs needing oracle verification; conventions like {cli} folded into one defaults question or deferred to first milestone-plan); each question carries a marked recommended option, each option states its consequence, every answer lands in a durable home (profile slots / DESIGN Conventions / test doctrine), "undecided" defaults to the reversible choice and is banked as a candidate row; cairn-init stays tracking-only — package skeleton is the obvious first milestone — added 2026-07-11 — toolchain-profiles candidate, references/design-interview-notes.md
