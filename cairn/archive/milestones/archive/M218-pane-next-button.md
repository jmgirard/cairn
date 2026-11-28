# M218: A Next button in the cairn pane

**Status:** done (2026-10-04, PR #225 https://github.com/jmgirard/cairn/pull/225)

**Goal:** The cairn pane's Next line carries a button that runs the next command, as the band's next-step button does.

**Outcome:** The pane's Next line keeps its colored pill and gains a
`secondary` Button, key `cairn-pane-next`, in a `next-action` Box with
`flexShrink` 0 and `marginLeft` 1 after the pill. Its label is the band's
(`Start`, `Resume`, `Review`, `Plan`), and its press is the band's
`pressNext`. `NEXT_LABELS` and `PLAN_LABEL` moved to `pane.ts`, read through
`nextLabel`, which takes own keys only. `paneLines` takes an `acts` flag,
true while `knownStep` reads no step. A pane gets no `isWorking` prop, so
the Button also shows in a turn outside a cairn skill, and
`$.command.run` queues such a press. Mod tests went to 1194. README,
DESIGN, and CHANGELOG describe it.

**Decisions:** none promoted. The pill stays, as a Button takes no fill
color. The operator accepted the look at a live look in bsync.

**Review:** three lenses, 19 findings. 4 were fixed on the branch: an
own-key label read, a press after the held run's release, the field
comment, and the docs wording. 10 went to "Pane button follow-ons (M218
review)" or rows that already held them. 2 were rejected and 3 noted.
Claim audit: 30 claims, 1 corrected. Nothing retired.
