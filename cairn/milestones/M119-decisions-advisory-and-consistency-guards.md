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
- [ ] T2: Add the section to the rulebook's history-member enumeration
      (`tracking-rules.md:205-207`) and pin the amended sentence under the
      file's existing mutation-registration rules; verify the pin reds when the
      member is removed.
- [ ] T3: Mirror the exempt-set constant across `cairn_scripts` and
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
- 2026-07-27: measured at the gate that density is not a usable signal — M84's section is a character survey and M98's a line-number inventory, so a numeric heuristic fires hardest on the files the exemption exists to serve; detector keys on shape only.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive -->
