# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-16 (M57 done + archived; graduated its candidate row; pruned M52 under terminal-row retention)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M57 | references/ + linking hardening — synthesis notes, INDEX lint, dangling-ID advisory | done | — | normal | milestones/archive/M57-references-linking-hardening.md |
| M56 | LLM Wiki investigation — references/ + linking fit assessment | done | — | normal | milestones/archive/M56-llm-wiki-investigation.md |
| M55 | Milestone-file cap exempts the Review section | done | — | normal | milestones/archive/M55-milestone-file-cap.md |
| M54 | Release positioning + DESIGN refresh | done | — | high | milestones/archive/M54-release-positioning-design-refresh.md |
| M53 | Prose-guard mutation harness | done | — | high | milestones/archive/M53-prose-guard-mutation-harness.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- Public release prep: LICENSE (MIT), README worked example + a human-facing "what cairn does without asking" section (candidate framing: a governed LLM Wiki for project state — M56, references/llm-wiki.md), external de-risking (env check in cairn-init, migration dry-run mode), remove DRAFT files, tag v1.0 — **positioning + DESIGN refresh carved to M54** (RR01 rec 1/5); remainder here is rec 14/§10 — added 2026-07-11, expanded 2026-07-13/2026-07-16 — DRAFT_2 §11, reviews/archive/RR01
- Rulebook doctrine placement: move dependency-change gating + deprecation-cycle policy up from the r-package/python `test-doctrine` slots to the core rulebook (universal governance, today duplicated in 2 profiles + absent from generic); extract the Validation doctrine (+registry/sources/ingestion, ~60 lines) to `skills/shared/validation-doctrine.md` under a "new domain doctrine gets a module, not a rulebook section" norm (stays universal — D-024/D-025 is core-vs-profile, not single-file); add an oracle registry-pointer line (a repo with numeric work declares *where* its records live, shape still free) — added 2026-07-13 — RR01 rec 4/6/9
- Skill/hook single-source-of-truth: align cairn-init §0's default-branch fallback to the canonical ls-remote recipe (never guess the current branch); stop enumerating cairn_validate's checks in `/milestone-review` step 4 + `/milestone` §2 (run-and-read, drop the now-mechanical "Coverage completeness" manual bullet); add a force-push-to-default-branch deny hook (reuse commit_guard's branch machinery); add a merge_guard PostToolUse companion that restores the marker on a failed merge (M33); progressive-disclose cairn-init §2 migration protocol to a shared file read only on footprint detection — added 2026-07-13 — RR01 rec 7/8/12/13/Q6/Q9
- Name IP4 — history integrity ("never fabricated, rewritten, or renumbered": append-only logs, no-invention migration, IDs never reused): already inviolable in practice (5+ sites), naming it arms the `ip-touching` RB tripwire + cairn_impact; needs an explicit user decision + D-entry — added 2026-07-13 — RR01 rec 10/Q7
- Changelog profile slot: when the next non-R/non-Python profile is authored, add a changelog declaration (file name or "none") read by `/hotfix`, `/cairn-release`, and the consistency-gate — the changelog is a toolchain fact with no slot today; until then the release-prep hotfix-wording fix suffices — added 2026-07-13 — RR01 rec 11/Q2
- `/design-interview` note-and-leave ingestion: teach `/design-interview` to ingest a migration-preserved numbered-principles file (kept intact by M43's G-I2 note-and-leave) and drive its IP/GP formalization + the eventual in-code `PRINCIPLES.md #N` repoint (a target-repo code touch). Downstream of M43 (which writes the deferral) and gated on a real repo needing it; `/design-interview` already formalizes principles, so this is the migration-specific ingestion path, not net-new formalization — added 2026-07-12 — M43 Out (Q1), references/migration-pilot-notes.md Pilot 3 G-I2
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
- Live-openac router test: run M08's classify-first router empirically in openac (plain-conversation requests should route to the right tier/skill); openac is a separate repo, no automated evidence lands here — added 2026-07-11 — M08 Out
- Python profile Codecov/CI parallel: mirror M52's r-package CI-pair guidance in the `python` profile's `test-doctrine` slot (a covr→Codecov analog beside the "`coverage.py` is a diagnostic" line — pytest-cov + `use_github_action` equivalent), diagnostic-only, for cross-profile symmetry — added 2026-07-12 — M52 Out
