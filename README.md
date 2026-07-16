# cairn

*A cairn is built one stone at a time, and marks the trail for whoever
comes next.*

A Claude Code plugin for milestone-driven development: a
governed LLM Wiki for project state — the agent maintains it, you gate it.
One canonical workflow — planning, implementation, review, hotfixes,
releases, and expert escalation — with all project state in plain markdown
under `cairn/`, kept honest by weight caps and a self-auditing health
check. The core is
language-agnostic; each repo declares a toolchain profile (R, Python, or
generic) that supplies its language-specific commands. Work lands as small
stacked milestones, and any session — today's or next month's — can find
the path from the files alone.

Born from maintaining many R packages with Claude Code and rebuilding
similar-but-diverging tracking systems in each. This plugin centralizes the
logic (skills, rules, templates) so every repo works identically; each repo
holds only its own state.

**Status: v0.1 — piloting.** Interfaces may change; see
[CHANGELOG.md](CHANGELOG.md). The full design rationale lives in
[DRAFT_2.md](DRAFT_2.md) (removed at 1.0).

## Install

Two paths; pick one — running both installs the plugin twice and the
duplicates will confuse skill routing.

**Dev install (recommended while piloting):** clone and symlink into your
skills directory. The plugin loads from your checkout, so `git pull`
updates it with no re-install step:

```bash
git clone https://github.com/jmgirard/cairn
ln -s /path/to/cairn ~/.claude/skills/cairn
```

Footgun to respect: *live* means live — whatever branch the checkout has
is what loads at your next session start, in every repo, including the
enforcement hooks. Keep the checkout on `main` unless you're developing
cairn itself. For a one-off trial without installing anything, use
`claude --plugin-dir /path/to/cairn` (that session only).

**Marketplace install:** a frozen snapshot; re-install to pick up new
releases. In Claude Desktop: Customize → Plugins. From the CLI:

```bash
claude plugin marketplace add jmgirard/cairn
claude plugin install cairn@cairn
```

Either way, the install includes the guardrail hooks (session-start
tracking re-injection, the uncommitted-tracking stop guard, and the
merge-approval guard); they activate at the next session start and are
no-ops in repos that aren't cairn-tracked.

Then, in your package repo, run `/cairn-init`. Fresh repos get scaffolding;
repos with an older tracking system get an interactive, PR-based migration.
Run `/milestone` any time you're unsure where things stand.

## The core loop

Development is a cycle of milestones — PR-sized units of work with explicit
acceptance criteria. You steer at defined gates; Claude works autonomously
between them:

```
idea → /milestone-plan → /milestone-implement → /milestone-review → merged
        (scope gate)      (choices gate)         (approval gate)
```

You rarely type the next command: each phase ends with clickable options
(chips) that route to the natural next step. Typing the slash command
directly always works too, e.g. to resume after a break.

## A worked example

Say your repo is a small CLI tool and you want a `--dry-run` flag.

**1. Plan it.** You say: *"plan a milestone: add a --dry-run flag to the
sync command."* Claude reads the roadmap, decisions, and the relevant code,
then asks one short batch of scoping questions, each with a recommendation
— should `--dry-run` cover `sync` only or every mutating subcommand? is
printing the would-be actions enough, or must exit codes match a real run?
You click answers (or type your own). Claude writes
`cairn/milestones/M07-dry-run-flag.md` — goal, in/out scope, verifiable
acceptance criteria, ordered tasks — registers it in the ROADMAP as
`planned`, commits, and offers a chip: **Start implementing M07**.

**2. Build it.** `/milestone-implement M07` cuts a branch, asks any
implementation choices the plan left open (flag naming, output format),
then works the tasks in order: tests first, one checkpoint commit per
task, each commit updating the milestone file's checkboxes alongside the
code. Between the gate and the finish you aren't asked anything. When all
tasks pass, status flips to `review` and you get a diff summary and a
chip: **Proceed to review**.

**3. Ship it.** `/milestone-review M07` re-runs every check fresh, gathers
evidence for each acceptance criterion (no evidence, no tick), and hands
the diff to independent reviewer agents that didn't write it. Then — the
one moment that matters — it opens a PR and asks *you* to merge, with the
evidence in front of you. Nothing reaches your default branch until you
say yes. After the merge, the milestone compresses to a short summary in
the archive, the ROADMAP row flips to `done`, and the next session —
tomorrow or next month — picks up the trail from the files alone.

## Which skill, when

| You want to… | Do this |
|---|---|
| See where the project stands / what to do next | `/milestone` — status snapshot + health audit + a suggested next action |
| Capture an idea for later | Just say it: "add X to the candidates" (one ROADMAP row, no ceremony) |
| Turn an idea into a real plan | `/milestone-plan <title>` — investigation, scoping questions, milestone file(s) with acceptance criteria |
| Build a planned milestone | `/milestone-implement M<NN>` — branch, tests-first tasks, checkpoint commits; resumable across sessions |
| Verify and ship a finished milestone | `/milestone-review M<NN>` — fresh evidence for every criterion, independent code review, merge on your approval |
| Get a stronger model's judgment on a hard question | `/milestone-brief M<NN> <topic>` — writes a self-contained brief; you approve (or run) the Fable review |
| Fix a reported bug quickly | `/hotfix` — or just describe the bug; regression test, fix, PR, your approval. Escalates to a milestone if it's bigger than it looked |
| Fix a typo or tweak docs | Just ask — trivial edits commit directly to main, no tracking |
| Prepare a CRAN release | `/cairn-release` — the full checklist; you do the actual submission |
| Articulate a repo's design & principles | `/design-interview` — a two-phase interview (facts → principles) that fills `DESIGN.md`; best run on Fable |
| Adopt the system in another repo | `/cairn-init` — idempotent; safe to re-run |

## What lives where

```
your-package/
├── CLAUDE.md                  # lean router; never holds status
└── cairn/
    ├── DESIGN.md              # architecture as it IS + principles
    ├── ROADMAP.md             # milestone index — the only status authority
    ├── DECISIONS.md           # append-only decision log
    ├── milestones/            # one file per milestone (+ archive/)
    ├── reviews/               # Fable review briefs & reports (+ archive/)
    └── references/            # source + synthesis notes; PDFs gitignored
```

Boundary rule: **Architecture → DESIGN · Status → ROADMAP · Tasks →
milestone files · Decisions → DECISIONS · History → archive + git log.**

## What the system expects from you

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

## Habits that keep it healthy

- One milestone in progress at a time. Tempted to start a second? Finish or
  explicitly pause the first.
- Let milestones be small. The plan skill will propose splitting oversized
  ones — take the split; three small merges beat one sprawling branch.
- Don't hand-maintain status in chat or memory: if it isn't in `cairn/`
  files or git, it didn't happen. Hand-editing the files is fine —
  ROADMAP.md wins any conflict.
- Trust the archive. Done milestones compress to short summaries; the full
  story stays in git history and the PR.

## What this system deliberately does NOT do

- Auto-merge, auto-release, or auto-submit to CRAN — every irreversible step
  is gated on you.
- Track status in CLAUDE.md, chat memory, or GitHub issues — `cairn/`
  files are the single source of truth; issues are an inbox.
- Run Fable, or any paid escalation, without a per-instance yes.
