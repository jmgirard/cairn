<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M339: Write hotfix flaw rows at the guest handoff

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes what `/hotfix` writes to the ROADMAP of an adopting guest repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m339-guest-handoff-flaw-rows, https://github.com/jmgirard/cairn/pull/354   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A guest-mode `/hotfix` records each flaw its idea vet found in what the fix leaves as it was when it hands the PR to the maintainers, so the flaw is not lost while the PR waits for their merge.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `skills/hotfix/SKILL.md` step 6's guest handoff and step 1's guest change route record each such flaw on disk (a new candidate row tagged with the PR number, or an extension of a matching row). Step 7's guest arm, on the merged-PR re-entry, judges those rows against the merged diff. Step 1's idea-vet paragraph says so. The prose guard, README, CHANGELOG, and a D-entry that supersedes D-225's close-block-only rule for these two guest paths follow.

**Out:** an owner-mode `/hotfix` declined at the merge question, and a guest run that stops before its PR opens, keep naming the flaw only in the close block → parked candidate row "Keep hotfix flaws after a declined merge". The owner arm's resumed merge (step 1) is unchanged.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: In `skills/hotfix/SKILL.md`, once step 6's guest handoff `gh pr create` succeeds, and once step 1's guest change route makes its approved push to PR #<n>, the run records on disk with no commit each flaw that step 1's idea vet found in what the diff leaves as it was, sweeping first by tracking-rules' search-first rule. It records the flaw as one of three things. The first is a new Candidates row of `cairn/ROADMAP.md` that names the flaw as a design decision for later work and whose provenance reads `hotfix PR #<n> handoff`. The second is an existing row extended with `extended YYYY-MM-DD by hotfix PR #<n> handoff`, placed before any ` — started` token. The third, on a standing rejection, is a close-block line naming the flaw and the decision. The close block shows each row written or extended, verbatim. A guest handoff that opens no PR names each flaw in its close block, as on main.
- [x] AC2: In step 7's guest arm, when the merged-PR re-entry finds that the maintainers merged PR #<N> and its post-hoc verification is accepted, each Candidates row of `cairn/ROADMAP.md` that holds `hotfix PR #<N> handoff` is judged against the merged diff, and for an extended row only the part the handoff added is judged. That part is deleted when the diff covers it in full (a new row is deleted whole), narrowed with step 7's `narrowed` note when the diff covers it in part, and kept otherwise. Each deleted or narrowed row is shown verbatim in chat. A flaw that the re-entry's idea vet finds and such a row holds adds no new row. Any other re-entry outcome leaves these rows as they are.
- [x] AC3: On the branch, step 1's idea-vet paragraph and step 6's guest arm of `skills/hotfix/SKILL.md` each say that a guest handoff whose `gh pr create` succeeds records the flaw at the handoff, and `git grep -n -E "only by its started token|only appends its started token" -- skills/hotfix/SKILL.md` lists no line.
- [x] AC4: README.md's `| Fix a reported bug quickly |` table row and an entry in CHANGELOG.md each say that in guest mode the flaw's candidate row is written at the handoff to the maintainers, not after their merge. The CHANGELOG entry sits under a `## Unreleased` heading above `## 2.2.0`, in its "Changes that affect existing repos" subsection.
- [x] AC5: The `verify` slot of `cairn/PROFILE.md` passes on the branch, except for `claude plugin test` failures whose test names also fail on the branch's merge base with main, run with the same binary; and the hand-run `python3 -m unittest discover -s skills/tests -p "test_*.py"` passes.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T1, T3
- AC4 → T5
- AC5 → T4, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: Step 6's guest handoff (`skills/hotfix/SKILL.md` ~lines 628-686): after the create and the started-token append, record each flaw per AC1 and show the rows in the close block; keep the close-block naming when no PR opens. Reword "The handoff changes a matched candidate row only by its started token" (~line 682) so a matched row can also be extended.
- [x] T2: Step 1's guest change route (~lines 289-324): on the approved push, record the flaws per AC1 with that PR's number, and show them in its close block.
- [x] T3: Step 1's idea-vet paragraph (~lines 115-133): state the guest handoff and change-route exception to "A close block that ends the run before step 7 names the flaw instead". Step 7's guest arm (~lines 719-726): replace "the handoff only appends its started token" and add AC2's judgment of the tagged rows.
- [x] T4: Update `skills/tests/test_hotfix_candidate_graduation.py` (the guest-arm test pins the two sentences T1 and T3 change) to pin the new sentences, including one that the tagged rows are judged at the re-entry.
- [x] T5: README `/hotfix` row (README.md:809, "becomes a candidate row after the merge") and a CHANGELOG `## Unreleased` entry, per AC4.
- [x] T6: Append a D-entry superseding D-225's clause "A close block that ends the run before step 7 names the flaw instead" for a guest handoff that opens its PR and for the change route's approved push, naming the parked row for the owner decline. Run the `verify` slot and the hand-run `skills/tests`.

