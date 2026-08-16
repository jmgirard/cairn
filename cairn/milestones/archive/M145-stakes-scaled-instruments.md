# M145: Standing instruments scale to stakes

**Status:** done (2026-08-16, PR #146 https://github.com/jmgirard/cairn/pull/146)

**Goal:** Standing verification instruments scale to the stakes of what they
check — or stand down (RR13 recs 5–7/B1).

**Outcome:** /milestone-review routes by surface tier — internal docs-only
diff → one [O] reviewer, else the three-lens fan-out; confidence scorer
retired: reviewers rank, the maintainer triages at the gate, all logged
(IP3). RRs advisory by default — Binding criteria only via the brief
header's request slot; a second-escalation brief lists removal as a
question. Plan-gate criteria audit scaled: full for user-facing or
tripwire-tagged work, reduced two-question form for internal tier.
records-hygiene §5 retired; its surviving triage heuristics live in step 5.

**Decisions:** none milestone-local; cross-cutting → D-110 (scorer),
D-111 (audit scaling), D-112 (routing — defines "both modes"),
D-113 (batched D-111 corrections).

**Review:** first review under its own rules — full fan-out, 24 ranked
findings: 14 fixed at the gate (step-ordering coherence, amendment-audit
mode, BC request slot, D-112/D-113), 2 follow-ups (sub-threshold-findings
row dropped as fulfilled — its ask is now standard triage; stakes-tier row
shape → M147 ledger), 8 rejected with logged reasons.
