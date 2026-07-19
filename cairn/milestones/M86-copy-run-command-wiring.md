<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M86: Copy-run command wiring — the handoff rule reaches the steps that hand over

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP3, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make every skill step that hands the user a command to run emit it as a
copyable fenced block, and sharpen the central rule so the handoff, naming,
and routing-chip cases stop blurring into each other.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the `tracking-rules.md` copy-run rule gains an explicit three-way
distinction (handoff → fenced block; naming a command/path/symbol in prose →
inline backticks; a routing-chip `→ /skill` arrow → neither, because the
orchestrator invokes it per D-022) and names slash commands alongside shell
commands. Per-skill directives at the three steps that actually hand a command
over — `/milestone-review` step 10, `/milestone-brief` step 3's manual-run
option, `/cairn-release` step 4's terminal-actions checklist — plus the
prose-guards locking them, mutation-registered. A D-entry recording the
three-way boundary and the handoff-vs-mention call.

**Out:** wiring the six skills that hand no command to the user (they get
nothing; the central rule already binds them). Changing
`/milestone-implement`'s "a safe `/clear` point" recap line — decided at the
plan gate to be a mention, not a handoff, and AC5 locks it inline so a later
over-fire is caught rather than left to judgment. Any change to the
routing-chip `→ /skill` notation itself (D-022 owns it). Reformatting the
agent-run commands throughout the skills (`gh`, `python3 …cairn_validate.py`) —
those are not handoffs and stay inline.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `skills/shared/tracking-rules.md`'s copy-run rule states all three
      cases, each label together with what it takes: a command handed to the
      user → its own fenced code block; naming a command, path, or symbol in
      prose → inline backticks; a routing-chip `→ /skill` option → neither,
      because the orchestrator invokes it (D-022).
- [ ] AC2 — that rule names slash commands (`/clear`, `/milestone-plan`) as
      covered, not only shell commands.
- [ ] AC3 — `skills/milestone-review/SKILL.md` step 10 no longer instructs the
      inline form: `grep -n "inline" skills/milestone-review/SKILL.md` returns
      no hit within step 10, and the step directs the `/clear` + next-skill
      handoff into a fenced block.
- [ ] AC4 — `skills/milestone-brief/SKILL.md` step 3's manual-run option and
      `skills/cairn-release/SKILL.md` step 4's terminal-actions checklist each
      name the fenced-block form at the point of handoff.
- [ ] AC5 — a prose-guard locks the directive in each of the three skills and
      asserts `/milestone-implement`'s `/clear` line stays a mention; each
      guarded label is pinned together with its members on one physical line
      (M74/M76), and the guard file is registered in
      `skills/tests/test_mutation_harness.py`.
- [ ] AC6 — the `verify` slot is clean: all three suites
      (`discover -s skills/tests`, `-s scripts/tests`, `-s hooks/tests`) green,
      each exit code checked explicitly (M56/M65), and
      `scripts/cairn_validate.py` passes.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. Review reads to fence
     evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3, T5
- AC4 → T4, T5
- AC5 → T5
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1 — Rewrite the copy-run rule at `skills/shared/tracking-rules.md:495`
      to state the three cases and to name slash commands. Author each
      guard anchor on its own physical line, unwrapped (M78/M82), and before
      committing grep every word an existing guard anchors on — `fenced`
      already occurs in `skills/design-interview/SKILL.md:105` and in
      `cairn_validate`'s fence-aware counter, so new prose can degrade a bare
      `assertIn` elsewhere (M60/M80/M85).
- [ ] T2 — Update `test_rulebook_polish.py:43`
      (`test_copy_run_commands_get_their_own_fenced_block`) to pin each of the
      three labels together with its members on one physical line, and refresh
      its `Mutation(...)` entry at `test_mutation_harness.py:545` (the current
      `block="own fenced code block"` moves if the line is reflowed).
- [ ] T3 — Rewrite `skills/milestone-review/SKILL.md:203-206`: drop "naming the
      obvious next action inline" and direct the close to emit `/clear` and the
      next skill as a fenced block. The step-10 prose stays chip-less (D-019).
- [ ] T4 — Wire `skills/milestone-brief/SKILL.md:42-44` (the manual-run
      blockquote renders no copy button — move the prompt to a fenced block)
      and `skills/cairn-release/SKILL.md:68-71` (the terminal-actions
      checklist names the fenced form).
- [ ] T5 — Add the per-skill guard covering T3/T4's three directives plus the
      `/milestone-implement:108` mention-stays-inline assert; pair the negative
      assert with a positive framing assert so it can carry a mutation entry
      (M53), and register the file in `test_mutation_harness.py`.
- [ ] T6 — Run the three suites from the repo root, checking each exit code
      separately and never through a pipe (M56/M65), plus `cairn_validate.py`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046). -->

- 2026-07-18: created by /milestone-plan.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046). -->
