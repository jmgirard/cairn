# M124: A section-consistency ledger, so a contradicted or renamed rule reds

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** —

## Goal

Give a doctrine section a guard that reds when a rule inside it is contradicted,
renamed, or relocated, deriving what it checks from the section's own text.

## Scope

**In:** a reusable section-consistency helper under `skills/tests/` that slices a
section by heading and returns its ordered, whitespace-normalized sentence
sequence; a committed ledger fixture holding that sequence for
`guard-doctrine.md` §8; a guard test failing on any difference and naming what
was added, removed, or moved; a new `guard-doctrine.md` §9 stating the
presence-vs-consistency rule and the instrument's detect-never-judge boundary;
mutation-harness registration; and replay evidence over the four mutations
M123's certification recorded. Absorbs the presence-not-consistency candidate
row (M123 §8 round 3 F2, extended at round 4 F3).

**Out:** applying the instrument to any section other than §8 → candidate row
(rollout), promotable once §8 has lived with it. Inferring contradiction from
extracted vocabulary or polarity → candidate row, promotable if the ledger
proves too coarse. Cross-file fork detection → stays with the parked
one-surface-pin row (D-065), a different class: that one is a rule forking
across files, this is contradiction within one. Any `cairn_validate` check →
not planned; D-067 rejects mechanizing either fresh-context reader, and this
stays a suite guard over section text. The five round-3 F2 mutations never
recorded verbatim → unrecoverable, not replayed.

## Acceptance criteria

- [ ] AC1 — `skills/tests/` contains a section-consistency helper that, given a
      file path and a section heading, returns that section's ordered,
      whitespace-normalized sentence sequence. Its extraction takes no list of
      terms, phrases, or subjects drawn from the section's content, as a
      parameter or as a module constant; a closed grammatical or punctuation
      class (abbreviation forms, sentence-boundary punctuation) is permitted,
      and each such constant carries a comment stating the class it closes over.
- [ ] AC2 — A committed ledger fixture records that sequence for
      `guard-doctrine.md` §8. A guard test compares the section against the
      ledger — the ledger is the extraction's committed output, compared
      downstream of it and never passed into the extraction — and fails when
      they differ, naming in its failure message which sentences were added,
      removed, or moved, the comparison being alignment-based so that a pure
      insertion reports as one addition rather than as a mass relocation.
- [ ] AC3 — Each of the four mutations recorded from M123's certification is
      applied to §8 in turn, fails the AC2 guard, and is restored
      byte-identical, with each result recorded in the milestone's evidence:
      (a) appending "A robustness observation outside them reopens a round on
      the same terms"; (b) relocating §8's three-checks list so that "the three
      named checks above" no longer follows it; (c) appending "Records
      predating round 1 are shielded on the same terms as fix-authored ones";
      (d) replacing "A fix-authored record is still read" with "A shielded
      entry is still read". The evidence states which of the four already fail
      the pre-milestone suite — (a) and (b) do not, (c) and (d) do — so (a) and
      (b) are the load-bearing replay and (c) and (d) are controls.
- [ ] AC4 — Re-wrapping every paragraph of §8 to a different column width with
      the token sequence unchanged — no break introduced inside a hyphenated
      compound — leaves the AC2 guard green; the evidence command is
      scoped to the AC2 guard rather than to the whole `skills/tests` suite, and
      §8 is restored byte-identical afterwards. Recorded as evidence.
- [ ] AC5 — `guard-doctrine.md` gains a new section appended after §8 as §9,
      with no existing section renumbered, stating that a prose guard pins a
      sentence's presence and not the section's consistency, naming the
      contradicting-sentence and the reusing-no-word rename as the two shapes
      that defeat presence pins, and stating that the instrument detects a
      change and never judges it. §8's two routing enumerations of `§§1–7` are
      updated to name §9 as well, and every pre-existing assert and registry
      block pinning either enumeration is re-anchored, so that at HEAD the
      enumeration names every craft section and the suite stays green.
- [ ] AC6 — Every rule AC5 adds is pinned by an assert that fails when that rule
      is inverted in place; each such assert and the AC2 ledger guard are
      registered in `skills/tests/test_mutation_harness.py`, and every block
      this milestone registers fails when blanked.
- [ ] AC7 — The `verify` slot is clean and the universal cairn-file check
      passes: `python3 -m unittest discover` over `skills/tests`,
      `scripts/tests`, and `hooks/tests` each exit 0, and `cairn_validate`
      exits 0.

## Coverage

- AC1 → T1
- AC2 → T3, T4
- AC3 → T5
- AC4 → T6
- AC5 → T2
- AC6 → T4, T7
- AC7 → T8

## Tasks

- [ ] T1 — Author the section-consistency helper: heading-delimited slice
      (bounded at the next `## `, and at EOF where the section is last),
      whitespace normalization, sentence sequence. Read targets with
      `Path.read_text` (M100). Comment each permitted closed-class constant
      (AC1).
- [ ] T2 — Append §9 to `guard-doctrine.md` — presence-vs-consistency, the two
      defeating shapes, the detect-never-judge boundary, no renumbering — and
      update §8's two `§§1–7` enumerations (`guard-doctrine.md:328`, `:384`),
      re-anchoring the four pins that move with them
      (`test_mutation_harness.py:2472`, `:2496`;
      `test_fresh_context_readers.py:477`, `:509`) (AC5).
