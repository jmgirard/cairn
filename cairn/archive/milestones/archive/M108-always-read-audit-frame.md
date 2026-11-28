# M108: Always-read audit frame

**Status:** done (2026-07-23, PR #106 https://github.com/jmgirard/cairn/pull/106)

**Goal:** Add the always-read audit frame — a rulebook doctrine paragraph
naming the three governance elements every always-read file must have (inflow
test, outflow/read-bound, attention signal) plus a `/milestone` audit bullet
flagging any file missing one.

**Outcome:** New `## Always-read governance` section in `tracking-rules.md`:
every always-read file names three elements, D-045's split decides legal
outflows, and a four-file worked table (ROADMAP/LESSONS/tracking-rules/
DECISIONS) fills them in. `/milestone` §2 audit gains a judgment bullet — flags
a missing element or new always-read surface, reports and never `FAIL`s.
Completeness-only: no mass measure, no `cairn_validate` check (D-057 stays
closed). Guard: `test_always_read_frame.py` + 10 mutation registrations.

**Decisions:** D-060 (the frame; annotates D-045, cites D-053/D-056/D-057) —
authored at plan.

**Review:** Three fresh-context lenses (diff-bug/blame/prior-review) — zero
actionable findings; scorer no-op; one observation dropped (loose
"~30-milestone" phrasing, verbatim from IP4-frozen D-060). Graduated the
"Always-read audit frame" candidate row; no lessons captured or retired.
