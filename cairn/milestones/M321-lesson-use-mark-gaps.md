<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M321: Fix the gaps in lesson use marks

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, IP4
- **Resolves:** —
- **Surface tier:** user-facing — it changes the review-hygiene and `/cairn-triage lessons` steps that adopting repos run
- **Branch/PR:** m321-lesson-use-mark-gaps, https://github.com/jmgirard/cairn/pull/334

## Goal

Review hygiene and `/cairn-triage lessons` keep every `used` mark, pinned string, and skipped lesson that M320's rules can now lose.

## Scope

**In:** `/milestone-review` step 9: read the `lessons used:` lines before
the live file is deleted; find pin files and keep their strings whole when
a mark forces a shortening; store a skipped lesson as a waiting line; show
every changed lesson line in the preview; the archived-file arm names the
skipped use marks. `/cairn-triage lessons`: where a `used` mark goes on
`split`, `merge`, `compress`, and `correct`; the `admit` disposition for a
waiting line; guest mode quotes each dropped or merged-away lesson; the
opening paragraph's stale "only". The over-limit remedy wording in the
lessons template, this repo's `cairn/LESSONS.md` header, and tracking-rules
"Weight caps" and "Retiring a lesson". One D-entry. The CHANGELOG's
Unreleased lessons entry. DESIGN.md's Known issues sentence on guest lesson
drops.

**Out:** code and test comments that cite evicted lessons → candidate row
"Cut code cites to evicted lessons". A live milestone's lesson citation that
a later mark changes → parked row "Match lesson citations after use marks".
Prose guards for M320 text this milestone leaves unchanged (README's lessons
row) → dropped at the user's choice at the question set.

## Acceptance criteria

- [x] AC1: In `skills/milestone-review/SKILL.md` step 9, the pass reads the
      live milestone file's `lessons used:` work-log lines before the
      sentence that deletes that file, and the use-mark sentence marks the
      lessons those lines name; the archived-file arm's list of work it
      skips names lesson use marks.
- [x] AC2: Step 9 says how the pass finds pin files (each file that
      `git grep -l "LESSONS.md"` lists whose path contains `test`), and says
      that shortening a lesson that a `used` mark takes past 450 bytes keeps
      whole each string those files assert present and each text a live
      milestone quotes, and that a lesson that cannot then fit in 450 bytes
      takes no `used` mark and is named in the close block beside a fenced
      `/cairn-triage lessons`.
- [x] AC3: In its too-few-removable case, step 9 writes each skipped lesson
      at the end of `cairn/LESSONS.md` as a waiting line,
      `- waiting YYYY-MM-DD (M<NNN>): <lesson>`, which counts toward the
      file's line cap and not toward its 25 lessons; where writing the line
      would bring `cairn/LESSONS.md` to 50 lines or more, that lesson is not
      written and the close block quotes it in full. Its durable-record
      preview shows verbatim each LESSONS line the pass captures, marks,
      shortens, or writes as waiting, and names each lesson it removes.
- [x] AC4: In `skills/cairn-triage/SKILL.md`'s lessons pass: each line of a
      `split` keeps the split lesson's `used` mark, and the `split` row's
      provenance sentence names that mark as kept on every line; a `merge`
      survivor carries the `used` mark with the higher milestone number of
      the two lessons, or the one mark either has; a `compress` or `correct`
      keeps the lesson's `used` mark; in guest mode the close block quotes in
      full each lesson the pass drops or merges away; and the pass's opening
      paragraph states that review hygiene marks use and removes the
      lowest-ranked lessons at the limit, and no longer says it checks only
      the lessons the milestone covers.
- [x] AC5: In the same pass, step 1 lists each waiting line as an item of
      its own, and step 2 proposes for it either `admit`, which removes its
      `waiting ` word so it becomes a lesson that the rank rule then counts,
      or `drop` with one of the pass's exits other than `rank`; a waiting
      line that a pin file holds or a live milestone quotes is proposed
      `admit`, never `drop`; until admitted, a waiting line is not counted
      among the lessons or ranked; and step 2's disposition count and table
      include `admit`, its row stating it applies only to a waiting line.
- [x] AC6: In `skills/shared/templates/lessons.md`, `cairn/LESSONS.md`'s
      header, tracking-rules "Weight caps", and tracking-rules "Retiring a
      lesson", the over-limit remedy sends a lesson over 450 bytes to
      shortening or splitting and a file over 25 lessons to retirement and
      then rank eviction, and none of the four names splitting or shortening
      as a remedy for the count; each says a waiting line is not a lesson,
      takes no `used` mark, and waits for `/cairn-triage lessons`; and the
      "Retiring a lesson" bullet names the waiting line in review's
      full-file case and `admit` among the whole-file pass's dispositions.
