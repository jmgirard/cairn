# M187: Guest-mode DESIGN.md — principles are the operator's provisional model of the maintainers' constraints

- **Status:** in-progress
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

- [ ] AC1: The "Collaboration mode" section of `skills/shared/tracking-rules.md` carries one bullet stating that in guest mode DESIGN.md's Conventions and IP/GP principles are the operator's provisional model of the maintainers' constraints, sourced from the upstream's public norms (CONTRIBUTING, style docs, review feedback), and that a principle or convention maintainer feedback contradicts is corrected in place with a `corrected <PR ref>` mark and no D-entry; the IP/GP definition (the "DESIGN.md principles" paragraph) and the "History integrity" exception each gain a clause naming that bullet as the guest-mode reading.
- [ ] AC2: `skills/cairn-init/SKILL.md`'s "Guest mode" passage adds a numbered item: the DESIGN seed also reads the files `ls CONTRIBUTING.md CONTRIBUTING CONTRIBUTING.Rmd .github/*.md 2>/dev/null` lists and any relative in-repo path a listed file names; each Conventions line the seed writes from them cites its source file; an empty listing is stated in the Conventions section. The passage's opening list of what "runs as above" no longer names the DESIGN seed.
- [ ] AC3: `skills/design-interview/SKILL.md`'s "Session start" gains one paragraph, entered only when `cairn/PROFILE.md` carries `# Collaboration mode: guest`, stating that the interview elicits the operator's understanding of the maintainers' design and naming AC1's bullet as its rule; the Phase 2 step that writes principles gains one sentence: in guest mode every principle written carries `(provisional — guest mode)`.
- [ ] AC4: `cairn/DECISIONS.md` gains a D-entry annotating D-137 recording the in-place correction rule and the rejected alternatives (owner-mode D-entry rule kept; IPs forbidden in guest mode).
- [ ] AC5: `python3 -m unittest discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests` pass; the hand-run `python3 -m unittest discover -s skills/tests` reports no more reds and errors than the ROADMAP hygiene line's pre-existing count (4 reds + 1 error).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: Write the guest-mode bullet in tracking-rules "Collaboration mode" (`skills/shared/tracking-rules.md:288`); add the guest-mode clause to the "DESIGN.md principles" paragraph (`:55`) and the "History integrity" exception (`:121`).
- [x] T2: Add the contributor-docs item to cairn-init's "Guest mode" passage (`skills/cairn-init/SKILL.md:246`) and trim the opener's unchanged-list.
- [ ] T3: Add the guest-mode paragraph to design-interview's Session start (`skills/design-interview/SKILL.md:31`, wording that echoes no pinned marker — LESSONS 2026-08-17) and the Phase 2 mark sentence.
- [ ] T4: Append the D-entry annotating D-137.
- [ ] T5: Run the two gating suites and the hand-run prose guards; record the counts in the work log.

## Work log

- 2026-09-10: created by /milestone-plan.
- 2026-09-10: criteria audit ran in full mode ([O] reader): four findings — AC1 contradicted the IP/GP definition and History-integrity text unless both were amended (fixed: both gain a clause; D-entry added as AC4); AC2's "style document" was unenumerable (fixed: narrowed to a relative in-repo path) and the guest passage's unchanged-list named the DESIGN seed (fixed); AC3 left Phase 2 ambiguous (fixed: one sentence there); AC4's "same set" was not enumerable from the ROADMAP (fixed: count comparison).
- 2026-09-10: plan gate chose in-place `corrected <PR ref>` with no D-entry over keeping the owner-mode D-entry rule because the correcting decision is the maintainers', not the operator's; falsified by a guest repo where the operator needs the correction's rationale later and the PR thread no longer holds it.
- 2026-09-10: plan gate chose IPs allowed, marked provisional, over a GP-and-Conventions-only guest mode because the Principles touched slot and Phase 2 keep one code path; falsified by a guest-mode adopter treating a provisional IP as binding on the maintainers.
- 2026-09-10: /milestone-implement started; branch m187-guest-design-principles cut from pushed main; question gate skipped (the plan gate settled the correction mark and the IP question).
- 2026-09-10: T1 done — guest bullet under "Collaboration mode" (tracking-rules), plus the pointer clauses in the IP/GP definition and the "Correcting a record proven false" exception; scripts + hooks suites green.
- 2026-09-10: T2 done — cairn-init "Guest mode" gains item 4 (the DESIGN seed reads the contributor docs, cites sources, states an empty listing); the close block item renumbers to 5; the opener's runs-as-above list no longer names the DESIGN seed; suites green.

## Decisions

## Review
