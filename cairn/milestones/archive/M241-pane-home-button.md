# M241: A ⌂ Button in the cairn pane clears the conversation and brings the pane to the front

**Status:** done (2026-10-10, PR #251 https://github.com/jmgirard/cairn/pull/251)

**Goal:** The cairn pane's first line carries a ⌂ Button that clears the conversation and opens the pane, which brings a hidden pane forward.

**Outcome:** `paneLines` gives the first line `['home', 'refresh']` while
`acts` is true. register.tsx draws `cairn-pane-home`, labeled `HOME_LABEL`
⌂, in a `-home` Box before ↻. `pressHome` sets the module mark `homeRun`
before its first await, takes it back on a set step, and runs `clear`.
`busy` reads the mark. `session.end` takes the mark and, at reason `clear`,
calls `openHome`, which opens the pane and toasts a refusal. The Next
line's `clear` and the `ended` parameter of `paneLines` are gone. The band
keeps its Clear. README, DESIGN, and CHANGELOG describe it. Mod tests 1627.

**Decisions:** none promoted. The question set chose clear and open over a
pane reset, removed the pane's Clear, hid ⌂ in a run, and granted a look. AC2 was
amended to drop the set-step press, which no test can reach. The operator
accepted the live look. Nobody saw whether a pane behind another tab comes
forward, which the title and Goal promise.

**Review:** claim audit, 55 claims, 3 corrected. Three lenses and Copilot
(Lite), 24 items: 8 fixed (a same-tick double press, the stuck-mark Known
issue, README wording, two tests, stale text), 9 to "⌂ edges (M241
review)", 5 rejected, 2 noted. Nothing retired.
