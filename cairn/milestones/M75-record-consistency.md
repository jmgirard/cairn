<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M75: Record consistency — the `leave` disposition and MCP-matcher semantics

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m75-record-consistency`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Close two gaps where cairn's durable record fails to carry a fact its own
work already established.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a `tracking-rules.md` Intake line legitimizing `leave` as a fourth
disposition, narrowed to noise, duplicates, and items already
cross-referenced in cairn; D-044 recording the IP3 reading that narrowing
rests on; an MCP-matcher bullet in `cairn/references/claude-code-hooks.md`;
a label-inclusive guard over the new rulebook line.

**Out:**

- Pruning `LESSONS.md:41` (the M71 matcher lesson) → ordinary post-merge
  hygiene, when the 50-line cap forces it. Decided at the M75 plan gate:
  the reference page becomes the durable home; the lesson prunes naturally.
- Guard coverage for the *rest* of the unguarded Intake paragraph → a
  candidate row if it ever matters; this milestone guards only the line it
  adds and the enumeration that line joins.
- Any change to `/milestone` §3's four dispositions → they stand as M74
  shipped them; the rulebook moves to meet the skill, not the reverse.
- A content guard over the hooks reference page → no reference page carries
  one (they record external facts, not cairn contracts); AC4's grep is the
  evidence.

**Settled at the plan gate, not open:** whether legitimizing `leave` weakens
IP3's conservation guarantee as D-042 extended it ("what the session
surfaced"). Settled in-session via D-044 rather than escalated — a
reason-stated, user-chosen `leave` on noise is not a *silent* drop, which is
what IP3 forbids. Implement inherits the answer, not the question.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `tracking-rules.md`'s Intake paragraph names `leave` as a legal
      fourth disposition with its narrowing (noise, duplicates, already
      cross-referenced) stated on one physical line; the pre-M75 three-way
      sentence no longer stands as the whole enumeration.
- [ ] AC2 — `cairn/DECISIONS.md` carries D-044 recording the IP3/D-042
      reading, the chosen narrowing, and the two rejected alternatives
      (drop `leave` from the skill; legitimize it unnarrowed).
- [ ] AC3 — the rulebook line and `/milestone` §3's `leave` bullet agree:
      both texts quoted side by side in the Review section show no
      contradiction, and §3's four dispositions are unchanged by this
      milestone (`git diff` over `skills/milestone/SKILL.md` touches no
      disposition text).
- [ ] AC4 — `cairn/references/claude-code-hooks.md`'s "Matchers & execution"
      section states that a matcher of only word chars, `-`, space, `,` or
      `|` is compared as an exact string, so an MCP tool matcher must carry a
      metacharacter; its `INDEX.md` line still describes the page accurately.
- [ ] AC5 — a guard asserts the new rulebook line *including its `leave`
      label* (M74/F3: a clause-only assert survives a label swap), with a
      mutation-harness entry whose anchor phrase is unique within
      `tracking-rules.md` (M58).
- [ ] AC6 — verify clean: `python3 -m unittest discover` green for
      `scripts/tests`, `skills/tests`, and `hooks/tests`; `cairn_validate.py`
      exits 0.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T4
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Add the `leave` line to the Intake paragraph,
      `skills/shared/tracking-rules.md:199-205`. Keep the guarded phrase on
      one physical line (M23) and clear of `**bold**` splits (M26). Do not
      touch `skills/milestone/SKILL.md`.
- [x] T2 — Append D-044 to `cairn/DECISIONS.md` (text drafted at the plan
      gate; append-only, never renumber).
- [x] T3 — Add the MCP-matcher bullet to the "Matchers & execution" section,
      `cairn/references/claude-code-hooks.md:94-100`, alongside the existing
      exact-vs-regex bullet. Re-read the page's `INDEX.md` line and confirm
      it still describes the page.
- [ ] T4 — Guard T1 in `skills/tests/test_external_pr_intake.py` (it already
      reads `tracking-rules.md` and owns the intake paragraph's PR half):
      a label-inclusive assert plus a `Mutation(...)` entry in
      `test_mutation_harness.py`. Run all three suites and `cairn_validate.py`;
      check exit codes explicitly, never through a pipe (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan; absorbs the M74-F5 and M71-F3 candidate rows.
- 2026-07-18: T1 — rulebook Intake paragraph names `leave`, narrowed per D-044; phrase unique in file; 96/287/72 suites green.
- 2026-07-18: T2 — no branch work needed: D-044 landed in the plan commit a00653d, before the branch was cut. Ticked as satisfied, not re-authored.
- 2026-07-18: T3 — MCP-matcher bullet added to the hooks reference; exemplar verified live against hooks.json:67 + idea_guard.py:28 (same suffix shape); INDEX line amended to record the non-official-docs provenance.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->
