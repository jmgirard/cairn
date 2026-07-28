# M120: Ingest the Opus 5 prompting guide, and adopt the three conduct rules cairn has no home for

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Branch/PR:** `m120-opus5-guide-adoptions` · https://github.com/jmgirard/cairn/pull/120

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

- [x] AC1 — `cairn/references/prompting-opus-5.md` exists, authored from
      `skills/shared/templates/source-note.md`, carrying a `**Provenance.**`
      block that names the ingested date and ingesting milestone in the form
      `_PROV_INGESTED` parses (`scripts/cairn_validate.py:286-289`), the
      guide's URL, how it was retrieved and by whom, `—` as the pagination
      basis, and an `Extraction:` status on one physical line carrying its own
      `— observed YYYY-MM-DD`. `cairn/references/INDEX.md` gains one line for
      it, and `python3 scripts/cairn_validate.py` exits 0 with
      `references index<->disk` passing and no `references staleness` WARN
      naming this page.
- [x] AC2 — Under the page's `## Traces to` heading, one line per rule this
      milestone ships that rests on the guide, each naming the file and the
      heading or step the rule landed in. The rules AC3–AC5 ship each appear
      there, and no line names a rule absent from `git diff <default>..HEAD`.
- [x] AC3 — `tracking-rules.md`'s "Output & interaction discipline" section
      carries a correction-narration rule stating all three of: an earlier
      chat statement is corrected only when the error would change the user's
      code, conclusions, or decisions; a correction is stated plainly and
      briefly and the task then continues; a chat slip that changes nothing for
      the user is fixed without being narrated, which never reaches a durable
      record (corrected in place and marked, D-045). A prose-guard in
      `skills/tests/` asserts a phrase from each of the three clauses, each
      phrase occurring within a single physical line of the shipped file, and
      each phrase carries its own entry in `skills/tests/test_mutation_harness.py`.
- [x] AC4 — `tracking-rules.md`'s "Model and agent strategy" section carries a
      delegation-warrant test stating both: work the session can finish itself
      in a handful of tool calls is done inline rather than delegated; and
      where one subagent can do the task, one is spawned rather than several.
      A prose-guard in `skills/tests/` asserts a phrase from each clause, each
      occurring within a single physical line of the shipped file, and each
      phrase carries its own mutation entry.
- [x] AC5 — `skills/milestone-review/SKILL.md` step 5 instructs all three
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
- [x] AC6 — `scripts/tests/test_scripts.py`'s `TestShippedPageStateLedger.EXPECTED`
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
- [x] T5 — Relocate the false-positive taxonomy in
      `skills/milestone-review/SKILL.md:178-190`; correct
      `test_review_fanout.py`'s taxonomy test name and docstring; author the
      guard per AC5, anchored off the rubric text, with the absence assert
      paired to its positive framing.
- [x] T6 — Append the `cairn/DECISIONS.md` entry for the relocation; note that
      D-016's rationale (the scorer gates what reaches the user) now covers
      more surface without needing supersession.
- [x] T7 — Complete `## Traces to` against the actual diff; run the §8
      description-layer certification (this milestone authors prose-guards) and
      enter the gate at zero unresolved.
