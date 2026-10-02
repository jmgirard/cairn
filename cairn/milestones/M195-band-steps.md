# M195: A milestone band that names every cairn step

- **Status:** review
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

- [x] AC1: The row that carries a running cairn skill shows that skill's label. A cairn skill has a `SKILL.md` under the cairn plugin's `skills/` directory. It counts when the engine expands its prompt by its bare name or its `cairn:` name. The labels come from one map in `hooks/status/band.ts`: milestone-plan `plan`, milestone-implement `implement`, milestone-review `review`, hotfix `hotfix`, cairn-triage `triage`, cairn-release `release`, milestone `status`, milestone-brief `brief`, design-interview `design`, cairn-init `init`. The prompts of `commit`, `other:hotfix`, and `cairn:nope` leave the band as it was. Shown by `claude plugin test` cases on terminal and desktop. They fire `skill.prompt` for each name in the skill list that `gen_fixtures.py` writes from that directory, in both spellings, and for the three other names.
- [x] AC2: A running skill with no matching active milestone gets a skill row above the milestone rows. That is the case for a skill other than milestone-implement and milestone-review. It is also the case for milestone-implement with no `in-progress` row, and for milestone-review with no `review` row. A skill row shows the label and the skill's slash command, such as `/milestone-plan`, and nothing on its right side. Otherwise the first active row with the matching status carries the skill, and no skill row is drawn. Shown by plugin test cases on both surfaces: milestone-plan over `no-active` and `mixed`, hotfix over `mixed`, milestone-review over `single-in-progress`, and milestone-implement and milestone-review over `mixed`.
- [x] AC3: The item row follows the session's chapters. A main-loop `mark_chapter` call can succeed after the running skill's prompt was expanded. The item row under the row that carries the skill then shows that call's title. The title replaces the next open task or criterion, or stands alone where the row has none. A skill row with no chapter has no item row. Each such call also reads the tracking files again, so the next drawing shows the counts at that call. Shown by plugin test cases on both surfaces over `mixed`. A milestone-review prompt and a `Post-merge hygiene` chapter put that title under M010. A fixture file edited between two chapter calls, with no turn end between them, draws the new counts. M010's ROADMAP status edited to `done`, then a chapter call, moves the chapter under M013. M013's ROADMAP status then edited to `done`, then a chapter call, moves it to a `review` skill row. A chapter call that a hook beneath denies leaves the item row as it was.
- [x] AC4: Every session end clears the step. After `session.end`, the band shows the milestone rows alone, each labeled from its status as before M195. Any cairn skill's prompt, the same skill included, replaces the skill and drops the chapter. Shown by plugin test cases on both surfaces for the reasons `clear` and `resume`, and for a second milestone-review prompt after a chapter.
- [x] AC5: The close button works with skill rows. It sits on the first header row, and a skill row counts as one. A press hides the band until the active ids and statuses, their ROADMAP order, or the running skill's name change. Shown by plugin test cases on both surfaces. After a press, a chapter call and a checked task box keep the band hidden. A different skill's prompt shows it again. A press on a lone skill row over `no-active` hides it.
- [x] AC6: README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry describe the skill row, the ten labels, and the chapter on the item row. They say that the chapter text needs the desktop app's chapter tool. On the terminal, milestone rows show their next open item, and a skill row has no item row. They also say that a subagent that loads a cairn skill sets the label.
- [x] AC7: The verify slot in `cairn/PROFILE.md` runs clean. It holds both Python suites, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T2, T3, T4, T6
- AC2 → T3, T5, T6
- AC3 → T1, T2, T3, T5, T6
- AC4 → T2, T6
- AC5 → T2, T5, T6
- AC6 → T7, T8, T9
- AC7 → T4, T6

## Tasks

