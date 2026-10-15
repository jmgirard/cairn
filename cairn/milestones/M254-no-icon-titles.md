<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M254: Candidate short titles hold no icons

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the rulebook and `/cairn-triage` ship to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m254-no-icon-titles https://github.com/jmgirard/cairn/pull/265   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A candidate row's short title names things in words and holds no icon, so the cairn pane's own marks and Buttons beside the title are never confused with title text.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a no-icon sentence in tracking-rules "Candidate short title";
an icon trigger in `/cairn-triage`'s `retitle` class, whose new title
replaces the old one; new titles for this repo's two icon rows and their
quoted mentions; a D-entry passing D-108's door; a CHANGELOG entry.

**Out:** a `cairn_validate` advisory (declined at the question set, as
D-163 declined one for long titles); the ROADMAP skeleton comment in
`skills/cairn-init/SKILL.md`, which points at the rule and is embedded in
`hooks/status/fixtures.gen.ts`; titles in other repos, which a
`/cairn-triage` pass there proposes for `retitle`.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [x] AC1: tracking-rules "Candidate short title" tells a writer to name
      things in words and to put no icon in a short title. It defines an
      icon as a non-ASCII character whose Unicode general category is `So`
      or `Sm` (emoji, and marks such as ○, ✓, ⌂, ✎, ↑, ⋯), with no
      exemption for text between backticks, and gives the reason: the cairn
      pane draws its own marks and Buttons beside the title. The
      paragraph's sentence on `/cairn-triage`'s `retitle` names a title that
      holds an icon beside an empty, long, or shared one.
- [ ] AC2: `skills/cairn-triage/SKILL.md`'s Title → `retitle` class text
      names a short title that holds an icon (tracking-rules "Candidate short
      title") as a trigger, and its new-title rule excludes an icon. Its
      `retitle` disposition text says that for a row proposed on the icon
      trigger whose short title ends at a `: `, the new title replaces the
      old one in place, so the old title does not stay in the row's text,
      and that any other row proposed on the icon trigger takes the new
      title and `: ` before its text, which stays with each icon removed.
- [x] AC3: At the review commit, a script that cuts each Candidates row's
      short title in `cairn/ROADMAP.md` by the tracking-rules rule reports no
      non-ASCII `So` or `Sm` character, where the same script on the plan
      commit reports the two rows "⌂ edges (M241 review)" and "✎ edges (M242
      review)". Those rows are titled "Home Button edges (M241 review)" and
      "Plan Button edges (M242 review)"; each new title is not empty, holds no
      `: ` or ` — `, runs to 60 code points at most, and differs from every
      other row's title. `grep -c` for each old title over `cairn/ROADMAP.md`
      and DESIGN.md's Known issues returns 0, and the two quoted mentions at
      the plan commit (ROADMAP lines 40 and 41) quote the new titles.
- [x] AC4: CHANGELOG.md's Unreleased section has an entry that states the
      no-icon rule with AC1's definition and the `retitle` icon trigger
      whose new title replaces the old one.
- [x] AC5: The active profile's `verify` passes: `python3 -m unittest` for
      `scripts/tests` and `hooks/tests` from the repo root, `claude plugin
      validate` on the plugin and marketplace manifests, and `claude plugin
      test` for the status mod.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2, T6, T7
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Edit tracking-rules "Candidate short title" (`:215-222`): the
      no-icon sentence, the definition, the reason, and the `retitle`
      sentence. Append D-164 to `cairn/DECISIONS.md`: the rule passes
      D-108's door on its retained trigger, a defect in shipped behavior
      (the pane draws a row titled "⌂ edges" or "✎ edges" beside its own ⌂
      and ✎ Buttons), at the user's request; record the rejected
      alternatives from the work log.
- [x] T2: Edit `skills/cairn-triage/SKILL.md`: the `retitle` row of the
      disposition table (`:108`) and the Title → `retitle` class
      (`:146-160`). Run the hand-run `skills/tests` prose guards that read
      this skill and the tracking-rules paragraph; fix any pin they break.
- [x] T3: Save the AC3 script in the milestone's scratch notes, run it on
      the plan commit (expect the two rows), retitle both rows by replacing
      the old title, rewrite the two quoted mentions, rerun it (expect none).
- [x] T4: CHANGELOG.md Unreleased entry under "Changes that affect existing
      repos".
