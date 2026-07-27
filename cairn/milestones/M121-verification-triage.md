# M121: Verification triage — classify every self-verification instruction, and re-decide D-067's two fresh-context readers

- **Status:** planned
- **Priority:** normal
- **Depends on:** M120
- **Driving RR:** —
- **Principles touched:** IP3
- **Branch/PR:** —

## Goal

Classify every self-verification instruction in cairn's shipped prose against
the Opus 5 guide's over-verification finding, apply a recorded disposition to
each, and re-decide D-067's two fresh-context readers on the evidence of what
they have caught since adoption.

## Scope

**In:** a committed synthesis note holding the classification ledger; applying
every `narrow` and `remove` disposition to the shipped prose; a `DECISIONS.md`
entry disposing of D-067's criteria audit and description-layer certification
individually; a rulebook rule in "Model and agent strategy" naming which class
of self-checking the delegation guidance governs and which it does not.

**Out:** evidence-gathering instructions that run a command and read its output
— they are the guide's own preferred pattern and are classified `keep` in the
ledger without further work. The three RB tripwires and the Fable gate → not
touched; they gate escalation, not self-verification. A reasoning-effort dial
and a numeric spawn cap → candidate rows opened at M120. Any change to the
review fan-out's three lenses or its scorer → out; M120 owns the one review
change in this batch, and the lenses rest on M17's diff-blindness argument,
which no finding here disturbs.

## Acceptance criteria

- [ ] AC1 — `cairn/references/self-verification-ledger.md` exists, authored
      from `skills/shared/templates/synthesis-note.md`, and records: the search
      that produced the corpus, stated so a later pass can re-run it; one ID'd
      row per instruction found, carrying `file:line`, the instruction's own
      words, its mechanism classified as one of `command-evidence`,
      `fresh-context-reader`, or `same-context-recheck`, and a disposition of
      `keep`, `narrow`, or `remove` with a stated ground. Every count in the
      note is pinned to a named measurement commit and marked
      `— observed YYYY-MM-DD`. Its `INDEX.md` line, its provenance block, and
      its `TestShippedPageStateLedger` pin all land in the same milestone, with
      the work-log justification the ledger contract requires.
- [ ] AC2 — Every row dispositioned `narrow` or `remove` is applied in the
      shipped prose, and for each, a grep over the working tree for that row's
      quoted instruction returns hits only in the ledger, `cairn/DECISIONS.md`,
      milestone files, and `milestones/archive/`. No row lacks a disposition,
      and the count of rows in the ledger equals the count of hits the AC1
      search returns at the measurement commit.
- [ ] AC3 — A `cairn/DECISIONS.md` entry disposes of D-067's two instruments
      separately — the plan-gate criteria audit and the `guard-doctrine.md` §8
      description-layer certification — each as `keep unchanged`, `narrow`, or
      `retire`. The entry states, per instrument, what it caught across M115
      through M119, read from those milestones' Review sections and work logs
      and cited by file, against what it cost in rounds; it cites
      `prompting-opus-5` for the guide's finding. Any disposition other than
      `keep unchanged` names D-067 as superseded in the entry's heading; a
      `keep unchanged` restates D-067's own falsifier as still standing.
- [ ] AC4 — `tracking-rules.md`'s "Model and agent strategy" section states
      which class of self-checking the delegation guidance governs and which it
      does not, naming both an author re-checking its own output and an
      independent fresh-context reading of it. A prose-guard asserts a phrase
      from each of the two named classes, each phrase occurring within a single
      physical line of the shipped file, and each carries its own entry in
      `skills/tests/test_mutation_harness.py`.
- [ ] AC5 — Any instruction the ledger removes from a file carrying a
      prose-guard has that guard's asserted phrases re-checked against the
      shipped bytes, and `python3 -m unittest` over `skills/tests`,
      `scripts/tests` and `hooks/tests` is green from the repo root with each
      exit code checked separately.

## Coverage

- AC1 → T1, T2, T6
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T3, T5

## Tasks

- [ ] T1 — Run the corpus search over the nine `skills/*/SKILL.md` files and
      the five `skills/shared/*.md` modules; record the exact command and its
      raw hit list. Pin the measurement commit.
- [ ] T2 — Classify each hit by mechanism and author the ledger from the
      synthesis-note template, with a disposition and ground per row. A row is
      `same-context-recheck` only where the instruction has the agent re-read
      work it just produced, with the context that produced it.
- [ ] T3 — Apply every `narrow` and `remove` disposition to the shipped prose.
      After each edit, grep every nearby guard's asserted substring for
      contiguity on one physical line (LESSONS 2026-07-20/M104), and re-run the
      three suites with exit codes checked.
- [ ] T4 — Read M115–M119's Review sections and work logs for what each of
      D-067's instruments caught and what it cost; author the DECISIONS entry
      per AC3. Show it verbatim in chat before its commit.
- [ ] T5 — Write the self-checking-class rule into "Model and agent strategy";
      guard + per-phrase mutation entries; verify each reddens when blanked.
- [ ] T6 — `INDEX.md` line and `TestShippedPageStateLedger` pin for the ledger
      page, with the work-log justification line.

## Work log

- 2026-07-27: created by /milestone-plan.
- 2026-07-27: plan gate chose reopening D-067's two readers over triaging only the same-context rechecks, at the user's direction, because the guide's advice against subagent self-verification reaches them even though its stated mechanism (an author's own re-read) does not; falsified by the M115–M119 evidence showing either reader caught a defect no later gate would have.
- 2026-07-27: plan chose a committed synthesis note over an in-milestone ledger because the classification is the artifact a later re-decision re-reads, which is the owed-applied-to-time test; falsified by nothing outside this milestone citing the ledger.
- 2026-07-27: plan chose a search-scoped criterion over a list of the 19 instructions a plan-time subagent found because a criterion that lists its sites becomes the sweep and omits what it never named (LESSONS 2026-07-27/M118); falsified by the search returning a corpus a reader judges materially incomplete.

## Decisions

## Review
