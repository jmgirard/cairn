---
name: cairn-init
description: Adopt the cairn system in a repo - scaffold the cairn/ tracking files, CLAUDE.md section, and ignore entries; or migrate an existing precursor tracking system. Use when the user wants to set up, initialize, adopt, repair, or migrate to cairn in a repository.
argument-hint: ""
---

# /cairn-init — scaffold, repair, or migrate

Plugin root: every `${CLAUDE_PLUGIN_ROOT}` path below is under the plugin
install directory. When the shell has that variable unset or empty — the
symlink install in `~/.claude/skills` leaves it so — substitute the
grandparent of this skill's directory (the `Base directory for this skill:`
line the harness prints above) in every read and command below; never run a
command with the variable empty.

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first.
Idempotent: safe to re-run any time; re-runs report and repair missing or
damaged pieces and **never overwrite user content without asking**.
Phase header: `# cairn-init` → `## Scaffold` / `## Repair` / `## Migration §n`.
Chapter markers: mark a chapter at each phase transition — each phase its
`Phase header:` directive names (session start implicit).

## 0. Detect the situation

- **Environment check (RR01 §10.2).** Before anything else, probe the
  external tools cairn leans on (`command -v git python3 gh`; `git remote`)
  and report each gap with its degradation path — one line per gap, then
  proceed (only a missing `git` is fatal):
  - `git` absent → stop: cairn is git-based; there is nothing to adopt.
  - `python3` absent → the plugin's hooks and the `scripts/` health checks
    (`cairn_validate`, `cairn_next`) are unavailable; skills degrade to
    by-hand file reads against the tracking files. On Windows (no `python3`
    on PATH by default) the registered hooks fall back to the `py` launcher
    (hooks.json) — best-effort, unverified on Windows (DESIGN Known
    issues); install Python 3 for the scripts either way.
  - `gh` absent or unauthenticated → PR creation, `gh pr checks`, and the
    mechanical merge gate are unavailable: PRs and merges happen in the
    GitHub UI and the approval model becomes honor-system (the merge-guard
    hook sees only agent Bash). Recommend `gh auth login`.
  - no git remote → local-only mode: PR flows degrade to local branch
    merges and push steps no-op; recommend adding a remote before the
    first milestone.
- **CI runs on tracking-only pushes (M178, M181).** When `.github/workflows/`
  exists, run
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_ci_paths.py" --report`;
  when it does not, this bullet is silent, as it is when every report line
  reads `no push or pull_request trigger`. When the report names a workflow
  file with a `push` or `pull_request` trigger, or reports one
  `unrecognized`, say in plain words:
  (a) cairn's tracking-only commits — phase-boundary checkpoints and
  review-side records — reach the remote on every branch push and start the
  push-triggered workflows whose `branches` filter admits the branch;
  (b) a `pull_request` trigger's filter reads the whole PR diff, so ignoring
  `cairn/**` skips a tracking-only push only for `push` triggers;
  (c) under branch protection requiring a check, a path-skipped run leaves
  that check pending and blocks the merge (the Branch-protection
  compatibility candidate keeps that remainder). Then (d) run
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_ci_paths.py" --apply --dry-run`
  (needs PyYAML; writes nothing; one line per file: `would apply` or
  `refused: <reason>`). When at least one dry-run line reads `would apply`,
  pose one approve/decline chip naming those files, in the same confirmation
  round as §0's other options (the disambiguation gate, the project-type
  chip) when one is posed, else as its own chip; the chip says the edit adds
  `- 'cairn/**'` under each named file's `push` → `paths-ignore` and nothing
  else (a last line lacking its line ending gains one), and a decline writes nothing to the workflow files, the by-hand
  suggestion below then standing for the declined files too. On approval run
  the same command without `--dry-run`, re-run `--report`, and state that
  the edited workflow files are left uncommitted for the operator to commit
  (a CI-config change is not a tracking commit; the §1 and §3 commit bullets
  exclude them, and both close blocks name them). A file the dry run refuses
  keeps the by-hand suggestion: for each such file whose `push` verdict lacks both `cairn/**` and `paths`,
  show the item to add — `- 'cairn/**'` under that trigger's `paths-ignore`,
  the key created as a block sequence where the trigger has none, and a
  scalar `on: push` or flow-list `on: [push, …]` first rewritten in block form (`on:` holding a `push:` key) before the item can go under it; for a
  `push` verdict showing `paths` and not `paths-ignore`, say that trigger
  cannot take `paths-ignore` (GitHub accepts one of the two per trigger) and
  leave it to the operator. When the dry run exits 3 (PyYAML absent), the
  by-hand suggestion stands for every such file and the bullet says that
  installing PyYAML enables the applied edit. This bullet
  sits in §0, so the scaffold and repair paths both enter it.
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
- **Collaboration mode (M184, D-137).** Decide whether the operator owns
  this repo or contributes to someone else's. Read
  `gh repo view --json viewerPermission -q .viewerPermission` (with `gh`
  absent or no remote, the read is skipped and the recommendation is
  `owner`): `ADMIN`/`MAINTAIN`/`WRITE` recommend **owner** — today's rules;
  `READ`/`TRIAGE`, or a remote that resolves to a fork of another
  account's repo, recommend **guest** — `cairn/` kept local and never
  committed, nothing written outside it (tracking-rules "Collaboration
  mode"). Pose a **mode chip** (AskUserQuestion: owner / guest, the read's
  recommendation first) in §0's confirmation round; the chosen mode is
  written as the second header line of `cairn/PROFILE.md`,
  `# Collaboration mode: guest` (owner may be written or left absent —
  absent reads as owner). Guest selected → §1 follows its **Guest mode**
  passage; §3 repair reads the line from the existing file, never re-asks.
