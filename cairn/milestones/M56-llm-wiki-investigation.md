# M56: LLM Wiki investigation — references/ + linking fit assessment

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** —
- **Branch/PR:** m56-llm-wiki-investigation

## Goal

Assess Karpathy's LLM Wiki formalism (and its ecosystem) against cairn's
`references/` feature set, cross-file linking, and agent-memory model,
producing a reference note and a disposition ledger — investigation only, no
format changes.

## Scope

**In:** Primary-source deep read of the Karpathy LLM Wiki gist; a lighter
ecosystem scan (LangChain OpenWiki, nvk/llm-wiki, SamurAIGPT llm-wiki-agent,
DeepWiki/AutoWiki, community hardening patterns); one reference note
`cairn/references/llm-wiki.md` + `INDEX.md` line; a three-target fit
assessment (references/ formalism, cross-file linking, agent-memory angle);
a disposition ledger banking every adopt/adapt verdict. The M06/M42
comparandum pattern: read-only with respect to cairn's own formalism.

**Out:** Implementing any adopted convention (linking syntax, references/
lint, entity pages) → follow-up milestone(s)/candidates named by the
disposition ledger. Changes to `tracking-rules.md` or `cairn_validate` →
same. Fable escalation → offered only on a live RB-tripwire hit
(gate decision 2026-07-16: run on Opus, per the M06/M42 precedent).

## Acceptance criteria

- [ ] AC1: `cairn/references/llm-wiki.md` exists with full citation of the
      gist (primary source read directly, per the primary-sources rule), the
      formalism (three layers, page schema, ingest/query/lint operations,
      schema-file role), and ecosystem-scan findings, all with URL anchors.
- [ ] AC2: The note's fit assessment maps LLM Wiki elements to cairn's
      references/ feature set element-by-element (raw/↔pdf/, index, log,
      lint, linking, entity pages, ingest workflow), each element carrying an
      adopt / adapt / reject verdict with reason.
- [ ] AC3: The fit assessment covers cross-file linking: current de-facto
      link-token practice (M<NN>, D-<NNN>, IPn/GPn; `cairn_impact` whole-word
      tracing) surveyed by `git grep`, assessed against a wikilink-style
      convention + a dangling-link lint — verdict with rationale.
- [ ] AC4: The fit assessment covers the agent-memory angle: wiki-as-memory
      framing vs. cairn's session-context injection + stateless-resume
      doctrine — verdict with rationale.
- [ ] AC5: Disposition ledger complete — every adopt/adapt verdict lands as a
      ROADMAP candidate row (search-first sweep applied) or a named follow-up
      milestone proposal; every reject carries its reason in the note; no
      element left verdict-less.
- [ ] AC6: `cairn_validate` passes after the additions (note + INDEX line +
      candidate rows respect caps and date rules).

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T6
- AC6 → T6

## Tasks

- [x] T1: Deep-read the Karpathy gist (primary source); draft the formalism
      section of `references/llm-wiki.md` with verbatim-critical rules quoted.
- [ ] T2: Ecosystem scan — LangChain OpenWiki, nvk/llm-wiki, SamurAIGPT
      llm-wiki-agent, DeepWiki/AutoWiki (light), community hardening patterns
      (provenance headers, page-vs-edit heuristic); add the scan section.
- [ ] T3: Fit assessment, target 1 — references/ formalism: element-by-element
      map + verdicts against tracking-rules "Source ingestion".
- [ ] T4: Fit assessment, target 2 — cross-file linking: `git grep` the
      current link-token practice across `cairn/`; verdict on a linking
      convention + dangling-link lint (note `cairn_impact`'s existing tracing).
- [ ] T5: Fit assessment, target 3 — agent-memory angle vs. `session_context`
      hook + the stateless-resume doctrine; verdict.
- [ ] T6: Disposition ledger: bank candidates (search-first), add the
      `INDEX.md` line, run `cairn_validate`.

## Work log

- 2026-07-16: created by /milestone-plan (gate: investigation-only; gist +
  ecosystem scan; all three targets; Opus, not Fable — no RB tripwire fires).
- 2026-07-16: T1 done — gist read raw (primary source); formalism section of
  references/llm-wiki.md drafted with verbatim rules; gist states no date.

## Decisions

## Review
