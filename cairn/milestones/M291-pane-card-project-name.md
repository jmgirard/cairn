# M291: The cairn pane's summary card names the project at its top left

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the pane ships to every plugin user
- **Branch/PR:** —

## Goal

The cairn pane's summary card shows the project's name in bold at the left of its first line, before the open pull request and issue counts.

## Scope

**In:** the name on the card's first line (`cardLines` in `hooks/status/pane.ts`), the name read beside the card's numbers (`baseOf` and `readRepo` in `hooks/status/register.tsx`, the `repo` atom to shape `repo-3`), a line flag that lets the tail grow so ⌂ and ↻ stay at the right end, tests, and the README, DESIGN, CHANGELOG, and `types/index.d.ts` text.

**Out:** a separate title line above the counts (the user chose the counts line at the question set). A placeholder in place of the folder name before the first read (AC3 accepts the folder name). Any other card line.

## Acceptance criteria

- [ ] AC1: The summary card's first line holds the project name in bold at its left, then the open pull request and issue counts, with ⌂ (while no cairn skill's step is set) and ↻ at its right end; the candidates, milestones, and release lines follow it unchanged. Tested on `paneLines` output and on the drawn tree for the desktop and terminal surfaces.
- [ ] AC2: Once a card read for the band's root has been written, whether or not its `gh` call gave counts, the project name is the repository part of the base remote's URL as `remoteRepo` in `repo.ts` parses it. When that URL is not a github.com one or the root has no base remote, the name is the name of the parent folder of the absolute `git rev-parse --git-common-dir` when that dir's own name is `.git`, so a linked worktree shows the repo's name and not the worktree's; otherwise, or when that git call fails, it is the last path segment of the band's root. Tested for an `origin` github.com remote, guest mode with an `upstream` github.com remote, guest mode with only `origin`, a remote not on github.com, no remote, a root inside a linked worktree, a common dir not named `.git`, and a failed git call.
- [ ] AC3: While the store holds no card read written for the band's current root (a first read for that root, or after a change of root), the first line shows the last path segment of that root, never a name stored for another root; in a linked worktree that segment is the worktree's name until the read is written. Tested with a read held unsettled and with a stored read written for another root.
- [ ] AC4: When the first line is too narrow for the whole name, the name is cut with an ellipsis, and the counts, ⌂, and ↻ keep their width. Tested on the drawn tree's props: the name's Text carries `wrap: 'truncate-end'` in a Box that may shrink, inside a line Box that may shrink below its content, and the counts' Box and each Button's Box have `flexShrink: 0`.
- [ ] AC5: README's pane section, DESIGN.md's summary-card paragraph, the CHANGELOG's Unreleased summary-card entry, and `types/index.d.ts` describe the name and its rule, and the `verify` slot passes (`python3 -m unittest` in `scripts/tests` and `hooks/tests`, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test` for the status mod).

## Coverage

- AC1 → T2
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3

## Tasks

- [ ] T1: The name read. `Where` (register.tsx ~1110) gains the main-tree name from `git rev-parse --path-format=absolute --git-common-dir` in the root, and `readRepo` writes `name`: `remoteRepo(url)?.repo`, else that name, else null. `CairnRepoRead` in `types/index.d.ts` gains `name`, and the `repo` atom moves to shape `repo-3` with its comment. Tests for each AC2 case in `pane.test.tsx`.
- [ ] T2: The first line. `paneLines` passes the name (the stored read's for this root, else the root's last segment, split on `/` and `\`) to `cardLines`, which puts it bold in the line's `text` with no grow and the counts in its `tail`. A new line flag makes the tail Box grow in `drawLine`, so ⌂ and ↻ stay at the right end. Update the tests that pin the `card-repo` text, and add AC1, AC3, and AC4 tests for both surfaces.
- [ ] T3: README, DESIGN.md, the CHANGELOG's Unreleased summary-card entry, and the pane.ts and register.tsx comments describe the name; run the `verify` slot.

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
