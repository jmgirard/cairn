<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M227: The status report lists open hotfix PRs

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — `/milestone` is a shipped skill that every cairn operator runs   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m227-status-hotfix-prs   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The `/milestone` health audit reports each open pull request that the operator opened from a `hotfix-*` branch.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Today `/milestone` §2 drops `hotfix-*` PRs from its inbox list,
because they are cairn's own work. But no other bullet reports them, so a
handed-off hotfix PR is invisible in the status report. The
`skills/milestone/SKILL.md` text at line 174 says such a PR is "already
reported two bullets up", which is not true for a hotfix PR. A new §2
bullet reads the open hotfix PRs with one `gh pr list` call and reports
each one. The `/hotfix` handoff text that says `/milestone` "reports
nothing for it" changes to match.

**Out:** A route for an open hotfix PR, such as a resume command, is not
in this milestone. It waits on the candidate row "`/hotfix` has no resume
route for an open PR". The
pane's Hotfixes section is M226. Comment counts stay in the pane (M225),
so the report names the review decision only.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: `skills/milestone/SKILL.md` §2 has an "Open hotfix PRs"
      bullet, in owner and guest mode. It runs one `gh pr list --repo
      <base-repo> --state open --author @me --limit 100 --json
      number,title,url,headRefName,reviewDecision` call. It keeps the PRs
      whose head branch starts with `hotfix-`. It reports each one's
      number, title, and review decision, with an empty decision shown as
      `none`. It carries no disposition to §3, names no next command, and
      writes nothing to GitHub. If the call returns 100 PRs, the report
      says that the list can be cut. The read fails if `gh` is missing or
      unauthenticated, if the repo has no remote, or for another cause.
      Then the bullet names the cause and reports no PR.
- [ ] AC2: The §2 inbox bullet no longer says that a `hotfix-*` PR is
      "already reported two bullets up", and it points at the new bullet
      instead. The `/hotfix` guest handoff text in `skills/hotfix/SKILL.md`
      no longer says `/milestone` "reports nothing for it", and says that
      §2 reports the open PR. The phrase in `skills/hotfix/SKILL.md` wraps
      across a line break today. So the search joins each file's lines
      first: `tr -s ' \n' ' ' < <file> | grep -c '<phrase>'` prints 0 for
      each phrase, over `skills/milestone/SKILL.md` and
      `skills/hotfix/SKILL.md`. The same search before the change prints 1.
- [ ] AC3: The hand-run prose guards in `skills/tests` pass, and this
      repo's verify passes: `python3 -m unittest` over `scripts/tests` and
      `hooks/tests`, `claude plugin validate` on the plugin and marketplace
      manifests, and `claude plugin test`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write the "Open hotfix PRs" bullet in `skills/milestone/SKILL.md`
      §2, after the blocked-milestone PR bullets. It uses the rulebook's
      `<base-repo>` slug recipe.
- [x] T2: Change the §2 inbox bullet's "already reported" clause and the
      `/hotfix` guest handoff sentence (`skills/hotfix/SKILL.md:259`).
- [x] T3: Run the `skills/tests` prose guards and verify. Fix a guard
      that pins the old wording.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-09: created by /milestone-plan, split from M226's plan. The operator asked at the question set for the status report to list open hotfix PRs now. It ships apart from the pane, so it is its own milestone.
- 2026-10-09: question set: `/milestone` report of open hotfix PRs — include now. Live look — yes, in parameters.
- 2026-10-09: criteria audit (full mode, fresh Opus reader): 8 findings, 7 fixed. AC2's search joins lines, because one phrase wraps. AC1 shows an empty decision as `none`, notes a list cut at 100, adds other read failures, and says "no disposition, no next command". AC3 names the linked checkout on the branch and checks against a literal `easystats/parameters` call. T2 drops the README check that no criterion backs. Kept: AC3's need for an open hotfix PR, which holds today with 5. AC4 clean.
- 2026-10-09: implement started on branch `m227-status-hotfix-prs`, cut from the pushed main. The untracked `cairn-probe.log` and `tsconfig.json` belong to no task and stay unstaged.
- 2026-10-09: T1 done. The "Open hotfix PRs" bullet sits after the blocked-milestone PR bullet in `skills/milestone/SKILL.md` §2. Choice: it calls a failed read a reported gap, never an audit `FAIL`, the same as the inbox bullet. Verify green: scripts 401, hooks 174, plugin test 1765, both validates; prose guards 669.
- 2026-10-09: T2 done. The inbox bullet now says that the `review` and `blocked` bullets report a milestone PR and the "Open hotfix PRs" bullet reports a hotfix PR. The `/hotfix` guest handoff says that §2 reports the open PR. The joined-line search prints 0 for both phrases in both files, and it printed 1 before. Suites and prose guards green.
- 2026-10-09: T3 done. No prose guard pins the old wording. Exit 0 for each: prose guards, scripts, hooks, plugin and marketplace validate, plugin test (1765 pass), and `cairn_validate`.
- 2026-10-09: T4 stopped before the run. `gh pr list --repo easystats/parameters --author @me --state open --limit 100` prints no PR, because #1261 to #1265 merged after the plan. `gh search prs --author @me --state open` finds no `hotfix-` head branch in any repo. AC3's setup does not hold, so the user picks how AC3 changes.
- 2026-10-09: substantive amendment: at the stop the user chose "Drop the live look". AC3 (the `/milestone` run in parameters) and T4 come out, and the old AC4 is now AC3 with its wording unchanged, mapped to T3. No criterion wording changed, so no re-audit ran. A candidate row holds the live look.
