# M325: Vet a hotfix on a resumed merge

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP2, IP3
- **Resolves:** —
- **Surface tier:** user-facing — every adopting repo runs `/hotfix`
- **Branch/PR:** —

## Goal

A `/hotfix` rerun that resumes an approved merge vets the PR's diff again, so a flaw that the fix leaves as it was still gets its candidate row.

## Scope

**In:** step 1's owner arm (Open-PR re-entry) and the first sentence of its Idea vet paragraph in `skills/hotfix/SKILL.md`. A D-entry. The README and CHANGELOG Unreleased text on the resumed merge and the hotfix vet. Re-pins of the hand-run guards.

**Out:** the owner-mode commit of a row that the over-the-bar stop writes. That gap is on every path of that stop, the resume's new stop included, and the candidate row "Commit the hotfix over-the-bar row" holds it. A flaw that the earlier run named and the resumed vet does not find again: no record can recover it, and the D-entry names it as a residual. The guest arm, which reaches no step 7, stays as it is. Released CHANGELOG sections stay as they are.

## Acceptance criteria

- [ ] AC1: When all three resume conditions hold, step 1's owner arm in `skills/hotfix/SKILL.md` runs the idea vet on the PR's diff (`gh pr diff <N>`). The vet runs before the arm says that the run resumes, and before step 6's CI wait. It checks nothing out, and it reads the records that a matched row cites from the current checkout. The arm still skips the rest of the tier check, steps 2 to 5, and the parts of step 6 that it skips now.
- [ ] AC2: In that arm, a flaw only in what the PR's diff leaves as it was does not stop the resumed merge. A name, an argument, or a behavior can hold such a flaw. Step 7 adds its candidate row after the merge. A close block that ends the resumed run before step 7 names the flaw.
- [ ] AC3: In that arm, a concern that the vet sends over the hotfix bar stops the resume before the CI wait. Such a concern is a flaw in what the PR's diff changes, a gap whose reading the diff does not take included, or a gap that `/milestone-plan` step 2 sends to its question set. The run removes the merge-guard marker, merges nothing, leaves the PR open, and takes step 1's over-the-bar route. Its close block says that the approval the marker recorded is withdrawn, names the concern, and says that the PR stays open.
- [ ] AC4: The first sentence of step 1's Idea vet paragraph names the owner arm's resumed merge as an entry that vets. It names it beside the entries that run the tier check.
- [ ] AC5: A new `cairn/DECISIONS.md` entry records AC1 to AC3. It supersedes D-168's clause that a resumed merge skips the tier check, for the idea vet only. It annotates D-225, whose Consequences name the gap that this milestone closes. It names, as a residual of D-042's rule, a flaw that the earlier run named and the resumed vet does not find again. It states that it passes D-108's door on the shipped-behavior trigger.
- [ ] AC6: `git grep -n -i -e 'resum' -e 'approved merge' -- README.md CHANGELOG.md 'skills/*.md'` lists lines. Each sentence that holds a listed line in README, in the CHANGELOG's Unreleased section, or in a skill file, and that says which checks a resumed `/hotfix` merge runs or skips, agrees with AC1. README's `/hotfix` resume sentence says that a resumed merge vets the fix again. So does the CHANGELOG Unreleased entry "The plan and the hotfix question the request before they build it."

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T1
- AC5 → T2
- AC6 → T3

## Tasks

- [ ] T1: Edit step 1's owner arm (`skills/hotfix/SKILL.md:195-216`): the vet before the resume sentence, the left-flaw path, and the over-the-bar stop with its marker removal and close block. Edit the first sentence of the Idea vet paragraph (`:52`). Add nothing to step 6's timeout close or the refused-merge close, since the Idea vet paragraph's close-block rule reaches both. (AC1 to AC4)
- [ ] T2: Write the D-entry. (AC5)
- [ ] T3: Edit README `:976-978` and the CHANGELOG Unreleased vet entry (`:363-372`). Run AC6's grep, and fix each stale sentence it finds in its domain. (AC6)
- [ ] T4: Re-pin the hand-run guards `skills/tests/test_resume_routing.py` and `skills/tests/test_idea_vet.py`, and the `test_mutation_harness.py` registrations keyed to owner-arm text, then run `python3 -m unittest discover -s skills/tests`. Run both gating suites, `claude plugin validate` on both manifests, and `claude plugin test`, and check each exit code.

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

## Decisions

## Review
