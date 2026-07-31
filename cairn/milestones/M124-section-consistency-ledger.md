# M124: A section-consistency ledger, so a contradicted or renamed rule reds

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** `m124-section-consistency-ledger`

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
      change and never judges it. §9 states the remedy an out-of-mandate
      consistency finding is fixed under as operation the author runs —
      regenerate the ledger, read the reported diff, repair or accept — never
      as adjudication the guard performs, so that naming §9 in §8's routing
      enumerations is true of the shipped section. §8's two enumerations of
      `§§1–7` are updated to name §9 as well; every pre-existing assert and
      registry block that the enumeration edit or its re-wrap breaks is
      re-anchored on the shipped bytes, so the suite is green at HEAD; and
      D-083 part 3(a)'s description of §8's routing, which the edit makes
      incomplete and IP4 forbids editing, is superseded by an appended
      D-entry.
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

- [x] T1 — Author the section-consistency helper: heading-delimited slice
      (bounded at the next `## `, and at EOF where the section is last),
      whitespace normalization, sentence sequence. Read targets with
      `Path.read_text` (M100). Comment each permitted closed-class constant
      (AC1).
- [x] T2 — Append §9 to `guard-doctrine.md` — presence-vs-consistency, the two
      defeating shapes, the detect-never-judge boundary, no renumbering — and
      update §8's two `§§1–7` enumerations (`guard-doctrine.md:328`, `:384`;
      note the en dash U+2013). Line 328 is 71 chars and needs no re-wrap, so
      it breaks only its own 2 pins; line 384 is 80 chars and forces bullet
      (i)'s re-wrap, taking 4 more. Re-anchor every pin the edit or its
      re-wrap breaks — 6 on a minimal edit, up to 9 on a full re-fill — and
      copy anchors from the shipped bytes (M95). Append the D-entry
      superseding D-083 part 3(a)'s now-incomplete routing description
      (`cairn/DECISIONS.md:2913`) — never edit it (IP4) (AC5).
- [x] T3 — Generate the §8 ledger fixture from the helper **after T2's §8 edit**
      and commit it; author the guard test comparing section to ledger, with an
      alignment-based added/removed/moved failure message (AC2).
- [x] T4 — Register the ledger guard in `test_mutation_harness.py`; confirm it
      fails when blanked, and that `TestRegistryCompleteness` stays green
      (AC2, AC6).
- [x] T5 — Replay the four recorded mutations against the AC2 guard, restoring
      §8 byte-identical after each; record which two already fail the
      pre-milestone suite and which two are the load-bearing defeats (AC3).
- [x] T6 — Reflow §8 with hyphen-breaking off, run the AC2 guard scoped via
      `-k`, restore byte-identical; record (AC4).
