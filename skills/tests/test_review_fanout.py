"""Regression guard: the /milestone-review fan-out.

The review gate's independent review is a four-lens fan-out (distinct evidence
bases) whose ranked findings the maintainer triages at the gate. These are
skill-text mechanics — nothing at runtime enforces them — so this test locks
the load-bearing pieces against silent regression:
  * four reviewers with *distinct* evidence bases, each naming its model
    (Opus diff-bug, Haiku blame-history, Haiku prior-PR-comments — M40,
    the two history lenses moved from Sonnet to Haiku by M269 — and Haiku
    ripple, M285);
  * the prior-PR lens reading archived Review sections first, walking PR
    threads only behind a probe, always spawned, and scoring nothing itself;
  * the reviewers reminded to use ref-based git only in the shared tree;
  * the model-strategy section counting four distinct-evidence reviewers
    and naming the two history lenses under Haiku, never Sonnet (M269);
  * the ripple lens in the docs-only pair and in the four-lens list, with
    its no-op case (M285);
  * Explore searches routed to Haiku in the rulebook and at the four skill
    sites that spawn them, with no Sonnet subagents bullet left (M277).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def review():
    return read("milestone-review", "SKILL.md")


def rules():
    return read("shared", "tracking-rules.md")


class TestReviewFanout(unittest.TestCase):
    def test_four_distinct_evidence_lenses(self):
        t = review()
        self.assertRegex(t, r"Diff-bug reviewer \(Opus\)")
        self.assertRegex(t, r"Blame-history reviewer \(Haiku\)")
        self.assertRegex(t, r"Prior-PR-comments reviewer \(Haiku\)")
        self.assertRegex(t, r"Ripple reviewer \(Haiku\)")

    def test_ripple_lens_runs_in_both_modes_and_noops(self):
        # M285 (D-185): the docs-only mode spawns the ripple lens beside the
        # diff-bug lens, and a diff that removes or changes nothing gives a
        # clean no-op. Whitespace is collapsed so a wrap still matches.
        t = " ".join(review().split())
        self.assertIn("the Opus diff-bug lens and the Haiku ripple lens below", t)
        self.assertIn("spawn the full four-lens fan-out", t)
        self.assertIn('"no ripple evidence"', t)

    def test_evidence_bases_are_distinct_by_design(self):
        # the whole point of the fan-out — a shared base finds things twice
        self.assertIn("distinct evidence base", review())

    def test_blame_lens_reads_history_not_just_diff(self):
        t = review()
        self.assertIn("git blame", t)
        self.assertIn("git log", t)


    def _scorer_rubric(self):
        """The scorer's rubric blockquote, located by its OWN first line.

        M120: asserting the taxonomy merely occurs in `SKILL.md` would pass
        with it still sitting in the reviewers' instruction — the arrangement
        this milestone exists to end. So the rubric is found by the text only
        it carries, and read as the contiguous blockquote run from there;
        slicing between two unrelated marker blocks would make the guard
        report on whatever happened to fall between them.
        """
        lines = review().splitlines()
        start = next(
            i for i, ln in enumerate(lines)
            if "Score 0–100 your confidence" in ln
        )
        run = []
        for ln in lines[start:]:
            if not ln.lstrip().startswith(">"):
                break
            run.append(ln)
        # A one-line run would make every membership assert below trivially
        # scoped to the rubric's own first sentence.
        self.assertGreater(len(run), 1, "scorer rubric blockquote not parsed")
        return "\n".join(run)


    def test_model_strategy_names_four_reviewers(self):
        # M40 grew a third distinct-evidence lens and M285 a fourth; the
        # model-strategy section must count four and name the ripple lens.
        r = " ".join(rules().split())
        self.assertRegex(r, r"[Ff]our distinct-evidence reviewers")
        self.assertIn("prior-PR", r)
        self.assertIn("Haiku ripple", r)

    def test_model_strategy_routes_history_lenses_to_haiku(self):
        # M269 (D-174): the review bullet names both history lenses under
        # Haiku, and no bullet names them under Sonnet. Whitespace is
        # collapsed so a wrap between the model and the lens name still
        # matches (the bullet wraps there today).
        r = " ".join(rules().split())
        self.assertIn("Opus diff-bug, Haiku blame-history, Haiku prior-PR-comments", r)
        self.assertNotRegex(r, r"Sonnet (blame-history|prior-PR-comments)")


class TestSearchModel(unittest.TestCase):
    """M277 (D-181): Explore searches run on Haiku. The rulebook's Haiku
    bullet names them, the Sonnet subagents bullet is gone, and each skill
    site that spawns an Explore fan-out names Haiku for it. Whitespace is
    collapsed so a wrap inside a phrase still matches."""

    SITES = {
        ("milestone-plan", "SKILL.md"): "fan out Haiku Explore subagents",
        ("milestone-implement", "SKILL.md"):
            "Haiku for well-specified mechanical work, test writing against "
            "a spec, boilerplate, and Explore searches",
        ("design-interview", "SKILL.md"): "fan out Haiku Explore subagents",
        ("cairn-triage", "SKILL.md"): "One Haiku Explore fan-out",
    }

    def test_rulebook_haiku_bullet_names_fan_out_searches(self):
        r = rules()
        start = r.index("- **Haiku subagents**")
        end = r.index("\n- **", start + 1)
        bullet = " ".join(r[start:end].split())
        self.assertIn("fan-out searches (Explore", bullet)
        self.assertIn("reading list", bullet)
        self.assertNotIn("**Sonnet subagents**", r)
        # No bullet of the section names Sonnet as a model a spawn sets: the
        # set-the-model list names the three models in use, and every
        # remaining "Sonnet" in the section is a past-measurement clause.
        sec = r[r.index("## Model and agent strategy"):r.index("## Toolchain profiles")]
        flat = " ".join(sec.split())
        self.assertIn("a role calls for (Haiku, Opus, or Fable,", flat)
        self.assertEqual(
            flat.count("Sonnet"), flat.count("measured on Sonnet"),
            "a Sonnet mention in the model section is not a past measurement",
        )

    def test_each_explore_site_names_haiku(self):
        for parts, phrase in self.SITES.items():
            with self.subTest(site="/".join(parts)):
                t = " ".join(read(*parts).split())
                self.assertIn(phrase, t)
                self.assertNotRegex(t, r"Sonnet (for )?Explore")


class TestPriorPRLens(unittest.TestCase):
    """M40: the third distinct-evidence lens — a prior-PR-comments reviewer.
    M101 repointed its input surfaces: primary evidence is the archived
    `## Review` sections (M91 measured the PR threads empty), and the GitHub
    PR-thread read survives only behind a cheap existence probe. This locks
    the new recipe and fails on the old always-read-the-threads one; the
    narrow judgment scope and always-spawn/no-op contract carry over from
    M40. Each asserted phrase is anchored on the lens's own contiguous line
    (M23/M26/M39 single-line rule).
    """

    def test_primary_evidence_is_archived_review_sections(self):
        # M101: the substantive review record lives in milestones/archive/
        # `## Review` sections, and the lens must say so as its primary base
        t = review()
        self.assertIn("Primary evidence: archived", t)
        self.assertIn("`cairn/milestones/archive/`, not in", t)

    def test_pr_thread_read_is_probe_gated(self):
        # M101: the thread walk runs only when a cheap existence probe finds
        # real review threads — never unconditionally (the measured no-op)
        t = review()
        self.assertIn("probe-gated", t)
        self.assertRegex(t, r"pulls/comments\?per_page=1")
        self.assertIn("only when the probe finds", t)

    def test_discovery_is_a_prose_gh_recipe(self):
        # recipe-in-prose, not a cairn_* helper script (plan gate); the
        # per-PR walk endpoint survives inside the probe-gated branch
        t = review()
        self.assertIn("gh api", t)
        self.assertRegex(t, r"pulls/\{n\}/comments")

    def test_judgment_scope_is_narrow_regression(self):
        # flags only where the diff regresses a prior review finding — not
        # every prior finding surfaced as context (plan gate: narrow)
        self.assertIn("reintroduces or contradicts", review())

    def test_always_spawns_and_noops_when_empty(self):
        # always spawn; no prior-review evidence on either surface → zero
        # findings, never blocks (M101 restates the M40 contract)
        t = review()
        self.assertRegex(t, r"[Aa]lways spawn")
        self.assertIn('"no prior-review evidence"', t)
        self.assertIn("either surface", t)

    def test_new_lens_defers_to_gate_triage(self):
        # AC4: the prior-PR lens funnels into the maintainer's gate triage and
        # introduces NO scoring of its own. This isolates the lens block and
        # asserts it carries no "score" token — lens-specific and M40-dependent
        # (deleting the lens makes the split raise, failing the test), unlike a
        # bare "scorer"/"80" assertion that pre-exists and passes even with the
        # lens removed (the M39 false-coverage trap; caught by M40's own review).
        t = review()
        lens = t.split("Prior-PR-comments reviewer (Haiku)")[1].split("\n\n")[0]
        self.assertNotIn("score", lens.lower())


class TestSharedCheckoutGuard(unittest.TestCase):
    """M37: cairn-spawned subagents share the primary checkout, so they use
    ref-based git only — never a HEAD-moving command (checkout/worktree add)
    in that tree (a reviewer that did so parked the checkout mid-M36-review).
    This is locked in two places: the general subagent-conduct rule in the
    shared rulebook, and the pointed reminder at the /milestone-review step.
    Phrases are asserted case-insensitively and each lives on one physical
    line with no bold marker inside it, since a line break or a bold marker
    splits the phrase."""


    def test_review_fanout_reminds_reviewers_ref_based_only(self):
        t = review().lower()
        self.assertIn("ref-based git only", t)
        self.assertIn("working tree", t)
        self.assertIn("git checkout", t)
        self.assertIn("git worktree add", t)


if __name__ == "__main__":
    unittest.main()
