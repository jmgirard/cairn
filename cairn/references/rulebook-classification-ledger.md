# Rulebook classification ledger (2026-07-20 sweep of `tracking-rules.md`)

A first-hand classification of every paragraph and bullet in
`skills/shared/tracking-rules.md` at commit `94038ea` (779 lines, 53,751
chars), against the placement test recorded in D-056. It is committed because
RR04 rec 9 makes it the **precondition** for superseding D-056, and because
Q8 item 4 makes committed ledgers the rule wherever an acceptance criterion
rests on a classification that has no oracle.

**Read this as a fourth agent-derived estimate, not as ground truth.** It
joins RR02's 165–215, RR03's 60–100, and M95's delivered ~0 as successive
answers to the same question, each produced by an agent declaring its
predecessor wrong. Class-2/class-4 boundaries have no oracle and inter-rater
disagreement is the documented history of this file. Audit the per-block rows
below, not the summary.

**Provenance.** First-hand analysis, not a source extraction — no shelf item
backs it. Produced by an Opus subagent spawned by the M95/RB04 orchestrating
session, with a prompt that supplied D-056's test, forbade treating
guard-pinning as a keep reason, and asked it to contradict the recorded claim
in either direction. Ingested 2026-07-20; ingesting milestone: none (drafted
during RB04's authoring, committed at RR04 ingest). Pagination basis: —.
Extraction: re-verified against the source 2026-07-23. The ledger's
checkable factual layer — the class-4 anchor openings, the class-3
D-entry owners, the two M55/M58 citation defects (old lines 114, 648),
and a spot-checked restatement row (528–529 ↔ 462–464) — was re-read
against `tracking-rules.md` at `94038ea` and every anchor resolved to the
claimed content (allowing for cairn's ~66-char wrap, which shifts a clause
a line or two below its bullet). Because that source is a frozen commit,
the factual layer cannot age. The per-block class-2/3/4 classifications are
no-oracle judgments — this file's documented inter-rater history is the
point — so there is nothing to re-verify them against, and the sweep's
author also authored the RB04 proposal the ledger was written to test;
those are recorded, not re-rated. (First pass 2026-07-20 checked two of
these citation claims; this pass extended it to the full anchor set.) —
observed 2026-07-23.

**Line numbers are already stale.** They describe `94038ea`; any edit
invalidates every row below it. Re-locate by content, and note that cairn
hard-wraps at ~66 chars so a plain `grep` misses a wrapped phrase.

## Summary

| Class | Line-equivalents | % of 779 |
|---|---|---|
| Structural (blank, heading, separator) | 86 | 11.0% |
| 1 + 2 — operative (rules + application doctrine) | ~628 | 80.6% (90.6% of content lines) |
| 3 — decision-owned (compress to rule + cite) | ~27 | 3.5% |
| 4 — free-floating justification (delete) | ~38 | 4.9% |
| **3 + 4 combined** | **~65** | **8.4%** |

Line-equivalents are char-mass ÷ ~68 (measured wrap width), because most
class-3/4 text is a clause inside a wrapped paragraph; the sweep spot-checked
19 ranges and reports the ratio held.

**This ledger confirms D-056's headline claim** — the file's mass is mostly
class 1/2 — and contradicts only its yield clause ("the test predicts no
yield"), by ~56 lines net.

## Per-section concentration

| § | Lines | Class 3+4 | % |
|---|---|---|---|
| Weight caps | 71 | 16 | 22.5% |
| What gets a test | 63 | 9.9 | 15.7% |
| References pages | 65 | 9.7 | 14.9% |
| Sizing and the work tiers | 65 | 5.7 | 8.8% |
| Model and agent strategy | 57 | 4.8 | 8.4% |
| Universal tracking rules | 70 | 4.5 | 6.4% |
| File map | 72 | 4 | 5.6% |
| Git and approval model | 75 | 4 | 5.3% |
| Question gates | 36 | 2.1 | 5.8% |
| Toolchain profiles | 35 | 1.7 | 4.9% |
| Output & interaction discipline | 94 | 1.3 | 1.4% |
| Milestone IDs · Context hygiene · Validation doctrine | 68 | 1.6 | ~2% |

Three sections hold 55% of removable mass in 25% of the file.

## Class 4 — free-floating justification (~38 lines)

| Line | Opening |
|---|---|
| 70 | "Fencing enforces what the Coverage map plans…" |
| 101 | "Density warns because 'too dense' is a judgment and an item count is not" |
| 120 | "a hard-wrapped entry costs several lines of a budget it no longer pays into" |
| 133 | "so the remedy can never aim at history" |
| 174 | "so it needs an outflow and not only a ceiling" |
| 196 | "An honest record keeps the next session from mistaking an exception for a precedent." |
| 251 | "because a milestone can wait on a human before work starts as well as after it finishes" |
| 289 | "because nothing outside `cairn/` is authoritative tracking state…" |
| 321 | "(`pak::pak()` installs it; pkgdown may deploy from it)" — R-specific example in the language-agnostic core |
| 369 | "because an approval that cannot be checked is not an approval" |
| 433 | "the chip makes consent explicit and auditable" |
| 447 | "(locked by `test_gate_wording.py`)" |
| 546 | "task panes show only the title, not the model" |
| 633 | "so a repo that adopted cairn before profiles keeps working unchanged" |
| 688 | "it reads as durable, is believed by every later plan-time harvest…" |
| 713 | "It stays an advisory and never a check because…" — duplicates the doctrine at 101 |
| 758 | "on its own line so the mapping stays pinnable" |
| 762 | "so sessions that write no guard never pay for it" |
| 772–779 | migration note; ~5.5 of 8 lines are "where things went", which git holds |

Lines 101 and 433 are text M95 itself wrote or preserved: 101 is the B3 clause
M95 compressed rather than deleted, on the argument its reason was behavioral.

## Class 3 — decision-owned, compress to rule + cite (~27 lines)

| Line | Owner |
|---|---|
| 25 | D-047 |
| 104, 105–108, 147–148 | D-052 |
| 114–116 | **D-030** — rulebook cites M55 (verified defect) |
| 117 | D-046 |
| 172–173 | D-045 |
| 182 | D-055 / D-051 |
| 309–310 | D-054 |
| 349–350 | D-043 |
| 591, 592–594 | D-004 |
| 648 | **D-031** — rulebook cites M58, quoting D-031's own heading (verified defect) |
| 740–743 | D-056(3), near-verbatim |

**Keep despite classification:** 378–380 — D-043(1) explicitly decided to
state this in the rulebook.

**No D-entry home (~4.3 lines; stay put per D-056 step 2):** 562 "(hit in the
M36 review)"; 575–577 the diff-blindness rationale (M95 kept this on a
behavioral argument, the sweep on "no home" — same outcome, different reason);
708–709 the divergence-vector line.

