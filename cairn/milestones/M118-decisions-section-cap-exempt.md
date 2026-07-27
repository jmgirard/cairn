<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. Drafting budgets: see the template. -->
# M118: The milestone-local `## Decisions` section joins the cap-exempt set

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** RR08
- **Principles touched:** IP4
- **Branch/PR:** `m118-decisions-cap-exempt`

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

- [ ] AC1: `milestone_body_line_count` excludes an exact `## Decisions` section,
      matched by the same shared constant and fence rules the work-log exemption
      uses; a fenced `## Decisions` and `## Decisions notes` both stay counted.
      Fixtures: exact, fenced, prefixed, absent.
- [ ] AC2: `milestone_section_line_counts` omits it from the heaviest-first
      breakdown, so no over-cap diagnostic names a section IP4 forbids editing,
      and `preamble + sections == body` (`cairn_scripts.py:436-441`) still holds.
- [ ] AC3: A committed ledger re-measures every milestone file's **peak
      plan-owned revision** under both counters; every file whose peak exceeded
      the cap falls below it. It carries the numbers; no prose here does (M99).
- [ ] AC4: `hooks/session_context.py` read-bounds `## Decisions` per D-063, and
      `SECTION_MAX_CHARS`'s justifying comment is re-derived over all three
      section types from fresh measurement, not left asserting a p90 over two.
      Test: newest-first injection plus the omission notice.
- [ ] AC5: Every site enumerating the cap-exempt set names all three members and
      each member's stated reason: the rulebook's weight-caps and cap-remedies
      bullets and its always-read frame row and prose (`:184-186`); the
      template's budget preamble and its `## Decisions` / `## Review` comments;
      and `test_milestone_cap_exemption.py:62`, whose set-membership assert is
      anchored on the whole set and is re-anchored, never appended to. No
      two-member set survives.
- [ ] AC6 (BC4): RR08 §BC4 — this file's own `## Decisions` holds only dated
      decision entries; the AC3 ledger lands as a committed file.
- [ ] AC7: All three suites clean (the profile's `verify` slot), `cairn_validate` green.

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
- [ ] T3: Peak-revision ledger over `git log --all`, run under both counters,
      committed as its own file (never into `## Decisions` — BC4).
- [ ] T4: Add `"decisions"` to `CAP_EXEMPT_SECTIONS` (`session_context.py:56`);
      re-measure p90 over all three section types and re-derive
      `SECTION_MAX_CHARS`'s comment. Hook test per AC4.
- [ ] T5: Re-anchor the set-membership guard and update AC5's prose sites;
      re-register the anchor and verify by mutation that deleting the
      three-member sentence reds it.
- [ ] T6: Full `verify` + `cairn_validate`; post-merge hygiene.

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
- 2026-07-27 (RR08 ingest gate): BC1-BC4 carried BY REFERENCE under the Deviations
  table — verbatim measured ~150 plan-owned lines and would red `weight caps` at this
  gate, the D-066 choice-4 case. Four ambiguities the criteria-audit surfaced were bound
  at the gate, each recorded as a Deviations row.

## Review
<!-- owner: review · exclusive -->
