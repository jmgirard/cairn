# M293: The cairn pane's ⓘ card shows a candidate row's whole text

**Status:** done (2026-10-19, PR #306 https://github.com/jmgirard/cairn/pull/306)

**Goal:** On the desktop, the card that a candidate row's ⓘ opens in the cairn pane shows the row's whole ROADMAP text, not only its short title.

**Outcome:** `CandidateRow` in `hooks/status/reader.ts` gains `text`, the row's text after an exact `[high] `/`[low] `/`[parked] ` token as `candidateTexts` reads it (HTML comments removed), trimmed with `trim()` as the short title is. `paneLines` sets a candidate line's `full` to `row.text` and `info` when it is not empty, so an empty-title row also opens its card from ⓘ, while the line still draws the short title. The pane atom's shape tag moved to `pane-8`, and `types/index.d.ts` names `text`. `python_candidates` gives `text` with `JS_TRIM`. 60 expected candidate entries in 8 fixtures gained `text` through a checked scratch script, and `fixtures.gen.ts` was regenerated. README, DESIGN, the unreleased M290 CHANGELOG entry, and the pane.ts and register.tsx comments say what the card holds. Mod tests went from 2332 to 2336.

**Decisions:** none promoted. Question set: the whole row after its token (over the row cut before ` — added`), and a live look in circumplex. The live look found the text right and a tall card cut at the pane's top.

**Review:** Criteria audit at plan (full), 7 findings, all taken toward the narrower promise. Claim audit: 25 claims, 3 corrected. Four lenses and Copilot (Lite, one thread; summary reply posted), 24 items: 13 fixed (30 test literals without `text`, a misplaced M291 comment, split comment sentences and long lines, DESIGN's `candidateRows` sentence, the M258 test's priority check), 11 rejected (a dead started token in a card as the planned whole row, spacing left by a removed comment, a render-level ⓘ test for empty titles, D-189's premise, and others). Hygiene: "Fix cut and odd names on the pane card" unparked, its item (3) the cut card seen at the live look. LESSONS M272 line extended.
