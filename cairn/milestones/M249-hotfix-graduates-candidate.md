<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M249: A hotfix removes the candidate row it fixes, once the fix merges

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1, GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/hotfix` does to an adopter's ROADMAP   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m249-hotfix-graduates-candidate, https://github.com/jmgirard/cairn/pull/259   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When a hotfix fixes the bug that a ROADMAP candidate row describes, the hotfix removes that row, or narrows it to the part left, once the fix merges.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `skills/hotfix/SKILL.md` steps 1, 6 and 7 and its guest arm: the hotfix
finds the candidate rows it fixes, names them at the approval chip, and
removes or narrows them after the merge. In owner mode the edit is a
docs-only commit on the default branch. In guest mode it is an edit on disk
when a later `/hotfix` run sees the maintainers' merge. One sentence in
`skills/shared/records-hygiene.md` §1 and README.md's `/hotfix` row. A
hand-run prose guard in `skills/tests/`.

**Out:** Milestone graduation does not change: a milestone's row still goes
at post-merge hygiene (records-hygiene §1). A resume route for an open
hotfix PR stays in the candidate row "`/hotfix` has no resume route for an
open PR". `/milestone` routing and the pane's ✎ press pass no new argument,
because step 1's match reads the Candidates section on every entry.

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

- [x] AC1: `skills/hotfix/SKILL.md` step 1 says how the hotfix finds the
      candidate rows it fixes. A matched row is a row whose title the
      argument quotes, or a row in `cairn/ROADMAP.md`'s Candidates section
      that describes the bug. For a PR-reference argument the hotfix reads
      the PR's title, body and `Fixes #N` line against the rows. The match
      runs again on every entry to step 1, PR-reference re-entries
      included, and is never taken from memory. The hotfix names each
      matched row's title in chat, or says that no row matched.
- [x] AC2: Two chips name each matched row's title in their question text
      and say whether the merge removes the row or narrows it: step 6's
      owner-mode approval chip, and step 1's "Nothing owed" acceptance chip
      on the merged-PR re-entry.
- [x] AC3: `skills/hotfix/SKILL.md` step 7 says what happens to the matched
      rows in owner mode after a merge whose diff passed the hotfix bar.
      This covers an authored fix, an adopted PR, a re-landed PR, and the
      merged-PR re-entry once its post-hoc verification is accepted. The
      hotfix deletes each row that the fix covers in full. It narrows each
      row that the fix covers in part, with a `narrowed YYYY-MM-DD by the
      PR #N hotfix` note, where `#N` is the PR that merged. Every ROADMAP
      edit that step 7 makes, its own new candidate row included, lands in
      one docs-only commit on the up-to-date default branch, pushed at once.
      The narrowed and new rows are shown verbatim in chat.
- [x] AC4: `skills/hotfix/SKILL.md` says that only step 7, after a merge,
      removes or narrows a matched row, and that step 7 on step 1's
      over-the-bar disposition neither removes nor narrows it.
- [x] AC5: `skills/hotfix/SKILL.md`'s guest arm says that the handoff
      leaves each matched row unchanged. When the merged-PR re-entry finds
      that the maintainers merged the PR, and its post-hoc verification is
      accepted, step 7 removes or narrows each row on disk, with no commit,
      judged against the merged diff. A PR closed without a merge leaves the
      row.
- [x] AC6: `skills/shared/records-hygiene.md` §1 says that a hotfix
      graduates the row it fixes at its step 7, after the merge, as the
      hotfix case of graduation at completion. The `/hotfix` row of
      README.md's commands table says that the hotfix removes or narrows the
      candidate row it fixes after the merge.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T5
- AC2 → T2, T5
- AC3 → T3, T5
- AC4 → T3, T5
- AC5 → T3, T5
- AC6 → T4, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Step 1 (`skills/hotfix/SKILL.md:33-45`): add the match clause
      after the ROADMAP read, with the PR-reference reading and the
      re-derive-on-every-entry rule. Trace the merged-PR re-entry
      (`:46-109`) so its path reaches the match (lesson M172).
- [x] T2: Step 6's approval chip (`:224-234`) and the "Nothing owed" chip
      (`:98-105`): add the row-title clause. The guest handoff chip carries
      no row text.
- [x] T3: Step 7 (`:299-307`): add the remove-or-narrow clause, the
      single docs-only commit for every ROADMAP edit step 7 makes, the
      verbatim preview, the over-the-bar exception, and the only-step-7
      rule. Add the guest sentences to the step 6 guest arm (`:269-297`) and
      step 7.