- [x] T1: Spike three platform facts and log each in the work log. First, the `skill` value `skill.prompt` carries for a plugin skill typed as `/cairn:milestone-plan`. Second, the `tool.call` matcher for the MCP chapter tool. Third, whether an atom update in the middle of a turn redraws the band in the desktop app. If it does not, the band shows the chapter at its next drawing. Confirm a refusal is the platform's before concluding it (the M191 lesson).
- [x] T2: State in `register.tsx` and `types/index.d.ts`. Add the `step` atom and its type under a shape tag. Add a `skill.prompt` hook that passes the text through unchanged. Add a `mark_chapter` hook that ignores a call with an `agentId`. It sets the chapter only after `next(e)` resolves with no deny and no error. Add the `session.end` reset. Add the skill to the close marks and a shape tag to `dismissed`.
- [x] T3: Rows in `band.ts`. Add the label map, the skill row, the rule for which row carries the skill, and the chapter item row.
- [x] T4: Skill list. Have `gen_fixtures.py` write the skill names from `skills/*/SKILL.md` into `fixtures.gen.ts`, less `shared` and `tests`. Have a mod test fail when the label map and that list differ. The existing stale-module check in `test_status_fixtures.py` then covers the list.
- [x] T5: Draw in `register.tsx`. Draw the skill row and the chapter item row, and keep the close button on the first header row.
- [x] T6: Tests. Add the AC1–AC5 cases on both surfaces, red first, and restate any M194 case whose tree changed.
- [x] T7: Docs. Update README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry.
- [x] T8: Look at the band live in the desktop app after the mod reloads: a `/cairn:milestone-implement M195` run, then chapters marked during one turn. Record what it showed in the work log. The plan look and a review chapter after all criteria are checked are recorded at M195's review.
- [x] T9: Docs gaps from review return 1. Add the subagent clause to the CHANGELOG entry. Add the ten labels and the terminal clause to the DESIGN.md `hooks/status/` line.

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
- claim audit: 45 claims read, 3 corrected — README.md, CHANGELOG.md, hooks/status/register.tsx. "Draws nothing outside a cairn repo" was false, because a running cairn skill draws its rows there. A `cairn-init` over `no-roadmap` case now backs the corrected text, for 131 mod tests. The terminal claim now names the chapter tool and gives the terminal as an example. The same reader re-read the three once and found them true.
- 2026-10-01: T8 split, a minor task edit. A mod edit made during a turn reloads at the turn end, and the band's skill and mid-turn redraw can only be seen by the operator. This session checks the implement row, the `cairn:` spelling, and the mid-turn redraw. The plan and review looks are recorded at M195's own review.
- 2026-10-01: operator screenshot of the band: `implement M195 … 7/8 tasks` with the pre-edit T8 text on the item row, so that drawing came before the band read `697a950`. Operator note: the band's `×` is smaller than the desktop app's own close icon. That note went to the "Band layout edge cases" candidate row, outside M195's scope.
- 2026-10-01: T8 attempt in the planning session after a `/cairn:milestone-implement M195` rerun. Three chapters were marked 15 seconds apart, and the operator saw no change on the M195 item row. The desktop session still ran the mod it loaded at session start, so the edits made during the session never loaded. T8 moves to a new Code session on this branch.
- 2026-10-01: T8 done in a new Code session that loaded the mod from this branch. After `/cairn:milestone-implement M195`, three chapters were marked in one turn, with the verify runs between them. With the turn still open at a question, the operator saw the M195 item row read `T8 probe: third chapter`. So the `cairn:` spelling sets the step, and the band redraws in the middle of a turn. Verify slot green: scripts 394, hooks 174, validate exit 0, mod tests 131.
- 2026-10-01: review return 1 (defect): AC6 fails as written. The CHANGELOG entry lacks the subagent clause. The DESIGN.md `hooks/status/` line lacks the ten labels and the terminal clause. AC1–AC5 and AC7 passed with fresh evidence. Status back to `in-progress`.
- 2026-10-01: T9 added, a minor amendment for the review return. AC6 now maps to T7, T8, and T9.
- 2026-10-01: T9 done. The CHANGELOG entry gained the subagent clause and the terminal's milestone-row clause. The DESIGN.md `hooks/status/` line gained the ten labels, the skill row's contents, and the terminal clause. Verify slot green: scripts 394, hooks 174, validate exit 0, mod tests 131.
- claim audit: 18 claims read, 0 corrected — CHANGELOG.md, cairn/DESIGN.md (the T9 lines only, one fresh Opus reader).
- 2026-10-01: review round 2 passed every criterion. The gate directed fixes F1 to F6, which landed on the branch with verify green.
- step-7 approval: m195-band-steps approved for merge

