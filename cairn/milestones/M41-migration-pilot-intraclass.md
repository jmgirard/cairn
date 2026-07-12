<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M41: Migration stress-test pilot — intraclass (first Lineage A)

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP3, GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** cairn `m41-migration-pilot-intraclass`; intraclass migration on `cairn-init-migration` → PR https://github.com/jmgirard/intraclass/pull/54   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] T1: Preconditions — cut `cairn-init-migration` from intraclass `main` @ 9a712c1; both trees clean; no in-flight milestone (M47 shipped).
- [x] T2: Inventory + proposal — presented the disposition at the migration gate; user chose pointer-only DECISIONS + integrate-where-cairn-has-a-home; principles reversed to note-and-leave after the 70-in-code-ref finding.
- [x] T3: Entomb verbatim — 27 moves, all 100% renames (status/history + 6 skills → `legacy/`; PRINCIPLES/REFERENCES/COVERAGE/estimand-specs → cairn homes). Evidence: `git diff -M --summary` all `rename … (100%)`, 0 ins/0 del.
- [x] T4: Author fresh — `DESIGN.md` (seed), `ROADMAP.md` (legacy pointer + 3 candidates, IDs from M48), `DECISIONS.md` (**pointer-only**, per gate), `LESSONS.md`, `references/INDEX.md`. (Compromise A superseded by the gate: no DESIGN.md existed; concern-files kept in their cairn homes.)
- [x] T5: Redistribute + sweep — `CLAUDE.md` repointed + cairn section appended; `.Rbuildignore` `^project$`→`^cairn$`; `.gitignore` += pdf/ + merge-approved; README roadmap ref repointed; 2 `tests/` path refs note-and-leave (docs-only).
- [x] T6: Audit + ledger + PR — `cairn_validate` 12/12 clean (CWD=intraclass); ledger in PR #54 body; docs-only PR opened, not merged (intraclass's own gate).
- [x] T7: "Pilot 3 — intraclass" written in `references/migration-pilot-notes.md` — Lineage A ledger + 5-row gap table (G-I1..G-I5), contrasted with the Lineage B pilots.
- [x] T8: **No `fix-here` emerged** (M20-like — gaps are design-level + interconnected); filed one grouped "Lineage A migration guidance" candidate; cairn guard suites green (scripts 53, skills 94).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (third migration pilot; first Lineage A; user chose live branch + real PR).
- 2026-07-12: gate amendment (substantive) — no DESIGN.md existed in the Lineage A precursor; concern-files (PRINCIPLES/REFERENCES/COVERAGE/estimand-specs) integrated into cairn homes / kept repo-specific rather than entombed; DECISIONS **pointer-only** (user choice) not "re-record still-governing".
- 2026-07-12: principles disposition reversed at gate — finding 70 in-code `PRINCIPLES.md #N` refs across 29 files blocks folding into DESIGN.md's IP/GP on a docs-only PR; kept `cairn/PRINCIPLES.md` note-and-leave, numbering intact.
- 2026-07-12: migration executed on intraclass → PR #54 (docs-only, 0 package files, 27×100% renames); `cairn_validate` 12/12 clean. Confirmed IP3 (migration ledger accounts for every file) + GP3 (one-command adoption on a mature Lineage A repo).
- 2026-07-12: no `fix-here` emerged (M20-like); 5 design-level gaps (G-I1..G-I5) → one grouped "Lineage A migration guidance" candidate. Cairn guard suites green (scripts 53, skills 94). Status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
