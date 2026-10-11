<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M239: Compare low with default reasoning effort on cairn's Sonnet and Haiku roles

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — a measurement note under `cairn/references/` that no adopter reads   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m239-effort-roles   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A committed note measures, per role group, whether the group's model at `low` reasoning effort does its work for less money and with no loss of quality against the same model at default effort.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The three role groups and their nine tasks are those of
`cairn/references/haiku-sonnet-roles.md` (M228): search, edit work, and
history review. The note reuses that note's task prompts, answer keys, E1
target, mutant set, judge prompt, cost method, and verdict margin, and
changes only the effort setting. Search and history review run on Sonnet
and edit work on Haiku, the models the rulebook gives those roles today
(D-151). Each task runs once with the Agent tool's `effort` unset and once
with it set to `low`. Search and edit runs work in copies of commit
`c023018`, so M228's keys and target still hold. A one-word probe spawn
first shows which `effort` values the transcripts record. The note is
`cairn/references/effort-roles.md`.

**Out:** Naming an effort level in any skill or in the rulebook → the
`[low]` "Reasoning-effort dial per spawned agent" candidate row, acted on
after this note. The Opus roles (criteria audit and claim audit readers,
the diff-bug reviewer, design-sensitive work) → the same row, since no
replayable task with a scoring rule exists for them yet. A `medium` arm →
the same row, for a group whose verdict here is `default`. Repeated runs
per task → the note's re-measurement procedure. The old cost figures →
the "Re-measure the figures built with the old `cairn_cost.py`" row, which
this note does not rely on.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: `cairn/references/effort-roles.md` exists with its `INDEX.md`
      line and a `**Provenance.**` block. Its run table holds 18 rows: the
      nine tasks of `haiku-sonnet-roles.md`, each run once with the Agent
      tool's `effort` unset and once with it set to `low`, from that task's
      prompt in that note. Search and history-review rows set the model to
      Sonnet, and edit-work rows set it to Haiku.
- [ ] AC2: Each row records the distinct `model` values and the distinct
      `effort` values found on the assistant records of its subagent
      transcript.
- [ ] AC3: Each row's dollar cost follows the cost method of
      `haiku-sonnet-roles.md` (its Design section, Cost), with the
      per-token prices it uses tabulated in the note and cited to
      Anthropic's pricing page by URL and access date.
- [ ] AC4: Each row's score follows its group's scoring rule in
      `haiku-sonnet-roles.md`, with that note's answer keys, E1 target, and
      mutant set. Each history-review row's score comes from that note's
      judge prompt, with the task's two runs as reports A and B. The note
      records, per history-review task, the label mapping and the judge's
      rating of each finding under each label.
- [ ] AC5: The note gives each role group a verdict, which follows from the
      run table by this rule. The verdict is `untested` when any of the
      group's `low` rows records no `effort` value or any value other than
      `low`.
      Otherwise it is `low` exactly when the default rows' summed score is
      above zero, the `low` rows' summed cost is below the default rows',
      and the `low` rows' summed score is at least 0.9 times the default
      rows'. Otherwise it is `default`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3, T4, T5, T6
- AC2 → T1, T3, T4, T5
- AC3 → T6
- AC4 → T2, T3, T4, T5
- AC5 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Probe: spawn one-word subagents on Sonnet and on Haiku, each with
      `effort` unset and with `low`, and read the `model` and `effort`
      fields of their transcripts. Write the note's Provenance, Scope, and
      Design sections, fixed before any task run: the arms, the models,
      the pinned copies, and pointers to the reused M228 sections.
- [x] T2: Prepare the inputs: a `git archive c023018` copy for each search
      run, and for each edit run a fresh copy under git, so `git diff -U0`
      reads the run's changes; re-run M228's key code at `c023018` and
      confirm it reproduces the keys that note lists.
- [x] T3: Search runs: S1 to S3, each on Sonnet (`Explore` agent type) at
      both arms, pointed at a pinned copy; score by F1 against the keys.
- [x] T4: Edit runs: E1 to E3, each on Haiku (`general-purpose`) at both
      arms in its own copy; score E1 by Jaccard against the target and E2,
      E3 by mutants killed, under `PYTHONDONTWRITEBYTECODE=1`.
- [x] T5: History-review runs: H1 to H3, each on Sonnet at both arms. Then
      run one model-blind Opus judge per task, labels drawn before the judge
      runs and the mapping read after it returns.
- [x] T6: Price every row by the M228 cost method, re-reading the pricing
      page; fill the run table and the verdict table; write Limits and the
      re-measurement procedure; add the `INDEX.md` line; run
      `cairn_validate` and the `verify` slot.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: question set: what to plan (the request named no work) — effort level per subagent role.
