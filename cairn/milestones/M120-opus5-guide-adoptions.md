# M120: Ingest the Opus 5 prompting guide, and adopt the three conduct rules cairn has no home for

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Branch/PR:** `m120-opus5-guide-adoptions`

## Goal

Ingest Anthropic's Claude Opus 5 prompting guide as a cited source note, and
adopt the three conduct changes it supplies where cairn measurably has no rule:
chat-level correction narration, a delegation-warrant test, and the removal of
the pre-report finding filter that instructs review reviewers to report less.

## Scope

**In:** the source note and its INDEX line; a correction-narration rule and a
delegation-warrant test in `tracking-rules.md`; relocating
`/milestone-review`'s false-positive taxonomy out of the reviewers' instruction
and into the scorer's rubric, with the D-entry that cross-cutting change owes;
prose-guards with per-phrase mutation entries for each new rule; the
`TestShippedPageStateLedger` pin the new page forces.

**Out:** the over-verification triage and any re-decision of D-067's two
fresh-context readers → M121 (planned now, depends on this). A reasoning-effort
dial per spawned agent → candidate row: unreachable today, since cairn ships no
agent definitions and the Agent tool exposes only model tier. A numeric cap on
subagent spawning → candidate row; `milestone/SKILL.md:79-84` forbids proposing
one without superseding it. A drafting budget for code comments and docstrings
→ T8 appends it to the standing §8 round-count candidate row as further
evidence; that row exists only on M119's unmerged branch today, so the append
waits for M119 to merge rather than being transcribed onto a row main lacks.

## Acceptance criteria

- [ ] AC1 — `cairn/references/prompting-opus-5.md` exists, authored from
      `skills/shared/templates/source-note.md`, carrying a `**Provenance.**`
      block that names the ingested date and ingesting milestone in the form
      `_PROV_INGESTED` parses (`scripts/cairn_validate.py:286-289`), the
      guide's URL, how it was retrieved and by whom, `—` as the pagination
      basis, and an `Extraction:` status on one physical line carrying its own
      `— observed YYYY-MM-DD`. `cairn/references/INDEX.md` gains one line for
      it, and `python3 scripts/cairn_validate.py` exits 0 with
      `references index<->disk` passing and no `references staleness` WARN
      naming this page.
- [ ] AC2 — Under the page's `## Traces to` heading, one line per rule this
      milestone ships that rests on the guide, each naming the file and the
      heading or step the rule landed in. The rules AC3–AC5 ship each appear
      there, and no line names a rule absent from `git diff <default>..HEAD`.
- [ ] AC3 — `tracking-rules.md`'s "Output & interaction discipline" section
      carries a correction-narration rule stating all three of: an earlier
      chat statement is corrected only when the error would change the user's
      code, conclusions, or decisions; a correction is stated plainly and
      briefly and the task then continues; a chat slip that changes nothing for
      the user is fixed without being narrated, which never reaches a durable
      record (corrected in place and marked, D-045). A prose-guard in
      `skills/tests/` asserts a phrase from each of the three clauses, each
      phrase occurring within a single physical line of the shipped file, and
      each phrase carries its own entry in `skills/tests/test_mutation_harness.py`.
- [ ] AC4 — `tracking-rules.md`'s "Model and agent strategy" section carries a
      delegation-warrant test stating both: work the session can finish itself
      in a handful of tool calls is done inline rather than delegated; and
      where one subagent can do the task, one is spawned rather than several.
      A prose-guard in `skills/tests/` asserts a phrase from each clause, each
      occurring within a single physical line of the shipped file, and each
      phrase carries its own mutation entry.
- [ ] AC5 — `skills/milestone-review/SKILL.md` step 5 instructs all three
      reviewers to report every candidate finding rather than to drop any
      before reporting, and carries the false-positive taxonomy verbatim inside
      the `[S]` scorer's rubric instead, framed so the scorer treats a taxonomy
      match as out of scope for this diff. A prose-guard asserts the
      report-everything instruction and asserts the taxonomy's label and all
      five members occur inside the rubric blockquote, anchored on the rubric's
      own text rather than on a block used as a slice bound; it asserts the
      literal string `drop anything matching it before reporting` is absent,
      registered with the report-everything phrase as its positive framing
      (guard-doctrine §3). `skills/tests/test_review_fanout.py`'s taxonomy test
      name and docstring no longer claim the taxonomy is handed to the
      reviewers. A `cairn/DECISIONS.md` entry records the relocation, the
      alternative rejected, and the IP3 gap it closes.
- [ ] AC6 — `scripts/tests/test_scripts.py`'s `TestShippedPageStateLedger.EXPECTED`
      gains `prompting-opus-5.md` with the staleness state `_last_verified`
      computes for the shipped page, and the milestone's work log carries the
      one-line justification the ledger's contract requires
      (`scripts/tests/test_scripts.py:1389-1392`).

## Coverage

- AC1 → T1
- AC2 → T1, T7
- AC3 → T3
- AC4 → T4
- AC5 → T5, T6
- AC6 → T2

## Tasks

