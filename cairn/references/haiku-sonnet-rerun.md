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

## Runs

Agent ids name each run's transcript, `agent-<id>.jsonl` under the
Provenance directory. "Model ids" lists every `model` value on the
transcript's assistant records. "Final match" is the Cost section's
check. Token columns sum the row's calls. The table holds all 36 runs.

| Task | Model | Run | Agent id | Model ids | Calls | Final match | Input | 5m write | 1h write | Cache read | Output | USD | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | sonnet | 1 | `a5fa44942dbcaac97` | claude-sonnet-5-5 | 3 | yes | 6 | 38610 | 0 | 73296 | 596 | 0.1098 | 1.0000 |
| S1 | sonnet | 2 | `a00f30c574503fc75` | claude-sonnet-5-5 | 2 | yes | 4 | 38145 | 0 | 36015 | 1184 | 0.1108 | 1.0000 |
| S1 | sonnet | 3 | `a3ac6b2bf7defb9b3` | claude-sonnet-5-5 | 4 | yes | 8 | 38907 | 0 | 111129 | 607 | 0.1145 | 1.0000 |
| S1 | haiku | 1 | `ab074ab0515c0bc67` | claude-haiku-5-5 | 2 | yes | 4 | 38500 | 0 | 36012 | 1890 | 0.0061 | 1.0000 |
| S1 | haiku | 2 | `a2f88e4a086f2afb6` | claude-haiku-5-5 | 3 | yes | 6 | 38717 | 0 | 73510 | 1184 | 0.0062 | 1.0000 |
| S1 | haiku | 3 | `a5cf34128cbf6f2fd` | claude-haiku-5-5 | 3 | yes | 6 | 40230 | 0 | 74607 | 959 | 0.0063 | 1.0000 |
| S2 | sonnet | 1 | `a4cfe5355f7e959dd` | claude-sonnet-5-5 | 2 | yes | 4 | 37977 | 0 | 36034 | 550 | 0.1041 | 1.0000 |
| S2 | sonnet | 2 | `aca06eb53336304f4` | claude-sonnet-5-5 | 2 | yes | 4 | 37977 | 0 | 36034 | 392 | 0.1025 | 1.0000 |
| S2 | sonnet | 3 | `affc06843f6869a6e` | claude-sonnet-5-5 | 2 | yes | 4 | 37977 | 0 | 36034 | 613 | 0.1047 | 1.0000 |
| S2 | haiku | 1 | `ad1536ae5d6f244d4` | claude-haiku-5-5 | 4 | yes | 8 | 40055 | 0 | 111241 | 1257 | 0.0067 | 0.0000 |
| S2 | haiku | 2 | `a98ca5cc3038ed37f` | claude-haiku-5-5 | 2 | yes | 4 | 39080 | 0 | 36031 | 1018 | 0.0058 | 0.0000 |
| S2 | haiku | 3 | `a060daa2f00357e53` | claude-haiku-5-5 | 3 | yes | 6 | 39460 | 0 | 74721 | 1402 | 0.0064 | 0.0000 |
| S3 | sonnet | 1 | `a0dbbf387ce4eecb6` | claude-sonnet-5-5 | 2 | yes | 4 | 42088 | 0 | 36056 | 5726 | 0.1661 | 0.9943 |
| S3 | sonnet | 2 | `a163d212e2e8c931c` | claude-sonnet-5-5 | 2 | yes | 4 | 42147 | 0 | 36056 | 5891 | 0.1679 | 0.9885 |
| S3 | sonnet | 3 | `a1017c899f5bb6df8` | claude-sonnet-5-5 | 2 | yes | 4 | 42087 | 0 | 36056 | 4506 | 0.1539 | 0.6767 |
| S3 | haiku | 1 | `a7b94be94516e19e0` | claude-haiku-5-5 | 3 | yes | 6 | 54478 | 0 | 84600 | 11182 | 0.0132 | 1.0000 |
| S3 | haiku | 2 | `ab25b41baad6dee08` | claude-haiku-5-5 | 6 | yes | 12 | 63666 | 0 | 248381 | 1624 | 0.0113 | 0.9885 |
| S3 | haiku | 3 | `a406de22edbdf2c3b` | claude-haiku-5-5 | 6 | yes | 12 | 61946 | 0 | 237164 | 10183 | 0.0152 | 1.0000 |
| H1 | sonnet | 1 | `ad5ca596cd445f64a` | claude-sonnet-5-5 | 16 | yes | 32 | 102648 | 0 | 1296054 | 2428 | 0.4106 | 1 |
| H1 | sonnet | 2 | `adf66583d08739e3f` | claude-sonnet-5-5 | 14 | yes | 28 | 99585 | 0 | 1087480 | 2843 | 0.3862 | 1 |
| H1 | sonnet | 3 | `a18bcfa4bb7f1b852` | claude-sonnet-5-5 | 18 | yes | 36 | 104806 | 0 | 1475460 | 2027 | 0.4299 | 2 |
| H1 | haiku | 1 | `a1f27d60869af76e1` | claude-haiku-5-5 | 23 | yes | 46 | 130100 | 0 | 2164972 | 3712 | 0.1185 | 2 |
| H1 | haiku | 2 | `a4a149e195c5a845f` | claude-haiku-5-5 | 28 | yes | 56 | 130412 | 0 | 2636497 | 2747 | 0.1304 | 2 |
| H1 | haiku | 3 | `a46daa9cd67678f47` | claude-haiku-5-5 | 27 | yes | 54 | 146351 | 0 | 2750934 | 2978 | 0.1608 | 1 |
| H2 | sonnet | 1 | `accbfc9194281254e` | claude-sonnet-5-5 | 11 | yes | 22 | 80194 | 0 | 705830 | 1188 | 0.2830 | 1 |
| H2 | sonnet | 2 | `ad684dce613b57209` | claude-sonnet-5-5 | 8 | yes | 16 | 77358 | 0 | 468543 | 1452 | 0.2548 | 2 |
| H2 | sonnet | 3 | `a0805c385571c8bd8` | claude-sonnet-5-5 | 8 | yes | 16 | 74411 | 0 | 460465 | 1357 | 0.2457 | 1 |
| H2 | haiku | 1 | `af4ffaac1b2f500ed` | claude-haiku-5-5 | 15 | yes | 30 | 111645 | 0 | 1216797 | 2078 | 0.0652 | 1 |
| H2 | haiku | 2 | `a041a705f2f4fc13f` | claude-haiku-5-5 | 17 | yes | 34 | 115192 | 0 | 1470189 | 2752 | 0.0738 | 1 |
| H2 | haiku | 3 | `a5d21cc45d85c0529` | claude-haiku-5-5 | 13 | yes | 26 | 102507 | 0 | 982324 | 2169 | 0.0335 | 0 |
| H3 | sonnet | 1 | `a03dc8f1ce751188f` | claude-sonnet-5-5 | 12 | yes | 24 | 87761 | 0 | 743391 | 2144 | 0.3152 | 2 |
| H3 | sonnet | 2 | `a0f1a9715a0f3b69c` | claude-sonnet-5-5 | 13 | yes | 26 | 76919 | 0 | 754800 | 1124 | 0.2791 | 2 |
| H3 | sonnet | 3 | `a1d56d7cdc1f0a286` | claude-sonnet-5-5 | 13 | yes | 26 | 88882 | 0 | 832909 | 1852 | 0.3241 | 1 |
| H3 | haiku | 1 | `a652efb6e6608a6fd` | claude-haiku-5-5 | 29 | yes | 58 | 110546 | 0 | 2215176 | 2681 | 0.0657 | 1 |
| H3 | haiku | 2 | `a6b8b87ec86964b39` | claude-haiku-5-5 | 32 | yes | 64 | 140832 | 0 | 3233572 | 4356 | 0.1724 | 2 |
| H3 | haiku | 3 | `a3e2017d7562e7a09` | claude-haiku-5-5 | 21 | yes | 42 | 126854 | 0 | 1805648 | 5780 | 0.1074 | 2 |

