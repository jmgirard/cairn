# M74: Issue triage — /milestone enumerates untriaged inboxes into candidate rows

**done** · PR https://github.com/jmgirard/cairn/pull/72 · merged 2026-07-18 · D-043's third deliverable

## Outcome

Replaced `/milestone`'s unenumerable "untriaged inboxes" bullet with a real sweep. §2
enumerates both inboxes (`gh issue list` / `gh pr list`), drops cairn's own in-flight PRs so
the list is genuinely an *inbox*, applies the search-first cross-check, and degrades cleanly
when `gh` is missing/unauthenticated/remote-less — reported, never an audit `FAIL`. §3 resolves
each item into one of four dispositions (candidate row / `/hotfix` / `/milestone-plan` / leave)
shown verbatim above the chip; external PRs route to M73's door, no second intake mechanism.
`DESIGN.md` + `README.md` stopped describing the pre-M73 `/hotfix` trigger (absorbed candidate,
M73 F5). Guard: `test_issue_triage.py` (20 tests) + 6 mutation entries.
Decisions: extended §3's existing triage option rather than adding a second chip (a second
forces rewording "ONE routing chip (AskUserQuestion)", asserted across seven skills); sweep
stays inside §2's judgment block, scripts stay offline; `leave` shipped though the rulebook's
Intake enumeration omits it → candidate row.

## Review

7/7 criteria fresh-verified; `cairn_validate` clean; scripts 96 / skills 287 / hooks 72. Fan-out
5 findings (blame 0; prior-PR 0, no evidence). Fixed F1/80 (own-PR filter — the audit re-reported
its own in-review PR), F3/92 (disposition guards asserted clauses without their labels; proven
false coverage, reproduced independently), F4/63. F2/30 rejected; F5/40 → candidate row.
