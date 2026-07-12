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
Phase header: `# Status` → `## Snapshot` / `## Audit` / `## Route`.

**Deterministic scripts.** Snapshot, the mechanical audit checks, and the
next-action derivation are shipped as read-only python3 scripts over the
`cairn/` files — run them verbatim instead of re-deriving by hand (instant,
token-free, drift-proof):

- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_status.py"` — snapshot.
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"` — the mechanical
  consistency checks (exit 1 on any failure).
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_next.py"` — the mechanical
  next-action recommendation.

They report; they never fix or decide. The semantic checks and every
user-facing judgment below stay yours.

## Session start

Read, in order: `cairn/ROADMAP.md`, any active (`in-progress` / `blocked` /
`review`) milestone file, `cairn/DECISIONS.md`. Check `cairn/reviews/`:
if an `RR<NN>-*.md` exists for an open brief, tell the user and route to
RR ingestion (see `/milestone-brief`) before anything else.

## 1. Snapshot

Run `cairn_status.py` and report its output (counts by status, active
milestone(s), next `planned` by priority, candidate count, last hygiene
date). Add only what the script can't know: the newest work-log line of
each active milestone, and open RBs and their age.

## 2. Health audit

Run `cairn_validate.py` first. It deterministically checks: **mirror
agreement** (ROADMAP vs file header Status), **at most one `in-progress`**,
**weight caps**, **done-row retention**, **status vocabulary**, **dependency
resolution** (targets exist and aren't `dropped`), **ROADMAP↔disk orphans**,
and **ID uniqueness**. Treat every
`FAIL` as a mechanical problem: fix it (docs-only commit to main; ROADMAP
wins mirror conflicts; apply the tracking-rules cap remedies, never "let it
grow"), then re-run to confirm green.

The script deliberately does not judge these — do them yourself and report:

- **Staleness:** `in-progress` with no work-log entry in 14+ days; open RB
  with no RR after 7+ days (remind the user to run it); `candidate` rows
  untouched ~6 months → offer a triage chip (promote / keep / drop — never
  auto-delete).
- **Semantic orphans:** `done` milestones not archived; RRs not ingested;
  uncommitted changes under `cairn/`.
- **Reconciliation with git:** commits since the last work-log entry that
  aren't reflected in tracking → add a one-line catch-up entry.
- **CLAUDE.md section present and intact**; if damaged, offer repair via
  `/cairn-init`.
- A milestone at `review` with an open unmerged PR → re-check CI now
  (`gh pr checks`), report the fresh state (this is normal, not an error).
- **Untriaged inboxes:** open GitHub issues or external PRs with no
  candidate row / hotfix disposition → list them for triage.

Update "Last hygiene check: YYYY-MM-DD" in ROADMAP.md.

## 3. Route

Run `cairn_next.py` for the mechanical recommendation (resume / review /
implement a workable milestone / plan) and lead the chip with it. End with
ONE routing chip (AskUserQuestion) offering the single most sensible next
action first (recommended). The bullets below are state-conditional
examples — only the applicable subset (≤4) is offered:

- Resume M<NN> → `/milestone-implement M<NN>` (an `in-progress` milestone
  exists)
- Review M<NN> → `/milestone-review M<NN>` (a milestone sits at `review`)
- Plan the next milestone → `/milestone-plan` (nothing in flight; planned or
  candidate items exist)
- Triage the flagged items (audit found problems needing user decisions)
- Stop here

Selecting a chip invokes that skill in this session. Never auto-proceed.
