# rpkg-tracking — Canonical System Spec (Draft 2)

Supersedes DRAFT_1.md. This document specifies the single, canonical Claude Code
workflow + tracking system for R package development, to be built as a Claude
Code **plugin** in this repo and shared on GitHub. It synthesizes the best of
the systems previously built in hitop, tidymedia, intraclass, ackwards, bsync,
and circumplex, and is written so the plugin files can be produced from it
almost mechanically.

---

## 1. Overview & Priorities

One plugin provides the skills (workflow logic, rules, templates); each package
repo holds only its own state (a small set of markdown files under `project/`).
Logic lives centrally and updates propagate by updating the plugin; state lives
locally and never needs to be "kept in sync" with other repos.

Priorities, in order:

1. **Efficient** — avoids redundant work; stores decisions and outcomes, not
   minutiae; keeps always-loaded context small (weight caps, archiving).
2. **Reliable** — doesn't go stale; self-corrects via a health audit; status
   has one authority; tracking travels with code so it can't drift from git.
3. **Portable** — identical across repos; one-command adoption in a new
   package; shareable on GitHub; repo-specific rules layer on top without
   forking the core.

---

## 2. Distribution: the plugin

### 2.1 Repo layout (this repo)

```
rpkg-tracking/
├── .claude-plugin/
│   └── plugin.json            # name, description, version
├── skills/
│   ├── milestone/             # entry point: status snapshot + health audit + routing
│   │   └── SKILL.md
│   ├── milestone-plan/
│   │   └── SKILL.md
│   ├── milestone-implement/
│   │   └── SKILL.md
│   ├── milestone-review/
│   │   └── SKILL.md
│   ├── milestone-brief/       # Fable RB/RR protocol
│   │   └── SKILL.md
│   ├── rpkg-init/             # scaffold or migrate a repo into the system
│   │   └── SKILL.md
│   ├── rpkg-release/          # CRAN release walk (adapted from circumplex)
│   │   └── SKILL.md
│   ├── hotfix/                # bug fix outside milestone machinery
│   │   └── SKILL.md
│   └── shared/
│       ├── tracking-rules.md  # the one rulebook every skill reads first
│       └── templates/
│           ├── milestone.md
│           ├── brief.md
│           ├── decision.md
│           └── claude-md-section.md
├── README.md                  # public-facing: what this is, install, usage
├── CHANGELOG.md               # plugin versions
└── DRAFT_*.md                 # design history (removed before public release)
```

Rules are stated **once**, in `shared/tracking-rules.md`. Every skill begins
by reading it (via `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md`) and
must not restate its content — the ackwards/bsync failure mode was the same
rules duplicated in CLAUDE.md and each skill, drifting apart.

### 2.2 Adoption & migration: `/rpkg-init`

Idempotent skill that brings any repo into the system:

- **Fresh repo:** create `project/` files from templates, append the standard
  section to CLAUDE.md (creating it if absent), add `^project$` to
  `.Rbuildignore` and `project/references/pdf/` to `.gitignore`, seed
  `ROADMAP.md` with an empty index.
- **Existing tracked repo (migration):** run the full migration protocol
  (§2.4). Never a freeform "propose a mapping and convert" — migration
  follows fixed rules, happens on a branch via PR, and is accepted only when
  the health audit passes.
- **Re-run any time:** reports and repairs missing pieces; never overwrites
  user content without asking.
- **Non-package repos:** if there's no DESCRIPTION file, say so and ask —
  either adapt (scaffold the tracking system minus the R-specific guardrails
  and gates) or abort. Never scaffold R machinery into a non-package repo
  silently.

### 2.3 Versioning & repo-specific overrides

- The plugin is versioned in `plugin.json` + `CHANGELOG.md`. Repos don't pin
  versions; whatever plugin version is installed is the law. Breaking changes
  to the state-file format ship with migration handling in `/rpkg-init`.
- **Install is manual for now** (local plugin / direct install). Publishing a
  `marketplace.json` for one-command install is deferred until the system has
  been battle-tested across several repos.

### 2.4 Migration protocol (existing precursor systems)

Governing principle: **migrate the living, entomb the dead.** Completed
history is never converted — conversion of dozens of done milestones is
where hallucination and loss happen, and git already preserves everything.
Only *live* state gets translated into the new format.

1. **Detect and identify.** Recognize the precursor from its footprint. The
   skill ships a mapping table for the known lineages (root-level
   `MILESTONES.md`/`DESIGN.md` with status in CLAUDE.md; older `project/`
   layouts; per-milestone-file layouts). Unrecognized footprints get an
   interview, not a guess.
2. **Migration runs on a branch, through a PR.** Never on main. The entire
   migration is one reviewable diff the user can inspect and revert.
   Requires a clean working tree and, ideally, no work in flight — an
   in-progress milestone is either finished first (recommended) or carried
   over as the sole `in-progress` item, explicitly confirmed.
3. **Entomb history verbatim.** Legacy tracking files move whole and
   unmodified to `project/legacy/` (committed). The new ROADMAP.md carries
   one header line: "Pre-migration history: see `project/legacy/` and git
   log." No completed milestone is ever rewritten into the new format —
   not even as a summary.
4. **Translate only live state**, under a no-invention rule (never infer a
   status, date, or rationale that isn't written down — mark it unknown or
   ask):
   - In-flight / planned / backlog items → milestone files or `candidate`
     rows, using the fixed status mapping (e.g., `READY`→`planned`,
     `IN PROGRESS`→`in-progress`, parking-lot / someday items →
     `candidate`).
   - **IDs are never renumbered.** New milestone numbering continues from
     the legacy maximum (a repo at M53 starts at M54). Legacy decision IDs
     (`ADR-0nn`, `D-00n`, DESIGN §-refs) stay valid as citations into
     `project/legacy/`; DECISIONS.md starts fresh at D-001 with a header
     note pointing at the legacy log. Only decisions still governing active
     work get re-recorded (as new entries citing their legacy ID).
   - Unresolved open questions / known issues → `candidate` rows or DESIGN
     "Known issues", per the ownership table.
