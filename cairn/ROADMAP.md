# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-11 (M16 done+archived; M11 row pruned per 5-done retention)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M16 | Lessons loop (capture → harvest) | done | — | normal | milestones/archive/M16-lessons-loop.md |
| M15 | Sync Impact Report on principle changes | done | — | normal | milestones/archive/M15-sync-impact-report.md |
| M14 | Section write allow-lists per skill | done | — | normal | milestones/archive/M14-section-allow-lists.md |
| M13 | Wire deterministic scripts into review + plan | done | — | normal | milestones/archive/M13-script-wiring.md |
| M12 | Design-interview skill (facts → principles) | done | — | normal | milestones/archive/M12-design-interview-skill.md |

## Candidates

- Stress-test migration on a Lineage B repo (ackwards or circumplex) — added 2026-07-11 — DRAFT_2 §11
- Public release prep: LICENSE (MIT), README worked example, remove DRAFT files, tag v1.0 — added 2026-07-11 — DRAFT_2 §11
- On-main commit-guard hook: PreToolUse guard that warns/blocks git commits touching non-cairn code while on main with no milestone branch active; false-positive-prone (trivial edits ARE allowed on main) so needs its own design; complements M08's router text — added 2026-07-11 — M08 Out
- Live-openac router test: run M08's classify-first router empirically in openac (plain-conversation requests should route to the right tier/skill); openac is a separate repo, no automated evidence lands here — added 2026-07-11 — M08 Out
- Toolchain profiles (generalize beyond R): core is ~80% language-agnostic (this repo runs it sans R); concentrate R-ness into a profile with 6 slots (verify commands, consistency gate, test doctrine, release walk, init detection, greenfield opener questions), chosen at init, recorded in CLAUDE.md section; extraction method: diff what this repo waives vs what openac uses; keep domain doctrine (oracles) orthogonal to language profile; target v0.3 after pilots harden the R slots — added 2026-07-11 — M02 pilot
- Scripts --json output mode: add a machine-readable `--json` flag to the cairn_* scripts once a consumer exists (deferred from M13 as YAGNI — today the only readers are the skills, which parse text) — added 2026-07-11 — M13 Out
- Review pipeline upgrades: distinct-evidence reviewer fan-out (blame history, prior-PR comments), verbatim confidence rubric + false-positive taxonomy, evidence-before-checkbox AC fencing, criterion→task coverage table; includes user decision on relaxing never-Haiku for mechanical triage (Anthropic's own pipeline does) — added 2026-07-11 — references/anthropic-code-review.md, competitive-landscape.md
- Baseline-commit capture at implement start: record the base SHA in the milestone header so review diffs against a fixed point (marginal — review already syncs main and diffs `main..HEAD`) — split 2026-07-11 from milestone-file-mechanics (→ M14–M16) — references/competitive-landscape.md
- read_when doc-routing frontmatter for references/: per-file frontmatter marking when to read a reference (marginal — `references/INDEX.md` already routes) — split 2026-07-11 from milestone-file-mechanics — references/competitive-landscape.md
- M06 deferred minor steals (one row per C6; promote individually if wanted): scored-rubric hygiene audit for /milestone, conflicts_with/parallel task metadata, principles-touched slot in milestone template, explicit branch↔milestone mapping, complexity-scored split advisory, tiered tool exposure, strict schemas for machine-written fragments, focus-lens subagent fan-out, search-first candidate creation — added 2026-07-11 — references/competitive-landscape.md + per-system notes
- Rulebook wording tweaks from M06 survey: cap-at-3 prioritized clarification markers at question gates (spec-kit), reading-list instruction for Explore subagents (feature-dev), state the why of different-model review — added 2026-07-11 — references/competitive-landscape.md
- Greenfield init flow (builds on toolchain profiles): when cairn-init runs in a new/empty repo, open with a project-type chip → selects the toolchain profile → profile supplies fixed opener questions (R profile: CRAN intent, compiled code Rcpp/RcppArmadillo, statistical calcs needing oracle verification; conventions like {cli} folded into one defaults question or deferred to first milestone-plan); each question carries a marked recommended option, each option states its consequence, every answer lands in a durable home (profile slots / DESIGN Conventions / test doctrine), "undecided" defaults to the reversible choice and is banked as a candidate row; cairn-init stays tracking-only — package skeleton is the obvious first milestone — added 2026-07-11 — toolchain-profiles candidate, references/design-interview-notes.md
