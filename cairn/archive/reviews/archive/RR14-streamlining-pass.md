# RR14: Streamlining pass over shipped code (M164)

- **Date:** 2026-08-29
- **Brief:** cairn/reviews/RB14-streamlining-pass.md
- **Corpus:** the 22 files the brief lists (read in full), plus hooks/hooks.json as context
- **Baseline:** both gating suites green before any change — scripts/tests: 327 tests OK; hooks/tests: 121 tests OK

## 1. Length

The runtime code is lean for what it does; most of its bulk is comment prose
carrying defect history (M-references, review findings), which is deliberate
institutional memory, not code that fails to earn its length (see Q5). The
sites below are the ones where actual code does not earn its lines.

- `scripts/cairn_status.py:21` — `counts = {s: [] for s in cs.STATUSES}` is a
  redundant initialization: line 23 uses `counts.setdefault(...)` and line 27
  uses `counts.get(status, [])`, so every access already tolerates a missing
  key. The pre-seeded keys (including `candidate`, which the printed tuple at
  line 25 deliberately omits) are never needed. Shorter form: `counts = {}`.
  Behavior identical; `TestStatus.test_snapshot` attests the output.
- `scripts/cairn_next.py:40-49` — `_workable(rows, done)` is computed twice on
  the no-active path: once as `workable_now` inside the `else` branch (line 40)
  and again unconditionally at line 49. Shorter form: compute `workable` once
  before the recommendation block and use it in both places.
- `scripts/cairn_cost.py:366-369` — `audit_line` walks the records twice with
  the same predicate: `any(milestone_of(r) == mid ...)` and then the list
  comprehension inside the `aggregate` call. Shorter form: bind
  `sub = [r for r in records if milestone_of(r) == mid]` once; `if not sub:`
  is the no-records branch, `aggregate(sub, lambda r: mid)[mid]` the bucket.
- `scripts/cairn_validate.py:665` — `token = slot` is a pure rename after the
  shape check; the seven subsequent uses of `token` can just use `slot`
  (or keep the name and drop the intermediate — one line either way).
- `scripts/cairn_validate.py:707` and `scripts/cairn_impact.py:31` — the same
  `\b[IG]P\d+\b` principle-id regex is defined in both files. Two lines total;
  hoisting it into `cairn_scripts` buys one line at the cost of a new
  cross-module constant. Noted for completeness; not worth a recommendation.
- `hooks/cairn_common.py:329-334` — `parse_roadmap_rows` is a six-line subset
  wrapper over `parse_roadmap_rows_full` with exactly one caller
  (`session_context.py:262`). It could be inlined as an unpack-and-ignore at
  the call site, but the named subset reads better than `for mid, _t, status,
  _d, _p, relpath in ...`; keep it.
- Test-side, the clear cases: `scripts/tests/test_scripts.py:3795-3796`
  defines `_days_ago(n)` character-for-character identical to `days_ago(n)` at
  line 740-745 of the same file (the release-window section grew its own copy);
  and `scripts/tests/test_scripts.py:82-96` (`_load_validate`) re-executes
  `cairn_validate` through `importlib.util.spec_from_file_location` on **every
  call** — it is called ~20 times across the suite — while lines 129-136
  (`_VALIDATE_MOD` / `_validate_module`) implement a cached variant of the same
  thing for the in-process runner. One cached loader (a plain `import
  cairn_validate` after the sys.path shim, which `_load_scripts` at line
  98-104 already demonstrates) replaces all three mechanisms.
- `scripts/tests/test_scripts.py:2030-2057` —
  `test_shipped_reference_profiles_are_valid` re-implements the module loader
  inline (its own `spec_from_file_location`, its own `sys.path.insert`/`pop`
  try/finally) and runs `import cairn_scripts as cs_mod` at line 2052 *inside*
  the per-profile loop. `_load_validate()` and `_load_scripts()` already exist
  for exactly this.

Dead/unreachable code: none found that is not already documented as
deliberate. The one flagged-as-unreachable branch
(`scripts/cairn_scripts.py:96-99`, the ROADMAP.md entry of
`REQUIRED_SCAFFOLD_FILES`) documents its own unreachability and the reason it
is kept; see Q5.

