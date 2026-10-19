# M286: The cairn pane opens with a repo summary card, wraps goals at its width, and takes a new look

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP3
- **Resolves:** —
- **Surface tier:** user-facing, because the cairn pane ships in the plugin to every adopting repo
- **Branch/PR:** m286-pane-card-look

## Goal

The cairn pane opens with a summary card of the repo's pull requests, issues, candidate rows, and milestones, wraps each milestone goal at the pane's width, and draws its headings, Next line, and pull-request rows in one look that the operator picks.

## Scope

**In:** goal reflow in `hooks/status/pane.ts`. The summary card's lines in `pane.ts`, its GitHub read and its git read in `register.tsx`, and a parser beside `counts.ts`. A new look for section headings, the milestone head line, the Next line, and the card. One layout for blocked-milestone lines and hotfix lines. README, DESIGN.md, CHANGELOG, and `types/index.d.ts`.

**Out:** the band above the prompt keeps its look. If the operator wants it to match, that is a new candidate row at the live look. A Button on the hotfix line stays the parked "Pane hotfix line Button" row. A timer or a turn-end refresh of the card's numbers is out, at the operator's choice at the question set.

## Acceptance criteria

- [ ] AC1: `paneLines` draws a milestone's goal with one wrapping line (`wraps: true`) per paragraph or list item, not one per line of the file. Within a paragraph, it trims each line of the Goal section that `reader.ts` returns and joins the lines with one space. A line whose trimmed text opens with `- `, `* `, or one or more digits and `. ` starts a new wrapping line. A line without such a marker joins the line above it, a list item included. One or more blank lines between paragraphs draw as one blank row. `pane.test.tsx` has three cases. Three lines broken by hand draw as one line with the three joined. Two paragraphs with two blank lines between them draw as two lines with one blank row between them. A list that mixes `- `, `* `, and `1. ` items, one of them with a continuation line, draws one line per item.
- [ ] AC2: While a ROADMAP is found, the pane's first lines are a summary card. The card shows the number of candidate rows at each level: high, normal, low, and parked. At each level it counts the rows of `state.candidates` that `startedRefs` does not mark, over the taken tokens, the shown hotfixes, and the started rows, whether or not a milestone is active. The card and the Candidates list share one filter function. With no active milestone, the sum of the four numbers equals the number of candidate lines drawn. The card also shows the planned count, `state.workable.length + state.waiting.length`, and the blocked count, `state.blocked.length`, archived rows included. The card's first line carries ↻, with ⌂ before it while `acts` is true, and it grows. `pane.test.tsx` asserts the card's lines whole, with no GitHub numbers stored (`?`) and no done count, for a fixture with rows at all four levels, one started row, and planned and blocked rows, with and without an active milestone.
- [ ] AC3: The card shows the number of open pull requests on the base remote's repo, from every author, and the number of open issues there. Both come from one `gh api graphql` call that names the owner and repo of the base remote that `baseRemoteUrl` picks. The call is made only from `readPrs`. A unit-tested parser reads the call's result. A reply with both counts as integers gives both numbers. A rejected call, a non-zero exit, text that is not JSON, a reply without one or both counts, or a count that is not an integer gives no numbers. A read that runs no call gives no numbers. A read runs no call when there is no repo root, no base remote URL, or a host other than github.com. If a read gives no numbers, the card keeps the last good numbers for the same repo root. While the store holds no good numbers for this repo root, each number draws as `?`. Tests cover the argv for `git@github.com:o/r.git`, `ssh://git@github.com/o/r`, and `https://user:tok@github.com/o/r`, and no call for a host other than github.com. The argv holds only `o` and `r` from the URL. The parser has a test for each failure shape.
- [ ] AC4: The card shows the number of milestones done since the latest release. The number is the count of files that `git diff --no-renames --diff-filter=A --name-only <tag> HEAD -- cairn/milestones/archive/` lists in the repo root. `<tag>` is the tag that `git describe --tags --abbrev=0 --match 'v*'` prints there. The two git calls run in `readPrs`, beside the GitHub call. The card leaves this number out in guest mode, when `git describe` fails or prints nothing, when the `git diff` call fails, and until the first read for this repo root settles. Unit tests over a pure function of the guest flag and the two calls' results cover a count, `git describe` failing, `git describe` printing nothing, a failed diff, and guest mode. An argv test shows `--no-renames` and the archive pathspec.
- [ ] AC5: Take a blocked milestone with a pull request and a hotfix pull request with the same state word and counts. Their two lines' lead, text, and tail spans are equal, except for the lead's identifier, the title, a PR number span, and the archived mark. Their count lines are equal, except for their keys. The blocked line keeps the Button that its word carries. `pane.test.tsx` asserts both lines whole for each `CairnPrWord` and for no read.
- [ ] AC6: The section headings, each milestone's head line, the Next line, and the card draw in the variant that the operator picks from browser prototypes at T1. `pane.test.tsx` asserts whole the spans of one heading of each form, one head line, the Next line, and the card. The forms are a plain heading (Goal), a count with a meter (Tasks), and a bare count (Blocked).
- [ ] AC7: README's cairn pane section, DESIGN.md's pane description, and an Unreleased CHANGELOG entry state the card, what it counts, when it reads, the goal wrapping, and the new look. `types/index.d.ts` declares the card's stored value type and any changed `CairnPaneState` field.
- [ ] AC8: The `verify` slot passes: both gating `unittest` suites, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test` for the status mod.

## Coverage

- AC1 → T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T7
- AC6 → T1, T6, T8
- AC7 → T4, T9
- AC8 → T10

## Tasks

- [x] T1: Build browser prototypes in the scratchpad, served with `python3 -m http.server` (LESSONS M201). Show two or three variants of the headings, the head line, the Next line, the card, and the shared pull-request row, dark and light, at 44 columns and wide. Stop for the operator's pick. Log the picked variant's spans for one heading of each form, the head line, the Next line, and the card.
- [x] T2: Goal reflow in `milestoneLines` (`pane.ts:442-448`), with the AC1 cases.
- [x] T3: Card lines in `pane.ts`: the shared candidate filter (from the `drawn` filter at `pane.ts:604-612`), the four level counts, and the planned and blocked counts. Move ↻ and ⌂ from `out[0]` (`pane.ts:491`) to the card's first line. Add the AC2 fixture, and add it to `EMPTY_FIXTURES` in `band.test.tsx` where it has nothing active or workable (LESSONS M193).
- [x] T4: GitHub read. Add the graphql argv (owner and repo parsed from the base remote URL) and the reply parser beside `counts.ts`. Add a stored atom with its own shape tag that holds the numbers and the root. Start the call in `readPrs` (`register.tsx:853`) beside `readHotfixes`. Declare the stored type in `types/index.d.ts`.
- [x] T5: Done-since-release read. Add the pure function over the two git results, and run the two git calls in `readPrs`. Guest mode is read as `baseRemoteUrl` reads it.
- [x] T6: Restyle the headings (`heading`, `counted`), the head line, the Next line, and the card to the pick, with the AC6 assertions.
- [x] T7: The shared blocked and hotfix row layout (`pane.ts:535-591`), with the AC5 cases.
- [ ] T8: Stop for a live look in a new Code session in this repo: docked at 44 columns and wide, dark and light (LESSONS M193, M201). Fix what the look finds, or record it as a candidate row.
- [ ] T9: README's cairn pane section, DESIGN.md's pane description, and the CHANGELOG entry.
- [ ] T10: Run the verify slot.

## Work log

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: milestone — new pane behavior (a card with new GitHub and git reads) and a new look, with design choices.
- 2026-10-18: collision check: D-167 (the pane hides started rows and rejected a hidden-row count), D-182 and D-184 (level order and the parked level). The card counts only drawn rows, so it agrees with D-167. No candidate row overlaps. "Pane content follow-ons" (decisions, lessons) and "Pane hotfix line Button" stay separate. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-18: question set: how the look is chosen — browser prototypes with a pick stop, then a live look in a new Code session before review.
- 2026-10-18: question set: card contents — open PRs, open issues, candidate rows per level, and planned, blocked, and done-since-release milestone counts.
- 2026-10-18: question set: card refresh — with the PR reads (pane open, ↻, `/clear`, `/resume`), no timer and no turn-end read.
- 2026-10-18: question set: "old titles" read as the section headings and milestone head lines, "command suggestions" as the Next line. The user did not correct this reading.
- 2026-10-18: plan gate chose one GraphQL call for both GitHub numbers over two `gh pr list` and `gh issue list` calls, because one call costs one round trip and returns `totalCount` with no page limit; falsified by a GitHub host whose GraphQL API differs from github.com's.
- 2026-10-18: plan gate chose to unwrap the goal in `pane.ts` over `reader.ts`, because the reader's goal string is held to the Python twin in `test_status_fixtures.py` and its stored shape would change; falsified by a second consumer of the goal that also needs it unwrapped.
- 2026-10-18: plan gate chose one milestone over a look milestone and a card milestone, because the card is part of the look and two milestones would need two prototype rounds and two live looks; 8 criteria and 10 tasks sit at the split tripwire.
- 2026-10-18: plan gate chose to count done milestones by archive files added since the newest `v*` tag over counting `review M<NNN>: done` commit subjects, because the archive move is the step every owner-mode review makes; falsified by a repo that archives outside review or tags releases another way.
- 2026-10-18: criteria audit (full) on the first draft: 15 findings, each fixed toward the narrower promise. AC1: the marker test is on trimmed text, and the cases vary the marker, the blank-line count, and a continuation line. AC2: it names the filter, the card and list share it, the sum compares to drawn lines, and ⌂ and ↻ are stated directly. AC3: one-count and non-integer replies, the no-call cases, the stored-value `?` rule, `readPrs` as the one caller, and four remote URL forms. AC5: the PR number span is excepted, and the no-read case is covered. AC6: the recording act moved to T1, and the test covers each heading form. AC7: it names the stored value type. AC8: no finding.
- 2026-10-18: criteria audit (full) re-run on AC2 and AC4 after the question set added milestone counts: 6 findings, each fixed. AC2 names the planned and blocked counts from `PaneState` and fixes the card test's GitHub and done values. AC4 adds `--no-renames` and the archive pathspec, the not-yet-read case, the guest flag as an input of the pure function, the empty `git describe` case, and an argv test. The other criteria: no finding. This amendment follows the plan commit 19e8ddc2, which landed before the re-audit returned.
- 2026-10-18: implement started on branch m286-pane-card-look, cut from main at 63324d1f. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-18: T1 prototypes: today's look (A) and three new looks (B bordered card, C stat tiles, D minimal), dark and light, 44 columns and wide, active and idle. The operator picked B at the pick stop.
- 2026-10-18: T1 picked spans (B). Card: a Box with a round border in `subtle`. Line 1 is `<n>` bold + ` PRs` gray + `   ` + `<n>` bold + ` issues` gray, then ⌂ ↻. Line 2 is `candidates ` gray, then each level's mark (as the list draws it) and its count, two spaces apart. Line 3 is gray `<p> planned · <b> blocked · <d> done since <tag>`. Heading: the label bold, a space, a `─` rule in `subtle` that takes the free room, then the tail. Tasks and Criteria tails are `<c>/<t> ` gray and a six-cell meter of `━` in the phase color and `─` in `subtle`. A bare count tail is the count in gray. Head line: the id bold in the phase color, two spaces, the title bold, and the percent in gray. Next: `→ ` and the command, both bold in the phase color, with no pill and no "Next" label. Items: a checked box is `✓` in `success` with gray text, an open box is `○` in gray. A PR row: a state mark in the word's color, the id bold (`fix` for a hotfix), the title, and a tail of `#<n>` gray and the word in its color.
- 2026-10-18: Text has no clip mode (`wrap` offers only truncate forms with an ellipsis), so the heading rule draws as a long `─` Text in a one-row Box with `overflow: hidden`. The live look (T8) checks that it clips with no ellipsis.
- 2026-10-18: T2 done: `goalBlocks` in `pane.ts` joins a paragraph's lines and keeps list items apart; three hand-written AC1 cases, and the fixture sweep compares to `goalBlocks`. Verify green, mod tests 2184 → 2187.
- 2026-10-18: T3–T7 landed as one checkpoint, because the restyle, the card, and the shared rows rewrite the same `paneLines` code and the same test expectations.
- 2026-10-18: T3: `drawnCandidates` is the one filter the list and the card share; `cardLines` draws three lines, and ⌂ ↻ moved from the first milestone's head line to the card's first line. The no-active line follows the card.
- 2026-10-18: T4: `hooks/status/repo.ts` holds `repoArgv` (scp-like, `ssh://`, and `http(s)://` github.com URLs; any other host gives no call) and `repoCounts`. The `repo` atom (shape `repo-1`) holds the numbers by root, and `types/index.d.ts` declares `CairnRepoRead`. `readPrs` looks up the root and base remote once (`baseOf`) for the hotfix list and the card, and a lookup that rejects writes neither.
- 2026-10-18: T5: `doneSince` and the two git calls run in `readRepo`; guest mode runs no git call. The test fake answers the card's calls in a `card` list apart from the calls older tests count.
- 2026-10-18: T6/T7: look B in `heading`, `counted`, the head line, the Next line, and `prLine`, which draws both blocked and hotfix lines. Old-look tests rewritten to look B; `headText` and `prText` write the expected text by hand.
- 2026-10-18: user override after the pick: the operator pointed at the desktop app's task list. A checked box is now a filled gray `●` and an open one a dotted gray `◌`, in place of look B's `✓` in success. Two spaces follow each item mark, and a blank row sits under the card, for more room. The operator also asked for the app's in-progress icon: the first open task of an `in-progress` milestone draws `⊙` in the text color, the nearest text glyph. Recorded in AC6's test as the picked look.
- 2026-10-18: T3–T7 verify green, mod tests 2187 → 2220 (new `repo.test.ts` and AC2–AC6 cases in `pane.test.tsx`).
