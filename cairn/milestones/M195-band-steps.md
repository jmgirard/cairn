# M195: A milestone band that names every cairn step

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's session draws the band
- **Branch/PR:** m195-band-steps

## Goal

Make the milestone band name the cairn skill that is running and its current step, so that planning, the final checks, and post-merge hygiene show in the band.

## Scope

**In:**
- The mod in `hooks/status/` hooks `skill.prompt`. When a cairn skill's prompt is expanded, a new `step` session atom stores the skill. The atom is declared in `types/index.d.ts` under a shape tag.
- The mod hooks `tool.call` for `mcp__ccd_session__mark_chapter`, the desktop app's chapter tool. Every cairn skill already calls it at each step it names. After a main-loop call succeeds, the atom stores its title as the chapter, and the mod reads the tracking files again.
- Each `session.end` clears the atom.
- One label map in `band.ts` for the ten skills. A skill row for a running skill with no matching active milestone. An item row that shows the chapter.
- The close button's stored marks gain the skill, and the `dismissed` atom gets a shape tag.
- README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry.
- Accepted limit: `skill.prompt` carries no agent id, so a subagent that loads a cairn skill also sets the label.

**Out:**
- A header label that changes to `checks`, `merge`, or `hygiene` → not planned. The gate kept `review` and shows the step on the item row.
- Step text on the terminal, which has no chapter tool → the "Status mod follow-ons" candidate row, extended in this plan commit.
- A dim idle line between milestones → the "Band idle line" candidate row.
- The other band layout and close-state items → the "Band layout edge cases" and "Band close-state edge cases" candidate rows.

## Acceptance criteria

- [ ] AC1: The row that carries a running cairn skill shows that skill's label. A cairn skill has a `SKILL.md` under the cairn plugin's `skills/` directory. It counts when the engine expands its prompt by its bare name or its `cairn:` name. The labels come from one map in `hooks/status/band.ts`: milestone-plan `plan`, milestone-implement `implement`, milestone-review `review`, hotfix `hotfix`, cairn-triage `triage`, cairn-release `release`, milestone `status`, milestone-brief `brief`, design-interview `design`, cairn-init `init`. The prompts of `commit`, `other:hotfix`, and `cairn:nope` leave the band as it was. Shown by `claude plugin test` cases on terminal and desktop. They fire `skill.prompt` for each name in the skill list that `gen_fixtures.py` writes from that directory, in both spellings, and for the three other names.
- [ ] AC2: A running skill with no matching active milestone gets a skill row above the milestone rows. That is the case for a skill other than milestone-implement and milestone-review. It is also the case for milestone-implement with no `in-progress` row, and for milestone-review with no `review` row. A skill row shows the label and the skill's slash command, such as `/milestone-plan`, and nothing on its right side. Otherwise the first active row with the matching status carries the skill, and no skill row is drawn. Shown by plugin test cases on both surfaces: milestone-plan over `no-active` and `mixed`, hotfix over `mixed`, milestone-review over `single-in-progress`, and milestone-implement and milestone-review over `mixed`.
- [ ] AC3: The item row follows the session's chapters. A main-loop `mark_chapter` call can succeed after the running skill's prompt was expanded. The item row under the row that carries the skill then shows that call's title. The title replaces the next open task or criterion, or stands alone where the row has none. A skill row with no chapter has no item row. Each such call also reads the tracking files again, so the next drawing shows the counts at that call. Shown by plugin test cases on both surfaces over `mixed`. A milestone-review prompt and a `Post-merge hygiene` chapter put that title under M010. A fixture file edited between two chapter calls, with no turn end between them, draws the new counts. M010's ROADMAP status edited to `done`, then a chapter call, moves the chapter under M013. M013's ROADMAP status then edited to `done`, then a chapter call, moves it to a `review` skill row. A chapter call that a hook beneath denies leaves the item row as it was.
- [ ] AC4: Every session end clears the step. After `session.end`, the band shows the milestone rows alone, each labeled from its status as before M195. Any cairn skill's prompt, the same skill included, replaces the skill and drops the chapter. Shown by plugin test cases on both surfaces for the reasons `clear` and `resume`, and for a second milestone-review prompt after a chapter.
- [ ] AC5: The close button works with skill rows. It sits on the first header row, and a skill row counts as one. A press hides the band until the active ids and statuses, their ROADMAP order, or the running skill's name change. Shown by plugin test cases on both surfaces. After a press, a chapter call and a checked task box keep the band hidden. A different skill's prompt shows it again. A press on a lone skill row over `no-active` hides it.
- [ ] AC6: README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry describe the skill row, the ten labels, and the chapter on the item row. They say that the chapter text needs the desktop app's chapter tool. On the terminal, milestone rows show their next open item, and a skill row has no item row. They also say that a subagent that loads a cairn skill sets the label.
- [ ] AC7: The verify slot in `cairn/PROFILE.md` runs clean. It holds both Python suites, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T2, T3, T4, T6
- AC2 → T3, T5, T6
- AC3 → T1, T2, T3, T5, T6
- AC4 → T2, T6
- AC5 → T2, T5, T6
- AC6 → T7, T8
- AC7 → T4, T6

## Tasks

