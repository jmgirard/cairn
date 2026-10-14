<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M250: The plan checks that the work needs a milestone before it plans one

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1, IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/milestone-plan` does in every adopting repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m250-plan-tier-check, https://github.com/jmgirard/cairn/pull/261   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Before `/milestone-plan` investigates, it checks whether the request needs a milestone, and when a hotfix or a direct edit fits instead, it offers that route.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A tier check in `skills/milestone-plan/SKILL.md` step 1, its chip
and the effect of each option, and the work-log line step 4 writes. One
sentence in tracking-rules "Question gates and phase closes" and a D-entry
annotating D-144. README.md's `/milestone-plan` row and a CHANGELOG entry.
A hand-run prose guard in `skills/tests/`.

**Out:** The tier definitions do not change: a one-sitting change to
running code that is not a bug stays a milestone (question set). `/hotfix`
step 1's opposite check does not change. The CLAUDE.md router template
does not change: it already routes before a skill fires. The guest-mode
trivial tier for files outside `cairn/` stays undefined, as it is today;
such a request is a milestone here.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [x] AC1: For a request that names work and that AC2's routers have not
      already tiered, `skills/milestone-plan/SKILL.md` step 1 holds a tier
      check that runs before step 2. It cites tracking-rules "Sizing and the work
      tiers" and puts the request as a whole in exactly one tier: `hotfix`
      when it is a user-visible bug whose fix restores documented behavior
      in one sitting with no design decision; `trivial` when it has no
      runtime surface, fits one sitting with no design decision, and, in
      guest mode, touches only files under `cairn/`; `milestone` otherwise.
      A request whose parts fall in more than one tier, or any of whose
      parts is `milestone`, is a milestone. The skill says the check may
      read the code and docs the request names, and that it does not run
      step 2's sweeps or spawn subagents.
- [x] AC2: The skill says that two invocations are classified `milestone`
      without re-judging, and that the work-log reason names the router:
      an invocation from `/milestone` §4's `milestone` verdict, and a
      `/milestone-plan` for work that `/hotfix` found over the hotfix bar
      earlier in this session, whether that hotfix stopped at step 1 or
      closed at step 7 after a merged-PR re-entry. A request that names no
      work is not checked.
- [x] AC3: When the check finds `hotfix` or `trivial`, the skill poses one
      chip before step 2. Its question text names the tier found and the
      reason. Its options are the tier's route (marked recommended),
      planning a milestone anyway, and stop. The trivial option's
      description says the edit is committed and pushed to the default
      branch (owner mode) or left uncommitted on disk (guest mode).
      tracking-rules "Question gates and phase closes" states that a run
      begins at the plan question set, and that `/milestone-plan`'s tier
      chip, posed only on a `hotfix` or `trivial` finding, comes before it.
- [x] AC4: `skills/milestone-plan/SKILL.md` says what each option of AC3's
      chip does. The hotfix route invokes `/hotfix` through the Skill tool
      with the request as its argument, and the plan skill writes no file.
      The trivial route in owner mode runs `git status`, then edits and
      commits only the files the edit touches and pushes at once. If the
      checkout is not on the default branch, or one of those files already
      has uncommitted changes, it makes no edit and ends with a close block
      naming why. On success it ends with a close block naming the commit.
      In guest mode it writes the edit on disk with no commit and ends with
      a close block. Stop ends with the close block and writes nothing.
      Planning anyway goes on to step 2.
- [x] AC5: The skill says that step 4 writes one work-log line in the
      first milestone file it writes: `tier check: milestone — <reason>`
      when the check found `milestone` and posed no chip, `tier check:
      <tier> — planned as a milestone at the user's choice` after the
      plan-anyway option, or `tier check: not run — work named at the
      question set` for a request that named no work.
- [x] AC6: README.md's `/milestone-plan` row in the commands table says
      that the plan first checks whether the work needs a milestone and
      offers `/hotfix` or a direct edit when it does not. CHANGELOG.md's
      Unreleased section has an entry for the check. No hit of
      `git grep -n -i "milestone-plan" -- README.md CLAUDE.md skills/
      ':!skills/tests'` states that `/milestone-plan` always produces a
      milestone.
- [x] AC7: The `verify` slot's five commands (`cairn/PROFILE.md`) each
      exit 0.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6
