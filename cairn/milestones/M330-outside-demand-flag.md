# M330: Ask who wanted the work in guest plans

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — `/milestone-plan` text that every guest repo runs
- **Branch/PR:** m330-outside-demand-flag, https://github.com/jmgirard/cairn/pull/344

## Goal

In guest mode, a plan asks whether to do work that nobody outside it asked for, before any file is written for that work.

## Scope

**In:** guest mode only. `/milestone-plan` step 2 gains an outside-demand check beside the maintainer decision.

Someone asked when a person other than the operator asks for this change in a text. A report also counts if it describes a problem that the change fixes and that still occurs at the base head. A maintainer's agreement found by step 2 counts too. The texts are what step 2's agreement read returns, each issue in any repo that the request or row cites, and a place that the user names. A bot's text does not count. A link to an issue whose text does neither does not count. A fix for a wrong number, a crash, or broken documented behavior is outside the check.

If no one asked and step 2's maintainer question covers the work, that question's text says so, and no separate question is posed. A maintainer's no stays the existing flaw. Otherwise the idea vet poses no-one-asked as a flaw on the existing path. A do-not-build answer writes no file, and the `idea vet:` line records the answer. The check also reaches work with no change to a result or output that users see, such as a refactor or a speedup, which the maintainer decision leaves out.

The question says who asked, or "no one in the texts read", and it names a failed read. It also says what users lose or see change. Its options are to build anyway, to name where someone asked, and not to build. If the plan can say what goes wrong for a user, a fourth option drafts an issue that the user posts. The draft reuses the maintainer question's temp file, command, rerun, and wait option. Its parked row says `promote when someone asks for it`. A named place runs the read as "a maintainer already agreed" does, so a place that no read can reach goes on as named by the user.

This question can be the whole set, so the rulebook's sentence on a lone maintainer question changes to allow it, and the rulebook mass is re-seeded. Also README, CHANGELOG, and one D-entry. No new header slot, work-log line, or validator failure.

**Out:**

- "A row the session found itself leads only to opening an issue" is not a rule of its own. The draft option carries it, and the user's 2026-11-02 approval replaced its demand part.
- Guest `cairn_next` keeps recommending `/milestone-plan` when idle. A script cannot judge whether a row says what goes wrong for a user, and the check stops that work at the plan. The D-entry rejects this change with a falsifier.
- Review follow-ups keep going to candidate rows. That change is a new rule about records with no defect in shipped behavior behind it (D-108). The D-entry rejects it with a falsifier.
- Owner mode and `/hotfix` stay as they are, because the user asked for guest mode. The D-entry names the falsifier.
- Triage of one repo's backlog is the see session's own work.

## Acceptance criteria

Reader runs. A reader run is one fresh-context subagent that has not seen this plan. It gets `skills/milestone-plan/SKILL.md` and `skills/shared/tracking-rules.md` at the branch head and the case text. The case is in guest mode unless it says otherwise. The reader says what the skill text requires and quotes the deciding sentence. Each criterion below states what the skill text requires.

