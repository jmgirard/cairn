# M325: Vet a hotfix on a resumed merge

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP2, IP3
- **Resolves:** —
- **Surface tier:** user-facing — every adopting repo runs `/hotfix`
- **Branch/PR:** m325-resumed-hotfix-vet, https://github.com/jmgirard/cairn/pull/338

## Goal

A `/hotfix` rerun that resumes an approved merge vets the PR's diff again, so a flaw that the fix leaves as it was still gets its candidate row.

## Scope

**In:** step 1's owner arm (Open-PR re-entry) and the first sentence of its Idea vet paragraph in `skills/hotfix/SKILL.md`. A D-entry. The README and CHANGELOG Unreleased text on the resumed merge and the hotfix vet. Re-pins of the hand-run guards.

**Out:** the owner-mode commit of a row that the over-the-bar stop writes. That gap is on every path of that stop, the resume's new stop included, and the candidate row "Commit the hotfix over-the-bar row" holds it. A flaw that the earlier run named and the resumed vet does not find again: no record can recover it, and the D-entry names it as a residual. The guest arm, which reaches no step 7, stays as it is. Released CHANGELOG sections stay as they are.

## Acceptance criteria

- [x] AC1: When all three resume conditions hold, step 1's owner arm in `skills/hotfix/SKILL.md` runs the idea vet on the PR's diff (`gh pr diff <N>`). The vet runs before the arm says that the run resumes, and before step 6's CI wait. It checks nothing out, and it reads the records that a matched row cites from the current checkout. The arm still skips the rest of the tier check, steps 2 to 5, and the parts of step 6 that it skips now.
- [x] AC2: In that arm, a flaw only in what the PR's diff leaves as it was does not stop the resumed merge. A name, an argument, or a behavior can hold such a flaw. Step 7 adds its candidate row after the merge. A close block that ends the resumed run before step 7 names the flaw.
- [x] AC3: In that arm, a concern that the vet sends over the hotfix bar stops the resume before the CI wait. Such a concern is a flaw in what the PR's diff changes, a gap whose reading the diff does not take included, or a gap that `/milestone-plan` step 2 sends to its question set. The run removes the merge-guard marker, merges nothing, leaves the PR open, and takes step 1's over-the-bar route. Its close block says that the approval the marker recorded is withdrawn, names the concern, and says that the PR stays open.
- [x] AC4: The first sentence of step 1's Idea vet paragraph names the owner arm's resumed merge as an entry that vets. It names it beside the entries that run the tier check.
- [x] AC5: A new `cairn/DECISIONS.md` entry records AC1 to AC3. It supersedes D-168's clause that a resumed merge skips the tier check, for the idea vet only. It annotates D-225, whose Consequences name the gap that this milestone closes. It names, as a residual of D-042's rule, a flaw that the earlier run named and the resumed vet does not find again. It states that it passes D-108's door on the shipped-behavior trigger.
- [x] AC6: `git grep -n -i -e 'resum' -e 'approved merge' -- README.md CHANGELOG.md 'skills/*.md'` lists lines. Each sentence that holds a listed line in README, in the CHANGELOG's Unreleased section, or in a skill file, and that says which checks a resumed `/hotfix` merge runs or skips, agrees with AC1. README's `/hotfix` resume sentence says that a resumed merge vets the fix again. So does the CHANGELOG Unreleased entry "The plan and the hotfix question the request before they build it."

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T1
- AC5 → T2
- AC6 → T3

## Tasks

