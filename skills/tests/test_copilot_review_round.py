"""Prose guard: the opt-in Copilot review round (M231).

`skills/shared/copilot-review.md` states the round once, and `/hotfix` and
`/milestone-review` cite it. With the round on, owner mode opens the PR
before the approval chip or the merge question (D-152). With the round off,
the post-approval push-and-open stays as the off arm (D-138). This file
pins the two skills' citations of the module (M231 AC1) and both arms in
each skill (M231 AC3).

Clauses run across wrapped lines, so targets are read with whitespace
collapsed (the M171 lesson). Hand-run only (M144, D-109):

    python3 -m unittest discover -s skills/tests
"""

import json
import pathlib
import re
import shutil
import subprocess
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
MODULE = "skills/shared/copilot-review.md"


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def flat(text):
    return re.sub(r"\s+", " ", text)


def section(text, start, end):
    """The slice of `text` between the first `start` and the next `end`.
    Both anchors must be present, so a renamed heading fails loudly rather
    than slicing to the end of the file (the M182 lesson)."""
    head, sep, rest = text.partition(start)
    if not sep:
        raise AssertionError(f"start anchor missing: {start!r}")
    body, sep, _ = rest.partition(end)
    if not sep:
        raise AssertionError(f"end anchor missing: {end!r}")
    return body


class TestModuleCitations(unittest.TestCase):
    """AC1: each skill's round arm cites the module. The arm sentence is
    pinned, not the bare path, because the path recurs in each skill."""

    def test_review_round_arm_cites_the_module(self):
        self.assertIn(
            f"the round on per `{MODULE}` §1; D-152, D-153). Here, at the start",
            flat(read("milestone-review", "SKILL.md")),
        )

    def test_hotfix_round_arm_cites_the_module(self):
        self.assertIn(
            f"the round on per `{MODULE}` §1; D-152). Before the approval",
            flat(read("hotfix", "SKILL.md")),
        )


class TestReviewArms(unittest.TestCase):
    """AC3: `/milestone-review` opens the PR and requests Copilot at step 2
    with the round on (D-153), and keeps step 8's post-approval open as the
    off arm."""

    def setUp(self):
        self.text = flat(read("milestone-review", "SKILL.md"))

    def test_round_arm_sits_in_step_two_before_verification(self):
        step2 = section(self.text, "2. Nothing is pushed and no PR is opened",
                        "3. **Execute every acceptance criterion")
        self.assertIn("**Copilot arm** (owner mode, the round on", step2)
        self.assertIn("push the branch and open the PR", step2)
        self.assertIn("Balanced (§2). Copilot then reviews while steps 3 to 6",
                      step2)

    def test_off_arm_keeps_the_post_approval_open(self):
        step8 = section(self.text, "8. **On approval — and only then:**",
                        "**Companion arm")
        self.assertIn("push the branch and open the PR", step8)
        self.assertIn("skipped when the header already names an open PR",
                      step8)


class TestHotfixArms(unittest.TestCase):
    """AC3: `/hotfix` opens the PR before its approval chip with the round
    on, and keeps the post-approval open as the off arm."""

    def setUp(self):
        self.step = flat(section(read("hotfix", "SKILL.md"),
                                 "6. **Approval gate:**",
                                 "7. If the fix revealed"))

    def test_round_arm_runs_before_the_gate(self):
        arm = section(self.step, "**Copilot round arm**", "**The gate:**")
        self.assertIn("Before the approval gate below, push and open the PR",
                      arm)
        self.assertIn("asking for Lite", arm)

    def test_off_arm_keeps_the_post_approval_open(self):
        gate = self.step.split("**The gate:**", 1)[1]
        self.assertIn("On approval of an authored fix, push and open the PR",
                      gate)


class TestWaitBound(unittest.TestCase):
    """Hotfix 2026-10-13: the wait runs 25 minutes, since Copilot took
    longer than 10 minutes on 11 of 27 easystats PRs requested from
    2026-10-11 to 2026-10-13, and the loop prints only a changed state, so
    a pending review does not wake the session every 30 seconds."""

    def setUp(self):
        self.wait = flat(section(read("shared", "copilot-review.md"),
                                 "## 4. Wait and read", "## 5."))

    def test_loop_runs_25_minutes_under_its_backstop(self):
        self.assertIn("or after 25 minutes", self.wait)
        self.assertIn("`timeout_ms` to 1560000", self.wait)
        self.assertIn("treat it as the 25-minute exit", self.wait)
        self.assertNotRegex(self.wait, r"10[ -]minute")

    def test_loop_prints_only_a_changed_state(self):
        self.assertIn("prints a result only when it differs from the last",
                      self.wait)

    def test_readme_states_the_same_bound(self):
        readme = flat(SKILLS.parent.joinpath("README.md").read_text())
        self.assertIn("Claude waits up to 25 minutes", readme)


class TestCopilotReviewSkill(unittest.TestCase):
    """M287 AC2: `/copilot-review` asks in chat about a note the agent
    cannot settle, before that review's comment goes (M314), and posts no question
    to GitHub. Each clause has its own test, so a removal of any one fails
    (the M287 criteria audit)."""

    def setUp(self):
        self.decide = flat(section(read("copilot-review", "SKILL.md"),
                                   "4. **Decide.**", "5. **Fix.**"))

    def test_unsettled_note_is_asked_in_chat(self):
        self.assertIn("If the agent cannot decide a note without the user, "
                      "ask the user in chat.", self.decide)
        self.assertIn("Use one `AskUserQuestion` chip", self.decide)

    def test_that_review_waits_for_the_answer(self):
        self.assertIn("That note's review gets no comment until the user "
                      "answers.", self.decide)

    def test_no_question_goes_to_github(self):
        self.assertIn("Never post a question for the user to GitHub.",
                      self.decide)


