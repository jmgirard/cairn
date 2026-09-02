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
- `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_cost.py" --audit-line` — the
  most recent milestone's measured cost.

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
Then check the byte budgets by hand — `wc -c cairn/ROADMAP.md cairn/LESSONS.md`
against the tracking-rules Weight caps budgets, and `wc -l -c` on each of
the repo's doctrine modules against the budget its own header states (the
maturation exit's rule) — since `cairn_validate` does not measure them; an
overrun takes the same remedies as the line caps, surfaced as a finding for
the user, never an auto-trim.

The script also emits non-failing **advisories** (`WARN` lines, exit-code
neutral) — e.g. a milestone over the split tripwires (>7 criteria / >10
tasks). An advisory is a judgment call surfaced for the user, **not** a
mechanical problem to auto-fix: report it and let the user decide (a
milestone may legitimately exceed a tripwire with justification, or it may
want splitting via `/milestone-plan`). A `WARN` never blocks the gate.

A `release window` WARN is reported, never argued with — release timing is the user's to declare (D-050), so carry a park disposition to §3 and never treat the WARN as a prompt to get the release moving.
It also **owns** the idleness question for every release-shaped milestone,
whether or not it fired. A release the advisory has already flagged
is not re-reported under the Staleness bullet below; a release-shaped milestone
the advisory stays silent on is still the advisory's to judge, never the
bullet's — otherwise one stalled release arrives as two separate items, or the
stricter Staleness bullet nags a release the advisory's lenient any-entry rule
deliberately spared (D-017).

Run `cairn_cost.py --audit-line` and report its one line verbatim. It measures
what the most recent milestone spent — turns, cache-read, fresh input, output,
and how many subagents it spawned (whose own tokens the store does not record,
so the figure is partial by that much). It is **a reporting surface only**:
there is no threshold, no verdict, and no pass/fail attached to any number —
never treat a large figure as a finding to act on, and never propose a cap from
it. No governing mechanism over these numbers exists or is owed: D-057 closed
the stock-side size-governance program, and only a measured `cairn_cost`
regression reopens that work.

Beside it, report the rulebook's mass the same way: measure
`skills/shared/tracking-rules.md` with `wc -l -m` and report current
lines/chars and the growth since the recorded baseline —
467 lines / 43,454 chars (M166, 2026-09-02; re-seed these figures only when
a later pass changes the file deliberately). Reporting only, same boundary
as the cost line: no threshold, no verdict, no pass machinery — growth is
governed at the door (D-057), and this line keeps it visible.

The script deliberately does not judge these — do them yourself and report:

