<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M41: Migration stress-test pilot — intraclass (first Lineage A)

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP3, GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** cairn `m41-migration-pilot-intraclass`; intraclass migration on `cairn-init-migration` (PR TBD)   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Harden `/cairn-init` §2 by piloting it live on intraclass — the first **Lineage A**
precursor (a full multi-file `project/` board) — folding small isolable gaps back
into the skill and deferring design-level ones as candidates.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** run `/cairn-init` §2 migration live on `jmgirard/intraclass` on a
`cairn-init-migration` branch → a docs-only PR (no package code touched); entomb
the `project/` board + the 6 repo-local `.claude/skills/` verbatim to
`cairn/legacy/`; translate only live state under the no-invention rule; capture
the Lineage A gaps as "Pilot 3 — intraclass" in
`references/migration-pilot-notes.md`; fold small `fix-here` gaps into cairn
(skill edit + guard test); defer design-level gaps as ROADMAP candidates.

**Out:** oracle-doctrine validation against intraclass's oracle system → M42
(depends on M41). Building the `ORACLES.md` registry or the R-provenance guard →
the two standing deferred candidates. Merging the intraclass PR → the user
approves it separately at intraclass's own gate (this milestone does not force
adoption). Design-level protocol hardening → a candidate-driven follow-on
milestone. Reformatting intraclass's `PRINCIPLES.md` into IP/GP → `/design-interview`
(§2 step 5 routes it there), not this milestone.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: The §2 migration runs end-to-end on intraclass on a
      `cairn-init-migration` branch cut from intraclass's detected default
      branch, and a **docs-only PR** exists in `jmgirard/intraclass` (URL in the
      header + ledger) touching no package code — `git diff --stat <base>..<branch>`
      shows no change under `R/`, `tests/`, `data-raw/`, `man/`, `NAMESPACE`,
      `DESCRIPTION`.
- [ ] AC2: Legacy entombment is **verbatim** — every `project/` tracking file and
      every repo-local `.claude/skills/` skill moved to `cairn/legacy/` with no
      content change, provable by `git diff -M --summary <base>..<branch>` showing
      `rename … (100%)` for each (M20 lesson).
- [ ] AC3: The `/milestone` health audit (`cairn_validate`) passes clean on the
      branch **run with CWD = intraclass** (M20 lesson), OR any FAIL is a
      documented, gate-accepted exception recorded in the ledger.
- [ ] AC4: A **migration ledger** in the PR description accounts for every legacy
      `project/` file and every live item (old→new location / entombed /
      candidate / dropped-at-user-request) — nothing silently vanishes (IP3).
- [ ] AC5: The Lineage A findings are recorded as "Pilot 3 — intraclass" in
      `cairn/references/migration-pilot-notes.md`, each gap tagged
      `fix-here | candidate | out`.
- [ ] AC6: Every `fix-here` gap is fixed in cairn this milestone with a guard test
      that **fails before** the fix; every design-level gap is a ROADMAP candidate
      row. (Zero `fix-here` gaps is a valid outcome, recorded — as in M20.)
- [ ] AC7: cairn's own guard-test suite passes
      (`python3 -m unittest discover -s scripts/tests` and the `skills/tests`
      suite). (R gates are waived here — cairn is a plugin, not an R package.)

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T4, T5, T6
- AC2 → T3
- AC3 → T6
- AC4 → T2, T3, T6
- AC5 → T7
- AC6 → T8
- AC7 → T8

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: Preconditions — `cd` into `jmgirard/intraclass`; confirm clean tree and
      no in-flight milestone (STATUS.md says none active); detect the default
      branch (per the canonical recipe); cut `cairn-init-migration` from the
      up-to-date default branch.
- [ ] T2: Inventory + proposal — list every `project/` file, the 6 repo-local
      `.claude/skills/`, and every live item (v0.1.0 release consolidation,
      parking-lot candidates, open design questions); present the per-item
      disposition at cairn-init's migration question gate (fixed status mapping;
      no-invention rule).
- [ ] T3: Entomb verbatim — move all `project/` tracking files + the 6 repo-local
      skills whole to `cairn/legacy/`; verify each is a 100% rename.
- [ ] T4: Translate live state — author `cairn/ROADMAP.md` (IDs continue from the
      legacy max M47 → M48+; live items → `candidate` / `blocked` / `planned` per
      no-invention), `DECISIONS.md` (still-governing ADRs re-recorded citing legacy
      IDs; **Compromise A** default for the rich 4959-line decision log), `LESSONS.md`,
      `references/INDEX.md`; keep `PRINCIPLES.md`/`COVERAGE.md`/`estimand-specs/`
      as declared repo-specific files under `cairn/` (IP/GP formalization deferred
      to `/design-interview`).
- [ ] T5: Redistribute + deactivate — old `CLAUDE.md` per the ownership table (drop
      status/index slots, keep commands + invariants, append the cairn section);
      reference sweep (in-code refs naming a relocated `project/` file; CLAUDE prose
      naming an entombed skill) → repoint or note-and-leave; prune stale per-file
      `.Rbuildignore` entries; scaffold any missing §1 pieces.
- [ ] T6: Health audit + ledger + PR — run `cairn_validate` (CWD = intraclass);
      assemble the migration ledger; open the docs-only PR (record its URL in the
      header). Do **not** merge — that is intraclass's own gate.
- [ ] T7: Capture "Pilot 3 — intraclass" in `references/migration-pilot-notes.md` —
      the Lineage A ledger summary + a gap table, each gap tagged
      `fix-here | candidate | out`, contrasting Lineage A against the Lineage B
      pilots (M20/M21).
- [ ] T8: Fold `fix-here` gaps into cairn (skill edit + guard test that fails before
      the fix); file each design-level gap as a ROADMAP candidate row; run the cairn
      guard-test suites green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (third migration pilot; first Lineage A; user chose live branch + real PR).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
