# Low against default reasoning effort on cairn's Sonnet and Haiku roles (M239)

**Provenance.** Ingested 2026-10-10 by M239 from first-hand runs: subagents
spawned with the Agent tool from a Claude Code desktop session in this repo,
each run's counts read from its subagent transcript under
`~/.claude/projects/-Users-jmgirard-github-cairn/0acf5eb5-22a4-47bd-bdaf-ea0b4c8a99c5/subagents/`.
Prices from Anthropic's pricing page (cited below). Tasks, keys, mutants, and
the judge prompt are those of `haiku-sonnet-roles.md` (M228), replayed at
commit `c023018`.
Pagination: —.
Extraction: the run records are first-hand from that day's session store, and a rerun reproduces the method, not the exact figures — observed 2026-10-10.

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

**Verdict rule.** Per group, sum each arm's cost and score over the
group's three tasks. The verdict is `untested` when any of the group's
`low` rows records no `effort` value or any value other than `low`.
Otherwise it is `low` exactly when the default arm's summed score is
above zero, the `low` arm's summed cost is below the default arm's, and
the `low` arm's summed score is at least 0.9 times the default arm's.
Otherwise it is `default`.
