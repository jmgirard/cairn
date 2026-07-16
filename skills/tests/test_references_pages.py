"""Regression guard: the references/ page-type doctrine (M57).

M56 found practice had outgrown the file map's "Source summaries" phrasing —
cross-source synthesis notes (competitive-landscape.md, migration-pilot-notes.md)
already live in `references/` unnamed. M57 legitimizes the second page type:
the file map names both committed page types (source notes + synthesis notes),
and the Source-ingestion section defines synthesis notes under the same
one-line-in-INDEX rule, mechanized by `cairn_validate`'s references check.

Guard tests read the file as one string, so an asserted phrase must live on one
physical line (M23 lesson); phrases are lowercased before matching.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rulebook():
    return (SKILLS / "shared" / "tracking-rules.md").read_text().lower()


class TestReferencesPages(unittest.TestCase):
    def test_file_map_names_both_page_types(self):
        # The file-map row names source notes AND synthesis notes as the two
        # committed page types — not the outgrown "source summaries" alone.
        self.assertIn(
            "source notes (`<citekey>.md`), synthesis notes", rulebook()
        )

    def test_ingestion_defines_synthesis_notes(self):
        # The Source-ingestion section defines the second page type in place.
        self.assertIn(
            "the second committed `references/` page type", rulebook()
        )

    def test_every_committed_page_carries_an_index_line(self):
        # The rule the references check mechanizes: page on disk ⇒ INDEX line.
        self.assertIn(
            "every committed `references/` page carries its", rulebook()
        )


if __name__ == "__main__":
    unittest.main()
