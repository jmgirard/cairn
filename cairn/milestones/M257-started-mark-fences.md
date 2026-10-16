<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M257: Started mark skips fenced lines

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane ships to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m257-started-mark-fences, https://github.com/jmgirard/cairn/pull/268   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A `Candidate row:` line quoted inside a fenced code block of a pull-request body no longer marks a candidate row, and README says where the mark comes from and when it goes.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `startedRows` in `hooks/status/pane.ts` skips lines inside a fence, any
fence line closing an open fence, the fence state starting closed in each
body. README's started-mark text. Tests in `hooks/status/pane.test.tsx`.

**Out:** guest pull requests, which carry no `Candidate row:` line by design (tracking-rules
"Collaboration mode"); lines written only at PR open, a retitle after it,
the 100-PR list cut, and CommonMark's same-character closing rule stay in
"Started mark edges (M252 review)".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [x] AC1: In one pull-request body, a `Candidate row: <title>` line between
      a fence line and the next fence line marks no row, where a fence line
      starts with three backticks or three tildes after optional spaces and
      any fence line closes an open fence; the fence state starts closed in
      each body. Shown by `startedRows` cases in `hooks/status/pane.test.tsx`:
      a backtick fence, a tilde fence, and a fence after leading spaces,
      each with one line inside and one after, give only the second title; a
      body whose fence never closes gives no title after its opening line;
      and a second body after that one still gives its title.
- [ ] AC2: README's started-mark text says that only owner-mode `/hotfix`
      and `/milestone-review` write the `Candidate row:` line, that any of
      your open pull requests whose body has one marks the row, and that a
      row's mark goes at the pane's first pull-request read after the merge,
      so the row shows no mark until `/milestone-review`'s hygiene commit or
      `/hotfix`'s step 7 removes or narrows it.
- [x] AC3: The active profile's `verify` passes: `python3 -m unittest` for
      `scripts/tests` and `hooks/tests` from the repo root, `claude plugin
      validate` on the plugin and marketplace manifests, and `claude plugin
      test` for the status mod.

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

- [x] T1: Tests first: the AC1 `startedRows` cases beside M252's
      (pane.test.tsx ~3870), red. Then a per-body fence flag in
      `startedRows` (pane.ts ~194). Run `verify`.
- [x] T2: README's started-mark text (~441-458) per AC2.
- [x] T3: CHANGELOG entry; run `verify`.

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

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: not run — work named at the question set.
- 2026-10-15: question set: which pane work — "Button press reliability", "Pane read and draw edges", "Started mark edges", planned as M255, M256, M257 in that order; live look — tests are enough, no live look owed.
- 2026-10-15: collision check: candidate rows only; no D-entry covers the pane; inbox sweep 0 open issues, 0 open PRs. The rows stay until this milestone's hygiene narrows them (records-hygiene §1).
- 2026-10-15: criteria audit (full, Opus fresh reader, one reader for M255-M257, with throwaway probe tests in a scratch copy) — 8 findings, all taken: see the per-milestone line below.
- 2026-10-15: audit findings for M257: AC1 pins the closing rule (any fence line) and a per-body reset, with a case table over both fence characters, leading spaces, an unclosed fence, and the next body; AC2 reworded so README makes no false claim (a hand-written line also marks; the mark goes at the next read after a merge; `/hotfix` narrows at step 7).
- 2026-10-15: plan chose "any fence line closes" over CommonMark's same-character rule because a stray `Candidate row:` line costs one wrong mark and the simple toggle is one line; falsified by a real PR body whose mixed fences mark or hide a row wrongly.
- 2026-10-15: implement started on branch m257-started-mark-fences; untracked `cairn-probe.log` left unstaged, not this milestone's.
- 2026-10-15: T1 done: two `startedRows` tests (backtick, tilde, and spaced fences; an unclosed fence then a second body) ran red with the fenced titles returned, then a per-body `fenced` toggle on a module-private `FENCE_LINE` (`/^ *(```|~~~)/`, any number of leading spaces as AC1's "optional spaces" reads) made them green; verify 5/5 green (plugin test 1740 pass).
- 2026-10-15: T2 done: README's started-mark paragraph now says no other skill and no guest run writes the line (grep of `skills/` finds it only in hotfix and milestone-review), that any of your open PRs with the line marks the row, hand-written included, that a fenced line does not count, and that the mark goes at the first PR read after the merge until review's hygiene or hotfix step 7 edits the row (read from both skills' text this session). The simple-english hook's 212 README hits predate the branch outside these lines; left as is.
- 2026-10-15: T3 done: the started mark is unreleased, so its existing `### New` CHANGELOG entry gains the fenced-line sentences (enforced by T1's tests) in place of a separate entry; verify 5/5 green (scripts 408 OK, hooks 175 OK, both validates pass with no version warning, plugin test 1740 pass), `cairn_validate` all checks passed.
- 2026-10-15: claim audit: 16 claims read, 3 corrected — CHANGELOG.md, README.md (fence definition missed leading spaces; "a PR opens only after you approve the merge" missed the hotfix re-land path, now names milestone-review and an authored hotfix; "shows no mark" was wrong, the row shows its priority mark again); the same Opus reader re-read the three, all true.
- 2026-10-15: AC2's "the row shows no mark" read as no `◐` mark: the README now says the row shows its priority mark again with no PR number, which the claim audit found true against pane.ts; the deliverable is unchanged, so no amendment.
- 2026-10-15: all tasks done; verify 5/5 green on the claim-audit head (plugin test 1740 pass); status → review.
- 2026-10-15: review opened PR #268 at its start and requested Copilot (state was `none`); review pass 1 fixed 6 findings in b61a455d (verify green, 1741 pass), sent 4 to a new fence-edges candidate row at hygiene, rejected 7.
- 2026-10-15: amendment routed: AC2 — diff-bug #1: AC2 asks README to say the row "shows no mark" after the merge, but pane.ts draws the priority mark again once no open PR names the row, so the README states the true behavior and the criterion's wording is false of the code; status → in-progress for the AC2 amendment alone.


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

