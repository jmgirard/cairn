# M246: The pane shows a blocked row whose milestone file was archived before its row was updated

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, GP2
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane, the `cairn_next.py` output, and `/milestone-review` are what plugin users see and run
- **Branch/PR:** m246-pane-archived-blocked-row, https://github.com/jmgirard/cairn/pull/256

## Goal

The cairn pane shows a `blocked` row as archived when its milestone file moved to the archive before the row changed, with its PR's state word and, for a merged PR, a Finish button that completes the row.

## Scope

**In:**
- `blocked` in `scripts/cairn_next.py` and its mirror in `hooks/status/reader.ts`: an archive fallback for a row with no live file.
- The `archived` mark on the pane's blocked line and in the `cairn_next.py` output.
- A `/milestone-review` resume arm that finishes the row update for such a row.
- DESIGN.md, README.md, and CHANGELOG.md.

**Out:**
- The Refresh button writing ROADMAP rows: not planned. The user chose this fallback over it on 2026-10-12. The pane stays a reader.
- An `in-progress` or `review` row with a missing file: unchanged, as the `missing-file` fixture holds.
- A `dropped` archive under a `blocked` row: unchanged. `cairn_validate`'s missing-file check reports the row.
- Issue writes owed by an archived row: the arm names them in its recap and does not post them.
- The performance repo's M001 row: fixed with the Finish button once this ships, or by hand.

## Acceptance criteria

- [x] AC1: For a `blocked` row whose ROADMAP path is not a regular file, `blocked` in `scripts/cairn_next.py` looks for files under `cairn/milestones/archive/` whose `canon_id` equals the row's `canon_id`.
      The row gets `archived: True` when exactly one such file exists, its read succeeds, and its `**Status:**` paragraph starts with `done`.
      The `**Status:**` paragraph is the first line that starts with `**Status:**`, through the line before the next blank line or the end of the file.
      For an archived row, `pr` and `url` come from the first `PR_URL` match in that paragraph.
      If the paragraph has no match, both are `None`.
      Every other `blocked` row gets `archived: False`, with `pr` and `url` as `blocked` gives them today.
      Unit tests in `scripts/tests` cover nine cases:
      1. a live file,
      2. the URL on the `**Status:**` line,
      3. the URL on the paragraph's second line,
      4. a URL only in a later paragraph,
      5. a row `M057` with an archive file `M57-x.md`,
      6. a `dropped` archive,
      7. two archive files with one canonical id,
      8. an archive file whose read fails,
      9. no live file and no archive file.
- [x] AC2: The `blocked` list that `hooks/status/reader.ts` computes equals `cairn_next.blocked` for each fixture under `hooks/status/fixtures/`, as `scripts/tests/test_status_fixtures.py` and `hooks/status/reader.test.ts` check.
      A new fixture holds the AC1 cases.
- [x] AC3: In the cairn pane, the tail of an archived blocked line reads `#<n>`, then `archived`, then the PR state word when one was read.
      With no PR number, the tail starts with `archived`.
      A blocked line for a row that is not archived carries no `archived`.
      Tests in `hooks/status/pane.test.tsx` assert these three forms.
      They also assert that an archived row whose PR reads `merged` carries the `merged` word and the `finish` Button, with the row's id as its target.
- [x] AC4: The "Externally blocked" line that `scripts/cairn_next.py` prints for an archived row ends with ` (PR #<n>, archived)`.
      If the row has no PR number, the line ends with ` (archived)`.
      The line for a row that is not archived is unchanged.
      A test in `scripts/tests` asserts the three printed forms.