- [x] T5: Run `verify`.
- [x] T6: Review return: amend AC2 for a row with neither separator, and
      align SKILL.md :108, tracking-rules' `retitle` sentence, and D-164.
- [x] T7: Review return 1: AC2 per the user's choice; triage step 4 Apply
      and trigger precedence; tracking-rules, D-164, CHANGELOG, README; the
      rulebook-mass baseline in three places; follow-ups into "Retitle edges
      (M251 review)"; ROADMAP back under its byte budget.

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

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: milestone — the change edits the shipped rulebook and `/cairn-triage`, which is runtime surface for plugin users.
- 2026-10-15: collision check: D-163 (M251) defined the short title and the `retitle` disposition; this extends both. D-108's door applies to a new records rule; T1's D-entry passes it on the shipped-pane defect. No ROADMAP row or archived milestone covers icons. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-15: criteria audit (full, Opus fresh reader) returned 9 findings, all fixed: D-108 door → T1 D-entry; `So` missed the pane's ↑ ↓ ⋯ (`Sm`) → definition widened to non-ASCII `So`/`Sm`; backtick exemption dropped, since the pane does not strip backticks; the paragraph's stale `retitle` sentence → in AC1; AC2 worded as skill text, not behavior over every repo; `retitle` prepend would leave the icon title in the row → the icon trigger replaces it; AC3 pinned to the review commit, its two mentions named, new titles checked against triage's rule; AC3's script shown to discriminate on the plan commit. False positives such as ©, ° and ≤ are accepted.
- 2026-10-15: question set: icon definition — non-ASCII `So` or `Sm` characters; enforcement — rule and triage `retitle` only, no validate advisory; new titles — "Home Button edges (M241 review)" and "Plan Button edges (M242 review)".
- 2026-10-15: plan gate chose non-ASCII `So`/`Sm` over `So` alone because the pane draws ↑ ↓ ⋯ (`Sm`) beside titles; falsified by a pane mark outside both categories, or by false positives in real titles.
- 2026-10-15: plan gate chose rulebook and triage only over a `cairn_validate` advisory because D-163 declined one for long titles and the repo has 2 icon rows; falsified by icon titles recurring after the rule ships.
- 2026-10-15: plan decided to leave the cairn-init ROADMAP skeleton comment as it is, since it points at the rule and `hooks/status/fixtures.gen.ts` embeds it.