- [x] T7: Review return 1: apply the pass-1 fix-now findings listed in the Review section (extension limits, flaw text in the note, record after the Copilot round, change-route order, scope and PR number, step 7 opening, README, guard pins, D-248 heading).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-11-25: created by /milestone-plan, from a report by the easystats session: a guest `/hotfix` handoff (easystats/insight#1317) named two flaws it left alone, and neither reached insight's ROADMAP.
- 2026-11-25: tier check: milestone — the change supersedes D-225's user-chosen rule on when a hotfix flaw gets its row, a design decision.
- 2026-11-25: idea vet: one gap — a row the maintainers' own edits fix stays until a re-entry; reading taken: the re-entry judges tagged rows against the merged diff, and a row with no re-entry is left to `/cairn-triage`. No flaw.
- 2026-11-25: lessons used: 2026-10-29 (M324), 2026-07-24 (M112), 2026-08-17 (M148), 2026-07-16 (M56).
- 2026-11-25: collision check: D-225 (the flaw's row comes from step 7, a close block names it before then) is superseded for the two guest paths at the user's choice; D-240 (step 1 stop rows commit; switching branches rejected) stands and is why owner mode is out; D-108's door passes on its retained trigger, a defect in shipped behavior (flaws lost in insight). `milestone-review` and `milestone-implement` checked: both write follow-up rows before their handoff. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-11-25: criteria audit (full mode, fresh Opus reader) returned 17 findings, all taken: AC1 gained the standing-rejection case, the extended-row form and its place before the started token, the no-PR case, and the change route; AC2 gained the file, the extended-row part rule, and the other-outcome clause (a second re-entry re-judging a narrowed row is accepted); AC3 now names the two passages and a grep that must list nothing, and leaves the owner resumed-merge arm alone; AC4 names the Unreleased heading and subsection; AC5 adds the hand-run `skills/tests`.
- 2026-11-25: question set: write rows at the guest handoff — yes, recommended; owner-mode decline — left for later as a parked row, recommended.
- 2026-11-25: plan gate chose writing at the handoff over writing at step 1's vet, because the diff can still change before the handoff (address-first fixes, the snapshot rule); falsified by a guest run that stops between the vet and the handoff and loses a flaw a user needed.
- 2026-11-25: plan gate chose a `hotfix PR #<n> handoff` provenance tag over the ` — started #<n>` token to find these rows at the re-entry, because a started token hides the row in the cairn pane while the PR is open and these rows hold work no one has taken; falsified by a re-entry that misses a row because triage rewrote its provenance.
- 2026-11-25: implement started on branch m339-guest-handoff-flaw-rows.
- 2026-11-25: T1-T3 done in `skills/hotfix/SKILL.md`: step 6 gains the "Handoff flaw record" paragraph, the change route makes it after its approved push (placed after the pinned "Then stop with the close block" sentences, which `test_resume_routing` pins together), step 1's idea vet names the guest exception, and step 7's guest arm gains "Handoff flaw rows". Implementation choice: a row step 1 matched is never the one extended (the flaw gets a new row), because step 7 can delete a matched row whole; so step 6's matched-row sentence keeps its meaning, reworded to pass AC3's grep. The branch adds no simple-english lint hits to the file (207 remain from main).
- 2026-11-25: T4 done: the guest-arm test pins the new step 6, change-route, and step 7 sentences; hand-run `skills/tests` 1031 OK.
- 2026-11-25: T5 done: README `/hotfix` row and a CHANGELOG `## Unreleased` entry under "Changes that affect existing repos".
- 2026-11-25: T6 in part: D-248 appended (via a shell heredoc, not the Edit tool, a slip from the rulebook's file-edit rule). Verify: scripts and hooks suites OK, both `claude plugin validate` OK, `claude plugin test .` fails 19 of 2466 `hooks/status` tests on the branch and identically with the branch edits stashed (main at f16ca210), with claude 2.1.323 and 2.1.331; the branch touches no `hooks/` file. Candidate row "Fix mod tests that fail on main" added at the high rung. AC5's narrowing to failures shared with main is with a fresh Opus re-audit; checkpoint before its result.
- 2026-11-25: substantive amendment: AC5 narrowed to exempt `claude plugin test` failures whose test names also fail on the merge base with main under the same binary; the deliverable is unchanged, so no stop. Review records the base sha and the binary version as evidence.
- 2026-11-25: re-audit: AC5 (full) — satisfiable (merge base = f16ca210, so the stash run was a merge-base run), no IP or D-143 conflict, bounded, proportionate; two optional tightenings (file-qualified test names, a hooks/ no-change clause) not taken, the wording kept as audited.
- 2026-11-25: T6 done: D-248 written; verify per amended AC5 (four commands green, plugin test's 19 failures shared with the merge base); hand-run `skills/tests` OK.
- 2026-11-25: claim audit: 38 claims read, 7 corrected — CHANGELOG.md, README.md, skills/hotfix/SKILL.md (re-entry keep and part-only edits in CHANGELOG and README, the matched-row exception, step 1's two guest exceptions and its step 7 sentence, the change route's vet scope and failed push, the `extended` note's removal); the re-read found all seven correct.
- 2026-11-25: implement done; status review.
- 2026-11-25: review return 1: diff-bug #3 / blame-history #4 (load-bearing) — a handoff can extend a row that another hotfix or a milestone started, whose step 7 or hygiene then deletes it and loses the flaw; fix with the other fix-now findings of pass 1 (Review section): no extension of a started, matched, already-holding, or §7-group row; flaw text inside the `extended` note; record after the Copilot round; change-route order, scope, and `<N>`; step 7 opening, README:809 and :1016, guard pins, D-248 heading.
- 2026-11-25: T7 added for review return 1 (minor amendment) and done: step 6's record now follows the Copilot round, gives no edit to a row that already holds the flaw, puts the flaw inside the `extended` note, and never extends a matched, started, or §7-group row; the change route records before its "Then stop" sentence (the `test_resume_routing` pin split in two), on its changed diff; step 7 names the guest record at its opening and reads `<N>` as the PR the re-entry names; README:809's "before then" names merge and handoff; README:1016 left (owner path, ripple #2 rejected); D-248's heading names D-240 and D-108's door and its Decision states the new limits; guard test renamed and pins AC2's delete/narrow/keep, step 1's guest exception, and the README sentence. `skills/tests` OK, scripts and hooks suites OK, both validates OK. One simple-english hit left ("after that round" read as a trailing condition), kept as a wording nit.
- 2026-11-25: implement done after return 1; status review.
- 2026-11-25: step-7 approval: m339-guest-handoff-flaw-rows approved for merge

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->

Review head 14a51b55, merge base f16ca210 (= origin/main). Copilot arm: PR #354 opened at review start; Copilot requested (state `pending` after the request).

- AC1: `skills/hotfix/SKILL.md` step 6 "Handoff flaw record (M339)" (lines 668-684) runs after the create and the started-token append: search-first; a new row with provenance `— added YYYY-MM-DD — hotfix PR #<n> handoff` naming the flaw as a design decision (672-674); an existing row extended with `; extended YYYY-MM-DD by hotfix PR #<n> handoff` before any ` — started` token (675-678); a standing rejection named in the close block (679-680); the close block shows each row (681); a handoff that opens no PR records nothing and names each flaw (682-684). The change route makes the same record after its approved push with that PR's number (325-330). Met.
- AC2: step 7 "Handoff flaw rows (M339)" (752-762): on the accepted re-entry, each Candidates row of `cairn/ROADMAP.md` holding `hotfix PR #<N> handoff` is judged against the merged diff, only the added part of an extended row; deleted (with its `extended` note, or the whole new row) when covered in full, narrowed with the `narrowed` note when in part, kept otherwise; each deleted or narrowed row shown verbatim; a re-entry vet flaw such a row holds adds no new row; any other outcome leaves the rows. Met.
- AC3: step 1's idea-vet paragraph (128-131, "with two guest-mode exceptions. A handoff whose `gh pr create` succeeds records the flaw at the handoff") and step 6's guest arm (668) say so; `git grep -n -E "only by its started token|only appends its started token" -- skills/hotfix/SKILL.md` lists no line (exit 1). Met.
- AC4: README.md:809 "In guest mode, the hotfix writes that row at the handoff of its PR to the maintainers, not after their merge."; CHANGELOG.md:3-20, `## Unreleased` above `## 2.2.0` (line 22), entry under "Changes that affect existing repos" says the row is written at the handoff, where before it came only after the merge. Met.
- AC5: on 14a51b55, `scripts/tests` OK (446, 21 skipped), `hooks/tests` OK (212), `claude plugin validate` of plugin.json and marketplace.json exit 0, `claude plugin test .` exit 1 with 19 failing of 2466, the same 19 test names (sorted diff empty) as the run with the branch edits stashed at merge base f16ca210, both under claude 2.1.323; hand-run `skills/tests` OK (1031). Met as amended.
- Consistency gate: `cairn_validate` all checks passed; no DESIGN principle text changed, so `cairn_impact` skipped; marketplace validate shows no `plugins[N].version` warning; CHANGELOG has the entry (AC4); verify per AC5.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a row that already holds the flaw itself (the change route re-vetting its own PR) gains a redundant extension each push — fix now
- diff-bug #2: the extension skips records-hygiene §7's bar on silently extending a finding-absorbing group's row — fix now
- diff-bug #3: a row started by another hotfix or a milestone can be extended, and that work's step 7 or hygiene then deletes it and loses the flaw — fix now (load-bearing: the defect this milestone fixes)
- diff-bug #4: the change route's record reads after "Then stop with the close block" — fix now (move it before, update the `test_resume_routing` pin)
- diff-bug #5: step 6's Copilot round can push fixes after the record — fix now (record after the round)
- diff-bug #6: the change route's "the diff" is unclear between the changed diff and the PR's whole diff — fix now
- diff-bug #7: step 1's "a search-first absorb on another path can add to the row" pulls against "a matched row is never extended" — reject (false: the absorb sentence permits, the handoff rule declines; no contradiction)
- diff-bug #8: an over-the-bar re-entry could write a duplicate row — reject (false: that route's row is search-first and finds the handoff row)
- diff-bug #9: README:809 "before then" is ambiguous between handoff and merge — fix now
- diff-bug #10: the guard pins none of AC2's delete/narrow/keep sentences, step 1's guest exception, or the new README sentence, and its test name is stale — fix now
- diff-bug #11: the `# M339:` test comment and sentence pins — reject (style: matches the file's `# M258:` comment and the skills/tests house form, D-109)
- diff-bug #12: D-248's heading names neither D-108's door nor D-240 — fix now
- blame-history #1: "It edits no other row" contradicts extending rows — reject (false: the same sentence names the flaw record, whose extension is the edit)
- blame-history #2: rows from a PR closed unmerged are never judged and point at a dead PR — reject (planned change: AC2 leaves them; the flaws stand independent of the PR, and `/cairn-triage` sees them)
- blame-history #3: deleting "the part the handoff added" has no text boundary — fix now (the flaw goes inside the `extended` note)
- blame-history #4: a row with a live started token can be extended — fix now (same fix as diff-bug #3)
- blame-history #5: D-248 does not mention D-165 — reject (false: D-165's token rule is unchanged)
- prior-review #1: on-disk writes at the handoff trip the stop guard — reject (false: guest `cairn/` is in git's exclude file, so `git status --porcelain -- cairn/` shows nothing; diff-bug (b) confirms)
- prior-review #2: `<N>` "the merged PR" can name a re-entry's follow-up PR — fix now (name the PR the re-entry reads)
- prior-review #3: a zero-flaw handoff has no close-block output — reject (false: "shows each row written" with none shows nothing)
- prior-review #4: the narrowed note and the handoff tag differ — reject (planned change: different records on purpose)
- prior-review #5: a colon-less flaw title is undefined — reject (false: tracking-rules "Candidate short title" governs every row written)
- prior-review #6: step 7's guest arm has no failed-write arm — follow-up, already held by the parked row "Say what a failed step 7 commit does" (pre-existing), no new row
- prior-review #7: the new pins lack a mutation-harness entry — reject (style: skills/tests is hand-run, D-109)
- ripple #1: records-hygiene §7 bar — fix now (same fix as diff-bug #2)
- ripple #2: README.md:1016-1018 says the flaw "still becomes a candidate row after the merge" — reject (false: that passage is the owner-mode resumed merge, unchanged; settled at implement return 1)
- ripple #3: step 7's opening rule states no guest exception — fix now
- ripple #4: the parked row "Keep hotfix flaws after a declined merge" — reject (false: still accurate)
- ripple #5: tracking-rules "Candidate started token" omits the flaw record — reject (false: incomplete, not contradicted; the token rule is unchanged)
- ripple #6: DESIGN.md:637 omits the flaw rows — reject (false: its claim is still true)
- ripple #7: the owner resume arm's step 7 sentence — reject (false: owner mode, consistent)
- Pass 1 fix-now items fixed 3b8c052a (T7), except ripple #2, re-settled as reject.

Pass 2 (head 3b8c052a, after return 1). Evidence: scripts OK (446, 21 skipped), hooks OK (212), both validates exit 0 with no `plugins[N].version` warning, `claude plugin test .` 19 fails of 2466 with the same names as the merge-base run (claude 2.1.323, no `hooks/` change), `skills/tests` OK (1031); AC1-AC4 re-read on the new text: still met (AC1's started-token placement is now moot, since a started row is never extended; AC2's part-only judgment now reads the flaw inside the `extended` note).
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: step 7's new sentence "step 6's handoff flaw record wrote those rows" leaves no row for a re-entry flaw no handoff row holds — fix now (not load-bearing: step 1's "unless a guest handoff's row already holds it" still governs; a wording error in the T7 sentence)
- diff-bug #2: CHANGELOG's "unless it is a row the fix itself closes" misstates step 6 — fix now
- diff-bug #3: after the Copilot round the record still lists flaws a Copilot fix changed — fix now
- diff-bug #4: narrowing an extended note's flaw has no placement — fix now
- diff-bug #5: deleting a handoff-written row drops later additions — fix now
- diff-bug #6: a handoff row can match as "a row that describes the bug" — reject (false: a flaw row describes code the fix left as it was, not the bug)
- diff-bug #7: a new row for a §7 group does not name the group row — fix now
- diff-bug #8: "approved push" vs "a push that fails records nothing" — fix now
- diff-bug #9: a failed on-disk ROADMAP write has no arm — reject (edge: a failed local Write is an error the session sees, outside common use)
- diff-bug #10: the split pin drops the order check — fix now
- diff-bug #11: the `# M339:` comment — reject (style, as pass 1)
- blame-history #1: CHANGELOG clause — fix now (same as diff-bug #2)
- blame-history #2: the record sits before the Copilot round's "Then stop" — fix now (the round's text now says to make the record before it stops)
- blame-history #3: the §7 group has no test the handoff can apply — reject (false: §7 defines the group)
- prior-review #1: CHANGELOG clause — fix now (same as diff-bug #2)
- prior-review #2: the change route could read the round-on/off timing — fix now (it says it runs no round)
- prior-review #3: a re-entry run on a follow-up PR's number misses rows tagged with the handoff PR — reject (edge: a guest re-entry on a follow-up number is outside common use, and the rows stay visible to `/cairn-triage`)
- ripple #1: README.md:641-644 says the guest arm writes the started token after the create — reject (false: still true)
- ripple #2: `narrowed … by the PR #N hotfix` vs `extended … by hotfix PR #<n> handoff` word order — reject (style)
- ripple #3: an `extended …: <flaw>` note changes a colon-less row's short title — reject (false: every row has ` — added` before its lineage, so the cut falls there first)
- ripple #4: `/cairn-triage` SKILL.md:85-86 on the guest token — reject (false: still true)
- copilot: review body https://github.com/jmgirard/cairn/pull/354#pullrequestreview-6067236613 — noted (no open issues, no threads, no note)
- Copilot level: Lite (set by GitHub's settings)
- conversation: PR #354 — empty read beyond that Copilot review (no issue comments, no threads)
- snapshot: none (no `_snaps` or `__snapshots__` path in the diff)
- Pass 2 fix-now items fixed 4e609136; on that head `skills/tests` OK, scripts and hooks suites OK, `claude plugin test .` the same 19 merge-base failures, AC3's grep lists nothing.
