# Milestone cap peak-revision ledger (M118)

Every milestone file this repo has ever had live, re-measured at its **peak
plan-owned revision** under both weight-cap counters: the pre-M118 counter,
which exempts only `## Work log`, and the post-M118 counter, which also exempts
the milestone-local `## Decisions` section (D-074). The question it answers is
narrow and checkable: does the exemption actually relieve the files that hit the
cap, and does it leave any file near it?

**Provenance.** Ingested 2026-07-27 by M118 from this repo's own git history —
no shelf item backs it. Derivation: the file set is every path ever touched
under `cairn/milestones/` excluding `archive/`, taken from
`git log --all --name-only`; for each path, every revision's blob is read with
`git show <rev>:<path>` and scored by the **shipped** counter internals
(`scripts/cairn_scripts.py`: `_plan_owned_scan`, then `boundary` less the
exempted sections' line counts), so the `## Review` boundary and the fence rules
measured here are the ones the gate enforces rather than a reimplementation of
them. The pre-M118 column subtracts `WORKLOG_HEADING` only; the post-M118 column
subtracts `EXEMPT_HEADINGS`. Pagination: —.
Extraction: first-hand record of this repo's own frozen history, nothing to re-verify against — every row names the commit it was read at, and re-running the derivation above at those commits reproduces it — observed 2026-07-27.

**Scope.** This is a measurement, not an authority: it does not decide the
exemption (D-074 does), does not set the cap, and holds no status. It is not a
source summary — there is no external source. It deliberately builds no tooling:
the derivation is a one-shot read of git history, not a committed script, for
the reason M56 rejected query machinery. Status lives in `ROADMAP.md`, decisions
in `DECISIONS.md`, architecture in `DESIGN.md`.

**Evidence snapshot.**

- `cairn/milestones/*.md`, all non-archive paths, every revision reachable from `git log --all` — 119 paths over 118 milestone IDs (M94 was re-cut under a second slug, so it holds two paths and appears as two rows) — observed 2026-07-27.
- `scripts/cairn_scripts.py` at `b8ef6e5` (`MILESTONE_CAP = 150`, `>=` fails, so 149 is the largest passing body) — observed 2026-07-27.

## What each column means

Both peaks are **independent maxima over a path's revisions**: the pre-M118
column is the largest body that counter ever saw, the post-M118 column the
largest the new counter ever saw, and they need not fall on the same revision.
So the gap between the two columns is a difference of maxima, not the size of
any single revision's `## Decisions` section. The commit named is where the
pre-M118 peak occurred.

Every row's milestone ID is its stable ID; rows are added, never reflowed.

## Ledger — peak plan-owned body per milestone file, both counters

| Milestone | peak, pre-M118 counter | peak, post-M118 counter | at commit |
|---|---|---|---|
| M114 | 166 | 123 | `e3abccf` |
| M98 | 165 | 123 | `c48db58` |
| M79 | 154 | 125 | `ddbc6e7` |
| M118 | 149 | 125 | `d1b1144` |
| M87 | 149 | 125 | `8a1c13d` |
| M81 | 148 | 124 | `4c10a91` |
| M83 | 147 | 112 | `3dafae8` |
| M88 | 147 | 120 | `957b69a` |
| M78 | 143 | 127 | `0b4e2ce` |
| M95 | 142 | 126 | `2ac59b4` |
| M94 (always-read-weight-signal) | 141 | 108 | `5b4889f` |
| M84 | 138 | 106 | `d8ab7b6` |
| M43 | 133 | 129 | `26c0b0f` |
| M80 | 130 | 127 | `4815763` |
| M82 | 130 | 121 | `c038d56` |
| M93 | 127 | 124 | `7213769` |
| M94 (cost-instrumentation) | 126 | 93 | `b2ee126` |
| M101 | 124 | 120 | `9f3586a` |
| M75 | 124 | 120 | `62d03e3` |
| M117 | 122 | 120 | `7d29ce8` |
| M89 | 122 | 101 | `f637fd1` |
| M41 | 121 | 117 | `44630d4` |
| M53 | 121 | 109 | `09f29e1` |
| M58 | 120 | 118 | `8d0f373` |
| M70 | 119 | 115 | `1942284` |
| M115 | 118 | 116 | `94b7237` |
| M20 | 118 | 103 | `627b926` |
| M96 | 118 | 106 | `1525aa1` |
| M90 | 117 | 112 | `dabf7cc` |
| M99 | 117 | 113 | `4699c5b` |
| M72 | 116 | 105 | `b660b42` |
| M86 | 116 | 112 | `d3fb535` |
| M92 | 116 | 114 | `e048746` |
| M45 | 115 | 103 | `c49fda2` |
| M113 | 114 | 93 | `3f26036` |
| M40 | 114 | 110 | `82ca240` |
| M44 | 114 | 111 | `9f00f6c` |
| M50 | 114 | 112 | `b9a443a` |
| M100 | 113 | 109 | `2db1295` |
| M25 | 112 | 108 | `3e0c60d` |
| M33 | 112 | 108 | `86e8fd6` |
| M91 | 112 | 108 | `bd83138` |
| M19 | 111 | 107 | `1d4709e` |
| M76 | 111 | 107 | `c76461e` |
| M08 | 109 | 102 | `11d84b9` |
| M97 | 108 | 102 | `9398bdf` |
| M54 | 106 | 104 | `b867b82` |
| M68 | 106 | 102 | `c1dedd0` |
| M71 | 105 | 101 | `625a80f` |
| M61 | 104 | 95 | `070f619` |
| M77 | 104 | 98 | `daf9862` |
| M108 | 103 | 101 | `fc2517a` |
| M12 | 103 | 93 | `f707488` |
| M74 | 102 | 99 | `40009d0` |
| M32 | 100 | 98 | `70e48bf` |
| M63 | 100 | 96 | `08b7ee6` |
| M73 | 100 | 97 | `010f9bd` |
| M07 | 98 | 91 | `510454e` |
| M22 | 98 | 96 | `271c1f7` |
| M28 | 98 | 96 | `dfc33ff` |
| M21 | 97 | 95 | `271c1f7` |
| M69 | 97 | 93 | `6e81d5f` |
| M85 | 97 | 95 | `98c38c0` |
| M30 | 96 | 92 | `e606480` |
| M51 | 95 | 91 | `7bc040f` |
| M57 | 95 | 91 | `78a0eeb` |
| M46 | 94 | 92 | `ffe07db` |
| M110 | 93 | 91 | `b16260c` |
| M42 | 93 | 89 | `31266ec` |
| M60 | 93 | 82 | `76cfb36` |
| M24 | 92 | 90 | `707c684` |
| M55 | 92 | 88 | `96b1897` |
| M59 | 92 | 90 | `39a605d` |
| M66 | 92 | 88 | `eb56020` |
| M103 | 91 | 89 | `116d27d` |
| M31 | 91 | 87 | `98e7366` |
| M62 | 91 | 88 | `9a110ec` |
| M119 | 90 | 86 | `704a595` |
| M26 | 90 | 88 | `0b5709e` |
| M36 | 90 | 87 | `e50c5bd` |
| M48 | 90 | 88 | `b2068d9` |
| M29 | 89 | 87 | `a52a4b4` |
| M23 | 88 | 86 | `9a798bc` |
| M09 | 87 | 79 | `6d9d7ee` |
| M107 | 87 | 85 | `946238c` |
| M10 | 86 | 78 | `01df055` |
| M112 | 86 | 84 | `e7ec1b4` |
| M65 | 86 | 84 | `75adf55` |
| M52 | 85 | 83 | `4a1528f` |
| M17 | 84 | 80 | `0eedbae` |
| M35 | 83 | 80 | `b00937c` |
| M37 | 83 | 79 | `4484673` |
| M56 | 83 | 81 | `7d8ba52` |
| M64 | 83 | 81 | `24c8d54` |
| M111 | 82 | 80 | `5fbef9c` |
| M67 | 82 | 78 | `7a70e57` |
| M13 | 81 | 71 | `2b6a42e` |
| M18 | 78 | 74 | `6de2080` |
| M06 | 75 | 67 | `6da6972` |
| M34 | 75 | 72 | `9d42569` |
| M38 | 75 | 73 | `99b8514` |
| M104 | 74 | 70 | `0abb880` |
| M04 | 73 | 70 | `2e4d9fb` |
| M05 | 73 | 70 | `00ea57c` |
| M105 | 73 | 71 | `b94796a` |
| M49 | 72 | 70 | `6890b7e` |
| M27 | 69 | 62 | `7d9ae86` |
| M47 | 67 | 65 | `fea7521` |
| M11 | 64 | 58 | `5d9c7aa` |
| M16 | 62 | 56 | `6596653` |
| M14 | 58 | 55 | `80825f4` |
| M15 | 58 | 55 | `5293667` |
| M109 | 57 | 48 | `fc6ef79` |
| M39 | 57 | 55 | `3ef9ba6` |
| M106 | 55 | 53 | `e57d78d` |
| M102 | 52 | 50 | `94473c7` |
| M116 | 51 | 49 | `5b6f883` |
| M03 | 45 | 43 | `ba40a77` |
| M02 | 42 | 40 | `a83443a` |

## Summary

| Reading | Value |
|---|---|
| Milestone file paths measured | 119 |
| Paths whose pre-M118 peak reached the cap (>= 150) | 3 — M114 (166), M98 (165), M79 (154) |
| Of those, still at or over the cap under the post-M118 counter | 0 — they land at 123, 123, 125 |
| Largest post-M118 peak across all 119 paths | 129 (M43) |
| Headroom at that maximum | 20 lines below the 149 ceiling |

The three over-cap peaks are real committed states, not hypotheticals: each file
sat over the gate's own threshold at that commit and was compressed back down
afterwards. M118's own file is the fourth-largest pre-M118 peak (149 at
`d1b1144`, the RR08 ingest) — the zero-headroom state its work log records.

