"""Prose guard: criteria and tasks carry positional labels (M169).

Coverage cites criteria and tasks by position (`AC1 → T1`), and
`cairn_validate`'s coverage-complete check counts checkboxes positionally
(M107). The shipped template showed bare bullets, so instantiated files
carried no label — or labels whose number drifted from the position. M169
makes the label part of the shipped form: the template's example items open
with `ACn:` / `Tn:`, each section's comment states the position rule, the
binding-criterion ingest form reads `ACn (BCm):`, and the plan and implement
skills state the labeling and renumbering obligation. Each positive block is
pinned here and registered in the mutation harness; the negative check that
the old spelling is gone has no block to mutate and is unregistered.

Anchors are copied from the shipped bytes; phrases crossing a hard wrap are
matched with `\\s+` so a reflow does not red a rule still present (M105).
Targets are read with `Path.read_text` because the mutation engine patches
only that call (M100). Hand-run only (M144, D-109):

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def template():
    return read("shared", "templates", "milestone.md")


def plan():
    return read("milestone-plan", "SKILL.md")


def implement():
    return read("milestone-implement", "SKILL.md")


def brief():
    return read("milestone-brief", "SKILL.md")


def section(text, start, end):
    """The slice of `text` between the first `start` and the next `end`."""
    return text.split(start, 1)[1].split(end, 1)[0]


class TestTemplateLabelsItsExamples(unittest.TestCase):
    """AC1: every example checkbox item opens with its positional label."""

    def test_acceptance_criteria_examples_are_labeled(self):
        seg = section(template(), "## Acceptance criteria", "## Coverage")
        items = re.findall(r"^- \[ \] (\S+)", seg, flags=re.M)
        self.assertEqual(items, ["AC1:", "AC2:"])

    def test_task_examples_are_labeled(self):
        seg = section(template(), "## Tasks", "## Work log")
        items = re.findall(r"^- \[ \] (\S+)", seg, flags=re.M)
        self.assertEqual(items, ["T1:"])


class TestTemplateCommentsStateThePositionRule(unittest.TestCase):
    """AC1: each section's comment says the label is the item's position,
    counted top-to-bottom, the number Coverage cites."""

    def test_acceptance_criteria_comment_states_the_rule(self):
        seg = section(template(), "## Acceptance criteria", "## Coverage")
        self.assertRegex(
            seg,
            r"Every item opens with its positional label — `ACn:` — the "
            r"item's\s+position counted top-to-bottom, the number Coverage "
            r"cites",
        )
        self.assertRegex(
            seg,
            r"an\s+insertion, removal, or reorder renumbers the labels and "
            r"the Coverage\s+lines together",
        )

    def test_tasks_comment_states_the_rule(self):
        seg = section(template(), "## Tasks", "## Work log")
        self.assertRegex(
            seg,
            r"Every item opens with its positional label —\s+`Tn:` — the "
            r"item's position counted top-to-bottom, the number Coverage"
            r"\s+cites",
        )
        self.assertRegex(
            seg,
            r"an insertion, removal, or reorder renumbers the labels and "
            r"the\s+Coverage lines together",
        )


class TestIngestFormIsUnified(unittest.TestCase):
    """AC1: the binding-criterion ingest form reads `ACn (BCm):` at the two
    shipped prose sites; the old hyphenated spelling is gone from the
    skills tree (the test-side sites are checked by the grep in the
    milestone, so this file spells the old form only by concatenation)."""

    def test_template_comment_shows_the_unified_form(self):
        self.assertIn("`- [ ] ACn (BCm): <verbatim>`", template())

    def test_brief_ingest_rule_shows_the_unified_form(self):
        self.assertIn("`- [ ] ACn (BCm): <verbatim>`", brief())

    def test_old_spelling_is_gone_from_shipped_prose(self):
        for text in (template(), brief(), plan(), implement()):
            self.assertNotIn("AC-" + "N", text)


class TestPlanStepFourStatesTheLabelingRule(unittest.TestCase):
    """AC2: plan step 4 states labeling, position equality, and joint
    renumbering."""

    def setUp(self):
        self.step4 = section(plan(), "4. **Solidify autonomously**",
                             "5. **Remainder ledger")

    def test_every_bullet_opens_with_its_label(self):
        self.assertRegex(
            self.step4,
            r"every criterion and task bullet\s+opens with its positional "
            r"label \(`ACn:` / `Tn:`\)",
        )

    def test_label_equals_position_counted_top_to_bottom(self):
        self.assertRegex(
            self.step4,
            r"the label equal to\s+the item's position counted top-to-bottom",
        )

    def test_edits_renumber_labels_and_coverage_together(self):
        self.assertRegex(
            self.step4,
            r"any insertion, removal, or reorder renumbers the labels"
            r"\s+and the Coverage lines together",
        )


class TestImplementStepSixRenumbersOnBothBranches(unittest.TestCase):
    """AC2: implement step 6 states the renumbering obligation on the minor
    branch and on the substantive branch."""

    def setUp(self):
        step6 = section(implement(), "6. **Plan amendments**",
                        "7. **Blocked?**")
        self.minor = section(step6, "- *Minor*", "- *Substantive*")
        self.substantive = section(step6, "- *Substantive*",
                                   "**Return-adjacent direction rule")

    def test_minor_branch_renumbers(self):
        self.assertRegex(
            self.minor,
            r"A change that\s+adds, removes, or reorders a criterion or task "
            r"renumbers the `ACn:` /\s+`Tn:` labels and the Coverage lines "
            r"together",
        )

    def test_substantive_branch_renumbers(self):
        self.assertRegex(
            self.substantive,
            r"A change that adds, removes, or reorders a criterion or task "
            r"renumbers\s+the `ACn:` / `Tn:` labels and the Coverage lines "
            r"together",
        )


if __name__ == "__main__":
    unittest.main()
