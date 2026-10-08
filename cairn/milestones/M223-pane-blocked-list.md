# M223: The pane lists blocked milestones and their PRs

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** m223-pane-blocked-list

## Goal

The cairn pane lists each `blocked` milestone and the pull request its header names, so the operator sees waiting PRs without running `/milestone`.

## Scope

**In:** `reader.ts` gains a `blocked` list in the pane state. The list
holds each `blocked` ROADMAP row in ROADMAP order. Each entry has the id,
the title, and the number of the pull request that the milestone file's
`Branch/PR` header names. The number comes from the first
`https://github.com/<owner>/<repo>/pull/<n>` URL before any `companion:`
entry. A trailing path such as `/files` does not change the number. A new
`blocked` helper in `scripts/cairn_next.py` computes the same list. Its
printed "Externally blocked" lines end with ` (PR #<n>)` for a numbered
row. `pane.ts` draws a `Blocked` section after the Waiting section and
before the Candidates. The section shows whether or not a milestone is
active. The pane atom's shape tag moves on (LESSONS M193). README, DESIGN,
and CHANGELOG describe the section.

**Out:** M224 reads each PR's state from GitHub and adds a Button per row.
M224 is planned now and depends on M223. The band does not change, because
the plan gate kept the PR view in the pane only. Blocked rows stay out of
the Next line's recommendation, which `scripts/cairn_next.py` decides.

## Acceptance criteria

- [x] AC1: If one or more ROADMAP rows are `blocked`, the pane draws a
      `Blocked` section after the Waiting section's place. The section
      holds one line per blocked row in ROADMAP order, with its id and
      title. If the milestone file's `Branch/PR` header names a pull
      request URL `https://github.com/<owner>/<repo>/pull/<n>` before any
      `companion:` entry, the line ends with `#<n>`. With several such
      URLs, the first one gives the number. `pane.test.tsx` cases show this
      over new fixtures, one with an active milestone and one with none.
      Their blocked rows together cover one URL, two URLs, a URL only
      after a `companion:` entry, and a URL with a trailing path.
