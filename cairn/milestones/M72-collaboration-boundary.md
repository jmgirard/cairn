<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M72: Collaboration boundary — what survives a merge outside cairn, plus PR-bound approval

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m72-collaboration-boundary` · https://github.com/jmgirard/cairn/pull/70   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

State plainly which parts of cairn's approval model survive a merge made
outside a cairn session, and bind the merge-approval marker to the specific PR
it authorizes.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a rulebook passage in "Git and approval model" naming what is
agent-session-scoped (merge_guard, force_push_guard) versus honor-system under
a GitHub-UI merge, a merge queue, or a contributor without the plugin; a
plain-words README subsection saying the same to a human; `merge_guard.py`
reading the marker body and refusing a `gh pr merge` for a PR the marker does
not name; the two marker-writing skills updated to the bound form. Closes RR01
§10 rec 4 (`cairn/reviews/archive/RR01-architecture-retrospective.md:395-400`),
which recorded this gap and was never actioned.

**Out:** an entry point for externally-authored PRs → M73. Issue enumeration →
M74. Concurrent-cairn-operator races (ID allocation, duplicate D-numbers,
pull-before-plan, the one-in-progress cap) → candidate rows. A CONTRIBUTING /
PR-template scaffold → candidate row. Branch-protection compatibility for the
docs-only direct pushes → candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1 — `skills/shared/tracking-rules.md` "Git and approval model" states
      which guarantees are enforced only inside a cairn-equipped session and
      which degrade to honor-system when the merge happens elsewhere (GitHub
      UI, merge queue, unplugged contributor), naming `merge_guard` and
      `force_push_guard` as agent-session-scoped. Evidence: the passage quoted
      + its guard test green.
- [x] AC2 — `README.md` carries a human-facing subsection saying the same in
      plain words: what cairn will block, and what it cannot see.
- [x] AC3 — `hooks/merge_guard.py` denies `gh pr merge <N>` when the marker
      body names a different PR, with the deny reason naming both numbers; it
      also denies a `gh pr merge` that names no PR at all, since an approval
      that cannot be checked against a command is not an approval. Neither
      denial consumes the marker. Evidence: three `TestMergeGuard` cases.
      *(Amended 2026-07-18 at the implement gate — the plan assumed the merge
      command carried a PR number; both skills in fact merged bare.)*
- [x] AC4 — the same hook allows-and-consumes when command and marker name the
      same PR, still allows when the marker body names no PR (back-compat for
      markers predating the convention), and leaves the guarded `git merge`
      path unchanged — it has no PR to name. Evidence: three `TestMergeGuard`
      cases.
- [x] AC5 — `/milestone-review` and `/hotfix` write the PR-bound marker form
      at their approval gates. Evidence: grep of the two SKILL.md files
      (tracking lines in this milestone file are not evidence).
- [x] AC6 — the new prose-guard file is registered in
      `skills/tests/test_mutation_harness.py`; the completeness meta-test is
      green.
- [x] AC7 — the `verify` slot is clean: all three `unittest discover` suites
      (`skills/tests`, `scripts/tests`, `hooks/tests`) pass from the repo root.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T5
- AC2 → T2
- AC3 → T3, T4
- AC4 → T3, T4
- AC5 → T3
- AC6 → T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Write the boundary passage into `skills/shared/tracking-rules.md`
      "Git and approval model" (after the `.merge-approved` paragraph,
      `:265-271`). Keep it ≤10 lines; the rulebook is already long.
      *(RB tripwire: ip-touching — the passage states where IP1's mechanical
      backing stops.)*
- [x] T2 — Add the README subsection. Plain words, no rulebook jargon; this is
      the surface a collaborator reads.
- [x] T3 — Bind the marker: `hooks/merge_guard.py` parses a PR number from the
      marker body and compares it to the `gh pr merge <N>` target
      (`hooks/cairn_common.py:29` `GH_PR_MERGE` is the existing detection);
      mismatch → deny; no PR token in the body → today's existence check.
      Update the marker-write lines in `skills/milestone-review/SKILL.md` and
      `skills/hotfix/SKILL.md:54-57` to the bound form.
- [x] T4 — Extend `TestMergeGuard` in `hooks/tests/test_hooks.py:186-292`:
      match allows+consumes, mismatch denies, PR-less body allows. Check
      `merge_guard_post`'s restore path still keys on the identical detection.
- [x] T5 — New guard test for the T1 passage; register it in
      `skills/tests/test_mutation_harness.py` (per-file registration, ≥1
      exemplar block on ONE physical line — M59/M65).
- [x] T6 — Run all three suites from the repo root; update `cairn/DESIGN.md`'s
      "Known issues" honor-system bullet to cite the new passage instead of
      restating it.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: in-progress on `m72-collaboration-boundary`.
- 2026-07-18: implement gate — marker binding requires the explicit PR number in the merge command (bare `gh pr merge` denied); marker stays prose with `for PR #<N>` appended; ip-touching tripwire on T1 not escalated (user choice).
- 2026-07-18: T1 — boundary passage + PR-binding bullet added to tracking-rules "Git and approval model"; three single-line mutation anchors verified unique.
- 2026-07-18: T2 — README "Working with collaborators" section; the "Merges are yours" bullet's unqualified "mechanically blocks" claim corrected to name its scope.
- 2026-07-18: AC3/AC4 amended via the implement gate — the plan assumed the merge command named a PR, but both skills merged bare (`gh pr merge --squash`), so the binding needed a deny-on-unnamed rule and the skills' merge commands changed; user chose this at the step-3 gate.
- 2026-07-18: T3 — `gh_merge_pr_number`/`marker_pr_number` in `cairn_common`; `merge_guard` denies mismatched and unnamed PRs without consuming the marker; both approval-writing skills updated to the bound marker + explicit-number merge. T3+T4 landed in one commit (implementation inseparable from its tests).
- 2026-07-18: T6 — DESIGN known-issues + hook-inventory bullets cross-reference the rulebook passage rather than restate it; all three suites green (246/96/66), `cairn_validate` all-pass, `cairn_impact --changed` traces IP1 to the declared slot; plan-owned body 120/150.
- 2026-07-18: T5 — `test_collaboration_boundary.py` (12 tests across boundary, PR binding, README); five mutation entries registered, all proven; skills suite 234 → 246.
- 2026-07-18: T4 — six `TestMergeGuard` cases (mismatch, bare, match, URL/value-flag parsing, branch-name argument, `git merge` exemption); `shlex` added to the stdlib allowlist in `TestStdlibOnly`.
- 2026-07-18: review — PR #70 opened; all seven criteria executed with fresh evidence; consistency gate clean; three-lens fan-out + scorer ran (prior-PR lens no-opped, no corpus). F4 (82) fixed on the branch: multi-occurrence PR check, 3 regression tests, hooks 66 → 69. Five sub-80 findings logged in the Review section.
- 2026-07-18: review — F1/F2/F5 additionally fixed at the user's direction at the approval gate (marker regex anchored on `for PR #<N>`; `--repo`/`-R` added and `-m` removed from the value-flag set); three more regression tests, hooks 69 → 72.

