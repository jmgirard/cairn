# M117: Detector coverage on the site axis, and a plan gate that records the alternative it rejected

**Status:** done (2026-07-27, PR #117 https://github.com/jmgirard/cairn/pull/117)

**Goal:** Close the two doctrine gaps intraclass M93's four-pass
evidence-quality return loop exposed in cairn's own rules.

**Outcome:** `guard-doctrine.md` §3 gains the SITE axis of a detector's
renderings — branches, message literals, code paths — beside the numeric-format
axis it already prescribed for; plus "a count of enumerated entries is not
coverage of renderings" (the `checked == N` shape over a hand-listed set), with
the producer-sweep remedy that enumerates nothing. `/milestone-plan` step 4
obliges one work-log line per approach choice weighed — what lost, why, and the
falsifying evidence class — none where none was weighed, so absence is
meaningful and `/milestone-review` trigger (b) reads it there.

**Decisions:** none promoted. Two gated Scope amendments (a predicted re-wrap
that never happened; a false locator count), both user-approved.

**Review:** One pass; 12 asserts, 11 registry entries, 3 containment asserts on
§2's by-hand check. Blame-history 0, prior-PR-comments 1, diff-bug 3+2.
Actioned F6 (92), F4 (90), and by override F1 (70) — on this milestone's own
work log demonstrating the under-fire — and F2 (60). Four §8 rounds preceded
review: 8 → 6 → 6 → 2. Hygiene: retired M103's lesson (label-to-set anchor
false coverage) under ownership — `guard-doctrine.md` §1 states it in full.
