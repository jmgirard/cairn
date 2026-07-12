"""Lock: the lessons loop (M16) stays wired end to end.

`cairn/LESSONS.md` is the durable, append-only, capped lessons home; the
capture step lives in `/milestone-review` post-merge hygiene, the harvest step
in `/milestone-plan` before the gate, and the 50-line cap is stated in two
places that must not drift — the tracking-rules weight-caps line and
`cairn_scripts.LINE_CAPS`. (The cap is *enforced* by the over-cap fixture in
scripts/tests; this test locks the wiring and the stated↔enforced agreement.)

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestLessonsLoop(unittest.TestCase):
    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_file_map_documents_lessons_home(self):
        self.assertRegex(self.rules, r"\|\s*`cairn/LESSONS\.md`\s*\|")

    def test_weight_caps_states_lessons_cap(self):
        self.assertRegex(self.rules, r"`LESSONS\.md`\s*<\s*50\s*lines")

    def test_stated_cap_matches_enforced_cap(self):
        # The rulebook's human-readable cap and the scripts' machine-enforced
        # cap are two encodings of one number; drift between them is the defect.
        stated = int(re.search(r"`LESSONS\.md`\s*<\s*(\d+)\s*lines", self.rules).group(1))
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        enforced = int(re.search(r'"cairn/LESSONS\.md":\s*(\d+)', scripts).group(1))
        self.assertEqual(stated, enforced)

    def test_lessons_home_exists_with_entry_format(self):
        lessons = read(ROOT / "cairn" / "LESSONS.md")
        self.assertIn("# Lessons", lessons)
        self.assertIn("YYYY-MM-DD (M<NN>)", lessons)  # documented one-line format

    def test_capture_wired_into_review(self):
        self.assertIn("LESSONS.md", read(SKILLS / "milestone-review" / "SKILL.md"))

    def test_harvest_wired_into_plan(self):
        self.assertIn("LESSONS.md", read(SKILLS / "milestone-plan" / "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
