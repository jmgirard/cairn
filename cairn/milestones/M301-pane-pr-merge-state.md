# M301: Show each open PR's merge state in the pane

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane's PR lines are what operators read
- **Branch/PR:** m301-pane-pr-merge-state

## Goal

Each open pull request line in the cairn pane shows an icon that tells whether the PR can merge or has conflicts.

## Scope

**In:** the PR read asks GitHub for `mergeable` on the graphql call and on the `gh pr view` call. The read keeps a merge state for an open PR. The `prs` state value takes the new field under a new shape tag. Two new icons, `mergeable` (green) and `conflicts` (red), each with a terminal glyph, go last in the tail of a Blocked or Hotfixes line. The changelog, `README.md`, and `cairn/DESIGN.md` describe the icon.

**Out:** the band (status line) shows no merge state, since it draws no PR lines. The behind-base, blocked-by-checks, and draft states of GitHub's `mergeStateStatus` are not shown, because the request named only mergeable and conflicts. No candidate row holds them. No timer re-reads a PR whose state GitHub reports as `UNKNOWN`, since the pane starts no read without an operator act (DESIGN, cairn pane part).

## Acceptance criteria

- [ ] AC1: An open pull request's read carries its merge state. The `gh api graphql` query in `hooks/status/counts.ts` asks for `mergeable`. The `gh pr view` fields, an exported constant that `readPr` in `hooks/status/register.tsx` uses, ask for it too, and a test asserts that constant. A read whose word is in `OPEN_WORDS` maps `MERGEABLE` to `mergeable` and `CONFLICTING` to `conflicts`. It maps `UNKNOWN`, any other value, or an absent field to null. A read whose word is not in `OPEN_WORDS` carries null. Tests in `hooks/status/counts.test.ts` and `hooks/status/pane.test.tsx` feed five inputs through both reply forms and assert the mapped value. The inputs are `MERGEABLE`, `CONFLICTING`, `UNKNOWN`, another string, and the field absent. The tests also feed a `MERGED` reply and a `CLOSED` reply, each carrying `MERGEABLE`.
- [ ] AC2: The pane draws the merge state as an icon. A Blocked or Hotfixes line whose read carries `mergeable` ends its tail with a span that names the `mergeable` icon. A line whose read carries `conflicts` ends its tail with a span that names the `conflicts` icon. Each icon comes after the state word, and each span carries a non-empty text glyph, which the terminal draws. A line whose read carries null draws neither icon, and a line with no read yet draws neither. Tests in `hooks/status/pane.test.tsx` assert these four cases on a blocked line and on a hotfix line, by the span's icon name and glyph.
- [ ] AC3: A live look runs in a new desktop Code session on this repo, in the dark and the light theme. The line of a throwaway draft hotfix PR whose branch conflicts with the default branch shows the conflicts icon. After the conflict is resolved on that branch, a ↻ press made once GitHub reports `MERGEABLE` shows the mergeable icon. An `UNKNOWN` read in between draws no icon. The PR is then closed unmerged and its branch deleted.
- [ ] AC4: `CHANGELOG.md`'s Unreleased section gains one entry for the merge-state icon. Two passages state the `mergeable` read, the two icons, and that an `UNKNOWN` reply draws no icon until a later read. They are the pane PR-line part of `README.md` that holds the state-word table, and the cairn pane part of `cairn/DESIGN.md`.
- [ ] AC5: The five `verify` commands in `cairn/PROFILE.md` each exit 0.

## Coverage

- AC1 → T1, T2
- AC2 → T3, T4
- AC3 → T6
- AC4 → T5
- AC5 → T1, T2, T3, T4, T5

## Tasks

