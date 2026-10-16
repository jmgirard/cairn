<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M256: Pane reads after late placement

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane ships to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m256-pane-late-placement, https://github.com/jmgirard/cairn/pull/267   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [x] AC1: A pane that becomes placed and draws while a clear start's
      classic hook awaits the pane list gets its pull-request read without a
      further draw. Shown by a `hooks/status/pane.test.tsx` case that holds
      the hook's first `ui.panes` answer (computed as not placed) through a
      `Copy` flag in `seat()`'s `ui.panes` handler, places and draws the pane
      during the hold, releases it, and sees each blocked pull-request URL
      read once with no second draw.
- [x] AC2: A pane owed a read when its session ends reads nothing at its
      first draw after the end. Shown by a `hooks/status/pane.test.tsx`
      case: a clear start leaves the unplaced pane owed a read, the session
      ends, the pane is placed and drawn, and no read runs; with the `owed`
      reset removed from the `session.end` handler, the case fails.
- [x] AC3: `hooks/status/register.tsx` spells the placed-and-shown test
      once, in one function that the command hook's close branch,
      `isShown`, and `markReopen` call: `grep -c "\.isShown"
      hooks/status/register.tsx` returns 1.
- [x] AC4: The active profile's `verify` passes: `python3 -m unittest` for
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
- [x] T3: One placed-and-shown predicate used at ~294, ~744-747, and
      ~1236; existing tests unchanged. Run `verify`.
