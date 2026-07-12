"""Regression guard: the milestone-file section-ownership table (M14) covers
exactly the template's sections — no more, no less.

The section write allow-list in tracking-rules.md ("Milestone-file section
ownership") assigns every milestone-file section to a writing skill. This
locks table <-> template parity: a new template section with no ownership
row, or an ownership row for a section the template no longer has, fails
here. Enforcement of *authorship* can't be mechanized (git records no
which-skill-wrote-what signal), so this structural check is the lock.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

MARKER = "### Milestone-file section ownership"


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def _norm(s):
    """Canonicalize a section name: lowercase, drop parentheticals."""
    return re.sub(r"\s*\([^)]*\)", "", s.strip().lower()).strip()


def template_sections():
    """Section tokens from the milestone template: the header fields (the
    `- **Field:**` bullets before the first H2) plus every H2 heading."""
    lines = read("shared", "templates", "milestone.md").splitlines()
    first_h2 = next(i for i, l in enumerate(lines) if l.startswith("## "))
    header = set()
    for l in lines[:first_h2]:
        m = re.match(r"- \*\*(.+?):\*\*", l)
        if m:
            header.add(_norm(m.group(1)))
    h2 = {_norm(l[3:]) for l in lines if l.startswith("## ")}
    return header | h2


def table_sections():
    """Section tokens the ownership table's first column covers (each cell
    comma-split, parentheticals dropped)."""
    body = read("shared", "tracking-rules.md").split(MARKER, 1)
    assert len(body) == 2, "ownership table heading missing from rulebook"
    covered = set()
    for line in body[1].splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if covered:
                break  # blank line after the table
            continue
        first = [c.strip() for c in line.strip("|").split("|")][0]
        if first.lower() == "section" or set(first) <= set("-: "):
            continue  # header or separator row
        for part in first.split(","):
            covered.add(_norm(part))
    return covered


class TestSectionAllowLists(unittest.TestCase):
    def test_table_matches_template_sections(self):
        self.assertEqual(table_sections(), template_sections())

    def test_write_mode_legend_defines_core_verbs(self):
        text = read("shared", "tracking-rules.md")
        for verb in ("create", "append-only", "amend-via-gate",
                     "mirror-update", "exclusive"):
            self.assertIn("**%s**" % verb, text)

    def test_phase_skills_reference_the_allow_list(self):
        for skill in ("milestone-plan", "milestone-implement",
                      "milestone-review"):
            self.assertIn("section-ownership table", read(skill, "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
