# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-12 (M19 done+archived; M14 row pruned per 5-done retention)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M20 | Migration stress-test pilot — ackwards (Lineage B) | review | — | normal | milestones/M20-migration-pilot-ackwards.md |
| M21 | Migration stress-test pilot — circumplex (Lineage B) | planned | M20 | normal | milestones/M21-migration-pilot-circumplex.md |
| M19 | Memory-boundary write guard (GP4 enforcement) | done | M18 | normal | milestones/archive/M19-memory-boundary-guard.md |
| M18 | Acceptance-criteria traceability | done | M17 | normal | milestones/archive/M18-ac-traceability.md |
| M17 | Review fan-out + confidence scoring | done | — | normal | milestones/archive/M17-review-fanout.md |
| M16 | Lessons loop (capture → harvest) | done | — | normal | milestones/archive/M16-lessons-loop.md |
| M15 | Sync Impact Report on principle changes | done | — | normal | milestones/archive/M15-sync-impact-report.md |

## Candidates

- Recalibrate the CLAUDE.md weight cap for mature repos: the `<80` cap fails on a real mature R package (ackwards CLAUDE.md was 187 lines after full redistribution — legit dev doctrine + the ~26-line appended cairn section floor well above 80); reconsider as a higher flat cap, size-tiered, or toolchain-profile-based — added 2026-07-12 — references/migration-pilot-notes.md G8 (M20)
- Parameterize the default branch (main/master) across cairn: the git model, CLAUDE template, and cairn-init §2 are `main`-hardcoded; detect the repo's default branch at init and adapt, or say "default branch (main/master)" throughout — added 2026-07-12 — references/migration-pilot-notes.md G1/G9 (M20)
- Migration guidance for a rich pre-existing DESIGN.md: §5 only anticipates a thin DESIGN; add guidance for a large living DESIGN with an embedded decision log (keep-verbatim vs extract-to-DECISIONS; the Compromise A/B split) and for routing invariants→IP/GP through /design-interview — added 2026-07-12 — references/migration-pilot-notes.md G3/G5 (M20)
- Migration: handle in-code references to relocated tracking files: mature repos cite `DESIGN.md`/`MILESTONES.md` by name in source comments/tests (15+ in ackwards) and CLAUDE prose references the skills being entombed; add a repoint-or-note sweep step to §4/§6 — added 2026-07-12 — references/migration-pilot-notes.md G6/G10 (M20)
- Migration hygiene tweaks: prune stale per-file `.Rbuildignore` entries after files move (§1 only says add `^cairn$`), and widen Lineage B detection wording to cover a repo that already has a forward-only ROADMAP + explicit status slot — added 2026-07-12 — references/migration-pilot-notes.md G7/G2 (M20)
- Public release prep: LICENSE (MIT), README worked example, remove DRAFT files, tag v1.0 — added 2026-07-11 — DRAFT_2 §11
- On-main commit-guard hook: PreToolUse guard that warns/blocks git commits touching non-cairn code while on main with no milestone branch active; false-positive-prone (trivial edits ARE allowed on main) so needs its own design; complements M08's router text — added 2026-07-11 — M08 Out
- Live-openac router test: run M08's classify-first router empirically in openac (plain-conversation requests should route to the right tier/skill); openac is a separate repo, no automated evidence lands here — added 2026-07-11 — M08 Out
- Toolchain profiles (generalize beyond R): core is ~80% language-agnostic (this repo runs it sans R); concentrate R-ness into a profile with 6 slots (verify commands, consistency gate, test doctrine, release walk, init detection, greenfield opener questions), chosen at init, recorded in CLAUDE.md section; extraction method: diff what this repo waives vs what openac uses; keep domain doctrine (oracles) orthogonal to language profile; target v0.3 after pilots harden the R slots — added 2026-07-11 — M02 pilot
- Scripts --json output mode: add a machine-readable `--json` flag to the cairn_* scripts once a consumer exists (deferred from M13 as YAGNI — today the only readers are the skills, which parse text) — added 2026-07-11 — M13 Out
- Prior-PR-comments reviewer lens: add a third distinct-evidence lens to /milestone-review's fan-out that reads review comments on previous PRs touching the modified files; marginal until a repo has a thick PR history and needs `gh` API plumbing — split 2026-07-11 from the review-pipeline candidate (→ M17/M18) — references/anthropic-code-review.md
- Mechanical coverage lint in cairn_validate.py: structural check that every acceptance criterion is referenced in a milestone's Coverage section; deferred from M18 (start with skill-text enforcement, add the script once the shape is proven) — added 2026-07-11 — M18 Out
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Baseline-commit capture at implement start: record the base SHA in the milestone header so review diffs against a fixed point (marginal — review already syncs main and diffs `main..HEAD`) — split 2026-07-11 from milestone-file-mechanics (→ M14–M16) — references/competitive-landscape.md
- read_when doc-routing frontmatter for references/: per-file frontmatter marking when to read a reference (marginal — `references/INDEX.md` already routes) — split 2026-07-11 from milestone-file-mechanics — references/competitive-landscape.md
- M06 deferred minor steals (one row per C6; promote individually if wanted): scored-rubric hygiene audit for /milestone, conflicts_with/parallel task metadata, principles-touched slot in milestone template, explicit branch↔milestone mapping, complexity-scored split advisory, tiered tool exposure, strict schemas for machine-written fragments, focus-lens subagent fan-out, search-first candidate creation — added 2026-07-11 — references/competitive-landscape.md + per-system notes
- Rulebook wording tweaks from M06 survey: cap-at-3 prioritized clarification markers at question gates (spec-kit), reading-list instruction for Explore subagents (feature-dev), state the why of different-model review; runnable commands the user is meant to copy-run go in their own fenced code block (copy button), not inline backticks (output discipline) — added 2026-07-11 — references/competitive-landscape.md + Jeff feedback 2026-07-11
- Greenfield init flow (builds on toolchain profiles): when cairn-init runs in a new/empty repo, open with a project-type chip → selects the toolchain profile → profile supplies fixed opener questions (R profile: CRAN intent, compiled code Rcpp/RcppArmadillo, statistical calcs needing oracle verification; conventions like {cli} folded into one defaults question or deferred to first milestone-plan); each question carries a marked recommended option, each option states its consequence, every answer lands in a durable home (profile slots / DESIGN Conventions / test doctrine), "undecided" defaults to the reversible choice and is banked as a candidate row; cairn-init stays tracking-only — package skeleton is the obvious first milestone — added 2026-07-11 — toolchain-profiles candidate, references/design-interview-notes.md
