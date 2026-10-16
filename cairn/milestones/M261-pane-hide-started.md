<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M261: The cairn pane hides started candidate rows

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane's candidate list is what plugin users see   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m261-pane-hide-started, https://github.com/jmgirard/cairn/pull/272   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The cairn pane's Candidates list leaves out each candidate row that work has started, in place of drawing it with the started mark `◐`.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `paneLines` in `hooks/status/pane.ts` skips a row that
`startedRefs` marks (all three sources: an open PR body's
`Candidate row:` line, a listed `#<n>` token, a counted `M<NNN>` token).
The Candidates heading counts only the drawn rows and is not drawn when
none is left. Each drawn line keeps its index in `state.candidates` as its
key and its ✎ target. `STARTED_MARK` goes. README, DESIGN, the
tracking-rules "Candidate started token" paragraph, and the unreleased
CHANGELOG entries describe the hiding. A D-entry annotates D-165 and D-166.

**Out:** the readers that find started rows (`startedRows`, `takenRows`,
the PR-body lines, the row tokens) and `pressCandidate`'s stale-press
check stay as they are. The edges in the "Started mark edges (M252
review)" candidate row now hide or show a row instead of marking it; the
row stays as it is until the review hygiene reads it.

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

- [x] AC1: With no active milestone, `paneLines` draws no line for a
      candidate row that `startedRefs` marks, whichever of its three
      sources marks it: an open PR body's `Candidate row:` line, a `#<n>`
      token whose n the open hotfix list holds, or an `M<NNN>` id in
      `state.taken`. Every other candidate row draws as it does today, in
      ROADMAP order, with its priority mark and, while `acts` is true and
      its short title is not empty, its ✎ Button. Each drawn line keeps the
      key `candidate-<i>`, with i its index in `state.candidates`. A
      `pane.test.tsx` test per source places the marked row between two
      unmarked rows and asserts the drawn candidate lines by key and text.
      One of the three uses a `[high]` and a `[low]` neighbour, one of them
      with an empty short title, and runs with `acts` true and false.
- [x] AC2: The Candidates heading's count is the number of candidate lines
      `paneLines` draws, and the heading and its gap are not drawn when
      every candidate row is hidden. `pane.test.tsx` tests assert both.
- [x] AC3: A drawn candidate line's ✎ `target` stays the row's index in
      `state.candidates`, so a ✎ press on a line drawn after a hidden row
      plans that line's own short title. A `pane.test.tsx` test presses ✎
      on such a line through the mod test kit and asserts the held
      command's args.
- [x] AC4: `STARTED_MARK` and the started mark are gone:
      `grep -rn "◐\|STARTED_MARK\|started mark" hooks README.md cairn/DESIGN.md skills types CHANGELOG.md`
      from the repo root prints no line but the M252 entry in the
      `hooks/status/` provenance list of `cairn/DESIGN.md`, which gains
      "a started row hidden in M261". README.md, cairn/DESIGN.md, the
      tracking-rules "Candidate started token" paragraph, and
      CHANGELOG.md's `## Unreleased` entries say that the pane hides a
      started row.
