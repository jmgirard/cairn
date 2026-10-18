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
Extraction: prices as `haiku-sonnet-roles.md` read directly from the pricing page 2026-10-09, and liable to change; the run records are first-hand from the 2026-10-16 session store, and a rerun reproduces the method, not the exact figures — observed 2026-10-16.

**Scope.** M228 compared Haiku 5.5 with Sonnet 5.5 on one run per task.
It gave search the verdict `stay` and history review `move`, on a 4-to-4
tie. D-151 kept both groups on Sonnet (observed 2026-10-16). This note
replays the same six tasks three times per model and states a verdict per
group. It changes no rule. The ROADMAP candidate "Haiku for the remaining
Sonnet roles" acts on the verdicts (observed 2026-10-16). The edit-work group, which D-151 moved to Haiku, is not
re-tested. This is a reference, not an authority. Status lives in
`ROADMAP.md`, decisions in `DECISIONS.md`.

## Design (fixed before any task run, 2026-10-16)

**Runs.** Six tasks of `haiku-sonnet-roles.md`: S1, S2, and S3 (search)
and H1, H2, and H3 (history review). Each task runs three times with the
Agent tool's `model` set to `sonnet`. It runs three times with `model` set
to `haiku`. A task's six runs all use that task's prompt, with `effort`
unset (D-157).
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
pairs, as M228's Sonnet run did. The other S3 runs followed the stated
rule. Haiku runs 1 and 3 match the key. Sonnet run 2 and Haiku run 2 miss
the two pairs from D-085's "supersede-on-firing". Sonnet run 1 misses
`D-116 D-108`, where D-108 follows "supersedes" in D-116's heading
(corrected at M264 review).

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

Per finding, in each report's own order. The short descriptions were
written at review from the uncommitted reviewer reports. The ratings are
the judges'.