- [x] AC1: Reader run on a request that names a candidate row. The session filed the row at an earlier plan. The row renames an internal helper with no change users can see, and no issue, comment, or review mentions it. The skill text requires a question at step 3 before any file is written for that work. The question says that no one in the texts read asked, and what users lose or see change. Its options include building anyway and not building, no draft option is offered, and the question can be the whole set. A second reader gets the same row chosen at the question set of a request that names no work. There the skill text requires a close block that names the concern, with a fenced `/milestone-plan` and the row's short title.
- [x] AC2: Reader run on easystats/see M015's Goal, its sentence "It removed the contour lines from the panel for most well-fitting models", and the fact that its row came from the operator's own earlier plan. The case also holds the text of easystats/performance#894, the fact that a LOESS change settled that report, and no maintainer agreement. The skill text requires the maintainer question with its three options and no separate outside-demand question. That question's text says that no one asked and that the contour lines leave the panel.
- [x] AC3: Reader run on these cases, one reader per case. The skill text requires no outside-demand question for each. The cases are a fix the session found for a function whose result differs from its cited formula, a fix the session found for a crash on an input the docs allow, and a fix the session found that restores documented behavior. Two more are a helper rename that another person's issue comment asks for, and AC1's case in owner mode. Where the maintainer question is still posed for such a fix, its text makes no statement on who asked.
- [x] AC4: Reader run on AC1's rename with each of these, one reader per case. The skill text requires the question for each. The first is an issue whose reporter blames a different cause and names neither the rename nor a problem it fixes. The second is an issue by the operator's own login with no other person's text. The third is a bot's review note that asks for the rename. The fourth is a read of the operator's PRs that fails, and there the question names that read.
- [x] AC5: Reader run on these outcomes for AC1's case, one reader per outcome. Building anyway writes the milestone file with an `idea vet:` line that names the flaw and the answer. Not building writes no file and leaves the row in place. Naming a place whose text asks for the rename goes on, and the line names the place. Naming a call that no read can reach goes on, and the line says the user named it. Naming a place whose text does not ask writes no file and ends with a close block. A maintainer's agreement that step 2 finds means no outside-demand question. A maintainer's no is a flaw that cites the no.
- [x] AC6: Reader run on a speedup of a slow default that users hit, which changes no result or output, with no one outside asking. The skill text requires the outside-demand question and not the maintainer question, with a draft option. Choosing it writes the temp file with text that says what goes wrong for a user, shows the command in the close block, and posts nothing. It writes no milestone file, and a parked row with `promote when someone asks for it` when no row holds the work. A rerun with the operator's own open issue and no other person's reply offers waiting in place of the draft.
- [x] AC7: `cairn/DECISIONS.md` holds an entry that states the check and D-108's door, and says that a text settles this check only, as an annotation of D-204. It rejects the `cairn_next` change, the review follow-up change, and owner mode and `/hotfix`, each with a falsifier. README and CHANGELOG's Unreleased section state the check.
- [x] AC8: The `verify` slot's five commands exit 0 at the head, and `python3 scripts/cairn_validate.py` passes.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T3, T6
- AC3 → T1, T3
- AC4 → T1, T3
- AC5 → T1, T3
- AC6 → T1, T3
- AC7 → T4
- AC8 → T5

## Tasks

- [x] T1: Edit `/milestone-plan`. Step 2 gains the outside-demand paragraph after "Maintainer decision". Step 3's maintainer question text, its flaw bullet, and "The maintainer question" gain the who-asked wording, the options, and the draft's parked row.
- [x] T2: Edit the rulebook's sentence "A guest plan's maintainer question can stand alone". Re-seed the rulebook mass in the `/milestone` skill line and the two hand-run pins.
- [x] T3: Run the reader runs at the head. Give each case the record it rests on, in neutral words. If a reader disagrees with a criterion, read the sentence it quotes, then change the text or record why not before a new reader runs. Run AC1's first case and AC2 once at the plan commit as a baseline.
- [x] T4: Write the D-entry, README, and CHANGELOG. Search the repo for text that the change makes stale.
- [x] T5: Run `verify`, `cairn_validate`, and the hand-run `skills/tests`. List added diff lines over 80 characters before the commit.
- [x] T6: Fix review return 1: step 2's sentence bars a separate question, and the pass's fix-now findings land in the skill, D-234, and README.

## Work log