- 2026-10-15: T1 done: tracking-rules "Candidate short title" gains the no-icon sentence, the `So`/`Sm` definition, the pane reason, and the `retitle` icon sentence; D-164 appended.
- 2026-10-15: T2 done: `/cairn-triage`'s `retitle` row says an icon title is replaced in place, keeping its `: ` or ` — `; the Title class names the icon trigger and the new-title rule excludes an icon. Implement choice: replace in place rather than prepend-then-strip, so a row cut at ` — ` keeps that cut. All 752 hand-run `skills/tests` pass.
- 2026-10-15: substantive amendment: AC3's parenthetical "(ROADMAP lines 39 and 40)" → "(ROADMAP lines 40 and 41)"; at plan commit 0c1976c2 the M254 row had moved the two quoted mentions down one line. Wording only, the deliverable unchanged.
- 2026-10-15: re-audit: AC3 (full) — nothing; the reader confirmed the mentions sit on lines 40 and 41 at 0c1976c2.
- 2026-10-15: T3 done: the AC3 script (session scratchpad `icon_titles.py`) reports 2 icon rows on 0c1976c2 and 0 after the edit; both rows retitled in place, the two quoted mentions rewritten; `grep -c` for each old title over ROADMAP and DESIGN.md returns 0; both new titles meet the triage new-title rule.
- 2026-10-15: T4 done: CHANGELOG Unreleased entry "Candidate short titles hold no icons" under "Changes that affect existing repos".
- 2026-10-15: T5 done: verify green — scripts/tests 408 OK (21 skipped), hooks/tests 175 OK, plugin validate passed with warnings, marketplace validate passed with no warning, plugin test 1729 pass 0 fail.
- 2026-10-15: claim audit fixes (checkpoint, re-read pending): "Emoji are icons" → "Most emoji are icons"; the pane reason now says some marks and Buttons sit beside the title; a no-separator row takes the new title and `: ` before its text; D-164's Context places each glyph as pane.ts draws it.
- 2026-10-15: claim audit: 17 claims read, 1 corrected — CHANGELOG.md, skills/cairn-triage/SKILL.md, skills/shared/tracking-rules.md. The re-read found the corrections hold; it also flagged D-164's "beside its own ⌂ and ✎ Buttons", now reworded.
- 2026-10-15: amendment routed: AC2 — AC2 promises the old title never stays in the row's text, but a row with neither `: ` nor ` — ` is all title, so replacing it in place would drop the row's detail; the skill (after the claim audit) gives that row the new title and `: ` before its text, so AC2 as written fails for that case alone.
- 2026-10-15: re-audit: AC2 (full) — the reader found the "says what a row with neither separator takes" clause accepted any answer, D-164 and tracking-rules stated replacement with no carve-out, and SKILL.md :108 said "the icon" where AC2 says "the old title"; all three fixed and the clause pinned.
- 2026-10-15: re-audit: AC2 (full) — nothing; the reader confirmed SKILL.md :108 and :146-157, D-164, and tracking-rules :225 agree with the amended wording.
- 2026-10-15: amendment return: AC2 — "Its `retitle` disposition text says that for a row proposed on the icon trigger whose short title ends at a `: ` or ` — `, the new title replaces the old one in place, so the old title does not stay in the row's text, and that a row with neither separator takes the new title and `: ` before its text, which stays."
- 2026-10-15: T6 done: SKILL.md :108 now says "so the old title and its icon do not stay in the row" and "which stays"; tracking-rules says the icon title is replaced in place when a `: ` or ` — ` follows it; D-164's Decision states the no-separator case.
- 2026-10-15: amendment routed: AC2 — diff-bug #2: in-place replacement deletes the detail of a row cut at ` — `; second AC2 amendment, posed to the user at the stop.
- 2026-10-15: question set (review stop): AC2's second amendment — "In place only after `: `": a title ending at `: ` is replaced in place, and any other icon row takes the new title and `: ` before its text, which stays with each icon removed.
- 2026-10-15: review return 1: triage SKILL.md step 4 Apply contradicts the icon exception (diff-bug #1, blame-history #1); also fix now: trigger precedence (diff-bug #3), tracking-rules no-separator case (diff-bug #4), CHANGELOG "opens with" (diff-bug #6), cut-title wording (blame-history #3), rulebook-mass baseline (prior-review #1), README triggers (prior-review #2), and the follow-ups into "Retitle edges (M251 review)".
- 2026-10-15: amendment return: AC2 — "Its `retitle` disposition text says that for a row proposed on the icon trigger whose short title ends at a `: `, the new title replaces the old one in place, so the old title does not stay in the row's text, and that any other row proposed on the icon trigger takes the new title and `: ` before its text, which stays with each icon removed." The user chose this wording at the review stop, so no further reader ran (two `re-audit: AC2` lines stand).
- 2026-10-15: T7 done: SKILL.md :108 and step 4 Apply state the icon exception and that it wins over other triggers; tracking-rules, D-164, CHANGELOG, README updated; rulebook-mass baseline re-seeded to 668 lines / 64,196 bytes (milestone SKILL.md, test_cost_audit_line.py, test_mutation_harness.py); "Retitle edges (M251 review)" absorbs diff-bug #7 and prior-review #3; four wide ROADMAP rows reworded with no fact dropped, ROADMAP 23,998 bytes.
- 2026-10-15: verify after T7: scripts/tests 408 OK (21 skipped), hooks/tests 175 OK, both validates passed, plugin test 1729 pass 0 fail; skills/tests 752 OK.
- 2026-10-15: review pass 2 fix: tracking-rules' `retitle` sentence now says the non-`: ` icon row gets the new title before its text with its icons removed; baseline re-seeded to 668 lines / 64,222 bytes in the three places.
- 2026-10-15: correction to the T7 line: ROADMAP was 23,993 bytes after T7, not 23,998.
- 2026-10-15: review pass 2 fixes: ROADMAP rows reworded in T7 restored to their 7abcfe7d text (the Re-measure row kept, no fact lost), the M254 follow-ups folded into "Retitle edges (M251 review)", twelve other rows reworded with no fact dropped, ROADMAP 59 lines / 23,997 bytes; D-164 heading; README wording; the Title class points at the `retitle` row's icon edit.

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

- AC1: tracking-rules.md:221-226 reads "Name things in words and put no icon in a short title, because the cairn pane draws its own marks and Buttons with such glyphs, and some sit beside the title", defines an icon as "a non-ASCII character whose Unicode general category is `So` or `Sm`, between backticks or not", gives emoji and ○ ✓ ⌂ ✎ ↑ ⋯ as examples, and its `retitle` sentence names an icon title beside empty, long, or shared ones. Met.
- AC2: cairn-triage SKILL.md:146-149 lists "holds an icon (tracking-rules "Candidate short title")" as a trigger; :155-156 "holds no `: `, ` — `, or icon"; :108 says the icon-trigger title "replaces the old one in place, and the row keeps the `: ` or ` — ` after it, so the old title and its icon do not stay in the row" and "A row with neither separator takes the new title and `: ` before its text, which stays". Met (amended wording).
- AC3: the scratchpad `icon_titles.py` cut script reports "45 rows, 2 with icons" (⌂ edges, ✎ edges) on 0c1976c2 and "45 rows, 0 with icons" on the head; both new titles meet the triage new-title rule; `grep -c` for each old title returns 0 over ROADMAP and DESIGN.md Known issues; ROADMAP:40-41 quote "Home Button edges (M241 review)" and "Plan Button edges (M242 review)", where 0c1976c2:40-41 quoted the old titles. Met.
- AC4: CHANGELOG.md:7-17, Unreleased "Changes that affect existing repos", states the `So`/`Sm` non-ASCII definition, between backticks or not, and the `retitle` icon trigger replacing the title in place. Met.
- AC5: verify on 64a59375: scripts/tests 408 OK (21 skipped), hooks/tests 175 OK, plugin validate passed with warnings, marketplace validate passed with no warning, plugin test 1729 pass 0 fail. `cairn_validate.py` all checks passed. Met.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: cairn-triage SKILL.md:252-256 step 4 Apply still says `retitle` always prepends and keeps the old title, contradicting :108 — fix now (in the return below).
- diff-bug #2: in-place replacement deletes the description of a row cut at ` — `, whose title is usually its whole detail and trigger — amendment routed (AC2 mandates it); second AC2 amendment, so the user decides.
- diff-bug #3: SKILL.md does not say which edit wins when a row meets the icon trigger and another — fix now.
- diff-bug #4: tracking-rules' `retitle` sentence does not cover an icon row with neither separator — fix now.
- diff-bug #5: AC1's "beside an empty, long, or shared one" against a two-sentence split — reject, false: the adjacent sentences name all four triggers.
- diff-bug #6: CHANGELOG says a title that "opens with" an icon reads as a Button, narrower than the rule — fix now.
- diff-bug #7: a retitle while a PR carries a `Candidate row:` line breaks the pane's link — follow-up, absorbed into "Retitle edges (M251 review)".
- diff-bug #8: archived M241/M242 files still quote the old titles — reject, planned change: history is not edited (IP4).
- diff-bug #9: uneven line wraps in DECISIONS, CHANGELOG, SKILL.md — reject, style.
- blame-history #1: same as diff-bug #1 — fix now.
- blame-history #2: same as diff-bug #3 — fix now.
- blame-history #3: the replaced span for `⌂ a — b: c` is defined only through the cut rule — fix now (wording names the cut title).
- blame-history #4: in-place replacement loses the old title's words — reject, planned change.
- blame-history #5: D-164 consistent with D-163 and D-149 — noted.
- blame-history #6: `→`, `×`, `≥` titles become `retitle` triggers — reject, planned change (the user chose non-ASCII `So`/`Sm`).
- blame-history #7: same as diff-bug #7 — follow-up, absorbed into "Retitle edges (M251 review)".
- prior-review #1: the rulebook-mass baseline (milestone SKILL.md:118, test_cost_audit_line.py:68, test_mutation_harness.py:120) still reads 664 lines / 63,690 bytes — fix now.
- prior-review #2: README.md:323-324 lists the old `retitle` triggers and no no-icon sentence — fix now.
- prior-review #3: the amend loop applies a user-named title with no icon check — follow-up, absorbed into "Retitle edges (M251 review)".
- prior-review #4: same as blame-history #3 — fix now.
- prior-review #5: retitled rows and mentions consistent — noted.
- prior-review #6: PR #257's stamp point — noted, no finding.

