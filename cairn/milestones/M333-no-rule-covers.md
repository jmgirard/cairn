# M333: Say so when no rule covers a task

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP4
- **Resolves:** —
- **Surface tier:** user-facing — every adopting repo's sessions get the new text
- **Branch/PR:** m333-no-rule-covers

## Goal

A session in a cairn repo says so when no route or rule covers its task, instead of fitting the task to the nearest rule.

## Scope

**In:** A fixed part in `hooks/session_context.py`, emitted in owner and guest mode ahead of the ROADMAP part. One hook test. A decision entry. README, DESIGN, and CHANGELOG lines.

**Out:** A line in the CLAUDE.md section template, because repair does not update an existing section and D-009 confines the section to routing (the decision entry records this). Extending the idea vet past `/milestone-plan` and `/hotfix` → candidate row "Extend the idea vet past plans and fixes". A PR review skill → candidate row "Add a skill for reviewing others' PRs". Updating existing owner repos' CLAUDE.md sections → candidate row "Detect drift in scaffold file content".

## Acceptance criteria

- [ ] AC1: With `cairn/PROFILE.md` naming no collaboration mode, and again with `# Collaboration mode: guest`, the context `hooks/session_context.py` emits for a `startup` SessionStart holds this text as one line, ahead of the `## cairn/ROADMAP.md` part: "If no cairn route or rule covers a task, say so before you start, and name what you are guessing. Look at how this repo already does that work, or ask the user. Do not apply the nearest rule and present the result as the normal way."
- [ ] AC2: In both modes, with a ROADMAP large enough that the hook truncates it, the emitted context still holds the AC1 text whole and is no longer than `MAX_CHARS`.
- [ ] AC3: `git diff main...HEAD -- skills/shared/templates/claude-md-section.md CLAUDE.md skills/shared/tracking-rules.md` is empty on the branch.
- [ ] AC4: `cairn/DECISIONS.md` gains one entry whose heading names D-009 as narrowed. It states that this conduct lives in the session hook rather than the rulebook, the rejected placements (the CLAUDE.md template with the repair path, and the rulebook) with the reason each lost, what the text does not reach (a session after `/clear` or compaction), and this falsifier: a session that still fits the nearest rule with the text in its context.
- [ ] AC5: `README.md`, `cairn/DESIGN.md`'s hook description, and `CHANGELOG.md`'s Unreleased "Changes that affect existing repos" section each state that a session gets this text in both modes. The README and CHANGELOG lines also state that it reaches a repo at its next session after a plugin update with no repair step, and that it is not injected again after `/clear` or compaction.
- [ ] AC6: A fresh reader, given the AC1 text and the template's `## Project tracking` section, answers (a) yes, (b) no, (c) no to whether the AC1 text tells the session to say so before it starts, for: (a) a request to review another person's PR and report back, without adopting it, (b) a question about what a function does, (c) a report of a user-visible crash.

## Coverage

- AC1 → T1, T2
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T4
- AC6 → T5

## Tasks

- [x] T1: In `hooks/session_context.py`, add a fixed constant holding a `## Work no rule covers` heading and the AC1 text as one line. Append it to `parts` in `build_context` after the guest block, before the shelf part, so it is charged against `MAX_CHARS` and comes before the ROADMAP part. It needs the `## ` heading: without one, two guest tests that read the mode part fail. Update the module docstring's list of parts.
- [x] T2: In `hooks/tests/test_hooks.py`, add one test with a subtest per mode. It checks the AC1 literal, written out in the test, and its place ahead of the ROADMAP part. It then writes an oversized ROADMAP and checks that the literal is still whole and the length is at most `MAX_CHARS`.
- [x] T3: Append the decision entry (D-238) to `cairn/DECISIONS.md` per AC4.
- [x] T4: Write the README, DESIGN, and CHANGELOG lines per AC5, the README's near its other notes on session-start text. Grep the repo for other text that lists what the hook injects.
- [ ] T5: Spawn a fresh reader for AC6 with neutral case wording and no hint of the answers. Ask it to quote the deciding words. If it answers (b) yes, the text is too broad: that is an amendment the user sees, since the text is the user's wording, so stop and ask. If it answers (a) no, the text's condition does not fire on the case that caused this work: stop the same way.

## Work log

- 2026-11-04: created by /milestone-plan. Source: the easystats orchestrator's finding on modelbased#701, weighed in this session; the user chose "Plan it" on the proposal.
- 2026-11-04: tier check: milestone — a new text in a running hook, not a bug fix or a tracking edit.
- 2026-11-04: idea vet: gap, "task" could read as every request, so a plain question gets the notice; reading taken: a task is work, as "that work" in the same text says, and AC6 case (b) tests it. Gap, a session with no rulebook loaded judges coverage only from what it holds; reading taken: accept, since the router sends non-trivial work to a skill first. No flaw.
- 2026-11-04: lessons used: 2026-07-24 (M112), the wording has more surfaces, so AC5 and T4 name them and a CHANGELOG entry; 2026-11-02 (M329), give a reader what the case rests on, so AC6 gives it the router; 2026-11-02 (M330), rerun a reader case after a later edit to its text.
- 2026-11-04: collision check: D-009 says "Conduct stays in `tracking-rules.md`, delivered when a skill fires"; this text is conduct outside the rulebook, so the entry narrows D-009 and leaves the router rule as it is. D-094 puts the hook's fixed text out of the always-read frame, as "a fixed string no repo writes to". D-108's door does not apply: the text is not about verification or records. M288 and M315 are the precedents for a hook part.
- 2026-11-04: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-11-04: placement evidence: of 24 repos under `~/github` with the CLAUDE.md section, 17 lack the route line that M232's template edit added on 2026-10-10; the section is 29 lines against a limit of under 30; `session_context.py` on the modelbased clone emitted 29,802 of 30,000 characters, so this text there makes the hook cut milestone or ROADMAP text, and the hook says so.
- 2026-11-04: plan gate chose the session hook over the CLAUDE.md template with a repair step because repair does not rewrite an existing section and the section has no free line; falsified by sessions that lose the text after `/clear` or compaction and then fit the nearest rule.
- 2026-11-04: plan gate chose the session hook over a rulebook line because the rulebook reaches no session that runs no skill, which is the case this work answers; falsified by a skill session whose context lost the hook text and that fits the nearest rule.
- 2026-11-04: question set: none posed; the user's request settled the wording and placement, and nothing foreseen needs the user before the merge question.
- 2026-11-04: criteria audit (full): an Opus reader ran the text in a scratch extract; tests and budget held with a `## ` heading. Fixed: AC1 and AC2 dropped their test clauses, instrument properties, moved to T2; AC2 names both modes; AC3 uses `main...HEAD`; AC4 says narrowed, not annotates; AC6 gives the reader the router, drops the stipulation in case (a), and moves the quote and record acts to T5 and review. Rejected: adding "Answering a question is not a task here" to the text, because the user approved the wording; T5 stops and asks if case (b) fails.
- 2026-11-04: cut: the user asked for "one hook test", T2 is one test with a subtest per mode. The two other items the session weighed are candidate rows, and the drift row gains the placement evidence.
- 2026-11-04: T1, T2: the test failed on the missing text in both modes, then passed with `NO_RULE_PART`; hook suite green, 212 tests. The part sits after the guest block, as the plan's T1 says.
- 2026-11-04: T3, T4: D-238 written, README, DESIGN, and CHANGELOG lines added; the sweep found no other list of what the hook injects. The simple-english lint hook flagged hundreds of existing README and CHANGELOG lines; the milestone reworded only its own lines and left the rest, which are out of scope.

## Decisions

## Review
