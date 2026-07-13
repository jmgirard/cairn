# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-12 (M52 r-package Codecov/CI test-doctrine done + archived; banked the python-profile Codecov parallel candidate; pruned M47 under terminal-row retention)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M52 | r-package profile — GitHub Actions CI (R-CMD-check + Codecov) | done | — | normal | milestones/archive/M52-r-profile-codecov-ci.md |
| M51 | Oracle-registry doctrine (shape-free) | done | — | normal | milestones/archive/M51-oracle-registry-doctrine.md |
| M50 | Greenfield init opener flow | done | — | normal | milestones/archive/M50-greenfield-init-openers.md |
| M49 | R fixture-provenance guard fold-in | done | — | normal | milestones/archive/M49-r-fixture-provenance-guard.md |
| M48 | Python toolchain profile | done | — | normal | milestones/archive/M48-python-toolchain-profile.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- Public release prep: LICENSE (MIT), README worked example, remove DRAFT files, tag v1.0 — added 2026-07-11 — DRAFT_2 §11
- `/design-interview` note-and-leave ingestion: teach `/design-interview` to ingest a migration-preserved numbered-principles file (kept intact by M43's G-I2 note-and-leave) and drive its IP/GP formalization + the eventual in-code `PRINCIPLES.md #N` repoint (a target-repo code touch). Downstream of M43 (which writes the deferral) and gated on a real repo needing it; `/design-interview` already formalizes principles, so this is the migration-specific ingestion path, not net-new formalization — added 2026-07-12 — M43 Out (Q1), references/migration-pilot-notes.md Pilot 3 G-I2
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
- Live-openac router test: run M08's classify-first router empirically in openac (plain-conversation requests should route to the right tier/skill); openac is a separate repo, no automated evidence lands here — added 2026-07-11 — M08 Out
- Python profile Codecov/CI parallel: mirror M52's r-package CI-pair guidance in the `python` profile's `test-doctrine` slot (a covr→Codecov analog beside the "`coverage.py` is a diagnostic" line — pytest-cov + `use_github_action` equivalent), diagnostic-only, for cross-profile symmetry — added 2026-07-12 — M52 Out
