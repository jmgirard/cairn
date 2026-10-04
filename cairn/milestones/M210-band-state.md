<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M210: The status band keeps the right state

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the status mod ships in the plugin and draws in every adopter's session   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m210-band-state   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The status band and pane show rows, steps, and the close state that match the session's real state in seven cases where they do not today.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the 2026-10-04 audit triage promoted these seven defects from the
"Status mod follow-ons" candidate row:

- a UNC share root in the upward ROADMAP walk,
- stale rows after the session moves to another repo,
- an empty ROADMAP text that empties the band,
- a close-button press racing a session end,
- the `dismissed` write at every refresh,
- a step lost while a skill waits on a one-shot cron,
- a dropped typed prompt that ends the step.

The scope also adds a test that edits the ROADMAP before a failed read, so kept
rows differ from a fresh read.

**Out:** each stays in the "Status mod follow-ons" candidate row, trimmed of
the promoted items at post-merge hygiene. A bare-named project skill such as
`hotfix` setting the step needs a live check of how a typed cairn command
arrives. Background work the skill did not start holding a step, and a one-shot
cron the skill did not create holding it, can only be guessed at. A ROADMAP cut
mid-table reads like a short file. Clickable next commands and `vscode`/`mobile`
surface tests are features, not defects.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `dirname` in `hooks/status/reader.ts` returns the UNC share roots
      `\\srv\share` and `//srv/share` unchanged and maps `\\srv\share\` and
      `\\srv\share\a` to `\\srv\share`, so `findRoot` started in
      `\\srv\share\a\b` probes no path above `\\srv\share`. A `reader.test.ts`
      test asserts each form and the list of paths `findRoot` probes.
- [ ] AC2: In the same repo root, a refresh whose ROADMAP read fails keeps the
      rows drawn before the failure, and a ROADMAP whose text is empty or only
      whitespace counts as a failed read. A `band.test.tsx` test edits the
      ROADMAP, makes the read fail, refreshes, and asserts that the band and
      the pane still draw the pre-edit row, then draw the edited row after the
      read succeeds again. A second test asserts the same keep for an empty
      ROADMAP text.
- [ ] AC3: The band state stores the repo root its rows came from. A refresh
      whose read fails draws the empty state in the band and the pane, never
      rows from another root, when the working directory is in a different
      repo root, when reading the working directory throws, or when no root is
      stored with the drawn rows. `band.test.tsx` tests cover each of the
      three cases.
- [ ] AC4: `reconcile` writes `dismissed` only when its value changes: a test
      asserts that a refresh with nothing hidden performs no `state.set` on
      `dismissed`. A close-button press whose `band` and `step` reads come
      before a `session.end` and whose write comes after it leaves `dismissed`
      null: a test starts with `dismissed` null and places the `session.end`
      between the reads and the write.
- [ ] AC5: At a `classic.Stop` with no background tasks, a running cairn skill
      keeps its step while `session_crons` holds at least one one-shot
      (non-recurring) entry, and the step ends when the crons are all
      recurring, empty, or absent. `band.test.tsx` tests cover one-shot only,
      one-shot plus recurring, recurring only, empty, and absent.
- [ ] AC6: An idle typed prompt (no `turnId`, `expanded` unset) that a hook
      beneath the mod drops (its `prompt.submit` result carries `drop`) leaves
      the step unchanged. One that goes through ends the step before any
      `skill.prompt` of its turn can set a new one. `band.test.tsx` tests
      assert both.
- [ ] AC7: The `verify` slot of `cairn/PROFILE.md` is clean: all four commands
      exit 0, each exit code checked.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1
- AC2 → T2
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T4
- AC7 → T1, T2, T3, T4, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: UNC roots. `dirname` (`reader.ts:225-232`) treats a `\\host\share`
      or `//host/share` head as a root. Add reader tests for each AC1 form and
      for the `findRoot` probe list (`memorySource`).
- [x] T2: Root-aware rows. `loadCairn` exposes the root it found and treats an
      empty or whitespace ROADMAP text as a failed read (`reader.ts:263-265`).
      The band state stores `root` under a new `shape` tag (LESSONS M193).
      `refresh` (`register.tsx:408-421`) keeps rows only when the failed read's
      root equals the stored one, and writes the empty state otherwise. Add
      band tests for AC2 in the describe block at `band.test.tsx:1239`, with
      the edit before the failed read, and for the three AC3 cases.
- [x] T3: `dismissed` writes. `reconcile` (`register.tsx:389-392`) reads first
      and writes only on a change. The press (`register.tsx:358-362`) writes
      only if no `session.end` landed since its reads, by a version-guarded set
      or a session-generation check. Add band tests for both AC4 halves.
- [x] T4: Step lifetime. `classic.Stop` (`register.tsx:186-195`) holds the step
      on a one-shot `session_crons` entry, and `stopWith` gains cron variants.
      `prompt.submit` (`register.tsx:206-215`) leaves the step when the result
      carries `drop` and keeps the end ahead of the turn's `skill.prompt`.
      `seat()` gains a drop flag. Add band tests for AC5 and AC6.
