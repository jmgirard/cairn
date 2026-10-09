<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M226: The pane lists open hotfix PRs

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane is shipped plugin surface that every cairn operator sees   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m226-pane-hotfix-prs   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The cairn pane lists each open pull request that the operator opened from a `hotfix-*` branch, with its state word and counts.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A `/hotfix` run has no ROADMAP row. In guest mode its PR goes to
the maintainers, and the PR is the only record. So the pane, which lists
only `blocked` milestones (M223), shows nothing for an open hotfix PR. At
each pane open and each Refresh press, the mod reads the operator's open
PRs on the base remote with one `gh pr list` call. The pane draws the
`hotfix-*` ones in a Hotfixes section. Each line gets the state word
(M224) and the counts line (M225) that a blocked line gets, and no Button.

**Out:** No command resumes an open hotfix PR today. So a Button on a
hotfix line waits on the candidate row "`/hotfix` has no resume route for
an open PR". The `/milestone` status report of open hotfix PRs is
M227. PRs from other branches that the operator opened by hand stay out
(question set). The read's races stay in the "Pane PR-state edges (M224
review)" and "Pane count edges (M225 review)" candidate rows.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [x] AC1: In a repo whose base remote resolves, each pane open (the
      `/cairn-pane` command, the band's open button, and the session-start
      reopen) and each Refresh press runs exactly one `gh pr list --repo
      <base remote URL> --state open --author @me --limit 100 --json
      number,title,url,headRefName` call. The mod picks the base remote as
      `cairn_common.base_remote` does: `upstream` in guest mode when `git
      remote` lists it, else `origin`. Tests with a fake `$.process.run`
      match the `gh` argv in three cases: an owner-mode repo, a guest-mode
      repo with an `upstream` remote, and a guest-mode repo without one.
- [x] AC2: The pane draws a Hotfixes section after every other section
      except Candidates, and before Candidates. It has one line for each
      PR from that call whose head branch starts with `hotfix-`. The line
      shows the PR's `#<number>` and its title. A test's fake reply holds
      a `hotfix-*` PR, an `m226-*` PR, and a PR on another branch. The
      test draws only the `hotfix-*` line.
- [x] AC3: Each hotfix line shows the same state word and counts line
      that a blocked line shows for the same `gh pr view` and `gh api
      graphql` replies. No hotfix line carries a Button. A test covers an
      open PR with counts, a changes-requested PR, and a merged PR. It
      shows each word, the counts line, and no Button on any of the lines.
- [x] AC4: If the list call rejects, exits non-zero, or prints stdout
      that is not a JSON array, the pane keeps the hotfix lines of the
      last good read from the same repo root. A good read replaces the
      kept lines, an empty array included. The pane skips an array entry
      that has no string `headRefName`, no string `url`, or no number
      `number`. If `git remote get-url` fails for the base remote, the
      mod runs no list call and the pane draws no Hotfixes section. Tests
      cover seven cases: a rejected call, a non-zero exit, a malformed
      reply, an entry with a missing field, and an empty array. The other
      two are a kept read from another root and a repo with no remote. In each
      case, the pane's other lines are equal to `paneLines` of the same
      state with no hotfix read.
- [x] AC5: The Hotfixes heading carries a Refresh Button whose key
      differs from the Blocked heading's. A Refresh press on either
      heading runs the list call and the PR reads again, in a repo whose
      base remote resolves. One test presses each heading's Refresh and
      sees the list call run.
- [ ] AC6: A live look happens in a new desktop Code session in the
      parameters repo (`/Users/jmgirard/github/parameters`, guest mode).
      At the time of the look, one call prints the open PRs: `gh pr list
      --repo easystats/parameters --author @me --state open --limit 100`.
      The pane's Hotfixes section lists exactly the `hotfix-` PRs it prints. At
      least one such PR is open, and each line shows a word other than
      `unknown`.
- [x] AC7: README's cairn pane section and DESIGN.md's `hooks/status/`
      text describe the Hotfixes section. This repo's verify passes:
      `python3 -m unittest` over `scripts/tests` and `hooks/tests`,
      `claude plugin validate` on the plugin and marketplace manifests,
      and `claude plugin test`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T3
- AC4 → T2, T3
- AC5 → T3
- AC6 → T5
- AC7 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Probe the call through the mod's `$.process.run`. Make sure
      that `gh pr list --repo` takes an https and an ssh remote URL, and
      that `--author @me` works. The plan's audit ran both forms in a
      shell with gh 2.102.
- [x] T2: In `hooks/status/register.tsx`, add the base-remote read. It
      reads the collaboration mode from `cairn/PROFILE.md`. Then it runs
      `git remote` and `git remote get-url`. Add the list read. Add a
      `hotfixes` atom with its own shape tag that holds the root and the PRs. Join
      the hotfix URLs to `readPrs`, so they get words and counts. Tests
      for AC1 and AC4.
- [x] T3: In `hooks/status/pane.ts`, draw the Hotfixes heading with its
      count and its own Refresh key, and the lines with their words and
      counts and no Button. Bump the `pane` shape tag if the state's
      layout changes. Update `types/index.d.ts`. Tests for AC2, AC3, and
      AC5.
