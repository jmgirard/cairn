<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M278: A failed read or session end leaves the cairn pane working

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the cairn pane and band are drawn for every user of the plugin's status mod   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m278-pane-failed-read-end, https://github.com/jmgirard/cairn/pull/290   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A ⌂ press whose step read fails, and a `/clear` session end whose handler
beneath fails, each leave the cairn pane's Buttons working, and the failed
end also resets the band, as a read or end that succeeds does.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `pressHome` in `hooks/status/register.tsx` (about line 1211) clears
its `homeRun` mark when its read of the stored step rejects, as
`pressChecked` clears `pressCheck` in a `finally`. The `session.end`
handler (about line 519) writes the stored `step`, `expanded`, `dismissed`,
and `ended` values on the rejected path as on the resolved path, for any
end reason (the criteria test `clear` ends), then
frees the run and press mark, hands off a held command, and opens the pane
for a ⌂ press's clear end, as it does now, and rethrows. Regression tests
in the mod's test files, a CHANGELOG Fixes entry, and the DESIGN.md lines
that describe the two paths.

**Out:** the third part of the "Rejected end edges (M260 review)" row, the
pane tests' short "nothing more happened" waits (`untilRuns` and
`untilOpens` at 10 tries), stays in that row, as does an end whose own
state write rejects and so skips `free()` (added to the row at this plan,
on either path). A ⌂ press's
`/clear` that brings no session end at all (DESIGN.md Known issues) stays
a known issue.

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

- [x] AC1: A ⌂ press whose read of the stored step rejects runs no
      `/clear` and leaves the Buttons free: a `pane.test.tsx` test denies
      that one read (the first `step` read after the ⌂ press, once) through
      a `state.get` hook, catches the press's rejection, then presses
      Status, and finds `copy.commands` equal to `[STATUS_RUN]`.
- [x] AC2: A session end of reason `clear` whose `next(e)` rejects writes
      the stored `step`, `expanded`, `dismissed`, and `ended` values as a
      resolved `clear` end writes them (`null`, `false`, `null`, `false`),
      and rejects with the message of the error `next(e)` threw: a test
      records the end's writes to those four keys through a `state.set`
      hook and finds them equal for a rejected and a resolved end; and for
      `step`, `dismissed`, and `ended`, a test gives the value its other
      state, rejects a `clear` end, and finds the band drawn as the same
      setup draws it after a resolved end.
- [x] AC3: A rejected end still opens the pane for a ⌂ press's `clear`
      end, frees the action Buttons, hands a held command to the prompt
      box with a toast, and cancels a ⌂ press whose step read it cut off:
      the four `pane.test.tsx` blocks "a ⌂ press's open still runs when the
      session end beneath rejects (M255 AC3)", "a rejected session end
      frees the action Buttons (M260 AC1)", "a rejected session end hands
      its held command to the prompt box (M260 AC2)", and "a session end
      during a ⌂ press's step read cancels its /clear (M260 AC3)" pass with
      no line in them changed from main.
- [x] AC4: `CHANGELOG.md`'s Unreleased Fixes section carries one entry for
      the two fixes, and each behavior it states is one an AC1 or AC2 test
      asserts.
- [x] AC5: The `verify` slot of `cairn/PROFILE.md` is green: both
      `unittest` suites, both `claude plugin validate` runs, and
      `claude plugin test .`, each exit code 0.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T3, T4
- AC3 → T4
- AC4 → T5
- AC5 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write the AC1 test in `pane.test.tsx` first: a `state.get` hook
      answers `{ deny }` for the ⌂ press's `step` read (the lesson on
      `claude plugin test` hooks: a throw is skipped, `{ deny }` rejects).
      Run it on the current code and see it red for AC1's reason (the
      Status press runs nothing), not a crash.
- [x] T2: In `pressHome`, clear `homeRun` (when it is still the press's
      mark) on a rejected step read, in the `try`/`finally` shape of
      `pressChecked`; the rejection goes on. See the T1 test green.
