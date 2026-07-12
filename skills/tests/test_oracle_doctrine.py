"""Regression guard: the oracle-type doctrine in the Validation doctrine (M33/M42).

M33 folded the generalizable core of ackwards' M57 oracle discipline into the
shared rulebook's "Validation doctrine (statistical/numeric packages)" section
(D-024): the frozen/live/invariant/closed-form type vocabulary, the "live
independent-impl is the stronger form" nuance, the ≥2-independent-oracle-types
bar, and the reproducibility hard-stop. M42 validated that doctrine against
intraclass's real 34-script oracle system and found its four types omit the
oracle 31/34 of those scripts use — simulation-coverage (recovery of a known
population parameter / nominal Monte-Carlo interval coverage), the defining
oracle for interval methods and the missing analog of intraclass's inviolable
PRINCIPLES.md #1(c). D-025 added it as the fifth type; this guard locks all
five anchors against a future edit silently dropping them.

Guard tests read the file as one string, so an asserted phrase must live on one
physical line (M23 lesson); phrases are lowercased before matching.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rulebook():
    return (SKILLS / "shared" / "tracking-rules.md").read_text().lower()


class TestOracleDoctrine(unittest.TestCase):
    def test_names_the_five_oracle_types(self):
        text = rulebook()
        for oracle_type in (
            "**frozen**",
            "**live**",
            "**invariant**",
            "**closed-form**",
            "**simulation-coverage**",
        ):
            with self.subTest(type=oracle_type):
                self.assertIn(
                    oracle_type,
                    text,
                    f"Validation doctrine must name the oracle type {oracle_type}",
                )

    def test_simulation_coverage_is_the_interval_method_oracle(self):
        # M42/D-025: the fifth type is the probabilistic oracle — recovery of a
        # known population parameter / nominal coverage — and the primary oracle
        # for interval methods, which the four deterministic types cannot name.
        self.assertIn("a ci method's oracle is coverage", rulebook())

    def test_states_the_two_independent_types_bar(self):
        # The strengthening over the old "every numeric result via an oracle":
        # ≥2 oracles of *independent types*, never two instances of one.
        self.assertIn("≥2 *independent* oracle types", rulebook())

    def test_states_live_is_the_stronger_form(self):
        # A live independent implementation beats a frozen regression pin.
        self.assertIn("independent implementation is the *stronger*", rulebook())

    def test_states_the_reproducibility_hard_stop(self):
        # Sourcing is necessary but not sufficient — the value must regenerate.
        self.assertIn("unsourced *or unreproducible*", rulebook())


if __name__ == "__main__":
    unittest.main()