- **Toolchain profile.** Select the repo's profile in this order:
  `DESCRIPTION` present → **r-package**; else `pyproject.toml` (primary) /
  `setup.py` / `setup.cfg` present → **python**; else a `Dockerfile` as the
  **only** toolchain marker → **docker-image**; otherwise → **generic**.
  `DESCRIPTION` outranks a `pyproject.toml` in a hybrid repo. A repo carrying
  **both** a `Dockerfile` and a language marker (`DESCRIPTION` /
  `pyproject.toml` / `setup.py` / `setup.cfg`) is a hybrid image+package repo.
  Run a **disambiguation gate** (AskUserQuestion)
  asking which is the primary deliverable — the language package or the
  container image — and select the chosen profile rather than guessing (the
  language markers keep their order above on the language side). cairn-init instantiates the chosen reference
  (`${CLAUDE_PLUGIN_ROOT}/skills/shared/profiles/<name>.md`) into
  `cairn/PROFILE.md` at §1; the operational skills read its slots for
  language-specific commands (tracking-rules "Toolchain profiles"). Confirm the
  recommended profile with the user before writing.
- **Greenfield?** A new/empty repo — no source to read and no toolchain marker
  (`DESCRIPTION` / `pyproject.toml` / `setup.py` / `setup.cfg` / `Dockerfile`) —
  has no profile to infer. When this fires, present a **project-type chip**
  (AskUserQuestion: R package / Python package / Docker image / generic;
  recommend per any weak signal, else generic) to select the profile
  *explicitly* rather than silently defaulting to
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
- Already on cairn → **repair mode** (§3).

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
├── DECISIONS.md       # header from templates/decisions.md (entry shape: decision.md)
├── LESSONS.md         # header from templates/lessons.md; repo lessons, capped 50 lines / 20,000 bytes (D-015; byte budget D-119)
├── PROFILE.md         # toolchain profile (r-package | python | docker-image | generic), instantiated
│                      # from skills/shared/profiles/<name>.md; capped 120 lines
├── milestones/archive/
├── reviews/archive/
└── references/sources/    # plus empty INDEX.md
```

ROADMAP.md skeleton (keep under 60 lines and 24,000 bytes forever):

```markdown
# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: YYYY-MM-DD (one short line, replaced each pass — never appended to)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->

## Candidates
<!-- unnumbered ideas; one line each, ordered high → normal → low:
     - [high] idea — added YYYY-MM-DD — links
     - idea — added YYYY-MM-DD — links
     the opening token is `[high]`/`[low]` or absent (`normal`) — tracking-rules "Candidate priority token" -->
