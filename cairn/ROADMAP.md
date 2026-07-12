# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-12 (M35 — done; pruned M30 to the 5-terminal cap; graduated 2 fulfilled candidates)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M36 | On-main commit-guard hook | planned | — | normal | milestones/M36-on-main-commit-guard.md |
| M34 | Mechanical coverage-map lint in cairn_validate | done | — | normal | milestones/archive/M34-coverage-map-lint.md |
| M35 | Rulebook & doc-wording polish batch | done | — | normal | milestones/archive/M35-rulebook-doc-polish.md |
| M33 | Assess ackwards' oracle discipline and fold its generalizable core into cairn | done | — | normal | milestones/archive/M33-oracle-discipline-coordination.md |
| M32 | Fold dropped rows into the ROADMAP retention cap (done-row → terminal-row) | done | — | normal | milestones/archive/M32-terminal-row-retention.md |
| M31 | Mark the opening phase — drop the "session start implicit" carve-out | dropped | — | normal | milestones/archive/M31-opening-phase-chapter-marker.md |

## Candidates

- Adopt an oracle registry (`ORACLES.md`) as a cairn tracking file: ackwards' M57 proved a per-oracle registry (ID, type, asserting test:line, source, provenance) auditable against the ≥2-independent-types bar; adopting it into cairn means the D-015/M16 four-wiring-points path (file-map + weight-caps, `LINE_CAPS`, date-scan) plus a cap and an opt-in decision. Domain-specific (only statistical packages need it) and entangled with the toolchain-profiles split, which wants domain doctrine (oracles) orthogonal to the language profile — promote *with* that work, not standalone — added 2026-07-12 — M33 Out, references/oracle-discipline-notes.md
- R-profile provenance guard: generalize ackwards' `provenance`-attr fixture convention + `test-oracle-provenance.R` guard (blocks any fixture lacking a structured provenance attr naming its `data-raw/` generator + source) into an R toolchain-profile slot; R/testthat-specific, so it belongs on the language side of the toolchain-profiles domain/language split — added 2026-07-12 — M33 Out, references/oracle-discipline-notes.md
- Descriptive label for a session's opening phase in the Claude Code TOC: today the opening phase shows as the generic implicit "Session Start" node, and a single-phase session that never calls `mark_chapter` shows an empty TOC. Marking the first message could give it a descriptive label / guarantee a node — but the `mark_chapter` docstring discourages marking the first message and the result is only verifiable by live Desktop probing (not observable agent-side, D-020). Promote only with a live-probe plan; keep the correct carve-out until then — added 2026-07-12 — M31 dropped (premise refuted)
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
- Public release prep: LICENSE (MIT), README worked example, remove DRAFT files, tag v1.0 — added 2026-07-11 — DRAFT_2 §11
- Live-openac router test: run M08's classify-first router empirically in openac (plain-conversation requests should route to the right tier/skill); openac is a separate repo, no automated evidence lands here — added 2026-07-11 — M08 Out
- Toolchain profiles (generalize beyond R): core is ~80% language-agnostic (this repo runs it sans R); concentrate R-ness into a profile with 6 slots (verify commands, consistency gate, test doctrine, release walk, init detection, greenfield opener questions), chosen at init, recorded in CLAUDE.md section; extraction method: diff what this repo waives vs what openac uses; keep domain doctrine (oracles) orthogonal to language profile; target v0.3 after pilots harden the R slots — added 2026-07-11 — M02 pilot
- Scripts --json output mode: add a machine-readable `--json` flag to the cairn_* scripts once a consumer exists (deferred from M13 as YAGNI — today the only readers are the skills, which parse text) — added 2026-07-11 — M13 Out
- Prior-PR-comments reviewer lens: add a third distinct-evidence lens to /milestone-review's fan-out that reads review comments on previous PRs touching the modified files; marginal until a repo has a thick PR history and needs `gh` API plumbing — split 2026-07-11 from the review-pipeline candidate (→ M17/M18) — references/anthropic-code-review.md
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- M06 deferred minor steals (one row per C6; promote individually if wanted): scored-rubric hygiene audit for /milestone, conflicts_with/parallel task metadata, principles-touched slot in milestone template, explicit branch↔milestone mapping, complexity-scored split advisory, tiered tool exposure, strict schemas for machine-written fragments, focus-lens subagent fan-out, search-first candidate creation — added 2026-07-11 — references/competitive-landscape.md + per-system notes
- Greenfield init flow (builds on toolchain profiles): when cairn-init runs in a new/empty repo, open with a project-type chip → selects the toolchain profile → profile supplies fixed opener questions (R profile: CRAN intent, compiled code Rcpp/RcppArmadillo, statistical calcs needing oracle verification; conventions like {cli} folded into one defaults question or deferred to first milestone-plan); each question carries a marked recommended option, each option states its consequence, every answer lands in a durable home (profile slots / DESIGN Conventions / test doctrine), "undecided" defaults to the reversible choice and is banked as a candidate row; cairn-init stays tracking-only — package skeleton is the obvious first milestone — added 2026-07-11 — toolchain-profiles candidate, references/design-interview-notes.md
