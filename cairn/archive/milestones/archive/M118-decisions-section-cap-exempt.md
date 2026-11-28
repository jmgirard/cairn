# M118: The milestone-local `## Decisions` section joins the cap-exempt set

**Status:** done (2026-07-27, PR #118 https://github.com/jmgirard/cairn/pull/118)

**Goal:** Exempt the append-only `## Decisions` section from the 150-line cap on
D-046's un-editability grounds, and wire the third member through every site.

**Outcome:** Both cap counters exempt it via a shared `EXEMPT_HEADINGS`, so the
count and its heaviest-first breakdown cannot disagree and `preamble + sections
== body` holds; one shared `_section_body_lines` scan now backs the work-log and
the new `milestone_decisions_lines` extractors. `CAP_EXEMPT_SECTIONS` gains it,
extending D-063's read-bound; `SECTION_MAX_CHARS` held at 6,000, comment
re-derived over three types. Ledger `references/m118-cap-exemption-ledger.md`:
119 milestones, all 3 over the cap fall to 123/123/125, largest remaining 129.

**Decisions:** D-076 (two grounds across three members, narrowing D-074 part 2's
"three distinct reasons"). Local: AC5 read as "no two-member set survives"; AC3's
"no prose here" scopes plan-owned prose, not the append-only work log.

**Review:** Three lenses, one finding — F1 (82), the rulebook's "two grounds"
diverging from live D-074, fixed as D-076; F2 (25) logged. Three §8 rounds
preceded it (16 -> 10 -> 2). M95/M105 anchor lessons consolidated; two captured.
