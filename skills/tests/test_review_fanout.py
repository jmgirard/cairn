"""Regression guard: the /milestone-review fan-out + confidence scorer.

The review gate's independent review is a three-lens fan-out (distinct evidence
bases) followed by a generate-then-verify confidence scorer. These are
skill-text mechanics — nothing at runtime enforces them — so this test locks
the load-bearing pieces against silent regression:
  * three reviewers with *distinct* evidence bases, tier-tagged (Opus diff-bug,
    Sonnet blame-history, Sonnet prior-PR-comments — M40);
  * a Sonnet confidence scorer, independent of finding generation, with a
    numeric threshold;
  * sub-threshold findings excluded from the actioned list but *logged*, never
    silently dropped (IP3);
  * the reviewers told to report everything and filter nothing, with the
    false-positive taxonomy carried in the scorer's rubric instead (M120,
    D-078);
  * the model-strategy section describing the fan-out while keeping the blanket
    "Never Haiku" rule (D-016).

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
    def test_three_distinct_evidence_lenses(self):
        t = review()
        self.assertRegex(t, r"diff-bug reviewer \(Opus\)")
        self.assertRegex(t, r"blame-history reviewer \(Sonnet\)")
        self.assertRegex(t, r"prior-PR-comments reviewer \(Sonnet\)")

    def test_evidence_bases_are_distinct_by_design(self):
        # the whole point of the fan-out — a shared base finds things twice
        self.assertIn("distinct evidence base", review())

    def test_blame_lens_reads_history_not_just_diff(self):
        t = review()
        self.assertIn("git blame", t)
        self.assertIn("git log", t)

    def test_confidence_scorer_present_with_threshold(self):
        t = review()
        self.assertIn("scorer", t.lower())
        self.assertIn("confidence", t.lower())
        self.assertRegex(t, r"\b80\b")

    def test_scorer_is_independent_of_generation(self):
        # generate-then-verify: the scorer must not be the finding generator
        self.assertRegex(review(), r"did \*?not\*? generate")

    def test_subthreshold_findings_logged_not_dropped(self):
        t = review()
        self.assertRegex(t, r"below 80.*excluded")
        self.assertIn("logged", t)
        self.assertRegex(t, r"never\s+silently\s+dropped")

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

    def test_false_positive_taxonomy_lives_in_the_scorer_rubric(self):
        # Each member is pinned WITH its predicate, never as a bare token:
        # guard-doctrine §1's label->SET trap is that pinning `nitpick` alone
        # leaves the set swappable — "a pre-existing issue the diff DID
        # introduce" keeps every bare token and inverts the taxonomy.
        rubric = self._scorer_rubric()
        self.assertIn("Not a finding, and out of scope for this diff", rubric)
        for member in (
            "a pre-existing issue the diff did not introduce",
            "anything a linter or formatter would catch",
            "a pure style nitpick",
            "a complaint about an unmodified line",
            "an intentional change the milestone's plan called for",
        ):
            with self.subTest(member=member):
                self.assertIn(member, rubric)

    def test_taxonomy_carries_its_scoring_disposition(self):
        # The members are inert without this sentence: it is what makes a
        # taxonomy match score sub-60 and so land in the logged-but-not-
        # actioned list rather than being dropped. Deleting it left every
        # other assert in this file green (M120 review, P2).
        self.assertIn(
            "Score anything matching this list below 60", self._scorer_rubric()
        )

    def test_reviewers_report_everything_and_filter_nothing(self):
        # Absence-assert paired with its positive framing (guard-doctrine §3):
        # `assertNotIn` alone is satisfied by an empty read, so the instruction
        # that REPLACED the pre-filter is asserted first, and it is that phrase
        # the mutation harness registers.
        t = review()
        self.assertIn("report every candidate finding", t)
        self.assertNotIn("drop anything matching it before reporting", t)

    def test_model_strategy_describes_fanout_and_keeps_never_haiku(self):
        r = rules()
        self.assertIn("Never Haiku", r)
        self.assertIn("fan-out", r)
        self.assertRegex(r, r"scorer \(Sonnet\)")

    def test_fanout_states_why_a_fresh_model_reviews(self):
        # M35 AC4: the fan-out states *why* review uses a fresh/different model
        # — an author shares their own diff-blindness (M23: one physical line).
        r = rules()
        self.assertIn("fresh-context subagents", r)
        self.assertIn("diff-blindness", r)

    def test_model_strategy_names_three_reviewers(self):
        # M40: the fan-out grew a third distinct-evidence lens; the
        # model-strategy section must count three and name the new lens.
        r = rules()
        self.assertRegex(r, r"[Tt]hree distinct-evidence reviewers")
        self.assertIn("prior-PR", r)


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

    def test_new_lens_defers_scoring_to_shared_scorer(self):
        # AC4: the prior-PR lens funnels into the single shared [S] scorer and
        # introduces NO scoring of its own. This isolates the lens block and
        # asserts it carries no "score" token — lens-specific and M40-dependent
        # (deleting the lens makes the split raise, failing the test), unlike a
        # bare "scorer"/"80" assertion that pre-exists and passes even with the
        # lens removed (the M39 false-coverage trap; caught by M40's own review).
        t = review()
        lens = t.split("prior-PR-comments reviewer (Sonnet)")[1].split("\n\n")[0]
        self.assertNotIn("score", lens.lower())


class TestSharedCheckoutGuard(unittest.TestCase):
    """M37: cairn-spawned subagents share the primary checkout, so they use
    ref-based git only — never a HEAD-moving command (checkout/worktree add)
    in that tree (a reviewer that did so parked the checkout mid-M36-review).
    This is locked in two places: the general subagent-conduct rule in the
    shared rulebook, and the pointed reminder at the /milestone-review step.
    Phrases are asserted case-insensitively and each lives on one physical
    line (M23 newline, M26 bold-split lessons)."""

    def test_tracking_rules_states_general_shared_checkout_rule(self):
        r = rules().lower()
        self.assertIn("ref-based git only", r)
        self.assertIn("primary checkout", r)
        # names the prohibited HEAD-moving commands, not just "no checkout"
        self.assertIn("git checkout", r)
        self.assertIn("git worktree add", r)

    def test_review_fanout_reminds_reviewers_ref_based_only(self):
        t = review().lower()
        self.assertIn("ref-based git only", t)
        self.assertIn("working tree", t)
        self.assertIn("git checkout", t)
        self.assertIn("git worktree add", t)


if __name__ == "__main__":
    unittest.main()