| Task | Run | Model | # | Finding, in short | Rating |
|---|---|---|---|---|---|
| H1 | 1 | sonnet | 1 | Every pane open now runs git and gh calls | I |
| H1 | 1 | sonnet | 2 | Own-hotfix filter differs from milestone skill rule | I |
| H1 | 1 | sonnet | 3 | Hotfixes heading has no Refresh when list empty | I |
| H1 | 1 | sonnet | 4 | Zero-URL branch writes hotfixes but not prs | I |
| H1 | 1 | sonnet | 5 | Probe note says only a shell probe ran | V |
| H1 | 1 | haiku | 1 | Hotfixes Refresh missing until a hotfix PR exists | I |
| H1 | 1 | haiku | 2 | git helper not on PATH silently drops Hotfixes section | V |
| H1 | 1 | haiku | 3 | README and DESIGN still name only Blocked Refresh | V |
| H1 | 1 | haiku | 4 | Hotfix list written in a separate update call | I |
| H1 | 1 | haiku | 5 | Hotfix URL skips the prUrl check blocked rows get | I |
| H1 | 2 | sonnet | 1 | Stale docs and comments name only Blocked Refresh | V |
| H1 | 2 | sonnet | 2 | Hotfix list and word written in two updates | I |
| H1 | 2 | sonnet | 3 | Repos without blocked rows now make GitHub calls | I |
| H1 | 2 | sonnet | 4 | AC4 wording says seven cases, lists five | I |
| H1 | 2 | haiku | 1 | Unverified cwd option for git remote calls | I |
| H1 | 2 | haiku | 2 | List read is awaited before per-URL reads | V |
| H1 | 2 | haiku | 3 | No control to pick up a new hotfix PR | I |
| H1 | 2 | haiku | 4 | Words and list written in separate updates | I |
| H1 | 2 | haiku | 5 | PANE_BUTTONS comment names only Blocked Refresh | V |
| H1 | 3 | sonnet | 1 | Stale pane comments and docs name only Blocked Refresh | V |
| H1 | 3 | sonnet | 2 | Serial git and gh calls exceed the old wait bound | V |
| H1 | 3 | sonnet | 3 | No Refresh when no hotfix PR or blocked URL | I |
| H1 | 3 | sonnet | 4 | Zero-URL early return leaves prs unwritten | I |
| H1 | 3 | haiku | 1 | Remote URL with credentials would enter gh argv | I |
| H1 | 3 | haiku | 2 | Hotfix list read runs in series before PR reads | V |
| H1 | 3 | haiku | 3 | Words and list written in two separate updates | I |
| H1 | 3 | haiku | 4 | Zero-URL check now runs git and gh calls | I |
| H2 | 1 | sonnet | 1 | Inbox bullet line is 117 characters, not rewrapped | V |
| H2 | 1 | sonnet | 2 | Orphan line Step 7's issue in hotfix handoff | I |
| H2 | 1 | sonnet | 3 | Guest-mode bullet checked and consistent with lineage | I |
| H2 | 1 | haiku | 1 | Inbox filter still drops hotfix PRs from others | I |
| H2 | 1 | haiku | 2 | In-progress milestone PR is reported by no bullet | V |
| H2 | 2 | sonnet | 1 | Inbox bullet line is over-long despite rewrap claim | V |
| H2 | 2 | sonnet | 2 | Hotfix PRs from other authors reported nowhere | I |
| H2 | 2 | sonnet | 3 | Handoff text reverses M185 reports nothing wording | I |
| H2 | 2 | sonnet | 4 | Guest milestone slug can match hotfix bullet | V |
| H2 | 2 | sonnet | 5 | Milestone-plan sweep drops hotfix PRs unchanged | I |
| H2 | 2 | haiku | 1 | Inbox drops hotfix PRs from third parties | I |
| H2 | 2 | haiku | 2 | Claim that milestone PRs are reported is false | V |
| H2 | 3 | sonnet | 1 | Claimed rewrap did not happen, 117-character line | V |
| H2 | 3 | sonnet | 2 | Stranded Step 7's issue fragment left on short line | I |
| H2 | 3 | sonnet | 3 | Plan sweep still drops third-party hotfix PRs | I |
| H2 | 3 | sonnet | 4 | Handoff says reports open PR, true only same login | I |
| H2 | 3 | haiku | 1 | Inbox drops hotfix PRs whoever opened them | I |
| H3 | 1 | sonnet | 1 | Sequential reads can wait up to 30 seconds | V |
| H3 | 1 | sonnet | 2 | Third copy of the PR URL pattern | V |
| H3 | 1 | sonnet | 3 | Ragged wraps in new README and CHANGELOG text | I |
| H3 | 1 | haiku | 1 | Newest-100 window can drop author review | I |
| H3 | 1 | haiku | 2 | README does not say late items stay uncounted | I |
| H3 | 1 | haiku | 3 | Third copy of the PR URL regex | V |
| H3 | 2 | sonnet | 1 | Count call runs after gh pr view, doubling wait | V |
| H3 | 2 | sonnet | 2 | Newest-read guard race still untested | I |
| H3 | 2 | sonnet | 3 | Third copy of PR URL, no parity test | V |
| H3 | 2 | sonnet | 4 | OPEN_WORDS is a second list of open words | I |
| H3 | 2 | haiku | 1 | Each open PR can now wait 30 seconds | V |
| H3 | 2 | haiku | 2 | URL pattern anchored differently in third copy | V |
| H3 | 3 | sonnet | 1 | OPEN_WORDS adds a third hand-typed word list | I |
| H3 | 3 | sonnet | 2 | Wait widens an edge M224 already logged | V |
| H3 | 3 | sonnet | 3 | Newest-read guard race stays untested | I |
| H3 | 3 | sonnet | 4 | Fourth copy of PR URL pattern | I |
| H3 | 3 | sonnet | 5 | README has unwrapped 106 character line | I |
| H3 | 3 | haiku | 1 | Types file has no type check in verify | I |
| H3 | 3 | haiku | 2 | ROADMAP row still says 15 seconds per read | V |
| H3 | 3 | haiku | 3 | README and CHANGELOG wraps are ragged | V |

No reviewer or judge tool call named the mapping file or a path under
`cairn/references/`. No tool result carried text from the three earlier
notes (`haiku-sonnet-roles.md`, `effort-roles.md`,
`effort-review-medium.md`). Both checks ran over the 27 transcripts on
2026-10-16. A first check searched each whole transcript, and it matched
every transcript on the branch name `m264-haiku-sonnet-rerun` in the
context each agent receives. So the check reads only tool calls and tool
results. It cannot see text an agent saw any other way.

## Verdicts

Per task, the mean over three runs, with each score's range over its runs:

