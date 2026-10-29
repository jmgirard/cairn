# M326: Let triage settle rows with no condition

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, GP1
- **Resolves:** —
- **Surface tier:** user-facing — it changes what `/cairn-triage` proposes and how `/milestone-review` writes rows in every adopting repo
- **Branch/PR:** m326-triage-conditionless-rows, https://github.com/jmgirard/cairn/pull/339

## Goal

`/cairn-triage` proposes a change for a candidate row that states no promotion condition, and review files each follow-up row with a condition.

## Scope

**In:**
- `/cairn-triage` step 2 gets a "No condition" evidence class. The pass checks it after Readiness and before Title. It applies to a candidate row that states no promotion condition, that is not `[high]`, and that no earlier class decided. A merge survivor counts as decided.
- For such a row, the class proposes one of two things. One is a `drop` under a fourth drop class, *not worth keeping*. The other is a condition change with `priority: <level> → parked`.
- The test for *not worth keeping* reads the row alone. The row cites no issue and no user report. The effect it names is an error, a warning, a cosmetic flaw, or slow running on a rare input. A wrong result with no error or warning never passes the test.
- A condition change is a row fact beside the disposition, like a token change. It rides on `keep`, `compress`, or `retitle`. It writes `; promote when <condition>` before the row's ` — added` provenance. If the row has no such provenance, the text goes at the end, before any started token. Where no `: ` comes before that place, the text opens with ` — ` instead of `; `. So the short title does not change.
- Declining a condition change at Amend also declines its move to parked.
- The pass's decision entry lists each accepted *not worth keeping* drop, so search-first finds it.
- `/milestone-review` writes `promote when <condition>` on each candidate row it files for a finding. If no documented or common use reaches the finding, the condition is "promote when a user reports it". `/copilot-review`'s defer route does the same. The rulebook's writer rule then opens such a row with `[parked]`.
- One D-entry for the change. README, CHANGELOG, and prose guards in `skills/tests`.

**Out:**
- A separate backfill mode: the next default `/cairn-triage` pass proposes a condition or a drop for each such row, as AC6 shows on wrapped.
- A nudge to run `/design-interview` when DESIGN.md has no principles → parked candidate row "Suggest a design interview in triage".
- Rows that implement, plan, or `/hotfix` file for deferred work keep their current shape. That work is wanted, and triage's new class still reaches those rows.

## Acceptance criteria

- [x] AC1: `grep -n -i 'candidate row'` over `skills/milestone-review/SKILL.md` and `skills/copilot-review/SKILL.md` lists the passages that file a row. Each passage that files a row for a finding states the condition rule or points to the rulebook's "Candidate priority token" paragraph. That paragraph states the rule and the default "promote when a user reports it" for a finding that no documented or common use reaches.
- [x] AC2: Step 2 of `skills/cairn-triage/SKILL.md` holds the "No condition" class, checked after Readiness and before Title. It never fires on a `[high]` row. It proposes either a *not worth keeping* `drop` or a condition change with `priority: <level> → parked`. Step 2's `drop` row lists *not worth keeping* as a fourth class with its row-only test.
- [x] AC3: The condition change runs through the pass. Step 3's table reason and chip name it with its row. Amend can decline it, which also declines its move to parked, or reword its condition. These sites each name it beside priority and token changes: the untouched-items rule, *Accept as proposed*, step 4's skip test, step 4's size count, step 5's list of changes with no decision entry, step 6's stamp, and step 7's status line.
- [x] AC4: Step 4 states where the condition text goes. It names the ` — ` opener for a row with no `: ` before that place, so the short title stays the same.
- [x] AC5: Step 3's table reason names a *not worth keeping* drop by its class and the row text it read. Step 5 writes the pass's decision entry when such a drop is accepted, and lists each one in it. The stamp and commit body name it too, and in guest mode the stamp.
- [x] AC6: A fresh subagent reads the revised `skills/cairn-triage/SKILL.md`. It runs steps 1 to 3 read-only over jmgirard/wrapped's `cairn/ROADMAP.md` and `cairn/DESIGN.md` at commit `796d6fa`. One planted `[high]` row with no condition is added to the copy. The open-PR read is taken as empty, and the run stops at the table. Each enumerated row that states no condition gets a non-`keep` disposition or a condition change, unless a started token, a live milestone, Overlap, or the `[high]` rule holds it. The planted row stays `keep`. At least one *not worth keeping* drop and one condition change appear.
- [ ] AC7: `README.md` and `CHANGELOG.md` describe the new class, the fourth drop class, and the review rule. `git grep -n -i -E 'three classes|refuted premise|on principle'` over `README.md`, `skills/`, and `CHANGELOG.md`, outside released CHANGELOG sections, lists hits. Each hit is read and is not stale. The `verify` slot, the hand-run `skills/tests`, and `scripts/cairn_validate.py` pass.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3
- AC5 → T2, T3
- AC6 → T5
- AC7 → T4, T5

