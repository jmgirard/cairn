# M235: `/cairn-triage` runs in guest mode and writes its edits to disk

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/cairn-triage` does for adopters in guest-mode repos   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m235-guest-triage   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In a guest-mode repo, `/cairn-triage` runs its whole pass over the local `cairn/` files and ends with the accepted edits on disk, never committed or pushed.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a guest arm in `skills/cairn-triage/SKILL.md` (session start, steps 5–7, the frontmatter description). The milestone also edits the tracking-rules "Collaboration mode" bullet, README.md's guest-mode section and its `/cairn-triage` table row, and the CHANGELOG. It adds a D-entry that annotates D-137 and prose guards in `skills/tests/`.

**Out:** `/cairn-release` keeps its guest stop, because a release is the maintainers' act (rulebook guest bullet, unchanged). The other guest edges stay in their candidate rows ("Intake and guest edges (M234 review)", "Issue look-in edges (M232 review)").

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: `skills/cairn-triage/SKILL.md`'s session start no longer stops in guest mode, and the old stop sentence (`stopped before enumeration: guest collaboration mode`) is absent from the file. In its place a guest arm states that the pass skips the clean-tree, default-branch, and sync preconditions (it moves no ref and commits nothing), runs steps 1–4 as written, and runs step 5 with the stamp standing in for the commit message.
- [ ] AC2: The skill's step 6 guest arm runs `cairn_validate.py` and replaces the `_Last hygiene check:` stamp as in owner mode, makes no commit and no push, and has the stamp name each refuted-premise or already-shipped drop with the record or path that holds its evidence. Step 7's guest close block reports the edits as written to disk and uncommitted in place of a commit hash, and its safety line says the same. The skill's frontmatter description and README.md's `/cairn-triage` table row name the guest arm's no-commit ending.
- [ ] AC3: The tracking-rules "Collaboration mode" section names `/cairn-release` alone as stopping in guest mode and states the triage guest arm, and README.md's guest-mode section says the same. No sentence containing a line that `grep -rniE 'triage' skills/ hooks/ scripts/ README.md` lists states that `/cairn-triage` stops in guest mode.
- [ ] AC4: The two guest-arm behaviors of AC1 and AC2 (the pass runs in guest mode with the old stop sentence gone, and the guest pass makes no commit or push) each have a prose guard in `skills/tests/` that fails when its sentence is blanked and passes on the branch.
- [ ] AC5: `CHANGELOG.md`'s `## Unreleased` section has an entry stating that `/cairn-triage` runs in guest mode with its edits written to `cairn/` on disk and not committed.
- [ ] AC6: The active profile's `verify` slot (`cairn/PROFILE.md`) is green on the branch.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2, T3
- AC3 → T3
- AC4 → T1, T5
- AC5 → T4
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Tests first: add `skills/tests/test_guest_triage.py` with one guard per AC4 behavior. Guard 1 reads the guest arm's run-in-guest-mode sentence and the absence of the old stop sentence. Guard 2 reads the guest arm's no-commit-no-push sentence. Register both in `REGISTRY` in `skills/tests/test_mutation_harness.py`, and see them fail on main's skill text.
- [ ] T2: Edit `skills/cairn-triage/SKILL.md`. Replace the guest stop (lines 29–33) with the guest arm. Give step 5's commit-message references and its D-entry preview ("the turn that commits it") a guest reading. Update the frontmatter description.
- [ ] T3: Edit step 6 with the guest arm: validate, a stamp that names each refuted-premise or already-shipped drop with its evidence record, no commit, no push. Step 4's byte-budget check counts the guest stamp's length, because the stamp is longer there. Edit step 7's status line and safety line. Edit tracking-rules lines 325–326, README.md's guest bullet (lines 735–737), and its `/cairn-triage` table row (line 510). Run the AC3 grep and read each listed line's sentence.
- [ ] T4: Add the CHANGELOG `## Unreleased` entry. Append D-156 to `cairn/DECISIONS.md`, annotating D-137: triage runs in guest mode with its edits on disk, the git preconditions are skipped, and the stamp carries the drop evidence.
- [ ] T5: Run the `verify` slot and the hand-run `skills/tests` suite (`python3 -m unittest discover -s skills/tests`), including `test_mutation_harness.py`'s registry completeness check.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: collision sweep: no candidate row, planned milestone, or D-entry rejects guest triage. The stop came from M184's rulebook bullet (reason: the commit to the default branch), and D-137 does not name triage. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-10: criteria audit (full mode, fresh Opus reader): 5 findings, all fixed by narrowing. AC1: steps 1–4, plus step 5 with the stamp for the commit message. AC2: adds the safety line, the frontmatter description, and README's table row. AC3: drops the nonexistent `templates/` path and judges sentences, not lines. AC4: asserts the old stop sentence is absent, and its harness registration moved to T1. AC4 stays a test-coverage criterion per "What gets a test". Note taken into T3: the guest stamp is longer, so step 4's byte check counts it.
- 2026-10-10: question set: git preconditions in guest mode — skip all three (clean tree, default branch, sync).
- 2026-10-10: question set: where a refuted-premise or already-shipped drop's evidence lives with no commit — in the stamp line.
- 2026-10-10: plan gate chose skipping all guest git preconditions over keeping the clean-tree check because the guest pass commits nothing and `cairn/` is the same folder on every branch; falsified by a guest pass that writes outside `cairn/`.
- 2026-10-10: plan gate chose the stamp line over chat-only for drop evidence because chat is lost at session end; falsified by a guest stamp that pushes ROADMAP over its byte budget in a real pass.
- 2026-10-10: approach: D-156 annotates D-137 rather than superseding it, because D-137 never named triage and its write rule stands.
- 2026-10-10: implement started on m235-guest-triage. Unrelated untracked `cairn-probe.log` and `tsconfig.json` left unstaged.
- 2026-10-10: T1: `skills/tests/test_guest_triage.py` (5 tests, 2 classes) and 4 REGISTRY entries added. All 5 fail on main's skill text as assertion failures on the pinned phrases (the old stop sentence still present).

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->
