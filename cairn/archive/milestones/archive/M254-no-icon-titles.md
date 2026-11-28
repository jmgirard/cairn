# M254: Candidate short titles hold no icons

**Status:** done (2026-10-15, PR #265 https://github.com/jmgirard/cairn/pull/265)

**Goal:** A candidate row's short title names things in words and holds no icon, so the cairn pane's own marks and Buttons beside the title are never confused with title text.

**Outcome:** tracking-rules "Candidate short title" tells writers to name things in words and put no icon in a short title, an icon being a non-ASCII character of Unicode category `So` or `Sm`, between backticks or not, because the pane draws its marks and Buttons with such glyphs. `/cairn-triage`'s `retitle` gains an icon trigger that wins over the other triggers: a title ending at `: ` is replaced in place, and any other icon row takes the new title and `: ` before its text, which stays with each icon removed. The table row, the Title class, and step 4 Apply say so. This repo's rows "⌂ edges (M241 review)" and "✎ edges (M242 review)" became "Home Button edges (M241 review)" and "Plan Button edges (M242 review)", with their two quoted mentions rewritten. README and CHANGELOG describe the rule. The rulebook baseline is 668 lines / 64,222 bytes.

**Decisions:** D-164 (extends D-163; passes D-108's door on a shipped-behavior trigger). The plan gate chose non-ASCII `So`/`Sm` over `So` alone, and rulebook plus triage over a validate advisory. AC3 was amended once (line numbers). AC2 was amended twice, the second time at a user stop: in-place replacement only for titles ending at `: `, because a title cut at ` — ` holds the row's description and trigger.

**Review:** Two passes of the three-lens fan-out gave 48 findings: 29 fixed, 8 sent to "Retitle edges (M251 review)", 7 rejected, 3 noted, 1 routed to the AC2 amendment. Copilot (Lite) raised 2 threads, both fixed and resolved. The claim audit corrected 1 of 17 claims. No lesson captured: LESSONS.md is at its byte budget. M251 and M254 each took a return for a `retitle` edit that deleted a dash-cut row's description.
