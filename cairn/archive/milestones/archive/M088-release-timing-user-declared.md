# M88: Release timing is user-declared — a release milestone stops nominating itself — done 2026-07-19

**Goal:** Make release timing a maintainer declaration rather than a routable
milestone state, so a release milestone parks silently until its window opens.

**Outcome:** A release milestone was modelled as an ordinary milestone, so every
routing surface nominated it forever off `(status, priority, deps)` alone,
though its readiness is a maintainer judgment. `blocked` now covers an unopened release window (`planned → blocked` and
`review → blocked` legalized); `/milestone-plan` gained a release-shaped
tripwire defaulting to no (absent a declared window the work becomes a
`candidate` row); `cairn_validate` gained a `release window` advisory (WARN,
exit-code neutral); `/milestone` reports it and offers park-as-`blocked`.
Live fire: intraclass M48 WARNs, circumplex M7 silent while actively shipped.

**Key decisions:** D-050 — reuse `blocked` over a new status word or a
`Release-window:` slot; distinguished from D-035 (which rejected `blocked` as a
*candidate-list grouping label*), so no supersession owed. M88-D1 — the trigger
is status-dependent: a `planned` release warns once its deps are satisfied,
its work log recording queueing, never work (M48's was all `Depends-on` edits).

**Review:** 6/6 ACs fresh, AC1 by inversion. Lenses: diff-bug 6, blame-history
0, prior-PR no-op (zero inline comments across 90 merged PRs). Five fixed —
F6/91 (the version half matched any prose decimal, and the tooling fixtures had
only ever run against a stubbed goal), F4/85, F1/72, F2/66, F5/28 — F3/28
rejected with reason. PR #87.
