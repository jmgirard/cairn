# RB03: The lifecycle of rationale — an architectural audit of accumulation across cairn's always-read files (M95)

- **Date:** 2026-07-19
- **Output required:** write findings to `cairn/reviews/RR03-rationale-lifecycle-architecture.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

cairn is a Claude Code plugin that gives a repo a milestone-based tracking
system. It ships skills (`skills/*/SKILL.md`), a shared rulebook
(`skills/shared/tracking-rules.md`), validation scripts (`scripts/`), and
hooks (`hooks/`). It dogfoods its own format under `cairn/`.

Four files are read at or near every session start:

| File | Lines | Chars | Governing mechanism |
|---|---|---|---|
| `skills/shared/tracking-rules.md` | 765 | 52,316 | **none** — no cap on either axis |
| `cairn/DECISIONS.md` | 1,425 | 95,374 | append-only (IP4); can never shrink |
| `cairn/LESSONS.md` | 48 | 20,484 | line cap <50, char threshold <20,500, retirement (D-051) |
| `cairn/ROADMAP.md` | 43 | 14,875 | line cap <60, char threshold <21,000 |

A `/milestone-plan` session start reads roughly **183,000 characters (~45k
tokens) before any work begins.**

Two prior Fable reviews are archived and should be read: `cairn/reviews/archive/RR01-architecture-retrospective.md`
and `cairn/reviews/archive/RR02-weight-management-architecture.md` (with their
briefs RB01/RB02 alongside). RR02 (2026-07-19) diagnosed rulebook growth as
"the rulebook restating D-entry context it does not own" and recommended a
one-time editorial pass (rec 1) returning it to ~550–600 lines with zero rules
removed.

**Milestone M95 was cut to execute RR02 rec 1, and stopped at its
implementation gate because its premise did not survive contact with the
evidence.** That failure is this brief's primary input.

### What M95 found

M95 inventoried 21 candidate "restated rationale" blocks in the rulebook and
verified each against `DECISIONS.md`, quoting the proving text. The full
per-block ledger is in the work log of
`cairn/milestones/M95-rulebook-editorial-slimming.md` (entries prefixed
`LEDGER B1`…`LEDGER B21`). Read it. Results:

- **9 of 21 blocks have no D-entry home at all.** The rulebook is their *only*
  home. Notably B17 (`tracking-rules.md:686-697`), the entire "standing facts
  vs. dated observations" doctrine — a substantial, mutation-registered,
  operative paragraph with **zero** footprint in `DECISIONS.md`.
- **14 of 21 are guard-pinned**, several mutation-registered. Under M95's AC2
  ("a rule is what reddens a guard when deleted or inverted") those are rules,
  not rationale.
- **RR02's flagship example is wrong.** RR02 §1(c) cites `tracking-rules.md:91-94`
  ("LESSONS.md sat at 49 lines … character mass grew 13% … nothing reported it")
  as a restatement of D-049's Context. D-049's Context states a *contrary* fact:
  "LESSONS held 36 lessons from M41 through M83 and 29 since, **never approaching
  50**." D-051's superficially similar "49 lines" is a third, different fact.
  Verified by hand.
- **Measured removable yield: ~35–40 lines (~5%)**, against RR02's projected
  22–28%.

So the rulebook is not primarily *restating* `DECISIONS.md`. For a large share
of this text it is the sole home of doctrine, and the remedy RR02 prescribed
("delete the restatement") has nothing to delete back to. The honest remedy —
author the missing D-entries, *then* slim — was explicitly out of M95's scope
and is a different milestone shape.

### The second, possibly deeper observation

`cairn/LESSONS.md` was never examined by RB01 or RB02. It is now at **20,484 of
20,500 characters — 16 characters of headroom** — with 31 item lines averaging
**630 characters**. D-051's Context recorded 20,466 chars at M92, the milestone
that *gave it a retirement outflow*. It has grown net since acquiring the
mechanism meant to shrink it.

Its lessons are visibly accreting rather than retiring: `(M53, extended M54,
trimmed M92)`, `(M56+M65, consolidated M78/M83)`, `(M87, extended M90/M91,
consolidated M92)`, `(M71, corrected M75, consolidated M92)`.

D-049 states the mechanism plainly, for thresholds:

> The mean is *measured*, never assumed or carried over: compression is the
> prescribed weight remedy and consolidating items raises the mean, so the
> derivation's own input moves every time the remedy is applied.

**The prescribed remedy for the weight axis (compress / consolidate in place)
is the mechanism that drives the weight axis.** The item axis stays green
because items merge; the mass grows because merging preserves content. The same
shape appears in all three files. The maintainer reports this as a recurring
problem in other cairn-adopting repos, not just here.

### Why this needs independent review

Nine milestones of weight-management work (M84–M94) have produced per-file
mechanisms — density thresholds, a non-item line cap, a proposed growth ratchet
(M96), a proposed bounded read (M97) — and RR02's own "Beyond the brief" notes
that **weight governance is the largest single contributor to the growth it
exists to govern** (the Weight-caps section grew 22→81 lines since RB01,
exceeding the extraction savings it was measuring). Each mechanism was derived
in isolation for one file. None asks where rationale *should* live or what its
lifecycle is. This review is that question.

## Materials

Read, in this order:

1. `cairn/milestones/M95-rulebook-editorial-slimming.md` — especially the
   `LEDGER B1`–`LEDGER B21` work-log entries (the primary evidence).
2. `skills/shared/tracking-rules.md` — the whole file (765 lines). Pay
   attention to `## Weight caps` (81 lines), `## Universal tracking rules`
   (72), `## References pages` (67), `## Output & interaction discipline` (98).
3. `cairn/LESSONS.md` — the whole file (48 lines).
4. `cairn/DECISIONS.md` — do **not** read whole (95k chars). Scan the 52
   `### D-` headings, then read these entries whole: **D-015** (LESSONS
   created), **D-030** (milestone cap / Review exemption), **D-031** (domain
   doctrine gets a module), **D-032** (IP4 named), **D-045** (history vs.
   current knowledge), **D-046** (work-log exemption), **D-049** (density
   thresholds), **D-050** (release timing), **D-051** (lesson retirement),
   **D-052** (non-item line cap; ROADMAP as current knowledge).
5. `cairn/reviews/archive/RR01-architecture-retrospective.md` and
   `cairn/reviews/archive/RR02-weight-management-architecture.md`.
6. `cairn/DESIGN.md` — the IP/GP principle block (GP1 and IP4 especially).
7. `cairn/ROADMAP.md` — the Candidates section, for what is already parked.

Measurement commands (run from repo root; `char_count` counts **characters,
not bytes** — `wc -c` overcounts by ~1% on this corpus because of em-dashes):

```
python3 -c "import pathlib;[print(f'{p}: {len(pathlib.Path(p).read_text().splitlines())} lines, {len(pathlib.Path(p).read_text())} chars') for p in ['skills/shared/tracking-rules.md','cairn/DECISIONS.md','cairn/LESSONS.md','cairn/ROADMAP.md']]"
python3 scripts/cairn_validate.py
```

## Questions

1. **Where should rationale live?** cairn's stated boundary is
   `tracking-rules.md:11-13`: "Substance lives in the owner; any other file
   gets at most a one-line cross-reference," with `DECISIONS.md` owning
   "cross-cutting decisions" and the rulebook owning rules. M95 found 9 of 21
   sampled rulebook blocks have no D-entry at all. Is that a **defect**
   (rationale that should have been recorded as D-entries and was not), or is
   it **correct** (some rationale is genuinely rule-like and belongs in the
   rulebook)? Give a decision procedure an author can apply at authoring time
   to place a new piece of rationale, and say what it implies for the 9 blocks.

2. **Is "guard-pinned ⇒ rule" a sound test?** M95 used it to decide what could
   be deleted, and it drove the stop. It is mechanical and auditable, but
   cairn's guards were authored ad hoc across ~40 milestones — a guard may pin
   prose that carries no rule, and a real rule may be unpinned. Assess the
   test's validity. If it is unsound, what should replace it? If it is sound,
   should it be promoted to explicit doctrine?

3. **Is compression a remedy or a deferral?** The weight axis's prescribed
   remedy on every capped file is "compress or consolidate in place" rather
   than evict. `LESSONS.md` is the live case: 31 items at a 630-char mean, 16
   chars of headroom, grown net since M92 gave it a retirement path, with
   visible accretion markers in the item text. Does consolidation actually
   discharge weight, or does it convert an item-axis problem into a weight-axis
   problem and defer it? What is the correct outflow for a file of durable
   lessons, and is D-051's two-criteria retirement (enforcement / ownership)
   sufficient? Answer with reference to the actual content of `LESSONS.md`.

4. **Can rationale have an IP4-compatible lifecycle?** IP4 (D-032) makes
   history — including `DECISIONS.md` — never edited, rewritten, or
   renumbered. `DECISIONS.md` is therefore guaranteed monotonic: 52 entries,
   95,374 chars, growing ~1,900 chars per decision. If rationale must be
   recorded and never removed, accumulation is structural, not a hygiene
   failure. Is there an IP4-compatible lifecycle — archival-with-tombstone
   (already parked as a candidate, RR02 rec 6), tiered/lazy reads (M97), a
   supersession-aware read, something else? Be explicit about where each
   option sits relative to IP4's letter and its intent, and flag if you think
   IP4 itself is the wrong constraint (that requires a user decision and a
   superseding D-entry — say so rather than assuming it).

5. **One lifecycle or three?** The three accumulating files are governed by
   three independently-derived mechanisms: the rulebook by nothing at all,
   `DECISIONS.md` by append-only, `LESSONS.md` by caps plus retirement. Should
   they share a common lifecycle model, or is per-file governance correct and
   the real defect just that the rulebook has none? Argue the trade rather than
   asserting a preference; a unified model that fits none of the three well
   would be worse than three fitted ones.

6. **GP1 is false as stated.** `cairn/DESIGN.md` GP1 asserts that caps and
   archiving keep always-read files small; RR02 found this false of the two
   largest always-read files, and the rulebook has no cap on either axis.
   Should GP1 be amended, retired, or kept with the practice corrected to meet
   it? Principle changes require an explicit user decision recorded as a
   D-entry — recommend, do not decide. If you recommend amended wording,
   supply the exact text.

7. **What should M95, M96, and M97 become?** All three are currently `planned`.
   M95 (editorial slimming) stopped on a refuted premise. M96 (growth ratchet
   for the rulebook) and M97 (bounded `DECISIONS.md` read) were both derived
   from RR02 and inherit its framing. Given your answers above, recommend the
   milestone set: what to re-cut, what to keep as-is, what to drop, what is
   missing. Order them and state dependencies. Prefer the smallest set that
   addresses the root cause.

## Constraints

Fixed; flag disagreement explicitly rather than working around it silently.

- **RR01 rec 15, upheld by RR02 Q5:** the cross-skill contract (file map, caps,
  status, git model, gates, output discipline, profiles mechanism) stays
  **monolithic** — no sectioned or conditional reads of the rulebook. The
  contract has no content trigger to gate a conditional read on, so any
  fragmentation reintroduces "skills must remember which sections apply." Do
  not re-propose splitting the rulebook.
- **D-031:** new *domain* doctrine gets a module, not a rulebook section
  (`skills/shared/validation-doctrine.md` is the precedent). Domain-conditional
  vs. universal is the boundary; universal file-family rules stay in core.
- **IP4 (D-032):** history is never fabricated, rewritten, or renumbered —
  `DECISIONS.md`, work logs, milestone IDs, `milestones/archive/`,
  `reviews/archive/`, `legacy/`. D-045 distinguishes this from *current
  knowledge* (`LESSONS.md`, `DESIGN.md`, `ROADMAP.md`, `references/`), which is
  corrected in place. D-052 added `ROADMAP.md` to the current-knowledge class.
- **Zero rules may be lost.** Any proposal that shrinks a file must preserve
  every operative rule. A slimming that loses a rule is a failed change.
- **D-004:** Fable escalation is gated per instance through this protocol; do
  not propose standing Fable automation.
- **No new tracking file** without arguing it against D-029's rejection of a
  central `ORACLES.md` (shape-free content doctrine was preferred over a new
  file) and D-015's four-wiring-points cost.
- Recommendations must be **implementable by the cairn maintainer alone** — a
  solo-operator repo, no CI, three Python stdlib `unittest` suites as the only
  gates (`cairn/PROFILE.md`).

## Output format

In `RR03-rationale-lifecycle-architecture.md`: answer each question by number
with your reasoning and the evidence you actually read (cite `file:line`). List
additional findings separately under "Beyond the brief". End with concrete
recommendations, each marked **apply / consider / reject-with-reason**, and
each naming the standing D-entry it touches, if any.

Where you disagree with RR01 or RR02, say so explicitly and give the evidence —
RR02's rec 1 was already falsified in execution, so prior review output carries
no presumption of correctness here.
