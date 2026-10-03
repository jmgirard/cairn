<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M201: A band label that holds through background waits

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the band ships in the plugin to every adopter   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m201-band-label-background-waits   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Keep a cairn skill's label on the band while the skill waits on background work and through the turns that the work's notices start.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `hooks/status/register.tsx` ends the skill's step at a main-loop
`classic.Stop` with no background work in flight. It also ends the step at a
prompt the user types while the session is idle. These replace M199's end at
every `turn.complete` with reason `answer`. Mod tests in
`hooks/status/band.test.tsx`. The step-end rule in README, CHANGELOG, DESIGN,
and the `register.tsx` comments. A live desktop look.

**Out:** A skill that waits through ScheduleWakeup or a cron (`session_crons`,
not `background_tasks`) still loses its label. Long-lived background work that
the skill did not start keeps a finished skill's label until the next typed
prompt. A typed prompt that a hook blocks or drops still ends the label,
because the hook clears the step before the prompt enters. README states all
three, and they go to the "Status mod follow-ons" candidate row with the work
of telling the skill's own tasks from other in-flight work.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: A `classic.Stop` with no `agent_id`, whose answer from beneath the
      mod carries no `block`, ends the running cairn skill's step when its
      `background_tasks` is empty or absent, and keeps the step when that list
      holds one or more tasks. A `classic.Stop` whose answer from beneath
      carries `block` keeps the step, and so does one with an `agent_id`. A
      `turn.complete` no longer ends the step, whatever its reason. `claude
      plugin test` cases show this. They raise `classic.Stop` five times: with
      an empty list, with no field, with a one-task list, with an empty list
      and a `block` from a hook beneath, and with an empty list and an
      `agent_id`. They also raise a `turn.complete` with reason `answer`. Each
      case then checks the band's skill label.
- [ ] AC2: The only hooks in `register.tsx` that start or end a step are
      `skill.prompt`, `session.end`, `classic.Stop`, and `prompt.submit`.
      Besides a cairn skill's prompt and a session end, a step, running or
      kept, ends at two events. One is the first later `classic.Stop` that AC1
      says ends a step. The other is a `prompt.submit` with origin kind
      `composer` or `bridge` and no `turnId`, unless a cairn skill's
      `skill.prompt` came after the last `classic.Stop`, `turn.complete`, or
      earlier `prompt.submit`; that prompt keeps the step. A turn that a
      `task-notification` prompt starts keeps the step. The `prompt.submit`
      hook in `register.tsx` names those two kinds and no other as ending a
      step. A typed cairn slash command thus keeps the label that its own
      `skill.prompt` sets, whether the engine raises that `skill.prompt` before
      the command's `prompt.submit` or beneath it. `claude plugin test` cases
      show this. After a Stop with one task keeps a step, they raise ten
      prompts: `task-notification`, `composer`, `bridge`, `peer`, `composer`
      with a `turnId`, `composer` after a cairn `skill.prompt`, `composer` with
      a beneath hook that raises `skill.prompt` before it resolves, and
      `composer` after each of these: a cairn `skill.prompt` then a
      `classic.Stop` with one task, a cairn `skill.prompt` then a
      `turn.complete`, and a non-cairn `skill.prompt`. Each case then checks
      the label.
- [ ] AC3: With one `in-progress` row and one `review` row and
      `/milestone-review` running, a `classic.Stop` that lists one background
      task keeps the `review` row under the `review` label, and so does the
      turn that a `task-notification` prompt then starts. A `claude plugin
      test` case shows this. It checks the drawn row after each event.
- [ ] AC4: In a live desktop session in this repo, one `/milestone-review` or
      `/milestone-plan` run starts a background subagent and ends its turn to
      wait. The band shows the skill's label during the wait and through the
      turn that the subagent's notice starts. After the skill's closing turn
      ends with no background work in flight, the band shows no skill label. In
      a second background wait, in a later wait or another run, a prompt the
      operator types ends the label.
- [ ] AC5: Each of four passages states the step-end rule of AC1 and AC2. The
      README and CHANGELOG passages also state the interrupt behavior that T4
      records and the three limits in Scope Out. The passages are:
      1. the band paragraph of `README.md` that names
         `mcp__ccd_session__mark_chapter`
      2. the band bullet of the Unreleased section of `CHANGELOG.md`
      3. the `hooks/status` paragraph of `cairn/DESIGN.md` that names the
         `step` state value
      4. the comments in `hooks/status/register.tsx` on the file header,
         the `step` atom, and the `classic.Stop`, `prompt.submit`, and
         `turn.complete` hooks.
