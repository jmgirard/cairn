<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M262: A rerun of /hotfix on an open PR resumes the merge

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — `/hotfix` conduct that plugin users run   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m262-hotfix-open-pr-resume   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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
PR stopped before its chip, or a marker lost), a `CLOSED` unmerged PR the
marker names, and a guest PR whose maintainers requested changes keep
today's path; all three stay in the "`/hotfix` has no resume route for an
open PR" candidate row, narrowed to them at this milestone's post-merge
hygiene. `/milestone` §2's "Open hotfix PRs" bullet keeps naming no next
command. The follow-up PR's lost
merged-PR number stays in "Hotfix row-graduation edges (M249 review)". A
pane Button on a hotfix line becomes a new candidate row, "Pane hotfix line
Button".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: In owner mode, `/hotfix` step 6 states that on approval of an
      authored fix the PR is opened, then the marker is written as
      `hotfix <slug> approved YYYY-MM-DD for PR #<N> at <headRefOid>`, and
      only then does the CI wait run.
- [ ] AC2: In owner mode, `/hotfix` step 1 states an open-PR re-entry. Its
      trigger: `gh pr view <N> --json state,headRefName,headRefOid` reports
      `OPEN` and a head branch not matching `m<nnn>-*`, and
      `cairn/.merge-approved` starts with `hotfix ` and names that PR
      (`for PR #<N>`). The run quotes the marker's line in chat, still makes
      step 1's candidate-row match, and skips the tier check and steps 2 to
      5. When the marker's head oid equals the PR's `headRefOid`, it also
      skips the Copilot round arm, the PR-conversation read, the approval
      chip, and the marker write, and goes on at step 6's CI wait, the
      merge, and step 7. When the two differ, or the marker has no head oid,
      it says so and re-poses step 6's gate on the PR as it stands. A
      resumed merge's step 7 edits only the rows the PR body's
      `Candidate row:` lines name and closes only the issue its `Fixes #N`
      line names; it names in chat, and leaves alone, any other row the
      rerun's match finds. An `OPEN` PR outside this trigger keeps step 1's
      existing path.
- [ ] AC3: In guest mode, step 1 states that a PR-reference argument whose
      `gh pr view <N> --repo <base-repo> --json
      state,headRefName,reviewDecision` reports `OPEN` and a head branch
      starting `hotfix-` takes no tier check and none of steps 2 to 7. The
      run reports the PR's number, state, and review decision, and stops
      with a close block whose CI line says the maintainers' CI on the PR is
      the check that counts and whose fenced next command is `/hotfix` with
      the PR reference.
- [ ] AC4: Step 6's CI-wait timeout close names step 1's open-PR
      re-entry as the route its rerun takes while the PR is still open and
      the marker names it, and the merged-PR re-entry for a PR merged since.
- [ ] AC5: README.md's pane paragraph and the hotfix comment in
      `hooks/status/pane.ts` give no reason that an open-PR resume makes
      false; `git grep -n -i "resumes an open hotfix"` outside `cairn/`
      returns no match; and CHANGELOG.md's Unreleased section has one entry
      describing the open-PR resume for owner and guest mode.
- [ ] AC6: The active profile's `verify` slot is green (both gating
      suites, both `claude plugin validate` runs, `claude plugin test .`),
      and the hand-run `skills/tests` suite is green.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2, T3
- AC2 → T1, T3
- AC3 → T1, T3
- AC4 → T2
- AC5 → T4
- AC6 → T3, T5

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
