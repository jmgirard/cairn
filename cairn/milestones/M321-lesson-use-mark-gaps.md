<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M321: Fix the gaps in lesson use marks

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, IP4
- **Resolves:** —
- **Surface tier:** user-facing — it changes the review-hygiene and `/cairn-triage lessons` steps that adopting repos run
- **Branch/PR:** —

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

- [ ] AC1: In `skills/milestone-review/SKILL.md` step 9, the pass reads the
      live milestone file's `lessons used:` work-log lines before the
      sentence that deletes that file, and the use-mark sentence marks the
      lessons those lines name; the archived-file arm's list of work it
      skips names lesson use marks.
- [ ] AC2: Step 9 says how the pass finds pin files (each file that
      `git grep -l "LESSONS.md"` lists whose path contains `test`), and says
      that shortening a lesson that a `used` mark takes past 450 bytes keeps
      whole each string those files assert present and each text a live
      milestone quotes, and that a lesson that cannot then fit in 450 bytes
      takes no `used` mark and is named in the close block beside a fenced
      `/cairn-triage lessons`.
- [ ] AC3: In its too-few-removable case, step 9 writes each skipped lesson
      at the end of `cairn/LESSONS.md` as a waiting line,
      `- waiting YYYY-MM-DD (M<NNN>): <lesson>`, which counts toward the
      file's line cap and not toward its 25 lessons; where writing the line
      would bring `cairn/LESSONS.md` to 50 lines or more, that lesson is not
      written and the close block quotes it in full. Its durable-record
      preview shows verbatim each LESSONS line the pass captures, marks,
      shortens, or writes as waiting, and names each lesson it removes.
- [ ] AC4: In `skills/cairn-triage/SKILL.md`'s lessons pass: each line of a
      `split` keeps the split lesson's `used` mark, and the `split` row's
      provenance sentence names that mark as kept on every line; a `merge`
      survivor carries the `used` mark with the higher milestone number of
      the two lessons, or the one mark either has; a `compress` or `correct`
      keeps the lesson's `used` mark; in guest mode the close block quotes in
      full each lesson the pass drops or merges away; and the pass's opening
      paragraph states that review hygiene marks use and removes the
      lowest-ranked lessons at the limit, and no longer says it checks only
      the lessons the milestone covers.
- [ ] AC5: In the same pass, step 1 lists each waiting line as an item of
      its own, and step 2 proposes for it either `admit`, which removes its
      `waiting ` word so it becomes a lesson that the rank rule then counts,
      or `drop` with one of the pass's exits other than `rank`; a waiting
      line that a pin file holds or a live milestone quotes is proposed
      `admit`, never `drop`; until admitted, a waiting line is not counted
      among the lessons or ranked; and step 2's disposition count and table
      include `admit`, its row stating it applies only to a waiting line.
- [ ] AC6: In `skills/shared/templates/lessons.md`, `cairn/LESSONS.md`'s
      header, tracking-rules "Weight caps", and tracking-rules "Retiring a
      lesson", the over-limit remedy sends a lesson over 450 bytes to
      shortening or splitting and a file over 25 lessons to retirement and
      then rank eviction, and none of the four names splitting or shortening
      as a remedy for the count; each says a waiting line is not a lesson,
      takes no `used` mark, and waits for `/cairn-triage lessons`; and the
      "Retiring a lesson" bullet names the waiting line in review's
      full-file case and `admit` among the whole-file pass's dispositions.
- [ ] AC7: `cairn/DECISIONS.md` gains one entry that names D-177's "one of
      five exits" clause as superseded by D-218's `rank` exit and D-218's
      "captures nothing when none can go" clause as superseded by the waiting
      line, and records the waiting line, triage's `admit` disposition, and
      guest triage's quoting of each dropped or merged-away lesson.
- [ ] AC8: The CHANGELOG's Unreleased lessons entry states that review
      stores a skipped lesson as a waiting line that `/cairn-triage lessons`
      admits or drops, and that guest `/cairn-triage lessons` quotes each
      lesson it drops or merges away; the repo's `verify` (both gating
      `python3 -m unittest` suites, both `claude plugin validate` runs,
      `claude plugin test`) and the hand-run `skills/tests` pass on the
      review head.

## Coverage

- AC1 → T1, T6
- AC2 → T1, T6
- AC3 → T1, T6
- AC4 → T2, T6
- AC5 → T2, T6
- AC6 → T3, T6
- AC7 → T4
- AC8 → T5, T6

## Tasks

- [ ] T1: Review hygiene (`skills/milestone-review/SKILL.md` step 9, about
      lines 867-1000, and the archived-file arm near line 41): move the
      `lessons used:` read before the deletion, add the pin-file procedure
      and the pin-safe shortening rule with its no-mark outcome, the waiting
      line with its 50-line stop, the preview wording, and "mark" in the
      arm's skipped list.
- [ ] T2: Triage lessons pass (`skills/cairn-triage/SKILL.md` about lines
      107-260): `used` mark placement on split, merge, compress, and
      correct; waiting-line enumeration and the `admit` row (eight
      dispositions); guest quoting in the close block; the opening
      paragraph. Narrow DESIGN.md's Known issues sentence on guest lesson
      drops (about line 1022) to say the close block now quotes them.
- [ ] T3: Remedy and waiting-line wording at the template, this repo's
      LESSONS header, and the two rulebook sites; re-seed the rulebook-mass
      baseline in its three places (the M149 lesson).
- [ ] T4: Write the D-entry (AC7), one batched entry.
- [ ] T5: Edit M320's Unreleased CHANGELOG entry for the waiting line and
      guest quoting; sweep README for the old remedy and "captures nothing"
      wording (the M112 lesson).
- [ ] T6: Prose guards in `skills/tests` for each sentence T1-T3 add or
      change, with mutation-registry entries where neighbours have them,
      each shown red when its sentence is blanked; re-pin guards whose text
      changed; run `verify` and the hand-run `skills/tests`.

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
