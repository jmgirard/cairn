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
- **Branch/PR:** m239-effort-roles, https://github.com/jmgirard/cairn/pull/249   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [x] AC1: `cairn/references/effort-roles.md` exists with its `INDEX.md`
      line and a `**Provenance.**` block. Its run table holds 18 rows: the
      nine tasks of `haiku-sonnet-roles.md`, each run once with the Agent
      tool's `effort` unset and once with it set to `low`, from that task's
      prompt in that note. Search and history-review rows set the model to
      Sonnet, and edit-work rows set it to Haiku.
- [x] AC2: Each row records the distinct `model` values and the distinct
      `effort` values found on the assistant records of its subagent
      transcript.
- [x] AC3: Each row's dollar cost follows the cost method of
      `haiku-sonnet-roles.md` (its Design section, Cost), with the
      per-token prices it uses tabulated in the note and cited to
      Anthropic's pricing page by URL and access date.
- [x] AC4: Each row's score follows its group's scoring rule in
      `haiku-sonnet-roles.md`, with that note's answer keys, E1 target, and
      mutant set. Each history-review row's score comes from that note's
      judge prompt, with the task's two runs as reports A and B. The note
      records, per history-review task, the label mapping and the judge's
      rating of each finding under each label.
- [x] AC5: The note gives each role group a verdict, which follows from the
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
- 2026-10-10: step-7 approval: m239-effort-roles approved for merge

## Review
<!-- owner: review · exclusive -->

