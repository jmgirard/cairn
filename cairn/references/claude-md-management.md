# claude-md-management (Anthropic official plugin)

**Provenance.** Citekey `claude-md-management` · ingested 2026-07-11 by M06 from https://github.com/anthropics/claude-plugins-official `plugins/claude-md-management/` @ dc72937.
Pagination: —.
Extraction: verified at ingestion — full source read; not re-read since.

Source: https://github.com/anthropics/claude-plugins-official
`plugins/claude-md-management/` @ dc72937 (studied 2026-07-11, full
source read).

## What it is

One skill (`claude-md-improver`) and one command (`/revise-claude-md`).
The skill audits every CLAUDE.md in a repo against a weighted 6-criterion
rubric (commands, architecture clarity, non-obvious patterns,
conciseness, currency, actionability), emits a scored quality report
(A–F letter grades), then applies user-approved targeted edits. The
command is a session-end reflection: harvest learnings from the current
session (commands discovered, gotchas, testing approaches) and propose
one-line CLAUDE.md additions as diffs, applied only on approval.

## Workflow model

- **Report before write; diff before apply.** Every change shown as a
  diff with a one-line "why", gated on explicit approval.
- **Brevity doctrine**: "CLAUDE.md is part of the prompt, so brevity
  matters"; one line per concept; reject one-off fixes and restatements
  of the obvious. Routing table: team-shared → CLAUDE.md, personal →
  `.claude.local.md` (gitignored), user-wide → `~/.claude/CLAUDE.md`.
- **Philosophy: CLAUDE.md is the single project-memory file** — commands,
  architecture, gotchas, workflow all accumulate there.

## What cairn should steal

- The scored-rubric audit pattern for `/milestone`'s hygiene check —
  cairn audits mechanically (caps, mirrors, dates) but has no graded
  quality assessment of tracking-file content.
- The session-end learning harvest: cairn work logs record *what
  happened*, but nothing captures *repo lessons* (a discovered build
  quirk, a testing trick) into a durable home.

## What cairn does that it doesn't

Cairn's boundary rule is the direct antithesis: time-varying state
*rots* in CLAUDE.md, so status/tasks/decisions are split into owned
files with caps, and CLAUDE.md holds only commands, hard rules, and
pointers. claude-md-improver improves the monolith; cairn replaces it.
**Compatibility risk**: running the improver in a cairn repo would push
architecture/gotcha content into CLAUDE.md against the <80-line cap and
ownership table — the two systems' doctrines conflict on where project
memory lives.

## Hands-on observations (source-execution trial, 2026-07-11)

Ran the improver workflow end-to-end on a scratch repo with a
deliberately weak CLAUDE.md: discovery `find` → rubric scoring (came
out ~20/100, F: vague "run with python", zero architecture, filler
"be careful when editing") → report → targeted 21-line rewrite. The
workflow is single-agent, linear, cheap; the rubric's weights made the
rewrite priorities obvious rather than arbitrary. Also scored cairn's
own CLAUDE.md read-only: ~70/100 (B) — the rubric docks points for
missing inline architecture/commands, i.e., it penalizes exactly what
cairn's boundary rule prescribes (pointers over content). Confirms the
compatibility risk is real but moderate: an unsupervised improver run
would recommend additions cairn routes elsewhere, though the
report-before-write gate gives the user a natural veto point.
