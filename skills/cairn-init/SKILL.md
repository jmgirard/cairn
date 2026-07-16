---
name: cairn-init
description: Adopt the cairn system in a repo - scaffold the cairn/ tracking files, CLAUDE.md section, and ignore entries; or migrate an existing precursor tracking system. Use when the user wants to set up, initialize, adopt, repair, or migrate to cairn in a repository.
argument-hint: ""
---

# /cairn-init — scaffold, repair, or migrate

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first.
Idempotent: safe to re-run any time; re-runs report and repair missing or
damaged pieces and **never overwrite user content without asking**.
Phase header: `# cairn-init` → `## Scaffold` / `## Repair` / `## Migration §n`.
Chapter markers: mark a chapter at each phase transition (session start implicit).

## 0. Detect the situation

- **Default branch.** Detect the repo's default branch per the canonical
  recipe in the tracking-rules git model: `git symbolic-ref --short
  refs/remotes/origin/HEAD` (strip the `origin/` prefix); if that fails but a
  remote exists — `origin/HEAD` unset locally (a shallow clone, a fresh
  `git remote add`, a CI checkout that never ran `set-head`) — query the
  remote with `git ls-remote --symref origin HEAD` and read the
  `ref: refs/heads/<name>` line. Only with no remote at all ask the user —
  never guess the local current branch. cairn does not assume `main`; use the
  detected name wherever the steps below (and the tracking-rules git model)
  say "the default branch".
- **Toolchain profile.** Select the repo's language profile in this order:
  `DESCRIPTION` present → **r-package**; else `pyproject.toml` (primary) /
  `setup.py` / `setup.cfg` present → **python**; otherwise → **generic**.
  `DESCRIPTION` outranks a `pyproject.toml` in a hybrid repo. cairn-init
  instantiates the chosen reference
  (`${CLAUDE_PLUGIN_ROOT}/skills/shared/profiles/<name>.md`) into
  `cairn/PROFILE.md` at §1; the operational skills read its slots for
  language-specific commands (tracking-rules "Toolchain profiles"). Confirm the
  recommended profile with the user before writing.
- **Greenfield?** A new/empty repo — no source to read and no toolchain marker
  (`DESCRIPTION` / `pyproject.toml` / `setup.py` / `setup.cfg`) — has no profile
  to infer. When this fires, present a **project-type chip** (AskUserQuestion:
  R package / Python package / generic; recommend per any weak signal, else
  generic) to select the profile *explicitly* rather than silently defaulting to
  generic, then run the greenfield opener flow (§1). A repo that has a marker or
  existing source is **not** greenfield: infer the profile as above and skip the
  openers.
- No existing tracking → **fresh scaffold** (§1).
- Existing tracking footprint → **migration** (§2). Recognize precursors by
  footprint: root-level `MILESTONES.md`/`DESIGN.md`/`ROADMAP.md` with status
  inside CLAUDE.md — or a forward-only `ROADMAP.md` plus an explicit status /
  `Current focus` slot (as the ackwards pilot had), which maps to cairn more
  cleanly than status-in-CLAUDE ("Lineage B"); an older `project/` layout with
  `STATUS.md`/`LOG.md`/`PRINCIPLES.md` or per-milestone files ("Lineage A" —
  precursors used `project/`, not `cairn/`);
  repo-local milestone skills in `.claude/skills/`. Unrecognized footprints
  get an interview, not a guess.
- Already on cairn → **repair mode**: verify every §1 piece exists
  and is intact; fix what's missing; report. A **missing `cairn/PROFILE.md`**
  (a repo that adopted cairn before profiles) is backfilled by inference —
  `DESCRIPTION` present → r-package, else `pyproject.toml`/`setup.py`/
  `setup.cfg` → python, else generic — restoring the explicit declaration
  without changing behavior (the inference is exactly what the skills fall back
  to when the file is absent).

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
├── LESSONS.md         # header + append-only note; repo lessons, capped 50 lines (D-015)
├── PROFILE.md         # toolchain profile (r-package | python | generic), instantiated
│                      # from skills/shared/profiles/<name>.md; capped 90 lines
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
<!-- rows grouped by status, not sorted by ID; keep only the 5 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->