- 2026-10-10: question set: which roles get a named effort level — measure before naming, so this milestone measures and changes no rule.
- 2026-10-10: inbox sweep: `gh` read 0 open issues and 0 open PRs on jmgirard/cairn, so nothing needs a disposition.
- 2026-10-10: collision check: the `[low]` "Reasoning-effort dial per spawned agent" row is promoted here, because its trigger (an Agent tool `effort` setting per spawn) fired at the 2026-10-10 triage. The row stays until post-merge hygiene (records-hygiene §1). M228 (done) built the reused tasks. D-026 rejects tool tiering, not effort. D-141 and D-151 set the per-role model shape. No standing rejection applies.
- 2026-10-10: the "Re-measure the figures built with the old `cairn_cost.py`" row does not fire: this note relies on M228's message-id cost method, not on the old figures.
- 2026-10-10: lessons harvested: M228's two returns were both on AC4 restating rules, so these criteria point at M228's sections instead of restating them. Mutant scoring runs under `PYTHONDONTWRITEBYTECODE=1` (M180). The zsh `path` and `====` gotchas (M133) apply to the session-local helpers.
- 2026-10-10: plan gate chose reusing M228's nine tasks, keys, mutants, and judge prompt over new tasks because they already passed review; falsified by a group whose two arms both sit at the scoring ceiling, as both models did on edit work in M228.
- 2026-10-10: plan gate chose two arms (unset and `low`) over three (adding `medium`) because `low` is the saving the rule can bank and a third arm adds nine runs; falsified by a `default` verdict in a group, which leaves `medium` unmeasured there (the candidate row holds that arm).
- 2026-10-10: plan gate chose the verdict `untested` for a group whose `low` rows do not record `low` over a criterion requiring every `low` row to record `low`, because the probe can show that a model ignores the setting; decided toward the narrower promise.
- 2026-10-10: criteria audit ran after the question set, because the request named no work until the set answered it.
- 2026-10-10: criteria audit (reduced mode, fresh Opus reader) returned 4 findings, all fixed. AC3 bound how prices were read, now the note's price table and citation. AC4 bound the label draw and read timing, now the note's per-task label mapping and ratings, with the timing kept in T5. AC4's judge clause counted tasks with no record, fixed by the same rewording. AC5 missed a `low` row with no `effort` value, now `untested`.
- 2026-10-10: implement started on branch m239-effort-roles; the untracked `cairn-probe.log` and `tsconfig.json` predate this milestone and stay unstaged.
- 2026-10-10: T1 probe: four one-word spawns show `effort` unset records `high` and `effort: "low"` records `low`, on Sonnet and on Haiku alike; the note's Design section is written and fixed before any task run.
- 2026-10-10: T2: twelve `git archive c023018` copies built in the session scratchpad (six search, six edit with a baseline commit); M228's key code re-run at `c023018` reproduces its listed keys (S1 10, S2 9, S3 88 items, set-equal).
- 2026-10-10: T3: six search runs on Sonnet; F1 per arm S1 1.0 and 1.0, S2 1.0 and 1.0, S3 0.6767 and 0.6767 (both arms listed the same 45 pairs, reading "supersede" by meaning). The first scoring pass read 0 for every run because the session-local scorer looked for the wrong field of the `SubagentHandback` call; the answer text is its `message` input.
- 2026-10-10: T4: six edit runs on Haiku; E1 Jaccard 1.0 in both arms (32-triple target), E2 and E3 6 of 6 mutants killed in both arms; the always-true control kills 0 of 6 for E2 and for E3.
- 2026-10-10: T5 in progress: six history-review runs done, three Opus judges spawned with labels drawn by `random.SystemRandom` and mappings written to a separate scratchpad directory before the judges ran. Cost method amended in the note: background runs carry no Agent tool `usage`, so the final call's output is the notification's `subagent_tokens` less the final id's input and cache counts (the identity holds on all five foreground spawns of this session).
- 2026-10-10: T5: judges returned H1 3 against 1, H2 1 against 1, H3 0 against 0 (default against `low`), mappings read after all three returned; no judge transcript names the mapping directory.
- 2026-10-10: T6: pricing page re-read, figures unchanged from M228's; verdicts search `low`, edit work `low`, history review `default`; every `low` row records only `low`. `cairn_validate` green; verify green after adding `effort-roles.md` (state `exempt`) to the pinned page ledger in `scripts/tests/test_scripts.py` (406 and 174 tests OK, both manifests valid, mod test 0 fail).
- 2026-10-10: claim audit: not owed — internal tier.
