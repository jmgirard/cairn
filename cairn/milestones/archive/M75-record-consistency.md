# M75: Record consistency — the `leave` disposition and MCP-matcher semantics

**Status:** done · 2026-07-18 · PR https://github.com/jmgirard/cairn/pull/73

**Goal.** Close two gaps where cairn's durable record failed to carry a fact
its own work had already established.
**Outcome.** `tracking-rules.md`'s Intake paragraph now names `leave` a legal
fourth issue disposition, narrowed to noise, duplicates, and items already
cross-referenced **in cairn** — closing the split where `/milestone` §3
offered it but the rulebook listed three routes, leaving an
acknowledged-and-left issue with the GitHub issue as its sole record (the
D-042 substitution). Two label-inclusive guards + mutation entries lock it;
falsifiability proven against label swap, not just blanking (M74/F3).
`references/claude-code-hooks.md` now documents hook matcher dispatch as
implemented, verified against binary 2.1.207 (`GFy`) — see LESSONS for the
rule. `LESSONS.md:41` (M71) carried the wrong rule; corrected in place.

**Key decisions.** D-044 records the IP3 reading the narrowing rests on — a
reason-stated `leave` on noise is not the *silent* drop IP3 forbids —
rejecting "drop `leave` from the skill" and "legitimize it unnarrowed". AC4
was amended at the implement gate: its wording mandated the wrong rule.

**Review.** Two trips. Trip 1 failed the gate; trip 2 passed 6/6 ACs fresh,
G1 fixed in review, G4 (in-place LESSONS correction vs. append-only)
accepted with the deviation logged and spun off as a candidate row.