- [x] T1 — Author `cairn/references/prompting-opus-5.md` from the source-note
      template: provenance (URL, retrieval, ingested date, `—` pagination,
      dated extraction status), citation, role, the guide's recommendations as
      extracted values with their section anchors, and a `## Traces to` stub.
      Add its `INDEX.md` line.
- [x] T2 — Pin the page in `scripts/tests/test_scripts.py`'s
      `TestShippedPageStateLedger.EXPECTED`; add the work-log justification
      line the ledger contract requires. `python3 -m unittest` over
      `scripts/tests` green from the repo root, exit code checked.
- [x] T3 — Write the correction-narration rule into `tracking-rules.md`'s
      Output & interaction discipline, adjacent to "Narrate outcomes, not
      deliberation" (D-039's central-rule-only wiring). Author the guard by
      copying the shipped bytes (LESSONS 2026-07-20/M95); add one mutation
      entry per asserted phrase; verify each reddens when blanked.
- [x] T4 — Write the delegation-warrant test into "Model and agent strategy".
      Guard + per-phrase mutation entries, same protocol as T3. Record in the
      work log that step-0 one-home was checked: nothing in the corpus states
      when to work inline.
- [ ] T5 — Relocate the false-positive taxonomy in
      `skills/milestone-review/SKILL.md:178-190`; correct
      `test_review_fanout.py`'s taxonomy test name and docstring; author the
      guard per AC5, anchored off the rubric text, with the absence assert
      paired to its positive framing.
- [ ] T6 — Append the `cairn/DECISIONS.md` entry for the relocation; note that
      D-016's rationale (the scorer gates what reaches the user) now covers
      more surface without needing supersession.
- [ ] T7 — Complete `## Traces to` against the actual diff; run the §8
      description-layer certification (this milestone authors prose-guards) and
      enter the gate at zero unresolved.
- [ ] T8 — Once M119 has merged and its §8 round-count candidate row is on the
      default branch, append the guide's written-deliverable-length finding to
      that row as third-party corroboration, naming that it adds a third
      disposition (budget the description layer) without changing the row's
      promotion condition. If M119 is still unmerged at this milestone's
      review, say so in the work log and leave the row alone.

## Work log

- 2026-07-27: created by /milestone-plan.
- 2026-07-27: plan gate chose relocating the review taxonomy into the scorer rubric over leaving both filters in place because a pre-report drop reaches neither the scorer nor the Review section, which IP3's sub-80 logging line already refuses downstream; falsified by a review pass whose scored-and-logged findings are dominated by taxonomy matches the reviewers used to absorb.
- 2026-07-27: plan gate chose the rulebook over a doctrine module for both new rules because both are continuous, universally-read conduct with no conditional trigger, which is D-039's precedent and fails D-031's module test; falsified by either rule proving to be read only at a specific gate.
- 2026-07-27: plan chose a source note over treating the guide as consulted-in-passing because three shipped rules will trace to it, which is the "When a page is owed" reliance test; falsified by all three rules being cut before merge.
- 2026-07-27: T1 — the guide was retrieved as raw Markdown (`curl` of the page's `.md` sibling at `platform.claude.com`, HTTP 200, 11,225 bytes) rather than through a summarizing fetch, so the extraction status claims a first-hand verification honestly; the `docs.claude.com` slug 302-redirects to that host.
- 2026-07-27: T2 — `TestShippedPageStateLedger.EXPECTED` gains `prompting-opus-5.md: "ok"` (the ledger contract's required justification): the page's extraction status claims a verification and carries the date `2026-07-27`, so `_last_verified` resolves `verified` → freshest non-future date → `ok`; no partial or negated clause appears in the status.
- 2026-07-27: minor amendment — T2 landed in T1's checkpoint commit rather than its own, because adding the page without its ledger pin leaves `scripts/tests` red and T1 could not be checked off against a clean verify slot. Task text unchanged.
- 2026-07-27: T4 — delegation-warrant rule added to Model and agent strategy, placed before the tier bullets because it decides whether a spawn happens and they decide which tier it gets. Step-0 one-home checked: nothing in the corpus states when to work inline — the rulebook's only delegation prose is tier selection, and `/milestone-implement`'s "delegation policy" pointer resolves to those same tier bullets. New guard `skills/tests/test_delegation_warrant.py`, three asserts, three mutation entries, each verified to redden when blanked.
- 2026-07-27: implement gate chose wording the new delegation rule to say why the review fan-out's several agents are not the case it forbids (they carry distinct evidence, not one task done three times) over stating the two clauses bare, at the user's direction, because both rules land in the same rulebook section; falsified by a reader still reading the two as contradictory.
- 2026-07-27: T3 — correction-narration rule added to Output & interaction discipline after "Narrate outcomes, not deliberation"; step-0 one-home checked, the corpus states nothing about narrating a chat correction and the nearest rule ("Correcting a record proven false") governs tracking records, so the new rule cross-references it rather than restating it. Guard is four asserts in `test_narration_discipline.py`, each phrase copied from the shipped bytes and each carrying its own mutation entry; all four verified to redden when blanked.
- 2026-07-27: implement gate chose placing each new guard with the file that owns its topic — correction narration into `test_narration_discipline.py`, delegation into a new file — over one milestone-named file, at the user's direction; falsified by the narration file growing beyond one subject.

## Decisions

## Review
