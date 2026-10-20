<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M295: A candidate title's issue number stays part of the title

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — skill routing and triage behavior that operators of adopting repos rely on   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m295-candidate-title-references https://github.com/jmgirard/cairn/pull/308   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A candidate row's short title, which since M292 can end in an issue number and
which open pull requests name in `Candidate row:` lines, keeps routing its row
to the skill that fits it.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the two M292 review rows "Keep tier check for issue-titled rows" and
"Keep rows named by open PRs at triage". `/milestone-plan`'s tier check and
`/hotfix` step 1 read a `(#N)` or `(#N, #M)` inside a candidate title as part
of the title. `/cairn-triage` reads the open pull requests' `Candidate row:`
lines and keeps each row they name. A D-entry narrows D-162's issue rule. A
CHANGELOG entry states both changes.

**Out:**
- The trivial route's candidate-row match for a ✎ press, which passes the
  title without quotes while the match asks for a quoted title → candidate
  row "Match bare titles on the trivial route".
- Copilot arm edge (3), the ripple lens reading additions → stays in the
  "Copilot arm edges" row; not chosen at this plan's question set.
- Any change to the cairn pane's code: it already passes the title and reads
  `Candidate row:` lines.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: In `skills/milestone-plan/SKILL.md`'s step-1 tier check, a `(#N)`
      or `(#N, #M)` inside a `cairn/ROADMAP.md` candidate row's short title
      (tracking-rules "Candidate short title") that the request contains
      verbatim does not make the request name a GitHub issue, so the issue
      rule's skip does not apply on account of it and the check runs, judging
      from the row's text and the code it names, not from issue #N's body. A
      `#N`, an issue URL, or a PR reference outside that title still takes the
      issue rule and the guest pull-request rule.
- [ ] AC2: In `skills/hotfix/SKILL.md` step 1, where it names the
      PR-reference forms (`#N`, a PR URL, "adopt PR 12"), a `(#N)` or
      `(#N, #M)` inside a candidate row's short title that the argument quotes
      verbatim is part of that title and not a PR reference, so an argument
      whose only `#N` sits in such a title is walked as a bug report with the
      candidate-row match and is not read with `gh pr view`; the title's
      number still names the issue for step 6's `Fixes #N` body line.
- [ ] AC3: `skills/cairn-triage/SKILL.md`'s default pass reads the base
      repo's open pull requests once with `gh pr list --repo <base-repo>
      --state open --limit 100 --json number,body`, parses each body line as
      the cairn pane's `startedRows` does (a line opening with exactly
      `Candidate row: `, outside a fenced code block, names the trimmed short
      title after it), and, for each such line in the pull requests that read
      returns, makes the candidate row whose short title the line names
      `keep`, with that pull request's number in the reason; a priority or
      token change may still ride on it, and no other disposition is proposed
      for it.
- [ ] AC4: When that read fails or `gh` cannot run, the triage pass names the
      failure in its proposal table and marks each candidate row it proposes
      for any disposition other than `keep` as not checked against open pull
      requests.
- [ ] AC5: `CHANGELOG.md`'s Unreleased section carries an entry that states
      both changes: `/milestone-plan` and `/hotfix` read an issue number
      inside a quoted candidate title as part of the title, and
      `/cairn-triage` keeps a candidate row that an open pull request names.
- [ ] AC6: The profile's `verify` slot is clean: both gating
      `python3 -m unittest discover` suites (`scripts/tests`, `hooks/tests`)
      and the three `claude plugin` checks it lists.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T4
- AC2 → T2
- AC3 → T3, T7
- AC4 → T3, T7
- AC5 → T5
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Edit the issue rule in `skills/milestone-plan/SKILL.md` step 1
      (~lines 57-64) for AC1: the title-number sentence and the clause that
      the check judges from the row's text, not issue #N's body.
- [x] T2: Edit `skills/hotfix/SKILL.md` step 1 (~lines 33-36) for AC2. Read
      each `grep -n "PR.reference"` hit in the file and confirm that it relies
      on step 1's definition rather than spotting `#N` on its own.
- [x] T3: Edit `skills/cairn-triage/SKILL.md` for AC3 and AC4: the open-PR
      read beside the started-token reads (~lines 64-90), the `keep` rule
      beside the live-token rule (~lines 345-362), and the failed-read mark
      in the proposal table. Say in the skill that this marks rows rather
      than holding them at `keep`, unlike a failed `#<n>` token read, so the
      pass still runs when `gh` is down.