## Decisions

## Review

Round 1, 2026-10-01, on `cf8bc35`. The branch already held `origin/main`, so no merge was needed.

- AC7: The verify slot is green. `scripts/tests` ran 394 OK (21 skipped), exit 0. `hooks/tests` ran 174 OK, exit 0. `claude plugin validate` exited 0 with the one known warning. It lists the `skill.prompt`, chapter `tool.call`, and `session.end` hooks. `claude plugin test .` gave 131 pass, 0 fail (2.1.286 binary).
- AC1: One case in `band.test.tsx` compares `SKILLS` with the `SKILL_LABELS` keys and a hand-written label map. `SKILLS` comes from `gen_fixtures.py` and holds the 10 names in `skills/`, less `shared` and `tests`. Other cases run each name in both spellings over `no-active`. Three more run `commit`, `other:hotfix`, and `cairn:nope`. `mountEach` draws each case on terminal and desktop. All are green.
- AC2: The skill-row cases run milestone-plan over `no-active` and `mixed`, and hotfix over `mixed`. They run milestone-review over `single-in-progress`. They run milestone-implement and milestone-review over `mixed`. Each runs on both surfaces and looks for an empty right side with the close button. All are green.
- AC3: The chapter cases cover the M010 `Post-merge hygiene` title and the M012 title. They cover a file edit between two chapters with no turn end. They cover the hand-off from M010 to M013 and then to a `review` skill row. They cover a deny and an error beneath. Each runs on both surfaces. All are green.
- AC4: The session-end cases cover the reasons `clear` and `resume`. One more case runs a second milestone-review prompt, in the `cairn:` spelling, after a chapter. Each runs on both surfaces. All are green.
- AC5: The close-button cases put the button on the skill row. After a press, a chapter, a ticked task box, and the same skill keep the band hidden. Another skill shows it again. A press on a lone skill row over `no-active` hides it. Each runs on both surfaces. All are green.
- AC6: Fails as written. README "The milestone band" says every clause. The CHANGELOG `Unreleased` entry does not say that a subagent that loads a cairn skill sets the label. The DESIGN.md `hooks/status/` line names `SKILL_LABELS` but not the ten labels. It also does not say what the terminal shows: milestone rows with their next open item, and a skill row with no item row. AC6 is not ticked.
- Steps 4 and 5 did not run, because a criterion failed. `cairn_validate` ran for information and passed.

Round 2, 2026-10-01, on `9950165`. `origin/main` is an ancestor of the branch, so no merge was needed.

