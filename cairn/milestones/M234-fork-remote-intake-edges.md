# M234: Guest pushes find the fork, and intake commands work in any remote layout or shell

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP3
- **Resolves:** —
- **Surface tier:** user-facing — adopters run this skill prose for guest pushes, the `/milestone` audit, and the reply hand-off
- **Branch/PR:** m234-fork-remote-intake-edges

## Goal

Close five issue-intake and guest-mode edges from the M232 and M233 reviews, so that cairn's commands reach the right remote and repo in any shell or locale.

## Scope

**In:** A guest-mode fork remote `<fork>`, found by its parent repository, that every guest push and `<fork-owner>` use. `--repo <base-repo>` on every `gh pr` and `gh issue` command in `/milestone`. The rulebook's Intake paragraph names `close`. The reply hand-off passes the reply as a file, not as a quoted argument. The rulebook-mass line counts bytes.

**Out:** The candidate row "Issue look-in edges (M232 review)" keeps two items that the user left out at the plan gate: `/hotfix`'s `issue <URL>` argument form, and closing an orphaned issue from the look-in. In guest mode, `/milestone` §2's orphan bullet still runs, so §3's `close` can offer to close an upstream issue. That row now holds this item too. `gh` reads in other skills keep their current `--repo` coverage, because M185 swept the guest arms.

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md`'s canonical recipe defines the guest-mode fork remote `<fork>`. It is the one remote that `git remote` lists, other than `<base>`, whose parent equals `<base-repo>` ignoring case. The parent is read with `gh repo view "$(git remote get-url <remote>)" --json parent -q '.parent.owner.login + "/" + .parent.name'`. A remote whose read fails is not a match. `<fork-owner>` reads `<fork>`'s owner. With no match, or more than one, a guest push stops before the push and names the remotes it read. In `~/github/insight`, `~/github/brms`, and `~/github/parameters`, the recipe's commands resolve `fork`, `origin`, and no match. A temporary clone given two remotes that are forks of its base reports two matches.
- [ ] AC2: A case-insensitive, whitespace-normalized search of `skills/**/*.md` (outside `skills/tests/`) and `README.md` for `push` or `the fork` gives a set of hits. Each hit that describes a guest-mode push names `<fork>`, and no hit calls `origin` the fork.
- [ ] AC3: In `skills/milestone/SKILL.md`, a whitespace-normalized scan finds every inline or fenced span that begins `gh pr ` or `gh issue ` and carries an argument or flag. Each such span also carries `--repo <base-repo>`. §2 states this rule for §2 and §3, as §4's "The repo." paragraph does for §4.
- [ ] AC4: The Intake paragraph of `skills/shared/tracking-rules.md` names `/milestone` §3's `close` disposition for an orphaned issue among the issue routes. The clause from "`leave` is legal only" to "genuinely new." matches its text at commit b369a63 after whitespace normalization.
- [ ] AC5: `/milestone` §4's reply hand-off writes the drafted reply to `cairn-reply-<owner>-<repo>-<N>.md` in the system temp directory (Python's `tempfile.gettempdir()`), outside the checkout. Its fenced command is `gh issue comment <N> --repo <base-repo> --body-file "<that file's absolute path>"`, so the reply text is not part of the command line. §4 no longer carries the `'\''` instruction or the four-backtick fence. The close block still gives the draft verbatim.
- [ ] AC6: The rulebook-mass line in `skills/milestone/SKILL.md` measures with `wc -l -c` and states its baseline in lines and bytes. The figures are the line and byte counts that `wc -l -c skills/shared/tracking-rules.md` prints at the branch head.
- [ ] AC7: The five checks of the `verify` slot in `cairn/PROFILE.md` pass.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks

- [x] T1: Write the `<fork>` recipe beside `<base-repo>` in `skills/shared/tracking-rules.md:226-233`, with the no-match and two-match stop. Make `<fork-owner>` read `<fork>`. Run the recipe in insight, brms, and parameters. Run it in a temporary clone of insight that has a second remote at the fork's URL. Log the four results in one work-log line.
- [x] T2: Change each guest push from `origin` to `<fork>` at `tracking-rules.md:324`, `hotfix/SKILL.md:273` and `:284`, `milestone-review/SKILL.md:604` and `:618`, `milestone-implement/SKILL.md:72`, `copilot-review.md:86`, and `milestone/SKILL.md:173`. Reword `hotfix/SKILL.md:28-29`, which assumes the fork layout. Run AC2's search and log the owner or guest disposition of each hit. Add a prose guard that pins `<fork>` at every guest push site (the whole list, M171 lesson). Make sure that it fails when one site is reverted.
- [x] T3: Add §2's `--repo` rule sentence. Add `--repo <base-repo>` at `milestone/SKILL.md:152` (as `gh pr checks <N> --repo <base-repo>`), `:156-158`, `:194-195`, `:218`, `:229`, `:239`, and `:310`. Add a prose guard that runs AC3's scan. Make sure that it fails on one planted bare span.
- [x] T4: Name `close` in the Intake paragraph (`tracking-rules.md:191-196`). Add a guard in `skills/tests/test_issue_triage.py`. Compare the `leave` clause with `git show b369a63:skills/shared/tracking-rules.md`.
- [x] T5: Rewrite §4's reply hand-off (`milestone/SKILL.md:450-465`) to use the temp file and the `--body-file` command. Add D-155's clause to the rulebook's guest bullet (`tracking-rules.md:310`). Re-pin `skills/tests/test_issue_look_in.py`, whose line 32 pins `--body '<reply>'`. Update the reply text in `README.md` near line 82.
- [ ] T6: After the last rulebook edit, change the rulebook-mass line to `wc -l -c` and bytes. Re-seed it together with the pins in `skills/tests/test_cost_audit_line.py` and `skills/tests/test_mutation_harness.py` (the M149 lesson names three sites). Correct the M149 lesson if it names chars.
- [ ] T7: Add CHANGELOG entries. Run the five `verify` checks and the hand-run `skills/tests` suite, and read each exit code.

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: question set: which candidate to plan: issue-intake edges. Which items: the core four plus PowerShell quoting. `/hotfix issue <URL>` and orphan close from the look-in stay on their row. The choice overrides the rows' "promote when one shows in a real session" condition. The fork layout already shows in 3 of 7 local guest checkouts (insight, correlation, glmmTMB keep the upstream at `origin`).
- 2026-10-10: collision check: absorbs 3 of 5 items of "Issue look-in edges (M232 review)" and both items of "Intake and audit-line edges (M233 review)". Extends archived M232 and M233. D-044 and D-154 stand, and the `leave` clause is unchanged. D-155 annotates D-137. Inbox: 0 open issues, 0 open PRs.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned 11 findings, all fixed in the wording above. The `parent` field has no `nameWithOwner`, so AC1 names the `-q` expression. A failed read is not a match, and AC1 gained a two-match probe. Four missed sites joined T2 (`milestone:173`, `hotfix:284`, `milestone-review:618`, `hotfix:28-29`). AC2's search now matches `push`, case-insensitive. `gh pr checks` with no argument rejects `--repo`, so AC3 covers spans with an argument or flag, fenced and wrapped spans included. AC4 compares the `leave` clause after whitespace normalization. AC5's temp file conflicted with D-137's text, so D-155 annotates it, and the file name carries owner and repo. AC6 names the counts that `wc` prints. AC7 dropped the guard suite, and the guard re-pins are tasks. The guest-mode orphan close went to the M232 row. No IP conflict.
- 2026-10-10: plan gate chose a fork remote found by its parent repository over a remote named `fork` or the operator's login. Remote names vary, and a login gives no remote to push to. Falsified by a guest checkout whose fork is a fork of a fork.
- 2026-10-10: plan gate chose a temp file with `--body-file` over one command per shell, a stdin heredoc, or a file under `cairn/` or the git directory. The first two stay shell-specific, and the last two write inside the repo or need a new ignore entry. Falsified by a platform whose temp path `gh` cannot read from a double-quoted argument.
- 2026-10-10: plan gate chose `wc -l -c` (bytes) over `LC_ALL=C wc -l -m`. Bytes do not change with the locale, and the prefix does not work in PowerShell. Falsified by a `wc` whose `-c` count changes with the locale.
- 2026-10-10: plan gate chose one §2 rule sentence plus per-site `--repo` over per-site edits alone (M185 lesson). Falsified by a later bare `gh` read in §2 that the guard misses.
- 2026-10-10: implement started on branch m234-fork-remote-intake-edges. The untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-10: T1: the `<fork>` recipe is in the rulebook's canonical recipe. Probe results: insight resolves `fork`, brms resolves `origin`, parameters has no match, and a scratch `git init` repo with remotes `origin` (easystats/insight), `fork`, and `fork2` (both jmgirard/insight) reports two matches. A remote whose read fails (jmgirard/no-such-repo-zz9) is not a match. The scratch repo stands in for a clone, because the recipe reads only `git remote`. Verify: 5 of 5 green.
- 2026-10-10: T2: 8 planned sites name `<fork>`, `hotfix:28-29` no longer assumes the layout, and AC2's search (142 hits in 30 files) found 3 more guest pushes that named no remote: the handoff chip example (`milestone-review:523`), the handoff's fix push (`milestone-review:620`), and the rulebook's "the push" back-reference. All 3 now name `<fork>`. Owner-mode pushes to `origin` stay: `hotfix:190`, `:235`, `milestone-review:112`, `:532`, `:585`, `milestone:473`. New guard `skills/tests/test_guest_fork_remote.py` (7 tests, EXEMPT entry added) pins the 5 recipe clauses and all 11 sites. Run against main it misses 11 of 11 sites and 5 of 5 clauses and finds the old "origin (the fork)" text. skills/tests 706 OK, verify 5 of 5 green.
- 2026-10-10: T3: §2 opens with a "The repo." rule for §2 and §3, and the 8 bare commands carry `--repo <base-repo>` (`gh pr checks` gained `<N>`, since gh refuses `--repo` without an argument). New guard `skills/tests/test_milestone_gh_repo.py` (6 tests, EXEMPT entry added) scans 15 commands in inline and fenced spans, indented fences included. On main it finds the 8 bare commands, and planted inline and fenced spans fail it. Re-pinned 5 older guards and 2 mutation blocks to the new text (`test_issue_triage`, `test_issue_linkage`, `test_resume_routing`). skills/tests OK, verify 5 of 5 green.
- 2026-10-10: T4: the Intake paragraph names "`close` (`/milestone` §3) for an orphaned issue whose closing milestone is done". The whitespace-normalized `leave` clause equals its b369a63 text. New class `TestIntakeNamesClose` in `test_issue_triage.py` fails with the rulebook change stashed. Re-pinned the M233 Intake guard in `test_external_pr_intake.py` and its mutation block. skills/tests OK, verify 5 of 5 green.
- 2026-10-10: T5: §4's reply hand-off writes the draft to `cairn-reply-<owner>-<repo>-<N>.md` in `tempfile.gettempdir()` and hands the user `gh issue comment <N> --repo <base-repo> --body-file "<path>"` in a `bash` fence. `gh issue comment --help` lists `-F, --body-file file`. The rulebook's guest bullet carries D-155's clause. A PowerShell claim was cut from the draft prose, because `pwsh` is not installed here to observe it (derived-claims rule). `test_issue_look_in.py` re-pinned the hand-off line and gained 4 tests. With the §4 change stashed, 3 of them fail. README's reply sentence updated. skills/tests OK, verify 5 of 5 green.

## Decisions

## Review
