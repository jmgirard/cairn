"""Mutation-harness engine (M53): mechanize the "mentally delete the feature"
false-coverage check for prose-guards.

A *prose-guard* is a test that reads a source file (`tracking-rules.md`, a
`SKILL.md`, `DESIGN.md`, …) as text and `assertIn`s phrases from a rule it
protects. Such a guard gives *false coverage* when a phrase it asserts also
occurs elsewhere in the file: deleting the rule's own occurrence leaves the
assertion satisfied, so the guard passes even though the rule is gone
(the recurring M23/M26/M39/M40/M47/M48/M50 trap).

This engine blanks the exact block a guard protects and re-runs *that guard*
against the mutated content: a guard that still passes is false coverage,
caught here at authoring time instead of by a review lens milestones later.

Mechanism is **zero-touch** on existing guards: every guard reads its source
via `pathlib.Path.read_text()`, so a single scoped patch of that method feeds
the mutated content back without any guard code change (verified M53: no guard
reads at import time).

Not a test module itself (no `test_` prefix) — imported by
`test_mutation_harness.py`, which owns the registry and the assertions.
"""

import importlib
import pathlib
import sys
import unittest
from unittest import mock

ENGINE_DIR = pathlib.Path(__file__).resolve().parent   # skills/tests
SKILLS = ENGINE_DIR.parent                             # skills
REPO = SKILLS.parent                                   # repo root

# Guards import their siblings by bare module name under `discover -s
# skills/tests`; make that resolution work regardless of how this module is
# imported (discover, `-m unittest <dotted>`, direct).
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))


def blank_block(content, block):
    """Return `content` with `block` removed. `block` must occur exactly once
    — zero or many is a hard error (an ambiguous or drifted locator must fail
    loudly, never silently blank the wrong region or nothing)."""
    n = content.count(block)
    if n != 1:
        raise ValueError(
            f"block locator must occur exactly once (found {n}): {block!r}"
        )
    return content.replace(block, "", 1)


def _run_single(test_cls, method, target_abspath, mutated_content):
    """Run one test method with reads of `target_abspath` redirected to
    `mutated_content`; every other file read passes through untouched."""
    real_read_text = pathlib.Path.read_text

    def fake_read_text(self, *args, **kwargs):
        try:
            hit = self.resolve() == target_abspath
        except OSError:
            hit = False
        if hit:
            return mutated_content
        return real_read_text(self, *args, **kwargs)

    result = unittest.TestResult()
    with mock.patch.object(pathlib.Path, "read_text", fake_read_text):
        test_cls(method).run(result)
    return result


def guard_fails_when_blanked(target_rel, block, test_cls, method):
    """True iff blanking `block` in `target_rel` makes `test_cls.method` fail —
    i.e. the guard actually notices its rule is gone. A False return means the
    guard is false coverage."""
    target = (REPO / target_rel).resolve()
    mutated = blank_block(target.read_text(), block)
    result = _run_single(test_cls, method, target, mutated)
    return not result.wasSuccessful()


def load_case(module_name, dotted):
    """Resolve a registered `"ClassName.method"` in a guard module to its
    (TestCase subclass, method name)."""
    module = importlib.import_module(module_name)
    cls_name, method = dotted.rsplit(".", 1)
    return getattr(module, cls_name), method
