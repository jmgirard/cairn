# M216: A Clear button when a cairn skill ends

**Status:** done (2026-10-04, PR #223 https://github.com/jmgirard/cairn/pull/223)

**Goal:** When a cairn skill finishes and the session is idle, the status band shows a `Clear` button that runs `/clear`.

**Outcome:** `register.tsx` gains the `ended` atom (`ended-1`, declared in
`types/index.d.ts`). A Stop that ends a known cairn step sets it. An idle
typed prompt that enters, a cairn skill's prompt, and `session.end` clear
it. While it is true, a row with the next-step and `Status` Buttons draws
`cairn-clear` before them, and drops it first when narrow (it takes 10
columns). `pressClear` re-reads the step and `ended`, then runs `clear`
through `run`. `session.end` frees `running`, and a run number stops a late
run from freeing a newer one. README, DESIGN, and CHANGELOG describe it.
Mod tests went from 1105 to 1133.

**Decisions:** none promoted. The question set chose showing after a
skill ends, a clear at once, and a live look. In the live look, a press
cleared the conversation.

**Review:** three-lens fan-out, 25 findings: 8 fixed on the branch, 8 to
"Clear button follow-ons (M216 review)", 5 rejected, 4 noted. Claim
audit: 40 claims, 9 corrected. Nothing retired.
