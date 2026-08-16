"""M112 (D-062): softening the Fable warning must not drop its gate.

D-062 lowered the cost framing and the recommend bar, but explicitly retained
two invariants: the per-instance explicit-approval gate, and the RB/RR-only
escalation path (ad-hoc Fable spawning stays prohibited). These guards pin both
so a future 'soften further' edit cannot silently remove them — the whole point
of M112's Scope `Out`.

Anchors are copied from the target files' actual bytes (M95).

Run: python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    # pathlib read_text, never open(): the mutation engine redirects reads by
    # patching Path.read_text (test_finding_enforcement.py:23-26).
    return SKILLS.joinpath(*parts).read_text(encoding="utf-8")


class TestPerInstanceApprovalGate(unittest.TestCase):
    def test_brief_requires_explicit_per_instance_approval(self):
        # milestone-brief: approval every time, only through this protocol.
        text = read("milestone-brief", "SKILL.md")
        self.assertIn("explicit user approval, every time", text)
        self.assertIn("only ever through this\nprotocol", text)


if __name__ == "__main__":
    unittest.main()
