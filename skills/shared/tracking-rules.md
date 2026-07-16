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
| `cairn/PROFILE.md` | The repo's toolchain profile — the six language/toolchain slots the operational skills read (see "Toolchain profiles") | Domain doctrine (oracles are universal), status, tasks, decisions |
| `cairn/ROADMAP.md` | The milestone index — **the only authority on status** | Task details, acceptance criteria, narrative |
| `cairn/milestones/M<NN>-<slug>.md` | One milestone's goal, scope (In/Out), acceptance criteria, tasks, work-log, review evidence | Status authority (header is a mirror; ROADMAP wins any conflict — fix the mirror immediately, before other work) |
| `cairn/milestones/archive/` | Compressed ≤25-line summaries of done/dropped milestones | Active work |
| `cairn/DECISIONS.md` | Append-only cross-cutting decisions (D-001, …), never renumbered — superseded by new entries | Milestone-local decisions (those live in the milestone file); deferrals ("not now" is a ROADMAP fact, not a decision) |
| `cairn/LESSONS.md` | Durable, append-only, capped repo lessons (build quirks, testing tricks) — captured at milestone end, surfaced at plan time | Status, decisions (a *choice* is a D-entry), per-milestone task notes |
| `cairn/reviews/` | RB<NN> briefs and RR<NN> reports for Fable escalation (+ `archive/` for resolved pairs) | Anything else |
| `cairn/references/` | Source notes (`<citekey>.md`), synthesis notes (cross-source analyses — fit assessments, surveys, pilot ledgers), `INDEX.md` (one line per committed page), gitignored `pdf/` | Anything else |
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
- a live milestone file's **plan-owned body < 150 lines** — everything before
  the review-exclusive `## Review` section. That `## Review` section is exempt
  from the cap, so review evidence never scrambles plan-owned content (M55): its
  evidence accumulates at review time and no longer competes with Scope, AC, or
  Coverage for the budget. A file with no `## Review` section counts whole.
- Work-log entries are one line each. Never paste command output or subagent
  transcripts into tracking files — summarize.
- Remedies when a cap is hit (never "let it grow"): over-cap ROADMAP →
  graduate or prune candidates and enforce terminal-row retention — and when
  a large legacy or parking-lot backlog blows the cap one-row-per-item,
  cluster related items into grouped candidate rows that point at the
  entombed legacy `ROADMAP.md` instead of listing each (M21 G-C4); over-cap
  milestone → split it or move reference material to `references/`; over-cap
  cairn CLAUDE.md section → trim it back to the template (it is routing
  boilerplate, not a content home); other CLAUDE.md content → its owner per
  the table above.
- Terminal-row retention: the ROADMAP table keeps only the 5 most recent
  terminal (`done` or `dropped`) rows combined; prune older ones as they
  accumulate — archive files and git history stay authoritative. Standing
  hygiene, not just a cap remedy.

## Universal tracking rules

- **Tracking travels with code.** Every commit that changes code also updates
  the milestone checkboxes/work-log in the same commit.
- **Absolute dates only** (YYYY-MM-DD). Never "yesterday" or "last week".
- **Append, don't rewrite.** Work-logs and DECISIONS.md are append-only;
  supersede, never edit history. Never fabricate history — if there is a
  gap, add one catch-up entry summarizing `git log`.
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
| `blocked` | Waiting on something external; work-log line names the blocker | any skill, reason logged |
| `review` | Tasks done, local checks clean; awaiting verification + merge approval | `/milestone-implement` on completion |
| `done` | Every criterion executed with fresh evidence; PR merged; file archived | `/milestone-review` only |
| `dropped` | Deliberately abandoned; one-line reason archived | user decision, via any skill |

Transitions: `candidate → planned → in-progress ⇄ blocked;
in-progress → review → done` (review failures return to `in-progress`).
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
system. Issues → `candidate` rows or the hotfix path. External PRs → small
and correct: review to the hotfix bar and merge on user approval; larger:
becomes/joins a milestone. Candidates may be added conversationally by
anyone at any time (one ROADMAP row).

**Search-first candidate creation.** Before adding a candidate row — by any
skill or conversationally — sweep existing candidates + `milestones/archive/`
+ `DECISIONS.md` for overlap; on a hit, absorb into or cross-reference the
existing row rather than add a duplicate. A standing rejection ("considered,
declined") is itself recorded once and follows the supersede discipline —
not re-litigated each time the idea recurs. This generalizes the plan-time
collision check to every candidate-creation point (any skill, conversational
adds alike).

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
  erases them.
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
  an audit result, amended text — requires that conclusion's substance
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
- **Copy-run commands get their own fenced block.** A command the user is
  meant to copy and run goes in its own fenced code block (it renders a copy
  button), not inline backticks — inline backticks are for *naming* a command,
  path, or symbol in prose, not for handing one over to run.
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
skills read its slots instead of hardcoding one language's commands. Six slots:

- **verify** — the per-task test/check command(s) `/milestone-implement` and `/hotfix` run.
- **consistency-gate** — toolchain checks `/milestone-review` runs *in addition to* the universal cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`).
- **test-doctrine** — toolchain-specific test expectations layered on the universal "What gets a test" rules.
- **release-walk** — the release procedure `/cairn-release` follows.
- **init-detection** — how `cairn-init` recognizes the toolchain.
- **greenfield-openers** — opener questions for a new/empty repo of this type.

The **domain verification doctrine (oracles) is universal, not a profile slot**:
it is orthogonal to the language profile (D-024/D-025), stated once in
`skills/shared/validation-doctrine.md` (see "Validation doctrine" below). A
profile carries *language mechanics*, never domain doctrine.

Three profiles ship: `r-package` (devtools/roxygen/testthat/pkgdown, CRAN),
`python` (pyproject/pytest/ruff/mypy/build+twine, PyPI), and `generic` (no
toolchain gates). **Absent `PROFILE.md` → infer** in order: a `DESCRIPTION` at
the repo root means `r-package`, else a `pyproject.toml` (or legacy
`setup.py`/`setup.cfg`) means `python`, else `generic` — so a repo that adopted
cairn before profiles keeps working unchanged, and `cairn-init` repair backfills
the explicit declaration. `cairn_validate` no-ops when `PROFILE.md` is absent
and, when present, FAILs on a missing, empty, or unrecognized slot.

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
