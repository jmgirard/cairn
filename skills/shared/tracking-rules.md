# Tracking rules (shared by all cairn skills)

Read this before touching any tracking file. Every cairn skill obeys these rules; skills state their own workflow but
never restate or override this rulebook. Repo-specific rules in CLAUDE.md and `cairn/DESIGN.md` bind in addition, never
instead. This file states operative rules only; the reasons behind a rule live in `cairn/DECISIONS.md` and git history.

## File map and ownership boundaries

All project state lives in markdown under `cairn/`: substance in the owner, other files at most a cross-reference line.

| File | Owns | Does NOT own |
|---|---|---|
| `CLAUDE.md` | Dev commands, repo-specific hard rules, pointers to `cairn/` | Status, TODOs, architecture rationale, history |
| `cairn/DESIGN.md` | Purpose & scope, function families, conventions, numbered principles (GP/IP), architecture as it **is**, known issues | Future work, task lists, status |
| `cairn/PROFILE.md` | The repo's toolchain profile — the seven slots the operational skills read (see "Toolchain profiles") | Domain doctrine, status, tasks, decisions |
| `cairn/ROADMAP.md` | The milestone index — **the only authority on status** | Task details, acceptance criteria, narrative |
| `cairn/milestones/M<NN>-<slug>.md` | One milestone's goal, scope (In/Out), acceptance criteria, tasks, work-log, review evidence | Status authority (header is a mirror; ROADMAP wins any conflict — fix the mirror immediately) |
| `cairn/milestones/archive/` | Compressed ≤25-line summaries of done/dropped milestones | Active work |
| `cairn/DECISIONS.md` | Append-only cross-cutting decisions (D-001, …), never renumbered — superseded by new entries | Milestone-local decisions (those live in the milestone file); deferrals ("not now" is a ROADMAP fact, not a decision) |
| `cairn/LESSONS.md` | Durable, capped repo lessons — captured at milestone end, surfaced at plan time; current knowledge, corrected in place when proven false, retired per "Retiring a lesson" | Status, decisions (a *choice* is a D-entry), per-milestone task notes |
| `cairn/reviews/` | RB<NN> briefs and RR<NN> reports for Fable escalation (+ `archive/` for resolved pairs) | Anything else |
| `cairn/references/` | Source notes (`<citekey>.md`), synthesis notes, `INDEX.md` (one line per committed page), the gitignored source shelf `sources/` | Anything else |
| `cairn/legacy/` | Entombed pre-migration tracking files, verbatim | Anything live |

Boundary rule: **Architecture → DESIGN · Status → ROADMAP · Tasks → milestone files · Decisions → DECISIONS · Lessons →
LESSONS · History → archive + git log.** Repo-specific extra files in `cairn/` are allowed; they declare their own scope
and must not claim another file's ownership.

### Milestone-file section ownership

Each section has a writing skill — a phase skill never rewrites another phase's section. Write-modes: **create**
(authored once), **append-only**, **exclusive** (one writer ever), **mirror-update** (synced to `ROADMAP.md`; ROADMAP
wins any conflict), **check-off** (implement ticks task checkboxes, minor task edits), **amend-via-gate** (changed only
through the implement amendment protocol or a review send-back, always with a work-log line).

| Section | Writing skill | Write-mode |
|---|---|---|
| Status (header) | the transitioning skill (plan → implement → review) | mirror-update |
| Priority, Depends on, Driving RR, Principles touched (header) | plan | create; amend-via-gate |
| Branch/PR (header) | implement (branch), review (PR URL) | create |
| Goal | plan | create; a wrong goal returns to plan, never edited in place |
| Scope (In/Out) | plan | create; amend-via-gate |
| Acceptance criteria | plan | create; amend-via-gate — review reads, never reinterprets; under AC fencing review ticks a verified criterion box (a verification mark, not a text change) |
| Coverage (criterion→task map) | plan | create; amend-via-gate — review reads to fence evidence, never reinterprets |
| Tasks | plan (create), implement (check-off, minor edits) | create; check-off; amend-via-gate for substantive change |
| Work log | any skill | append-only |
| Decisions (milestone-local) | implement, review | append-only |
| Review | review | exclusive |

