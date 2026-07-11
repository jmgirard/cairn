# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-11 (M09 planned)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M09 | Phase headers (H2/H3) replace inline stage banner | review | — | normal | milestones/M09-phase-headers.md |
| M08 | Skill-less routing guardrails | done | — | high | milestones/archive/M08-skill-less-routing.md |
| M07 | Guardrail hooks (blocking enforcement + re-injection) | done | — | high | milestones/archive/M07-guardrail-hooks.md |
| M06 | Competitive-landscape research | done | — | high | milestones/archive/M06-competitive-landscape.md |
| M05 | Rulebook conventions & protocol gaps | done | M04 | high | milestones/archive/M05-rulebook-conventions.md |
| M04 | Skill conduct & output discipline | done | — | high | milestones/archive/M04-output-discipline.md |

## Candidates

- Stress-test migration on a Lineage B repo (ackwards or circumplex) — added 2026-07-11 — DRAFT_2 §11
- Public release prep: LICENSE (MIT), README worked example, remove DRAFT files, tag v1.0 — added 2026-07-11 — DRAFT_2 §11
- Design-interview skill: one interview, two phases (facts → principles) with banked proto-principles and a chip-gated seam; proposed gold standard — encode question-quality + reconciliation findings so interviews improve on Opus; complement: elevate phase 2 to Fable behind a gate — added 2026-07-11 — references/design-interview-notes.md
- On-main commit-guard hook: PreToolUse guard that warns/blocks git commits touching non-cairn code while on main with no milestone branch active; false-positive-prone (trivial edits ARE allowed on main) so needs its own design; complements M08's router text — added 2026-07-11 — M08 Out
- Live-openac router test: run M08's classify-first router empirically in openac (plain-conversation requests should route to the right tier/skill); openac is a separate repo, no automated evidence lands here — added 2026-07-11 — M08 Out
- Toolchain profiles (generalize beyond R): core is ~80% language-agnostic (this repo runs it sans R); concentrate R-ness into a profile with 6 slots (verify commands, consistency gate, test doctrine, release walk, init detection, greenfield opener questions), chosen at init, recorded in CLAUDE.md section; extraction method: diff what this repo waives vs what openac uses; keep domain doctrine (oracles) orthogonal to language profile; target v0.3 after pilots harden the R slots — added 2026-07-11 — M02 pilot
- Deterministic tracking scripts: ship status/next/validate bash scripts over cairn/ files (instant, token-free, drift-proof) instead of LLM re-derivation each session; ccpm's script-first rule is the model — added 2026-07-11 — references/ccpm.md
- Review pipeline upgrades: distinct-evidence reviewer fan-out (blame history, prior-PR comments), verbatim confidence rubric + false-positive taxonomy, evidence-before-checkbox AC fencing, criterion→task coverage table; includes user decision on relaxing never-Haiku for mechanical triage (Anthropic's own pipeline does) — added 2026-07-11 — references/anthropic-code-review.md, competitive-landscape.md
- Milestone-file mechanics: section write allow-lists per skill, baseline-commit capture at implement start, prior-milestone lessons harvest at plan time, Sync Impact Report on rulebook/principle changes, session-end repo-lessons capture, read_when doc-routing frontmatter for references/ — added 2026-07-11 — references/competitive-landscape.md
- M06 deferred minor steals (one row per C6; promote individually if wanted): scored-rubric hygiene audit for /milestone, conflicts_with/parallel task metadata, principles-touched slot in milestone template, explicit branch↔milestone mapping, complexity-scored split advisory, tiered tool exposure, strict schemas for machine-written fragments, focus-lens subagent fan-out, search-first candidate creation — added 2026-07-11 — references/competitive-landscape.md + per-system notes
- Rulebook wording tweaks from M06 survey: cap-at-3 prioritized clarification markers at question gates (spec-kit), reading-list instruction for Explore subagents (feature-dev), state the why of different-model review — added 2026-07-11 — references/competitive-landscape.md
- Greenfield init flow (builds on toolchain profiles): when cairn-init runs in a new/empty repo, open with a project-type chip → selects the toolchain profile → profile supplies fixed opener questions (R profile: CRAN intent, compiled code Rcpp/RcppArmadillo, statistical calcs needing oracle verification; conventions like {cli} folded into one defaults question or deferred to first milestone-plan); each question carries a marked recommended option, each option states its consequence, every answer lands in a durable home (profile slots / DESIGN Conventions / test doctrine), "undecided" defaults to the reversible choice and is banked as a candidate row; cairn-init stays tracking-only — package skeleton is the obvious first milestone — added 2026-07-11 — toolchain-profiles candidate, references/design-interview-notes.md
