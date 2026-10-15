<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M256: Pane reads after late placement

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane ships to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m256-pane-late-placement   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A pane placed while a clear start is still listing panes gets its pull-request read at once, and the placed-and-shown test lives in one place.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** After the classic `SessionStart` hook sets `owed`, a pane that became placed
during its pane-list await gets its read without a further draw. A test pins
the `owed` reset at `session.end`. One predicate replaces the three spellings
of the placed-and-shown test. A `Copy` flag in `seat()` holds a `ui.panes`
answer.

**Out:** the render hook's first-draw read and its ⋯ (unlooked live), the second
`startRead` check's test (harness ordering unknown), the end-before-start
assumption, `owed` after a pane closed before its first draw, the same race
on a resume start, and the 20 ms `settled()` window stay in "Pane edges
(M238 review)".

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

- [ ] AC1: A pane that becomes placed and draws while a clear start's
      classic hook awaits the pane list gets its pull-request read without a
      further draw. Shown by a `hooks/status/pane.test.tsx` case that holds
      the hook's first `ui.panes` answer (computed as not placed) through a
      `Copy` flag in `seat()`'s `ui.panes` handler, places and draws the pane
      during the hold, releases it, and sees each blocked pull-request URL
      read once with no second draw.
- [ ] AC2: A pane owed a read when its session ends reads nothing at its
      first draw after the end. Shown by a `hooks/status/pane.test.tsx`
      case: a clear start leaves the unplaced pane owed a read, the session
      ends, the pane is placed and drawn, and no read runs; with the `owed`
      reset removed from the `session.end` handler, the case fails.
- [ ] AC3: `hooks/status/register.tsx` spells the placed-and-shown test
      once, in one function that the command hook's close branch,
      `isShown`, and `markReopen` call: `grep -c "\.isShown"
      hooks/status/register.tsx` returns 1.
- [ ] AC4: The active profile's `verify` passes: `python3 -m unittest` for
      `scripts/tests` and `hooks/tests` from the repo root, `claude plugin
      validate` on the plugin and marketplace manifests, and `claude plugin
      test` for the status mod.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Tests first: a one-shot `ui.panes` hold in `seat()` (~150) that
      computes its answer before holding; the AC1 case, red. Then, after
      `owed = true` (register.tsx ~273), list the pane again and read when
      it is now placed. Run `verify`.
- [x] T2: The AC2 case; check it fails with the `owed = false` line
      (~509) removed, then restore it. Run `verify`.
- [ ] T3: One placed-and-shown predicate used at ~294, ~744-747, and
      ~1236; existing tests unchanged. Run `verify`.
- [ ] T4: CHANGELOG entry; run `verify`.

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
- 2026-10-15: audit findings for M256: AC1 names the `seat()` hold (a second `ui.panes` registration fails to load) and "each blocked pull-request URL read once"; AC3's grep became `\.isShown`, which also catches the negated form at ~1236.
- 2026-10-15: plan chose a second pane listing after `owed = true` over `$.ui.invalidate('ui.render')` because a listing reads without a draw the host may delay; falsified by a test or live look where the second listing still answers not placed after the pane drew.
- 2026-10-15: started on branch m256-pane-late-placement; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-15: T1 done: `Copy.panesHold` (one-shot, cleared when reached, so a test sees the hold was hit); the AC1 case over blocked-active and blocked-prs went red at its final read assertion (reads `[]`) after the hold was reached and the held draw read nothing; the hook now lists again after `owed = true` and reads when placed and `owed` still holds (a draw, open, or end clears it). Verify green: 408 + 175 Python tests, both validates, 1736 mod tests.
- 2026-10-15: T2 done: the AC2 case (clear start owes, `CLEAR_END`, place, draw, no read); with the `session.end` handler's `owed = false` removed it alone failed, reading `[URL_1250]` at its last assertion (1 of 1737); restored, `register.tsx` back to no diff. Verify green: 1737 mod tests.


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
