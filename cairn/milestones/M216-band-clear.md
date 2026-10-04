<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M216: A Clear button when a cairn skill ends

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the band draws in every adopter's session   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m216-band-clear   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When a cairn skill finishes and the session is idle, the status band shows a `Clear` button that runs `/clear`.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a third action Button, `Clear`, on the band's first row beside
M212's next-step and `Status` Buttons. It shows after a main-loop Stop
ends a cairn skill's step (`register.tsx` `classic.Stop`), and it goes at
the next idle typed prompt, the next cairn skill, or the session's end. A
press runs the built-in `clear` command through M212's `run`, whose
rejection path puts `/clear` in the prompt box and shows a toast. The row
drops `Clear` first when it lacks room. README, DESIGN, and CHANGELOG
describe it. One live look in a desktop Code session (question set).

**Out:** a press that clears and then starts the next command. The user
did not ask for it, and nothing is planned. A Clear button in the cairn
pane, which has no buttons (the "Status mod follow-ons" row). M212's and
M213's open follow-ons stay in "Band button follow-ons (M212, M213
review)".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: A main-loop Stop that ends a cairn skill's step makes the
      band's first row draw a `Clear` Button (key `cairn-clear`) before
      the next-step Button. It draws only where the row draws the
      next-step and `Status` Buttons and has room for all three (AC4).
      `band.test.tsx` cases show it present after such a Stop. They show
      it absent, with the other two present, in a session where no cairn
      skill ran and in a session whose step an idle typed prompt ended.
- [ ] AC2: The `Clear` Button is gone after a prompt that the operator
      types while the session is idle and that no hook beneath drops, and
      after the session ends. No `cairn-clear` draws while a cairn skill's
      step is set. One `band.test.tsx` case per clause shows it.
- [ ] AC3: A press of `Clear` calls `$.command.run` with command `clear`
      and empty args. A press while another action Button's run is in
      flight calls nothing. If the run rejects, the press appends `/clear`
      to the prompt box and shows a toast that names it. `band.test.tsx`
      cases cover the run, the in-flight press, and the rejection.
- [ ] AC4: The row counts `Clear`'s columns (its label, 4 chrome columns,
      and one space) when it decides whether the action Buttons fit. Where
      all three do not fit but the next-step and `Status` Buttons do, it
      draws those two as in M212. `band.test.tsx` cases on a milestone-row
      fixture, on the terminal and the desktop surface, show the widest
      width that drops `Clear` and one column wider, which draws it.
- [ ] AC5: In a new desktop Code session in a real cairn repo, after a
      cairn skill ends, the operator sees the `Clear` Button. A press
      either clears the conversation, or puts `/clear` in the prompt box
      and shows the toast.
- [ ] AC6: README.md's "The milestone band" section, the `hooks/status/`
      lines of `cairn/DESIGN.md`, and CHANGELOG.md's `## Unreleased`
      section describe the `Clear` Button. The five verify commands in
      `cairn/PROFILE.md` exit 0 at the branch head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3
- AC6 → T1, T2, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: State, tests first. Add an `ended` atom in `register.tsx`
      (shape `ended-1`), true when `classic.Stop` sets a non-null step to
      null. `prompt.submit` clears it on an idle typed prompt and puts it
      back on a drop, as it does the step (M210). `skill.prompt` and
      `session.end` clear it. Write the AC1 and AC2 cases first. The
      skill-step case asserts on `cairn-clear` while the step is set.
- [x] T2: Drawing and press, tests first. Draw `cairn-clear` before
      `cairn-next` while `ended` is true and the M212 show rules hold. Try
      the row with three Buttons' columns reserved, then with two, then
      with none (`actionsFit`, `register.tsx:316-322`). `pressClear` runs
      `clear` through `run`. `session.end` sets `running` to false, so a
      `/clear` whose run never settles does not block later presses (audit
      note). Update `ACTION_KEYS` and the M212 and M213 cases that expect
      two Buttons. Write the AC3 and AC4 cases first.
