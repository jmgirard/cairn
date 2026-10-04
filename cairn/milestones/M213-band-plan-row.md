<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M213: A Plan button on the empty band

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the band draws in every adopter's session   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m213-band-plan-row   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When a cairn repo has no milestone to work on, the status band shows a row with a button that starts planning.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a band row for a found ROADMAP with no `in-progress` or `review`
row and no workable `planned` row (today the band draws nothing then,
`hooks/status/band.ts:271`, `register.tsx:284`). The row's left side is
the text `No milestone ready`. Its right side carries a `Plan` button and
M212's `Status` button, under M212's show rules, then the open and close
buttons. A `Plan` press runs `/cairn:milestone-plan` through M212's `run`.
The close button hides the row as it hides other rows. README, DESIGN, and
CHANGELOG describe the row. One live look in a desktop Code session
(question set).

**Out:** a clickable next command in the cairn pane, which stays in the
"Status mod follow-ons" candidate row. The row does not name a planned
milestone that waits on a dependency or a `blocked` one. The pane's queue
already lists those (M205). M212's open follow-ons stay in "Band button
follow-ons (M212 review)".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: When the reader finds and parses a ROADMAP (the pane state's
      `found` is true) with no `in-progress` or `review` row and no
      workable `planned` row, the band draws one row whose left side is the
      text `No milestone ready` in the theme's gray and whose right side
      ends in the open and close buttons. When no ROADMAP is found, the band
      still draws nothing. `band.test.tsx` cases show both.
- [x] AC2: On that row, while no cairn skill's step is set and `isWorking`
      is not true, a `Plan` button and the `Status` button draw before the
      open and close buttons at every band width from 40 to 200 columns,
      on the terminal and the desktop surface, where the row's text keeps
      at least `TEXT_ROOM` (10) columns beside them, and at no other width
      in that range. M212's width sweep in `band.test.tsx` gains this row
      as a case, and other cases show the Buttons absent while a step is
      set and while `isWorking` is true.
- [x] AC3: A press of `Plan` runs the next step that the pane state holds
      at the press, as M212's next-step press does. When that step is
      planning, the press calls `$.command.run` with command
      `cairn:milestone-plan` and empty args. A press while another action
      Button's run is in flight calls nothing. A run that rejects appends
      `/cairn:milestone-plan` to the prompt box and toasts the reason.
      `band.test.tsx` cases cover the run, the in-flight press, and the
      rejection.
- [x] AC4: The close button on that row hides the band. A `band.test.tsx`
      case presses it, shows the band stays hidden after a refresh over the
      same ROADMAP and after a refresh that adds only a `planned` row
      waiting on an undone dependency, and shows the band again, as the
      idle row, after a refresh that finds a workable `planned` row.
- [x] AC5: README.md's "The milestone band" section and the `hooks/status/`
      paragraph of `cairn/DESIGN.md` describe the row and its `Plan` button,
      and CHANGELOG.md's `## Unreleased` section has an entry for them. The
      two sentences that `grep -n "draws nothing" README.md cairn/DESIGN.md`
      found at plan time saying the band draws nothing with no workable
      planned milestone (README.md:178-179, `cairn/DESIGN.md:162`) no longer
      say so.
- [x] AC6: The four verify checks in `cairn/PROFILE.md` exit 0 at the
      branch head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T2
- AC5 → T4
- AC6 → T1, T2, T4
- T3 maps to no criterion: it is the operator's look, and a change it asks
  for lands under AC1 to AC4.

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Model, tests first. Use the fixtures that already reach the
      state (`all-waiting`, `no-active`, `idle-deps`, per the audit), and
      add one only if none fits. Rewrite the cases that assert the band
      draws nothing in that state (`describe('the band draws nothing')`
      near `band.test.tsx:1481`, and the all-fixture sweeps that expect
      "the idle row or none" near :661). Add the cases for AC1 and AC2's
      width sweep. In `band.ts`, add the row's line (its own key, no id,
      no track) and its fit rule for the action Buttons beside
      `actionsFit`, and have `stepLines` return it in place of `[]` when
      the caller says a ROADMAP was found.
