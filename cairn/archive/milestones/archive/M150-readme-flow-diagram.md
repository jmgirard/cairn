# M150: The core loop becomes a rendered diagram

**Status:** done (2026-08-17, PR #151 https://github.com/jmgirard/cairn/pull/151)

**Goal:** README.md's "The core loop" ASCII block becomes a Mermaid flowchart
that GitHub renders, showing the three gates and the review→implement return
the one-line chain cannot.

**Outcome:** README.md:77-84 is a mermaid-fenced `flowchart LR` — idea →
`/milestone-plan (scope gate)` → `/milestone-implement (choices gate)` →
`/milestone-review (approval gate)` → merged, plus a `criteria unmet` edge back
from review to implement. Each gate sits inside its phase's node label as plain
quoted text; no `<br>`, image file, or build step. One CHANGELOG entry; the
other three README fenced blocks untouched.

**Decisions:** none.

**Review:** three lenses (user-facing tier). Blame-history and prior-review
record: nothing — no guard or decision pinned this block to ASCII. Diff-bug:
five, all fix-now before merge — gates on edges rather than their phases,
misplacing the choices gate against both the shipped skill and the README's own
worked example; two false CHANGELOG claims; a return label wider than the return
floor, which none of them tripped. A first repair used `<br>`, whose rendering
could not be observed, and became the in-label form. Graduated: the
README-flow-diagram row.