## Tasks

- [x] T1: Write the D-entry. Add the condition rule to tracking-rules "Candidate priority token". Then edit `skills/milestone-review/SKILL.md` step 5's follow-up and the other passages AC1's grep lists, and `skills/copilot-review/SKILL.md:88`.
- [x] T2: In `skills/cairn-triage/SKILL.md` step 2, add the "No condition" class and the fourth drop class. Add the class's place in the evidence order.
- [x] T3: Wire the condition change and the new drop through steps 3 to 7: table, chip, Amend, untouched rule, skip test, size count, placement rule, decision entry, stamp, status line.
- [x] T4: Update README's candidate and triage text and add a CHANGELOG entry. Add prose guards in `skills/tests` for the class, the drop class, the placement rule, and the review rule.
- [x] T5: Run AC6's dry run in a fresh subagent and record its table. Run `verify`, `skills/tests`, and `cairn_validate`.

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: milestone — design change to two skills and the rulebook, more than one sitting.
- 2026-10-29: idea vet: gap — the reporter's default condition named "a render fails", which fits wrapped only; reading taken: "promote when a user reports it". gap — a separate backfill mode; reading taken: the default pass's new class does the backfill. No flaw.
- 2026-10-29: collision check: no archive milestone or D-entry covers condition-less rows. D-108's door applies (a rule about records); it passes on its trigger, since triage in wrapped kept every review-filed row on each pass. D-027 (drop classes), D-134 and D-184 (tokens, parked) are annotated, not superseded.
- 2026-10-29: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-29: lessons used: 2026-07-24 (M112, extended M249) doc surfaces and CHANGELOG task; 2026-08-17 (M148, extended M182) prose-guard markers; 2026-08-22 (M152, extended M287) decision change owes a D-entry; 2026-07-16 (M56+M65) run each gating suite.
- 2026-10-29: criteria audit (full mode, fresh Opus reader): 8 findings, all taken narrower. Short title kept by a ` — ` opener (AC4). No firing on `[high]` rows. Condition change wired through all listing sites, and declining it declines parked. D-entry added, and drops are listed in a decision entry for search-first. Drop test reads the row alone. Dry run pinned to `796d6fa` with a planted `[high]` row. Review rule covers every row-filing passage found by grep. Stale-wording grep widened and each hit read.
- 2026-10-29: question set: low-value drop — park or drop; review rows — condition at filing; design-interview nudge — parked candidate.
- 2026-10-29: plan gate chose a condition change as a row fact over a ninth disposition, because D-027 fixes the vocabulary and token changes set the pattern; falsified by an Amend flow that cannot express a condition change without a disposition.
- 2026-10-29: plan gate chose a decision entry for *not worth keeping* drops over the stamp alone, because D-027 recorded its YAGNI drop so search-first finds it; falsified by a dropped row refiled because the sweep missed it anyway.
- 2026-10-29: remainder ledger: review rows born with a condition → M326; triage proposes for condition-less rows → M326; value-based drop → M326; backfill → M326 by the default pass (AC6); Known issues at the review gate → not built, triage's route class covers accepted limitations; design-interview nudge → parked candidate row, at the user's choice.
- 2026-10-29: branch m326-triage-conditionless-rows cut from main at 4d201653; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-29: T1 done: D-227; the rule sits in tracking-rules "Candidate priority token". In `/milestone-review`, step 5's follow-up states it, and the snapshot and PR-conversation follow-ups point to it. `/copilot-review` step 5 points to the rulebook. The descope remainder at review line 261 is wanted work, not a finding, so it is unchanged.
- 2026-10-29: T2 done: step 2 gains the No condition class after Readiness and before Title. The `drop` row names *not worth keeping* as its fourth class, with the row-only test. A merge survivor and a `[high]` row are outside the class.
- 2026-10-29: T3 done: the condition change is wired through the table, chip, Accept, Amend (decline drops parked too, or reword), the fifth untouched carve-out, the skip test, the placement rule, the size count, step 5's no-entry list, the stamp, and the status line. A not-worth-keeping drop writes the pass's decision entry and is named in the commit body and stamp. Placement: before ` — added ` with `; ` when the first `: ` comes first, else at the lineage clause's place with ` — `, chosen because a row whose first `: ` sits after ` — added` would otherwise take the condition into its short title.
- 2026-10-29: T4 done: README's triage row and parked paragraph, a CHANGELOG entry under "Changes that affect existing repos", and `skills/tests/test_triage_conditionless_rows.py` (13 guards, exempt from the mutation registry like M298's file). Against main's triage skill, 10 of the 13 fail; the 3 that pass check the review skills, which main does not change. Three older guards and their harness blocks pinned sentences that this milestone extends, so they now read the new wording. `skills/tests` green, `cairn_validate` green.
- 2026-10-30: T5 dry run (fresh Opus, wrapped at 796d6fa with a planted `[high]` row, open-PR read empty): 31 candidates, 29 with no condition. It proposed 5 *not worth keeping* drops and 19 condition changes, plus a route, a compress, and a split. The planted `[high]` row stayed `keep`. Gaps found: a §7 group `keep` (Cut the Ubuntu mirror) and an Overgrowth `compress` (Test small wrap-lines stops) skipped the class; fixed so both take a condition change. The reader was unsure whether "on a rare input" covered all four effects; the test now says "either only a rare input reaches it or it changes no output". Pre-existing notes, not this milestone's: Overgrowth splits a row with two "or" triggers for one piece of work, and §7's "filed finding" wording differs between the skill and records-hygiene. Review's AC6 run reads the fixed skill.
- 2026-10-30: claim audit: 40 claims read, 5 corrected — CHANGELOG.md, README.md, skills/tests/test_triage_conditionless_rows.py (the held-row exceptions in the two docs; the test docstring and two tests' assertions).
- 2026-10-30: minor amendment at review: T4's new prose-guard file removed per M323's practice (prior-review #2); the three edited older guards and the re-seeded rulebook-mass pins stay.
- 2026-10-30: verify green on the T4 head: scripts/tests, hooks/tests, both plugin validates, and plugin test (2466 pass); skills/tests and cairn_validate green after the T5 fixes.

## Decisions

## Review

- 2026-10-30: Copilot arm: PR #339 opened at review start, header recorded and pushed; feature cap read 0 open PRs. The request exited 0, but the state query still read `none`: "Copilot request on PR #339 may not be recorded by GitHub (used-up Copilot credits are one cause)". No second request.
- AC1: `grep -n -i 'candidate row'` over both review skills lists 21 lines. The passages that file a row for a finding are review 410 (step 5 follow-up, states the rule and the default), 558 (snapshot follow-up, "with step 5's promotion condition"), 613 (PR-conversation follow-up, same), and copilot-review 88-90 (points to the rulebook paragraph). Review 922-929 (hygiene's new row for deferred findings) files step 5's follow-ups, which step 5's sentence "Every other row this skill files for a finding follows the same rule" covers. 261 is a descope remainder, not a finding; the rest name rows without filing one. tracking-rules 260-263 states the rule and the default. Met.
- AC2: `skills/cairn-triage/SKILL.md` step 2 holds "No condition → `drop` or a condition change" after Readiness and before Title, skipping `[high]` rows; the `drop` row lists *not worth keeping* as the fourth class with its row-only test. Guards `test_class_sits_between_readiness_and_title`, `test_class_skips_high_rows`, `test_class_proposes_a_condition_and_parked`, `test_fourth_drop_class_reads_the_row_alone` pass (14/14 in the file). Met.
- AC3: read steps 3-7: table reason cell format, chip names each condition change, Accept applies it, Amend declines it with its parked move or rewords it, fifth untouched carve-out, skip test, size count, step 5 no-entry list, stamp, status line. Guards `test_decline_drops_parked_too`, `test_skip_test_counts_it` and the updated priority-token guards pass. Met.
- AC4: step 4 places the condition before ` — added ` with `; ` when the first `: ` comes first, else at the lineage clause's place with ` — `, and says the short title stays the same. Guard `test_placement_keeps_the_short_title` passes. Met.
- AC5: step 3 names the class and quotes the effect from the row; step 5 writes the decision entry for an accepted *not worth keeping* drop and lists it; step 6's commit body and the guest stamp name it. Guards `test_decision_entry_lists_the_drop`, `test_commit_body_names_it`, and the guest-triage stamp guard pass. Met.
- AC6: fresh Opus dry run on the head at 96f06992 (the ripple fixes after it change no step-2 rule), over wrapped's ROADMAP and DESIGN at 796d6fa plus a planted `[high]` row, open-PR read empty, stopped at the table. 31 candidates, 29 with no condition. Each of the 29 got a non-`keep` disposition (8 *not worth keeping* drops, 4 routes, 1 split, 1 promote) or a condition change (14, including a §7 `keep`), except the planted `[high]` row, which stayed `keep`. Met. The reader's notes on the drop test: a wrong result that comes with a warning, rows naming only "untested", and no measure of "rare". These are judgment edges the gate settles, and the wording matches D-205's `edge` test.
- spawned: diff-bug, blame-history, prior-review, ripple
- ripple #1: lessons-pass text at triage SKILL.md:202 still said "three drop reason classes" — fix now
- ripple #2: the skill's description named only principled drops as recorded in a decision — fix now
- ripple #3: the close's safety line named only principled drops as returning by supersession — fix now
- ripple #4: `/hotfix` and `/milestone-implement` file finding rows with no condition — reject, planned change: Scope Out keeps those rows' shape, and the triage class still reaches them
- ripple #5: step 4's "`keep` changes nothing of its own" ignores the condition change — fix now
- ripple #6: no skill clears `[parked]` from a row whose condition is "a user reports it" — reject, false: triage step 3 re-rates a parked row whose condition held to normal
- ripple #7: README and CHANGELOG stated the drop test as "on a rare input", narrower than the skill's "or changes no output" — fix now
- ripple #8: copilot-review cites the rulebook paragraph and not the parked default — reject, false: the cited paragraph states the default, and AC1 accepts a pointer
- prior-review #1: the rulebook grew to 851 lines / 84,189 bytes, but `/milestone`'s baseline and its two pins still read 848 / 83,903 (M211, M235 records) — fix now, re-seeded at all three sites
- prior-review #2: M323 removed new prose guards and mutation entries because the profile says new skill rules owe none; this milestone added `test_triage_conditionless_rows.py` — fix now, file and its EXEMPT entry removed; the three older guards stay updated to the new wording
- prior-review #3: the condition placement does not check a started token, unlike the lineage rule (M298 record) — reject, false: the `; ` branch puts the text before ` — added `, which comes before any started token, and the other branch uses the lineage place
- prior-review #4: the No condition class does not restate the PR-named exemption (D-191) — reject, false: step 2 holds a PR-named row at `keep` "before §7 and every class below"
- prior-review #5: the class order does not say Title still runs on a row with a condition change — reject, false: such a row stays `keep`, which is Title's input
- prior-review #6: a row citing an issue can be parked — reject, planned change: the drop test spares issue rows from a drop, and a condition plus parked is the class's other branch for any row with no condition
- diff-bug #1: the No condition class could write a condition and parked on a row a live milestone absorbs — fix now, the class skips such a row
- diff-bug #2: tracking-rules' guest triage stamp named only refuted-premise and already-shipped evidence — fix now
- diff-bug #3: `skills/shared/copilot-review.md` files Copilot follow-ups for `/hotfix` with no condition — reject, planned change: Scope Out leaves `/hotfix`'s rows as they are, and triage's class reaches them
- diff-bug #4: placement put the condition after ` — added ` for a row with no `: `, against Scope and compress's shape — fix now, it goes before ` — added ` with ` — ` there; the lineage place is kept only when a `: ` follows ` — added `
- diff-bug #5: class order unclear for Title after a condition change — reject, false: the row stays `keep`, Title's input
- diff-bug #6: a parked row with no condition got `parked → parked` — fix now, no priority change for a row already parked
- diff-bug #7: hygiene's unpark check reads each new parked review row — reject, false: it judges each condition, and "a user reports it" does not hold at a merge
- diff-bug #8: step 5's "two kinds of removal" header and "named there too" were loose — fix now
- diff-bug #9: the review rule states parked only for the default condition — reject, false: the rulebook's writer rule parks any condition not held
- diff-bug #10: D-227's heading said "drop classes" and did not name D-134; the door covered only triage — fix now, heading and door corrected before merge
- diff-bug #11: Amend did not say what a bare named item does to a condition change, or how a typed `: ` is written — fix now
- diff-bug #12: a drafted condition quoting another row's title would form a §7 group — fix now, the condition quotes no other row's title
- diff-bug #13: more triage D-entries raise the id-collision risk when the remote moved ahead — follow-up, absorbed by the existing row "Support two cairn operators in one repo", which already names duplicate D-numbers; no edit
- diff-bug #14: Overlap's survivor draft and the PR-named sentence list only priority and token changes — reject, false: the class skips both kinds of row
- diff-bug (c): the new guard file's docstring and one weaker assertion — reject, moot: the file was removed (prior-review #2)
