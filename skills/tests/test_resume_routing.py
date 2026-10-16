"""Prose guard: a merged or stopped review milestone resumes at the right
step (M172).

A review session that stopped at the CI wait, or whose PR was merged
outside the session, once re-entered at step 1 and pushed a deleted branch;
post-merge hygiene was skipped by accident. M172 gives `/milestone-review`'s
Session start a four-way resume route read off the header PR's state and
the Review section, `/milestone`'s audit a merged-but-`review` bullet, and
`/hotfix` step 1 a merged-PR re-entry. Each is pinned here and registered
in the mutation harness.

The route list is pinned whole — every branch (a)–(d), never its head
(M171 lesson) — and the list runs across many wrapped lines, so it is read
with whitespace collapsed (`re.sub(r"\\s+", " ", …)`): the deliberate
exception to the one-physical-line anchor convention. Targets are read with
`Path.read_text` because the mutation engine patches only that call (M100).
Hand-run only (M144, D-109):

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def flat(text):
    return re.sub(r"\s+", " ", text)


def section(text, start, end):
    """The slice of `text` between the first `start` and the next `end`."""
    return text.split(start, 1)[1].split(end, 1)[0]


class TestReviewResumeRoute(unittest.TestCase):
    """AC1: `/milestone-review`'s Session start reads the header PR's state
    before step 1 and routes on it and the Review section — all four
    branches present, in full."""

    def setUp(self):
        self.route = flat(section(read("milestone-review", "SKILL.md"),
                                  "**Resume routing (M172).**",
                                  "## Workflow"))

    def test_reads_pr_state_before_step_one(self):
        self.assertIn(
            "read that PR's state before step 1 — `gh pr view <N> --json "
            "state,mergedAt` (N from the URL or the list)",
            self.route,
        )

    def test_route_a_merged_and_reviewed_goes_to_step_nine(self):
        self.assertIn(
            "(a) `MERGED`, every acceptance-criterion box ticked against a "
            "recorded evidence line, and a work-log line recording step-7 "
            "approval (read by its prefix, `step-7 approval: …`) → append "
            "one work-log "
            "line naming the PR, its `mergedAt` value, and the re-entry "
            "(`resume: PR #<N> merged <mergedAt>; re-entering at step 9`), "
            "then steps 9–10 with steps 1–8 skipped — the recorded approval "
            "stands as step 9's issue-write authorization.",
            self.route,
        )

    def test_route_b_merged_unreviewed_verifies_post_hoc(self):
        self.assertIn(
            "(b) `MERGED` otherwise (a box unticked or unevidenced, or no "
            "approval line) → the same work-log line with step 3 as its "
            "re-entry step, plus a chat statement that verification never "
            "ran before the merge; then steps 3–7 executed against the "
            "merged default-branch head (check it out and pull; "
            "Review-section evidence and the step-6 checkpoint land by "
            "docs-only commit; step 5's reviewers read the merged PR's diff "
            "— `gh pr diff <N>` — in place of the branch diff; fix-now code, "
            "a step-4 gate failure, and a floor return go through `/hotfix`, "
            "never a commit on the default branch and never a return to "
            "`/milestone-implement`), "
            "step 7's chip posed with question text naming acceptance of "
            "the post-hoc verification and the issue writes it authorizes, "
            "its recommended option accepting that verification rather than "
            "merging — a decline logs the requested changes as tasks and "
            "sets status `in-progress` (step 7's decline exit); on "
            "acceptance, steps 9–10 with step 8 skipped.",
            self.route,
        )

    def test_route_c_open_and_approved_reposes_the_gate(self):
        self.assertIn(
            "(c) `OPEN`, every box ticked against a recorded evidence line, "
            "and a recorded approval → step 1 re-run and the branch pushed "
            "(when the default branch had moved, step 3 re-run so the "
            "evidence matches the merged tree), the step-7 chip re-posed, "
            "and on approval step 8 skipping `gh pr create` — the header "
            "already names the open PR — from the push and the marker "
            "write onward.",
            self.route,
        )

    def test_route_d_everything_else_goes_to_step_one(self):
        self.assertIn(
            "(d) any other state, or a state above whose conditions are not "
            "met → step 1, then the review with the post-approval open at "
            "step 8 skipping `gh pr create` when the header already names "
            "an open PR. A `gh` that is missing, "
            "unauthenticated, or has no remote → step 1, the recap naming "
            "which of the three it was.",
            self.route,
        )

    def test_step_seven_records_the_approval_line(self):
        step7 = flat(section(read("milestone-review", "SKILL.md"),
                             "7. **The merge question.**",
                             "8. **On approval"))
        self.assertIn(
            "Approval appends one work-log line naming the branch it "
            "approved (`step-7 approval: <branch> approved for merge`)",
            step7,
        )


class TestReviewArchivedFileArm(unittest.TestCase):
    """M246 AC5 (amended): in guest mode, Session start accepts a `blocked`
    row whose path is not a regular file and whose one archive file reads
    done. Owner mode and other rows stop. The arm runs a named list of
    step 9's parts, writes nothing to the archive, and makes no issue
    write."""

    def setUp(self):
        text = read("milestone-review", "SKILL.md")
        self.arm = flat(section(text,
                                "**Archived-file arm (M246, D-159).**",
                                "**Resume routing (M172).**"))
        self.start = flat(section(text, "## Session start",
                                  "**Archived-file arm (M246, D-159).**"))

    def test_status_rule_names_the_exception(self):
        self.assertIn("except under the archived-file arm below.", self.start)

    def test_trigger_is_a_missing_path_and_one_done_archive(self):
        self.assertIn(
            "The target's ROADMAP path is not a regular file, and exactly one "
            "file under `cairn/milestones/archive/` has its canonical id (any "
            "zero-padding) and a `**Status:**` paragraph",
            self.arm,
        )
        self.assertIn("spaces and tabs or the end of the file) that starts with `done`.", self.arm)
        self.assertIn("the archived file, under the archived-file arm below", self.start)

    def test_skips_steps_one_to_eight_and_ends_at_step_ten(self):
        self.assertIn("Resume routing below does not run. Skip steps 1 to 8.", self.arm)
        self.assertIn(
            "Name a cap breach or a `cairn_validate.py` FAIL in the recap, "
            "with no prune, and go on to step 10.",
            self.arm,
        )

    def test_owner_mode_and_other_rows_stop(self):
        self.assertIn("In owner mode, or when the row is not `blocked`, stop there.", self.arm)
        self.assertIn("In guest mode with a `blocked` row, the target is accepted", self.arm)

    def test_runs_only_the_named_step_nine_parts(self):
        self.assertIn(
            "Of step 9, run only these parts: the default branch's fetch, "
            "checkout, and fast-forward (its guest arm), the ROADMAP row "
            "update to `done` with the archive path, the hygiene stamp, the "
            "cap and budget checks, the hand-run prose guards where the repo "
            "ships them, and `cairn_validate.py`.",
            self.arm,
        )

    def test_writes_nothing_to_the_archive_and_no_issue(self):
        self.assertIn(
            "Write nothing to the archive file, capture or retire no lesson, "
            "and archive no RB/RR pair",
            self.arm,
        )
        self.assertIn("Make no issue write", self.arm)
        self.assertIn(
            "names each `partial` entry of the archive's `resolves` clause as "
            "an owed comment, and each `closes` entry as left to the "
            "maintainers' merge, whose `Closes` keyword closes it",
            self.arm,
        )


class TestMilestoneAuditMergedReview(unittest.TestCase):
    """AC3: `/milestone`'s audit reports a `review` milestone whose header
    PR is merged as post-merge hygiene owed, beside the open-PR bullet."""

    def setUp(self):
        self.raw = read("milestone", "SKILL.md")
        self.audit = flat(self.raw)

    def test_merged_review_milestone_is_hygiene_owed(self):
        self.assertIn(
            "- A milestone at `review` whose header PR reports `MERGED` "
            "(`gh pr view <N> --repo <base-repo> --json state`; a header naming "
            "only the branch is resolved with `gh pr list --repo <base-repo> "
            "--head <branch> --state all`, the "
            "PR having been opened after approval and its record left "
            "unpushed — `/milestone-review` step 8) → post-merge hygiene "
            "owed: report it as such and route to `/milestone-review M<NNN>`",
            self.audit,
        )

    def test_bullet_sits_beside_the_open_pr_bullet(self):
        open_pr = self.raw.index("- A milestone at `review` with an open "
                                 "unmerged PR")
        merged = self.raw.index("- A milestone at `review` whose header PR "
                                "reports `MERGED`")
        between = self.raw[open_pr + 1:merged]
        # No other bullet starts between the two: they are adjacent.
        self.assertNotIn("\n- ", between)


class TestHotfixMergedPrReentry(unittest.TestCase):
    """M172 AC4, rewritten at M174: `/hotfix` step 1's merged-PR re-entry
    runs a post-hoc verification of the merged diff before step 7 — never
    step 7 alone. Each move is pinned as a whole passage, whitespace
    collapsed (M171 lesson)."""

    def setUp(self):
        self.step1 = flat(section(read("hotfix", "SKILL.md"),
                                  "1. **Tier check first.**",
                                  "2. **Branch"))

    def test_merged_pr_runs_posthoc_verification(self):
        self.assertIn(
            "A PR-reference argument whose `gh pr view <N> --json "
            "state,headRefName` reports `MERGED` and a head branch not "
            "matching `m<nnn>-*` (a hotfix branch or an adopted PR, merged "
            "outside the session or after a stopped CI wait) states in chat that "
            "the hotfix bar never ran before this merge, then runs a post-hoc "
            "verification of the merged diff before step 7",
            self.step1,
        )
        self.assertNotIn("runs step 7 only", self.step1)
        self.assertNotIn("steps 2–6 skipped", self.step1)

    def test_baseline_is_base_ref_oid_never_the_default_branch(self):
        self.assertIn(
            "The pre-fix baseline is the oid `gh pr view <N> --json "
            "baseRefOid` reports, cross-checked against the merge commit's "
            "first parent (`gh pr view <N> --json mergeCommit --jq "
            ".mergeCommit.oid`, then `git rev-parse <oid>^`); a disagreement "
            "is stated in "
            "chat, `baseRefOid` governing. The current default branch is "
            "never the baseline: it already carries the fix, so a test "
            "passes on both and proves nothing.",
            self.step1,
        )

    def test_two_way_check_runs_against_the_baseline(self):
        # Two passages around the guest-arm sync clause (M185), which this
        # guard does not pin (M214).
        self.assertIn(
            "a test the merged diff carries is run on the default branch, checked "
            "out and brought up to date (fetch, pull ff-only",
            self.step1,
        )
        self.assertIn(
            "), and in a "
            "throwaway worktree of the "
            "baseline created outside the repo (`git worktree add --detach "
            "/tmp/<repo>-verify <baseRefOid>`) with only the test file "
            "copied in; it must pass on the default branch and fail on the "
            "baseline. When the merged diff carries no test, or its test "
            "passes on both, author one on a `hotfix-<slug>` branch cut from "
            "the up-to-date default branch and prove it the same two ways. "
            "`git worktree remove` the worktree either way",
            self.step1,
        )

    def test_owed_items_land_through_the_pr_path(self):
        self.assertIn(
            "The regression test and the changelog entry land on the "
            "`hotfix-<slug>` branch (cut here when the regression-test move "
            "did not) and reach the default branch only through step 6's "
            "authoring variant — the approval chip, then the push and a new "
            "PR opened after that approval",
            self.step1,
        )
        self.assertIn(
            "— never by a commit to the default branch.",
            self.step1,
        )

    def test_clean_check_poses_one_acceptance_chip(self):
        self.assertIn(
            "pose one `AskUserQuestion` chip whose question text names "
            "acceptance of the post-hoc verification and, when the PR body "
            "carries a `Fixes #N` line, the issue close it authorizes (a "
            "hotfix keeps no work log to show whether step 6's chip "
            "authorized it, so it is asked once here, and the issue-close "
            "chip is not posed separately), the recommended option accepting "
            "and a decline option present. Step 7 runs only on acceptance",
            self.step1,
        )
        self.assertIn(
            "A decline stops with a close block naming the decline and the "
            "reason where the user gave one, plus a `candidate` row "
            "(search-first).",
            self.step1,
        )

    def test_over_the_bar_diff_still_reaches_step_seven(self):
        self.assertIn(
            "A diff over the hotfix bar takes the over-the-bar disposition "
            "above with no regression test demanded, and step 7's close-out "
            "still runs — the candidate row or the `/milestone-plan` next "
            "command rides in that close block; when the PR body carries a "
            "`Fixes #N` line, the issue close is put to the user as a chip "
            "before step 7 runs, never written unasked.",
            self.step1,
        )


class TestHotfixOpenPrReentry(unittest.TestCase):
    """M262 (AC2 amended): `/hotfix` step 1's open-PR re-entry. The owner
    arm resumes an approved merge at step 6's CI wait only when the marker's
    head oid is the PR's head, no review requests changes, and the row match
    equals the PR body's `Candidate row:` lines; otherwise it takes the
    walk. The resumed merge pins the head, and a refused merge stops. The
    guest arm reports and stops. Step 6 notes the head the gate shows,
    writes the marker with the head oid before the wait, merges with
    `--match-head-commit`, and its timeout close names both re-entries.
    Each trigger part and each outcome is pinned on its own (M165 lesson),
    whitespace collapsed (M171 lesson)."""

    def setUp(self):
        text = read("hotfix", "SKILL.md")
        self.step1 = flat(section(text, "1. **Tier check first.**",
                                  "2. **Branch"))
        self.step6 = flat(section(text, "6. **Approval gate:**", "7. If"))

    def test_reads_the_open_state_and_head(self):
        self.assertIn(
            "**Open-PR re-entry (M262).** A PR-reference argument whose "
            "`gh pr view <N> --json "
            "state,headRefName,headRefOid,latestReviews,author` "
            "reports `OPEN` takes one of the two arms below when its "
            "conditions hold. Any other open PR takes the tier-check walk "
            "that opens this step.",
            self.step1,
        )

    def test_owner_trigger_is_a_hotfix_marker_naming_the_pr(self):
        self.assertIn(
            "*Owner arm.* This arm runs in owner mode. Its head branch does "
            "not match `m<nnn>-*`. Step 6's merge-guard marker starts with "
            "`hotfix ` and names that PR (`for PR #<N>`).",
            self.step1,
        )

    def test_resume_needs_three_conditions(self):
        self.assertIn(
            "Quote the marker's line in chat. Make the candidate-row match "
            "above. The run resumes the approved merge only when three "
            "conditions hold. First, the marker's ` at <oid>` equals the PR's "
            "`headRefOid`. Second, no entry of `latestReviews` has the state "
            "`CHANGES_REQUESTED`, even one the user overrode at the earlier "
            "chip. Third, the match names exactly the rows that the PR body's "
            "`Candidate row:` lines name.",
            self.step1,
        )

    def test_resume_skips_to_the_wait_and_pins_the_head(self):
        self.assertIn(
            "When all three hold, say that the run resumes the approved "
            "merge. Skip the tier check, steps 2 to 5, and step 6's Copilot "
            "round arm, PR-conversation read, approval chip, and marker "
            "write. Go on at step 6's CI wait, then the merge with "
            "`--match-head-commit <oid>`, then step 7 as it runs after an "
            "approval at step 6's chip.",
            self.step1,
        )

    def test_refused_merge_stops(self):
        self.assertIn(
            "If GitHub refuses the merge because the head moved during the "
            "wait, stop with a close block that names the refusal and the "
            "PR's current `headRefOid`. Its fenced next command is `/hotfix` "
            "with the PR reference.",
            self.step1,
        )

    def test_a_failed_condition_takes_the_walk(self):
        self.assertIn(
            "When a condition fails, or the marker names no head oid, say in "
            "chat which one. Then take the tier-check walk that opens this "
            "step, which ends at step 6's "
            "chip. A decline at that chip removes the marker (step 6). If the "
            "walk stops before that chip, remove the marker too.",
            self.step1,
        )

    def test_step_six_refused_merge_stops_without_retry(self):
        self.assertIn(
            "If GitHub refuses the merge because the head no longer matches "
            "`--match-head-commit`, do not retry it and do not drop the flag, "
            "whatever the guard's restore note says.",
            self.step6,
        )

    def test_guest_arm_reports_and_stops(self):
        self.assertIn(
            "*Guest arm.* This arm runs in guest mode, for an `OPEN` PR whose "
            "head branch starts with `hotfix-`.",
            self.step1,
        )
        self.assertIn(
            "Skip the tier check and steps 2 to 7. Report the PR's number, "
            "state, and review decision",
            self.step1,
        )

    def test_guest_stop_names_the_ci_line_and_next_command(self):
        self.assertIn(
            "Its CI line says that the maintainers' CI on the PR is the check "
            "that counts. It also says that nothing waits on that CI here. "
            "Its fenced next command is `/hotfix` with the PR reference, to "
            "run after they merge.",
            self.step1,
        )

    def test_step_six_writes_the_marker_before_the_wait(self):
        self.assertIn(
            "In owner mode, on approval, the order is fixed: the push and any "
            "`gh pr create` above, then the merge-guard marker, then the CI "
            "wait, then the merge.",
            self.step6,
        )
        self.assertIn(
            "`hotfix <slug> approved YYYY-MM-DD for PR #<N> at <headRefOid>`",
            self.step6,
        )

    def test_step_six_binds_the_marker_to_the_head_the_gate_showed(self):
        self.assertIn(
            "When the gate presents the diff, note the head it shows: local "
            "`HEAD` for an authored fix not yet pushed, or the PR's "
            "`headRefOid` where a PR already exists.",
            self.step6,
        )
        self.assertIn(
            "If it differs from the head the gate showed, write no marker and "
            "stop with a close block that names the new head. Its fenced next "
            "command is `/hotfix` with the PR reference, which takes the new "
            "commits through the tier-check walk.",
            self.step6,
        )

    def test_step_six_decline_removes_the_marker(self):
        self.assertIn(
            "A decline at the chip removes any merge-guard marker that names "
            "this PR.",
            self.step6,
        )

    def test_step_six_merge_pins_the_head(self):
        self.assertIn(
            "`gh pr merge <N> --squash --delete-branch --match-head-commit "
            "<oid>`, `<oid>` the marker's head oid",
            self.step6,
        )

    def test_timeout_close_names_the_open_pr_route(self):
        self.assertIn(
            "while the PR is still open and the marker names it, step 1's "
            "open-PR re-entry resumes at this wait",
            self.step6,
        )
        self.assertIn(
            "and for a PR merged since, step 1's merged-PR re-entry verifies "
            "the merged diff post-hoc",
            self.step6,
        )


class TestHotfixClosedPrStop(unittest.TestCase):
    """M266 AC1: `/hotfix` step 1's closed-PR stop. A `CLOSED` PR whose head
    is not a milestone branch stops in both modes after the candidate-row
    match, removes only a `hotfix ` marker naming it, edits no row, and
    ends with a close block whose next command starts over. Trigger and
    each outcome are pinned on their own (M165 lesson), whitespace
    collapsed (M171 lesson)."""

    def setUp(self):
        text = read("hotfix", "SKILL.md")
        self.step1 = flat(section(text, "1. **Tier check first.**",
                                  "2. **Branch"))

    def test_trigger_is_a_closed_non_milestone_pr(self):
        self.assertIn(
            "**Closed-PR stop (M266).** A PR-reference argument whose "
            "`gh pr view <N> --json state,headRefName` reports `CLOSED`, with "
            "a head branch not matching `m<nnn>-*`, stops here in owner and "
            "guest mode.",
            self.step1,
        )

    def test_stop_skips_the_walk_after_the_row_match(self):
        self.assertIn(
            "Make the candidate-row match above, then skip the tier check and "
            "steps 2 to 7.",
            self.step1,
        )

    def test_owner_removes_only_a_hotfix_marker_naming_the_pr(self):
        self.assertIn(
            "In owner mode, remove step 6's merge-guard marker when its line "
            "starts with `hotfix ` and names that PR (`for PR #<N>`), and "
            "leave any other marker as it is.",
            self.step1,
        )

    def test_stop_comes_before_the_merged_pr_re_entry(self):
        closed = self.step1.index("**Closed-PR stop (M266).**")
        merged = self.step1.index("**Merged-PR re-entry (M172, M174).**")
        self.assertLess(closed, merged)

    def test_stop_edits_no_row(self):
        self.assertIn("The stop edits no candidate row.", self.step1)

    def test_close_block_says_closed_and_starts_over(self):
        self.assertIn(
            "End with a close block that says the PR closed without a merge "
            "and that reopening it on GitHub is the operator's choice. The "
            "close block names each matched row that ends with ` — started "
            "#<N>`, a dead token that `/cairn-triage` proposes to remove. Its "
            "fenced next command is `/hotfix` with a description of the bug, "
            "which starts over on a new branch.",
            self.step1,
        )


class TestHotfixOwnOpenPr(unittest.TestCase):
    """M266 AC2: the operator's own open `hotfix-` PR that the owner arm
    does not resume takes the walk as an authored fix whose PR exists. The
    trigger, the adopting variants, and the step 6 and step 7 exemption
    sentences are pinned on their own (M165 lesson), whitespace collapsed
    (M171 lesson)."""

    def setUp(self):
        text = read("hotfix", "SKILL.md")
        self.step1 = flat(section(text, "1. **Tier check first.**",
                                  "2. **Branch"))
        self.step6 = flat(section(text, "6. **Approval gate:**", "7. If"))
        self.step7 = flat(text.split("7. If the fix revealed", 1)[1])

    def test_trigger_is_the_operators_own_hotfix_pr(self):
        self.assertIn(
            "**Own open PR (M266).** This paragraph covers an `OPEN` PR in "
            "owner mode whose `headRefName` starts with `hotfix-` and whose "
            "`author.login` equals `gh api user --jq .login`.",
            self.step1,
        )

    def test_walk_treats_it_as_an_authored_fix(self):
        self.assertIn(
            "When the owner arm above does not resume it, the run takes the "
            "tier-check walk with it as an authored fix whose PR exists, not "
            "as an adopted PR.",
            self.step1,
        )

    def test_steps_two_three_five_take_adopting_variants(self):
        self.assertIn(
            "Steps 2, 3, and 5 take their adopting variants. Step 2 runs `gh "
            "pr checkout <N>`, step 3 runs the two-way check of the regression "
            "test, and step 5 runs the changelog check. Pushes go to the PR's "
            "head branch, and step 5's contributor fallback does not apply.",
            self.step1,
        )

    def test_copilot_round_runs_without_a_create(self):
        self.assertIn(
            "Step 6's Copilot round arm runs for it, with a push to the PR's "
            "head branch and no `gh pr create`. Step 7's off-but-present rule "
            "applies to it as to an authored fix this run merged.",
            self.step1,
        )
        self.assertIn(
            "An adopted PR skips the round: the contributor's PR is theirs to "
            "put to a reviewer. Step 1's own open PR is outside that "
            "exemption: the round runs for it, with a push to the PR's head "
            "branch and no `gh pr create`.",
            self.step6,
        )

    def test_round_decline_leaves_the_own_pr_open(self):
        self.assertIn(
            "Step 1's own open PR existed before the run, so a decline leaves "
            "it open, and the close block says so. That close block's CI line "
            "says that nothing waits on CI now, and its fenced next command is "
            "`/hotfix` with the PR reference, not a new branch.",
            self.step6,
        )

    def test_step_seven_rule_applies_to_it(self):
        self.assertIn(
            "Step 1's own open PR is outside that adopted-PR exemption, so the "
            "rule applies to it.",
            self.step7,
        )


class TestHotfixGuestChangeRoute(unittest.TestCase):
    """M266 AC3 and AC4: the guest arm's change route for the operator's own
    `hotfix-` PR with a change request newer than its head. The trigger, the
    stale-request fallback, the reads, the checks, the chip, the push, and
    both closes are pinned on their own (M165 lesson), whitespace collapsed
    (M171 lesson)."""

    def setUp(self):
        text = read("hotfix", "SKILL.md")
        self.step1 = flat(section(text, "1. **Tier check first.**",
                                  "2. **Branch"))

    def test_guest_read_has_the_route_fields(self):
        self.assertIn(
            "--json state,headRefName,reviewDecision,author,latestReviews,"
            "commits`, and make the candidate-row match above. A PR that the "
            "change route below covers takes that route.",
            self.step1,
        )

    def test_every_other_guest_pr_reports_and_stops(self):
        self.assertIn(
            "For any other PR, the arm goes on here. Skip the tier check and "
            "steps 2 to 7.",
            self.step1,
        )

    def test_trigger_is_own_pr_with_a_newer_change_request(self):
        self.assertIn(
            "*Change route (M266).* It covers a PR whose `author.login` equals "
            "`gh api user --jq .login`. The PR's `latestReviews` also has an "
            "entry with the state `CHANGES_REQUESTED` and a `submittedAt` "
            "later than the `committedDate` of the last entry of `commits`.",
            self.step1,
        )

    def test_an_older_change_request_reports_and_stops(self):
        self.assertIn(
            "A change request older than the head means that the PR waits for "
            "a new review, so it takes the report-and-stop above.",
            self.step1,
        )

    def test_route_reads_the_conversation_and_makes_changes(self):
        self.assertIn(
            "The route runs the three reads of step 6's PR-conversation read, "
            "with `--repo <base-repo>`.",
            self.step1,
        )
        self.assertIn(
            "The reads only read: the Copilot round's replies and resolves "
            "(`skills/shared/copilot-review.md` §5) do not run on this route.",
            self.step1,
        )
        self.assertIn(
            "Make a change for each requested item, or name the reason for "
            "making none, and commit each change on the branch.",
            self.step1,
        )

    def test_route_rechecks_the_bar_and_the_test(self):
        self.assertIn(
            "tier-check the PR's whole diff against `<base>/<default-branch>`. "
            "A diff over the hotfix bar takes this step's over-the-bar "
            "disposition, and nothing is pushed. That close block names the "
            "commits left on the branch. Re-run step 3's two-way check against "
            "`<base>/<default-branch>`, and step 4's `verify` slot on the new "
            "head.",
            self.step1,
        )

    def test_a_failed_check_pushes_nothing(self):
        self.assertIn(
            "If either fails, push nothing, and stop with a close block that "
            "names the failure and the local commits.",
            self.step1,
        )

    def test_route_checks_out_from_the_base_repo(self):
        self.assertIn(
            "Run step 2's `git status` check, then `gh pr checkout <N> --repo "
            "<base-repo>`.",
            self.step1,
        )

    def test_one_chip_lists_each_item(self):
        self.assertIn(
            "Then pose one `AskUserQuestion` chip. Its question text lists "
            "each requested item with its change or its reason, and a decline "
            "option is present.",
            self.step1,
        )

    def test_approval_pushes_and_posts_nothing(self):
        self.assertIn(
            "On approval, push to the remote that holds the PR's head, the one "
            "`gh pr checkout` set as the branch's upstream: `git push <head-remote> "
            "HEAD:<headRefName>`. Post no comment or reply on the PR. Then stop with the close block of "
            "the report-and-stop above. That close block also says that the "
            "reply to the maintainers is the operator's.",
            self.step1,
        )

    def test_decline_pushes_nothing(self):
        self.assertIn(
            "On decline, push nothing, and stop with a close block that names "
            "the unpushed commits.",
            self.step1,
        )


if __name__ == "__main__":
    unittest.main()
