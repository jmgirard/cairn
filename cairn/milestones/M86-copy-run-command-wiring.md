<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M86: Copy-run command wiring — the handoff rule reaches the steps that hand over

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP3, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m86-copy-run-command-wiring` · https://github.com/jmgirard/cairn/pull/85   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1 — `skills/shared/tracking-rules.md`'s copy-run rule states all three
      cases, each label together with what it takes: a command handed to the
      user → its own fenced code block; naming a command, path, or symbol in
      prose → inline backticks; a routing-chip `→ /skill` option → neither,
      because the orchestrator invokes it (D-022).
- [x] AC2 — that rule names slash commands (`/clear`, `/milestone-plan`) as
      covered, not only shell commands.
- [x] AC3 — `skills/milestone-review/SKILL.md` step 10 no longer instructs the
      inline form: the instruction "naming the obvious next action inline" is
      gone from the file, and step 10 directs the `/clear` + next-skill handoff
      into a fenced block, citing the tracking-rules copy-run rule.
      <!-- amended 2026-07-18 via the implement step-6 gate: the original
           grep-for-"inline" evidence self-hit the fix, which must state the
           prohibition (M58/M59/M62 lesson). Intent unchanged. -->
- [x] AC4 — `skills/milestone-brief/SKILL.md` step 3's manual-run option and
      `skills/cairn-release/SKILL.md` step 4's terminal-actions checklist each
      name the fenced-block form at the point of handoff.
- [x] AC5 — a prose-guard locks the directive in each of the three skills and
      asserts `/milestone-implement`'s `/clear` line stays a mention; each
      guarded label is pinned together with its members on one physical line
      (M74/M76), and the guard file is registered in
      `skills/tests/test_mutation_harness.py`.
- [x] AC6 — the `verify` slot is clean: all three suites
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

- [x] T1 — Rewrite the copy-run rule at `skills/shared/tracking-rules.md:495`
      to state the three cases and to name slash commands. Author each
      guard anchor on its own physical line, unwrapped (M78/M82), and before
      committing grep every word an existing guard anchors on — `fenced`
      already occurs in `skills/design-interview/SKILL.md:105` and in
      `cairn_validate`'s fence-aware counter, so new prose can degrade a bare
      `assertIn` elsewhere (M60/M80/M85).
- [x] T2 — Update `test_rulebook_polish.py:43`
      (`test_copy_run_commands_get_their_own_fenced_block`) to pin each of the
      three labels together with its members on one physical line, and refresh
      its `Mutation(...)` entry at `test_mutation_harness.py:545` (the current
      `block="own fenced code block"` moves if the line is reflowed).
- [x] T3 — Rewrite `skills/milestone-review/SKILL.md:203-206`: drop "naming the
      obvious next action inline" and direct the close to emit `/clear` and the
      next skill as a fenced block. The step-10 prose stays chip-less (D-019).
- [x] T4 — Wire `skills/milestone-brief/SKILL.md:42-44` (the manual-run
      blockquote renders no copy button — move the prompt to a fenced block)
      and `skills/cairn-release/SKILL.md:68-71` (the terminal-actions
      checklist names the fenced form).
- [x] T5 — Add the per-skill guard covering T3/T4's three directives plus the
      `/milestone-implement:108` mention-stays-inline assert; pair the negative
      assert with a positive framing assert so it can carry a mutation entry
      (M53), and register the file in `test_mutation_harness.py`.
- [x] T6 — Run the three suites from the repo root, checking each exit code
      separately and never through a pipe (M56/M65), plus `cairn_validate.py`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046). -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: T1+T2 — rule rewritten as three labelled cases + slash commands + the handoff/mention test; guard pins each label with its treatment on one line, mutation block sharpened to the full label phrase. Committed together since the rule and its guard cannot land apart. skills 376/376.
- 2026-07-18: T3 — AC3 amended via the step-6 gate (its grep-for-"inline" evidence self-hit the fix, M58/M59/M62); review step 10 rewritten to emit the handoff fenced.
- 2026-07-18: T4 — brief's manual-run prompt moved from a blockquote to a fenced block; release step 4's checklist names the fenced form.
- 2026-07-18: T5 — new `test_copy_run_handoffs.py` (7 tests) locks all three directives plus implement's mention-stays-inline; three mutation entries registered, all blank-and-fail verified. skills 383/383.
- 2026-07-18: review — PR #85; 3 lenses (5 findings, all diff-bug) + scorer; F1/F2/F3 (85/88/88) fixed on branch, F4/F5 (62/25) logged and fixed anyway; F5 not upheld as stated. All 6 AC ticked against fresh evidence. skills 385, scripts 174, hooks 72, validate 0.
- 2026-07-18: T6 — verify slot clean, exit codes checked separately: skills 383 (0), scripts 174 (0), hooks 72 (0), cairn_validate (0). Status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046). -->

**PR:** https://github.com/jmgirard/cairn/pull/85 · reviewed 2026-07-18 ·
no CI on this repo (`gh pr checks`: "no checks reported" — M16 lesson).

### Acceptance-criteria evidence (fresh, by command)

- **AC1** — all three labelled cases present in `tracking-rules.md`, each
  label on one physical line with its treatment: `:498` handoff → own fenced
  code block; `:499` naming → inline backticks; `:500` routing-chip option →
  neither fence nor handoff (cites D-022).
- **AC2** — `:496` names slash commands (`/clear`, `/milestone-plan`) as
  covered alongside shell commands.
- **AC3** — `grep -c "naming the obvious next action inline"` on
  `milestone-review/SKILL.md` returns **0** (the superseded instruction is
  gone); `:206` carries the replacement directive citing the copy-run rule.
- **AC4** — `milestone-brief/SKILL.md:43` and `cairn-release/SKILL.md:73`
  each name the fenced form at the point of handoff.
- **AC5** — `test_copy_run_handoffs.py` holds 7 tests across the three skills
  plus the implement mention-stays-inline pair; 3 entries registered in
  `test_mutation_harness.py`, and `TestRegisteredGuardsFailWhenBlanked`
  passing is live proof each directive's guard fails when its block is
  blanked. All four registered blocks verified to occur exactly once in
  their target files.
- **AC6** — verify slot clean, each exit code checked separately, no pipes
  (M56/M65): skills 383 (0), scripts 174 (0), hooks 72 (0),
  `cairn_validate` 21/21 (0).

### Consistency gate

`cairn_validate` all checks passed (15 PASS, 6 advisory OK). Toolchain half
is a clean no-op: the `generic` profile's `consistency-gate` slot names no
checks beyond the verify suites already re-run above. `cairn_impact` skipped
per its condition — `DESIGN.md` is untouched by the diff (GP3/GP4 are worked
*under*, not changed).

Additional author-side check: no new prose duplicates a phrase an existing
guard anchors on (M60/M80/M85) — `fenced` occurs 2× and `copy button` 1× in
`tracking-rules.md`, and no guard uses a bare substring anchor on either.

### Independent review — three lenses + scorer

- **[O] diff-bug:** 5 findings (below).
- **[S] blame-history:** 0 findings. Traced the `milestone-brief` blockquote
  to the plugin's initial commit — never a deliberate later choice, so
  replacing it loses nothing. D-004/D-019/D-022 and the D-036/037/038 wiring
  all verified intact.
- **[S] prior-PR-comments:** 0 findings. Confirmed PRs #63–#84 carry no
  inline GitHub comments, so cross-checked the archive Review sections
  instead; verified the 3 mutation blocks match their registered text
  byte-for-byte and the work-log's "three entries" claim is not stale
  (the M66 stale-count trap).

**Actioned (score ≥ 80) — all three fixed on the branch:**

- **F1 (85)** — `test_rulebook_polish.py:59` pinned only
  `"option → neither fence nor handoff"`, dropping the identifying label, so
  relabeling the exemption onto the case that must be fenced passed green.
  *Fixed:* the assert now carries the full label
  `a routing chip's \`→ /skill\` option → …`.
