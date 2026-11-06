<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M338: Note the pushed head after a merge push

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/milestone-review` and `/hotfix` do at a merge   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In owner mode, after a merge push, `/milestone-review` and `/hotfix` wait until GitHub reports the pushed commit as the PR head before they write the approval marker or read the PR's checks.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/milestone-review` step 8's push (a Red CI rerun's push and the
companion arm's push included) and `/hotfix` step 6's push of an authored
fix: one spelled-out, bounded re-read of `headRefOid` until it equals the
pushed commit, placed before the marker write and the first checks read,
and a stop when it does not. The rulebook's merge CI wait, a D-entry, and a
CHANGELOG entry.

**Out:** a lagging head read outside a merge push, such as the Copilot
round's state query (it decides no merge; no row, since no harm is known).
The parked row "Ask again after a merge conflict fix" keeps its clauses
(the work log says why).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: In owner mode, `skills/milestone-review/SKILL.md` step 8, after its push (the push it makes whether or not the PR already exists, a Red CI rerun's push included), reads the pushed commit with `git rev-parse origin/<branch>`, not local `HEAD`, and runs one spelled-out re-read command that reads `gh pr view <N> --json headRefOid` until it equals that commit, for at most about a minute. The re-read comes before the `cairn/.merge-approved` write, step 8 notes that commit as the head the wake compares against, and the first `gh pr checks <N>` read comes after both. The companion arm's push takes the same re-read, spelled `cd <abs-path> && …`, before that companion PR's first `gh pr checks` read.
- [ ] AC2: When step 8's re-read ends with the PR head not equal to the pushed commit, step 8 writes no marker, arms no watch, and stops with a close block that names both commits; its fenced next command is `/milestone-review M<NNN>`.
- [ ] AC3: In owner mode, `skills/hotfix/SKILL.md` step 6, for an authored fix, replaces its one head read before the marker write with the same re-read form, run until the PR head equals the head the gate showed; for an adopted PR the one read stays. When the head still differs, it writes no marker and stops with a close block that names the PR head it read and the head the gate showed, in place of "names the new head", with `/hotfix` and the PR reference as the fenced next command. Its first `gh pr checks <N>` read stays after the marker write.
- [ ] AC4: `skills/shared/tracking-rules.md`'s merge CI wait states that, after a push, the session re-reads the PR head until it equals the pushed commit before step (a)'s first check read, and its recorded-head clause reads, in substance, "`/milestone-review`: the pushed commit, once the PR reports it as its head; `/hotfix`: the marker's head oid". `git grep -n -E "PR head read right after|right after step 8's push|read and note the PR head" -- . ':!cairn'` prints no line.
- [ ] AC5: `cairn/DECISIONS.md` gains one entry that supersedes D-232's clause "`/milestone-review` reads the PR head with `gh pr view --json headRefOid` right after step 8's push and before the first check read", and states that D-108's trigger clause admits this milestone because its trigger is a defect in shipped behavior, the lagging head read seen on PR #351.
- [ ] AC6: `CHANGELOG.md`'s Unreleased section gains one entry that says, in user terms, that both skills now wait for GitHub to show the pushed commit as the PR head before they record approval or read checks.
- [ ] AC7: The `verify` slot of `cairn/PROFILE.md` is green on the branch head: `python3 -m unittest` over `scripts/tests` and `hooks/tests`, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: Write the re-read command form and try it once on a real `gh pr view` of a merged PR (for example #351 against its known head), in this harness, since a foreground command that starts with `sleep` is blocked (LESSONS M328).
- [ ] T2: Edit `skills/milestone-review/SKILL.md` step 8 (lines 734-822): the pushed-commit read, the re-read before the marker write, the note, the stop, the Red CI rerun's wording ("notes the new PR head"), and the companion arm (lines 829-866).
- [ ] T3: Edit `skills/hotfix/SKILL.md` step 6 (lines 590-598): the re-read for an authored fix, the one read for an adopted PR, and the stop text.
- [ ] T4: Edit the merge CI wait in `skills/shared/tracking-rules.md` (lines 401-417), then run AC4's `git grep` and fix each hit.
- [ ] T5: Write the D-entry of AC5.
- [ ] T6: Write the CHANGELOG entry of AC6.
- [ ] T7: Run the `verify` slot, each suite checked by its exit code, and hand-run `skills/tests` (LESSONS M148).

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

- 2026-11-05: created by /milestone-plan from the candidate row "Note the pushed head after a merge push".
- 2026-11-05: tier check: milestone — it changes what two skills do at a merge and supersedes a D-232 clause.
- 2026-11-05: idea vet: one gap, no flaw. Gap: which head to record (the PR read or the local pushed commit); reading taken: re-read the PR until it reports the pushed commit, since recording the local commit alone still lets a checks read see the old head's runs.
- 2026-11-05: collision check: the candidate row is absorbed (started M338). D-232's read clause is superseded by T5's entry; D-229 and D-231 stand. D-108's door passes on its retained trigger (the lagging read on PR #351). M336 (done) added the no-checks re-read, which stays. The parked row "Ask again after a merge conflict fix" names a gap after "a push whose first checks already passed"; this re-read covers it only where those checks belong to the previous head, so the row stays as it is.
- 2026-11-05: inbox sweep: 0 open issues, 0 open PRs.
- 2026-11-05: lessons used: 2026-07-16 (M56+M65), 2026-07-24 (M112), 2026-08-17 (M148), 2026-08-22 (M152), 2026-10-25 (M323), 2026-10-31 (M328), 2026-11-02 (M331), 2026-11-05 (M336).
- 2026-11-05: plan gate chose re-reading the PR head until it equals the pushed commit over recording the local pushed commit alone, because a checks read made before GitHub moves the head reports the old head's runs; falsified by a `gh pr checks` read that reports the old head's runs after `headRefOid` already shows the pushed commit.
- 2026-11-05: question set: none posed — the user named the row, and no open choice is the user's alone; the run's outward actions are the merge question's.
- 2026-11-05: criteria audit (full, Opus): 8 findings, all taken. The re-read moves before the marker write, so AC2 writes no marker; AC1 names the push made when the PR exists, the Red CI rerun, and the companion arm; AC1 says not local `HEAD`; both skills spell one re-read command, tried at T1; AC3 splits authored fix from adopted PR and changes "names the new head"; AC5 states the D-108 answer; AC4's grep adds "read and note the PR head" and names the hotfix head; the Goal narrows to the pushes the criteria name.
