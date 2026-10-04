<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M212: Buttons on the status band

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the band draws in every adopter's session   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m212-band-buttons   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The status band shows a button for each cairn command that fits the moment, and a press runs that command.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** two action Buttons on the band's first row, beside the open and
close Buttons. The next-step Button runs the command that `recommend` in
`hooks/status/reader.ts` picks, the same rule as the pane's Next line, with
the milestone id. The status Button runs `/milestone`. Both show only while
no cairn skill's step is set and no turn is working. A press runs the
command through `$.command.run`. If the run rejects, the press appends the
command line to the prompt box and shows a toast. The two Buttons give way at
narrow widths before the title loses its room. A CHANGELOG entry.

**Out:**
- Buttons in the cairn pane → the "Status mod follow-ons" candidate row,
  which keeps the pane half of its "clickable next-command actions".
- A plan Button: the band draws nothing while no milestone is active or
  workable, so it has no row to carry one → added to the same row.
- Button colors in light, colorblind, and ANSI themes → "Band label colors
  in other themes".
- Keyboard hotkeys for the Buttons → not asked for; a candidate if missed.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: At 120 columns, while the band is drawn, the mod's `step` value
      names no cairn skill (`knownStep` is null), and the `AbovePrompt` props
      carry `isWorking: false`, the band's first row carries a next-step
      Button (key `cairn-next`) and a status Button (key `cairn-status`). A
      press of `cairn-next` runs `cairn:` plus the `command` that `recommend`
      in `hooks/status/reader.ts` returns for the same ROADMAP, without its
      `/`. Its `args` equal that result's `id`. A press of `cairn-status`
      runs `cairn:milestone` with empty `args`. Evidence: `band.test.tsx`
      cases on both surfaces over the `single-in-progress`, `states-review`,
      `idle-order`, and `mixed` fixtures. In `mixed` the band shows M012 and
      `recommend` names M010. Each case presses each Button. It asserts the
      `command` and `args` that a `command.run` hook beneath the mod receives.
- [ ] AC2: The first row carries neither action Button while the `step`
      value names a cairn skill or while `isWorking` is true, and the open
      and close Buttons stay. Evidence: two `band.test.tsx` cases on both
      surfaces over `single-in-progress`. The first case starts a cairn
      skill. It finds neither action key and finds `cairn-open` and
      `cairn-close`. It ends the step and finds both action keys again. The
      second case draws with `isWorking: true` and finds neither action key.
- [ ] AC3: When `$.command.run` rejects, the press puts the command line
      (`/cairn:<command> <id>` or `/cairn:milestone`) in the prompt box with
      `mode: 'append'`, so a typed draft stays. It also shows one toast that
      contains the rejection's message. Evidence: a `band.test.tsx` case on
      both surfaces for each Button, with a `command.run` hook beneath that
      throws. It asserts the `text` and `mode` that a `prompt.fill` hook
      beneath receives. It asserts the toast that a `ui.toast` hook beneath
      receives.
- [ ] AC4: The sweep domain is every column count from 40 to 200, over each
      case of the M197 sweep (`each row fits the band from 40 to 200
      columns`): each fixture row drawn alone, and each `IDLE_DRAWN` idle
      row. At each point the first row carries both action Buttons, or it
      carries neither and draws the same tree as the row at that width with
      `isWorking: true`. With both Buttons, the title keeps the smaller of
      its width and 10 columns, each action Button counted at its terminal
      width wherever it sits in the row. In each case the widths with both
      Buttons are one run that includes 120 and ends at 200. Evidence: a
      `band.test.tsx` sweep on both surfaces.
- [ ] AC5: In a new desktop Code session over this repo with an active
      milestone, the band shows both action Buttons while idle, and a press
      of the status Button runs `/cairn:milestone`. Evidence: a live look by
      the operator.
- [ ] AC6: The `## Unreleased` section of `CHANGELOG.md` gains one entry for
      the Buttons, and each behavior it states is one that the AC1 to AC3
      cases or the AC4 sweep assert.
- [ ] AC7: The four verify-slot commands in `cairn/PROFILE.md` exit 0 on the
      review head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3
- AC5 → T5
- AC6 → T4
- AC7 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Write the AC1 to AC3 cases in `hooks/status/band.test.tsx` first
      and see them red: capture presses with `command.run`, `prompt.fill`,
      and `ui.toast` hooks beneath the mod, keyed Buttons found by
      `findAll`.
- [x] T2: In `hooks/status/register.tsx` (the `AbovePrompt` hook, near
      :334), draw `cairn-next` and `cairn-status` on the first row from the
      pane value's `next` and the `step` atom and `e.props.isWorking`; a
      press runs `$.command.run`, and a rejection appends to the box and
      toasts.
      Labels are short words that the live look settles.
- [x] T3: In `hooks/status/band.ts`, reserve the two Buttons' columns in
      `stepLines`. Drop them at a width where the title loses its room.
      Write the AC4 sweep.
- [x] T4: Add the CHANGELOG entry, then run the four verify-slot commands.
- [ ] T5: Live look (operator, approved at the question set): a new desktop
      Code session on the branch, idle band with both Buttons, press the
      status Button.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to work on — "add convenience buttons to the status band"; the first round named no work, so a second round asked about the buttons.
