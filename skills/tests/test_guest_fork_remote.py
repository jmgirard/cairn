"""Regression guard: the M234 guest-mode fork remote.

In guest mode the operator's fork is not always `origin`. Three of seven
local guest checkouts keep the upstream at `origin` and the fork at a remote
named `fork`, so a push to `origin` there goes to the upstream repo. Three
things have to survive:

  1. The rulebook's recipe. `<fork>` is the one remote, other than `<base>`,
     whose parent equals `<base-repo>`. A failed read is not a match, and no
     match or more than one stops the push. `<fork-owner>` reads `<fork>`.
  2. Every guest push site names `<fork>`. The list is the whole list (M171
     lesson): a test fails when any one site goes back to `origin`.
  3. No skill prose calls `origin` the fork.

The pinned phrases wrap across source lines, so this guard collapses
whitespace on read. That is the deliberate exception to the one-line
convention (M23), as in the M171 guards. The target is read per-test,
never cached on the class (M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

RECIPE = [
    "In guest mode the **fork remote** `<fork>` is the one remote that `git remote` lists, other than `<base>`, whose parent equals `<base-repo>`, ignoring case.",
    "--json parent -q '.parent.owner.login + \"/\" + .parent.name'",
    "A remote whose read fails is not a match.",
    "`<fork-owner>` reads `<fork>` with `--json owner -q .owner.login`.",
    "With no match, or more than one, a guest push stops before the push",
]

# (file under skills/, phrase) for every guest-mode push site.
SITES = [
    ("shared/tracking-rules.md", "pushed to `<fork>` (the git model's fork remote) at the handoff"),
    ("shared/tracking-rules.md", "(the push to `<fork>` plus the `gh pr create` above)"),
    ("hotfix/SKILL.md", "`git push -u <fork> hotfix-<slug>`"),
    ("hotfix/SKILL.md", "and fix pushes to `<fork>`. Its `copilot:`"),
    ("milestone-review/SKILL.md", "`git push -u <fork> <slug>`"),
    ("milestone-review/SKILL.md", "and fix pushes to `<fork>`. When the round"),
    ("milestone-review/SKILL.md", "pushes it to `<fork>` and opens the PR"),
    ("milestone-review/SKILL.md", "fixed on the branch and pushed to `<fork>`"),
    ("milestone-implement/SKILL.md", "`git push --force-with-lease <fork> <slug>`"),
    ("shared/copilot-review.md", "(guest mode: to `<fork>`, the rulebook's fork remote,"),
    ("milestone/SKILL.md", "re-pushed to `<fork>`"),
]

ORIGIN_IS_FORK = re.compile(r"`origin`,? \(?the fork|the fork,? \(?`origin`", re.I)


def norm(text):
    return " ".join(text.split())


def read(rel):
    return norm(SKILLS.joinpath(rel).read_text(encoding="utf-8"))


def missing_sites(texts):
    """The SITES entries whose phrase is absent from `texts` (rel -> text)."""
    return [(rel, phrase) for rel, phrase in SITES if phrase not in texts[rel]]


def origin_fork_hits(text):
    return ORIGIN_IS_FORK.findall(text)


def skill_texts():
    return {
        p.relative_to(SKILLS).as_posix(): norm(p.read_text(encoding="utf-8"))
        for p in SKILLS.glob("**/*.md")
        if "tests/" not in p.relative_to(SKILLS).as_posix()
    }


class TestForkRecipe(unittest.TestCase):
    def test_recipe_clauses_present(self):
        text = read("shared/tracking-rules.md")
        for clause in RECIPE:
            self.assertIn(clause, text)

    def test_fork_owner_no_longer_reads_origin(self):
        text = read("shared/tracking-rules.md")
        self.assertNotIn("`<fork-owner>` reads `origin`", text)


class TestGuestPushSites(unittest.TestCase):
    def test_every_site_names_fork(self):
        texts = {rel: read(rel) for rel, _ in SITES}
        self.assertEqual(missing_sites(texts), [])

    def test_one_reverted_site_fails(self):
        texts = {rel: read(rel) for rel, _ in SITES}
        rel, phrase = SITES[8]
        texts[rel] = texts[rel].replace(phrase, phrase.replace("<fork>", "origin"))
        self.assertEqual(missing_sites(texts), [(rel, phrase)])


class TestNoOriginCalledFork(unittest.TestCase):
    def test_domain_not_empty(self):
        self.assertGreater(len(skill_texts()), 20)

    def test_no_skill_calls_origin_the_fork(self):
        hits = {rel: origin_fork_hits(t) for rel, t in skill_texts().items()}
        self.assertEqual({rel: h for rel, h in hits.items() if h}, {})

    def test_planted_phrase_is_found(self):
        planted = "synced by rebase, pushed to `origin` (the fork) at the handoff"
        self.assertEqual(len(origin_fork_hits(planted)), 1)
        self.assertEqual(len(origin_fork_hits("(guest mode: to `origin`, the fork, with")), 1)


if __name__ == "__main__":
    unittest.main()