- AC1 evidence (2026-10-10, review pass 1): `effort-roles.md` exists, `INDEX.md` has 1 line naming it, 1 `**Provenance.**` block. A parse of the run table finds 18 rows over 18 distinct task-arm pairs. Each run's `agent-<id>.meta.json` records the requested model (`sonnet` on S and H rows, `haiku` on E rows) and `effort` (`low` on low rows, absent on default rows), and each run's first user message carries its task's prompt text from `haiku-sonnet-roles.md` (whitespace-collapsed anchor match, 18 of 18).
- AC2 evidence: a fresh re-run of the session-local cost script over the 18 transcripts gives each row's distinct `effort` and `model` values, and all 18 match the table's Effort and Model ids columns (0 mismatches): `high` on every default row, `low` on every low row, `claude-sonnet-5-5` on S and H rows, `claude-haiku-5-5` on E rows.
- AC3 evidence: the re-run cost script (message-id grouping, last-record counts, the note's price table, the Haiku 100,000-token tier) reproduces every row's five token sums, call count, and USD figure (0 mismatches over 18 rows). The note's price table equals the Sonnet 5.5 and both Haiku 5.5 rows of the pricing page read 2026-10-10, cited by URL and date. The final call's output comes from the completion notification's `subagent_tokens` less the final id's input and cache counts, the note's dated Cost amendment, because background runs have no Agent tool `usage`. On the five foreground spawns of this session, `totalTokens` equals the `usage` input, cache, and output sum, so both sources give the same figure. Every row's derived output is at least its recorded one.
- AC4 evidence: the re-run scorer gives S1, S2 1.0 and S3 0.6767 in both arms (F1 against keys that M228's key code rebuilds at `c023018`, set-equal to the note's lists), E1 1.0 in both arms (Jaccard against the 32-triple target), and E2, E3 6 of 6 mutants killed in both arms; the always-true control kills 0 of 6 for E2 and E3. Every S and E score equals the table (0 mismatches). H scores equal the judges' `A valid`/`B valid` lines under the recorded mappings (H1 3 and 1, H2 1 and 1, H3 0 and 0, default first). The note records each task's mapping and a rating per finding by arm, and the per-finding rows match the judges' lines.
- AC5 evidence: a parse of the run table, summed per group and run through the stated rule, gives search 0.3299 against 0.3247 USD at 2.6767 each, `low`; edit work 0.0293 against 0.0263 at 3.0 each, `low`; history review 0.8794 against 0.6002 at 4 against 2, `default`. No `low` row records an effort other than `low`, so none is `untested`. All three equal the note's verdict table.
- gate: `cairn_validate` exit 0 (no WARN); verify on the review head: scripts 406 tests OK (21 skipped), hooks 174 OK, plugin manifest valid (one warning, the repo-root `CLAUDE.md` not loaded as plugin context, present before this branch), marketplace manifest valid with no `plugins[N].version` warning, mod test 1609 tests 0 fail. No principle changed, so `cairn_impact` is skipped. Changelog: no entry owed, since the branch adds an in-repo reference note and a test-ledger line and changes no user-visible behavior.
- Copilot: requested on PR #249 at review start (state query `none`, `gh pr edit --add-reviewer @copilot` exit 0).
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: page wrongly `exempt` from the staleness advisory though it carries aging prices — fix now (Extraction names the dated price read, ledger pins `ok`), fixed 18ca241
- diff-bug #2: the Cost amendment changes the method AC3 binds to with no gate amendment — reject (false as an AC3 failure): the method's computation is unchanged, and the notification's `subagent_tokens` equals `totalTokens` on every foreground spawn, so the final-call figure is the one the method specifies; the dropped tie check is now stated in the note (diff-bug #3's fix)
- diff-bug #3: the amendment's check proves `totalTokens` = `usage`, not the `subagent_tokens` link it uses — fix now (the note states the `subagent_tokens` = `totalTokens` link and that M228's tie check is unavailable), fixed 18ca241
- diff-bug #4: search reversal written as a hypothetical though visible output is near the threshold — fix now (visible-output difference measured, about 390 tokens against 518), fixed 18ca241
- diff-bug #5: break-even figures from rounded USD — fix now (518 and 5,935 tokens, unrounded gaps stated), fixed 18ca241
- diff-bug #6: ledger entry has no rationale comment — fix now, fixed 18ca241
- diff-bug #7: edit cost omits test code and INDEX gives no reversal caveat — fix now, fixed 18ca241
- diff-bug #8: pointer places the scoring rules in the wrong section of M228's note — fix now, fixed 18ca241
- diff-bug #9: "M228's runs also record high" cites one transcript — fix now (all 18 read), fixed 18ca241
- blame-history #1: `exempt` pin undoes M228's deliberate `ok` for aging prices — fix now (same as diff-bug #1), fixed 18ca241
- blame-history #2: ledger entry without comment breaks the convention — fix now (same as diff-bug #6), fixed 18ca241
- blame-history #3: the history-review gap equals M228's run-to-run spread on the same reviewer — fix now (reading added, column "What could flip it"), fixed 18ca241
- blame-history #4: Verdicts table drops M228's "What could flip it" column — fix now, fixed 18ca241
- blame-history #5: weaker final check than M228's tie, `subagent_tokens` link unshown — fix now (same as diff-bug #3), fixed 18ca241
- blame-history #6: the "Reasoning-effort dial" ROADMAP row still says the Agent tool has no effort setting — follow-up: this milestone's post-merge hygiene rewrites that row with the verdicts
- blame-history #7: history-review runs could read M228's results in the live tree — fix now (transcripts checked: none names `haiku-sonnet-roles.md`, stated in the note), fixed 18ca241
- prior-review #1: `exempt` repeats the mistake M228 pass 1 fixed — fix now (same as diff-bug #1), fixed 18ca241
- prior-review #2: no "What could flip it" column — fix now (same as blame-history #4), fixed 18ca241
- prior-review #3: no reading that the score does not measure missed defects (D-016) — fix now, fixed 18ca241
- prior-review #4: ledger entry without comment — fix now (same as diff-bug #6), fixed 18ca241
- prior-review #5: Limits drops M228's judge-rule sensitivity caveat — fix now, fixed 18ca241
- prior-review #6: "cost gaps are small" and "cannot show a gap" are characterizations — fix now, fixed 18ca241
- prior-review #7: the Design heading says "fixed before any task run" though it holds a later amendment — fix now (heading names the one amendment), fixed 18ca241
- copilot: cairn/milestones/M239-effort-roles.md:14 — fix now (PR URL already recorded), fixed 872a42c
- copilot: cairn/references/effort-roles.md:11 — fix now (same as diff-bug #1), fixed 18ca241
- copilot: review body — noted (its two findings are the two threads above)
- Copilot level: Lite (set by GitHub's settings)
- conversation: jmgirard PR — noted (two empty-body reviews, GitHub's records of the two thread replies); 0 unresolved threads, 0 issue comments; Copilot state `reviewed earlier-head Lite`, no re-request.
- verify after fixes (18ca241): scripts 406 OK, hooks 174 OK, both manifests valid with no version warning, mod test 0 fail; `cairn_validate` exit 0 with no WARN.
