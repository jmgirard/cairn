# M141: README plain-language pass

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** `m141-readme-plain-language`

## Goal

README.md reads as plain prose — the em-dash tic and machine-styled
constructions removed — with its commands, guarded claims, and section
structure intact.

## Scope

**In:** a style rewrite of README.md's prose, structure kept; guard and
registration retargets under `skills/tests/` where a pinned claim's wording
changes; one bounded fresh-reader style check (milestone-local; the plan
gate ruled it outside D-095's retirement).

**Out:**
- The Substantive-bullet re-pin → stays a candidate on its own promotion
  condition (gate declined planning it now).
- Any standing style instrument, lint rule, or repeat reader round → D-095;
  the reader runs exactly once, inside this milestone.
- Every other doc (DESIGN, CHANGELOG, skill prose) → untouched; README only.
- The fenced command blocks → frozen byte-for-byte (AC3).

## Acceptance criteria

- [ ] AC1. `grep -o '—' README.md | wc -l` reports at most 10 at the review
      commit, down from 50 measured at edb6942 (2026-08-14), and
      `grep -oE ' (--|–) ' README.md | wc -l` reports 0.
- [ ] AC2. `grep -c '' README.md` reports at most 265 at the review commit
      (the edb6942 baseline).
- [ ] AC3. The fenced-block list of README.md at the review commit equals the
      list at edb6942 element-wise — same length, same order, each element
      byte-identical — where a block is the fence's info string plus the
      lines strictly between it and its closing fence, blocks extracted top
      to bottom by the same procedure from both revisions.
- [ ] AC4. The README-pinning guards hold: `test_readme_currency.py`,
      `test_positioning_guard.py`, `test_collaboration_boundary.py` and
      `test_mutation_harness.py` pass at the review commit, and that file
      still carries at least 19 `target="README.md"` registrations.
      `git diff -w main...HEAD -- skills/tests/` is either empty or, for
      each changed assert or registration, a `## Review` line names either
      the reworded README claim it tracks or — for a structural anchor such
      as a paragraph index — the claim whose location moved; a guard is
      retargeted, never deleted or weakened to bare presence.
- [ ] AC5. One fresh-context reader that authored none of the rewrite reads
      README.md as of a named branch commit and reports each construction it
      judges machine-styled; the enumeration is the reader's. Each reported
      item is either rewritten or kept with a one-line reason. Exactly one
      such pass is run — this is a milestone-local reading, not a doctrine
      step, and no guard, rulebook rule or repeat round is added by it.
      Evidence in `## Review`: the commit read, the report count, the
      rewritten count, and each kept-with-reason line.
- [ ] AC6. `python3 -m unittest discover -s skills/tests`,
      `python3 -m unittest discover -s scripts/tests`,
      `python3 -m unittest discover -s hooks/tests` and
      `python3 scripts/cairn_validate.py` are green at the review commit.
      Evidence: one Review line per command with the commit and reported
      counts.
- [ ] AC7. `grep -n '^## ' README.md` at the review commit lists the same 10
      section headings, in the same order, as at edb6942 (verified
      2026-08-14), and `grep -c ''` reports at least 230.

## Coverage

- AC1 → T2, T4
- AC2 → T2, T4
- AC3 → T2, T4
- AC4 → T1, T2, T4
- AC5 → T3
- AC6 → T4
- AC7 → T2, T4

## Tasks

- [x] T1. Map the guard anchors: extract every pinned README literal from
      the three reader guard files and the 19 harness registrations, with
      file:line, so the rewrite knows what survives byte-for-byte and what
      needs a same-commit retarget (M104). Note
      `test_positioning_guard.py`'s positional ¶-index anchor.
- [x] T2. The rewrite: section-by-section prose pass, structure and fenced
      blocks frozen (AC3, AC7), pinned phrases kept contiguous or guards
      retargeted in the same commit; count AC1/AC2 while writing, never at
      the gate.
- [x] T3. The one-pass style reader ([O], fresh context) at a named branch
      commit; disposition every report; record the tallies.
- [ ] T4. Measurements per criterion command, three suites and validate;
      Review-line evidence.

## Work log

- 2026-08-14: T3 — one-pass style reader ([O], fresh context) read the README at ad7f827 and reported 48 constructions (8 on test-pinned phrases); disposition: 19 rewritten on the branch (including the buildup before the merge ask, the 'final outward step' vagueness, the 'live means live' tautology, four 'not X' reversal tails, the duplicated trail flourish), 29 kept with reasons to be recorded per item in the Review section. Exactly one pass, per AC5; no second round convened.
- 2026-08-14: T1 — anchor map: 19 harness registrations (all single-line literals, verified present), the currency guard's one-physical-line phrases, the positioning guard's normalized ¶-index-2 anchor plus four profile labels, the collaboration guard's three lowercase phrases. T2 — full rewrite: em dashes 50 -> 1 (the frozen tree block's), companion count 0, 265 lines, blocks and headings element-wise equal to edb6942, every pinned phrase kept contiguous (two ¶1 wraps caught by the suite and re-wrapped); three suites and validate exit 0, `git diff -w main...HEAD -- skills/tests/` empty — no retarget needed.
- 2026-08-14: created by /milestone-plan; absorbs the README-cleanup candidate row (conversational, maintainer, 2026-08-14).
- 2026-08-14: criteria audit ran ([O], fresh context, authored none of the wording): AC1/AC2/AC6 clear (AC1 gained the auditor's `--`/`–` companion check; AC6 names its runners verbatim); AC3 reworded to element-wise fenced-block list equality with info strings (duplicate/info-string/new-block holes); AC4 reworded to name its four guard files, floor the 19 registrations, and carry a lane for the positional ¶-anchor; AC5 bounded to exactly one pass; AC7 added on the auditor's own wording (heading freeze + 230-line floor) closing the gutted-README hole. Premise corrected: `test_toolchain_profiles.py` never reads README.
- 2026-08-14: plan gate (maintainer): the one-pass reader ruled outside D-095's retirement — that entry retired a standing, looping certification step; this is one bounded milestone-local read. Falsified by the pass convening a second round or surviving into another milestone, which re-opens D-095's question.
- 2026-08-14: plan gate chose the ≤10 em-dash target over ≤5 and ≤20 — kills the tic, keeps genuinely-right uses; falsified by the shipped README still reading machine-styled at the merge gate with the target met.
- 2026-08-14: plan gate declined planning the Substantive re-pin now: its row's promotion condition (a milestone editing step 6, or a silent-edit incident) has not fired.
- 2026-08-14: plan chose script-measurable bars plus one bounded judgment pass over judgment alone or metrics alone, because "reads naturally" is unmeasurable and metrics alone are gameable by a gutted file (the auditor's AC7 finding); falsified by the reader pass reporting nothing while the maintainer still flags constructions at the merge gate.

## Decisions

## Review
