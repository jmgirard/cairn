# M236: The pane has one ↻ Button and counts only unresolved threads

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane is part of the shipped status mod
- **Branch/PR:** m236-pane-one-refresh

## Goal

The cairn pane shows only the unresolved review threads of each PR, and one ↻ Button at the right end of the pane's first line reads everything again and shows ⋯ while a read runs.

## Scope

**In:** Remove the `unanswered` count from the counts read, its state, and the pane's count line. Keep the `unresolved` count. Replace the `Refresh` Buttons on the `BLOCKED` and `HOTFIXES` headings with one ↻ Button at the right end of the pane's first line. A milestone's head line shows its id in the phase color, with no phase word. The ↻ label is `⋯` while a read of PR states runs. A press during an earlier ↻ press's read does nothing. Update README, DESIGN, and CHANGELOG.

**Out:** A timer or turn-end read. The pane reads only at an open, a press, and an in-process `/clear` (M224, M230). That rule stays. The band's own Buttons stay as they are. The other pane edges stay in the candidate rows "Pane edges (M222–M226 reviews)" and "Pane edges (M230 review)".

## Acceptance criteria

- [ ] AC1: `prCounts` and `countPr` in `hooks/status/counts.ts` give only `unresolved`, the number of review threads with `isResolved` false. `COUNTS_QUERY` asks for no reviews, conversation comments, or commits. `CairnPrRead` in `types/index.d.ts` holds `counts: { unresolved: number } | null`, and the `prs` atom takes a new `shape` tag. The pane's count line reads `1 unresolved thread` or `N unresolved threads`, and no count line shows when the number is 0. `git grep -n -i "unanswered" -- hooks/status types README.md cairn/DESIGN.md` returns no match. `claude plugin test .` passes tests for these replies: no threads, one unresolved thread, two unresolved threads with one resolved thread, a reply whose threads are not a list (counts null), and the reply that PR #245 gave on 2026-10-10. That reply is stored as `gh api graphql` printed it with the new query, unedited. It has one Copilot review and no threads, and it gives `unresolved` 0 and no count line.
- [ ] AC2: In the drawn pane for a found ROADMAP, exactly one Button has the key `cairn-pane-refresh`. It sits on the first line that `paneLines` gives. That line is the first milestone's head line, or the `no active milestone` line when no milestone is active. The Button's Box, `<line key>-refresh`, is the last child of that line's Box, after the tail Box when the head line has a percent. Only that line's text Box has `flexGrow` 1, so its tail and the Button sit at the right end, and no line Box has `justifyContent`. No Button key ends in `-hotfixes`, and the `BLOCKED` and `HOTFIXES` heading rows carry no Button. `claude plugin test .` passes tests that find every Button in the drawn pane (`findAll`) for five states. The first state has blocked PRs and hotfix PRs and no active milestone. The second has an `in-progress` and a `review` milestone, and its second head line carries no Button. The third has the Next line with Status and Clear and one active milestone. The fourth has one active milestone and no PRs. The fifth has no ROADMAP and draws no `cairn-pane-refresh` Button.
- [ ] AC3: A milestone's head line starts with its id, bold, in its phase's color. That is the implement color for `in-progress` and the review color for `review`, the two statuses that reach the pane. No phase word comes before the id. `claude plugin test .` passes tests that check the head line's lead spans for an `in-progress` and a `review` milestone.
- [ ] AC4: From the start of any read of PR states (a pane open, a ↻ press, or an in-process `/clear`) until the newest read started has settled, the `cairn-pane-refresh` Button's label is `⋯`. At other times its label is `↻`, also after a read whose calls exit non-zero or reject, except that a stored reading state of true left by a reload shows `⋯` until the next read settles. From a ↻ press until the read it started settles, a further press reads no file and runs no `$.process.run` call. A press when no press's read runs reads the tracking files, the hotfix list, and the state and thread count of each PR, as the old `Refresh` press did. When the stored reading state is true but no press's read runs in this module, as after a reload, a press starts a read, and the label is `↻` when that read settles. `claude plugin test .` passes tests in `hooks/status/pane.test.tsx` for seven cases. A held read shows `⋯`, with the Button's Box still the last child of the first line. The label is `↻` after the read succeeds, after it exits 1, and after it rejects. An open and a press overlap, the older read held longer, and the label is `↻` once the newer read settles. A second press during a held press read leaves the number of `$.fs.read`, `gh pr view`, `gh api graphql`, `gh pr list`, and `git` calls unchanged, with a blocked PR URL in the fixture. A stored reading state of true with no read in this module lets a press start a read.
- [ ] AC5: README's pane section and the `hooks/status/` entry in DESIGN describe the one ↻ Button at the right end of the pane's first line and its `⋯` label during a read. They say that a press during an earlier ↻ press's read does nothing. They say that the count line shows only unresolved threads, and that a head line shows the milestone id in its phase color with no phase word. No line that `git grep -n -i "refresh" -- README.md cairn/DESIGN.md` returns puts a Button on the `BLOCKED` or `HOTFIXES` heading. No line that `git grep -n -i "dim" -- README.md cairn/DESIGN.md CHANGELOG.md` returns says that the ↻ draws dim or with `dimColor`. `CHANGELOG.md` has entries under `## Unreleased` for the thread-only count, the one ↻ Button on the first line with its `⋯` label, and the head line's id in its phase color with no phase word.
- [ ] AC6: The five `verify` commands in `cairn/PROFILE.md` exit 0 on the branch head.
- [ ] AC7: At a live look in the operator's session after a plugin reload, the operator sees ↻ at the right end of the pane's first line, and the id in the phase color with no phase word. The operator presses ↻ and sees `⋯` and then `↻`, or the work-log line says that the read was too short to see. The operator accepts the look, and the answer is a work-log line.

