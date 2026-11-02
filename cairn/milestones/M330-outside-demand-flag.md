# M330: Ask who wanted the work in guest plans

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — `/milestone-plan` text that every guest repo runs
- **Branch/PR:** m330-outside-demand-flag

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

- [ ] AC1: Reader run on a request that names a candidate row. The session filed the row at an earlier plan. The row renames an internal helper with no change users can see, and no issue, comment, or review mentions it. The skill text requires a question at step 3 before any file is written for that work. The question says that no one in the texts read asked, and what users lose or see change. Its options include building anyway and not building, no draft option is offered, and the question can be the whole set. A second reader gets the same row chosen at the question set of a request that names no work. There the skill text requires a close block that names the concern, with a fenced `/milestone-plan` and the row's short title.
- [ ] AC2: Reader run on easystats/see M015's Goal, its sentence "It removed the contour lines from the panel for most well-fitting models", and the fact that its row came from the operator's own earlier plan. The case also holds the text of easystats/performance#894, the fact that a LOESS change settled that report, and no maintainer agreement. The skill text requires the maintainer question with its three options and no separate outside-demand question. That question's text says that no one asked and that the contour lines leave the panel.
- [ ] AC3: Reader run on these cases, one reader per case. The skill text requires no outside-demand question for each. The cases are a fix the session found for a function whose result differs from its cited formula, a fix the session found for a crash on an input the docs allow, and a fix the session found that restores documented behavior. Two more are a helper rename that another person's issue comment asks for, and AC1's case in owner mode. Where the maintainer question is still posed for such a fix, its text makes no statement on who asked.
- [ ] AC4: Reader run on AC1's rename with each of these, one reader per case. The skill text requires the question for each. The first is an issue whose reporter blames a different cause and names neither the rename nor a problem it fixes. The second is an issue by the operator's own login with no other person's text. The third is a bot's review note that asks for the rename. The fourth is a read of the operator's PRs that fails, and there the question names that read.
- [ ] AC5: Reader run on these outcomes for AC1's case, one reader per outcome. Building anyway writes the milestone file with an `idea vet:` line that names the flaw and the answer. Not building writes no file and leaves the row in place. Naming a place whose text asks for the rename goes on, and the line names the place. Naming a call that no read can reach goes on, and the line says the user named it. Naming a place whose text does not ask writes no file and ends with a close block. A maintainer's agreement that step 2 finds means no outside-demand question. A maintainer's no is a flaw that cites the no.
- [ ] AC6: Reader run on a speedup of a slow default that users hit, which changes no result or output, with no one outside asking. The skill text requires the outside-demand question and not the maintainer question, with a draft option. Choosing it writes the temp file with text that says what goes wrong for a user, shows the command in the close block, and posts nothing. It writes no milestone file, and a parked row with `promote when someone asks for it` when no row holds the work. A rerun with the operator's own open issue and no other person's reply offers waiting in place of the draft.
- [ ] AC7: `cairn/DECISIONS.md` holds an entry that states the check and D-108's door, and says that a text settles this check only, as an annotation of D-204. It rejects the `cairn_next` change, the review follow-up change, and owner mode and `/hotfix`, each with a falsifier. README and CHANGELOG's Unreleased section state the check.
- [ ] AC8: The `verify` slot's five commands exit 0 at the head, and `python3 scripts/cairn_validate.py` passes.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T3
- AC3 → T1, T3
- AC4 → T1, T3
- AC5 → T1, T3
- AC6 → T1, T3
- AC7 → T4
- AC8 → T5

## Tasks

- [x] T1: Edit `/milestone-plan`. Step 2 gains the outside-demand paragraph after "Maintainer decision". Step 3's maintainer question text, its flaw bullet, and "The maintainer question" gain the who-asked wording, the options, and the draft's parked row.
- [x] T2: Edit the rulebook's sentence "A guest plan's maintainer question can stand alone". Re-seed the rulebook mass in the `/milestone` skill line and the two hand-run pins.
- [ ] T3: Run the reader runs at the head. Give each case the record it rests on, in neutral words. If a reader disagrees with a criterion, read the sentence it quotes, then change the text or record why not before a new reader runs. Run AC1's first case and AC2 once at the plan commit as a baseline.
- [x] T4: Write the D-entry, README, and CHANGELOG. Search the repo for text that the change makes stale.
- [ ] T5: Run `verify`, `cairn_validate`, and the hand-run `skills/tests`. List added diff lines over 80 characters before the commit.

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

## Decisions

## Review
