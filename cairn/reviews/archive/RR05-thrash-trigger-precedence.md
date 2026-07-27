# RR05: Thrash-rule trigger precedence and the post-re-cut case (M114)

- **Date:** 2026-07-26
- **Brief:** `cairn/reviews/RB05-thrash-trigger-precedence.md`
- **Reviewer baseline:** working tree at `main`-tracking branch state per the
  brief; all three suites green from the repo root with exit codes checked
  separately (skills 621 / scripts 280 / hooks 91, exit 0 each);
  `python3 scripts/cairn_validate.py` exit 0, all checks passed. No tracked
  file was modified during this review.

## Answers

### 1. Trigger (a)'s condition — keep the threshold, make the wording say so, and make the remedy state-aware

**Keep it a threshold.** The predicate should be true on the third return and
on every return after it. Reject the two named alternatives:

- **"Exactly the third return" — reject.** A point predicate fires once and
  then goes silent for every later return. That recreates the intraclass M93
  signature (D-064 Context: "the thrash rule fired once, at the third return,
  and then went silent for four more") through the trigger side instead of the
  counter side. The original defect was not *where* the reset lived; it was
  that the rule stopped speaking while the milestone kept returning. A
  maintainer who declines the return-3 recommendation would then face returns
  4, 5, 6 with the rule mute — the exact drift M93's log recorded as
  "thrash-rule disposition left to the maintainer".
- **"The third return since the last re-cut" — reject.** This is per-cut
  resetting of the trigger window. D-064 choice 1 counts "per milestone, never
  per cut" because "a re-cut is itself evidence of thrash"; a window that
  reopens three fresh returns of headroom after each re-cut grants exactly the
  leniency that let M93 run to eight passes across three re-cuts. The
  constraint says a per-cut-reset recommendation must argue against D-064
  directly; I decline to — D-064's evidence is sound, and a rule should be
  *more* ready to fire after a re-cut, not freshly lenient.

**Two changes are still owed.** First, wording: "A third return" reads
naturally as either a point or a threshold, and J2 (82) turned on the
threshold reading. Say it in so many words: *the third return, and every
return after it*. Second — and this is where J2's trap actually lives — the
predicate staying true forever is only a defect because the remedy attached to
it is static. "Recommend re-plan or split" is a single-shot remedy; from the
first post-re-cut return onward the rule prescribes a remedy the work log
shows is already spent. The fix is not to narrow the predicate but to branch
the remedy on whether a trigger-(a) re-plan/split has already been taken —
which the work log, the counting source the rule already names, records. The
pre-spend branch keeps today's remedy; the post-spend branch is question 3.

### 2. Precedence should not exist in its unconditional form — the triggers compose, with (a) owning only the disposition

**Composition is correct, and M114's own history proves it.** The two triggers
answer orthogonal questions — (a) "is this milestone mis-sized?", (b) "is this
approach wrong?" — and mis-sized and wrong-approach are not mutually
exclusive, so a rule that answers one by discarding the other throws away
evidence. Concretely, (b)'s diagnosis is exactly what a trigger-(a) re-plan
needs: the rule's own words say re-cutting around the same predicate "buys the
next mechanism, not a fix", so a re-plan performed blind to the shape evidence
walks straight into that. Unconditional precedence therefore degrades (a)'s
own remedy. And the one time both actually fired — M114 pass 3 — the re-cut in
practice composed them: it followed (a)'s disposition (split) while using
(b)'s shape evidence to decide where to draw the line ("Split at the line the
evidence drew" — work log, re-cut entry). The shipped clause forbids what the
humans correctly did.

**The genuinely conflicting element is one question only:** whether to queue
another retry. (b) standing alone permits a retry that adopts the recorded
alternative; (a) says do not queue another retry. On that single question,
**(a) is the right winner** — three returns mean the current plan is not
containing the work whatever the failure shape, and the shipped clause's
justification ("it is the stricter") is correct exactly this far and no
further. Everything else in (b) — the diagnosis, the
reconsider-the-alternative instruction, the `/milestone-brief` offer where no
alternative was recorded — answers a question (a) does not, and survives.

So: **scoped precedence, which is composition.** Where both fire, (a) governs
the disposition (no further retry under the current plan; route through
`/milestone-plan`), and (b)'s diagnosis rides into that routing — the re-plan
reconsiders the recorded alternative rather than re-cutting around the same
predicate, and where none was recorded the escalation offer stands at the
routing chip rather than being foreclosed. One nuance on J2's "unreachable by
rule": D-062 already permits offering escalation for any genuinely hard
question, so the clause could not literally forbid it — but a rule that
directs the session away from the offer suppresses it in practice, which is
what happened: at pass 3 the session followed (a) and offered no escalation;
pass 4's escalation came from the user, outside the rule. J2 is real in
effect.

### 3. The post-re-cut case — escalating remedies, not a terminal disposition, and the absence is not correct

**The absence is a real gap.** I confirmed the brief's claim: neither
`skills/milestone-plan/SKILL.md`, `skills/milestone-brief/SKILL.md`, nor
`skills/shared/tracking-rules.md` says anything about a milestone returning
after a re-plan or split (`milestone-plan` mentions `blocked` only for release
parking; tracking-rules' status table and transitions are silent on thrash).
Today the count rises and trigger (a) re-prescribes the spent remedy. M114 is
the live case: fourth return, one re-cut spent, resolved only because the user
called an escalation by hand.

**"The maintainer approves every chip anyway" does not make absence correct.**
The whole thrash rule exists because that argument already failed once:
intraclass M93's maintainer approved every chip too, and with no rule
composing the right recommendation the disposition drifted to retry-by-default
for four extra returns. A routing chip is only as good as what the session
composes into it (the contextual-chips doctrine); the rule's job is to change
the *recommended* option when the evidence says the standard remedies are
exhausted. Silence here re-creates M93 one level up.

**Reject a terminal disposition.** An automatic drop violates IP3 (nothing the
user asked for is silently dropped — `dropped` is a user decision in the
status table). Mandatory escalation violates the D-004/D-062 frame the
constraints fix: escalation is offered per instance, never automatic. A forced
park pre-empts a maintainer who may know exactly why the next attempt will
land.

**Recommend: an exhaustion branch on trigger (a).** When (a) fires and the
work log already records a re-plan or split spent on this milestone, the rule
stops prescribing re-plan-or-split and instead directs the session to compose
the routing chip from the remaining honest dispositions:

- **offer escalation via `/milestone-brief`** (per instance, gated — this is
  an offer on a condition hit, like an RB tripwire, not a standing menu item;
  a milestone still returning after a re-cut is squarely D-062's "genuinely
  hard question the session cannot confidently settle");
- **park as `blocked`**, work-log line naming what it waits on (legal today:
  "any skill, reason logged");
- **drop**, as an explicit user decision, one-line reason archived (IP3-clean
  because the user selects it, nothing silent);

and never composes a bare retry as the recommended option. The maintainer
still decides everything — the rule only stops the chip from nominating a
spent remedy. This is precisely what M114's own resolution did by hand
(blocked on RB05 at the user's call); the rule should encode what the humans
already did. Cost: two or three sentences in `/milestone-review`, which is not
the always-read rulebook, so D-057's door governance is not in play.

### 4. Reverting is not the honest answer — ship the scoped fix

Weighing revert (back to F4's documented ambiguity, 60) against a scoped fix:

- **The ambiguity is not hypothetical.** F4 predicted the collision at pass 1;
  it happened at pass 3. Reverting reinstates a gap that this milestone's own
  history proves gets hit, and the post-re-cut case (question 3) would remain
  unwritten — M114 itself is standing in it right now.
- **The D-059 precedent does not transfer.** D-059 retired a *mechanical
  classifier* whose defects were measured to interact ("independent patches
  leave the advisory's green contingent on where a paragraph wraps") and whose
  recall was already carried by another mechanism — repair was genuinely
  hazardous and retirement cost nothing. Here the artifact is a prose clause,
  the correct replacement is derivable from the failure analysis (question 2),
  no other mechanism carries the load, and retirement costs a known,
  demonstrated collision returning to "no stated precedence".
- **The escalation reason was author self-distrust, not unknowability.** The
  author escalated because their judgment on their own doctrine edits was the
  thing in question — a good reason to want independent review, which this RR
  now supplies, complete with binding criteria a mechanical diff will hold the
  implementation to. With that in hand, the argument for reverting (no vetted
  replacement exists) no longer holds.
- **Cost parity.** The precedence clause is guard-pinned with two asserts and
  two registry entries; revert and replace each require touching the same two
  test files. Reverting buys no meaningful diff reduction.

Revert would be defensible only as an explicit maintainer choice to minimize
motion while parking the design in a candidate row; on the merits, the scoped
fix is better on every axis except diff size, and not by much there. Nothing
in this recommendation supersedes a recorded decision: the precedence clause
is milestone-authored prose from M114's re-cut gate, not a D-entry, and all
six D-064 choices stand untouched.

### 5. Guard changes owed by the recommendation

If the rule text changes per questions 1-3, in
`skills/tests/test_thrash_rule.py` and `skills/tests/test_mutation_harness.py`:

**Delete (with their registry entries):**
- `TestThrashTriggers.test_trigger_a_takes_precedence_where_both_fire` — both
  asserts pin the removed clause (`"**where both fire, trigger (a) wins**"`
  and the `do not queue the retry \(b\) alone would\s+allow` regex), and both
  its `Mutation(...)` entries in `test_mutation_harness.py` (the blocks
  `"**Where both fire, trigger (a) wins**"` and
  `"do not queue the retry (b) alone would\n   allow."`).

**Amend:**
- `TestThrashTriggers.test_third_return_is_a_trigger_and_recommends_replan_or_split`
  — the `"**a third return** — a mis-planned milestone"` anchor changes with
  the explicit-threshold rewording; its registry entry's block string changes
  with it. The `recommend re-plan or split` assert survives but now pins the
  pre-spend branch only.

**Add (each with its own registry entry, anchors copied from shipped bytes):**
- an assert pinning the threshold wording — that (a) fires on the third return
  *and every return after it*;
- an assert pinning the composition clause's disposition half — where both
  fire, no further retry, route through `/milestone-plan`;
- an assert pinning the composition clause's carry half — (b)'s diagnosis and
  escalation offer ride into the routing rather than being discarded;
- two asserts pinning the exhaustion branch, **diagnosis and remedy
  separately** (the M114 T4 lesson: a diagnosis with no remedy is what lets a
  defect recur) — one that a work-log-recorded re-plan/split spends (a)'s
  remedy, one that the chip then composes from escalation-offer / park / drop
  and never a bare retry as the recommended option.

**Doctrine compliance of the guard itself:**
- **§3 (matcher exercised at every rendering)** applies narrowly here: these
  are presence pins on one known file whose rendering is the shipped bytes,
  not detectors sweeping surfaces — the deleted one-surface pin was the §3
  case, and it is out. What §3's spirit still demands is the wrap axis: every
  new multi-word anchor that can cross the file's ~75-column wrap must be
  matched with `\s+` across the break (M105), copied from the shipped bytes,
  never from the draft; and the M104 adjacency sweep must be re-run after the
  edit, because rewriting the block reflows neighboring pinned lines.
- **§7 (silent cells)** does not bite: the guard is a fixed list of positive
  asserts, no corpus loops, no cell that may legitimately be silent. Keep it
  that way — do not reintroduce data-driven control loops here.
- **Counts measured, never assumed:** after the edit, the doctrine-pinning
  assert count must equal the registry-entry count, read out of the files
  (pass-1 F5 was exactly this drifting), and every registered block must red
  on deletion.
- **The module docstring must stop carrying counts.** It has gone stale three
  times in one milestone (G6, G7 recurring as J3, J4) on "four properties" and
  "one `\s+` exception". §6's own remedy — let the list be the count — was
  already applied to the harness comment at G7; apply it to the docstring in
  the same edit: name the properties, state no number of them and no count of
  exceptions.

## Beyond the brief

- **B1. Trigger (b) has the same point-vs-threshold ambiguity as (a).** It
  reads "failing twice"; at M114 pass 3 it was applied at the third mechanism
  ("failed three times, each by a new mechanism of one shape" — pass-3
  record). The reading used was threshold; the wording, like (a)'s, permits
  point. If the (a) rewording ships, spend two words making (b) explicitly
  "twice or more". Not load-bearing today, but this exact ambiguity class just
  cost a review pass.
- **B2. J1's label mismatch resolves for free.** The rule's bullets carry no
  `(a)`/`(b)` labels while the precedence clause uses them (J1, 50). Any
  rewrite of the clause should either label the two trigger bullets or refer
  to them by remedy ("the third-return trigger"); labeling the bullets is
  cheaper and makes the new composition text shorter.
- **B3. A sub-threshold finding that predicts a defect in doctrine the same
  milestone ships deserved a cheaper disposition than "wait until it
  happens".** F4 (60) predicted the pass-3 collision precisely. The 80
  threshold is sound as a general fix-now bar, but a logged finding whose
  subject is a rule the milestone itself is shipping is a special case: the
  marginal cost of resolving it was two sentences at a gate already open.
  Observation only — the scoring policy is out of this brief's scope and I
  make no recommendation to change the threshold.
- **B4. K1 (D-064's false Consequences claim) is confirmed as described and
  explicitly not my question.** Noting only: the superseding-entry correction
  it needs (IP4: append, never edit) is independent of every recommendation
  here and can land in the same milestone without interaction.

## Recommendations

1. **Apply.** Reword trigger (a)'s condition to explicit threshold form — the
   third return and every return after it — keeping per-milestone,
   never-resetting counting verbatim (Q1).
2. **Apply.** Replace the unconditional precedence clause with the scoped
   composition clause: (a) wins the retry question only (no further retry;
   route through `/milestone-plan`); (b)'s diagnosis and its escalation offer
   carry into that routing (Q2).
3. **Apply.** Add the exhaustion branch: when (a) fires with a re-plan/split
   already recorded in the work log, the remedy is no longer re-plan-or-split;
   the routing chip composes from offer-escalation / park-as-`blocked` / drop,
   never a bare retry as the recommended option (Q3).
4. **Reject reverting the precedence clause** — reason: it reinstates a
   collision demonstrated to occur (F4 → pass 3), leaves the post-re-cut case
   unwritten while M114 stands in it, and the D-059 retire-don't-repair
   precedent does not transfer (that mechanism's repair was hazardous and its
   recall carried elsewhere; neither holds here) (Q4).
5. **Apply.** Guard updates per Q5: delete the two precedence asserts and
   their registry entries; amend the third-return anchor; add five asserts
   (threshold, composition disposition, composition carry, exhaustion
   diagnosis, exhaustion remedy), each with its own registry entry; `\s+`
   across any wrapped anchor; re-run the M104 adjacency and M113
   false-coverage sweeps; measure asserts == entries.
6. **Apply.** Strip counts from the guard's module docstring (properties,
   exceptions); let the list be the count (§6), closing the G6/G7/J3/J4
   recurrence class in this file.
7. **Consider.** Reword trigger (b) to "twice or more" and label the two
   trigger bullets `(a)`/`(b)` while the block is open (B1, B2).
8. **Reject a tracking-rules or `cairn_validate` home for any of this** —
   reason: D-064 choices 4 and 6 already decided both, on grounds (single
   surface; judgment-not-mechanics) that these changes do not disturb.

## Binding criteria

- BC1: The thrash rule states trigger (a)'s condition as an explicit
  threshold — it fires on the third return and on every return after it — and
  retains verbatim that returns are counted per milestone, never per cut, with
  a re-cut incrementing and never resetting the count. No wording introduces a
  per-cut window for either the count or the trigger.
- BC2: The clause "Where both fire, trigger (a) wins" and its "do not queue
  the retry (b) alone would allow" sentence are removed from
  `skills/milestone-review/SKILL.md`, and their two asserts and two
  `Mutation(...)` registry entries are removed with them.
- BC3: In their place the rule states that where both triggers fire, trigger
  (a) governs the disposition — no further retry under the current plan; the
  milestone routes through `/milestone-plan` — and trigger (b)'s diagnosis and
  its `/milestone-brief` escalation offer carry into that routing rather than
  being discarded.
- BC4: The rule defines the post-re-cut case: when trigger (a) fires and the
  work log already records a re-plan or split spent on this milestone, the
  prescribed remedy is no longer re-plan-or-split, and the routing chip is
  composed from — an offered `/milestone-brief` escalation, parking as
  `blocked` with the blocker named in a work-log line, or dropping at the
  user's explicit decision — with no bare-retry option as the recommended
  chip option.
- BC5: No wording added by this change makes `/milestone-brief` automatic or
  a standing menu item; every escalation surface remains an offer gated per
  instance (D-004, D-062).
- BC6: `skills/tests/test_thrash_rule.py` pins each clause BC1, BC3, and BC4
  add, with the exhaustion branch's diagnosis and remedy pinned by separate
  asserts; every multi-word anchor that can cross a line wrap is matched with
  `\s+` across the break; each doctrine-pinning assert carries its own
  `Mutation(...)` entry; the doctrine-pinning assert count equals the
  registered entry count, both read out of the files (tolerance: exact), and
  blanking every registered block reds its named test (tolerance: 0
  survivors).
- BC7: The guard's module docstring states no numeric count of pinned
  properties and no numeric count of `\s+` exceptions.
- BC8: On the final tree, the three suites pass from the repo root with exit
  codes checked separately (tolerance: exit 0 each, never piped) and
  `python3 scripts/cairn_validate.py` exits 0.