- [x] AC5: At Session start, `skills/milestone-review/SKILL.md` accepts, in guest mode only, a target whose ROADMAP row is `blocked`, whose ROADMAP path is not a regular file, and for which exactly one file under `cairn/milestones/archive/` has the row's canonical id and a `**Status:**` paragraph (AC1's definition) that starts with `done`.
      Session start's status rule names this exception.
      For such an archive in owner mode, or under a row that is not `blocked`, Session start says in chat that the archive exists and the row was not updated, and stops.
      In the accepted case, the arm says the same in chat.
      It reads the archive file in place of the milestone file, reads no `Branch/PR` header and no PR state, and takes the archive's `done` Status as the record of the merge.
      It skips steps 1 to 8.
      Of step 9 it runs only these parts: the default branch's fetch, checkout, and fast-forward (step 9's guest arm), the ROADMAP row update to `done` with the archive path, the hygiene stamp, the cap and budget checks, the hand-run prose guards where the repo ships them, and `cairn_validate.py`.
      A cap breach or a `cairn_validate.py` FAIL is named in the recap, with no prune, and step 10 still runs.
      It writes nothing to the archive file, captures or retires no lesson, and archives no RB/RR pair, and its recap names these as skipped.
      It skips the issue writes.
      Its recap names each `partial` entry of the archive's `resolves` clause as an owed comment, and each `closes` entry as left to the maintainers' merge.
      Then it runs step 10.
- [x] AC6: `cairn/DESIGN.md`'s paragraph on the pane's `blocked` rows, `README.md`'s description of the pane's blocked section, and a `CHANGELOG.md` entry each state the archive fallback and the `archived` mark.
- [x] AC7: The profile's `verify` slot is green: its five commands each exit 0 from the repo root.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T1, T4
- AC4 → T1, T2
- AC5 → T5, T8
- AC6 → T6
- AC7 → T7

## Tasks

- [x] T1: Write the tests first: the AC1 and AC4 cases in `scripts/tests`, the new fixture with its `expected.json` (the read-fail case through its `unreadable` key), and the reader and pane mod tests.
      Add `archived: false` to the `blocked` entries of the existing fixtures (`blocked-prs`, `blocked-active`, and any other with a `blocked` key).
      The new tests fail before T2 to T4.
- [x] T2: `scripts/cairn_next.py`: the archive fallback in `blocked`, a Status-paragraph URL reader beside `_pr_match`, the `archived` key, and the printed suffix.
- [x] T3: `hooks/status/reader.ts`: the same fallback, with archive paths and not only ids, and `BlockedRow.archived`.
      Give the pane atom a new shape tag in `register.tsx` (LESSONS, M193).
      Regenerate `fixtures.gen.ts` with `hooks/status/gen_fixtures.py`.
- [x] T4: `hooks/status/pane.ts`: the `archived` word in the blocked line's tail.
- [x] T5: `skills/milestone-review/SKILL.md`: the Session start acceptance and the resume arm.
      Add a prose guard in `skills/tests` (hand-run) that fails when the arm's trigger or its step-9 entry point is removed.
- [x] T6: `cairn/DESIGN.md`, `README.md`, and `CHANGELOG.md`.
- [x] T7: Run the `verify` slot and the hand-run `skills/tests` suite.
- [x] T8: Rewrite the archived-file arm in `skills/milestone-review/SKILL.md` to the amended AC5, and the status rule's exception.
      Rewrite `TestReviewArchivedFileArm` and its harness entries to pin the guest-mode limit, the `blocked` limit, the owner-mode stop, the step-9 parts, and the no-write clause.
      Add a D-entry annotating D-130, and say "guest mode" in the README, CHANGELOG, and DESIGN.md lines on Finish.

## Work log