- [x] T2: Drawing and press, tests first. In `register.tsx`, draw the row
      when the pane state's `found` is true and nothing is active or
      workable. Add `Plan` to `NEXT_LABELS` for the planning next step. Let
      the next-step press run `cairn:milestone-plan` with empty args when
      the re-read next step is planning (today it returns at a null id). Keep the head Box from drawing a
      lone space for the row with no id. Cases for AC2's step and
      `isWorking` rules, AC3, and AC4. Check `mark` and `same` need no
      change for AC4.
- [x] T3: Live look (question set: one stop). Make a scratch repo outside
      this checkout whose `cairn/ROADMAP.md` has no active or workable row,
      ask the operator to open a new desktop Code session there (LESSONS
      M195: a session keeps the mod it loaded at start), and record what
      they saw in one work-log line. A change the look asks for is made
      here, with its tests.
- [x] T4: Docs. README's band section and the DESIGN paragraph per AC5,
      plus the DESIGN `hooks/status/` lineage line (`… and the empty-band
      row in M213`). CHANGELOG `## Unreleased` entry under `### New`. Run
      the claim audit over the branch-added prose claims. Run all four
      verify checks.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to work on — a Plan button on the empty band (promoted from the "Status mod follow-ons" candidate row's M212-Out item; the row is pruned at post-merge hygiene, not here).
- 2026-10-04: question set: stop once during implement for a live look in a new desktop Code session — yes, one live look (T3).
- 2026-10-04: collision check: the "Status mod follow-ons" candidate row holds this item (absorbed). D-143 (the mod ships in the plugin, its checks gate) is read and planned under, not changed. No open GitHub issues or PRs. No checker-regress shape. Not release-shaped.
- 2026-10-04: lessons harvested: M193/M194 (`minWidth: 0` and `flexShrink: 0` on the row's Boxes, short Button labels), M195 (a live look needs a new Code session), M204 (look prototypes in the browser pane first if the look is in doubt), M112 (sweep README and DESIGN for the old wording, hence AC5's grep).
- 2026-10-04: plan gate chose a text-only left side, `No milestone ready`, over showing the first candidate row's title because candidates are not milestones and the pane already lists them (M207); falsified by an operator at the live look or later finding the row's text uninformative.
- 2026-10-04: plan gate chose the text `No milestone ready` over `Nothing planned` because a `planned` row waiting on a dependency or a `blocked` row makes "nothing planned" false; falsified by the live look reading the text as wrong for the repo's real state.
- 2026-10-04: plan gate chose to reuse M212's next-step press, which runs the next step re-read at the press, over a plan-only press that does nothing once the next step changes, because the planning next step already comes from `recommend` (`reader.ts:445`) and M212's buttons follow the same rule; falsified by a live press on `Plan` that starts a milestone the operator did not mean to start.
- 2026-10-04: criteria audit (full mode, fresh Opus reader) returned 8 findings, all taken toward the narrower promise: AC3's stale-press no-op cases cannot be staged by the test kit and a reused press runs the re-read step, so AC3 now states M212's rule and tests the run, the in-flight press, and the rejection; AC2's "wherever" now names M212's 40 to 200 column sweep on both surfaces; AC1 now requires a parsed ROADMAP (`found` true); AC1's fixture clause (an instrument) is dropped and T1 uses existing fixtures; T1 now rewrites the cases that assert the band draws nothing; Coverage notes T3 maps to no criterion; AC4 adds the waiting-row refresh that keeps the band hidden. AC5, AC6, and the IP check returned nothing.

- 2026-10-04: implement: set in-progress on branch `m213-band-plan-row`. The untracked `cairn-probe.log` and `tsconfig.json` in the tree are not this milestone's and stay unstaged.
- 2026-10-04: T1 done: `band.ts` gains `emptyLines` (key `plan-row`, no id, text `No milestone ready`), a `found` argument to `stepLines`, a zero-width head for an empty id, and the empty row in `actionsFit`; two unit cases in `band.test.tsx` (the row by `found`, and the fit at 37 but not 36 columns with 25 reserved). Minor amendment: the rewrites of drawn cases that assert an empty band draws nothing move to T2, since they need the drawing. `claude plugin test .` 1081 pass.
- 2026-10-04: T2 done: `register.tsx` draws the empty row when the pane state's `found` is true, labels the planning step `Plan`, runs a planning press with empty args, and draws no head Box for an empty id; `mark` and `same` needed no change (the AC4 case passes on them). Tests: new describes for AC1 (2 fixtures plus 2 `noneWorkable` copies, with and without a skill), AC2/AC3 (press, hide, refusal, in-flight), and AC4; the empty rows join the M197 and M212 width sweeps, the latter requiring the Buttons at all 161 widths; 10 cases that asserted an empty band rewritten. Planted defects went red for their reasons: a press that returns on a null id (8 fail, `commands` undefined), and `actionsFit` without the empty row (20 fail, "empty row Buttons at 0 of 161 widths"). All four verify checks exit 0, `claude plugin test .` 1103 pass.
- 2026-10-04: T3 done: the operator found opening a session in a scratch folder annoying; the look ran instead in a new desktop Code session in `/Users/jmgirard/github/bsync`, a cairn repo with nothing workable (the plugin is a symlink to this checkout, so the session loaded the branch). The operator reported the band reads `No milestone ready` with Plan, Status, the pane button, and the close button, and looks right. No change asked for.
- 2026-10-04: T4 done: README's band section (the opening sentence, a new empty-row paragraph replacing "the band draws nothing", and the close button's re-show rule), DESIGN's `hooks/status/` paragraph (lineage, the right-group sentence, and the empty-row description replacing "With an empty list the band draws nothing"), and a CHANGELOG `### New` entry.
- 2026-10-04: claim audit: 34 claims read, 5 corrected — README.md (a hidden idle row also shows again as the empty row), CHANGELOG.md (session end re-shows; the `cairn:` command names), cairn/DESIGN.md (session end re-shows), hooks/status/band.ts (header comment: the empty row needs a found ROADMAP and has no id).
- 2026-10-04: implement complete: all four verify checks exit 0 at the head (`claude plugin test .` 1103 pass); status set to review.
- 2026-10-04: review: three-lens fan-out, 21 findings: 5 fixed on the branch (eebd0fa), 5 rejected, 11 to the new candidate row "Empty band row follow-ons (M213 review)". ROADMAP: the M211 done row pruned for the line cap, and the reasoning-effort row's re-check note shortened for the byte budget.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Evidence at `06c9b3b`, 2026-10-04, branch current with `origin/main` (`ac39d7d`).

