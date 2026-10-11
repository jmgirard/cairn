# Low against default reasoning effort on cairn's Sonnet and Haiku roles (M239)

**Provenance.** Ingested 2026-10-10 by M239 from first-hand runs: subagents
spawned with the Agent tool from a Claude Code desktop session in this repo,
each run's counts read from its subagent transcript under
`~/.claude/projects/-Users-jmgirard-github-cairn/0acf5eb5-22a4-47bd-bdaf-ea0b4c8a99c5/subagents/`.
Prices from Anthropic's pricing page (cited below). Tasks, keys, mutants, and
the judge prompt are those of `haiku-sonnet-roles.md` (M228), replayed at
commit `c023018`.
Pagination: —.
Extraction: the run records are first-hand from that day's session store, with nothing to re-verify against, and a rerun reproduces the method, not the exact figures — observed 2026-10-10.

**Scope.** Measures, for each role group of `haiku-sonnet-roles.md`, whether
the model the rulebook gives that group (observed 2026-10-10: Sonnet for
search and history review, Haiku for edit work, D-151) does the group's work
at `low` reasoning effort for less money and with a score at least 0.9 times
its score at default effort. It records a measurement and a verdict per
group. It changes no rule: the ROADMAP candidate "Reasoning-effort dial per
spawned agent" acts on the verdicts. This is a reference, not an authority:
status lives in `ROADMAP.md`, decisions in `DECISIONS.md`.

## Design (fixed before any task run, 2026-10-10)

