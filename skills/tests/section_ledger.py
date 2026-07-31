"""Derive a doctrine section's sentence sequence from the section's own bytes.

A prose-guard pins that a sentence is PRESENT. It does not pin that the
section stays CONSISTENT: a contradicting sentence added elsewhere in the same
section, a defined term renamed to a coinage that reuses none of its words, or
a list relocated out from under a back-reference all leave every anchor
matching. Measured at M123's §8 certification, where eight of ten mutations
touching no pinned block defeated six acceptance-criterion clauses with the
whole suite green.

This module is the extraction half of the remedy. `sentences()` returns a
section's ordered, whitespace-normalized sentence sequence; a guard compares
that sequence against a committed ledger and reports what differs. The two
halves are deliberately separate (M124 AC1/AC2): the extraction never receives
the ledger, so it cannot be tuned to agree with it.

**No content-drawn enumerations.** The extraction takes no list of terms,
phrases, or subjects from any section it reads — that enumeration is the
failure `guard-doctrine.md` §3 names, and the class this module exists for has
already beaten five successive hand-extended matchers over §8 alone. One
closed punctuation class ships under AC1's carve-out, `_SENTENCE_BOUNDARY`,
with the comment AC1 requires; no abbreviation class is needed, because §8
carries no abbreviation-shaped mid-sentence period.
`test_extraction_carries_no_word_constant` holds the no-content-word property
to the shipped bytes rather than to intent, and
`test_each_module_constant_names_the_class_it_closes_over` holds the comment.

**Normalization is what makes a reflow invisible.** Whitespace is collapsed
before splitting, so re-wrapping a paragraph yields the identical sequence and
the guard stays green — provided the re-wrap does not break a hyphenated
compound, which changes the token sequence and is a real difference (M124 AC4;
`zero-unresolved` split across a wrap is the measured case).

Targets are read with `Path.read_text` because the mutation engine patches
only that call (M100).
"""

import difflib
import pathlib
import re

# The heading that introduces a section, and the marker that ends it. Both are
# markdown structure, not content: no term, phrase, or subject drawn from any
# section appears in this module (AC1).
_NEXT_SECTION = re.compile(r"\n## ")

# A sentence boundary is terminal punctuation followed by whitespace. This is a
# closed punctuation class in AC1's sense, and it is the ONLY lexical constant
# here. §8 carries no abbreviation-shaped mid-sentence period (no `e.g.`,
# `i.e.`, `etc.`, `vs.`), so no abbreviation suppression is needed; a section
# that acquires one will need the carve-out AC1 already permits, and the
# constant added for it carries a comment naming the class it closes over.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def section_body(path, heading):
    """Return the body under `heading`, excluding the heading line itself.

    Bounded at the next `## ` heading, or at end of file where the section is
    the last one. Excluding the heading matters: a heading like `## 8. The
    author...` ends in a numeral-period and would otherwise split off as a
    spurious first "sentence".
    """
    content = pathlib.Path(path).read_text()
    start = content.index(heading)
    rest = content[start + len(heading):]
    end = _NEXT_SECTION.search(rest)
    return rest[:end.start()] if end else rest


def sentences(path, heading):
    """Return the section's ordered, whitespace-normalized sentence sequence."""
    flat = " ".join(section_body(path, heading).split())
    return [s for s in _SENTENCE_BOUNDARY.split(flat) if s]


def diff(ledger, current):
    """Describe how `current` departs from `ledger`, aligned.

    Alignment matters, and a set difference is the wrong instrument: measured
    on a pure one-sentence insertion, comparing by index reports `added=1,
    moved=35`, which buries the one real change under every sentence that
    merely shifted position. `SequenceMatcher` reports the same insertion as a
    single opcode. So "moved" here means a sentence that survives alignment at
    a different position, never one displaced by an edit above it (AC2).
    """
    added, removed = [], []
    matcher = difflib.SequenceMatcher(None, ledger, current, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "delete"):
            removed.extend(ledger[i1:i2])
        if tag in ("replace", "insert"):
            added.extend(current[j1:j2])
    # A sentence present on both sides of the alignment gap moved rather than
    # being replaced; report it as such so a relocation does not read as an
    # unrelated add plus an unrelated delete.
    moved = [s for s in added if s in removed]
    return {
        "added": [s for s in added if s not in moved],
        "removed": [s for s in removed if s not in moved],
        "moved": moved,
    }


def describe(ledger, current):
    """Render `diff` as a guard failure message, or "" when the two agree."""
    delta = diff(ledger, current)
    if not any(delta.values()):
        return ""
    lines = []
    for label in ("added", "removed", "moved"):
        for sentence in delta[label]:
            lines.append(f"  {label.upper():<8}{sentence}")
    return (
        f"the section and its ledger differ by {len(lines)} sentence(s); "
        f"regenerate the ledger and read this diff before accepting it:\n"
        + "\n".join(lines)
    )


def render(path, heading):
    """Render a ledger file's contents: one sentence per line.

    One sentence per line is the format because the diff is the mechanism —
    §9's remedy is that the author reads what changed, and a line-oriented file
    is what `git diff` renders legibly. Sentences are whitespace-normalized, so
    none contains a newline and the format is unambiguous.
    """
    return "".join(s + "\n" for s in sentences(path, heading))


if __name__ == "__main__":
    # Regeneration, which is the first step of the remedy `guard-doctrine.md`
    # §9 assigns: `python3 skills/tests/section_ledger.py <file> <heading>`.
    import sys

    sys.stdout.write(render(sys.argv[1], sys.argv[2]))