Pass 1 (2026-10-15, head b61a455d, PR #268 opened at review start for the Copilot round):

- AC1: `claude plugin test .` at b61a455d, 1741 pass, 0 fail. The `startedRows` cases pass: backtick, tilde, and spaced fences each give only the after-fence title; an unclosed fence gives no title after its opening line while the next body still gives its title; and (added this pass) a backtick fence closed by tildes and the reverse give only the after-fence title. The first two tests ran red at implement with the fenced titles returned (T1 work-log line).
- AC2: not verified. The README says the row shows its priority mark again after the merge, which pane.ts (`STARTED_MARK` replaces `PRIORITY_MARK` only while a PR names the row) shows to be true; AC2 as written asks README to say the row "shows no mark", which is false of the code. The criterion is wrong, so it is routed for amendment (work log).
- AC3: at b61a455d, `scripts/tests` 408 OK (21 skipped), `hooks/tests` 175 OK, `claude plugin validate` on plugin.json and marketplace.json both exit 0 with no version warning, `claude plugin test .` 1741 pass.
- consistency gate: `cairn_validate` all checks passed (exit 0); verify green at b61a455d; marketplace validate shows no `plugins[N].version` warning; CHANGELOG's unreleased started-mark entry carries the fenced-line rule.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: AC2 as written ("shows no mark") is not met by README, which correctly says the priority mark returns — amendment return (AC2 wording is false of the code).
- diff-bug #2: new fence sentences made "such a line" point at a fence line in README and CHANGELOG — fix now, fixed b61a455d.
- diff-bug #3: no test pins "any fence line closes" with mixed characters — fix now, fixed b61a455d.
- diff-bug #4: a four-backtick fence holding a three-backtick line closes early, so a quoted line inside marks a row — follow-up, to the new "Fence edges (M257 review)" candidate row at hygiene.
- diff-bug #5: four or more leading spaces still count as a fence line, unlike Markdown's indented code — follow-up, same row (AC1's "optional spaces" chose it).
- diff-bug #6: a fence opened after a list marker is missed, so its indented close opens a fence — follow-up, same row.
- diff-bug #7: README said `◐` goes at the first read after the merge even when another open PR names the row — fix now, fixed b61a455d.
- diff-bug #8: README's "keeps that look until hygiene or step 7" did not hold for a hand-written line on a PR no cairn skill merges — fix now, fixed b61a455d (scoped to a `/milestone-review` or `/hotfix` merge).
- diff-bug #9: README's "a PR opened before this change" read as the fence change — fix now, fixed b61a455d.
- diff-bug #10: the "Started mark edges (M252 review)" row still says a fenced line counts — reject, planned change: the hygiene commit narrows it (records-hygiene §1, work log).
- diff-bug #11: overlong unwrapped lines in README and CHANGELOG — reject, style; the #2 fix rewrapped them.
- blame-history #1: DESIGN.md's `startedRows` description omits fence skipping — fix now, fixed b61a455d.
- blame-history #2: the ROADMAP row still says a fenced line counts — reject, planned change (as diff-bug #10).
- blame-history #3: the CHANGELOG sentence was folded into M252's unreleased entry as one long line — reject, style; folding into the unreleased entry was T3's recorded choice, and the line was rewrapped.
- blame-history #4: inline triple-backtick spans at a line start and fences in blockquotes or list items toggle wrongly — follow-up, to "Fence edges (M257 review)".
- blame-history #5: README's rewritten Copilot sentence loses the contrast with the round on — reject, false: the sentence keeps its "Without the opt-in Copilot round (below)" opening.
- blame-history #6: README adds claims beyond the fence fix (writers, hand-written lines) and wraps unevenly — reject, planned change (AC2 asks for them) and style.
- prior-review: no prior-review evidence; M252's archived Review parks the fence edge in the row this milestone narrows.
