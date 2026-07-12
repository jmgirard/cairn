# Claude Desktop / Claude Code TOC mechanism (M27 characterization)

**Date:** 2026-07-12 · **Method:** live probing in Jeff's Claude Desktop,
viewing a Claude Code (cairn) session — the surface where cairn skills run.

## What was tested

Emitted markdown headers into the session and observed the navigable table
of contents (outline), varying:

- **Level** — `#` (H1), `##` (H2), `###` (H3), in one message and then a
  second longer message.
- **Format at H2** — bare phase word (`## Plan`) vs the unit form
  (`## Milestone 27: …`).
- **Placement** — headers positioned mid-message (after leading prose),
  end-of-message, and spread across two separate messages.
- **Verbatim vs. paraphrase** — headers with unguessable nonsense strings
  (`## Sazerac Grommet 4471`) plus a header-free paragraph on an absurdly
  specific topic, to distinguish a markdown-header parser from an LLM
  summarizer.
- **Chapter marker** — a single `mcp__ccd_session__mark_chapter` call.

## Observations

1. **Markdown headers → no TOC.** Two messages containing H1, H2, and H3
   headers (incl. a real `# PROBE-A1`) produced **zero** TOC entries. The
   headers rendered as visual headings in the transcript (confirmed by
   screenshot) but populated no outline.
2. **Chapter marker → TOC.** One `mark_chapter` call produced a two-entry
   outline: "Session Start" (implicit) + "M27 chapter-TOC probe" (the marker).
3. All three variants held the same result: no level (H1/H2/H3), no format
   (`## Plan` vs `## Milestone 27`), and no placement (mid-message,
   end-of-message, across two messages) produced any TOC entry. The result
   is invariant to all three, so the verbatim-vs-summarizer question is moot
   for this surface — nothing indexed to compare.

## Conclusion

In a **Claude Code session** (cairn's runtime, even when viewed inside
Claude Desktop) the navigable TOC is built from **chapter markers**, not
markdown `#`/`##` headers. D-012's "both H1/H2 land in Claude Desktop's TOC"
does not hold where cairn operates; whether it holds on any other Claude
surface (a regular Desktop / claude.ai chat) was **not tested** here and stays
unverified. The phase-header level convention (H1
unit / H2 phase) is retained for in-transcript visual hierarchy, not TOC
indexing; the chapter-marker discipline is the actual outline driver.

Recorded as D-020, which annotates D-012. Supports M27 AC1 (this note) and
AC2 (D-020).
