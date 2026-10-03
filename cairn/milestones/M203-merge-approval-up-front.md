# M203: Approve the merge in the question set

- **Status:** planned
- **Priority:** normal
- **Depends on:** M202
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing, because the skills and the merge guard ship in the plugin to every adopter
- **Branch/PR:** m203-merge-approval-up-front

## Goal

The user can approve the merge of a milestone in the plan question set, so a run whose review passes merges without a second question.

## Scope

**In:** IP1 and a D-entry that records the user decision of 2026-10-03.
A `Merge approval:` header slot that the plan writes from the question
set. The merge path of review for an up-front approval, with the cases that
go back to the merge question. The deny text of `merge_guard` and a test.
The rulebook, README, routing template, CLAUDE.md, and CHANGELOG text on
approval.

**Out:** A standing approval for every run of a repo. The user chose one
approval for each plan at the 2026-10-03 gate, so this has no row. The
merge question of `/hotfix` goes to the candidate row "`/hotfix` keeps its
own questions".

## Acceptance criteria

- [x] AC1: IP1 in `cairn/DESIGN.md` keeps its sentence that nothing reaches the default branch without
      explicit user approval at a gate. It adds the two gates for a milestone merge. One is the merge
      question. The other is the plan question set, for a milestone whose promise, as that plan committed it,
      merges unchanged. That milestone also meets none of the route-back cases that the rulebook lists. A
      D-entry records the user decision that changes IP1 (RB tripwire: ip-touching). The D-entry states that
      the up-front approval comes before the diff exists. It names the route-back cases as the mechanism that
      keeps the promise unchanged, and states that removing or narrowing a route-back case changes IP1. It
      narrows D-138 and D-144 and annotates D-043 by name.
- [x] AC2: The milestone template carries a `Merge approval:` header slot. Step 3 of
      `skills/milestone-plan/SKILL.md` lists merge approval among the questions of the set, with one answer
      for each milestone. When a plan creates several, the user can hold any of them `at the end`. The
      question states that a run with no route-back case merges unseen. It also states that the code and the
      finding dispositions of such a run appear only after the merge. For a user-facing or IP-touching
      milestone, it recommends `at the end`. The plan writes each slot as `up front YYYY-MM-DD` or `at the
      end`. A set that did not pose the question writes `at the end`. A re-cut via `/milestone-plan` asks
      again and rewrites the slot. Review and the guard read `—` or a missing slot as `at the end`.
- [x] AC3: If all of these hold, `skills/milestone-review/SKILL.md` skips the merge question:
      - the default-branch copy of the slot reads `up front`,
      - this invocation of review started with an empty Review section and no PR for the branch, and the
        work log has no `step-7 approval:` line,
      - the Goal, Scope, and Acceptance criteria text on the branch differs from that of the plan commit only
        in checkbox ticks (the plan commit is the newest default-branch commit whose subject is `plan …` and
        names M<NNN>),
      - no work-log line records a substantive amendment, an `amendment return:`, or a declined merge
        question,
      - each criterion has passing evidence,
      - no finding the agent disposed fix-now is left unfixed,
      - no finding that its lens ranked first was rejected as false,
      - on a user-facing milestone, no finding was rejected as false,
      - the Review section records the spawned reviewers,
      - `Principles touched:` names no IP, and `git diff <default>...HEAD` adds no `### D-` heading,
      - no condition of step 7 that adds to the merge question applies (a Driving RR shortfall, guest mode, a
        companion PR, an issue write from `Resolves:`).

      In that case it commits the work-log line `step-7 approval: <branch> approved up front per plan <sha>`
      before the push of step 8, and step 8 runs in the same invocation. Step 8 writes the marker `M<NNN>
      approved up front YYYY-MM-DD per plan <sha> for PR #<N>` only when CI is green, or the rulebook rule for
      a PR with no CI runs applies, and the PR-conversation read finds no item from a non-bot author. Red CI,
      a non-bot item, or any stop poses the merge question, in this invocation or the next. In every other
      case it asks the merge question as before. The close block or merge question that ends the run lists
      each milestone merged up front in the run. For each, it gives the PR and each finding verbatim with its
      disposition and the reason for each reject.
- [x] AC4: The deny text and the docstring of `hooks/merge_guard.py` name both points of approval. For a
      marker that carries `up front`, the guard reads the milestone file at the local remote-tracking ref of
      the default branch of the base remote. If the file, the ref, or the slot cannot be read, the guard
      denies the merge. If the slot does not read `up front`, the guard denies the merge. The deny text names
      the slot value it read, or that none could be read, and the ref and path it read from. `hooks/tests`
      tests show that the guard allows `gh pr merge <N>` in one case: an `approved up front` marker for PR
      `<N>` and a default-branch slot of `up front`. The tests show a denial for each of these:
      - another PR number,
      - a slot of `at the end`, a slot of `—`, and a missing slot,
      - `up front` only in the working tree,
      - `up front` only on the local default branch,
      - no remote-tracking ref,
      - an absent file,
      - a marker for one milestone while only another milestone's slot reads `up front`.

      A legacy marker without `up front` behaves as before.
- [x] AC5: Three surfaces state the up-front approval and the cases that go back to the merge question: the
      approval bullet of the git model in `skills/shared/tracking-rules.md`, "Merges are yours" in
      `README.md`, and a `CHANGELOG.md` entry. `skills/shared/templates/claude-md-section.md` and the cairn
      section of `CLAUDE.md` state the up-front approval and either list the cases or point to the rulebook's
      approval bullet for them. The verify slot passes as in AC7 of M202.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3, T8, T9, T12
- AC4 → T4, T9
- AC5 → T5, T6, T8, T10

## Tasks

- [x] T1: Rewrite IP1 in `cairn/DESIGN.md` and append the D-entry (RB
      tripwire: ip-touching). The user decided it at the plan gate.
