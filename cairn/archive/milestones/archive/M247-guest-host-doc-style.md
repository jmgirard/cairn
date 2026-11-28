# M247: In guest mode, text written for the host repo matches the host's own style

**Status:** done (2026-10-12, PR #257 https://github.com/jmgirard/cairn/pull/257)

**Goal:** In guest mode, the documentation, commit messages, PR text, and replies that a session writes for the host repo match the host's own length, tone, and level of technical detail, where no other writing-style instruction in the session settles them.

**Outcome:** tracking-rules "Collaboration mode" gained a bullet after the
no-cairn-vocabulary bullet: text for the host repo or its maintainers
matches the host's existing text of the same kind, read before writing. A
style the host states in writing comes first. The vocabulary bullet and the
derived-claims rule still bind. Another writing-style instruction in the
session wins, and Plain style and record-prose do not govern host text. The
guest line in `hooks/session_context.py` `build_context` carries a short
form, still one line, tested by
`test_guest_mode_line_carries_the_host_style_rule`. README and CHANGELOG
describe it. The rulebook-size baseline is re-seeded to 653 lines / 62,604
bytes at its three sites.

**Decisions:** D-161 (the rule and its precedence, annotates D-137 and
D-139); one milestone-local entry for the two review-added clauses.

**Review:** three lenses, 22 findings: 7 fixed (4 were one long CHANGELOG
line), 15 rejected, none to follow-ups. Copilot (Lite, earlier head): 3
items, all rejected. Nothing retired.
