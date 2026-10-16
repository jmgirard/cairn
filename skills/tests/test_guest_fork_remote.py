"""Regression guard: the guest-mode fork remote (M234) and push remote (M267).

In guest mode the operator's fork is not always `origin`. Three of seven
local guest checkouts keep the upstream at `origin` and the fork at a remote
named `fork`, so a push to `origin` there goes to the upstream repo. Since
M267 a guest repo can also push to the base repo instead of the fork. These
things have to survive:

  1. The rulebook's recipe. `<fork>` is the one remote, other than `<base>`,
     whose parent equals `<base-repo>`. A failed read is not a match, and no
     match or more than one stops a push bound for the fork. `<fork-owner>`
     reads `<fork>`.
  2. The push remote. `<push>` is `<base>` under `# Push remote: base`, else
     `<fork>`. A branch with an open PR is pushed to that PR's head remote.
  3. Every guest push site names `<push>` or the PR's head remote. The list
     is the whole list (M171 lesson): a test fails when any one site goes
     back to `<fork>` or `origin`.
  4. The push-access read before a handoff push to the base repo, in
     `/milestone-review` and `/hotfix`; implement's stop before it rebases
     over commits it does not have, with no check for a branch never
     pushed; and review's rebase, which takes that check first and leases
     step 8's push on the tip it read.
  5. No skill prose calls `origin` the fork.

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
    "When a guest push target resolves to the fork, by `<push>` or by an open PR's head, and no remote matches, or more than one, the push stops before it is made.",
    "A target that resolves to `<base>` needs no fork.",
    "The stop names the remotes it read, each parent it found, and each failed read.",
]

PUSH_REMOTE = [
    "In guest mode the **push remote** `<push>` is where a guest branch is pushed: `<base>` when `cairn/PROFILE.md` carries the header line `# Push remote: base`, else `<fork>`.",
    "Owner mode never reads the line.",
    "`<push-owner>` is the owner of the repo `<push>` names",
    "A push to a branch that already has an open PR goes to the remote that holds that PR's head, whatever `<push>` now says (the **open-PR head rule**).",
    "Read the head's owner with `gh pr view <N> --repo <base-repo> --json headRepositoryOwner -q .headRepositoryOwner.login`.",
    "The head remote is `<base>` when that login equals the base repo's owner, and `<fork>` when it equals `<fork-owner>`, both ignoring case.",
    "Any other login, or a failed or empty read, stops the push, and the stop names the read.",
]

# (file under skills/, phrase) for every guest-mode push site.
SITES = [
    ("shared/tracking-rules.md", "pushed to `<push>` (the git model's push remote: the fork, or the base repo where `cairn/PROFILE.md` asks for it) at the handoff"),
    ("shared/tracking-rules.md", "`gh pr create --repo <base-repo> --head <push-owner>:<slug>`"),
    ("shared/tracking-rules.md", "(the push to `<push>` plus the `gh pr create` above)"),
    ("hotfix/SKILL.md", "`git push -u <push> hotfix-<slug>`"),
    ("hotfix/SKILL.md", "`gh pr create --repo <base-repo> --head <push-owner>:hotfix-<slug>`"),
    ("hotfix/SKILL.md", "`git push <head-remote> HEAD:<headRefName>`"),
    ("hotfix/SKILL.md", "and fix pushes to the remote that holds the PR's head. Its `copilot:`"),
    ("milestone-review/SKILL.md", "`git push -u <push> <slug>`"),
    ("milestone-review/SKILL.md", "`gh pr create --repo <base-repo> --head <push-owner>:<slug>`"),
    ("milestone-review/SKILL.md", "and fix pushes to the remote that holds the PR's head. When the round"),
    ("milestone-review/SKILL.md", "pushes it to `<push>`, the fork or, where `cairn/PROFILE.md` asks, the base repo"),
    ("milestone-review/SKILL.md", "fixed on the branch and pushed to that remote before the close"),
    ("milestone-implement/SKILL.md", "`git push --force-with-lease=<slug>:<sha> <remote> <slug>`"),
    ("shared/copilot-review.md", "(guest mode: to the remote that holds the PR's head, found by the rulebook's open-PR head rule)"),
    ("milestone/SKILL.md", "re-pushed to the remote that holds the PR's head"),
]

ACCESS_READ = [
    "When `<push>` is `<base>`, first run `gh api repos/<base-repo> --jq .permissions.push`.",
    "On any output but `true`, or a failed read, push nothing, open no PR, and stop with a close block that names the read and its result.",
]
ACCESS_FILES = ["milestone-review/SKILL.md", "hotfix/SKILL.md"]

REMOTE_ONLY_STOP = [
    "so the rebase waits on one check, run before the rebase.",
    "Read the remote the branch tracks with `git config branch.<slug>.remote`",
    "With no remote set the branch was never pushed: rebase, and push nothing.",
    "read `git rev-list <slug>..<remote>/<slug>`.",
    "If that lists commits, do not rebase, push nothing, and stop with a close block that names those commits.",
    "Otherwise note the remote tip's sha, rebase, and push with",
]

# Review's guest rebase takes the check before it, and step 8 leases on its sha.
REVIEW_REBASE = [
    "after `/milestone-implement` step 2's remote-only-commits check, which runs before the rebase and notes the remote tip's sha.",
    "The rebased branch is not pushed here. Step 8 pushes it with that sha's lease.",
    "A pushed branch that step 1 rebased goes up with `--force-with-lease=<slug>:<sha>`, `<sha>` being the remote tip that step 1's check read.",
]

ORIGIN_IS_FORK = re.compile(r"`origin`,? \(?the fork|the fork,? \(?`origin`", re.I)


def norm(text):
    return " ".join(text.split())


def read(rel):
    return norm(SKILLS.joinpath(rel).read_text(encoding="utf-8"))


def missing(text, clauses):
    return [c for c in clauses if c not in text]


def missing_sites(texts):
    """The SITES entries whose phrase is absent from `texts` (rel -> text)."""
    return [(rel, phrase) for rel, phrase in SITES if phrase not in texts[rel]]


def origin_fork_hits(text):
    return ORIGIN_IS_FORK.findall(text)


def skill_texts():
    """Every skill markdown file outside `skills/tests/`, plus README.md."""
    texts = {
        p.relative_to(SKILLS).as_posix(): norm(p.read_text(encoding="utf-8"))
        for p in SKILLS.glob("**/*.md")
        if "tests/" not in p.relative_to(SKILLS).as_posix()
    }
    texts["README.md"] = norm(SKILLS.parent.joinpath("README.md").read_text(encoding="utf-8"))
    return texts


class TestForkRecipe(unittest.TestCase):
    def test_recipe_clauses_present(self):
        self.assertEqual(missing(read("shared/tracking-rules.md"), RECIPE), [])

    def test_fork_owner_no_longer_reads_origin(self):
        text = read("shared/tracking-rules.md")
        self.assertNotIn("`<fork-owner>` reads `origin`", text)


class TestPushRemote(unittest.TestCase):
    def test_definition_present(self):
        self.assertEqual(missing(read("shared/tracking-rules.md"), PUSH_REMOTE), [])

    def test_each_removed_clause_fails(self):
        text = read("shared/tracking-rules.md")
        for clause in PUSH_REMOTE:
            self.assertEqual(missing(text.replace(clause, ""), PUSH_REMOTE), [clause])

    def test_profile_row_names_the_line(self):
        self.assertIn("also the optional `# Push remote: base` header line", read("shared/tracking-rules.md"))


class TestGuestPushSites(unittest.TestCase):
    def test_every_site_names_the_push_target(self):
        texts = {rel: read(rel) for rel, _ in SITES}
        self.assertEqual(missing_sites(texts), [])

    def test_each_site_reverted_to_fork_fails(self):
        base = {rel: read(rel) for rel, _ in SITES}
        for rel, phrase in SITES:
            reverted = phrase.replace("<push-owner>", "<fork-owner>").replace("<push>", "<fork>")
            reverted = reverted.replace("<head-remote>", "<fork>").replace("<remote> <slug>", "<fork> <slug>")
            reverted = reverted.replace("the remote that holds the PR's head", "`<fork>`")
            reverted = reverted.replace("to that remote", "to `<fork>`")
            self.assertNotEqual(reverted, phrase, rel)
            texts = dict(base)
            texts[rel] = texts[rel].replace(phrase, reverted)
            self.assertEqual(missing_sites(texts), [(rel, phrase)])


class TestAccessRead(unittest.TestCase):
    def test_both_handoffs_read_push_access(self):
        for rel in ACCESS_FILES:
            self.assertEqual(missing(read(rel), ACCESS_READ), [], rel)

    def test_removed_read_fails_in_each_file(self):
        for rel in ACCESS_FILES:
            for clause in ACCESS_READ:
                self.assertEqual(missing(read(rel).replace(clause, ""), ACCESS_READ), [clause], rel)


class TestRemoteOnlyCommitsStop(unittest.TestCase):
    def test_stop_present(self):
        self.assertEqual(missing(read("milestone-implement/SKILL.md"), REMOTE_ONLY_STOP), [])

    def test_removed_stop_fails(self):
        text = read("milestone-implement/SKILL.md")
        for clause in REMOTE_ONLY_STOP:
            self.assertEqual(missing(text.replace(clause, ""), REMOTE_ONLY_STOP), [clause])


class TestReviewRebaseLease(unittest.TestCase):
    def test_present(self):
        self.assertEqual(missing(read("milestone-review/SKILL.md"), REVIEW_REBASE), [])

    def test_removed_clause_fails(self):
        text = read("milestone-review/SKILL.md")
        for clause in REVIEW_REBASE:
            self.assertEqual(missing(text.replace(clause, ""), REVIEW_REBASE), [clause])


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
