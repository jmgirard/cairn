# M167: Outside merges reach the health audit

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Branch/PR:** m167-outside-merges-audit

## Goal

The `/milestone` health audit lists pull requests merged since the last hygiene stamp by anyone but the operator, shows which archived milestone summaries mention the files each one touched, and carries each to the triage chip for a disposition.

## Scope

**Surface tier:** user-facing — the deliverable is `/milestone` audit conduct every adopting repo runs.

**Door trigger (D-090/D-108, hosted per D-098):** a shipped-behavior defect — the inbox sweep (M73, M166) lists open PRs only, so nestedtune PR #30 (merged by topepo in the web UI, 2026-08-31) collapsed the pkgdown split nestedtune's M17 built and was noticed only by M35's review fan-out, never by the audit. Promoted from the ROADMAP candidate row at the user's request on 2026-09-02 with one outside merge on record (the row's condition read "a second time").

**In:** a §2 **Outside merges** bullet in `skills/milestone/SKILL.md` — enumerate merged PRs, keep those merged on or after the ROADMAP stamp date by a login other than the operator's, read each kept PR's file list and report which `cairn/milestones/archive/` summaries contain any of its paths as a literal string (an overlap hint, not a claim); §3 resolves each with an existing disposition; one README sentence in the contributions bullet; a live run against nestedtune.

**Out:** merges by the operator outside cairn (the operator's own web-UI merge is tracked by its milestone; the git-reconciliation bullet already catches the commit) → not planned; a revert or repair of what a merge undid → the `/hotfix` disposition at triage, never automatic; a script reading GitHub → none (D-043 chose skill conduct over `gh`; scripts read no GitHub); the tracking-rules Enforcement boundary paragraph → unchanged (the audit's skill owns the sweep; a rulebook edit would re-seed the mass baseline for no rule change); a prose guard → none (profile test-doctrine: none owed; gate choice); env-prefix blindness in the other guards → its standing candidate row; CHANGELOG → written at release by the release walk.

## Acceptance criteria

- [ ] AC1: `skills/milestone/SKILL.md` §2 carries an **Outside merges** bullet that enumerates pull requests with `gh pr list --state merged --limit 100 --json number,title,url,author,mergedBy,mergedAt` and keeps those whose `mergedAt` date is on or after the date on `cairn/ROADMAP.md`'s `Last hygiene check` line and whose `mergedBy` login differs from the login `gh api user --jq .login` returns (raising `--limit` when the oldest returned merge is newer than that date); when `gh` is missing, unauthenticated, the repo has no remote, or the read otherwise fails, the bullet names what failed and skips the read, never an audit `FAIL`.
- [ ] AC2: For each pull request AC1 keeps, the bullet reads its file list with `gh pr diff <N> --name-only` and lists the `cairn/milestones/archive/` summaries whose text contains any listed path as a literal string, reported as a possible-overlap hint and not as a claim the milestone touched the file, stating "none" when no summary matches; the bullet writes nothing to GitHub.
- [ ] AC3: §3 resolves each kept pull request with exactly one of the dispositions §3 already lists, drawn from candidate row, `/hotfix`, `/milestone-plan`, and leave (`close` stays issue-only), adding no disposition to that list; the proposed disposition shown for the item names the pull request number and the archive summaries AC2 matched.
- [ ] AC4: `README.md`'s contributions bullet states that the audit lists pull requests merged by others since the last hygiene stamp, that it only reads, and that each becomes a triage item.
- [ ] AC5: AC1's commands, run verbatim from the nestedtune checkout, keep PR #30 (`mergedBy` `topepo`) and no pull request whose `mergedBy` is `jmgirard` with the date set to `2026-08-01`, and keep nothing with the date set to `2026-09-01`; AC2's read on PR #30 lists nestedtune's M17 summary among its matches.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4

## Tasks

- [ ] T1: Write the §2 **Outside merges** bullet in `skills/milestone/SKILL.md` beside the "Untriaged inboxes" (line ~125) and "Orphaned issues" (line ~148) bullets: the enumeration and filters, the `--limit` clause, the per-PR `gh pr diff --name-only` read and archive literal-substring hint, the writes-nothing clause, and the failure clause. Then hand-run `python3 -m unittest discover -s skills/tests` and confirm no pinned-phrase locator broke (lesson M148: reword the new sentence, never a pinned one).
- [ ] T2: Extend §3 (line ~195, "The §2 inbox sweep resolves here") so outside-merge items resolve there with the existing four dispositions and the shown disposition names the PR number and matched archive summaries.
- [ ] T3: Add one sentence to README's "Contributions come in through you" bullet (line ~282) stating the three AC4 claims, written against the shipped bullet text (derived-claims rule).
- [ ] T4: Run AC1's commands and AC2's read from `/Users/jmgirard/github/nestedtune` with the dates `2026-08-01` and `2026-09-01`; summarize the kept list and the archive matches in one work-log line.

## Work log

- 2026-09-02: created by /milestone-plan.
- 2026-09-02: criteria audit ran in full mode (fresh [O] reader): 8 findings — the `--search "merged:>=…"` enumeration returned nothing under `--repo` (AC1/AC5 rewritten to a plain merged list filtered client-side, verified: date 2026-08-01 keeps #30 only, 2026-09-01 keeps none); AC5 gained the second-date axis; AC3 named `close` as issue-only (§3 lists five dispositions, not four); AC2 narrowed to a literal-substring overlap hint; AC1 gained the "or the read otherwise fails" clause; AC4's "derived wording" replaced by three checkable claims; the D-090/D-108 door trigger stated in Scope; AC5's instrument question and the guard question went to the gate.
- 2026-09-02: plan gate (all four recommendations taken): promote with one outside merge on record; show the archive overlap hint; keep the nestedtune run as AC5; no prose guard.
- 2026-09-02: plan gate chose client-side date and merger filtering over `gh pr list --search "merged:>=<date>"` because the search form returned an empty list when run with `--repo` and the plain list did not; falsified by a repo whose merges since the stamp exceed the `--limit` the bullet names without the raise clause catching it.
- 2026-09-02: plan gate chose reusing §3's existing dispositions over a new revert disposition because an undone shipped behavior is a user-visible regression and `/hotfix` already fits it; falsified by an outside merge none of the four dispositions can carry.
- 2026-09-02: plan gate chose the archive literal-substring hint over listing PRs alone because the row's stated gap was that the audit never re-reads what a merged diff undid; falsified by the hint's over-matching (paths that read as prose) misleading a triage in practice.

## Decisions

## Review