- [x] T3: Write the AC2 tests first: the `state.set` write record (`update`
      always writes, so a resolved end writes all four), and one drawing
      test each for `step`, `dismissed`, and `ended` (`expanded` draws
      nothing; only `prompt.submit` reads it). The band tests' `seat` needs
      an `endThrows` switch like the pane tests' copy, or the tests go in
      `pane.test.tsx`. See each red on the current code for its own reason.
- [x] T4: Restructure the `session.end` handler so the four updates run on
      both paths before `free()`, the held-command hand-off, and the ⌂
      open; the rejected path rethrows `next(e)`'s error after them. See
      the T3 tests and the four AC3 blocks green with no line in them
      edited.
- [x] T5: Add the CHANGELOG Fixes entry, written from the T1 to T4 test
      output. Update DESIGN.md's two descriptions (the `pressHome` lines
      near 536 and "An end whose `next(e)` rejects skips those updates"
      near 225). Grep README.md and DESIGN.md for other sentences about a
      failed end or the ⌂ step read and fix any the change makes false.
- [x] T6: Run the five `verify` commands from the repo root, each exit code
      checked on its own.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: not run — work named at the question set.
- 2026-10-18: question set: which work to plan — "Pane rejected-read fixes"; the user chose it over the row's "promote when one shows in a real session" condition.
- 2026-10-18: collision: candidate row "Rejected end edges (M260 review)" absorbed in part (its first two items); its third (short negative test waits) stays in the row, which takes the started token. No D-entry collides; M241, M255, M260 shipped the code this extends. Inbox: 0 open issues, 0 open PRs.
- 2026-10-18: criteria audit (full, fresh Opus reader): AC1 "denies that read" read two ways → narrowed to one read, once; AC2 unobservable for `expanded` in the band → split into a `state.set` write record for all four and drawing tests for three; AC2 end reason unbounded → narrowed to `clear`; AC2 error clause cannot go red → reworded as the rethrown message; AC3 bound test files → restated as behavior, and the M260 AC3 block added; T4's "even when an update rejects" had no AC → dropped from T4 and added to the candidate row; Goal's "band reset" also covered the ⌂ read → reworded. AC4, AC5: no finding.
- 2026-10-18: plan gate chose writing the four values on the rejected end path over leaving them (treating a failed end as no end) because M260 already treats a failed end as an end (it frees the Buttons and opens the pane); falsified by a real session that goes on after a rejected `next(e)` with its old step still true.
- 2026-10-18: plan gate chose a `try`/`finally` inside `pressHome` over routing it through `pressChecked` because the ⌂ press holds `homeRun`, not `pressCheck`, and its `/clear` is not a held command; falsified by a third press kind needing the same mark handling.
- 2026-10-18: lessons surfaced: `{ deny }` rejects a hooked call where a throw is skipped (M191, M237; T1); doc surfaces restate behavior, so grep README and DESIGN (M112; T5); run each gating suite and check each exit code (M56; T6).
- 2026-10-18: implement started on branch m278-pane-failed-read-end; untracked `cairn-probe.log` and `tsconfig.json` predate the milestone and stay unstaged.
- 2026-10-18: T1: AC1 test in pane.test.tsx red on main for its own reason (denied read once, no `/clear`, Status press ran nothing: received undefined).
- 2026-10-18: T2: `pressHome` takes its mark back in a `finally` when the step read rejects; T1 test green; verify green (scripts 418 OK, hooks 179 OK, both validates 0, plugin test 2077 pass).
- 2026-10-18: T3: AC2 tests in band.test.tsx (a `stateWrites` record in the kit's one `state.set` hook, since the kit refuses a second; drawing tests for step, dismissed, ended on both surfaces); all 7 red on the pre-T4 handler (rejected end wrote nothing; old step row, hidden band, Clear Button drawn).
- 2026-10-18: T3: `session.end` takes no `{ deny }` and a throwing hook is skipped, so the rejected `next(e)` carries the kit's "no implementation for session.end"; the test asserts that text (`NO_END`), which `register.tsx` never writes (git grep, no match).
- 2026-10-18: T4: the `session.end` handler catches `next(e)`'s error, runs the four updates, `free()`, the held-command hand-off (`the session end failed` on a rejected end), and the ⌂ open on both paths, then rethrows; T3 tests and the four AC3 blocks green, no line in those blocks edited; verify green (scripts 418 OK, hooks 179 OK, both validates 0, plugin test 2084 pass).
- 2026-10-18: T5: CHANGELOG Fixes entry (the ⌂ press after a failed step read; the band reset after a failed `/clear` end), each behavior one the AC1 or AC2 tests assert; DESIGN.md's rejected-end line (near 225) and `pressHome` line (near 539) updated; a grep of README.md and DESIGN.md for failed-end and step-read sentences found none the change makes false. The simple-english hook flags 368 older hits in CHANGELOG.md; the new entry lints clean alone.
- 2026-10-18: T6: verify green from the repo root, each exit code 0 (scripts 418 OK, hooks 179 OK, plugin and marketplace validate, plugin test 2084 pass); cairn_validate all checks passed.
- 2026-10-18: claim audit: 35 claims read, 3 corrected — CHANGELOG.md (the ⌂ sentence said "now runs no `/clear`", which main also did, and "every pane button", though `↻` was never blocked and the band's action Buttons were), hooks/status/band.test.tsx (the `endTwice` comment named the hook's thrown error, not the kit's `NO_END`); same reader re-read all 3 as true; verify green after (plugin test 2084 pass).
- 2026-10-18: implement complete; status set to review.
- 2026-10-18: review: PR #290 opened at review start (Copilot round on); Copilot requested on state `none`.

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

- AC1 (2026-10-18, head 5ceddd3f): `claude plugin test .` exit 0, 2084 pass; "a ⌂ press whose step read rejects leaves the Buttons free (M278 AC1) > the ⌂ press runs no /clear, and a Status press after it runs" passes: one `step` read denied, no command after the ⌂ press, `copy.commands` equal to `[STATUS_RUN]` after Status. Red on main at T1 (Status ran nothing).
- AC2 (2026-10-18, head 5ceddd3f): the 7 tests under "a rejected session end resets the band as a resolved one does (M278 AC2)" in band.test.tsx pass: the write record finds a resolved `clear` end writing step null, expanded false, dismissed null, ended false and the rejected end writing the same, with the rejection's message equal to the kit's `NO_END` (the error `next(e)` rejected with; `register.tsx` writes no such text, git grep no match); drawing tests for step, dismissed, ended on terminal and desktop find the band after a rejected end equal to the band after a resolved one. All 7 red before T4.
- AC3 (2026-10-18, head 5ceddd3f): the four named blocks' 12 tests pass (M255 AC3: 2, M260 AC1: 4, M260 AC2: 2, M260 AC3: 4). `git diff main...HEAD -- hooks/status/pane.test.tsx` is 34 added, 0 removed lines in one hunk after main line 4766, the end of the M260 AC3 block; each block's describe name appears once on main and once at head.
- AC4 (2026-10-18, head 5ceddd3f): `git diff main...HEAD -- CHANGELOG.md` adds 10 lines, 0 removed: one entry, the first under Unreleased `### Fixes` (CHANGELOG.md:509). Its behaviors map to tests: the ⌂ press lets go of its hold and the other action buttons work again (AC1 test: Status runs after the denied read); after a failed `/clear` end the step goes, a hidden band shows, `Clear` goes (AC2 drawing tests for step, dismissed, ended). Its two "Before" sentences state main's behavior, read against `git show main:hooks/status/register.tsx` by the claim audit and shown by the red runs at T1 and T3.
- AC5 (2026-10-18, head 5ceddd3f): the five verify commands from the repo root, each exit 0: scripts/tests 418 OK (21 skipped), hooks/tests 179 OK, plugin.json validate, marketplace.json validate, `claude plugin test .` 2084 pass 0 fail.
- gate (2026-10-18): `cairn_validate.py` exit 0, all checks passed; no DESIGN.md principle changed, so `cairn_impact` skipped; consistency-gate slot: verify green on the review head (AC5), marketplace validate shows no `plugins[N].version` warning, CHANGELOG.md has the entry (AC4) with no milestone id in it. No CI in this repo (profile).
