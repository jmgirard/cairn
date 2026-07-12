<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M23: Migration-protocol §2 guidance hardening

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** M22
- **Branch/PR:** m23-migration-guidance

## Goal

Fold the M20 ackwards pilot's remaining migration-protocol gaps into
`/cairn-init` §2 and the rulebook — guidance for a rich living DESIGN.md,
in-code references to relocated tracking files, and post-move hygiene — so the
next real migration doesn't re-hit them.

## Scope

**In:**
- **Rich pre-existing DESIGN.md guidance (G3/G5).** §5 today only anticipates a
  thin DESIGN. Add guidance for a large living DESIGN with an embedded decision
  log: the keep-verbatim vs extract-to-`DECISIONS.md` choice (the Compromise
  A/B split the ackwards gate used — keep DESIGN verbatim, re-record only
  still-governing decisions, defer full decision-log extraction), and routing
  hard-constraint invariants → IP/GP formalization via `/design-interview`
  rather than forcing them at migration time.
- **In-code reference sweep (G6/G10).** Mature repos cite relocated tracking
  files by name in source comments and tests (~17 refs across 9 files + 3 tests
  in ackwards, e.g. `DESIGN.md s.N`); §4/§6 are silent, so a move strands them.
  Add a repoint-or-note sweep step with two dispositions (repoint the ref to the
  new `cairn/` path, or note-and-leave when content/anchors are preserved).
  Same step covers §6 sweeping redistributed CLAUDE.md prose for references to
  just-entombed repo-local skills (G10).
- **Post-move hygiene (G7/G2).** §1/§6: prune stale per-file `.Rbuildignore`
  entries after files move (today §1 only says add `^cairn$`). §0: widen
  Lineage B detection wording to cover a repo that already has a forward-only
  ROADMAP + an explicit status/`Current focus` slot (mapped cleaner than the
  current "status inside CLAUDE.md" assumption described).

**Out:**
- Default-branch parameterization and the CLAUDE.md weight cap → **M22**
  (dependency; the branch-parameterized §2 prose lands there first).
- Full decision-log extraction into `DECISIONS.md` for a migrated repo → the
  repo's own later `/design-interview` run, not the migration protocol.
- Building the toolchain-profile system → "Toolchain profiles" candidate.

## Acceptance criteria

- [ ] `/cairn-init` §2/§5 carries explicit guidance for a rich living DESIGN.md
      with an embedded decision log: the keep-verbatim vs extract-to-DECISIONS
      choice (Compromise A/B) and routing hard-constraint invariants to
      `/design-interview` for IP/GP formalization. Evidence: skill diff naming
      both dispositions and citing the ackwards case.
- [ ] §4/§6 gains a repoint-or-note sweep for (a) in-code references (source
      comments/tests) naming relocated tracking files and (b) redistributed
      CLAUDE.md prose referencing just-entombed repo-local skills — the step
      names the sweep and the two dispositions. Evidence: skill diff.
- [ ] Post-move hygiene is covered: §1/§6 instructs pruning stale per-file
      `.Rbuildignore` entries after the move, and §0 Lineage B detection wording
      is widened to include a forward-only ROADMAP + explicit status slot.
      Evidence: skill/§0 diff.
- [ ] Any new mechanical invariant (e.g. a required §2 sweep-step phrase the
      section-allow-list test keys on) is guard-tested; suite green over
      `skills/tests/` and `scripts/tests/`. Evidence: test run output.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4

## Tasks

- [ ] **T1** — Add §5 rich-DESIGN guidance to `skills/cairn-init/SKILL.md`:
      keep-verbatim vs extract-to-DECISIONS (Compromise A/B), invariants →
      `/design-interview`. Cite the ackwards pilot.
- [ ] **T2** — Add the §4/§6 repoint-or-note sweep step (in-code refs to
      relocated tracking files + CLAUDE prose refs to entombed skills), with the
      two dispositions.
- [ ] **T3** — Add §1/§6 `.Rbuildignore` prune guidance; widen §0 Lineage B
      detection wording (forward-only ROADMAP + explicit status slot).
- [ ] **T4** — Guard test any new mechanical invariant (keep the
      `test_section_allow_lists.py` literal-phrase invariants intact when
      editing SKILL prose — M18 lesson); run the full suite green; commit.

## Work log

- 2026-07-12: created by /milestone-plan. Absorbs ROADMAP candidates
  "Migration guidance for a rich pre-existing DESIGN.md" (G3/G5), "handle
  in-code references to relocated tracking files" (G6/G10), and "Migration
  hygiene tweaks" (G7/G2), all from `references/migration-pilot-notes.md` (M20).
  Depends on M22 (shared cairn-init §2 edits sequence after the branch
  parameterization); sequenced before M21.

## Decisions

## Review
