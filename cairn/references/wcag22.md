# wcag22 — the WCAG 2.2 text contrast ratio

**Provenance.** Ingested 2026-10-04 by M217 from https://www.w3.org/TR/WCAG22/,
the W3C Recommendation of 12 December 2024, downloaded with `curl` by the
implementing session and read at the anchors below.
Pagination: — (section anchors).
Extraction: verified 2026-10-04 against the source — observed 2026-10-04.

**Citation.** W3C (2024). Web Content Accessibility Guidelines (WCAG) 2.2.
W3C Recommendation, 12 December 2024. https://www.w3.org/TR/WCAG22/

**Role.** The contrast bar for the desktop track's pill text in the status
mod (M217 AC3): the formula the band tests compute and the 4.5:1 minimum
they assert.

## Extracted values

- Text contrast minimum: text has "a contrast ratio of at least 4.5:1", and large-scale text at least 3:1 — Success Criterion 1.4.3 Contrast (Minimum), Level AA, `#contrast-minimum`. Large-scale text is at least 18 point, or 14 point bold. The pill's 10.5 px text is not large-scale, so 4.5:1 applies.
- Contrast ratio: (L1 + 0.05) / (L2 + 0.05), L1 the relative luminance of the lighter color and L2 of the darker. Ratios range from 1:1 to 21:1 (Note 1) — glossary, `#dfn-contrast-ratio`.
- Relative luminance in sRGB: L = 0.2126 R + 0.7152 G + 0.0722 B, where each channel C = C8bit / 255 is linearized as C / 12.92 when C <= 0.04045, else ((C + 0.055) / 1.055) ^ 2.4 — glossary, `#dfn-relative-luminance`, Note 1. Note 2 says the threshold was 0.03928 before May 2021, with no practical effect.

## Traces to

- `hooks/status/band.test.tsx` — `luminance`, `contrast`, and the "the desktop pill text reads on its fill (M217 AC3)" tests: the formula, its 21:1 and 1:1 endpoints, and the 4.5 bound.
- `hooks/status/track.ts` — the palette comment's 4.5:1 claim for the pill label and count.

## Open questions

- None — observed 2026-10-04.
