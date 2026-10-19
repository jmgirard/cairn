# M284: A candidate row that waits on its trigger is parked, and the pane shows it last with an hourglass

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP3
- **Resolves:** —
- **Surface tier:** user-facing — the token rule, the cairn pane, validate, and triage ship to every adopting repo
- **Branch/PR:** m284-parked-candidate-token

## Goal

A candidate row whose promotion condition has not held opens with a `[parked]` token that the skills write and remove, and the cairn pane draws such rows last, each with a gray `⧗`.

## Scope

**In:** the `[parked]` opening token in tracking-rules and the `/cairn-init` skeleton comment. The readers that know the token's level: `reader.ts`, `cairn_next.candidate_texts`, and the `candidate order` advisory. The pane's mark and group. Token upkeep: `/cairn-triage` re-rates it as a priority level, and `/milestone-review` post-merge hygiene removes it from a row whose condition the merge made hold. README, DESIGN.md, CHANGELOG, a D-entry, and this repo's own rows.

**Out:** a check that every row with a promotion condition carries the token. D-134 rejected a token check, and the decision stands. A token that keeps a parked row's importance (`[low]` and `[parked]` together): the row takes one opening token. A copy of the token in adopting repos' ROADMAPs: their operators run `/cairn-triage`, which proposes it (the CHANGELOG says so).

## Acceptance criteria