- [x] AC7: `cairn/DECISIONS.md` gains one entry that names D-177's "one of
      five exits" clause as superseded by D-218's `rank` exit and D-218's
      "captures nothing when none can go" clause as superseded by the waiting
      line, and records the waiting line, triage's `admit` disposition, and
      guest triage's quoting of each dropped or merged-away lesson.
- [x] AC8: The CHANGELOG's Unreleased lessons entry states that review
      stores a skipped lesson as a waiting line that `/cairn-triage lessons`
      admits or drops, and that guest `/cairn-triage lessons` quotes each
      lesson it drops or merges away; the repo's `verify` (both gating
      `python3 -m unittest` suites, both `claude plugin validate` runs,
      `claude plugin test`) and the hand-run `skills/tests` pass on the
      review head.

## Coverage

- AC1 → T1, T6
- AC2 → T1, T6, T8
- AC3 → T1, T6
- AC4 → T2, T6, T7
- AC5 → T2, T6, T8
- AC6 → T3, T6, T7, T8
- AC7 → T4
- AC8 → T5, T6

## Tasks

- [x] T1: Review hygiene (`skills/milestone-review/SKILL.md` step 9, about
      lines 867-1000, and the archived-file arm near line 41): move the
      `lessons used:` read before the deletion, add the pin-file procedure
      and the pin-safe shortening rule with its no-mark outcome, the waiting
      line with its 50-line stop, the preview wording, and "mark" in the
      arm's skipped list.
- [x] T2: Triage lessons pass (`skills/cairn-triage/SKILL.md` about lines
      107-260): `used` mark placement on split, merge, compress, and
      correct; waiting-line enumeration and the `admit` row (eight
      dispositions); guest quoting in the close block; the opening
      paragraph. Narrow DESIGN.md's Known issues sentence on guest lesson
      drops (about line 1022) to say the close block now quotes them.
- [x] T3: Remedy and waiting-line wording at the template, this repo's
      LESSONS header, and the two rulebook sites; re-seed the rulebook-mass
      baseline in its three places (the M149 lesson).
- [x] T4: Write the D-entry (AC7), one batched entry.
- [x] T5: Edit M320's Unreleased CHANGELOG entry for the waiting line and
      guest quoting; sweep README for the old remedy and "captures nothing"
      wording (the M112 lesson).
- [x] T6: Prose guards in `skills/tests` for each sentence T1-T3 add or
      change, with mutation-registry entries where neighbours have them,
      each shown red when its sentence is blanked; re-pin guards whose text
      changed; run `verify` and the hand-run `skills/tests`.
- [x] T7: Review return 1: name the `used` mark in the `split` row's
      provenance sentence, and say in the "Retiring a lesson" bullet that
      retirement runs before rank eviction; re-pin guards and the
      rulebook-mass baseline.
- [x] T8: Review return 2: shrink the LESSONS.md header and the template
      back under main's line count, guarded; fix the pass-2 fix-now items
      (Review section); file the follow-up row.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: milestone — the request names candidate row "Fix the gaps in lesson use marks", whose gaps change review and triage skill steps across several files.
