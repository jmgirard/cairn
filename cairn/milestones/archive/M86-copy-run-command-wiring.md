# M86: Copy-run command wiring — the handoff rule reaches the steps that hand over

- **Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/85 · **Merged:** 2026-07-18

## Goal
Make every step handing the user a command emit it as a copyable fenced block,
and sharpen the rule so handoff/naming/chip-arrow stop blurring.

## Outcome
The M35 copy-run rule was central-only and drifted: `/milestone-review` step 10
instructed the violation outright ("naming the obvious next action inline"),
`/milestone-brief`'s manual-run prompt sat in a blockquote (no copy button),
`/cairn-release`'s had no format directive. The rule is now three labelled
cases (handoff → fenced; naming → inline backticks; chip arrow → neither,
D-022), names slash commands, and separates a handoff from a mention. Wired
into those three steps; new `test_copy_run_handoffs.py` + 3 mutation entries.
D-048 records the text, the three-skill scope (not all nine), and
`/milestone-implement`'s `/clear` staying a *mention*.

## Review
3 lenses + scorer; blame and prior-PR 0 findings, diff-bug 5. F1/85, F2/88,
F3/88 were all the M74/M76 label-swap defect — in the milestone whose own AC5
demands it — fixed and proven by inverting each rule until the suite went red
(the harness blanks, it cannot swap). F4/62, F5/25 logged and fixed anyway.
skills 385, scripts 174, hooks 72, validate 21/21, all exit 0.
