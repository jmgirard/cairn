---
name: cairn-init
description: Adopt the cairn system in a repo - scaffold the cairn/ tracking files, CLAUDE.md section, and ignore entries; or migrate an existing precursor tracking system. Use when the user wants to set up, initialize, adopt, repair, or migrate to cairn in a repository.
argument-hint: ""
---

# /cairn-init — scaffold, repair, or migrate

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first.
Idempotent: safe to re-run any time; re-runs report and repair missing or
damaged pieces and **never overwrite user content without asking**.
Stage banner: `[cairn · init · <scaffold|repair|migration §n>]`.

## 0. Detect the situation

- No DESCRIPTION file → **non-package repo**: say so and ask — adapt
  (scaffold the tracking system minus R-specific guardrails/gates) or
  abort. Never scaffold R machinery into a non-package repo silently.
- No existing tracking → **fresh scaffold** (§1).
- Existing tracking footprint → **migration** (§2). Recognize precursors by
  footprint: root-level `MILESTONES.md`/`DESIGN.md`/`ROADMAP.md` with
  status inside CLAUDE.md ("Lineage B"); an older `project/` layout with
  `STATUS.md`/`LOG.md`/`PRINCIPLES.md` or per-milestone files ("Lineage A" —
  precursors used `project/`, not `cairn/`);
  repo-local milestone skills in `.claude/skills/`. Unrecognized footprints
  get an interview, not a guess.
- Already on cairn → **repair mode**: verify every §1 piece exists
  and is intact; fix what's missing; report.

## 1. Fresh scaffold

Create (from `${CLAUDE_PLUGIN_ROOT}/skills/shared/templates/` where a
template exists):

```
cairn/
├── DESIGN.md          # skeleton: Purpose & Scope / Function Families /
│                      # Conventions / Design Principles — IP<n> = Inviolable
│                      # (hard constraint) block first, then GP<n> = Guiding
│                      # (tradeable with justification); numbers never
│                      # reused / Architecture / Known issues
├── ROADMAP.md         # empty index (below)
├── DECISIONS.md       # header + append-only note (see decision.md template)
├── milestones/archive/
├── reviews/archive/
└── references/pdf/    # plus empty INDEX.md
```

ROADMAP.md skeleton (keep under 60 lines forever):

```markdown
# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: YYYY-MM-DD_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 5 most
     recent done rows — older ones live in milestones/archive/ + git -->

## Candidates
<!-- unnumbered ideas; one line each: idea — added YYYY-MM-DD — links -->
```

Then:

- Append `templates/claude-md-section.md` to CLAUDE.md (create CLAUDE.md if
  absent). If a conflicting section exists, show the diff and ask.
- `.Rbuildignore`: add `^cairn$` (packages only).
- `.gitignore`: add `cairn/references/pdf/` and `cairn/.merge-approved`
  (single-use merge-approval marker written at review gates, consumed by
  the plugin's merge-guard hook — never committed).
- Fill DESIGN.md's Purpose & Scope from DESCRIPTION and a quick read of
  `R/` — 5–10 honest lines, marked for the user to refine; never invent
  principles.
- Commit (docs-only, main): `cairn-init: scaffold tracking system`; push
  if a remote exists (origin/main is main — see tracking-rules git model).
- Routing chip, composed from what the scaffold found (chip rules per
  tracking-rules) — e.g. **Plan the first milestone** → `/milestone-plan`
  (recommended) / Run `/milestone` / Stop.

## 2. Migration protocol

Governing principle: **migrate the living, entomb the dead.** Completed
history is never converted — conversion of dozens of done milestones is
where hallucination and loss happen, and git already preserves everything.
Only *live* state gets translated.

**Variant: adopt-in-place.** When the precursor is young (little completed
history to protect) and its structure is already near-identical to cairn's
(per-milestone files, an index with compatible statuses), full entombment
is overkill: propose moving the live files into `cairn/` and adjusting
them to the templates in place — keeping their IDs — instead of entombing
and re-translating. Choosing this variant is a question-gate decision at
step 3; present it alongside the default, never silently. Steps 4–5
collapse into the in-place adoption; everything else — branch + PR, the
no-invention rule, and the step-7 ledger + audit bar — applies unchanged.
Lineage: M03 tidymedia pilot (PR #8).

1. **Preconditions.** Clean working tree. Ideally nothing in flight — an
   in-progress item is either finished first (recommend it) or carried over
   as the sole `in-progress` milestone, explicitly confirmed.

2. **Branch + PR.** All migration work on `cairn-init-migration`, merged via
   PR — one reviewable, revertible diff. Never on main.

3. **Inventory + proposal.** List every legacy tracking file and every live
   item found (in-flight/planned work, backlog/parking-lot/someday items,
   open questions, decisions still governing active work). Present the
   proposed disposition of each at one question gate. Fixed status mapping:
   `READY`→`planned`, `IN PROGRESS`/`active`→`in-progress`,
   `BLOCKED`→`blocked`, parking-lot/someday/candidates→`candidate` rows,
   everything finished→entombed. Ambiguities are asked, not guessed.

4. **Entomb history verbatim.** Legacy tracking files move whole and
   unmodified to `cairn/legacy/` (committed). New ROADMAP.md carries one
   header line: "Pre-migration history: see `cairn/legacy/` and git log."
   No completed milestone is ever rewritten into the new format — not even
   as a summary.

5. **Translate only live state** under a **no-invention rule**: never infer
   a status, date, or rationale that isn't written down — mark unknown or
   ask.
   - Live items → milestone files (template) or `candidate` rows.
   - **IDs are never renumbered.** New numbering continues from the legacy
     maximum (a repo at M53 starts at M54). Legacy decision IDs (ADR-0nn,
     D-00n, DESIGN §refs) stay valid as citations into `cairn/legacy/`;
     DECISIONS.md starts fresh at D-001 with a header note pointing at the
     legacy log; only still-governing decisions are re-recorded (citing
     their legacy ID).
   - Unresolved open questions / known issues → `candidate` rows or DESIGN
     "Known issues", per the ownership table.

6. **Redistribute and deactivate.**
   - Old CLAUDE.md content redistributed per the ownership table:
     invariants → DESIGN or CLAUDE hard rules; status slots and milestone
     indexes → deleted (ROADMAP owns status now); commands kept. Append the
     standard CLAUDE.md section.
   - **Old repo-local skills and rulebooks move to `cairn/legacy/`** —
     they must not remain in `.claude/skills/`, where they would collide
     with or contradict this plugin's skills.
   - Repo-specific assets with no canonical home (spec files, coverage
     matrices, principles docs) stay in `cairn/` as declared
     repo-specific files — kept, not forced into canonical shapes.
   - Scaffold anything from §1 that's still missing (ignore entries, dirs).

7. **Accept by audit + ledger.** The PR is mergeable only when: (a) the
   `/milestone` health audit passes clean on the branch, and (b) a
   **migration ledger** in the PR description accounts for every legacy
   file and every live item — old location → new location, "entombed", or
   "dropped at user request". Nothing silently vanishes. The user approves
   the merge like any milestone.

8. Routing chip, composed from the migration's actual end state — e.g.
   **Run a health audit** → `/milestone` (recommended) / Plan a milestone
   → `/milestone-plan` / Stop.