- [x] T7 — Author asserts pinning every rule §9 adds, anchored on the shipped
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
- 2026-07-30: criteria audit pass 3 returned 2 findings. One clear, fixed: AC5's repair obligation was scoped to pins on the enumerations (4) while its stated purpose was a green suite, and the two do not coincide — the measured breakage is 2 failures + 4 errors on a minimal edit and 2 failures + 7 errors on a full re-fill, because `guard-doctrine.md:328` is 71 chars and needs no re-wrap while `:384` is 80 and forces bullet (i)'s. Rescoped to every pin the edit or its re-wrap breaks, 6 to 9; T2 carries the line lengths and the en-dash U+2013 warning. Pass 3 also confirmed T2-before-T3 resolves the ledger-ordering hazard and that no §8 anchor becomes unpinnable.
- 2026-07-30: plan gate chose making §9 a fix destination named in §8's routing enumerations over referencing it descriptively beside them, because §9 carries the ledger instrument and a consistency gap found as out-of-mandate work is fixed by applying it; the rider is that §9 must state a remedy and not only a caution, which AC5 now requires. Falsified by §9 shipping with no remedy a finding could be routed to, which would make its presence in the enumerations a false claim of the kind §8's own claim-vs-file check exists to catch.
- 2026-07-30: criteria audit pass 4 returned 1 finding, clear and fixed: AC5's remedy clause admitted a §9 attributing the remedy to the instrument, which would falsify the same criterion's "detects a change and never judges it" while still satisfying the clause. Restated as operation the author runs — regenerate, read the diff, repair or accept — never adjudication the guard performs, which is also the only family outside D-067's rejection of a mandatory re-derivation step and consistent with §8 discharging this class "by operation" (`guard-doctrine.md:331-332`). Pass 4 also confirmed D-067's `cairn_validate` rejection is scoped to the two readers and does not reach a doctrine section.
- 2026-07-30: pass 4 flagged, outside its own count, that D-083 part 3(a) (`cairn/DECISIONS.md:2913`) describes §8 as routing out-of-mandate work "as ordinary §§1-7 work" — incomplete after T2, and unfixable in place under IP4. Added to AC5 and T2 as a superseding append. This clause was authored AFTER pass 4 and was not read by it; it is mechanically satisfiable and IP4-mandated rather than IP4-blocked, so the audit loop is closed here at 4 passes rather than re-opened for it.
- 2026-07-30: status -> in-progress on `m124-section-consistency-ledger`, cut from `main` at 65437f5.
- 2026-07-30: T1 — `skills/tests/section_ledger.py`: `section_body` (heading-delimited, heading EXCLUDED, bounded at the next `## ` or EOF), `sentences` (whitespace-normalized, split on terminal punctuation), `diff` and `describe` (SequenceMatcher-aligned). Measured on §8 at HEAD: 50 sentences, no suspicious units. Excluding the heading is what removes the spurious 51st unit the audit found (`## 8.` ends in a numeral-period), and with it excluded the splitter needs ZERO lexical constants — AC1's closed-class carve-out ships unused, which the module's docstring states rather than implies.
- 2026-07-30: T1 verify — reflow at width 66 with `break_on_hyphens=False` yields a sequence IDENTICAL to HEAD (AC4's invariant holds); the same reflow with hyphen-breaking ON differs by 4 sentences, reproducing the audit's measurement and confirming AC4's exclusion is the operative one. A pure one-sentence insertion reports `added=1, removed=0, moved=0` against the set-difference alternative's `added=1, moved=35` (AC2's alignment clause). skills 777 / scripts / hooks each exit 0; `cairn_validate` exit 0.
- 2026-07-30: AMENDMENT (minor) — T1 ships the helper module alone; its unit tests move to T3, which is where the ledger fixture makes them meaningful. Reason: `skills/tests/` treats every `test_*.py` as a prose-guard that `TestRegistryCompleteness` requires be registered or exempted, and a test file landing before the ledger guard has nothing registrable in it. No criterion or scope text changes, so no gate is owed; T1's helper is covered by the measurements recorded above until T3.
- 2026-07-30: T2 — `guard-doctrine.md` §9 "Presence is not consistency" appended (450 lines total, no renumbering): the presence-vs-consistency claim, the three shapes it comes apart in (contradicting sentence, rename reusing no word, relocation falsifying a back-reference), the derive-from-the-section rule, the detect-never-judge boundary, and the remedy as operation the author runs. The rubber-stamp failure mode — a ledger updated without its diff read — is DISCLOSED in §9 rather than hidden, since no guard can detect it.
- 2026-07-30: T2 — both §8 enumerations updated. Line 328 (75 chars) took `, §9` to 79 with no re-wrap and broke only its own 2 pins, exactly as the plan predicted; line 384 (84 chars) took ` or §9` and forced bullet (i)'s tail to re-wrap, taking 4 more. Six breakages total — 2 asserts and 4 registry blocks — matching criteria-audit pass 3's minimal-edit measurement exactly, and not the 4 the plan's first draft assumed.
- 2026-07-30: T2 — all six re-anchored on the shipped bytes: asserts `test_out_of_mandate_observations_route_to_sections_one_to_seven_and_nine` (renamed, since the old name asserted a routing set the section no longer has) and `test_the_falsifier_counts_where_a_finding_was_found`; registry blocks for those two plus `test_the_falsifier_window_carries_a_non_vacuity_floor` and `test_the_falsifier_carries_both_tolerances`, whose ASSERTS survived on `\s+` while their byte-anchored blocks did not — the re-anchoring tax, not a false-red.
- 2026-07-30: T2 — verified by inversion, not by blanking: reverting `§§1–7, §9 and the mutation harness` to its old form reds its own test, and so does reverting `§§1–7 or §9 does not remove`; §8 restored byte-identical after each. D-088 appended (`git diff` +30/−0, no entry edited) superseding D-083 part 3(a)'s now-incomplete enumeration; `dangling id tokens` OK after the append, so M115's unmasking batch did not appear.
- 2026-07-30: T2 verify — skills 777 / scripts / hooks each exit 0; `cairn_validate` exit 0.
- 2026-07-30: T3+T4 done together, and they could not be split: `skills/tests/` treats every `test_*.py` as a prose-guard `TestRegistryCompleteness` requires be registered, so a test file landing one checkpoint before its registration reds the suite. Ledger at `skills/tests/ledgers/guard-doctrine-8.txt`, 50 sentences, one per line — a line-oriented file because the diff IS the mechanism and `git diff` renders it legibly. Generated AFTER T2's §8 edit, as the plan required; both §9 references are in it.
- 2026-07-30: T3 — `section_ledger.py` gained a `render` + `__main__` CLI, unplanned but owed: §9 assigns "regenerate the ledger" as the remedy, and a remedy with no way to perform it is a claim the section cannot support.
- 2026-07-30: T3 — two bugs found by the new tests against their own author. `test_extraction_carries_no_word_constant` first captured the raw-string `r` prefix and red on its own syntax; then, fixed, it red on `\s+` — a regex escape is letters to a naive search. Now strips escapes before checking. Both are the M114 shape: the claim was right, the instrument measuring it was not.
- 2026-07-30: T4 — one registry entry, `TestSectionEightLedger.test_section_matches_its_ledger` on block `Zero unresolved stays the bar;`. That block is pinned by another assert too, which is not a defect: the harness runs the NAMED test alone, so the entry proves this guard reds. What the ledger catches that no anchor does is proved at T5 instead, not by this entry — recorded so the registration is not read as evidence it is not.
- 2026-07-30: T3+T4 verify — skills 790 (up 13) / scripts / hooks each exit 0; `cairn_validate` exit 0.
- 2026-07-30: T5 — all four recorded mutations replayed, §8 restored byte-identical after each (`git status` clean at the end). Every one reds the ledger guard. The split AC3 states is confirmed against the shipped suite: (a) the contradicting append and (b) the three-checks relocation red the ledger guard and NOTHING ELSE — those are the load-bearing cases, and before this milestone they shipped green. (c) also reds `test_the_class_is_never_called_by_a_synonym` and (d) also reds `test_a_fix_authored_record_is_still_read_and_still_corrected` plus the blanking harness, so both are controls, closed by M123's own rounds 4-7 rather than by this guard.
- 2026-07-30: T5 — this is the evidence the T4 registry entry deliberately does not carry: two mutations that defeat all 777 pre-existing tests and are caught only here.
- 2026-07-30: T6 — §8 re-wrapped paragraph by paragraph at width 68 (the file sits at ~76-80) with `break_on_hyphens=False`; the ledger guard, run scoped via `-k section_matches_its_ledger`, is OK. §8 restored byte-identical. The scoping matters and is not cosmetic: 84 registry locators inside §8 carry literal newlines, so a whole-suite run under a reflow errors on them — that is the re-anchoring tax, not the invariant AC4 measures.
- 2026-07-30: T7 — 10 asserts for §9's 10 rules, in `TestSectionNineDoctrine`, plus 10 registry entries. Every assert reads §9's OWN slice, never the whole file: M123's extension of the M95 lesson is that whole-file anchors let six §8 clauses be moved verbatim into §7 with 777 tests green, so scope the read to the unit the criterion names.
- 2026-07-30: T7 — inversion sweep 10/10, each rule negated in place reds its OWN test, §8+§9 restored byte-identical after each, tree clean at the end. Reported with its denominator (M123's lesson): every one of the 10 had a mutation and none was skipped for want of one, so 10/10 is over all rules and not over the rules the sweep happened to handle.
- 2026-07-30: T7 — two authoring bugs caught by running rather than by reading, both M95/M105 shapes: the label-to-clause gap matchers used `.`, which cannot cross the file's hard wrap (3 asserts red); the fix then double-escaped to `[\\s\\S]` inside a raw string, matching a literal backslash. Anchors verified against shipped bytes after both.
- 2026-07-30: T7 verify — skills 800 / scripts 332 / hooks 103, each exit 0; `cairn_validate` exit 0.
- 2026-07-30: §8 CERTIFICATION ROUND 1 — 11 reopening, 2 out-of-mandate, zero fix-authored records (round 1 has none by definition). The gate did NOT open. Six acceptance-criterion clauses were unpinned and five record claims false; every one is fixed below, and each of the six was REPRODUCED before fixing rather than taken on the reader's word.
- 2026-07-30: round 1 coverage gaps, all six reproduced green then closed RED: AC1's constant scan read `re.compile` assignments only, so `_TERMS = [...]` at module level shipped invisible to the test meant to ban it — re-parsed with `ast` so every module-level assignment is reached whatever shape it takes; AC1's "as a parameter" and AC2's "never passed into the extraction" were both unpinned (`terms=(...)` and `ledger=None` each left 800 green) — one signature assert now covers both; AC1's comment-per-constant clause was unpinned; AC2's "moved" category was unpinned at the `describe` level, so a relocation would have failed the guard with an empty message body; and AC5's remedy STEPS were unpinned while its headline was, so §9 could have stopped stating the operation §8's enumerations now route findings to. Five new asserts, one registered against `guard-doctrine.md`.
- 2026-07-30: BY-HAND CHECK, disclosed rather than registered: four of the five new asserts target `skills/tests/section_ledger.py`, a Python module and not doc prose, so the mutation harness has no target for them and blanking would break the import rather than red the assert (`guard-doctrine.md` §2's carve-out, M117's shape). Each was instead verified by the mutation that defeated it at round 1, reproduced and re-run. The fifth, the §9 remedy assert, is registered normally.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T2 line says "Line 328 (75 chars) took `, §9` to 79 ... line 384 (84 chars)". Both figures are wrong and neither describes either revision: at `main` line 328 is 71 chars and line 384 is 80; at HEAD they are 75 and 78. The plan's own T2 text carries the correct pre-edit figures. The asymmetry the line reports is real; the numbers attached to it were not.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T6 line says "84 registry locators inside §8 carry literal newlines". 84 is the pre-milestone TOTAL, not the newline-carrying subset. Measured at HEAD: 85 registry blocks resolve inside §8, 69 of them carry a literal newline, and 21 stop resolving under the T6 reflow specifically.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T7 line says whole-file anchors let "six §8 clauses be moved verbatim into §7 with 777 tests green". That pairs a count from M123's round-3 F2 contradiction finding with its round-6 C1 relocation finding, which are different findings over different criteria sets. M123 records the relocation defect as defeating AC2, AC3, AC5 and AC11 clauses across ~75 anchors, and states no clause count. The `section9()` docstring carried the same import and is corrected in place, being current knowledge rather than history (D-045).
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T1 line says "the splitter needs ZERO lexical constants — AC1's closed-class carve-out ships unused". The module ships `_SENTENCE_BOUNDARY`, one closed punctuation class, with the comment AC1 requires: the carve-out ships USED. What is unneeded is an abbreviation class, because §8 carries no abbreviation-shaped mid-sentence period. The module docstring asserted the same thing while contradicting itself six lines later, and is corrected in place.
- 2026-07-30: round 1's two OUT-OF-MANDATE findings FIXED as §8's boundary prescribes, not merely recorded — the boundary says such a finding "is recorded and fixed", and M123's review return settled that recorded-and-not-fixed is the reading it does not license. §9's "defeated four acceptance-criterion clauses" was unsourced and is restated to M123's record (one of eight mutations which between them defeated six). And AC3's mutation (d) source string `A fix-authored record is still read` now occurs TWICE in the target, because §9 quotes both sides of that rename — a plain `str.replace` replay would mutate §9 as well as §8, so a replay must scope to the first occurrence, as T5's did.
- 2026-07-30: §8 CERTIFICATION ROUND 2 — 9 reopening, 0 fix-authored, 2 out-of-mandate. Gate did not open. All 11 fixed, each reproduced green before the fix and RED after: 8/8 on the reproduction sweep.
- 2026-07-30: round 2's two worst findings are the milestone's own doctrine turned on itself. `test_the_rename_shape_is_named` and `test_the_remedy_names_its_three_steps` both opened PAST the polarity carrier — `is not defeated` and `is not discharged` each shipped green — which is precisely M123 round 4's shape, in the milestone that cites it, in a class docstring claiming "each opens on the SUBJECT rather than after it". The docstring was false when written. Both anchors now span the verb.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T7 line claims "inversion sweep 10/10 ... over all rules and not over the rules the sweep happened to handle". The denominator was honest and the MUTATIONS were not: they substituted the anchored words rather than negating the rule, so two anchors that survive `is not X` still red under `is unaffected by X`. Measured under polarity mutation at round 2, the real figure was 8/10. Re-run after the fixes with polarity-carrying mutations across all thirteen §9 rules: 13/13, 0 unmutated.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T3 line's `added=1, moved=35` is wrong. Re-derived at the shipped 50-sentence extraction: AC3's mutation (a) inserts at index 27, so an index comparison gives `added=1, removed=0, moved=23`. 35 came from a plan-time splitter that no longer exists. The same figure in `section_ledger.py` and `test_section_ledger.py` is corrected in place, being current knowledge (D-045).
- 2026-07-30: round 2 coverage gaps closed: AC1's `ast` scan reached `ast.Assign` only, so `_TERMS: list = [...]` shipped green one annotation away from the ban (now `AnnAssign`/`AugAssign` too); AC1's "stating the class" was satisfied by `# TODO: revisit.` (the comment must now name a class); AC2's "removed" was pinned by the LABEL and not the sentence text; AC5's no-renumbering clause was pinned only by §9 existing somewhere, so `## 5.` -> `## 5b.` and even relocating §9 BEFORE §8 shipped green — now the headings must read 1..9 in document order, derived from the file rather than enumerated.
- 2026-07-30: round 2's two out-of-mandate findings FIXED, not merely recorded: §9's disclosure sentence inverted green (`No failure mode...`), and two §9 sentences carried no assert at all. Two new asserts, both registered.
- 2026-07-30: §8 CERTIFICATION ROUND 3 — 2 reopening, 3 fix-authored, 5 out-of-mandate. Reopening trend 11 -> 9 -> 2. Check 1 came back CLEAN for the first time: the reader enumerated every clause of AC1-AC7, negated each in place, and found none unpinned. Both reopening findings are check 2, and both are false claims of mine.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the plan-gate line "because §8 contains `(iii).`, `i.e.`, `D-085.` and `§§1-7`" is wrong on two of its four literals. Measured at `main` and at HEAD: `D-085.` occurs 3x and `§§1-7` 2x, but `i.e.` occurs ZERO times in the whole of `guard-doctrine.md`, and `(iii).` zero times — §8's three `(iii)` are never followed by a period. The gate's decision stands on the two literals that are real, and the shipped module says the true thing ("§8 carries no abbreviation-shaped mid-sentence period"), so this is a false premise beside a correct conclusion — the M114 shape exactly.
- 2026-07-30: round 3's F2 fixed in place — a harness comment read "Registration is per assert and not per file (`guard-doctrine.md` §2)", which states the NEGATION of §2's own bolded sentence and then cites §2 for it. The practice was right; the attribution inverted its source.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the round-2 correction line says "the T3 line's `added=1, moved=35`". No T3 line carries that figure; it is the T1 verify line. The substance of the correction is unaffected and independently re-derived at round 3 (insertion index 27 of 50, so `moved=23`).
- 2026-07-30: CORRECTION, appended not edited (IP4) — the round-1 correction line says "21 stop resolving under the T6 reflow specifically". Re-derived under the procedure that line itself states (paragraph-wise `textwrap.fill(width=68, break_on_hyphens=False)`): 75 of the 85 stop resolving, and the whole-suite run under that reflow reports exactly 75 errors. The first two figures in that line, 85 and 69, reproduce exactly.
- 2026-07-30: round 3's fix-authored records corrected in place, not reopening: the `section9()` docstring's "~75 anchors" and its AC list are unsourced — M123 records no round-6 finding and the string `75` appears nowhere in `cairn/` — so it is restated to what M123 actually ships, anchors scoped to the section over the 84 blocks resolving inside §8.
- 2026-07-30: round 3's out-of-mandate findings: O4 (dead `preceding` binding) and O5 (four over-80 prose wraps from in-place corrections) fixed. O1 is seven §9 sentences that invert green, and ONE of them is fixed here because it negates a shipped rule — "an ordinary edit is exactly a question a diff can answer" contradicts detect-never-judge three sentences after §9 states it, with all 806 green. That is §9's own contradicting-sentence shape turned on §9, and it is now pinned and registered.
- 2026-07-30: the other six of O1, plus O2 (a terms list declared INSIDE `sentences()` satisfies AC1, which names only a parameter or a module constant) and O3 (the comment test accepts any comment containing the word `class`), are RECORDED and routed to the rollout candidate row rather than fixed here. They are the row's promotion condition met exactly as written — a consistency defeat found in a doctrine section other than §8 — and §9 is that section. The row is promotable on this evidence at the next plan gate; recording that is the disposition, not deferral by silence.
- 2026-07-30: §8 CERTIFICATION ROUND 4 — 3 reopening, 1 fix-authored, 1 out-of-mandate. Round 4 OVERTURNED round 3's "check 1 clean": AC5's no-renumbering clause was pinned by the heading NUMBERS only, so swapping §6 and §7 bodies and relabelling preserves `1..9` and ships green, silently staling 12 cross-file citations. Now pinned as ordered (number, title) pairs — the milestone's own ledger instrument at section scale.
- 2026-07-30: round 4's other two reopening findings: AC1's comment check selected constants by NAME regex, so `ABBREVIATIONS = re.compile(...)` with no comment at all shipped green — the exact addition the module docstring anticipates — now derived from the `ast` targets; and AC5's superseding-D-entry clause was pinned by nothing, so deleting D-088 and D-089 outright left 807 OK and `cairn_validate` exit 0, with §8's routing enumeration contradicting a standing D-entry and nothing red. All three reproduced green, then RED after the fix.
- 2026-07-30: CORRECTION OF A CORRECTION, appended not edited (IP4) — round 3's F3 was WRONG and I acted on it. It said the T7 line's "six acceptance-criterion clauses ... 777 tests green" was unsourced and paired two different M123 findings. `cairn/LESSONS.md:28` carries that sentence VERBATIM, unchanged since `main`. The T7 line was right, correctly attributed and correctly counted; my round-3 "fix" replaced a true sourced claim with a weaker one and introduced `AC11` and `~75 anchors`, which occur nowhere in `cairn/` except the lines I wrote. The `section9()` docstring is restored to the sourced wording and now cites `LESSONS.md`. Verified against the file myself before acting, which is what round 3 did not get from me.
- 2026-07-30: round 4's O1 disputed and RE-MEASURED rather than adopted. It reports the T6 reflow as "75 errors and 11 failures"; run under the procedure T6 actually used — paragraph-wise `textwrap.fill(width=68, break_on_hyphens=False)`, bullet paragraphs left alone — the whole suite gives `failures=2, errors=21`. Round 1's original "21" was right and round 3's "75" correction was wrong; both figures are reproducible and the discriminator is whether bullet paragraphs are re-wrapped, which none of the three records stated. That is the third time in this milestone a bare number was recorded without the procedure that produces it, and it is the same defect class in a different medium from the one §9 ships against.
- 2026-07-30: the 2 failures under that reflow are asserts false-redding on a token-preserving re-wrap — the M105 shape, out of mandate (AC4 scopes its evidence to the AC2 guard, which stays green). Recorded here and routed to the rollout candidate row with round 3's O1/O2/O3.
- 2026-07-30: criteria audit closed. Four passes, 13 findings total: 9 clear (all fixed), 3 judgment (all taken to the gate and decided), 1 uncounted observation (actioned above). Passes 2-4 each independently re-measured rather than reusing an earlier count, and pass 3 corrected pass 2's own pin count from 4 to 6-9.

## Decisions

## Review