- 2026-10-25: idea vet: one concern — the row's item to guard M320's unchanged doc claims adds checks on text this milestone does not change; the user chose to guard only changed text, so that item is dropped. The skipped-lesson store was a choice the row left open (question set line below).
- 2026-10-25: lessons used: 2026-07-16 (M56+M65, …) on running both suites and `skills/tests` after skill edits; 2026-07-24 (M112, …) on sweeping README, templates, and CHANGELOG for old wording; 2026-08-17 (M149, …) on re-seeding the rulebook-mass baseline in three places; 2026-08-17 (M148, …) on prose-guard start markers; 2026-08-22 (M152, …) on a repair that changes a decision's text owing a D-entry; 2026-08-30 (M165, …) on pinning a rule's trigger subject and checking pin tests.
- 2026-10-25: collision: candidate row "Fix the gaps in lesson use marks" absorbed in full (started token). Rows "Cut code cites to evicted lessons" and "Match lesson citations after use marks" are distinct and stay. D-218's capture-nothing clause and D-177's five-exit clause are superseded by AC7's entry. D-051 rejection (2), a separate graduated-lessons file, is not hit: the waiting line sits in `cairn/LESSONS.md` itself.
- 2026-10-25: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-25: question set: where to keep a lesson review skips at a full file — the user asked whether to store it for the next triage or run triage at once; after a follow-up chip, a waiting line in `cairn/LESSONS.md` that `/cairn-triage lessons` admits or drops.
- 2026-10-25: question set: guard M320's unchanged README lessons row — no, guard only text this milestone changes.
- 2026-10-25: criteria audit (full mode, fresh Opus reader): 8 findings on the first draft (pin-file procedure, a fixed outcome for an unfittable lesson, summary line cap, plural skipped lessons, verbatim preview, split provenance sentence, merge mark rule, stale "only", CHANGELOG scope) and 5 on the re-audit after the answers (D-218 clause to supersede, pinned waiting lines, the "Retiring a lesson" site and the no-mark rule, the 50-line threshold, the disposition count); all taken.
- 2026-10-25: plan gate chose a waiting line over an archive-summary record because triage reads `cairn/LESSONS.md` whole and can admit it; falsified by waiting lines that stay unadmitted across two or more triage runs.
- 2026-10-25: plan chose no `used` mark for a lesson that cannot fit 450 bytes with its pinned or quoted text whole, over keeping the mark past the limit, because it keeps the per-lesson limit intact; falsified by such a lesson being rank-evicted for the missing mark.
- 2026-10-25: sizing: 8 criteria, one past the ~7 tripwire; kept as one milestone because all eight edit the same two passes, and a split would ship the waiting line without its `admit` reader.
- 2026-10-25: changelog: M320's Unreleased lessons entry is edited, not joined by a new entry, since both change the same unreleased behavior.
- 2026-10-25: branch m321-lesson-use-mark-gaps cut from main at 7eaeb0a2; untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-25: T1 done — review step 9 reads the `lessons used:` lines and trap-met lessons before the deletion; pin files found by `git grep -l "LESSONS.md"` (path contains `test`); the mark's shortening keeps pinned and quoted text whole, else no mark and the close block names it; the too-few case writes `- waiting` lines (none at 49 or more lines, quoted instead); the preview shows captured, marked, shortened, and waiting lines and names removed ones; the archived-file arm says "capture, mark, or retire no lesson". Agent chose: the 50-line stop reads as "already holds 49 lines or more". Verify 5/5 green; `skills/tests` red on four guards of the changed text, re-pinned at T6.
- 2026-10-25: T2 done — triage lessons pass: opening says review retires covered lessons and also marks use and evicts by rank (D-218); step 1 lists `- waiting` lines as items of their own, not counted or ranked until admitted; eight dispositions with the `admit` row (waiting line only); a waiting line's `drop` takes any exit but `rank`, and a pinned or quoted one is `admit`; split lines keep the `used` mark, a merge survivor keeps the higher mark, compress and correct keep it; apply and record name admits; guest close block quotes each dropped or merged-away lesson or waiting line. DESIGN.md Known issues narrowed. Agent chose: an unpinned waiting line takes the planner test, and an admitted line counts in the rank rule. Verify 5/5 green.
- 2026-10-25: T3 done — template, LESSONS.md header, and tracking-rules Weight caps now send a lesson over 450 bytes to shortening or splitting and a count over 25 to retirement then rank eviction; each says a `- waiting` line is not a lesson, takes no `used` mark, and waits for `/cairn-triage lessons`; "Retiring a lesson" names the waiting line in the none-can-go case and `admit`. Rulebook-mass baseline re-seeded to 847 lines / 83,737 bytes in its three places. Verify 5/5 green; `skills/tests` red on guards of changed text (T6).
- 2026-10-25: T4 done — D-221 written: the waiting line (supersedes D-218's "captures nothing when none can go"), triage `admit`, six exits (supersedes D-177's "one of five exits"), guest triage quoting (extends D-219 (5)); the rulebook and review skill cite D-221; rulebook baseline re-seeded to 847 lines / 83,744 bytes. Validate green.
- 2026-10-25: correction to the T4 line: the T4 commit f22a5944 went in past a red `claude plugin test` (1 of 2466 failed), because the verify call piped through `tail` and lost the exit code (the M56 lesson's trap, met). A rerun failed 2 other mod tests; the branch changes no `hooks/` code, so a run on main is checking for flakiness before T5's commit.
- 2026-10-25: flake check: the run on a main worktree is no comparison (two test files did not load there, untracked dependencies absent); `git diff main --stat -- hooks scripts` is empty, and a solo rerun on the branch passed 2466/2466 in 120 s against about 400 s for the two failing runs, so the mod-test failures are load-timing flakes, not this branch.
- 2026-10-25: T5 done — CHANGELOG's Unreleased lessons entry now says review writes a skipped lesson as a `- waiting` line that `/cairn-triage lessons` admits or drops, and that guest triage quotes each lesson it drops or merges away; README sweep found no "captures nothing" or "shorten or split" wording (README's lessons row stays as it is). Verify 5/5 green, exit codes read from a log, not a pipe.
- 2026-10-25: T6 done — guards re-pinned in `test_lessons_loop.py`, `test_triage_lessons.py`, and `test_resume_routing.py` for the changed text; new guards for the read-before-deletion order (an index comparison), pin-safe shortening and the pin-file procedure, the waiting line and its 49-line stop, the preview, the remedy and waiting line at template, LESSONS header, and both rulebook sites, the eight dispositions with `admit`, waiting-line handling, the opening paragraph, split and merge marks, the rank count, and guest quoting; 28 new or updated mutation entries, each red when blanked. `skills/tests` 974 OK; verify 5/5 green; validate green.
- 2026-10-25: correction to the T6 line: it changed 31 mutation entries, 27 new and 4 updated, not 28.
- 2026-10-25: claim audit: 49 claims read, 2 corrected — CHANGELOG.md, skills/shared/tracking-rules.md, skills/shared/templates/lessons.md, cairn/LESSONS.md header (the 49-line exception was missing, so "writes it" read as unconditional), skills/cairn-triage/SKILL.md (step 1's empty-file sentence ignored waiting lines). Same reader re-read all corrected claims: true. Guards added for the new sentences (3 new mutation entries, 1 updated); rulebook-mass baseline re-seeded to 847 lines / 83,799 bytes. `skills/tests` 974 OK; verify 5/5 green.
- 2026-10-25: PR #334 opened at review start (Copilot round on); Copilot request may not be recorded (state still `none`).
- 2026-10-25: review return 1: AC4 fails as written — the `split` row's provenance sentence ("Each new line keeps the original date and only the provenance ids its text came from") does not name the `used` mark, which sits in the next sentence; AC6 fails as written — the tracking-rules "Retiring a lesson" bullet does not say retirement runs before rank eviction for a count over 25.
- 2026-10-25: T7 done (minor amendment for return 1: task added, Coverage AC4 and AC6 cite T7) — the `split` row now reads "Each new line keeps the original date, only the provenance ids its text came from, and the split lesson's `used` mark"; "Retiring a lesson" adds "Over 25 lessons, retirement runs first and rank eviction second."; guards re-pinned and one added (red when blanked); rulebook-mass baseline re-seeded to 848 lines / 83,866 bytes. `skills/tests` 974 OK; verify 5/5 green. Handing back to review.

- 2026-10-25: review return 2: load-bearing defect (diff-bug #1, blame-history #1) — the LESSONS.md header grew from 20 to 25 non-lesson lines and the template from 18 to 22, so 25 lessons reach the 50-line cap that `cairn_validate` fails; this pass's fix-now items ride with the fix (Review section, pass 2).
- 2026-10-25: T8 done (minor amendment for return 2: task added, Coverage AC2, AC5, AC6 cite T8) — LESSONS.md header back to 20 non-lesson lines (41 lines with 21 lessons, 45 at 25) and the template to 19 lines, the waiting sentence now "A `- waiting` line is not a lesson: it takes no `used` mark and waits for `/cairn-triage lessons`." with no "at the end" and no 49-line clause; a new guard fails when the header leaves no room for 25 lessons and a waiting line (red on the 25-line header at c3c096a6); rulebook says "is written as a `- waiting` line"; CHANGELOG says "Instead" and "49 lines or more"; review: "It keeps the lesson's date and every mark in its provenance." and "None listed means no pins and no failure."; triage: an admitted line is never a `rank` drop and counts as kept, and a waiting line moved to `keep` stays waiting; plan harvest names no waiting line; DESIGN.md Known issues names review's pin search and moves its provenance to the entry's end; test comments lose the milestone tags, the docstring says eight; `assertNotIn` for the retired remedy wording; guards for every new sentence, each red when blanked. Follow-up row "Close the leftover lesson hygiene gaps" added; the M321 candidate row shortened for the byte budget; the parked band-flake row notes the 2026-10-25 recurrence. Rulebook baseline re-seeded to 848 lines / 83,854 bytes. `skills/tests` 976 OK; verify 5/5 green. Handing back to review.
- 2026-10-25: correction to the T8 line: only the LESSONS.md header had a room guard then; the template's guard came with the pass-3 fixes.
- 2026-10-25: collision (late, found at review pass 3): D-108's door covers new conduct rules about records. M321's trigger is a defect in shipped skill behavior (review hygiene and triage losing use marks, pinned text, and skipped lessons), so it passes on D-108's retained trigger, as D-177 and D-218 did. The plan's collision check did not surface D-108.
- 2026-10-25: review pass-3 fix-now work — rulebook partial-case and limit-order wording, triage's waiting-line proposal sentence and Amend reason, review's whole-provenance shortening, header-room guard excludes waiting lines and covers the template, follow-up row extended; rulebook baseline 848 lines / 83,903 bytes. `skills/tests` 977 OK; verify 5/5 green.

## Decisions

## Review

Pass 1 (2026-10-25), branch head b5011c05, PR #334. Copilot: state query `none`; one request (exit 0), state still `none` — Copilot request on PR #334 may not be recorded by GitHub (used-up Copilot credits are one cause); no second request.

- AC1 evidence: `skills/milestone-review/SKILL.md:880` reads the `lessons used:` lines ("Before the live file is deleted below, read its `lessons used:` work-log lines") before `:888` "**deleting the live"; `:913` marks "each lesson that the `lessons used:` lines read before the deletion name"; the archived-file arm at `:58` says "capture, mark, or retire no lesson". `test_review_reads_the_used_lines_before_the_deletion` asserts the order by index. Pass.
- AC2 evidence: step 9 finds pin files at `:972-974` ("each file that `git grep -l "LESSONS.md"` lists whose path contains `test`", read for the strings asserted present); `:919-922` says the mark's shortening "keeps whole each string a pin file asserts present and each text a live milestone quotes (both defined below)", and a lesson that "cannot then fit in 450 bytes takes no `used` mark, and the close block names it beside a fenced `/cairn-triage lessons`". Pass.
- AC3 evidence: step 9 `:977-987` writes each skipped lesson at the end of `cairn/LESSONS.md` as `- waiting YYYY-MM-DD (M<NNN>): <lesson>`, "counts toward the file's line cap and not toward its 25 lessons", and when the file "already holds 49 lines or more" (one more line brings it to 50 or more, `LINE_CAPS` 50 at `scripts/cairn_scripts.py:44`) writes no line and quotes the lesson in full in the close block; `:991-996` previews verbatim each LESSONS line "the pass captures, marks, shortens, or writes as waiting" and names each removed lesson by date and provenance. Pass.
- AC4 evidence: `skills/cairn-triage/SKILL.md:180-183` — compress and correct keep "any `corrected`, `trimmed`, or `used` mark", a merge survivor "carries the `used` mark with the higher milestone number of the two lessons, or the one mark either has", each split line keeps "the split lesson's `used` mark"; `:285-287` guest close block quotes each dropped or merged-away lesson or waiting line in full; `:118-120` opening says review "retires only the lessons that milestone's work covers (D-051). It also marks the lessons the milestone used, and at the 25-lesson limit it removes the lowest-ranked ones (D-218)"; `grep -c "still checks only"` 0. But the `split` row (`:172`) names the mark in a sentence after its provenance sentence ("Each new line keeps the original date and only the provenance ids its text came from. Every new line also keeps the split lesson's `used` mark."), so the provenance sentence itself does not name it, and its "only" still reads as excluding the mark. Fail as written.
- AC5 evidence: `skills/cairn-triage/SKILL.md:154-159` lists each `- waiting` line as an item of its own and says that until admitted "the pass does not count it among the lessons or rank it"; `:164-166` "An item takes one of eight dispositions … A waiting line takes only `admit` or `drop`"; `:176` the `admit` row ("A waiting line only. Its `waiting ` word is removed, so the line becomes a lesson … and the rank rule then counts it"); `:205-207` a waiting line's `drop` names an exit "other than `rank`", and one a pin file holds or a live milestone quotes "is proposed `admit`, never `drop`". Pass.
- AC6 evidence: the template (`skills/shared/templates/lessons.md:13-15`), the `cairn/LESSONS.md` header (`:13-15`), and Weight caps (`tracking-rules.md:88-89`) each send a lesson over 450 bytes to shortening or splitting and a count over 25 to retirement then rank eviction; none ties splitting or shortening to the count. All four sites say a `- waiting` line is not a lesson, takes no `used` mark, and waits for `/cairn-triage lessons` (template `:18-20`, header `:19-21`, Weight caps `:71-72`, Retiring `:145-146`), and "Retiring a lesson" names the waiting line in the none-can-go case and `admit` (`:150`). But the "Retiring a lesson" bullet states the 450-byte remedy ("shortens or splits each lesson over 450 bytes") and rank eviction at the limit, and nowhere says retirement runs first, so it does not send a count overrun to "retirement and then rank eviction". Fail as written.
- AC7 evidence: `cairn/DECISIONS.md` gains one entry, D-221 (`grep -c "^### D-221"` 1; the diff against main removes no line). It supersedes D-177's "one of five exits" (`:8001`) and D-218's "captures nothing when none can go" (`:7994`), and records the waiting line (`:7990`), the `admit` disposition (`:7995-7998`), and guest triage's quoting of each dropped or merged-away lesson (`:8002`). Pass.
- AC8 partial: `CHANGELOG.md:16-23` says review writes each new lesson it cannot fit as a `- waiting` line that the next `/cairn-triage lessons` run proposes to admit or drop, and that guest `/cairn-triage lessons` quotes each lesson it drops or merges away. Verify on the review head waits for the return below. Not ticked.

Pass 2 (2026-10-25), branch head 603cd3c5, after return 1. Copilot: state query `none`; one request (exit 0), state still `none` — Copilot request on PR #334 may not be recorded by GitHub (used-up Copilot credits are one cause); no second request.

- AC4 recheck: the `split` row (`skills/cairn-triage/SKILL.md:172`) now reads "Each new line keeps the original date, only the provenance ids its text came from, and the split lesson's `used` mark", so its provenance sentence names the mark kept on every line; the merge, compress, correct, guest-quoting, and opening evidence of pass 1 is unchanged (the diff since b5011c05 touches only that row in the skill). Pass.
- AC6 recheck: `tracking-rules.md:143-144` "Retiring a lesson" now says "Over 25 lessons, retirement runs first and rank eviction second.", beside its 450-byte "shortens or splits each lesson over 450 bytes"; the other three sites and the waiting-line statements of pass 1 are unchanged. Pass.
- AC8 evidence: CHANGELOG as in pass 1; on 603cd3c5 `scripts/tests`, `hooks/tests`, both `claude plugin validate` runs, and `claude plugin test` exit 0, and hand-run `skills/tests` OK (974). Pass.
- AC1, AC2, AC3, AC5, AC7 recheck on 603cd3c5: the diff since b5011c05 leaves review step 9, the waiting-line triage text, and D-221 untouched. Pass.
- Consistency gate: `cairn_validate` exit 0 (one advisory, the 8-criteria sizing tripwire the plan logged); coverage complete passes; no DESIGN principle changed, so `cairn_impact` is skipped; profile checks: verify green on 603cd3c5, the marketplace validate prints no `version` warning, CHANGELOG's Unreleased lessons entry covers the user-visible changes with no milestone numbers. Pass.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the LESSONS.md header grew from 20 to 25 non-lesson lines, so 25 lessons make 50 lines and `cairn_validate` fails at 50; the template grew from 18 to 22 lines — load-bearing; return 2 (fix now), fixed 30d663ad
- diff-bug #2: a pinned or quoted waiting line forced to `admit` can leave 26 lessons when every other lesson is protected, sending step 4 back to the chip — reject, edge (a full file of 25 protected lessons plus a quoted waiting line; the effect is a return to the chip, where Amend settles it)
- diff-bug #3: an admitted waiting line over 450 bytes has no remedy — reject, false (review captures within the 450-byte limit, and `admit` removes the `waiting ` word)
- diff-bug #4: later captures land after a waiting line, so "at the end" stops being true — fix now, fixed 30d663ad (drop "at the end" from template, header, and rulebook)
- diff-bug #5: "already holds 49 lines" in template, header, and CHANGELOG vs "49 lines or more" in step 9 and the rulebook — fix now, fixed 30d663ad
- diff-bug #6: guest mode loses the pre-edit text of a triage `compress`, `split`, or `correct` and of review's mark shortening — follow-up, row "Close the leftover lesson hygiene gaps"
- diff-bug #7: Amend to `keep` is undefined for a waiting line — fix now, fixed 30d663ad (it stays waiting)
- diff-bug #8: the rank rule can propose a `rank` drop for an admitted line — fix now, fixed 30d663ad (an admitted line is never a `rank` drop)
- diff-bug #9: the plan harvest can name a waiting line in `lessons used:`; the `/milestone` audit does not surface waiting lines — fix now, fixed 30d663ad for the plan (one sentence); the audit half is follow-up, row "Close the leftover lesson hygiene gaps"
- diff-bug #10: unpark reads the deleted file with `git show HEAD:`, which fails in guest mode (pre-existing) — follow-up, row "Close the leftover lesson hygiene gaps"
- diff-bug #11: review's pin search does not say that none listed means no pins; untracked test files are missed — fix now, fixed 30d663ad for the first; reject the second, edge (an untracked test that pins live LESSONS.md text; the effect is that test failing)
- diff-bug #12: "The close block names each waiting line it wrote." and the waiting line's planner-test sentence have no guard — fix now, fixed 30d663ad
- diff-bug #13: AC6's negative half has no `assertNotIn` for the old remedy wording — fix now, fixed 30d663ad
- diff-bug #14: `test_triage_lessons.py` docstring still says seven dispositions — fix now, fixed 30d663ad
- diff-bug #15: milestone-tagged rationale comments in `test_lessons_loop.py` and `test_triage_lessons.py` — fix now, fixed 30d663ad (tags removed)
- diff-bug #16: triage's opening leaves out the pin exclusion and the waiting line — reject, false (the sentence is a summary that cites D-218; nothing in it is wrong)
- diff-bug #17: DESIGN.md's "(narrowed by M321)" sits mid-entry, not in the entry's closing provenance — fix now, fixed 30d663ad
- diff-bug #18: step 9 does not say which marks survive the mark's shortening — fix now, fixed 30d663ad
- blame-history #1: same as diff-bug #1 — return 2 (fix now), fixed 30d663ad
- blame-history #2: at 49 or more lines the skipped lesson is quoted only in chat — reject, planned change (AC3 names this outcome; with the header fixed, a 25-lesson file has room for waiting lines)
- blame-history #3: same as diff-bug #9 (plan half) — fix now, fixed 30d663ad
- blame-history #4: "takes no `used` mark" and "becomes a lesson of its own" give one case two outcomes — reject, false (the first is a mark that cannot fit, the second is extension text; they are different cases)
- blame-history #5: the split copies the `used` mark to every line, against M320's "only the provenance ids" — reject, planned change (AC4)
- blame-history #6: same as diff-bug #3 — reject, false
- blame-history #7: a hygiene pass stopped after the deletion loses the use marks, since the archived-file arm marks nothing — follow-up, row "Close the leftover lesson hygiene gaps"
- blame-history #8: same as diff-bug #17 — fix now, fixed 30d663ad
- blame-history #9: the suite pins the 49-line fallback and the header wording — reject, planned change
- prior-review #1: same as diff-bug #15 for the test comments — fix now, fixed 30d663ad; the mutation-registry comment and docstring tags — reject, style (the files' own convention, as at M320 diff-bug #13)
- prior-review #2: review's pin discovery relies on the `git grep -l` that DESIGN.md's Known issues calls incomplete — fix now, fixed 30d663ad (the Known issues sentence names review's use)
- prior-review #3: same as diff-bug #17 — fix now, fixed 30d663ad
- ripple #1: same as diff-bug #9 (plan half) — fix now, fixed 30d663ad
- ripple #2: same as prior-review #2 — fix now, fixed 30d663ad
- ripple #3: the "Fix the gaps in lesson use marks" row still lists the closed gaps — reject, planned change (post-merge hygiene removes the row)
- ripple #4: README's `/cairn-triage lessons` row omits `admit` and guest quoting — reject, false (nothing it says is wrong; the user chose no README guard work)
- ripple #5: CHANGELOG's "a file over 25 lessons is cut back at the next review that captures a lesson" — reject, false (still true for an adopting repo over 25)
- ripple (inside diff): CHANGELOG's waiting-line sentence reads as covering every captured lesson — fix now, fixed 30d663ad; DESIGN.md's quoting sentence reads as all modes — reject, false (it follows "A guest lesson drop")

Pass 3 (2026-10-25), branch head 30d663ad, after return 2. Copilot state query to run before the merge chip (PR-conversation read).

- AC1–AC8 recheck on 30d663ad: the diff since c0c53ff1 adds to review step 9 ("It keeps the lesson's date and every mark in its provenance.", "None listed means no pins and no failure."), triage (an admitted line is never a `rank` drop; a waiting line moved to `keep` stays waiting), the plan harvest, and rewrites the template and LESSONS header waiting sentence to "A `- waiting` line is not a lesson: it takes no `used` mark and waits for `/cairn-triage lessons`."; every quoted pass-1 and pass-2 evidence string still reads as recorded, the four AC6 sites still state both remedies and the waiting line (none names splitting or shortening for the count, now asserted by `assertNotIn`), and LESSONS.md is 41 lines (45 at 25 lessons). Verify 5/5 green, `skills/tests` 976 OK. Pass.
- Consistency gate on 30d663ad: `cairn_validate` exit 0 (the sizing advisory only); marketplace validate prints no `version` warning; CHANGELOG entry present. Pass.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the rulebook's "When none can go" disagrees with step 9's too-few rule in the partial case — fix now, fixed 2bb47883 (rulebook says "When too few can go to leave 25, none goes"); D-221's Rejected clause is false in that case — follow-up, row "Close the leftover lesson hygiene gaps"
- diff-bug #2: the header-room guard counts `- waiting` lines as header and goes red on a legal file — fix now, fixed 2bb47883 (waiting lines excluded)
- diff-bug #3: "A waiting line takes only `admit` or `drop`" contradicts the Amend `keep`, whose reason is undefined — fix now, fixed 2bb47883 ("Step 2 proposes only `admit` or `drop` for a waiting line"; the Amend `keep` takes the same reason)
- diff-bug #4: the rank rule's stop does not list admitted lines — reject, false ("the rule counts it as kept" places it under the stop's kept lessons)
- diff-bug #5: "every mark in its provenance" leaves plain provenance ids unprotected — fix now, fixed 2bb47883 ("its whole parenthesized provenance")
- diff-bug #6: the hand byte check measures waiting lines too — reject, false (the check is of each lesson's bytes; the command measures every line, header lines included)
- diff-bug #7: the template's length is unguarded though T8's line says guarded — fix now, fixed 2bb47883 (template room guard added; the T8 line is corrected in the work log)
- diff-bug #8: ROADMAP near its byte budget — noted (23,910 bytes; hygiene removes the started row)
- diff-bug #9: milestone tags in test docstrings — reject, style (repeat of prior-review #1)
- diff-bug #10: DESIGN.md's close-block sentence reads as all modes — reject, false (repeat)
- blame-history #1: tracking-rules "At the limit the lowest-ranked lesson leaves first" gives the old order — fix now, fixed 2bb47883 ("At the limit, after retirement, …")
- blame-history #2: "Over 25 lessons" reads as no retirement at 25 — reject, false (over 25 is the over-limit case; at 25 the one-in-one-out capture rule applies)
- blame-history #3, #4, #8, #9, #11: repeats of pass-2 blame-history #5, #2, prior-review #2, diff-bug #2, blame-history #7 — dispositions as recorded there
- blame-history #5: an unfittable lesson loses its `used` mark — reject, planned change (AC2)
- blame-history #6: "at the end" stays in step 9 and the CHANGELOG — reject, false (the line is written at the file's end; the pass-2 fix removed the phrase where it described the line's lasting place)
- blame-history #7: an unadmitted waiting line can read 458 bytes and the length rule cannot apply — reject, false (the length rule covers lessons, and a waiting line is not one)
- blame-history #10: the plan harvest's no-waiting-line choice is not in D-221 — reject, planned change (a skill detail; D-221 records the waiting line's rules)
- blame-history #12: triage's opening dropped the D-169 and D-177 cites — reject, style
- blame-history #13: D-221 has no Door line for D-108 — fix now as a work-log record (the plan's collision check missed D-108; the trigger passes it), fixed 2bb47883
- blame-history #14: the header compression dropped the weight-caps pointer and the "Current knowledge" label — reject, false (no rule is lost; each rule stays in the header)
- blame-history #15: a waiting line kept at Amend changes nothing — reject, false (that is the user's choice to leave it waiting)
- prior-review #1, #2, #8: repeats of the parked row "Match lesson citations after use marks", pass-2 blame-history #7, pass-2 blame-history #5 — dispositions as recorded
- prior-review #3, #4: milestone tags in docstrings and the registry comment — reject, style (repeat)
- prior-review #5, #6: "at the end" and DESIGN/CHANGELOG guards — reject, false and planned change (repeats)
- prior-review #7: `test_plan_names_no_waiting_line` asserts one sentence — reject, style (the sentence is the rule the name states)
- prior-review #9: context only (the user's PR replies say skill rules owe no guard) — noted
- ripple #1: same as blame-history #1 — fix now, fixed 2bb47883
- ripple #2: "replaces pruning at the limit" — reject, false (pruning means D-015's prune, which rank eviction replaces)
- ripple #3, #4: repeats of pass-2 ripple #4 and diff-bug #9 — dispositions as recorded
- conversation and copilot: read at the merge chip below