- [ ] AC1: tracking-rules "Candidate priority token" defines `[parked]` as a fourth opening token, in place of `[high]` or `[low]`, for a row whose promotion condition has not held. It orders the Candidates section high → normal → low → parked. It says that whoever adds a row writes `[parked]` when the row states a promotion condition that does not hold at that time. It says that the token goes when the condition holds, at `/cairn-triage` or at `/milestone-review` post-merge hygiene. "Candidate short title" removes a leading `[parked] ` as it removes `[high] ` and `[low] `. The `/cairn-init` skeleton comment names `[parked]` and the order high → normal → low → parked.
- [ ] AC2: `candidateTexts` in `hooks/status/reader.ts` and `candidate_texts` in `scripts/cairn_next.py` read a row that opens with exactly `[parked] ` as level `parked`, with the token removed from the text. Any other spelling reads as `normal`, as a misspelled `[high]` does today. `high_title` and the pane's next step never name a parked row. The `candidate order` advisory ranks `parked` below `low`: it WARNs on each row of another level that the file holds below a parked row, and it stays silent on a file in level order.
- [ ] AC3: In the cairn pane's Candidates list, a `parked` row draws a gray `⧗` in the mark position and its title in gray. The parked rows draw after the `[low]` rows, in ROADMAP order. A parked row's ✎, its key, and its press target follow the same rules as any other row's. The heading's count includes the drawn parked rows, and a started parked row is hidden like any started row.
- [ ] AC4: `/cairn-triage` reads `parked` as a priority level. Its step-1 table shows the level, and its misspelling clause does not read `[parked]` as a misspelling. A priority change can add `[parked]` (`priority: normal → parked`) or remove it (`priority: parked → normal`). A `promote` of a parked row replaces the token with `[high]`. Its apply step's token list and its order sentence name the fourth level. `/milestone-review` step 9 checks each `[parked]` row whose short title the milestone file quotes, or whose text names the milestone's id. Where the merge made that row's condition hold, step 9 removes the token, and the row reads `normal`.
- [ ] AC5: README's candidate paragraph, DESIGN.md's pane and reader descriptions, and an unreleased CHANGELOG entry state the token, the mark, and the order. The CHANGELOG entry tells an adopting repo to run `/cairn-triage` to have the token proposed for its rows. A D-entry records the decision. It passes D-108's door on its trigger, which is D-179's falsifier: the operator cannot tell a ready row from a waiting one. It narrows D-035's rejection of a "parked" label and D-134's statement that the no-grouping rejection stands. It supersedes D-179's consequence that `[high]` means "important" or "ready to plan", names D-180, and annotates D-182. It names the alternatives the plan rejected, among them keeping a parked row's `[low]` rating.
- [ ] AC6: Every row of this repo's `## Candidates` section opens with `[parked]`, except the rows that the work log names, each with its reason (its condition held, or it states none). The file is in level order, and the section's header line states the four-level order.
- [ ] AC7: The `verify` slot passes: both gating `unittest` suites, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test` for the status mod.

## Coverage

- AC1 → T1
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5, T6
- AC5 → T7
- AC6 → T8
- AC7 → T9

## Tasks

- [x] T1: Edit tracking-rules "Candidate priority token" and "Candidate short title" (`skills/shared/tracking-rules.md:239-266`) and the skeleton comment (`skills/cairn-init/SKILL.md:190-196`). Grep `skills/tests` for pinned slices of both before editing (LESSONS M148).
- [x] T2: Readers. Add `parked` to `CandidateRow['priority']` and the token list in `reader.ts`, and to `candidate_texts` in `cairn_next.py`. Add rows to the `candidates` fixture ROADMAP for `[parked] `, `[PARKED] `, `[parked]` with no space, and `[parked]` mid-row, and update its `expected.json`. Regenerate `fixtures.gen.ts` with `gen_fixtures.py`. The fixture test then holds both twins to the rows. Add a case where a parked row is first in the file and `high_title` names no row.
- [x] T3: `_LEVEL_RANK` in `cairn_validate.py:1845` gains `parked: 3`. Add tests for a low row below a parked row (WARN names the low row and the level `parked`) and for a file in level order (no WARN).
- [x] T4: Pane. `PRIORITY_MARK.parked` is a gray `⧗`, `LEVEL_RANK.parked` is 3, and a parked title draws gray. In `pane.test.tsx`, add `⧗` to the `MARKS` literal map and assert `PRIORITY_MARK` whole. Add cases for order, key, count, a started parked row, a parked row with an empty short title (no ✎), a parked row while a skill runs (no ✎), and a parked row first in the file that the next step does not name.
- [ ] T5: `/cairn-triage`: the step-1 priority list and misspelling clause, the re-rating clause, the promote clause, the apply step's token list, and its order sentence (`skills/cairn-triage/SKILL.md:248`, `:386-400`, `:478`, `:489`).
- [ ] T6: `/milestone-review` step 9: the parked-row check, beside the candidate-row graduation it already does. Each removal shows in the durable-record preview and in the archive summary's Review line, which already holds what hygiene graduated. Add a records-hygiene §1 sentence if §1 is the clause's home.
- [ ] T7: README, DESIGN.md, CHANGELOG, and the D-entry. Grep README and DESIGN for `high → normal → low` and for `↑`, `○`, `↓` lists, so that every restated order or mark list gains the new level (LESSONS M112).
- [ ] T8: Add `[parked]` to this repo's rows, log each row left without it, and move the rows into level order. Update the Candidates header line's order. Run `cairn_validate` to show the `candidate order` advisory silent.
- [ ] T9: Run the verify slot.

## Work log

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: milestone — new pane behavior, a new record token, and skill conduct across triage and review, with design choices.
- 2026-10-18: collision check: D-035 (flat list, triggers in row prose), D-134 (priority token, rejected a type/kind token), D-179 (`[high]` means important or ready, falsifier: operator cannot tell ready from waiting), and D-182 (pane level order). The token is per row and adds no section, so D-035's no-grouping decision stands. The new entry annotates all four. Shipped pane marks: M207, M253, M261, M280, extended here. No candidate row overlaps. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-18: question set: how the pane tells a waiting row — an explicit token that the skills write at row creation and update at milestone and triage (over reading the word "promote" in row prose).
- 2026-10-18: question set: look and order — a gray hourglass in the mark position, with parked rows as their own group below `[low]`.
- 2026-10-18: plan gate chose an explicit `[parked]` token over detecting the word "promote" in row prose, at the user's choice; prose detection would mark a row that triage promoted, and rows word triggers many ways; falsified by an operator who finds the token stale on rows whose condition held.
- 2026-10-18: plan gate chose one fourth level over a second token beside `[high]`/`[low]`, because the user asked for one group below low; falsified by an operator who needs a parked row's importance and cannot read it.
- 2026-10-18: named the token `[parked]`, not `[waiting]`, because the pane already has a Waiting section for planned milestones that wait on others.
- 2026-10-18: a parked row's title draws gray, like a `[low]` row's, since the group sits below low. Hygiene removing the token makes the row `normal`, not `[high]`, because "wanted now" is triage's call (`/cairn-triage` "Readiness → promote").
- 2026-10-18: criteria audit (full) on the first draft, which detected the word "promote": 11 findings, each fixed toward the narrower promise. The question set then replaced that design, so the criteria above went back through the audit (next line).
- 2026-10-18: criteria audit (full) on the token design: 10 findings, all fixed. AC1 adds `[parked] ` to the short-title rule and the order to the skeleton. AC2's WARN names the row below the parked row, as the check reports, and `high_title` never names a parked row. AC3's missing probe cases moved to T2 and T4. AC4's hygiene check is bounded to rows the milestone file quotes or whose text names its id, and its recording clause moved to T6. AC4 names triage's misspelling clause and order sentence. AC5 states each relation to D-035, D-134, D-179, D-180, and D-182, and records that parked `[low]` rows lose their rating. AC6 became a set a reviewer can check, plus the header line. AC7: no finding.
- 2026-10-18: a `[low]` row that takes `[parked]` loses its low rating: 13 of this repo's 24 rows are `[low]`. Recorded as a rejected alternative in the D-entry (AC5), and stated in the plan summary.
- 2026-10-18: implement started on branch m284-parked-candidate-token. Untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-18: T1 done. The tracking-rules token paragraph defines `[parked]` and the four-level order, "Candidate short title" removes `[parked] `, and the `/cairn-init` skeleton shows a parked row. `skills/tests/test_candidate_priority_token.py` and its mutation entries pin the new phrases (27 tests OK). Verify: all five green (scripts 423, hooks 179, mod 2132).
- 2026-10-18: T2-T4 done in one commit, because validate raises KeyError on a `parked` level that has no rank, and the mod tests draw every fixture. Both readers and the Python twin read `[parked] `. The new fixture `candidates-parked` holds the probe rows, so the existing `candidates` fixture's drawn lines stay as they were. `_LEVEL_RANK` and the pane's `LEVEL_RANK` gain `parked: 3`, and `PRIORITY_MARK.parked` is a gray `⧗` with a gray title. With the old readers, 3 of 5 new Python tests fail, each one reading `[parked]` as normal (the other 2 are controls). With the old `pane.ts`, 25 mod tests fail, 9 of them new M284 tests. Verify: all five green (scripts 428, hooks 179, mod 2184).
