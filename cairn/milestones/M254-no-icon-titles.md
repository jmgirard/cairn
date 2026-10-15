<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M254: Candidate short titles hold no icons

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the rulebook and `/cairn-triage` ship to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: tracking-rules "Candidate short title" tells a writer to name
      things in words and to put no icon in a short title. It defines an
      icon as a non-ASCII character whose Unicode general category is `So`
      or `Sm` (emoji, and marks such as ○, ✓, ⌂, ✎, ↑, ⋯), with no
      exemption for text between backticks, and gives the reason: the cairn
      pane draws its own marks and Buttons beside the title. The
      paragraph's sentence on `/cairn-triage`'s `retitle` names a title that
      holds an icon beside an empty, long, or shared one.
- [ ] AC2: `skills/cairn-triage/SKILL.md`'s Title → `retitle` class text
      names a short title that holds an icon (tracking-rules "Candidate short
      title") as a trigger, its new-title rule excludes an icon, and its
      `retitle` disposition text says that for a row proposed on the icon
      trigger the new title replaces the old one, so the old title does not
      stay in the row's text.
- [ ] AC3: At the review commit, a script that cuts each Candidates row's
      short title in `cairn/ROADMAP.md` by the tracking-rules rule reports no
      non-ASCII `So` or `Sm` character, where the same script on the plan
      commit reports the two rows "⌂ edges (M241 review)" and "✎ edges (M242
      review)". Those rows are titled "Home Button edges (M241 review)" and
      "Plan Button edges (M242 review)"; each new title is not empty, holds no
      `: ` or ` — `, runs to 60 code points at most, and differs from every
      other row's title. `grep -c` for each old title over `cairn/ROADMAP.md`
      and DESIGN.md's Known issues returns 0, and the two quoted mentions at
      the plan commit (ROADMAP lines 39 and 40) quote the new titles.
- [ ] AC4: CHANGELOG.md's Unreleased section has an entry that states the
      no-icon rule with AC1's definition and the `retitle` icon trigger
      whose new title replaces the old one.
- [ ] AC5: The active profile's `verify` passes: `python3 -m unittest` for
      `scripts/tests` and `hooks/tests` from the repo root, `claude plugin
      validate` on the plugin and marketplace manifests, and `claude plugin
      test` for the status mod.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: Edit tracking-rules "Candidate short title" (`:215-222`): the
      no-icon sentence, the definition, the reason, and the `retitle`
      sentence. Append D-164 to `cairn/DECISIONS.md`: the rule passes
      D-108's door on its retained trigger, a defect in shipped behavior
      (the pane draws a row titled "⌂ edges" or "✎ edges" beside its own ⌂
      and ✎ Buttons), at the user's request; record the rejected
      alternatives from the work log.
- [ ] T2: Edit `skills/cairn-triage/SKILL.md`: the `retitle` row of the
      disposition table (`:108`) and the Title → `retitle` class
      (`:146-160`). Run the hand-run `skills/tests` prose guards that read
      this skill and the tracking-rules paragraph; fix any pin they break.
- [ ] T3: Save the AC3 script in the milestone's scratch notes, run it on
      the plan commit (expect the two rows), retitle both rows by replacing
      the old title, rewrite the two quoted mentions, rerun it (expect none).
- [ ] T4: CHANGELOG.md Unreleased entry under "Changes that affect existing
      repos".
- [ ] T5: Run `verify`.

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