Search notes. Every S1 and S2 Sonnet run and every S1 Haiku run scored 1.0. All
three Haiku S2 runs listed the nine registrations correctly but wrote each
script without its `.py` extension, so each scores 0. S3 Sonnet run 3
applied its own reading of which heading clauses supersede and listed 45
pairs, as M228's Sonnet run did. The other S3 runs followed the stated rule
and differ from the key by at most two pairs, from D-085's
"supersede-on-firing".

Judging. Each judge ran on Opus (`claude-opus-5-5`, read from its
transcript). The mappings were read after all nine judges returned. "Sonnet
label" names the label the Sonnet report carried. A rating list gives each
numbered finding of a report in order: V valid, I invalid. No finding was
rated a duplicate.

| Task | Run | Judge id | Sonnet label | Sonnet ratings | Sonnet valid | Haiku ratings | Haiku valid |
|---|---|---|---|---|---|---|---|
| H1 | 1 | `a9122ca7c75a06ec9` | B | I I I I V | 1 | I V V I I | 2 |
| H1 | 2 | `a6ce0b1608d1b0fd7` | B | V I I I | 1 | I V I I V | 2 |
| H1 | 3 | `a977c78c50e9976b7` | B | V V I I | 2 | I V I I | 1 |
| H2 | 1 | `abaa9f5a569079ec0` | B | V I I | 1 | I V | 1 |
| H2 | 2 | `abe4003ce49da45e0` | B | V I I V I | 2 | I V | 1 |
| H2 | 3 | `a53758de58d5e6991` | B | V I I I | 1 | I | 0 |
| H3 | 1 | `a184bfa5485d4bca2` | B | V V I | 2 | I I V | 1 |
| H3 | 2 | `aa75203b7c05ee2b5` | A | V I V I | 2 | V V | 2 |
| H3 | 3 | `a4fe8a23ba090403b` | A | I V I I I | 1 | I V V | 2 |

No reviewer or judge tool call named the mapping file or a path under
`cairn/references/`. No tool result carried text from the three earlier
notes (`haiku-sonnet-roles.md`, `effort-roles.md`,
`effort-review-medium.md`). Both checks ran over the 27 transcripts on
2026-10-16.