**AC fencing (review discipline).** An acceptance-criterion checkbox is ticked only against fresh evidence recorded in
the Review section — no evidence line, no tick; each box as its own evidence line lands, never batched at phase end.
Every criterion must map to ≥1 existing task via the Coverage section; an unmapped criterion (or one mapped to a missing
task) is a gate failure, returned to `/milestone-implement` for a gated Coverage amendment, never patched review-side.

DESIGN.md principles: **GP<n> — Guiding Principle**, a default stance tradeable with stated justification; **IP<n> —
Inviolable Principle**, a hard constraint never violated — changed only by explicit user decision recorded as a
D-entry. IP block first, then GPs; numbers are never reused or renumbered — retiring one takes a D-entry.

## Weight caps

- The cairn `## Project tracking` section of `CLAUDE.md` < 30 lines (the repo's dev doctrine outside it is not cairn's
  to cap) · `ROADMAP.md` < 60 lines · `LESSONS.md` < 50 lines · `PROFILE.md` < 120 lines · archived summary ≤ 25 lines.
  `ROADMAP.md` and `LESSONS.md` also keep byte budgets — `ROADMAP.md` < 24,000 bytes, `LESSONS.md` < 20,000 bytes
  (line cap × 400) — judgment-checked at hygiene passes (`wc -c`), not covered by `cairn_validate`.
  `ROADMAP.md` and `LESSONS.md` are parsed one item per line; never split an item across lines.
