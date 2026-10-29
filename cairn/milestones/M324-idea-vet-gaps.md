<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M324: Settle vague ideas and ask about flawed ones

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes what `/milestone-plan` and `/hotfix` ask adopters
- **Branch/PR:** m324-idea-vet-gaps

## Goal

The idea vet settles a concern that one fitting reading of the request avoids, and asks the user about a concern that no fitting reading avoids.

## Scope

**In:** `/milestone-plan` step 2's idea vet sorts each concern as a gap or a flaw. Step 3 asks about flaws, and about a gap only when fitting readings give the user different behavior. Step 4's `idea vet:` line tags each concern. `/hotfix` step 1's vet sorts concerns the same way. A flaw in a name, argument, or behavior that the fix's diff leaves as it was no longer stops a hotfix and becomes a candidate row. This absorbs the parked candidate row "Do not stop fixes on old naming flaws". The hand-run guard `skills/tests/test_idea_vet.py`, the README, the CHANGELOG Unreleased vet entry, and a D-entry that narrows D-204 follow.

**Out:** A fresh reader for the vet stays rejected (D-204), with no row. `/milestone` §4 gets no vet of its own (D-204's Consequences). A count of past misroutes is not possible, because archives keep no `idea vet:` line, so there is no row for it.

## Acceptance criteria

- [ ] AC1: `skills/milestone-plan/SKILL.md` step 2's **Idea vet.** paragraph sorts each concern it finds. If one reading of the request avoids a set of concerns, each of them is a gap. That reading fits the request's words and the records it cites. Its user-visible behavior is behavior that the request's words name or leave open. Nothing the request asks for is left out. A reading whose user-visible behavior differs from behavior the words name is not such a reading. A concern that this one reading cannot also avoid is a flaw.
- [ ] AC2: The same paragraph says that the plan drafts the criteria to that reading. The plan asks nothing about a gap, with one exception. That exception is a gap where another reading also fits the request and gives different user-visible behavior. Such a gap goes to step 3's set. Before the vet sorts a concern on a candidate row's request, it reads each record the row cites.
- [ ] AC3: Step 3's idea-vet bullet poses only flaws, each with an option not to build. It says that the agent never decides a flaw. Step 3's "choices that the request leaves open" bullet poses each gap that AC2 sends to the set. That question recommends the reading taken and has no option not to build. Step 3's "Work chosen at the set" arm ends with its goal-wrong close on a flaw. It ends the same way on a gap of AC2's exception. The agent decides any other gap there.
- [ ] AC4: Step 2 states the form of the `idea vet:` work-log line. Each concern is a clause tagged `gap` or `flaw`. A gap carries the reading taken, and a flaw carries the set's answer. With no concern, the line says that the vet found none.
- [ ] AC5: `skills/hotfix/SKILL.md` step 1's **Idea vet (M306).** paragraph sorts concerns by AC1's test. For a gap, the fix takes the reading, and the chat result names it. Step 6's approval chip question text also names a gap of AC2's exception as a choice. A flaw in a name, argument, or behavior that the fix's diff changes takes the over-the-bar route, as now. A flaw only in a name, argument, or behavior that the fix's diff leaves as it was does not stop the fix. Step 1 then adds a candidate row that names the flaw (search-first applies), and the hotfix goes on. On the merged-PR re-entry, a flaw goes in step 7's close block, and such a flaw also gets the candidate row. The guest change route's vet sentence gives a concern on the changed diff the same dispositions.
- [ ] AC6: On the branch head, the `verify` slot passes. That slot is both gating `python3 -m unittest` suites, `claude plugin validate` on both manifests, and `claude plugin test`.
- [ ] AC7: Four doc sites say that the agent settles a gap without a question unless its reading changes what you get. They also say that the agent asks you about a flaw. The sites are README.md's `/milestone-plan` row, its `/hotfix` row, and its "Answer two questions in a run" bullet. The fourth site is the CHANGELOG Unreleased entry "The plan and the hotfix question the request before they build it." The `/hotfix` row and that entry also say that a flaw in behavior the fix leaves as it was does not stop a hotfix.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T1
- AC5 → T3
- AC6 → T4, T6
- AC7 → T5

## Tasks

- [x] T1: Edit `/milestone-plan` step 2's Idea vet paragraph (`skills/milestone-plan/SKILL.md:257`) and step 4's Idea-vet line bullet (`:627`) (AC1, AC2, AC4). Add a gap example beside the winsorize flaw example.
- [x] T2: Edit step 3's choices-left-open bullet, its idea-vet bullet (`:389`), and the "Work chosen at the set" arm (`:401`) (AC3).
- [ ] T3: Edit `/hotfix` step 1's Idea vet paragraph (`skills/hotfix/SKILL.md:52`), the guest change route's vet sentence (`:224`), and step 6's approval chip text (AC5).
- [ ] T4: Update `skills/tests/test_idea_vet.py`. Re-pin each changed phrase, and add one assertion per new clause. Show each new pin red by deleting its clause, and log the hand-run `skills/tests` result. The mutation-harness EXEMPT entry stays.
- [ ] T5: Edit the three README vet sites and the CHANGELOG Unreleased vet entry (AC7). Append D-224, which narrows D-204 and names its D-108 door.
- [ ] T6: Run the `verify` slot on the branch head (AC6).

## Work log

- 2026-10-29: created by /milestone-plan.
- 2026-10-29: tier check: milestone — changes skill behavior and needs a design decision.
- 2026-10-29: idea vet: gap — "a reasonable reading" was undefined, resolved as one reading that fits the words and cited records, names or leaves open the user-visible behavior, and drops nothing asked; no flaw.
- 2026-10-29: lessons used: 2026-07-24 (M112, extended M249, used M323); 2026-08-17 (M148, extended M182, used M323); 2026-08-22 (M152, extended M287, used M323); 2026-07-16 (M56+M65, consolidated M78/M83/M124, extended M121/M138, corrected M144, trimmed M147, used M323).
- 2026-10-29: collision: narrows D-204 (decided at plan, D-224 at T5); extends M306 (archived); absorbs the parked row "Do not stop fixes on old naming flaws", whose promotion condition has not held, at the user's choice in the question set.
- 2026-10-29: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-29: door: D-108 passes. Narrowing what the vet asks is its carve-out. The tag and the hotfix row rest on the retained trigger: the shipped vet asked the user about vague cairn-written rows that the agent could settle (user report, 2026-10-29).
- 2026-10-29: criteria audit (full, fresh Opus reader): 10 findings, all taken. Gap test bound to user-visible behavior (1). One reading covers all gaps (2). Exception baseline is another fitting reading (3). "Unclear" replaced by a provenance read before sorting (4). Step 3 names which bullet poses a gap (5). D-108 door named (6). Hotfix gap exception at the approval chip (7). Old flaw bound to the fix's diff, and the merged-PR re-entry writes the row (8). Hand-run `skills/tests` dropped from AC6 per D-109 (9). AC7 names its four sites, not a grep (10).
- 2026-10-29: question set: a gap whose fitting readings give different behavior is asked, not decided — ask (recommended).
- 2026-10-29: question set: a hotfix flaw in what the fix's diff leaves as it was lets the fix go on with a candidate row — fix goes on (recommended).
- 2026-10-29: plan gate chose the one-reading test over a rule that only cairn-written candidate rows skip the vet question, because a user's own vague request has the same gaps and a cairn row can hold a real flaw; falsified by a gap the agent settled that the user would have read differently.
- 2026-10-29: M324 in-progress on m324-idea-vet-gaps; untracked `cairn-probe.log` and `tsconfig.json` left unstaged.
- 2026-10-29: T1 done: step 2's Idea vet sorts gap and flaw, reads a candidate row's cited records first, sends an exception gap as an open choice, and tags the `idea vet:` line; step 4's bullet already points at step 2's form, unchanged. Gap example added beside the winsorize flaw. Both suites green.
- 2026-10-29: T2 done: step 3's open-choices bullet takes an exception gap (reading recommended, no option not to build); the idea-vet bullet now poses only flaws; "Work chosen at the set" closes on a flaw or an exception gap, and the agent decides other gaps.

## Decisions

## Review
