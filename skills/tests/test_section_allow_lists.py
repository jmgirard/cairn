"""Regression guard: the milestone-file section-ownership table (M14) agrees
with the template on both section *names* and their *owners*.

The section write allow-list in tracking-rules.md ("Milestone-file section
ownership") assigns every milestone-file section to a writing skill. Two
artifacts encode it — the rulebook table and the template's per-section
`owner:` tags — and they must not drift. This locks:
  * name parity: a new template section with no ownership row, or a row for a
    section the template no longer has, fails.
  * owner parity: a section whose template `owner:` tag names a different
    skill than the table's Writing-skill cell fails (the exact clobber M14
    exists to prevent).
Authorship itself can't be mechanized (git records no which-skill-wrote-what
signal), so these structural checks are the lock.

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


def _owner_tokens(s):
    """Canonical owner set from an owner string. 'transitioning skill' and
    'any skill' are their own markers; otherwise the set of phase skills
    named. Cut trailing prose at the first `·`/`;` so mode/notes text can't
    inject a false skill name (e.g. 'review reads, never reinterprets')."""
    s = re.split(r"[·;]", s.lower(), 1)[0]
    if "transitioning" in s:
        return {"transitioning"}
    if "any skill" in s:
        return {"any"}
    return {w for w in ("plan", "implement", "review") if w in s}


def table_rows():
    """(section-name set, owner tokens) per data row of the ownership table."""
    body = read("shared", "tracking-rules.md").split(MARKER, 1)
    assert len(body) == 2, "ownership table heading missing from rulebook"
    rows = []
    for line in body[1].splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if rows:
                break  # blank line after the table
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0].lower() == "section" or set(cells[0]) <= set("-: "):
            continue  # header or separator row
        sections = {_norm(p) for p in cells[0].split(",")}
        rows.append((sections, _owner_tokens(cells[1])))
    return rows


def table_section_owners():
    owners = {}
    for sections, toks in table_rows():
        for s in sections:
            owners[s] = toks
    return owners


def template_section_owners():
    """{section-name: owner tokens} from the template — header `- **Field:**`
    bullets (before the first H2) plus each H2 and its following comment."""
    lines = read("shared", "templates", "milestone.md").splitlines()
    first_h2 = next(i for i, l in enumerate(lines) if l.startswith("## "))
    owners = {}
    for l in lines[:first_h2]:
        m = re.match(r"- \*\*(.+?):\*\*.*?owner:\s*(.+?)\s*-->", l)
        if m:
            owners[_norm(m.group(1))] = _owner_tokens(m.group(2))
    for i, l in enumerate(lines):
        if l.startswith("## "):
            comment = "\n".join(lines[i + 1:i + 4])
            m = re.search(r"owner:\s*(.+?)\s*-->", comment, re.S)
            assert m, "H2 %r has no owner tag" % l
            owners[_norm(l[3:])] = _owner_tokens(m.group(1))
    return owners


class TestSectionAllowLists(unittest.TestCase):
    def test_table_matches_template_sections(self):
        self.assertEqual(set(table_section_owners()),
                         set(template_section_owners()))

    def test_owner_parity(self):
        table, tmpl = table_section_owners(), template_section_owners()
        for section in set(table) | set(tmpl):
            with self.subTest(section=section):
                self.assertEqual(table.get(section), tmpl.get(section))

    def test_write_mode_legend_defines_core_verbs(self):
        text = read("shared", "tracking-rules.md")
        for verb in ("create", "append-only", "amend-via-gate",
                     "mirror-update", "check-off", "exclusive"):
            self.assertIn("**%s**" % verb, text)

    def test_phase_skills_reference_the_allow_list(self):
        for skill in ("milestone-plan", "milestone-implement",
                      "milestone-review"):
            self.assertIn("section-ownership table", read(skill, "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
