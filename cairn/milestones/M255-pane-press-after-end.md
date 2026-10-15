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
- **Branch/PR:** m255-pane-press-after-end   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: After a session end, a pane press whose checks pass runs its
      command even when a press check begun before the end has not settled
      by the end. Shown by a `hooks/status/pane.test.tsx` case: a Status
      press's first `step` read, held once and armed after mount, has not
      settled when the session ends with reason `clear`; a second Status
      press then runs the Status command, and after the first press's read
      is released the commands are still exactly one Status run.
- [ ] AC2: A press check that settles after a session end runs no command
      and leaves no command held for a later clear end. Shown by AC1's case
      and a `hooks/status/pane.test.tsx` case in which a next-step press
      whose checks would hold a `/clear` command has its `step` read
      released only after a session end, and no command runs through that
      release and a later session end with reason `clear`.
- [ ] AC3: A ⌂ press's open of the pane still runs at its clear end when the
      mod's `next(e)` rejects in its `session.end` handler. Shown by a
      `hooks/status/pane.test.tsx` case in which `seat()`'s `session.end`
      handler throws behind a `Copy` flag, a ⌂ press precedes a session end
      with reason `clear`, the test catches `$.session.end`'s rejection, and
      one `ui.open` of the pane follows.
- [ ] AC4: The active profile's `verify` passes: `python3 -m unittest` for
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