- [x] AC5: The repo's `verify` slot (`cairn/PROFILE.md`) passes on the
      milestone branch.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T2, T3
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Tests first in `hooks/status/pane.test.tsx`: the AC1 per-source
      tests, the AC2 count and no-heading tests, and the AC3 press test
      (the kit's ✎ presses near lines 1559-1654 are the model). Rewrite the
      tests that assert `◐` (near lines 472, 4142, 4148, 4185, and the
      `MARKED` kit test near 4296) to assert the row is not drawn. See them
      fail.
- [x] T2: `hooks/status/pane.ts` (lines 559-592): skip a marked row, keep
      `i` as key and target, count the drawn rows, draw no heading when
      none is drawn. Remove `STARTED_MARK` and its tail ref, and fix the
      comments near lines 307-317 and 559-567 and `pressCandidate`'s in
      `register.tsx` near line 1228.
- [x] T3: Docs: README.md (near lines 440-475), cairn/DESIGN.md (near lines
      79, 313-320, and 737), tracking-rules "Candidate started token",
      `types/index.d.ts` comments, and the CHANGELOG `## Unreleased`
      entries near lines 184-202, rewritten in place since they have not
      shipped. Append a D-entry that annotates D-165 and D-166: the pane
      hides a row that a body line or a counted token marks, in place of
      the mark.
- [x] T4: Run the `verify` slot and the AC4 grep.

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

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: milestone — a change to how the pane draws candidate rows, not a bug fix.
- 2026-10-16: collision sweep: M252 and M258 shipped the `◐` mark this reverses (archived, `done`); D-165 and D-166 describe the mark and get an annotating D-entry (T3); no candidate row asks for this; GitHub inboxes hold 0 open issues and 0 open PRs.
- 2026-10-16: question set: how to treat started rows — hide them; heading count — rows shown; live look before merge — no live look.
- 2026-10-16: plan gate chose hiding over a gray "N started" line and over moving the rows to the bottom, at the user's choice; falsified by the operator missing a started row's work because no other pane section shows it.
- 2026-10-16: plan chose keeping `startedRefs` and the readers over removing the started tokens and body lines, because hiding still needs them; falsified by a hiding rule that reads no started source.
- 2026-10-16: criteria audit (full, fresh Opus reader): 4 findings, all fixed — AC4's grep now spares the DESIGN.md provenance entry (IP4); T3 adds the D-entry annotating D-165 and D-166; AC1 pins keys to the state index; AC1 adds a high/low/empty-title neighbour case with `acts` both ways; the M source is named as `state.taken`.
- 2026-10-16: lessons harvest: the M56 line (run each gating suite from the repo root and check each exit code) shapes T4; the M193 line (no tool type-checks `types/index.d.ts`) applies if T3 touches more than its comments.
- 2026-10-16: implement started on m261-pane-hide-started; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-16: T1 done: new and rewritten pane tests (16) failed first against the old drawing, e.g. keys `candidate-0..2` drawn where `candidate-0, candidate-2` was expected and a count of 8 for 3.
- 2026-10-16: T2 done: `paneLines` filters the started rows before the heading, keeps `i` as key and target, and `STARTED_MARK` is removed; mod tests 1777 pass, 0 fail.
- 2026-10-16: T3 done: README, DESIGN (lines 79, 313-322, 472, 737), tracking-rules "Candidate started token", hotfix and milestone-review SKILL.md pane sentences, CHANGELOG Unreleased entries rewritten in place; D-167 annotates D-165 and D-166; `types/index.d.ts` comments describe data only and needed no change.
- 2026-10-16: the simple-english plugin's PostToolUse lint hook reported whole-file counts (hundreds of hits) on each edited doc; the hits are in text this milestone did not write, so no rewrite was made.
- 2026-10-16: T4 done: scripts 408 tests OK (21 skipped), hooks 175 OK, both `claude plugin validate` exit 0, mod tests 1777 pass 0 fail, each exit code 0; the AC4 grep prints only DESIGN.md:79's provenance entry; cairn_validate all checks passed.
- 2026-10-16: claim audit: 52 claims read, 1 corrected — README.md (the after-merge sentence now also names a counted started token; re-read true by the same reader).
- 2026-10-16: implement complete; status set to review.

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

Pass 1 (2026-10-16), on m261-pane-hide-started at `fcff1e41`, main level with origin/main, PR #272 opened at review start (Copilot arm).

- AC1 evidence: `claude plugin test .` exit 0, 1777 pass 0 fail. Per source, each passing: body line — "matched rows draw no line, and the others draw as before under their own keys" (acts true and false; drawn keys `candidate-3, -6, -7`, each equal to the no-items line) and "a hidden row between a high and an untitled low row leaves both as before" (acts true and false; keys `candidate-0, -2`, marks ↑ and ↓, ✎ only on the titled row with acts); `#<n>` — "a #n token hides its row only while the open hotfix list holds n" (rows 2 and 4 drawn either side of hidden row 3); `M<NNN>` in `state.taken` — "a hidden row between two plain rows leaves them drawn in order" (rows 3 and 5 drawn either side of hidden row 4), plus the mixed-source and done/dropped/absent tests.
- AC2 evidence: same run; "the heading counts the drawn rows only" passes (count span `3` with 3 rows drawn, `8` in the no-items control) and "with every row hidden there is no heading and no gap" passes (no `candidate*` key; the one-row-left control draws `candidates-head-gap`, `candidates-head`).
- AC3 evidence: same run; "the hidden row draws no line or ✎, and the next row plans its title" passes: with ` — started M031` (M031 `planned`) on row 0, the first drawn key is `candidate-1`, `candidate-0` is absent, and a kit press of `cairn-pane-plan-1` gives `/clear` then the plan command with args `Normal row`.
- AC4 evidence: the AC4 grep from the repo root prints one line, `cairn/DESIGN.md:79`, the provenance entry, which holds "a started row hidden in M261". Hiding is described at README.md:452-455 and 483, cairn/DESIGN.md:315-321, tracking-rules.md:218, and CHANGELOG.md:176, 180, 194, all three CHANGELOG lines inside `## Unreleased` (lines 3-460).
- AC5 evidence: verify slot from the repo root, each exit 0: scripts/tests 408 OK (21 skipped), hooks/tests 175 OK, `claude plugin validate` plugin.json and marketplace.json, `claude plugin test .` 1777 pass 0 fail.
- Consistency gate: `cairn_validate.py` exit 0, all checks passed; no DESIGN principle text changed, so `cairn_impact` skipped; verify green on the review head (above); marketplace validate shows no `plugins[N].version` warning; CHANGELOG `## Unreleased` carries the change, with no milestone number in its added lines.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the kit test "a read hides the line" lost its positive control and would pass on an empty drawing — fix now (asserts `blocked-M101` drawn)
- diff-bug #2: D-167 says an open milestone PR's row shows in no other section, but the milestone reads `planned` on the default branch and shows in Workable or Waiting — fix now (sentence corrected)
- diff-bug #3: hotfix SKILL.md lines 266 and 310 dropped the no-active-milestone condition that milestone-review's sentence keeps — fix now
- diff-bug #4: the test comment before `bodied` still said a body line "draws as started" — fix now
- diff-bug #5: `MARKED = undefined` names a mark that no longer exists — fix now (renamed `HIDDEN`)
- diff-bug #6: the all-hidden test's control relied on unstated alignment between `all` and `one` — fix now (`all` built from `one`, alignment asserted)
- diff-bug #7: README "the effect of that milestone's PR shows" is vague — fix now (names the hidden row)
- blame-history #1: the "Started mark edges (M252 review)" ROADMAP row still describes `◐` — fix now (row reworded, title kept)
- blame-history #2: D-167's milestone-PR sentence — same as diff-bug #2, fix now
- blame-history #3: the stale-press branch of `pressCandidate` stays untested — follow-up, already recorded in "Plan Button edges (M242 review)"; no new row
- blame-history #4: `startedRefs` runs per row as before, no behavior change — reject (false: no defect)
- blame-history #5: DESIGN.md:79 still names the `◐` mark of M252 — reject (planned change: the provenance entry is history, AC4 keeps it)
- blame-history #6: one long README line — reject (style)
- blame-history #7: CHANGELOG entries rewritten in place rather than a new entry — reject (planned change: the entries never shipped, T3)
- prior-review #1: the "Started mark edges" row is stale — same as blame-history #1, fix now
- prior-review #2: the row's edges now hide or show a row silently — fix now through the same row rewording
- prior-review #3: same-title rows hide together — fix now through the same row rewording ("same-title rows hide together")
- prior-review #4: stale-press branch untested — same as blame-history #3, follow-up in "Plan Button edges (M242 review)"
- prior-review #5: the no-heading test was hard to follow — same as diff-bug #6, fix now
- prior-review #6: a guest-mode row has no on-screen cue while hidden before hygiene — reject (planned change: hiding with no trace was the user's choice at the question set)
