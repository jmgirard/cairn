# M219: Status and Clear buttons in the cairn pane

**Status:** done (2026-10-05, PR #226 https://github.com/jmgirard/cairn/pull/226)

**Goal:** The cairn pane carries the band's Status and Clear buttons on a row of their own under the Next line (placement superseded at the live look: on the Next line).

**Outcome:** `paneLines` gives the Next line `buttons`, `status` with
`clear` before it while `ended` is true, set only with the next-step label
and while no step is set. `register.tsx` draws `cairn-pane-clear` and
`cairn-pane-status` after `next-action`, each `secondary` in a Box
`next-clear` or `next-status` with `flexShrink` 0, pressing the band's
`pressClear` and `pressStatus`. `STATUS_LABEL` and `CLEAR_LABEL` moved to
`pane.ts`. Mod tests went to 1244. README, DESIGN, and CHANGELOG describe it.

**Decisions:** none promoted. The operator moved the buttons from a row of
their own onto the Next line at the first live look. A probe showed that a
desktop click on a pane without keyboard focus only focuses it, with no
`ui.press`. AC5 counts presses that reach the mod, and the click went to
"Mod pane placement (upstream)". Refocusing after a press was declined.

**Review:** three lenses, 24 findings, by part: 10 fixed on the branch
(buttons only with a label, docs wording, a pane-wide Button check), 10 to
"Pane Status and Clear follow-ons (M219 review)", 7 rejected, 4 noted.
Claim audit: 30 claims, 6 corrected. Nothing retired.