- 2026-10-04: question set: which buttons — "contextually displayed, the ones that make sense at any given moment"; press — run it at once (fill the box only as the fallback); live look — yes, ask the operator to open a new Code session near the end of implement.
- 2026-10-04: collision: absorbs the band half of the "Status mod follow-ons" candidate row (clickable next-command actions); the row stays until post-merge hygiene, and the pane half and the plan Button stay in it. D-124 (chat routing chips replaced by fenced commands) read whole: it governs chat chips, not the band, so no collision. D-143 read: the mod's checks gate this repo, unchanged.
- 2026-10-04: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-04: lessons harvested: M193/M194 (shrinking Box needs minWidth 0, a new shape tag on a layout change, live look needed for drawing), M195 (plugin skill names are `cairn:<name>`; a live look needs a new Code session), M201 (a second session can be driven by send_message).
- 2026-10-04: plan gate chose "contextual" as a next-step Button from `recommend` plus a status Button over one Button per cairn command because the pane's Next rule already says what fits the moment; falsified by a live look where the next-step Button names a command the operator would not run next.
- 2026-10-04: plan gate chose to hide the action Buttons while `isWorking` or a cairn skill's step is set over showing them with a queued run because a press mid-turn queues a command behind work in flight; falsified by the operator pressing for a queued run in a real session.
- 2026-10-04: criteria audit (full mode, fresh Opus reader) returned 8 findings, all fixed toward the narrower promise: AC1 pinned to 120 columns (it contradicted AC4's narrow-width drop); `mixed` added to AC1 (band row and `recommend` name different ids); "a cairn skill runs" restated as the `step` value; AC1 names `recommend`'s `command` and `id` fields; AC3 covers any rejection, its evidence a throwing hook, and pins `mode: 'append'` so a draft stays; AC4's domain named as the M197 sweep's cases, the title room stated directly, and the Button widths made one run ending at 200; AC6 cites the AC4 sweep. AC2, AC5, AC7 clean.
- 2026-10-04: audit note, no change: the next-step press after a merge runs the next milestone's implement without the `/clear` that D-148's close block puts first; the press is the operator's own act, so the CHANGELOG entry says the press does not clear the context.
- 2026-10-04: plan gate chose `mode: 'append'` for the fallback fill over `replace` because `replace` wipes a typed draft; falsified by a live look where the appended command does not run as typed.
- 2026-10-04: plan gate chose fixed `cairn:<skill>` names over looking each name up in `$.command.list()` because the mod ships inside the plugin, whose skills are `cairn:<name>` (M195 lesson); falsified by an install where the band loads and a `cairn:` command is unknown (AC3's fallback then fills the box).
- 2026-10-04: implement started on branch m212-band-buttons; the untracked `cairn-probe.log` and `tsconfig.json` in the tree are not this milestone's and stay unstaged.
- 2026-10-04: implement chose plain Buttons labeled `Resume`, `Review`, or `Start` and `Status`, drawn only when the row is at its fullest form (track at 52 columns, or the long warning label) and the title keeps its room with them counted; plain because an idle row at 120 columns leaves 20 columns and a bracketed pair takes 24; the fullest-form rule because a post-hoc fit check showed buttons at 40 to 47 columns on an idle row and not above, which breaks AC4's one run.
- 2026-10-04: T1 done: AC1 to AC4 cases written in `band.test.tsx`, and the M194, M197, and M199 cases that list the band's Buttons now expect the two action Buttons at 120 columns with no cairn skill running; `claude plugin test .` red by design, 77 fail (the M212 cases and those updated cases), 1000 pass.
- 2026-10-04: T2, T3 done: `actionsFit` in `band.ts`, the `cairn-next` and `cairn-status` Buttons and the `run` press handler in `register.tsx`. The AC3 test first asserted the thrown text; the engine skips a hook that throws, so the run rejects at the bottom of the chain with "no implementation for command.run", and the test now asserts that message, the rejection the toast names.
- 2026-10-04: check discrimination for the AC4 sweep: planting "fullest form not required" reddened 5 idle cases (buttons at 40 to 200 with gaps); planting "action columns not counted" reddened 37 AC4 cases plus the M197 and M206 sweeps; both restored, `git status` clean against 3b1d3ec.
- 2026-10-04: T4 done: CHANGELOG entry under Unreleased > New; the AC1 cases also assert the labels it names. The audit note's "press does not clear the context" stays out of the entry, because AC6 admits only tested behavior. Verify: scripts 397 OK, hooks 174 OK, validate passed (the known CLAUDE.md warning), `claude plugin test .` 1077 pass.
- 2026-10-04: live look 1 (operator, new desktop Code session): the Status press ran and the buttons showed, but "these look more like text than buttons". Implement dropped `plain` and gave the next-step Button `variant="primary"` and Status `variant="secondary"`; each now takes its label plus 4 columns, with no space between the two, so an idle row at 120 columns (20 columns free) still fits `Start` and `Status`. Mod tests 1077 pass; a second live look follows.
- 2026-10-04: claim audit: 44 claims read, 3 corrected — register.tsx (the fill-catch comment named the wrong cause: a fill with no box resolves `isFilled: false`, it does not reject), band.test.tsx (two comments said cairn_next.py wrote the fixtures' `next`; gen_fixtures.py copies it and test_status_fixtures.py holds it to `recommend`).

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