- [x] T2: Add the `Merge approval:` slot to
      `skills/shared/templates/milestone.md`. Add the merge question to the
      step-3 list of `skills/milestone-plan/SKILL.md` and the slot write to
      step 4.
- [x] T3: `skills/milestone-review/SKILL.md` steps 5, 7, and 8: the
      route-back cases, the up-front path, the work-log line, the marker
      after green CI, and the end-of-run list of dispositions. Step 5 gives
      each finding its lens, rank, and disposition, and records the spawned
      lenses. Read the resume routes that parse the `step-7 approval:` line.
      A resume after a CI timeout finds the up-front line and re-derives CI.
- [x] T4: The slot read, the deny text, and the docstring in
      `hooks/merge_guard.py`, with the `hooks/tests` tests of AC4.
- [x] T5: The surfaces in AC5.
- [x] T6: Run the verify slot and `cairn_validate`.
- [x] T7: Before T1, take RR15 recs 1 to 9 to the step-6 amendment stop. Recs 1 to 5 are route-backs: a substantive amendment, a false-reject, an IP touched or a D-entry written, a degraded review, and a CI fix after the PR opens. Rec 6 binds the approval per milestone, rec 7 is the IP1 wording, and rec 8 has the guard read the slot. Rec 9 fixes the wording of AC2, AC3, T3, and T4. The other choice to offer is dropping the up-front path.
- [x] T8: Review return 1. Every close block that ends a run in which a
      milestone merged up front carries the end-of-run list (rulebook
      close-block shape, implement and review stops). The routing template
      and the CLAUDE.md section state the route-back cases. The
      `merge_guard` line of `cairn/DESIGN.md` names the slot read.
- [x] T9: Review return 2 and the pass-2 findings marked "fix now". One
      definition of a late push: the PR head is the commit that added the
      up-front line. A red-CI fix goes straight to the merge question. The
      PR-conversation read runs before the marker, and any item routes back.
      The guard resolves the default branch locally (no network), strips
      backticks, matches `up front` as a word, and reads `ref:./path` from
      `ls-tree -z`. Add tests for those cases and a zero-padded id. Fix the
      stale prose sites.
- [x] T10: Execute the AC5 amendment: the two routing surfaces point to the
      rulebook bullet, the template is back under the cap, and the CLAUDE.md
      Trivial reflow is reverted.
- [x] T11: Take RR16 recs 1 to 6 to the step-6 amendment stop: the one-pass AC3, a D-entry, the pass-3 one-line fixes, one route-back list, the guard deny for an unset remote HEAD, and non-bot route-back. The other choice to offer is removal (rec 9).
- [x] T12: Apply RR16 recs 1 to 6 and review return 3: D-146, the one-pass review text, the rulebook's
      single route-back list, the guard deny for an unset remote HEAD, and the pass-3 one-line fixes.

## Work log

