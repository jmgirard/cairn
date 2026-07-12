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
| `cairn/ROADMAP.md` | The milestone index — **the only authority on status** | Task details, acceptance criteria, narrative |
| `cairn/milestones/M<NN>-<slug>.md` | One milestone's goal, scope (In/Out), acceptance criteria, tasks, work-log, review evidence | Status authority (header is a mirror; ROADMAP wins any conflict — fix the mirror immediately, before other work) |
| `cairn/milestones/archive/` | Compressed ≤25-line summaries of done/dropped milestones | Active work |
| `cairn/DECISIONS.md` | Append-only cross-cutting decisions (D-001, …), never renumbered — superseded by new entries | Milestone-local decisions (those live in the milestone file); deferrals ("not now" is a ROADMAP fact, not a decision) |
| `cairn/LESSONS.md` | Durable, append-only, capped repo lessons (build quirks, testing tricks) — captured at milestone end, surfaced at plan time | Status, decisions (a *choice* is a D-entry), per-milestone task notes |
| `cairn/reviews/` | RB<NN> briefs and RR<NN> reports for Fable escalation (+ `archive/` for resolved pairs) | Anything else |
| `cairn/references/` | Source summaries (`<citekey>.md`), `INDEX.md`, gitignored `pdf/` | Anything else |
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
| Priority, Depends on (header) | plan | create; amend-via-gate |
| Branch/PR (header) | implement (branch), review (PR URL) | create |
| Goal | plan | create; a wrong goal returns to plan, never edited in place |
| Scope (In/Out) | plan | create; amend-via-gate |
| Acceptance criteria | plan | create; amend-via-gate — review reads, never reinterprets |
| Coverage (criterion→task map) | plan | create; amend-via-gate — review reads to fence evidence, never reinterprets |
| Tasks | plan (create), implement (check-off, minor edits) | create; check-off; amend-via-gate for substantive change |
| Work log | any skill | append-only |
| Decisions (milestone-local) | implement, review | append-only |
| Review | review | exclusive |

**AC fencing (review discipline).** At `/milestone-review`, an
acceptance-criterion checkbox is ticked only against fresh evidence recorded
in the Review section — no evidence line, no tick — and every criterion must
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

- `CLAUDE.md` < 80 lines · `ROADMAP.md` < 60 lines · `LESSONS.md` < 50 lines
  · active milestone file < 150 lines · archived summary ≤ 25 lines.
- Work-log entries are one line each. Never paste command output or subagent
  transcripts into tracking files — summarize.
- Remedies when a cap is hit (never "let it grow"): over-cap ROADMAP →
  graduate or prune candidates and enforce done-row retention; over-cap
  milestone → split it or move reference material to `references/`;
  over-cap CLAUDE.md → push content to its owner per the table above.
- Done-row retention: the ROADMAP table keeps only the 5 most recent
  `done` rows; prune older ones as they accumulate — archive files and
  git history stay authoritative. Standing hygiene, not just a cap remedy.

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
- **Tracking files outrank memory.** Claude's persistent memory never holds
  project state (status, milestones, decisions, architecture). Memory is for
  meta-context only; `cairn/` files win any conflict.

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
leaves main shippable. Splitting never discards the remainder.

Work that isn't a milestone:

- **Trivial** (no runtime surface — typos, tracking, comments): direct
  commit to main. No tracking beyond the commit.
- **Hotfix** (user-visible bug): `/hotfix` — regression test first, gate-lite,
  PR, user approval. NEWS entry; no milestone file.
- **Milestone**: needs more than one sitting, changes exported behavior
  (beyond restoring documented behavior), or requires a design decision.

Intake: GitHub issues and external PRs are inboxes, never a second tracking
system. Issues → `candidate` rows or the hotfix path. External PRs → small
and correct: review to the hotfix bar and merge on user approval; larger:
becomes/joins a milestone. Candidates may be added conversationally by
anyone at any time (one ROADMAP row).

## Git and approval model

- **main is a distribution channel** (`pak::pak()` installs it; pkgdown may
  deploy from it). It stays installable at all times.
- main accepts only: docs-only tracking commits and squash-merges of
  milestone/hotfix branches. Never implement on main.
- **origin/main is main.** When a remote exists, push docs-only commits to
  main immediately. A local-only main means branches get cut from commits
  the PR base doesn't have — the squash-merge then duplicates them and main
  diverges from origin ("ahead N, behind 1").
- Milestone work on `m<nn>-<slug>`; hotfixes on `hotfix-<slug>`; both cut
  from up-to-date main. Checkpoint commits are cheap — squash erases them.
- Before branching or committing, check `git status`: a dirty tree with
  unrelated changes means ask the user — never sweep strangers into a
  checkpoint commit.
- If main moves under an active branch (e.g., a hotfix merged), merge main
  into the branch and re-run tests before continuing or reviewing.
- **Nothing reaches main without the user's explicit approval at the review
  gate.** Never force-push; never merge red or pending CI.
- Approval is recorded on disk: the approving skill writes the single-use,
  gitignored marker `cairn/.merge-approved` at the gate; the plugin's
  merge-guard hook denies `gh pr merge`/`git merge`-to-main without it and
  consumes it per merge attempt. Never write the marker except at an
  explicit user approval.

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
  post-merge hygiene commit, everything load-bearing is on main; carrying
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
gates, work autonomously; never drip questions one at a time.

