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

- **Default branch.** Detect the repo's default branch —
  `git symbolic-ref --short refs/remotes/origin/HEAD` (strip the `origin/`
  prefix), falling back to the current branch (`git branch --show-current`)
  whenever that fails: no remote, or `origin/HEAD` unset (a shallow clone, a
  fresh `git remote add`, or a CI checkout that never ran `set-head`). cairn
  does not assume `main`; use the detected name wherever the steps below (and
  the tracking-rules git model) say "the default branch".
- No DESCRIPTION file → **non-package repo**: say so and ask — adapt
  (scaffold the tracking system with the **generic** toolchain profile, minus
  R-specific guardrails/gates) or abort. Never scaffold R machinery into a
  non-package repo silently.
- **Toolchain profile.** Select the repo's language profile: `DESCRIPTION`
  present → **r-package**; otherwise → **generic**. cairn-init instantiates the
  chosen reference (`${CLAUDE_PLUGIN_ROOT}/skills/shared/profiles/<name>.md`)
  into `cairn/PROFILE.md` at §1; the operational skills read its slots for
  language-specific commands (tracking-rules "Toolchain profiles"). Confirm the
  recommended profile with the user before writing.
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
  `DESCRIPTION` present → r-package, else generic — restoring the explicit
  declaration without changing behavior (the inference is exactly what the
  skills fall back to when the file is absent).

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
├── PROFILE.md         # toolchain profile (r-package | generic), instantiated
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
- `.gitignore`: add `cairn/references/pdf/` and `cairn/.merge-approved`
  (single-use merge-approval marker written at review gates, consumed by
  the plugin's merge-guard hook — never committed).
- Instantiate `cairn/PROFILE.md` from the selected reference profile
  (`${CLAUDE_PLUGIN_ROOT}/skills/shared/profiles/r-package.md` if DESCRIPTION
  present, else `generic.md`) — copy it verbatim; the repo edits its slots
  (notably `verify`) afterward as needed.
- Fill DESIGN.md's Purpose & Scope from DESCRIPTION and a quick read of
  `R/` — 5–10 honest lines, marked for the user to refine; never invent
  principles. The deep version — eliciting the contract boundary,
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
  elicited one) / **Plan the first milestone** → `/milestone-plan` /
  Run `/milestone` / Stop.

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

2. **Branch + PR.** All migration work on `cairn-init-migration`, cut from the
   up-to-date default branch, merged via PR — one reviewable, revertible diff.
   Never on the default branch.

3. **Inventory + proposal.** List every legacy tracking file and every live
   item found (in-flight/planned work, backlog/parking-lot/someday items,
   open questions, decisions still governing active work). Present the
   proposed disposition of each at one question gate. Fixed status mapping:
   `READY`→`planned`, `IN PROGRESS`/`active`→`in-progress`,
   `BLOCKED`→`blocked`, parking-lot/someday/candidates→`candidate` rows,
   everything finished→entombed. `READY`→`planned` holds only when the item
   carries acceptance criteria and ordered tasks — otherwise it is a
   `candidate` (see step 5). Ambiguities are asked, not guessed. **Clean
   domain skills** — repo-local skills with domain value and no tracking
   coupling (the §6 classification) — are surfaced here too, each with an
   explicit keep-or-entomb choice.

4. **Entomb history verbatim.** Legacy tracking files move whole and
   unmodified to `cairn/legacy/` (committed). New ROADMAP.md carries one
   header line: "Pre-migration history: see `cairn/legacy/` and git log."
   No completed milestone is ever rewritten into the new format — not even
   as a summary.

5. **Translate only live state** under a **no-invention rule**: never infer
   a status, date, or rationale that isn't written down — mark unknown or
   ask.
   - Live items → milestone files (template) or `candidate` rows. A legacy
     "planned"/`READY` item maps to cairn `planned` only if it carries
     acceptance criteria and ordered tasks; a scoped item with neither maps to
     a `candidate` row instead (inventing criteria violates no-invention) —
     replan it later.
   - **IDs are never renumbered.** New numbering continues from the legacy
     maximum (a repo at M53 starts at M54). Legacy decision IDs (ADR-0nn,
     D-00n, DESIGN §refs) stay valid as citations into `cairn/legacy/`;
     DECISIONS.md starts fresh at D-001 with a header note pointing at the
     legacy log; only still-governing decisions are re-recorded (citing
     their legacy ID). For a **large decision log** (dozens of ADRs),
     **pointer-only** is an explicit and often cleanest disposition: re-record
     *nothing* — `DECISIONS.md` is a pure pointer at the entombed legacy log,
     and active work cites `ADR-0nn` into `cairn/legacy/` directly. It is the
     most no-invention-safe choice for a log too large to re-record without
     risking drift. Lineage: M41 intraclass (58 ADRs → pointer-only).
   - Unresolved open questions / known issues → `candidate` rows or DESIGN
     "Known issues", per the ownership table. A large legacy backlog that
     would blow the <60-line ROADMAP cap one-row-per-item clusters into
     grouped candidate rows pointing at the entombed legacy `ROADMAP.md`
     (tracking-rules weight-caps remedies), never a per-item dump.
   - **Rich pre-existing `DESIGN.md`?** A large living DESIGN (hundreds of
     lines, embedded decision log, known issues) fits neither entombment nor
     the thin §1 scaffold. Default (**Compromise A**, the ackwards pilot's
     choice): keep it verbatim as `cairn/DESIGN.md` and re-record only
     still-governing decisions into `DECISIONS.md` (each citing its DESIGN
     anchor), deferring full decision-log extraction to the repo's own later
     `/design-interview`. Offer **Compromise B** (extract the whole decision
     log into `DECISIONS.md` now) only if the user asks — it is slower and
     invention-prone. Either way, hard-constraint invariants embedded in the
     DESIGN are **not** forced into IP/GP shape at migration time — route
     their formalization to `/design-interview`, which is built for it.
   - **Concern-split precursor (no single `DESIGN.md`)?** A Lineage A board
     splits DESIGN concerns across dedicated files (a principles doc, a
     decision log, references, coverage matrices, estimand/spec dirs) with no
     single DESIGN to keep verbatim or entomb, so neither the entomb/translate
     binary nor Compromise A fits. Map each concern-file to its cairn home
     where one exists (references → `references/`; a decision log → the
     `DECISIONS.md` pointer of this step), **keep repo-specific** where cairn
     has no home (coverage matrices, estimand/spec dirs) as declared
     repo-specific files under `cairn/`, and author a **thin `DESIGN.md` seed
     that points to them** rather than duplicating their content. Lineage: M41
     intraclass pilot (first Lineage A).