- 2026-11-02: created by /milestone-plan.
- 2026-11-02: tier check: not run — work named at the question set.
- 2026-11-02: idea vet: no flaw. gap — "reports the problem" would count easystats/performance#894 for M015, so the reading taken counts a report only if the problem still occurs at the base head. gap — the operator's own typed request is not outside demand, so the question says that no one else asked. gap — M329's check covers a change of behavior, so the reading taken has this check reach work with no change to a result or output that users see. Premise checked: see M015's archive says no user or maintainer reported the axis growth, and PR 487's closing comment says the LOESS changes made it unnecessary.
- 2026-11-02: lessons used: 2026-07-24 (M112), 2026-08-17 (M148), 2026-08-17 (M149), 2026-10-29 (M325), 2026-10-30 (M327), 2026-11-02 (M329).
- 2026-11-02: collision check: candidate row "Ask for outside demand in guest plans" absorbed in full by promotion. M329 (done) is the base, and this plan extends its question. D-233 rejected a plan-anyway option because rule (4) says to wait, and that stands for its question, since this option applies only to work rule (4) does not cover. D-204 says an issue's wording answers none of the vet's questions, so the D-entry says that a text settles this check only. D-224's flaw path carries the question. D-057 closes size work only. D-108's door: the check decides what to build and adds no record line, and the `idea vet:` line already exists. M015 predates the idea vet, so no shipped rule failed, and the check is excepted by name at the user's decision, as D-233 did.
- 2026-11-02: inbox sweep: no open issues and no open PRs in jmgirard/cairn, 0 items to triage.
- 2026-11-02: weigh of the row's four changes, which the row assigns to the plan: (1) the flag is built, as the user approved. (2) is carried by the draft option. (3) is declined: guest `cairn_next` and the mirrored `recommend` in `hooks/status/reader.ts` cannot judge prose, and a `(#N)` title test is a proxy that cannot see who opened the issue. (4) is declined: 7 of the 289 candidate rows in the 9 easystats guest repos with rows name a still-`blocked` milestone's review, and M015's drop removed its rows by hand, with two items that also applied on main.
- 2026-11-02: plan gate chose the flaw path and the `idea vet:` line over an `outside demand:` line because the path already writes no file on a do-not-build answer and D-108 bars a new record rule without a defect; falsified by a resumed run or a review that cannot find the answer in that line.
- 2026-11-02: plan gate chose a build-anyway option over the typed-only override of M329 because the user's approved question asks whether to do the work at all and rule (4) does not bar this work; falsified by a run of guest plans in which every flagged question is answered build anyway.
- 2026-11-02: plan gate declined a guest `cairn_next` change over a mechanical `(#N)` row test because the test cannot show demand; falsified by a run of idle guest sessions whose recommended plans the user keeps answering do not build.
- 2026-11-02: plan gate declined keeping review follow-ups in the milestone file over filing rows because D-108 bars the new record rule; falsified by rows for code that never merged being picked as work, or by a shipped defect they cause.
- 2026-11-02: criteria audit (full mode, one fresh Opus reader): 10 findings, all fixed in the criteria and Scope. Fixes: a report counts only if the problem still occurs at the base head, cited issues in other repos are read, AC2 gets #894's text, agreement counts as asking and a no stays a flaw, AC6 names the no-output-change case and the parked row and wait option, the rulebook clause changes so the question can stand alone, AC2 narrows to no separate question, the question says "no one in the texts read" and names a failed read, a place no read can reach goes on as named by the user, AC1 gains the request that names no work, AC7 gains the owner-mode falsifier and the D-204 annotation, and AC3 covers a maintainer question on a fix. AC8 had no finding.
- 2026-11-02: sizing: 8 criteria pass the advisory tripwire of 7, kept as one milestone because six are reader cases over one skill paragraph and no part ships alone.
- 2026-11-02: implement started: branch m330-outside-demand-flag cut from main at c6584d1c, in a worktree in the session's scratch directory, because `~/.claude/skills/cairn` links to the main checkout and a branch switch there changes the plugin that running sessions read. Untracked `cairn-probe.log` and `tsconfig.json` in the main checkout stay unstaged.
- 2026-11-02: reader runs use Haiku first, one reader per case as the criteria say, and any disagreement runs again on Opus, because no role names a model for them and about 20 readers on Opus is out of proportion to one skill paragraph.
- 2026-11-02: T1, T2: step 2 gains the outside-demand paragraph, step 3 gains its bullet and options paragraph, the rulebook sentence allows the question alone, and the mass is re-seeded at 892 lines / 88,366 bytes in the `/milestone` line and the two pins. The file-wide style hook's hits on these skill and rulebook files are older text, left alone as out of scope.
- 2026-11-02: T4: D-234, README (two sites), and CHANGELOG written. A search for "maintainer question can stand alone" and "a maintainer decision that step 2" outside `cairn/` finds no stale restatement.
- 2026-11-02: T3 baseline at the plan commit, on Haiku: the rename case gets no question ("the text requires none"), and the M015 case gets the maintainer question with no statement on who asked. Both fall short of AC1 and AC2, as expected.
- 2026-11-02: T3 first head pass: the crash-fix reader required the maintainer question to say that no one asked, against AC3, because "When step 2 found that no one outside asked" did not exclude a fix outside the check. The sentence now reads "When step 2's outside-demand check ran and found that no one asked" and adds "For a fix outside that check, it says nothing on who asked."
- 2026-11-02: T3 head pass: 20 cases on Haiku across AC1 to AC6, plus a rerun of the crash fix with a maintainer question after the fix above. No reader disagreed with a criterion after that fix, so no Opus rerun was needed. Each reader's pointer to the question-set bullet named the wrong section of the rulebook, which changed no answer. The AC6 reader led to one more edit: step 7's close-block list now names the outside-demand question.
- 2026-11-02: T5: at the T4 head, the five `verify` commands, `cairn_validate`, and the hand-run `skills/tests` exit 0, with 2466 mod tests passing. Added diff lines hold nothing over 80 characters.
- 2026-11-02: correction to the T3 line: the wrong pointer was in the session's own reader brief, and several readers reported it, not each.
- 2026-11-02: claim audit: 51 claims read, 3 corrected — CHANGELOG.md, skills/milestone-plan/SKILL.md
- 2026-11-02: review return 1: AC2's reader required a separate outside-demand question beside the maintainer question, because step 2's "says so if it covers the work" does not bar a second question. Fix that sentence and the pass's other fix-now findings, listed in the Review section.
- 2026-11-02: T6: added as a minor amendment for return 1. Step 2 now says "and no separate question is posed" and reads a cited PR. Step 3 has one recommendation at a time. Waiting turns on "no other person". D-234's heading names D-144 and its Decision names the call path. README counts a maintainer's agreement. The claim audit is not owed again for these six wording fixes, which correct findings against the lines it read, and review's lenses read them next.

