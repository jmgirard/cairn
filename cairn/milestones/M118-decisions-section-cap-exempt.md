<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. Drafting budgets: see the template. -->
# M118: The milestone-local `## Decisions` section joins the cap-exempt set

- **Status:** blocked
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** —

## Goal

Exempt the append-only `## Decisions` section from the 150-line plan-owned cap,
on the same un-editability grounds D-046 used for `## Work log`, and wire the
third exempt member through every surface that enumerates the set.

## Scope

**In:** the cap counter and its heaviest-first breakdown; the session-start
read-bound for cap-exempt sections; a wrapped-entry advisory for the
newly-unbudgeted section; every rulebook, template, and guard site that names
the exempt set; a D-entry superseding D-046's choice (3).

**Out:** redistributing the ≥21 template lines the exemption frees into the
per-section drafting budgets → candidate row (maintainer's call at this gate,
2026-07-27); any change to the 150 cap itself → not proposed; exempting an
RR-bound AC block, and making carry-by-reference the standard ingestion form →
both declined at this gate on the measured evidence, and D-066 choice 4 already
governs carry-by-reference as a tabled deviation.

## Acceptance criteria

- [ ] AC1: `milestone_body_line_count` excludes an exact `## Decisions`
      heading's section from the plan-owned body, matching the section by the
      same shared heading constant and fence rules the work-log exemption uses;
      a fenced `## Decisions` and a `## Decisions notes` heading both stay
      counted. Evidence: fixtures in `scripts/tests` for the exact, fenced,
      prefixed, and absent cases.
- [ ] AC2: `milestone_section_line_counts` omits `## Decisions` from the
      heaviest-first breakdown, so an over-cap diagnostic never names a section
      IP4 forbids editing, and the documented `preamble + sections == body`
      invariant (`cairn_scripts.py:436-441`) still holds. Evidence: a fixture
      whose Decisions section is the largest section reports a breakdown that
      does not name it, plus an invariant assertion.
- [ ] AC3: A committed ledger re-measures every milestone file in this repo's
      git history at its **peak plan-owned revision**, under both the old and
      new counters, and reports per file. Every file whose peak exceeded the cap
      falls below it under the new counter. The ledger carries the numbers; no
      criterion or prose here restates them (M99).
- [ ] AC4: `hooks/session_context.py` read-bounds `## Decisions` as a third
      cap-exempt section per D-063, and `SECTION_MAX_CHARS`'s justifying comment
      is re-derived over all three section types from a fresh measurement rather
      than left asserting a p90 over two. Evidence: a hook test that a long
      Decisions section injects newest-first and states what it omitted.
- [ ] AC5: A `decisions format` advisory WARNs, exit-code neutral, on a
      milestone-local `## Decisions` entry that is not a one-line `- ` entry,
      reading the section through a shared extractor that takes its heading and
      fence rules from the same constant AC1 exempts — the hole
      `milestone_worklog_lines` (`cairn_scripts.py:394-397`) names.
- [ ] AC6: Every site that enumerates the cap-exempt set names all three
      members and each member's own reason: the rulebook's weight-caps bullet,
      its cap-remedies bullet, and its always-read frame row and frame prose
      (`tracking-rules.md:184-186`); the milestone template's budget preamble
      and its `## Decisions` and `## Review` comments; and
      `test_milestone_cap_exemption.py`, whose set-membership assert
      (`:62`) is deliberately anchored on the whole set and must be re-anchored,
      not merely appended to. No site is left naming a two-member set.
- [ ] AC7: `python3 -m unittest` clean over all three suites (the `generic`
      profile's `verify` slot), and `cairn_validate` green.

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks

- [ ] T1: Add the shared `DECISIONS_HEADING` constant beside `WORKLOG_HEADING`
      (`cairn_scripts.py:97`) and a `milestone_decisions_lines` extractor
      mirroring `milestone_worklog_lines`, so the exemption and the advisory
      read one section by one rule.
- [ ] T2: Exempt the section in `milestone_body_line_count` and drop it from
      `milestone_section_line_counts`; update both docstrings, which state the
      exempt set and its reasons. Fixtures first (exact/fenced/prefixed/absent
      plus the sum invariant), red before the change.
- [ ] T3: Write the peak-revision ledger script over `git log --all` for
      `cairn/milestones/M*.md`, run it under both counters, and commit the
      per-file table into this file's `## Decisions`— which by then costs no
      budget, the exemption's first use.
- [ ] T4: Add `"decisions"` to `CAP_EXEMPT_SECTIONS`
      (`hooks/session_context.py:56`); re-measure p90 across all three section
      types over the live-milestone corpus and re-derive `SECTION_MAX_CHARS`'s
      comment from that measurement. Hook test for the newest-first bound and
      the omission notice.
- [ ] T5: Add `check_decisions_format` beside `check_worklog_format`
      (`cairn_validate.py:1321`), register it in `ADVISORIES` (`:1590`), and
      fixture both arms (wrapped → WARN + exit 0; clean → OK).
- [ ] T6: Re-anchor the guard and update the prose sites in AC6. The
      set-membership assert is registered in the mutation harness — re-register
      the new anchor and verify by mutation that deleting the three-member
      sentence reds it (guard-doctrine; the harness cannot catch a swap, which
      is why the whole set is the anchor).
- [ ] T7: Full `verify` + `cairn_validate`; post-merge hygiene.

## Work log

- 2026-07-27: created by /milestone-plan.
- 2026-07-27: plan gate chose exempting `## Decisions` over exempting an RR-bound AC block, and over standardizing carry-by-reference, because the squeeze is not RR-specific — of the 7 files ever at ≥145 plan-owned lines only M114 was RR-driven, and all 7 carry a Decisions section of 24–43 lines against a median of 4 over 116 files; falsified by a future squeeze whose Decisions section is at or below the median, which would locate the cost elsewhere.
- 2026-07-27: plan gate classified the section as history (D-045) over current knowledge, because the ownership table already makes it append-only and the alternative is self-defeating — a correctable section is trimmable, and a trimmable section has no claim to the un-editability exemption; falsified by a milestone-local decision that must be corrected in place rather than superseded by a later entry in the same section.
- 2026-07-27: escalation offered at the gate on the `ip-touching` tripwire (the classification extends IP4's reach to a new section) and declined by the maintainer, who returned the call to the session.
- 2026-07-27: blocked on RB08 — the maintainer reversed the gate's escalation decline and sent the history-vs-current-knowledge classification (D-074 part 1) to independent review before any code is written.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive -->
