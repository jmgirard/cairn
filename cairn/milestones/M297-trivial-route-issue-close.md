<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M297: A trivial edit closes the issue of the row it deletes

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M296   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it adds a GitHub issue close to an adopter's trivial-tier route   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m297-trivial-route-issue-close https://github.com/jmgirard/cairn/pull/310   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In owner mode, when the trivial route deletes a candidate row whose short title ends with an issue number, the route closes that issue after its push, and the tier chip's option names the close before the user chooses.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/milestone-plan` step 1's trivial route (the candidate-row match, the trivial option's description, and the commit, push, and close block); one D-entry; README's trivial-edit row, a CHANGELOG Unreleased entry, and the hand-run guard in `skills/tests/test_plan_tier_check.py`. Absorbs the candidate row "Close the issue a trivial edit fixes" in full.

**Out:** an issue that a row names only in its detail, or in a form other than the title's `(#N)` or `(#N, #M)`: the title is the one form the rulebook fixes, so no row holds the rest. A narrowed row's issue stays open, since part of its work is left, and so does an issue that another kept row's title names. A number that names a pull request is left alone, since `gh issue view` reads a PR too. Guest mode closes no issue, since closing the maintainers' issue is their act. A comment on the closed issue is not posted; no row holds it.

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

- [x] AC1: `skills/milestone-plan/SKILL.md` step 1 states that in owner mode, for each matched row the edit deletes whose short title ends with `(#N)` or `(#N, #M)`, the plan reads each such number with `gh issue view <N> --repo <base-repo> --json state,url` before the chip. It states that the trivial option's description names as one the route will close each such number that it reads as `OPEN`, whose URL path holds `/issues/`, and that is in the `(#N)` or `(#N, #M)` ending no kept row's title, a kept row being a candidate row the edit narrows or leaves in place. It states that the description names each other such number as one the route leaves alone: one read as closed, one whose URL path holds `/pull/`, one it cannot read, and one in a kept row's title reference.
- [x] AC2: Step 1 states that the commit's one-line summary ends with the deleted rows' issue references, and that after the push succeeds the route runs `gh issue close <N> --repo <base-repo>` for each issue the description named for closing, then re-reads each one's state. It states that the close block names as closed each issue named for closing whose re-read reads `CLOSED`, and names each other one as left open with the close command's error, the re-read's state, or the failed re-read. It states that a failed or rejected push closes no issue.
- [x] AC3: Step 1 states that a narrowed row's issue stays open and that in guest mode no issue is closed. It states that when a narrowed row's title, or in guest mode a deleted row's title, ends with `(#N)` or `(#N, #M)`, the option description names that number as one the route leaves alone.
- [x] AC4: `cairn/DECISIONS.md` gains one entry whose heading names D-170 and D-162. It records that the tier chip's trivial option approves the issue close, with the rejected alternative of a `Fixes #N` keyword in the commit message and its falsifier, and it states whether D-108's door applies and why.
- [x] AC5: README's trivial-edit row and one new CHANGELOG `## Unreleased` → `### Changes that affect existing repos` entry state that the route closes the issue of a row it deletes, in owner mode, after naming the close in its option.
- [x] AC6: The profile's `verify` slot passes at the branch head, and so does the hand-run `python3 -m unittest discover -s skills/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T1, T3
- AC4 → T4
- AC5 → T5
- AC6 → T3, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: In `skills/milestone-plan/SKILL.md` step 1, add the issue-state read for deleted rows with an issue-ending title to the trivial-route checks, and add the named issues, the narrowed-row case, and the guest case to the trivial option's description.
- [x] T2: Extend the owner-mode commit sentence: the summary carries the issue references, and after a successful push each named issue is closed and re-read, with the close block naming each result. Trace each path the new step opens (push fails, push rejected, close fails, `gh` cannot run) to the outward write it reaches (LESSONS M172).
- [x] T3: Add a test to `skills/tests/test_plan_tier_check.py` pinning T1's and T2's sentences, each member pinned on its own. Show each new assertion red against the pre-change step 1 before trusting its green.
- [x] T4: Append the D-entry (next free id) per AC4.
- [x] T5: Edit README's trivial-edit row and add the CHANGELOG entry.
- [x] T6: Run the `verify` slot and the hand-run `skills/tests` from the repo root, each exit code checked.

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
- 2026-10-20: question set: which candidate work to plan — all four unparked rows (see M296's work log).
- 2026-10-20: plan gate chose an explicit `gh issue close` after the push over a `Fixes #N` keyword in the commit message, because the keyword closes the issue later on GitHub's side with no exit code the route can read; falsified by a `gh issue close` that reports success while the issue stays open.
- 2026-10-20: plan gate chose to close only the issues of rows the edit deletes over also closing a narrowed row's issue, because a narrowed row still holds work for that issue; falsified by a user who wants a narrowed row's issue closed at the chip.
- 2026-10-20: plan gate split this from M296 since both edit one paragraph of step 1; M297 depends on M296.
- 2026-10-20: criteria audit (full mode, one Opus reader over M296 to M298): 11 findings, all fixed. Here: AC2's close block now says which state counts as closed and covers a failed re-read; AC3 says when the description names a left-open issue; AC4 names D-108's door; AC5 names its CHANGELOG subsection.
- 2026-10-20: branch m297-trivial-route-issue-close cut from main at 8cf2fe66; untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-20: substantive amendment: AC1 reads `--json state,url` and closes only an `OPEN` number whose URL path holds `/issues/` and that no kept row's title reference holds, because `gh issue view 309 --repo jmgirard/cairn --json state,url` returned the merged PR #309 (an open PR reads `OPEN`); AC3 names a narrowed or guest row's number as left alone; Scope Out gains the kept-row and PR cases.
- 2026-10-20: re-audit: AC1 (full) — "ends its title with" fails for `(#N, #M)` and "no row" took milestone rows; both fixed; it also flagged AC3 calling a PR an issue, fixed in AC3.
- 2026-10-20: re-audit: AC1 (full) — AC3's "leaves open" against AC1's "leaves alone", fixed in AC3; AC2's summary can end with a PR or kept-row number, answered: a bare reference only links and closes nothing, AC2 kept; AC1's "is in the … ending no kept row's title" reads awkwardly, answered: it means no kept row's title reference holds the number, AC1 kept.
- 2026-10-20: re-audit: AC3 (full) — its "stays open" against "leaves alone" for a closed or PR number, answered: step 1 states both, "stays open" meaning the route does not close it, AC3 kept.
- 2026-10-20: T1-T3 done: step 1 gains an **Issue read** paragraph after the candidate-row match, three option sentences, and the commit/close sentences; T2 trace: a failed or rejected push reaches no close, a pre-chip read that fails or a `gh` that cannot run leaves the number alone so no close runs for it, a failed close or re-read is named in the close block; `test_trivial_route_closes_deleted_rows_issues` pins 20 phrases, each absent from main's step 1 (checked one by one) and present now; the M265 push pin split in two around the inserted sentence; verify 5/5 green, skills/tests OK.
- 2026-10-20: implementation choice: the step names a kept row (narrowed or left in place) once in the Issue read paragraph and reuses the term; the summary example is `(#12)`.
- 2026-10-20: T4 done: D-195 appended (annotates D-170 and D-162; rejects `Fixes #N` with its falsifier; D-108's door does not apply, since the close is a route step, not a conduct rule about verification or records).
- 2026-10-20: T5 done: README's trivial-edit row and a CHANGELOG Unreleased "Changes that affect existing repos" entry name the owner-mode issue close; long added sentences split for the simple-english hook, whose remaining hits are older text.
- 2026-10-20: T6 done: from the repo root, scripts/tests 0, hooks/tests 0, plugin validate 0, marketplace validate 0, plugin test 0, skills/tests 0; cairn_validate all checks passed.
- 2026-10-20: claim audit: 37 claims read, 0 corrected — CHANGELOG.md, README.md, skills/milestone-plan/SKILL.md, skills/tests/test_plan_tier_check.py
- 2026-10-20: implement done; status review. Open concern: the summary's references can include a PR or kept-row number (the second AC1 re-audit's AC2 point, answered, AC2 kept).

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

Evidence at head a4af303d, 2026-10-20, read by a whitespace-collapsed substring check of step 1 (`1. Confirm` to `2. **Investigate first.**`) and of the other named files.

- AC1: step 1's **Issue read (trivial route, owner mode)** paragraph states the owner-mode read `gh issue view <N> --repo <base-repo> --json state,url` before the chip for each deleted row ending `(#N)`/`(#N, #M)`, defines a kept row, the close set (`OPEN`, URL path `/issues/`, in no kept row's title reference), and the leave-alone set (closed, `/pull/`, failed read or no `gh`, kept-row reference); the option text names each number to close and each deleted row's number left alone with the reason — all 6 phrases present; `test_trivial_route_closes_deleted_rows_issues` OK.
- AC2: step 1 states the summary ends with the deleted rows' references, the `gh issue close <N> --repo <base-repo>` after a successful push for each number named for closing, the re-read with the same `gh issue view` call, the close block naming `CLOSED` re-reads as closed and each other as left open with the close error, re-read state, or failed re-read, and "A failed or rejected push closes no issue." — all 4 phrases present; the test's order assert puts the close after the `git push` command.
- AC3: step 1 states "A narrowed row's issue stays open … the route closes no narrowed row's number", "In guest mode no issue is closed and none is read", and that the option names a narrowed row's number, or in guest mode a deleted row's, as left alone — all 3 phrases present.
- AC4: `cairn/DECISIONS.md` D-195's heading names D-170 and D-162; its Decision says the trivial option's description names each close so selecting it approves the close; its Rejected section has the `Fixes #N` keyword with the falsifier "a `gh issue close` that reports success while the issue stays open"; it says D-108's door does not apply because the close is a route step, not a conduct rule about verification or records.
- AC5: README's trivial-edit row states that in owner mode the edit closes the open issue of a row it removes after the push, once its option names the close; CHANGELOG `## Unreleased` → `### Changes that affect existing repos` holds the entry "A direct edit closes the issue of the row it removes", owner mode, the option naming each issue before the choice.
- AC6: at a4af303d from the repo root, `scripts/tests` 0, `hooks/tests` 0, plugin validate 0, marketplace validate 0, `claude plugin test .` 0 (with `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`), hand-run `skills/tests` 0.

Consistency gate at a4af303d: `cairn_validate.py` all checks passed (exit 0); no principle changed, so `cairn_impact` skipped; profile gate: verify green (AC6), marketplace validate shows no `plugins[N].version` warning, CHANGELOG Unreleased holds this milestone's entry.

Copilot arm: PR #310 opened at review start, header commit pushed, state query `none`, request made (exit 0), re-query `pending`.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: a failed `git commit` still reaches the close, since a push with nothing new exits 0 — fix now
- diff-bug #2: a close that exits 0 with a failed re-read is reported as left open — fix now (the close block also says the close command succeeded; AC2's "left open … the failed re-read" stands)
- diff-bug #3: the summary's references reach GitHub as timeline cross-references the chip does not name — fix now (the option says the summary carries them)
- diff-bug #4: a kept row holding #N only in its detail does not protect #N — follow-up, row "Keep owed issues open on a trivial edit"
- diff-bug #5: an issue in an open milestone's `Resolves:` slot can be closed early — follow-up, same row
- diff-bug #6: the issue read's order against the five checks is unstated (a failed check can sit beside numbers named to close) — follow-up, same row
- diff-bug #7: a failed push's close block gives no close command for later — fix now
- diff-bug #8: the close passes no `--comment`, unlike `/hotfix` and `/milestone` — reject, planned change (Scope Out: no comment is posted)
- diff-bug #9: an issue closed by someone else between read and close is reported as closed — reject, false: the block reports the re-read state, which is `CLOSED`, and claims nothing about who closed it
- diff-bug #10: the test does not pin "and none is read" or "The read takes no issue body", and option phrases are pinned against the whole step — fix now
- diff-bug #11: README leaves out the closed and unreadable cases — reject, false: the row states nothing wrong and points at the option, which names each case
- blame-history #1: after a failed open-PR read the route can delete a PR-named row and now also close its issue — follow-up, same row
- blame-history #2: an issue a planned milestone still owes can be closed — follow-up, same row (diff-bug #5)
- blame-history #3: no `--comment` on the close — reject, planned change (diff-bug #8)
- blame-history #4: the split push pin no longer pins the close-block sentence's place after the failed-push sentence — fix now (order assert)
- blame-history #5: whether an unmatched row citing `(#N)` protects it — reject, false: a kept row is "a candidate row the edit narrows or leaves in place", which includes every unmatched row
- prior-review #1: chip phrases pinned against the whole step — fix now (diff-bug #10)
- prior-review #2: a mid-title `(#N)` is not read — reject, planned change (Scope Out: only the title-ending form)
- prior-review #3: narrowed against kept is an edit-time judgment — reject, planned change (D-170's delete-or-narrow judgment, unchanged)
- ripple #1: ROADMAP's "Close the issue a trivial edit fixes" row says the route has no issue-close step — reject, planned change: step 9's hygiene deletes the row at this merge
- ripple #2: the git model and CLAUDE.md say the chip approves a trivial-tier commit, not the issue close — reject, false: they name what may reach the default branch, which is still the commit alone; the close is approved in step 1 and D-195
- ripple #3: tracking-rules Intake does not list the trivial route as an issue exit — reject, false: Intake lists routes for an incoming issue, and this close follows a row, not an issue
- ripple #4: tracking-rules' trivial-tier sentence says only that the commit graduates rows — fix now (adds the owner-mode issue close)
- ripple #5 and #6: `/milestone` §3's "only on the user's selection" and `/milestone-review`'s "no other issue write … on the review path" — reject, false: each is scoped to its own path, as the lens notes
