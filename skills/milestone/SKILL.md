---
name: milestone
description: Project status snapshot, tracking health audit, and next-action routing for cairn repos. Use when the user asks where the project stands, what to do next, "project status", "health check", when returning after time away, or when reconciliation between tracking files and git is needed.
argument-hint: ""
---

# /milestone — status, health audit, next action

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it. This skill is read-mostly: it fixes mechanical tracking problems
immediately, reports everything else, and never starts implementation work
itself — it routes.
Stage banner: `[cairn · milestone · <snapshot|audit|route>]`.

## Session start

Read, in order: `cairn/ROADMAP.md`, any active (`in-progress` / `blocked` /
`review`) milestone file, `cairn/DECISIONS.md`. Check `cairn/reviews/`:
if an `RR<NN>-*.md` exists for an open brief, tell the user and route to
RR ingestion (see `/milestone-brief`) before anything else.

## 1. Snapshot

Report concisely: current `in-progress` / `blocked` / `review` milestones
(one line each, with the newest work-log line); the next `planned`
milestones by priority; open RBs and their age; count of candidates.

## 2. Health audit

Fix mechanical problems immediately (docs-only commit to main); report the
rest. Check:

- **Consistency:** ROADMAP vs milestone-file header mirrors agree (ROADMAP
  wins; fix mirrors); at most one `in-progress`.
- **Weight caps** (per tracking-rules) — apply the named remedies, never
  "let it grow".
- **Dangling dependencies:** every `Depends on:` resolves to a live or
  `done` milestone; flag references to `dropped`/nonexistent IDs for
  re-wiring.
- **Staleness:** `in-progress` with no work-log entry in 14+ days; open RB
  with no RR after 7+ days (remind the user to run it); `candidate` rows
  untouched ~6 months → offer a triage chip (promote / keep / drop — never
  auto-delete).
- **Orphans:** `done` milestones not archived; RRs not ingested; milestone
  files missing from ROADMAP or vice versa; uncommitted changes under
  `cairn/`.
- **Reconciliation with git:** commits since the last work-log entry that
  aren't reflected in tracking → add a one-line catch-up entry.
- **ID uniqueness:** no M-number appears twice across active + archive.
- **CLAUDE.md section present and intact**; if damaged, offer repair via
  `/cairn-init`.
- A milestone at `review` with an open unmerged PR → re-check CI now
  (`gh pr checks`), report the fresh state (this is normal, not an error).
- **Untriaged inboxes:** open GitHub issues or external PRs with no
  candidate row / hotfix disposition → list them for triage.

Update "Last hygiene check: YYYY-MM-DD" in ROADMAP.md.

## 3. Route

End with ONE routing chip (AskUserQuestion) offering the single most
sensible next action first (recommended). The bullets below are
state-conditional examples — only the applicable subset (≤4) is offered:

- Resume M<NN> → `/milestone-implement M<NN>` (an `in-progress` milestone
  exists)
- Review M<NN> → `/milestone-review M<NN>` (a milestone sits at `review`)
- Plan the next milestone → `/milestone-plan` (nothing in flight; planned or
  candidate items exist)
- Triage the flagged items (audit found problems needing user decisions)
- Stop here

Selecting a chip invokes that skill in this session. Never auto-proceed.