- AC1: `claude plugin test .` exit 0, 1103 pass. Passing cases: "a found ROADMAP with nothing active or workable draws the empty row (M213 AC1)" (all-waiting, candidates-skeleton, and `noneWorkable` copies of no-active and idle-deps, each with no skill and with milestone-plan, on both surfaces: one `plan-row`, left group the gray `No milestone ready` alone, no track, ends in open then close), its fixture-domain case, and "the band draws nothing where no ROADMAP is found" (no-roadmap with and without a skill).
- AC2: same run. The M212 width sweep "the action Buttons give way before the title loses its room (M212 AC4)" passes for `all-waiting: plan-row` and `candidates-skeleton: plan-row`, which require both Buttons at all 161 widths 40 to 200 on both surfaces with the text's room at least 10; the unit case shows the fit at 37 and not 36 columns with 25 reserved. Absent while a step is set or `isWorking` is true: "a running cairn skill and a working turn hide Plan and Status on the empty row" (both surfaces) and "with nothing workable, <skill> draws the empty row with no action Buttons (M213)" for all 10 skills.
- AC3: same run. "<fixture>: Plan runs /cairn:milestone-plan with no arguments, and Status runs /cairn:milestone" (2 fixtures, both surfaces: `commands` equals `{cairn:milestone-plan, ''}` then the status run, no fill or toast), "a refused Plan run appends /cairn:milestone-plan to the prompt box and toasts" (both surfaces), and "a Plan press while a run is in flight reaches no second run" (both surfaces). At T2 a planted press that returns on a null id turned the press cases red with `commands` undefined.
- AC4: same run. "the close button hides the empty row until a milestone is workable (M213 AC4)" passes on both surfaces: hidden after the press, after a turn end over the same ROADMAP, and after adding M094 waiting on the blocked M092; the idle row for M095 shows after adding M095 with its one dependency done.
- AC5: README.md lines 180-190 describe the empty row and its `Plan` and `Status` buttons, lines 201-204 its re-show rule; `cairn/DESIGN.md` lines 73, 84-86, and 164-174 describe it; CHANGELOG.md `## Unreleased` `### New` opens with "A Plan button on the empty band". `grep -n "draws nothing" README.md cairn/DESIGN.md` now returns README.md:130 (the running skill), README.md:223 (outside a cairn repo), and cairn/DESIGN.md:174 (no ROADMAP found); the plan-time sentences at README.md:178-179 and DESIGN.md:162 are gone.
- AC6: at `06c9b3b`: `python3 -m unittest discover -s scripts/tests` exit 0 (397 tests, OK); `python3 -m unittest discover -s hooks/tests` exit 0 (174 tests, OK); `claude plugin validate .claude-plugin/plugin.json` exit 0 (passed with warnings); `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exit 0 (1103 pass, 0 fail), with Claude Code 2.1.287.

Consistency gate: `cairn_validate.py` all checks passed; no IP/GP changed, so no `cairn_impact` run; the `generic` profile's consistency-gate names no toolchain checks.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: `refresh` writes `band` then `pane`, so a render between them can draw `Plan` on an idle row or the empty row after a found→not-found move, for one frame — follow-up, "Empty band row follow-ons (M213 review)".
- diff-bug #2: a stale `Start`/`Resume`/`Review` press now runs planning when the re-read step names no milestone, where M212 did nothing — fix now, fixed eebd0fa.
- diff-bug #3: a `cairn/ROADMAP.md` in a parent folder makes a nested non-cairn repo show the empty row and `Plan` — follow-up (the nearest-above search is documented and older than M213).
- diff-bug #4: the empty row's close mark equals the no-ROADMAP mark, so a hide lasts through a ROADMAP leaving and coming back — follow-up.
- diff-bug #5: the right group's margin and its leading gap Text both draw on the empty row, 4 blank columns before `[ Plan ]` — reject, planned change: the operator accepted the drawing at the T3 live look.
- diff-bug #6: `NEXT_LABELS` keys on the prose action string `plan the next milestone` — reject, false as a silent risk: the press cases assert the `Plan` label, so a rewording fails them.
- diff-bug #7: no test stages a render between the two writes or asserts `Plan` never labels a milestone row — follow-up, with diff-bug #1.
- diff-bug #8: the AC4 case does not show a hidden empty row re-shown by an active row, or kept hidden by a skill, both README claims — fix now, fixed eebd0fa.
- diff-bug #9: AC2's "at no other width" is vacuous in 40 to 200 since the threshold is 37 — reject, planned change: AC2 as written is met, and the unit case holds the 36/37 boundary.
- diff-bug #10: the CHANGELOG entry leaves out the 37-column condition — fix now, fixed eebd0fa.
- blame-history #1: M213 dropped M212's null-id guard, so a stale milestone-labelled press runs planning — fix now, fixed eebd0fa (the guard holds again for `Start`/`Resume`/`Review`; `Plan` keeps AC3's run-the-re-read-step rule).
- blame-history #2: a non-empty ROADMAP that parses to no rows (a cut write, a renamed header) draws the empty row — follow-up.
- blame-history #3: the empty row's close mark carries no repo identity — follow-up (same as diff-bug #4).
- blame-history #4: the `pane` read moved above the `dismissed` read — reject, false: the reviewer traced no behavior change, and the guard's outcome is unchanged for every state.
- blame-history #5: unwrapped prose lines in README and CHANGELOG — reject, style.
- prior-review #1: the M208 two-write race now flashes a whole row — follow-up (same as diff-bug #1).
- prior-review #2: with the null-id guard gone, a `Plan` press after a milestone turns workable starts that milestone, and a stale `Start` runs planning — fix now for `Start`, fixed eebd0fa; the `Plan` half is the planned AC3 behavior, its falsifier in the work log, recorded in the follow-up row.
- prior-review #3: a refused press appends with no separator to a draft, now for `/cairn:milestone-plan` too — follow-up (open in "Band button follow-ons (M212 review)").
- prior-review #4: the hide case starts the skill by a typed prompt, not a press-started skill — follow-up (open in "Band button follow-ons (M212 review)").
- prior-review #5: Buttons are counted at terminal width on the desktop, and the empty row has no track to give back — follow-up.
- prior-review #6: the desktop look beside the Buttons is unswept for the empty row — follow-up.

Fix-now re-verify at eebd0fa: all four verify checks exit 0, `claude plugin test .` 1105 pass. The stale-press guard cannot be staged in the test kit (it presses the current drawing), as M212 recorded.