- [x] T1: Spike three platform facts and log each in the work log. First, the `skill` value `skill.prompt` carries for a plugin skill typed as `/cairn:milestone-plan`. Second, the `tool.call` matcher for the MCP chapter tool. Third, whether an atom update in the middle of a turn redraws the band in the desktop app. If it does not, the band shows the chapter at its next drawing. Confirm a refusal is the platform's before concluding it (the M191 lesson).
- [x] T2: State in `register.tsx` and `types/index.d.ts`. Add the `step` atom and its type under a shape tag. Add a `skill.prompt` hook that passes the text through unchanged. Add a `mark_chapter` hook that ignores a call with an `agentId`. It sets the chapter only after `next(e)` resolves with no deny and no error. Add the `session.end` reset. Add the skill to the close marks and a shape tag to `dismissed`.
- [x] T3: Rows in `band.ts`. Add the label map, the skill row, the rule for which row carries the skill, and the chapter item row.
- [x] T4: Skill list. Have `gen_fixtures.py` write the skill names from `skills/*/SKILL.md` into `fixtures.gen.ts`, less `shared` and `tests`. Have a mod test fail when the label map and that list differ. The existing stale-module check in `test_status_fixtures.py` then covers the list.
- [x] T5: Draw in `register.tsx`. Draw the skill row and the chapter item row, and keep the close button on the first header row.
- [x] T6: Tests. Add the AC1–AC5 cases on both surfaces, red first, and restate any M194 case whose tree changed.
- [x] T7: Docs. Update README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry.
- [ ] T8: Look at the band live in the desktop app during a real plan, implement, and review, including a review chapter after all criteria are checked. Record what it showed in the work log.

## Work log

- 2026-10-01: created by /milestone-plan, from the operator's request to fill in band phases for the other cairn steps, such as planning, final checks, and post-merge hygiene.
- 2026-10-01: criteria audit, full mode, one fresh Opus reader, 18 findings, each with one clear fix, all fixed before the gate. AC1 names the plugin's `skills/` directory and bounds the outside names to three probes. AC2 drops a duplicate case and empties the skill row's right side. AC3 moves the subagent clause into T2, promises the next drawing, and adds a deny case and a `done` case. AC4 resets on every session end. AC5 names its cases and gives `dismissed` a shape tag. AC6 fixes a wrong terminal claim and drops a recording clause.
- 2026-10-01: plan gate chose the skill event and the existing chapter calls over a phase file that each skill writes. The chapter calls need no new instruction to the model, and a file can go stale across sessions. Falsified by live sessions where the chapter calls are missing or too coarse to name the step.
- 2026-10-01: plan gate chose to infer nothing from git or the criteria alone. Planning has no row before its id exists, and hygiene runs inside one turn. Falsified by a mod event that names the git branch and a band that redraws only at turn end.
- 2026-10-01: plan gate chose rows for all ten skills over the milestone loop and hotfix alone, and over all but `/milestone`. Falsified by a status check whose leftover row gets in the way in real sessions.
- 2026-10-01: plan gate kept the `review` label with the chapter on the item row over labels mapped from chapter titles, because chapter titles are free text. Falsified by a reader who cannot tell the final checks from hygiene in the band.
- 2026-10-01: implement started on branch `m195-band-steps`. No question gate, because the plan left no choice open.
- 2026-10-01: T1 spike, harness half. A save made during the session's own turn reloads the mod only when the turn ends (plugin-authoring reference), so no live probe can run inside one turn. `claude plugin validate` lists the `skill.prompt` and `tool.call{tool=mcp__ccd_session__mark_chapter}` hooks. The skill-name spelling and the mid-turn redraw move to T8's live look. The code takes both spellings, and AC3 promises only the next drawing.
- 2026-10-01: AC3 amended at a mini gate. Over `mixed`, M013's `Review` status reads as `review`, so M010 moving to `done` hands the chapter to M013, not to a skill row. The gate chose a two-step clause over editing both rows at once, because the two steps also test the hand-off to the next `review` row.
- re-audit: AC3 (full) — the both-at-once wording was satisfiable. The reader suggested the two-step form and running the chapter cases on desktop only. The surfaces were kept, because the cases test the drawing of a given state on each surface.
- re-audit: AC3 (full) — the two-step wording was satisfiable. Fixed: the edits name the ROADMAP status, because M013 has no file. Noted: no chapter case on an `in-progress` row, so the tests add one for M012 without a criterion change.
- 2026-10-01: T2–T6 done in `972c6a5`. A `step` atom (`step-1`) and a `dismissed` atom (`dismissed-2`, now marks plus skill), the `skill.prompt`, chapter `tool.call`, and `session.end` hooks, `SKILL_LABELS`, `cairnSkill`, `skillLines`, and `stepLines` in `band.ts`, and `SKILLS` in `fixtures.gen.ts`. 48 new mod cases, 130 in all, green on the first run.
- 2026-10-01: discrimination. Ten planted defects each turned at least one new case red (any prefix accepted, deny or error not checked, no session-end reset, skill left out of or chapter put in the close mark, no refresh at a chapter, a re-run that keeps the chapter, the carrier rule removed, the skill name as label). The restored tree was green again. A probe `skills/zz-probe/SKILL.md` made `gen_fixtures.py --check` exit 1. Verify slot green: scripts 394, hooks 174, plugin validate (the same one CLAUDE.md warning as main), mod tests 130.
- 2026-10-01: T7 done. README "The milestone band" gained the skill row, chapter, and terminal paragraphs, and its close-button and refresh paragraphs name the skill. The DESIGN.md `hooks/status/` line and the CHANGELOG entry say the same. A sweep for "draws nothing" found one stale CHANGELOG clause, now "no active milestone and no cairn skill running". Verify slot green: scripts 394, hooks 174, validate exit 0, mod tests 130.

## Decisions

## Review