| Task | Sonnet score | Sonnet range | Haiku score | Haiku range | Sonnet USD | Haiku USD | Sonnet calls | Haiku calls |
|---|---|---|---|---|---|---|---|---|
| S1 | 1.0000 | 1.0000 to 1.0000 | 1.0000 | 1.0000 to 1.0000 | 0.1117 | 0.0062 | 3, 2, 4 | 2, 3, 3 |
| S2 | 1.0000 | 1.0000 to 1.0000 | 0.0000 | 0.0000 to 0.0000 | 0.1038 | 0.0063 | 2, 2, 2 | 4, 2, 3 |
| S3 | 0.8865 | 0.6767 to 0.9943 | 0.9962 | 0.9885 to 1.0000 | 0.1626 | 0.0132 | 2, 2, 2 | 3, 6, 6 |
| H1 | 1.3333 | 1 to 2 | 1.6667 | 1 to 2 | 0.4089 | 0.1366 | 16, 14, 18 | 23, 28, 27 |
| H2 | 1.3333 | 1 to 2 | 0.6667 | 0 to 1 | 0.2612 | 0.0575 | 11, 8, 8 | 15, 17, 13 |
| H3 | 1.6667 | 1 to 2 | 1.6667 | 1 to 2 | 0.3061 | 0.1152 | 12, 13, 13 | 29, 32, 21 |

| Group | Sonnet USD | Haiku USD | Sonnet score | Haiku score | Haiku ÷ Sonnet score | Verdict | What flips it |
|---|---|---|---|---|---|---|---|
| Search | 0.3781 | 0.0257 | 2.8865 | 1.9962 | 0.6916 | stay | A prompt that settles whether `.py` is part of S2's base name |
| History review | 0.9762 | 0.3092 | 4.3333 | 4.0000 | 0.9231 | move | One judged finding either way (score), and the output undercount (cost) |

Each verdict applies the design's rule to the sums above.

Readings that bear on the verdicts:

- Search is `stay`, as in M228. Haiku's deficit on S2 (1.0000) is larger
  than the net search gap (0.8903), because Haiku leads on S3. All three
  Haiku S2 runs dropped `.py`, so the miss is not run-to-run noise. The S2
  prompt asks for "the Python file's base name" and does not say whether
  the extension is part of it. So this gap can come from the prompt and
  not from the model's search. A reading that adds a missing `.py` to each S2 item
  scores every Haiku S2 run 1.0. Under it, Haiku's search score is 2.9962
  against Sonnet's 2.8865. That reading is outside the verdict rule, which
  was fixed before the runs. M277 (`haiku-search-clarified.md`) reran the
  search tasks with S2's base name stated to include `.py`, and gave
  search `move`.
- History review is `move`, as in M228, now on three runs per task. Haiku
  scored 12 judged-valid findings over its nine runs and Sonnet 13. The
  margin is one finding. One fewer Haiku finding makes Haiku's sum 3.6667
  (ratio 0.8462), and one more Sonnet finding makes the ratio 0.8571. Both
  are `stay`.
- Haiku scored lower on H2 in M228 (0 against 1) and here (0.6667 against
  1.3333). H2 is a skill-prose commit. H1 and H3 are pane-code commits.
- Haiku used more calls on every history task: a mean of 26 against 16
  on H1, 15 against 9 on H2, and 27.3 against 12.7 on H3. Of its 205
  history calls, 90 had a prompt over 100,000 tokens and paid the higher
  Haiku price. Even so, every Haiku history run cost less than every
  Sonnet run on the same task.
- Costs are lower bounds (see Cost). Take Sonnet's unrecorded output as
  zero and price Haiku's at its higher tier. If Haiku's unrecorded output
  then costs more than the gap, the group's cost comparison reverses.
  For history review the gap is 0.6670 USD. That is about 267,000 tokens,
  or about 4,100 per non-final Haiku call (65.3 such calls per group sum of
  means). M228's break-even was about 870 per call. For search the gap is
  0.3524 USD, about 18,400 tokens per non-final Haiku call. The final
  calls of the Haiku history runs recorded 2,078 to 5,780 output tokens
  per run (the Output column, almost all from the final call). The
  break-even is inside that range. Non-final calls that each produced as
  much output as a final call close the history gap. This note has no measure of non-final output.
- The score counts reported findings that the judge rated valid. It does
  not measure real conflicts that a reviewer missed. D-016 named that
  risk for a weaker model in a review step: it "can silently drop a real
  bug". This note does not test that risk. `history-review-recall.md`
  (M269) tests it with planted history conflicts.

## Limits and re-measurement

Three runs per model per task, three tasks per group, at default effort,
on tasks drawn from this repo. One Opus judge rates each run pair. In
M228, two judgings of the same 22 findings under two rules rated 11 of
them differently. That disagreement is larger than this note's
one-finding history margin. The measurement helpers were session-local and are not committed (observed
2026-10-16). To re-measure, follow the Design section with the same
models and prompts, and apply the verdict rule. A rerun that flips a
group's verdict falsifies this note's verdict for that group.