- [x] T4: Describe the section in README's cairn pane section and in the
      DESIGN.md `hooks/status/` text. Run verify.
- [x] T5: Prepare the live look in parameters. The look runs at the
      merge question in a new Code session there, because a desktop
      session keeps the mod it loaded at its start.
- [x] T6: Add the `CHANGELOG.md` Unreleased entry for the Hotfixes
      section (review return 1).

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

- 2026-10-09: created by /milestone-plan. The operator found the pane empty in parameters with five open hotfix PRs (#1261 to #1265).
- 2026-10-09: collision sweep: extends M223, M224, and M225. The Out Button waits on the candidate row "`/hotfix` has no resume route for an open PR". The Out races stay in the M224 and M225 edge rows. No D-entry collides. Inbox sweep: no open issues or PRs in this repo.
- 2026-10-09: plan gate chose a live `gh pr list` read over a record that `/hotfix` writes under `cairn/`, because the hotfix skill already says the PR is the record and a second record can go stale; falsified by a hotfix PR that `gh pr list --author @me` does not return, such as one opened under another account.
- 2026-10-09: criteria audit (full mode, fresh Opus reader): 7 findings, all fixed toward the narrower promise. AC1 names the open paths and skips the call with no remote. The call gains `--limit 100`. AC2 places the section before Candidates. AC3 adds a merged reply. AC4 names the non-zero exit, entries with missing fields, the root, and the baseline for "unchanged". AC5 gives each Refresh its own key and tests both. AC6 requires exactly the listed PRs, at least one, with no `unknown`. AC7 clean.
- 2026-10-09: question set: which PRs — `hotfix-*` only. Buttons — none on hotfix lines. `/milestone` report — include now, split to M227 because it ships alone. Live look — yes, in a new Code session in parameters at the merge question.
- 2026-10-09: T1: gh 2.102 in a shell took `--repo` as an https URL (`.git` suffix included) and an ssh URL, and `--author @me` gave the 5 parameters hotfix PRs. The mod's `$.process.run` running `gh` from the app's PATH is M224's T1 probe, so no new mod probe ran. In parameters, `origin` is `easystats/parameters` itself.
- 2026-10-09: T2 and T3 land in one commit, because the list read and the drawing share the new atom and tests. `readHotfixes` runs inside `readPrs` before the per-URL reads, and the list is written with the words, by the newest read only. `collaborationMode` in `reader.ts` mirrors `cairn_common.collaboration_mode`. The `pane` shape tag stays at 4, because the pane state did not change: the list sits in its own `hotfixes` atom (`hotfixes-1`). The hotfix heading's Refresh carries the target `hotfixes`, so its key is `cairn-pane-refresh-hotfixes`. The test fake `gh` now answers `git` and `gh pr list` calls apart, with no remote by default, so the M224 and M225 tests run unchanged.
- 2026-10-09: tests: 17 new cases for AC1 to AC5, and mod tests went to 1756. Four planted defects at once (no keep on a failed list, no root check at drawing, no `hotfix-` filter, guest mode ignored) turned 7 of them red, and the files were restored.
- 2026-10-09: T4: README's pane section gained a hotfix paragraph, and DESIGN.md's `hooks/status/` text gained the read and drawing and an M226 entry in its list. Verify green: 401 script tests, hooks suite, both validates, 1756 mod tests.
- 2026-10-09: T5: look prepared. `~/.claude/skills/cairn` links to this checkout, so a new desktop Code session in parameters loads the branch's mod while it is checked out. In parameters, `gh pr list --repo https://github.com/easystats/parameters.git --author @me --state open` shows 5 `hotfix-*` PRs (#1261 to #1265). The look runs at the merge question.
- 2026-10-09: claim audit: 60 claims read, 6 corrected — README.md, types/index.d.ts, hooks/status/register.tsx, hooks/status/pane.test.tsx. The same reader re-read the 6 and found them right.
- 2026-10-09: review return 1: consistency gate failed. `CHANGELOG.md` has no Unreleased entry for the pane's Hotfixes section, which the profile's consistency-gate slot requires. All other gate checks and the AC1 to AC5 and AC7 runs were green (1756 mod tests, 401 script tests, 174 hooks tests, both validates, cairn_validate).
- 2026-10-09: T6 added for review return 1 (minor amendment, no criterion changed). The CHANGELOG entry went under Unreleased, New, first. Its claims match README's hotfix paragraph, which the claim audit read against the code.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->

Pass 2, on dcfe338 after review return 1 (no CHANGELOG entry), 2026-10-09.

- AC1: `claude plugin test .`: 5 "M226 AC1" cases pass. They match the `gh pr list` argv for owner mode (`origin` with `upstream` present), guest mode with `upstream`, and guest mode without it. They show exactly one list call for `/cairn-pane`, the band's open button, and the session-start reopen, and none at a turn end. The Refresh press is in the AC5 case.
- AC2: the "M226 AC2" case passes. A reply with a `hotfix-*`, an `m226-*`, and a `feature-x` PR draws only `hotfix-1265`, after `blocked-head` and directly before `candidates-head-gap`.
- AC3: 2 "M226 AC3" cases pass. In review, changes requested, and merged words, the count line `2 unresolved threads · 1 unanswered`, and no Button on any hotfix line. The second case shows the hotfix count line equal to M111's blocked count line for the same replies.
- AC4: 8 "M226 AC4" cases pass: rejected call, non-zero exit with `[]`, non-JSON, non-array JSON, entries with missing fields, empty array, a kept read from another root, and no remote. Non-hotfix lines equal the no-read baseline in each. Plants at implement turned the keep and root cases red (work log).
- AC5: the "M226 AC5" case passes: Blocked heading key `cairn-pane-refresh`, Hotfixes heading key `cairn-pane-refresh-hotfixes`, and each press runs one more list call and one more `gh pr view` of the hotfix URL.
- AC6: pending. The live look in parameters runs at the merge question.
- AC7: README pane section (hotfix paragraph) and DESIGN.md `hooks/status/` text (M226 paragraph and list entry) describe the section. Verify on dcfe338: 401 script tests OK, 174 hooks tests OK, plugin validate passed with the usual CLAUDE.md warning, marketplace validate passed, 1756 mod tests pass, 0 fail.
- Gate: `cairn_validate` all checks passed. No principle changed, so `cairn_impact` is skipped. Marketplace validate shows no `plugins[N].version` warning. CHANGELOG has the Unreleased entry (T6).
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: no Refresh when the list is empty and no blocked row has a URL — follow-up, "Pane hotfix edges (M226 review)"
- diff-bug #2: the list read runs before the PR reads, up to about 45 s more wait — follow-up, same row
- diff-bug #3: a newer read settling between the two writes loses its list — fixed now (each write checks the newest read again), fixed 1fa492f
- diff-bug #4: the empty-URL path writes the list but not `prs` — reject, false: the `prs` value keeps M224's behavior on that path, and nothing draws a stale word from it
- diff-bug #5: the other-root test passes without the read's own root check — fixed now (asserts the old URL is not read again), fixed 1fa492f
- diff-bug #6: no parity test for `collaborationMode` — fixed now (9 cases against Python's results), fixed 1fa492f
- diff-bug #7: `prNumber`'s comment sat above `collaborationMode` — fixed now, fixed 1fa492f
- diff-bug #8: owner repo with only `upstream` shows no section — reject, false: README says no section when the base remote has no URL, and the rule matches `base_remote`
- diff-bug #9: a remote URL that `gh` cannot map shows no section, and a credential URL goes into the argv — follow-up, "Pane hotfix edges (M226 review)"
- diff-bug #10: a PR in both a blocked row and the list draws twice — follow-up, same row
- diff-bug #11: repeated entries give two lines one key — fixed now (`hotfixPrs` skips a repeated URL or number), fixed 1fa492f
- diff-bug #12: titles draw as GitHub gives them — follow-up, same row
- diff-bug #13: `blockedView` gives no Buttons for a missing line — reject, false: the AC3 test asserts each line's text first, so the lines exist
- diff-bug #14: the list call has a `cwd` and the view calls do not — reject, style
- diff-bug #15: a UNC root is untested for `git` — follow-up, same row
- diff-bug #16: shape tags are consistent — no finding
- diff-bug #17: docs match the code — no finding
- blame-history #1: the pre-read runs in series before the PR reads — follow-up, "Pane hotfix edges (M226 review)" (same as diff-bug #2)
- blame-history #2: the two writes can tear — fixed now with diff-bug #3, fixed 1fa492f
- blame-history #3: an in-process `/clear` leaves no Hotfixes Refresh — follow-up, same row
- blame-history #4: read-then-write with no version check — reject, false: only the newest read writes, and each write now checks it
- blame-history #5: misplaced `prNumber` comment — fixed now with diff-bug #7, fixed 1fa492f
- blame-history #6: the Refresh comments named only the Blocked heading — fixed now, fixed 1fa492f
- blame-history #7: README did not say the list stops at 100 — fixed now, fixed 1fa492f
- blame-history #8: the fake's default runs no list in the M224 and M225 tests — reject, false: the M226 AC3 cases run words and counts with a list call
- blame-history #9: a PR in both places draws twice — follow-up with diff-bug #10
- prior-review #1: open and reopen waits grow — follow-up with diff-bug #2
- prior-review #2: no race tests for the new list — follow-up, same row
- prior-review #3: `collaborationMode` has no parity test — fixed now with diff-bug #6, fixed 1fa492f
- prior-review #4: a PR in both places draws twice — follow-up with diff-bug #10
- prior-review #5: an in-process `/clear` loses the list — follow-up, same row
- prior-review #6: one contract type, aliased — no finding
- prior-review #7: a non-github.com PR gets a word but no counts — follow-up, same row
- Fix-now re-run on 1fa492f: 1765 mod tests pass, 0 fail. Planting the two defects again (no root check in the read, no repeated-entry skip) turned their 2 tests red.