- [x] T3: Live look (operator, question set). The operator opens a new
      desktop Code session in this repo or bsync, runs `/cairn:milestone`
      to its end, looks at the row, and presses `Clear`. If the press only
      fills the prompt box, stop and ask the user, since the question set
      chose a clear at once.
- [x] T4: Docs and gate. Describe the Button in README.md (near :187),
      the `hooks/status/` lines of `cairn/DESIGN.md` (:73 and :170), and
      CHANGELOG.md's `## Unreleased`. Run the five verify commands.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: when the Clear button shows — after a cairn skill ends, until the next typed prompt or skill.
- 2026-10-04: question set: what a press does — runs /clear at once, with the prompt-box fill as the fallback on a rejected run.
- 2026-10-04: question set: a live look in a new desktop Code session before the merge — granted.
- 2026-10-04: criteria audit (full mode, fresh Opus reader): 6 findings, all taken by narrowing. AC1 bound to the row's fit, two cases that could not fail replaced, "typed prompt" narrowed to idle and not dropped, AC4 bound to the fit rule at a boundary pair, AC5's work-log clause removed and the fallback accepted. One note (`running` stuck after `/clear`) moved to T2.
- 2026-10-04: plan gate chose showing Clear after a skill ends over showing it whenever Start and Status show, because a fresh session has nothing to clear (user's choice); falsified by the operator pressing Clear in sessions where no skill ended.
- 2026-10-04: plan gate chose a press that runs /clear at once over one that fills the prompt box, because the button shows only at a saved stop point (user's choice); falsified by a clear that loses unsaved work in a real session.
- 2026-10-04: plan chose dropping Clear first when the row is narrow over all-or-none Buttons, because Start and Status already fit from 37 columns and Clear must not take them away; falsified by an operator who misses Clear at a narrow width.
- 2026-10-04: collision sweep: no ROADMAP row, archive, or D-entry names a Clear button. D-148 makes the run's end a /clear point, which this serves. Inbox: 0 open issues, 0 open PRs.
- 2026-10-04: implement started on m216-band-clear. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-04: T1 and T2 landed in one checkpoint, because the AC1 and AC2 cases observe the drawn `cairn-clear` and need T2's drawing. New `ended` atom (`ended-1`), declared in `types/index.d.ts` (plugin validate failed until it was). 26 new mod cases. A dropped typed prompt puts `ended` back only while no step is set. Mod tests 1105 to 1131, all five verify checks exit 0.
- 2026-10-04: check discrimination: with the Stop's `ended` write planted out, 24 of the 26 new cases and the M213 empty-row case went red. The two absence cases stayed green, as they assert no Clear. Restored, then green.
- 2026-10-04: AC4's sweep on single-in-progress shows the Clear threshold 10 columns above the two-Button threshold on both surfaces. One M213 case (`isEmptyRow` after a skill's Stop) now expects Clear first.
- 2026-10-04: the T2 edit to `register.tsx` and some tracking edits went through a python script, not the Edit tool, against the rulebook's file-edit rule. Later edits use Edit.
- 2026-10-04: T4 done before T3 so the live look sees the finished branch. README (a paragraph after the empty row's buttons), DESIGN (the `hooks/status/` history line and a paragraph after the empty row), and CHANGELOG `## Unreleased` describe the Button. Scripts and hooks suites exit 0, and the hand-run `skills/tests` stays at 665 OK.
- 2026-10-04: live look (T3): in a new desktop Code session in this repo on m216-band-clear, the operator ran `/cairn:milestone` to its end. Clear showed before the other Buttons, and a press cleared the conversation (operator's answer at the stop chip).
- 2026-10-04: claim audit: 40 claims read, 9 corrected — CHANGELOG.md, README.md, hooks/status/register.tsx, types/index.d.ts, cairn/DESIGN.md
- 2026-10-04: the 9 corrections: "goes away when you type a prompt" narrowed to an idle prompt no hook drops; Clear shows on any row with the next-step and Status Buttons, the idle row included; the README no longer says a skill's end means committed work; three comments now say Clear needs the action Buttons and room; DESIGN names a cairn skill's prompt. The same reader re-read all 9 as correct. Verify: all five checks exit 0 (mod tests 1131).

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
