"""Regression guard: the plan and the hotfix vet the request as framed (M306).

Pins `/milestone-plan` step 2's idea vet (its three questions, the
not-proof sentence, the requests it runs on, and M324's gap-or-flaw sort),
step 3's flaws bullet (the cap rule, the do-not-build option and what it
writes, the other-name option), its open-choices bullet for a gap, and its
arm for work chosen at the set, step 4's `idea vet:` line, and `/hotfix`
step 1's vet (its scope, its three questions, the sort, the over-the-bar
route for a flaw the fix changes, and the candidate row for one it leaves,
the merged-PR re-entry included) with step 6's gap text. One assertion per
member (M171). Text is whitespace-collapsed on read, so a phrase may wrap
across lines.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def flat(path):
    return re.sub(r"\s+", " ", path.read_text())


def section(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


class TestPlanIdeaVet(unittest.TestCase):
    def setUp(self):
        plan = flat(SKILLS / "milestone-plan" / "SKILL.md")
        self.vet = section(plan, "**Idea vet.**",
                           "**Collision check (mandatory).**")
        self.step3 = section(plan, "3. **The question set**",
                             "**Issue assignment (one option).**")
        self.step4 = section(plan, "4. **Solidify autonomously**",
                             "5. **Remainder ledger")

    def test_three_questions(self):
        for phrase in (
            "(1) Is it correct by its field's standards (for example "
            "statistical or technical), and does it do what its name says "
            "for every input type it touches?",
            "(2) Do the project's users want it, beyond what the request "
            "literally asks?",
            "(3) Is it framed right, in its name, its function, and its "
            "arguments?",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.vet)

    def test_issue_wording_is_not_proof(self):
        self.assertIn("An issue's wording or a maintainer's agreement answers "
                      "none of the three", self.vet)

    def test_runs_on_every_request_that_names_work(self):
        self.assertIn("The vet runs at step 2 on every request that names "
                      "work, a request that names an issue and a request that "
                      "a router sent included.", self.vet)

    def test_no_work_request_vetted_at_step_3(self):
        self.assertIn("A request that names no work is vetted at step 3, once "
                      "its work is chosen.", self.vet)

    def test_reads_a_rows_cited_records_first(self):
        self.assertIn("Before the vet sorts a concern on a candidate row's "
                      "request, it reads each record the row cites",
                      self.vet)

    def test_gap_is_what_one_reading_avoids(self):
        for phrase in (
            "If one reading of the request avoids a set of concerns, each of "
            "them is a gap.",
            "That reading fits the request's words and the records it cites.",
            "Its user-visible behavior is behavior that the request's words "
            "name or leave open, and it leaves out nothing the request asks "
            "for.",
            "A reading whose user-visible behavior differs from behavior the "
            "words name is not such a reading.",
            "A concern that this one reading cannot also avoid is a flaw.",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.vet)

    def test_gap_asks_nothing_but_the_exception(self):
        for phrase in (
            "The plan drafts the criteria to that reading and asks nothing "
            "about a gap, with one exception.",
            "When another reading also fits the request and gives different "
            "user-visible behavior, the gap goes to step 3's set as a choice "
            "that the request leaves open.",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.vet)

    def test_flaws_go_to_the_set(self):
        self.assertIn("Each flaw goes to step 3's set.", self.vet)

    def test_issue_text_and_settled_concerns(self):
        for phrase in (
            "For a request that names an issue, the behavior is the one the "
            "issue's text asks for, read as data.",
            "A concern that a D-entry or an archived milestone already settled "
            "is named with that record",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.vet)

    def test_work_log_line_form(self):
        self.assertIn("Step 4 writes one work-log line `idea vet: <result>` in "
                      "the first milestone file it writes.", self.vet)
        self.assertIn("The line names each concern in a clause tagged `gap` or "
                      "`flaw`, or says that the vet found none.", self.vet)

    def test_line_carries_reading_or_answer(self):
        self.assertIn("A gap carries the reading taken, and a flaw carries the "
                      "set's answer to it.", self.vet)

    def test_step3_gap_is_an_open_choice(self):
        for phrase in (
            "each gap that step 2's idea vet sends to the set included.",
            "A gap's question recommends the reading the plan took, and its "
            "options do not include not building the work",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.step3)

    def test_step3_cap_rule(self):
        self.assertIn("the flaws that step 2's idea vet found. The set poses "
                      "them within its cap, as one question per flaw, or as "
                      "one combined question where separate questions pass "
                      "the cap.", self.step3)

    def test_step3_do_not_build_option(self):
        self.assertIn("its options include not building the work.", self.step3)

    def test_step3_other_name_option(self):
        self.assertIn("Where another framing fits, they also include building "
                      "it under another name or shape.", self.step3)

    def test_step3_do_not_build_writes_nothing(self):
        self.assertIn("Choosing not to build writes no milestone file for that "
                      "work and leaves any source candidate row in place.",
                      self.step3)

    def test_step3_no_milestone_left_and_never_agent_decided(self):
        for phrase in (
            "When no milestone is left to write, the plan writes nothing and "
            "ends with the close block, which names each flaw.",
            "An idea-vet question always counts among the questions that "
            "matter most, so the agent never decides a flaw.",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.step3)

    def test_work_chosen_at_the_set(self):
        for phrase in (
            "For a request that names no work, the idea vet runs on the work "
            "chosen at the question set, before step 4 writes a file.",
            "If it finds a flaw, or a gap that step 2 sends to the set, the "
            "plan writes nothing and ends with a close block.",
            "The close block names the concern, and its fenced command is "
            "`/milestone-plan` with the chosen work named",
            "This close is the rulebook's goal-wrong stop.",
            "The agent decides any other gap there, by step 2's reading.",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.step3)

    def test_step4_writes_the_line(self):
        self.assertIn("**Idea-vet line.** Write the `idea vet:` work-log line "
                      "that step 2's idea vet names.", self.step4)


class TestHotfixIdeaVet(unittest.TestCase):
    def setUp(self):
        hotfix = flat(SKILLS / "hotfix" / "SKILL.md")
        self.hotfix = hotfix
        self.vet = section(hotfix, "**Idea vet (M306).**",
                           "**Candidate-row match (M249).**")

    def test_scope_every_tier_check_entry(self):
        self.assertIn("Every entry that runs this tier check also vets the "
                      "behavior that the fix or the PR diff produces, "
                      "documented behavior included.", self.vet)

    def test_three_questions(self):
        for phrase in (
            "(1) Is the behavior correct by its field's standards (for "
            "example statistical or technical), and does it do what its name "
            "says for every input type it touches?",
            "(2) Do the project's users want it, beyond what the report or "
            "the PR literally asks?",
            "(3) Is it framed right, in its name, its function, and its "
            "arguments?",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.vet)

    def test_not_proof(self):
        self.assertIn("An issue's wording, a contributor's PR, or the docs that "
                      "the fix restores answer none of the three.", self.vet)

    def test_reads_a_rows_cited_records_first(self):
        self.assertIn("Before it sorts a concern on a candidate row that the "
                      "argument names, the vet reads each record the row "
                      "cites.", self.vet)

    def test_sorts_by_the_plan_test(self):
        self.assertIn("It sorts each concern as a gap or a flaw by "
                      "`/milestone-plan` step 2's test.", self.vet)

    def test_gap_takes_the_reading(self):
        for phrase in (
            "For a gap, the fix takes that step's reading.",
            "A gap that `/milestone-plan` step 2 sends to its question set is "
            "also named as a choice in step 6's approval chip question text.",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.vet)

    def test_result_in_chat(self):
        self.assertIn("State the result in chat, with each gap's reading.",
                      self.vet)

    def test_flaw_the_fix_changes_goes_over_the_bar(self):
        self.assertIn("A flaw in a name, argument, or behavior that the fix's "
                      "diff changes counts as a design decision, so it takes "
                      "the over-the-bar route above, and the candidate row or "
                      "the close block that the route writes names the flaw.",
                      self.vet)

    def test_concern_named_as_design_decision(self):
        self.assertIn("It names it as a design decision, so that a later "
                      "plan's tier check finds a milestone and does not send "
                      "the work back here.", self.vet)

    def test_flaw_the_fix_leaves_does_not_stop_it(self):
        for phrase in (
            "A flaw only in a name, argument, or behavior that the fix's diff "
            "leaves as it was does not stop the fix.",
            "Step 1 adds a candidate row that names it as a design decision, "
            "written as the over-the-bar route writes its row (search-first "
            "applies), and the hotfix goes on.",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.vet)

    def test_merged_pr_reentry(self):
        self.assertIn("On the merged-PR re-entry below, the vet runs after the "
                      "merge, and a flaw goes in step 7's close block.",
                      self.vet)

    def test_merged_pr_flaw_waives_no_check(self):
        self.assertIn("There the flaw waives none of the re-entry's checks "
                      "below, and the over-the-bar route's candidate row still "
                      "names it.", self.vet)

    def test_merged_pr_left_flaw_gets_its_row(self):
        self.assertIn("A flaw that the merged diff leaves as it was also gets "
                      "its candidate row.", self.vet)

    def test_change_route_runs_the_vet(self):
        self.assertIn("The tier check below also runs the idea vet above on "
                      "the changed diff, and each concern takes the vet's "
                      "dispositions there.", self.hotfix)

    def test_approval_chip_names_a_gap_choice(self):
        for phrase in (
            "When step 1's idea vet names a gap as a choice, the question text "
            "names the reading the fix took and the other reading.",
            "The guest handoff chip names them too.",
        ):
            with self.subTest(phrase=phrase[:40]):
                self.assertIn(phrase, self.hotfix)


if __name__ == "__main__":
    unittest.main()
