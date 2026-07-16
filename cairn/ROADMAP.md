# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-16 (M63 done + archived; M58 pruned under terminal-row retention; design-interview-ingestion candidate graduated)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M64 | Durable-record preview — verbatim in-chat preview before docs-only commits | in-progress | — | high | milestones/M64-durable-record-preview.md |
| M63 | /design-interview note-and-leave ingestion — detect, formalize with #N lineage, bank the repoint | done | — | normal | milestones/archive/M63-design-interview-ingestion.md |
| M62 | Release docs — LICENSE, README worked example + framing, DRAFT removal | done | M61 | high | milestones/archive/M62-release-docs.md |
| M61 | External de-risking — env check, migration dry-run, Windows story, python CI parity | done | — | high | milestones/archive/M61-external-derisking.md |
| M60 | Git-safety hooks — force-push deny, merge-marker restore | done | — | normal | milestones/archive/M60-git-safety-hooks.md |
| M59 | Skill single-source-of-truth — canonical fallback, de-enumerated checks, migration module | done | — | normal | milestones/archive/M59-skill-single-source-of-truth.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- v1.0 release: release prep shipped (M54 positioning, M61 de-risking, M62 release docs, all done 2026-07-16); remaining = a `/cairn-release` run (generic release-walk: version bump, changelog, tag) — user-triggered — added 2026-07-16 (converted from the 2026-07-11 public-release-prep row at its graduation)
- Durable-record preview: skills author durable record text (D-entries, milestone files' plan-owned sections, LESSONS lines, archive summaries) post-gate and commit it sight-unseen — "solidify autonomously" + "deltas, not dumps" compress exactly the text that outlives the chat (bit live 2026-07-16: D-035's rationale reached main unread); add an output-discipline rule + guards requiring verbatim in-chat preview before the commit — added 2026-07-16
- Changelog profile slot: when the next non-R/non-Python profile is authored, add a changelog declaration (file name or "none") read by `/hotfix`, `/cairn-release`, and the consistency-gate — the changelog is a toolchain fact with no slot today; until then the release-prep hotfix-wording fix suffices — added 2026-07-13 — RR01 rec 11/Q2
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
