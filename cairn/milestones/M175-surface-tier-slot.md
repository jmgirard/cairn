# M175: The surface tier is a milestone header slot

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the milestone template and the plan and review skills ship to every adopting repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it (this milestone's own deliverable, written by hand ahead of the template) -->
- **Branch/PR:** m175-surface-tier-slot   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A milestone's surface tier and its one-clause reason are recorded in a `Surface tier:` header slot of the milestone file, which `/milestone-plan` fills and `/milestone-review` reads by name.

## Scope
<!-- owner: plan · create/amend-via-gate -->

Surface tier: user-facing — the template and the skill conduct around it ship
to adopting repos. Lineage: promotes the ROADMAP candidate row "Stakes-tier
follow-through" (M142 review finding D19: step 4 and the template carry no
tier-recording support); the row graduates at post-merge hygiene. D-108's
door is read as not reached: D-107 already mandates classifying and recording
the tier, and this milestone changes only where the record lands — confirmed
by the user at the plan gate on 2026-09-03.

**In:** a `- **Surface tier:**` header line in the milestone template, between
`Resolves:` and `Branch/PR:`, holding `user-facing | internal — <one-clause
reason>`; `/milestone-plan` step 2 names the slot as the recording place and
step 4 gains the matching header-slot bullet; `/milestone-review` step 5
reads the declared tier from the slot, its existing `no declared tier` arm
retained (a file lacking the slot takes that arm); the tracking-rules
section-ownership table lists `Surface tier` in the plan-owned header row;
the existing `skills/tests` pins on the step-2 wording are re-seeded.

**Out:** a `cairn_validate` check parsing the slot — refused at step 2 (work
log); a prose-form fallback when review finds no slot — rejected at the gate
(work log); re-tiering archived milestone files — history, untouched (IP4);
the archive-summary template — its Review line already names the tier
freeform; the amendment-time audit record line — stays its own candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `skills/shared/templates/milestone.md` carries a `- **Surface tier:**`
      header line between its `Resolves:` and `Branch/PR:` lines, whose trailing
      comment names `plan` as owner with write-mode `create; amend-via-gate`, the
      value form `user-facing | internal — <one-clause reason>`, and states that
      no validate check parses it. Evidence: `grep -n 'Resolves:\|Surface
      tier:\|Branch/PR:' skills/shared/templates/milestone.md` shows the three
      lines in that order.
- [ ] AC2: The surface-tier rule in `skills/milestone-plan/SKILL.md` step 2 names
      the `Surface tier:` header slot as where the tier and its one-clause reason
      are recorded, and step 4 carries a `**Surface tier** (header slot)` bullet
      among the header-slot bullets; step 5 of `skills/milestone-review/SKILL.md`
      names the `Surface tier:` header slot as where the declared tier is read
      and retains its existing `no declared tier` arm; the section-ownership
      table in `skills/shared/tracking-rules.md` lists `Surface tier` in the
      plan-owned header row. Evidence: `grep -n 'Surface tier\|no declared
      tier\|^[0-9]\. \*\*' skills/milestone-plan/SKILL.md
      skills/milestone-review/SKILL.md skills/shared/tracking-rules.md`, read in
      line order so each hit falls under its step header.
- [ ] AC3: Over every file `git ls-files -- skills README.md` lists, a
      case-insensitive search for the retired spelling `goal or scope` after
      collapsing each file's whitespace to single spaces returns no match (sites
      naming the new location are settled by AC2). Evidence: the search command
      and its empty output.
- [ ] AC4: The active profile's `verify` slot is clean — `python3 -m unittest
      discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests`
      each exit 0 — and the hand-run `python3 -m unittest discover -s
      skills/tests` exits 0. Evidence: each command's exit code.

## Coverage
<!-- owner: plan · create/amend-via-gate; review reads to fence evidence. -->

- AC1 → T1
- AC2 → T2, T3, T4
- AC3 → T2, T3, T5
- AC4 → T5, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits). -->

- [x] T1: Add the `- **Surface tier:**` header line to
      `skills/shared/templates/milestone.md` between `Resolves:` (line 12) and
      `Branch/PR:` (line 13), with the owner/write-mode/value-form comment and
      the "no validate check parses it" clause.
- [x] T2: `skills/milestone-plan/SKILL.md`: reword the step-2 surface-tier rule
      (lines 43–49) so the tier and reason are recorded in the `Surface tier:`
      header slot; add a `**Surface tier** (header slot)` bullet to step 4
      beside the Principles touched / Resolves / Driving RR bullets (lines
      265–290).
- [x] T3: `skills/milestone-review/SKILL.md` step 5 (lines 191–200): the declared
      tier is read from the `Surface tier:` header slot; keep the `no declared
      tier` arm verbatim.
- [x] T4: `skills/shared/tracking-rules.md:39`: add `Surface tier` to the
      plan-owned header row of the section-ownership table.
- [ ] T5: Re-seed `skills/tests/test_stakes_tier.py` (the pin at line 174 and
      `SURFACE_FIXTURE`) and `skills/tests/test_mutation_harness.py` (the block
      near line 1806) to the new step-2 wording, in the same commit as T2; run
      the AC3 sweep and record its empty output.
- [ ] T6: Run both gating suites and the hand-run `skills/tests` suite from the
      repo root; record each exit code in the work log.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-09-03: created by /milestone-plan.
- 2026-09-03: criteria audit ran in full mode ([O] fresh reader, user-facing tier): AC1 evidence grep widened to show the slot's position; AC2 evidence grep interleaves step headers and its slot-less-file clause narrowed to retention of the existing arm; AC3 kept with its promise stated as the retired spelling only; AC4 clean.
- 2026-09-03: step 2 chose no `cairn_validate` check over parsing the slot because a check widens the checker's promise (D-107's regress shape) for a value no script consumes; falsified by a milestone merging with the slot empty or misspelled past review.
- 2026-09-03: plan gate chose a slot holding tier and reason over tier-only with the reason in prose because one line then carries what D-107 requires; falsified by reason clauses that will not fit one line in practice.
- 2026-09-03: plan gate chose slot-only reading in review over a prose fallback because the legacy case fades within a milestone and the existing `no declared tier` arm defaults to full rigor; falsified by an adopting repo's internal-tier milestone paying for a three-lens fan-out it did not need.
- 2026-09-03: plan gate chose re-seeding the existing pins over adding a template-slot pin because the slot is skill conduct like `Resolves:`; falsified by the slot line leaving the template unnoticed.
- 2026-09-03: T1 — template gains the `Surface tier:` slot between `Resolves:` and `Branch/PR:`; verify green (scripts 0, hooks 0).
- 2026-09-03: T2 — plan step 2 records the tier in the `Surface tier:` header slot; step 4 gains the header-slot bullet; T5's pin, fixture, and mutation block re-seeded in this commit; stakes-tier guard 19/19, mutation harness 9/9, verify green.
- 2026-09-03: T3 — review step 5 reads the tier from the `Surface tier:` slot; `no declared tier` arm kept, glossed as a missing or `—` slot; verify green; hand-run skills/tests 602/604 — the two reds are the template/table parity guard T4 settles.
- 2026-09-03: T4 — `Surface tier` added to the plan-owned header row of the section-ownership table; verify green; hand-run skills/tests 604/604 (the parity guard now passes).

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion. -->
