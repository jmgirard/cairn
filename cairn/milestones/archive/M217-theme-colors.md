# M217: Band and pane colors that follow the theme

**Status:** done (2026-10-04, PR #224 https://github.com/jmgirard/cairn/pull/224)

**Goal:** The status band and the cairn pane take their colors from the Claude Code theme wherever the surface can read it.

**Outcome:** `FLOW_COLORS` in `band.ts` is now the theme keys `planMode`,
`claude`, and `success`, and `PILL_TEXT` is `inverseText`. The terminal
track, the pane's marks, meters, and Next pill, and the candidate `↑` draw
them. `track.ts` holds the mod's only raw colors between `// palette`
comments: the desktop SVG's grays and darker phase fills (rgb(71,103,158),
rgb(152,85,57), rgb(68,113,81)), with the count's fill-opacity at 0.85. A
band test computes the WCAG 2.2 ratio from the built SVG per phase (label
and count at least 4.5:1). New source note `references/wcag22.md`, pinned
in the page-state ledger. Docs updated. Mod tests 1133 to 1137.

**Decisions:** none promoted. The plan chose `planMode` over the blue keys
and one desktop palette over one per theme (no theme signal reaches an
image). The operator accepted the colors at a live look.

**Review:** three-lens fan-out, 17 findings: 5 fixed on the branch
(contrast-test opacity guards, an unused export, README wording, wraps), 2
to "Theme color follow-ons (M217 review)", 10 rejected. Claim audit: 40
claims, 2 corrected. Four promoted candidate rows trimmed to their
remainders. Nothing retired.
