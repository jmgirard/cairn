<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M74: Issue triage — /milestone enumerates untriaged inboxes into candidate rows

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M73   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m74-issue-triage · https://github.com/jmgirard/cairn/pull/72   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Replace `/milestone`'s unenumerable "untriaged inboxes" audit bullet with a
concrete sweep that lists open issues and external PRs and proposes a
disposition for each.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a concrete enumeration step in `/milestone` §2 (`gh issue list` /
`gh pr list`, cross-checked against existing candidate rows, the archive, and
DECISIONS per the search-first rule); a triage acceptance chip in §3 showing
each proposed disposition verbatim per D-037/D-038; clean degradation when
`gh` is absent, unauthenticated, or the repo has no remote — report and skip,
never fail the audit; and the doc surfaces that still describe the pre-M73
`/hotfix` trigger (`cairn/DESIGN.md:69-70`, `README.md:118` and `:194`),
brought in line with the bidirectional description M73 shipped.

**Out:** any writing to GitHub (labels, comments, closing issues) — cairn
reads the inbox, it never manages it. Auto-creating candidate rows without the
chip. A scheduled or hook-driven sweep. Making `cairn_validate` aware of
issues — the scripts stay offline and stdlib-only
(`cairn/DESIGN.md:55-62`); this step lives in skill prose, like every other
`gh` invocation in the repo.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `skills/milestone/SKILL.md` §2's untriaged-inboxes bullet
      (`:78-79`) is replaced by a step naming the actual commands and the
      search-first cross-check against candidates + `milestones/archive/` +
      `DECISIONS.md`. Evidence: the step quoted.
- [ ] AC2 — the step states the degradation path for no `gh` / no auth / no
      remote: report the reason, skip the sweep, do not FAIL the audit.
- [ ] AC3 — §3's triage chip shows each proposed disposition verbatim above
      the chip (issue → candidate row / hotfix via `/hotfix` / milestone via
      `/milestone-plan` / leave), satisfying the Acceptance-chips bar.
- [ ] AC4 — external PRs in the same sweep route to M73's `/hotfix` door for
      the hotfix-bar disposition; no second intake mechanism is introduced.
- [ ] AC5 — a guard test locks AC1's commands and AC2's degradation clause,
      registered in `skills/tests/test_mutation_harness.py` with the
      completeness meta-test green; `test_gate_conclusion_preview.py` still
      passes with the new chip wording.
- [ ] AC6 — `cairn/DESIGN.md`'s Conventions bullet no longer says `/hotfix`
      triggers only on bug reports, and README's `/hotfix` row + contributions
      bullet name PR adoption; all three read consistently with the shipped
      `skills/hotfix/SKILL.md` `description:`. Evidence: the passages quoted
      beside that description, plus a repo-wide `git grep` for surviving
      pre-M73 trigger prose (history files excepted per M58, and this
      milestone's own file — which necessarily quotes the prose it
      removes, M62).
- [ ] AC7 — the `verify` slot is clean: all three `unittest discover` suites
      pass from the repo root.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3
- AC6 → T4
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Rewrite the §2 bullet (`skills/milestone/SKILL.md:78-79`) as a
      concrete step: `gh issue list --state open --json number,title,url` (and
      the PR equivalent), the search-first cross-check, and the degradation
      clause. Keep it inside the "script deliberately does not judge these"
      block (`:64`) — this stays model judgment over a mechanical listing.
- [x] T2 — Add the triage disposition chip to §3 (`:83-101`), with the
      verbatim-above-the-chip requirement stated at the step; route the PR
      dispositions to `/hotfix` per M73.
- [x] T3 — Write the guard test; register it in the mutation harness; re-run
      `test_gate_wording.py` and `test_gate_conclusion_preview.py`, which
      assert on `/milestone`'s chip wording.
- [x] T4 — Bring the doc surfaces in line with M73: rewrite
      `cairn/DESIGN.md:69-70`'s trigger clause and `README.md:118`/`:194` so
      the PR door is described where a reader looks for architecture. `git
      grep` the whole repo for other pre-M73 trigger prose (M48/M58: sweep
      live files, excluding only history — DECISIONS, CHANGELOG, legacy,
      reviews archive).
