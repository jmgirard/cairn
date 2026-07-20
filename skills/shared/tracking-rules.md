# Tracking rules (shared by all cairn skills)

Read this before touching any tracking file. Every cairn skill obeys
these rules; skills state their own workflow but never restate or override
this rulebook. Repo-specific hard rules in the repo's CLAUDE.md and
conventions in `cairn/DESIGN.md` bind in addition to (never instead of)
these rules.

## File map and ownership boundaries

All project state lives in markdown under `cairn/`. Substance lives in the
owner; any other file gets at most a one-line cross-reference.

| File | Owns | Does NOT own |
|---|---|---|
| `CLAUDE.md` | Dev commands, repo-specific hard rules, pointers to `cairn/` | Status, TODOs, architecture rationale, history — anything time-varying rots here |
| `cairn/DESIGN.md` | Purpose & scope, function families, conventions, numbered principles (GP/IP), architecture as it **is**, known issues | Future work, task lists, status |
| `cairn/PROFILE.md` | The repo's toolchain profile — the seven language/toolchain slots the operational skills read (see "Toolchain profiles") | Domain doctrine (oracles are universal), status, tasks, decisions |
| `cairn/ROADMAP.md` | The milestone index — **the only authority on status** | Task details, acceptance criteria, narrative |
| `cairn/milestones/M<NN>-<slug>.md` | One milestone's goal, scope (In/Out), acceptance criteria, tasks, work-log, review evidence | Status authority (header is a mirror; ROADMAP wins any conflict — fix the mirror immediately, before other work) |
| `cairn/milestones/archive/` | Compressed ≤25-line summaries of done/dropped milestones | Active work |
| `cairn/DECISIONS.md` | Append-only cross-cutting decisions (D-001, …), never renumbered — superseded by new entries | Milestone-local decisions (those live in the milestone file); deferrals ("not now" is a ROADMAP fact, not a decision) |
| `cairn/LESSONS.md` | Durable, capped repo lessons (build quirks, testing tricks) — captured at milestone end, surfaced at plan time; current knowledge, so a lesson proven false is corrected in place and marked (D-045), and retired once a test enforces it, another file owns it, or a matured family graduates whole into a doctrine module (D-051, D-055) | Status, decisions (a *choice* is a D-entry), per-milestone task notes |
| `cairn/reviews/` | RB<NN> briefs and RR<NN> reports for Fable escalation (+ `archive/` for resolved pairs) | Anything else |
| `cairn/references/` | Source notes (`<citekey>.md`), synthesis notes (cross-source analyses — fit assessments, surveys, pilot ledgers), `INDEX.md` (one line per committed page), the gitignored source shelf `sources/` (renamed from `pdf/` at M79 — the shelf holds any source, not only PDFs) | Anything else |
| `cairn/legacy/` | Entombed pre-migration tracking files, verbatim | Anything live |

Boundary rule: **Architecture → DESIGN · Status → ROADMAP · Tasks →
milestone files · Decisions → DECISIONS · Lessons → LESSONS · History →
archive + git log.**

Repo-specific extra files in `cairn/` are allowed (spec docs, coverage
matrices); they declare their own scope and must not claim another file's
ownership.

### Milestone-file section ownership

Within a milestone file, each section has a writing skill — a phase skill
never rewrites another phase's section. Write-modes: **create** (authored
once by the named skill), **append-only** (lines added, never rewritten),
**amend-via-gate** (changed only through the implement amendment protocol,
`/milestone-implement` step 6, or a review send-back — always with a work-log
line), **mirror-update** (the status field is synced to `ROADMAP.md` by
whichever skill makes the transition; ROADMAP wins any conflict),
**check-off** (implement ticks task checkboxes and makes minor task edits),
**exclusive** (only the named skill ever writes it).

| Section | Writing skill | Write-mode |
|---|---|---|
| Status (header) | the transitioning skill (plan → implement → review) | mirror-update |
| Priority, Depends on, Principles touched (header) | plan | create; amend-via-gate |
| Branch/PR (header) | implement (branch), review (PR URL) | create |
| Goal | plan | create; a wrong goal returns to plan, never edited in place |
| Scope (In/Out) | plan | create; amend-via-gate |
| Acceptance criteria | plan | create; amend-via-gate — review reads, never reinterprets; under AC fencing review check-offs a verified criterion box (a verification mark, not a text change) |
| Coverage (criterion→task map) | plan | create; amend-via-gate — review reads to fence evidence, never reinterprets |
| Tasks | plan (create), implement (check-off, minor edits) | create; check-off; amend-via-gate for substantive change |
| Work log | any skill | append-only |
| Decisions (milestone-local) | implement, review | append-only |
| Review | review | exclusive |

