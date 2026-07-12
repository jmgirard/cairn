# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-12 (M26 done+archived; M21 row pruned per 5-done retention)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M26 | Lock the routing-chip mandate; exempt review as the chip-less phase | done | — | normal | milestones/archive/M26-routing-chip-mandate-lock.md |
| M27 | Desktop TOC pickup of the `##` phase headers | in-progress | — | low | milestones/M27-desktop-toc-header-pickup.md |
| M25 | Parameterize the default branch in the operational skill steps | done | M22 | normal | milestones/archive/M25-default-branch-operational-skills.md |
| M24 | Scaffold-drift detection in the audit | done | — | normal | milestones/archive/M24-scaffold-drift-check.md |
| M23 | Migration-protocol §2 guidance hardening | done | M22 | normal | milestones/archive/M23-migration-guidance.md |
| M22 | Generalize cairn beyond `main`; recalibrate the mature-repo CLAUDE.md cap | done | — | normal | milestones/archive/M22-mature-repo-defaults.md |

## Candidates

- Extend the routing-chip mandate lock to `milestone-brief`: its RR-ingest phase ends with a "Routing chip" (step 5) that doesn't name `AskUserQuestion`, so M26's guard (`TestRoutingChipMandate`) leaves it uncovered — add the token + fold it into `NON_REVIEW_CHIP_SKILLS`; M26 scoped it out on a wrong premise ("ends on RR-ingest" — the ingest itself ends on a routing chip) — added 2026-07-12 — M26 review F2 (scored 65)
- `cairn_validate` ISO-date scan false-positives on R CMD check result notation (three slash-separated counts, errors/warnings/notes, commonly all-zero) — the `\d{1,4}/\d{1,2}/\d{1,4}` slash-date pattern matches it; a clean fix is ambiguous (requiring a 4-digit year regresses on 2-digit-year dates), so it needs deliberate design not a reflexive regex tweak — added 2026-07-12 — M21 circumplex pilot G-C2
- Migration guidance for a mature backlog vs the <60-line ROADMAP cap: a large parking-lot (continuous track + deferred review findings + pre-release items) blows the candidate budget one-row-per-item; document the "cluster related backlog into grouped candidate rows pointing at the entombed legacy ROADMAP" remedy in §5/§6 — added 2026-07-12 — M21 circumplex pilot G-C4
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
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
