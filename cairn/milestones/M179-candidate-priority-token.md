# M179: ROADMAP candidate rows carry an optional priority token

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP3
- **Resolves:** —
- **Surface tier:** user-facing — the candidate-row shape ships to every adopting repo through cairn-init's ROADMAP skeleton and the shared rulebook.
- **Branch/PR:** m179-candidate-priority-token

## Goal

A ROADMAP candidate row can open with one priority token, so a reader tells at a glance which rows matter, without candidates gaining a status, a file, or an ID.

## Scope

**In:** the rulebook rule (a row may open with `[high]` or `[low]`; neither reads as `normal`; the section orders high → normal → low; the token is the fact, the order derived from it); the cairn-init ROADMAP skeleton comment; `/cairn-triage` reading and re-rating the token; a `candidate_count` regression test; this repo's own Candidates section rated and re-ordered. Ratings this milestone applies here: `[high]` — Chip-applied `cairn/**` `paths-ignore` edit; `[low]` — Review-side reclassification, Standing-instrument adoption discipline, Reasoning-effort dial, Numeric cap on subagent spawning, Dedicated `/explore-sources` skill, Citekey resolution, Concurrent-cairn-operator hardening, BC-aware coverage message, Scaffold-spec version stamp, Phase-gated loading, Action-graded finding vocabulary, Deferred second tier for hook nudges; untagged (`normal`) — Second-driver adoption pass, Contributor-facing scaffold, Branch-protection compatibility.

**Out:** a type/kind token (feature, fix, edge case) — rejected at the 2026-09-06 plan gate, not deferred; a mandatory token on every row — rejected at the gate; a `cairn_validate` check on the token — rejected at the gate (re-openable if a misspelled token misleads an operator in practice; no row, since a rejection is not a deferral); category grouping or sub-sections of the Candidates list — D-035 stands; re-rating rows in other repos — each repo's own triage pass.

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md` states, in one paragraph after the `Search-first candidate creation` paragraph in `## Sizing and the work tiers`, that a candidate row may open with `[high]` or `[low]`, that a row with neither reads as `normal`, that the Candidates section orders rows high → normal → low, and that the token is the fact the order derives from.
- [ ] AC2: The ROADMAP skeleton `/cairn-init` scaffolds (`skills/cairn-init/SKILL.md`, the fenced `## Candidates` block) shows the row shape with the optional token — `[high]`/`[low]` or absent.
- [ ] AC3: `/cairn-triage` (`skills/cairn-triage/SKILL.md`) reads the token: step 1's enumeration lists each row's priority (`high`/`normal`/`low`, untagged = `normal`); step 3's proposal table may carry a priority change on a `keep` or `compress` row, applied with that row's edit as the accepted change step 3's byte-for-byte rule carves out; the re-ordering sentence in step 4's Apply orders by token, then advisory within a level.
- [ ] AC4: `candidate_count()` returns the same count for a `## Candidates` section whose rows carry `[high]`/`[low]` tokens as for the same section with the tokens removed.
- [ ] AC5: This repo's own `cairn/ROADMAP.md` Candidates section carries a token on every row this milestone's Scope names `high` or `low`, is ordered high → normal → low, and its italic ordering line names the token rule instead of "candidates carry no Priority field".
- [ ] AC6: Both gating suites (`python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`) exit 0 at the branch head.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks

- [x] T1: Add the rulebook paragraph (AC1). Add a hand-run prose guard in `skills/tests/` asserting its phrases, written first and seen red before the paragraph lands (D-109: hand-run, gating nothing).
- [x] T2: Rewrite the cairn-init ROADMAP skeleton's `## Candidates` comment to show `- [high] idea — added YYYY-MM-DD — links` beside the untagged form (AC2).
- [x] T3: Edit `skills/cairn-triage/SKILL.md` step 1 (priority column in the enumeration), step 3 (a priority change proposed on a `keep`/`compress` row, named as an accepted edit the byte-for-byte rule carves out), and step 4's ordering sentence (AC3). Extend the existing triage prose guard in `skills/tests/` for the new phrases.
- [x] T4: Add a `scripts/tests/test_scripts.py` test over an in-test fixture with at least one `[high]`, one `[low]`, and one untagged row, asserting `candidate_count` equals the fixture's row count with and without tokens (AC4).
- [x] T5: Tag and re-order this repo's Candidates section per Scope; rewrite the italic ordering line to name the token rule and this milestone; check `wc -l -c cairn/ROADMAP.md` stays under 60 lines and 24,000 bytes (AC5).
- [ ] T6: Run both gating suites from the repo root, checking each exit code separately, and hand-run `skills/tests`; record the three exit codes in the work log (AC6).

