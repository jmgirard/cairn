# M172: A merged or stopped review milestone resumes at the right step

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Branch/PR:** m172-resume-routing · https://github.com/jmgirard/cairn/pull/175

## Goal

A review or hotfix session that stopped at the CI wait, or whose PR was
merged outside the session, re-enters at the step the record shows is
next, so post-merge hygiene is never skipped by accident.

## Scope

Surface tier: user-facing — skill conduct rules are what an adopting
repo's operator runs under.

**In:** `/milestone-review` session start reads the header PR's state and
the Review section and routes to step 9 (merged, review complete), to a
post-hoc verification of the merged head (merged, review incomplete), to
the re-posed approval and the CI watch (open, review complete), or to step
1; step 7 records its approval in the work log so the route can read it;
the tracking-rules wait rule's timeout stop hands off with the invoking
skill's own command and its resume clause re-derives merge state; the
three restating sites carry the next-command sentence; `/milestone`'s
audit reports a merged-but-`review` milestone as hygiene owed; `/hotfix`
re-enters at step 7 for a merged hotfix or adopted PR; a hand-run prose
guard pins the new routes; a D-entry annotates D-128.

**Out:** keeping a watcher alive across a stop point (D-128's rule
stands); a `gh` call inside `cairn_next.py` (it stays offline — its
`review → /milestone-review` recommendation is already the right door);
a validator or hook for the merged-but-`review` state (prose plus the pin,
D-128's proportionality stance); detecting merges of the milestone PR by
others (M167's outside-merges audit owns that).

## Acceptance criteria

- [x] AC1: `/milestone-review`'s "Session start" section states that when
      the target milestone's `Branch/PR` header carries a PR URL, the
      session reads that PR's state with `gh pr view <N> --json
      state,mergedAt` (N from the URL) before step 1 and routes on the
      state and the Review section: (a) `MERGED`, every criterion box
      ticked, and a work-log line recording step-7 approval → one work-log
      line naming the PR, its `mergedAt` value, and the re-entry, then step
      9 with steps 1–8 skipped, the recorded approval standing as step 9's
      issue-write authorization; (b) `MERGED` otherwise → the same work-log
      line plus a chat statement that verification never ran, then steps
      3–7 executed against the merged default-branch head, step 7's chip
      posed with question text naming acceptance of the post-hoc
      verification and the issue writes it authorizes (a decline logs the
      requested changes as tasks and sets status `in-progress`, step 7's
      decline exit), then step 9 with step 8 skipped; (c) `OPEN`, every box
      ticked, and a recorded approval → step 1 re-run, the step-7 chip
      re-posed, and on approval step 8 from the marker write onward; (d)
      any other state, or a state above whose conditions are not met →
      step 1; a `gh` that is missing, unauthenticated, or has no remote →
      step 1 with the recap naming which. Step 7 states that approval
      appends one work-log line naming the PR number it approved.
- [x] AC2: The tracking-rules "Waiting on CI and background work"
      paragraph's "On timeout" clause states that the stop emits a close
      block whose fenced next command is the invoking skill's own command,
      and its "Resume is stateless" clause names the PR's merge state
      (`gh pr view <N> --json state`) beside its check state as what a
      resume re-derives; and the three restating sites — `/milestone-review`
      step 8, `/hotfix` step 6, `/cairn-release` step 3 — each state that
      the stop's close block names that skill's own command as the next
      command.
- [x] AC3: `/milestone`'s §2 audit list carries a bullet, adjacent to the
      existing bullet for a `review` milestone with an open unmerged PR,
      stating that a `review` milestone whose header PR reports `MERGED` is
      reported as post-merge hygiene owed and routed to
      `/milestone-review M<NNN>`.
- [x] AC4: `/hotfix` step 1 states that a PR-reference argument whose
      `gh pr view <N> --json state,headRefName` reports `MERGED` and a head
      branch not matching `m<nnn>-*` runs step 7 only, steps 2–6 skipped:
      the candidate-row check, then — when the PR body carries a `Fixes #N`
      line — one chip authorizing the issue close before any issue write,
      then the close block with one recap line naming the merged PR.
- [x] AC5: The active profile's `verify` slot — `python3 -m unittest
      discover -s scripts/tests` and `python3 -m unittest discover -s
      hooks/tests` from the repo root — passes at the branch head.

## Coverage

- AC1 → T2
- AC2 → T1, T2, T3
- AC3 → T3
- AC4 → T3
- AC5 → T4
- (T5's D-entry binds no criterion — D-120's disposition; review checks
  it under the consistency gate, not AC fencing.)

## Tasks

- [x] T1: `skills/shared/tracking-rules.md` "Waiting on CI and background
      work" (~lines 250–258): the "On timeout" clause ends in a close block
      with the invoking skill's command; "Resume is stateless" adds merge
      state. Keep `skills/tests/test_wait_rule.py` anchors intact.
- [x] T2: `skills/milestone-review/SKILL.md`: Session start (~line 17)
      gains the four-way route of AC1; step 7 (~line 287) appends the
      approval work-log line; step 8's timeout clause (~line 325) names
      `/milestone-review M<NNN>` as the close block's next command.
- [x] T3: `skills/milestone/SKILL.md` §2 (~line 124) merged-PR bullet;
      `skills/hotfix/SKILL.md` step 1 (~line 19) merged-PR re-entry and
      step 6 (~line 108) next-command sentence; `skills/cairn-release/SKILL.md`
      step 3 (~line 62) next-command sentence.
- [x] T4: Hand-run guard `skills/tests/test_resume_routing.py` pinning
      AC1's whole route list (M171 lesson: the list, never its head), AC3's
      bullet, and AC4's re-entry clause, each pin registered in
      `skills/tests/test_mutation_harness.py`; run both gating suites and
      the hand-run suite from the repo root.
- [x] T5: D-entry annotating D-128: the timeout stop gains a resume route
      and the merged-but-`review` state a door; alternatives rejected at
      the gate with the evidence class that reopens each.

## Work log

- 2026-09-02: created by /milestone-plan from the user's report that the CI watch stop never resumes to post-merge hygiene.
- 2026-09-02: collision sweep — no candidate, archive, or D-entry covers a resume route; D-128's "On timeout" clause stops with no next command named; D-090/D-108 door passed on the trigger clause (shipped skill behaviour misroutes after an outside merge: step 2 pushes a deleted branch); inbox sweep: 0 open issues, 0 open PRs.
- 2026-09-02: criteria audit ran in full mode ([O] fresh reader, tier user-facing), two passes: pass 1 returned 11 findings (IP1 conflict for an unreviewed merged PR — became gate Q1; unauthorized step-9 issue writes; three instrument-bound criteria dropped to tasks; site enumeration widened to D-128's three sites; a bundled criterion split; wording fixes); pass 2 on the gate-revised text returned 8 findings, all fixed autonomously: approval recorded in the work log so routes (a)/(c) are reachable; branch (d) covers unmet conditions; branch (b)'s decline takes step 7's exit; the post-hoc chip names what it authorizes; branch (c) re-runs step 1; D-128 names no sites (enumerated explicitly); hotfix re-entry poses its own close authorization; head-branch test excludes only `m<nnn>-*` so adopted PRs qualify.
- 2026-09-02: plan gate chose post-hoc verification of an unreviewed merged PR over hygiene-with-override because an archived `done` row should rest on verified criteria (IP1); falsified by a post-hoc verification that cannot be run against a merged head in practice.
- 2026-09-02: plan gate chose in-scope hotfix and open-PR re-entry over candidate rows at the user's election; falsified by the milestone tripping the split tripwires at implement.
- 2026-09-02: plan chose prose routes plus a hand-run pin over a `gh` call in `cairn_next.py` or a validator because the routing surface is the skill's session start and `cairn_next` stays offline; falsified by a merged-but-`review` milestone reaching a hygiene stamp unarchived under the new prose.

- 2026-09-02: /milestone-implement started; branch m172-resume-routing cut from main at 83b10de; question gate skipped — the plan left no genuinely open choice (work-log line shapes for the approval and re-entry lines fixed in T2).
- 2026-09-02: T1 done — tracking-rules "On timeout" clause now ends in a close block naming the invoking skill's command; "Resume is stateless" re-derives merge state via `gh pr view <N> --json state` beside check state; M170 anchors intact; verify green (scripts 121, hooks 588), hand-run skills/tests green.
- 2026-09-02: T2 done — `/milestone-review` Session start carries the four-way resume route (a)–(d) on `gh pr view <N> --json state,mergedAt` plus the Review section; step 7 appends `step-7 approval: PR #<N> approved for merge`; step 8's timeout stop closes with `/milestone-review M<NNN>` as next command; verify green, hand-run skills/tests green.
- 2026-09-02: T3 done — `/milestone` §2 gains the merged-but-`review` hygiene-owed bullet beside the open-PR bullet; `/hotfix` step 1 gains the merged-PR re-entry (step 7 only, head branch not `m<nnn>-*`, own close-authorization chip) and step 6 names `/hotfix` as the timeout stop's next command; `/cairn-release` step 3 names `/cairn-release`; verify green, hand-run skills/tests green.
- 2026-09-02: T4 done — `skills/tests/test_resume_routing.py` pins the trigger, all four routes (a)–(d) whitespace-collapsed, step 7's approval line, the audit bullet and its adjacency, and the hotfix re-entry; nine blocks registered in `test_mutation_harness.py`, each proven to red its guard when blanked; scripts/tests, hooks/tests, and the hand-run suite green.
- 2026-09-02: T5 done — D-130 appended, annotating D-128 with the resume route and the merged-but-`review` door, the three gate rejections each carrying its reopening evidence class; validate green.
- 2026-09-02: all tasks checked; verify green (scripts/tests, hooks/tests), hand-run skills/tests green; status → review.

## Decisions

## Review

- 2026-09-02 AC1: read `skills/milestone-review/SKILL.md` Session start at 257f506 — the M172 resume-routing paragraph triggers on a `Branch/PR` PR URL, reads `gh pr view <N> --json state,mergedAt` before step 1, and routes (a) merged+ticked+approval → resume line then step 9 with 1–8 skipped and the approval as issue-write authorization; (b) merged otherwise → resume line, chat statement, steps 3–7 on the merged head, post-hoc acceptance chip naming the issue writes, decline → tasks + `in-progress`, acceptance → step 9 skipping 8; (c) open+ticked+approval → step 1 re-run, chip re-posed, step 8 from the marker write; (d) anything else → step 1, a missing/unauthenticated/no-remote `gh` → step 1 with the recap naming which. Step 7 (line 340) appends `step-7 approval: PR #<N> approved for merge`. Pass.
- 2026-09-02 AC2: read `skills/shared/tracking-rules.md` lines 250–260 at 257f506 — "On timeout" ends with a close block whose fenced next command is the invoking skill's own command (`/milestone-review M<NNN>`, `/hotfix`, `/cairn-release`); "Resume is stateless" re-derives check state from `gh pr checks` and merge state from `gh pr view <N> --json state`. The three restating sites: `/milestone-review` step 8 (line 359) names `/milestone-review M<NNN>`, `/hotfix` step 6 (line 120) names `/hotfix` with the PR reference, `/cairn-release` step 3 (line 66) names `/cairn-release`. Pass.
- 2026-09-02 AC3: read `skills/milestone/SKILL.md` §2 lines 124–129 at 257f506 — the bullet for a `review` milestone whose header PR reports `MERGED` (`gh pr view <N> --json state`) reports post-merge hygiene owed and routes to `/milestone-review M<NNN>`, immediately below the open-unmerged-PR bullet. Pass.
- 2026-09-02 AC4: read `skills/hotfix/SKILL.md` step 1 lines 33–40 at 257f506 — a PR-reference argument whose `gh pr view <N> --json state,headRefName` reports `MERGED` with a head branch not matching `m<nnn>-*` runs step 7 only, steps 2–6 skipped: candidate-row check, then one chip authorizing the issue close when the body carries `Fixes #N` before any issue write, then the close block with one recap line naming the merged PR. Pass.
- 2026-09-02 AC5: ran the `verify` slot from the repo root at 257f506 — `python3 -m unittest discover -s scripts/tests` 329 tests OK (exit 0); `python3 -m unittest discover -s hooks/tests` 121 tests OK (exit 0). Hand-run `skills/tests` 598 tests OK (exit 0), noted for the D-109 stamp. No Driving RR — projection-vs-outcome no-ops. Pass.
- 2026-09-02 consistency gate: `cairn_validate.py` exit 0 at 257f506 (16 PASS, 7 OK, `release window` advisory silent); Principles touched — so `cairn_impact --changed` skipped; `generic` profile names no toolchain checks; D-130 present once, annotating D-128 (T5). Defect-return count for this milestone: 0. Pass.
- 2026-09-02 independent review (full fan-out, tier user-facing, .py touched): [S] blame-history — no findings (M170 anchors byte-identical, D-130 states D-128 accurately, hotfix step 7 holds what the re-entry cites); [S] prior-review-record — no regressions (probe `pulls/comments?per_page=1` returned `[]`, walk skipped; M171 whole-list lesson complied with); [O] diff-bug — 15 findings, ranked, triaged at the gate below.
- F1 (hotfix step 1): merged-PR re-entry skips steps 2–6 so a PR merged outside the session reaches step 7 with no regression test or gate-lite check — recommended: follow-up candidate row (plan-chosen shape; a post-hoc hotfix bar is new conduct).
- F2 (review route c): step 1's branch-sync merge is never pushed because step 2 is skipped, so the squash merges a stale remote head — recommended: fix now (push after step 1; re-gather step-3 evidence when the default branch moved).
- F3 (review route d): an OPEN PR with a half-done review reaches step 2's `gh pr create`, which fails on a branch with an open PR — recommended: fix now (step 2 skips creation when the header names an open PR).
- F4 (review step 7): the approval work-log line lands after step 6's checkpoint and is never committed, so routes (a)/(c) cannot read it after the squash — recommended: fix now (step 7 commits and pushes the line before the marker write).
- F5 (review route b): step 5's tier diff `git diff <default>...HEAD` is empty on the default branch; step 5 fix-now and step 6 checkpoint name a branch that no longer exists — recommended: fix now (reviewers read the merged PR's diff via `gh pr diff <N>`; fix-now code goes through `/hotfix`; the checkpoint is a docs-only commit).
- F6 (hotfix step 1): "step 6's chip never ran" is false on the stopped-CI-wait trigger — recommended: fix now (reword: a hotfix keeps no record of step 6's chip, so authorization is asked once here).
- F7 (cairn-release step 3): the close block is bound to the `TaskStop`-before-commit clause, not the timeout stop, so a routine mid-session `TaskStop` reads as a handoff — recommended: fix now (bind to the background-move/timeout stop like the other two sites).
- F8 (milestone §2): "re-enters at the hygiene step" holds only for route (a) — recommended: fix now ("at the step the record shows is next").
- F9 (review route b): "the same work-log line" carries route (a)'s "re-entering at step 9" — recommended: fix now (step 3 in the line).
- F10 (review route b): step 7's chip mandates a merge as the recommended option, which is meaningless for a merged PR — recommended: fix now (the recommended option accepts the post-hoc verification).
- F11 (review route a): tests ticks, not evidence, which step 3 says is not a pass — recommended: fix now ("ticked against a recorded evidence line").
- F12: AC2's clause has no pin and `test_wait_rule.py`'s docstring says two clauses — recommended: reject the pin (a new rule owes no prose guard, D-108/D-109, test-doctrine slot); fix the docstring now.
- F13 (review routes a/b): end at step 9, never naming step 10's close — recommended: fix now ("steps 9–10").
- F14 (tracking-rules): the next-command parenthetical reads as a closed list of three — recommended: reject (the three are the sites that exist; no restating site is missing).
- F15 (mutation registry): routes pinned by tail clause rather than one entry per deletable clause — recommended: reject (guards proven non-vacuous; convention deviation only).
- 2026-09-02 gate triage (user chose fix-now at the step-7 chip): F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F13 and F12's docstring half fixed on the branch — routes (a)–(d) rewritten (evidence-backed ticks, route (c) pushes and re-gathers evidence when the default branch moved, route (d) skips `gh pr create` for an open PR, route (b) re-enters at step 3 with reviewers on `gh pr diff <N>`, fix-now code via `/hotfix`, a docs-only checkpoint, and an accept-not-merge recommended option, routes end at steps 9–10), step 7 commits and pushes the approval line before the marker, `/cairn-release` binds its close block to the timeout stop, `/hotfix` states the honest reason for its authorization chip, `/milestone`'s bullet names the step the record shows is next, `test_wait_rule.py`'s docstring names the unpinned third clause; pins and mutation blocks updated to the new text. F1 → candidate row "Post-hoc hotfix bar for a PR merged outside the session" (search-first: no overlap). Rejected: F12's pin half (a new rule owes no prose guard, D-108/D-109), F14 (the three named sites are all that exist), F15 (guards proven non-vacuous; convention only). No finding failed a criterion as written; return floor not crossed.
- 2026-09-02 re-verification at 16faa73 after the fix-now edits: AC1's four routes and step-7 line re-read at the new text — each route still carries the clause the criterion names (a → step 9 with 1–8 skipped, b → steps 3–7 then step 9 with 8 skipped, c → step 1 re-run, chip re-posed, step 8 from the marker, d → step 1); AC2's three restating sites re-read, `/cairn-release` now bound to the timeout stop; AC3's bullet re-read, still adjacent; AC4's re-entry re-read, three moves intact; AC5 re-run — scripts 329 OK, hooks 121 OK, hand-run skills 598 OK; validate exit 0. All five hold.
