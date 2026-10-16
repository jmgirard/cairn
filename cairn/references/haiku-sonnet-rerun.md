# Haiku 5.5 against Sonnet 5.5 on search and history review, three runs each (M264)

**Provenance.** Ingested 2026-10-16 by M264 from first-hand runs. The runs
are subagents spawned with the Agent tool from a Claude Code desktop
session in this repo. Each run's counts come from its subagent transcript
under
`~/.claude/projects/-Users-jmgirard-github-cairn/4d1bdd61-2546-4408-993c-fd281327a17a/subagents/`.
Tasks, keys, and the judge prompt are those of `haiku-sonnet-roles.md`
(M228), replayed at commit `c023018`. Prices are those
`haiku-sonnet-roles.md` lists.
Pagination: —.
Extraction: prices as `haiku-sonnet-roles.md` read directly from the pricing page 2026-10-09, and liable to change; the run records are first-hand from that day's session store, and a rerun reproduces the method, not the exact figures — observed 2026-10-16.

**Scope.** M228 compared Haiku 5.5 with Sonnet 5.5 on one run per task.
It gave search the verdict `stay` and history review `move`, on a 4-to-4
tie. D-151 kept both groups on Sonnet. This note replays the same six
tasks three times per model and states a verdict per group. It changes no
rule. The ROADMAP candidate "Haiku for the remaining Sonnet roles" acts on
the verdicts. The edit-work group, which D-151 moved to Haiku, is not
re-tested. This is a reference, not an authority. Status lives in
`ROADMAP.md`, decisions in `DECISIONS.md`.

## Design (fixed before any task run, 2026-10-16)

**Runs.** Six tasks of `haiku-sonnet-roles.md`: S1, S2, and S3 (search)
and H1, H2, and H3 (history review). Each task runs three times with the
Agent tool's `model` set to `sonnet`. It runs three times with `model` set
to `haiku`. All six runs use the same prompt, with `effort` unset (D-157).
Run index r is 1, 2, or 3. Agent types are M228's: `Explore` for search
and `general-purpose` for history review. Every spawn runs in the
foreground, so its Agent tool result carries `usage`.

**Pinned inputs.** Every search run reads its own `git archive c023018`
copy in the session scratchpad. Its prompt's repository path is replaced
by the copy's path, as in `effort-roles.md`. History-review runs read refs
of this repository, as in M228. Every ref they name predates `c023018`.

**Reused from `haiku-sonnet-roles.md`.** This note reuses four things from
that note. The first is the task prompts with the scoring rules they state
(Design, Search group, History-review group). The second is the answer
keys (Answer keys, target, and mutants). The third is the judge prompt,
and the fourth is the cost method (Design, Cost). `<LENS>` is the lens
paragraph of `skills/milestone-review/SKILL.md` at `c023018`. It runs from
the paragraph's bold name to the end of its bullet, with whitespace
collapsed. In it, `<default-branch>..HEAD` reads as `<SHA>^..<SHA>`.

**Judging.** One Opus judge rates each history task's run index r. It
reads the Sonnet run r report and the Haiku run r report under labels A
and B. The labels are drawn with `random.SystemRandom`. They are written
to a mapping file in the session scratchpad before the judge runs. The
mappings are read after all nine judges return. A run's score is the
judge's valid count for its label.

**Cost.** The M228 method groups records by `message.id`. Each id takes
its five class counts from its last record, times the model's price. A
Haiku call can have a prompt over 100,000 tokens, counting input, both
cache writes, and cache read. Such a call pays the higher row for every
class. The run's final id takes its output count from one Agent tool
result in the main session transcript
`~/.claude/projects/-Users-jmgirard-github-cairn/4d1bdd61-2546-4408-993c-fd281327a17a.jsonl`.
That result is the one whose `agentId` matches, and the count is its
`usage` output. "Final match" says whether that `usage`'s input and cache
counts equal the final id's last-record counts. Earlier calls keep the
stream-start output count. On the plan's audit reader that count was 5
and 7 tokens, where the final `usage` gave 878 (observed 2026-10-16). So
every row's cost is a lower bound.

**Verdict rule.** For each group and model, take each task's mean score
over its three runs. Take each task's mean cost the same way. Sum each
mean over the group's three tasks. If three things hold, the verdict is
`move`. Sonnet's summed score is above zero. Haiku's summed
cost is below Sonnet's. Haiku's summed score is at least 0.9 times
Sonnet's. Otherwise the verdict is `stay`.

Prices, USD per million tokens, as `haiku-sonnet-roles.md` lists them:

| Model | Input | 5m cache write | 1h cache write | Cache read | Output |
|---|---|---|---|---|---|
| Sonnet 5.5 | 2.00 | 2.50 | 4.00 | 0.10 | 10.00 |
| Haiku 5.5, prompt ≤ 100,000 tokens | 0.10 | 0.125 | 0.20 | 0.01 | 0.50 |
| Haiku 5.5, prompt > 100,000 tokens | 0.50 | 0.625 | 1.00 | 0.05 | 2.50 |