5. **Redistribute and deactivate.** Old CLAUDE.md content is redistributed
   per the §3.2 ownership table (invariants → DESIGN or CLAUDE hard rules;
   status slots and milestone indexes → deleted, ROADMAP owns status now;
   commands kept). **Old repo-local skills and rulebooks are moved to
   `project/legacy/`** — they must not remain in `.claude/skills/`, where
   they would collide with or contradict the plugin (e.g., a legacy
   `/milestone` or `plan-milestone` skill fighting the plugin's).
   Repo-specific assets with no canonical home (spec files, coverage
   matrices, principles docs) stay in `project/` as declared repo-specific
   files — kept, not forced into the canonical shapes.
6. **Accept by audit + ledger.** The migration PR is mergeable only when:
   (a) the `/milestone` health audit passes clean on the branch, and (b) a
   **migration ledger** in the PR description accounts for every legacy
   file and every live item — old location → new location or explicit
   "entombed" / "dropped at user request". Same conservation rule as
   planning (§5.2): nothing silently vanishes. The user approves the merge
   like any milestone.
- **Repo-specific rules never fork the plugin.** They live in the repo:
  hard rules in that repo's CLAUDE.md (e.g., hitop's "keying tables need
  Jeff's PR sign-off"), conventions and principles in that repo's
  `project/DESIGN.md`. Skills always read both, so local rules bind without
  touching the shared core.

---

## 3. Per-repo file map, ownership boundaries, weight caps

### 3.1 File map (created by `/rpkg-init`)

```
<package-repo>/
├── CLAUDE.md                      # lean router (see §3.2), < 80 lines
└── project/
    ├── DESIGN.md                  # architecture as it IS + principles
    ├── ROADMAP.md                 # milestone index — the ONLY status authority
    ├── DECISIONS.md               # append-only decision log (D-001, ...)
    ├── milestones/
    │   ├── M<NN>-<slug>.md        # one file per planned/active milestone
    │   └── archive/
    │       └── M<NN>-<slug>.md    # compressed ≤25-line summaries of done/dropped
    ├── reviews/
    │   ├── RB<NN>-<slug>.md       # Fable Review Briefs (open)
    │   ├── RR<NN>-<slug>.md       # Fable Review Reports (awaiting ingestion)
    │   └── archive/               # resolved RB/RR pairs
    └── references/
        ├── INDEX.md               # one line per ingested source
        ├── <citekey>.md           # committed summary per source (§9.1)
        └── pdf/                   # the PDFs themselves — gitignored (copyright,
                                   # repo weight); summaries are what's shared
```

### 3.2 Ownership boundary table

The single most effective anti-drift mechanism. Substance lives in the owner;
any other file gets at most a one-line cross-reference.

| File | Owns | Does NOT own |
|---|---|---|
| `CLAUDE.md` | Dev commands, repo-specific hard rules, pointers to `project/` | Status, TODOs, architecture rationale, history — anything time-varying rots here |
| `project/DESIGN.md` | Purpose & scope, function families, conventions, numbered principles (GP/IP), architecture as it **is**, known issues | Future work, task lists, status |
| `project/ROADMAP.md` | The milestone index table — ID, title, status, depends-on, priority. **The only authority on status.** | Task details, acceptance criteria, narrative |
| `project/milestones/M<NN>-*.md` | One milestone's goal, scope (In/Out), acceptance criteria, tasks, work-log, review evidence | Status authority (header mirrors ROADMAP; on conflict ROADMAP wins, fix the mirror immediately), architecture |
| `project/DECISIONS.md` | Append-only cross-cutting decisions (D-001), never renumbered or edited — superseded by new entries | Milestone-local decisions (those live in the milestone file) |
| `project/reviews/` | RB briefs and RR reports for Fable escalation | Anything else |
| `project/references/` | Primary sources, bibliography, oracle registry | Anything else |

Boundary rule, one line: **Architecture → DESIGN · Status → ROADMAP · Tasks →
milestone files · Decisions → DECISIONS · History → archive + git log.**

### 3.3 Weight caps

Enforced by the `/milestone` health audit (§5.1):

- `CLAUDE.md` < 80 lines
- `project/ROADMAP.md` < 60 lines
- Active milestone file < 150 lines
- Archived milestone summary ≤ 25 lines
- Work-log entries: one line each; **never** paste command output or subagent
  transcripts into tracking files — summarize.

### 3.4 Universal tracking rules

- **Tracking travels with code.** Every commit that changes code also updates
  the milestone checkboxes/work-log in the same commit.
- **Absolute dates only** (YYYY-MM-DD); never "yesterday" or "last week".
- **Append, don't rewrite.** Work-logs and DECISIONS.md are append-only;
  supersede, never edit history. Never fabricate history — if there's a gap,
  add one catch-up entry summarizing `git log`.
- **Stop points are commit points.** Never end a session or turn with
  uncommitted work — checkpoint-commit code and tracking together (even
  half-done, marked as such in the work-log) so any future session resumes
  statelessly from files + git, never from what a previous session "was
  about to do".
- **Git is ground truth for code.** If commits were made outside the system
  (manual edits, other tools), the `/milestone` audit reconciles: a catch-up
  work-log line summarizing them, never retroactive rewriting.
- **User overrides are logged, never resisted.** When the user says to skip
  a gate or bend a rule, comply — and record the override in the work-log
  ("merged without CI at user request, YYYY-MM-DD"). The system's job is an
  honest record, not an argument; the record is what keeps the next session
  from mistaking an exception for a precedent.
- **Tracking files outrank memory.** Claude's persistent memory must never
  hold project state (status, milestones, decisions, architecture) — that
  belongs to `project/` files, which are the source of truth on any conflict.
  Memory is for meta-context only (user preferences, how Jeff likes to work).
  This rule is stated in tracking-rules.md and in the CLAUDE.md section, so
  the two systems complement rather than compete.

---

## 4. Milestones: IDs, status, ordering

### 4.1 IDs are identifiers, not a sequence

- `M<NN>` (zero-padded to two digits: M01, M02, …), assigned at planning time,
  **monotonically increasing, never reused** — including for dropped
  milestones. Past M99 the ID simply grows (M100); lexicographic file sorting
  degrades slightly at that point, but nothing depends on it — the ROADMAP
  index is the authority and is grouped by status, not filename order.
- **No completion-order requirement.** M09 may finish before M05. The old
  "next milestone must be prior+1" rule is abolished.
- Ordering of *work* is governed by two things only: each milestone's
  `Depends on:` field (a milestone isn't workable until its dependencies are
  `done`) and its `Priority:` (high / normal / low) in the ROADMAP index.
- The ROADMAP index table is **grouped by status** (in-progress/blocked/review
  first, then planned by priority, then candidates), not sorted by ID.
- Archived files keep their ID: `archive/M07-<slug>.md`.
- **Doc hygiene:** user-facing materials (NEWS.md, README, vignettes, pkgdown)
  never reference milestone numbers — those are internal bookkeeping.

### 4.2 Status vocabulary (frozen — exactly these seven)

`candidate | planned | blocked | in-progress | review | done | dropped`

| Status | Meaning | Set by (gatekeeper) |
|---|---|---|
| `candidate` | Idea captured as a ROADMAP row; may have no milestone file yet | anyone, any time |
| `planned` | Fully planned: milestone file exists with goal, In/Out scope, verifiable acceptance criteria, ordered tasks, dependencies | `/milestone-plan` only |
| `in-progress` | Being worked on a branch. **At most ONE at a time.** | `/milestone-implement` only |
| `blocked` | Waiting on something external — a dependency, an answer, or an open RB. Work-log line names the blocker. | any skill, with the reason logged |
| `review` | Implementation complete (tasks checked, local checks clean); awaiting verification + merge approval | `/milestone-implement` on completion |
| `done` | Every acceptance criterion executed with fresh evidence; PR merged; file compressed and archived | `/milestone-review` only |
| `dropped` | Deliberately abandoned; one-line summary with reason archived | user decision, via any skill |

Transitions: `candidate → planned → in-progress ⇄ blocked; in-progress →
review → done` (review failures return to `in-progress`); anything can go to
`dropped`. Skipping states is not allowed except `candidate → dropped`.

### 4.3 Milestone sizing, scoping, and subdivision

The milestone is the **only** unit of subdivision above the task. No slices,
phases, or sub-milestones inside a milestone file — past projects that grew
internal "slices" were signalling that the milestone should have been split.
If structure is emerging inside a milestone, split it and wire the pieces
with `Depends on:`.

**Size target:** one milestone = one reviewable PR = roughly 1–3 working
sessions. Concrete tripwires — if any of these is true at planning time,
split before setting `planned`:

- More than ~7 acceptance criteria or ~10 tasks.
- The goal sentence needs an "and" joining two unrelated outcomes.
- Some tasks could ship usefully even if the rest were dropped (that's two
  milestones with a dependency).
- The active file can't plausibly stay under its 150-line cap.

When a tripwire fires, the planning run **emits multiple milestone files at
once** (§5.2) — splitting never means discarding the remainder.

**How to split:** prefer **vertical slices** (a thin end-to-end capability —
one function family working, documented, and tested) over horizontal layers
("all the code" then "all the tests" then "all the docs"). Every milestone
must leave main shippable after its merge — a milestone that ends in a
half-wired state is a layer, not a slice. Shared groundwork that multiple
slices need may be its own small milestone (e.g., "M12: scaffolding for X"),
but never a "misc cleanup" grab-bag — those become `candidate` rows instead.

`/milestone-plan` enforces this: sizing is a standard item at its question
gate ("this looks like 2 milestones; here's the proposed cut — agree?"), and
it refuses to mark a tripwire-violating plan `planned` without explicit user
override.

### 4.4 Work that isn't a milestone

Not everything deserves the machinery. Three tiers:

- **Trivial path** — no runtime surface (typos, tracking updates, comment
  fixes): direct commit to main (§7). No tracking beyond the commit itself.
- **Hotfix path** — a user-visible bug that shouldn't wait for milestone
  ceremony: branch `hotfix-<slug>`, fix with a regression test, run
  `devtools::test()` + `check()`, PR, merge. Record: NEWS.md entry + the PR;
  if the fix reveals deeper work, add a `candidate` row. No milestone file.
- **Milestone** — everything else. Threshold: if the work needs more than
  one sitting, changes exported behavior (beyond restoring documented
  behavior), or requires a design decision, it's a milestone.

**GitHub issue intake:** external issues are triaged into ROADMAP `candidate`
rows (one line, linking the issue) or handled via the hotfix path. Milestone
files list the issues they close in Notes; the PR description uses
`Fixes #N` so GitHub closes them on merge. Issues are an inbox, never a
second tracking system — the ROADMAP row is the canonical record.

**External contributor PRs** are a third inbox (these repos are public).
Triage on arrival: small and correct → review it to the hotfix bar
(regression test present or added, `test()`/`check()` clean, NEWS entry) and
merge with the user's approval; larger or design-touching → it becomes or
joins a milestone — a `candidate`/`planned` row linking the PR, with the
contribution reviewed under that milestone's criteria. Never merged outside
one of these two paths, and never left untriaged in the audit.

**How each tier is initiated.** A skill exists where a multi-step protocol
must be enforced; plain rules-in-context suffice where the action is a
single safe edit:

- **Trivial path:** no skill — just ask in conversation. The §7 carve-out
  lives in the CLAUDE.md section (always in context), so any session knows
  typo-class work commits directly to main.
- **Hotfix path:** `/hotfix` (§5.9). Explicitly invocable, but its skill
  description is written to **auto-trigger** on bug-fix requests ("users
  report an error in X", "fix this crash") so the protocol applies even
  when the user just describes the bug — the skill's first job is the tier
  check: too big for a hotfix → routing chip to `/milestone-plan`.
- **Candidate capture:** no skill — "add X to the candidates" in any
  session appends a one-line ROADMAP row (§4.2 allows `candidate` to be set
  by anyone, any time). Batch issue triage works the same way
  conversationally ("triage the open GitHub issues"); the `/milestone`
  audit verifies the results are well-formed either way.
- **Milestone work:** always through the phase skills — the whole point is
  that this tier is never initiated casually.

---

## 5. Skills & workflow

Eight skills. Separate slash commands per phase (fast to type, clear intent),
glued together by **routing chips**: every phase ends with an AskUserQuestion
call whose options include the natural next phase. Claude Code renders
AskUserQuestion as clickable option buttons ("chips"); when the user clicks
one, the model invokes the corresponding skill in the same session. One click
instead of typing the next command, but every transition is an explicit user
stop — never an auto-proceed. Example of what the user sees at the end of
`/milestone-implement`:

> **How should I proceed with M07?**
> `[ Proceed to review (Recommended) ]` — runs /milestone-review M07
> `[ Adjust first ]` — make changes on the branch before review
> `[ Pause here ]` — stop; milestone stays at `review`
> `[ Other… ]` — free-text (treated as adjustment instructions)

**Session-start protocol** (every skill, first thing):
1. Read `shared/tracking-rules.md` from the plugin.
2. Read `project/ROADMAP.md`, then the target/active milestone file, then
   `project/DECISIONS.md`. Read nothing else from `project/` unless a step
   requires it.
3. Check `project/reviews/`: if an `RR<NN>-*.md` exists for an open brief, run
   **RR ingestion** (§5.6) before anything else.

**Question gates.** User interaction happens at exactly three gates — plan
questions, pre-implementation questions, final merge approval — plus the
routing chips. At a gate, ask one batched round of 2–5 concrete decision
questions via AskUserQuestion, each with a recommendation and brief pros/cons.
Between gates, work autonomously; never drip questions one at a time.

### 5.1 `/milestone` — entry point, status, health audit

The "where am I?" command and the system's immune system.

1. Snapshot: current in-progress/blocked/review milestones, next planned by
   priority, open RBs.
2. Health audit — fix mechanical problems immediately, report the rest:
   - ROADMAP vs milestone-file headers consistent; ≤ 1 `in-progress`.
   - Weight caps (§3.3) respected — with named remedies, never "let it
     grow": over-cap ROADMAP → graduate or prune candidates; over-cap
     milestone file → split the milestone or move reference material to
     `references/`; over-cap CLAUDE.md → push content to its §3.2 owner.
   - **Dangling dependencies:** every `Depends on:` resolves to a live or
     `done` milestone; references to `dropped`/nonexistent IDs are flagged
     for re-wiring or unblocking.
   - Staleness: `in-progress` with no work-log entry in 14+ days; open RB
     with no RR after 7+ days (remind the user to run it); `candidate` rows
     untouched for ~6 months → triage chip (promote / keep / drop — never
     auto-deleted).
   - Orphans: `done` not archived; RRs not ingested; milestone files missing
     from ROADMAP or vice versa; uncommitted changes under `project/`.
   - **ID uniqueness:** no M-number appears twice across active + archive.
   - **CLAUDE.md section present and intact** (other tools can clobber it);
     if damaged, offer repair via `/rpkg-init`.
3. End with a routing chip: the single most sensible next action
   (e.g., "Resume M07 (implement)" / "Plan next milestone" / "Run review").

### 5.2 `/milestone-plan [title]`

1. Session-start protocol. Confirm nothing else is `in-progress` (or get
   sign-off to plan ahead).
2. Investigate first: read relevant code and DECISIONS.md; for scopes touching
   more than a couple of files, fan out **Explore subagents** with specific
   focuses and require file:line citations. Draft scope, tasks, and the list
   of genuinely open decisions internally.
   **Collision check (mandatory):** sweep the ROADMAP (all statuses), the
   archive, and DECISIONS.md for overlap with what the user is describing.
   Prior state is *surfaced at the question gate*, never silently obeyed or
   silently overridden. Disposition by what it hits:
   - **`candidate` row** → the normal promotion path: this planning run
     absorbs the row (note the lineage, remove/convert the row).
   - **`planned` milestone** → no duplicates. Options: amend that milestone's
     file, supersede its plan entirely, or confirm the scopes are genuinely
     distinct and cross-reference them.
   - **`in-progress` milestone** → fold into it via the amendment protocol
     (§5.3), or plan as a separate milestone with `Depends on:` it.
   - **`done` (archived)** → it shipped. Tell the user (it may already do
     what they want); if not, plan as an extension referencing the old ID.
   - **`dropped` milestone or a D-entry rejection** → quote the prior
     rationale verbatim ("D-014 rejected X because Y — does that still
     hold?"). If the user wants to proceed anyway: **supersede, don't
     ignore** — append a new D-entry superseding the old one, then plan
     normally. Never plan against a standing rejection without superseding
     it, and never refuse to plan merely because a rejection exists — the
     user outranks the record, but the record must be updated to say so.
3. **Question gate:** pose the open decisions (scope boundary, sequencing,
   acceptance bar) in one batched round. When proposing a scope cut, the
   proposal must include **where the remainder goes** — never just "M12
   covers A and B", but "M12 covers A and B; C becomes M13, planned now,
   depends on M12; D becomes a candidate row; E sounds like you don't
   actually want it — drop entirely?".
4. Solidify autonomously. Create **one or more** milestone files from the
   template (§6.1) — when the user's request splits (§4.3 tripwires), the
   answer is multiple milestones in one planning run, not shrink-to-fit and
   discard. For each file:
   - Acceptance criteria **verifiable with evidence** — a test that passes,
     `devtools::check()` output, a file that exists. Never vibes.
   - Scope has explicit **Out:** items — what this milestone refuses to do.
     `Out:` means "not in *this* milestone"; where the item lives instead is
     named right there (e.g., `Out: batch scoring → M13`).
   - Tasks sized to one working session or less, ordered by dependency.
   Deferred chunks not yet plannable get `candidate` ROADMAP rows instead of
   files.
5. **Remainder ledger (conservation check):** before committing, enumerate
   every distinct thing the user originally asked for and its disposition —
   in this milestone / planned as M<NN> / candidate row / dropped at the
   user's explicit request. Nothing may be silently absent, and **deferral
   is never recorded as a decision not to do something**: DECISIONS.md
   D-entries are reserved for genuine "we considered X and rejected it
   because…" outcomes with rationale. Postponement lives in the ROADMAP,
   where it stays visible and actionable. Include the ledger in the plan
   summary presented to the user.
6. Add/update the ROADMAP rows (`planned` / `candidate`); commit the tracking
   files **directly to main, no branch, no PR** — commit message
   `plan M<NN>[, M<NN>…]: <title>`. Rationale: planning touches only
   `project/` (which is `.Rbuildignore`d), so main stays installable; the
   milestone branch doesn't exist yet and a PR for docs-only bookkeeping is
   ceremony. This is the §7 "docs-only tracking commit" carve-out.
   **Planning is atomic:** files, ROADMAP rows, and the commit land as one
   unit — a session dying mid-plan must not leave a half-planned ghost.
7. Routing chip: **Start implementing M<NN>** (the proximal one) /
   Plan another / Stop here.

### 5.3 `/milestone-implement <id>`

1. Session-start protocol. Verify status `planned` (or resume `in-progress` /
   `blocked`-with-resolved-RB). Set `in-progress` in ROADMAP + header mirror.
2. First session only: update main, then `git checkout -b m<nn>-<slug>`.
   Later sessions resume the branch — and if main has moved since the branch
   was cut (e.g., a hotfix merged), merge main into the branch and re-run
   `devtools::test()` before continuing, so the branch never drifts silently
   behind reality. In all cases check `git status` first: a dirty tree with
   unrelated changes means ask the user — never sweep strangers into a
   checkpoint commit.
3. **Question gate:** surface implementation choices the plan left open (API
   shape, naming, dependency picks). Skip only if nothing is genuinely open.
4. Work tasks in order, autonomously:
   - Tests first where feasible (testthat 3e); numeric results verified per
     the oracle doctrine (§9.1).
   - Gates per task: `devtools::document()` after roxygen edits;
     `devtools::test()` clean before checking a task off.
   - Checkpoint-commit per task on the branch, **including** the milestone
     file update (checkbox + one work-log line). Branch commits are cheap —
     the squash-merge erases them.
5. Delegation per the model strategy (§8).
6. **Plan amendments** (implementation always learns things planning didn't
   know):
   - *Minor* — reorder tasks, refine wording, add a discovered sub-task:
     edit the milestone file directly, one work-log line noting the change.
   - *Substantive* — an acceptance criterion must change, or scope must
     grow/shrink: mini question gate (AskUserQuestion with recommendation);
     record the amendment as a dated work-log line, and a D-entry if it's a
     cross-cutting reversal.
   - *The goal itself is wrong* — stop; status back to `planned`; chip to
     re-run `/milestone-plan` for a proper re-cut (possibly splitting).
   Never silently deliver something other than what the plan promised —
   the review gate checks criteria as written.
7. If blocked on a question needing Fable: chip to `/milestone-brief`, stop.
8. When all tasks are checked and `devtools::check()` is clean: set status
   `review`, then stop with a recap — file-level summary of the branch diff,
   test/check results, deviations from plan, open concerns — and a routing
   chip: **Proceed to review** (recommended) / Adjust first / Pause here.

### 5.4 `/milestone-review <id>`

1. Session-start protocol. Status must be `review` (or user overrides).
2. **Sync with main first:** if main has moved since the branch was cut,
   merge main into the branch and re-run tests before gathering any
   evidence — evidence from a stale branch is worthless and the squash-merge
   would conflict anyway. Then push the branch; open a **draft PR** so CI
   runs while the review proceeds.
3. Execute **every acceptance criterion with fresh evidence** — actually run
   the tests and `devtools::check()`; record results in the milestone's
   Review section. Then run the **consistency gate** — mechanical checks for
   the things sessions habitually forget, verified by command rather than
   recall:
   - `devtools::document()` produces no diff (docs in sync with roxygen).
   - If README.Rmd exists and differs meaningfully from README.md's render:
     `devtools::build_readme()` and commit the result.
   - If the package has a pkgdown site: `pkgdown::check_pkgdown()` passes —
     this catches exported objects missing from `_pkgdown.yml`'s reference
     index.
   - `NEWS.md` has an entry for this milestone's user-visible changes.
   - New top-level files have `.Rbuildignore` entries (check `check()` NOTEs).
   **Criteria are never reinterpreted at review.** If the work seems right
   but a criterion as written fails, the criterion is wrong — send the
   milestone back for a gated amendment (§5.3 step 6), then re-review. A
   charitable reading at review time silently destroys what the criteria
   are for.
   Any failure → status back to `in-progress`, work-log line naming exactly
   what failed, stop. **Thrash rule:** if this is the milestone's third trip
   back from review (count the work-log), do not queue a third retry —
   that's a mis-planned milestone. Recommend re-plan or split via
   `/milestone-plan` instead.
4. **Fresh-context review:** spawn an Opus subagent that has not seen the
   implementation to review the full diff (`git diff main..HEAD`) against the
   acceptance criteria, DESIGN.md conventions, and DECISIONS.md. Triage its
   findings: fix now / spawn follow-up milestone / reject with logged reason.
5. Update NEWS.md under the development-version heading (no milestone
   numbers); final checkpoint commit.
6. **Final approval gate:** present acceptance-criteria evidence, problems
   found and their handling, diffstat, anything the user should eyeball; ask
   plainly for authorization to merge. Approval withheld → log requested
   changes as tasks, back to `in-progress`, stop.
7. On approval only: mark PR ready, require green CI (fix on branch if red),
   then `gh pr merge --squash --delete-branch`.
8. Post-merge hygiene pass on main: compress the milestone file to a ≤25-line
   summary (goal, outcome, key decisions, PR link) → `milestones/archive/`;
   ROADMAP row → `done` + archive path; archive resolved RB/RR pairs; verify
   weight caps. Docs-only commit: `review M<NN>: done`.
9. Routing chip: **Plan next milestone** / Run `/milestone` audit / Stop.

### 5.5 `/milestone-brief <id> <topic>` — Fable escalation (RB)

For questions needing Fable-level rigor (statistical correctness, high-stakes
design). Verified fact (2026-07): a main session on any model **can** spawn a
Fable subagent (`model: "fable"` via the Agent tool or agent frontmatter), but
Fable is token-billed pay-per-use even on subscription plans — so spawning is
**gated behind explicit user approval, every time, with no standing
authorization.**

Either way, the brief artifact comes first — it's what makes the review
reproducible and its findings ingestible:

1. Create `project/reviews/RB<NN>-<slug>.md` from the template (§6.2): fully
   self-contained (assume zero conversation context) — background, exact
   files/lines to examine, numbered specific questions (never "thoughts?"),
   constraints, and the required output path `RR<NN>-<slug>.md`.
2. Set the milestone `blocked` (work-log line: "blocked on RB<NN>"). Commit.
3. **Approval gate (AskUserQuestion):** present the brief's scope, a rough
   size estimate (files/lines Fable must read), and a reminder that Fable is
   token-billed. Options:
   - **Spawn Fable subagent** (default recommendation) — on approval, launch
     an Agent with `model: "fable"` prompted only with: read the RB file and
     follow its instructions exactly, writing findings to the RR path. When
     it returns, run RR ingestion (§5.6) immediately in the same session.
   - **I'll run it manually** — tell the user verbatim:
     > Open a fresh Fable session in the repo root and prompt:
     > `Read project/reviews/RB<NN>-<slug>.md and follow its instructions exactly.`
     Then stop the turn; ingestion happens at the next session start.
   - **Cancel** — unblock the milestone and note the question as unresolved.
4. Never spawn Fable without this gate, and never proceed past the blocking
   question while the RB is open.

### 5.6 RR ingestion (immediately after a spawned review returns, or
automatically at session start when a manual RR appears)

When an `RR<NN>` artifact appears: read it; record answers as dated entries in
the milestone's Decisions section (promote cross-cutting ones to
DECISIONS.md); apply or schedule recommendations as tasks; move the RB/RR pair
to `reviews/archive/`; status back to `in-progress`; commit.

Two robustness rules:

- **If an RR recommendation contradicts a standing D-entry**, apply the same
  supersede-don't-ignore rule as the planning collision check (§5.2): quote
  the prior rationale to the user, and only proceed by appending a
  superseding D-entry — never by silently overriding the record (or silently
  discarding Fable's advice).
- **If the user pastes RR content into chat** instead of the file (common
  when running the brief manually), normalize it: write the RR file from the
  pasted content verbatim, then ingest as usual. Never reject usable review
  output on formal grounds. An RR that fails to answer the brief's questions
  is marked unresolved and a fresh RB (new number) is drafted rather than
  re-ingesting a bad artifact.

### 5.7 `/rpkg-init`

As specified in §2.2.

### 5.8 `/rpkg-release`

CRAN release walk, adapted from circumplex's proven `/release-checklist`:
version bump decision (patch/minor/major), NEWS.md consolidation for the
release heading, `devtools::check()` + reverse-dependency checks as
applicable, `cran-comments.md` update, win-builder/rhub as needed, and a
final human checklist. **Never self-submits to CRAN** — it prepares
everything and hands the submission step to the user. Requires no milestone
`in-progress` (release from a clean main).

### 5.9 `/hotfix [description]`

The enforced version of the §4.4 hotfix path. Invocable explicitly, and its
skill description auto-triggers on bug-fix requests so users can simply
describe the bug.

1. **Tier check first:** reproduce or at least localize the bug. If the fix
   needs a design decision, changes exported behavior beyond restoring
   documented behavior, or won't fit one sitting — stop, add a `candidate`
   row (or chip to `/milestone-plan` if urgent), and say why.
2. Branch `hotfix-<slug>` from up-to-date main. Write the **regression test
   first** (failing), then the fix.
3. Gate-lite: `devtools::test()` + `devtools::document()` (and
   `devtools::check()` if the fix touched anything structural).
4. NEWS.md entry under the development version; `Fixes #N` in the PR
   description if an issue exists. Open the PR.
5. **Approval gate:** present the diff, test evidence, and NEWS line; merge
   (squash) only on explicit user approval. If the fix revealed deeper work,
   add a `candidate` row before closing out.

---

## 6. Templates (shipped in `skills/shared/templates/`)

### 6.1 Milestone file — `milestone.md`

```markdown
# M<NN>: <Title>

- **Status:** planned   <!-- mirror; ROADMAP.md is the authority -->
- **Priority:** normal
- **Depends on:** M<xx>, M<yy> (or —)
- **Branch/PR:** — <!-- m<nn>-<slug>; PR URL once opened -->

## Goal
One sentence.

## Scope
**In:** what this milestone does.
**Out:** what it explicitly refuses to do.

## Acceptance criteria
- [ ] Each objectively checkable (a command that passes, a file that exists).
- [ ] Always for code milestones: `devtools::check()` clean.

## Tasks
- [ ] Ordered concrete steps with file:line references where known.

## Work log  <!-- append-only, one line per entry -->
- YYYY-MM-DD: ...

## Decisions  <!-- milestone-local; promote cross-cutting ones to DECISIONS.md -->

## Review  <!-- evidence per acceptance criterion; subagent findings + triage -->
```

### 6.2 Review Brief — `brief.md`

```markdown
# RB<NN>: <Topic> (M<NN>)

**Date:** YYYY-MM-DD
**Output required:** write findings to `project/reviews/RR<NN>-<slug>.md`

## Background
Self-contained context — assume the reader has NOT seen any conversation.

## Materials
Exact files/lines to examine; how to run relevant code/tests.

## Questions
1. Numbered, specific, answerable. Never "any thoughts?"

## Constraints
What is fixed and must not be relitigated (link D-entries).
```

### 6.3 Decision entry — `decision.md` (append to DECISIONS.md)

```markdown
### D-00N (YYYY-MM-DD): Title
**Context:** 1–2 lines.
**Decision:** 1–2 lines.
**Consequences:** 1–2 lines. (Supersedes D-0xx, if any.)
```

D-entries record *choices with rationale* — including genuine rejections
("considered X, rejected because…"). They never record deferrals: "not now"
is a ROADMAP fact (`candidate` row or future milestone), not a decision
(§5.2 step 5).

### 6.4 CLAUDE.md section — `claude-md-section.md`

The block `/rpkg-init` appends: pointer to `project/`, the one-line boundary
rule, the skill list, and the "no status/TODOs in this file" warning.

---

## 7. Git & approval model

- **main is a distribution channel**, not just a dev branch (users install via
  `pak::pak()`; pkgdown may deploy from it). It must stay installable.
- main accepts only: docs-only tracking commits (from plan / hygiene passes)
  and squash-merges of milestone branches. **Never implement on main.**
- Milestone work happens on `m<nn>-<slug>`, cut from up-to-date main. Commit
  freely there — checkpoints are squashed away.
- **Nothing reaches main without the user's explicit approval at the review
  gate.** Never force-push; never merge red or pending CI.
- Trivial edits with no runtime surface (typos, tracking updates) may commit
  directly to main.

### 7.1 Waiting on CI and background work

Past failure mode: Claude polls CI or a local background task, misses the
completion, or leaves orphaned monitoring "tasks" dangling across sessions.
Rules:

- **Prefer blocking waits over polling.** For CI: `gh pr checks <pr> --watch`
  (or `gh run watch <id>`) in the foreground with an explicit timeout — one
  command that returns when CI resolves. Never spawn a background watcher
  and continue other work "until it finishes".
- **At most one wait at a time,** and it must resolve within the current
  turn. If the timeout expires: report the actual current state (from a
  fresh `gh pr checks`), add a one-line work-log entry ("CI pending on PR
  #N as of YYYY-MM-DD"), and stop — do not leave anything watching.
- **Resume is stateless.** No session ever trusts a remembered "CI was
  running" — the PR URL lives in the milestone header, and status is always
  re-derived on demand from `gh pr checks` / `gh run list`. The same applies
  to local long-running jobs: record how to check (the command), never the
  belief about their state.
- The `/milestone` health audit treats a milestone sitting at `review` with
  an open unmerged PR as a prompt to re-check CI, not as an error.

---

## 8. Model & agent strategy

- **Orchestrator: Opus**, running the skills in the main session.
- **Sonnet subagents** (`model: "sonnet"`): well-specified, self-contained
  work — fan-out searches (Explore), mechanical migrations, test writing
  against a spec, formatting/boilerplate. Give complete specs; verify their
  diffs before committing. Summarize results into one work-log line.
- **Opus subagents** (`model: "opus"`): design-sensitive implementation,
  parallel worktree work, and always the fresh-context review at §5.4.
- **Never Haiku.** For anything. Accuracy-critical work uses the inherited
  model or stronger.
- **Fable subagents** (`model: "fable"`): allowed, but **only** through the
  RB/RR brief protocol (§5.5) and only after the per-instance approval gate —
  Fable is token-billed pay-per-use, so no standing authorization exists. The
  orchestrator should proactively recommend an RB — with a short rationale —
  whenever statistical correctness or a high-stakes design question exceeds
  what a fresh Opus review can settle. Ad-hoc Fable spawning outside the
  brief protocol is prohibited: the brief artifact is what makes the
  escalation reproducible, auditable, and ingestible.

---

## 9. Validation doctrine & R package guardrails

### 9.1 Oracle strategy (opt-in section for statistical packages)

A test that asserts whatever the code currently produces enshrines bugs.
Every numeric-results test suite includes, in priority order:

1. **Hand-computed fixtures** — tiny synthetic datasets scored by hand from
   published formulas/instructions, exact expected values asserted, with the
   hand-worked arithmetic in comments.
2. **Published reference values** — worked examples from papers or official
   materials (cite the source in the test).
3. **Independent recomputation** — recompute at least one result inside the
   test with deliberately dumb, explicit code and compare to the package's
   general implementation; the only check that catches transcription errors.
4. **Invariant tests** — properties that must hold for any input.

Snapshot tests only *on top of* the above (message wording etc.), never as
the sole oracle for a numeric result.

**Primary sources rule (hard stop).** Never substitute secondary
descriptions or model memory for a primary source on scoring/algorithmic
content. When a primary source (paper, preprint, chapter, manual, scoring
key) is needed: search for it (DOI, publisher, OSF); if it cannot be
accessed, **stop and ask the user to supply the PDF** — do not proceed from
memory. Enforced at the two places sources matter: `/milestone-plan`
(criteria that cite a formula/value must name their source) and
`/milestone-review` (evidence tracing to "model memory" fails the criterion).

**Source ingestion protocol.** When a PDF is supplied or a source is
otherwise ingested, standardize its capture in `project/references/`:

1. Save the PDF to `project/references/pdf/` — **gitignored and
   .Rbuildignore'd** (copyright: these repos are public; also repo weight).
2. Create `project/references/<citekey>.md` (e.g., `wright2012pid5.md`) —
   committed. Contents: full citation + DOI/URL; what was extracted
   (formulas, cutoffs, item keys, worked examples) with **page/table
   anchors**; verbatim-critical values quoted exactly; which tests/oracles
   trace to it; open questions about the source.
3. Add one line to `project/references/INDEX.md` (citekey — title — what it
   anchors).

Tests and milestone files cite `citekey (p. N)` rather than restating source
content — the summary file is the single ingestion point, so a source is
read once and reused everywhere (including by subagents that can't see the
original conversation).

### 9.2 R package guardrails

- After roxygen changes: `Rscript -e 'devtools::document()'`. After code
  changes: `Rscript -e 'devtools::test()'`. At review: `devtools::check()`.
- Never hand-edit `NAMESPACE`, `man/`, or `data/*.rda`; data regenerates from
  `data-raw/` scripts.
- README.md is knitted from README.Rmd (`devtools::build_readme()`).
- **Dependency changes are never unilateral.** Adding, removing, or moving a
  package between Imports/Suggests is always a question-gate item and gets a
  D-entry (what it's for, why this package, Imports-vs-Suggests rationale).
- Breaking changes to exported behavior follow a deprecation cycle
  (lifecycle badges, `lifecycle::deprecate_warn()` before removal) unless
  the package is pre-1.0 and the user explicitly waives it.
- Every newly exported object gets a row in `_pkgdown.yml`'s reference index
  in the same commit that exports it (verified mechanically at review via
  `pkgdown::check_pkgdown()`).
- New user-facing conditions use `cli::cli_abort()` / rlang, not assertthat.
- New top-level tracked files/dirs need `.Rbuildignore` entries (`^project$`
  is added by `/rpkg-init`).

These guardrails are advisory in the moment but **mechanically enforced at
the review consistency gate (§5.4)** — the reliable fix for habitual
omissions is a deterministic command at a mandatory gate, not hoping the
model remembers mid-task. (A future enhancement could ship plugin hooks for
immediate feedback — e.g., a reminder after editing README.Rmd — but v1
relies on the gate.)

### 9.3 What gets a test (and what doesn't)

No coverage-percentage target — a global number invites padding tests to
please a dial. Instead, test scope is decided at **planning time**: each
milestone's acceptance criteria name the behavior that must be tested, so
"is it tested enough?" is settled per milestone, with evidence, at review.
The rules of thumb the plan skill applies:

**Always tested:**
- Every **exported function**: at least one happy-path test on
  representative input, every documented error condition (each
  `cli_abort()` branch fires on the input that should trigger it), and the
  edge cases R is famous for — zero-row input, `NA` handling, length-one
  vectors, factor vs. character, empty strings.
- Every **numeric result**: per the oracle doctrine (§9.1) — an oracle,
  not a snapshot.
- Every **bug fix**: a regression test that fails before the fix (§5.9).
- Every **claimed behavior in documentation**: if a roxygen example or
  vignette asserts something works, a test asserts it too.

**Tested indirectly (through exported callers), by default:**
- Internal helpers. Direct unit tests only when a helper embodies
  independent logic (parsing, nontrivial math) that's awkward to exercise
  through the public API — otherwise helper tests just cement the current
  factoring and punish refactors.

**Not tested:**
- Cosmetics of printed output beyond a snapshot where wording is the
  product (cli messages users are meant to read).
- Trivial pass-through wrappers with no logic of their own.
- The behavior of dependencies (don't test that `dplyr::filter()` works).
- Plots, except `vdiffr` snapshots when the plot *is* the product.

**Test the contract, not the implementation:** assert on outputs and
observable behavior, never on internal call structure; avoid mocks unless
isolating true external effects (network, filesystem). A test that breaks
under a behavior-preserving refactor is a defect in the test.

Coverage tooling (`covr`) is a **diagnostic, not a gate**: run it
occasionally to *find* untested exported behavior; a low number is a prompt
to look, never a criterion to satisfy.

---

## 10. Resolved questions (review pass, 2026-07-11)

Decisions from the first review, now folded into the spec above:

1. **LOG.md dropped.** History = per-milestone work-logs + archived summaries
   + DECISIONS.md + git log.
2. **Combined `/milestone`** entry-point + health audit (§5.1); no separate
   `/milestone-status`.
3. **Weight caps** start at 80/60/150/25; adjust after real use.
4. **Two-digit zero-padding** (M01); IDs grow naturally past M99 with only
   cosmetic file-sort impact (§4.1).
5. **`/rpkg-release` included in v1** (§5.8), adapted from circumplex.
6. **Manual plugin install only** for now; marketplace publishing deferred
   (§2.3).
7. **Fable subagents are possible and permitted** — but only via the RB/RR
   protocol with a per-instance approval gate (§5.5, §8); the manual
   clean-session route remains as a fallback.
8. **Acceptance criteria stay above Tasks** in the milestone template:
   criteria define "done" and tasks derive from them; reviewers and resuming
   sessions should hit the definition of done before the how.
9. **Primary-source hard stop + source ingestion protocol** added (§9.1);
   PDFs gitignored, per-source summary files committed.
10. **Memory non-compete rule** added (§3.4): project state never goes in
    Claude's persistent memory; `project/` files win on any conflict.

Second review pass (2026-07-11):

11. **Milestone sizing/subdivision nailed down** (§4.3): no slices or
    sub-milestones — tasks are the only unit inside a milestone; concrete
    split tripwires; vertical slices over horizontal layers; enforced at the
    plan question gate.
12. **CI/background-work waiting rules** (§7.1): blocking watch commands
    with timeouts, one wait at a time resolved within the turn, stateless
    resume from `gh pr checks` — never from remembered state.
13. **Habitual omissions** (README knit, pkgdown reference index, doc sync)
    are fixed by the mechanical **consistency gate** in `/milestone-review`
    (§5.4), not by separate skills; guardrails (§9.2) remain as in-the-moment
    advisories. Read-before-edit errors are harness-level and self-correcting
    — out of scope.

Third review pass (2026-07-11):

14. **Non-milestone work tiers** (§4.4): trivial path / hotfix path /
    milestone, with an explicit threshold; GitHub issues triage into
    `candidate` rows — an inbox, never a second tracking system.
15. **Plan amendment protocol** (§5.3 step 6): minor edits logged; substantive
    changes gated; wrong goal → back to `planned` and re-plan. Never silently
    deliver something other than what the plan promised.
16. **Stop points are commit points + git is ground truth** (§3.4): stateless
    resume from files + git; outside-system commits reconciled by catch-up
    work-log lines.
17. **Dependency & deprecation policy** (§9.2): dependency changes always
    gated + D-entried; breaking changes follow a lifecycle deprecation cycle
    unless pre-1.0 and explicitly waived.
18. **Pilot rollout plan** (§11) added: build v0.1 → pilot in one fresh and
    one migrated repo → refine → public release.
19. **Initiation of non-milestone work** (§4.4, §5.9): trivial edits and
    candidate capture are conversational (rules-in-context via the CLAUDE.md
    section); hotfixes get an eighth skill, `/hotfix`, that auto-triggers on
    bug-fix requests and starts with a tier check. Skills exist where a
    protocol must be enforced; rules suffice for single safe edits.
20. **User guide added** (§12), destined to become the core of the public
    README: quickstart, the core loop, a which-skill-when table, what the
    system expects from the user, healthy habits, and explicit non-goals.
21. **Remainder ledger** (§5.2 step 5): planning conserves the user's
    request — every asked-for item is dispositioned (this milestone /
    planned follow-up milestone / candidate row / explicitly dropped), the
    plan skill may emit multiple milestone files in one run, `Out:` items
    name where the work lives instead, and **deferral is never recorded as
    a decision not to do something** — D-entries are for genuine rejections
    with rationale; postponement lives in the ROADMAP (§6.3).
22. **Collision check in planning** (§5.2 step 2): overlap with existing
    candidates/milestones/decisions is mandatory to detect and is surfaced
    at the question gate — candidates get promoted, duplicates get amended
    or superseded, shipped work gets pointed out, and prior rejections are
    quoted with their rationale and must be explicitly superseded (new
    D-entry) before planning proceeds against them. The user outranks the
    record; the record must be updated to say so.

Fourth review pass (2026-07-11) — edge-case hardening:

23. **Seven edge-case fixes:** dangling-dependency detection in the audit
    (§5.1); milestone branches must sync with a moved main before resuming
    or reviewing (§5.3, §5.4); review thrash rule — third bounce means
    re-plan, not retry (§5.4); criteria are never reinterpreted at review —
    wrong criteria go back for gated amendment (§5.4); external contributor
    PRs get a triage path (§4.4); RR-vs-D-entry conflicts use
    supersede-don't-ignore (§5.6); candidate-rot triage and named weight-cap
    remedies in the audit (§5.1).
24. **Cheap robustness checks:** dirty-tree check before branching (§5.3),
    atomic planning commits (§5.2), ID-uniqueness and CLAUDE.md-section
    checks in the audit (§5.1), non-package repo detection in `/rpkg-init`
    (§2.2), pasted-RR normalization (§5.6), and user overrides logged, never
    resisted (§3.4).
25. **Test-scope guidance** (§9.3): no coverage-percentage target — test
    scope is set per milestone via acceptance criteria. Always: exported
    functions (happy path, every error branch, R edge cases), numeric
    results via oracles, regression tests for bug fixes, documented claims.
    Indirect by default: internal helpers. Never: cosmetics, pass-throughs,
    dependency behavior. Contract over implementation; `covr` as diagnostic,
    never gate.
26. **Migration protocol** (§2.4) replaces the one-paragraph migration
    sketch: migrate the living, entomb the dead — legacy files move verbatim
    to `project/legacy/`, only live state is translated (no-invention rule),
    IDs are never renumbered (new numbering continues from the legacy max;
    legacy decision IDs stay valid as citations), old skills/rulebooks are
    deactivated so they can't fight the plugin, and the whole migration is
    one PR accepted only by a clean health audit plus a
    file-and-item-complete migration ledger. Pilot order: tidymedia first,
    a Lineage B repo (ackwards/circumplex) as the stress test before broad
    rollout (§11).

---

## 11. Building and piloting this plugin

1. **Build v0.1** in this repo from this spec: `plugin.json`, the eight
   SKILL.md files, `tracking-rules.md`, templates, README. Use milestone
   tracking for the build itself (a hand-maintained `project/` here —
   dogfooding the file formats even though this repo isn't an R package).
2. **Pilot in exactly two repos:** one fresh adoption (a package with no
   existing system) and one migration — **tidymedia first** (its format is
   nearest the canonical one, so the migration protocol gets exercised
   without maximum difficulty). Run at least 3 full milestones
   (plan → implement → review) in each, including one RB/RR escalation and
   one release walk.
   Before broad rollout, additionally stress-test migration on one
   Lineage B repo (ackwards or circumplex — root-level files, status inside
   CLAUDE.md, 50+ legacy milestones); that's the migration most likely to
   surface mapping-table gaps.
3. **Capture friction as issues** on this repo during the pilot — every time
   a skill asks the wrong question, misses a gate, or a cap feels wrong.
   Fold fixes into v0.2.
4. **Public release:** add a LICENSE (MIT), build README from the §12 user
   guide plus install instructions and a worked example, remove `DRAFT_*.md`
   (git history preserves them), tag v1.0. Marketplace publishing remains deferred (§2.3)
   until post-1.0.
5. **Broad rollout:** run `/rpkg-init` across the remaining active package
   repos, migrating their legacy tracking files.

---

## 12. User guide (destined for the GitHub README)

Written for the human driving the system — how to use it day to day. This
section becomes the core of README.md at public release.

### Getting started

1. Install the plugin (manual install for now; see repo instructions).
2. In your package repo, run `/rpkg-init`. Fresh repos get scaffolding;
   repos with an older tracking system get an interactive migration.
3. Run `/milestone` any time you're unsure where things stand.

### The core loop

Development is a cycle of milestones — PR-sized units of work with explicit
acceptance criteria. You steer at defined gates; Claude works autonomously
between them:

```
idea → /milestone-plan → /milestone-implement → /milestone-review → merged
        (scope gate)      (choices gate)         (approval gate)
```

You rarely need to type the next command: each phase ends with clickable
options (chips) that route to the natural next step. Typing the slash
command directly always works too, e.g. to resume after a break.

### Which skill, when

| You want to… | Do this |
|---|---|
| See where the project stands / what to do next | `/milestone` — status snapshot + health audit + a suggested next action |
| Capture an idea for later | Just say it: "add X to the candidates" (one ROADMAP row, no ceremony) |
| Turn an idea into a real plan | `/milestone-plan <title>` — investigation, scoping questions, a milestone file with acceptance criteria |
| Build a planned milestone | `/milestone-implement M<NN>` — branch, tests-first tasks, checkpoint commits; resumable across sessions |
| Verify and ship a finished milestone | `/milestone-review M<NN>` — fresh evidence for every criterion, independent code review, merge on your approval |
| Get a stronger model's judgment on a hard question | `/milestone-brief M<NN> <topic>` — writes a self-contained brief; you approve (or run) the Fable review |
| Fix a reported bug quickly | `/hotfix` — or just describe the bug; regression test, fix, PR, your approval. Escalates to a milestone if it's bigger than it looked |
| Fix a typo or tweak docs | Just ask — trivial edits commit directly to main, no tracking |
| Prepare a CRAN release | `/rpkg-release` — the full checklist; you do the actual submission |
| Adopt the system in another repo | `/rpkg-init` — idempotent; safe to re-run |

### What the system expects from you

- **Answer the gates.** Questions arrive in small batches at three points
  (planning scope, implementation choices, merge approval), each with a
  recommendation. Between gates, expect autonomy — if you're being asked
  questions mid-implementation, something is off.
- **Merges are yours.** Nothing reaches main without your explicit approval
  at review. "Proceed to review" is not "merge" — you get the evidence first.
- **Supply primary sources.** If a formula, cutoff, or scoring key needs a
  paper the model can't access, it will stop and ask you for the PDF rather
  than work from memory. That stop is a feature; feed it the PDF.
- **Fable costs real money.** Fable reviews are token-billed, so each one
  asks your approval with a scope estimate first. Say no freely — the brief
  file remains and can be run any time.
- **Run `/milestone` when returning after time away.** It reconciles
  tracking against git, flags stale work, and hands you a resume chip.

### Habits that keep it healthy

- One milestone in progress at a time. If you're tempted to start a second,
  finish or explicitly pause the first.
- Let milestones be small. The plan skill will propose splitting oversized
  ones — take the split; three small merges beat one sprawling branch.
- Don't hand-maintain status in chat or memory: if it isn't in `project/`
  files or git, it didn't happen. Anything you edit by hand there is fine —
  ROADMAP.md wins any conflict.
- Trust the archive. Done milestones compress to short summaries; the full
  story stays in git history and the PR.

### What this system deliberately does NOT do

- Auto-merge, auto-release, or auto-submit to CRAN — every irreversible step
  is gated on you.
- Track status in CLAUDE.md, chat memory, or GitHub issues — `project/`
  files are the single source of truth; issues are an inbox.
- Run Fable, or any paid escalation, without a per-instance yes.
```
