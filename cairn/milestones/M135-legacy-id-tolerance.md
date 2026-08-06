<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M135: Legacy-id tolerance for check_dangling_ids

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m135-legacy-id-tolerance · https://github.com/jmgirard/cairn/pull/135   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

`check_dangling_ids` stops WARNing on a migrated repo's references to its
pre-migration milestone ids, so a real post-migration dangler is visible
again instead of drowned (intraclass: 321 standing WARNs, measured 2026-08-06).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a third tolerance rule in `check_dangling_ids`
(`scripts/cairn_validate.py:1735`), following D-023's
missed-format-beats-false-positive doctrine: when `cairn/legacy/` exists,
unresolved `M<NN>` tokens numerically at or below the highest `M<NN>` token
found in any `cairn/legacy/**/*.md` are skipped (an empty or M-token-free
legacy directory yields a floor of 0 — tolerance inert). Docstring updated to
enumerate three tolerances; fixture tests; the M115 lesson line in
`cairn/LESSONS.md` corrected in place (D-045) to name the new skip;
`cairn/references/llm-wiki.md`'s description of the advisory checked and
corrected if stale; real-world before/after evidence from the local
intraclass checkout.

**Out:** a legacy tolerance for `D-<NNN>` tokens — gate decision 2026-08-06:
no measured flood (all 321 intraclass WARNs are M-tokens); becomes worth a
row only if a migrated repo floods on D-ids. Any change to the other two
tolerances or other checks — untouched.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: With `cairn/legacy/` present, an unresolved `M<NN>` token in a live
      `cairn/` markdown file at or below the highest `M<NN>` token in any
      `cairn/legacy/**/*.md` is skipped: a fixture with live max assigned id
      M60, legacy max M47, and a live file citing an unassigned M12 (no
      `owner/repo` slug on the line) reports `OK    dangling id tokens`.
- [x] AC2: The tolerance is gated on the directory: a second fixture identical
      to AC1's but built without `cairn/legacy/` reports
      `WARN  dangling id tokens` naming M12.
- [x] AC3: In the AC1 fixture, an unresolved M55 token (above legacy max M47,
      at or below live max M60, no slug on its line) still WARNs, and an
      unresolved `D-<NNN>` token at or below the live D max still WARNs.
- [x] AC4: A fixture with `cairn/legacy/` present but containing no `M<NN>`
      token behaves as if the directory were absent: the unassigned M12 WARNs.
- [x] AC5: The docstring's tolerance enumeration corresponds one-to-one with
      the tolerance branches in the shipped function body — each named
      tolerance has a live branch, no branch is unnamed, and any stated count
      agrees — checked by reading the function's shipped bytes at review.
- [x] AC6: All three suites pass from the repo root (`scripts/tests`,
      `skills/tests`, `hooks/tests`), each exit code checked individually.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T1, T2
- AC5 → T3
- AC6 → T5
<!-- T4 (LESSONS/llm-wiki correction) and T6 (intraclass evidence) serve the
     Scope's record-hygiene and evidence clauses; no AC maps to them. -->

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Tests first — add fixture cases for AC1–AC4 to the dangling-id test
      class in `scripts/tests/test_scripts.py` (existing class at :1472),
      matching its fixture style; confirm each new WARN-expecting case is red
      against the unmodified check where the tolerance would wrongly fire.
- [x] T2: Implement the legacy scan + skip in `check_dangling_ids`
      (`scripts/cairn_validate.py:1735`): compute the legacy max with a
      `default=0` floor over `M<NN>` tokens in `cairn/legacy/**/*.md`; skip
      unresolved M-tokens `<=` that max; `legacy/` stays excluded from the
      live walk.
- [x] T3: Update the docstring to enumerate the three tolerances (above-max,
      repo-slug, legacy-max) with the count word agreeing, wording derived
      from the shipped body (derived-claims rule).
- [x] T4: Correct the M115 lesson line in `cairn/LESSONS.md` in place, marked
      `(corrected M135)`: a clean line also tolerates ids at/below the legacy
      max when `cairn/legacy/` exists. Check `cairn/references/llm-wiki.md`'s
      advisory description; correct only if it states the tolerance set.
- [x] T5: Run the three suites from the repo root, one command each, exit
      codes checked individually.
- [x] T6: Run `cairn_validate` against the local intraclass checkout before
      and after the change; record both WARN counts in the work log as dated
      evidence (baseline 321, 2026-08-06). Skip with a logged line if the
      checkout is absent.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-06: created by /milestone-plan from the 2026-08-06 candidate row (intraclass audit); criteria audit ran — 9 findings: AC1 vacuity, AC2 deletion wording, AC3 universal heading, AC4 unverifiability+count word, empty-legacy gap, and the M115 lesson staleness fixed into the wording above; M-only asymmetry and intraclass evidence went to the gate (both resolved as recommended); legacy-max-above-live-max judged behaviorally identical, docstring states the skip as independent.
