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

import pathlib
import re
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
    cannot settle, before that thread gets a reply, and posts no question
    to GitHub. Each clause has its own test, so a removal of any one fails
    (the M287 criteria audit)."""

    def setUp(self):
        self.decide = flat(section(read("copilot-review", "SKILL.md"),
                                   "4. **Decide.**", "5. **Fix.**"))

    def test_unsettled_note_is_asked_in_chat(self):
        self.assertIn("If the agent cannot decide a note without the user, "
                      "ask the user in chat.", self.decide)
        self.assertIn("Use one `AskUserQuestion` chip", self.decide)

    def test_that_thread_waits_for_the_answer(self):
        self.assertIn("That thread gets no reply until the user answers.",
                      self.decide)

    def test_no_question_goes_to_github(self):
        self.assertIn("Never post a question for the user to GitHub.",
                      self.decide)


class TestNoThanks(unittest.TestCase):
    """M287 AC3: in the skill and the module, every line that names
    thanks forbids it, and each file states the rule."""

    FILES = (("copilot-review", "SKILL.md"), ("shared", "copilot-review.md"))

    def test_skill_thread_reply_forbids_thanks(self):
        step = flat(section(read("copilot-review", "SKILL.md"),
                            "6. **Reply and resolve.**",
                            "7. **Answer the summary.**"))
        self.assertIn("never thanks Copilot", step)

    def test_module_thread_reply_forbids_thanks(self):
        step = flat(section(read("shared", "copilot-review.md"),
                            "3. Reply on the thread's first comment",
                            "4. Resolve the thread."))
        self.assertIn("Never thank Copilot.", step)

    def test_module_summary_reply_forbids_thanks(self):
        reply = flat(section(read("shared", "copilot-review.md"),
                             "**Summary reply.**", "## 6."))
        self.assertIn("It never thanks Copilot", reply)

    def test_every_thanks_line_forbids_it(self):
        for parts in self.FILES:
            hits = [line for line in read(*parts).splitlines()
                    if "thank" in line.lower()]
            self.assertTrue(hits, f"no thanks line in {'/'.join(parts)}")
            for line in hits:
                with self.subTest(file="/".join(parts), line=line):
                    self.assertRegex(line.lower(), r"never thank")


class TestSummaryReply(unittest.TestCase):
    """M287 AC4: the module answers each Copilot review's summary after
    its threads are resolved, links the review, and skips a review an
    operator comment already links. One test per clause."""

    def setUp(self):
        self.reply = flat(section(read("shared", "copilot-review.md"),
                                  "**Summary reply.**", "## 6."))

    def test_reply_comes_after_the_threads_are_resolved(self):
        self.assertIn("once all its threads (the ones its body anchors) are "
                      "resolved", self.reply)

    def test_reply_links_the_review(self):
        self.assertIn("the review's `url`, then one line per thread and "
                      "body item", self.reply)

    def test_a_linked_review_is_skipped(self):
        self.assertIn("Skip a review whose `url` an operator comment "
                      "already carries", self.reply)


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


if __name__ == "__main__":
    unittest.main()