- Doctrine modules keep the line and byte budgets their own headers state (the maturation exit's rule, "Retiring a
  lesson" below), judgment-checked at hygiene passes (`wc -l -c`, not covered by `cairn_validate`); over either figure
  the remedy is compressing or retiring the module's content — never "let it grow".
- A live milestone file's **plan-owned body < 150 lines** — everything before the review-exclusive `## Review` section,
  less `## Work log` and `## Decisions`. Those three are cap-exempt (`## Review` so evidence never competes with plan
  content; the other two as IP4 history); the `session_context` hook bounds their read, injecting each one's newest
  content and stating what it left out. A file with no `## Review` counts to EOF, still less those two.
- Work-log entries are one line each (`cairn_validate`'s `work-log format` advisory WARNs, never fails). Never paste
  command output or subagent transcripts into tracking files — summarize; the `decisions format` advisory WARNs (never
  fails) on pastes in the milestone-local `## Decisions` section, never on entry length.
- Remedies when a cap is hit (never "let it grow"): over-count ROADMAP → graduate or prune candidates, clustering a
  large backlog into grouped rows pointing at the entombed legacy file; over-cap milestone → compress the single
  heaviest plan-owned section (named by the `cairn_validate` breakdown, which lists only trimmable sections, so the
  remedy can never aim at history) in one rewrite — never a nibble-and-recount loop — cross-referencing durable records
  rather than restating them, splitting or moving material to `references/` only when no one section can carry the cut;
  over-budget `ROADMAP.md` (bytes) → compress the widest rows first, then the same graduate-or-prune remedy; over-cap or over-budget `LESSONS.md` → retire
  or prune entries (the remedy its own header states); over-cap cairn CLAUDE.md section → trim back to the template.
- Terminal-row retention (standing hygiene): the ROADMAP table keeps only the 5 most recent terminal (`done`/`dropped`)
  rows combined; prune older ones as they accumulate.
- The `Last hygiene check` stamp is one short line naming what changed since the last check, **replaced each pass, never
  appended to** — no `Prior:` chain; git holds every earlier stamp.

## Universal tracking rules

- **Tracking travels with code.** A commit that changes code also updates the checkboxes/work-log in that same commit.
- **Absolute dates only** (YYYY-MM-DD). **Append, don't rewrite:** work-logs and DECISIONS.md are append-only;
  supersede, never edit history; never fabricate it — a gap gets one catch-up entry summarizing `git log`.
- **Verify a batched or scripted edit landed before writing the record that claims it did** — re-read the aimed site
  first; a section-targeting edit anchors on text occurring exactly once; a tick write follows its verified evidence
  write, never the same unverified batch.
- **Branch-added behavior claims in code-adjacent artifacts are derived, never composed** (the derived-claims rule). In
  code comments, docstrings, changelog entries, and user-facing docs, a prose claim the branch adds about what an
  artifact does is written against an execution's observed output or a same-session read, never from recollection; prose
  restating what its cited artifact shows becomes a cross-reference, a member enumeration a pointer unless the
  enumeration is itself the deliverable. Tracking records are exempt from this rule and from the derived-figures and
  failure-identity rules below — ordinary care, the record-prose rule, the review lenses, and the correction discipline
  govern them instead.
- **A derived figure in a code-adjacent artifact is pinned or procedural, never free-standing** (the derived-figures
  rule): beside its producing procedure and the commit or date measured, or replaced by its derivation.
- **An observed failure backs a claim only as the failure it is verified to be** (the failure-identity rule): in
  code-adjacent artifacts and tests, verify the failure's identity — condition class, message, or signaling site —
  confirming the inputs reach the behavior under test; a test asserting a failure asserts *which* failure, and a
  discriminating test's passing control is shown to pass for the claim's reason, never merely to pass.
- **Records are written plain** (the record-prose rule): a durable record under `cairn/` — work-log lines, D-entries,
  milestone-file sections, LESSONS lines, ROADMAP rows, archive summaries — states decision-relevant facts in plain
  words, omits characterizations the facts don't need (adjectives, superlatives, hype), and matches its length to the
  record's job — the Plain style rule's length standard, applied to what is written down.
- **A D-entry carries the decision and its rationale, and no derived measurements** — a supporting count or measurement
  lives in the artifact or milestone file the entry cites (binding after M146; prior entries stand, IP4).
- **History-record corrections batch to at most one superseding entry per milestone**, not a chain of per-claim entries
  — binding at authoring time (a defect found in the batching entry after it lands takes a further superseding entry
  under IP4).
- **Correcting a record proven false.** History — `DECISIONS.md`, work-logs, the milestone-local `## Decisions` section,
  milestone IDs, the archives, `legacy/` — is never edited (IP4); it is superseded. Current knowledge — `LESSONS.md`,
  `references/` pages, `DESIGN.md`, `ROADMAP.md` — is fixed where it sits, the correction marked (`corrected M75`);
  never append a correction leaving the wrong text readable. Exception: a wrong IP/GP *principle* still changes only by
  explicit user decision recorded as a D-entry.
- **Retiring a lesson that no longer earns its line.** Three exits: **enforcement** — a test *fails* on the mistake the
  lesson warns about (a guard merely existing nearby is not enforcement); **ownership** — another tracking file's slot
  owns the content (the retiring milestone may *move* it there); **maturation** — a stabilized family graduates whole
  into a doctrine module, when it teaches transferable craft, has been extended or consolidated at least twice, and
  neither other exit applies. The graduating milestone writes the module's line and byte budget into the module's own
  header — set from the graduated size plus stated headroom — hand-read with `wc -l -c` at the repo's hygiene passes
  and covered by no validator. A lesson covered in part is trimmed to its remainder; a retired lesson leaves no line
  behind — the archive summary names what it graduated. Retirement removes the redundant, never the merely disputed (a
  disputed lesson is corrected, not deleted). Checked at `/milestone-review` post-merge hygiene, scoped to what the
  milestone shipped; prune-the-stalest is the last resort. The graduated records-hygiene family lives in
  `skills/shared/records-hygiene.md` (candidate-row lifecycle; superseding a decision), read at hygiene or plan gates.
- **Stop points are commit points.** Never end a session or turn with uncommitted work — checkpoint-commit code and
  tracking together (even half-done, marked as such).
- **Git is ground truth for code.** Outside commits are reconciled with a catch-up work-log line, never retroactive
  rewriting. **User overrides are logged, never resisted** — comply and record the override in the work-log.
- **Dependency changes are never unilateral** — any add/remove/re-pin goes through a question gate and is recorded as a
  D-entry. **Breaking changes to public behavior follow a deprecation cycle** unless the project is pre-1.0 and the user
  explicitly waives it; the active profile names the language's mechanics.
- **Release timing is user-declared, never agent-proposed** (D-050): cairn never proposes, plans unprompted, or
  nominates a release; an unopened window parks it as `blocked`. `/cairn-release` never self-submits.
- **Prefer script-measurable acceptance criteria**; where judgment is unavoidable, commit the classification ledger.
- **Tracking files outrank memory.** Persistent memory never holds project state; `cairn/` files win any conflict.
  **Memory intake gate (GP4):** durable project knowledge → `cairn/`; a generalizable conduct or plugin defect → the
  plugin; only genuinely per-user meta-context stays in memory (the `memory_guard.py` hook nudges this).

## Milestone IDs and status

- IDs are `M<NN>` (zero-padded to two digits), assigned at planning time, monotonically increasing, **never reused** —
  dropped milestones included; past M99, IDs simply grow (M100). **No completion-order requirement**: work order is
  governed only by `Depends on:` (workable only when dependencies are `done`) and `Priority:` (high / normal / low); the
  ROADMAP index is grouped by status, not sorted by ID.
- Bare `M<NN>` is repo-local: with more than one cairn-tracked repo in scope, qualify the ID with the repo name —
  "tidymedia M07". User-facing materials (NEWS.md, README, vignettes, pkgdown) never reference milestone numbers.

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

Transitions: `candidate → planned → in-progress ⇄ blocked; in-progress → review → done` (review failures return to
`in-progress`); `planned → blocked` and `review → blocked` are both legal; anything can go to `dropped`; no other skips.

## Sizing and the work tiers

One milestone = one reviewable PR ≈ 1–3 working sessions. Tasks are the only unit inside a milestone — no slices or
sub-milestones; internal structure means split, wired with `Depends on:`. Split tripwires: >~7 acceptance criteria, >~10
tasks, a goal sentence needing "and", tasks shippable independently, or no hope of the 150-line cap. Prefer vertical
slices; every milestone leaves the default branch shippable; splitting never discards the remainder.

Work that isn't a milestone: **Trivial** (no runtime surface — typos, tracking, comments) → direct commit to the default
branch, no tracking beyond the commit. **Hotfix** (user-visible bug) → `/hotfix`: regression test first, gate-lite, PR,
user approval; NEWS entry; no milestone file. **Milestone** → more than one sitting, changes exported behavior (beyond
restoring documented behavior), or requires a design decision.

Intake: GitHub issues and external PRs are inboxes, never a second tracking system. Issues → `candidate` rows or the
hotfix path; `leave` is legal only for noise, duplicates, or items already cross-referenced in cairn — never anything
genuinely new. External PRs: **`/hotfix` is the door** for the small and correct — it adopts the PR (`gh pr checkout`),
holds it to the hotfix bar, merges on user approval; larger → `/milestone-plan`. Candidates may be added
conversationally by anyone at any time (one ROADMAP row).

**Out-of-band idea capture.** A capture channel that is not a cairn tracking file — a chip, a scratch TODO, an ad-hoc
note — is never the record of record: the idea also lands as a `candidate` ROADMAP row in the same turn (search-first
applies), the out-of-band item at most a pointer to that row. The `idea_guard.py` hook nudges this.

**Search-first candidate creation.** Before adding a candidate row — by any skill or conversationally — sweep existing
candidates + `milestones/archive/` + `DECISIONS.md` for overlap; on a hit, absorb into or cross-reference the existing
row rather than duplicate it; a standing rejection is recorded once and superseded, never re-litigated. A candidate
recording an alternative to a chosen approach states its promotion condition as **the class of evidence that would
falsify the chosen approach**, never as a count of failures.

**Bounded `DECISIONS.md` read.** Read `DECISIONS.md` by scanning its `### D-` headings — never whole. A matched
heading's entry is read whole before anything is surfaced; a match is back-referenced (its own `D-0NN` id searched
across the file) so a superseding or annotating entry surfaces even when its heading omits the relationship; a collision
is quoted verbatim from the full entry, never the heading. Prior state is surfaced, never silently obeyed or overridden
(IP2). A `### D-` heading names its subject and any entry it supersedes, annotates, or narrows.

## Git and approval model

- **The default branch is a distribution channel** — installable at all times; cairn never assumes the name is `main`.
  It accepts only docs-only tracking commits and squash-merges of milestone/hotfix branches — never implement on it.
  **The remote's default branch is authoritative**: push docs-only commits immediately, so branches are cut from commits
  the PR base has.
- **Detecting the default branch (canonical recipe).** Never hardcode `main`; store no branch name. Detect with `git
  symbolic-ref --short refs/remotes/origin/HEAD` (strip `origin/`); if `origin/HEAD` is unset locally but a remote
  exists, query `git ls-remote --symref origin HEAD` and read the `ref: refs/heads/<name>` line. Only with **no remote
  at all** ask the user — never guess from the local current branch (wrong on a feature branch).
- Milestone work on `m<nn>-<slug>`; hotfixes on `hotfix-<slug>`; both cut from the up-to-date default branch. Checkpoint
  commits are cheap — squash erases them. Exception: an adopted external PR keeps the contributor's branch and its name.
- Before branching or committing, check `git status`: a dirty tree with unrelated changes means ask the user — never
  sweep strangers into a checkpoint commit. If the default branch moves under an active branch, merge it into the branch
  and re-run tests before continuing or reviewing.
- **Nothing reaches the default branch without the user's explicit approval at the review gate.** Never force-push (the
  force_push_guard hook denies it on the default branch); never merge red or pending CI.