6. **Redistribute and deactivate.**
   - Old CLAUDE.md content redistributed per the ownership table:
     invariants → DESIGN or CLAUDE hard rules; status slots and milestone
     indexes → deleted (ROADMAP owns status now); commands kept. Append the
     standard CLAUDE.md section.
   - **Repo-local skills — classify, then entomb or ask.** A precursor's
     `.claude/skills/` holds two kinds. **Tracking-coupled** skills (they
     drive the old board/gate model — next-task pickers, milestone movers,
     release checklists) collide with or contradict this plugin's skills and
     **move to `cairn/legacy/`**; they must not remain in `.claude/skills/`.
     **Clean domain** skills (domain workflow with no tracking coupling — e.g.
     an estimator scaffold, an oracle-verification runner) carry value this
     plugin has no home for, so **surface them at the step-3 question gate for
     an explicit keep-or-entomb decision** rather than entombing blindly. A
     skill that is *both* domain and tracking-coupled entombs — the coupling
     wins (it would contradict the plugin) — but note its domain value has no
     cairn home yet, feeding the toolchain-profiles / oracle-registry
     candidates. Lineage: M41 intraclass (all 6 skills coupled — 4 purely, 2
     domain-but-coupled — so all entombed).
   - Repo-specific assets with no canonical home (spec files, coverage
     matrices, principles docs) stay in `cairn/` as declared
     repo-specific files — kept, not forced into canonical shapes.
   - **Reference sweep — repoint or note.** Moving files in steps 4–5
     strands references to them. Sweep for two kinds: (a) in-code references
     (source comments, tests) that name a relocated tracking file (e.g.
     `DESIGN.md s.N`, found in ~17 spots across ackwards' R sources and
     tests), and (b) redistributed CLAUDE.md prose that still names a
     just-entombed repo-local skill (e.g. "/plan-milestone step 8a"). Each
     hit takes one of two dispositions: **repoint** it to the new `cairn/`
     path, or **note-and-leave** when the content and anchors are preserved
     at the new path. Record which in the migration ledger.
     **Numbered-principle refs are a forced note-and-leave.** When the
     relocated file is a *principles doc cited by number* in package code
     (e.g. `PRINCIPLES.md #N` — 70× across 29 files in the M41 intraclass
     pilot), repoint is not available: folding those principles into
     `DESIGN.md`'s IP/GP renumbers them, which strands every in-code ref or
     forces a package-code touch that breaks the docs-only migration. Keep the
     principles file at a `cairn/` path with its **numbering and basename
     intact** (note-and-leave), and defer both the IP/GP formalization *and*
     the eventual in-code repoint to `/design-interview` + a target-repo code
     milestone. This is the blocking, larger form of the ~17-ref ackwards
     `DESIGN.md s.N` case above (M20 G6).
   - **Post-move hygiene:** prune per-file `.Rbuildignore` entries for
     tracking files that just moved into `cairn/` (e.g. `^DESIGN\.md$`,
     `^ROADMAP\.md$`) — `^cairn$` now covers them, so a stale per-file entry
     is dead weight that misleads the next reader.
   - Scaffold anything from §1 that's still missing (ignore entries, dirs).

7. **Accept by audit + ledger.** The PR is mergeable only when: (a) the
   `/milestone` health audit passes clean on the branch, and (b) a
   **migration ledger** in the PR description accounts for every legacy
   file and every live item — old location → new location, "entombed", or
   "dropped at user request". Nothing silently vanishes. The user approves
   the merge like any milestone.

8. Routing chip (AskUserQuestion), composed from the migration's actual end
   state — e.g.
   **Run a health audit** → `/milestone` (recommended) / Plan a milestone
   → `/milestone-plan` / Stop.