**Probe.** Four one-word spawns (`general-purpose`, prompt "Reply with the
single word: ready. Use no tools.") read on 2026-10-10. Each assistant
record of a subagent transcript carries an `effort` field and a
`message.model` field:

| Spawn | Agent id | `effort` values | `model` values |
|---|---|---|---|
| `model: "sonnet"`, `effort` unset | `ac2e8f74147970969` | high | claude-sonnet-5-5 |
| `model: "sonnet"`, `effort: "low"` | `a791d71bb625ac803` | low | claude-sonnet-5-5 |
| `model: "haiku"`, `effort` unset | `ac14210f28ec50955` | high | claude-haiku-5-5 |
| `model: "haiku"`, `effort: "low"` | `a8a8c7b91a68e96d2` | low | claude-haiku-5-5 |

So the default arm ran at `high` in this session. M228's runs, all with
`effort` unset, also record `high` (its S1 Sonnet transcript
`agent-a507fc85cce3e1c5d.jsonl`, read 2026-10-10).

**Arms.** Each of the nine tasks runs twice from the same prompt: once
with the Agent tool's `effort` unset (the default arm) and once with
`effort: "low"`. Search and history review set `model: "sonnet"`, edit
work `model: "haiku"`. Agent types are M228's: `Explore` for search,
`general-purpose` for edit work and history review. One run per arm per
task.

**Pinned inputs.** M228's search runs read the working tree, which moved
after `c023018`, and its edit runs used worktrees cut from that
day's HEAD. Here every search run reads its own `git archive c023018`
copy, and every edit run works in its own `git archive c023018` copy
with a baseline commit made in it, so `git diff -U0` reads the run's
changes. Each prompt's repository path is replaced by the copy's path,
and the edit prompts' "In this git worktree" by "In the git repository
at <copy>". History-review runs read refs of this repository, as in
M228, since every ref they name predates `c023018`.

**Reused from `haiku-sonnet-roles.md`.** The task prompts (Design,
Search group, Edit-work group, History-review group), the scoring rules,
the answer keys, the E1 target, and the mutant set (Answer keys, target,
and mutants), the judge prompt (Design, History-review group), and the
cost method (Design, Cost). The edit-work mutants are scored in a fresh
`git archive c023018` copy under `PYTHONDONTWRITEBYTECODE=1`, as there.
In the judge prompt, A and B are the two arms of one task, labels drawn
with `random.SystemRandom` and written to a mapping file before the
judge runs, and the mapping read after it returns.

**Cost.** The M228 cost method: records grouped by `message.id`, each
id's five class counts from its last record, times the model's price.
The run's final id takes its output count from the `usage` of the Agent
tool result whose `agentId` matches, in the main session transcript
`~/.claude/projects/-Users-jmgirard-github-cairn/0acf5eb5-22a4-47bd-bdaf-ea0b4c8a99c5.jsonl`.
Every row's cost is a lower bound, as there.

Amended 2026-10-10, after all 18 task runs: the task runs ran in the
background, and a background spawn's Agent tool result carries no `usage`.
The final call's output count therefore comes from the run's completion
notification in the main session transcript, whose `subagent_tokens`
figure, less the final id's input and cache counts from its last
transcript record, is that call's output. On the five foreground spawns of
this session (the four probes and the plan's criteria-audit reader), each
Agent tool result's `totalTokens` equals the sum of its `usage` input,
both cache-write, cache-read, and output counts, so the two sources give
the same figure there. Each row's "Final check" column says whether the
derived output is at least the output count the final id's last record
holds.

**Verdict rule.** Per group, sum each arm's cost and score over the
group's three tasks. The verdict is `untested` when any of the group's
`low` rows records no `effort` value or any value other than `low`.
Otherwise it is `low` exactly when the default arm's summed score is
above zero, the `low` arm's summed cost is below the default arm's, and
the `low` arm's summed score is at least 0.9 times the default arm's.
Otherwise it is `default`.

Prices, USD per million tokens, from
<https://platform.claude.com/docs/en/about-claude/pricing> (read
2026-10-10, the same figures `haiku-sonnet-roles.md` lists for 2026-10-09).
A Haiku call whose prompt (input, both cache writes, and cache read) is
over 100,000 tokens pays the higher row for every class.

| Model | Input | 5m cache write | 1h cache write | Cache read | Output |
|---|---|---|---|---|---|
| Sonnet 5.5 | 2.00 | 2.50 | 4.00 | 0.10 | 10.00 |
| Haiku 5.5, prompt ≤ 100,000 tokens | 0.10 | 0.125 | 0.20 | 0.01 | 0.50 |
| Haiku 5.5, prompt > 100,000 tokens | 0.50 | 0.625 | 1.00 | 0.05 | 2.50 |

## Runs

Agent ids name each run's transcript, `agent-<id>.jsonl` under the
Provenance directory. "Effort" and "Model ids" list every value on the
transcript's assistant records. "Final check" is the Cost amendment's
check. Token columns sum the row's calls. No Haiku call went over the
100,000-token prompt tier.

| Task | Arm | Agent id | Effort | Model ids | Calls | Final check | Input | 5m write | 1h write | Cache read | Output | USD | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | default | `a313c2fdde2a0db1c` | high | claude-sonnet-5-5 | 3 | yes | 6 | 35533 | 0 | 66419 | 715 | 0.1026 | 1.0000 |
| S1 | low | `ad385e809f1ad94f3` | low | claude-sonnet-5-5 | 3 | yes | 6 | 33284 | 0 | 64948 | 407 | 0.0938 | 1.0000 |
| S2 | default | `ab3c345c76a7eb50e` | high | claude-sonnet-5-5 | 2 | yes | 4 | 34115 | 0 | 32166 | 637 | 0.0949 | 1.0000 |
| S2 | low | `ad9df3ca770a33748` | low | claude-sonnet-5-5 | 2 | yes | 4 | 34117 | 0 | 32166 | 366 | 0.0922 | 1.0000 |
| S3 | default | `a67a24ab58c24a121` | high | claude-sonnet-5-5 | 2 | yes | 4 | 38226 | 0 | 32188 | 3357 | 0.1324 | 0.6767 |
| S3 | low | `a8d07da9840b55494` | low | claude-sonnet-5-5 | 3 | yes | 8 | 40422 | 0 | 70412 | 3062 | 0.1387 | 0.6767 |
| E1 | default | `ada3cd96f1bc738b5` | high | claude-haiku-5-5 | 4 | yes | 8 | 55345 | 0 | 150049 | 700 | 0.0088 | 1.0000 |
| E1 | low | `ab393283fa0c7358e` | low | claude-haiku-5-5 | 6 | yes | 12 | 54229 | 0 | 254294 | 912 | 0.0098 | 1.0000 |
| E2 | default | `a42a88991a752134b` | high | claude-haiku-5-5 | 5 | yes | 10 | 60754 | 0 | 209136 | 580 | 0.0100 | 1.0000 |
| E2 | low | `a5463a36c5869cf8d` | low | claude-haiku-5-5 | 4 | yes | 8 | 56900 | 0 | 154413 | 340 | 0.0088 | 1.0000 |
| E3 | default | `a92a33da04641a9a1` | high | claude-haiku-5-5 | 7 | yes | 14 | 57167 | 0 | 311640 | 477 | 0.0105 | 1.0000 |
| E3 | low | `aece8ce4d3b6b9ee3` | low | claude-haiku-5-5 | 3 | yes | 6 | 52425 | 0 | 96920 | 303 | 0.0077 | 1.0000 |
| H1 | default | `aa3398a8cbe013dcd` | high | claude-sonnet-5-5 | 16 | yes | 32 | 93647 | 0 | 1167753 | 2735 | 0.3783 | 3 |
| H1 | low | `a634df029fd93f118` | low | claude-sonnet-5-5 | 4 | yes | 8 | 72519 | 0 | 179990 | 1064 | 0.2100 | 1 |
| H2 | default | `a19090c5879113da4` | high | claude-sonnet-5-5 | 8 | yes | 16 | 69133 | 0 | 422133 | 1133 | 0.2264 | 1 |
| H2 | low | `a5d0d806ae26fc33b` | low | claude-sonnet-5-5 | 4 | yes | 8 | 58665 | 0 | 156351 | 682 | 0.1691 | 1 |
| H3 | default | `a358c3f0ff2386c3e` | high | claude-sonnet-5-5 | 11 | yes | 22 | 78742 | 0 | 653107 | 1248 | 0.2747 | 0 |
| H3 | low | `a644db04aceec02b6` | low | claude-sonnet-5-5 | 10 | yes | 20 | 64587 | 0 | 511186 | 849 | 0.2211 | 0 |

Search notes. Every run listed the same S1 and S2 items as the key. On
S3 both arms listed the same 45 pairs, all in the key, reading "supersede"
by meaning where the prompt's rule counts every id after the word (88
pairs). M228's Sonnet run did the same. The first scoring pass read 0 for
every search run because the session-local scorer read the wrong field of
the `SubagentHandback` call. The answer text is its `message` input, and
the scores above are from the corrected pass.