- Approval is recorded on disk: the approving skill writes the single-use, gitignored marker `cairn/.merge-approved` at
  the gate — never except at an explicit user approval; the merge-guard hook denies `gh pr merge`/`git merge` to the
  default branch without it and consumes it per attempt (a failed attempt's marker is restored). The marker names the PR
  it approves (`… approved YYYY-MM-DD for PR #<N>`); the guard refuses a merge whose PR it does not name — spell the
  number out: `gh pr merge <N> --squash`.

**Enforcement boundary.** Every guard is a PreToolUse hook on *this* session's own Bash calls; a merge made in the
GitHub web UI, by a merge queue, or by a contributor without the plugin is invisible to them — there the approval
requirement and never-force-push degrade to honor-system, and the rest of the conduct is prose on any path. cairn
assumes **one operator running these skills**; outside contributions come in through intake.

Waiting on CI: prefer one **blocking** wait (`gh pr checks <pr> --watch` with a timeout) over background polling — one
wait at a time, resolved within the turn; on timeout, report the fresh state, log one line, stop with nothing left
watching. **Resume is stateless**: re-derive from `gh pr checks` (PR URL: the milestone header), never a remembered "CI
was running".

## Context hygiene

Stateless resume makes conversation context disposable. Only the user can `/clear` — skills mark the seams in their
recaps, never assume continuation. **The milestone boundary is the canonical `/clear` point**: after the post-merge
hygiene commit, everything load-bearing is on the default branch; prefer `/clear` over `/compact` there. **Stop points
are commit points are safe-clear points**: never tidy mid-task — finish the current task, checkpoint-commit with an
honest work-log line, stop, resume fresh; if compaction threatens to lose something important, write it to the milestone
file instead. Same-session implement → review is fine (evidence by command, never recall; review in a fresh subagent) —
the seam that matters is milestone → milestone. A resume stumble is a tracking-file gap — fix the file.

## Question gates and routing chips

User interaction happens at exactly three gates — plan questions, pre-implementation questions, final merge approval —
plus routing chips. At a gate, ask one batched round of 2–5 concrete decision questions via AskUserQuestion, each with a
recommendation and brief pros/cons; between gates, work autonomously, never dripping questions. When more are open than
one round holds, flag at most 3 prioritized markers and defer the rest. The **final merge-approval gate is itself an
AskUserQuestion chip** — one approve/decline question (a decline option always present), never a prose yes/no.

Every phase ends with a **routing chip**: an AskUserQuestion offering the single most sensible next action first,
composed per the chip rules below. A chip is an explicit user stop — never auto-proceed — but the selection itself is
the go: on selection **the orchestrator immediately invokes the target skill via the Skill tool** (the `→ /skill`
notation in an option names that skill); the user never types the command. A routing chip is always an AskUserQuestion
call — emitting a prose list of options where a chip is required is a drift bug. `/milestone-review`'s end is the **sole
exception** (D-019): after a successful merge it closes with a plain-prose `/clear` nudge — the sole phase whose end is
deliberately chip-less. (Its merge-approval gate stays an AskUserQuestion chip.)

## Output & interaction discipline

These rules bind all chat output while any cairn skill is active.

- **Phase header.** Orient with Markdown headings, not an inline banner: a `#` names the unit of work, a `##` the phase.
  Milestone skills: `# Milestone <NN>: <title>` → `## Plan` / `## Implement` / `## Review`; every other skill states its
  own pair in its `Phase header:` directive. One `#` per unit of work (re-emit when the unit changes), a `##` per phase
  entry; replies within a phase are plain deltas underneath.
- **Deltas, not dumps; narrate outcomes, not deliberation.** Between gates, report what changed since the last report —
  never a restated plan, pasted command output, or a running readout of reasoning; a one-line signpost or a compact
  summary where a question needs context is fine. Two exceptions: drafted durable-record text and conclusion text above
  an acceptance chip.
- **Correct what matters, and only narrate that.** Correct an earlier chat statement only when the error would change
  the user's code, conclusions, or decisions — plainly, briefly, then continue; a slip that changes nothing is fixed
  without narration. A chat slip never reaches a durable record.
- **Durable-record preview.** Newly authored durable-record text — a D-entry, a milestone file's plan-owned sections
  (new or amended), a LESSONS line, an archive summary, a ROADMAP candidate/graduation row — is shown verbatim in chat
  immediately before the commit that lands it: same turn, no added stop; objections handled by amend/supersede. Exempt:
  work-log one-liners, checkbox ticks, status-mirror updates, and hotfix/code-branch content already reviewable at the
  PR merge gate — not a milestone branch's tracking records.
- **Outcome-first recaps.** Phase-completion recaps lead with what the work did, changed, or accomplished, in plain
  words; hygiene mechanics follow compressed — one line when clean.
- **Plain style.** Write for the reader: response length matched to what the turn needs — the main answer carries the
  response, caveats and asides stay short; plain words over jargon — a term of art appears only as the precise name for
  a thing, glossed at first use or dropped; facts stated straight, with no stock filler phrasing, hype adjectives, or
  padding. The decision surface keeps its stricter Accessible-language test below; like the narration rule above,
  this never licenses compressing the Durable-record preview or Acceptance-chip substance.
- **Chips carry choices, not evidence.** Supporting detail and justification live in chat *above* the chip; option
  labels are short; descriptions say in plain language what is chosen and why it matters; ≤4 options per question.
- **Accessible language on the decision surface.** A question's text, the prose framing a chip, and every option label
  and description pass the two-sentence test: the first sentence says what is being decided in plain words, the second
  what happens on each choice, both before any term of art; a technical term is glossed at first use. Cairn-internal
  record identifiers — D-/RR-/BC-ids, IP/GP numbers, doctrine section numbers — stay out of question text and option
  labels (`M<NN>` is exempt); the identifier and its justification live in the chat above the chip. A gate prompt the
  user flags as unclear is captured verbatim same-session (a work-log line, or a candidate ROADMAP row when no milestone
  is active). Applied in authorial judgment, never as a gate.
- **Acceptance chips show what's accepted.** A chip option accepting or approving a produced conclusion — review
  findings, a verdict, an audit result, amended text, a proposed disposition — requires that conclusion's substance
  verbatim in chat above the chip (a long artifact: its conclusions verbatim plus the file path); a paraphrase never
  stands in for the text being accepted.
- **Contextual chip construction.** Compose options from the actual session state, not a fixed menu; chip menus in
  skills are examples, not scripts. Invariants: recommended option first and marked, ≤4 options, a stop/pause option
  present, and a chip is a user stop — never auto-proceed.
- **Chapter markers (per-phase mandate).** Mark a chapter at each phase transition (session start implicit) via the
  runtime's chapter mechanism (`mark_chapter` in Claude Code — it drives the navigable TOC); absent one, the H1/H2
  headers are the fallback.
- **Copy-run commands get their own fenced block.** Handing the user a command to run → its own fenced code block, never
  inline backticks; naming a command, path, or symbol in prose → inline backticks; a routing chip's `→ /skill` option →
  neither fence nor handoff (selecting the option is what acts). Slash commands count as commands. A step ending the
  turn expecting the user to run something is a handoff (fence); noting a safe `/clear` point beside a chip already
  offering the route is a mention (inline).
- **Subagent titles carry the model tier.** Prefix every Agent description with `[S]`/`[O]`/`[F]` for Sonnet/Opus/Fable
  — task panes show only the title, not the model.

## Model and agent strategy

- Orchestrator: Opus, running these skills in the main session. Exception: `/design-interview` recommends the user run
  the *main session* on Fable — a session-model choice, not a subagent.
- **Subagents share the primary checkout.** Every spawned subagent uses ref-based git only (`diff`/`show`/`log`/`blame`
  against refs), never a HEAD-moving command (`checkout`/`switch`/`worktree add`/`reset`) in the shared tree.
- **Delegate only what warrants it.** A subagent is warranted by a large, genuinely independent track of work (a wide
  investigation, a mechanical migration across many sites). Work the session can finish in a handful of tool calls is
  done inline; where one subagent can do the task, spawn one rather than several. A spawn made for *freshness* — a
  reader that must not have authored what it reads — is warranted by who the reader is, not by volume (an author's
  re-check of its own just-produced work is not).
- **Sonnet subagents**: well-specified self-contained work — fan-out searches (Explore), mechanical migrations, test
  writing against a spec, boilerplate. Give complete specs (for an Explore fan-out, a reading list naming the files or
  areas to read); verify their diffs before committing; summarize results into one work-log line.
- **Opus subagents**: design-sensitive implementation; the diff-bug lens of the review fan-out.
- **The `/milestone-review` review** runs in fresh-context subagents, never the implementing session: an internal-tier
  milestone whose diff touches only markdown/tracking files gets one **[O]** diff reviewer; any other diff gets the
  three distinct-evidence reviewers the review skill defines ([O] diff-bug, [S] blame-history, [S] prior-PR-comments —
  always spawned, no-op without prior-review evidence); reviewers rank their findings, the maintainer triages the ranked
  list at the gate, every finding logged.
- **Never Haiku.** For anything.
- **Fable subagents**: only through the RB/RR brief protocol (`/milestone-brief`) after a per-instance approval gate —
  costlier than Opus, so a deliberate per-instance choice, never a standing default; ad-hoc Fable spawning is
  prohibited. The implementing session never authors the durable verdict on the review constraining it — that routes to
  a new RB or the maintainer at the gate.
- **RB tripwires** — the canonical must-offer cases for Fable escalation, with their tag tokens: statistical/scoring
  correctness with no available oracle (`no-oracle`); irreversible exported-API decisions (`irreversible-api`); anything
  touching an IP (`ip-touching`). `/milestone-plan` tags tripwire-hitting open questions inline — `(RB tripwire:
  <token>)` — and `/milestone-implement` inherits the tags; a tripwire can also fire mid-implementation (no tag
  required). An escalation chip option may be offered on a tripwire hit OR for a genuinely hard question the session
  cannot confidently settle, and stays a gated, per-instance choice through `/milestone-brief`, never standing.

## Toolchain profiles

Language/toolchain specifics live in a **profile**, not in the core rules. A repo declares its profile in
`cairn/PROFILE.md` (instantiated by `cairn-init` from `skills/shared/profiles/`); the operational skills read its slots
instead of hardcoding one language's commands. Seven slots: **verify** — the per-task test/check command(s)
`/milestone-implement` and `/hotfix` run; **consistency-gate** — toolchain checks `/milestone-review` runs *in addition
to* the universal cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`); **test-doctrine** —
toolchain test expectations layered on "What gets a test"; **release-walk** — the procedure `/cairn-release` follows;
**init-detection** — how `cairn-init` recognizes the toolchain; **greenfield-openers** — opener questions for a
new/empty repo; **changelog** — the repo's changelog file (or "none" — legal), read by `/hotfix`, the release-walk, and
the consistency-gate.

Four profiles ship: `r-package`, `python`, `docker-image`, and `generic` (no toolchain gates). **Absent `PROFILE.md` →
infer** in order: `DESCRIPTION` at the repo root → `r-package`, else `pyproject.toml` (or legacy `setup.py`/`setup.cfg`)
→ `python`, else a `Dockerfile` as the sole toolchain marker → `docker-image`, else `generic`; a hybrid repo keeps the
language marker (`cairn-init`'s disambiguation gate is the only place the image-vs-package choice is asked).
`cairn_validate` no-ops when `PROFILE.md` is absent and FAILs on a missing, empty, or unrecognized slot.

## Validation doctrine (statistical/numeric work)

The domain-verification doctrine (oracle types and priority, the ≥2-independent-types bar, the oracle registry, the hard
stops, source ingestion) lives in `skills/shared/validation-doctrine.md`, a module of this rulebook and universal domain
doctrine, never a profile slot. Read it whenever a milestone touches a numeric result or scoring/algorithmic content.

## References pages

Committed `cairn/references/` pages come in two types. **Source notes** (`<citekey>.md`) each own one primary source —
citation, extracted values with page/table anchors, what traces to it (ingestion workflow:
`skills/shared/validation-doctrine.md`). **Synthesis notes** are cross-source analyses no single `<citekey>.md` owns.
Both: committed, cited (`citekey (p. N)` / page name), never restated into tracking files; every page carries its
`INDEX.md` line (mechanized by `cairn_validate`'s references check); author from the shipped templates under
`skills/shared/templates/`.

**When a page is owed.** A source consulted in passing owes nothing; a page is owed once the repo *relies* on the source
— a claim, value, convention, or decision traces back to it — authored in the milestone that takes the dependency, never
left for later. An analysis that will outlive its milestone is a synthesis note; analysis serving only the milestone in
hand stays in the milestone file. The trigger is universal — it fires with no numeric work at all.

**Exploring prospective sources.** The owed rule is demand-pull; reading a corpus of maybe-relevant sources to
*discover* what the repo does not yet know it wants is supply-push exploration, legitimate. It always produces ROADMAP
candidate rows for the promising finds (search-first); a committed survey synthesis note only when the triage will
outlive its exploration; no per-source `<citekey>.md` pages (demand-pull) and no machinery (no committed raw sources,
references log, query op, or graph tooling).

**Standing facts vs. dated observations.** A **standing fact** — a claim about the *source* (an extracted value, a
formula, an anchor) — holds as long as the source does. A **dated observation** — a claim about the *repo's own state*
(what is on the shelf, what has been read, what must still be checked) — carries `— observed YYYY-MM-DD` inline on the
claim itself; the undated absence claim ("not present", "not yet checked") is the failure this rule stops.

**Page provenance and re-verification.** Every committed `references/` page carries a `**Provenance.**` block — prose,
not frontmatter — recording source pointer, ingested date, ingesting milestone, pagination basis, and
extraction-verified status (a dated observation). A page the repo still relies on is re-checked against its source as it
ages; a re-check marks inline on the extraction status — never in a new file, section, or log. `cairn_validate`'s
`references staleness` advisory WARNs (never a check) on a page with no verified re-check or one older than 180 days; a
status naming no date ages from the ingested date; a first-hand record with nothing to re-verify against is exempt by
saying so.

## What gets a test

No coverage-percentage target — test scope is set per milestone via acceptance criteria. Always: every exported/public
function (happy path, every error branch fired with its condition asserted — the test names which failure, never bare
failure — and the language's edge cases); every numeric result via an oracle; every bug fix via a regression test that
fails before the fix; every documented claim. A changelog entry asserting a behavior requires a test that fails without
that behavior, or the entry narrows to what a named test enforces. Indirect by default: internal helpers (direct tests
only for independent logic). Never: cosmetic output beyond meaningful snapshots, trivial pass-throughs, dependency
behavior. Test the contract, not the implementation — a test that breaks under a behavior-preserving refactor is a
defect in the test. Language-mechanical specifics — edge cases, error mechanism, coverage-tool status, plot/snapshot
conventions — live in the active profile's `test-doctrine` slot; the rules here are the universal floor.
