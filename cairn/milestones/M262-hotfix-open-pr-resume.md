<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M262: A rerun of /hotfix on an open PR resumes the merge

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — `/hotfix` conduct that plugin users run   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m262-hotfix-open-pr-resume, https://github.com/jmgirard/cairn/pull/274   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A `/hotfix` rerun with the PR reference of a hotfix PR that is still open goes back to where the earlier run stopped, in place of starting the adopt-a-PR walk.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/hotfix` step 1 (`skills/hotfix/SKILL.md`) gains an open-PR
re-entry beside the merged-PR re-entry. Owner arm: an `OPEN` hotfix PR
that a `hotfix ` marker names at the PR's current head resumes at step 6's
CI wait and merge, then step 7; a head that moved re-poses the approval
chip. Step 6 states its order (PR open, marker with the head oid, then the
CI wait). Guest arm: an `OPEN` PR from a `hotfix-` branch is reported as
still with the maintainers, and the run stops. Step 6's timeout close
names the new route. README's pane paragraph and the `hooks/status/pane.ts`
comment drop the "no command resumes an open hotfix PR" reason, and
CHANGELOG.md gets an entry. `skills/tests/test_resume_routing.py` pins the
new route.

**Out:** an open owner PR that no `hotfix ` marker names (a Copilot-round
PR stopped before its chip, or a marker lost) and a `CLOSED` unmerged PR
the marker names keep today's path. A guest PR whose maintainers requested
changes is reported by the guest stop, with no route here to make the
changes. All three stay in the "`/hotfix` has no resume route for an
open PR" candidate row, narrowed to them at this milestone's post-merge
hygiene. `/milestone` §2's "Open hotfix PRs" bullet keeps naming no next
command. The follow-up PR's lost
merged-PR number stays in "Hotfix row-graduation edges (M249 review)". A
pane Button on a hotfix line becomes a new candidate row, "Pane hotfix line
Button".

## Acceptance criteria

- [x] AC1: In owner mode, `/hotfix` step 6 states that on approval of an
      authored fix the PR is opened, then the marker is written as
      `hotfix <slug> approved YYYY-MM-DD for PR #<N> at <headRefOid>`, and
      only then does the CI wait run.
- [ ] AC2: In owner mode, `/hotfix` step 1 states an open-PR re-entry. Its
      trigger: `gh pr view <N> --json state,headRefName,headRefOid,latestReviews`
      reports `OPEN` and a head branch not matching `m<nnn>-*`, and
      `cairn/.merge-approved` starts with `hotfix ` and names that PR
      (`for PR #<N>`). The run quotes the marker's line in chat and makes
      step 1's candidate-row match. When the marker's head oid equals the
      PR's `headRefOid`, no entry of `latestReviews` has the state
      `CHANGES_REQUESTED` (even one the user overrode at the earlier chip),
      and the match names exactly the rows that the PR body's
      `Candidate row:` lines name, the run skips the tier check, steps 2 to
      5, and step 6's Copilot round arm, PR-conversation read, approval
      chip, and marker write. It goes on at step 6's CI wait, merges with
      `--match-head-commit` set to that oid, and runs step 7 as it does
      after an approval at step 6's chip. A merge refused for a moved head
      stops with a close block that names the refusal and the PR's current
      head, its fenced next command `/hotfix` with the PR reference. When
      any of the three conditions fails, or the marker names no oid, the run
      says which in chat and takes step 1's existing path, where a decline
      at step 6's chip removes `cairn/.merge-approved`. An `OPEN` PR outside
      this trigger keeps step 1's existing path.
- [x] AC3: In guest mode, step 1 states that a PR-reference argument whose
      `gh pr view <N> --repo <base-repo> --json
      state,headRefName,reviewDecision` reports `OPEN` and a head branch
      starting `hotfix-` takes no tier check and none of steps 2 to 7. The
      run reports the PR's number, state, and review decision, and stops
      with a close block whose CI line says the maintainers' CI on the PR is
      the check that counts and whose fenced next command is `/hotfix` with
      the PR reference.