- [x] T8 — Once M119 has merged and its §8 round-count candidate row is on the
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
- 2026-07-27: T7 — §8 description-layer certification round 1, fresh-context [O] reader, 4 discrepancies, all fixed: (1)+(2) two docstring quotes were verbatim in the guide but absent from the ingested page's Extracted values, so the page gained both — a corrector walking `## Traces to` could not have checked them; (2) also mis-attributed a claim about Claude Opus 5 to "the orchestrator tier"; (3) D-078 said the sub-80 logging paragraph was "the very next paragraph" when the rubric sits between them — it is two below; (4) a registry comment said a block blanks a line when it blanks a four-word phrase of one. Anchor-vs-shipped-bytes and AC-clause-to-assert coverage both passed with no discrepancy.
- 2026-07-27: T7 — D-078's Context and Consequences were corrected in place rather than superseded, and the entry has never been on the default branch: the branch squash-merges, so D-078 enters history once, in the corrected form, and there is no published version to supersede. Recorded here because the correction is invisible in the merged diff.
- 2026-07-27: T7 — §8 round 3 scoped to the one fix and a re-resolution of all 8 `## Traces to` anchors: UNRESOLVED 0, gate entered at zero. Three rounds total (4 discrepancies, then 1, then 0) — recorded for the standing §8 round-count candidate row, whose promotion condition is exactly this figure from the next guard-authoring milestone.
- 2026-07-27: T7 — §8 round 2: all four round-1 fixes verified real, 1 new discrepancy, self-inflicted — the round-1 docstring rewrite grew `test_delegation_warrant.py` by one line, so the `## Traces to` anchor written in round 1 pointed at a blank line and the class had moved to :41. Fixed, and every other anchor re-verified rather than assumed. Round 2 also flagged, without counting it, that the extraction status cannot be checked from the artifact because the source is a URL and the shelf is gitignored — inherent to a non-PDF source and sanctioned by the template, so no change.
- 2026-07-27: T7 — certification also noted a coverage limit that is not an AC5 gap: the guard reds when the taxonomy is MOVED out of the scorer's rubric, but a fresh restatement of it ADDED to the reviewers' instruction, in wording the literal absence-assert does not name, leaves both tests green. AC5 asks only for the literal-string absence, which is asserted; D-078's Consequences now states the bound instead of claiming closure.
- 2026-07-27: T8 — M119 merged before this milestone started (archived at `8dace78`), so its §8 round-count row was on the default branch and the corroboration was appended in place rather than deferred. Row edited as current knowledge (D-052); the promotion condition is untouched, and the append names a third disposition only.
- 2026-07-27: T6 — D-078 appended. Bounded read run over the `### D-` headings; D-016 matched and was read whole and back-referenced (its own id appears only at its heading, so no later entry annotates it). D-016 is annotated, not superseded: its rationale that the scorer gates what reaches the user is unchanged and now covers more surface.
- 2026-07-27: T5 — taxonomy relocated into the scorer's rubric; reviewers now told to report every candidate finding and filter nothing. Guard locates the rubric by its own first line and walks the contiguous blockquote, so the taxonomy drifting back into the reviewers' instruction reds it; the `assertNotIn` is paired with the report-everything phrase, which is what the harness registers (guard-doctrine §3). Caught in the act: the first draft wrapped "an intentional / change" across two lines and the token assert failed — the M23/M64 one-physical-line rule, found by the suite rather than by eye.
- 2026-07-27: T4 — delegation-warrant rule added to Model and agent strategy, placed before the tier bullets because it decides whether a spawn happens and they decide which tier it gets. Step-0 one-home checked: nothing in the corpus states when to work inline — the rulebook's only delegation prose is tier selection, and `/milestone-implement`'s "delegation policy" pointer resolves to those same tier bullets. New guard `skills/tests/test_delegation_warrant.py`, three asserts, three mutation entries, each verified to redden when blanked.
- 2026-07-27: implement gate chose wording the new delegation rule to say why the review fan-out's several agents are not the case it forbids (they carry distinct evidence, not one task done three times) over stating the two clauses bare, at the user's direction, because both rules land in the same rulebook section; falsified by a reader still reading the two as contradictory.
- 2026-07-27: T3 — correction-narration rule added to Output & interaction discipline after "Narrate outcomes, not deliberation"; step-0 one-home checked, the corpus states nothing about narrating a chat correction and the nearest rule ("Correcting a record proven false") governs tracking records, so the new rule cross-references it rather than restating it. Guard is four asserts in `test_narration_discipline.py`, each phrase copied from the shipped bytes and each carrying its own mutation entry; all four verified to redden when blanked.
- 2026-07-27: implement gate chose placing each new guard with the file that owns its topic — correction narration into `test_narration_discipline.py`, delegation into a new file — over one milestone-named file, at the user's direction; falsified by the narration file growing beyond one subject.

## Decisions
- 2026-07-27: review fan-out found 3 asserts surviving inversion (F1, F4, F16) because guard-doctrine §1's inversion protocol had not been run — only blanking was. All 10 asserts now verified by inversion, 0 survive. Fixed 7 distinct findings scored 80+; 20 sub-80 findings logged in the Review section.

## Review