## Decisions
<!-- owner: implement / review · append-only -->

- 2026-07-18 (implement gate, surfaced by review F7): the PR binding denies an
  unnamed merge *before* consulting the marker, so D-043's "no-PR-token body
  keeping today's behavior for back-compat" is narrower than written — a
  legacy marker still authorizes a numbered merge, but never a bare one.
  Deliberate: an approval that cannot be checked is not an approval, and a
  legacy marker is no reason to skip the check. Not cross-cutting enough to
  supersede D-043; AC3/AC4 carry the amendment note.

## Review
<!-- owner: review · exclusive -->

**PR:** https://github.com/jmgirard/cairn/pull/70 · reviewed 2026-07-18 ·
branch 5 ahead / 0 behind `origin/main` at review start.

### Acceptance-criteria evidence

- AC1 — passage read back from `tracking-rules.md:277-287`: names the web-UI /
  merge-queue / unplugged-contributor paths, both guards by filename, the
  honor-system degradation, and the one-operator assumption. Guard test
  `TestEnforcementBoundary` (5 tests) green.
- AC2 — `README.md` "Working with collaborators" read back; four bullets
  (guards watch this session; the rest was always conduct; contributions come
  in through the operator; concurrent operators unsupported).
  `TestReadmeCollaboratorSurface` (3 tests) green.
