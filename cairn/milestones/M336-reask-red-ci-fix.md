<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M336: Ask again before merging a red-CI fix

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes when a plugin user is asked before a merge   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m336-reask-red-ci-fix https://github.com/jmgirard/cairn/pull/351   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In owner mode, `/milestone-review` merges a red-CI fix only after the user approves the merge again, whatever the fix's size.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Candidate row "Ask again before merging a red-CI fix". The red-CI rule of `/milestone-review` step 8 for the primary PR and the companion arm, the marker and the decline, Resume routing's read of a recorded approval, the no-checks re-read after a push, README, CHANGELOG, and one D-entry.

**Out:**
- `/hotfix` step 6's re-ask: it already asks after every fix. Only its no-checks wording changes (AC3).
- Guest mode: its handoff has no merge and no CI wait.
- A fresh review-lens pass over the fix: re-verify stays as it is, and the chip shows the fix.
- `--match-head-commit` on the review's merge: stays a DESIGN Known issue.
- Route (c)'s push before its chip, when a session dies between the fix and the chip: the chip still asks before any merge. It stays under DESIGN's Known issue "A typed resume can restart CI", which T4 extends.
- The rulebook's wait rule: it only names the red-CI path, and the merge question is already one of the two gates.

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

- [x] AC1: `skills/milestone-review/SKILL.md` step 8's red-CI rule sends every fix on the primary PR's branch back to the user: the session commits the fix, re-verifies, and re-poses step 7's merge chip, with no test of the fix's size. `grep -n nontrivial skills/milestone-review/SKILL.md` prints nothing.
- [x] AC2: That rule says the re-posed chip runs step 7's PR-conversation read and blocking rule, and that its question text names the failed check and says in plain words what the fix changed.
- [x] AC3: That rule says the session does not push the fix before the new approval, and that on approval the session appends and commits a new `step-7 approval:` line and runs step 8 again from the push, so it writes the marker and notes the new PR head before the next CI wait. The no-checks re-read in step 8 and in `/hotfix` step 6 covers a PR pushed moments ago as well as one created moments ago.
- [x] AC4: Taking the red-CI path removes `cairn/.merge-approved` before the fix. Step 7's decline exit removes any `cairn/.merge-approved` that names this PR. Resume routing counts a `step-7 decline:` line newer than the latest `step-7 approval:` line as no recorded approval for routes (a) and (c).
- [x] AC5: Step 8's companion arm says a companion's red CI that the agent fixes goes back to the user before that companion merges: the fix stays unpushed, the chip names the companion PR, the failed check, and what the fix changed, and step 7's PR-conversation read stays on the primary's PR. On approval the session appends and commits a new `step-7 approval:` line in the primary's work log, and the arm resumes at that companion's push. On re-entry, a companion checkout with commits past its PR head goes to that chip before its push.
- [x] AC6: README's "Merges are yours" bullet says that a fix after a failed CI run needs your approval again. `CHANGELOG.md`'s `## Unreleased` holds an entry for this change, and its existing "A merge waits for CI in the background" entry says the same. Each line that `grep -n -i -w "on red\|red ci\|red run" README.md` prints, and each such line of `CHANGELOG.md` above `## 2.1.0`, agrees with this rule.
- [x] AC7: The profile's `verify` slot is clean on the review head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T2
- AC5 → T3
- AC6 → T4
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Rewrite the red-CI sentence at `skills/milestone-review/SKILL.md:798-799` for AC1 to AC3, and widen the "created moments ago" clause there (`:794-798`) and at `skills/hotfix/SKILL.md:587-590`.
- [x] T2: Add the marker removal to the red-CI rule and to step 7's decline exit (`SKILL.md:701-705`), and the decline clause to Resume routing (`SKILL.md:82-109`).
- [x] T3: Add the companion rule to step 8's companion arm (`SKILL.md:804-827`), its re-entry check included.
- [x] T4: Update README's "Merges are yours" bullet (`README.md:919`). Add the CHANGELOG entry and edit the "On red" sentence (`CHANGELOG.md:91`). Run AC6's sweep. Add one sentence on the chip that does not name the fix to DESIGN's Known issue "A typed resume can restart CI".
- [x] T5: Append the D-entry: every red-CI fix re-asks in `/milestone-review`, and the approval marker goes when the red path starts. It narrows D-229's consequence "After the merge approval, the session merges on green with no rerun by the user". State that D-108's door passes because the trigger is a defect in shipped behavior.
- [x] T6: Run the `verify` slot. Hand-run `python3 -m unittest discover -s skills/tests` and update any pin the wording edits break (`test_resume_routing.py`, `test_wait_rule.py`, and `test_mutation_harness.py` hold nearby text). Add no new prose guard (`cairn/PROFILE.md` test-doctrine).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-11-05: created by /milestone-plan.
- 2026-11-05: tier check: not run — work named at the question set
- 2026-11-05: idea vet: gap, which fixes the re-ask covers: reading taken is every fix on the primary and companion branches, by the row's title and `/hotfix`'s practice, since an "only after a wake" reading leaves out a fix the title names; no flaw found. The row's "promote when a user reports it" has not held, and the user chose the row at the question set with that stated.
- 2026-11-05: lessons used: 2026-07-16 (M56+M65), 2026-07-24 (M112), 2026-08-17 (M148), 2026-08-22 (M152), 2026-10-25 (M323), 2026-11-02 (M331)
- 2026-11-05: question set: how far the run goes — through to the merge question. Which work — this candidate row, over "Let guest maintainers merge their PRs" and the parked hotfix step 7 row.
- 2026-11-05: collision check: candidate row absorbed, row gets ` — started M336`. D-229 to D-232 and M328 surfaced: M328 review filed this row, and D-229's consequence is narrowed by T5. DESIGN Known issues on `--match-head-commit` and the typed resume stay. Inbox sweep: 0 open issues, 0 open PRs. No checker-regress hit, no release shape.
- 2026-11-05: plan gate chose asking before the fix is pushed over pushing the fix and asking after green CI because `/hotfix` already asks first and D-138's order pushes after approval; falsified by users declining re-asks because the chip lacked CI's result.
- 2026-11-05: plan gate chose removing the marker when the red path starts over removing it only at a decline because the marker names a PR and not a head, so it would otherwise cover the fix until the chip is answered; falsified by a guard that reads a head from the review's marker.
- 2026-11-05: criteria audit: full mode, 9 findings. Taken: companion re-entry check (2), companion read stays on the primary and the approval line's home (3), marker removal at the red path (4), decline line counts as no recorded approval (5), "appends and commits" (6), no-checks re-read after a push, extended to `/hotfix` for the same words (7), `grep -w` (8), AC7's guard sentence and `skills/tests` moved to T6 since D-109 says that suite gates nothing (9). Narrowed: route (c)'s push before its chip, finding 1, is Out, since the chip still asks before any merge.
- 2026-11-05: T1 done: step 8's red-CI rule re-poses the merge chip after every fix and removes the marker first; the no-checks re-read covers a PR pushed moments ago in step 8 and `/hotfix` step 6. The simple-english lint hook reports hundreds of hits in these skill files, all but the new sentences older than this work; left as they are, out of scope.
- 2026-11-05: T2 done: step 7's decline exit removes a marker that names the PR, and a decline line newer than the latest approval line counts as no recorded approval for routes (a) and (c); the marker removal on the red path landed in T1's commit.
- 2026-11-05: T3 done: a companion's fix stays unpushed and goes to the merge chip before that companion merges, and a re-entry that finds commits past the companion's PR head takes that chip before its push. The check is `git rev-list <branch> --not origin/<branch>`, since the arm already pushes to `origin`.
- 2026-11-05: T4 done: README, a new CHANGELOG entry, the "On red" sentence of the CI-wait entry, and the DESIGN Known issue. AC6's sweep prints README's two "red CI it cannot fix" lines and the CHANGELOG's "On red" and "red run" lines, and all agree.
- 2026-11-05: T5 done: D-241 appended.
- 2026-11-05: T6 done: `verify` slot clean (scripts and hooks suites exit 0, both manifest validates exit 0, `claude plugin test` 2466 pass and 0 fail); hand-run `skills/tests` green, 1014 tests, with no pin broken and no pin edited.
- 2026-11-05: claim audit: 25 claims read, 5 corrected — CHANGELOG.md, skills/milestone-review/SKILL.md. Corrected: the fix's push (a resume or a Copilot fix can push it first), marker not approval, the Red CI re-pose as a new pass of step 7's read, the companion read's reach, and a failed `rev-list` read taking the chip. The same reader's one re-read passed all but the Copilot push beside "Do not push the fix", now stated there. A sentence for a check the agent cannot fix was added and held on that re-read.

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

