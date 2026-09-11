# M187: Guest-mode DESIGN.md — principles are the operator's provisional model of the maintainers' constraints

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP3
- **Resolves:** —
- **Surface tier:** user-facing — skill prose every guest-mode adopter reads
- **Branch/PR:** m187-guest-design-principles

## Goal

In guest mode, DESIGN.md's Conventions and IP/GP principles are stated to be the operator's provisional model of the maintainers' constraints — inferred from the upstream's public norms, corrected by maintainer feedback — and the seed and the interview say so.

## Scope

**In:** one tracking-rules bullet under "Collaboration mode" plus a pointer in the IP/GP definition it narrows; a D-entry annotating D-137; the cairn-init guest DESIGN seed reading contributor docs; a guest-mode paragraph in `/design-interview`'s Session start and one sentence in its Phase 2 write step.

**Out:** anything a repo hands an outsider (CONTRIBUTING, PR template) → the "Contributor-facing scaffold" candidate row stands; a guest branch of the interview forbidding IPs → rejected at the plan gate, not deferred; new prose-guard tests → none (D-109: the suite gates nothing).

## Acceptance criteria

- [x] AC1: The "Collaboration mode" section of `skills/shared/tracking-rules.md` carries one bullet stating that in guest mode DESIGN.md's Conventions and IP/GP principles are the operator's provisional model of the maintainers' constraints, sourced from the upstream's public norms (CONTRIBUTING, style docs, review feedback), and that a principle or convention maintainer feedback contradicts is corrected in place with a `corrected <PR ref>` mark and no D-entry; the IP/GP definition (the "DESIGN.md principles" paragraph) and the "History integrity" exception each gain a clause naming that bullet as the guest-mode reading.
- [x] AC2: `skills/cairn-init/SKILL.md`'s "Guest mode" passage adds a numbered item: the DESIGN seed also reads the files `ls CONTRIBUTING.md CONTRIBUTING CONTRIBUTING.Rmd .github/*.md 2>/dev/null` lists and any relative in-repo path a listed file names; each Conventions line the seed writes from them cites its source file; an empty listing is stated in the Conventions section. The passage's opening list of what "runs as above" no longer names the DESIGN seed.
- [x] AC3: `skills/design-interview/SKILL.md`'s "Session start" gains one paragraph, entered only when `cairn/PROFILE.md` carries `# Collaboration mode: guest`, stating that the interview elicits the operator's understanding of the maintainers' design and naming AC1's bullet as its rule; the Phase 2 step that writes principles gains one sentence: in guest mode every principle written carries `(provisional — guest mode)`.
- [x] AC4: `cairn/DECISIONS.md` gains a D-entry annotating D-137 recording the in-place correction rule and the rejected alternatives (owner-mode D-entry rule kept; IPs forbidden in guest mode).
- [x] AC5: `python3 -m unittest discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests` pass; the hand-run `python3 -m unittest discover -s skills/tests` reports no more reds and errors than the ROADMAP hygiene line's pre-existing count (4 reds + 1 error).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: Write the guest-mode bullet in tracking-rules "Collaboration mode" (`skills/shared/tracking-rules.md:288`); add the guest-mode clause to the "DESIGN.md principles" paragraph (`:55`) and the "History integrity" exception (`:121`).
- [x] T2: Add the contributor-docs item to cairn-init's "Guest mode" passage (`skills/cairn-init/SKILL.md:246`) and trim the opener's unchanged-list.
- [x] T3: Add the guest-mode paragraph to design-interview's Session start (`skills/design-interview/SKILL.md:31`, wording that echoes no pinned marker — LESSONS 2026-08-17) and the Phase 2 mark sentence.
- [x] T4: Append the D-entry annotating D-137.
- [x] T5: Run the two gating suites and the hand-run prose guards; record the counts in the work log.

## Work log

