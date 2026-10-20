# M291: The cairn pane's summary card names the project at its top left

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the pane ships to every plugin user
- **Branch/PR:** m291-pane-card-project-name · https://github.com/jmgirard/cairn/pull/303

## Goal

The cairn pane's summary card shows the project's name in bold at the left of its first line, before the open pull request and issue counts.

## Scope

**In:** the name on the card's first line (`cardLines` in `hooks/status/pane.ts`), the name read beside the card's numbers (`baseOf` and `readRepo` in `hooks/status/register.tsx`, the `repo` atom to shape `repo-3`), a line flag that lets the tail grow so ⌂ and ↻ stay at the right end, tests, and the README, DESIGN, CHANGELOG, and `types/index.d.ts` text.

**Out:** a separate title line above the counts (the user chose the counts line at the question set). A placeholder in place of the folder name before the first read (AC3 accepts the folder name). Any other card line.

## Acceptance criteria

- [x] AC1: The summary card's first line holds the project name in bold at its left, then the open pull request and issue counts, with ⌂ (while no cairn skill's step is set) and ↻ at its right end; the candidates, milestones, and release lines follow it unchanged. Tested on `paneLines` output and on the drawn tree for the desktop and terminal surfaces.
- [x] AC2: Once a card read for the band's root has been written, whether or not its `gh` call gave counts, the project name is the repository part of the base remote's URL as `remoteRepo` in `repo.ts` parses it. When that URL is not a github.com one or the root has no base remote, the name is the name of the parent folder of the absolute `git rev-parse --git-common-dir` when that dir's own name is `.git`, so a linked worktree shows the repo's name and not the worktree's; otherwise, or when that git call fails, it is the last path segment of the band's root. Tested for an `origin` github.com remote, guest mode with an `upstream` github.com remote, guest mode with only `origin`, a remote not on github.com, no remote, a root inside a linked worktree, a common dir not named `.git`, and a failed git call.
- [x] AC3: While the store holds no card read written for the band's current root (a first read for that root, or after a change of root), the first line shows the last path segment of that root, never a name stored for another root; in a linked worktree that segment is the worktree's name until the read is written. Tested with a read held unsettled and with a stored read written for another root.
- [x] AC4: When the first line is too narrow for the whole name, the name is cut with an ellipsis, and the counts, ⌂, and ↻ keep their width. Tested on the drawn tree's props: the name's Text carries `wrap: 'truncate-end'` in a Box that may shrink, inside a line Box that may shrink below its content, and the counts' Box and each Button's Box have `flexShrink: 0`.
- [x] AC5: README's pane section, DESIGN.md's summary-card paragraph, the CHANGELOG's Unreleased summary-card entry, and `types/index.d.ts` describe the name and its rule, and the `verify` slot passes (`python3 -m unittest` in `scripts/tests` and `hooks/tests`, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test` for the status mod).

## Coverage

- AC1 → T2
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3

## Tasks