## Cap-exempt section sizes, in characters

Input to `hooks/session_context.py`'s `SECTION_MAX_CHARS`, which bounds how much
of each cap-exempt section a session start injects (D-063). Measured over the
same corpus by the same derivation, each path scored at its own peak per
section, via `_section_body_lines`; character counts include one newline per
line. `## Review` is absent from exactly one path, hence n=118.

| Section | n | median | p90 | max | paths over 6,000 |
|---|---|---|---|---|---|
| `## Work log` | 119 | 1,292 | 4,228 | 55,150 | 5 |
| `## Decisions` | 119 | 122 | 1,372 | 4,647 | 0 |
| `## Review` | 118 | 2,346 | 6,718 | 8,477 | 14 |

Three readings the constant's justifying comment now rests on. `## Decisions` is
the smallest of the three types by an order of magnitude at the median and never
reaches 6,000 in the corpus, so admitting it to the read-bound costs the budget
little. `## Review`'s p90 has passed 6,000 since the M113 measurement that set
the constant (which recorded work log 3,740 and review 5,866 over 111 files), so
6,000 no longer clears the p90 of every type — the outliers it trims are review
sections, and that is the bound working, not failing. The work log's 55,150
maximum is M114, whose nine review passes make it the corpus outlier by a factor
of 2.4 over the next path (M95, 22,932).

## Disposition

- The three over-cap rows and the 129 maximum are AC3's evidence; nothing here
  is restated into `M118`'s milestone file (M99).
- The section-size table is AC4's fresh measurement; the re-derived
  `SECTION_MAX_CHARS` comment cites this page rather than carrying a second copy
  of the numbers.
- The exemption itself is locked by the fixtures in
  `scripts/tests/test_scripts.py` (`TestMilestoneBodyLineCount`,
  `TestMilestoneSectionLineCounts`, `TestMilestoneDecisionsLines`) and the prose
  by `skills/tests/test_milestone_cap_exemption.py`; this page produces no rule
  of its own.
- No candidate row falls out of this measurement: nothing here shows a second
  section under cap pressure.

## Open questions

- Whether `## Review`'s growth past the read-bound trims state a resuming session actually needed is unmeasured — the gate kept 6,000 rather than raise it, and the falsifying observation is recorded in M118's work log — observed 2026-07-27.