- AC2 → T1, T6
- AC3 → T2, T4, T6, T7
- AC4 → T2, T6, T7
- AC5 → T3, T6
- AC6 → T5, T7
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Step 1 (`skills/milestone-plan/SKILL.md:37-41`): add the tier
      check paragraph after the in-progress check, without renumbering
      steps (lesson M148). Trace each entry path to it (lesson M172):
      `/milestone` §4's Do it now (`skills/milestone/SKILL.md`), `/hotfix`
      step 1's over-the-bar route (`skills/hotfix/SKILL.md:33-45`), the
      pane's ✎ press (README.md:320), and a request naming no work.
- [x] T2: Add the chip and each option's effect, with the owner and
      guest arms of the trivial route.
- [x] T3: Add the `tier check:` work-log line to step 4's rules.
- [x] T4: Add the sentence to tracking-rules "Question gates and phase
      closes" (`:378-390`). Append a D-entry annotating D-144 on the chip's
      place before the run. Re-seed the rulebook baseline at its three
      sites (lesson M149): `skills/milestone/SKILL.md:117`,
      `skills/tests/test_cost_audit_line.py:68`,
      `skills/tests/test_mutation_harness.py:120`.
- [x] T5: Edit README.md's `/milestone-plan` row (`:545`) and add the
      CHANGELOG entry. Run AC6's sweep and fix each hit (lesson M112).
- [x] T6: Add a hand-run prose guard in `skills/tests/` pinning the
      clauses of T1-T4, and show each pin red by deleting its clause. Run
      `skills/tests` once and note red or green in the work log (D-109).
      Run the five verify commands and `cairn_validate`.
- [x] T7: Review return 1: the `/hotfix` argument form, the trivial
      route's sync and refusals, and each other fix-now line of the Review
      section.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-14: created by /milestone-plan from the user's request that cairn check a milestone is needed before planning one.