- [ ] AC6: The `verify` slot of `cairn/PROFILE.md` runs clean: both gating
      `python3 -m unittest` suites, `claude plugin validate`, and `claude
      plugin test`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T4
- AC5 → T2, T3
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Tests first in `hooks/status/band.test.tsx`: beneath-hooks for
      `classic.Stop` and `prompt.submit` in the setup. Add the AC1 to AC3
      cases. Rewrite the existing cases that end a step with `turn.complete`.
      Show the end cases red on the current `register.tsx`. Show the
      clear-before-`next` case red against a clear-after-`next` variant. Show
      that a test-given `origin` reaches the mod's hook.
- [x] T2: In `hooks/status/register.tsx`, add a `classic.Stop` hook and a
      `prompt.submit` hook that carry the rule. Each hook calls `refresh`.
      Reduce the `turn.complete` hook to a refresh. Update the comments that
      AC5 names.
- [x] T3: Update the README band paragraph, the CHANGELOG Unreleased band
      bullet, and the DESIGN `hooks/status` paragraph.
- [x] T4: Do a live look in the desktop app with the branch's mod loaded. It
      covers one skill run with a background subagent, a prompt typed during a
      second wait, and an Esc interrupt of a skill's turn. Record in the work
      log what the band showed, whether the interrupt kept or ended the label,
      and the typed prompt's origin kind, read from the session transcript or a
      temporary debug line. Then bring T3's wording in line with it.
- [ ] T5: Run the `verify` slot of `cairn/PROFILE.md`, each exit code checked
      on its own.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-02: created by /milestone-plan from the candidate row "Band skill label across background waits" (M199 review D1, B1). It extends M199.
