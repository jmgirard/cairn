# M213: A Plan button on the empty band

**Status:** done (2026-10-04, PR #220 https://github.com/jmgirard/cairn/pull/220)

**Goal:** When a cairn repo has no milestone to work on, the status band shows a row with a button that starts planning.

**Outcome:** `band.ts` gains `emptyLines` (key `plan-row`, no id, the gray
text `No milestone ready`, no track), a `found` argument to `stepLines`,
and the empty row in `actionsFit`. `register.tsx` draws it when the pane
state's `found` is true and nothing is active or workable, with no head
Box. `NEXT_LABELS` maps the planning step to `Plan`, which runs
`cairn:milestone-plan` with empty args beside M212's `Status`. The Buttons
fit from 37 columns. A `Start`, `Resume`, or `Review` press still does
nothing when the re-read step names no milestone. The close mark needed no
change. README, DESIGN, and CHANGELOG describe the row.

**Decisions:** none promoted. The operator did the live look in a new
session in bsync, a real repo with nothing workable, after a scratch
folder proved annoying to open.

**Review:** three-lens fan-out, 21 findings: 5 fixed on the branch (the
stale-press guard, two close-state cases, the changelog width), 5
rejected, 11 to "Empty band row follow-ons (M213 review)". Claim audit:
34 claims, 5 corrected. Nothing retired.