## Work log

- 2026-09-06: created by /milestone-plan from the user's question whether candidate rows should carry a type or priority classification.
- 2026-09-06: criteria audit ran in full mode (user-facing tier) on a fresh [O] reader; six findings, five fixed at the gate (AC2 unenumerable trailing clause cut; AC3 ordering sentence relocated to step 4 and the `keep` no-op clash worded as a carve-out; AC4 instrument clause moved to T4; AC5 "rows the gate rates" replaced by the Scope list; AC6 hand-run suite clause dropped per D-109), the sixth (D-108 door) posed as a gate question and settled as trigger met (D-134).
- 2026-09-06: plan gate chose a priority token over a type token because type does not answer "how important" and fix-shaped work already routes to /hotfix; falsified by an operator who, reading tagged rows, still cannot choose which to promote.
- 2026-09-06: plan gate chose an optional token (untagged = normal) over a mandatory one because adopting repos' existing rows stay valid unedited; falsified by an adopting repo where untagged rows are read as unrated rather than normal.
- 2026-09-06: plan gate chose a prose convention over a `cairn_validate` token check because triage reads the token anyway and a misspelling degrades to normal; falsified by a misspelled token misleading an operator's promotion choice.
- 2026-09-06: plan gate passed D-108's door by reading the trigger as met (shipped rows carry no importance signal) over parking the idea or rewriting the door's terms; falsified by evidence the illegibility was this repo's alone — an adopting repo whose untagged rows an operator ranks without difficulty.
- 2026-09-06: M179 branch `m179-candidate-priority-token` cut from main; question gate skipped (no open choice); T1 done — guard `skills/tests/test_candidate_priority_token.py` seen red (5/5) before the paragraph landed after the Search-first paragraph, five asserts registered in the mutation harness; gating suites 0/0. Observed pre-existing on main: hand-run `test_lesson_graduation.test_partial_coverage_was_trimmed_not_deleted` fails since M178 hygiene pruned the `trimmed M98` lesson — out of scope here.
- 2026-09-06: T2 done — cairn-init `## Candidates` skeleton comment shows the `[high]` and untagged row shapes and names the token optional; two guard asserts seen red then green, registered in the harness; gating suites 0/0.
- 2026-09-06: T3 done — `/cairn-triage` step 1 lists each row's priority (untagged = normal), step 2 names the token a row fact beside the disposition, step 3's table and chip carry a priority change on a `keep`/`compress` row as the byte-for-byte carve-out, step 4 skips only on `keep` with no change and orders by token then advisory, step 6's stamp names re-rated items. Minor amendment: no prose guard over `/cairn-triage` existed to extend, so the five asserts live in the new M179 guard file, registered in the harness; gating suites 0/0.
- 2026-09-06: T4 done — `TestCandidateCountPriorityToken` over a three-row fixture (one `[high]`, one untagged, one `[low]`, non-candidate bullets outside the section) asserts the count equals the stated 3 with and without tokens; seen red against a planted token-blind counter, then restored; gating suites 0/0 (349+126).
- 2026-09-06: T5 done — Candidates section rated per Scope (1 high, 3 untagged, 12 low), re-ordered high → normal → low with each level's prior relative order kept, rows otherwise byte-for-byte; italic line names the token rule and M179; `wc -l -c` 40/10817 under 60/24000; `cairn_validate` green; `cairn_status` still counts 16 candidates.

## Decisions

## Review