- [x] AC2: A blocked row draws its id and title with no number in three
      cases. Its milestone file is missing, or its read fails (the
      fixtures' `unreadable` list), or its header names no such URL. With
      no blocked row, the pane draws no `Blocked` section. `pane.test.tsx`
      shows this with one case per row shape and a fixture with no blocked
      row.
- [x] AC3: For each row shape that AC1 and AC2 name, the reader's blocked
      rows and PR numbers equal those of a new helper in
      `scripts/cairn_next.py`. `scripts/tests/test_status_fixtures.py`
      holds the two equal over the fixtures under `hooks/status/fixtures/`.
      `cairn_next.py` prints an "Externally blocked" line that ends with
      ` (PR #<n>)` for a numbered row and has no suffix for an unnumbered
      row. A `scripts/tests` case shows both.
- [x] AC4: The operator looks at the desktop app's docked pane in the
      guest-mode insight checkout (`~/github/insight`, four handed-off
      PRs). The Blocked section draws each row's id, title, and number on
      one line. The operator accepts this at the merge question.
- [x] AC5: README's pane section, `cairn/DESIGN.md`'s pane text, and
      CHANGELOG.md's Unreleased section describe the Blocked section. Each
      claim is read against the code at implement time.
- [x] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T1, T2
- AC4 → T5
- AC5 → T4
- AC6 → T3, T4

## Tasks

- [x] T1: Fixtures and tests first. Add fixtures under
      `hooks/status/fixtures/` for the AC1 and AC2 row shapes, with and
      without an active milestone. Extend `gen_fixtures.py` and each
      `expected.json` with a `blocked` key. The `all-waiting` and
      `no-active` fixtures already hold blocked rows with no URL. Add the
      `pane.test.tsx` cases and the `scripts/tests` print case. Make sure
      that they fail against the current code.
- [x] T2: Add the `blocked` helper to `scripts/cairn_next.py` beside
      `waiting` (line 51), and the suffix to `render`'s "Externally
      blocked" lines. Add the second implementation in
      `test_status_fixtures.py`. Mirror the helper in `reader.ts`'s
      `loadAt` (line 288) and `PaneState`, and in the `cairn.pane` contract
      in `types/index.d.ts`.
- [x] T3: Draw the section in `pane.ts`'s `paneLines` (line 217), with the
      queue's heading and color and the number in the line's `tail`. Move
      the pane atom's shape tag in `register.tsx` (line 94). Run `verify`.
- [x] T4: Describe the section in README.md's "The cairn pane", in
      `cairn/DESIGN.md` near the M219 pane text, and in CHANGELOG.md's
      Unreleased section. Run `verify`.
- [x] T5: Prepare the live look in a new desktop Code session in
      `~/github/insight`, with the cairn pane open (LESSONS M195, M213).
      Review runs the look before the merge question, as the question set
      placed it.

## Work log

- 2026-10-08: created by /milestone-plan.
- 2026-10-08: collision sweep: no ROADMAP row, archive entry, or D-entry covers blocked milestones or PR state in the pane. M205 drew only `in-progress` and `review` rows. The "Pane content follow-ons" row names decisions and lessons, a different scope. D-143 (the mod ships in the plugin) governs and does not change. The GitHub inbox has 0 open issues and 0 open PRs.
- 2026-10-08: criteria audit (full mode, fresh Opus reader) over M223 and M224: 12 findings, all taken toward the narrower promise. In M223, AC1's cases cover the URL forms. AC2 names a failed read and one case per shape. AC3 binds the reader-equals-Python promise per row shape and names a test for the print suffix.
- 2026-10-08: question set: live look in the desktop app at review in `~/github/insight` — granted.
- 2026-10-08: question set: a band note for a PR that needs the operator — declined, pane only.
- 2026-10-08: plan chose to list all `blocked` rows over only rows with a PR, because an owner-mode blocked row also waits on someone. Falsified by an operator who finds the rows with no PR to be noise.
- 2026-10-08: plan chose to draw the section in every state over only while idle, because a guest often implements one PR while others wait. Falsified by the section pushing the active milestone's tasks off a 44-column pane in a real session.

- 2026-10-08: implement started on branch `m223-pane-blocked-list`. The untracked `cairn-probe.log` and `tsconfig.json` at the repo root are not this milestone's and stay unstaged.
- 2026-10-08: T1: fixtures `blocked-prs` (seven blocked rows, one per URL and file shape, no active row, one candidate row so the Candidates order shows) and `blocked-active` (one in-progress row beside one blocked row). An `expected.json` `blocked` key defaults to empty, as `unreadable` does, so only `no-active` and `all-waiting` gained one. Before T2, 22 Python subtests failed with `cairn_next` having no `blocked`, the print case failed on the missing suffix, and 16 mod cases failed on the missing section. Two band tables (`EMPTY_FIXTURES`, `FLOWS`) list fixtures by hand and took the new ones.
- 2026-10-08: T2: `blocked`, `pr_number`, and `read_file` in `scripts/cairn_next.py`. The `read` argument lets the fixture test fail the reads the fixtures mark `unreadable`. `prNumber` in `reader.ts` mirrors `pr_number` with `[0-9]` in place of `\d`. One case list of nine header forms (fragment, issue URL, a URL in the body) runs on both sides. `cairn_next.py` on `~/github/insight` printed `(PR #1250)` and `(PR #1247)`, and no suffix for M007, whose header names only a branch.
- 2026-10-08: T3: the section draws after Waiting with the queue's color and a row count, and the number sits in the line's tail in gray. Pane shape tag `pane-3`. verify: all five checks exit 0, with 1434 mod tests.
- 2026-10-08: T4: README "The cairn pane", DESIGN's pane-state paragraph and module line, and a CHANGELOG Unreleased New entry describe the section, written against the T1-T3 tests and the insight run. verify: all five checks exit 0, and `cairn_validate` passes.
- 2026-10-08: minor amendment: T5 now prepares the live look, and review runs it before the merge question, where the question set placed it. The plugin loads from this checkout through the `~/.claude/skills/cairn` symlink, so a new desktop Code session in `~/github/insight` draws the branch's mod.
- 2026-10-08: claim audit: 44 claims read, 2 corrected — CHANGELOG.md, README.md (both now say the number comes from a GitHub pull request URL before any `companion:` entry; the same reader re-read both as true). The reader also caught a dropped space in `gen_fixtures.py`'s `unreadable:` line, restored and regenerated. verify: all five checks exit 0.
- 2026-10-08: implement done; status set to `review`.
- 2026-10-08: merge question: the operator asked whether the pane reports unanswered comments or Copilot reviews. It does not, and M224 as planned does not either. The operator chose to add those counts to M224, which is amended on main after this merge.
- 2026-10-08: step-7 approval: m223-pane-blocked-list approved for merge

## Decisions

## Review

Fresh run on 74b9ebd, 2026-10-08. The branch contains `origin/main` (505c070), so no sync was needed.

- AC1 evidence: `claude plugin test .` passes all 53 cases of "the pane lists the blocked milestones and their PRs", 26 on each surface plus the domain case. On both surfaces, `blocked-prs` (no active row) draws `▎ BLOCKED 7` with the seven hand-written lines: `#12` for one URL, `#34` for the first of two, `#90` for a trailing `/files`, and no number for a URL only after `companion:`. The heading comes after `next`, and `candidates-head` comes after the last blocked line. `blocked-active` draws `M111  Handed to the maintainers  #1250` after `next`, beside `M110-head`. In `all-waiting`, the section follows `waiting-M093`. The number sits in the `blocked-M111-tail` Box.
- AC2 evidence: in the same run, the `blocked-prs` lines show no number for M105 (no URL), M106 (the read fails, from the fixture's `unreadable` list), and M107 (missing file). The per-fixture case passes over all 23 fixtures with a ROADMAP on both surfaces, and it asserts that no `blocked` key is drawn where a fixture has no blocked row, as in `single-in-progress`.
- AC3 evidence: `python3 -m unittest discover -s scripts/tests` ran 400 tests, OK. In it, `test_python_helpers_match_expected` holds `cairn_next.blocked` to each fixture's `blocked` key over all 23 fixtures, and `reader.test.ts` holds `loadCairn(...).pane.blocked` to the same key (23 passing reader cases). `test_blocked_fixtures_hold_the_row_shapes` and `test_pr_number_header_forms` pass. So does `test_externally_blocked_line_names_its_pull_request`, where `  M05 — Handed off (PR #1250)` has the suffix and `  M06 — Held` has none.
- AC5 evidence: README.md:304, `cairn/DESIGN.md`:270-282, and CHANGELOG.md:7 describe the section. The claim audit (work log) read 44 claims and corrected 2, and the same reader re-read both as true.
- AC6 evidence: all five `verify` commands exit 0. `scripts/tests` ran 400 tests, `hooks/tests` ran 174, both `claude plugin validate` runs passed, and `claude plugin test .` ran 1434 tests with 0 failures.
- consistency gate: `cairn_validate` passes. The profile gate's three checks pass: verify is green on the review head, the marketplace validate prints no `plugins[N].version` warning, and the CHANGELOG Unreleased entry names no milestone number. No principle changed, so `cairn_impact` was skipped.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the `companion:` cut gives no number when an owner-mode primary PR URL is written after a companion entry — follow-up, row "Blocked-row PR number edges (M223 review)".
- diff-bug #2: DESIGN Known issues still named the `pane-2` tag — fix now, fixed 77e89b0 (corrected in place).
- diff-bug #3: `\s` takes different characters in Python and JavaScript (`\x1f`, a BOM) — fix now, fixed 77e89b0: both regexes spell out space and tab, with a BOM case and a tab case on both sides.
- diff-bug #4: a number past 2^53 reads differently on the two sides — fix now, fixed 77e89b0: the URL takes at most 15 digits and a longer number reads as none, tested on both sides.
- diff-bug #5: a non-UTF-8 milestone file can give a number in the pane and none in `cairn_next.py` — follow-up, same row.
- diff-bug #6: a `Branch/PR` line quoted below the header also counted — fix now, fixed 77e89b0: both sides stop at the first `## ` heading, tested on both sides.
- diff-bug #7: `Companion:` capitalized, an upper-case host, and `www.github.com` are not matched — reject (planned change: AC1 names the exact URL form, and the template spells `companion:` in lower case).
- diff-bug #8: the header-form cases are two hand-kept lists, and the T2 work-log line's "one case list runs on both sides" overstates it — reject (test structure: both lists state their expectations by hand, and the blocked-prs fixture ties the sides together). The work-log line means one list copied to both sides.
- diff-bug #9: no case for two `Branch/PR` lines with no URL in the first — fix now, fixed 77e89b0: added on both sides.
- diff-bug #10: the order of Workable before Blocked was not tested — fix now, fixed 77e89b0: `blocked-active` gained a workable row M112, and the case asserts the order.
- diff-bug #11: duplicate ids give duplicate `blocked-<id>` keys — reject (false as new: DESIGN Known issues already records duplicate pane keys).
- diff-bug #12: the `pane.ts` queue-color comment did not name Blocked — fix now, fixed 77e89b0.
- diff-bug #13: the new README, DESIGN, and `reader.ts` text was not wrapped — fix now, fixed 77e89b0 (rewrapped, with a blank line before the README paragraph).
- blame-history #1: the same companion-order gap as diff-bug #1 — follow-up, same row.
- blame-history #2: blocked rows now read their files at every refresh — reject (planned change: the scope reads the header, and the regular-file guard stays).
- blame-history #3: the M205 record says `cairn_next.py`'s output is unchanged, and the module docstring did not name blocked rows — fix now, fixed 77e89b0 (docstring). The new suffix is planned, and no consumer parses those lines.
- blame-history #4: README paragraph glued to the candidates paragraph, and long lines — fix now, fixed 77e89b0 (as diff-bug #13).
- prior-review #1: the 44-column width sweep did not include the blocked fixtures — fix now, fixed 77e89b0: `blocked-prs` and `blocked-active` added.
- prior-review #2: no heading case for `blocked-head` — fix now, fixed 77e89b0: two HEADS rows added.
- prior-review #3: after a reload, the moved shape tag shows `no cairn ROADMAP found` until the next refresh — fix now, fixed 77e89b0 (the Known issues text now names the moved tag, as diff-bug #2).
- prior-review #4: duplicate ids give duplicate keys — reject (as diff-bug #11).
- prior-review #5: the `\s` difference — fix now, fixed 77e89b0 (as diff-bug #3).
- prior-review #6: the case lists are written twice — reject (as diff-bug #8).
- prior-review #7: `CairnPaneState` in `types/index.d.ts` and `PaneState` in `reader.ts` are two copies — follow-up, same row (pre-existing, and M223 kept them equal).
- prior-review #8: ragged wraps — fix now, fixed 77e89b0 (as diff-bug #13).
- AC4 evidence: at the merge question on 2026-10-08, the operator opened a new desktop Code session in `~/github/insight`, ran `/cairn-pane`, and answered "looks right" to the described Blocked section (M007 with no number, M006 `#1250`, M005 `#1247`, one line each).
- fix-now re-run on the fixed tree: all five verify commands exit 0. `scripts/tests` ran 400 tests and `claude plugin test .` ran 1442 tests, all passing. `cairn_validate` passes, and `cairn_next.py` on insight prints the same three lines as before.