- 2026-08-06: plan gate chose M-token-only tolerance over M+D symmetry because all 321 measured WARNs are M-tokens and pre-migration systems rarely use cairn's D-id format; falsified by a migrated repo flooding on entombed D-ids.
- 2026-08-06: plan chose scanning `cairn/legacy/` for its max M-token over an explicit declared ceiling (config surface) because the scan needs no new file format and D-023's doctrine tolerates the overshoot; falsified by a legacy corpus whose stray high M-token masks a real dangler class in practice.
- 2026-08-06: T1 — four fixture cases added to TestDanglingIds; red-first verified: AC1's case fails against the unmodified check (M12 WARNs), the other eight in the class pass.
- 2026-08-06: T2+T3 — legacy-max scan (`default`-0 floor via seeded `max`, recursive `.md` walk) and `> legacy_max` filter added; docstring re-derived from the body ("Three tolerance rules", recursive-scan wording corrected before commit); all three suites green (341/743/103), exit codes checked individually.
- 2026-08-06: T4 — M115 lesson line corrected in place, marked (corrected M135); `references/llm-wiki.md:187` says only "FP-tolerant", does not state the tolerance set, left untouched per the task's condition.
- 2026-08-06: T5 — three suites green from repo root (scripts 341, skills 743, hooks 103), each exit code captured directly, no pipes (M56 lesson).
- 2026-08-06: T6 — intraclass evidence: main's validator 322 dangling WARNs (baseline drifted +1 from the morning's 321), branch validator 0, exit 0 both runs; intraclass legacy max M47 and every WARNed id ≤ 47, so the tolerance removed exactly the flood. Tasks complete; status → review.
- 2026-08-06: review return 1 (defect-return count: 1) — floor fired on O-F1 (92): unbounded legacy-max lets one stray high M-token silently disable the whole M-dangling check; O-F3 (87) M00 skipped with no legacy dir; O-F2 (85) non-UTF-8 legacy file silently drops the tolerance. Status → in-progress for the three fixes plus in-passing sub-threshold items (class docstring, boundary fixture, nested fixture).

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Evidence gathered fresh 2026-08-06, on the branch at PR #135:

- AC1: `test_legacy_max_tolerates_entombed_id_cite` ok (fixture: live max M60, legacy max M47, unassigned M12, slug-free line → `OK    dangling id tokens`), fresh run exit 0.
- AC2: `test_legacy_tolerance_gated_on_directory` ok (same fixture minus legacy/ → WARN naming M12), fresh run exit 0.
- AC3: `test_legacy_max_does_not_widen_other_skips` ok (M55 WARNs; D-002 WARNs with legacy/ present), fresh run exit 0.
- AC4: `test_empty_legacy_directory_is_inert` ok (M-token-free legacy/ → M12 WARNs), fresh run exit 0.
- AC5: shipped bytes read at review (`cairn_validate.py:1735-1804`): docstring names three tolerances (above-max, repo-slug, legacy-max), the body carries exactly those three mechanisms, count word "Three" agrees, no unnamed branch.
- AC6: three suites from repo root, exit codes captured directly: scripts 341 exit 0, skills 743 exit 0, hooks 103 exit 0.

Consistency gate 2026-08-06: `cairn_validate` exit 0, all checks pass; generic profile names no toolchain checks.

Fan-out 2026-08-06: [O] diff-bug 16 findings, [S] blame-history 6, [S] prior-review 0 (no prior-review evidence on either surface — probe found zero inline PR comments). [S] scorer over all 22.

Actioned (≥80), all triaged fix-now, return floor fired on O-F1 (92 ≥ 90, deliverable defect):
- O-F1 (92): a single stray high M-token anywhere in `cairn/legacy/` (a date-shaped `M20260806`, a fenced example `M99`) sets `legacy_max ≥ m_max` and silently disables the entire M-dangling check — the exact inverse of the Goal, verified empirically. Fix: count only legacy tokens `< m_max` into the ceiling.
- O-F3 (87): with no `cairn/legacy/` at all, the `> legacy_max` filter with floor 0 silently skips `M00` — a behavior change main does not have, contradicting the docstring's inert claim (outside AC2/AC4's fixture domains, so no AC breach). Fix: `None` sentinel when absent/token-free.
- O-F2 (85): a non-UTF-8 legacy file raises under `encoding="utf-8"`, is swallowed by the bare except, and silently drops the tolerance — entombed pre-migration files are the likeliest non-UTF-8 corpus. Fix: `errors="replace"` on the legacy read.

Logged below threshold (19; surfaced, not actioned — IP3): O-F6/B-F1 (78/78) stale two-tolerance class docstring in TestDanglingIds — will fix in passing with the return; O-F4 (68) `<=` boundary M47 unpinned by any fixture — will fix in passing; O-F5 (65) recursion unverified by fixtures — will fix in passing; B-F2 (62) generic bare-except shape, duplicative of O-F2; O-F7 (45) test name says empty-dir, fixture is token-free file (matches AC4 as written); O-F9 (45) nested `legacy/` dirs pruned from live walk but not in ceiling scan; O-F14 (35) AC3 lacks assertNotIn M12 (AC1 covers it); O-F12 (35) unconditional legacy read cost; O-F13 (30) AC2 fixture re-inlined; O-F8 (25) .md-only scan is the Scope as written; B-F3 (25) D-005 read-dependency tension is the Scope's intent; O-F16 (20) work-log named :187 only though :134 also examined and correctly left; O-F10/O-F15 (15/15) cosmetic wording; O-F11 (10) dead `sorted`; B-F4/B-F5/B-F6 (5/5/8) reported-compliant completeness notes.