- [x] T5 — Run all three suites from the repo root.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: /milestone-plan gated amendment — absorbed the M73-review-F5 candidate (stale `/hotfix` trigger prose in DESIGN + README) as AC6/T4 at user request; prior AC6 verify renumbered AC7/T5.
- 2026-07-18: implement started on m74-issue-triage; gate settled three open choices (bullet not subsection, extend §3's existing triage option not a second chip, new guard file).
- 2026-07-18: T1 — §2 untriaged-inboxes bullet is now a concrete step (both `gh` commands, search-first cross-check, three-case degradation clause); kept inside the `:64` judgment block per plan. Skills suite green (267).
- 2026-07-18: T2 — §3 resolves the sweep: four named dispositions (candidate row / `/hotfix` / `/milestone-plan` / leave), PRs routed to M73's door, verbatim-above-the-chip stated; extended the existing triage option rather than adding a second chip. Both registered blocks verified still unique.
- 2026-07-18: T3 — new `test_issue_triage.py` (18 tests) + 4 mutation entries (commands, search-first ordering, degradation floor, PR routing), each block verified unique and proven to fail when blanked. Hit the M23/M64 reflow trap live: the degradation directive wrapped mid-phrase, so the prose was reflowed to keep it on one line rather than weakening the assert. Skills suite 285 green.
- 2026-07-18: T4 — DESIGN Conventions bullet now says `/hotfix` is bidirectional; README gained an outside-PR row and the contributions bullet names both doors. Repo-wide sweep found the stale claim in live prose only at `DESIGN.md:69` (README's two spots were incomplete, not wrong).
- 2026-07-18: T4 amendment (step-6 gate, user approved) — AC6's evidence grep hit this milestone's own AC text (M62 trap); criterion amended to except it alongside the M58 history files.
- 2026-07-18: T5 — all three suites green from the repo root (scripts 96, skills 285, hooks 72); `cairn_validate` all checks passed. Status → review.
- 2026-07-18: review — PR #72 opened; all 7 criteria verified with fresh evidence; consistency gate clean.
- 2026-07-18: review fan-out — 5 findings (diff-bug), 0 (blame), 0 (prior-PR, no evidence). Fixed F1/80 (own-PR filter), F3/92 (label-bound disposition asserts — proven false coverage, reproduced independently), F4/63 (overridden sub-threshold per M73 lesson). F2/30 rejected as thin, F5/40 → candidate row. Suites re-run green (skills 287).

## Decisions
<!-- owner: implement / review · append-only -->

## Review
<!-- owner: review · exclusive; exempt from the 150-line plan-owned cap (M55) -->

**PR:** https://github.com/jmgirard/cairn/pull/72 · reviewed 2026-07-18
**CI:** none configured — `gh pr checks 72` reports "no checks reported", exit 0 (M16: treat as no-CI, never wait for green).

### Acceptance-criteria evidence (fresh, by command)

- **AC1 ✓** — the `:78-79` bullet is gone; §2 now carries a step naming both
  commands (`gh issue list --state open --json number,title,url`,
  `gh pr list --state open --json number,title,url,author`) and the
  search-first cross-check over `candidate` rows + `milestones/archive/` +
  `DECISIONS.md`. Verified still inside the `:64` judgment block (block opens
  `:64`, section closes `:92`); step quoted at review.
- **AC2 ✓** — degradation clause present and names all three modes: "When
  `gh` is missing, unauthenticated, or the repo has no remote: name which of
  the three it was, skip the sweep, and finish the audit. An unreachable
  inbox is a reported gap, never an audit `FAIL`."
- **AC3 ✓** — §3 names all four dispositions (candidate row / `/hotfix` /
  `/milestone-plan` / leave) and states the bar: "Show every proposed
  disposition verbatim above the chip, never a count or a summary of them"
  (1 occurrence).
- **AC4 ✓** — PR disposition routes to `/hotfix` ("This is the door M73
  opened; route to it rather than inventing a second intake mechanism").
  Grep confirms `/milestone` introduces no `gh pr checkout` and no second
  intake path of its own.
- **AC5 ✓** — `test_issue_triage.py` (18 tests) green; 4 mutation entries
  registered, each block verified unique (count 1) and proven to fail when
  blanked via `test_each_registered_guard_fails_when_its_block_is_blanked`;
  `test_every_prose_guard_is_registered_or_exempt` green. 23 gate-test
  methods across `test_gate_conclusion_preview` / `test_gate_wording` ran,
  0 non-ok.
- **AC6 ✓** — DESIGN's Conventions bullet now reads bidirectional and
  matches the shipped `skills/hotfix/SKILL.md` `description:`; README gained
  a "Take in an outside pull request" row (`:119`) and the contributions
  bullet names both doors. Repo-wide sweep with AC6's exclusions returns
  clean — no surviving pre-M73 trigger prose in live files.
- **AC7 ✓** — all three suites green from the repo root, exit-gated with no
  tail-pipe hiding status (M56/M65): scripts 96, skills 285, hooks 72.

### Consistency gate

`cairn_validate.py` exit 0, all checks passed (run at review, output read not
recalled — M28). Profile is `generic`; its `consistency-gate` slot names no
toolchain checks, so that half is a clean no-op by design. No IP/GP principle
text changed (M74 works *under* IP3, does not alter it), so `cairn_impact`
is skipped per step 4.

### Independent fan-out — 3 lenses + scorer

[O] diff-bug: 5 findings. [S] blame-history: none (traced §2's run-and-read
discipline, §3's ONE-chip lineage, DESIGN's founding-commit bullet, M72's
README section, and the M53/M59/M60/M68 registry lessons — all clean).
[S] prior-PR-comments: no prior-PR evidence — 17 merged PRs touching these
files carry zero inline comments (single-operator merge pattern); clean
no-op, zero findings.

**Actioned (≥80):**

- **F1 (80) — fixed.** §2's PR sweep had no "external" filter: the bullet
  said "external PRs" and fetched `author`, but nothing used it, so
  `gh pr list --state open` returned every open PR. Reachable in cairn's own
  steady state — the audit would re-report the in-review milestone PR as
  inbox and could propose adopting a PR the session authored. Fix: the step
  now drops PRs authored by the operator or on `m<nn>-*`/`hotfix-*` branches
  before the sweep, with two guards + a mutation entry.
- **F3 (92) — fixed.** `test_candidate_row_is_the_default` and
  `test_larger_work_routes_to_milestone_plan` asserted only their clause,
  never the disposition *label* that carries the routing rule. Proven false
  coverage: inverting the labels (`candidate row`→`do nothing`,
  `/milestone-plan`→`/hotfix`) left all 18 tests green. Reproduced
  independently at review before fixing. All five disposition asserts now
  bind their label; the same inversion now fails 2 tests. One label
  registered in the mutation harness.
- **F4 (63) — fixed despite sub-threshold score (operator judgment, M73
  lesson).** The chip guard's comment claimed it "pins that choice so a
  later edit doesn't fork the chip", but the assert was a presence check on
  pre-existing text. Same false-coverage family as F3 and a two-line fix, so
  the score was overridden rather than logged. Now asserts the singular
  framing (`end with\none routing chip`) plus a count of exactly 1, and the
  comment states its real scope.

**Sub-threshold, logged not actioned (IP3 — surfaced, never dropped):**

- **F2 (30)** — §3 doesn't state whether mixed dispositions are accepted as
  a batch or per-item, nor who writes the candidate row. Scorer: largely
  covered by the rulebook's pre-existing search-first and durable-record
  preview rules, which M74 shouldn't restate. Rejected as thin; re-open if
  an agent actually improvises here.
- **F4 (63)** — see actioned above; fixed on operator judgment.
- **F5 (40)** — the `leave` disposition isn't in the rulebook's "Issues →
  `candidate` rows or the hotfix path" enumeration
  (`tracking-rules.md:200`). Rejected as a review-side change: AC3 names
  `leave` explicitly, and review never reinterprets a criterion. The
  doctrine divergence is real but small → candidate row for a rulebook
  decision.