- **Staleness:** `in-progress` with no *work* entry in 14+ days — measured
  from the last work-log line that records actual progress, never the last
  line of any kind, because bookkeeping refreshes a naive clock though no work
  happened and a milestone can sit unworked while every recent entry is one
  (M88 T3, generalizing M88-D1's release-case insight).
  Clock-neutral bookkeeping — a `Depends-on` amendment, a status/mirror catch-up, and a git-reconciliation catch-up line — never resets the 14-day clock.
  Release-shaped milestones are exempt: their idleness is owned by the
  `release window` advisory above whether or not it fired, so the bullet never
  judges one. Open RB with no RR after 7+ days (remind the user to run it);
  `candidate` rows untouched ~6 months → offer a triage chip (promote / keep /
  drop — never auto-delete). A finding-absorbing candidate row — one already
  carrying deferred review findings filed from two or more distinct
  milestones — is triaged even though not untouched: pose the disposition
  chip whose options `skills/shared/records-hygiene.md` §7 states, rather
  than restating them here; a row meeting both triggers takes the
  disposition chip.
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
  drop this session's own work from the PR list, which is what the `author`
  field is for: a PR you opened, or one whose head branch is `m<nnn>-*` or
  `hotfix-*`, is cairn's own in-flight work — already tracked by its
  milestone and already reported two bullets up. Only what survives that
  filter is inbox; without it the audit re-reports the milestone PR you are
  reviewing right now and can propose adopting a PR this session authored.
  Then
  apply the search-first rule to every hit before proposing anything: sweep
  the existing `candidate` rows, `milestones/archive/`, and `DECISIONS.md`,
  so an item already covered is cross-referenced, never duplicated as a
  second row. Carry one proposed disposition per item to §3, where the user
  decides; reading is the whole mandate here — the sweep and the orphan
  read below never write to
  GitHub (no labels, comments, or closes) and never add a row unprompted;
  the one audit-path write is §3's close disposition, at the user's
  selection.
  **When `gh` is missing, unauthenticated, or the repo has no remote:**
  name which of the three it was, skip the sweep, and finish the audit.
  An unreachable inbox is a reported gap, never an audit `FAIL`.
- **Orphaned issues:** for each `done` row still in the ROADMAP table — the
  retained terminal rows bound the reads — whose archive summary's status
  line carries a `resolves` entry marked `closes`, read that issue's state
  with `gh issue view <N> --json state,url`; one still open is reported as
  an orphan: the milestone slotted as closing it is done, but the close
  never happened (a missed keyword, a merge outside cairn). A row with no
  `resolves` clause, or with `partial` entries only, reads nothing; a row
  with several `closes` entries reads each. Carry one close disposition per
  orphan to §3; the orphan read writes nothing. The inbox bullet's
  unreachable-`gh` rule applies unchanged: name which of the three it was,
  skip the reads, finish the audit.
**Replace** "Last hygiene check: YYYY-MM-DD" in ROADMAP.md with one short line naming what changed since the last check — never append to the previous stamp or demote it to a `Prior:` clause; git and `milestones/archive/` hold the older stamps.

## 3. Route

Run `cairn_next.py` for the mechanical recommendation (resume / review /
implement a workable milestone / plan) and lead the close block with it. End
with the close block (tracking-rules "Question gates and phase closes"):
recap, status line, the fenced next command(s) — the single most sensible
action's command first, each with a plain one-line label — and the
adjust-or-`/clear` safety line; no chip.
Acceptance chips (tracking-rules): a triage option that accepts an audit
conclusion carries that conclusion compactly in the chip with its full text verbatim in the chat above, best-effort (Mandated-substance rule). The commands below are state-conditional
examples for the close block's fences — only the applicable subset is offered:

- `/milestone-implement M<NNN>` — resume (an `in-progress` milestone exists)
- `/milestone-review M<NNN>` — review (a milestone sits at `review`)
- `/milestone-implement M<NNN>` — implement (a workable planned milestone
  exists — its dependencies `done`, nothing `in-progress`)
- `/milestone-plan` — plan next (nothing in flight and no workable planned
  milestone)
- a triage chip — the audit found problems needing user decisions,
  including any untriaged inbox item or orphaned issue §2 surfaced (a
  decision gate, not a route)
- Park M<NNN> as `blocked` → the release window is not open (a `release window` WARN fired in §2) — a decision put to the user, not a route

Parking sets the milestone to `blocked` and writes a work-log line naming the
maintainer's unopened release window as the blocker. It is reachable from
`planned` and from `review` (tracking-rules transitions), it closes no PR, and
it is reversed by the user declaring the window — never by cairn deciding the
release looks ready. Offer parking whenever the advisory fired, and lead the close block with it only when `cairn_next`'s own recommendation names that same release milestone.
`cairn_next` reads status and priority alone, so where it names the flagged
release its recommendation *is* the nag D-050 exists to stop and parking
displaces it. Where it names something else — an unrelated `in-progress`
milestone outranks a workable planned one in its precedence order —
that recommendation is legitimate and keeps the lead, with parking offered alongside it.

The §2 inbox sweep resolves here, and nowhere else. §2's orphan bullet
resolves here too.
Each item takes exactly one disposition — you propose, the user chooses:

- **candidate row** — the default for anything real but not urgent; one
  ROADMAP row, search-first already applied at §2.
- **`/hotfix`** — a user-visible bug, or an external PR that meets the
  hotfix bar. This is the door M73 opened; route to it rather than inventing
  a second intake mechanism.
- **`/milestone-plan`** — anything larger than the hotfix bar.
- **leave** — no row, no action, with the reason stated.
- **close** — an orphaned issue from §2's orphan bullet: only on the
  user's selection in the triage chip, close it with
  `gh issue close <N> --comment` carrying a one-line comment naming the
  archived milestone's PR; the option text names the issue and that PR.
  Not selected → the issue stays open and nothing is written.

Show every proposed disposition verbatim in the chat above and compactly in the disposition chip itself (Mandated-substance rule), never a count or a
summary of them: the dispositions are what the user is accepting, so a
paraphrase would have them approve text they never saw.

Selecting a triage-chip option acts in this session (a `→ /skill` option
invokes that skill). Never auto-proceed.
