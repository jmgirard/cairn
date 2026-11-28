# M290: The desktop cairn pane shows a candidate row's ✎ only under the pointer

**Status:** done (2026-10-19, PR #302 https://github.com/jmgirard/cairn/pull/302)

**Goal:** On the desktop, the cairn pane draws a candidate row's ✎ only while the pointer is over that row, and the terminal draws ✎ where it does today.

**Outcome:** Off the terminal, a candidate line's ✎ Box in `register.tsx` has no key and is placed `position: 'absolute'`, `top 0`, `bottom 0`, `right: PLAN_PARK` (-8), past the edge the pane clips, with `hover: { right: 0 }` and `alignItems: 'center'`. A candidate line with a `full` sets the new `info` field (`pane.ts`). Before ✎ it draws a hidden unkeyed Box that the line reveals, with a `PLAN_SLOT` (4) right margin when ✎ is there. That Box holds a gray `Text` `INFO_LABEL` ⓘ with `hover: { scope: infoScope(line.key), bold: true }`, and the line's card names the same scope, so only ⓘ opens it. Other lines' cards are unchanged, and so is the terminal. The design came from five live looks in circumplex and two probes. A hidden ✎ took no click, and a `Box` naming a hover group never lit it. Tests: a `holderOf` and `isCard` helper, the M242 AC4 keyed-Box check limited to the terminal, and M290 tests for both surfaces, presses, other Buttons, ⓘ and its scope, and ⓘ alone while a skill runs. Mod tests went from 2286 to 2304. README, DESIGN, CHANGELOG, and the code comments describe it, and DESIGN drops M286's "engine refuses a hover scope drawn hidden".

**Decisions:** none promoted. The operator chose in-row placement, pointer-only reach on the desktop, the info icon on candidate rows only, and a probe over dropping the card. Three substantive amendments followed the live looks.

**Review:** Claim audits, 19 claims (2 corrected) and 55 (0). Four lenses and Copilot (Lite, no threads), 34 items: 13 fixed, 14 rejected, 2 to items (4) and (5) of "Gaps only the app or mod API can close" (the hand cursor, and the card closing when the pointer moves onto it), 5 noted. LESSONS: the M201 live-look lesson gained the two desktop facts. Nothing retired or unparked.