## Candidates
<!-- unnumbered ideas; one line each: idea — added YYYY-MM-DD — links -->
```

Then:

- Append `templates/claude-md-section.md` to CLAUDE.md (create CLAUDE.md if
  absent). If a conflicting section exists, show the diff and ask.
- `.Rbuildignore`: add `^cairn$` (packages only). On a migration, also prune
  stale per-file entries for tracking files that moved into `cairn/` (§2 step 6).
- `.gitignore`: add `cairn/references/pdf/`, `cairn/.merge-approved`, and
  `cairn/.merge-approved.pending` (the single-use merge-approval marker
  written at review gates and its consumed-but-unresolved state — the
  plugin's merge-guard hooks manage both; never committed).
- Instantiate `cairn/PROFILE.md` from the selected reference profile
  (`${CLAUDE_PLUGIN_ROOT}/skills/shared/profiles/<name>.md` — `r-package.md`,
  `python.md`, or `generic.md` per the selection order above) — copy it
  verbatim; the repo edits its slots (notably `verify`) afterward as needed.
- **Greenfield openers (new/empty repos only).** When §0 flagged the repo
  greenfield, after instantiating `PROFILE.md` ask the opener set in batched
  AskUserQuestion rounds (question-gate rules) — each option marked with its
  consequence and a recommended **reversible default**:
  - **Universal layer** (every profile): distribution ambition — rendered per
    the selected profile (r-package → CRAN vs GitHub-only; python → PyPI vs
    private; generic → tagged public release vs internal-only), landing in
    DESIGN Purpose & Scope; and **numeric-work-needs-oracle-verification**
    (universal — D-024/D-025), landing in DESIGN Conventions (a line committing
    numeric results to the oracle doctrine's ≥2-types bar).
  - **Profile layer:** the selected profile's `greenfield-openers` slot
    questions, each landing in the durable home the slot names (a PROFILE slot,
    DESIGN Conventions). The generic profile adds none.
  - **Undecided** on any opener ⇒ take that opener's marked reversible default
    now and bank **one** ROADMAP `candidate` row recording the deferred choice
    (IP3 — nothing silently locked in).
  Stay **tracking-only**: record answers in `cairn/` files; never scaffold a
  package skeleton (`DESCRIPTION` / `pyproject.toml` / `R/` / `src/`) — that is
  the repo's obvious first milestone, surfaced on the routing chip below. The
  openers are toolchain-config only; DESIGN *principle* elicitation stays
  `/design-interview` (offered on the chip), never duplicated here.
- Fill DESIGN.md's Purpose & Scope from DESCRIPTION and a quick read of
  `R/` — 5–10 honest lines, marked for the user to refine; never invent
  principles. **In a greenfield repo** there is no DESCRIPTION or source to
  read and the greenfield openers above already seeded Purpose & Scope
  (distribution ambition) and Conventions (oracle-on) — extend those honestly,
  never overwrite them. The deep version — eliciting the contract boundary,
  conventions, and IP/GP principles the code can't show — is
  `/design-interview`, offered on the routing chip below; this step only
  seeds the file.
- Commit (docs-only, on the default branch): `cairn-init: scaffold tracking
  system`; push if a remote exists (the remote's default branch is
  authoritative — see tracking-rules git model).
- Routing chip (AskUserQuestion), composed from what the scaffold found
  (chip rules per tracking-rules) — e.g. **Run the design interview** →
  `/design-interview`
  (recommended for a fresh repo, to turn the seeded DESIGN.md into an
  elicited one) / **Plan the first milestone** → `/milestone-plan` (for a
  greenfield repo, the package skeleton is the obvious first milestone) /
  Run `/milestone` / Stop.

## 2. Migration protocol

The protocol lives in
`${CLAUDE_PLUGIN_ROOT}/skills/shared/migration-protocol.md` — read it in
full when (and only when) §0 detects an existing tracking footprint
(progressive disclosure, M59: a greenfield scaffold or repair run never
loads it). Follow its steps 1–8 as this skill's §2; the `## Migration §n`
phase headers and the chapter-marker directive apply to them unchanged.
