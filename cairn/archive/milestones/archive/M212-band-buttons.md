# M212: Buttons on the status band

**Status:** done (2026-10-04, PR #219 https://github.com/jmgirard/cairn/pull/219)

**Goal:** The status band shows a button for each cairn command that fits the moment, and a press runs that command.

**Outcome:** The band's first row gains `cairn-next` and `cairn-status`,
both `variant="secondary"`, before the open and close buttons. The first
reads `Resume`, `Review`, or `Start` and runs `cairn:` plus `recommend`'s
command with its id. The second runs `cairn:milestone`. They show while no
cairn skill's step is set and `isWorking` is false. `register.tsx` lays the
row out with their columns reserved (label + 5 each), so the track gives
way down to 12 columns. `band.ts` `actionsFit` keeps them only where the row
has its track or long warning label and the title keeps its room. A press
re-reads the step and the next step, skips while a run is in flight, and
calls `$.command.run`. A rejection appends the command line to the prompt
box and toasts the reason and the line.

**Decisions:** none promoted. Live looks moved the Buttons from `plain`
(read as text) through `primary` (clashed) to `secondary` with a space, and
made the track give way (at a full-width track they vanished near 95).

**Review:** three-lens fan-out, 26 findings: 10 fixed on the branch, 14 to
"Band button follow-ons (M212 review)", 2 rejected (1 planned change, 1
false). Claim audit: 44 claims, 3 corrected. Nothing retired.
