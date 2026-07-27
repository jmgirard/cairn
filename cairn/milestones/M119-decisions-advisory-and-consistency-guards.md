<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. Drafting budgets: see the template. -->
# M119: RR08's follow-ons — the decisions-format advisory, the history enumeration, and a two-sided exempt-set guard

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** M118
- **Driving RR:** RR08
- **Principles touched:** IP4
- **Branch/PR:** `m119-decisions-advisory-and-consistency-guards`

## Goal

Ship RR08's three remaining binding criteria: the counterweight advisory for the
now-unbudgeted `## Decisions` section, the rulebook's history-class member
enumeration, and a test that reds when the hook and the cap counters disagree
about the exempt set.

## Scope

**In:** `check_decisions_format` and its registration; the history-member
enumeration in the rulebook's "Correcting a record proven false" bullet and its
pin; the mirrored exempt-set constant and its two-sided consistency test.

**Out:** the cap exemption itself, the hook read-bound, the exempt-set
enumeration sites and the peak-revision ledger → **M118** (this milestone
depends on it and cannot start before it merges); redistributing the template's
freed drafting budget → candidate row; changing the advisory's severity from
WARN → not proposed (D-046's severity reasoning stands, D-075).

## Acceptance criteria

- [ ] AC1: A `decisions format` advisory WARNs, exit-code neutral, on pasted
      output or a fenced transcript block in a milestone-local `## Decisions`
      section — the section's own genre, never the work log's one-line grammar
      (D-075) — reading the section through the shared extractor M118 adds, so
      the section the cap stops measuring is the section the advisory polices.
- [ ] AC2 (BC3): RR08 §BC3 — the shipped advisory emits exactly 0 WARNs over
      the whole `## Decisions` sections of M83, M84, M94, M98 and M114 as
      fixtures, and >=1 on a constructed pasted-output fixture.
- [ ] AC3 (BC1): RR08 §BC1 — the rulebook's history-member enumeration names
      this section, pinned per the file's mutation rules.
- [ ] AC4 (BC2): RR08 §BC2 — a test reds whenever the hook's
      `CAP_EXEMPT_SECTIONS` and the counters' effective exempt set disagree
      either way, via mirrored constants read from each side (the hook imports
      only `cairn_common`, so no shared constant is reachable).
- [ ] AC5: All three suites clean (the profile's `verify` slot), `cairn_validate` green.

**Deviations from RR08.** BC1-BC3 are carried **by reference** to the archived
RR rather than verbatim, per the D-066 choice-4 decision taken at the RR08
ingest gate and inherited by this split. BC4 departs: it constrains M118's own
file and its ledger, and is delivered there.

| BC | Departure | Reason |
|---|---|---|
| BC1 | by reference | cap discipline inherited from the RR08 ingest gate |
| BC2 | by reference; "shared constant" resolved to *mirrored* | hooks import only `cairn_common` |
| BC3 | by reference; 0-WARN arm bound to whole sections, detector scoped to pasted output / fenced blocks | BC3 left both open; bound at the ingest gate |
| BC4 | not in this milestone | constrains M118's own file and ledger → delivered by M118 |

## Coverage

- AC1 -> T1
- AC2 -> T1
- AC3 -> T2
- AC4 -> T3
- AC5 -> T4

## Tasks

- [x] T1: Add `check_decisions_format` beside `check_worklog_format`
      (`cairn_validate.py:1321`) and register it in `ADVISORIES` (`:1590`);
      detector is pasted-output/fenced-block shaped. Fixtures: the five corpus
      sections via ref-based `git show` at 0 WARNs, a pasted-output fixture at
      >=1, exit 0 throughout.
- [x] T2: Add the section to the rulebook's history-member enumeration
      (`tracking-rules.md:205-207`) and pin the amended sentence under the
      file's existing mutation-registration rules; verify the pin reds when the
      member is removed.
- [x] T3: Mirror the exempt-set constant across `cairn_scripts` and
      `hooks/session_context.py`; two-sided consistency test with a by-hand
      one-sided-removal red check. Note `## Review` is excluded by the body
      boundary, not by set membership — the test compares effective sets.
- [ ] T4: Full `verify` + `cairn_validate`; post-merge hygiene.

## Work log

- 2026-07-27: created by /milestone-plan, splitting M118 at the maintainer's call after `cairn_validate`'s sizing advisory reported 11 acceptance criteria against the >7 tripwire.
- 2026-07-27: split boundary chose core-vs-followons over splitting by surface (scripts / hooks / rulebook), because the follow-ons all depend on the shared extractor and exempt set M118 introduces while the core does not depend on any of them, so this cut is the only one that leaves the first milestone shippable alone; falsified by a follow-on turning out to need no M118 artifact, which would mean the two could have run in parallel.
- 2026-07-27: both files declare `Driving RR: RR08` and enumerate all four binding criteria, because `check_binding_criteria` holds every milestone naming an RR to that RR's whole criteria set — a split that let each file list only its own share would red the check on the absent ones.
- 2026-07-27: D-075's "Delivered by M118" now reads as this pair; the entry is history (IP4) and is not edited — the split is recorded here and in M118's work log instead.
- 2026-07-27: implement question gate — detector covers fenced blocks AND unfenced machine-output signatures (AC1's two arms, not D-075's narrower fenced-only fallback); corpus read from git history at the five archiving commits rather than copied into fixtures; one WARN per pasted chunk, not per line.
- 2026-07-27: T1 — `check_decisions_format` + `_pasted_runs` shipped and registered as `decisions format`, adjacent to `work-log format`; 12 tests including the five-section corpus at 0 WARNs with per-file non-vacuity asserts and a same-path positive control. Three by-hand mutations (signatures off, fences off, quote-normalization off) each redden the right tests.
- 2026-07-27: T2 — the history enumeration names the milestone-local `## Decisions` section; the pin is RE-ANCHORED whole (the pre-M119 six-member line satisfies nothing), and a second assert pins the wrap line, whose four members lost their incidental cover when `milestones/archive/` moved off line 1. Both registered in the mutation harness; a by-hand revert to the six-member list reds both.
- 2026-07-27: T2 minor amendment (discovered sub-task) — the rulebook also names the shipped advisory and its subject beside `work-log format`, and the always-read frame's attention-signal cell gains it; `cairn_scripts.py`'s forward reference to "M119 ships `decisions format`" is retired. Not enumerated in Scope, taken as part of "and its registration": an advisory the rulebook does not name leaves the repo contradicting itself, M118 F1's shape. Two new guards (subject, stated↔emitted label), both registered; three by-hand mutations red.
- 2026-07-27: T3 — `cairn_scripts.CAP_EXEMPT_SECTIONS` derives the counters' effective set from `EXEMPT_HEADINGS + (REVIEW_HEADING,)`, and `_plan_owned_scan`'s boundary now reads that constant instead of a literal; `hooks/session_context.py` declares itself the mirror. `TestExemptSetMirror` (4 tests) asserts set EQUALITY, non-vacuity, and — the arm a constant-only comparison misses — that the real scan exempts what the constant claims. Four by-hand mutations red: a member dropped from either side, a member added, and the counters silently abandoning the `## Review` boundary with both constants untouched.
- 2026-07-27: §8 certification (fresh-context [O], authored no part of this): 8 discrepancies, all fixed, zero unresolved. Two were defects, not wording — AC1's "reads through the shared extractor" clause was pinned by nothing, and `_pasted_runs` closed an unfenced run at the first non-signature line, so a realistic unittest paste (progress dots, `-----` rule, blank) reported as 3 findings against the one-per-chunk decision. Fixed by gap-tolerant runs closing on markdown prose, plus a fixture in the shape an author actually pastes.
- 2026-07-27: correction (supersedes this session's T2 line, IP4 — appended, not edited): the wrap line's members that lost incidental cover are TWO (`milestone IDs`, `milestones/archive/`), not four; `reviews/archive/` and entombed `legacy/` were already below the wrap pre-M119 and were never covered by any assert.
- 2026-07-27: six certification findings were record accuracy — "WARNs on every entry in the corpus" is false at three sites (measured: 117 WARNs, 23 of 24 entries wrap, one M84 review line does not); "the shared scan the cap counters exempt it by" conflated the extractor scan with `_plan_owned_scan` (only the heading constant is shared — M118's work-log twin carried the same error and is corrected in place); a registry comment said "above" of a precedent that is below; the blockquote comment enumerated four renderings for a regex that takes any; and two forward references still called the advisory unshipped, one of them in the template the new guard reads.
- 2026-07-27: §8 round 2 (second fresh-context [O], did not do round 1): 3 discrepancies + 3 minor, all fixed. The defect was round 1's own fix being fitted to the EASY shape — the passing unittest run — while the failure transcript actually pasted as evidence still split into three findings on its `======`/`FAIL:`/`-----` banner. `_pasted_runs` gained a filler class (rules, progress dots, indented frames, blanks) that neither closes a run nor advances the gap, and prose is now judged with its indentation so a diff's ` - context` line stops closing the diff it sits in. Four shapes now pinned: passing run, failure transcript, two-hunk diff, and prose closing a run at the gap.
- 2026-07-27: round 2's other fixes — the shared-scan claim corrected at its definition site (`_section_body_lines`), not just at the two extractors; the blockquote comment's rendering count removed rather than re-counted (the test is the record); D-077 written because D-075's "every entry" measurement is live in `DECISIONS.md` and the shipped code now contradicts it — D-076's shape exactly, and a milestone-local record would not reach a later reader.
- 2026-07-27: measured at the gate that density is not a usable signal — M84's section is a character survey and M98's a line-number inventory, so a numeric heuristic fires hardest on the files the exemption exists to serve; detector keys on shape only.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive -->