- [x] T4: CHANGELOG entry; run `verify`.

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
- 2026-10-15: T3 done: chose the name `placedAndShown(mine)`, taking a listing (`undefined` from `paneOf`, `null` from `listedPane`); the command's close branch, `isShown`, and `markReopen` call it; `grep -c "\.isShown" hooks/status/register.tsx` returns 1; `pane.test.tsx` untouched. Verify green: 1737 mod tests.
- 2026-10-15: T4 done: a Fixes entry in CHANGELOG.md names the `/clear` start only, since the AC1 test drives `source: 'clear'`; the second list sits in the branch that `clear` and `resume` share, so a resume start runs it too, untested and unclaimed (the resume race stays in "Pane edges (M238 review)" per Out). Verify green, `cairn_validate` all checks passed.
- 2026-10-15: claim audit: 21 claims read, 4 corrected — CHANGELOG.md (heading "at once" → "with no further draw", "pull requests that blocked rows name" → "that the pane shows", "listed but not placed"), register.tsx (second-listing comment names another start's hook); the `/clear`-only scope kept on purpose (only a clear test); 3 unchanged comments the second listing made stale (the classic hook header, the render comment, the `owed` declaration) updated; the re-read found all true, its one optional note (the `owed` comment omits two starts at once) not taken. Verify green after the fixes.


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

Review head 1ff4cdee; branch contains origin/main (0/0 ahead-behind on main). PR #267 opened at review start (Copilot arm), Copilot requested.

- AC1 evidence (2026-10-15): `claude plugin test .` on 1ff4cdee passes both "M256 AC1" cases in `hooks/status/pane.test.tsx` (blocked-active, blocked-prs). Each holds the hook's first `ui.panes` answer through `Copy.panesHold` in `seat()`, computed with the pane unplaced; asserts the hold was reached; places and draws during the hold and sees no read; releases and sees each blocked URL read once (sorted equality), with no second draw. Discrimination: a scratch copy with the second listing disabled fails both cases at that final assertion (reads `[]`).
- AC2 evidence (2026-10-15): the "M256 AC2" case passes on 1ff4cdee: a clear start leaves the unplaced pane owed (no read), `session.end` (`CLEAR_END`), the pane is placed and drawn, and no read runs. The same scratch copy, with `owed = false` removed from the `session.end` handler, fails it at the last assertion, reading `[URL_1250]`; only the three M256 cases failed there (1734 pass, 3 fail).
- AC3 evidence (2026-10-15): `grep -c "\.isShown" hooks/status/register.tsx` returns 1 (the body of `placedAndShown`, line 777); its callers are the `command.run` close branch (305), `isShown` (771), and `markReopen` (1278), and no other line tests `isShown`.
- AC4 evidence (2026-10-15): on 1ff4cdee from the repo root, `scripts/tests` 408 tests OK (21 skipped), `hooks/tests` 175 OK, `claude plugin validate` exit 0 on `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, `claude plugin test .` 1737 pass, 0 fail (2.1.299 binary).
- Consistency gate (2026-10-15): `cairn_validate.py` exit 0, all checks passed; `cairn_impact` skipped (Principles touched —). Profile gate: verify green on the review head (AC4 line); the marketplace validate output has no `plugins[N].version` warning; CHANGELOG.md's Unreleased Fixes carries the entry for the user-visible change, with no milestone number.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: no test covers the second listing's `&& owed` check; dropping it gives two reads when a draw or open lands while the second listing waits — fix now, fixed 12f1cbf9 (a case holding both listings; with `&& owed` removed it alone fails, reading URL_1250 twice).
- diff-bug #2: the AC1 test checks only that the hold was reached, not that the held answer was "not placed", so a harness that built its answer after the hold would pass it with the fix removed — fix now, fixed 12f1cbf9 (`Copy.panesHeld` keeps the held answer; the case asserts it is not placed).
- diff-bug #3: "Pane edges (M238 review)" still lists three gaps this branch closes — reject (planned change: records-hygiene §1 narrows the row at step 9's hygiene, where the resume wording is also corrected).
- diff-bug #4: a "placed" answer built before a `/cairn-pane` close lets the second listing read for a closed pane (wasted `gh` calls) — follow-up, new row "Late placement edges (M256 review)".
- diff-bug #5: a second listing begun before a session end can take the next start's read, from the older `$` — follow-up, same new row (rests on the end-before-start assumption in Out).
- diff-bug #6: one more `ui.panes` call per clear or resume start that finds the pane unplaced — reject (planned change: the plan chose the second listing).
- diff-bug #7: the CHANGELOG entry names `/clear` only, and breaks a line early — reject (planned scope: the claim stays within the clear-only test; the wrap is style).
- blame-history #1: DESIGN.md (~381) and README.md (~387) still say an unplaced pane's first draw starts the read, with no second listing — fix now, fixed 12f1cbf9.
- blame-history #2: the ROADMAP row is not narrowed — reject (planned change, as diff-bug #3).
- blame-history #3: the second listing re-checks `owed` and not `startRead`, an implicit coupling — reject (false as a defect: every `startRead = true` write clears `owed` with it, at register.tsx 271, 283, 329, 1315, so `owed` true implies `startRead` false and the extra check is unreachable).
- blame-history #4: the cross-start read from an older `$` — follow-up, as diff-bug #5.
- blame-history #5: the resume path runs the new code with no test — reject (planned change: Out keeps the resume race; the row narrowing says the code now covers it untested).
- blame-history #6: no test covers the second listing answering not placed or throwing — follow-up, new row.
- blame-history #7: the hold catches whichever `ui.panes` call comes first, so an earlier call in the clear path would hold the wrong listing — follow-up, new row.
- blame-history #8: the AC2 test pins an M238-era gap rather than M256 behavior — reject (planned change: Scope In names it).
- blame-history #9: CHANGELOG wording and wrap — reject (as diff-bug #7).
- blame-history #10: `placedAndShown`'s long signature line — reject (style).
- prior-review #1: the `&& owed` guard has no failing test — fix now (as diff-bug #1), fixed 12f1cbf9.
- prior-review #2: the new no-read assertions trust `settled()`'s 20 ms — reject (planned change: Out keeps the 20 ms window in the row).
- prior-review #3: DESIGN.md is stale and the ROADMAP row is unnarrowed — fix now for DESIGN (as blame-history #1), fixed 12f1cbf9; the row at hygiene (as diff-bug #3).
- prior-review #4: CHANGELOG's earlier Unreleased bullet ("The cairn pane fills again after `/resume`…") says an unshown pane reads at its first draw, unless an open read first, which omits the second listing — fix now, fixed 12f1cbf9.
- copilot: cairn/milestones/M256-pane-late-placement.md:14 — fix now (the Branch/PR header lacked the PR URL; already added at review start), fixed 1ff4cdee; replied and resolved.
- copilot: review body (COMMENTED on 4c647a14) — noted; its one anchored finding is the thread above.
- Copilot level: Lite (set by GitHub's settings). Conversation read: no issue comments; no human reviews.
- prior-review #5: CHANGELOG `/clear` only and the wrap — reject (as diff-bug #7).
- prior-review #6: the AC1 test's `until` handshake — reject (false as a regression: the file's M238 and M255 held-promise tests use the same pattern).
