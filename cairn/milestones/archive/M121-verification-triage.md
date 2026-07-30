# M121: Verification triage — classify every self-verification instruction, and re-decide D-067's two fresh-context readers

**Status:** done (2026-07-28, PR #121 https://github.com/jmgirard/cairn/pull/121)

**Goal:** Classify every self-verification instruction in cairn's shipped prose against the
Opus 5 guide's over-verification finding and re-decide D-067's two readers on evidence.

**Outcome:** cairn does not have the guide's over-verification. Of 79 hits over the nine
`SKILL.md` files and five `shared/` modules, 31 are `command-evidence`, 36 `not-an-instruction`,
11 are D-067's instruments, and exactly **one** is a `same-context-recheck` —
`references/self-verification-ledger.md`, one row per hit, with its `INDEX.md` line and
`TestShippedPageStateLedger` pin. The plan-gate criteria audit now records a work-log line
either way (three of five milestones after adoption left none), at `/milestone-plan` step 3 and
cross-referenced from `/milestone-brief`; `tracking-rules.md` names both self-checking classes
so the guide's delegation clause cannot reach a fresh-context reader. `guard-doctrine.md` ships
**unchanged** — a §8 narrowing was drafted, replaced, escalated (RB09/RR09) and withdrawn.

**Decisions:** D-079 (both instruments narrowed), D-080 (§8's narrowing withdrawn on RR09's
evidence — inert under one reading, discards real findings under the other), D-081 (records
M121's own in-place edits of D-079, the IP4 violation D-065 forbids), D-082 (widens the
supersession; restores D-067's falsifier in full, "don't tune it" included).

**Review:** Two passes. Pass 1: 9 of 37 at 80+, returned — AC1's search gave 119 not 79 run
literally. Pass 2: 7 at 80+, fixed in-pass; four logged ones closed at the gate on a maintainer
hold. LESSONS 49/50: two lines extended in place, none added or retired.
