"""Fixture tests for cairn_validate's §1 scaffold-drift check (M24).

Reuses the shared, fully-scaffolded ``Tree`` fixture from test_scripts and
removes exactly one required piece per case, asserting the scaffold check
FAILs and names it. The empty-dir carve-out (git drops empty dirs) and the
package-only ``.Rbuildignore`` rule get their own cases. This locks the two
gaps that bit the tidymedia repair: a missing ``LESSONS.md`` and a missing
``cairn/.merge-approved`` .gitignore entry.

    python3 -m unittest discover -s scripts/tests -v
"""

import unittest

from test_scripts import ScriptCase, run

LABEL = "scaffold present"


def set_gitignore(root, entries):
    (root / ".gitignore").write_text("".join(f"{e}\n" for e in entries))


class TestScaffoldClean(ScriptCase):
    def test_full_scaffold_passes(self):
        # The base fixture never creates cairn/reviews/ or cairn/references/pdf/
        # (empty scaffold dirs), yet the check passes — proving the carve-out.
        root = self.tree.build()
        self.assertFalse((root / "cairn" / "reviews").exists())
        self.assertFalse((root / "cairn" / "references" / "pdf").exists())
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn(f"PASS  {LABEL}", proc.stdout)


class TestScaffoldFailures(ScriptCase):
    def assert_scaffold_fail(self, root, needle):
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn(f"FAIL  {LABEL}", proc.stdout)
        self.assertIn(needle, proc.stdout)

    def test_missing_design(self):
        root = self.tree.build()
        (root / "cairn" / "DESIGN.md").unlink()
        self.assert_scaffold_fail(root, "cairn/DESIGN.md")

    def test_missing_lessons(self):
        # The exact gap the tidymedia migration left (LESSONS.md added to §1
        # after that repo adopted cairn).
        root = self.tree.build()
        (root / "cairn" / "LESSONS.md").unlink()
        self.assert_scaffold_fail(root, "cairn/LESSONS.md")

    def test_missing_references_index(self):
        root = self.tree.build()
        (root / "cairn" / "references" / "INDEX.md").unlink()
        self.assert_scaffold_fail(root, "cairn/references/INDEX.md")

    def test_missing_merge_approved_gitignore_entry(self):
        # The other tidymedia gap — .merge-approved ignore line absent.
        root = self.tree.build()
        set_gitignore(
            root, ["cairn/references/pdf/", "cairn/.merge-approved.pending"]
        )
        self.assert_scaffold_fail(root, "cairn/.merge-approved")

    def test_missing_pending_gitignore_entry(self):
        # The consumed-but-unresolved marker state (M60) is required too —
        # and the exact-line check must not let the plain marker entry
        # satisfy it.
        root = self.tree.build()
        set_gitignore(root, ["cairn/references/pdf/", "cairn/.merge-approved"])
        self.assert_scaffold_fail(root, "cairn/.merge-approved.pending")

    def test_missing_pdf_gitignore_entry(self):
        root = self.tree.build()
        set_gitignore(
            root, ["cairn/.merge-approved", "cairn/.merge-approved.pending"]
        )
        self.assert_scaffold_fail(root, "cairn/references/pdf/")

    def test_gitignore_absent_entirely(self):
        root = self.tree.build()
        (root / ".gitignore").unlink()
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn(f"FAIL  {LABEL}", proc.stdout)
        self.assertIn("cairn/.merge-approved", proc.stdout)
        self.assertIn("cairn/references/pdf/", proc.stdout)


class TestScaffoldRbuildignore(ScriptCase):
    """The `^cairn$` .Rbuildignore entry is required only on package repos."""

    def test_package_missing_rbuildignore_entry_fails(self):
        root = self.tree.build()
        (root / "DESCRIPTION").write_text("Package: fixture\nVersion: 0.0.1\n")
        # no .Rbuildignore at all
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn(f"FAIL  {LABEL}", proc.stdout)
        self.assertIn("^cairn$", proc.stdout)

    def test_package_with_rbuildignore_entry_passes(self):
        root = self.tree.build()
        (root / "DESCRIPTION").write_text("Package: fixture\nVersion: 0.0.1\n")
        (root / ".Rbuildignore").write_text("^cairn$\n")
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn(f"PASS  {LABEL}", proc.stdout)

    def test_non_package_needs_no_rbuildignore(self):
        # No DESCRIPTION → the ^cairn$ entry is irrelevant; base fixture passes.
        root = self.tree.build()
        self.assertFalse((root / "DESCRIPTION").exists())
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn(f"PASS  {LABEL}", proc.stdout)


if __name__ == "__main__":
    unittest.main()