- 2026-10-03: created by /milestone-plan, in one run with M202.
- 2026-10-03: criteria audit (full mode, fresh Opus reader) covered M202 and M203. The M202 work log has the result.
- 2026-10-03: plan gate chose one approval for each plan over a standing approval and over the end question, at the user's answer. Falsified by an up-front merge that the user reverts.
- 2026-10-03: implement started on branch m203-merge-approval-up-front, in the run after M202 merged. Untracked `tsconfig.json` left unstaged.
- 2026-10-03: T1 escalation offer (ip-touching): the user chose to escalate the IP1 change via `/milestone-brief` before T1 starts.
- 2026-10-03: blocked on RB15. The brief is committed on this branch, not on main, because the milestone's state already lives on the branch, and a main commit would conflict with it.
- 2026-10-03: RR15 ingested (Fable, advisory, 16 recommendations). Apply: recs 1 to 9. They add route-backs to the merge question, bind the approval per milestone, add the slot read to the guard, and change the IP1, AC2, AC3, T3, and T4 wording. These widen AC2 to AC4 and change the per-plan approval the user chose, so T7 records them for the step-6 amendment stop. Follow-up row: recs 10 to 13. Rejected as RR15 reasons: rec 14 (stronger marker binding exceeds the stakes, D-043), rec 15 (a D-entry alone, against IP2), and rec 16 (dropping the path, unless recs 1 to 5 do not ship).
- 2026-10-03: T7 amendment stop: the user chose to apply RR15 recs 1 to 9.
- re-audit: AC1 (full) — IP1's new text would cover docs-only commits, D-138 and D-144 not narrowed, "every check of the run passed" unbounded; fixed.
- re-audit: AC2 (full) — the "seen only after the merge" clause false under route-backs, no recommended option; fixed.
- re-audit: AC3 (full) — CI condition after the pre-push approval line, "substantive" left to judgment, dead M202 AC1 citation, slot copy and D-entry scope unnamed, no list for a chained run; fixed.
- re-audit: AC4 (full) — probes vary only the PR number and one slot value; fixed.
- re-audit: AC1 (full) — D-043 not annotated, a rulebook edit to the route-back list would change IP1 without the IP procedure.
- re-audit: AC2 (full) — RR15's "a re-cut asks again" dropped.
- re-audit: AC3 (full) — stop detection reads close blocks that are not on disk, "amendment line" undefined, a declined merge question does not route back, plan commit ambiguous, no-push clause worded as a ban.
- re-audit: AC4 (full) — probes do not vary the milestone file or the ref, deny text cannot name a slot it never read.
- 2026-10-03: stop at the second re-audit of AC1 to AC4 (repeated review-failure stop). Amended text not yet written.
- 2026-10-03: substantive amendment of AC1 to AC4 at the user's answer: the second reader's seven fixes applied, the "no stop fired" condition dropped (the user is present at each stop and types the resume), no third reader. T3 and T4 widened to match, T7 ticked.
- 2026-10-03: T1 done: IP1 adds the two gates for a milestone merge, D-145 records the change, its route-back cases, and the D-138, D-144, and D-043 links. Verify green (scripts 395 OK, hooks 174 OK, plugin validate and test 632 pass).
- 2026-10-03: T2 done: template slot defaults to `at the end`; plan step 3 adds the per-milestone merge question, step 4 the slot write with the re-cut rule. No script parses header slots, so no parser change. Verify green.
- 2026-10-03: T3 done. Review step 7 reads the default-branch slot and runs the route-back checks, step 8's up-front arm writes the marker only after green CI, resume route (c) re-runs the check, and steps 7 and 10 carry the end-of-run list. To make the checks readable from files, step 5 logs each finding as `<lens> #<rank>: … — <disposition>` with a `spawned:` line, a decline writes `step-7 decline:`, and implement step 6 opens its line `substantive amendment:`. Verify green. `skills/tests` resume_routing has one red in `/hotfix` text, the same on the pre-edit tree.
- 2026-10-03: T4 done. `cairn_common` gains `marker_up_front_milestone` and `default_branch_merge_slot`, which read the slot at `refs/remotes/<base>/<default>`. `merge_guard` denies an up-front marker unless that slot reads `up front`, and its docstring and missing-marker text name both gates. `TestMergeGuardUpFront` has 13 tests. Three planted defects each turned their target test red: a working-tree read, a local-branch read, and a match on any milestone's slot. Verify green (hooks 187 OK).
- 2026-10-03: T5 done. The rulebook approval bullet lists the route-back cases and the up-front marker, and its merge-question gate bullet names the skip. README "Merges are yours", the routing template, the CLAUDE.md section (26 lines), and a CHANGELOG entry state the up-front approval and the cases. Verify green.
- 2026-10-03: T6 done. Verify green: scripts 395 OK (21 skipped), hooks 187 OK, plugin validate passes with warnings, plugin test 632 pass, `cairn_validate` all checks passed. The hand-run `skills/tests` showed two new reds in `test_section_allow_lists`, fixed by adding Merge approval to the rulebook's section-ownership table. It now has the 4 reds and 1 error that main has.
- claim audit: 42 claims read, 5 corrected — skills/shared/tracking-rules.md, README.md, CHANGELOG.md, hooks/tests/test_hooks.py
- 2026-10-03: claim audit re-read by the same reader: all 5 corrected claims now match. Its one edge note (a deny with no default branch names the base remote, not a ref) is folded into the test docstring.
- review return 1: AC3 fails because a run that merged a milestone up front and then ends at a stop (an implement stop, a review CI timeout, a thrash stop) ends with a close block that carries no end-of-run list of that merge's findings. AC5 fails because the routing template and the CLAUDE.md section name the cases only as "any route-back case". The gate fails because `cairn/DESIGN.md:61-63`, the `merge_guard` line, does not name the default-branch slot read.
- 2026-10-03: T8 added for review return 1 (minor amendment, Coverage AC3 and AC5 gain T8). Done: the rulebook close-block shape, implement step 8, and review step 10 carry the end-of-run list at any close that ends the run. The routing template and the CLAUDE.md section list the route-back cases. To keep the CLAUDE.md section at 29 lines, its Trivial bullet now fits on one line. The template's file grows to 35 lines, past its "~25 lines" body note, which no check reads. DESIGN's `merge_guard` line names the slot read. Verify green, `skills/tests` at main's 4 reds and 1 error.
- claim audit: 37 claims read, 2 corrected — CLAUDE.md, skills/shared/templates/claude-md-section.md
- 2026-10-03: the T8 claim audit (commit f1c43f8 only) found both route-back lists missing the open-PR-thread case. Fixed, and the same reader confirmed both now match.
- review return 2: two review findings fail what the up-front path does. The step-8 red-CI fix re-enters step 7's up-front check and can merge with no question, against AC3 (diff-bug #1). The guard's slot read can run past the hook's 15-second timeout through `git ls-remote` and leave the merge unguarded (blame-history #5). The other fix-now findings of pass 2 are in the Review section, marked "fix now".
- amendment return: AC5 — "Three surfaces state the up-front approval and the cases that go back to the merge question: the approval bullet of the git model in `skills/shared/tracking-rules.md`, "Merges are yours" in `README.md`, and a `CHANGELOG.md` entry. `skills/shared/templates/claude-md-section.md` and the cairn section of `CLAUDE.md` state the up-front approval and point to the rulebook's approval bullet for the cases, each within the 30-line section cap. The verify slot passes as in AC7 of M202."
- re-audit: AC5 (full) — "within the 30-line section cap" is ambiguous at 30 against the strict `< 30` cap, and it binds the template's line count, a property the old AC5 did not bind (a widening under D-118); fixed by dropping the cap clause, since `cairn_validate` already enforces the CLAUDE.md cap.
- re-audit: AC5 (full) — requiring a pointer on the two routing surfaces binds a property the old AC5 did not, so it is a substitution, not a pure narrowing (D-118); proposed "state the up-front approval and either list the cases or point to the rulebook's approval bullet for them".
- 2026-10-03: stop at the second re-audit of AC5 (repeated review-failure stop). Amended AC5 not yet written.
- 2026-10-03: substantive amendment: AC5 written at the user's answer as the second reader's strict narrowing. The two routing surfaces either list the cases or point to the rulebook bullet. T9 (return 2) and T10 (AC5) added, Coverage updated. The plan-owned body went to 160 lines, so the criteria section was rewrapped to 110 columns with no word changed (checked by whitespace-normalized compare) and AC5 unticked.
- 2026-10-03: T9 done. The guard resolves the default branch locally (`<base>/HEAD`, then `main`, then `master`, no `ls-remote`), reads `ls-tree -z` and `ref:./path`, and matches the slot through `slot_is_up_front`, which drops backticks and needs `up front` as words. Its docstring and DESIGN state that a chip-form marker is not checked. Six new tests cover a backtick value, `up frontier`, a zero-padded file, a non-ASCII name, an unset remote HEAD, and a cairn root in a subdirectory. Four of them failed before the fix. In review step 7, the prefix check reads `carries` and adds `ci route-back:`. The `spawned:` line must come from the current pass and name every required lens. Any PR-conversation item routes back, and route (b) never runs the up-front check. In step 8, a late push means the PR head is not the up-front line's commit, red CI writes `ci route-back:` and goes straight to the chip, and the conversation is read again before the marker. Route (c) does not push under an up-front line. The plan question names the cases that always route back. Stale "stops at the merge question" prose is fixed in README, DESIGN, and the plan and implement skills. Verify green (hooks 193 OK), and `skills/tests` shows main's 4 reds and 1 error.
- 2026-10-03: T10 done. The routing template and the CLAUDE.md section state the up-front approval and point to the rulebook's approval bullet for the cases. `claude_section_line_count` gives 28 for the template and 26 for CLAUDE.md, both under the 30 cap, and the Trivial reflow is reverted. Verify green.
- claim audit: 42 claims read, 7 corrected — skills/shared/tracking-rules.md, skills/milestone-review/SKILL.md, README.md, CHANGELOG.md, CLAUDE.md, skills/shared/templates/claude-md-section.md
- 2026-10-03: the T9/T10 claim audit (`5314538..HEAD`) found one behavior bug and six wording gaps. The bug: route (c) appended an unpushed second approval line, so a resumed up-front run always read a late push. Fixed: route (c) appends none. Step 8 writes `step-8 route-back:` for red CI, a late push, or a conversation item, and step 7 reads it. The rulebook bullet lists the T9 cases and the late-push definition. The README and CHANGELOG name the read's items. The same reader confirmed all seven. Verify green, and `skills/tests` shows main's 4 reds and 1 error.
- review return 3: two pass-3 findings fail what the up-front path does. Step 8's up-front arm keys on any up-front line, so a chip approval after a route-back loops (diff-bug #1, AC3). A default branch that moves before a resume is not logged, so a later resume can merge an unverified tree unattended (diff-bug #3).
- 2026-10-03: stop at the thrash rule. Trigger (a): this is the third defect return. Trigger (b): AC3 has failed in three passes by three mechanisms (the end-of-run list at a stop, the red-CI re-entry, the approval-line keying and the moved default branch).
- 2026-10-03: thrash stop answered: the user chose to escalate the up-front state machine via `/milestone-brief` before any more fixes, over the recommended one-pass descope.
- 2026-10-03: blocked on RB16. The brief is committed on this branch, as RB15 was, because the milestone's state lives on the branch.
- 2026-10-03: RR16 ingested (Fable, advisory, 12 recommendations). Apply: recs 1 to 6, through T11's amendment stop, because rec 1 narrows AC3 and changes what the user sees. Consider: rec 7 (pose the plan's merge question only when a plan has an internal, IP-free milestone) and rec 8 (a `resume:` line on routes (c) and (d)) go to the follow-on row. Rec 9 (removal) is the fallback offered at T11 and named for the next AC3 return. Rejected as RR16 reasons: rec 10 (the script leaves the writers in prose), rec 11 (new pass-id or base-oid writers are the mechanism of all three returns), and rec 12 (the main/master fallback guesses).
- 2026-10-03: substantive amendment: AC3 narrowed to the one-pass rule at the user's answer to T11, as drafted from RR16 Q5. The skip runs only in an invocation that started with an empty Review section, no PR, and no `step-7 approval:` line. Step 8 runs in the same invocation, and red CI, a non-bot PR item, or any stop asks. The "PR review that requests changes" adder moves into the non-bot item rule. AC3 has two `re-audit` lines, so the user's answer settled the wording with no reader (step 6). Removal is named for the next AC3 return. T12 added, AC3 unticked.
- 2026-10-03: T12 done. D-146 records the one-pass rule, the rulebook's single route-back list, the bot rule, the D-138 narrowing, and the guard's `<base>/HEAD`-only read. Review step 7's check now runs only in a first-pass invocation, and step 8's arm is entered by control flow. Route (c)'s up-front branch, `step-8 route-back:`, the late-push detector, and "this pass" are gone. Step 1 runs `git remote set-head <base> -a`. The pass-3 one-line fixes are in: `fixed <sha>` suffix, lens slugs, cairn-root `git show` paths, a `%H` plan recipe, "carries" in implement, and the template header. README and CHANGELOG keep their case lists because AC5 requires them, synced to the narrowed list, which departs from RR16 rec 4. The plan question points to the rulebook list. The guard denies an unset remote HEAD, and its test was flipped (red before the change). Verify green (hooks 193 OK), and `skills/tests` shows main's 4 reds and 1 error.
- claim audit: 55 claims read, 4 corrected — skills/milestone-review/SKILL.md, skills/shared/tracking-rules.md, README.md, CHANGELOG.md
- 2026-10-03: T12 claim-audit fixes. The end-of-run lists include `conversation:` lines, and the thread query selects author `__typename`. The rulebook reads "a `Resolves:` slot other than `—`". A bot item disposed fix-now is fixed as red CI is and then asks, which keeps D-146's "never routes back" true of the item's presence. The same reader confirmed all four. One edit broke a pinned prose-guard phrase, and the restore followed the M148 lesson: the pinned sentence is kept and a new sentence added. Verify green, and `skills/tests` shows main's 4 reds and 1 error.
- review return 4: two pass-4 findings fail AC3's one-pass path. A failed merge retried after a push can merge an unreviewed tree unattended (diff-bug #1). A chip approval re-enters the up-front arm and loops (diff-bug #4).
- 2026-10-03: stop at the thrash rule (fourth defect return, AC3 failing a fourth time). D-146's falsifier and the user's T11 answer name removal of the up-front path for this case, with no further brief.
- 2026-10-03: thrash stop answered: the user chose to remove the up-front path and re-cut M203. The goal is wrong as planned, so the status returns to `planned` for `/milestone-plan`. The re-cut keeps RR16 Q4's list: the finding-line and `spawned:` shapes and the `step-7 decline:` and `substantive amendment:` prefixes. It drops the `Merge approval:` slot, the guard's slot read, the end-of-run list, and the IP1 change, and a new D-entry supersedes D-145 and D-146. The branch `m203-merge-approval-up-front` stays as the record and the source for the kept parts.