- AC7: The verify slot is green. `scripts/tests` ran 394 OK (21 skipped), exit 0. `hooks/tests` exited 0 (174 tests). `claude plugin validate` exited 0 with the one known CLAUDE.md warning, and it lists the `skill.prompt`, chapter `tool.call`, and `session.end` hooks. `claude plugin test .` gave 131 pass, 0 fail, exit 0 (2.1.286 binary).
- AC1: Same cases as round 1, all green in the run above. `gen_fixtures.py --check` exited 0, so `SKILLS` matches the 10 `skills/` directories. The map test holds `SKILLS`, `SKILL_LABELS`, and the hand-written label map equal.
- AC2: The seven skill-row cases in `band.test.tsx` (lines 867–906) cover the six named cases plus `cairn-init` over `no-roadmap`, each through `mountEach` on both surfaces. All green.
- AC3: The chapter cases (lines 908–1020) cover the M010 `Post-merge hygiene` title, the M012 title, and a file edit between two chapters. They also cover the M010 → M013 → `review` skill row hand-off, and a deny and an error beneath. All green on both surfaces.
- AC4: The session-end cases for `clear` and `resume`, and the second `cairn:milestone-review` prompt case (lines 1022–1055), are green on both surfaces.
- AC5: The close-button cases (lines 1057–1124) are green on both surfaces.
- AC6: Passes. README "The milestone band" names the skill row, the ten labels, and the chapter on the item row. It also names the chapter tool `mcp__ccd_session__mark_chapter`, the terminal behavior, and the subagent clause. The DESIGN.md `hooks/status/` line now lists the ten labels, the terminal clause, and the subagent clause. The CHANGELOG `Unreleased` entry now has the terminal clause and the subagent clause.
- T8's plan look was not taken. It needs a `/milestone-plan` run, and that run replaces the review skill on the band. The AC2 and AC3 `milestone-plan` cases cover that drawing on both surfaces.
- Consistency gate: `cairn_validate` passed every check, exit 0, coverage complete included. M195 touches GP2 but changes no principle text, so `cairn_impact` was skipped. The `generic` profile names no toolchain checks.
- Independent review: three fresh reviewers (Opus diff-bug, Sonnet blame-history, Sonnet prior-review). The PR-comment probe returned none. No finding shows a criterion failing, so no return. Findings, ranked, with the disposition put to the gate:
  - F1 (diff-bug 1): the chapter hook builds its write from a `step` value read before the call, not from the value `update` passes in. A skill prompt or session end in that gap is undone. Fix now: write from the passed value.
  - F2 (diff-bug 2): no test sends a chapter call with an `agentId`, so the subagent guard can be removed with all cases green. Fix now: add that case, and a chapter call with no running skill.
  - F3 (prior 4, diff-bug 6): an empty chapter title draws a bare `  → ` row. Fix now: treat an empty title as no title.
  - F4 (diff-bug 7): a stored skill missing from the label map makes the drawing throw. Fix now: read such a step as no step.
  - F5 (diff-bug 8, 9): the CHANGELOG close-button clause leaves out a session end while a skill runs. The DESIGN.md line says every chapter is stored, but the hook stores one only while a skill runs. Fix now.
  - F6 (prior 3): the new CHANGELOG, README, and DESIGN.md lines are wrapped unevenly, as M193 and M194 fixed before. Fix now: rewrap.
  - F7 (prior 1, 2, blame 2): the read-then-clear of `dismissed`, a known item, now also runs at each skill prompt, chapter, and session end. Follow-up: widen the "Band close-state edge cases" row.
  - F8 (blame 1, prior 7): a press with no skill running stays hidden across a `/clear` or resume, and a press with a skill running does not. Follow-up: the same row.
  - F9 (diff-bug 4, blame 4): the step stays after its skill ends, so later chapters attach to it. Follow-up: the "Band idle line" row, whose "draws nothing" text is now stale.
  - F10 (diff-bug 3, blame 5): a project skill with a bare cairn name, such as `hotfix`, sets the step. Follow-up: the "Status mod follow-ons" row.
  - F11 (diff-bug 5): the chapter goes to the first row of the status, not the milestone the skill names. Follow-up: the same row.
  - F12 (prior 5): skill rows add more space-padded labels in the desktop font. Noted: the "Band layout edge cases" row holds it.
  - Rejected: a chapter under a state-label row is what AC3 asks for (blame 3). Scope accepts that a subagent's skill prompt sets the label (prior 6). The `trimEnd` in `lineText` changes no assertion (blame 5). A chapter call with no skill only reads the files again (blame 5). A skill prompt at compaction is unconfirmed (diff-bug 10).
- Gate: the operator chose to fix F1–F6 and then merge. F7–F11 go to candidate rows at hygiene, and F12 stays noted. The operator saw `review M195` with all 7 criteria checked and `→ Approval gate` under it. That is T8's review-chapter look.
- Fix-now outcomes, all on the branch before the push. F1: the chapter hook writes from the value `update` passes in. F2: new cases for a subagent's chapter call and for a chapter with no running skill. F3: an empty title sets no chapter, with a new case. F4: `knownStep` in `band.ts` reads a step with no label as no step, with a direct test. F5: the CHANGELOG close-button clause names a session end while a skill runs. The DESIGN.md line says a chapter is stored only while a skill runs. F6: the new lines are rewrapped.
- Planted defects: removing the `agentId` guard turned the subagent case red, and removing the empty-title check turned the empty-title case red. The `knownStep` call in `register.tsx` has no drawing case, and the mod tests cannot stage the F1 timing gap.
- Re-verify after the fixes: scripts 394 OK (21 skipped), hooks 174 OK, validate exit 0, mod tests 135 pass and 0 fail, `cairn_validate` all checks passed.