Evidence on head 978bed5f, read by one script per criterion, one check for each named property, whitespace-normalized over step 8's Red CI paragraph, its companion arm, step 7's decline exit, and Resume routing.

- AC1: `grep -n nontrivial skills/milestone-review/SKILL.md` printed nothing (exit 1). The Red CI paragraph holds "Every fix goes back to the user, whatever its size", "commit the fix, and re-verify", and "re-pose step 7's merge chip".
- AC2: the paragraph holds "Run step 7's PR-conversation read and blocking rule", "question text names the failed check", and "says in plain words what the fix changed".
- AC3: the paragraph holds "Do not push the fix", "append and commit a new `step-7 approval:` line", "run this step again from the push", and "writes the marker and notes the new PR head before the next CI wait". "created or pushed moments ago" is in step 8 and in `/hotfix` step 6.
- AC4: the paragraph holds "remove `cairn/.merge-approved`. Then fix it". Step 7's decline exit holds "remove any `cairn/.merge-approved` that names this PR". Resume routing holds the decline sentence for routes (a) and (c).
- AC5: the companion arm holds the go-back sentence, "The fix stays unpushed", "It names the companion PR, the failed check, and what the fix changed", the read on the primary's PR, the approval line in the primary's work log, the resume at that companion's push, and "that chip comes before the arm's push" on re-entry.
- AC6: README's "Merges are yours" bullet holds "A fix after a failed CI run needs your approval again". `## Unreleased` holds the new entry and the wait entry's "asks you to approve the merge again". The sweep printed README:718 and :913 ("red CI it cannot fix") and CHANGELOG:103 and :117. All agree with the rule, CHANGELOG:103 read with the sentence that follows it.
- AC7: on 978bed5f, scripts and hooks suites exit 0, both manifest validates exit 0, `claude plugin test` exit 0 with 2466 pass and 0 fail.

Consistency gate: `cairn_validate.py` exit 0. No DESIGN principle text changed, so no `cairn_impact` run. Toolchain: verify as AC7; the marketplace validate output holds no `plugins[N].version` warning; `## Unreleased` holds this change's entry. This repo has no CI.
