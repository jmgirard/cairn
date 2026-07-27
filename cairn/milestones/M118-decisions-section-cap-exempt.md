<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. Drafting budgets: see the template. -->
# M118: The milestone-local `## Decisions` section joins the cap-exempt set

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** RR08
- **Principles touched:** IP4
- **Branch/PR:** `m118-decisions-cap-exempt` · https://github.com/jmgirard/cairn/pull/118

## Goal

Exempt the append-only `## Decisions` section from the 150-line plan-owned cap,
on the same un-editability grounds D-046 used for `## Work log`, and wire the
third exempt member through every surface that enumerates the set.

## Scope

**In:** the cap counter and its heaviest-first breakdown; the session-start
read-bound for cap-exempt sections; every rulebook, template and guard site that
enumerates the exempt set; the peak-revision ledger; D-074.

**Out:** the `decisions format` advisory, the rulebook's history-class member
enumeration, and the hook/counter consistency test → **M119** (planned now,
depends on this); redistributing the >=21 template lines the exemption frees →
candidate row; any change to the 150 cap itself → not proposed; exempting an
RR-bound AC block and standardising carry-by-reference → declined at the plan
gate on measured evidence (D-066 choice 4 already governs the latter).

## Acceptance criteria

- [x] AC1: `milestone_body_line_count` excludes an exact `## Decisions` section,
      matched by the same shared constant and fence rules the work-log exemption
      uses; a fenced `## Decisions` and `## Decisions notes` both stay counted.
      Fixtures: exact, fenced, prefixed, absent.
- [x] AC2: `milestone_section_line_counts` omits it from the heaviest-first
      breakdown, so no over-cap diagnostic names a section IP4 forbids editing,
      and `preamble + sections == body` (`cairn_scripts.py:436-441`) still holds.
- [x] AC3: A committed ledger re-measures every milestone file's **peak
      plan-owned revision** under both counters; every file whose peak exceeded
      the cap falls below it. It carries the numbers; no prose here does (M99).
- [x] AC4: `hooks/session_context.py` read-bounds `## Decisions` per D-063, and
      `SECTION_MAX_CHARS`'s justifying comment is re-derived over all three
      section types from fresh measurement, not left asserting a p90 over two.
      Test: newest-first injection plus the omission notice.
- [x] AC5: Every site enumerating the cap-exempt set names all three members and
      each member's stated reason: the rulebook's weight-caps and cap-remedies
      bullets and its always-read frame row and prose (`:184-186`); the
      template's budget preamble and its `## Decisions` / `## Review` comments;
      and `test_milestone_cap_exemption.py:62`, whose set-membership assert is
      anchored on the whole set and is re-anchored, never appended to. No
      two-member set survives.
- [x] AC6 (BC4): RR08 §BC4 — this file's own `## Decisions` holds only dated
      decision entries; the AC3 ledger lands as a committed file.
