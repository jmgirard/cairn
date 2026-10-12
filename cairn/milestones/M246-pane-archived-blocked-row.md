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
- [x] AC5: At Session start, `skills/milestone-review/SKILL.md` accepts a target whose live milestone file is missing and whose single archive file's `**Status:**` paragraph starts with `done`.
      Its "Resume routing" has an arm for that target that reads no `Branch/PR` header and no PR state.
      The arm skips steps 1 to 8 and step 9's summary write and live-file delete.
      It runs step 9 from the ROADMAP row update onward, then step 10.
      It skips step 9's issue writes, and its recap names each `resolves` entry of the archive's Status paragraph as owed.
- [x] AC6: `cairn/DESIGN.md`'s paragraph on the pane's `blocked` rows, `README.md`'s description of the pane's blocked section, and a `CHANGELOG.md` entry each state the archive fallback and the `archived` mark.
- [x] AC7: The profile's `verify` slot is green: its five commands each exit 0 from the repo root.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T1, T4
- AC4 → T1, T2
- AC5 → T5
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