- AC3 — `TestMergeGuard` named cases green: mismatch denies naming both
  numbers, bare merge denies, branch-name argument denies; each asserts the
  marker text is intact after the denial. Extended at review for chained
  commands (see F4).
- AC4 — green: `test_allows_and_consumes_when_pr_matches`,
  `test_allows_and_consumes_marker` (legacy `#`-less marker, back-compat),
  `test_git_merge_is_exempt_from_the_pr_check`,
  `test_repeated_merge_of_the_approved_pr_still_allowed`.
- AC5 — `grep` over the two SKILL.md files: `milestone-review:162` and
  `hotfix:58` write the `for PR #<N>` marker form; `milestone-review:174` and
  `hotfix:52` merge with the number spelled out. No other skill writes the
  marker.
- AC6 — `TestRegistryCompleteness` + `TestRegisteredGuardsFailWhenBlanked`
  green: all five M72 blocks proven to fail their guard when blanked; the
  completeness meta-test accepts the new file.
- AC7 — three suites from the repo root: skills 246, scripts 96, hooks 69 —
  all OK.

### Consistency gate

`cairn_validate` exit 0, all 15 checks PASS + 2 advisories OK.
`cairn_impact --changed` traces IP1 to 12 references incl. the declared slot.
The `generic` profile's `consistency-gate` slot names no toolchain checks —
clean no-op.

### Independent review — three lenses + scorer

[O] diff-bug (3 findings), [S] blame-history (3 findings), [S] prior-PR
(**no prior-PR evidence** — 0 inline comments across all 69 merged PRs; this
repo reviews in-session, so the lens has no corpus; expected no-op, zero
findings). Scored by a fresh [S] scorer.

**Actioned (≥80):**

- **F4 (82) — chained-merge bypass.** The detection read only the first
  merge in a command, so a chained second merge rode through on the first
  one's approval — fail-open in exactly the property M72 exists to create.
  **Fixed:** `gh_merge_pr_number` → `gh_merge_pr_numbers` (`finditer`, one
  entry per occurrence); the guard denies if any occurrence names no PR or
  names an unapproved one, and lists every unapproved number in the reason.
  Three regression tests added, incl. one proving a repeat of the *approved*
  PR is still allowed (over-correction guard). Verified by probe.

**Below threshold but fixed at the user's direction at the approval gate**
(one-line fixes in the function F4 already reworked; F1 is an authorization
hole whose trigger the scorer judged unlikely rather than impossible):

- F2 (78) — `--repo`/`-R` absent from `_GH_MERGE_VALUE_FLAGS`, so passing
  `--repo owner/name` before the number denied with a message telling the
  operator to spell out a number they already spelled out. **Fixed:** both
  spellings added to the value-flag set.
- F5 (74) — `-m` was listed as value-taking but for this command it means
  `--merge` (boolean), so `-m 7` falsely denied. **Fixed:** removed, with a
  comment recording why it must not return.
- F1 (68) — `_MARKER_PR` took the first `#N` in the marker, but the
  convention writes the PR last; a hotfix slug containing `#43` would both
  deadlock the approved merge and (inversely) authorize an unapproved one.
  **Fixed:** anchored on the convention's `for PR #<N>` tail; a body that
  does not follow the convention yields None and falls back to the existence
  check, as a pre-convention marker does. Three regression tests (approved
  merge allowed despite a label reference; a label reference cannot authorize
  an unapproved merge; `--repo`/`-R`/`-m` parse correctly). Hooks 69 → 72.

**Below threshold — logged, not actioned (surfaced per IP3):**
- F7 (68) — the milestone's `## Decisions` section was empty though the
  implement-gate choice narrowed D-043's back-compat wording. Recorded above.
- F6 (62) — two new assertions carry no `Mutation(...)` entry; scorer noted
  the finding inverts M53 (registration is per *file*, ≥1 exemplar block), so
  the completeness meta-test is legitimately green — a comment-accuracy nit.
- F3 (55) — "Every guard is a PreToolUse hook on *this* session's own Bash
  calls" is over-broad (5 of 8 hooks are PreToolUse; `stop_guard` is a Stop
  hook, `merge_guard_post` PostToolUse). Scorer noted the wording is D-043's
  own and that the mutation anchors sit on other sentences.