- [x] T1: Read. Add `mergeable` to `COUNTS_QUERY` in `hooks/status/counts.ts` and map it in `prRead`. Add a `mergeOf` mapper in `pane.ts` beside `wordOf`. Export the `gh pr view` fields as a constant (`state,reviewDecision,mergeable`) and use it in `readPr`. Give `prWord`'s path the merge state too. Tests per AC1 in `counts.test.ts` and `pane.test.tsx`.
- [x] T2: State. Add `mergeable: 'mergeable' | 'conflicts' | null` to `CairnPrRead` in `types/index.d.ts`. Change the `prs` atom's shape tag in `register.tsx` from `prs-3` to `prs-4`. Update every test fixture and stub that builds a `prs` value or a `PrRead`.
- [x] T3: Icons. Add `mergeable` and `conflicts` to `IconName` in `hooks/status/icons.ts`, with a red in `ICON_COLORS`. Draw a merge symbol in green for one and in red for the other, or a red mark that differs from `attention`. Pick terminal glyphs that no other pane mark uses.
- [x] T4: Draw. In `prLine` (`pane.ts`), push the icon span last in the tail for an open read with a merge state. Check that `centers` in `register.tsx` centers a tail icon on the desktop, and fix it if not. Tests per AC2 on a blocked line and a hotfix line.
- [ ] T5: Docs. Add the changelog entry, and the README and DESIGN passages per AC4, each written against a same-session read of the shipped code.
- [ ] T6: Live look per AC3. Cut a `hotfix-` branch that edits a line `main` also changes, open it as a draft PR, and look in a new desktop Code session in both themes. Resolve the conflict, push, press ↻ until GitHub answers, and look again. Close the PR unmerged and delete its branch.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: milestone — a new pane feature with a design choice (which states get an icon), not a bug or a no-runtime edit.
- 2026-10-20: collision sweep: no ROADMAP row, archive summary, or D-entry heading names mergeable or merge conflicts. Inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-20: lessons harvested: mod facts (new shape tag on a value layout change, `types/index.d.ts` by hand, drawing needs a live look in a new session) and live-look conduct (a real repo, never a scratch folder).
- 2026-10-20: criteria audit (full mode, fresh Opus reader) returned 6 findings, all fixed: AC1 tests the `gh pr view` fields as an exported constant and adds a `CLOSED` reply, AC2 requires a non-empty terminal glyph, AC3 allows an `UNKNOWN` read between push and answer, names the throwaway PR, and drops its recording clause. Side note on tail-icon centering moved to T4.
- 2026-10-20: question set: which states get an icon — both, green mergeable and red conflicts.
- 2026-10-20: question set: may review open a throwaway draft hotfix PR on jmgirard/cairn that conflicts with main, look in a new session, then close it unmerged and delete its branch — yes.
- 2026-10-20: plan chose the icon last in the tail, after the state word, over beside the number, because the tail sits at the line's right end, so icons line up in one column; falsified by a live look where the icon is cut or crowds the word in a 44-column dock.
- 2026-10-20: plan chose GitHub's `mergeable` field over `mergeStateStatus`, because the request named only mergeable and conflicts, and `mergeStateStatus` mixes in checks and review state; falsified by the operator asking for behind-base or blocked-by-checks marks.
- 2026-10-20: started /milestone-implement on branch m301-pane-pr-merge-state. Untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-20: T1+T2 done: `mergeOf` and `prViewRead` in pane.ts, `PR_VIEW_FIELDS` used by `readPr`, `mergeable` in `COUNTS_QUERY` and `prRead`, `CairnPrMerge` and the `mergeable` field in types/index.d.ts, `prs` shape tag `prs-4`. Chose a separate `prViewRead` over widening `prWord`, so `prWord`'s word-only tests stand. Verify: all five green (mod suite 2404 pass).
- 2026-10-20: T3+T4 done: `mergeable` icon is a green merge symbol, `conflicts` a red disc with an ink cross (new `red` in `ICON_COLORS`); terminal glyphs `✓` (success key) and `✗` (error key), which no other pane mark uses. Chose a disc-and-cross for conflicts over a red merge symbol, so the two differ by shape as well as color. `MERGE_MARK` in pane.ts; `prLine` pushes it last in the tail; `centers` now also centers a row with a tail icon. A planted defect (mark never pushed) turned the 4 mergeable/conflicts AC2 tests red. Verify: all five green (mod suite 2412 pass).

## Decisions

## Review