**AC fencing (review discipline).** At `/milestone-review`, an
acceptance-criterion checkbox is ticked only against fresh evidence recorded
in the Review section — no evidence line, no tick (review ticks the box as a
verification mark; the criterion wording stays plan-owned, amended only via
gate) — and every criterion must
map to ≥1 existing task via the Coverage section. An unmapped criterion (or
one mapped to a task that isn't there) is a gate failure, returned to
`/milestone-implement` for a gated Coverage amendment, never patched
review-side. Fencing enforces what the Coverage map plans: evidence gates the
checkbox, coverage gates the plan.

DESIGN.md principles come in two strengths: **GP<n> — Guiding Principle**, a
default stance that may be traded off with stated justification; **IP<n> —
Inviolable Principle**, a hard constraint never violated in implementation —
changing one requires an explicit user decision recorded as a D-entry.
Ordering: the IP block comes first, then GPs; numbers run within each type
(IP1…, GP1…) and are never reused or renumbered — retiring a principle
takes a D-entry, and its number stays retired.

## Weight caps

- the cairn `## Project tracking` section of `CLAUDE.md` < 30 lines (the repo's
  own dev doctrine outside that section is not cairn's to cap — D-018) ·
  `ROADMAP.md` < 60 lines · `LESSONS.md` < 50 lines · `PROFILE.md` < 120 lines ·
  archived summary ≤ 25 lines.
- **Two axes, one file.** Those caps count **items**: `ROADMAP.md` and
  `LESSONS.md` are parsed one item per line (rows read positionally; D-015
  makes a lesson one line), so a line count measures rows and lessons and is
  structurally blind to prose accumulating *inside* a line — cairn's own
  `LESSONS.md` sat at 49 lines, one under its cap, across six milestones while
  its character mass grew 13% and nothing reported it. The second axis is
  **weight** — total character mass over the same whole file, reported by
  `cairn_validate`'s `record density` advisory against
  per-file character thresholds — `ROADMAP.md` < 21,000 · `LESSONS.md` < 20,500
  — each the mass its own line cap permits at measured item length: non-item
  mass plus capacity × the measured mean item length, rounded up, where capacity
  is (line cap − 1, since the cap fails at `>=`) less the file's fixed non-item
  lines. Measure that mean, never assume one: compression is
  the weight remedy and consolidating items raises the mean, so a mean carried
  over from last time is stale by construction — and a threshold set below what
  the line cap permits stops backstopping that cap and silently becomes the real
  one, firing at ordinary density (M87, superseding M84-D1's assumed means,
  which did exactly that on both files).
  The two axes take opposite remedies: an over-count file graduates or prunes items, an over-weight file compresses them in place.
  The two also differ in severity, and the labels say which is which: the item axis is the hard `weight caps` CHECK and still FAILs the gate, while the weight axis is the `record density` advisory and only ever WARNs.
  Density warns rather than fails because an item count is a structural fact but
  "too dense" is a judgment about prose quality — the same call the
  `references staleness` advisory makes.
  **The per-line axis covers non-item lines only, and deliberately never item lines** (D-052, narrowing M84's blanket rejection).
  Item lines stay exempt for M84's original reason, which survives the narrowing: pressure on individual line length would reward splitting an item across lines and corrode the one-item-per-line format both parsers depend on.
  A non-item line — heading, preamble, stamp, HTML comment — carries no such
  format to corrode, and prose accretes there unseen by *both* whole-file axes:
  the item cap counts lines and the density threshold counts whole-file mass, so
  one line reached 3,152 characters in an adopting repo with every gate green,
  and a review hygiene pass then rewrote that stamp and still left it at 2,568
  (2026-07-19; M93). Non-item lines are capped at `NON_ITEM_LINE_CAP` (< 400 characters),
  reported under the same `record density` advisory at the same WARN severity.
- a live milestone file's **plan-owned body < 150 lines** — everything before
  the review-exclusive `## Review` section, less the `## Work log`.
  The cap-exempt sections are exactly `## Review` (review-owned, M55) and `## Work log` (history under D-045, D-046); every other plan-owned section counts.
  They are exempt for two different reasons. `## Review` is exempt so that
  review evidence never scrambles plan-owned content (M55): it accumulates at
  review time and no longer competes with Scope, AC, or Coverage for the budget.
  The `## Work log` is exempt because D-045 makes it history — never edited — so counting it could leave an over-cap file fixable only by an edit IP4 forbids (D-046).
  A file with no `## Review` section counts up to EOF — still less its work log,
  which is exempt wherever it sits.
- Work-log entries are one line each — a hard-wrapped entry costs several lines
  of a budget it no longer pays into, so `cairn_validate`'s `work-log format`
  advisory WARNs on any work-log line that is not a one-line `- ` entry. It
  warns and never fails: the cap no longer counts the section, so a wrap is
  untidiness, not damage (D-046). Never paste command output or subagent
  transcripts into tracking files — summarize.
- Remedies when a cap is hit (never "let it grow"): over-count ROADMAP →
  graduate or prune candidates and enforce terminal-row retention — and when
  a large legacy or parking-lot backlog blows the cap one-row-per-item,
  cluster related items into grouped candidate rows that point at the
  entombed legacy `ROADMAP.md` instead of listing each (M21 G-C4); over-cap
  milestone → the `cairn_validate` breakdown names the heaviest plan-owned
  section and the lines to shed, so compress that one section in a single
  rewrite, never a nibble-and-recount loop; the breakdown lists only trimmable
  sections — both cap-exempt sections are omitted, so the remedy can never aim
  at history (D-046); cross-reference a durable record
  rather than restate its substance in the milestone (a milestone restating a
  DECISIONS entry is the classic overrun); split it or move reference material
  to `references/` only when no single section can carry the cut; over-cap
  cairn CLAUDE.md section → trim it back to the template (it is routing
  boilerplate, not a content home); other CLAUDE.md content → its owner per
  the table above.
- Terminal-row retention: the ROADMAP table keeps only the 5 most recent
  terminal (`done` or `dropped`) rows combined; prune older ones as they
  accumulate — archive files and git history stay authoritative. Standing
  hygiene, not just a cap remedy.
- **The `Last hygiene check` stamp is replaced each pass, never appended to** — it records the CURRENT check only, and no `Prior:` or `Earlier:` chain accumulates behind it.
  The stamp is current knowledge (D-045), not history, so overwriting it is not
  an IP4 edit: `git log` holds every earlier stamp verbatim and
  `milestones/archive/` holds the detail behind it, which is the same boundary
  terminal-row retention already runs on. Keep it to one short line naming what
  changed since the last check; the `NON_ITEM_LINE_CAP` axis of the
  `record density` advisory backstops it at 400 characters (D-052, M93).

## Universal tracking rules

- **Tracking travels with code.** Every commit that changes code also updates
  the milestone checkboxes/work-log in the same commit.
- **Absolute dates only** (YYYY-MM-DD). Never "yesterday" or "last week".
- **Append, don't rewrite.** Work-logs and DECISIONS.md are append-only;
  supersede, never edit history. Never fabricate history — if there is a
  gap, add one catch-up entry summarizing `git log`.
- **Correcting a record proven false.** The tracking files split by purpose,
  and the split sets the remedy: current knowledge is corrected in place,
  history is superseded and never edited.
  History — `DECISIONS.md`, work-logs, milestone IDs, `milestones/archive/`,
  `reviews/archive/`, entombed `legacy/` files — records what was decided or
  done at a time, and is never edited (IP4).
  Current knowledge — `LESSONS.md`, `references/` pages, `DESIGN.md`, `ROADMAP.md` — records what is true *now* and is read to act on,
  so a line later proven
  false is fixed where it sits, the correction marked (`(M71, corrected M75)`)
  and git holding the original. `ROADMAP.md` is the clearest case and was the
  one D-045 left unenumerated (D-052): it is the sole authority on *current*
  status, every transition rewrites a row in place, and terminal-row retention
  prunes rows outright on the grounds that archive and git stay authoritative. **Exception — `DESIGN.md`'s IP/GP block:** a
  wrong *principle* is not a wrong fact, and still changes only by explicit
  user decision recorded as a D-entry (see the IP/GP paragraph above).
  Ruled out: appending a correction while leaving the wrong text readable —
  a false lesson is harvested into every later plan (D-045).
- **Retiring a lesson that no longer earns its line.** `LESSONS.md` is capped, so
  it needs an outflow and not only a ceiling. Three criteria retire a lesson (D-051, D-055):
  **enforcement — a test fails on the mistake the lesson warns about**, where the
  discriminating word is *fails* and never *exists*, since a guard in the same area
  is not enforcement when the lesson teaches the judgment that guard does not make;
  and **ownership — another tracking file's slot owns the content**, where
  **the retiring milestone may *move* the content there rather than only find it already duplicated**;
  and **maturation — a stabilized family graduates whole into a doctrine module** (D-055), where the bar is conjunctive: it teaches transferable authoring or verifying craft rather than a fact about this repo's tools, it has been extended or consolidated at least twice, and neither enforcement nor ownership offers it an exit today.
  Maturation moves content rather than removing it, which is why it is not the second record D-051 rejected: the source line is deleted in the same pass, so exactly one record exists at every moment.
  **A lesson covered only in part is trimmed to its uncovered remainder**, never kept whole.
  **A retired lesson leaves no line behind — the retiring milestone's archive summary names what it graduated**, and git holds the original.
  **Retirement is not correction: a retired lesson is redundant, a corrected one was false** — conflating the two would license deleting a lesson merely disputed.
  The check runs at `/milestone-review` post-merge hygiene beside capture,
  **scoped to what the milestone shipped, never as a full re-sweep**; D-015's
  prune-the-stalest stays the last resort when retirement cannot free the budget.
- **Stop points are commit points.** Never end a session or turn with
  uncommitted work — checkpoint-commit code and tracking together (even
  half-done, marked as such) so any future session resumes statelessly.
- **Git is ground truth for code.** Commits made outside the system are
  reconciled with a catch-up work-log line, never retroactive rewriting.
- **User overrides are logged, never resisted.** If the user says to skip a
  gate or bend a rule, comply and record it in the work-log ("merged without
  CI at user request, YYYY-MM-DD"). An honest record keeps the next session
  from mistaking an exception for a precedent.
- **Dependency changes are never unilateral.** Adding, removing, or re-pinning
  a dependency — in any toolchain — goes through a question gate and is
  recorded as a D-entry; the active profile's `test-doctrine` slot names the
  mechanical dependency surface.
- **Breaking changes to public behavior follow a deprecation cycle** unless
  the project is pre-1.0 and the user explicitly waives it; the active
  profile names the language's deprecation mechanics.
- **Release timing is user-declared, never agent-proposed** (D-050). cairn never proposes a release, never plans a release milestone unprompted, and never nominates one as the next action.
  A release's readiness condition is a maintainer judgment about when to ship, never a dependency graph going green — deps going green says only that the *bundle* is complete.
  So a release milestone whose window the maintainer has not opened is parked as `blocked`, where no routing surface nominates it.
  It stays parked until the maintainer opens the window. The release *act* is already
  user-triggered — `/cairn-release` never self-submits — and this rule extends
  the same authority upstream, to whether the release is even queued.
- **Tracking files outrank memory.** Claude's persistent memory never holds
  project state (status, milestones, decisions, architecture). Memory is for
  meta-context only; `cairn/` files win any conflict.
- **Memory intake gate (GP4).** Before writing to per-user memory, apply the
  GP4 test to decide where the content actually belongs: durable project
  knowledge (decisions, conventions, architecture, status) → the `cairn/`
  files; a generalizable conduct or plugin defect → the plugin (skills,
  `tracking-rules.md`, guard tests); only genuinely per-user meta-context
  stays in memory. When a memory write happens inside a cairn repo the
  `memory_guard.py` PreToolUse hook injects this reminder as a non-blocking
  nudge — it prompts the test, it does not make the call.

## Milestone IDs and status

- IDs are `M<NN>` (zero-padded to two digits), assigned at planning time,
  monotonically increasing, **never reused** — including dropped milestones.
  Past M99, IDs simply grow (M100).
- **No completion-order requirement.** Work order is governed only by
  `Depends on:` (a milestone is workable only when its dependencies are
  `done`) and `Priority:` (high / normal / low).
- The ROADMAP index is grouped by status, not sorted by ID.
- Bare `M<NN>` is repo-local. Whenever more than one cairn-tracked repo is
  in scope (cross-repo conversation, briefs, commits touching two repos),
  qualify the ID with the repo name — "tidymedia M07", never bare "M07".
- User-facing materials (NEWS.md, README, vignettes, pkgdown) never
  reference milestone numbers.

Status vocabulary — exactly these seven, lowercase:

| Status | Meaning | Set by (gatekeeper) |
|---|---|---|
| `candidate` | Idea captured as a ROADMAP row; usually no file, no ID yet | anyone, any time |
| `planned` | File exists: goal, In/Out scope, verifiable criteria, ordered tasks, dependencies | `/milestone-plan` only |
| `in-progress` | Being worked on a branch. **At most ONE at a time.** | `/milestone-implement` only |
| `blocked` | Waiting on something external — a maintainer who has not opened the release window counts; work-log line names the blocker | any skill, reason logged |
| `review` | Tasks done, local checks clean; awaiting verification + merge approval | `/milestone-implement` on completion |
| `done` | Every criterion executed with fresh evidence; PR merged; file archived | `/milestone-review` only |
| `dropped` | Deliberately abandoned; one-line reason archived | user decision, via any skill |

Transitions: `candidate → planned → in-progress ⇄ blocked;
in-progress → review → done` (review failures return to `in-progress`).
Parking reaches every routable status: `planned → blocked` and `review → blocked` are both legal, because a milestone can wait on a human before work starts as well as after it finishes.
Anything can go to `dropped`. No skipping except `candidate → dropped`.

## Sizing and the work tiers

One milestone = one reviewable PR ≈ 1–3 working sessions. Tasks are the only
unit inside a milestone — no slices or sub-milestones; emerging internal
structure means split, wiring the pieces with `Depends on:`. Split tripwires:
>~7 acceptance criteria, >~10 tasks, a goal sentence needing "and", tasks
shippable independently, or no hope of the 150-line cap. Prefer vertical
slices (thin end-to-end capability) over horizontal layers; every milestone
leaves the default branch shippable. Splitting never discards the remainder.

Work that isn't a milestone:

- **Trivial** (no runtime surface — typos, tracking, comments): direct
  commit to the default branch. No tracking beyond the commit.
- **Hotfix** (user-visible bug): `/hotfix` — regression test first, gate-lite,
  PR, user approval. NEWS entry; no milestone file.
- **Milestone**: needs more than one sitting, changes exported behavior
  (beyond restoring documented behavior), or requires a design decision.

Intake: GitHub issues and external PRs are inboxes, never a second tracking
system. Issues → `candidate` rows or the hotfix path; or, as the fourth
disposition `/milestone` §3 offers,
`leave` is legal only for noise, duplicates, or items already cross-referenced in cairn —
no row, no action, reason stated, never anything genuinely new (D-044).
External PRs → small
and correct: **`/hotfix` is the door** — it adopts the PR (`gh pr checkout`
rather than cutting its own branch), holds it to the hotfix bar, and merges
on user approval; larger: becomes/joins a milestone via `/milestone-plan`.
Candidates may be added conversationally by
anyone at any time (one ROADMAP row).

**Out-of-band idea capture.** A capture channel that is not a cairn tracking
file — a background-task chip, a scratch TODO, an ad-hoc note — is never the
record of record for an idea. The idea also lands as a `candidate` ROADMAP row
in the same turn (search-first applies below), and the out-of-band item is at
most a convenience pointer to that row. The channel stays usable; what it may
not do is be the only place the idea exists, because nothing outside `cairn/`
is authoritative tracking state — an inbox (issues, PRs) or a chip feeds the
ROADMAP, it never substitutes for it. When a chip-creating tool fires in a
cairn repo the `idea_guard.py` PreToolUse hook injects this reminder as a
non-blocking nudge — it prompts the pairing, it does not make the call.

**Search-first candidate creation.** Before adding a candidate row — by any
skill or conversationally — sweep existing candidates + `milestones/archive/`
+ `DECISIONS.md` for overlap; on a hit, absorb into or cross-reference the
existing row rather than add a duplicate. A standing rejection ("considered,
declined") is itself recorded once and follows the supersede discipline —
not re-litigated each time the idea recurs. This generalizes the plan-time
collision check to every candidate-creation point (any skill, conversational
adds alike). Its `DECISIONS.md` sweep follows the bounded read below.

**Bounded `DECISIONS.md` read.** `DECISIONS.md` is append-only and can never
shrink, so it is read by scanning its `### D-` headings — never whole (D-054).
**A matched heading's entry is read whole before anything is surfaced.**
**A match is back-referenced — its own `D-0NN` id searched across the file** — so
an entry superseding or annotating it surfaces even when that entry's heading
omits the relationship (D-012, D-014, and D-019 each omit one).
**A collision is quoted verbatim from the full entry, never from the heading.**
IP2 is unchanged — prior state is surfaced, never silently obeyed or silently
overridden; what narrows is recall, not the obligation.
**A `### D-` heading names its subject and any entry it supersedes, annotates, or narrows.**
`cairn_validate`'s `decision heading quality` advisory WARNs on entries from
D-054 onward that do not; the three that predate it are covered by the
back-reference instead, since IP4 forbids repairing them.

## Git and approval model

- **The default branch (`main`/`master`) is a distribution channel**
  (`pak::pak()` installs it; pkgdown may deploy from it). It stays installable
  at all times. cairn does not assume the name is `main`; everywhere below,
  "the default branch" means the repo's actual default branch.
- **Detecting the default branch (canonical recipe).** cairn never hardcodes
  `main` in a git command. `/cairn-init` detects the name at adoption; every
  operational skill (`/milestone-implement`, `/milestone-review`, `/hotfix`,
  `/cairn-release`) re-detects it at runtime whenever it issues a
  default-branch git command — cairn stores no branch name, so detection is
  the single source of truth. Detect with
  `git symbolic-ref --short refs/remotes/origin/HEAD` (strip the leading
  `origin/`); if that fails because `origin/HEAD` is unset locally (a shallow
  clone, a `git remote add` without `set-head`) but a remote exists, query the
  remote directly with `git ls-remote --symref origin HEAD` and read the
  `ref: refs/heads/<name>` line. Only with **no remote at all** ask the user —
  never guess the local current branch (`git symbolic-ref --short HEAD`), which
  on a feature branch is the wrong answer, and operational skills run on the
  feature branch. Substitute the detected name wherever a skill step writes
  `<default-branch>`.
- The default branch accepts only: docs-only tracking commits and
  squash-merges of milestone/hotfix branches. Never implement on it.
- **The remote's default branch is authoritative.** When a remote exists, push
  docs-only commits to the default branch immediately. A local-only default
  branch means branches get cut from commits the PR base doesn't have — the
  squash-merge then duplicates them and it diverges from origin ("ahead N,
  behind 1").
- Milestone work on `m<nn>-<slug>`; hotfixes on `hotfix-<slug>`; both cut
  from the up-to-date default branch. Checkpoint commits are cheap — squash
  erases them. **An adopted external PR is the exception:** `/hotfix` checks
  the contributor's branch out (`gh pr checkout <N>`) and leaves its name
  alone — the branch is theirs, renaming it breaks the PR, and the PR number
  is the identifier that matters.
- Before branching or committing, check `git status`: a dirty tree with
  unrelated changes means ask the user — never sweep strangers into a
  checkpoint commit.
- If the default branch moves under an active branch (e.g., a hotfix merged),
  merge it into the branch and re-run tests before continuing or reviewing.
- **Nothing reaches the default branch without the user's explicit approval at
  the review gate.** Never force-push — the plugin's
  force_push_guard hook mechanically denies a force-push to the default branch
  (feature branches are not blocked); never merge red or pending CI.
- Approval is recorded on disk: the approving skill writes the single-use,
  gitignored marker `cairn/.merge-approved` at the gate; the plugin's
  merge-guard hook denies `gh pr merge`/`git merge` to the default branch
  without it and consumes it per merge attempt. A failed attempt's consumed
  marker is restored automatically (merge_guard_post), so one approval
  survives failed retries but never a successful merge. Never write the
  marker except at an explicit user approval.
- The marker names the PR it approves (`… approved YYYY-MM-DD for PR #<N>`) and
  the guard refuses a `gh pr merge` whose PR the marker does not name — a bare
  `gh pr merge` with no PR argument included, because an approval that cannot be
  checked is not an approval. Spell the number out: `gh pr merge <N> --squash`.

**Enforcement boundary — what survives a merge made outside a cairn session.**
Every guard is a PreToolUse hook on *this* session's own Bash calls, so it sees
only what an agent runs here. A merge performed in the GitHub web UI, by a merge
queue, or by a contributor without the plugin installed is invisible to
`merge_guard` and `force_push_guard`: on those paths IP1's approval requirement
and the never-force-push line degrade to honor-system, and the post-merge
hygiene pass runs late or not at all. The rest of the conduct — AC fencing,
tracking-travels-with-code, question gates, the review fan-out — is prose with
no mechanical backing on any path. cairn assumes **one operator running these
skills**; outside contributions come in through the intake path above and are
governed by that operator's session, never the contributor's.

Waiting on CI / background work:

- Prefer one **blocking** wait (`gh pr checks <pr> --watch` with a timeout)
  over background polling. At most one wait at a time, resolved within the
  current turn; on timeout, report the fresh actual state, log one line, and
  stop with nothing left watching.
- **Resume is stateless.** Never trust a remembered "CI was running" — the
  PR URL lives in the milestone header; re-derive status from `gh pr checks`
  on demand.

## Context hygiene

Stateless resume makes conversation context disposable; exploit that at
the seams. Only the user can `/clear` — skills mark the seams in their
recaps, never assume continuation.

- **The milestone boundary is the canonical `/clear` point.** After the
  post-merge hygiene commit, everything load-bearing is on the default branch;
  carrying
  the finished milestone's transcript into the next one imports stale
  state (superseded plans, old CI status), not insight. Prefer `/clear`
  over `/compact` there — compaction keeps a lossy summary of what the
  tracking files already record losslessly.
- **Stop points are commit points are safe-clear points.** Never tidy
  mid-task. A long implementation session ends by finishing the current
  task, checkpoint-committing with an honest work-log line, and stopping;
  resume fresh. If compaction threatens to lose something important,
  that's a smell: write it to the milestone file instead.
- Same-session implement → review is fine: criteria evidence is gathered
  by command (never recall) and code review runs in a fresh subagent. The
  seam that matters is milestone → milestone.
- A fresh session stumbling on resume is a tracking-file gap, not a
  reason to avoid clearing — report and fix the file, don't lean on
  remembered context.

## Question gates and routing chips

User interaction happens at exactly three gates — plan questions,
pre-implementation questions, final merge approval — plus routing chips. At
a gate, ask one batched round of 2–5 concrete decision questions via
AskUserQuestion, each with a recommendation and brief pros/cons. Between
gates, work autonomously; never drip questions one at a time. When more
questions are genuinely open than one round holds, prioritize the blocking
ones: flag at most 3 prioritized clarification markers at a single gate and
defer the rest to a later gate — never more than three at once.

The **final merge-approval gate is itself an AskUserQuestion chip** — a
single approve/decline question (recommended option merges; a decline option
is always present), never a prose "do you authorize?" yes/no. A merge is
outward-facing and irreversible; the chip makes consent explicit and
auditable (a bare prose "yes" is weaker consent and can be read as answering
something else).

Every phase ends with a **routing chip**: an AskUserQuestion offering the
single most sensible next action first, composed per the chip rules in
"Output & interaction discipline" below. Selecting an option is an
imperative on the orchestrator, not a suggestion for the user: on selecting
a routing-chip option **the orchestrator immediately invokes the target skill via the Skill tool**
and does not stop to have the user type the command. This does not weaken the
stop: a chip is an explicit user stop — never auto-proceed — but the stop is
*before* selection; the selection itself is the go, and executing it is the
orchestrator's job. In a chip option, the `→ /skill` notation
names the skill the orchestrator invokes on selection, not a command for the user to run.
A routing chip is always an AskUserQuestion call:
a prose list of options is not a routing chip, and emitting a prose list
where a chip is required is a drift bug (locked by `test_gate_wording.py`).

`/milestone-review`'s end is the **sole exception**. After a successful
merge the natural next step is a fresh context, not an in-session route, so
review closes with a plain-prose `/clear` nudge instead of a routing chip —
it is the sole phase whose end is deliberately chip-less; every other phase
skill ends with an AskUserQuestion routing chip. (This does not touch
review's merge-approval gate, which stays an AskUserQuestion chip.)

## Output & interaction discipline

How skills talk to the user. These rules bind all chat output while any
cairn skill is active.

- **Phase header.** Orient the user with Markdown headings, not an inline
  banner. A `#` names the unit of work and its title; a `##` beneath it
  names the phase. (These headers give in-transcript visual hierarchy; in
  Claude Code — cairn's runtime — the navigable table of contents is built
  from chapter markers, not markdown headers, so phases become navigable via
  the "Chapter markers" rule below, not these headings — M27/D-020.)
  Milestone skills: `# Milestone <NN>: <title>` →
  `## Plan` / `## Implement` / `## Review`. Other skills map onto the same
  two levels: `# Hotfix: <slug>` → `## <step>`; `# cairn-init` →
  `## Scaffold` / `## Repair` / `## Migration §n`; `# Release <version>`
  → `## <step>`; `# Status` → `## Snapshot` / `## Audit` / `## Route`;
  `# Review brief RB<NN>` → `## Draft` / `## Gate` / `## Ingest`;
  `# Design interview` → `## Facts` / `## Principles`. Emit the
  `#` once per unit of work — at that unit's first phase — re-emitting when
  the unit changes: a routing chip into the next skill, or a fresh
  post-`/clear` session, both start a new `#` so the reply stands alone (a
  plan run that creates several milestones stays under one `# Planning`).
  Emit a `##` at each phase entry — usually coincident with a chapter marker
  (the session's very first header carries none: session start is implicit).
  Replies within the same phase run as plain deltas underneath — never a
  heading per reply.
- **Deltas, not dumps.** Between gates, report what changed since the
  last report — findings, decisions, surprises, direction changes. Never
  restate the plan or paste command output; the tracking files hold the
  record. Two exceptions: (1) drafted durable-record text is the deliverable,
  not a dump — see the Durable-record preview rule below. (2) conclusion
  text above an acceptance chip — see the Acceptance chips rule.
- **Narrate outcomes, not deliberation.** Between tool calls, chat carries
  findings, decisions, and the mandated previews —
  never a running readout of reasoning (no "now I'll check whether…",
  no weighing of options aloud, no italicized play-by-play commentary).
  A one-line signpost before a long step is fine;
  a compact summary where a question needs context is fine (D-039).
  This never licenses compressing mandated substance: the Durable-record
  preview and Acceptance chips rules still show their text verbatim.
- **Durable-record preview.** Newly authored durable-record text — a
  D-entry, a milestone file's plan-owned sections (new or via a gated
  amendment), a LESSONS line, an archive summary, a ROADMAP
  candidate/graduation row — is shown verbatim in chat immediately before
  the docs-only commit that lands it: same turn, no added stop; objections
  are handled by amend/supersede right after (D-036). Exempt as mechanical
  noise: work-log one-liners, checkbox ticks, status-mirror updates, and
  hotfix/code-branch content (NEWS entries, code) already reviewable at
  the PR merge gate — not a milestone branch's tracking records (D-036).
- **Outcome-first recaps.** Phase-completion recaps lead with what the
  work did, changed, or accomplished, in plain words. Hygiene mechanics
  (caps, hashes, archive paths, commit lists) follow compressed — one
  line when they're clean. A recap the user must re-read to find out
  what happened has failed.
- **Chips carry choices, not evidence.** Supporting detail and technical
  justification live in chat *above* the chip. Option labels are short;
  each description says in plain language what is being chosen and why
  it matters. At most 4 options per question. When a chip asks acceptance
  of a produced conclusion, the Acceptance chips rule below sets the bar —
  a summary never substitutes for the accepted text.
- **Acceptance chips show what's accepted.** A chip option that accepts or
  approves a produced conclusion — review findings, a subagent's verdict,
  an audit result, amended text, or
  a proposed disposition or action plan awaiting confirmation (D-038)
  — requires that conclusion's substance
  verbatim in chat above the chip (D-037): the verdict and each actioned
  finding appear verbatim; a long artifact shows its conclusions section
  verbatim plus the file path for the rest; a paraphrase never stands in
  for the text being accepted.
- **Contextual chip construction.** Compose options from the actual
  session state — the specific issue found, the specific next action —
  not from a fixed menu; chip menus listed in skills are examples, not
  scripts. Invariants that never bend: recommended option first and
  marked, ≤4 options, a stop/pause option present, and a chip is a user
  stop — never auto-proceed.
- **Chapter markers (per-phase mandate).** Mark a chapter at each phase transition
  (session start is implicit) via the runtime's chapter mechanism — in Claude
  Code, `mark_chapter`, which drives the navigable TOC, not the markdown headers
  (M27/D-020). This is a hard per-phase requirement, not "only where supported."
  Fallback: where the runtime provides no chapter mechanism, no marker is emitted
  and the H1/H2 phase headers are the visual fallback — nothing breaks.
- **Copy-run commands get their own fenced block.** Three adjacent cases, three
  different treatments:
  - **Handing the user a command to run → its own fenced code block**, never inline backticks (a fenced block renders a copy button; inline backticks do not).
  - **Naming a command, path, or symbol in prose → inline backticks** — naming a thing is not handing it over.
  - **A routing chip's `→ /skill` option → neither fence nor handoff** — that arrow is not the user's to type; selecting the option is what acts on it (D-022).

  Slash commands (`/clear`, `/milestone-plan`) count as commands here exactly as shell commands do — most handoffs are one, not a shell line.

  Handoff or mention, when the same step does both:
  - **A step that ends the turn expecting the user to go run something → a handoff, and it gets the fence** — nothing else will run it.
  - **A line noting that a moment is a safe `/clear` point, beside a chip already offering the route → a mention, and it stays inline** — the chip, not the user's typing, is what acts.

  The prose framing a handoff stays prose; only the runnable lines get fenced.
- **Subagent titles carry the model tier.** Prefix every Agent
  description with `[S]`/`[O]`/`[F]` for Sonnet/Opus/Fable — task panes
  show only the title, not the model.

## Model and agent strategy

- Orchestrator: Opus, running these skills in the main session. Exception:
  `/design-interview` recommends the user run the *main session* on Fable
  (D-014) — a per-instance session-model choice, not a spawned subagent, so
  it does not touch the Fable-subagent gate below.
- Every spawned Agent's description starts with its tier tag —
  `[S]`/`[O]`/`[F]` — per the output-discipline section.
- **Subagents share the primary checkout.** Every subagent cairn spawns runs
  in the same working tree as the main session, so it uses ref-based git only
  (`git diff`/`show`/`log`/`blame` against refs like `main..HEAD`) and never a
  HEAD-moving command — `git checkout`, `git switch`, `git worktree add`,
  `git reset` — in that shared tree, which would park the primary checkout on
  another branch mid-task (hit in the M36 review). Binds every spawned agent:
  Explore/Sonnet/Opus workers and the `/milestone-review` reviewers alike.
- **Sonnet subagents**: well-specified self-contained work — fan-out
  searches (Explore), mechanical migrations, test writing against a spec,
  boilerplate. Give complete specs — for an Explore fan-out that means a
  reading list naming the files or areas each subagent should read, so it
  searches the right ground instead of guessing; verify their diffs before
  committing; summarize results into one work-log line — the log line
  compresses, but an acceptance chip built on those results still shows
  them verbatim (Acceptance chips rule).
- **Opus subagents**: design-sensitive implementation; the diff-bug lens of
  the fresh-context review at `/milestone-review`.
- **The `/milestone-review` fan-out** (M17) runs in fresh-context subagents,
  not the implementing session, because an author shares their own
  diff-blindness — a reviewer that did not write the code catches the contract
  and convention breaks the author reads straight past.
  Three distinct-evidence reviewers —
  an **[O]** diff-bug reviewer (Opus, correctness/contract/convention),
  an **[S]** blame-history reviewer (Sonnet, does the change undo deliberate
  prior work), and an **[S]** prior-PR-comments reviewer (Sonnet, does the diff
  regress a point a prior PR review raised on these files; always spawned,
  no-ops when a repo has no prior-PR evidence — M40)
  — then an **[S]** confidence scorer (Sonnet) that scores each finding
  0–100 and drops sub-threshold ones from the actioned list (logged, not
  discarded). The scorer gates what the user sees, so it stays on Sonnet, never
  Haiku.
- **Never Haiku.** For anything.
- **Fable subagents**: only through the RB/RR brief protocol
  (`/milestone-brief`) and only after a per-instance approval gate — Fable
  is token-billed; no standing authorization exists. Ad-hoc Fable spawning
  is prohibited: the brief artifact is what makes escalation reproducible,
  auditable, and ingestible. RR ingestion follows the protocol in
  `/milestone-brief` ("Ingesting an RR").
- **RB tripwires** — the three question categories that warrant offering
  Fable escalation, with their canonical tag tokens: statistical/scoring
  correctness with no available oracle (`no-oracle`); irreversible
  exported-API decisions (`irreversible-api`); anything touching an IP
  (`ip-touching`). `/milestone-plan` tags tripwire-hitting open questions
  inline on the affected task or criterion — `(RB tripwire: <token>)` —
  and `/milestone-implement` inherits the tags; a tripwire can also fire
  mid-implementation (same categories, no tag required). An escalation
  chip option is offered only on a tripwire hit, never as a standing menu
  item (D-004: Fable is gated per instance).

## Toolchain profiles

Language/toolchain specifics live in a **profile**, not in the core rules. A
repo declares its profile in `cairn/PROFILE.md` (instantiated by `cairn-init`
from a shipped reference under `skills/shared/profiles/`); the operational
skills read its slots instead of hardcoding one language's commands. Seven slots:

- **verify** — the per-task test/check command(s) `/milestone-implement` and `/hotfix` run.
- **consistency-gate** — toolchain checks `/milestone-review` runs *in addition to* the universal cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`).
- **test-doctrine** — toolchain-specific test expectations layered on the universal "What gets a test" rules.
- **release-walk** — the release procedure `/cairn-release` follows.
- **init-detection** — how `cairn-init` recognizes the toolchain.
- **greenfield-openers** — opener questions for a new/empty repo of this type.
- **changelog** — the repo's changelog file (or "none"), read by `/hotfix`, `/cairn-release`'s release-walk, and the consistency-gate; "none" is legal — hotfix skips the changelog entry, and the release-walk skips consolidation and derives the version bump from git history.

The **domain verification doctrine (oracles) is universal, not a profile slot**:
it is orthogonal to the language profile (D-024/D-025), stated once in
`skills/shared/validation-doctrine.md` (see "Validation doctrine" below). A
profile carries *language mechanics*, never domain doctrine.

Four profiles ship: `r-package` (devtools/roxygen/testthat/pkgdown, CRAN),
`python` (pyproject/pytest/ruff/mypy/build+twine, PyPI), `docker-image`
(hadolint/`docker build`/buildx, a container registry), and `generic` (no
toolchain gates). **Absent `PROFILE.md` → infer** in order: a `DESCRIPTION` at
the repo root means `r-package`, else a `pyproject.toml` (or legacy
`setup.py`/`setup.cfg`) means `python`, else a `Dockerfile` as the sole
toolchain marker means `docker-image`, else `generic` — so a repo that adopted
cairn before profiles keeps working unchanged, and `cairn-init` repair backfills
the explicit declaration. Inference has no user, so a hybrid repo carrying both
a `Dockerfile` and a language marker keeps the language marker (the language
branches rank first); `cairn-init`'s disambiguation gate, where a user is
present, is the only place the image-vs-package choice is asked.
`cairn_validate` no-ops when `PROFILE.md` is absent and, when present, FAILs on
a missing, empty, or unrecognized slot.

## Validation doctrine (statistical/numeric work)

The domain-verification doctrine — oracle priority list, the five oracle
types, the ≥2-independent-types bar, the oracle registry + its declared
pointer, the reproducibility and primary-sources hard stops, and source
ingestion — lives in `skills/shared/validation-doctrine.md`, a module of
this rulebook (M58: new domain doctrine gets a module, not a rulebook
section). It is universal domain doctrine, never a profile slot
(D-024/D-025). Read the module whenever a milestone touches a numeric
result or scoring/algorithmic content.

## References pages

Committed `cairn/references/` pages come in two types. **Source notes**
(`<citekey>.md`) each own one primary source — citation, extracted values
with page/table anchors, what traces to it (the ingestion workflow is in
`skills/shared/validation-doctrine.md`). **Synthesis notes** are
the second committed `references/` page type —
cross-source analyses (a fit assessment, a comparative survey, a pilot
ledger) that no single `<citekey>.md` owns. Same rules for both: committed,
cited (`citekey (p. N)` / page name), never restated into tracking files.
Every committed `references/` page carries its
`INDEX.md` line — mechanized by `cairn_validate`'s references check (M57).

**When a page is owed.** A source consulted in passing owes nothing.
A page is owed once the repo *relies* on the source — a claim, value, convention, or decision here traces back to it — and it is authored in the milestone that takes the dependency, never left for later.
Repo-internal analysis earns the second page type by the same test applied to time:
an analysis that will outlive its milestone — a fit assessment, a comparative survey, a pilot ledger — is a synthesis note, while analysis serving only the milestone in hand stays in the milestone file.
The over-cap remedy above is a separate last-resort route into `references/`, not this one.
Author from the shipped templates: `skills/shared/templates/source-note.md` for a source note, `skills/shared/templates/synthesis-note.md` for a synthesis note.
This trigger is universal — it fires in a repo with no numeric work at all,
which is why it lives here and not in the conditionally-read domain module;
`skills/shared/validation-doctrine.md` carries only the numeric/scoring
instance of the workflow, where the source is a paper backing a number.

**Standing facts vs. dated observations.** A committed `references/` page —
source note and synthesis note alike — makes two kinds of claim, and they age
differently.
A **standing fact** is a claim about the *source*: an extracted value, a printed formula, a verbatim wording, a page or table anchor.
A **dated observation** is a claim about the *repo's own state*: what is on the shelf, what has or has not been read, what another page does or does not yet say, what a later task must still check.
A standing fact holds as long as the source does. A dated observation is true
at a moment and can go stale within the hour — `cairn/references/sources/` is a
live directory the maintainer adds to mid-session, and a note written by a
subagent is a snapshot of the repo at write time, not at merge time. So a
dated observation carries `— observed YYYY-MM-DD` inline on the claim itself,
where a reader meets it, and is never recorded as a standing fact. The
undated absence claim — "not present", "not retrieved", "not yet checked",
"must be verified when X is written" — is the specific failure this rule
exists to stop; it reads as durable, is believed by every later plan-time
harvest, and is routinely false by merge time.

**Page provenance.** Every committed `references/` page carries a
`**Provenance.**` block recording how the page came to exist: source pointer
(the shelf PDF path, or the URL and retrieval record for a non-PDF source),
ingested date, ingesting milestone, pagination basis (`—` where the source is
unpaginated), and extraction-verified status — whether the extracted values
have been re-read against the source, or are an unverified first pass. The
page's citekey and full citation are carried by the page itself (its heading
and citation), not restated inside the block.
The block is prose in the page's own idiom, not frontmatter.
Provenance is what lets a reader judge a page's age without opening the
source; the verified status is what keeps an unchecked subagent extraction
from reading like a confirmed one. Because "when this was last checked" is
itself a claim about the repo's state, an extraction status carries its own
`— observed YYYY-MM-DD`.

**Re-verification.** An extraction status is written once and then ages, so a page the repo still relies on is re-checked against its source as it gets old, and a page never checked against its source at all keeps saying so.
A re-check marks inline in the provenance block, on the extraction status itself — never in a new file, a new section, or a log.
A second record of when a page was last read is a divergence vector (the
reason M56 rejected a central ledger), and the block is where a reader
already looks. `cairn_validate`'s `references staleness` advisory reads that
status and WARNs on a page recording no verified re-check, and on one last
verified more than 180 days ago; a status naming no date of its own ages from
the block's ingested date, and a first-hand record with nothing to re-verify
against is exempt by saying so. It stays an advisory and never a check
because "this page is too old" is a judgment about evidence quality, not a
structural fact a gate can settle.

## What gets a test

No coverage-percentage target — test scope is set per milestone via
acceptance criteria. Always: every exported/public function (happy path,
every error branch fired, the language's edge cases); every numeric result
via an oracle; every bug fix via a regression test that fails before the fix;
every documented claim. Indirect by default: internal helpers (direct tests
only for independent logic). Never: cosmetic output beyond meaningful
snapshots, trivial pass-throughs, dependency behavior. Test the contract, not
the implementation — a test that breaks under a behavior-preserving refactor
is a defect in the test.

**A rule is what changes compliant behavior when deleted or inverted.** That
test decides whether prose in this rulebook is operative — a rule, or the
doctrine for applying one — or is justification the file does not owe and git
already holds (D-056, which classifies the rulebook as current knowledge and
states the three-step placement test). Prove it by inversion: relabel, negate,
or transpose the rule in place, run the suite, require red, restore and diff;
where no guard exists, record a by-hand inversion.

**Guard-reddening is a deletion screen, never a licence to keep** — sufficient
to block a careless deletion, never necessary to justify one, and never
sufficient to keep prose that fails the behavioral test above. The text owns
the guard, not the reverse: anchors are exemplar blocks chosen partly for
matchability, so a guard can pin scaffolding, and reading pinned as frozen is
how a rulebook's editability dies one guard at a time. A pinned block that
fails the test is shortened *with* re-anchoring, never skipped.

**A guard must fail when the rule it locks is deleted.** A prose-guard — a
test that locks wording by asserting substrings of a doc (skill, rulebook,
template) — gives *false coverage* when a phrase it asserts also occurs
elsewhere: deleting the rule leaves the assertion satisfied, so the guard
passes over a rule that is gone (the recurring M39/M40 trap). Verify by
mutation, not by eye: cairn's own prose-guards register in the mutation
harness (`skills/tests/test_mutation_harness.py`), which blanks each
registered block and asserts its guard fails; the completeness meta-test
fails CI on any unregistered prose-guard *file*. Registration is per file
(one or more exemplar blocks), **not** per assertion — a new `assertIn`
added to an already-registered file still needs its own entry or the by-hand
check ("would this pass against the pre-milestone content?").

**The craft of making a guard falsifiable lives in a module of this rulebook**, on its own line so the mapping stays pinnable:
`skills/shared/guard-doctrine.md` covers anchors and what an assert must pin, the mutation harness's own blind spots, absence assertions, fixture design, matchers over authored markdown, restatement and numbers, and sweep scoping.
Read it when authoring or editing a prose-guard, a fixture, a matcher, or a
`cairn_validate` check. The rule above states the obligation; the module is
how to meet it, and like the Validation doctrine it is read conditionally, so
sessions that write no guard never pay for it.

The language-mechanical specifics — which edge cases, which error mechanism,
coverage-tool status, plot/snapshot conventions — live in the active profile's
`test-doctrine` slot (`cairn/PROFILE.md`; absent → infer per "Toolchain
profiles"); the rules here are the universal floor. **Profiles supply language
mechanics; the oracle / Validation doctrine module stays universal** (D-024/D-025),
never a profile slot.

The language/toolchain guardrails that were once stated here — package-build
rules, generated-file conventions, error-condition idioms — now live in the
active profile's `test-doctrine` and `consistency-gate` slots (for the R
toolchain, `skills/shared/profiles/r-package.md`); they are advisory in the
moment and mechanically enforced by the `consistency-gate` slot at
`/milestone-review`. The dependency-change gate and the deprecation-cycle
policy are universal governance (see "Universal tracking rules"); profiles
carry only their mechanical renderings.
