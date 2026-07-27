<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. Drafting budgets: see the template. -->
# M119: RR08's follow-ons — the decisions-format advisory, the history enumeration, and a two-sided exempt-set guard

- **Status:** review
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
- [x] T4: Full `verify` + `cairn_validate` (post-merge hygiene is review-phase
      by construction — minor amendment, M119 §8 round 6).

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
- 2026-07-27: §8 round 3 (third fresh-context [O]): 3 defects + 5 record errors, and rounds 2 and 3 were the same class — every fixture written for the adjacency chunker was the convenient shape. Round 3 broke round 2's own fixtures: the common `assertEqual` failure splits on its banner, a two-hunk diff splits on its changed lines, this commit's own diff gives 3 findings, and the `>` rendering splits because the quote pattern eats the diff context line's indentation.
- 2026-07-27: mini gate (amendment) — the maintainer chose to REMOVE the run-boundary logic rather than tune it. Shipped: a fenced block keeps its own finding and its own range (delimiters are read, never inferred); all loose output in a section collapses to one finding anchored at its first signature line with the rest counted. `_DECISIONS_PROSE`, `_DECISIONS_FILLER` and `_DECISIONS_GAP` are gone, and with them six of round 3's eight findings. Departure from the implement gate's "one per chunk": two loose pastes in one section now report once — disclosed in the code, and pinned by a test rather than left implicit. No acceptance criterion moves; AC1 and AC2 are satisfied either way.
- 2026-07-27: the four paste shapes three rounds surfaced are kept as a fixture table (`PASTE_SHAPES`) at the raggedness an author actually pastes — passing run, `assertEqual` failure, two-hunk markdown diff, transcript astride a paragraph — so the removal's payoff is what reds if boundary inference ever returns.
- 2026-07-27: §8 round 4 (fourth fresh-context [O]): 3 defects + 4 record errors, all fixed. The defects were coverage the round-3 removal dropped or never had — the loose finding's anchor line survived being moved to the last signature line and to `first + 7` with the class green, the fenced range survived losing its closing delimiter, `PASTE_SHAPES` passed in 8ms when emptied, and the loose finding was emitted after every fenced one regardless of line order. All five now red under by-hand mutation.
- 2026-07-27: correction (supersedes this session's T1 line, IP4 — appended, not edited): `_pasted_runs` no longer exists. The shipped functions are `_pasted_findings` and `_span`; the round-3 removal named what it deleted but not what replaced it.
- 2026-07-27: correction (supersedes this session's round-3 table line, IP4): three of `PASTE_SHAPES`' four shapes came from rounds 1-3, not all four — the fourth ("transcript astride a paragraph of prose") was the removed chunker's own gap fixture and is kept because it pins the disclosed two-loose-pastes collapse. The `>`-quoted shape round 3 surfaced is pinned by its own test, not by the table. Also corrected in this round: the removal note's three examples were {round 2, round 3, round 3} with round 1's shape missing, and "nothing infers an extent" is false of an unterminated fence — the one place an extent still is inferred, now stated and covered by a test.
- 2026-07-27: §8 round 5 — **no code defects and no regressions**, 2 record errors ("the note above the signature table" is below it; the `>`-quoted shape round 3 surfaced was a quoted DIFF, which the marker sweep never reached). Both fixed, the second by adding the quoted-diff case rather than narrowing the wording.
- 2026-07-27: round 5's three out-of-scope observations were taken rather than banked — they were coverage gaps in this milestone's own deliverable. Six of the ten signatures deleted green because the shape tests assert `len == 1`, which any one matching line satisfies; `~~~` support, column-0 fences and prefix-closing all deleted green too. Now: every signature fires on its own with a prose negative control, both delimiters and an indented opener covered, and fence closing pinned on its ENDPOINT — `len == 1` plus a `\d+-\d+` range left equality-closing green, because an unclosed fence also reports one ranged finding.
- 2026-07-27: the quoted-fence miss is documented rather than fixed: fence detection reads the raw line, so a quoted ``` is not a delimiter and the block reports as loose output — a change of kind, never silence. Widening it would make a fence's extent depend on quoting depth, which is more inference than the round-3 removal left standing. Pinned by a test so the comment cannot drift from what ships.
- 2026-07-27: T4 / AC5 evidence — `python3 -m unittest discover` green on all three suites (skills 680, scripts 328, hooks 98) and `python3 scripts/cairn_validate.py .` reports all checks passed with `OK    decisions format`, run at 2026-07-27 on `a288d8f` + round-6 fixes.
- 2026-07-27: T4 minor amendment — its second clause named post-merge hygiene, which cannot run before review by construction, so five §8 rounds passed an unticked task. Task text narrowed to the pre-review half; hygiene stays review's.
- 2026-07-27: §8 round 6 — **no code defects and no regressions**, 4 record errors + 4 pre-existing coverage gaps, all closed. The records: "a change of kind, never silence" was false for a quoted fence whose body carries no signature (measured: unquoted reports, quoted reports nothing) and the shipped test used the one fixture that made the claim look true; "six of the ten signatures" is seven; "two cases equality gets wrong" was one, the info-string case pinning a different rule; "one line per signature" over twelve lines for ten.
- 2026-07-27: round 6's four gaps closed — `_span`'s single-line arm (reachable via a fence opening on the section's last line), the 60-char preview truncation, the message's section name, and both `kind` labels, all of which deleted or mutated green. The preview assert takes a FIXED bound with the constant pinned separately, because deriving it from the constant under test let raising the constant pass (guard-doctrine §6).
- 2026-07-27: §8 round 7 — **no record errors**, 2 coverage gaps. Both were one-directional pins: the line-order test's fixture had the loose line first, so a sort key hard-coded to 0 sorted correctly and survived; and the unterminated fence is a third emission site round 6's whole-message test never reached, so `"fenced blockk"` survived there. Fixed with a both-orders fixture and a whole-message assert.
- 2026-07-27: round 7's alternation survivors closed too — narrowing `PASS|FAIL|WARN|OK` to `PASS`, dropping the singular from `Ran N test(s)`, and widening `Traceback` past its anchor all survived. `SIGNATURE_LINES` gained the branches, and a `NEAR_MISS_LINES` control now holds the patterns from being widened into the permanent WARN D-075 exists to prevent.
- 2026-07-27: the near-miss control found a live false positive in the shipped detector — `^diff --git ` matched prose opening with those words. Tightened to `^diff --git a/`, git's actual path prefix. Every AC5 suite re-run green after the change.
- 2026-07-27: §8 round 8 — **0 shipped-behaviour defects, 0 regressions**; 3 record errors + 2 coverage gaps, all closed. The records: the near-miss control's own comment named a widening (`Traceback`'s `$`) that no entry could reach; "one character away" measured true of 1 of 5 entries; and "git's actual path prefix" overstated `a/`, which `--no-prefix`, `--src-prefix`, `diff.mnemonicPrefix` and C-quoted paths all miss. Each entry now names the widening it holds against, a sixth reaches the `$`, and the signature comment states the trade — a header-only paste in those forms is lost, any diff with a hunk header still fires on `^@@ .* @@`.
- 2026-07-27: round 8's two gaps were both boundary arms an over-limit fixture leaves free — the preview comparison (`>` → `>=` survived, since a 61-char truncated preview satisfies "ends in … and is ≤ 61") and the fence preview's `and stripped` clause (no fixture opened a fence on a blank line). One fixture at exactly the limit and one blank-opened fence red both.
- 2026-07-27: §8 round 9 — 0 shipped-behaviour defects, 0 regressions, 74 mutations run. Two record errors (a "note below this table" that is above it — the same inversion round 5 fixed, re-introduced; and the near-miss control's stated function overclaiming for signatures it did not cover) and one real gap: `NEAR_MISS_LINES` covered 5 of the 10 signatures, and five widenings survived, the sharpest being `--- a/|+++ b/` → `---|+++`, which claims an ordinary markdown thematic break and so WARNs forever. The set now covers all ten; each widening reds under by-hand mutation.
- 2026-07-27: **§8 loop stopped at round 9, not converged.** Rounds 5-9 found zero shipped-behaviour defects apart from round 7's live `^diff --git ` false positive; what repeated was a false claim in the previous round's own fix comment — round 9's two findings sit in round 8's text. The thrash rule could not fire: it counts review returns (`/milestone-review`, D-064) and this milestone has had none, so nine implement-phase rounds ran with the counter at zero. Recorded as a candidate row; the disposition (retire §8 per its own falsifier, or extend the counter to implement-phase loops) is the maintainer's and needs a D-entry either way.
- 2026-07-27: measured at the gate that density is not a usable signal — M84's section is a character survey and M98's a line-number inventory, so a numeric heuristic fires hardest on the files the exemption exists to serve; detector keys on shape only.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive -->
