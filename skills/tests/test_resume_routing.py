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
            "state,mergedAt` (N from the URL)",
            self.route,
        )

    def test_route_a_merged_and_reviewed_goes_to_step_nine(self):
        self.assertIn(
            "(a) `MERGED`, every acceptance-criterion box ticked against a "
            "recorded evidence line, and a work-log line recording step-7 "
            "approval (`step-7 approval: PR #<N> …`) → append one work-log "
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
            "— `gh pr diff <N>` — in place of the branch diff; fix-now code "
            "goes through `/hotfix`, never a commit on the default branch), "
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
            "(step 2's push, its draft PR already open; when the default "
            "branch had moved, step 3 re-run so the evidence matches the "
            "merged tree), the step-7 chip re-posed, and on approval step 8 "
            "from the marker write onward.",
            self.route,
        )

    def test_route_d_everything_else_goes_to_step_one(self):
        self.assertIn(
            "(d) any other state, or a state above whose conditions are not "
            "met → step 1, step 2 skipping `gh pr create` when the header "
            "already names an open PR. A `gh` that is missing, "
            "unauthenticated, or has no remote → step 1, the recap naming "
            "which of the three it was.",
            self.route,
        )

    def test_step_seven_records_the_approval_line(self):
        step7 = flat(section(read("milestone-review", "SKILL.md"),
                             "7. **Final approval gate.**",
                             "8. **On approval"))
        self.assertIn(
            "Approval appends one work-log line naming the PR number it "
            "approved (`step-7 approval: PR #<N> approved for merge`)",
            step7,
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
            "(`gh pr view <N> --json state`) → post-merge hygiene owed: "
            "report it as such and route to `/milestone-review M<NNN>`",
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
    """AC4: `/hotfix` step 1 runs step 7 only for a merged PR whose head
    branch is not a milestone branch."""

    def setUp(self):
        self.step1 = flat(section(read("hotfix", "SKILL.md"),
                                  "1. **Tier check first.**",
                                  "2. **Branch"))

    def test_merged_pr_runs_step_seven_only(self):
        self.assertIn(
            "A PR-reference argument whose `gh pr view <N> --json "
            "state,headRefName` reports `MERGED` and a head branch not "
            "matching `m<nnn>-*`",
            self.step1,
        )
        self.assertIn("runs step 7 only, steps 2–6 skipped", self.step1)

    def test_reentry_names_its_three_moves(self):
        self.assertIn(
            "the candidate-row check, then — when the PR body carries a "
            "`Fixes #N` line — one chip authorizing the issue close before "
            "any issue write (a hotfix keeps no work log to show whether "
            "step 6's chip authorized it, so it is asked once here), then "
            "the close block with one recap line naming the merged PR.",
            self.step1,
        )


if __name__ == "__main__":
    unittest.main()
