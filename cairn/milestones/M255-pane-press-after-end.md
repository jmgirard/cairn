<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M255: Pane Buttons recover after a session end

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane ships to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m255-pane-press-after-end https://github.com/jmgirard/cairn/pull/266   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A pane Button press whose check was cut off by a session end neither freezes later presses nor runs late, and a ⌂ press still opens the pane when the session-end chain rejects.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `session.end` frees the shared press mark (`pressCheck`), and `pressChecked`
drops a check that settles after an end; `openHome` runs at a clear end even
when the mod's `next(e)` rejects. Tests in `hooks/status/pane.test.tsx`,
with one-shot holds and a throwing `session.end` behind `Copy` flags in
`seat()`.

**Out:** a press in flight from a reloaded module, the queued-⌂ against typed-`/clear`
race, an open that revives a closed pane, a non-`clear` end's silent drop,
and `openHome`'s session `$` stay in "Home Button edges (M241 review)" and
"Shared press mark edges (M243 review)" (live looks); a held Plan,
Implement, or ✎ command dropped when `next(e)` rejects joins "Shared press
mark edges (M243 review)"; the ✎ rows' gaps stay in "Plan Button edges
(M242 review)".

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

- [x] AC1: After a session end, a pane press whose checks pass runs its
      command even when a press check begun before the end has not settled
      by the end. Shown by a `hooks/status/pane.test.tsx` case: a Status
      press's first `step` read, held once and armed after mount, has not
      settled when the session ends with reason `clear`; a second Status
      press then runs the Status command, and after the first press's read
      is released the commands are still exactly one Status run.
- [x] AC2: A press check that settles after a session end runs no command
      and leaves no command held for a later clear end. Shown by AC1's case
      and a `hooks/status/pane.test.tsx` case in which a next-step press
      whose checks would hold a `/clear` command has its `step` read
      released only after a session end, and no command runs through that
      release and a later session end with reason `clear`.
- [x] AC3: A ⌂ press's open of the pane still runs at its clear end when the
      mod's `next(e)` rejects in its `session.end` handler. Shown by a
      `hooks/status/pane.test.tsx` case in which `seat()`'s `session.end`
      handler throws behind a `Copy` flag, a ⌂ press precedes a session end
      with reason `clear`, the test catches `$.session.end`'s rejection, and
      one `ui.open` of the pane follows.
- [x] AC4: The active profile's `verify` passes: `python3 -m unittest` for
      `scripts/tests` and `hooks/tests` from the repo root, `claude plugin
      validate` on the plugin and marketplace manifests, and `claude plugin
      test` for the status mod.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Tests first: a one-shot `step` hold through an `on('state.get')`
      override armed after mount (pane.test.tsx ~3165 shows the pattern);
      the AC1 and AC2 cases, red. Then `pressCheck = null` in the
      `session.end` handler (register.tsx ~516) and a stale-mark return in
      `pressChecked` after `await checks()` (~1112). Run `verify`.
- [x] T2: Tests first: a `Copy` flag that makes `seat()`'s `session.end`
      (~173) throw; the AC3 case, red. Then make the open at a clear end
      (~535) run when `next(e)` rejects, keeping the rejection. Run `verify`.
