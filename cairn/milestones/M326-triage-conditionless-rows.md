# M326: Let triage settle rows with no condition

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, GP1
- **Resolves:** —
- **Surface tier:** user-facing — it changes what `/cairn-triage` proposes and how `/milestone-review` writes rows in every adopting repo
- **Branch/PR:** m326-triage-conditionless-rows

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

- [ ] AC1: `grep -n -i 'candidate row'` over `skills/milestone-review/SKILL.md` and `skills/copilot-review/SKILL.md` lists the passages that file a row. Each passage that files a row for a finding states the condition rule or points to the rulebook's "Candidate priority token" paragraph. That paragraph states the rule and the default "promote when a user reports it" for a finding that no documented or common use reaches.
- [ ] AC2: Step 2 of `skills/cairn-triage/SKILL.md` holds the "No condition" class, checked after Readiness and before Title. It never fires on a `[high]` row. It proposes either a *not worth keeping* `drop` or a condition change with `priority: <level> → parked`. Step 2's `drop` row lists *not worth keeping* as a fourth class with its row-only test.
- [ ] AC3: The condition change runs through the pass. Step 3's table reason and chip name it with its row. Amend can decline it, which also declines its move to parked, or reword its condition. These sites each name it beside priority and token changes: the untouched-items rule, *Accept as proposed*, step 4's skip test, step 4's size count, step 5's list of changes with no decision entry, step 6's stamp, and step 7's status line.
- [ ] AC4: Step 4 states where the condition text goes. It names the ` — ` opener for a row with no `: ` before that place, so the short title stays the same.
- [ ] AC5: Step 3's table reason names a *not worth keeping* drop by its class and the row text it read. Step 5 writes the pass's decision entry when such a drop is accepted, and lists each one in it. The stamp and commit body name it too, and in guest mode the stamp.
- [ ] AC6: A fresh subagent reads the revised `skills/cairn-triage/SKILL.md`. It runs steps 1 to 3 read-only over jmgirard/wrapped's `cairn/ROADMAP.md` and `cairn/DESIGN.md` at commit `796d6fa`. One planted `[high]` row with no condition is added to the copy. The open-PR read is taken as empty, and the run stops at the table. Each enumerated row that states no condition gets a non-`keep` disposition or a condition change, unless a started token, a live milestone, Overlap, or the `[high]` rule holds it. The planted row stays `keep`. At least one *not worth keeping* drop and one condition change appear.
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
- [ ] T3: Wire the condition change and the new drop through steps 3 to 7: table, chip, Amend, untouched rule, skip test, size count, placement rule, decision entry, stamp, status line.
- [ ] T4: Update README's candidate and triage text and add a CHANGELOG entry. Add prose guards in `skills/tests` for the class, the drop class, the placement rule, and the review rule.
- [ ] T5: Run AC6's dry run in a fresh subagent and record its table. Run `verify`, `skills/tests`, and `cairn_validate`.

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

## Decisions

## Review
