# M235: `/cairn-triage` runs in guest mode and writes its edits to disk

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/cairn-triage` does for adopters in guest-mode repos   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m235-guest-triage, https://github.com/jmgirard/cairn/pull/244   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [x] AC1: `skills/cairn-triage/SKILL.md`'s session start no longer stops in guest mode, and the old stop sentence (`stopped before enumeration: guest collaboration mode`) is absent from the file. In its place a guest arm states that the pass skips the clean-tree, default-branch, and sync preconditions (it moves no ref and commits nothing), runs steps 1–4 as written, and runs step 5 with the stamp standing in for the commit message.
- [x] AC2: The skill's step 6 guest arm runs `cairn_validate.py` and replaces the `_Last hygiene check:` stamp as in owner mode, makes no commit and no push, and has the stamp name each refuted-premise or already-shipped drop with the record or path that holds its evidence. Step 7's guest close block reports the edits as written to disk and uncommitted in place of a commit hash, and its safety line says the same. The skill's frontmatter description and README.md's `/cairn-triage` table row name the guest arm's no-commit ending.
- [x] AC3: The tracking-rules "Collaboration mode" section names `/cairn-release` alone as stopping in guest mode and states the triage guest arm, and README.md's guest-mode section says the same. No sentence containing a line that `grep -rniE 'triage' skills/ hooks/ scripts/ README.md` lists states that `/cairn-triage` stops in guest mode.
- [x] AC4: The two guest-arm behaviors of AC1 and AC2 (the pass runs in guest mode with the old stop sentence gone, and the guest pass makes no commit or push) each have a prose guard in `skills/tests/` that fails when its sentence is blanked and passes on the branch.
- [x] AC5: `CHANGELOG.md`'s `## Unreleased` section has an entry stating that `/cairn-triage` runs in guest mode with its edits written to `cairn/` on disk and not committed.
- [x] AC6: The active profile's `verify` slot (`cairn/PROFILE.md`) is green on the branch.

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
- [x] T2: Edit `skills/cairn-triage/SKILL.md`. Replace the guest stop (lines 29–33) with the guest arm. Give step 5's commit-message references and its D-entry preview ("the turn that commits it") a guest reading. Update the frontmatter description.
- [x] T3: Edit step 6 with the guest arm: validate, a stamp that names each refuted-premise or already-shipped drop with its evidence record, no commit, no push. Step 4's byte-budget check counts the guest stamp's length, because the stamp is longer there. Edit step 7's status line and safety line. Edit tracking-rules lines 325–326, README.md's guest bullet (lines 735–737), and its `/cairn-triage` table row (line 510). Run the AC3 grep and read each listed line's sentence.
- [x] T4: Add the CHANGELOG `## Unreleased` entry. Append D-156 to `cairn/DECISIONS.md`, annotating D-137: triage runs in guest mode with its edits on disk, the git preconditions are skipped, and the stamp carries the drop evidence.
- [x] T5: Run the `verify` slot and the hand-run `skills/tests` suite (`python3 -m unittest discover -s skills/tests`), including `test_mutation_harness.py`'s registry completeness check.

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
- 2026-10-10: T2: triage skill's guest stop replaced by the guest arm ("Guest mode runs on disk"), owner preconditions labeled owner-mode, step 5's commit-message and D-entry-preview clauses given guest readings, frontmatter description names the no-commit ending. Implementation choice: the guest arm also names step 4 among the steps with guest arms, because the byte check counts the longer guest stamp there.
- 2026-10-10: T3: step 4 counts the guest stamp, step 6 guest arm (stamp names each drop's evidence, no commit, no push), step 7 status and safety lines. Rulebook guest bullet split (`/cairn-release` stops, `/cairn-triage` runs on disk). README guest bullet split in two and the table row amended. AC3 grep: 118 lines, none states a guest triage stop. `test_guest_triage` 5/5 OK.
- 2026-10-10: T4: CHANGELOG Unreleased entry added. D-156 appended, annotating D-137.
- 2026-10-10: T5: verify green: scripts 406 OK (21 skipped), hooks 174 OK, plugin and marketplace validate exit 0, `claude plugin test .` 1777 pass. Hand-run `skills/tests` 724 OK, registry completeness included. `cairn_validate` all checks passed.
- 2026-10-10: claim audit: 26 claims read, 4 corrected — skills/cairn-triage/SKILL.md (exclude-file claim now names the commit guard; steps 1–4 sentence no longer contradicts step 4; step 2 path checks read the checked-out branch, named above the step-3 table), README.md (sync check added). Re-read once by the same reader: all 4 true.
- 2026-10-10: implementation choice: the branch-naming rule for guest path checks lands in step 3's table bullet as well as session start, at the claim reader's re-read note. No guard pins it (AC4 names two behaviors only).
- 2026-10-10: implement complete, status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

Copilot round: PR #244 opened at review start, state query `none`, Copilot requested (exit 0).

- AC1 evidence: `grep -c` of the old stop sentence in `skills/cairn-triage/SKILL.md` = 0. Session start (lines 29–38) holds the "Guest mode runs on disk" arm: skips clean-tree, default-branch, and sync preconditions ("it moves no ref and commits nothing"), runs steps 1–4 as written and step 5 with the stamp standing in for the commit message. `test_guest_triage` green.
- AC2 evidence: step 6 guest arm (`**Guest arm**` at ~line 287) validates and stamps "as above", the stamp names each refuted-premise or already-shipped drop's evidence record, "The guest pass makes no commit and no push". Step 7: status line `written to disk, not committed (guest mode)` in place of the hash, safety line "in guest mode its edits are on disk in `cairn/` and uncommitted". Frontmatter description and README.md:510 row both say "on disk with no commit".
- AC3 evidence: tracking-rules.md:325–328 names `/cairn-release` alone as stopping and states the `/cairn-triage` arm. README.md:735–741 says the same. Sweep `grep -rniE 'triage' skills/ hooks/ scripts/ README.md` = 118 lines (41 outside `skills/tests/`); each sentence read, none states triage stops in guest mode (the two `assertNotIn` lines in the guard quote the old text to forbid it).
- AC4 evidence: `test_guest_triage` 5/5 OK on the branch (7/7 after the review fixes). Blanking each registered block fails its guard (`mutation_engine.guard_fails_when_blanked` True for all 4 entries, 8 after fixes). The old-stop absence guard failed on main's text at T1 (work log).
- AC5 evidence: CHANGELOG.md lines 7–13, first `## Unreleased` entry: "`/cairn-triage` runs in guest mode", edits "written to `cairn/` on disk and not committed or pushed".
- AC6 evidence: verify on fc63360: scripts 406 OK (21 skipped), hooks 174 OK, plugin validate 0, marketplace validate 0, `claude plugin test .` 1777 pass 0 fail.
- Consistency gate: `cairn_validate.py` all checks passed (exit 0). No principle changed, `cairn_impact` skipped. Profile consistency-gate checks are the verify slot (AC6).
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: guest drop evidence lasts only until the next stamp replaces it — follow-up (new candidate row "Guest triage drop evidence outlives one stamp"); D-156 and the rulebook bullet now state the limit.
- diff-bug #2: longer guest stamp conflicts with the rulebook's "one short line" — fix now, fixed 9507b51 (rulebook guest bullet names the exception).
- diff-bug #3: "already shipped" can be judged against the operator's unmerged branch — fix now, fixed 9507b51 (step 2 reads `<base>/<default-branch>` with `git cat-file -e`; a shipped drop names a commit reachable from it).
- diff-bug #4: skipped sync leaves step 2 judging stale code — fix now, fixed 9507b51 (same fix as #3, the ref is named above the step-3 table as last fetched).
- diff-bug #5: step 6's commit sentence is unscoped before the guest arm — fix now, fixed 9507b51 ("In owner mode, make one docs-only commit").
- diff-bug #6: "steps 1–4 as written" loose given step 2–4 guest clauses — reject (false: the arm names those clauses in the next sentence, and "as written" includes them).
- diff-bug #7: registered mutation only blanks the label — fix now, fixed 9507b51 (two more entries on the behavior phrases).
- diff-bug #8: negative asserts have no registry entry — reject (false as a gap: blanking cannot exercise `assertNotIn`; the old-stop guard was shown red on main at T1).
- diff-bug #9: README "runs as usual, but" is loose — reject (style).
- diff-bug #10: rulebook "skips its git preconditions" vaguer than other surfaces — reject (style; the bullet points at the skill, which names all three).
- blame-history #1: skipping sync reads stale upstream, M173 sync rationale unaddressed — fix now, fixed 9507b51 (same fix as diff-bug #3; D-156 now states the sync rationale and its guest replacement).
- blame-history #2: D-156 leaves the default-branch rationale implicit — fix now, fixed 9507b51 (D-156 decision names it).
- blame-history #3: stamp is the only audit trail for guest drops — follow-up (same row as diff-bug #1).
- blame-history #4: reverses M184's stop — reject (planned change; D-156 records the reason).
- blame-history #5: "same untracked folder on every branch" too broad across worktrees — fix now, fixed 9507b51 ("on every branch of the checkout").
- blame-history #6: no prior guard asserted the stop — noted, no defect.
- blame-history #7: overlong owner-precondition line — reject (style).
- prior-review #1: README edits unguarded (M234 put README in the guard domain) — fix now, fixed 9507b51 (`test_readme_states_the_guest_arm` plus a registry entry).
- prior-review #2: `test_old_stop_sentence_is_gone` has no mutation entry — reject (same ground as diff-bug #8).
- Post-fix verify on 9507b51: scripts OK (21 skipped), hooks OK, plugin and marketplace validate 0, `claude plugin test .` 1777 pass 0 fail, `cairn_validate` all passed, hand-run `skills/tests` OK.
- Return floor: no finding shows a criterion failing. Diff-bug #3 is a real defect in what the skill does; judged not load-bearing for a floor return because every drop passes the user's gate, so it is fixed on the branch with no status change.
