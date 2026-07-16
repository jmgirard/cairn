# LLM Wiki (Karpathy) — formalism + cairn fit assessment (M56)

**Citation:** Karpathy, A. *LLM Wiki*. GitHub gist
`karpathy/442a6bf555914893e9891c11519de94f`
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), no date
stated in the document; read directly (raw text) 2026-07-16. A pattern
document, not a product — secondary ecosystem surveyed separately below.

## The formalism

Core move: instead of RAG-style re-retrieval ("the LLM is rediscovering
knowledge from scratch on every question. There's no accumulation"), the
agent incrementally builds and maintains a persistent markdown wiki — "the
wiki is a persistent, compounding artifact. The cross-references are already
there. The contradictions have already been flagged."

**Three layers:**

1. **Raw sources** — "your curated collection of source documents … These are
   immutable — the LLM reads from them but never modifies them."
2. **Wiki** — "a directory of LLM-generated markdown files. Summaries, entity
   pages, concept pages, comparisons, an overview, a synthesis." "The LLM owns
   this layer entirely. It creates pages, updates them when new sources
   arrive, maintains cross-references, and keeps everything consistent." Two
   special pages: `index.md`, "a catalog of everything in the wiki — each
   page listed with a link, a one-line summary, and optionally metadata …
   organized by category," updated "on every ingest"; and `log.md`, "an
   append-only record of what happened and when — ingests, queries, lint
   passes."
3. **Schema** — a CLAUDE.md/AGENTS.md "that tells the LLM how the wiki is
   structured, what the conventions are, and what workflows to follow." It
   co-evolves with the user; it is what makes the agent a disciplined
   maintainer rather than a generic chatbot.

**Three operations:**

- **Ingest** — drop a source into raw; the LLM "reads the source, discusses
  key takeaways with you, writes a summary page in the wiki, updates the
  index, updates relevant entity and concept pages across the wiki, and
  appends an entry to the log." One source may touch 10–15 pages.
- **Query** — "the LLM searches for relevant pages, reads them, and
  synthesizes an answer with citations"; outputs vary (page, table, deck,
  chart). Key rule: "good answers can be filed back into the wiki as new
  pages … these are valuable and shouldn't disappear into chat history."
- **Lint** — periodic health check: "contradictions between pages, stale
  claims that newer sources have superseded, orphan pages with no inbound
  links, important concepts mentioned but lacking their own page, missing
  cross-references, data gaps that could be filled with a web search."

**Deliberately unspecified:** no mandated link syntax (Obsidian
`[[wikilinks]]`/graph view are suggested tooling, not rules), no citation
format, no page frontmatter schema, no new-page-vs-edit rule — the schema
file is where each deployment pins those down. Division of labor: "The
human's job is to curate sources, direct the analysis, ask good questions,
and think about what it all means. The LLM's job is everything else."

**Rationale worth quoting:** "Humans abandon wikis because the maintenance
burden grows faster than the value. LLMs don't get bored, don't forget to
update a cross-reference, and can touch 15 files in one pass. The wiki stays
maintained because the cost of maintenance is near zero."