- [x] AC7: All three suites clean (the profile's `verify` slot), `cairn_validate` green.

**Deviations from RR08.** BC4 is carried **by reference** to the archived RR
(cap; verbatim measured ~150 plan-owned lines at ingestion — the D-066 choice-4
case). BC1-BC3 depart this milestone entirely: they are delivered by M119, which
declares the same Driving RR and carries them under its own table.

| BC | Departure | Reason |
|---|---|---|
| BC1 | not in this milestone | rulebook history enumeration → M119 |
| BC2 | not in this milestone | hook/counter consistency test → M119 |
| BC3 | not in this milestone | `decisions format` advisory → M119 |
| BC4 | by reference; committed-file horn taken | cap; `## Review` is review-exclusive, T3 is an implement task |

## Coverage

- AC1 -> T2
- AC2 -> T2
- AC3 -> T3
- AC4 -> T4
- AC5 -> T5
- AC6 -> T3
- AC7 -> T6

## Tasks

- [x] T1: Add `DECISIONS_HEADING` beside `WORKLOG_HEADING` (`cairn_scripts.py:97`)
      and a `milestone_decisions_lines` extractor mirroring the work log's, so
      the exemption and M119's advisory read one section by one rule.
- [x] T2: Exempt the section in `milestone_body_line_count`, drop it from
      `milestone_section_line_counts`, update both docstrings. Fixtures first
      (exact/fenced/prefixed/absent + the sum invariant), red before the change.
- [x] T3: Peak-revision ledger over `git log --all`, run under both counters,
      committed as its own file (never into `## Decisions` — BC4).
- [x] T4: Add `"decisions"` to `CAP_EXEMPT_SECTIONS` (`session_context.py:56`);
      re-measure p90 over all three section types and re-derive
      `SECTION_MAX_CHARS`'s comment. Hook test per AC4.
- [x] T5: Re-anchor the set-membership guard and update AC5's prose sites;
      re-register the anchor and verify by mutation that deleting the
      three-member sentence reds it.
- [x] T6: Full `verify` + `cairn_validate`; post-merge hygiene.

## Work log

- 2026-07-27: created by /milestone-plan.
- 2026-07-27: plan gate chose exempting `## Decisions` over exempting an RR-bound AC block, and over standardizing carry-by-reference, because the squeeze is not RR-specific — of the 7 files ever at ≥145 plan-owned lines only M114 was RR-driven, and all 7 carry a Decisions section of 24–43 lines against a median of 4 over 116 files; falsified by a future squeeze whose Decisions section is at or below the median, which would locate the cost elsewhere.
- 2026-07-27: plan gate classified the section as history (D-045) over current knowledge, because the ownership table already makes it append-only and the alternative is self-defeating — a correctable section is trimmable, and a trimmable section has no claim to the un-editability exemption; falsified by a milestone-local decision that must be corrected in place rather than superseded by a later entry in the same section.
- 2026-07-27: escalation offered at the gate on the `ip-touching` tripwire (the classification extends IP4's reach to a new section) and declined by the maintainer, who returned the call to the session.
- 2026-07-27: blocked on RB08 — the maintainer reversed the gate's escalation decline and sent the history-vs-current-knowledge classification (D-074 part 1) to independent review before any code is written.
- 2026-07-27: RR08 ingested; classification upheld, four binding criteria carried by reference, AC5/T3/T5 amended and T7 added at the gate; status back to `planned`.
- 2026-07-27: ingest gate chose carry-by-reference over compressing the heaviest plan-owned section, because verbatim measured ~150 lines against a 149 ceiling and compression would repeat M114's zero-headroom end state; falsified by a plan-owned section whose compression frees the criteria set without touching content the AC or Coverage maps depend on.
- 2026-07-27: RR08 rec 6 applied as supporting context, not a second ground — the section was never plan-owned (the template's own budget preamble says plan spends none of it), which independently explains why a plan-discipline budget never should have charged it.
- 2026-07-27: ingestion put the file at 172/149 and the AC and Tasks sections were compressed in one pass each to reach 149/149 — zero headroom, M114's end state exactly. The 24 lines that broke it are this milestone's own `## Decisions` section, which stops counting at T2: M118 is over cap for the reason M118 exists.
- 2026-07-27: split at the maintainer's call after the sizing advisory reported 11 criteria against the >7 tripwire — the advisory, the rulebook history enumeration and the consistency test (BC1-BC3) become M119, which depends on this milestone; nothing was discarded. Plan-owned body 149 -> 122.
- 2026-07-27: split kept BC4 here because it constrains this file's own `## Decisions` section and the AC3 ledger; D-075's "Delivered by M118" now reads as the M118+M119 pair, and being history it is recorded rather than edited.
- 2026-07-27: status -> in-progress on branch `m118-decisions-cap-exempt`.
- 2026-07-27: implement gate re-measured the three cap-exempt section types over every live revision of all 119 milestone files (peak per file per section, chars): work log p90 4107, review p90 6718, decisions p90 1372 / max 4647. `## Review` already exceeds `SECTION_MAX_CHARS` before M118 adds anything.
- 2026-07-27: gate kept `SECTION_MAX_CHARS` at 6000 and re-derived its comment honestly over all three types, rather than raising it to clear review's p90, because the constant bounds a read and M118 raises the per-milestone worst case from two sections to three (18k -> 21k of a 30k budget if raised); falsified by an injection whose review trim loses state a resuming session needed.
- 2026-07-27: gate placed the AC3 ledger at `cairn/references/` as a synthesis note, following `rulebook-classification-ledger.md` (M116), over a file beside the milestone.
- 2026-07-27: T1 — `DECISIONS_HEADING` + `milestone_decisions_lines`; the work-log extractor's body factored into a shared `_section_body_lines(path, heading)` so both exempt sections are read by one rule. 9 tests red first, all three suites green.
- 2026-07-27: T2 — both counters exempt the section via a shared `EXEMPT_HEADINGS` tuple, so the count and its breakdown can never disagree; 9 fixtures added, 4 red first (fenced/prefixed/absent controls green as designed). This file's own plan-owned body 122 -> 98.
- 2026-07-27: T3 — peak-revision ledger committed as `references/m118-cap-exemption-ledger.md` (+ INDEX line), scored by the shipped `_plan_owned_scan` rather than a reimplementation; every path that ever reached the cap falls below it and none lands near it. The ledger carries the numbers; the AC4 section sizes ride the same derivation.
- 2026-07-27: T3 checked off on `cairn_validate` alone without the full `verify` slot — the omission surfaced at T4 as a red `TestShippedPageStateLedger` (the new page was missing from the pinned state ledger) and was fixed there; no other task skipped the slot.
- 2026-07-27: T4 — `CAP_EXEMPT_SECTIONS` is three members; `SECTION_MAX_CHARS` held at 6000 with its comment re-derived over all three types and citing the ledger instead of carrying a second copy. 3 hook tests, 2 red first (the prefixed-heading control green as designed).
- 2026-07-27: T5 — all five AC5 sites widened to three members; set-membership and cap-remedy asserts re-anchored whole, three new asserts added (decisions reason, always-read enumeration, template comment), each registered in the mutation harness. Verified both ways: blanking reds each new block, and a by-hand SWAP back to the two-member sentence reds the membership guard (M76 — blanking is not swapping).
- 2026-07-27: T6 — full `verify` slot clean (676 + 298 + 94) and `cairn_validate` green before the guard-doctrine §8 gate.
- 2026-07-27: §8 certification round 1 — a fresh-context [O] reader that authored none of the work returned 16 discrepancies, 11 blocking, in all three categories. All resolved this pass; nothing argued down.
- 2026-07-27: the §8 reader's largest class was five two-member enumerations of the exempt set in files AC5 did not list — `cairn_budget.py`'s operator-facing note (which captioned a number that already subtracted the third section), `cairn_validate`'s breakdown comment, and three docstrings. AC5 widened the sites it named and stopped there.
- 2026-07-27: three shipped records claimed the `decisions format` advisory watches the section in the present tense; M118's own Scope sends that advisory to M119, so the claims were false at HEAD. Corrected in `cairn_scripts.py` (x2) and the template comment.
- 2026-07-27: the ledger's corpus was scoped by path prefix and so dropped M01 entirely plus three pre-rename `project/milestones/` paths; re-derived over both roots and grouped by milestone ID — 119 milestones over 122 paths. No conclusion moved: still 3 over cap before, 0 after, max 129 (M43).
- 2026-07-27: ledger reconciliation — the work-log p90 recorded at the implement gate (4107, measured at `35b14ed`) is superseded by the ledger's 4228, and the work-log over-6000 count moved 5 -> 6, both because M118's own file grew inside the corpus it measures. The counts now ship as dated observations naming their measurement commit.
- 2026-07-27: the ledger's Extraction status claimed re-running the derivation at a named commit reproduces its row; true only of the pre-M118 column, since the two peaks are independent maxima. M55 is the counter-example (row 92/88, `96b1897` scores 92/86) and is now the worked case in the page.
- 2026-07-27: three guard gaps the §8 reader found and this pass closed — the template's `## Review` comment could revert to two members with the suite green, the template's `## Decisions` reason clause deleted green, and the emitted over-cap diagnostic had no assert for the new member (its fixture also lacked the section, so the assert would have been vacuous — M79).
- 2026-07-27: §8 certification round 2 (fresh reader, not round 1's) confirmed 15 of 16 round-1 items closed and independently reproduced all 119 ledger rows plus a 7,002-case differential check that the work-log extractor refactor is behaviour-preserving; it returned 4 blocking and 6 cosmetic items, all resolved this pass.
- 2026-07-27: the rulebook's own definitional line for the cap still read "less the `## Work log`" — the one two-member statement the T5 sweep missed, and the line the stated-vs-enforced cap regex reads. Widened.
- 2026-07-27: the ledger and the hook comment both claimed one milestone "has never had a `## Review`". False: M105 carries the heading in 6 of its 7 revisions with an empty body, so n=118 counts milestones with CONTENT in that section. Corrected at both sites; a by-hand check of my own contradicted the reader first and was wrong (a zsh quoting bug swallowed the path), which is the case for the fresh reader in one line.
- 2026-07-27: the ledger declared a lower-rank percentile convention but computed its medians by averaging, which showed up only in the one even-n row (`## Review` 2,346 vs 2,340). Convention extended to medians and the cell corrected.
- 2026-07-27: the `INDEX.md` line still carried the pre-correction corpus (119 paths / 3 paths) after the ledger itself was fixed to 119 milestones over 122 paths; corrected. Also fixed: the ledger's surplus attribution (M02/M03/M94 hold two paths each, not M01-M03), two `_plan_owned_scan`/breakdown docstrings under-describing the widened exempt set, and a fourth present-tense `decisions format` claim in a test docstring.
- 2026-07-27: §8 certification round 3, scoped to round 2's remediation commit only so the gate converges rather than treadmilling (M114 ran four rounds; D-069 puts each round's own report outside scope). It reproduced all six section statistics under the newly stated lower-rank convention and all 438 registry anchors, and returned 1 blocking + 1 cosmetic.
- 2026-07-27: the blocking one — the cap bullet's DEFINITIONAL line, widened in round 2, was pinned by nothing: reverting it to "less the `## Work log`" left all 677 skills tests green while the guarded sentence one line below said three. Now pinned and registered; verified by inversion that the two-member form reds it, and the anchor occurs exactly once.
- 2026-07-27: M118's own file crossed the cap under the PRE-M118 counter at `68434d7` — 151 plan-owned lines against 98 under the shipped counter — making it the fourth milestone ever to do so, on `## Decisions` and `## Work log` lines alone. That is the milestone's own thesis demonstrated on itself; the ledger and the `INDEX.md` line now pin their counts to `6733b8e` rather than reading as standing facts.
- 2026-07-27: correction to two round-2 log lines above (their subject is a certification round, so D-069 puts them outside the certified scope; corrected by appending, never edited): M105 carries `## Review` in all SIX of its content revisions, the seventh commit being the archival deletion; and the stated-vs-enforced cap regex reads the bullet's line 109, not the line 110 that was widened.
- 2026-07-27: three §8 rounds for this milestone, findings 16 -> 10 -> 2 — recorded as data for §8's own falsifier, which retires the step if guard-authoring milestones keep averaging multiple returns.
- 2026-07-27: T5 minor amendment (discovered sub-task) — M99's two `## Decisions` reserve guards in `test_budget_first_drafting.py` rest on the ground D-074 removes, so the cap-fit sum drops the phantom 21-line reserve term and the reserve-wording assert is re-anchored on the exemption while keeping the spend-none instruction; the new anchor is registered. AC5 did not enumerate these because they are budget guards, not exempt-set enumerations.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

- 2026-07-27 (RR08 Q1/Q2): classification UPHELD — the section is history. Forward
  grounds: entries are dated dispositions, the section is DECISIONS.md's declared local
  shard, and M83-D3 is the corpus's one live correction, handled by supersession. D-074's
  "self-defeating" clause is a coherence check that cannot pick the horn — not load-bearing.
- 2026-07-27 (RR08 Q3): the ownership route (exempt as differently-owned, no IP4
  extension) is real but REJECTED as the route — it leaves the record class undecided,
  re-creating the gap D-045 exists to close. Kept as supporting context only (rec 6).
- 2026-07-27 (RR08 Q4): cost-if-wrong is an acceptable OUTCOME, not a tolerated tax —
  the plan-time harvest surface does not reach a live milestone's section, and the
  D-066/D-067 post-mortems depended on exactly the unedited trail.
- 2026-07-27 (RR08 Q5): AC5's transplanted one-line grammar was a real plan defect —
  all 13 M114 entries wrap, so it would WARN permanently on the files the exemption
  serves. Redefined against the section's own genre; D-075 narrows D-074 part 3.
- 2026-07-27 (RR08 recs 7-8, REJECTED with reasons in the RR): the third-option route,
  and any "current knowledge with restrictions" hedge, which D-045's taxonomy lacks.
- 2026-07-27 (AC5 reading, raised by the §8 certification): AC5's operative clause is
  "every site *enumerating* the cap-exempt set names all three members ... No two-member
  set survives"; the colon-list that follows names the sites to touch, not sites that must
  each carry the full set. Three of the six enumerate nothing on their own (the
  cap-remedies bullet names a count, the always-read table row names none, the template
  preamble names one member), so under the alternative reading AC5 could not be satisfied
  by any edit short of restating the whole set six times. The full three-members-with-
  reasons statement lives once, in the weight-caps bullet, per the rulebook's own step-0
  single-home rule; every other site is consistent with it and none names a pair. Review
  may reject this reading — the criterion is plan-owned and unamended.
- 2026-07-27 (AC3 reading, raised by the §8 certification): "no prose here does" scopes
  plan-owned prose, not the append-only work log. The gate line at 2026-07-27 records the
  measurement that justified a gate choice, which is what the falsifying-ground discipline
  requires of it; its work-log p90 of 4107 is superseded by the ledger's 4228, the drift
  caused by this milestone's own work log growing inside the corpus it measures. History
  is not edited (IP4), so the reconciliation is an appended work-log line.
- 2026-07-27 (departure from D-074, raised by the §8 certification): D-074 part 2 says the
  set "becomes three members carrying three distinct reasons". The shipped prose says TWO
  grounds — review-ownership, and the un-editability that the work log and the decisions
  section share — because the two history members reach the same IP4 ground by their own
  classifications, and writing three would invent a distinction the entry's own reasoning
  does not carry ("for D-046's reason and not D-030's"). Each member still states its own
  reason, which is what AC5 requires. Recorded as a departure rather than silently taken.
- 2026-07-27 (AC6 clause 1, raised by the §8 certification): "this file's own `## Decisions`
  holds only dated decision entries" has no assert and no task of its own, because RR08's
  intended checker for it was BC3's advisory, which departed to M119. It is therefore
  inspection-only at this gate, and the inspection passes: every entry in this section
  opens `- 2026-07-27 (…)`, and the only non-entry line is the template's own
  `<!-- owner: … -->` comment, which RR08 §BC3 names as a standard corpus form.
- 2026-07-27 (RR08 ingest gate): BC1-BC4 carried BY REFERENCE under the Deviations
  table — verbatim measured ~150 plan-owned lines and would red `weight caps` at this
  gate, the D-066 choice-4 case. Four ambiguities the criteria-audit surfaced were bound
  at the gate, each recorded as a Deviations row.

## Review
<!-- owner: review · exclusive -->

Verified 2026-07-27 at `198e325` on `m118-decisions-cap-exempt`, PR #118.
`origin/main` had not moved since the branch was cut, so no merge was needed and
all evidence below is current.

### Acceptance-criteria evidence

- **AC1 — PASS.** `milestone_body_line_count` exempts an exact `## Decisions`
  section. Shared constant confirmed by reading: `EXEMPT_HEADINGS =
  (WORKLOG_HEADING, DECISIONS_HEADING)` (`cairn_scripts.py:105`), consumed at
  `:399`, and both counters run through the one `_plan_owned_scan`, so the fence
  rules are literally the work log's. All four required fixture shapes present
  and green in `TestMilestoneBodyLineCount` (16 tests): exact
  (`test_decisions_section_is_exempt`), fenced
  (`test_fenced_decisions_heading_is_not_the_section`), prefixed
  (`test_decisions_prefixed_heading_is_still_counted`), absent
  (`test_absent_decisions_section_counts_as_before`), plus
  `test_both_history_sections_are_exempt_together` pinning that the third member
  did not cost the work log its exemption.
- **AC2 — PASS.** `TestMilestoneSectionLineCounts` green (12 tests):
  `test_decisions_excluded_from_the_breakdown` omits it,
  `test_decisions_prefixed_heading_stays_in_the_breakdown` keeps trimmable
  content nameable, and `test_preamble_plus_sections_still_sum_to_body_with_both_exemptions`
  holds the invariant across all three exempt members. The "no over-cap
  diagnostic names a section IP4 forbids editing" clause is verified against the
  *emitted* diagnostic, not only the function:
  `test_over_cap_shows_heaviest_first_breakdown` asserts `Decisions` is absent
  from `cairn_validate`'s printed breakdown, and its fixture carries a
  `## Decisions` section so the assertion is not vacuous. Noted, not counted
  against the criterion: AC2's parenthetical locator `cairn_scripts.py:436-441`
  is a plan-time line number that has since moved (the invariant's docstring is
  now at `:469-475`); the substance it points at is what was verified.
- **AC3 — PASS.** `cairn/references/m118-cap-exemption-ledger.md` is committed
  (257 lines, 119 milestone rows) with its `INDEX.md` line. Re-derived
  independently at review time rather than read from the page: 119 milestones
  over 122 paths; milestones whose pre-M118 peak reached the 150 cap and their
  post-M118 peaks — M114 166→123, M98 165→123, M79 154→125, M118 151→125; none
  remains at or over the cap; largest post-M118 peak anywhere 129 (M43). The
  ledger's own summary states three rather than four because it is pinned to
  `6733b8e`; M118 crossed the cap later on its own branch, which the page
  discloses in its Summary prose and its third evidence-snapshot bullet. Both
  readings are true of their stated commits and the criterion's substance —
  every over-cap milestone falls below — holds at each.
- **AC4 — PASS.** `CAP_EXEMPT_SECTIONS = ("work log", "decisions", "review")`
  (`session_context.py:74`). `TestSessionContextReadBound` green (18 tests):
  `test_the_decisions_section_is_bounded_by_the_same_rule` pins newest-first in
  both directions (newest entry present, oldest absent),
  `test_bounded_decisions_section_names_what_it_elided` pins the omission notice
  and the read-the-file pointer, and `test_a_decisions_prefixed_heading_is_not_bounded`
  is the non-vacuous control. `SECTION_MAX_CHARS`'s comment is re-derived over
  all three section types from the fresh 119-milestone measurement and cites the
  ledger rather than carrying a second copy of the numbers.
- **AC5 — PASS.** Swept `skills/`, `scripts/`, `hooks/` at review time for
  surviving two-member enumerations; every candidate the sweep surfaced was
  inspected and is either a three-member statement its window had cut short
  (`cairn_scripts.py:92-98`, `:330-332`) or prose deliberately scoped to one
  section (`test_hooks.py:403`). No two-member set survives. The three-member
  statements as shipped: `tracking-rules.md:110` (the cap's definitional line),
  `:111` (the set with each member's reason), `:132` (the remedy), `:186` (the
  always-read frame); `templates/milestone.md:86` and `:92-93`. Each is pinned
  by an assert registered in the mutation harness.
- **AC6 (BC4) — PASS.** Parsed this file's own `## Decisions` through the
  milestone's own `milestone_decisions_lines` extractor: 10 dated entries, 38
  wrapped continuations of those entries, 2 template ownership-comment lines, 0
  other content. The AC3 ledger landed as a committed file, never in this
  section. BC4's second evidence half — "the advisory of BC3 reporting no WARN
  on M118 itself" — is unavailable at this gate by design: BC3 departs to M119
  under the Deviations table, so it is M119's to satisfy against this file.
- **AC7 — PASS.** Profile `verify` slot, run fresh: `skills/tests` 677 OK ·
  `scripts/tests` 298 OK · `hooks/tests` 94 OK. `cairn_validate` exit 0 — 16
  checks PASS, 7 advisories OK.

### Consistency gate

- `cairn_validate.py` exit 0; 16 checks PASS, 7 advisories OK. No `scaffold
  present` or `coverage complete` failure.
- No `DESIGN.md` principle (IPn/GPn) changed, so `cairn_impact --changed` is
  not applicable. IP4 is *touched* in reach but unchanged in wording, per D-074.
- Toolchain checks: the `generic` profile's `consistency-gate` slot names none,
  so this half is a clean no-op. This repo has no CI — `gh pr checks` reports
  none, and the profile says to treat a PR as mergeable on local green.
- Projection-vs-outcome (Driving RR: RR08): no numeric projection from RR08
  binds this milestone. BC3 is the only criterion carrying numeric tolerances
  (0 WARNs / ≥1 WARN) and it departs to M119; BC4, the one criterion bound
  here, is non-numeric. The step no-ops cleanly.
- Thrash count: one prior return on this milestone (the M118/M119 split at the
  maintainer's call after the sizing advisory reported 11 criteria). Below
  trigger (a)'s threshold of three, and no criterion has failed twice, so
  trigger (b) is unmet.