_Evidence gathered by command 2026-07-27; each criterion ticked as its own line landed._
- **AC1 verified** 2026-07-27. `cairn/references/prompting-opus-5.md` exists, authored from `templates/source-note.md`. `_provenance_block` parses it; `_PROV_INGESTED` yields `2026-07-27`, `_PROV_SOURCE` and `_PROV_LOCATOR` both match, and the block names `by M120`. `Pagination: —` at `:8`. `Extraction:` is one physical line (`:10`) carrying its own `— observed 2026-07-27`; `_last_verified` returns `('ok', 2026-07-27)`. `INDEX.md` carries exactly one line for the page. `python3 scripts/cairn_validate.py` exits 0 with `references index<->disk` PASS and `references staleness` OK — the page is named in zero WARNs.
- **AC2 verified** 2026-07-27. `## Traces to` carries five bullets and eight `file:line` anchors. Each anchor was resolved by reading line N out of the named file: all eight point at what they claim (`tracking-rules.md:553`/`:650`, `SKILL.md:178`/`:191`, `test_narration_discipline.py:55`, `test_delegation_warrant.py:41`, `test_review_fanout.py:97`/`:105`). Every anchored file appears in `git diff --name-only main..HEAD`, so no line names a rule absent from the diff; the rules AC3, AC4 and AC5 ship each have their own bullet.
- **AC3 verified** 2026-07-27. The rule sits at `tracking-rules.md:553` in Output & interaction discipline and states all three clauses. `TestCorrectionNarrationRule` asserts four phrases; each occurs exactly once in the shipped file and each lies within a single physical line (per-line scan, not whole-file). Each of the four carries its own `test_mutation_harness.py` entry, and `guard_fails_when_blanked` returns True for all four — no false coverage.
- **AC4 verified** 2026-07-27. The rule sits at `tracking-rules.md:650` in Model and agent strategy and states both clauses. `TestDelegationWarrantRule` asserts three phrases (the two required plus the fan-out reconciliation added at the implement gate); each occurs exactly once and within a single physical line, and each carries its own mutation entry, all three verified to redden when blanked.
- **AC5 verified** 2026-07-27. `SKILL.md:178` tells all three reviewers to report every candidate finding, filtering nothing. The scorer's rubric blockquote — located by its own first line and walked as a contiguous `>` run, `SKILL.md:186-195`, 10 lines — carries `Not a finding` and all five members, framed `out of scope for this diff` and scored `below 60`. The literal `drop anything matching it before reporting` occurs zero times; its absence-assert is paired with `report every candidate finding`, and that positive phrase is what the harness registers (REDDENS). Repo-wide grep for `handed to the reviewers` and `taxonomy_handed` returns nothing. D-078 (`DECISIONS.md:2523`) records the relocation, two rejected alternatives, and the IP3 gap.
- **AC6 verified** 2026-07-27. `scripts/tests/test_scripts.py:1431` pins `"prompting-opus-5.md": "ok"`; `TestShippedPageStateLedger` passes, and `_last_verified` independently computes `ok` for the shipped page. The work log carries the one-line justification the ledger contract requires.
- **Verify slot** 2026-07-27: `python3 -m unittest discover` over `skills/tests` (688), `scripts/tests` (332) and `hooks/tests` (98) — all OK, each exit code checked separately, all 0. `cairn_validate` exits 0 across 16 PASS checks and 8 advisories, none naming this milestone's files.

### Independent review (three lenses + scorer)

- **Fan-out** 2026-07-27: [O] diff-bug (20 findings), [S] blame-history (6, its
  verdict "nothing in M120 silently undoes prior work"), [S] prior-PR-comments
  (2; the `gh api .../pulls/comments` probe returned `[]`, so no PR-thread walk
  was warranted — primary evidence was `milestones/archive/` `## Review`
  sections and `LESSONS.md`). 28 findings scored by a fresh [S] scorer given the
  rubric verbatim plus the diff and this file.