## Decisions

## Review

Pass 1, at 4f45dea3. Readers on Haiku, one per case.

- AC1 (pass 1): the rename case requires the question before any file, saying "no one in the texts read" asked and what users lose or see change, with build anyway, someone already asked, and do not build, no draft, and the question alone allowed. The same row chosen at the set requires a close block and a fenced `/milestone-plan` with the short title. Met; the recommended-option fix below touches this sentence, so it reruns.
- AC2 (pass 1): NOT MET. The reader required two questions, the maintainer question and a separate outside-demand question, reading "says so if it covers the work" as no bar on the second.
- AC3 (pass 1): formula fix, crash fix, documented fix, a helper rename another person's comment asks for, and owner mode each require no outside-demand question. A fix's maintainer question says nothing on who asked. Met.
- AC4 (pass 1): the other-cause issue, the operator's own issue, the bot's note, and the failed PR read each require the question, and the failed read's question names the read. Met.
- AC5 (pass 1): build anyway writes the file and the line names the flaw and answer. Do not build writes no file and leaves the row. A place that asks goes on and names the place. A call goes on and says the user named it. A place that does not ask writes no file and ends with a close block. A maintainer's agreement means no question. A maintainer's no is a flaw that cites the no. Met.
- AC6 (pass 1): the speedup requires the outside-demand question, not the maintainer question, with the draft option. The draft goes to the temp file, says what goes wrong for a user, posts nothing, writes no milestone file, and writes the parked row. A rerun with the operator's open issue offers waiting. Met; the "no other person" fix touches this sentence, so it reruns.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: the sweep's `gh issue list` returns 30 open issues, so an older request goes unread with no failed read named — follow-up: parked row "Tighten the outside-demand check edges".
- diff-bug #2: "asks for this change" has no still-occurs test, while a report does — follow-up: same row.
- diff-bug #3: a cited PR or Discussion goes unread, so the question says no one asked — fix now for a cited PR; a Discussion goes to the same row.
- diff-bug #4: "base head" names no ref, and a static read cannot show that a behavior occurs — reject (false): "base head" names the ref, and step 2's guest reads fetch first.
- diff-bug #5: the read recipes hard-code `<base-repo>`, and `author_association` is relative to the other repo — reject (false): any person other than the operator counts as asking, so the association changes no result.
- diff-bug #6: waiting has nothing to replace when no draft is offered — follow-up: same row.
- diff-bug #7: "no one else has answered" includes a bot — fix now: "no other person".
- diff-bug #8: the flaw is "one question of its own" while the flaw bullet allows combining past the cap — follow-up: same row.
- diff-bug #9: a maintainer question that carries no-one-asked leaves the `idea vet:` line without it — reject (false): that path has its own `maintainer decision:` line.
- diff-bug #10: build anyway leaves maintainers no sign that no one asked — follow-up: same row, since no plan or user text asks for a PR line.
- diff-bug #11: the exempt list omits security fixes, hangs, and data loss — follow-up: same row, since the user approved the list as written.
- diff-bug #12: the draft is recommended where a host has issues turned off — follow-up: same row; M329's question has the same shape.
- diff-bug #13: D-234's heading omits D-144, whose question list grows — fix now.
- diff-bug #14: T5 and the reader pass predate the claim audit's rewording — reject (false): this review reruns the readers and `verify`.
- diff-bug #15: README's "someone asked" leaves out a maintainer's agreement — fix now.
- diff-bug #16: the CHANGELOG entry has no test — reject (false): `cairn/PROFILE.md` exempts new skill rules from prose guards, and the reader runs check the behavior.
- blame-history #1: the call path counts where D-234 says "in a text the plan reads" — fix now: D-234 names the path.
- blame-history #2: one question marks two options as recommended — fix now.
- blame-history #3: D-234 says the check adds no record line, but the flaw and answer go in the `idea vet:` line — reject (false): that line already exists, and D-234 excepts the check by name either way.
- blame-history #4: "so this flaw is the question it gets" is ambiguous — reject (planned change): Scope states that reach.
- blame-history #5: the exempt list is wider than D-233's — reject (planned change): Scope and the user's approval state it.
- prior-review #1: a maintainer's agreement counts without M329's design-coverage test — reject (false): this check asks about demand, and M329's test still governs the design question.
- prior-review #2: a failed read gives the same "no one asked" sentence — reject (planned change): the question names the read, as Scope states.
- prior-review #3: a call that no read can reach settles the check on the user's word — reject (planned change): Scope states it, and the user picks it.
- ripple #1: rule (4) does not name the new check — reject (false): rule (4) governs a maintainer's agreement and is unchanged.
- ripple #2: the session-start text does not name the check — reject (false): same reason.
- ripple #3: README's rule (4) sentence and the new sentence give two standards for "asked" — reject (false): one is agreement and one is demand.
- ripple #4: "Work chosen at the set" does not list the outside-demand question — reject (false): "If it finds a flaw" covers it.
- ripple #5: the candidate row still lists the declined changes — reject (false): the row graduates at hygiene.
- ripple #6: the PR-body rule has no line for build anyway — follow-up: same as diff-bug #10.
- ripple #7: README's `/milestone-plan` row does not name the question — reject (style): the row summarizes the set.

