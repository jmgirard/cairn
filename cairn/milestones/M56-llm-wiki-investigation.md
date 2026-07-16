# M56: LLM Wiki investigation — references/ + linking fit assessment

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** —
- **Branch/PR:** m56-llm-wiki-investigation · https://github.com/jmgirard/cairn/pull/54

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

- [x] AC1: `cairn/references/llm-wiki.md` exists with full citation of the
      gist (primary source read directly, per the primary-sources rule), the
      formalism (three layers, page schema, ingest/query/lint operations,
      schema-file role), and ecosystem-scan findings, all with URL anchors.
- [x] AC2: The note's fit assessment maps LLM Wiki elements to cairn's
      references/ feature set element-by-element (raw/↔pdf/, index, log,
      lint, linking, entity pages, ingest workflow), each element carrying an
      adopt / adapt / reject verdict with reason.
- [x] AC3: The fit assessment covers cross-file linking: current de-facto
      link-token practice (M<NN>, D-<NNN>, IPn/GPn; `cairn_impact` whole-word
      tracing) surveyed by `git grep`, assessed against a wikilink-style
      convention + a dangling-link lint — verdict with rationale.
- [x] AC4: The fit assessment covers the agent-memory angle: wiki-as-memory
      framing vs. cairn's session-context injection + stateless-resume
      doctrine — verdict with rationale.
- [x] AC5: Disposition ledger complete — every adopt/adapt verdict lands as a
      ROADMAP candidate row (search-first sweep applied) or a named follow-up
      milestone proposal; every reject carries its reason in the note; no
      element left verdict-less.
- [x] AC6: `cairn_validate` passes after the additions (note + INDEX line +
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
- [x] T2: Ecosystem scan — LangChain OpenWiki, nvk/llm-wiki, SamurAIGPT
      llm-wiki-agent, DeepWiki/AutoWiki (light), community hardening patterns
      (provenance headers, page-vs-edit heuristic); add the scan section.
- [x] T3: Fit assessment, target 1 — references/ formalism: element-by-element
      map + verdicts against tracking-rules "Source ingestion".
- [x] T4: Fit assessment, target 2 — cross-file linking: `git grep` the
      current link-token practice across `cairn/`; verdict on a linking
      convention + dangling-link lint (note `cairn_impact`'s existing tracing).
- [x] T5: Fit assessment, target 3 — agent-memory angle vs. `session_context`
      hook + the stateless-resume doctrine; verdict.
- [x] T6: Disposition ledger: bank candidates (search-first), add the
      `INDEX.md` line, run `cairn_validate`.

## Work log

- 2026-07-16: created by /milestone-plan (gate: investigation-only; gist +
  ecosystem scan; all three targets; Opus, not Fable — no RB tripwire fires).
- 2026-07-16: T1 done — gist read raw (primary source); formalism section of
  references/llm-wiki.md drafted with verbatim rules; gist states no date.
- 2026-07-16: T2 done — scan of openwiki/nvk/SamurAIGPT/DeepWiki; convergent
  hardening: wikilinks de-facto, lint mechanized, log universal, schema
  human-owned (ecosystem re-derived cairn-style governance).
- 2026-07-16: T3 done — references/ map: two real deltas (name the synthesis
  page type; add a references lint), rest already-have or reject.
- 2026-07-16: T4 done — grep survey: 480 M / 249 D / 96 IP-GP tokens, zero
  true dangling; wikilinks rejected (bare IDs are the link syntax);
  dangling-ref ADVISORY adopted (M57/M99 = FP hazards to tolerate).
- 2026-07-16: T5 done — cairn IS a governed LLM Wiki for project state;
  structural steals rejected, positioning framing adopted → release prep.
  T3–T5 committed together (one file, three sections — minor fold).
- 2026-07-16: T3–T5 verify ran late — a lingering `cd cairn` broke discover
  and `tail -1` masked it; re-ran green from root before T6. Lesson banked.
- 2026-07-16: T6 done — grouped candidate row added; positioning framing
  absorbed into the release-prep row (search-first); INDEX line; validate.

## Decisions

## Review

Evidence gathered fresh by command, 2026-07-16 (PR #54):

- AC1: note exists; gist citation (hash) present ×2; 4 URL anchors; the three
  ops each defined; `## Ecosystem scan` section present. PASS.
- AC2: element map table = 9 element rows + header, 12 bolded verdicts, each
  row carries adopt/adapt/reject/already-have + reason. PASS.
- AC3: grep survey figures (480/249/96) in the note; 8 verdict bullets across
  assessments 2–3 incl. wikilink reject + dangling-ref advisory adopt, both
  with rationale (M57/M99 FP hazards named). PASS.
- AC4: `## Fit assessment 3` present — memory-type mapping, structural reject
  + positioning adopt with rationale. PASS.
- AC5: `## Disposition ledger` complete; grouped candidate row in ROADMAP;
  release-prep row absorbed the positioning framing (search-first: absorbed,
  not duplicated); INDEX line added; 6 rejects with reasons in the note. PASS.
- AC6 + consistency gate: `cairn_validate` all 14 checks pass + sizing OK;
  three unittest suites OK. Coverage completeness: AC1–AC6 all mapped, T1–T6
  all exist. No principle change → `cairn_impact` skipped. Toolchain half:
  generic profile names none — clean no-op.

Independent review (three lenses + scorer, 2026-07-16): diff-bug [O] verified
every checkable claim (gist quotes verbatim, grep counts reproduce at the T4
tree state, validate/orphan-check/ADVISORY claims accurate, ledger conserves
all verdicts) — 1 finding; blame-history [S] — no findings (release-prep
amendment consistent with M54's carve-out; no rejected idea re-added; one
count-drift observation discarded as taxonomy noise); prior-PR [S] — no
prior-PR evidence (52 merged PRs, zero inline comments), clean no-op.
Scored ≥80 (actioned): F1/88 — DeepWiki/AutoWiki bullet lacked the URL
anchors AC1 requires → fixed (deepwiki.com + the OpenWiki announcement
anchoring the "credited as inspiration" claim). Below 80 (logged): none.