- **Scorer's meta-finding, actioned above all others:** `guard-doctrine.md` §1
  mandates verification by **inversion** ("Blanking proves only that the text is
  present; inversion is what proves the guard pins the rule"), and this
  milestone's work log recorded only blanking for all seven new asserts. The
  mandated step had not been run. Running it found three asserts that survive
  inverting the rule they claim to pin.

**Actioned — scored 80 or above (8 findings, 7 distinct defects; all fixed):**

- **F1 (92)** — the delegation assert pinned `where one subagent can do the task, spawn one`, leaving the operative predicate `rather than several` on the next physical line: the rule inverted to "spawn several rather than one" with the guard green. Rule rewrapped; assert re-anchored on `spawn one rather than several`.
- **F4 (88)** — the five taxonomy members were pinned as bare tokens (`nitpick`, `linter`, …), so negating every predicate ("a pre-existing issue the diff DID introduce") left the guard green — guard-doctrine §1's label→SET trap. Rubric rewrapped one member per line; each member now pinned whole.
- **F6 (87) / P1 (87)** — the `Score 0–100 your confidence` mutation entry registered the guard's own slice *locator*: blanking it reds by `StopIteration` whether or not the taxonomy is in the rubric, so it proved nothing. That is LESSONS 2026-07-27 (M117), "register the CONTAINED phrase, never the bound". Entry replaced with the disposition sentence; the comment now states that the location claim is not mutation-provable at all, because the harness blanks and never moves.
- **F16 (87)** — two correction-narration anchors stopped mid-clause (`conclusions,` without `or decisions`; `continue the` without `task`); the materiality bar inverted green. Rule rewrapped; both asserts re-anchored on the full clause.
- **P2 (86)** — `Score anything matching this list below 60`, the sentence that gives the taxonomy any effect in its new home, was asserted nowhere; deleting it left all 11 `TestReviewFanout` tests green. New `test_taxonomy_carries_its_scoring_disposition`, with its own mutation entry.
- **F7 (83)** — the relocation moved three diff-relative judgments (pre-existing, unmodified line, plan-called-for) to a scorer whose evidence base step 5 never specified. Step 5 now gives the scorer the diff and the milestone file, and says its independence is from *generating* findings, not from the diff. D-078's Consequences records it.
- **F3 (80)** — "The bullets below decide *which* tier a warranted spawn gets" is false of the Fable bullet, which gates *whether* a Fable spawn happens. Sentence corrected in the rule and in the guard docstring.

**Post-fix re-verification** 2026-07-27: all ten asserted phrases re-checked for
single-physical-line contiguity and uniqueness; every one reddens under
**inversion** (negating the rule in place, running the guard, requiring red) —
0 of 10 survive, against 3 before the fixes. All eight `## Traces to` anchors
recomputed and corrected, the rewraps having shifted four of them. Three suites
green (689 / 332 / 98, exit 0 each); `cairn_validate` exit 0, 24 checks, no FAIL
or WARN.

**Logged, not actioned — 20 findings below 80** (IP3: surfaced, never silently
dropped). F20 (78) Scope "Out" text about M119 being unmerged is stale in the
merged artifact — true at plan time, plan-owned, amendable only by gate. F17
(76) the generic `assertIn` suffix-append weakness, not specific to this diff.
F9 (68) narration guard's module docstring named only the M67 rule — **fixed
anyway**, it was one line. F10 (68) `references/anthropic-code-review.md`'s
taxonomy bullet lacks a `*(Shipped: …)*` disposition annotation. F2 (62) the
inline-floor rule's reach over mandated fresh-context spawns — **partly
addressed**: the rule now says a spawn made for freshness is not a volume
judgment it reaches. F14 (62) "executed by Claude Opus 5" cited to a rulebook
line saying only "Opus". F15 (60) the ROADMAP corroboration crosses from
written-deliverable length to code comments. F18 (60) possible IP2 tension in
the unremarked-slip clause. F5 (48) `_scorer_rubric()`'s bare `StopIteration`
diagnostic and blockquote-walk brittleness. F13 (45) "third clause" mislabels
the guide's sample prompt (scorer judged clause-counting genuinely ambiguous).
F19 (45) D-078's heading says "closes an IP3 gap" where its Consequences says
"the bound, not a closure" — different referents. F11 (35) / H5 (35) the
`EXPECTED` map's comment-per-entry precedent not followed (the literal contract,
a work-log justification, is met). F8 (30) the self-reference that this review
is the new arrangement's own first run. F12 (20) `REGISTRY +=` block placement.
H1–H4, H6 (8 each) history-lens findings reporting no defect.

