"""Guard: the r-package release-walk keeps cran-comments.md in its short form.

The slot's cran-comments line named the file's contents ("test environments,
check results, NOTE justifications, revdep summary") but set no bound on
length or scope, so the release walk filled it with a NEWS rehash — a long
file CRAN reviewers do not want. The line now names the conventional short
form and forbids restating NEWS. Prose guards read the file as one string, so
each asserted phrase lives on a single source line (M23).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def release_walk():
    text = SKILLS.joinpath("shared", "profiles", "r-package.md").read_text()
    out, capturing = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if capturing:
                break
            capturing = line[3:].strip().lower() == "release-walk"
            continue
        if capturing:
            out.append(line)
    return "\n".join(out).lower()


class TestCranCommentsShortForm(unittest.TestCase):
    def test_walk_names_the_short_form(self):
        self.assertIn("cran-comments.md", release_walk())
        self.assertIn("short form", release_walk())

    def test_walk_forbids_restating_news(self):
        self.assertIn("do not restate news", release_walk())


if __name__ == "__main__":
    unittest.main()