## Coverage

- AC1 → T1
- AC2 → T2, T6
- AC3 → T6
- AC4 → T3, T6
- AC5 → T4, T6
- AC6 → T5, T7
- AC7 → T8

## Tasks

- [x] T1: Count (AC1). Cut `COUNTS_QUERY`, `PrNodes`, `prNodes`, and `countPr` in `hooks/status/counts.ts` down to the threads. Remove `unanswered` from `countsText` in `pane.ts`, from `CairnPrRead`, and from the `counts.ts` header. Bump the `prs` shape tag in `register.tsx`. Capture the PR #245 reply into a fixture file and rewrite `counts.test.ts`.
- [x] T2: One ↻ Button (old AC2, wording before the T6 amendment). Add a first line to `paneLines` that carries `refresh`, and remove the heading Buttons and the `hotfixes` target. Draw the first row with `justifyContent="flex-end"` in the `ui.render` Pane hook. Set `REFRESH_LABEL` to `↻`. Update the pane tests.
- [x] T3: Reading state (old AC3). Add a `reading` atom with its own shape tag that `readPrs` sets at its start and clears when the newest read settles. Add a module-level press guard in `pressRefresh`. Draw the ↻ Button with `dimColor` from the atom. Add the six tests, driving the second press through a second mount (the held-press test near `pane.test.tsx:1974`).
- [x] T4: Docs (old AC4). README pane section, DESIGN `hooks/status/` entry, CHANGELOG `## Unreleased`.
- [x] T5: Run the five `verify` commands (old AC5).
- [ ] T6: Live-look amendment (AC2, AC3, AC4, AC5). Remove the `refresh` first line, and put the `refresh` Button on the first line `paneLines` gives, with its text Box at `flexGrow` 1. Drop the phase word from `milestoneLines`, and color the id with the phase. Swap the `dimColor` for the `⋯` label. Update the tests and the docs.
- [ ] T7: Run the five `verify` commands again (AC6).
- [ ] T8: Live look again (AC7).

## Work log

