# M221: Plan and Implement clear the conversation first

**Status:** done (2026-10-06, PR #228 https://github.com/jmgirard/cairn/pull/228)

**Goal:** A press of the `Plan` or `Implement` Button, on the band or in the pane, runs `/clear` and then its command in the cleared conversation.

**Outcome:** `pressNext` in `register.tsx` holds the command in `heldRun`
for the actions in pane.ts's `CLEARS_FIRST`, when the drawn label is still
the next step's label, and runs `clear`. The `session.end` hook takes
`heldRun` first and runs it, unawaited, when the reason is `clear`. Any
other end drops it through `fallBack` (prompt box and toast), and a
refused clear drops it too. `busy()` blocks every action press while it
is held. A live probe (T1) found that a Button's `/clear` session end
arrives before its run resolves. README, DESIGN, CHANGELOG, and the
comments describe it. Mod tests went to 1291.

**Decisions:** none promoted. The plan gate chose clearing for Plan and
Implement only, the plain labels, and consent by press for the IP3 point.
T1 chose the held-command way over awaiting the clear. The operator's live
look in desktop sessions passed. The terminal had no live look.

**Review:** claim audit, 66 claims, 2 corrected. Three lenses, 38
findings: 16 fixed on the branch (drawn-label check, toast on a dropped
command, take before `next(e)`, rename, shared list, 4 tests, docs), 13 to
"Clear-then-run follow-ons (M221 review)", 9 rejected. Nothing retired.