Pass 2, on the fix commits. Readers on Haiku. Readers reran only for the sentences the fixes changed: step 2's no-separate-question sentence (AC2), step 3's recommendation (AC1), and the wait sentence (AC6). AC3, AC4, and AC5 stand on pass 1, whose sentences did not change in a way their cases read, except the two pass 2 fix-now edits named below.

- [AC1 evidence, pass 2] The rename case requires the question before any file, "no one in the texts read", what users see change, build anyway, someone already asked, and do not build as the recommended option, no draft, and the question alone allowed. Pass 1 holds for the row chosen at the set.
- [AC2 evidence, pass 2] Met. The reader requires one question, the maintainer question with its three options, and quotes "that question says so, and no separate question is posed". Issue #894 does not count, because the problem no longer occurs. The question says that no one asked and that the contour lines leave the panel.
- [AC3 evidence] Pass 1 above. Met.
- [AC4 evidence] Pass 1 above. Met.
- [AC5 evidence] Pass 1 above, and the pass 2 edit that a maintainer's no at a named place stops the plan agrees with the outcome that a no is a flaw. Met.
- [AC6 evidence, pass 2] The speedup requires the outside-demand question and not the maintainer question, with the draft first and recommended, and quotes "so this flaw is the question it gets". The draft says what goes wrong for a user, goes to the temp file, posts nothing, writes no milestone file, and a new parked row says `promote when someone asks for it`. The rerun offers waiting in the draft's place and writes no file. Met.
- [AC7 evidence] `cairn/DECISIONS.md` D-234 states the check and D-108's door, says a text settles this check only as an annotation of D-204, and rejects the `cairn_next` change, the review follow-up change, and owner mode and `/hotfix`, each with a falsifier. README and CHANGELOG's Unreleased section state the check. Met.
- [AC8 evidence] At 7e65808c: scripts, hooks, plugin validate, marketplace validate (no `plugins[N].version` warning), and `claude plugin test` (2466 pass, 0 fail) exit 0. `cairn_validate` passes with the sizing advisory only, and the hand-run `skills/tests` exit 0. The rulebook measures 892 lines / 88,366 bytes, matching its seed. The commit after it rewraps two lines. Met.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: **someone already asked** goes on even when the thread holds a maintainer's no — fix now, fixed 7e65808c.
- diff-bug #2: a cited PR's body goes unread — fix now, fixed 7e65808c.
- diff-bug #3: the maintainer question has no option to name a person who asked — follow-up: row "Tighten the outside-demand check edges".
- diff-bug #4: a maintainer's no can read as two flaws — follow-up: same row.
- diff-bug #5: the checkout held an uncommitted edit — reject (false): the session's own Copilot fix, committed in 7e65808c.
- diff-bug #6: CHANGELOG lacked the maintainer's agreement that README gained — fix now, fixed 7e65808c.
- diff-bug #7: Scope says "each issue" where the skill reads an issue or PR — reject (false): the read recipe treats a PR as an issue, and the Scope's promise holds.
- diff-bug #8: prep work split from an asked-for change draws the question — follow-up: same row.
- diff-bug #9: three lines broke the wrap — fix now, fixed 7e65808c and the rewrap commit after it.
- blame-history #1: D-234's "adds no record line" against the draft's parked row — reject (false): the row is M329's existing shape, and D-234 excepts the check by name either way.
- blame-history #2: D-234 did not put the draft first — fix now, fixed 7e65808c.
- blame-history #3: the read runs on every guest plan of non-fix work — reject (planned change): Scope states it.
- blame-history #4 and #5: wrap — fixed with diff-bug #9.
- blame-history #6: README omits the operator and bot exclusion — reject (style): "another person" implies it.
- prior-review #1: a rerun overwrites an edited draft, now for a second kind of draft — follow-up: same row.
- prior-review #2: the wait conditions differ behind "as above" — reject (planned change): this check counts any person, and diff-bug #7 of pass 1 chose that wording.
- prior-review #3: a closed issue or PR that nothing cites goes unread — follow-up: same row.
- ripple: no ripple evidence.
- snapshot files: `git diff --name-only origin/main...HEAD` lists none.
- conversation: copilot-pull-request-reviewer PR — noted, its one thread below.
- copilot: skills/milestone-plan/SKILL.md:491 — fix now, the failed read is now "any failed read", fixed 7e65808c.
- Copilot level: Lite (set by GitHub's settings)
