# M157: Milestone IDs sort numerically — three-digit padding, numeric resolution

**Status:** done (2026-08-23, PR #158 https://github.com/jmgirard/cairn/pull/158)

**Goal:** Milestone filenames sort in id order: the rulebook pads IDs to three
digits, the scripts resolve id spellings numerically, and the 99 two-digit
archive files are renamed once.

**Outcome:** tracking-rules ID rule rewritten (three-digit padding, cross-width
resolution, padded filename prefixes, M999 one-commit re-pad); `canon_id`
(M%03d, isdecimal, non-numeric pass-through) applied at every ID
membership/lookup site in cairn_validate/cairn_next; `id_num` → isdecimal;
`M<NN>`/`m<nn>` placeholders swept to three-N forms across skills/, README,
hooks/, scripts/; 99 archive files `git mv`'d M01–M99 → M001–M099 (all R100);
D-125. Ten history-side path cites left dangling unedited (IP4): D-051's M53,
RB02 M84+M87, RB03 M95×2, RB04 M96, RR03 M95/M96/M97, RR04 M96.

**Decisions:** none milestone-local; cross-cutting → D-125.

**Review:** three-lens fan-out, two rounds. Round 1: defect return #1 ([O] F5,
release-window row-id lookup untested) plus riding fixes (canon_id isdecimal,
dep FAIL-message as-written spelling, example modernization); F1 → cairn_cost
candidate row. Round 2: [S] lenses zero findings; [O] G1 (id_num crash) fixed
at gate, G8 examples fixed, G5 cite-count superseded, G6 one-digit-dep
divergence accepted, G2/G3/G4/G7 rejected (logged).