- 2026-10-14: collision sweep: no candidate, planned, or in-progress overlap; M008 (the CLAUDE.md router) and `/hotfix` step 1's over-the-bar check are distinct; no D-entry rejects this; D-144 (one plan gate) is annotated, not contradicted; checker-regress shape not hit.
- 2026-10-14: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-14: lessons harvested: M112 (sweep the doc surface), M148 (prose-guard markers, no step renumbering), M149 (rulebook baseline at three sites), M172 (trace each entry path).
- 2026-10-14: criteria audit (full mode, fresh Opus reader): 9 findings, all fixed: routed requests are not re-judged; a request naming no work is checked after step 3; mixed-tier requests and long docs work are milestones; the check reads only named code and docs; the rulebook gate section names the chip; the trivial option says it pushes; the trivial route refuses off the default branch or over dirty files; the guest rule moved into AC1; the work-log line names its file; the sweep became a no-hit claim over README, CLAUDE.md and skills; the hand-run suite moved to a task (D-109).
- 2026-10-14: question set: on a smaller-tier finding — ask, route recommended; small non-bug runtime changes — stay milestones; trivial route — the plan skill makes the edit.
- 2026-10-14: plan gate chose a chip on a smaller-tier finding over an automatic route because a wrong call would cost a rerun and the user keeps the plan-anyway option; falsified by tier chips the user always answers with the recommended route.
- 2026-10-14: plan gate chose the tier check in step 1 over a question in step 3's set because step 2's sweeps and the criteria audit would run first on work that needs no milestone; falsified by tier chips that cannot be answered without step 2's investigation.
- 2026-10-14: plan gate kept the rulebook's tier definitions over widening `/hotfix` to small non-bug changes, at the user's choice; falsified by small refactors that the check keeps sending through a full milestone run.
- 2026-10-14: implement started on m250-plan-tier-check; untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-14: T1-T3: tier check, tier chip, and the `tier check:` line added to step 1 of `skills/milestone-plan/SKILL.md`, with a pointer bullet in step 4; no steps renumbered; entry paths traced: `/milestone` §4 passes the issue (exempt), `/hotfix` step 1 routes by a close block (exempt in-session), the ✎ press passes a row title (checked).
- 2026-10-14: T4: tracking-rules "Question gates and phase closes" names the tier chip as before the run, not a run gate; D-162 appended (annotates D-144); rulebook baseline re-seeded to 655 lines / 62,812 bytes at its three sites.
- 2026-10-14: T5: README `/milestone-plan` row and CHANGELOG Unreleased entry added; AC6 sweep read 52 hits, none says the plan always produces a milestone; the router's "One question set follows" (CLAUDE.md, template) left as is per Scope Out.
- 2026-10-14: T6: `skills/tests/test_plan_tier_check.py` added (5 tests, 27 pinned clauses), each clause shown red by deleting it, tree restored; registered EXEMPT in the mutation harness like M249's guard; `skills/tests` green (751 tests) after that entry, red once before it; verify five green; `cairn_validate` green.
- 2026-10-14: claim audit: 50 claims read, 3 corrected — CHANGELOG.md (routed-work exemption overstated), skills/milestone-plan/SKILL.md (hotfix route wording; deferred check contradicts the chip's before-step-2 timing).
- 2026-10-14: re-audit: AC3 (full) — 3 findings: a deferred chip after the question set still contradicts AC4, the closed stop list, and D-162; descoping recommended; the AC3 amendment was not taken.
- 2026-10-14: re-audit: AC2 (full) — 4 findings: AC5's no-file fallback unreachable; `/hotfix`'s merged-PR re-entry route missed; AC1 lacked the no-work scope; branch text lags (known).
- 2026-10-14: re-audit: AC5 (full) — same reader as AC2: the no-file fallback names a state step 4 never reaches.
- 2026-10-14: re-audit: AC1 (full) — 3 findings: routed requests double-classified; D-162 lacks the no-work exception; last sentence read as a runtime claim.
- 2026-10-14: re-audit: AC2 (full) — nothing.
- 2026-10-14: re-audit: AC5 (full) — nothing.
- 2026-10-14: substantive amendment: AC1 scoped to requests that name work and are not already tiered, its last sentence put under "the skill says"; AC2 lists both routers, the `/hotfix` arm covering step 1 and the step-7 merged-PR re-entry, and a request naming no work is not checked; AC5 gains the `tier check: not run` form and drops the no-file fallback. Deferral descoped: a bare `/milestone-plan` whose work is picked at the question set is planned as a milestone.
- 2026-10-14: re-audit: AC1 (full) — 1 finding: the last sentence's second clause can still attach to "the check" (a runtime claim); proposed "The skill says the check may read the code and docs the request names, and that it does not run step 2's sweeps or spawn subagents." Second AC1 line: stop for the user.
- 2026-10-14: user at the AC1 stop: took the reader's rewording; no further reader.
- 2026-10-14: skill step 1, CHANGELOG, and guard pins follow the amended AC1, AC2, AC5; D-162 gained the no-work sentence in place, since it has not reached main; clause probe 0 survivors; `skills/tests`, verify five, and `cairn_validate` green; rulebook still 655 lines / 62,812 bytes. Status → review.
- 2026-10-14: review: PR #261 opened at review start and Copilot requested (state `none` before); all 7 criteria verified and ticked; three-lens fan-out returned 26 findings.
- 2026-10-14: review return 1: two load-bearing defects in the tier check's routes — an issue `#N` handed to `/hotfix` as a bare PR reference (diff-bug #1, blame-history #1), and the trivial route pushing without comparing the default branch with origin (diff-bug #2, prior-review #2); the other fix-now items in the Review section ride the same pass.
- 2026-10-14: T7 added for review return 1 (minor amendment; Coverage maps AC3, AC4, AC6 to it).
- 2026-10-14: T7: `/hotfix` argument in §4's `issue <URL>` form; trivial route fetches, refuses with no remote, off the default branch, out of step with `<base>`, or over dirty or staged files, names other dirty paths, shows the edit, commits by path, never forces; plain chip words; README core loop and "Answer two questions"; D-162 reworded (IP1 sentence, same-session bound, guest narrowing, falsifier); header PR URL; guard pins 32 clauses, 0 survivors; verify five, `skills/tests`, `cairn_validate` green. Status → review.
- 2026-10-14: review pass 2: Copilot `reviewed earlier-head Lite`, not re-requested; AC evidence re-recorded; three-lens fan-out returned 23 findings.
- 2026-10-14: review return 2: the pass-1 hotfix-route fix drops the request text and has no issue-URL read (diff-bug #2, #3), and the trivial commit fails on a new file (diff-bug #5); the route's checks move before the chip in one rewrite rather than further patches.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->

Pass 1, 2026-10-14, branch head 0124aa36, synced with origin/main (5f4bb1a0). PR #261 opened at review start (Copilot arm); Copilot requested on `none`.

- AC1 evidence: `skills/milestone-plan/SKILL.md:41-62` holds "Tier check (before step 2)", cites "Sizing and the work tiers" (1 hit), gives the three tier tests and the mixed-parts rule, scopes to "every source of request that names work" with the two routed invocations exempt, and says the check can read the named code and docs and "does not run step 2's sweeps or spawn subagents" (:54-55); `test_tiers_are_defined_before_step_2` ok.
- AC2 evidence: SKILL.md:57-64 names both routers (`/milestone` §4's verdict; `/hotfix` over-the-bar work at step 1 or step 7's merged-PR re-entry, earlier in this session), classified `milestone` without re-judging with the router in the reason, and "A request that names no work is not checked"; `test_routed_sources_and_no_work_requests` ok.
- AC3 evidence: SKILL.md tier-chip paragraph poses one chip before step 2 on a `hotfix` or `trivial` finding, question text names tier and reason, options route (recommended) / plan anyway / stop, trivial description names push or on-disk; tracking-rules.md:380-382 states a run begins at the question set and the chip comes before it, posed only on a hotfix or trivial finding; `test_tier_chip_and_its_options` and `test_rulebook_puts_the_chip_before_the_run` ok.
- AC4 evidence: SKILL.md option bullets: hotfix route invokes `/hotfix` via the Skill tool with the request, no file written; owner trivial runs `git status`, commits only touched files, pushes, refuses off the default branch or over uncommitted changes with a close block naming why, else a close block naming the commit; guest writes on disk, no commit, close block; stop writes nothing; plan anyway goes to step 2; `test_tier_chip_and_its_options` ok.
- AC5 evidence: SKILL.md step-1 closing paragraph names the three `tier check:` forms (milestone, plan-anyway, not run) in the first milestone file, and step 4's "Tier-check line" bullet points to it; `test_tier_check_work_log_line` ok.
- AC6 evidence: README.md:545 row says the plan first checks the work needs a milestone and offers `/hotfix` or a direct edit; CHANGELOG.md:7 Unreleased entry present; `git grep -n -i "milestone-plan" -- README.md CLAUDE.md skills/ ':!skills/tests'` gives 52 hits, read at implement and re-filtered for "always"/"every request" (0): none states the plan always produces a milestone.
- AC7 evidence: verify five, fresh: scripts/tests 407 OK (21 skipped), hooks/tests 175 OK, plugin validate 0, marketplace validate 0, `claude plugin test .` 1707 tests 0 fail; all exit 0.
- Consistency gate: `cairn_validate.py` exit 0; no DESIGN.md principle changed (cairn_impact skipped); claude-plugin consistency-gate = the verify slot above; hand-run `skills/tests` exit 0. Marketplace validate prints no `version` warning; the CHANGELOG entry carries no milestone id.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: hotfix route passes the request as-is, so an issue `#N` reaches `/hotfix` as a PR reference — fix now (floor: load-bearing defect)
- diff-bug #2: trivial route never compares the default branch with origin, so it can push unapproved local commits or fail its push silently — fix now (floor: load-bearing defect)
- diff-bug #3: "commits only the files the edit touches" does not exclude files already staged — fix now
- diff-bug #4: unrelated dirty paths go unmentioned at the chip — fix now (named in the option description)
- diff-bug #5: the trivial route leaves a matched candidate row in the ROADMAP — follow-up (new row "Tier check edges (M250 review)")
- diff-bug #6: git model says the default branch takes only docs-only commits, while the trivial route pushes a code-comment commit — follow-up (absorbed into "Branch-protection compatibility"; the router's trivial tier predates M250)
- diff-bug #7: "A run begins at the plan question set" leaves steps 1-2 outside the early-stop clause — reject (false: the run's definition at tracking-rules.md:378 already starts with the question set; M250 adds no change there)
- diff-bug #8: in guest mode a PR reference judged `hotfix` routes to `/hotfix`, which cannot adopt a third party's PR there — follow-up (new row; a fix changes AC1's tier definitions)
- diff-bug #9: `/milestone` §3's `/milestone-plan` disposition is not in the already-tiered list — follow-up (new row; AC2 names two routers)
- diff-bug #10: "names the tier found" invites cairn words into chip text — fix now (plain words)
- diff-bug #11: README "Answer two questions" / "one question set" understate the tier chip — fix now (README core loop; CLAUDE.md template stays out of scope)
- diff-bug #12: no commit subject form and no no-remote behavior for the trivial route — fix now (with #2)
- diff-bug #13: the guard does not pin "every source of request that names work" — fix now
- diff-bug #14: D-162's rejection of the automatic route has no falsifier of its own — fix now
- blame-history #1: same as diff-bug #1 (M232's `issue <URL>` argument form) — fix now
- blame-history #2: D-162 calls the tier chip "the gate IP1 asks for" though the chip approves a route before the edit exists — fix now (D-162 reworded; the edit is shown verbatim when committed)
- blame-history #3: same as diff-bug #9 — follow-up (new row)
- blame-history #4: same as diff-bug #11 — fix now
- blame-history #5: the rulebook sentence restates step 1's condition — reject (planned change: AC3 requires the rulebook to state it)
- blame-history #6: D-162 does not record the guest `cairn/`-only narrowing of trivial — fix now (one D-162 sentence)
- blame-history #7: the route proceeds past unrelated dirty files where tracking-rules says to ask — fix now (with diff-bug #4)
- blame-history #8: the trivial commit draws commit_guard's non-blocking nudge — noted (informational, no defect)
- prior-review #1: the trivial edit lands on main without a verbatim preview — fix now
- prior-review #2: no sync before the push — fix now (with diff-bug #2)
- prior-review #3: the routed-work exemption depends on this session's memory; after a `/clear` routed work is re-judged — fix now (D-162 states the accepted bound: the plan-anyway option ends any bounce)
- prior-review #4: header carries no PR URL — fix now
- fixed: diff-bug #1-#4, #10-#14, blame-history #1, #2, #4, #6, #7, prior-review #1-#4, fixed cb478930 (README, D-162, SKILL.md, guard) and ce44d6e2 (header).

Pass 2, 2026-10-14, head ce44d6e2 (code as of cb478930; ce44d6e2 touches only `cairn/`), synced with origin/main. Copilot state `reviewed earlier-head Lite`: not requested again.

- AC1-AC5 evidence (pass 2): `test_plan_tier_check` 5 tests OK at head, 32 pinned clauses each red when deleted (probe, 0 survivors); SKILL.md:66-94 keeps every clause AC1-AC5 name, now with the `issue <URL>` argument form (:73-77), the fetch and refusals (:81-89), and plain-words chip text (:68).
- AC6 evidence (pass 2): README.md:545 row unchanged; README.md:469-472 and :636-638 name the tier question before the question set; CHANGELOG.md:7 entry unchanged; the AC6 sweep's no-hit claim holds (no new "always" hit).
- AC7 evidence (pass 2): at cb478930: scripts/tests OK, hooks/tests OK, plugin validate 0, marketplace validate 0, `claude plugin test .` 0 fail; all exit 0. `cairn_validate.py` exit 0 at ce44d6e2; hand-run `skills/tests` exit 0.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: other dirty paths must be named at the chip, but `git status` runs only after selection — fix now (checks move before the chip)
- diff-bug #2: the hotfix argument keeps only a one-line summary and drops the request text — fix now (floor: load-bearing defect)
- diff-bug #3: an issue source has no step that reads the issue or its URL, so `issue <URL>` cannot be built — fix now (floor: load-bearing defect)
- diff-bug #4: the trivial option is recommended even when its checks will refuse — fix now (description says it cannot run now and why)
- diff-bug #5: `git commit -- <paths>` fails for a new file — fix now (floor: load-bearing defect; stage the paths first)
- diff-bug #6: a rejected push leaves an unpushed commit with no recovery step — fix now (close block gives the undo command; push command named)
- diff-bug #7: the fetch runs before the no-remote refusal — fix now (checks reordered)
- diff-bug #8: README "Answer two questions" heading and "Between them" now ambiguous — fix now
- diff-bug #9: README core-loop colon now introduces the diagram after the tier sentences — fix now
- diff-bug #10: D-162's guest sentence reads as a tier-definition change — fix now (worded as the plan's check)
- diff-bug #11: CHANGELOG refusal list omits the new refusals — fix now
- diff-bug #12: a candidate-row source's title should pass to `/hotfix` verbatim for its exact-title match — fix now
- blame-history #1: the chip approves the route, not the content — fix now (option description names the file and the change, so the approval covers the content)
- blame-history #2: D-162 should name the git model's docs-only sentence the trivial route departs from — fix now (one D-162 clause; the rulebook edit stays in the follow-up row)
- blame-history #3: same as diff-bug #8 — fix now
- blame-history #4: same as diff-bug #3 — fix now
- blame-history #5: same as diff-bug #5 — fix now
- blame-history #6: CLAUDE.md and the routing template say "One question set follows" with no follow-up row — follow-up (named in the new row "Tier check edges (M250 review)")
- prior-review #1: same as diff-bug #4 — fix now
- prior-review #2: same as diff-bug #8 — fix now
- prior-review #3: same as blame-history #6 — follow-up
- prior-review #4: the guard pins no README text — fix now (pin README.md's `/milestone-plan` row)