- [ ] T3 — Generate the §8 ledger fixture from the helper **after T2's §8 edit**
      and commit it; author the guard test comparing section to ledger, with an
      alignment-based added/removed/moved failure message (AC2).
- [ ] T4 — Register the ledger guard in `test_mutation_harness.py`; confirm it
      fails when blanked, and that `TestRegistryCompleteness` stays green
      (AC2, AC6).
- [ ] T5 — Replay the four recorded mutations against the AC2 guard, restoring
      §8 byte-identical after each; record which two already fail the
      pre-milestone suite and which two are the load-bearing defeats (AC3).
- [ ] T6 — Reflow §8 with hyphen-breaking off, run the AC2 guard scoped via
      `-k`, restore byte-identical; record (AC4).
- [ ] T7 — Author asserts pinning every rule §9 adds, anchored on the shipped
      bytes (M95); verify each by in-place inversion restored byte-identical,
      and register each (AC6).
- [ ] T8 — Full verify and `cairn_validate`; then `/milestone-implement` step 8
      fires `guard-doctrine.md` §8 certification, since this milestone authors
      prose-guards (AC7).

## Work log

- 2026-07-30: created by /milestone-plan.
- 2026-07-30: absorbs the presence-not-consistency candidate row (added 2026-07-30 from M123 §8 round 3 F2, extended at round 4 F3). Its cross-file sibling stays with the parked one-surface-pin row (D-065) — that class is a rule forking across files, this is contradiction within one.
- 2026-07-30: criteria audit (fresh-context [O], authored none of the criteria) returned 7 findings. Six clear, all fixed before the gate: AC3's word "defeating" false for two of the four mutations; AC4 missing the byte-identical restore, jointly unsatisfiable with AC7 because 68 of the 84 §8 registry locators carry literal newlines; AC6's registration clause too narrow for `TestRegistryCompleteness`; AC5's renumbering unreachable under IP4, since appended D-entries cite "§8"; AC7 mislabelling `cairn_validate` as the `verify` slot when `PROFILE.md` puts it in `consistency-gate`; AC1 and AC2 jointly forbidding the ledger AC2 mandates. One judgment finding — AC1's enumeration-ban breadth — went to the gate and was decided as content-drawn lists only.
- 2026-07-30: the audit's replay independently reproduced at plan time before AC3 was written on it — mutation (a) leaves `skills/tests` at 777 tests OK; (c) FAILED (failures=1); (d) FAILED (failures=1, errors=1); §8 restored byte-identical after each, `git diff` empty. Mutation (b) rests on the audit's measurement and was not re-run here.
- 2026-07-30: plan gate chose planning the milestone over narrowing it to the rename case or deferring it, because two of the four recorded mutations still defeat the whole suite; falsified by the ledger guard catching no consistency defeat the shipped suite does not already catch, across the next two guard-authoring milestones.
- 2026-07-30: plan gate chose a committed sentence ledger over inferring contradiction from extracted vocabulary and polarity, because this repo has beaten five successive matchers on this same section and D-065 names a content hash over normalized blocks as the promotable shape; falsified by a contradiction shipping with the ledger updated in the same commit, i.e. the diff being rubber-stamped rather than read.
- 2026-07-30: plan gate chose §8 as the sole application over all nine guard-doctrine sections, because eight of the nine carry no recorded consistency defeat and their ledgers would be maintenance with no evidence behind them; falsified by a consistency defeat found in a guard-doctrine section other than §8 before the rollout row is promoted.
- 2026-07-30: plan gate chose banning only content-drawn enumerations over banning every lexical constant, because §8 contains `(iii).`, `i.e.`, `D-085.` and `§§1–7`, and the candidate row's own promotion condition bans enumerating subjects rather than punctuation; falsified by a permitted closed-class constant growing to encode section-specific content.
- 2026-07-30: CHECKPOINT — committed with the revised criteria set out for a second criteria-audit pass, which had not returned when this commit was made. Any finding it returns lands as a plan amendment before `/milestone-implement` starts.
- 2026-07-30: criteria audit pass 2 returned 3 findings. Two clear, both fixed: AC4's "no word changed" admitted two states, because a `textwrap.fill` re-wrap at defaults breaks hyphenated compounds and reds the guard (4 sentences added, 4 removed, first divergence `zero-unresolved` at `guard-doctrine.md:331`) while `break_on_hyphens=False` leaves it green — restated as token-sequence-unchanged; and AC2's failure message admitted a set-difference implementation reporting mutation (a) as `added=1, moved=35` against `difflib`'s single insert opcode — restated as alignment-based. Pass 2 also confirmed AC3's factual claim independently and filled in mutation (b), which is green like (a).
- 2026-07-30: plan gate chose updating §8's two `§§1–7` enumerations over leaving them stale or rewording them to stop enumerating, because appending §9 makes the list incomplete and shipping that defect in the milestone that names the class is the worse outcome; falsified by the re-anchoring cost exceeding the milestone's headroom, or by a later section append repeating the staleness a reword would have prevented.
- 2026-07-30: CHECKPOINT — AC5's enumeration clause and the T2-before-T3 reordering it forces are out for criteria-audit pass 3, which had not returned when this commit was made. AC1, AC3, AC6 and AC7 passed pass 2 unchanged and are deliberately not re-read.

## Decisions

## Review
