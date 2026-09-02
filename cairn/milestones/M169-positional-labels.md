# M169: Criteria and tasks carry positional labels

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Branch/PR:** m169-positional-labels

## Goal

Every milestone file's acceptance criteria and tasks open with the positional
label Coverage cites (`AC1:`, `T1:`), because the shipped template shows them
and the plan and implement skills state the rule.

## Scope

**In:** the milestone template's example items and section comments; the
binding-criterion ingest form unified to `ACn (BCm):` at its five sites;
`/milestone-plan` step 4's labeling rule; `/milestone-implement` step 6's
renumbering obligation on both its branches; a hand-run prose guard over the
new template and skill text. Tier: user-facing — the template and skills ship
to adopting repos, whose plan sessions instantiate them. Door trigger (D-090,
D-108): the shipped template shows bare bullets while the shipped Coverage rule
counts by position — a defect in shipped behavior, measured as bare-bullet
files in this repo's own history (M13–M16, M60–M62, M69, M71, M78, M79, M82,
M85, M89, M91 at creation) and label forms varying since (`AC1:`, `AC1.`,
`AC1 —`, `AC-1`, `**T1** —`).

**Out:** a validator advisory on missing or misnumbered labels — declined at
the plan gate (checker-regress shape, D-107); relabeling archived or live
milestone files in any repo — none of this repo's live files lack labels and
history is never rewritten; a change to `cairn_validate`'s positional counting
(M107), which the label prefix leaves untouched.

## Acceptance criteria

- [ ] AC1: `skills/shared/templates/milestone.md`'s Acceptance criteria and
      Tasks sections each show every example checkbox item opening with its
      positional label — `- [ ] AC1:`, `- [ ] AC2:` and `- [ ] T1:` — and each
      section's comment states the rule: the label is the item's position
      counted top-to-bottom, the number Coverage cites; the binding-criterion
      ingest form reads `- [ ] ACn (BCm): <verbatim>` at its five sites — the
      template comment, `skills/milestone-brief/SKILL.md`, the docstring of
      `scripts/tests/test_bc_ac_ingest_form.py`, and the two assertions in
      `skills/tests/test_finding_enforcement.py` — so
      `git grep -n "AC-N" -- skills scripts` returns no match.
- [ ] AC2: `skills/milestone-plan/SKILL.md` step 4 states that every criterion
      and task bullet opens with its positional label (`ACn:` / `Tn:`), that
      the label equals the item's position counted top-to-bottom, and that any
      insertion, removal, or reorder renumbers the labels and the Coverage
      lines together; `skills/milestone-implement/SKILL.md` step 6 states the
      same renumbering obligation on both of its branches — a minor edit and a
      gated amendment — for a change that adds, removes, or reorders a
      criterion or task.
- [ ] AC3: The active profile's `verify` slot is clean from the repo root
      (`cairn/PROFILE.md`: the two gating `python3 -m unittest` suites over
      `scripts/tests` and `hooks/tests`).

## Coverage

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T4

## Tasks

- [x] T1: Author the prose guard `skills/tests/test_positional_labels.py`
      red-first: it pins the template's labeled example items and both section
      comments, the plan step-4 rule, and the implement step-6 obligation on
      both branches; register one mutation entry per pinned block in
      `skills/tests/test_mutation_harness.py`'s `REGISTRY` (a new sentence near
      a pinned slice must not echo its start marker — LESSONS M148).
- [x] T2: Edit `skills/shared/templates/milestone.md`: label the example
      items in the Acceptance criteria and Tasks sections, add the position
      rule to each section's comment, and change the ingest form to
      `ACn (BCm):`; make the same form change in `skills/milestone-brief/SKILL.md`
      (line 88), the docstring of `scripts/tests/test_bc_ac_ingest_form.py`,
      and `skills/tests/test_finding_enforcement.py` (lines 41, 78); confirm
      with `git grep -n "AC-N" -- skills scripts`.
- [ ] T3: Edit `skills/milestone-plan/SKILL.md` step 4 (the Coverage-map
      bullet, lines 251–258) to add the labeling and renumbering rule, and
      `skills/milestone-implement/SKILL.md` step 6 (lines 79–92) to state the
      renumbering obligation on the minor and the substantive branch.
- [ ] T4: Run both gating suites and the hand-run `skills/tests` suite from
      the repo root, each exit code checked explicitly (LESSONS M56+M65);
      fix any red.

## Work log

- 2026-09-02: created by /milestone-plan.
- 2026-09-02: criteria audit ran in full mode ([O] fresh reader): F1 — AC1's grep clause covered two unnamed sites in `test_finding_enforcement.py`; fixed by enumerating all five. F2 — AC2 bound renumbering to gated amendments while implement step 6 treats a reorder as minor; posed at the gate, resolved as both branches. F3 — AC3 promised suite exit codes (an instrument property); narrowed to the verify slot, the skills/tests hand-run moved to T4. Repaired wording re-audited: no findings on AC1–AC3 (reader noted the two test assertions must change in the same commit as the template, folded into T2).
- 2026-09-02: plan gate chose a template-and-prose fix over a `criteria labels` validator advisory because the checker-regress shape recommends against extending a checker over tracking files (D-107) and no mislabel has yet reached a review; falsified by a milestone file whose label number differs from its position reaching `/milestone-review` in a tracked repo.
- 2026-09-02: plan gate chose renumbering on both implement step-6 branches over the gated branch alone because a minor reorder is the likeliest desync path; falsified by the both-branch rule being logged as a user override or deviation in a work log.
- 2026-09-02: plan gate chose the colon form `ACn:` / `Tn:` over any-separator labels because it is the form this repo's files have used since M130 and the binding tag fits as `ACn (BCm):`; falsified by an adopting repo's tooling requiring a different separator.
- 2026-09-02: started by /milestone-implement on branch m169-positional-labels; question gate skipped (the plan gate settled the label form, the both-branch renumbering, and the no-validator choice). T1: `skills/tests/test_positional_labels.py` authored red-first (12 tests, 12 failures against the unedited files); 13 mutation entries registered, one per pinned block.
- 2026-09-02: T2: template example items labeled `AC1:`/`AC2:`/`T1:`, position rule added to both section comments, ingest form changed to `ACn (BCm):` at all five sites; `git grep -n "AC-N" -- skills scripts` returns nothing (exit 1).

## Decisions

## Review
