# M119: RR08's follow-ons — the decisions-format advisory, the history enumeration, and a two-sided exempt-set guard

**Status:** done (2026-07-27, PR #119 https://github.com/jmgirard/cairn/pull/119)

**Goal:** Ship RR08's three remaining binding criteria: a counterweight advisory
for the now-unbudgeted `## Decisions` section, the rulebook's history-member
enumeration, and a hook/counter exempt-set consistency test.

**Outcome:** `check_decisions_format` ships in `ADVISORIES` as `decisions
format` — WARN, exit-neutral — reading the section through M118's shared
extractor and keying on ten shape signatures (`_DECISIONS_PASTED`) plus fenced
blocks, one finding per paste, blockquote markers stripped before matching.
`tracking-rules.md`'s "Correcting a record proven false" bullet names the
section as a history member. `CAP_EXEMPT_SECTIONS` is derived in
`cairn_scripts` from `EXEMPT_HEADINGS + (REVIEW_HEADING,)` and mirrored in
`hooks/session_context.py`, held equal by `TestExemptSetMirror`.

**Decisions:** D-077 — D-075's "WARN on every entry" narrowed to 23 of 24.

**Review:** 3 lenses + scorer; blame-history and prior-review each 0 findings.
F1/85 and F2/74 fixed at review — two signatures claimed ordinary prose, and
HTML comments went unskipped where the sibling advisory skips them. F4/80 and
F3/55 logged under a user override on description-layer findings; F4 banked as
a candidate row. BC3 met exactly: 0 WARNs projected and measured, ≥1 projected
and 1 measured on each fixture shape.