class TestNoThanks(unittest.TestCase):
    """M287 AC3: in the skill and the module, every line that names
    thanks forbids it, and each file states the rule."""

    FILES = (("copilot-review", "SKILL.md"), ("shared", "copilot-review.md"))

    def test_skill_comment_forbids_thanks(self):
        step = flat(section(read("copilot-review", "SKILL.md"),
                            "6. **Comment.**", "7. **Resolve.**"))
        self.assertIn("never thanks Copilot", step)

    def test_module_comment_forbids_thanks(self):
        comment = flat(section(read("shared", "copilot-review.md"),
                               "**The comment.**", "## 6."))
        self.assertIn("The comment never thanks Copilot", comment)

    def test_every_thanks_line_forbids_it(self):
        for parts in self.FILES:
            hits = [line for line in read(*parts).splitlines()
                    if "thank" in line.lower()]
            self.assertTrue(hits, f"no thanks line in {'/'.join(parts)}")
            for line in hits:
                with self.subTest(file="/".join(parts), line=line):
                    self.assertRegex(line.lower(), r"never thank")


class TestOneComment(unittest.TestCase):
    """M314 AC1: the module answers each Copilot review with one comment
    and no thread reply, after every note has a disposition and each fix
    is pushed, links the review, lists each note, resolves after it, and
    posts no second comment for a review an operator comment links. One
    test per clause, except the link and the note lines, which share one."""

    def setUp(self):
        module = read("shared", "copilot-review.md")
        self.read = flat(section(module, "2. A fix-now item",
                                 "**The comment.**"))
        self.comment = flat(section(module, "**The comment.**", "## 6."))

    def test_no_reply_on_a_thread(self):
        self.assertIn("The read posts no reply on a thread.", self.read)

    def test_comment_waits_for_dispositions_and_pushes(self):
        self.assertIn("once every note of the review has a disposition and "
                      "each fix is pushed", self.comment)

    def test_comment_links_the_review_and_lists_each_note(self):
        self.assertIn("Its first line is the review's `url`, then one line "
                      "per note", self.comment)

    def test_resolves_follow_the_comment(self):
        self.assertIn("Then resolve each Copilot thread the comment names.",
                      self.comment)

    def test_a_linked_review_gets_no_second_comment(self):
        self.assertIn("already carries gets no second comment", self.comment)

    def test_a_linked_review_is_finished_not_redisposed(self):
        self.assertIn("Its notes get no disposition, its open Copilot threads "
                      "are resolved", self.comment)

    def test_a_return_floor_item_holds_back_its_review(self):
        self.assertIn("puts its review's comment and resolves on hold",
                      self.read)

    def test_no_reply_command_in_the_module(self):
        module = read("shared", "copilot-review.md")
        self.assertNotRegex(
            module, r"/replies|addPullRequestReviewThreadReply|in_reply_to")


class TestUnsettledNoteInTheRound(unittest.TestCase):
    """M287 AC5: in `/hotfix` and `/milestone-review`, a note the agent
    cannot settle takes the follow-up disposition unless it takes the
    return floor, the approval chip or merge question names it, and
    questions go to chat."""

    def setUp(self):
        self.step = flat(section(read("shared", "copilot-review.md"),
                                 "1. Dispose of it", "2. A fix-now item"))

    def test_unsettled_note_takes_the_follow_up(self):
        self.assertIn("thread the agent cannot settle without the user takes "
                      "the follow-up disposition, unless it takes the return "
                      "floor below.", self.step)

    def test_the_gate_chip_names_it(self):
        self.assertIn("The approval chip or merge question names it.",
                      self.step)

    def test_questions_go_to_chat(self):
        self.assertIn("A question for the user goes to chat, never to "
                      "GitHub.", self.step)


@unittest.skipUnless(shutil.which("jq"), "jq not installed")
class TestStateQueryLevel(unittest.TestCase):
    """Hotfix 2026-10-19: §3's state query reads the level from both forms
    of Copilot's level line. Copilot wrote `🧠 **Review effort:** Lite` up
    to PR #275 and `<sub>Review effort: Lite</sub>` from PR #282, and the
    capture that needed the `**` printed `unknown` for the new form. The
    test runs the module's own `--jq` filter with jq over a fixture
    response. gh runs `--jq` with gojq, so a live query backs this one."""

    def setUp(self):
        block = section(read("shared", "copilot-review.md"),
                        "## 3. State query", "## 4. Wait and read")
        line = next(ln for ln in block.splitlines()
                    if ln.startswith("gh api graphql"))
        self.jq = line.split("--jq '", 1)[1].rsplit("'", 1)[0]

    def state(self, body):
        response = {"data": {"repository": {"pullRequest": {
            "headRefOid": "abc",
            "reviewRequests": {"nodes": []},
            "reviews": {"nodes": [{
                "author": {"login": "copilot-pull-request-reviewer"},
                "commit": {"oid": "abc"},
                "body": body,
            }]},
        }}}}
        run = subprocess.run(["jq", "-r", self.jq], input=json.dumps(response),
                             capture_output=True, text=True, check=True)
        return run.stdout.strip()

    def test_sub_form_gives_the_level(self):
        self.assertEqual(self.state("Summary.\n\n<sub>Review effort: Lite</sub>"),
                         "reviewed head Lite")

    def test_bold_form_gives_the_level(self):
        self.assertEqual(self.state("Summary.\n\n🧠 **Review effort:** Balanced"),
                         "reviewed head Balanced")

    def test_no_level_line_gives_unknown(self):
        self.assertEqual(self.state("Summary with no level line."),
                         "reviewed head unknown")


if __name__ == "__main__":
    unittest.main()