- **F2 (88)** — the slash-command anchor stopped at `"count as"`, leaving the
  predicate on the next physical line; inverting the rule to "count as
  mentions, never handoffs" satisfied it. *Fixed:* the sentence was moved onto
  one physical line and the assert now pins subject + predicate.
- **F3 (88)** — the handoff/mention asserts pinned only predicates, so
  transposing the two clauses inverted the rule (and reversed D-048(3)) with
  both asserts green. *Fixed:* the discriminator is now two labelled
  sub-bullets, each subject on one line with its verdict.

All three were the M74/M76 label-swap defect — in the very milestone whose
AC5 demands that discipline. The mutation harness could not have caught them:
it blanks, and blanking is not swapping. Verified by direct mutation instead —
relabeling F1's case, inverting F2's rule, and transposing F3's clauses each
turn the suite **red** (exit 1); the file was restored and re-verified byte-identical.

**Logged, below threshold (IP3 — surfaced, not dropped). Both fixed anyway,
per M73's "read every sub-80 finding's substance":**

- **F4 (62)** — `test_copy_run_handoffs.py`'s mention guard banned the literal
  words "fenced block" anywhere in `milestone-implement/SKILL.md`: wrong in
  both directions (an actual over-fire need not use those words; a legitimate
  fourth handoff site there — which D-048 anticipates — would redden it for an
  unrelated reason and invite deleting the guard). *Fixed:* replaced with a
  structural check that no fenced region in the file contains `/clear`, plus a
  self-test proving the detector fires — without it the loop is vacuous today,
  since that file has zero fenced regions (the M84 vacuity trap).
- **F5 (25)** — claimed the rule's worked example contradicts review step 10.
  **Not upheld:** step 10 keeps the descriptive sentence as unfenced prose and
  fences only the runnable lines — two textual units, no contradiction. The
  residue was real though: the rule omitted the actual distinguisher. *Fixed:*
  the mention branch now names it (a chip beside the line already offers the
  route), and a new sentence scopes the fence to the runnable lines only.

Post-fix re-verify: skills **385** (0), scripts 174 (0), hooks 72 (0),
`cairn_validate` 21/21 (0).