- [x] T1: Edit step 1's owner arm (`skills/hotfix/SKILL.md:195-216`): the vet before the resume sentence, the left-flaw path, and the over-the-bar stop with its marker removal and close block. Edit the first sentence of the Idea vet paragraph (`:52`). Add nothing to step 6's timeout close or the refused-merge close, since the Idea vet paragraph's close-block rule reaches both. (AC1 to AC4)
- [x] T2: Write the D-entry. (AC5)
- [x] T3: Edit README `:976-978` and the CHANGELOG Unreleased vet entry (`:363-372`). Run AC6's grep, and fix each stale sentence it finds in its domain. (AC6)
- [x] T4: Re-pin the hand-run guards `skills/tests/test_resume_routing.py` and `skills/tests/test_idea_vet.py`, and the `test_mutation_harness.py` registrations keyed to owner-arm text, then run `python3 -m unittest discover -s skills/tests`. Run both gating suites, `claude plugin validate` on both manifests, and `claude plugin test`, and check each exit code.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: milestone — it changes `/hotfix`'s resume behavior and narrows D-168's decision, a design decision.
- 2026-10-29: idea vet: two concerns, both gaps. (1) gap: how a resumed run learns of the earlier run's flaw. Reading taken: the resume runs the vet again, as the row's title and D-225's Consequences name. (2) gap: what a resumed vet's over-the-bar concern does. Another reading changes what the user gets, so the question set asked it (answer below).
- 2026-10-29: collision: absorbs the candidate row "Vet a hotfix on a resumed merge" (M324 AC5 re-audit). D-168's skip-the-tier-check clause is narrowed and D-225 annotated at T2. D-108's door passes on its retained trigger, a defect in shipped behavior (a flaw loses its record on a resume). The row "Commit the hotfix over-the-bar row" stays separate (Out). No checker-regress shape: the vet judges a fix's behavior, not repo-internal artifacts. Inbox sweep: no open issues or PRs.
- 2026-10-29: lessons used: 2026-07-16 (M56+M65, both suites), 2026-07-24 (M112, grep the whole doc surface), 2026-08-17 (M148, prose-guard re-pins), 2026-08-22 (M152, a decision change owes a D-entry), 2026-10-29 (M324, name the commit that lands a row write).
- 2026-10-29: criteria audit (full): 9 findings, all taken. AC1 vets before the resume sentence and checks nothing out. AC2 kept, and T1 adds no close-block text. AC3 withdraws the approval in its close block, leaves the PR open, and covers a gap the diff does not take. AC5 narrows D-168 instead of annotating it, and names the residual and D-108's door. AC6 is bounded to sentences that its grep finds in README, the CHANGELOG Unreleased section, and skill markdown. T4 adds the mutation-harness re-pins. AC4 clean.
- 2026-10-29: question set: a resumed merge whose vet finds an over-the-bar concern — stop the merge, withdraw the approval, and leave the PR open (recommended, chosen).
- 2026-10-29: plan gate chose running the vet again on resume over recording the earlier run's flaw before the CI wait (in the marker or an early row), because the row's title and D-225 name the vet and the marker is a one-line guard contract; falsified by a resumed vet that misses a flaw the earlier run named.
- 2026-10-29: plan gate chose to keep "Commit the hotfix over-the-bar row" separate over absorbing it, to keep this scope to the resume; falsified by a resumed over-the-bar stop whose row is lost uncommitted before that row is planned.
- 2026-10-29: changelog: edit the Unreleased vet entry, since the vet is unreleased, and add no new entry.
- 2026-10-29: started; branch m325-resumed-hotfix-vet cut from main at a8784953. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-29: T1 done: the owner arm runs the vet on `gh pr diff <N>` before its resume sentence, an over-the-bar concern removes the marker, leaves the PR open, and withdraws the approval in its close block; the Idea vet paragraph's first sentence names the resumed merge. Gating suites green; three hand-run pins go stale, re-pinned at T4.
- 2026-10-29: T2 done: D-226 supersedes D-168's skip-the-tier-check clause for the idea vet, annotates D-225, names the not-found-again residual (D-042) and the over-the-bar row's commit gap, and passes D-108's door on its retained trigger.
- 2026-10-29: T3 done: README's resume sentence and the CHANGELOG Unreleased vet entry say that a resumed merge vets again and that an over-the-bar concern withdraws the approval. AC6's grep (released CHANGELOG sections from line 511 and `skills/tests` left out) found no other sentence on which checks a resumed `/hotfix` merge runs; CHANGELOG:450 and `skills/shared/copilot-review.md:44` name one check each and agree.
- 2026-10-29: T4 done: re-pinned `test_idea_vet.py`, `test_resume_routing.py`, and one `test_mutation_harness.py` block; hand-run `skills/tests` 977 OK. Verify: scripts and hooks suites OK, both `claude plugin validate` runs exit 0, `claude plugin test` 2466 pass, 0 fail.
- 2026-10-29: claim audit: 27 claims read, 2 corrected — CHANGELOG.md (the row lands after the merge, or the close block names the flaw), skills/hotfix/SKILL.md step 6 (the CI-wait sentence names the resumed vet's stop before the wait); both re-read and hold. Guards, both suites, and both validates rerun green; the mod test not rerun, since only markdown changed after it.
- 2026-10-29: implement done; status review.

## Decisions

## Review

Copilot: request accepted by `gh pr edit 338 --add-reviewer @copilot` (exit 0), but the next state query read `none`. Copilot request on PR #338 may not be recorded by GitHub (used-up Copilot credits are one cause). No second request.

- AC1: `skills/hotfix/SKILL.md:200-203` runs the idea vet on `gh pr diff <N>` when all three conditions hold, with no other part of the tier check, checking nothing out and reading cited records from the current checkout. The stop sits before the CI wait (`:205-206`), and the resume sentence follows it (`:212`, "With no such concern, say that the run resumes"). `:213-215` still skips the rest of the tier check, steps 2 to 5, and step 6's Copilot round arm, PR-conversation read, approval chip, and marker write. Pinned by `test_resume_routing.py` (hand-run `skills/tests` 977 OK at 03e565ce).
- AC2: `skills/hotfix/SKILL.md:203-205`: a flaw only in what the diff leaves as it was "does not stop the resume, and it takes the vet's dispositions above". Those dispositions (`:72-84`) cover a name, argument, or behavior: step 7 adds the candidate row if the run reaches step 7, and a close block that ends the run before step 7 names the flaw. Step 7 (`:615-617`) adds the row "for each flaw that step 1's idea vet found", which the resumed vet now is. The claim audit confirmed the cross-reference.
- AC3: `skills/hotfix/SKILL.md:205-212`: an over-the-bar concern "stops the resume here, before the CI wait"; it is a flaw in what the diff changes, "a gap whose reading the diff does not take included", or a gap that `/milestone-plan` step 2 sends to its question set; the run removes the marker, merges nothing, leaves the PR open, takes this step's over-the-bar route, and its close block says the approval the marker recorded is withdrawn, names the concern, and says the PR stays open. Step 6's CI-wait sentence (`:506-509`) names this stop too.
- AC4: `skills/hotfix/SKILL.md:52-54`, the paragraph's first sentence: "Every entry that runs this tier check, and the owner arm's resumed merge below, also vets the behavior that the fix or the PR diff produces". Pinned by `test_idea_vet.py` (`test_scope_every_tier_check_entry`).
- AC5: `cairn/DECISIONS.md:8160` D-226 (new on this branch) records the vet on resume, the left-flaw path, and the over-the-bar stop; its heading and Decision supersede D-168's skip-the-tier-check clause for the idea vet only and annotate D-225; its Consequences name the not-found-again flaw as a residual of D-042's rule; its Door names D-108's retained trigger (a defect in shipped behavior).
- AC6: the named `git grep` at 03e565ce lists 75 lines in the domain (CHANGELOG lines from 511, the released sections, left out). The sentences among them that say which checks a resumed `/hotfix` merge runs or skips: README:976-981 (skips the read, checks change requests, vets again, stops on an over-the-bar concern), CHANGELOG:373-378 (vets again before the CI wait), CHANGELOG:450 (checks `Candidate row:` lines, one check, agrees), `skills/hotfix/SKILL.md:200-216` and `:506-509`. All agree with AC1. `skills/shared/copilot-review.md:44` said "a `/hotfix` resume" requests Copilot again, which a resumed merge does not; it now says "rerun" (03e565ce). README's resume sentence and the CHANGELOG Unreleased entry "The plan and the hotfix question the request before they build it." each say a resumed merge vets the fix again.
- Gate: `cairn_validate.py` exit 0, all checks passed. No DESIGN principle changed, so `cairn_impact` is skipped. Verify at 03e565ce: `scripts/tests` 446 OK, `hooks/tests` 210 OK, both `claude plugin validate` runs exit 0 with no `version` warning in the marketplace output, `claude plugin test` 2466 pass, 0 fail. Changelog: the Unreleased vet entry is edited (CHANGELOG:373-378), with no milestone number. No CI on this repo.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the Own open PR paragraph's "When the owner arm above does not resume it, the run takes the tier-check walk" sends a resume the vet stopped into a second walk — fix now, fixed ed3f3941
- diff-bug #2: the tree the vet reads on a resume is the current checkout, which can be dirty, stale, or another branch — follow-up, row "Tidy the resumed hotfix vet's stop"
- diff-bug #3: `gh pr diff` is not pinned to the approved head, so a push during the vet can be vetted — reject (edge): only a push in the seconds between the head read and the diff reaches it, and its effect is a withdrawn approval or a merge that `--match-head-commit` refuses, never a wrong merge
- diff-bug #4: D-226's Decision omits the close-block case for a left flaw and that the PR stays open — reject (false): D-226 states what this milestone decides, and the close-block case is D-225's standing rule, which D-226 annotates
- diff-bug #5: "the vet's dispositions above" is a loose reference — fix now (names step 7's row or the close block outright), fixed ed3f3941
- diff-bug #6: after the stop the open PR's `Candidate row:` lines keep hiding the matched rows — follow-up, row "Tidy the resumed hotfix vet's stop"
- diff-bug #7: the new stop has no guard — reject (planned change): the profile's test-doctrine slot owes no prose guard for a new rule
- diff-bug #8: edited lines left long or short (SKILL.md:54, :216, README.md:982) — fix now, fixed ed3f3941
- blame-history #1: the Copilot module's "`/hotfix` resume" changed to "rerun", but D-183's Decision names that wording and README:1041 matches it — fix now (reverted), fixed ed3f3941
- blame-history #2: D-226 does not name the gap-not-taken class — reject (false): D-226 says "a concern that the vet sends over the hotfix bar" with no list, and that class is a flaw in what the diff changes by D-224
- blame-history #3: step 6's CI-wait sentence was edited though T1 said to add nothing to the timeout close — reject (false): T1's note is about close-block flaw text; the edit corrects the re-entry description at the claim audit, logged in the work log
- blame-history #4: D-226 does not discuss D-168's rejection of re-posing the chip — reject (false): the stop poses no chip, and D-226 says the rest of D-168's skips stand
- blame-history #5: approvals given under D-224's chip-naming clause are now withdrawn — reject (false): D-225 superseded that clause inside M324 before its merge, so no such approval exists
- blame-history #6: cited records read from the current checkout can be missing there — follow-up, row "Tidy the resumed hotfix vet's stop"
- blame-history #7: the stop's close block does not say whether to close the open PR — follow-up, row "Tidy the resumed hotfix vet's stop"
- blame-history #8: README's "design problem" is narrower than the skill's "concern" — reject (style): README's plain wording for the same class
- prior-review #1: the resumed over-the-bar stop writes a row with no owner-mode commit, the M324 floor-return defect on a new path — follow-up, absorbed by the existing row "Commit the hotfix over-the-bar row", whose text covers every over-the-bar stop (planned Out, D-226)
- prior-review #2: ragged wraps in README and SKILL.md — fix now, fixed ed3f3941
- ripple #1: the Own open PR sentence (same as diff-bug #1) and its pin in `test_resume_routing.py:569` — fix now, fixed ed3f3941
- ripple #2: the `TestHotfixOpenPrReentry` docstring lists the outcomes without the vet stop — fix now, fixed ed3f3941
- ripple #3: the candidate row "Vet a hotfix on a resumed merge" still says no vet runs — reject (planned change): step 9's hygiene graduates it at merge
- ripple #4: the mutation registry comment lists resume outcomes without the vet stop — fix now (comment names it and that it has no entry), fixed ed3f3941
- ripple #5: README says "design problem" where the skill says "concern" — reject (style)
- Return floor: no finding shows a criterion failing; diff-bug #1 duplicated a walk that stops again at the bar, with no wrong merge. No return.
- AC1 to AC6 re-checked at ed3f3941: the owner arm reads at `skills/hotfix/SKILL.md:201-218` (vet at :201-204, left flaw at :204-206, stop at :206-215, resume sentence at :214), the vet's first sentence at :52-54, the Own open PR walk at :284-286. The Copilot module line is back to "a `/hotfix` resume"; it says that a later run of the request step requests again, not which checks a resumed merge skips, so it is outside AC6's subset. Hand-run `skills/tests` OK, scripts and hooks suites OK, both validates exit 0; the mod test was not rerun, since only markdown and hand-run tests changed after its 2466-pass run.