- 2026-09-10: created by /milestone-plan.
- 2026-09-10: criteria audit ran in full mode ([O] reader): four findings — AC1 contradicted the IP/GP definition and History-integrity text unless both were amended (fixed: both gain a clause; D-entry added as AC4); AC2's "style document" was unenumerable (fixed: narrowed to a relative in-repo path) and the guest passage's unchanged-list named the DESIGN seed (fixed); AC3 left Phase 2 ambiguous (fixed: one sentence there); AC4's "same set" was not enumerable from the ROADMAP (fixed: count comparison).
- 2026-09-10: plan gate chose in-place `corrected <PR ref>` with no D-entry over keeping the owner-mode D-entry rule because the correcting decision is the maintainers', not the operator's; falsified by a guest repo where the operator needs the correction's rationale later and the PR thread no longer holds it.
- 2026-09-10: plan gate chose IPs allowed, marked provisional, over a GP-and-Conventions-only guest mode because the Principles touched slot and Phase 2 keep one code path; falsified by a guest-mode adopter treating a provisional IP as binding on the maintainers.
- 2026-09-10: /milestone-implement started; branch m187-guest-design-principles cut from pushed main; question gate skipped (the plan gate settled the correction mark and the IP question).
- 2026-09-10: T1 done — guest bullet under "Collaboration mode" (tracking-rules), plus the pointer clauses in the IP/GP definition and the "Correcting a record proven false" exception; scripts + hooks suites green.
- 2026-09-10: T2 done — cairn-init "Guest mode" gains item 4 (the DESIGN seed reads the contributor docs, cites sources, states an empty listing); the close block item renumbers to 5; the opener's runs-as-above list no longer names the DESIGN seed; suites green.
- 2026-09-10: T3 done — design-interview Session start gains the guest-mode paragraph (entered on the PROFILE mode line, names the tracking-rules bullet as its rule; no pinned-marker phrase echoed — the skill has no guarded slice there) and the Phase 2 write-out gains the `(provisional — guest mode)` sentence; suites green.
- 2026-09-10: T4 done — D-139 appended, annotating D-137 (in-place `corrected <PR ref>` correction, no D-entry; rejected: owner-mode D-entry rule, no-IP guest interview); validate green.
- 2026-09-10: T5 done — scripts 391 green, hooks 146 green; skills/tests 661: first run 4 reds + 2 errors, one over the ROADMAP baseline — the T1 bullet's back-reference echoed the guard marker "Correcting a record proven false", so the mutation harness's blanking no longer removed the only occurrence (LESSONS 2026-08-17); reworded to "the record-correction rule's principle exception"; re-run 4 reds + 1 error, the pre-existing set as on main.
- 2026-09-10: claim audit: 17 claims read, 1 corrected — skills/cairn-init/SKILL.md, skills/design-interview/SKILL.md, skills/shared/tracking-rules.md (the contributor-docs `ls` listing aborted under zsh on an unmatched glob with an error the redirect cannot hide; wrapped in `bash -c`, the criterion's command kept literal inside it; the re-read ran in a fresh [O] reader rather than the same one — this session has no send-message tool to continue an agent — and returned HOLDS, noting the wrapped command exits 1 on success because the absent `CONTRIBUTING`/`CONTRIBUTING.Rmd` operands always fail `ls`; nothing reads the exit code).
- 2026-09-10: all tasks checked; status → review.

## Decisions

## Review

_2026-09-10, on branch m187-guest-design-principles at a49d7d4; main at f2b9d67 (not moved since the cut)._

- AC1: evidence — the "Collaboration mode" section of tracking-rules carries the bullet (`awk` over the section: "provisional model of the maintainers' constraints", "sourced from the upstream's public norms — CONTRIBUTING, style docs, review feedback", "corrected in place, marked `corrected <PR ref>`, with no D-entry"); the "DESIGN.md principles" paragraph (:55–59) and the "Correcting a record proven false" exception (:120–125) each carry one clause naming the "Collaboration mode" bullet (grep count 1 each). PASS.
- AC2: evidence — cairn-init "Guest mode" item 4 states the seed reads the files `ls CONTRIBUTING.md CONTRIBUTING CONTRIBUTING.Rmd .github/*.md 2>/dev/null` lists (the command run under `bash -c`, the implement claim audit's correction) and any relative in-repo path a listed file names; each Conventions line cites its source file; an empty listing is stated in the Conventions section; the opener's runs-as-above list reads "the `cairn/` tree, the ROADMAP skeleton, the PROFILE instantiation, the greenfield openers" — no DESIGN seed. PASS.
- AC3: evidence — design-interview Session start paragraph at :48 opens "When `cairn/PROFILE.md` carries `# Collaboration mode: guest`", states the interview elicits the operator's understanding of the maintainers' design, and names "the 'Collaboration mode' bullet on DESIGN.md in tracking-rules" as its rule; Phase 2 write-out :136 carries "In guest mode every principle written carries `(provisional — guest mode)`". PASS.
- AC4: evidence — `### D-139` at DECISIONS.md:5149, heading says "annotates D-137"; body records the in-place `corrected <PR ref>` no-D-entry rule and the two rejected alternatives (owner-mode D-entry rule; IPs forbidden in guest mode). PASS.
- AC5: evidence — `python3 -m unittest discover -s scripts/tests`: 391 OK; `hooks/tests`: 146 OK; hand-run `skills/tests`: 661, 4 failures + 1 error, equal to the ROADMAP hygiene line's pre-existing count (4 reds + 1 error). PASS.
- Consistency gate: `cairn_validate.py` all checks passed (exit 0); no DESIGN.md principle changed, so `cairn_impact --changed` skipped; generic profile names no toolchain checks. Driving RR: none.

**Independent review** (user-facing tier → three lenses; ranked as reported):

- [O] diff-bug F1 — cairn-init item 4's closing "writes what the upstream's own documents say and nothing it infers" contradicted the seed step above it, which infers Purpose & Scope from DESCRIPTION and source. **Fix now**: reworded to "a Conventions line the seed writes from those documents stays close to what they say, and the inference the seed step above already allows for Purpose & Scope is not extended to Conventions".
- [O] diff-bug F2 — the interview marks principles provisional but not Conventions, so a guest interview could overwrite the seed's cited Conventions lines unmarked. **Reject**: the tracking-rules bullet makes Conventions provisional by statement, mark or no mark; AC3 binds the mark to principles; how the interview treats existing Conventions lines is pre-existing interview conduct the diff did not touch.
- [O] diff-bug F3 — design-interview's opening ("interviews the human for the intent behind the repo") read against the new guest paragraph ("not the operator's own intent"). **Fix now**: the opening gains the parenthetical "(in guest mode, for their understanding of the maintainers' intent — Session start below)".
- [O] diff-bug F4 — the three pointers call the bullet "the 'Collaboration mode' bullet on DESIGN.md" and the bullet carries no such literal name; the phrase could read as a bullet inside DESIGN.md. **Reject**: the pointer is descriptive (section name plus subject), the bullet's bold opener begins "DESIGN.md's Conventions and IP/GP principles", and this repo owes no prose guard (D-109).
- [O] diff-bug F5 — the scaffolded DESIGN.md skeleton comment (cairn-init :151–154) still defines IP as a plain hard constraint with no guest reading. **Reject**: an unmodified line of a template shared by both modes; the rulebook bullet governs and the skeleton comment states the owner definition the guest bullet narrows.
- [O] diff-bug F6 — AC1 names "the 'History integrity' exception", a heading tracking-rules does not carry; the clause landed in "Correcting a record proven false". **Reject as a naming slip, not a reinterpretation**: the plan's criteria-audit work-log line names the same passage ("History-integrity text", the IP4 exception), the referent is the only principle exception in that rule, and the promise is met as written — no amendment convened.
- [O] diff-bug F7 — AC2's command ships wrapped in `bash -c`, and the wrapped form exits 1 even when it lists files. **Reject**: already dispositioned by the implement claim audit (work log 2026-09-10); the criterion's command is literal inside the wrapper and nothing reads the exit code.
- [O] diff-bug F8 — two insertions broke the files' wrap (one overlong line, one short orphan line). **Fix now**: rewrapped alongside F1 and F3.
- [S] blame-history — no contradiction of D-045 or D-137 (D-139 annotates D-137 by the rulebook's own mechanism); the item renumbering 4→5 is cited nowhere by number; one note restating F7's exit-code gotcha. **Noted** (F7's disposition).
- [S] prior-PR-comments — no prior-review evidence: the M184/M185/M186 and design-interview-lineage archives carry no findings on the changed lines; the GitHub inline-comment probe returned empty. Zero findings.
- Post-fix: scripts 391 OK, hooks 146 OK, skills/tests 4 reds + 1 error (baseline), validate green.
