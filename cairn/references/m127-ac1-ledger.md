# M127 AC1 classification ledger (retirement search over `skills/` + `README.md`)

Every hit of AC1's search — `grep -rn "certif"` and `grep -rn "§8"` over
`skills/` and `README.md` — after M127's edits, each classified against AC1's
operative class: *a shipped sentence that obliges, routes to, or presupposes
the certification step as live*. Zero hits are operative — observed 2026-07-31.
Committed because AC1 rests on a per-hit judgment with no oracle (RR04 rec 8).

**Provenance.** First-hand analysis, not a source extraction — no shelf item
backs it. Produced by the M127 implementing session on branch
`m127-retire-certification`; the state it describes is the tree at this
ledger's own first commit (the ledger's rows exclude themselves and the
milestone's tracking files, which AC1 scopes out by searching only `skills/`
and `README.md`). Ingested 2026-07-31; ingesting milestone M127. Pagination
basis: —.

Extraction: first-hand record with nothing to re-verify against — the corpus is this repo's own prose at the commit that carries this ledger, and the search is re-runnable from the two commands above; line numbers go stale with any edit, so re-locate by content — observed 2026-07-31.

## Surviving-hit classes (AC1's enumeration)

- **RP** — retrospective provenance citation in a comment, docstring, or guard
- **§9M** — §9's motivating measurement
- **CA** — the criteria audit's own prose (D-067's surviving instrument)

README.md: zero hits on either term. One hit was reclassified during the
sweep: `test_always_read_frame.py`'s docstring read "the job §8's first
sentence *describes*" — present tense over removed text, the operative class —
and was tense-shifted with a retirement note in the same pass.

## Per-hit rows

| File:line | Hit (compressed) | Class |
|---|---|---|
| test_delegation_warrant.py:86 | docstring: retired assert's history, "M127 removed that sentence" | RP |
| test_delegation_warrant.py:148 | comment: M121 F-B1 inversion measurement narrated via §8's loop | RP |
| test_guard_doctrine_sections.py:1,3,6 | own docstring: the retirement and M124's numbering measurement | RP |
| test_fresh_context_readers.py:18 | docstring: "Until M127 this file also locked … §8" | RP |
| test_fresh_context_readers.py:55 | comment: "certify-your-model-of-the-artifact failure the instrument exists to stop" — the audit's diagnosis | CA |
| test_fresh_context_readers.py:180 | comment: "Found by M115's own certifier against its own guard" | RP |
| test_lesson_graduation.py:38,245,253 | comments: M125 §8-round finding provenance | RP |
| test_mutation_harness.py:2395 | comment on kept §6 recorded-counts entries: "(§8 round 2 finding 1)" | RP |
| test_mutation_harness.py:2429 | comment: "gapped at the retired §8" | RP |
| test_always_read_frame.py:24-26 | docstring: RR11's self-certification finding, now past-tense with the retirement named | RP |
| test_always_read_frame.py:169,191,205 | comments: M126 §8-round finding provenance | RP |
| milestone-plan/SKILL.md:40 | "audit over a rougher draft certifies text that never ships" | CA |
| guard-doctrine.md:268 | §9's "Every assert in §8 matched … (M123 round 3)" | §9M |
| guard-doctrine.md:308 | §9's closing record: "covered §8, the certification section M127 retired whole" | RP |
