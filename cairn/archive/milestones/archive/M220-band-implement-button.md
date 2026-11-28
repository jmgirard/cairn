# M220: An Implement button in place of the idle row's command

**Status:** done (2026-10-06, PR #227 https://github.com/jmgirard/cairn/pull/227)

**Goal:** The band's idle row starts its milestone from a button labeled `Implement`, and no longer draws the command `/milestone-implement <id>` as text.

**Outcome:** `idleLines` in `band.ts` returns an empty tail, so the idle
row's right side is the track alone, which a narrow row drops.
`NEXT_LABELS.implement` in `pane.ts` reads `Implement`, so the band's
`cairn-next` Button and the pane's Next Button both read it. The Buttons
keep their M212 rules, and when they hide the row draws no command. With
the command's columns free, the track stays down to 24 columns for a short
title. README, DESIGN, CHANGELOG, and the `register.tsx` comments describe
it. Mod tests went to 1246.

**Decisions:** none promoted. The plan gate chose one shared label map, and
the operator chose no fallback text when the Buttons hide. The operator
looked in openac (M21) and approved dropping the M217 and M218 done rows
for the ROADMAP's caps.

**Review:** three lenses, 21 findings: 6 fixed on the branch (CHANGELOG
width claim, DESIGN list and wrap, two `register.tsx` comments, a stale
ROADMAP clause), 4 to "Implement button follow-ons (M220 review)", 6
rejected, 5 noted. Claim audit: 28 claims, 3 corrected. Nothing retired.
