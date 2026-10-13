<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M249: A hotfix removes the candidate row it fixes, once the fix merges

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1, GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/hotfix` does to an adopter's ROADMAP   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m249-hotfix-graduates-candidate   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: `skills/hotfix/SKILL.md` step 1 says how the hotfix finds the
      candidate rows it fixes. A matched row is a row whose title the
      argument quotes, or a row in `cairn/ROADMAP.md`'s Candidates section
      that describes the bug. For a PR-reference argument the hotfix reads
      the PR's title, body and `Fixes #N` line against the rows. The match
      runs again on every entry to step 1, PR-reference re-entries
      included, and is never taken from memory. The hotfix names each
      matched row's title in chat, or says that no row matched.
- [ ] AC2: Two chips name each matched row's title in their question text
      and say whether the merge removes the row or narrows it: step 6's
      owner-mode approval chip, and step 1's "Nothing owed" acceptance chip
      on the merged-PR re-entry.
- [ ] AC3: `skills/hotfix/SKILL.md` step 7 says what happens to the matched
      rows in owner mode after a merge whose diff passed the hotfix bar.
      This covers an authored fix, an adopted PR, a re-landed PR, and the
      merged-PR re-entry once its post-hoc verification is accepted. The
      hotfix deletes each row that the fix covers in full. It narrows each
      row that the fix covers in part, with a `narrowed YYYY-MM-DD by the
      PR #N hotfix` note, where `#N` is the PR that merged. Every ROADMAP
      edit that step 7 makes, its own new candidate row included, lands in
      one docs-only commit on the up-to-date default branch, pushed at once.
      The narrowed and new rows are shown verbatim in chat.
- [ ] AC4: `skills/hotfix/SKILL.md` says that only step 7, after a merge,
      removes or narrows a matched row, and that step 7 on step 1's
      over-the-bar disposition neither removes nor narrows it.
- [ ] AC5: `skills/hotfix/SKILL.md`'s guest arm says that the handoff
      leaves each matched row unchanged. When the merged-PR re-entry finds
      that the maintainers merged the PR, and its post-hoc verification is
      accepted, step 7 removes or narrows each row on disk, with no commit,
      judged against the merged diff. A PR closed without a merge leaves the
      row.
- [ ] AC6: `skills/shared/records-hygiene.md` §1 says that a hotfix
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
- [ ] T4: Add the sentence to `skills/shared/records-hygiene.md` §1 and
      keep the module under its 55-line, 4,000-byte budget (`wc -l -c`).
      Edit README.md's `/hotfix` row (`:549`). Sweep
      `git grep -n -i candidate -- README.md skills/` for prose that says a
      hotfix leaves a row it fixes, and fix each hit (lesson M112).
- [ ] T5: Add a hand-run prose guard in `skills/tests/` that pins the
      clauses of T1-T4, and show each pin red by deleting its clause. Run
      the whole `skills/tests` suite (lesson M148), both gating suites, and
      `cairn_validate`.

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