- 2026-10-12: created by /milestone-plan. Seen in the performance repo: M001's row says `blocked` and points to a missing live file, the archive says done with PR #956, and the pane showed no state word or Button for it.
- 2026-10-12: collision sweep: no candidate row overlaps. M223 and M224 (archived) shipped the blocked list and its PR read, and this extends them. D-130 was read whole: the new arm narrows its issue-write rule by skipping the writes.
- 2026-10-12: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-12: lessons harvested: a new pane shape tag when the atom's layout changes (M193), the prose-guard locator rules (M148), and run each gating suite with its exit code checked (M56).
- 2026-10-12: criteria audit (full mode, fresh Opus reader) returned 10 findings, and all were fixed. AC5 now names Session start and reads no header or PR state. The arm skips the issue writes, whose approval line left with the live file.
- 2026-10-12: criteria audit fixes, continued: the fallback needs a `done` archive, ids match by `canon_id`, one archive file only, and a failed read gives no fallback. AC2 drops its harness promise, AC3 states the tail order and narrows the Button claim to `merged`, and the goal names when Finish shows.
- 2026-10-12: question set: what Finish does for an archived row. Answer: it runs `/milestone-review`, which gains an arm that completes the row update.
- 2026-10-12: question set: live look in the performance repo at review. Answer: no, tests only.
- 2026-10-12: plan gate chose the review arm behind Finish over an `archived` mark with a Check button and no skill change, because the user chose it. Falsified by a half-done hygiene state that the arm's step-9 entry point cannot finish.
- 2026-10-12: plan gate chose to read the PR from the archive's Status paragraph over adding a `Branch/PR` line to the archive template, because every existing archive has only the Status line. Falsified by archives that put the PR outside the Status paragraph.
- 2026-10-12: the user chose this fallback over a Refresh button that writes ROADMAP rows, in chat before the plan.
- 2026-10-12: implement started. Branch `m246-pane-archived-blocked-row` cut from main at 48469bd. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-12: T1 done. New fixture `blocked-archived` holds the nine AC1 cases, and the four existing fixtures with blocked rows gained `archived: false`. Its files were written with shell heredocs, not the Write tool. The Python tests failed before T2 on the missing key and suffix. The mod tests were not run before T3 and T4.
- 2026-10-12: choice: `archived_text` globs the archive directory itself, because `archive_files` keys by raw id and keeps one path per id, so it cannot see two files with one canonical id.
- 2026-10-12: T2 to T4 done. `test_status_fixtures.py` states the nine cases apart from the helper. `band.test.tsx`'s list of empty fixtures gained `blocked-archived`. The pane shape tag is `pane-5`.
- 2026-10-12: T5 done. The arm sits in Session start before Resume routing, keeps step 9's default-branch sync, and skips the issue writes. Guard `TestReviewArchivedFileArm` and two harness entries; `skills/tests` 728 tests OK.
- 2026-10-12: T6 and T7 done. Verify: scripts 407 OK, hooks 174 OK, both validates exit 0, mod tests 1703 pass. `cairn_validate` passes.
- 2026-10-12: claim audit: 77 claims read, 6 corrected — hooks/status/reader.ts, scripts/cairn_next.py, skills/milestone-review/SKILL.md, skills/tests/test_resume_routing.py, skills/tests/test_mutation_harness.py, scripts/tests/test_status_fixtures.py, README.md
- 2026-10-12: claim audit fixes: the BlockedRow comment and `blocked` docstring state the null cases, the arm names step 9's checkout and pull, and README says `archived` shows alone with no URL. The same reader re-read the 6 and found 0 wrong. The reader also noted a root path holding a glob character such as `[` empties Python's `glob` but not the TS `list`, which `archive_files` and `archivedIds` share since before this branch.
- 2026-10-12: all tasks checked. Verify green again after the fixes: scripts 407 OK, hooks OK, both validates exit 0, mod tests 1703 pass, `skills/tests` OK. Status set to review.
- 2026-10-12: review: AC1 to AC7 verified and ticked at 34be02d5. PR #256 opened at review start for the Copilot round. Three reviewers gave 31 findings: 11 fixed in 1b3ae96b, 5 to the AC5 amendment, 1 row "Archived blocked rows (M246 review)", 6 rejected, the rest noted or duplicates.
- 2026-10-12: amendment routed: AC5 — the arm accepts a finished milestone whatever its row status and makes a `blocked → done` move in owner mode that the rulebook does not admit (diff-bug #1, #2, blame-history #2); the criterion narrows to guest-mode `blocked` rows and names the step-9 parts the arm runs
- 2026-10-12: re-audit: AC5 (full) — 4 findings on the first narrowed wording: in guest mode `closes` entries are the maintainers' merge, not owed; the prose guards and lesson pruning are conditional in step 9; the trigger did not use AC1's terms and dropped the chat line (IP2); the guard did not pin the new limits. All four fixed in the second wording.
- 2026-10-12: re-audit: AC5 (full) — 4 findings on the second wording: the fast-forward needs step 9's checkout; a `cairn_validate.py` FAIL has no rule when pruning is barred; owner mode and non-`blocked` rows have no exit; RB/RR archiving is dropped unsaid. It also advised a D-entry annotating D-130. This is the second re-audit line, so the third wording goes to the user.
- 2026-10-12: question set: accept the third AC5 wording (repeated review-failure stop). Answer: accept the wording, with Finish still shown in owner mode, where it reports and stops.
- 2026-10-12: amendment return: AC5 — "accepts, in guest mode only, a target whose ROADMAP row is `blocked`, whose ROADMAP path is not a regular file, and for which exactly one file under `cairn/milestones/archive/` has the row's canonical id and a `**Status:**` paragraph (AC1's definition) that starts with `done`. Session start's status rule names this exception. For such an archive in owner mode, or under a row that is not `blocked`, Session start says in chat that the archive exists and the row was not updated, and stops. In the accepted case, the arm says the same in chat. It reads the archive file in place of the milestone file, reads no `Branch/PR` header and no PR state, and takes the archive's `done` Status as the record of the merge. It skips steps 1 to 8. Of step 9 it runs only these parts: the default branch's fetch, checkout, and fast-forward (step 9's guest arm), the ROADMAP row update to `done` with the archive path, the hygiene stamp, the cap and budget checks, the hand-run prose guards where the repo ships them, and `cairn_validate.py`. A cap breach or a `cairn_validate.py` FAIL is named in the recap, with no prune, and step 10 still runs. It writes nothing to the archive file, captures or retires no lesson, and archives no RB/RR pair, and its recap names these as skipped. It skips the issue writes. Its recap names each `partial` entry of the archive's `resolves` clause as an owed comment, and each `closes` entry as left to the maintainers' merge. Then it runs step 10."
- 2026-10-12: the amendment narrows what the arm accepts and the step-9 parts it runs. It adds the status-rule exception, the owner-mode stop, the chat line, the archive read, the no-write clause, and the split `partial` and `closes` recap. T8 added (minor amendment), and AC5's tick removed until fresh evidence.
- 2026-10-12: T8 done. The arm is rewritten to the amended AC5, the status rule names it, D-159 annotates D-130, and README, CHANGELOG, and DESIGN.md say guest mode. `TestReviewArchivedFileArm` now has 5 tests with 5 harness entries.
- 2026-10-12: claim audit: 41 claims read, 4 corrected — skills/milestone-review/SKILL.md, README.md, CHANGELOG.md, skills/tests/test_resume_routing.py
- 2026-10-12: claim audit fixes: the trigger says "first word ... is `done`" and "up to" the blank line, the `closes` sentence says the keyword closes it at the maintainers' merge, and README and CHANGELOG name only the three skipped items. The same reader re-read the 4 and found 0 wrong.
- 2026-10-12: verify green at 54ab66a8: scripts 407 OK, hooks OK, both validates exit 0, mod tests 1707 pass, `skills/tests` 731 OK. Status set to review.

## Decisions

## Review

Evidence run 2026-10-12 on branch head 34be02d5.

- AC1: `test_python_helpers_match_expected` compares `cairn_next.blocked` with the `blocked-archived` fixture's nine cases, and `test_blocked_fixtures_hold_the_row_shapes` states the nine (pr, archived) pairs apart from the helper: M201 (11, False), M202 (21, True), M203 (32, True), M204 (None, True), M057 (57, True), M206, M207, M208, M209 (None, False). Both ok. Planted in memory, an any-status `STATUS_DONE` and a never-matching `BLANK` each turned the fixture test red, and the restored control passed.
- AC2: `reader.test.ts` "blocked-archived: the pane's milestones and next step match expected.json" passed, and it compares `pane.blocked` with the fixture's `blocked` key that `test_python_helpers_match_expected` holds `cairn_next.blocked` to. The four other fixtures with blocked rows pass both sides with `archived: false`.
- AC3: `pane.test.tsx` "an archived row shows `archived`, its state word, and Finish" passed. With every PR read `MERGED` it asserts `M202  The URL on the Status line  #21  archived  merged` with Button `cairn-pane-finish-M202`, `M204  A URL only in a later paragraph  archived` with no Button, `M201  A live file  #11  merged`, and `M206  A dropped archive`. A Finish press ran `cairn:milestone-review M202`. "blocked-archived: blocked rows" passed on both surfaces.
- AC4: `test_externally_blocked_line_marks_an_archived_row` passed. It asserts `  M05 — Archived with a PR (PR #956, archived)`, `  M06 — Archived with no PR (archived)`, and `  M07 — Still live (PR #7)`. `cairn_next.py` over the fixture printed `(PR #21, archived)`, `(archived)` for M204, and `(PR #11)` for M201.
- AC5: `skills/milestone-review/SKILL.md` lines 40 to 53, read at 34be02d5. The archived-file arm sits in Session start, accepts a target whose live file is missing and whose one archive file (any zero-padding) has a Status paragraph starting with `done` whatever its ROADMAP status, reads no `Branch/PR` header and no PR state, skips steps 1 to 8 and step 9's summary write and live-file delete, runs step 9 from its ROADMAP row update onward and then step 10, and skips the issue writes, naming each `resolves` entry as owed. `TestReviewArchivedFileArm` (2 tests) passed in `skills/tests`, 728 tests OK, and the harness turns both red when their blocks are blanked.
- AC6: `cairn/DESIGN.md` line 317 opens the paragraph "Each blocked row also has `archived` (M246)" inside the pane's blocked-rows text, and line 79 lists M246. `README.md` lines 337 to 346 describe the fallback, the `archived` mark, and the printed forms. `CHANGELOG.md` line 7 opens the Unreleased entry for it.
- AC7: from the repo root at 34be02d5, each exit code checked: `scripts/tests` 407 OK (21 skipped), `hooks/tests` 174 OK, `claude plugin validate` exit 0 on `plugin.json` and on `marketplace.json`, and `claude plugin test .` 1703 pass, 0 fail.

Consistency gate, 2026-10-12:
- `cairn_validate.py`: exit 0, all checks passed.
- No DESIGN.md principle changed, so `cairn_impact.py` was not run.
- Profile gate: the verify checks pass on the review head (AC7), the marketplace validate output has no `version` warning, and `CHANGELOG.md` has the entry, with no milestone number.
- `skills/tests` (hand-run): 728 tests OK.
- Copilot round: PR #256 opened at review start, state query `none`, review requested with exit 0.

Independent review, 2026-10-12:
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the arm accepts a row already `done` or `dropped`, so a typed `/milestone-review` on any finished milestone reruns step 9 — amendment return: AC5 promises acceptance whatever the row status, so the criterion narrows to `blocked` rows
- diff-bug #2: in owner mode the arm makes a `blocked → done` or other transition the rulebook does not admit — amendment return, with #1: AC5 narrows to guest mode, where the rulebook admits `blocked → done`
- diff-bug #3: the tests pass if the archive wins over a live file — fix now, fixed 1b3ae96b (a done archive beside M201's live file)
- diff-bug #4: Session start's "Status must be `review`" and "read the target milestone file" come before the arm with no pointer to it — fix in the AC5 amendment pass
- diff-bug #5: step 9 "from its ROADMAP row update onward" includes writes to the archive summary and lesson steps that need the deleted work log — fix in the AC5 amendment pass (the arm names the step-9 parts it runs)
- diff-bug #6: Revise and Check can show on an archived row — fix now, fixed 1b3ae96b (an archived row carries only Finish, two new pane tests)
- diff-bug #7: an archived row with no PR URL gets no Button — follow-up, ROADMAP row "Archived blocked rows (M246 review)"
- diff-bug #8: `glob.glob` on an unescaped root differs from the TS `list` — fix now for the new code, fixed 1b3ae96b (`os.listdir`); the same gap in `archive_files` is older, follow-up, same row
- diff-bug #9: invalid UTF-8 in an archive file fails the Python read and not the TS one — follow-up, same row (the gap is older, on live files)
- diff-bug #10: Unicode digits in archive names count on the Python side only — reject, false as new: the reader.ts header already states this mirror gap
- diff-bug #11: `blocked` checks the real file system before the injected `read` — reject, false as a defect: the TS side also checks `isFile` apart from `read`, so the two sides agree
- diff-bug #12: `cs._ID_RE` is a private name — reject, style
- diff-bug #13: `doneish`, two Status lines, and no space before `done` are untested — fix now in part, fixed 1b3ae96b (`doneish` and a tab-only blank line); the rest follow-up, same row
- diff-bug #14, #15, #16: shape tag enough, mirror agrees on the traced inputs, tail order matches AC3 — no defect, noted
- blame-history #1: archived rows map `changes requested` and `closed` to Buttons — fix now, same as diff-bug #6, fixed 1b3ae96b
- blame-history #2: the arm departs from D-130's merge-state routing and the transition table — amendment return, with diff-bug #1 and #2; the narrowed arm runs only where the rulebook admits `blocked → done`
- blame-history #3: `types/index.d.ts` lacks `archived` — fix now, fixed 1b3ae96b
- blame-history #4: `/milestone` §2 does not route an archived blocked row — follow-up, ROADMAP row "Archived blocked rows (M246 review)"
- blame-history #5: the arm skips the companion check — fixed by the guest-mode narrowing, since guest mode has no companion arm
- blame-history #6: step 9's lesson and Known-issues steps need the deleted work log — fix in the AC5 amendment pass, same as diff-bug #5
- blame-history #7: the Status paragraph has no `companion:` exclusion — reject, planned change: AC1 names the first URL in the paragraph, and the archive template's Status line names one PR
- blame-history #8: Python reads the archive without an `isfile` check — reject, false: `read_file` checks `os.path.isfile`
- blame-history #9: README and CHANGELOG do not cover Revise or Check on archived lines, and the CHANGELOG's "accepts such a milestone" is broad — Revise and Check are gone with diff-bug #6; the wording is fixed in the AC5 amendment pass
- blame-history #10: shape-tag practice followed — no defect, noted
- prior-review #1: DESIGN.md Known issues still named `pane-3` — fix now, fixed 1b3ae96b
- prior-review #2: `types/index.d.ts` parity — fix now, same as blame-history #3
- prior-review #3: the 44-column sweep lacks `blocked-archived` — fix now, fixed 1b3ae96b
- prior-review #4: thin parity cases for the Status paragraph cut — fix now in part, same as diff-bug #13
- prior-review #5: unescaped glob, and the Status scan does not stop at a `## ` heading — the glob fixed 1b3ae96b; the heading stop is follow-up, same row

Pass 2 evidence, 2026-10-12, at 07bbee17 (after the AC5 amendment and the pass-2 fixes), each exit code checked from the repo root:
- AC1: `test_python_helpers_match_expected` and `test_blocked_fixtures_hold_the_row_shapes` ok over the fixture's eleven blocked rows. The added rows are M201 with a done archive beside its live file, giving (11, False), M210 `doneish`, giving (101, True) under AC1's literal "starts with `done`", and M211 with a tab-and-space line, giving (None, True).
- AC2: `reader.test.ts` "blocked-archived: the pane's milestones and next step match expected.json" passed in the 1707-test mod run.
- AC3: the archived-row pane test passed again. Two new tests pass, and they assert no Button on an archived row whose PR reads `changes requested` or `closed`, while the live M201 row keeps Revise or Check. The 44-column sweep passed for `blocked-archived` on both surfaces.
- AC4: `test_externally_blocked_line_marks_an_archived_row` passed. `cairn_next.py` over the fixture printed `(PR #101, archived)` for M210 and `(archived)` for M211.
- AC5: `skills/milestone-review/SKILL.md` lines 30 to 63 at 07bbee17, read against the amended AC5 clause by clause. Guest mode and a `blocked` row are required, with the path not a regular file, one archive with the canonical id, and a done Status paragraph. The status rule names the exception (line 32), and line 30 points to the archive. Owner mode and other rows report and stop. The arm has the chat line, reads the archive in place of the file, reads no header or PR state, and takes `done` as the merge record. It skips steps 1 to 8 and lists the step-9 parts it runs. A cap breach or validate FAIL is named with no prune, and the arm goes on to step 10. It writes nothing to the archive, touches no lesson or RB/RR pair, and names them skipped. It makes no issue write, and the recap splits `partial` from `closes`. Then step 10. `TestReviewArchivedFileArm` 7 tests pass, and the 7 harness entries each turn their test red. `skills/tests` 732 OK.
- AC6: README lines 337 to 350, the CHANGELOG Unreleased entry, and DESIGN.md's blocked-rows paragraph state the fallback, the `archived` mark, and the guest-mode arm.
- AC7: `scripts/tests` 407 OK (21 skipped), `hooks/tests` OK, both `claude plugin validate` exit 0 with no `version` warning, `claude plugin test .` 1707 pass and 0 fail. `cairn_validate.py` passes.

Independent review, pass 2, 2026-10-12, over `06ee90d4..HEAD`:
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the guards miss the `done` condition, the step-1-to-8 skip, the FAIL rule, and other arm clauses — fix now, fixed 07bbee17 (pins for the `done` clause, the skip and FAIL rule, and the line-30 pointer, with two harness entries); the rest of the arm's sentences stay unpinned, as a guard pins the rule's trigger and limits
- diff-bug #2: D-159's reason for not reading the PR state is false, since the archive's Status line carries the URL — fix now, fixed 07bbee17 (D-160 corrects it: step 9 writes the archive only after a merge was read)
- diff-bug #3: an owner-mode step 9 that stops leaves the same state with no route — follow-up, row "Archived blocked rows (M246 review)"
- diff-bug #4: line 30 "Read ... the target milestone file" has no pointer to the arm — fix now, fixed 07bbee17
- diff-bug #5: the arm's paragraph wording drifts from AC1 and AC5 — fix now, fixed 07bbee17 (the arm states AC1's paragraph and "starts with `done`")
- diff-bug #6: AC1's literal "starts with `done`" conflicts with the M210 `doneish` fixture — fix now, fixed 07bbee17: the word-boundary lookahead is dropped on both sides, so the code meets AC1 as written; archive statuses are `done` or `dropped`
- diff-bug #7: some skipped step-9 parts are not named in the recap — reject, planned change: AC5 names the three the recap lists
- diff-bug #8: the `os.listdir` switch has no test with `[` in the root — follow-up, same row
- diff-bug #9: the M211 case is named "tab-only" but holds a tab and a space — fix now, fixed 07bbee17 (renamed)
- diff-bug #10: D-159's Context says Session start required `review` — fix now, fixed 07bbee17 (D-160)
- blame-history #1: the arm sets `done` without reading the merge, and D-159's reason is wrong — the reason is fixed by D-160; the trust is kept, since step 9 runs only after a merge was read
- blame-history #2: tracking-rules and D-137 are not updated for the arm's `blocked → done` — reject, false: the rulebook admits `blocked → done` for a guest handoff the maintainers merged, which is the state the archive records
- blame-history #3: Finish dead-ends in owner mode — planned change (question set answer); the owner-mode route is follow-up, same row
- blame-history #4: archives with no PR URL are accepted — reject, same ground as #1 (D-160)
- blame-history #5: a press of a Button drawn before the row turned archived still routes — follow-up, same row
- blame-history #6: the `PR_BUTTON` comment is stale and `word !== 'merged'` hardcodes the word — fix now, fixed 07bbee17
- blame-history #7: step-9 parts skipped while the row is `done` — reject, planned change (AC5)
- blame-history #8: prose and regex differ on `done-x`, `done.`, and no space — fixed with diff-bug #6, since both now read "starts with `done`"
- blame-history #9: Python `archived_text` has no `isfile` check, and `archive_files` still globs — the first is false (`read_file` checks it); the second is follow-up, same row
- blame-history #10: `/milestone` and `cairn_next.py` do not route the arm — follow-up, same row
- prior-review: no prior-review evidence that pass 2 reintroduces or contradicts; its optional item is diff-bug #4

PR conversation read, 2026-10-12, PR #256: 0 unresolved threads, 0 issue comments, 1 review.
- conversation: copilot-pull-request-reviewer[bot] PR — noted: a COMMENTED review saying Copilot could not review because the requester reached the quota limit. It requests nothing.
- Copilot level: no review ran (quota limit), so there are no Copilot threads to handle.