- [x] T3: CHANGELOG entry; run `verify`.

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

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: not run — work named at the question set.
- 2026-10-15: question set: which pane work — "Button press reliability", "Pane read and draw edges", "Started mark edges", planned as M255, M256, M257 in that order; live look — tests are enough, no live look owed.
- 2026-10-15: collision check: candidate rows only; no D-entry covers the pane; inbox sweep 0 open issues, 0 open PRs. The rows stay until this milestone's hygiene narrows them (records-hygiene §1).
- 2026-10-15: criteria audit (full, Opus fresh reader, one reader for M255-M257, with throwaway probe tests in a scratch copy) — 8 findings, all taken: see the per-milestone line below.
- 2026-10-15: audit findings for M255: AC3's trigger named the mod's own `next(e)` rejecting (a second `session.end` registration fails to load, and on the host another handler's rejection does not reach `next(e)`); AC1's case releases the stale read and asserts one Status run, which covers AC2's non-held branch; AC1 says "whose checks pass" and "has not settled by the end".
- 2026-10-15: ROADMAP: the three upstream-blocked rows ("Pane Button takes two clicks (upstream)", "Band in the app's code font", "Band label colors in other themes") merged into one row "Gaps only the app or mod API can close" with every fact and promotion condition kept, to fit three planned rows under the 60-line and 24,000-byte caps; no ROADMAP row or Known issues entry quoted their titles.
- 2026-10-15: plan chose to drop the ⌂ open when the pane is no longer listed out of scope because whether a `/clear` keeps the pane listed is unlooked live, and a wrong guess stops ⌂ from opening the pane at all; falsified by a live look showing the pane stays listed across a clear.

- 2026-10-15: T1 done: `holdStep` (a one-shot `state.get` hold on `step`, armed after mount) and the AC1/AC2 cases at the end of pane.test.tsx, both red first (no Status run after the end; the stale press ran `/clear`); then `pressCheck = null` in the `session.end` handler and `if (pressCheck !== mark) got = undefined` after `await checks()` in `pressChecked`. Plugin test 1731 pass 0 fail.
- 2026-10-15: T2 done: `Copy.endThrows` makes `seat()`'s `session.end` throw; the AC3 case was red (no open), then the mod's `session.end` handler catches a rejecting `next(e)`, opens the pane for a ⌂ press at a clear end, and rethrows. Implement choice: open in the catch and rethrow, not try/finally, so the later updates keep their present behavior on a rejection.
- 2026-10-15: T3 done: CHANGELOG Unreleased "Fixes" entry. Verify: scripts/tests OK (21 skipped), hooks/tests OK, plugin validate passed with warnings, marketplace validate passed, plugin test 1732 pass 0 fail.
- 2026-10-15: claim audit: 23 claims read, 3 corrected — CHANGELOG.md, hooks/status/pane.test.tsx. The CHANGELOG overstated the freeze (a read that settled freed the mark; ↻ was never blocked) and the cut-off rule's reach (⌂ does not use the press mark); the `holdStep` comment gave the end's update as a reason to arm after mount. Also fixed the stale `pressCheck` comment (register.tsx ~1101). Re-read pending.
- 2026-10-15: claim audit re-read: the 3 corrected claims and the stale comment now hold.

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

- AC1: pane.test.tsx "a Status press after the end runs once, and the cut-off press runs nothing" passes on fbdccbec: the held `step` read, the clear end, a second Status press giving `[STATUS_RUN]`, and after release still `[STATUS_RUN]`. Red before T1's fix (no second run). Met.
- AC2: the same case (no command from the released Status read) and "all-waiting: a cut-off next-step press holds nothing for a later clear end" pass: no command through the release and a second clear end. Red before T1's fix (`/clear` ran). Met.
- AC3: "a clear end whose next(e) rejects opens the pane once" passes: `$.session.end` rejects, one `{ id: 'cairn', title: 'cairn' }` open and no second within the wait; a no-press twin opens nothing. Red before T2's fix. Met.
- AC4: verify on fbdccbec: scripts/tests OK (21 skipped), hooks/tests OK, plugin validate passed with warnings, marketplace validate passed with no warning, plugin test 1733 pass 0 fail; `cairn_validate.py` all checks passed. Met.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: a rejecting `next(e)` still skips `running = false`, so a never-settling run keeps the Buttons dead — follow-up, new row "Press end edges (M255 review)" (pre-existing; the plan kept the later updates unchanged on a rejection).
- diff-bug #2: clearing `pressCheck` before `next(e)` let a new press read the ending session's state — fix now, fixed fbdccbec (an `ends` counter cuts off stale checks; the mark clears beside `running` after the end's updates).
- diff-bug #3: CHANGELOG left out the Clear press — fix now, fixed fbdccbec.
- diff-bug #4, #5: the "Shared press mark edges" and "Home Button edges" rows state gaps M255 closed — fix now at this milestone's hygiene (rows narrowed).
- diff-bug #6: a rejecting `next(e)` drops a held command with no prompt-box line or toast — follow-up, "Press end edges (M255 review)" (Scope Out).
- diff-bug #7: the catch's ⌂ open runs before the end's state updates — follow-up, "Press end edges (M255 review)".
- diff-bug #8: the hold could be taken by a read other than the press's — fix now, fixed fbdccbec (no command before the end is asserted).
- diff-bug #9: negative waits pass by timing out — noted; `await first` bounds them.
- diff-bug #10: AC2's second clear end adds no coverage — reject, false: it checks no command is held for a later clear end, which AC2 names.
- diff-bug #11: no cut-off ✎ or blocked-line case — reject, planned change: the criteria name Status and next-step, and all share `pressChecked`.
- diff-bug #12: `copy.hidden` dead in the AC3 test — fix now, fixed fbdccbec.
- diff-bug #13: AC3 lacks a no-press case and a late-duplicate wait — fix now, fixed fbdccbec.
- diff-bug #14: `let result` untyped — fix now, fixed fbdccbec (`unknown`).
- blame-history #1: same as diff-bug #6 — follow-up.
- blame-history #2: same as diff-bug #1 — follow-up.
- blame-history #3: the catch opens the pane though the clear may not have happened — follow-up, "Press end edges (M255 review)".
- blame-history #4: DESIGN.md's press paragraph not updated — fix now, fixed fbdccbec.
- blame-history #5: same as diff-bug #4, #5 — fixed at hygiene.
- blame-history #6: AC3 does not check a later press works — noted.
- blame-history #7: the cut-off applies to every end reason — noted, intended (M242's wording).
- prior-review #1: `pressHome` can still run `/clear` after an end during its `step` read — follow-up, "Press end edges (M255 review)".
- prior-review #2: same as diff-bug #1 — follow-up.
- prior-review #3: the catch-path open for a ⌂ press that never cleared — follow-up, "Press end edges (M255 review)".
- prior-review #4: same as diff-bug #4, #5 — fixed at hygiene.
- prior-review #5: same as blame-history #4 — fixed fbdccbec.
- prior-review #6: the reloaded-module press — noted, Scope Out, row keeps it.
- copilot: hooks/status/register.tsx (the mark cleared before `next(e)` lets a press overlap the end) — fix now, fixed fbdccbe; regression test with a held `next(e)` in 11f3c1e, red with the mark freed before `next(e)`.
- copilot: cairn/milestones/M255-pane-press-after-end.md (PR URL in Branch/PR) — fix now, fixed d4e141f.
- copilot: review body — noted.
- Copilot level: Lite (set by GitHub's settings).
- AC5-adjacent re-run after 11f3c1e: plugin test 1734 pass 0 fail.