- [x] T4: Append the next D-entry to `cairn/DECISIONS.md`: it narrows D-162's
      issue rule for a title's `(#N)`, answers D-162's reason (an issue's text
      steering a direct edit; a bare `#N` reaching `/hotfix` as a PR), and
      annotates D-189's consequence that names this row.
- [x] T5: Add the CHANGELOG Unreleased entry (AC5). Grep `README.md`,
      `skills/`, and tracking-rules for the old phrasings ("names a GitHub
      issue", "names an issue", "PR reference", "retitle") and fix any
      statement the change made stale (LESSONS M112).
- [x] T6: Run the five `verify` commands from the repo root, checking each
      exit code. Hand-run `skills/tests` (non-gating, D-109) and compare its
      reds with main's (LESSONS M148: new prose near pinned slices).
- [x] T7: Review return 1: in `skills/cairn-triage/SKILL.md`, rank the
      PR-named keep with the live-token keep (~line 303) before §7 and every
      class; plan's hotfix-route summary carries no `#N`; `/hotfix`'s
      title-number sentence covers each number; a 100-PR list read says it
      may be cut; step 3's table spec names the failed-read notice.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: not run — work named at the question set.
- 2026-10-20: question set: which candidate to plan — both title fixes in one milestone; if the Copilot row were picked, part 3 only (not picked, so the row stays as it is).
- 2026-10-20: collision check: absorbed candidate rows "Keep tier check for issue-titled rows" and "Keep rows named by open PRs at triage" (M292 review); D-162's issue rule is narrowed, not overridden, by T4's D-entry; D-189's consequence names the first row; no standing rejection hit; no checker-regress shape.
- 2026-10-20: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-20: lessons harvested: M112/M249 (grep old phrasings, CHANGELOG task) into T5; M148 (hand-run skills/tests near pinned prose) and M56 (check each exit code) into T6.
- 2026-10-20: criteria audit (full mode, fresh Opus reader): 10 findings and 2 clean criteria (AC5, AC6), all taken. AC1 scoped to the issue rule only (the trivial-route match for a bare ✎ title went to a candidate row); AC1 and AC2 use the same `(#N)`/`(#N, #M)` form; AC1 judges from the row's text, not issue #N's body; AC1's no-op guest clause dropped; AC2 says "quotes" to match hotfix's row match and keeps `Fixes #N`; AC3 bounded to the PRs the read returns and parses lines as `startedRows`; AC4 marks every non-`keep` proposal; T3 names the mark-vs-keep difference from failed `#<n>` reads.
- 2026-10-20: plan gate chose editing the two skills over a rulebook sentence in "Candidate short title" because the skills hold the issue and PR-reference rules and a rulebook edit re-seeds three rulebook-mass pins; falsified by a third skill that reads a title's `(#N)` as an issue or PR.
- 2026-10-20: plan gate chose making a PR-named row `keep` over excluding it from `retitle` alone because `merge`, `drop`, `route`, and `compress` also remove or rewrite the title the line names, as the live-token rule already treats such rows; falsified by a needed disposition of a PR-named row that `keep` blocks.
- 2026-10-20: plan gate chose marking rows on a failed PR read over holding every row at `keep` because holding them all would stop the candidate pass whenever `gh` is down; falsified by a marked row being retitled or dropped at the gate while an open PR names it.
- 2026-10-20: implement started on m295-candidate-title-references, cut from origin/main at e4e9701b; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-20: T1 done: the plan skill's issue rule now reads a candidate title's `(#N)` as part of the title (step 1, after "the door that tiers an issue"); the simple-english PostToolUse hook flagged 194 file-wide STE hits that predate this edit, left as they are (out of scope; the added sentences carry none of the flagged kinds).
- 2026-10-20: T2 done: `/hotfix` step 1 reads a quoted candidate title's `(#N)` as part of the title and keeps it for `Fixes #N`; the 16 other `grep -n "PR.reference"` hits each say "PR-reference argument" or "the PR reference", the term step 1 defines, and none spots a bare `#N` on its own; same pre-existing hook hits, left.
- 2026-10-20: T3 done: `/cairn-triage` session start reads open PRs' `Candidate row:` lines with one `gh pr list`, parsed as `startedRows` parses them; step 2 keeps each PR-named row and, on a failed read, marks every non-`keep` proposal as unchecked; the read sits in Session start, not a numbered step, so the plan's "~lines 64-90" placement held and the cross-references say "session start" and "step 3's table".
- 2026-10-20: T4 done: D-191 appended (narrows D-162's issue rule; annotates D-189 and D-166; passes D-108's door on its retained trigger, the M292 review's shipped-behavior defects).
- 2026-10-20: T5 done: two Unreleased Fixes entries in CHANGELOG.md; README's candidate-title paragraph gains the triage keep and the ✎ press's issue-number sentence; sweep (`git grep` for "names a GitHub issue", "names an issue", "request that names", "tier check", "retitle" over README.md, docs, CHANGELOG.md, skills/shared) found only released CHANGELOG entries (history, left) and profile changelog-heading "retitle" uses (unrelated).
- 2026-10-20: T6 done: verify clean (scripts and hooks suites OK, both `claude plugin validate` exit 0, `claude plugin test` 2389 pass 0 fail); hand-run `skills/tests` 917 OK with no reds, so no comparison with main was needed.
- 2026-10-20: claim audit: 30 claims read, 4 corrected — CHANGELOG.md, skills/cairn-triage/SKILL.md (CHANGELOG: the pane counts only your own PRs, `/hotfix` and `/milestone-review` write the lines in owner mode, the failed-read mark covers non-`keep` rows; triage: an unclosed fence runs to the end of the body; also a sentence that triage reads every author's PRs, moved after the PR-named definition at the reader's wording note); the same reader re-read all corrections as true.
- 2026-10-20: implement complete; status set to review.
- 2026-10-20: review return 1: AC3 fails — `skills/cairn-triage/SKILL.md` ranks the PR-named keep after §7's options and the Title class, so a PR-named row in a §7 group can be proposed `promote`/`route`/`drop` and one with a bad title `retitle` (diff-bug #1, prior-review #1, ripple #1); rank it with the live-token keep. Fix-now items riding on the return: plan's hotfix-route summary carries no `#N` (diff-bug #2); hotfix "each number names its issue" (#3); a 100-PR list read says it may be cut (#4); step 3's table spec names the failed-read notice (#7).
- 2026-10-20: T7 added for review return 1 (minor amendment; Coverage AC3, AC4 → T3, T7) and done: the PR-named keep now sits beside the live-token keep before §7 and every class, the Title class included, and step 2's later sentence points back to it; plan's hotfix-route summary carries no `#N`; `/hotfix` says each number names its issue; a 100-PR read is noted as possibly cut, and step 3's table names a failed or cut open-PR read. Status set to review.

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

Pass 1 (2026-10-20), branch at 1b0a1d9 over origin/main e4e9701b (main had not moved). Copilot arm: PR #308 opened, header URL pushed, state query `none`, request exit 0, re-query `pending`.

- AC1 evidence: `skills/milestone-plan/SKILL.md:60-67` reads a `(#N)`/`(#N, #M)` inside a candidate short title the request contains verbatim as not naming an issue, says the request names that row and the check runs, judges from the row's text and the code, never issue #N's body, and keeps the issue and guest rules for a `#N`, issue URL, or PR reference outside the title. Met.
- AC2 evidence: `skills/hotfix/SKILL.md:36-42`, inside the PR-reference sentence of step 1: such a number in a quoted title is part of the title, an argument whose only `#N` sits there is a bug report with the candidate-row match and no `gh pr view`, and the number still names the issue for step 6's `Fixes #N`. Met.
- AC3 evidence: `skills/cairn-triage/SKILL.md:88-102` holds the one `gh pr list --repo <base-repo> --state open --limit 100 --json number,body` read and the `startedRows` parse (trailing `\r`, exact prefix, trim, blank rest, fence to next fence or end of body; matches `hooks/status/pane.ts:214-240`); `:381-383` makes a PR-named row `keep` with its PR number. NOT met: diff-bug #1 shows `:306-309` sends a finding-absorbing row to §7's options before the `:381` keep, so a PR-named row in a §7 group can be proposed `promote`, `route`, or `drop`. Box left unticked.
- AC4 evidence: `skills/cairn-triage/SKILL.md:384-387`: on a failed list read the table names the failure and each non-`keep` proposal's reason says it was not checked against open PRs; `:99-102` says the pass still runs. Met.
- AC5 evidence: `CHANGELOG.md:146-163`, under `## Unreleased` (line 3, before `## 2.1.0` at 173), Fixes: "A candidate title's issue number stays part of the title" (plan and `/hotfix`) and "`/cairn-triage` keeps a row that an open pull request names". Met.
- AC6 evidence: fresh run 2026-10-20: `scripts/tests` 428 OK (21 skipped) exit 0; `hooks/tests` 193 OK exit 0; `claude plugin validate` plugin.json exit 0, marketplace.json exit 0; `claude plugin test .` 2389 pass 0 fail exit 0. Met.
- Consistency gate: `cairn_validate.py` exit 0, all checks passed; no DESIGN principle changed, so `cairn_impact` skipped; the claude-plugin consistency-gate slot's checks are the verify commands above.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a PR-named row in a §7 group takes §7's options (`promote`, `route`, `drop`) before the step-2 keep at `cairn-triage/SKILL.md:381` — fix now, floor return (AC3 fails inside its domain); rank the PR-named keep with the live-token keep at `:303`.
- diff-bug #2: the plan's hotfix route opens with a one-line bug summary that can carry a `#N` outside the title, which `/hotfix` then reads as a PR — fix now (the summary carries no `#N`).
- diff-bug #3: "That number still names the issue" is singular while the rule covers `(#N, #M)` — fix now (each number names its issue).
- diff-bug #4: a list read that returns exactly 100 PRs may be cut and marks nothing — fix now (the table says the list may be cut).
- diff-bug #5: guest mode and third-party PR bodies can hold a row at `keep` — reject, planned change (the plan chose reading every author's PRs; over-keeping is the safe side).
- diff-bug #6: a non-`keep` disposition set at Amend after a failed read gets no mark, and Amend can retitle a PR-named row (same gap for live-token rows) — follow-up, new row "Guard PR-named rows on other skill paths".
- diff-bug #7: step 3's table spec lists the guest ref line but not the failed-read notice — fix now.
- diff-bug #8: a merge survivor's lineage clause could lengthen a PR-named row's short title when the row has no `: ` or ` — ` (pre-existing for live-token rows) — follow-up, "Guard PR-named rows on other skill paths".
- diff-bug #9: D-191's heading says it annotates D-166 but the body does not say what changes — reject, false (the Decision says triage keeps a PR-named row "as it keeps a row with a live started token", D-166's keep rule extended).
- diff-bug #10: an unquoted typed `/hotfix … (#100)` still reads `#100` as a PR — reject, planned change (AC2 says "quotes"; the audit chose it).
- diff-bug #11: lines over 80 columns and ragged wraps — reject, style.
- blame-history #1: the trivial-route match needs a quoted title, and D-170's Rejected section rests on "a pane press sends the quoted title", which is false — follow-up, absorbed into "Match bare titles on the trivial route" (D-170's premise added to its detail).
- blame-history #2: the trivial route's row match does not skip a row an open PR names, so a trivial commit can delete a row an open hotfix PR carries — follow-up, "Guard PR-named rows on other skill paths".
- blame-history #3: the PR-named keep overrides D-164's icon retitle, and D-191 does not annotate D-164 — reject, false (the live-token keep already precedes the icon retitle; D-164's rule for rows that are retitled is unchanged).
- blame-history #4: triage reads every author's PRs, wider than the pane — reject, planned change (documented in the skill).
- prior-review #1: a PR-named row with an icon, shared, or out-of-bounds title can still be proposed `retitle`, since the Title class runs before the step-2 keep — fix now, same fix as diff-bug #1 (the keep is ranked before every class).
- prior-review #2: running the check on a titled `(#N)` reverses M250's user choice — reject, planned change (D-191 narrows D-162 at the user's pick of this row).
- prior-review #3: a ✎-press `(#N)` request gets no trivial-route graduation — follow-up, already "Match bare titles on the trivial route".
- ripple #1: the retitle bullet and table row (`cairn-triage/SKILL.md:301`, `:343-347`) still make a PR-named row eligible; tracking-rules:275 and the M292 CHANGELOG entry state retitle with no PR-named exception — fix now for the skill (diff-bug #1's ranking); reject for tracking-rules and the CHANGELOG, false (they state the retitle edit's triggers and form, which still hold for rows that are retitled, as for live-token rows).
- ripple #2: `/milestone-review` writes `Candidate row:` lines only for rows it "graduates", not for narrowed rows — reject, false (records-hygiene §1: graduation is removing or narrowing).
- ripple #3: `milestone-plan/SKILL.md:155` "A request that names an issue writes `tier check: not run …`" — reject, false (a request whose only `(#N)` is in a candidate title does not name an issue under the new sentence, so the line stays correct).
- ripple #4: the trivial-route match still needs a quoted title — follow-up, already "Match bare titles on the trivial route".
- Pass 1 result: floor return on AC3 (diff-bug #1); fix-now items diff-bug #2, #3, #4, #7 and prior-review #1 ride on the return. Copilot still `pending`; the next pass's PR-conversation read handles it.