- [x] AC4: Step 6's CI-wait timeout close names step 1's open-PR
      re-entry as the route its rerun takes while the PR is still open and
      the marker names it, and the merged-PR re-entry for a PR merged since.
- [x] AC5: README.md's pane paragraph and the hotfix comment in
      `hooks/status/pane.ts` give no reason that an open-PR resume makes
      false; `git grep -n -i "resumes an open hotfix"` outside `cairn/`
      returns no match; and CHANGELOG.md's Unreleased section has one entry
      describing the open-PR resume for owner and guest mode.
- [x] AC6: The active profile's `verify` slot is green (both gating
      suites, both `claude plugin validate` runs, `claude plugin test .`),
      and the hand-run `skills/tests` suite is green.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2, T3, T7
- AC2 → T1, T3, T6
- AC3 → T1, T3, T7
- AC4 → T2, T7
- AC5 → T4
- AC6 → T3, T5, T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write the open-PR re-entry into `skills/hotfix/SKILL.md` step 1,
      after the merged-PR re-entry (ends near line 124): the owner arm
      (AC2) and the guest arm (AC3). Keep the session-start guest clause
      (line 26) true: every `gh pr` read carries `--repo <base-repo>`. Say
      that step 7's off-but-present Copilot rule (lines 369-373) applies to
      a resumed authored fix.
- [x] T2: In step 6 (lines 255-296), state the order of AC1 and the marker
      line with ` at <headRefOid>` (`_MARKER_PR` in `hooks/cairn_common.py`
      already reads past trailing text); reword the timeout close (lines
      273-284) per AC4; check that the guest handoff close (lines 319-324)
      still reads true against T1's guest arm.
- [x] T3: Add a test class to `skills/tests/test_resume_routing.py` that
      pins the owner arm's trigger and its two outcomes (same head: on at
      the wait; moved head: the gate re-posed), the guest arm's stop, and
      step 6's order, each passage whole with whitespace collapsed; register
      mutation entries in `skills/tests/test_mutation_harness.py` beside
      the existing `test_resume_routing` ones that vary each trigger part
      on its own (state, marker prefix, PR named, head oid) and each
      outcome, and see each one red. Hand-run
      `python3 -m unittest discover -s skills/tests`.
- [x] T4: Reword README.md line 434 and the `hooks/status/pane.ts:541-542`
      comment so neither gives a reason this milestone makes false, and add
      the CHANGELOG.md Unreleased entry.
- [x] T5: Run the `verify` slot from the repo root, checking each exit code.
- [ ] T6: Rewrite step 1's owner arm to the amended AC2 (three-condition
      resume, `--match-head-commit`, refused-merge close, fallback to the
      existing path, marker removed on a decline at step 6's chip), and
      update the guard pins and mutation entries to match.
