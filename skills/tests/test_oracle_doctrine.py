"""Regression guard: the oracle-type doctrine in the Validation doctrine (M33/M42/M58).

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

M58 (RR01 recs 6/9) extracted the doctrine to its own module,
`skills/shared/validation-doctrine.md` (the rulebook keeps a reference), and
added the registry-pointer requirement — a numeric-work repo declares *where*
its oracle records live. This guard reads the module; the rulebook must still
point at it.

Guard tests read the file as one string, so an asserted phrase must live on one
physical line (M23 lesson); phrases are lowercased before matching.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def doctrine():
    return (SKILLS / "shared" / "validation-doctrine.md").read_text().lower()


def rulebook():
    return (SKILLS / "shared" / "tracking-rules.md").read_text().lower()


class TestOracleDoctrine(unittest.TestCase):
    def test_names_the_five_oracle_types(self):
        text = doctrine()
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
        self.assertIn("a ci method's oracle is coverage", doctrine())

    def test_states_the_two_independent_types_bar(self):
        # The strengthening over the old "every numeric result via an oracle":
        # ≥2 oracles of *independent types*, never two instances of one.
        self.assertIn("≥2 *independent* oracle types", doctrine())

    def test_states_live_is_the_stronger_form(self):
        # A live independent implementation beats a frozen regression pin.
        self.assertIn("independent implementation is the *stronger*", doctrine())

    def test_states_the_reproducibility_hard_stop(self):
        # Sourcing is necessary but not sufficient — the value must regenerate.
        self.assertIn("unsourced *or unreproducible*", doctrine())

    def test_oracle_registry_records_the_audit_fields(self):
        # M51/D-029: at scale the ≥2-types bar is only checkable if each oracle
        # is recorded — the per-oracle field list, single-sourced to its test.
        self.assertIn(
            "**id, type, asserting `test:line`, source, and provenance**",
            doctrine(),
        )

    def test_oracle_registry_is_shape_free(self):
        # M51/D-029: content not shape — a central file, distributed headers,
        # or embedded fixture fields all satisfy the registry requirement.
        self.assertIn("shape is the repo's choice", doctrine())


class TestModuleExtraction(unittest.TestCase):
    """M58 (RR01 rec 9): the doctrine lives in its own module; the rulebook
    keeps a reference so every skill (which reads the rulebook whole) learns
    the module exists — rulebook-reference-only wiring, no per-skill lines."""

    def test_rulebook_points_at_the_module(self):
        # The unique reference-section phrase, not the bare path (which also
        # appears in the References-pages section) — keeps the mutation
        # harness's blank-one-block proof honest.
        self.assertIn("lives in `skills/shared/validation-doctrine.md`", rulebook())

    def test_rulebook_states_the_module_norm(self):
        # The placement norm the extraction establishes (D-entry in M58).
        self.assertIn("gets a module, not a rulebook", rulebook())

    def test_rulebook_no_longer_carries_the_doctrine_body(self):
        # Negative regression guard (not mutation-registrable — M54 lesson);
        # positive pairs are the module-content asserts above and the two
        # rulebook-reference asserts in this class.
        self.assertNotIn("≥2 *independent* oracle types", rulebook())
        self.assertNotIn("**oracle types & the ≥2-types bar.**", rulebook())


class TestRegistryPointer(unittest.TestCase):
    """M58 (RR01 recs 4→6, §4): the shape-free registry gains an address — a
    numeric-work repo declares where its oracle records live (DESIGN.md
    Conventions); absence of the declaration is itself the audit finding.
    No validate CHECK — advisory prose enforced by review judgment (D-029)."""

    def test_registry_pointer_is_required(self):
        self.assertIn("declares *where* its oracle records live", doctrine())

    def test_pointer_absence_is_the_audit_finding(self):
        self.assertIn(
            "absence of the line in a repo with numeric work is itself the audit",
            doctrine(),
        )


if __name__ == "__main__":
    unittest.main()
