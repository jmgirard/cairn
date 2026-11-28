# M242: A ✎ Button on each candidate row in the cairn pane plans that candidate

**Status:** done (2026-10-11, PR #252 https://github.com/jmgirard/cairn/pull/252)

**Goal:** Each candidate row in the cairn pane carries a ✎ Button whose press starts `/milestone-plan` with the row's short title.

**Outcome:** `paneLines` sets `grow` on every candidate line and, while
`acts` is true, gives each line with a non-empty short title the `plan`
Button, its `target` the index and its new `title` field the short title.
register.tsx draws it as `cairn-pane-plan-<index>`, labeled
`PLAN_CANDIDATE_LABEL` ✎. `pressCandidate` sets a `candidateCheck` mark,
which `busy()` reads, before its first await. It returns on a set step,
on stored state that draws no candidates, or on a stored row at that index
that is missing or has another title. Else it holds `cairn:milestone-plan`
with the title in `heldRun` and runs `clear`, and `session.end` runs it.
README, DESIGN, and CHANGELOG describe it. Mod tests 1644.

**Decisions:** none promoted. The question set chose clear first, the ✎
label, and a live look in circumplex, which the operator accepted. The plan
chose the short title over the full row text as the args.

**Review:** claim audit, 46 claims, 4 corrected. Three lenses and Copilot
(Lite), 34 items: 20 fixed (the hold set after the checks, a check that
candidates still draw, 6 tests, docs), 6 to "✎ edges (M242 review)", 7
rejected, 1 noted. Nothing retired.
