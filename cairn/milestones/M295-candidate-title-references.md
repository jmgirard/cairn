<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M295: A candidate title's issue number stays part of the title

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — skill routing and triage behavior that operators of adopting repos rely on   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m295-candidate-title-references   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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
- AC3 → T3
- AC4 → T3
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
- [ ] T4: Append the next D-entry to `cairn/DECISIONS.md`: it narrows D-162's
      issue rule for a title's `(#N)`, answers D-162's reason (an issue's text
      steering a direct edit; a bare `#N` reaching `/hotfix` as a PR), and
      annotates D-189's consequence that names this row.
- [ ] T5: Add the CHANGELOG Unreleased entry (AC5). Grep `README.md`,
      `skills/`, and tracking-rules for the old phrasings ("names a GitHub
      issue", "names an issue", "PR reference", "retitle") and fix any
      statement the change made stale (LESSONS M112).
- [ ] T6: Run the five `verify` commands from the repo root, checking each
      exit code. Hand-run `skills/tests` (non-gating, D-109) and compare its
      reds with main's (LESSONS M148: new prose near pinned slices).

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
