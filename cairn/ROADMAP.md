# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-16 (M61 done + archived; M56 pruned under terminal-row retention; python-Codecov candidate graduated)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M62 | Release docs — LICENSE, README worked example + framing, DRAFT removal | planned | M61 | high | milestones/M62-release-docs.md |
| M61 | External de-risking — env check, migration dry-run, Windows story, python CI parity | done | — | high | milestones/archive/M61-external-derisking.md |
| M60 | Git-safety hooks — force-push deny, merge-marker restore | done | — | normal | milestones/archive/M60-git-safety-hooks.md |
| M59 | Skill single-source-of-truth — canonical fallback, de-enumerated checks, migration module | done | — | normal | milestones/archive/M59-skill-single-source-of-truth.md |
| M58 | Rulebook doctrine placement — governance up, validation doctrine out, registry pointer | done | — | normal | milestones/archive/M58-rulebook-doctrine-placement.md |
| M57 | references/ + linking hardening — synthesis notes, INDEX lint, dangling-ID advisory | done | — | normal | milestones/archive/M57-references-linking-hardening.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- Public release prep: **M61 (de-risking) shipped 2026-07-16; M62 (LICENSE, README, DRAFT removal) remains planned**; v1.0 tag = a `/cairn-release` run after M62 merges; positioning + DESIGN refresh shipped via M54 — row graduates when M62 ships — added 2026-07-11 — DRAFT_2 §11, reviews/archive/RR01 rec 14/§10
- Changelog profile slot: when the next non-R/non-Python profile is authored, add a changelog declaration (file name or "none") read by `/hotfix`, `/cairn-release`, and the consistency-gate — the changelog is a toolchain fact with no slot today; until then the release-prep hotfix-wording fix suffices — added 2026-07-13 — RR01 rec 11/Q2
- `/design-interview` note-and-leave ingestion: teach `/design-interview` to ingest a migration-preserved numbered-principles file (kept intact by M43's G-I2 note-and-leave) and drive its IP/GP formalization + the eventual in-code `PRINCIPLES.md #N` repoint (a target-repo code touch). Downstream of M43 (which writes the deferral) and gated on a real repo needing it; `/design-interview` already formalizes principles, so this is the migration-specific ingestion path, not net-new formalization — added 2026-07-12 — M43 Out (Q1), references/migration-pilot-notes.md Pilot 3 G-I2
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