- 2026-10-10: created by /milestone-plan, from a `/hotfix` run that stopped at the tier check: the count followed the documented rule (`counts.ts` header, README "Bots count as other people"), so the change is a design change. PR #245's Copilot summary review, with no threads, counted as 1 unanswered.
- 2026-10-10: question set: what "unanswered" leaves out — drop the count, keep only unresolved threads.
- 2026-10-10: question set: ↻ placement — a new top row, right end.
- 2026-10-10: question set: reading state — dim ↻ (`dimColor`), not a "↻ reading…" label.
- 2026-10-10: question set: live look before the merge question — yes, in this session.
- 2026-10-10: plan gate chose dropping `unanswered` over leaving out bot reviews and empty reviews because the operator picked it; falsified by a session where a person's top-level comment or review summary goes unseen because the pane no longer counts it.
- 2026-10-10: plan gate chose a dim ↻ over a "↻ reading…" label because the operator picked it; falsified by the live look showing that the desktop app draws a `variant="secondary"` Button the same with and without `dimColor`.
- 2026-10-10: plan chose a module-level press guard beside a stored `reading` atom over a guard on the atom alone, because a reload resets module variables but keeps state, so a stored true blocks every press (audit finding 8); falsified by a test where a press after a reload runs no read.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned 11 findings on the draft, all taken toward narrower promises: deleted-author handling, zero cases after the anchor, an unedited PR #245 fixture, removal of the old bots-count lines, a drawn-tree Button check with the right-end layout, the reading state across overlapping reads and after a reload, the press guard covering all calls with a blocked URL, and `## Unreleased`. The operator's answers then removed the count rule (findings 1, 2, 4 become the AC1 removal and its grep) and changed the label to `dimColor`. AC1 and AC3 were rewritten after the answers and checked again against the audit's questions by the author, no new finding.
- 2026-10-10: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-10: collision: the "Pane edges (M222–M226 reviews)" row's items "With no hotfix PR and no blocked PR URL, the pane has no `Refresh`" and the counts-anchor items are absorbed (this milestone removes the anchor), and the row keeps the rest. M224 and M225 (done) shipped the Buttons and the count this milestone changes.
- 2026-10-10: implement started on m236-pane-one-refresh. Untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-10: T1 done. `counts.ts` reads only `reviewThreads`, `CairnPrRead.counts` is `{ unresolved }`, `prs` tag is `prs-3`. The PR #245 reply is stored in `hooks/status/fixtures/pr-245-threads.ts` as a string constant, because the mod tests import TypeScript, not JSON. `claude plugin test .` 1546 pass, the other four verify checks exit 0.
- 2026-10-10: T2 and T3 done in one checkpoint, since both rewrite the same Refresh tests. The first pane line has key `refresh`, no text, and `end: true`, which the render turns into `justifyContent="flex-end"`. `REFRESH_LABEL` is `↻`. A `reading` atom (`reading-1`, added to `types/index.d.ts`) is set at each `readPrs` start and cleared in its `finally` by the newest read only. A module-level `pressing` guards `pressRefresh`. The reload case is tested by a `state.get` hook that answers true until the mod writes the key. `claude plugin test .` 1556 pass, the other four verify checks exit 0.
- 2026-10-10: T4 done. The M225 CHANGELOG entry sits under `## Unreleased` and never shipped in a release, so it was rewritten in place to the thread count, and a new entry describes the ↻ Button. `git grep -n -i "refresh" -- README.md cairn/DESIGN.md` returns 17 lines, none of which puts a Button on a heading. `git grep -n -i "unanswered" -- hooks/status types README.md cairn/DESIGN.md` returns nothing.
- 2026-10-10: T5 done. All five verify commands exit 0 on the T4 head, `claude plugin test .` 1556 pass.
- 2026-10-10: claim audit: 46 claims read, 1 corrected — hooks/status/pane.test.tsx (the `gate()` helper comment named a `then` it does not have).
- 2026-10-10: T6 stop for the operator's live look. The plugin loads from `~/.claude/skills/cairn`, a symlink to this checkout, which is on the M236 branch, so a new session in `~/github/cairn` or a plugin reload here runs the branch's mod.
- 2026-10-10: T6 live look: the operator saw ↻ on its own row above the head line and no dim during a read, and said the look was wrong. They asked to put ↻ on the head line, shift the head line left, and drop the phase word, with the id in the phase color. The dim choice's falsifier fired: the desktop app drew no `dimColor` change.
- 2026-10-10: question at the T6 stop: reading look — the operator chose a `⋯` label during a read, over a "↻ reading…" label and over no reading state.
- 2026-10-10: substantive amendment: AC2 moves ↻ to the right end of the first line `paneLines` gives. New AC3 drops the phase word from head lines, which supersedes the phase word the operator picked at the M208 look. AC4 swaps `dimColor` for the `⋯` label, AC5 covers the new docs, and old AC5 and AC6 become AC6 and AC7. Goal and Scope follow. T6 to T8 are added, and the old T6 look becomes T8.
- 2026-10-10: re-audit: AC2 (full) — 9 findings across AC2 to AC7, all taken: the Button Box as the last child, `flexGrow` on the first line only, five test states, no dead gray status, the `⋯` layout check, an earlier-press wording, a `dim` grep, and a look that may be too short.
- 2026-10-10: re-audit: AC3 (full) — first reader: no unreachable status (finding 4 taken).
- 2026-10-10: re-audit: AC4 (full) — first reader: the `⋯` layout check (finding 5 taken).
- 2026-10-10: re-audit: AC5 (full) — first reader: `dim` grep and earlier-press wording (findings 6, 7 taken).
- 2026-10-10: re-audit: AC7 (full) — first reader: a read too short to see (finding 9 taken).
- 2026-10-10: re-audit: AC2 (full) — second reader: nothing.
- 2026-10-10: re-audit: AC3 (full) — second reader: nothing.
- 2026-10-10: re-audit: AC4 (full) — second reader: the reload exception, `$.fs.read` in the press count, and seven cases. The fixes went to the operator at the stop, and the operator accepted them.
- 2026-10-10: re-audit: AC5 (full) — second reader: the CHANGELOG entries were not named. The fix went to the operator at the stop, and the operator accepted it.
- 2026-10-10: re-audit: AC7 (full) — second reader: nothing.

## Decisions

## Review