## 2. Directness

- **Fabricated argv to reuse the root resolver.** `cairn_scripts.resolve_root`
  (scripts/cairn_scripts.py:128-134) takes an argv list and reads `argv[1]`.
  The two scripts with real flag parsing must therefore fake an argv:
  `scripts/cairn_impact.py:160` — `cs.resolve_root(["cairn_impact"] +
  ([root_arg] if root_arg else []))` — and `scripts/cairn_cost.py:421` the
  same. The direct form is a start-path entry point: `resolve_start(start)`
  raising `NotCairn`, with `resolve_root(argv)` a two-line wrapper over it for
  the three positional-ROOT scripts. Call sites become
  `cs.resolve_start(root_arg or os.getcwd())`. No observable behavior changes
  (same walk, same exception, same exit-2 text); `TestOutsideCairn`,
  `TestValidateCliContract.test_impact_exits_2_outside_cairn` and the cost
  tests attest it.
- **Raw subprocess beside an existing git helper.**
  `scripts/cairn_impact.py:82-93` (`_base_commit`) shells out with
  `subprocess.run` directly although `cairn_common.git` (never raises, returns
  `(rc, stdout)`) is importable one hop away. Converting `_base_commit` is a
  small directness win. `changed_principles` (lines 96-117) should **stay** on
  raw subprocess: its two distinct stderr warnings ("git diff failed" vs "git
  unavailable") key on returncode-vs-exception, a distinction `cc.git`
  deliberately erases.
- **Flag parameter selecting between two callers** —
  `scripts/cairn_validate.py:267` `_provenance_block(path,
  for_extraction=False)` is the textbook shape the brief names. In this case
  the flag is the right call: the docstring (lines 281-292) documents why the
  two callers need opposite protections (a wider block ERASES failures for the
  hard CHECK and only the advisory can afford it, M81 review F1), and a split
  into two functions would duplicate the block-collection loop the flag
  parameterizes by one clause. Do not split; see Q5.
- **State threaded through record mutation** — `cairn_cost.read_records`
  stamps `record["_session"]` and `session_of` reads it back
  (scripts/cairn_cost.py:125-129, 171). This is threading state where a tuple
  return would do, but every aggregation keys off plain records, the stamp is
  documented at both ends, and tests pin it (`test_session_id_comes_from_the_
  transcript_filename`). Converting to `(session, record)` tuples would touch
  every consumer for no reader benefit. Leave it.
- **Uniform-signature lambdas in the check registry** —
  `scripts/cairn_validate.py:1789-1828` wraps all 23 checks/advisories in
  `lambda root, rows:` adapters even where the target already has that exact
  signature (`check_mirror`, `check_dependencies`, `check_orphans`,
  `check_id_uniqueness`, `check_dangling_ids`). Five could be bare function
  references. The counter-argument is real: the uniform lambda column makes
  every row read identically and makes each function's true arity a
  local fact rather than a registry constraint. Weak-consider at most.

## 3. Simplification

Concrete rewrites, all behavior-preserving and attested by the existing
suites (each is also a numbered recommendation below):

1. `cairn_status.py:21` — drop the STATUSES-keyed init (Q1). Attested by
   `TestStatus.test_snapshot` (exact count lines including a zero-count
   status via `.get`).
2. `cairn_next.py:40-49` — single `_workable` call (Q1). Attested by
   `TestNext` (all four recommendation branches are pinned).
3. `cairn_cost.py:366-369` — single filtered list in `audit_line` (Q1).
   Attested by `TestMilestoneFlagIsHonouredOrRefused` and
   `TestSubagentBlindSpot.test_every_report_surface_carries_the_spawn_count`.
4. `cairn_validate.py:665` — drop `token = slot` (Q1). Attested by the whole
   binding-criteria suite.
5. `cairn_scripts.resolve_root` start-path refactor (Q2). Attested by the
   exit-2 CLI tests across all five scripts.
6. `cairn_impact._base_commit` on `cc.git` (Q2). Attested by
   `test_changed_derives_from_design_diff` and
   `test_changed_sees_committed_branch_edit`. One caveat the suites would
   NOT catch: `cc.git` imposes a 10s timeout where `_base_commit` currently
   has none — on a pathological repo a merge-base slower than 10s would now
   fall through to the next ref instead of hanging. I judge that an
   improvement, but it is technically a behavior difference no test
   witnesses; flagged per the brief's instruction.

Rewrites I considered and rejected as not simplifying (details in Q5): a
shared renderer for the near-identical CHECKS/ADVISORIES loops in
`cairn_validate.run` (lines 1831-1861) — the two loops differ in tally
semantics (checks count 1 per failing check, advisories count findings) and
in labels, so a shared function needs three parameters and reads worse than
the 15 duplicated lines; `argparse` for the two hand-rolled `parse_args`
functions — argparse's usage/error text differs from the pinned stderr
contract, so it changes observable behavior for zero length saved.

## 4. Test-suite streamlining

The four test files are unusually disciplined (fixtures shared through
`Tree`/`ScriptCase`/`RepoFixture`, the M102 template/in-process optimizations
already applied, positive twins paired with negative asserts). The findings:

- **Duplicated helper**: `test_scripts.py:3795-3796` `_days_ago` ==
  `days_ago` (line 740). Remove `_days_ago`; the release-window class uses
  `days_ago`.
- **Triplicated module loading**: `test_scripts.py:82-96` + 129-136 + the
  inline loader at 2030-2057 (Q1). Collapse to one cached loader.
- **Duplicate test, same contract, same fixture**:
  `test_scripts.py:1253-1260` `test_a_status_dated_only_in_the_future_is_
  still_flagged` is byte-for-byte the same install + assertion as
  `test_scripts.py:1154-1162` `test_future_verification_date_is_flagged_not_
  silently_exempt` (both: `verified {days_ago(-30)} against the source`,
  both assert `dated {ahead}, in the future`). The second was added as "the
  other side of F4" but re-asserts the identical contract at the identical
  input. Remove one — survivor:
  `test_future_verification_date_is_flagged_not_silently_exempt` (it carries
  the F5 rationale); move the one-line F4-side comment onto it.
- **Duplicate test, subsumed by a loop**: `test_scripts.py:3240-3245`
  `test_non_iso_date` injects `07/11/2026` and asserts
  `non-ISO date '07/11/2026'`; `test_non_iso_date_formats` (3247-3257) loops
  over six formats *including* `"07/11/2026"` with the identical fixture
  shape and identical assertion. Remove `test_non_iso_date` — survivor:
  `test_non_iso_date_formats`, subTest `bad="07/11/2026"`. Its comment about
  the clean tree proving ISO passes should move to the survivor.
- **Duplicate test across classes + a tmpdir leak**:
  `test_bc_ac_ingest_form.py:130-135` `test_numbering_and_mapping_together_
  clear_the_red` rebuilds the AC_PRESCRIBED fixture and asserts both checks
  quiet — exactly what `TestPrescribedFormIsQuietOnBoth` (lines 89-101)
  already asserts, test for test. It also builds into `tempfile.mkdtemp()`
  with no cleanup, leaking a directory per run. Remove it — survivors:
  `TestPrescribedFormIsQuietOnBoth.test_binding_criteria_quiet` and
  `.test_coverage_complete_quiet` cover both halves of its contract. (If the
  explicit-twin-inside-the-negative-class reading is preferred, keep it but
  switch to `TemporaryDirectory` — the leak is real either way.)
- **Triplicated scaffolding**: `test_hooks.py:478-487`, `606-615`, `787-792`
  — three setUp methods each insert the same sys.path entries with
  addCleanup and import `session_context`/`cairn_scripts`. Hoist to module
  level (one sys.path block + two imports at the top, beside `HOOKS_DIR`),
  or to a small mixin; the three setUps shrink to assignments or vanish.
  Module-level imports do not affect the subprocess-driven tests (those spawn
  their own interpreters), and the METHODOLOGY NOTE's subprocess rule is
  about hook contracts, which these direct-import classes already document
  themselves as exceptions to.
- **Identical fixture built twice for two assertions**:
  `test_scaffold_check.py:102-133` — `test_legacy_entry_satisfies_scaffold_
  check` and `test_legacy_entry_warns_with_the_new_name` build the same
  gitignore state and run validate twice to assert on the same report
  (PASS line vs WARN line). They can merge into one test with both
  assertions; two names for one run is the only cost. Mild — consider.
- **Function-local imports repeated**: `test_cairn_cost.py` imports
  `tempfile` in four tests (144, 330, 372, 457), `os` inside
  `_live_records_or_skip` (57), `mock` inside one test (325). Hoisting to the
  module header removes seven lines and matches the other three files' style.
  Cosmetic.

Coverage overlaps I examined and would NOT remove: the two
`test_decoy_provenance_heading...` tests (test_scripts.py:506 and 1290) hit
two different readers (hard CHECK vs staleness advisory) of the same parser;
`test_never_verified_page_is_flagged` (816) is nominally subsumed by the
decoration×layout grid (1264) but is the named smoke case a failure is
diagnosed from, and the grid's subTest failure output is far less legible —
keep both; the TestExemptSetMirror / TestHeadingNormalizationContract /
TestMilestoneBodyLineCount trio looks redundant from altitude but pins three
different facts (constant equality across packages, normalization agreement
per rendering, per-function contract), and the second exists precisely
because the first was shown insufficient (measured mutation, 2026-07-30).

## 5. Not worth it

Named so a later pass does not "fix" them:

- **The CAP_EXEMPT_SECTIONS mirror** (`hooks/session_context.py:79` vs
  `scripts/cairn_scripts.py:82`). Looks like copy-paste begging for a shared
  constant; it is a documented cross-package mirror (a hook may import only
  `cairn_common`) held equal by a two-sided test
  (`TestExemptSetMirror`). Consolidating it means either a new import-path
  arrangement (milestone-sized per the brief's constraints) or moving the
  constant into `cairn_common` — which is a real option but changes where
  scripts get their exempt set from and should be its own decision, not a
  streamlining edit.
- **The older CMD_POS copies** in `hooks/commit_guard.py:39-40` and
  `hooks/force_push_guard.py:45-46` versus `cairn_common.py:38`. The
  duplication is known and already carried as a ROADMAP candidate
  (cairn_common.py:36-37 says so). Consolidating is NOT behavior-preserving:
  the shared pattern admits env-assignment prefixes (M162), so
  `FOO=1 git commit`/`FOO=1 git push -f origin main` would start matching in
  guards that today ignore them. That is probably the desired end state, but
  it is a guard-behavior change — milestone-sized, and already tracked.
- **`_provenance_block`'s `for_extraction` flag**
  (cairn_validate.py:267). The one flag-parameter in the corpus, and it is
  load-bearing: the docstring records why one shared rule cannot serve both
  callers and what a widened block does to the hard CHECK (erases FAILs).
  Splitting duplicates the collection loop for a cosmetic win.
- **`REQUIRED_SCAFFOLD_FILES`' ROADMAP.md entry**
  (cairn_scripts.py:96-99). Unreachable through the CLI (resolve_root exits 2
  first) and says so; kept so the tuple is the complete §1 set for the
  planned cairn-init-repair consumer. Deleting it as "dead" would be wrong.
- **The near-twin nudge hooks** (`idea_guard.py`, `memory_guard.py`; also the
  emit envelope repeated across guards). Hooks are independently registered
  entry points; the small structural duplication is the price of each staying
  runnable as its own script, and the shared parts that matter already live
  in `cairn_common`. Extracting a "nudge hook" template would add a layer for
  ~15 saved lines.
- **`session_context.build_context`'s shedding/truncation arithmetic**
  (session_context.py:286-344). Every non-obvious move (floor costing at
  budget 0, notice reserved at full width, ROADMAP cut instead of tail
  slice) exists because a simpler version shipped and failed a specific way,
  and each is pinned by a test in TestSessionContextReadBound. Simplifying
  here means re-earning those defects.
- **The `_pasted_findings` signature table and its removed extent-inference**
  (cairn_validate.py:917-1005, 1442-1512). The comments record three rounds
  of a "smarter" chunker being removed; the shipped one-finding-per-paste
  contract, the ten narrow signatures, and their per-signature near-miss
  controls (test_scripts SIGNATURE_LINES / NEAR_MISS_LINES) are the
  equilibrium. Any streamlining that merges signatures or trims controls
  re-opens the widening trap the tests exist to catch.
- **The staleness classifier's clause machinery** (cairn_validate.py:996-1330
  — `_clauses`, `_clause_claims`, `_qualified_partial`, `_resolve_claims`).
  Six functions for what looks like a keyword scan, but the layering IS the
  fix history (M81→M83→M89, seven review findings), and each layer has a
  fixture that fails without it. The prose-heavy comments are the record.
- **Subprocess-per-test in test_hooks.py.** Tempting to convert more hook
  tests to direct imports for speed; the METHODOLOGY NOTE explains why the
  JSON-contract tests must stay subprocess-shaped, and the M102 template
  optimization already removed the expensive part (per-test git spawns).
- **The crossed fixture grids** in TestReferencesStaleness (decoration ×
  layout × phrasing). 48+ subTests that look thinnable; the comments at
  test_scripts.py:1170-1173 and 1267-1268 pre-empt exactly that: the grids
  run in-process and cost nothing, and walking instead of crossing is the
  vacuity trap (LESSONS M57/M79).
- **Hand-rolled `parse_args` in cairn_impact/cairn_cost.** argparse would be
  shorter but changes the pinned usage/stderr text and error phrasing —
  observable contract, out of scope.
- **The long defect-history comments across all shipped files.** They
  dominate the line counts (cairn_validate.py is roughly half comment prose)
  and are the repo's memory of *why* the code is shaped this way; a prose-size
  program (D-114) governs prose, and trimming them here would be scope
  violation dressed as streamlining.

## Beyond the brief

- `test_bc_ac_ingest_form.py:133` leaks a temp directory every run
  (`tempfile.mkdtemp()` with no cleanup) — folded into R6 since the
  recommended removal of the test also removes the leak.
- `hooks/tests/test_hooks.py:1817` — `commands()` treats any entry as
  matching when `event == "SessionStart"`; correct today (SessionStart
  entries carry no matcher) but the condition reads as a bug. A one-line
  comment would help; no code change needed.
- `commit_guard.committed_paths(command, cwd)`
  (hooks/commit_guard.py:48) is always called with the repo *root* (main
  passes `root`, with a comment explaining why); the parameter name `cwd`
  contradicts that. Rename to `root` when touching the file. Cosmetic.

## Recommendations

Each is small enough to verify by running the two gating suites
(`python3 -m unittest discover -s scripts/tests` and `-s hooks/tests`, both
exit 0), except where marked.

- **R1 (apply)** — scripts/tests/test_scripts.py:3795-3796: delete
  `_days_ago`; use the identical `days_ago` (line 740) in
  TestReleaseWindowAdvisory.
- **R2 (apply)** — scripts/tests/test_scripts.py:82-96 and 129-136: replace
  `_load_validate`'s per-call importlib exec and the parallel
  `_VALIDATE_MOD`/`_validate_module` cache with one cached loader (sys.path
  shim + plain `import cairn_validate`, as `_load_scripts` already does);
  point `_run_validate_inproc` and every `_load_validate()` caller at it.
- **R3 (apply)** — scripts/tests/test_scripts.py:2030-2057: rewrite
  `test_shipped_reference_profiles_are_valid` to use `_load_validate()` /
  `_load_scripts()`; delete its inline spec-loader, the try/finally sys.path
  pop, and the per-iteration `import cairn_scripts as cs_mod`.
- **R4 (apply)** — scripts/tests/test_scripts.py:1253-1260: remove
  `test_a_status_dated_only_in_the_future_is_still_flagged`; survivor:
  `test_future_verification_date_is_flagged_not_silently_exempt`
  (lines 1154-1162, identical fixture and assertion); carry its F4-side
  comment over.
- **R5 (apply)** — scripts/tests/test_scripts.py:3240-3245: remove
  `test_non_iso_date`; survivor: `test_non_iso_date_formats` (its
  `bad="07/11/2026"` subTest asserts the same message on the same fixture
  shape); move the ISO-passes comment to the survivor.
- **R6 (apply)** — scripts/tests/test_bc_ac_ingest_form.py:130-135: remove
  `test_numbering_and_mapping_together_clear_the_red` (also fixes its
  mkdtemp leak); survivors:
  `TestPrescribedFormIsQuietOnBoth.test_binding_criteria_quiet` and
  `.test_coverage_complete_quiet`, which assert the identical contract on the
  identical fixture.
- **R7 (apply)** — hooks/tests/test_hooks.py:478-487, 606-615, 787-792:
  hoist the three duplicated sys.path shims + imports of
  `session_context`/`cairn_scripts` to module level (or one mixin); shrink or
  delete the three setUps.
- **R8 (apply)** — scripts/cairn_status.py:21: `counts = {}` — the
  STATUSES-keyed init is redundant with the setdefault/get accesses.
- **R9 (apply)** — scripts/cairn_next.py:40-49: compute
  `workable = _workable(rows, done)` once, before the recommendation block;
  use it for both the recommendation and the listing.
- **R10 (apply)** — scripts/cairn_cost.py:366-369: in `audit_line`, filter
  the records to `mid` once; use the list for both the emptiness check and
  the `aggregate` call.
- **R11 (apply)** — scripts/cairn_validate.py:665: drop the `token = slot`
  rename (use `slot` in the seven `token` sites, or rename at the match).
- **R12 (consider)** — scripts/cairn_scripts.py:128-134: add
  `resolve_start(start)` (walk + NotCairn) and make `resolve_root(argv)` a
  wrapper over it; convert the fake-argv call sites
  scripts/cairn_impact.py:160 and scripts/cairn_cost.py:421 to
  `cs.resolve_start(root_arg or os.getcwd())`. Behavior identical; consider
  rather than apply only because it widens the shared module's API by one
  function.
- **R13 (consider)** — scripts/cairn_impact.py:82-93: run `_base_commit`'s
  merge-base probes through `cairn_common.git` instead of raw subprocess.
  Leave `changed_principles` as is (its two stderr messages key on
  returncode-vs-exception). Caveat the suites can't attest: `cc.git` adds a
  10s timeout `_base_commit` currently lacks (see Q3 item 6).
- **R14 (consider)** — scripts/cairn_validate.py:1789-1828: use bare function
  references for the five registry entries whose signature is already
  `(root, rows)` (`check_mirror`, `check_dependencies`, `check_orphans`,
  `check_id_uniqueness`, `check_dangling_ids`). Weak: the mixed style may
  read worse than 5 redundant lambdas; reject if uniformity is preferred.
- **R15 (consider)** — scripts/tests/test_scaffold_check.py:102-133: merge
  `test_legacy_entry_satisfies_scaffold_check` and
  `test_legacy_entry_warns_with_the_new_name` into one test asserting both
  lines of the same report (one fixture build, one run).
- **R16 (consider)** — scripts/tests/test_cairn_cost.py:57, 144, 325, 330,
  372, 457: hoist the repeated function-local `os`/`tempfile`/`mock` imports
  to the module header.
- **R17 (reject — behavior change, already tracked)** — consolidating
  commit_guard/force_push_guard onto `cairn_common.CMD_POS`
  (hooks/commit_guard.py:39-40, hooks/force_push_guard.py:45-46): the shared
  pattern's env-assignment prefix run would change what those guards match
  (`FOO=1 git commit` starts nudging, `FOO=1 git push -f origin main` starts
  denying). Milestone-sized, and cairn_common.py:36-37 records it as an
  existing ROADMAP candidate.
- **R18 (reject — load-bearing flag)** — splitting
  `_provenance_block(for_extraction=)` (scripts/cairn_validate.py:267) into
  two functions: the divergence is the documented M81-F1 fix and a split
  duplicates the collection loop; see Q5.
- **R19 (reject — observable contract)** — replacing the hand-rolled
  `parse_args` in cairn_impact/cairn_cost with argparse: shorter, but the
  usage/stderr text and error phrasing are pinned output; argparse rewords
  them.

No `## Binding criteria` section: the brief's header slot says
"not requested".
