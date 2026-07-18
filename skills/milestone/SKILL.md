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
Chapter markers: mark a chapter at each phase transition (session start implicit).

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

Run `cairn_validate.py` first and
read its output — one line per check; never restate or recall its
internals (a restated list is a stale-count trap, M28). Treat every
`FAIL` as a mechanical problem: fix it (docs-only commit to the default
branch; ROADMAP wins mirror conflicts; apply the tracking-rules cap
remedies, never "let it grow"), then re-run to confirm green. **Exception — a `scaffold present`
FAIL** means the repo's §1 scaffold has drifted behind the spec (a missing
tracking file or ignore entry, typically because the repo adopted cairn
before a later scaffold addition); fix it by running `/cairn-init` (repair
mode), which is the sole scaffolder — never hand-create the pieces here.

The script also emits non-failing **advisories** (`WARN` lines, exit-code
neutral) — e.g. a milestone over the split tripwires (>7 criteria / >10
tasks). An advisory is a judgment call surfaced for the user, **not** a
mechanical problem to auto-fix: report it and let the user decide (a
milestone may legitimately exceed a tripwire with justification, or it may
want splitting via `/milestone-plan`). A `WARN` never blocks the gate.

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
- **Untriaged inboxes:** open GitHub issues and external PRs carrying no
  candidate row or hotfix disposition yet. Enumerate both inboxes —
  `gh issue list --state open --json number,title,url` for issues,
  `gh pr list --state open --json number,title,url,author` for PRs — then
  apply the search-first rule to every hit before proposing anything: sweep
  the existing `candidate` rows, `milestones/archive/`, and `DECISIONS.md`,
  so an item already covered is cross-referenced, never duplicated as a
  second row. Carry one proposed disposition per item to §3, where the user
  decides; reading the inbox is the whole mandate here — never write to
  GitHub (no labels, comments, or closes) and never add a row unprompted.
  **When `gh` is missing, unauthenticated, or the repo has no remote:** name
  which of the three it was, skip the sweep, and carry on with the rest of
  the audit — an unreachable inbox is a reported gap, never an audit `FAIL`.

Update "Last hygiene check: YYYY-MM-DD" in ROADMAP.md.

## 3. Route

Run `cairn_next.py` for the mechanical recommendation (resume / review /
implement a workable milestone / plan) and lead the chip with it. End with
ONE routing chip (AskUserQuestion) offering the single most sensible next
action first (recommended).
Acceptance chips (tracking-rules): a triage option that accepts an audit
conclusion shows that conclusion's text verbatim above the chip. The bullets below are state-conditional
examples — only the applicable subset (≤4) is offered:

- Resume M<NN> → `/milestone-implement M<NN>` (an `in-progress` milestone
  exists)
- Review M<NN> → `/milestone-review M<NN>` (a milestone sits at `review`)
- Plan the next milestone → `/milestone-plan` (nothing in flight; planned or
  candidate items exist)
- Triage the flagged items (audit found problems needing user decisions)
- Stop here

Selecting a chip invokes that skill in this session. Never auto-proceed.
