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

- [ ] AC1: If one or more ROADMAP rows are `blocked`, the pane draws a
      `Blocked` section after the Waiting section's place. The section
      holds one line per blocked row in ROADMAP order, with its id and
      title. If the milestone file's `Branch/PR` header names a pull
      request URL `https://github.com/<owner>/<repo>/pull/<n>` before any
      `companion:` entry, the line ends with `#<n>`. With several such
      URLs, the first one gives the number. `pane.test.tsx` cases show this
      over new fixtures, one with an active milestone and one with none.
      Their blocked rows together cover one URL, two URLs, a URL only
      after a `companion:` entry, and a URL with a trailing path.
- [ ] AC2: A blocked row draws its id and title with no number in three
      cases. Its milestone file is missing, or its read fails (the
      fixtures' `unreadable` list), or its header names no such URL. With
      no blocked row, the pane draws no `Blocked` section. `pane.test.tsx`
      shows this with one case per row shape and a fixture with no blocked
      row.
- [ ] AC3: For each row shape that AC1 and AC2 name, the reader's blocked
      rows and PR numbers equal those of a new helper in
      `scripts/cairn_next.py`. `scripts/tests/test_status_fixtures.py`
      holds the two equal over the fixtures under `hooks/status/fixtures/`.
      `cairn_next.py` prints an "Externally blocked" line that ends with
      ` (PR #<n>)` for a numbered row and has no suffix for an unnumbered
      row. A `scripts/tests` case shows both.
- [ ] AC4: The operator looks at the desktop app's docked pane in the
      guest-mode insight checkout (`~/github/insight`, four handed-off
      PRs). The Blocked section draws each row's id, title, and number on
      one line. The operator accepts this at the merge question.
- [ ] AC5: README's pane section, `cairn/DESIGN.md`'s pane text, and
      CHANGELOG.md's Unreleased section describe the Blocked section. Each
      claim is read against the code at implement time.
- [ ] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

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

## Decisions

## Review
