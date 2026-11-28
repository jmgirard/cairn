# M120: Ingest the Opus 5 prompting guide, and adopt the three conduct rules cairn has no home for

**Status:** done (2026-07-27, PR #120 https://github.com/jmgirard/cairn/pull/120)

**Goal:** Ingest Anthropic's Claude Opus 5 prompting guide as a cited source
note and adopt the three conduct changes it supplies where cairn had no rule.

**Outcome:** `/milestone-review`'s three reviewers no longer drop taxonomy
matches before reporting — they report everything and the false-positive
taxonomy runs once downstream in the `[S]` scorer's rubric, scoring a match
below 60 into the logged sub-80 list; step 5 now also states the scorer's
evidence base (diff + milestone file). `tracking-rules.md` gains a
correction-narration rule and a delegation-warrant test, each guarded with
per-phrase mutation entries. Adds `references/prompting-opus-5.md` + INDEX line
+ ledger pin, and a third disposition on the §8 round-count candidate row.

**Decisions:** D-078 — the relocation, its two rejected alternatives, the IP3
gap it closes, and the scorer's evidence base. Milestone-local: none.

**Review:** 3 lenses + scorer, 28 findings; 8 scored ≥80 (7 distinct), all fixed
(92/88/87/87/86/83/80); 20 logged sub-80. Three asserts survived inverting their
own rule — guard-doctrine §1's inversion had not been run; all 10 redden now.
§8 took 3 rounds. Retired: none; M117's harness-blind-spot lesson extended with
"a green §8 certification does not prove inversion either".
