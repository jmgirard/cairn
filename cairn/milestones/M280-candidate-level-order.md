# M280: The pane shows candidates by priority, and validate warns on file order

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters see the pane's Candidates list and `cairn_validate` output   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m280-candidate-level-order   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The cairn pane lists candidate rows high → normal → low whatever their file order, and `cairn_validate` warns on a Candidates section whose file order breaks that rule.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `paneLines` in `hooks/status/pane.ts` sorts the drawn candidate rows by level, stable within a level, keeping each row's ROADMAP index as its key and ✎ target. A new `candidate order` advisory in `scripts/cairn_validate.py`, one WARN line per out-of-order row. Pane and validate tests, a fixture with rows out of order, the DESIGN.md and README pane text, a CHANGELOG entry, and a D-entry annotating D-134.

**Out:** reordering ackwards' ROADMAP (an edit in that repo, which the new WARN will name; question set). The reader's ROADMAP-order `candidates` state, each fixture's `expected.json` order, `cairn_next.high_title`, and `nextTitle` stay as they are: each picks the first `[high]` row in file order, which a stable sort also draws first. A FAIL check on order, and a check on the token's spelling (D-134's rejection stands). The rulebook's "Candidate priority token" text, which already states the order. A `/cairn-triage` reorder disposition (no request).

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

- [ ] AC1: While no milestone is active, the cairn pane draws its candidate lines in level order: every `high` line before every `normal` line, every `normal` line before every `low` line, and lines of one level in ROADMAP order. A pane test over a fixture whose ROADMAP holds a `[high]` row below a `[low]` row, an untagged row below a `[low]` row, and two rows of one level with a row of another level between them asserts the full drawn title order, written out by hand; the per-fixture test in `hooks/status/pane.test.tsx` asserts that order for every fixture with drawn candidate lines.
- [ ] AC2: A candidate line drawn away from its ROADMAP position keeps its row's index in the ROADMAP-order `candidates` state as its key and ✎ target, so its ✎ press plans that row: a pane test presses ✎ on such a line and asserts that the held command carries that row's short title.
- [ ] AC3: `scripts/cairn_validate.py` reports a new advisory, `candidate order`, that WARNs once for each candidate row (as `cairn_next.candidate_texts` reads the rows) whose level ranks above the level of an earlier row, naming the row's short title and its level, and prints `OK` when no row does; the advisory leaves the exit code unchanged. Tests in `scripts/tests` assert OK on an in-order ROADMAP; a WARN naming exactly the out-of-order rows on a ROADMAP holding a `normal` row after a `low` row, a `high` row after a `normal` row, and a row out of order only against a non-adjacent earlier row (`low`, `normal`, `normal`, where both `normal` rows WARN); and the same exit code with and without those rows.
- [ ] AC4: `cairn/DESIGN.md`'s pane paragraph and the README's cairn pane section say the pane draws candidate rows in level order, and the CHANGELOG's Unreleased section carries one entry naming the pane order and the `candidate order` WARN.
- [ ] AC5: The `claude-plugin` profile's `verify` slot is clean: both gating `python3 -m unittest` suites (`scripts/tests`, `hooks/tests`), `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T1, T2, T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Pane order. In `paneLines` (`hooks/status/pane.ts:595`), sort the filtered `{ row, i }` list stably by level (high, normal, low) before drawing, and update the comment above it. Add or extend a fixture so its ROADMAP holds the AC1 shapes (regenerate `fixtures.gen.ts` with `gen_fixtures.py` and its `expected.json`, which stays in ROADMAP order). In `pane.test.tsx`, write the new fixture's drawn order by hand, reorder `CANDIDATE_LINES` to the sorted order, sort `drawnCandidates` by level, and add the AC2 ✎ press test. Show the new tests red against the unsorted code first. Run `claude plugin test`.
- [x] T2: Validate advisory. Add `check_candidate_order(root)` to `scripts/cairn_validate.py`, reading rows with `cairn_next.candidate_texts` and short titles with `cairn_next.short_title`, and register it in `ADVISORIES` as `candidate order`. One finding per row whose level ranks above the lowest level read before it. Add the AC3 tests to `scripts/tests`, each WARN asserted by title and level, and plant an adjacent-only comparison to see the non-adjacent case red. Confirm this repo's validate prints `OK    candidate order`.
- [x] T3: Docs and records. Add the level-order sentence to `cairn/DESIGN.md`'s pane paragraph (~line 305) and to the README's pane Candidates text, an Unreleased CHANGELOG entry for both changes, and D-182 in `cairn/DECISIONS.md`: `cairn_validate` WARNs on Candidates file order, annotating D-134, whose rejected token check this is not. Run the full `verify` slot.

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

- 2026-10-18: created by /milestone-plan, from the user's report that the ackwards pane shows a `[high]` row below ten `[low]` rows (the pane draws file order; ackwards' file is out of order).
- 2026-10-18: tier check: milestone — changes the pane's drawing and adds a validate advisory, a change to running code that is not a bug fix.
- 2026-10-18: collision sweep: D-134 rejected "a `cairn_validate` check on the token"; an order advisory reads the token but does not check its spelling, so D-182 annotates D-134 rather than superseding it. D-035 (flat list) stands. Archive M179 (token) and M207 (pane candidates) shipped what this extends. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-18: checker-regress shape not hit: `cairn_validate` checks adopters' tracking files, a shipped user-facing tool, and the advisory adds a new promise rather than hardening a shipped one. The "Plan-gate clauses for standing instruments" row's clause (a) binds an instrument before it gates; this advisory never gates, so the row stays.
- 2026-10-18: criteria audit (full mode, fresh Opus reader): 3 findings, all fixed. (1) D-134 needs a record: the D-182 annotation went to T3, not an AC, since a D-entry is a recording act. (2) AC3's probe planted only adjacent inversions: added the `low, normal, normal` case. (3) AC1's fixture did not test stability, and `drawnCandidates` would mirror the code: added two same-level rows split by another level, with the order written by hand.
- 2026-10-18: question set: WARN shape — one line per out-of-order row. Live look in ackwards — no, the pane tests suffice. Reorder ackwards' ROADMAP — no, leave it to that repo.
- 2026-10-18: split tripwire weighed: the goal joins two parts with "and", but both enforce one rule (high → normal → low) at its two readers, in 5 criteria and 3 tasks; kept as one milestone.
- 2026-10-18: plan gate chose sorting in `paneLines` over sorting in the reader (`candidateRows`) because the reader's file-order state feeds `pressCandidate`'s index lookup, the fixtures' `expected.json`, and the Python mirror; falsified by a second pane surface (the band, a press) needing the sorted order from state.
- 2026-10-18: started on branch m280-candidate-level-order; untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-18: T1 done: `paneLines` sorts drawn rows by `LEVEL_RANK`, then ROADMAP index; new fixture `candidates-order` (6 rows); the M280 order tests were red before the sort (19 fails), all 2132 pane tests green after. Tests that read draw position as ROADMAP index (M207, M242, M261) now match by key, and `candidates-order` joined the band's empty-fixture and Plan-title lists by hand.
- 2026-10-18: T2 done: `check_candidate_order` in `cairn_validate.py` imports `cairn_next` for `candidate_texts` and `short_title` (added to `TestStdlibOnly.ALLOWED`, an in-repo module) rather than copying a third reader; 5 new tests red before, green after; a planted adjacent-only comparison turned the non-adjacent test red for the missing second row. This repo prints `OK    candidate order`; ackwards (after its M099 merge removed its `[high]` row) prints 4 WARNs, its untagged rows below `[low]` rows.
- 2026-10-18: T3 done: DESIGN.md pane paragraph, README pane section, a CHANGELOG entry under "Changes that affect existing repos", and D-182 annotating D-134. Validate green; both gating suites and both manifest validates green; hand-run `skills/tests` 886 green. The simple-english hook flags 368 and 219 file-wide hits in CHANGELOG.md and README.md that predate this branch; the two long sentences this branch added were split, the rest left as out of scope.
- 2026-10-18: claim audit: 29 claims read, 2 corrected — CHANGELOG.md, README.md (both said one WARN line per row; validate prints one `WARN  candidate order (N)` header with one line per row under it; the same reader re-read both, 0 wrong).
- 2026-10-18: verify clean at 9bb2924b: scripts/tests 423 OK, hooks/tests 179 OK, both manifest validates exit 0, `claude plugin test` 2132 pass 0 fail; status → review.

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