- [ ] T7: Review pass 1 fix-now items: head pin on every owner merge
      (diff-bug #1); the gate's presented head recorded and compared at the
      marker write (diff-bug #9, with the AC1 re-audit's four points); step
      6's order sentence scoped to owner mode (#11); "read at most once per
      run" (#8); the timeout close and its CI-line clause (#14); a D-entry
      annotating D-130 (#12); guard pins for AC3's CI line and next command
      and AC4's merged half (#13); the CHANGELOG entry; `verify` and
      `skills/tests` green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: not run — work named at the question set.
- 2026-10-16: question set: which candidate to plan — "`/hotfix` has no resume route for an open PR"; scope — confirmed defects only; live look — tests only, no live look before the merge question.
- 2026-10-16: collision check: absorbs candidate row "`/hotfix` has no resume route for an open PR" (M183 review); related rows "Hotfix row-graduation edges (M249 review)" and "Live look at `/milestone`'s 'Open hotfix PRs' bullet" stay distinct; D-130 and D-131 read whole: they add the merged-PR route and leave the open-PR case unrouted, no standing rejection; no planned or in-progress milestone overlaps.
- 2026-10-16: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-16: lessons harvested: M112 (sweep README and CHANGELOG for the old wording, so T4), M148 (new prose near a pinned slice can break locators, so T3 hand-runs `skills/tests`), M165 (pin the trigger as well as the outcome, so T3).
- 2026-10-16: plan gate chose to resume on the marker's recorded approval with no chip when the marker's head oid equals the PR's head, over re-posing the approval chip every time as `/milestone-review` route (c) does, because step 6's timeout close already promises that a rerun re-derives the check state and waits, and the head oid binds the approval to the diff the user saw; falsified by a resumed merge whose merged diff differs from the one shown at the approval chip.
- 2026-10-16: plan gate chose to leave an open owner PR with no `hotfix ` marker on today's walk over a no-marker resume that re-poses the chip, because only the marker shows that steps 3 to 5 ran; falsified by a Copilot-round PR stopped before its chip being rerun in a real session.
- 2026-10-16: plan gate chose no D-entry: the route is `/hotfix`-local and works under IP1 (the merge rests on an approval given at a gate, bound to the PR and its head), and D-130's route (c) governs milestones only, so no RB tripwire tag.
- 2026-10-16: criteria audit (full mode, fresh Opus reader) returned 8 findings, all taken toward the narrower promise: step 6's marker-before-wait order made a criterion (new AC1); the marker records the head oid and a moved head re-poses the gate (AC2); the trigger requires a `hotfix ` marker and a non-`m<nnn>-*` head (AC2); resumed row edits and issue close come from the PR body's lines (AC2); a `CLOSED` PR named by the marker moved to Out; AC4 conditioned on the marker; AC5's grep widened and the `pane.ts` comment added (T4); the off-but-present rule for a resumed fix added to T1. Optional `/milestone` §2 next command declined (Out). AC3 and AC6 clean.
- 2026-10-16: new candidate row "Pane hotfix line Button" (search-first: no overlap in candidates, archive, or DECISIONS).
- 2026-10-16: branch m262-hotfix-open-pr-resume cut from main at b00d0270; untracked `cairn-probe.log` and `tsconfig.json` (not this milestone's) left unstaged.
- 2026-10-16: T1 done: step 1 gains the "Open-PR re-entry (M262)" paragraph with owner and guest arms. A moved head's gate shows the commits since the approved oid (`git log -p <oid>..FETCH_HEAD`), or `gh pr diff` when no oid or the oid is not an ancestor, because the chip's regression-test evidence was shown at the earlier approval. Step 1 names the marker as "step 6's merge-guard marker", not by path, so `test_external_pr_intake`'s one-mention pin (one approval mechanism) holds. The simple-english lint hook reports 169 hits for the whole file, all but 2 (one 26-word sentence, one trailing condition) in text this milestone does not change. Gating suites and `skills/tests` green.
- 2026-10-16: T2 done: step 6 states the order on approval (push and any create, marker, CI wait, merge) and the marker line `… for PR #<N> at <headRefOid>`, the oid read by `gh pr view <N> --json headRefOid` after the push; the timeout close names the open-PR re-entry (still open, marker names it) and the merged-PR re-entry. The guest handoff close ("whose step 1 re-derives the PR's state") reads true against T1's guest arm, unchanged. Suites green.
- 2026-10-16: T3 done: `TestHotfixOpenPrReentry` (9 tests) in `skills/tests/test_resume_routing.py` pins the step-1 route and step 6's order, marker line, and timeout close; 14 mutation entries (each trigger part and each outcome on its own) each turn the guard red when blanked, checked by `guard_fails_when_blanked` per entry; `skills/tests` 761 tests OK.
- 2026-10-16: T4 done: README's pane paragraph now says "A hotfix line has no Button." with no reason, the `hooks/status/pane.ts` comment drops its "No command resumes" sentence, and CHANGELOG.md's Unreleased Fixes section opens with the open-PR resume entry (owner and guest). A whitespace-collapsed sweep of 323 tracked files outside `cairn/` finds neither stale phrase (control phrase found).
- 2026-10-16: T5 done: verify slot green (scripts and hooks suites exit 0, both `claude plugin validate` exit 0, `claude plugin test .` 1777 pass 0 fail); `skills/tests` exit 0.
- 2026-10-16: claim audit: 28 claims read, 4 corrected — skills/hotfix/SKILL.md, CHANGELOG.md, skills/tests/test_resume_routing.py. (1) The PR-body row rule is scoped to a merge resumed with no chip, and an adopted PR's body has no `Candidate row:` line, so its resumed merge edits no row; after a re-posed chip, step 7 runs as for any approved merge (CHANGELOG narrowed to match). (2) The moved-head fetch is `git fetch origin pull/<N>/head`, so a fork PR works, with a failed fetch falling back to `gh pr diff`. (3) The timeout close names the re-asked approval when the head moved. (4) The head oid is read "after any push, just before the marker write". Suites green after the corrections.
- 2026-10-16: implement done; status `review`. Reading recorded for review: AC2's "a resumed merge" row rule is shipped for a merge resumed with no chip, since a moved head re-poses the gate and that chip names step 1's current matches.
- 2026-10-16: review pass 1: AC1, AC3–AC6 verified at 97d8a333; three lenses spawned; Copilot requested on PR #274 (pending).
- 2026-10-16: amendment routed: AC2 — the promise mandates an unsafe resume: a moved head re-poses the gate with steps 2 to 5 skipped, so no fresh regression-test or verify evidence (diff-bug #4, prior-review #1, #2); a same-head resume skips the changes-requested blocking rule (diff-bug #3, blame-history #2); the PR-body row clause drops rows the chip promised and contradicts step 7 (diff-bug #5, blame-history #3). Fix-now items for the same round: diff-bug #1, #2 (Scope Out), #7, #8, #9, #11, #12 (D-entry), #13, #14.
- 2026-10-16: re-audit: AC2 (full) — 5 findings on the first amended wording (moved head or changes requested → existing path; `--match-head-commit`; step 7 as for any approved merge): step 7 could edit rows the earlier chip never named (taken: the match must agree with the body's `Candidate row:` lines); "that run" ambiguous (taken); an earlier override still reads `CHANGES_REQUESTED` (taken, stated); late comments go unread (declined, follow-up); refused-merge outcome unstated (taken).
- 2026-10-16: re-audit: AC2 (full) — 4 findings on the fixed wording: override parenthetical ambiguous; the row check must be exact, both directions; the refused-merge close needs its object and next command; a declined chip on the fallback path leaves a marker that a later `gh pr merge` passes; plus AC1 should bind the marker's oid to the head the gate presented. Second re-audit on AC2: the repeated review-failure stop; the disposition goes to the user.
- 2026-10-16: stop answered: the user chose "Adopt the narrowed wording" (over "Always ask again on rerun" and "Stop here"); AC2 takes the second reader's fixes 1-4.
- 2026-10-16: amendment return: AC2 — "When the marker's head oid equals the PR's `headRefOid`, no entry of `latestReviews` has the state `CHANGES_REQUESTED` (even one the user overrode at the earlier chip), and the match names exactly the rows that the PR body's `Candidate row:` lines name, the run skips the tier check, steps 2 to 5, and step 6's Copilot round arm, PR-conversation read, approval chip, and marker write. It goes on at step 6's CI wait, merges with `--match-head-commit` set to that oid, and runs step 7 as it does after an approval at step 6's chip. A merge refused for a moved head stops with a close block that names the refusal and the PR's current head, its fenced next command `/hotfix` with the PR reference. When any of the three conditions fails, or the marker names no oid, the run says which in chat and takes step 1's existing path, where a decline at step 6's chip removes `cairn/.merge-approved`."
- 2026-10-16: re-audit: AC1 (full) — 4 findings on the proposed added sentence (presented head undefined for an unpushed authored fix; adopted PRs left out; re-presented gate's decline unstated); the sentence is withdrawn and AC1 stays as written, narrower; the check ships as fix-now diff-bug #9 under T7 with those four points.
- 2026-10-16: substantive amendment: Scope Out — a guest PR whose maintainers requested changes is reported by the guest stop (AC3 as written) rather than keeping today's path; fixing requested changes stays in the narrowed candidate row (diff-bug #2).
- 2026-10-16: tasks T6 (AC2 amendment) and T7 (fix-now items) added; Coverage updated.
- 2026-10-16: the amendment took the plan-owned body to 159 lines; the heaviest section (Acceptance criteria) shed its 10-line template comment in one rewrite, criterion text unchanged; 149 lines, `cairn_validate` green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->

Review head 97d8a333, PR #274 (opened at review start, Copilot arm). Evidence is a whitespace-collapsed substring read of `skills/hotfix/SKILL.md` step 1 (to `2. **Branch`) and step 6 (to `7. If`), run 2026-10-16.

- AC1: step 6 carries "On approval, the order is fixed: the push and any `gh pr create` above, then the merge-guard marker, then the CI wait, then the merge." and the marker line `hotfix <slug> approved YYYY-MM-DD for PR #<N> at <headRefOid>` — both found. `_MARKER_PR` (`hooks/cairn_common.py:184`) matches `for PR #<N>` with trailing text. PASS.
- AC3: step 1 guest arm found: trigger "This arm runs in guest mode, for an `OPEN` PR whose head branch starts with `hotfix-`", the read `gh pr view <N> --repo <base-repo> --json state,headRefName,reviewDecision`, "Skip the tier check and steps 2 to 7. Report the PR's number, state, and review decision", the CI line ("the maintainers' CI on the PR is the check that counts"), and the fenced `/hotfix` with the PR reference. PASS.
- AC4: step 6's timeout close found: "while the PR is still open and the marker names it, step 1's open-PR re-entry resumes at this wait (or asks for approval again when the head moved since the approval), and for a PR merged since, step 1's merged-PR re-entry verifies the merged diff post-hoc". PASS.
- AC5: `git grep -n -i "resumes an open hotfix" -- . ':!cairn/'` exit 1 (no match); README.md:434 reads "A hotfix line has no Button."; `hooks/status/pane.ts:541` ends the comment at "(M226)."; CHANGELOG.md:363, under `## Unreleased` → `### Fixes`, holds the one entry "A `/hotfix` rerun on an open hotfix PR finishes the merge you approved." covering owner and guest mode. PASS.
- AC6: scripts/tests 408 OK (21 skipped), hooks/tests 175 OK, `claude plugin validate` plugin and marketplace exit 0 (no `plugins[N].version` warning), `claude plugin test .` 1777 pass 0 fail, `skills/tests` 761 OK. PASS.
- Consistency gate: `cairn_validate.py` exit 0, all checks passed; no principle changed, so `cairn_impact` skipped; profile gate: verify green on the review head, no marketplace version warning, CHANGELOG entry present with no milestone number.
- AC2: every phrase found in step 1 (trigger, quote, skip of tier check and steps 2 to 5, same-head skip and CI wait, moved-head re-posed gate, PR-body row and issue rule, other open PRs on the walk). Not ticked: the review findings below show the criterion's own promise is unsafe, so it routes to an amendment return.
- spawned: diff-bug, blame-history, prior-review (pass 1).
- diff-bug #1: the head is checked once at step 1 and `gh pr merge` carries no `--match-head-commit`, so a push during the wait merges unapproved commits — fix now, in the AC2 amendment round (merge with `--match-head-commit <oid>`).
- diff-bug #2: the guest arm stops a `CHANGES_REQUESTED` PR while Scope Out says such a PR keeps today's path — fix now, in the amendment round (Scope Out reworded: the stop reports the decision; fixing requested changes stays in the narrowed candidate row).
- diff-bug #3: the same-head resume skips the PR-conversation read and its changes-requested blocking rule, so a later "request changes" is merged past — amendment return (AC2 mandates the skip).
- diff-bug #4: the moved-head gate has no fresh regression-test or `verify` evidence, against step 5's "Never merge a fix whose regression test is still missing" and the hotfix bar on every path (D-131) — amendment return (AC2 mandates skipping steps 2 to 5).
- diff-bug #5: a resumed adopted merge edits no row although the approval chip promised the row edits — amendment return (AC2's PR-body row clause).
- diff-bug #6: a resumed follow-up PR of the merged-PR re-entry may never close the merged PR's `Fixes #N` issue, which rode on the follow-up's chip — follow-up, new candidate row "Hotfix resume edges (M262 review)".
- diff-bug #7: the moved-head path's "skip the push" conflicts with step 6's create-skip clause — fix now, in the amendment round (moot once a moved head takes the walk).
- diff-bug #8: "the read runs at most once per hotfix" is false once a rerun reads again — fix now, in the amendment round (reworded per run).
- diff-bug #9: the head oid read before the marker write can bind commits pushed after the gate's diff was shown — fix now, in the amendment round (compare with the head the gate presented).
- diff-bug #10: the guest arm does not check who opened the `hotfix-` PR — follow-up, "Hotfix resume edges (M262 review)".
- diff-bug #11: step 6's order sentence is not scoped to owner mode — fix now, in the amendment round.
- diff-bug #12: no D-entry records the no-chip resume against D-130 route (c) — fix now, in the amendment round (D-entry annotating D-130).
- diff-bug #13: the guard leaves AC3's CI line and next command and AC4's merged half unpinned — fix now, in the amendment round.
- diff-bug #14: step 6's CI-line clause still says only "re-derives that state and waits again" — fix now, in the amendment round.
- blame-history #1: a resumed merge closes the issue from the PR body with no chip — reject, false as a new defect: step 7 already reads the body's `Fixes #N` after the CI wait on every path, and the marker shows that step 6's chip, which names that close, was approved.
- blame-history #2: same as diff-bug #3 — amendment return.
- blame-history #3: step 1's PR-body row rule contradicts step 7's "edit each row step 1 matched" — amendment return (with diff-bug #5).
- blame-history #4: same as diff-bug #2 — fix now, in the amendment round.
- blame-history #5: same as diff-bug #12 — fix now, in the amendment round.
- blame-history #6: the marker is fragile resume state (a server-side merge failure leaves it consumed; `/milestone-review` writes the same path) — follow-up, "Hotfix resume edges (M262 review)"; the fallback is today's walk, not an unsafe merge.
- blame-history #7: same as diff-bug #1 — fix now, in the amendment round.
- blame-history #8: unpushed local commits are invisible to the head check — reject, false as a defect: the merge takes the remote head the approval bound, and unpushed commits were never approved.
- blame-history #9: same as diff-bug #6, and the narrowing note's PR number is the Out item in "Hotfix row-graduation edges (M249 review)" — follow-up.
- blame-history #10: same as diff-bug #10 — follow-up.
- blame-history #11: the one-mechanism pin is met by wording — reject, planned change: step 1 reads the same marker step 6 writes, no second mechanism.
- blame-history #12: README line 434 rewraps short — reject, style.
- blame-history #13: mutation blocks embed physical wraps — reject, planned change: the M172 entries use the same convention, and the harness hard-errors on a missing block, so a reflow fails loud.
- prior-review #1: the moved-head gate does not re-run the hotfix bar (M172 F1, D-131) — amendment return (with diff-bug #4).
- prior-review #2: an old-format marker with no oid takes the same path — amendment return (with diff-bug #4).
- prior-review #3: the row match runs before each stop (PR #259) — noted, clean.
- prior-review #4: no stale "no command resumes" text; tracking-rules:285 shows the milestone marker without an oid — reject, false: that line is `/milestone-review`'s marker, which this milestone does not change.
- prior-review #5: same as blame-history #8 — reject.
- prior-review #6: mutation entries per assertion (PRs #242, #243, #260) — noted, clean.