Edit-work notes. Both E1 runs produced the 32-triple target diff exactly.
All four test files passed on the unmutated code and killed all six
mutants: 24 and 25 tests at default, 30 and 15 at `low`. A file holding
one always-true test kills 0 of 6 for E2 and 0 of 6 for E3 (re-run
2026-10-10), so the mutant scoring can tell runs apart, but both arms
reached 1.0 on every task, as both models did in M228.

Review notes. Judges (Opus, `claude-opus-5-5`, effort `high` on every
record): H1 `a77a1ccdfb8b84875`, H2 `a9acd640dd5954ffe`, H3
`af133335d2a3fc529`. Each judge read its two report files from a
`judge/reports/` directory of the session scratchpad. The label mappings
were drawn with `random.SystemRandom` and written to a separate
`judge/mapping/` directory before the judges ran, and no judge transcript
contains that directory's path. The mappings, read after all three
judges returned: H1 A default, B `low`; H2 A default, B `low`; H3 A
`low`, B default. No finding was rated a duplicate. Both H3 reports
found no regression: the `low` report has no numbered finding, and the
default report's five numbered items each conclude that a past point
"holds", so the judge rated all five invalid.

Per-finding ratings (V valid, I invalid; the number is the reviewer's own):

| Task | Arm | # | Finding, in short | Rating |
|---|---|---|---|---|
| H1 | default | 1 | `register.tsx` comments still name only the Blocked heading's Refresh, though the review log says fixed | V |
| H1 | default | 2 | `collaborationMode` in `reader.ts` is a second parser of the mode line | I |
| H1 | default | 3 | an older M224 sentence in DESIGN.md disagrees with the new M226 text | V |
| H1 | default | 4 | `readPrs` no longer makes no calls when no blocked row has a URL | V |
| H1 | default | 5 | the `hotfix-` filter misses adopted PRs | I |
| H1 | default | 6 | `/hotfix` step 6 still says nothing reports an open hotfix PR | I |
| H1 | low | 1 | `readHotfixes` runs before the parallel reads and delays the blocked words | V |
| H1 | low | 2 | a third hand-kept copy of the mode rule | I |
| H1 | low | 3 | no Refresh when there is no hotfix PR and no blocked URL | I |
| H1 | low | 4 | the DESIGN.md parenthetical grows again | I |
| H2 | default | 1 | the commit promises a rewrap, but the line is 117 characters | V |
| H2 | default | 2 | a ragged wrap in the hotfix skill | I |
| H2 | default | 3 | someone else's `hotfix-*` PR is still reported nowhere | I |
| H2 | default | 4 | the guest handoff keeps M185's intent | I |
| H2 | low | 1 | the commit promises a rewrap, but the line is 117 characters | V |
| H2 | low | 2 | someone else's `hotfix-*` PR is still reported nowhere | I |
| H2 | low | 3 | the plan skill's inbox has the same drop | I |
| H2 | low | 4 | the hotfix handoff change is correct | I |
| H3 | default | 1–5 | five past review points, each found to hold | I (each) |

## Verdicts

| Group | Default USD | Low USD | Default score | Low score | Low ÷ default score | Verdict |
|---|---|---|---|---|---|---|
| Search | 0.3299 | 0.3247 | 2.6767 | 2.6767 | 1.0000 | low |
| Edit work | 0.0293 | 0.0263 | 3.0000 | 3.0000 | 1.0000 | low |
| History review | 0.8794 | 0.6002 | 4 | 2 | 0.5000 | default |

Every `low` row records only `low`, so no group is `untested`. Each
verdict applies the rule fixed in the Design section to the sums of the
run table.

Readings that bear on the verdicts:

- History review is `default`. The whole gap is H1, 3 valid findings
  against 1, where the `low` run made 4 calls against the default run's
  16. H2 tied at 1 against 1, and H3 found no valid finding in either arm.
- Search and edit work tie on score, and their cost gaps are small: $0.0052
  (1.6%) for search and $0.0030 (10%) for edit work. Costs are lower bounds
  (see Cost). Taking the default arm's unrecorded output as zero, the
  search comparison reverses if the `low` arm's five non-final calls left
  more than 520 output tokens unrecorded at Sonnet's output price, about
  104 per call. The edit comparison reverses at 6,000 unrecorded tokens
  over the `low` arm's ten non-final Haiku calls, about 600 per call. So
  the search verdict says `low` costs no more at an equal score. It does
  not show a saving.
- The default arm ran at `high`, so these verdicts compare `low` with
  `high`, the level a spawn with `effort` unset received in this session.
- Edit work sits at the scoring ceiling in both arms, as both models did
  in M228. The tasks cannot show a gap on harder edits.

## Limits and re-measurement

One run per arm per task, three tasks per group, on tasks drawn from this
repo. The judge is one Opus reader per task. No Opus role was measured.
The measurement helpers (key builder, scorer, cost script) were
session-local and are not committed (observed 2026-10-10). To re-measure:
re-run the nine task prompts of `haiku-sonnet-roles.md` against fresh
`git archive c023018` copies with `effort` unset and set to `low`, read
each run's `effort` and `model` values and its counts from its subagent
transcript, take the final call's output as the Cost amendment states,
score with M228's keys, target, mutants, and judge prompt, and apply the
verdict rule. A rerun that flips a group's verdict falsifies this note's
single-run verdict for that group.