## Decisions

- 2026-10-03 (RR15 Q1): An up-front answer approves the promise as the plan commit carries it, not the code. It satisfies IP1 only if that promise merges unchanged and the cases where the merge question adds information go back to it. The 323-to-1 figure was measured with the read in place. The real gain is an unattended run, because CI waits on the approval (D-138).
- 2026-10-03 (RR15 Q2, Q6): Six cases pass AC3 as written. The agent rejects a real finding as false. The agent makes a substantive amendment that it judges wording only. The agent narrows the scope. A plan chains several milestones. The review is degraded, with no spawned reviewers. The diff rewrites the gate machinery or an IP. A self-fixed defect return is an acceptable risk. The fix is to send each of these cases back to the merge question.
- 2026-10-03 (RR15 Q3): The approval binds each milestone, not the plan. One question can answer for several ids and lets the user hold any of them `at the end`. A re-cut asks again.
- 2026-10-03 (RR15 Q4): The marker was always written by the agent. The guard's PR regex already accepts the `up front` form, so AC4's test is a regression guard. A stronger tie would have the guard read the milestone's `Merge approval:` slot from the base remote's default branch, with the marker and the work-log line citing the plan commit.
- 2026-10-03 (RR15 Q5): RR15 recommends the IP1 wording "Nothing reaches the default branch without the user's explicit approval at a gate of the run: at the merge question, or in the plan question set for a milestone whose promise, as that plan committed it, then merges unchanged and with every check of the run passed." It rejects a D-entry alone with IP1 unchanged. It does not recommend dropping the up-front path, but only if recommendations 1 to 5 ship with M203.
- 2026-10-03 (RR16 Q1): The skip rests on non-monotone predicates ("newest approval line", "this pass", "moved since") read over an append-only log. Four readers key the approval line four ways, and three facts the readers need (pass identity, base oid at evidence time, "fixed") have no writer. The route-back list is enumerated by hand in six places. The design as written is an open set.
- 2026-10-03 (RR16 Q2): A verifiable full design needs every predicate monotone, with the approval line one-shot. A script could compute "may skip", but it leaves the writers in prose, so the drift stays. Rejected for now.
- 2026-10-03 (RR16 Q3): The one-pass rule removes pass-3 diff-bug #1 to #3 and blame #4 by construction. The up-front check runs only in an invocation that starts with an empty Review section and no PR for the branch, and step 8's arm is entered by control flow only. Checkable from three monotone facts at the start. Cost: a CI run longer than the foreground ceiling stops, and the resume asks.
- 2026-10-03 (RR16 Q4): Under removal, keep only the finding-line and `spawned:` shapes and the `step-7 decline:` and `substantive amendment:` prefixes. In this repo, with no CI, removal costs the user's presence at each milestone end and no unattended chaining. Nearly every milestone here is user-facing, where the plan question recommends `at the end`, so the skip's domain here is small.
- 2026-10-03 (RR16 Q5): RR16 recommends the one-pass narrowing, with removal as the fallback if the next review pass returns on AC3 again or the user judges the domain too small. AC1, AC2, AC4, and AC5 hold, and AC3 narrows. Narrowing the skip's domain (more cases ask) is not a narrowing of a route-back case.
- 2026-10-03 (RR16 Q6): Only non-bot PR conversation items route back (author `type`, as M177's blocking rule), and bot items are logged and listed. The read after CI on a fresh PR takes a rejected D-138 alternative, so a D-entry narrows D-138 for it.
- 2026-10-03 (RR16 Q7): For an unset `<base>/HEAD`, the guard denies and names `git remote set-head <base> -a`, and review step 1 runs that command with its fetch. The main/master fallback is a guess the rulebook forbids.

## Review

- AC1 evidence (2026-10-03): `cairn/DESIGN.md:199-203` IP1 keeps "Nothing reaches the default branch without explicit user approval at a gate" and adds the merge question and the plan question set for a milestone whose promise merges unchanged and meets no route-back case. D-145 (DECISIONS.md) records the user decision at the 2026-10-03 gate, states the approval "comes before the diff exists", calls the route-back cases "the mechanism that keeps that promise unchanged", says removing or narrowing a case changes IP1, narrows D-138 and D-144, and annotates D-043, each found by grep. Pass.
- AC2 evidence (2026-10-03): `skills/shared/templates/milestone.md:14` carries `- **Merge approval:** at the end`. `skills/milestone-plan/SKILL.md` step 3 lists merge approval with one answer per milestone, lets the user hold any `at the end`, says a run with no route-back case merges with no further question and its code and dispositions are seen only after the merge, and recommends `at the end` for a user-facing or IP-touching milestone. Step 4 (line 328) writes `up front YYYY-MM-DD` or `at the end`, writes `at the end` when the set did not pose the question, and asks again on a re-cut. Review step 7 (line 389) reads `—` or a missing slot as `at the end`. The guard treats both the same as `at the end`: `test_denies_slot_dash`, `test_denies_missing_slot`, and `test_denies_slot_at_the_end` pass. Pass.
- AC3 evidence (2026-10-03): `skills/milestone-review/SKILL.md` step 7 (lines 386-415) carries each route-back check of AC3: it reads the default-branch slot, compares Goal, Scope, and criteria with the plan commit's apart from ticks, checks the `substantive amendment:`/`amendment return:`/`step-7 decline:` prefixes and the evidence lines, finds no unfixed fix-now and no `#1` or user-facing reject as false, and reads the `spawned:` line, the IP slot, the `### D-` diff, and the step-7 adders. It commits `step-7 approval: <branch> approved up front per plan <sha>` before step 8's push. The step-8 up-front arm (lines 574-585) writes `M<NNN> approved up front YYYY-MM-DD per plan <sha> for PR #<N>` only after green CI or the no-checks case with no push after the PR opened, and sends red CI to the merge question. Steps 7 (line 441-447) and 10 (line 749) carry the end-of-run list. FAIL on one clause: "The close block or merge question that ends the run lists each milestone merged up front in the run". A run that merged a milestone up front and then ends at a stop ends with a close block that carries no such list: an implement stop, a review CI timeout, or a thrash stop of a later milestone. Only step 10's close and step 7's merge question carry it.
- AC4 evidence (2026-10-03): `hooks/merge_guard.py:3-6` (docstring) and its missing-marker deny (line 149) name the merge question and the plan question set. The up-front branch reads the slot through `cairn_common.default_branch_merge_slot` at `refs/remotes/<base>/<default>`, denies on an unread ref, file, or slot or a value other than `up front`, and names the value read (or why none) and its source. `python3 -m unittest discover -s hooks/tests -k UpFront`: 13 tests OK. They cover the allow case, a denial for another PR, `at the end`, `—`, a missing slot, working-tree-only, local-default-branch-only, no remote-tracking ref, an absent file, and another milestone's slot, plus the legacy marker. During T4, three planted defects each turned their target test red. Pass.
- AC5 evidence (2026-10-03): the approval bullet of `skills/shared/tracking-rules.md` and "Merges are yours" in `README.md` state the up-front approval and list the route-back cases, and the `CHANGELOG.md` Unreleased entry does too. Verify, as in M202 AC7: `scripts/tests` 395 OK (21 skipped), `hooks/tests` 187 OK, `claude plugin validate` passed with warnings, `claude plugin test .` 632 pass and 0 fail, each exit 0. FAIL on two surfaces: `skills/shared/templates/claude-md-section.md` and the cairn section of `CLAUDE.md` state the up-front approval but name the cases only as "any route-back case". They do not state the cases.
- Consistency gate (2026-10-03): `cairn_validate` all checks passed (exit 0). IP1 changed, so `cairn_impact.py IP1` ran and listed 34 references. The DECISIONS, archive, and M203 references are history or this milestone. One live reference is unreconciled: `cairn/DESIGN.md:61-63` describes `merge_guard` as bound to the PR it approves and does not name the default-branch slot read for an up-front marker. The `generic` profile names no toolchain checks.
- Pass 2 (2026-10-03, after review return 1). `origin/main` has not moved. AC3 evidence: the step 7 and step 8 text recorded above stands. The failed clause now holds at every run-ending close. The rulebook's close-block shape (`skills/shared/tracking-rules.md:417-419`) carries the end-of-run list at whichever stop or skill ends the run. Implement step 8 (`skills/milestone-implement/SKILL.md:233-234`) carries it at an implement stop. Review step 10 (`skills/milestone-review/SKILL.md:749-754`) carries it at step 10's close and at a CI timeout, decline, or thrash stop. Step 7 (line 441-447) carries it at the merge question. Pass.
- Pass 2 AC5 evidence: `skills/shared/templates/claude-md-section.md:20-26` and the cairn section of `CLAUDE.md` (29 lines) now state the up-front approval and list the route-back cases. The T8 claim audit read the list against review step 7 and step 8 and found every case after one fix. The tracking-rules bullet, README, and CHANGELOG stand as recorded above. Verify: `scripts/tests` 395 OK (21 skipped), `hooks/tests` 187 OK, `claude plugin validate` passed with warnings, `claude plugin test .` 632 pass and 0 fail, each exit 0. Pass.
- Pass 2 consistency gate: `cairn_validate` all checks passed. The one live IP1 reference from pass 1, `cairn/DESIGN.md:61-64`, now names the slot read for an up-front marker. The other `cairn_impact.py IP1` references are history or this milestone. Pass.
- spawned: diff-bug (Opus), blame-history (Sonnet), prior-review (Sonnet)
- diff-bug #1: after red CI the fix push re-enters step 7's up-front check, which can pass and merge with no question; step 8's exemption hides the push. — fix now (floor: AC3's "If CI is red or a fix is pushed, it asks the merge question" fails as executed)
- diff-bug #2: route (c) pushes the unpushed PR-URL commit, so an up-front resume always reads "pushed after the PR opened". — fix now
- diff-bug #3: step 8's "after this step's push" exemption is narrower than the rulebook's route-back case. — fix now (one definition: the PR head is the commit that added the up-front approval line)
- diff-bug #4: an older pass's `spawned:` line satisfies the check after a later author-inline pass, and a partial fan-out passes too. — fix now
- diff-bug #5: on a fresh PR, nothing reads the PR conversation before an unattended merge. — fix now (read after green CI, before the marker)
- diff-bug #6: step 7 does not order the PR-conversation read before the up-front check. — fix now
- diff-bug #7: "opens `substantive amendment:`" misses a dated line. — fix now ("carries")
- diff-bug #8: the plan question promises an unattended merge where guest mode, an IP, a `Resolves:` slot, or a companion always routes back. — fix now
- diff-bug #9: the guard denies a slot value wrapped in backticks. — fix now
- diff-bug #10: a cairn root in a repo subdirectory denies every up-front merge (`git show ref:path` is root-relative). — fix now
- diff-bug #11: `ls-tree` without `-z` quotes non-ASCII filenames, which then fail to match. — fix now
- diff-bug #12a: a chip-form marker skips the slot read, and DESIGN, README, and the docstring overstate the guard. — fix now (state the limit)
- diff-bug #12b: no tests for a zero-padded id, guest `upstream`, or a `cd`-target repo. — fix now for the zero-padded id; follow-up for guest and `cd`-target (row "Up-front merge approval follow-ons")
- diff-bug #12c: "a Fable shortfall" names the Driving RR case differently from step 7. — reject (style: plain words for readers of the routing surfaces)
- blame-history #1: the routing template's section is 33 lines, against the 30-line cap `cairn_validate` applies to an adopter's CLAUDE.md (27 on main). — fix now, through an amendment return of AC5 (the cap makes the list unreachable there)
- blame-history #2: resume route (b) would run the up-front check and skip its post-hoc acceptance chip. — fix now
- blame-history #3: same as diff-bug #12a. — fix now (as #12a)
- blame-history #4: no resolvable default branch denies every up-front merge. — fix now (local fallback, with #5)
- blame-history #5: the slot read can call `git ls-remote` plus three 10-second git calls, past the hook's 15-second timeout, leaving the merge unguarded. — fix now (floor: a guard that can time out open is a defect in what the hook does)
- blame-history #6: same as diff-bug #5. — fix now (as diff-bug #5)
- blame-history #7: same as diff-bug #2. — fix now (as diff-bug #2)
- blame-history #8: stale prose says the run always ends at the merge question (README 251 and 323, DESIGN 36-38, plan 140 and 395, implement 254). — fix now for those sites
- blame-history #9: the CLAUDE.md Trivial reflow is noise. — fix now (revert once the amended AC5 shortens the list)
- prior-review #1: stale "merge question" sentences (M112 lesson). — fix now for the sites in blame-history #8; reject the rest as false (tracking-rules "two gates" and review's "second gate" stay true, because the plan question set is the other gate, and the README mermaid label names the default path)
- prior-review #2a: an unreadable marker falls back to the existence check and is consumed (M100). — follow-up (changes M72's deliberate legacy fallback; row "Up-front merge approval follow-ons")
- prior-review #2b: `startswith("up front")` accepts `up frontier`. — fix now (with diff-bug #9)
- prior-review #3: the rulebook-size baseline is not re-seeded (M149). — follow-up (already in the "Run edge cases" row, M202 F4)
- prior-review #4: `COMMENTED` reviews and conversation comments neither route back nor reach the end-of-run list (M177). — fix now (any item in the read routes back)
- Pass 3 (2026-10-03, after return 2 and the AC5 amendment return). `origin/main` has not moved. AC3 evidence: step 7 (`skills/milestone-review/SKILL.md` lines 386-425) carries every route-back check of AC3. The amendment check is the plan-commit diff plus the `substantive amendment:`/`amendment return:`/`step-7 decline:`/`step-8 route-back:` lines. The `spawned:` check needs the current pass with every required lens, and the step-7 adders include any PR-conversation item. It commits `step-7 approval: <branch> approved up front per plan <sha>` before step 8's push. The step-8 up-front arm writes `M<NNN> approved up front YYYY-MM-DD per plan <sha> for PR #<N>` only after green CI or the no-checks case, with no late push (the PR head is the approval-line commit) and an empty PR-conversation read. Red CI, a late push, or a read item writes `step-8 route-back:` and poses the chip. The end-of-run list holds at step 7, step 10, and every run-ending close (rulebook close-block shape, implement step 8). Pass.
- Pass 3 AC4 evidence: `python3 -m unittest discover -s hooks/tests -k UpFront` runs 19 tests, all OK. That covers each allow and deny case AC4 names, plus a backtick value, `up frontier`, a zero-padded file, a non-ASCII name, an unset remote HEAD, and a subdirectory cairn root. The docstring and missing-marker deny name both gates, and a slot deny names the value read, or why none, and its ref and path. Pass.
- Pass 3 AC5 evidence (amended AC5): the rulebook's approval bullet (`skills/shared/tracking-rules.md:240-250`), README "Merges are yours" (line 424), and the CHANGELOG Unreleased entry (line 91) state the up-front approval and list the cases. `skills/shared/templates/claude-md-section.md:20-21` and `CLAUDE.md:27-29` state the up-front approval and point to "the rulebook's approval bullet". Section lengths are 28 and 26 lines. Verify: `scripts/tests` 395 OK (21 skipped), `hooks/tests` 193 OK, `claude plugin validate` passed with warnings, `claude plugin test .` 632 pass and 0 fail, each exit 0. Pass.
- Pass 3 consistency gate: `cairn_validate` all checks passed. `cairn/DESIGN.md`'s `merge_guard` line names the slot read and its limit. Pass.
- spawned: diff-bug (Opus), blame-history (Sonnet), prior-review (Sonnet) — pass 3
- diff-bug #1: step 8's up-front arm keys on any up-front line, not the newest approval line, so a chip approval after a route-back loops on a late push, and step 7 and step 10 list a chip merge as "merged up front". — fix now (floor: AC3 "In every other case it asks the merge question as before" fails as executed)
- diff-bug #2: the `spawned:` line carries no pass id, so the "this pass" check cannot be read on resume route (c). — fix now
- diff-bug #3: a moved default branch on resume (c) writes no work-log line, so the next resume can merge unattended without step 3 re-run. — fix now (floor: an unattended merge of an unverified tree)
- diff-bug #4: "no fix-now finding left unfixed" has no writer, because the line shape never records the fix. — fix now
- diff-bug #5: lens names have no fixed slug (`prior-review` against "Prior-PR-comments reviewer"). — fix now
- diff-bug #6: the skill's `git show` paths are git-root-relative, so a subdirectory cairn root fails the slot read. — fix now
- diff-bug #7: step 7 cites step 10's plan-commit recipe, which prints subjects only, not the sha. — fix now
- diff-bug #8: any bot comment routes an up-front run back. — fix now (state it in the plan question)
- diff-bug #9: README and CHANGELOG omit the moved-default-branch case. — fix now
- diff-bug #10: a stale `<base>/HEAD` target denies without trying main or master. — follow-up (safe direction; row "Up-front merge approval follow-ons")
- diff-bug #11: the 2026-10-03 "substantive amendment of AC1 to AC4" line lacks the colon. — reject (false as a defect: the line is history under IP4, and the plan-commit diff check catches the change it records)
- blame-history #1: the read after green CI on a fresh PR reverses a path D-138 rejected, and D-145 does not narrow that clause. — fix now (a D-entry)
- blame-history #2: routing back on every comment, bots included, widens M177's grading beyond D-145's list. — fix now (record it with blame-history #1)
- blame-history #3: the main/master fallback guesses the default branch against the canonical recipe. — fix now
- blame-history #4: the `-S'approved up front'` pickaxe can pick a later commit that quotes the phrase. — fix now (key on the full `step-7 approval: <branch> approved up front` text)
- blame-history #5: README and CHANGELOG omit the `spawned:` and moved-default cases. — fix now (as diff-bug #9)
- blame-history #6: implement step 6 still says the line "opens" the prefix. — fix now
- blame-history #7: the template's header still says "~25 lines" at 28. — fix now
- prior-review #1: README and CHANGELOG omit the moved-default case (M112). — fix now (as diff-bug #9)
- Pass 4 (2026-10-03, after return 3, RR16, and the AC3 amendment). `origin/main` has not moved, and `git remote set-head origin -a` ran with the fetch. AC3 evidence (amended AC3): step 7 (`skills/milestone-review/SKILL.md:390-430`) runs the up-front check only in a first-pass invocation, one that started with an empty Review section, no PR, and no `step-7 approval:` line. It reads the default-branch slot and carries each AC3 check: plan-commit diff, the amendment and decline prefixes, evidence ticks, fix-now `fixed <sha>`, `#1` and user-facing rejects, `spawned:`, IP and `### D-`, and the step-7 adders without the PR-review adder. It commits `step-7 approval: <branch> approved up front per plan <sha>` before step 8's push and goes to step 8 in the same invocation. Step 8's arm (line 593) writes `M<NNN> approved up front YYYY-MM-DD per plan <sha> for PR #<N>` only after green CI or the no-checks case and a read with no non-bot item. Red CI, a non-bot item, or a CI-ceiling stop poses the chip, and route (c) never skips it. The end-of-run list holds at step 7 (line 463), step 10, implement step 8 (line 234), and the rulebook close-block shape (line 423). Pass.
- Pass 4 AC4 evidence: `python3 -m unittest discover -s hooks/tests -k UpFront` runs 19 tests, all OK. They include each case AC4 names, with `test_denies_without_remote_tracking_ref` and `test_denies_when_remote_head_is_unset` for an unreadable ref, and `test_legacy_marker_reads_no_slot`. Pass.
- Pass 4 AC5 evidence: the rulebook approval bullet (the one list), README "Merges are yours", and the CHANGELOG entry state the up-front approval and the narrowed cases. The routing template and CLAUDE.md point to the rulebook bullet. Verify: `scripts/tests` 395 OK (21 skipped), `hooks/tests` 193 OK, `claude plugin validate` passed with warnings, `claude plugin test .` 632 pass and 0 fail, each exit 0. Pass.
- Pass 4 AC1 note: IP1 now cites D-145 and D-146, and the AC1 clauses recorded in pass 1 stand. Consistency gate: `cairn_validate` all checks passed (one sizing advisory, 12 tasks). Pass.
- spawned: diff-bug (Opus), blame-history (Sonnet), prior-review (Sonnet) — pass 4
- diff-bug #1: step 8's "if a merge fails and is retried, rewrite the marker" applies on the up-front arm, so a failed merge, a default-branch merge-in, and a push can merge an unreviewed tree with no question, and D-146's "the only push after the PR opens is a red-CI fix" is false. — fix now (floor: an unattended merge of an unreviewed tree, AC3)
- diff-bug #2: bot `conversation:` lines written after CI have no stated path into the squash, so the end-of-run list read at the merge commit misses them. — fix now
- diff-bug #3: "merged up front" is still keyed on the presence of the up-front line, so a chip merge after a route-back is listed as up front (pass-3 diff-bug #1, second half). — fix now
- diff-bug #4: the arm's entry condition stays true after the arm posed the chip, so a chip approval re-enters the arm and re-poses the chip without end. — fix now (floor: the run never finishes, AC3)
- diff-bug #5: the first-pass fact is observable only at session start, and nothing records it. — fix now
- diff-bug #6: a `review return` written before any Review line leaves the next invocation a first pass, against "any return asks" on four surfaces. — fix now
- diff-bug #7: the rulebook says "pass" where step 8 says "invocation". — fix now
- diff-bug #8: the rulebook's close-block list omits `conversation:` lines. — fix now
- diff-bug #9: README and CHANGELOG do not say a partial reviewer set routes back. — fix now
- diff-bug #10: "an empty Review section" is undefined against the template comment. — fix now
- diff-bug #11: up to five 10-second git calls inside the 15-second hook timeout. — follow-up (row "Up-front merge approval follow-ons")
- blame-history #1: same as diff-bug #3. — fix now (as diff-bug #3)
- blame-history #2: a failed `set-head` in step 1 has no route, and an unset ref is first seen at the guard after the marker. — fix now
- blame-history #3: the bot test is worded three ways (`__typename`, `type`, `user.type`). — fix now
- blame-history #4: same as diff-bug #8. — fix now (as diff-bug #8)
- blame-history #5: the `step-7 decline:` prefix and its "so a later pass asks again" sentence are redundant under the one-pass rule. — fix now
- blame-history #6: the plan-commit recipe leaves the id match to the reader and reads the local default branch. — fix now
- prior-review #1: the plan question does not say bot items are listed after the merge and do not stop it. — fix now