- [x] T1: The name read. `Where` (register.tsx ~1110) gains the main-tree name from `git rev-parse --path-format=absolute --git-common-dir` in the root, and `readRepo` writes `name`: `remoteRepo(url)?.repo`, else that name, else null. `CairnRepoRead` in `types/index.d.ts` gains `name`, and the `repo` atom moves to shape `repo-3` with its comment. Tests for each AC2 case in `pane.test.tsx`.
- [x] T2: The first line. `paneLines` passes the name (the stored read's for this root, else the root's last segment, split on `/` and `\`) to `cardLines`, which puts it bold in the line's `text` with no grow and the counts in its `tail`. A new line flag makes the tail Box grow in `drawLine`, so ⌂ and ↻ stay at the right end. Update the tests that pin the `card-repo` text, and add AC1, AC3, and AC4 tests for both surfaces.
- [x] T3: README, DESIGN.md, the CHANGELOG's Unreleased summary-card entry, and the pane.ts and register.tsx comments describe the name; run the `verify` slot.

## Work log

- 2026-10-19: created by /milestone-plan.
- 2026-10-19: tier check: milestone — a change to the pane's running code, not a bug.
- 2026-10-19: collision check: no candidate, planned, or D-entry overlap; extends M286's summary card (archived). Inbox: 0 open issues, 0 open PRs.
- 2026-10-19: question set: name placement — on the counts line, before the counts (the user's pick over a new title line). Live look — none; tests and a browser preview stand in.
- 2026-10-19: the user asked for the name in bold mid-plan; AC1 says bold.
- 2026-10-19: plan gate chose the GitHub repo name with the main-tree folder name as fallback over the root folder's name alone, because a desktop worktree root is named after the worktree; falsified by a repo whose GitHub name differs from what its operator calls the project.
- 2026-10-19: plan gate chose the folder name before the first read over a blank placeholder, because the folder name is right outside worktrees; falsified by an operator reading the worktree name as wrong in a real session.
- 2026-10-19: criteria audit (full mode, Opus): 5 findings on the first draft, all taken (stored-read wording for AC3, main-tree fallback, written-not-settled and failed-`gh` wording, guest-only-`origin` case, line Box in AC4's test). Re-audit after the placement answer: 3 findings, all taken (common dir not named `.git`, worktree name before the read stated in AC3, AC4 narrowed to a too-narrow line).
- 2026-10-19: untracked `cairn-probe.log` and `tsconfig.json` predate this plan; left unstaged.
- 2026-10-19: implement started on branch m291-pane-card-project-name.
- 2026-10-19: T1+T2 in one commit, since the AC2 tests read the name through the drawn line. `projectName` and `lastSegment` in repo.ts; the common-dir call runs only when the URL is not a github.com one; the first line has no text with no name (root `/`) and no lead space in its tail then. Updated 13 tests that pinned the old first line (text `''` with grow, counts in the lead). Mod tests 2304 → 2330, verify slot green.
- 2026-10-19: T3: README, DESIGN (card paragraph and `repo-3`), and the CHANGELOG's Unreleased card entry name the project and its rule; the simple-english hook flags older text in README and CHANGELOG, left as is (out of scope). Browser preview (a hand-built page, dark and light, 330 px, short and long names) shows the long name cut and the counts and Buttons kept. Verify slot green, mod tests 2330.
- 2026-10-19: claim audit: 48 claims read, 3 corrected — CHANGELOG.md, README.md, cairn/DESIGN.md (base remote only; a common dir not named `.git` and the first read fall back to the folder's own name; when the common-dir call runs). Re-read of the 3 pending.
- 2026-10-19: claim re-read: all 3 hold; one README sentence order slip (the worktree sentence) moved beside the first-read sentence.
- 2026-10-19: all tasks done, verify slot green (mod tests 2330 before the README reorder; Python suites rerun after it); status review.
- 2026-10-19: review: PR #303 opened at review start (Copilot round on), Copilot requested (pending). Fix-now work from the diff-bug and ripple lenses in progress (old-git common-dir output, type and header comments, DESIGN's grow sentence); verify not yet re-run on it.
- 2026-10-19: step-7 approval: m291-pane-card-project-name approved for merge
- 2026-10-19: review fixes verified: verify slot green on 550da7b4 (mod tests 2332, scripts and hooks suites OK, both validates exit 0, no `plugins[N].version` warning), `cairn_validate` all checks passed.

## Review

Evidence on head 550da7b4, 2026-10-19, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`: 2332 pass, 0 fail; all 28 M291-named tests pass.

- AC1: pane.test.tsx "the name bold, then the counts, then ⌂ and ↻ … (AC1, desktop|terminal)" pass: card children `card-repo`, `card-candidates`, `card-milestones`; first line children text, tail, home, refresh; name Text bold `alpha`; tail `  3 PRs   12 issues` with `flexGrow` 1. The M286 AC6 layout test pins the `paneLines` first line (`cairn` bold text, counts tail, `tailGrows`) and the unchanged candidates, milestones, and release lines; M236 tests pin ⌂ only while `acts`.
- AC2: eight "names <x> (AC2)" tests pass (origin github.com, guest upstream, guest origin only, gitlab, no remote, linked worktree, common dir `.git/modules/sub` → `subdir`, failed git call), each also asserting the common-dir call runs only without a github.com URL; "a failed GitHub read still names the project from the URL" pass; repo.test.ts `projectName` table (13 cases incl. Windows, bare repo, old git) pass.
- AC3: "a linked worktree draws its own folder name until the read is written", "a held read draws the root folder name, then the name it reads", and "a name stored for another root is not drawn" pass (`w1`, `proj` → `alpha`, `two`).
- AC4: "a long name is the part that is cut … (AC4, desktop|terminal)" pass at 44 columns: line Box `minWidth` 0, text Box `flexShrink` 1 and `minWidth` 0, its Text `wrap: 'truncate-end'`, tail, home, and refresh Boxes `flexShrink` 0.
- AC5: README (summary-card paragraph), DESIGN (card paragraph, `repo-3`, ↻ paragraph), CHANGELOG Unreleased card entry, and `types/index.d.ts` (`name`) describe it; verify slot: scripts OK, hooks OK, plugin validate 0, marketplace validate 0, mod test 0.

Consistency gate: `cairn_validate` all checks passed; no principle changed (no `cairn_impact` run); profile gate: verify green on the head, no marketplace version warning, CHANGELOG Unreleased entry covers the change.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: a cut name has no hover card on the desktop — follow-up, row "Card name edges"
- diff-bug #2: git before 2.31 echoes `--path-format=absolute` before the dir — fix now, fixed 96581092
- diff-bug #3: type comment omits the empty name for root `/` — fix now, fixed 96581092
- diff-bug #4: `cardLines` header comment omits the name — fix now, fixed 96581092
- diff-bug #5: one reflowed comment line runs long — reject (style)
- diff-bug #6: AC1 drawn-tree test does not pin the other lines' text or the ⌂-absent case — reject (false: the M286 AC6 layout test and the M236 tests pin both)
- diff-bug #7: a drive-root `C:\` names the card `C:` — reject (false as a defect: a drive root has no folder name, and `C:` names it)
- diff-bug #8: odd github.com repo segments reach the card as parsed — follow-up, row "Card name edges" (pre-existing parser)
- prior-review #1: no live look though LESSONS says drawing needs one — reject (planned change: the user chose a browser preview at the question set); recorded in row "Card name edges"
- prior-review #2: a cut name has no hover card — follow-up, row "Card name edges" (same as diff-bug #1)
- ripple #1: DESIGN's ↻ paragraph says the first line's text grows — fix now, fixed 96581092
- ripple #2: `readRepo` comment says three git calls — fix now, fixed 96581092
- ripple #3: repo.ts header omits the name read — fix now, fixed 96581092
- ripple #4: `cardLines` comment omits the name — fix now, fixed 96581092 (same as diff-bug #4)
- ripple #5: pane.ts file header omits the name — fix now, fixed 96581092
- ripple #6: the `repo` atom comment omits the name — fix now, fixed 96581092
- blame-history #1: the `repo-3` bump drops shipped `repo-2` counts until the first read — reject (planned change: LESSONS M193 requires a new tag for a changed value layout)
- blame-history #2: DESIGN's ↻ paragraph stale — fix now, fixed 96581092 (same as ripple #1)
- blame-history #3: git before 2.31 — fix now, fixed 96581092 (same as diff-bug #2)
- blame-history #4: one more git call per read without a github.com remote — reject (planned change, AC2)
- blame-history #5: the M236 test now pins the tail's grow — reject (planned change; ↻ stays at the right end)
- blame-history #6: the M226 test's `repo` after the move is a mock artifact — reject (false: that name comes from the origin URL; the M291 tests cover a name per root)
- blame-history #7: comments at pane.ts:654 and pane.test.tsx:3709 drift — reject (false: both still describe what grows)
- copilot: review body — the release-line test's stored read lacks the required `name` — fix now, fixed 6e87160e (verify green after: mod tests 2332)
- copilot: review body summary — noted; summary reply posted (issuecomment-6280891829). No threads.
- Copilot level: Lite (set by GitHub's settings; the state query printed `unknown`, the known `<sub>` form in row "Copilot level line format")
- conversation: no other reviews or comments on PR #303.