The **final merge-approval gate is itself an AskUserQuestion chip** — a
single approve/decline question (recommended option merges; a decline option
is always present), never a prose "do you authorize?" yes/no. A merge is
outward-facing and irreversible; the chip makes consent explicit and
auditable (a bare prose "yes" is weaker consent and can be read as answering
something else).

Every phase ends with a **routing chip**: an AskUserQuestion offering the
single most sensible next action first, composed per the chip rules in
"Output & interaction discipline" below. Selecting a chip invokes that
skill in the same session. A chip is an explicit user stop — never
auto-proceed.

## Output & interaction discipline

How skills talk to the user. These rules bind all chat output while any
cairn skill is active.

- **Phase header.** Orient the user with Markdown headings, not an inline
  banner. A `#` names the unit of work and its title; a `##` beneath it
  names the phase. (Both levels land in Claude Desktop's table of contents,
  which indexes only H1/H2.) Milestone skills: `# Milestone <NN>: <title>` →
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
  record.
- **Outcome-first recaps.** Phase-completion recaps lead with what the
  work did, changed, or accomplished, in plain words. Hygiene mechanics
  (caps, hashes, archive paths, commit lists) follow compressed — one
  line when they're clean. A recap the user must re-read to find out
  what happened has failed.
- **Chips carry choices, not evidence.** Supporting detail and technical
  justification live in chat *above* the chip. Option labels are short;
  each description says in plain language what is being chosen and why
  it matters. At most 4 options per question.
- **Contextual chip construction.** Compose options from the actual
  session state — the specific issue found, the specific next action —
  not from a fixed menu; chip menus listed in skills are examples, not
  scripts. Invariants that never bend: recommended option first and
  marked, ≤4 options, a stop/pause option present, and a chip is a user
  stop — never auto-proceed.
- **Chapter markers.** Where the harness supports conversation chapters,
  mark phase transitions (session start is implicit).
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
- **Sonnet subagents**: well-specified self-contained work — fan-out
  searches (Explore), mechanical migrations, test writing against a spec,
  boilerplate. Give complete specs; verify their diffs before committing;
  summarize results into one work-log line.
- **Opus subagents**: design-sensitive implementation; the diff-bug lens of
  the fresh-context review at `/milestone-review`.
- **The `/milestone-review` fan-out** (M17): two distinct-evidence reviewers —
  an **[O]** diff-bug reviewer (Opus, correctness/contract/convention) and an
  **[S]** blame-history reviewer (Sonnet, does the change undo deliberate prior
  work) — then an **[S]** confidence scorer (Sonnet) that scores each finding
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

## Validation doctrine (statistical/numeric packages)

Tests verify against ground truth, not against the code. Every
numeric-results suite includes, in priority order: (1) hand-computed
fixtures from published formulas, arithmetic in comments; (2) published
reference values, cited; (3) independent recomputation with deliberately
dumb explicit code; (4) invariant tests. Snapshots only on top, never as the
sole oracle for a number.

**Primary sources rule (hard stop):** never substitute secondary
descriptions or model memory for a primary source on scoring/algorithmic
content. Search (DOI, publisher, OSF); if inaccessible, stop and ask the
user for the PDF.

**Source ingestion:** PDF → `cairn/references/pdf/` (gitignored).
Summary → `cairn/references/<citekey>.md` (committed): full citation,
extracted values with page/table anchors, verbatim-critical values quoted
exactly, which tests/oracles trace to it, open questions. One line in
`INDEX.md`. Tests and milestones cite `citekey (p. N)`, never restate.

## What gets a test

No coverage-percentage target — test scope is set per milestone via
acceptance criteria. Always: every exported function (happy path, every
`cli_abort()` branch fired, R edge cases — zero rows, `NA`, length-one,
factor vs. character, empty strings); every numeric result via an oracle;
every bug fix via a regression test that fails before the fix; every
documented claim. Indirect by default: internal helpers (direct tests only
for independent logic). Never: print cosmetics beyond meaningful snapshots,
trivial pass-throughs, dependency behavior, plots except `vdiffr` when the
plot is the product. Test the contract, not the implementation — a test that
breaks under a behavior-preserving refactor is a defect in the test. `covr`
is a diagnostic, never a gate.

## R package guardrails

- After roxygen changes: `Rscript -e 'devtools::document()'`. After code
  changes: `Rscript -e 'devtools::test()'`. At review: `devtools::check()`.
- Never hand-edit `NAMESPACE`, `man/`, or `data/*.rda`; data regenerates
  from `data-raw/` scripts.
- README.md is knitted from README.Rmd (`devtools::build_readme()`).
- **Dependency changes are never unilateral**: adding, removing, or moving a
  package between Imports/Suggests is a question-gate item and gets a
  D-entry.
- Breaking changes to exported behavior follow a lifecycle deprecation cycle
  unless the package is pre-1.0 and the user explicitly waives it.
- Every newly exported object gets a `_pkgdown.yml` reference-index row in
  the same commit that exports it.
- New user-facing conditions use `cli::cli_abort()` / rlang, not assertthat.
- New top-level tracked files/dirs need `.Rbuildignore` entries.

These are advisory in the moment and **mechanically enforced by the
consistency gate in `/milestone-review`**.