```

Then:

- Append `templates/claude-md-section.md` to CLAUDE.md (create CLAUDE.md if
  absent). If a conflicting section exists, show the diff and ask.
- `.Rbuildignore`: add `^cairn$` (packages only). On a migration, also prune
  stale per-file entries for tracking files that moved into `cairn/` (§2 step 6).
- `.gitignore`: add `cairn/references/sources/`, `cairn/.merge-approved`, and
  `cairn/.merge-approved.pending` (the single-use merge-approval marker
  written at review gates and its consumed-but-unresolved state — the
  plugin's merge-guard hooks manage both; never committed).
- Instantiate `cairn/PROFILE.md` from the selected reference profile
  (`${CLAUDE_PLUGIN_ROOT}/skills/shared/profiles/<name>.md` — `r-package.md`,
  `python.md`, `docker-image.md`, or `generic.md` per the selection order above) — copy it
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
  the repo's obvious first milestone, surfaced in the close block below. The
  openers are toolchain-config only; DESIGN *principle* elicitation stays
  `/design-interview` (offered in the close block), never duplicated here.
- Fill DESIGN.md's Purpose & Scope from DESCRIPTION and a quick read of
  `R/` — 5–10 honest lines, marked for the user to refine; never invent
  principles. **In a greenfield repo** there is no DESCRIPTION or source to
  read and the greenfield openers above already seeded Purpose & Scope
  (distribution ambition) and Conventions (oracle-on) — extend those honestly,
  never overwrite them. The deep version — eliciting the contract boundary,
  conventions, and IP/GP principles the code can't show — is
  `/design-interview`, offered in the close block below; this step only
  seeds the file.
- Commit (docs-only, on the default branch): `cairn-init: scaffold tracking
  system`, staging the scaffold by path and never a workflow file §0's chip
  edited (`.github/workflows/*.yml`, `*.yaml`) — that file stays in the
  working tree for the operator; push if a remote exists (the remote's
  default branch is authoritative — see tracking-rules git model).
- Close block (tracking-rules "Question gates and phase closes"), composed
  from what the scaffold found — recap, status line, fenced next command(s)
  with plain labels — e.g. `/design-interview` to turn the seeded DESIGN.md
  into an elicited one (the natural first move in a fresh repo), or
  `/milestone-plan` where the package skeleton is the obvious first
  milestone — the name of each workflow file §0's chip edited and left
  uncommitted, when it edited one — and the adjust-or-`/clear` safety line;
  no chip.

### Guest mode

When §0's mode chip chose **guest**, §1 changes in exactly these ways;
everything not named here (the `cairn/` tree, the ROADMAP skeleton, the
PROFILE instantiation, the DESIGN seed, the greenfield openers) runs as
above:

1. **The mode line.** After instantiating `cairn/PROFILE.md`, insert
   `# Collaboration mode: guest` as its second line, directly under
   `# Toolchain profile: <name>` (the profile templates carry no mode line;
   init writes it).
2. **The `.git/info/exclude` write.** Append `cairn/` to the file
   `git rev-parse --git-path info/exclude` names — `.git/info/exclude` in a
   plain checkout, the main repo's file in a worktree, where `.git` is a
   file (create it if absent). This is the only write outside `cairn/`,
   and it is to a file git never tracks; it is what `cairn_validate`'s
   `scaffold present` check requires in guest mode in place of the ignore
   entries below. That check also FAILs while `git ls-files -- cairn` lists
   anything: an exclude line covers untracked files only, so a repo that
   ever committed `cairn/` first takes `git rm -r --cached cairn`.
3. **Five writes skipped.** (a) the **CLAUDE.md append** — the session hook
   injects the routing section from the plugin's template instead; (b) the
   **`.gitignore` entries** — nothing under `cairn/` is ever committed, so
   there is nothing to keep out of it; (c) the **`.Rbuildignore` entry**;
   (d) the **CI `paths-ignore` chip** of §0 — the report bullet still runs
   and says what it found, but no edit is offered, because workflow files
   are the maintainers'; (e) the **scaffold commit + push** — `cairn/` is
   excluded, so there is nothing to commit and the default branch is never
   pushed to.
4. **Close block.** Its status line names the mode; the safety line adds
   that `cairn/` exists only in this clone (a fresh clone starts from
   nothing, and `git clean -fdx` removes it).

The mode chip and the `viewerPermission` read behind its recommendation
are §0's; this passage is entered only on a guest selection.

## 2. Migration protocol

The protocol lives in
`${CLAUDE_PLUGIN_ROOT}/skills/shared/migration-protocol.md` — read it in
full when (and only when) §0 detects an existing tracking footprint
(progressive disclosure, M59: a greenfield scaffold or repair run never
loads it). Follow its steps 1–8 as this skill's §2; the `## Migration §n`
phase headers and the chapter-marker directive apply to them unchanged.

## 3. Repair

Reached from §0 when the repo is already on cairn. Repair restores §1 pieces
that are missing and migrates scaffold names **cairn itself** renamed; it
never rewrites content the repo authored.

- **Missing §1 pieces.** Verify every §1 piece exists and is intact; create
  what is missing; report each fix. Read `cairn/PROFILE.md`'s
  `# Collaboration mode:` line first: in **guest** mode the scaffold is §1's
  Guest mode passage — `cairn/` in the exclude file (`git rev-parse
  --git-path info/exclude`) is the piece to
  verify and restore, `git ls-files -- cairn` must list nothing, and the CLAUDE.md section, the `.gitignore` and
  `.Rbuildignore` entries, and the commit + push below are not pieces at all
  (repair writes nothing outside `cairn/` and `.git/info/exclude`). A **missing `cairn/PROFILE.md`**
  (a repo that adopted cairn before profiles) is backfilled by inference —
  `DESCRIPTION` present → r-package, else `pyproject.toml`/`setup.py`/
  `setup.cfg` → python, else a `Dockerfile` (sole marker) → docker-image, else
  generic — restoring the explicit declaration without changing behavior (the
  inference is exactly what the skills fall back to when the file is absent;
  with no user present, a hybrid `Dockerfile`+language-marker repo keeps the
  language marker — the disambiguation gate is a cairn-init-time step only).

- **Scaffold deprecations.** cairn is post-1.0, so a scaffold name cairn
  renames follows the deprecation cycle rather than breaking adopters
  (D-047): the old `.gitignore` entry keeps satisfying `scaffold present`,
  and a non-failing `scaffold deprecations` advisory names its successor.
  The advisory names the fix; **this step is the only place cairn performs
  it** — `/milestone`'s audit surfaces advisories and never auto-fixes them,
  so an un-migrated repo carries the WARN until repair runs.

  Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"` and read its `scaffold deprecations` advisory.
  The advisory prints two kinds of line: an entry line — `'<old>' is superseded by '<new>'` — naming a superseded `.gitignore` entry, and a directory line — `directory '<old>' still holds files` — naming a superseded shelf directory still occupied on disk, whatever `.gitignore` says (M129: this arm is what lets a repair re-run resume a declined or deferred move).
  Act on every line the advisory prints, never on a pair named in this text — the advisory is generated from the plugin's own map of superseded entries, so a rename added after this was written migrates with no edit here.
  Per line, by kind:

  On an entry line: **Add the successor entry, no ask.** `<new>` joins `.gitignore` and `<old>` stays for now.
  It is cairn's own scaffold line, not one the repo authored, and adding
  touches nothing git tracks — so it needs no gate. Both entries present is
  silent to the entry arm, so the shelf stays ignored for as long as the old
  directory still holds files.

  On a directory line: it is only the trigger for the directory-state cases below — the case is still chosen by what is on disk.
  A directory line with both `.gitignore` entries already present is exactly
  the declined-or-deferred move this arm exists to resume; re-entering the
  cases below is how repair resumes it.

  Then take **exactly one** of the cases below, chosen by what is on disk
  *before* anything moves. They are mutually exclusive states, not a sequence —
  reading them in order would put a move ahead of the check meant to stop it.

  - **Both directories present: surface, never clobber.** Never merge or overwrite one shelf with the other unasked.
    Report what each holds and let the user choose — merge old into new, keep
    both and skip, or stop.
  - **Only the old directory present: move it only after an explicit ask.** The shelf is gitignored, so its contents are untracked and git cannot restore them.
    Show what is on the shelf (file count, and the names when few) and ask
    via AskUserQuestion before moving anything. A declined move is reported
    and the directory left alone.
  - **Old directory absent: the entry change *is* the migration.** Nothing to
    move, nothing to ask.

  **Remove `<old>` from `.gitignore` only once the old directory is gone from disk.** A declined or deferred move keeps both entries, and both entries keep the shelf ignored;
  dropping the superseded entry while its directory still holds files would
  un-ignore untracked contents the repo may be keeping out of git deliberately.

  Close by re-running `cairn_validate.py`. **A quiet advisory now confirms the entries and the directory both** — the directory arm reads the filesystem, so a superseded shelf still holding files keeps its line firing whatever `.gitignore` says.
  A declined or deferred move therefore stays visible to the next repair run
  by design; the line is silenced only by the directory being moved or
  removed (an empty leftover is the one residue it stays silent on — nothing
  is lost by that). Report the directory outcome on its own: what moved,
  what was declined, and what still awaits a choice.

- Commit (docs-only, on the default branch): **stage the files repair touched by path, never `git add -A` or `.`** — a mid-migration shelf is untracked
  by design, and a blanket stage would commit the very files the entry above
  keeps ignored, and a workflow file §0's chip edited (`.github/workflows/*.yml`,
  `*.yaml`) is never staged — it stays in the working tree for the operator.
  Then `cairn-init: repair scaffold`; push if a remote exists.
  Nothing to fix → report that and skip the commit.
- Close block (tracking-rules "Question gates and phase closes"), composed
  from what repair found — e.g. `/milestone` fenced first (re-audit a repo
  that just changed), `/milestone-plan` beside it, the name of each workflow
  file §0's chip edited and left uncommitted, when it edited one, and the
  safety line.