- [x] T5: Docs and gate. README, `cairn/DESIGN.md`, CHANGELOG, and the
      `register.tsx` and `reader.ts` comments describe the changed behaviors.
      Grep for the old wording (LESSONS M112). Run the four verify commands.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-04: created by /milestone-plan from the `/milestone` audit triage of the "Status mod follow-ons" row (user chose "Plan a milestone").
- 2026-10-04: question set: which band items to fix — the seven clear defects; the bare skill name, foreign background work, clickable commands, and vscode/mobile tests stay in the candidate row.
- 2026-10-04: question set: live check before the merge question — tests only, no live check.
- 2026-10-04: criteria audit (full): a fresh Opus reader returned 6 findings on M210 (AC1 share-root forms, the no-root case between AC2 and AC3, AC4's universal writer clause and the press-version conflict, AC5's mixed and absent cron cases, AC6's universal "goes through" clause), each fixed toward the narrower wording above.
- 2026-10-04: plan gate chose the seven clear defects over adding the bare-skill-name fix because a typed `/hotfix` may reach `skill.prompt` bare; falsified by a live check showing typed cairn commands always arrive as `cairn:<name>`.
- 2026-10-04: plan chose to treat an empty or whitespace ROADMAP text as a failed read over a delayed re-read of any empty result, because the re-read adds a timer to the refresh path; falsified by a real session where a ROADMAP cut mid-table empties the band.
- 2026-10-04: implement started on m210-band-state. The untracked `cairn-probe.log` and `tsconfig.json` in the tree are unrelated and stay unstaged.
- 2026-10-04: T1 done. `dirname` returns a `\\host\share` or `//host/share` head unchanged. Two new reader tests failed on their asserted values before the fix. Verify is clean: scripts 397 OK, hooks OK, validate passed with warnings, mod tests 1000 pass.
- 2026-10-04: T2 implementation choice: the root lives in the band atom's value (`band-4`, and `CairnBandState` gains `root`), and `readCairn` in reader.ts reports the root beside the state. A throw while parsing keeps the rows in the same root, as before, and only a throw from `$.session.cwd()` leaves the root unknown.
- 2026-10-04: T2 done. Ten new band tests cover AC2 and AC3 on both surfaces. Against the pre-T2 source, those ten failed on their row assertions: the six root cases kept the old row and the four empty-text cases emptied the band. The edit-before-failure test passed there too, as it guards the M200 keep. The harness's `state.set` hook sees a shaped value as `{ shape, value }`. Verify is clean: scripts 397 OK, hooks 174 OK, validate passed with warnings, mod tests 1012 pass.
- 2026-10-04: T3 implementation choice: the press takes the close state's version before its reads and writes through `$.state.set` with `ifVersion`, over a session-generation atom. Any write in between drops the press, and a second press hides the band. The engine needs the reference as a literal `const` (`DISMISSED_REF`).
- 2026-10-04: T3 done. Four new band tests cover AC4 on both surfaces. Before the fix they failed on their assertions: the refresh wrote `dismissed`, and the press hid the band over the session end. Verify is clean: scripts 397 OK, hooks 174 OK, validate passed with warnings, mod tests 1016 pass.
- 2026-10-04: T4 implementation choice: an idle typed prompt still ends the step before `next`, so a skill prompt of its turn sets the new step as before. On a `drop` the prompt puts back the step it ended, unless something set a step meanwhile. This keeps the M201 slash-command test green, which a clear after `next` would break.
- 2026-10-04: T4 done. Seven new band tests: five cron cases for AC5, and a dropped prompt for each of `composer` and `bridge` for AC6. Before the fix, the two keep cases and the two drop cases failed on their row assertions, and the three end cases passed as controls. Verify is clean: scripts 397 OK, hooks 174 OK, validate passed with warnings, mod tests 1023 pass.
- 2026-10-04: claim audit: 64 claims read, 5 corrected — types/index.d.ts, hooks/status/register.tsx, hooks/status/reader.ts, cairn/DESIGN.md, README.md, CHANGELOG.md. The same reader's re-read of the five is pending. Open concern, unclaimed by any line: a prompt that a hook drops puts back the step but not a `dismissed` cleared by the refresh before `next`. So a band hidden while `/milestone-review` moved it can show again.
- 2026-10-04: claim audit re-read: the same reader found all 5 corrected claims hold, and one comment line was rewrapped.
- 2026-10-04: T5 done. CHANGELOG gains an Unreleased "Fixes" entry. The README band section moves the wakeup and dropped-prompt cases out of the limits and adds the same-repo keep, the empty ROADMAP, the press at a session end, and the share root. The DESIGN band bullet and the `register.tsx` and `reader.ts` comments describe the M210 behavior. A grep for `session_crons`, `ScheduleWakeup`, `cannot be read`, and `blocks or drops` found no other site. Verify is clean: scripts 397 OK, hooks 174 OK, validate passed with warnings, mod tests 1023 pass.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
