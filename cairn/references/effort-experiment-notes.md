# The high→medium reasoning-effort experiment, measured across five repos

**Provenance.** Ingested 2026-08-08 from the local Claude Code session stores
(`~/.claude/projects/<slug>/*.jsonl` — the `effort` field on every record, plus
`message.usage` and `gitBranch` per M94's method) and from the milestone
archives and git logs of five cairn-tracked repos: cairn, intraclass,
tidymedia, circumplex, hitop. Archive review lines were read by two
fresh-context readers; cost figures computed with the M94 attribution method
(`scripts/cairn_cost.py` conventions). Observed 2026-08-08; the stores are
live append logs, so every figure is a snapshot.
Extraction: first-hand read of this machine's session stores and the five repos' own archives, nothing to re-verify against — the stores append live, so a re-run reproduces the method rather than the exact figures — observed 2026-08-08.

**Scope.** Records the evidence gathered on Jeff's effort experiment —
switching Opus 5 / Fable 5 from `high` to `medium` reasoning effort — and the
comparison method, so a later re-measurement has a baseline and a procedure.
It is a measurement with a stated recommendation, not a rule: nothing here
binds a session to an effort level. Standard disclaimer: this is a reference,
not an authority — status lives in `ROADMAP.md`, decisions in `DECISIONS.md`,
architecture in `DESIGN.md`.

## The switch, dated

The session store writes `effort` on every assistant record. Across all
project stores: every turn through 2026-07-30 ran `high`; every turn from
2026-07-31 on ran `medium`. Model is roughly constant across the boundary
(claude-opus-5 / claude-fable-5 from 2026-07-26 on; claude-opus-4-8 before
that), so the cohorts below are close to an effort-only comparison:

- **High cohort:** milestones merged ~2026-07-23 … 2026-07-30 (this repo:
  M113–M127).
- **Medium cohort:** milestones merged 2026-07-31 … 2026-08-08 (this repo:
  M128–M136).

## Cost — medium ≈ half price per milestone

This repo, branch-attributed per M94 (plan phase excluded per A3):

| Cohort | n | turns median | output median | cache-read/turn |
|---|---|---|---|---|
| High, M113–M127 excl. M114 outlier | 14 | 314 | 366k | ~200–330k |
| Medium, M128–M136 | 9 | 165 | 169k | ~200–260k |

Cache-read per turn is similar in both eras, so total cost scales with turns:
roughly a **50% cut per milestone**. Throughput rose visibly — 2026-07-31
alone merged eight hitop milestones and four intraclass milestones.

## Quality — more (cheaper) returns, slightly more escapes

Per-repo review-thrash tally from archive `**Review:**` lines and git logs:

| Repo | High: returned/total | Medium: returned/total | Post-merge defects high→medium |
|---|---|---|---|
| cairn | ~6/15 (incl. 8-pass M114, 7-round M123) | 3/9 (all single-defect returns) | 0 → 0 |
| intraclass | 2/8 (7-pass M92, 10-pass M93) | 6/16 (+ M100/M101 dropped per its D-021) | 0 → 2 |
| tidymedia | 3/8 | 5/12 | 1 → 0 |
| circumplex | 2/8 | 7/9 | 0 → 2 |
| hitop | 0/8 | 4/11 | 2 → 1 |
| **pooled** | **14/47 (30%)** | **25/57 (44%)** | **3 → 5** |

Readings that temper the raw return-rate increase:

- **Severe thrash (3+ passes or a re-cut) did not increase:** ~17% high vs
  ~14% medium. The worst disasters are all high-era (intraclass M93: 10
  passes, 3 re-cuts; cairn M114: 8 passes).
- **Known confound, direction stated:** M130's defect-return floor (merged
  2026-08-02, shared to every repo via the plugin symlink) made returns
  mandatory where previously discretionary — it *inflates* the medium
  cohort's return count, so the true quality gap is smaller than 30%→44%
  reads. The other anti-thrash milestones (M114, M125) cut the other way.
- **Review detection rate held:** medium-era reviews still action findings
  in the 82–97 range at comparable per-milestone rates, so the gate did not
  go quiet — first drafts carry more defects, and the gate absorbs them at
  one cheap round each.

The genuinely adverse signal is **escaped defects** (5 medium vs 3 high),
concentrated in circumplex's norms-ingestion work: the interleaved iei norms
defect broke `norm_standardize()` post-merge (fixed 2026-08-07, its #99), and
the CAIS out-of-range means shipped (fixed 2026-08-08; that commit's own
analysis says provenance auditing could not have caught it, since shipped
values matched the source). Circumplex is also the return-rate outlier (7/9).

## Recommendation (as of 2026-08-08)

**Keep medium as the default.** Half the cost, higher throughput, no increase
in catastrophic thrash; the elevated return rate is partly the stricter
return floor, and the review gate contains the residual quality gap at one
extra round per affected milestone.

**Exception:** statistically delicate, data-heavy ingestion of the
circumplex-norms variety — where a wrong value passes review because it looks
plausible — leans the other way. For that class, run the session on high or
escalate through `/milestone-brief` (RB/RR); those are exactly the defects
that escaped to main under medium.

## Re-measurement procedure

1. Effort timeline: tally `effort` × day over `~/.claude/projects/*/**.jsonl`
   assistant records.
2. Cost: M94 method — per-milestone turns/output via `gitBranch`, four token
   classes kept separate, plan phase unattributable (A3), subagent tokens
   unrecorded (A4).
3. Thrash: archive `**Review:**` lines — rounds/passes, returns (defect vs
   amendment), actioned ≥80 counts.
4. Escapes: git log per repo for hotfix/fix/revert commits landing after a
   milestone's merge, attributed to its files.

## Open questions

- Whether the medium-era escape rate persists once the M130 floor and the
  norms-batch work are out of the window — worth re-running after ~10 more
  medium milestones.
- Whether high effort on circumplex-class ingestion actually prevents the
  escaped defects, or whether (per the CAIS analysis) they are
  process-invisible at any effort.
