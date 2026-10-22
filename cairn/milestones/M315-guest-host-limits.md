# M315: Keep guest sessions within the host's limits

- **Status:** in-progress
- **Priority:** high
- **Depends on:** M314
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — guest sessions' PRs, thread resolves, bot replies, and issue closes on the host's GitHub
- **Branch/PR:** m315-guest-host-limits

## Goal

In a repo the operator does not own, cairn sessions keep the operator's open PRs under a cap and follow set rules for review threads, bot comments, and other people's issues.

## Scope

**In:** an open-PR cap, read from a `# Open PR cap: N` header line of `cairn/PROFILE.md` (default 2), checked by `/milestone-review` step 8 and `/hotfix` before a guest handoff opens a new PR. Four guest rules in the session-start text (`hooks/session_context.py`, with a cap reader in `hooks/cairn_common.py`) and in tracking-rules "Collaboration mode": the cap, no resolve of a thread a person started, no reply to a bot, and limits on closing another person's issue. README, CHANGELOG, DESIGN's header-line list, and a D-entry.

**Out:** the one-comment Copilot reply → M314. When the Copilot round runs: guest repos keep the opt-in line (the user's answer). A hook that blocks `gh pr create` or `gh issue close` by count: the rules are instructions to the session, and only the two handoffs check the cap. The cap at `/milestone-implement`'s branch cut: the handoff is where a PR opens.

## Acceptance criteria

- [ ] AC1: In guest mode, `/milestone-review` step 8 and `/hotfix` read the operator's open PRs on `<base-repo>` with `gh pr list --repo <base-repo> --author @me --state open --limit 100 --json number,url` before a handoff that would open a new PR: `/milestone-review` after step 8's push-access and stack-base reads and just before its push, when the header names no open PR, and `/hotfix` at step 1, for an authored fix, before it cuts a branch. When the list holds as many PRs as the cap or more, the skill pushes nothing, opens no PR, leaves any milestone status as it is, and stops with a close block that names the cap and each open PR. `/milestone-review`'s close block fences `/milestone-review M<NNN>`, labeled as rerunning the review up to the handoff. A failed read stops the same way, naming the read and its error in place of the open PRs. A push to an already-open PR reads no cap. The cap is N from a `# Open PR cap: N` line in the header of `cairn/PROFILE.md`, read as the `# Collaboration mode:` line is read, when N matches `[1-9][0-9]?`, and 2 otherwise, and the close block names a line it did not take.
- [ ] AC2: In guest mode, the session-start text that `hooks/session_context.py` injects states four rules. (1) Keep at most N of your open PRs on the host repo, N being AC1's cap, and name a `# Open PR cap:` line it did not take. (2) Never resolve a review thread that a person started. (3) Reply to no bot, except the one comment per Copilot review that the Copilot round or `/copilot-review` posts. (4) Close an issue someone else opened only when a merged change clearly fixes it or its fix belongs in another repo, with a one-line comment naming that change or repo, which holds over host style matching, and at most 3 such closes on that repo per UTC day, counting your closes there that day; when unsure, ask the user in chat and post nothing. A close the user picks at a cairn chip is the user's act and is outside rule (4). Cases in `hooks/tests` show the text reading "at most 4 of your open PRs" for a `# Open PR cap: 4` line; "at most 2 of your open PRs" for no line, for `many`, `0`, and `100` lines, and for the line placed below the first `## `; and no cap rule in owner mode with the line present.
- [ ] AC3: tracking-rules "Collaboration mode" states each of AC2's four rules, the cap given as AC1's rule. Its file-map row for `cairn/PROFILE.md` names the `# Open PR cap:` header line and `/milestone-review`, `/hotfix`, and `hooks/session_context.py` as its readers, and still says that no validator reads it.
- [ ] AC4: README's guest-mode section and `CHANGELOG.md`'s Unreleased section describe the open-PR cap and its header line, that `/milestone-review` and `/hotfix` stop at the cap before opening a PR, and the three rules on threads, bots, and issues as instructions each guest session is given. README's Copilot bullet says that in guest mode, with the round on, the session requests the review from your account when the PR has none yet.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3

## Tasks

- [x] T1: Add the cap read to `/milestone-review` step 8's guest arm (after the push-access and stack-base reads, before the push, only with no open PR in the header) and to `/hotfix` step 1's guest arm for an authored fix, with the close blocks of AC1.
- [x] T2: Add `open_pr_cap(root)` to `hooks/cairn_common.py` beside `push_remote` (one parser, `[1-9][0-9]?`, else 2, reporting a line it did not take), and the four rules to the guest part of `hooks/session_context.py`. Tests first in `hooks/tests`: the cases AC2 names, each asserting the rule's phrase.
- [x] T3: State the four rules in tracking-rules "Collaboration mode" and the header line in its file-map row; add the line to DESIGN's header-line list and the session hook's entry; update README's guest section and Copilot bullet and CHANGELOG Unreleased; write the D-entry (annotates D-137, D-152 for the guest request wording, and D-172). Its trigger is shipped behavior, the easystats audit, so D-108's door does not bar it.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — new guest-mode rules and a design decision.
- 2026-10-21: idea vet: none found. The cap and the rules come from the second easystats audit (the operator opened 175 of 199 org PRs, 38 open at once and up to 8 per repo; one maintainer thread resolved; "Fixed in <sha>" replies to a lint bot; 41 issues others opened were closed, 23 on one day, comments averaging 657 characters).
- 2026-10-21: collision check: D-137 (guest mode), D-152 (the Copilot opt-in, which stands), D-172 (push remote and its access read), D-207 (host style) bear; none bars this. Inbox sweep: 0 open issues, 1 open PR (#327, M312's), no overlap.
- 2026-10-21: question set: guest Copilot — keep the opt-in line (the round runs only with `# Copilot review: on`).
- 2026-10-21: question set: open-PR cap — 2 by default, changeable per repo with `# Open PR cap: N`; a push to an open PR is never blocked.
- 2026-10-21: question set: issue closes — the user's answer: when a merged change clearly fixes it or the solution belongs in another repo. The plan keeps the user's easystats stopgap terms around it: a one-line comment, at most 3 a day per repo, and ask the user when unsure.
- 2026-10-21: criteria audit (full mode, fresh Opus reader, first draft): the guest Copilot default, its permission gap and budget AC went with the user's answer; the cap read became new-PR-only with a named stop and rerun; a 1-99 value rule; the bot exception names `/copilot-review`; the issue rule asks the user in chat, not on GitHub; docs call the rules instructions; DESIGN's header list and the file map join T3.
- 2026-10-21: re-audit (full mode, fresh Opus reader, after the answers): taken — the read sits after the push-access and stack-base reads; `/hotfix` reads at step 1 so a capped fix leaves no branch; a failed read names its error; the parse matches `[1-9][0-9]?` read as the collaboration-mode line, and an untaken line is named; a chip-picked close is outside rule (4); the one-line comment holds over host style; the day is UTC, counted from the session's own closes; the test cases vary the value, the line's place, and the mode, and assert the rule's phrase; Depends on M314, so the bot rule never contradicts the per-thread replies; the README billing claim is dropped for want of a source.
- 2026-10-21: plan gate chose instructions in the session-start text, with the cap checked only at the two handoffs, over a hook that blocks `gh pr create` or `gh issue close` by count, because a hook would need a network read on each matching call and the audit's PRs and closes came through sessions the injected text reaches; falsified by a guest repo where the operator's open PRs pass the cap, or a day's closes pass 3, after this ships.
- 2026-10-22: implement start: branch m315-guest-host-limits cut from main at 60cb84e3; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-22: choice: both skills cite the cap as tracking-rules "Collaboration mode" states it (T3 writes it there) rather than restating the parse rule; `/hotfix`'s stop fences `/hotfix` with the bug's description.
- 2026-10-22: T1 done: `/milestone-review` step 8's guest arm reads the cap after the stack-base read, before the push, only with no open PR in the header; `/hotfix` step 1 reads it for an authored fix before step 2 cuts a branch; verify green.
- 2026-10-22: choice: `open_pr_cap(root)` returns `(cap, untaken)`; `session_context.host_limits` appends the four rules to the one guest mode line, so M184's and M247's one-line tests stand unchanged.
- 2026-10-22: T2 done: 4 new tests in `hooks/tests` (the AC2 cases, each asserting the rule's phrase) failed first, pass now; a planted `[0-9]+` parser turned the `0` and `100` cases red; verify green (hooks 197 OK).
- 2026-10-22: minor amendment: DESIGN had no list of `PROFILE.md` header lines, so T3 wrote one sentence that lists all four, beside the `session_context` entry's guest note.
- 2026-10-22: T3 done: tracking-rules "Collaboration mode" gains the four-limits bullet and the file-map row the header line; README guest bullets, Copilot bullet, CHANGELOG Unreleased entry, D-213 written; cairn_validate and skills/tests green; verify green.
- 2026-10-22: claim audit: 28 claims read, 2 corrected — README.md, CHANGELOG.md (a cap line "cairn cannot read" is named only when it sits in the header with a bad value; corrections land in the amendment's rewrite of those lines).
- 2026-10-22: user decision at a chip, after requests relayed by the easystats session: split the cap into 3 bug-fix and 1 feature PR per repo in every mode, and add a guest issue-first rule, both in M315; datawizard's guest-merge case went to a candidate row. Amended criteria drafted; fresh Opus re-audit running before they are written here (checkpoint, amendment in progress).
