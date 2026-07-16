# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-16 (M64 done + archived; M59 pruned under terminal-row retention; durable-record-preview candidate graduated)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M64 | Durable-record preview — verbatim in-chat preview before docs-only commits | done | — | high | milestones/archive/M64-durable-record-preview.md |
| M63 | /design-interview note-and-leave ingestion — detect, formalize with #N lineage, bank the repoint | done | — | normal | milestones/archive/M63-design-interview-ingestion.md |
| M62 | Release docs — LICENSE, README worked example + framing, DRAFT removal | done | M61 | high | milestones/archive/M62-release-docs.md |
| M61 | External de-risking — env check, migration dry-run, Windows story, python CI parity | done | — | high | milestones/archive/M61-external-derisking.md |
| M60 | Git-safety hooks — force-push deny, merge-marker restore | done | — | normal | milestones/archive/M60-git-safety-hooks.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- v1.0 release: release prep shipped (M54 positioning, M61 de-risking, M62 release docs, all done 2026-07-16); remaining = a `/cairn-release` run (generic release-walk: version bump, changelog, tag) — user-triggered — added 2026-07-16 (converted from the 2026-07-11 public-release-prep row at its graduation)
- Gate-time conclusion preview: a chip can ask the user to accept a review's or subagent's conclusion whose substance never appeared in chat — "Chips carry choices, not evidence" states the principle centrally but has no per-skill wiring or guard, and summarize-don't-paste pressure compresses the very text being accepted (hit live in circumplex 2026-07-16: a /milestone-plan session ran a review, then asked acceptance of its unseen conclusion); extend M64's preview discipline to acceptance chips — the conclusion's full text or verbatim findings shown above any chip that asks to accept/approve it, wired per-skill + guarded (the D-021/M64 pattern) — added 2026-07-16
- Changelog profile slot: when the next non-R/non-Python profile is authored, add a changelog declaration (file name or "none") read by `/hotfix`, `/cairn-release`, and the consistency-gate — the changelog is a toolchain fact with no slot today; until then the release-prep hotfix-wording fix suffices — added 2026-07-13 — RR01 rec 11/Q2
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