Only ~4.3 line-equivalents are homeless, against the 9-of-21 that stopped
M95's first run — that figure was an artifact of which blocks were nominated.

## Fifth class — intra-file restatement (~10 lines)

Rules stated in full in one section and restated in another. No git backfill
and no D-entry needed; the rule stays in the file. D-056's three-step test
misroutes these to class 1 (they *are* rules), which RR04 Q6 treats as a
structural defect in the test.

| Line | Restates |
|---|---|
| 23 (LESSONS table cell tail) | 160–188, in full |
| 301–303 | 296–297, one sentence earlier |
| 451–452 | 435–447 |
| 528–529 | 462–464 |
| 555–556 | 545–547 |
| 657–658 | 654 |
| 768–770 | 621–624, near-verbatim |

## Verdict as recorded by the sweep

Realistic yield of a thorough pass: **~50–60 lines net**, concentrated enough
to be one pass rather than a file-wide crawl — Weight caps, References pages,
What gets a test, and the 772–779 migration paragraph carry ~40 of the ~60.
The yield is **one-time**: after such a pass the file sits ~97% operative and
there is no second harvest, so controlling inflow remains the durable lever.

RR04 Q9 subsequently rated capturing this yield as low-value relative to its
cost (~3% of per-read tokens), and rec 11 closes the stock-side program absent
a measured `cairn_cost` regression. This ledger is therefore a record of what
*could* be cut, not a work order.