- 2026-10-02: criteria audit (full mode, fresh Opus reader) returned 13 findings on the draft. AC1 had four: the blocked-stop case's task list, an untested `agent_id` axis, "result" for the answer from beneath, and evidence wording bound to the test file. AC2 had four: a typed prompt over a running turn, the clear-before-`next` order, an incomplete end list, and the desktop origin kind as a live-only fact. AC4 had an unnamed run and two unobserved facts. AC5 had a grep in place of the passages. The gate fixed all 13. AC3 and AC6 were clean.
- 2026-10-02: the same reader re-read the revised criteria. It found the earlier 13 resolved and returned five more: T1's red claim for keep cases, AC2's unbounded "only", the label cleared by a dropped prompt, one AC4 run that could not show both the notice turn and a typed-prompt end, and AC4 and AC5 clauses that bound a recording act. All five were fixed: AC2 names the four hooks that write `step`, AC4 uses a second wait, the dropped prompt became a third Scope Out limit, and the origin kind and Esc result moved to T4.
- 2026-10-02: plan gate chose ending the step at an unblocked main-loop `classic.Stop` with empty `background_tasks`. It rejected an end at the next typed prompt alone, and a restore of the last step at a `task-notification` prompt. The chosen rule keeps the label through the wait itself, and it does not linger after every closing summary. A live session falsifies it if `classic.Stop` does not reach the mod, or if `background_tasks` does not list a running background subagent.
- 2026-10-02: plan gate chose to let an idle `composer` or `bridge` prompt end a kept step. It rejected an end only at a Stop with nothing in flight. The chosen rule bounds the label when unrelated long-lived work stays in flight. A desktop-typed prompt that arrives with an origin kind other than `composer` falsifies it.
- 2026-10-02: implement started on branch m201-band-label-background-waits. No question gate: the plan left no choice open.
- 2026-10-02: T1 done. The AC1 to AC3 cases and the rewritten M199 cases ran 18 red, 610 green on the old `register.tsx`. Every end case was red, and each keep case was red at its closing empty-list Stop. A clear-after-`next` variant of the `prompt.submit` hook failed the slash-command case alone ("brief" expected, "implement" drawn). Each prompt case asserts that the test's origin kind and turn id reached the hook beneath.
- 2026-10-02: T2 done. `register.tsx` gains `classic.Stop` and `prompt.submit` hooks, and `turn.complete` only refreshes. The header, `step` atom, and hook comments state the rule, and so does the `CairnStep` comment in `types/index.d.ts`. Verify: scripts 395 OK, hooks 174 OK, validate passed with its one CLAUDE.md warning, plugin test 628 pass.
- 2026-10-02: T3 done. The README band paragraph, the CHANGELOG band bullet, and the DESIGN `hooks/status` paragraph state the Stop and typed-prompt rule and the three Scope Out limits. The DESIGN history line names M201. The old "interrupt or error keeps it" sentences are gone; T4's Esc result supplies the interrupt sentence. Verify 4/4 green, `cairn_validate` green.
- 2026-10-02: T4 started. Temporary `$.ui.log` debug lines in the `classic.Stop` and `prompt.submit` hooks print each Stop's agent, in-flight list, and block, and each prompt's origin kind and turn id, because the session transcript records a typed prompt as origin `human`, not the hook's kind. They come out before review. Waiting on the operator's live look in a new desktop Code session.
- 2026-10-03: T4 debug lines moved to a helper that appends each Stop, prompt, skill prompt, and turn end, with the step the band then draws, to `.m201-band-debug.log` (excluded in `.git/info/exclude`), because `$.ui.log` lines do not reach the session transcript file. This session drives the live-look session by peer messages and `stop_session`, and the operator types one prompt. Plugin validate passed, plugin test 628 pass.
- 2026-10-03: T4 live look, run 1, ran main's mod, because opening the new desktop session switched the `cairn` checkout to `main` (reflog 15:12). The checkout went back to the branch, and run 2 used a session with the branch picked.
- 2026-10-03: T4 live look, run 2 (`/cairn:milestone-plan` dry run, one background subagent). The Stop during the wait listed `subagent:running`. The typed prompt arrived as origin `composer` with no `turnId`, the subagent's hand-back as `peer`, and the Esc interrupt (here `stop_session`) raised `turn.complete` reason `aborted` and no Stop, so the label stayed until the operator's next typed prompt ended it. Defect: the engine raised the typed command's `skill.prompt` 25 ms before its `prompt.submit`, so that prompt cleared the label it had just set, and the label was gone for the whole wait.
- 2026-10-03: amendment gate: the operator chose a short-lived `expanded` mark that a cairn `skill.prompt` sets and every Stop, turn end, and prompt clears, over matching the prompt text against cairn command names and over dropping the typed-prompt end. The mark works with either event order. A live session falsifies it if a typed cairn slash command's label is gone during its first background wait.
- re-audit: AC2 (full) — two findings: the typed-prompt end clause contradicted the slash-command clause (repaired with an "unless a cairn skill's `skill.prompt` came after" carve-out), and no case tested the mark's lifetime or a non-cairn skill (three cases added, ten in all).
- re-audit: AC2 (full) — three findings, all repaired: `tool.call` also writes `step` (now "start or end a step"), "the last `prompt.submit`" could include the judged prompt (now "earlier"), and "over a kept step" misdescribed two cases (now "After a Stop with one task keeps a step"). This is AC2's second re-audit, so further churn goes to the operator.
- 2026-10-03: AC2 amended to the wording above. `register.tsx` gains the `expanded` atom (`types/index.d.ts` contract entry), and `band.test.tsx` gains the engine-order case and three lifetime cases. The engine-order case ran red on the old hook. Removing the clear at Stop, the clear at turn end, or the cairn-only guard each turned its own case red. README, CHANGELOG, and DESIGN state the interrupt result and the mark. Plugin validate passed, plugin test 632 pass. T4 stays open for one more live look on the fixed mod.
- 2026-10-03: the AC2 amendment took the plan-owned body to 155 lines. The criteria, Scope, and Tasks text was rewrapped to 79 columns with no word changed, and the Tasks dropped their stale file line references, to land under the cap.
- 2026-10-03: T4 done. Live look, run 3, on the fixed mod (`d331c2c`), session opened on the branch. Phase 1: the typed `/cairn:milestone-plan` kept its label (`skill.prompt`, then `prompt.submit` origin `composer`, step `milestone-plan`). The Stop during the wait listed `subagent:running` and kept it, the notice turn (the subagent's hand-back, origin `peer`) kept it, and that turn's Stop with an empty list ended it. Phase 2, started by a peer message whose `skill.prompt` came from the Skill tool: the wait's Stop kept the label, and the operator's typed word (origin `composer`, no `turnId`) ended it at 20:36:20. The step values come from the debug log, which records the step the band draws after each event. The temporary debug code is gone, and `.m201-band-debug.log` and its exclude line are deleted. README, CHANGELOG, and DESIGN already state the interrupt result from run 2.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->
