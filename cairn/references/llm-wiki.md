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

## Ecosystem scan (what survived contact with real use)

Surveyed 2026-07-16, lighter touch than the gist:

- **langchain-ai/openwiki** (https://github.com/langchain-ai/openwiki,
  shipped 2026-07-01) — the repo-documentation specialization: a CLI that
  generates an `openwiki/` wiki for a codebase, refreshes it via `--update`
  (CI templates open PRs with doc updates), and wires agents to it by
  maintaining a fenced `<!-- OPENWIKI:START -->…<!-- OPENWIKI:END -->` block
  in CLAUDE.md/AGENTS.md, "leav[ing] the rest of your content untouched."
  Notable parallels to cairn: owned-section discipline inside CLAUDE.md, and
  a human-authored brief (`INSTRUCTIONS.md`) separate from generated pages.
- **nvk/llm-wiki** (https://github.com/nvk/llm-wiki) — the most hardened
  community build. Adds: a **dual-link format** (`[[slug|Label]]` +
  a plain relative-path markdown link) so links resolve in Obsidian *and*
  plain viewers; `/wiki:lint` mechanized (broken links, orphan articles,
  registry drift; `--fix`); a trust `/wiki:audit` with evidence-chain
  tracing; per-article confidence ratings from source quality; and a
  **human-owned advisory `schema.md`** with "proposal-only" convention
  updates — the agent proposes, the human owns the schema.
- **SamurAIGPT/llm-wiki-agent** (https://github.com/SamurAIGPT/llm-wiki-agent)
  — canonical `[[wikilinks]]` throughout; typed YAML frontmatter
  (`type: source`, tags); auto entity/concept pages; a two-pass graph builder
  (explicit wikilinks = deterministic edges, then inferred edges tagged with
  confidence); contradictions flagged at *ingest* time; query answers filed
  back only on user choice.
- **DeepWiki (Cognition) / AutoWiki (Factory)** — hosted auto-generated
  wikis for GitHub repos; credited by OpenWiki as inspiration. Fully
  generated from code, no curation loop — the opposite pole from cairn's
  human-gated model; noted for positioning only.

**Convergent hardening across implementations:** (1) wikilinks became the
de-facto link syntax, with nvk's dual-link form solving plain-markdown
rendering; (2) lint got *mechanized* everywhere (broken links, orphans,
index drift) rather than staying an LLM judgment pass; (3) append-only
`log.md` is universal; (4) the schema/conventions file trends
**human-owned** with agent-proposed amendments — the ecosystem
independently arrived at cairn-style governance.

## Fit assessment 1: the references/ feature set

Element-by-element, LLM Wiki → cairn's `references/` (tracking-rules
"Source ingestion"), with verdicts:

| LLM Wiki element | cairn today | Verdict |
|---|---|---|
| `raw/` immutable, committed | `references/pdf/`, immutable but **gitignored** | **Adapt (keep cairn's)** — immutability already holds; gitignoring is a copyright necessity for published PDFs. Reject committing raw sources. |
| Per-source summary pages | `<citekey>.md` with page/table anchors | **Already have** — cairn's version is stronger (verbatim-critical values quoted, tests/oracles trace to it). |
| `index.md` catalog, updated per ingest | `INDEX.md`, one line per note | **Already have** — same shape. |
| Entity/concept pages (cross-source synthesis) | Not in the stated formalism — but practice already outgrew it: `competitive-landscape.md` (M06 synthesis), `migration-pilot-notes.md` (cross-pilot ledger) are concept pages living in `references/` unnamed | **Adopt (name it)** — legitimize the existing second page type: source notes (`<citekey>.md`) + synthesis notes. A one-line widening of the file-map entry, not new machinery. |
| `log.md` append-only op record | None; ingestion recorded in milestone work-logs + git | **Reject** — duplicates state the boundary rule already places ("History → archive + git log"); a second log is a divergence vector. |
| **Ingest** op | The Source-ingestion recipe (pdf → summary → INDEX line) | **Already have** — leaner, equivalent. |
| **Query** op (+ answers filed back) | No formal op; but "answers filed back as pages" is already practice (M42's and this note's fit assessments *are* filed-back query answers) | **Reject formalizing**; the filed-back norm already operates. |
| **Lint** op | **Nothing** — `cairn_validate` has zero `references/` checks (no INDEX↔disk orphan check; the roadmap↔disk orphan check has no references sibling) | **Adopt** — the one genuine gap. A mechanized INDEX↔disk check fits the existing validate architecture. |
| Schema file (human-owned, co-evolved) | `tracking-rules.md` — plugin-shipped, guard-tested, amended via D-entries | **Already have, stronger** — cairn ships the schema as a versioned artifact with mutation-tested guards; the ecosystem's "human-owned, proposal-only amendments" is cairn's model re-derived. |

**Headline:** cairn's `references/` is already a small LLM Wiki; the real
deltas are just two — *name the synthesis page type* and *add a references
lint*. The formalism validates the design rather than replacing it.

## Fit assessment 2: cross-file linking

Current practice (grep survey, 2026-07-16): the implicit link graph is
dense — **480 `M<NN>` tokens, 249 `D-<NNN>` tokens, 96 `IPn`/`GPn` tokens**
across `cairn/`. These bare tokens are true stable identifiers (append-only,
never renumbered, never reused — stronger link targets than file paths), and
`cairn_impact` already resolves principle tokens whole-word to citing
file:line. Dangling-ref audit: zero true dangling IDs today; the two
non-existent-here IDs found are `M57` (qualified cross-repo cite, "ackwards
M57") and `M99` (example prose about ID growth in the M10 archive) — both
false-positive hazards a naive checker must tolerate.

- **`[[wikilink]]` syntax: Reject.** Bare ID tokens already resolve
  unambiguously; wikilinks would break plain-markdown/GitHub rendering (nvk
  needed a dual-link workaround for a problem bare tokens don't have), and
  retrofitting ~800 existing tokens would rewrite append-only history.
  cairn's link syntax *is* the ID vocabulary.
- **Dangling-reference lint: Adopt, as an advisory.** A `cairn_validate`
  ADVISORY (WARN tier, M44) scanning `cairn/` for `M<NN>`/`D-<NNN>` tokens
  that resolve to no ROADMAP row, archive file, or D-entry — tolerating
  repo-qualified refs and example prose per the two hazards above (the
  D-023 "missed weird format beats a false positive" doctrine). Sibling of
  the existing roadmap↔disk orphan check and `cairn_impact` tracing.
- **Graph/hub tooling: Reject.** On-demand `grep` answers "what cites
  D-024" already; a graph artifact is state that rots.

## Fit assessment 3: the agent-memory angle

The ecosystem frames a maintained wiki as agent memory (semantic = durable
facts, entity = pages, episodic = logs). Mapping cairn onto it: **cairn is
already a governed LLM Wiki specialized to project state** — schema =
`tracking-rules.md` (plugin-shipped), wiki = the `cairn/` file map with
ownership boundaries, raw = the repo + git history, ingest = the phase
skills, lint = `cairn_validate` + the `/milestone` audit, query =
`/milestone` + `cairn_status`/`cairn_next`, log = work-logs + DECISIONS.
Session memory = the `session_context` hook injecting ROADMAP + active
milestone at session start; stateless resume is the discipline that makes
the wiki, not the transcript, the memory.

- **Structural steals: Reject.** Free-form agent-created pages are the
  *opposite* of cairn's differentiator — governed state (fixed file map,
  sole status authority, caps, gates; M06 positioning). Where LLM Wiki lets
  the agent own the wiki layer entirely, cairn deliberately gates every
  transition; that difference is the product.
- **Positioning framing: Adopt.** "A governed LLM Wiki for project state —
  the agent maintains it, the human gates it" is a stronger one-line
  explanation of cairn than any current README phrasing, and the pattern's
  name now carries recognition (Karpathy, LangChain). Feed into the
  public-release-prep README work; independent convergence on human-owned
  schemas + mechanized lint (ecosystem scan above) is third-party
  validation of the design bet.