- [x] T4: Add the sentence to `skills/shared/records-hygiene.md` §1 and
      keep the module under its 55-line, 4,000-byte budget (`wc -l -c`).
      Edit README.md's `/hotfix` row (`:549`). Sweep
      `git grep -n -i candidate -- README.md skills/` for prose that says a
      hotfix leaves a row it fixes, and fix each hit (lesson M112).
- [x] T5: Add a hand-run prose guard in `skills/tests/` that pins the
      clauses of T1-T4, and show each pin red by deleting its clause. Run
      the whole `skills/tests` suite (lesson M148), both gating suites, and
      `cairn_validate`.
- [x] T6: Add a `CHANGELOG.md` Unreleased entry for the change (review
      return 1).
- [x] T7: Fix review return 2 and the pass-1 fix-now items: the
      "Nothing owed" chip names rows in both modes, deleted rows are shown,
      the one-commit rule covers every step-7 ROADMAP edit with a
      `git status` check first, "within a hotfix", the narrowing replaces a
      second row, records-hygiene §1 restored, CHANGELOG guest wording; guard
      re-pinned.

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

- 2026-10-12: created by /milestone-plan from the user's request that a hotfix remove the candidate row it fixes.
- 2026-10-12: collision sweep: no candidate, planned, or in-progress overlap; the rows on hotfix resume, the companion arm, hotfix questions, and issue look-in edges are distinct; the PR #238 hotfix narrowed a row by hand (edccd564); no D-entry rejects this; checker-regress shape not hit.
- 2026-10-12: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-12: lessons harvested: M112 (sweep the whole doc surface), M148 (prose-guard markers), M154 (rows graduate at completion), M172 (trace each re-entry path).
- 2026-10-12: criteria audit (full mode, fresh Opus reader): 9 findings, all fixed by narrowing: no row ids, so match by quoted title or description; match re-derived on re-entry; AC2 names the nothing-owed chip; one commit for every step-7 ROADMAP edit; `#N` is the merged PR; "unchanged" became "neither removed nor narrowed"; the path list became an only-step-7 rule; guest edit tied to accepted verification and the merged diff; §1 sentence placed as the hotfix case.
- 2026-10-12: question set: owner-mode timing — after the merge, a docs-only commit on main; guest-mode timing — when a later /hotfix run sees the maintainers' merge.
- 2026-10-12: plan gate chose a post-merge docs-only commit over a row deletion inside the PR's diff because an adopted PR would carry a tracking edit pushed to the contributor's branch and an unpushable branch needs the post-merge commit anyway; falsified by hotfix runs that merge and leave the row because the step-7 commit was skipped.
- 2026-10-12: plan gate chose guest removal at the merged re-entry over removal at handoff because a PR closed unmerged would lose the row's idea; falsified by guest operators who never rerun /hotfix after a merge, leaving fixed rows in place.
- 2026-10-12: implement started on m249-hotfix-graduates-candidate; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-12: T1-T3 done: step 1 match clause, chip clauses at step 6 and the nothing-owed chip, step 7 remove-or-narrow clause with its one docs-only commit, and the guest sentences in step 6's guest arm and step 7; the nothing-owed sentence sits after the bullet's decline sentence because `test_resume_routing` pins the text before it (lesson M148).
- 2026-10-12: T4 done: records-hygiene §1 sentence added and the paragraph reflowed to keep the module at 54 lines and 3,160 bytes (its "Kept, the graduation is one step where the work actually lands" rationale sentence dropped for the line); README `/hotfix` row edited; the candidate sweep over README.md and skills/ found no prose saying a hotfix leaves a row it fixes.
- 2026-10-12: T5 done: `skills/tests/test_hotfix_candidate_graduation.py` pins the clauses, 11 planted deletions each turned their test red with the control green; registered EXEMPT in `test_mutation_harness.py` (hand-run, D-109); scripts, hooks, and skills suites, both plugin validates, the mod test, and cairn_validate all green.
- 2026-10-12: claim audit: 29 claims read, 2 corrected — skills/hotfix/SKILL.md (step 1's "no other step edits it" now allows a search-first absorb that adds to the row; step 7 now covers the owed-items follow-up PR and names the PR that carried the fix); also tightened the guest sentences; the same reader's re-read confirmed both; guard updated, suites green.
- 2026-10-12: claim audit minor items left as is: the README row does not spell out guest mode or the over-the-bar case, and a row with no `: ` has no title (all 42 current rows have one).
- 2026-10-12: review started; Copilot arm opened PR #259 and requested Copilot (state was `none`).
- 2026-10-12: review return 1: consistency gate — `CHANGELOG.md` has no entry for this milestone's user-visible change (the plan had no task for it).
- 2026-10-12: minor amendment: T6 added for review return 1; T6 done, a CHANGELOG Unreleased entry written against the same-session read of steps 1, 6 and 7; suites green; status back to review.
- 2026-10-12: review return 2: AC2 fails in guest mode — `skills/hotfix/SKILL.md:120-122` limits the "Nothing owed" chip's row naming to owner mode (diff-bug #2); fix it with the pass-1 fix-now items (diff-bug #3, #4, #6, #8, #9, #10, #14; blame-history #4) and file the follow-up row; AC2 box unticked.
- 2026-10-12: minor amendment: T7 added for review return 2; T7 done: SKILL.md step 1 ("In both modes", "Within a hotfix"), step 7 (narrowing replaces a second row; one docs-only commit for every step-7 ROADMAP edit on any path after a `git status` check; deleted rows shown, guest too), records-hygiene §1 back to "through planning and implementation" with its rationale sentence and "A hotfix graduates the same way" (budget paragraph reflowed, module 54 lines, 3,255 bytes), CHANGELOG guest sentence; guard re-pinned with 10 new plants each red, control green; all suites and cairn_validate green.

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

Evidence at 5beab549 (2026-10-12); `test_hotfix_candidate_graduation` 5/5 OK, each pin shown red at implement (11 planted deletions).

- AC1: `skills/hotfix/SKILL.md:46-56` (step 1, before the merged-PR re-entry): finds rows "whose title the argument quotes, or a row that describes the bug being fixed" (:49-50), runs "on every entry to step 1, PR-reference re-entries included, and never from memory" (:47-48), reads "the PR's title, body and `Fixes #N` line against the rows" (:52-53), names each title or says none matched (:53-54). Pinned by `test_step1_matches_rows_on_every_entry`. Pass.
- AC2: the "Nothing owed" acceptance chip, owner mode, names each matched row's title and remove-or-narrow (`:119-122`); step 6's approval chip question text does the same (`:247-249`), and the guest handoff chip "carries no row text" (`:250`). Pinned by `test_chips_name_each_matched_row`. Pass.
- AC3: step 7 `:325-338`: owner mode, "after a merge whose diff passed the hotfix bar"; covers authored, adopted, re-landed, and the re-entry once accepted (plus the owed-items follow-up, a superset); deletes full-coverage rows, narrows partial ones with the `narrowed YYYY-MM-DD by the PR #N hotfix` note where `#N` is "the merged PR that carried the fix" (the PR that merged); every step-7 ROADMAP edit, the step-7 added row included, in one docs-only commit on the up-to-date default branch, pushed at once; narrowed and new rows shown verbatim. Pinned by `test_step7_removes_or_narrows_after_a_merge`. Pass.
- AC4: `:54-56` "Only step 7, after a merge, removes or narrows a matched row" (a search-first absorb elsewhere may add to it, never remove or narrow it); `:334-335` "On step 1's over-the-bar disposition, step 7 neither removes nor narrows a matched row." Pinned by the step-1 and step-7 tests. Pass.
- AC5: step 6 guest arm `:314-316` "The handoff leaves each matched candidate row unchanged"; step 7 guest arm `:340-345`: on the merged-PR re-entry with accepted verification, remove or narrow on disk with no commit, judged against the merged diff; "A PR closed without a merge leaves the row." Pinned by `test_guest_arm_waits_for_the_maintainers_merge`. Pass.
- AC6: `skills/shared/records-hygiene.md:19-20`, inside §1 "Candidate rows graduate at completion", right after the post-merge-hygiene sentence: "A hotfix's step 7 removes or narrows the row it fixes after the merge." README.md:549 (`/hotfix` row): "After the merge it removes the candidate row it fixed, or narrows it to the part left." Module at 54 lines, 3,160 bytes (under 55 / 4,000). Pinned by `test_records_hygiene_and_readme_say_so`. Pass.

Consistency gate at 5beab549: cairn_validate exit 0; scripts and hooks suites OK; plugin and marketplace validate exit 0, no `plugins[N].version` warning; `claude plugin test` 0 fail; skills/tests OK; CHANGELOG Unreleased entry present. No principle changed, so no `cairn_impact` run.

Review pass 1. spawned: diff-bug, blame-history, prior-review.
- diff-bug #1: guest re-entry with owed items never reaches an accepted verification, so the row edit has no route — follow-up (new candidate row "Hotfix row-graduation edges (M249 review)")
- diff-bug #2: in guest mode the "Nothing owed" chip names no rows, yet accepting it edits them; AC2 has no owner-only limit — fix now; AC2 fails as written in guest mode, review return 2
- diff-bug #3: deleted rows are never shown when the edit lands — fix now
- diff-bug #4: the one-commit rule sits under "after a merge whose diff passed the hotfix bar", so the over-the-bar re-entry's added row has no stated commit — fix now
- diff-bug #5: a CI-timeout rerun on the owed-items path can lose the original PR number — follow-up (same new row)
- diff-bug #6: step 7 switches to the default branch with no dirty-tree check — fix now
- diff-bug #7: a narrowing can push ROADMAP past its byte budget — reject (planned change: the byte budget is judgment-checked at hygiene passes by rule, like any conversational row edit, and a narrowing replaces covered text with its remainder)
- diff-bug #8: the guard leaves the sync-and-push phrase, the narrow phrase, and the title definition unpinned — fix now
- diff-bug #9: "Only step 7 ... removes or narrows" reads as a repo-wide rule against `/cairn-triage` and review hygiene — fix now
- diff-bug #10: the records-hygiene reflow dropped "planning" and the rationale sentence, and does not frame the hotfix as the same graduation — fix now
- diff-bug #11: the "Nothing owed" chip sentence sits after the decline sentence — reject (style; placed there because `test_resume_routing` pins the text before it, lesson M148)
- diff-bug #12: AC3's `#N` widened to "the merged PR that carried the fix" without an amendment — reject (false: with one merged PR the two readings agree, and on the owed path the PR that merged carrying the fix is the one AC3's wording names)
- diff-bug #13: a guest operator gets no prompt to rerun `/hotfix` after the maintainers merge — follow-up (same new row; the plan's recorded falsifier)
- diff-bug #14: the CHANGELOG entry omits that the guest edit waits for accepted verification — fix now
- blame-history #1: the dropped "Kept, the graduation is one step where the work actually lands" came from M110 and M211 — fix now (with diff-bug #10)
- blame-history #2: "through planning and implementation" lost "planning" — fix now (with diff-bug #10)
- blame-history #3: first hotfix write to the default branch outside a PR, with no D-entry — reject (false as a gap: the git model admits docs-only tracking commits on the default branch, and the PR #238 hotfix's row narrowing, edccd564, already landed that way)
- blame-history #4: a partly covered row can get both a narrowing and a new row for the same remainder — fix now
- blame-history #5: "the candidate-row check" in the re-entry now means two things — reject (style; the sentence after the bullet names the row edit)
- blame-history #6: guest arm complies with D-137 and the guest rules — noted, requests nothing
- blame-history #7: EXEMPT entry follows D-109 — noted, requests nothing
- blame-history #8: README row history clean — noted, requests nothing
- blame-history #9: CHANGELOG placement clean — noted, requests nothing
- prior-review #1: owed-items rerun may not re-match the original row and `#N` is ambiguous — follow-up (same new row as diff-bug #5)
- prior-review #2: guest acceptance chip names no row before the on-disk edit — fix now (with diff-bug #2)
- prior-review #3: the durable-record preview's hotfix exemption is stale for the post-merge commit — reject (false: the enumeration already lists candidate graduation rows and the exemption covers only content reviewable at the merge gate, so the preview is owed, which step 7 states)
- prior-review #4: the rulebook's hotfix tier line does not mention the ROADMAP edit — reject (false as a contradiction: the tier line is a summary that the change leaves true)
- prior-review #5: deleted rows get no preview — fix now (with diff-bug #3)
- prior-review #6: `--repo` covered by the session-start clause — noted, requests nothing
- prior-review #7: records-hygiene lost "planning" — fix now (with diff-bug #10)
- prior-review #8: CHANGELOG and README match — noted, requests nothing

Review pass 2, evidence at e6844aa3 (2026-10-12); guard 5/5 OK, 10 new plants each red at T7.
- AC1 (re-verified): step 1 `:46-57`, now "Within a hotfix, only step 7" (`:54`); title definition pinned. Pass.
- AC2: the "Nothing owed" chip, "In both modes", names each matched row's title and remove-or-narrow (`:120-122`); step 6's approval chip does the same (`:247-249`); the guest handoff chip carries no row text (`:250`). Pinned by `test_chips_name_each_matched_row`, now sliced to the Nothing-owed bullet. Pass.
- AC3 (re-verified): step 7 `:327-341`; one docs-only commit for every step-7 ROADMAP edit on any path (`:337-341`), after the `git status` check, synced and pushed at once; deleted, narrowed, and new rows shown. Pass.
- AC4 (re-verified): `:54-57`, `:335-336`. Pass.
- AC5 (re-verified): `:314-316`, `:342-348`. Pass.
- AC6 (re-verified): records-hygiene `:16-20` keeps "through planning and implementation" and adds "A hotfix graduates the same way: step 7 removes or narrows its row after merge."; README `:549` unchanged; module 54 lines, 3,255 bytes. Pass.
