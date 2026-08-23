# M66: cairn-init migration gates show the proposal — D-037 wiring extension (done 2026-07-16)

**Goal:** a `/cairn-init` migration chip never asks the user to confirm a
proposal that hasn't appeared in chat (D-038; hit live in the hitop repo:
the step-3 disposition gate fired with no proposal text in chat).

**Outcome:** the acceptance-chips rule enumeration now names "a proposed
disposition or action plan awaiting confirmation" (closing the
proposal-isn't-a-conclusion loophole); migration-protocol step 3 requires
the inventory + per-item dispositions verbatim in chat above the gate chip
(adopt-in-place variant included) and step 7 requires the migration ledger
in chat above the merge-approval chip (PR description alone never carries
it). 3 prose-guards + 5 mutation registrations lock the wording.

**Key decisions:** D-038 — supersedes D-037's cairn-init exclusion via the
extension path D-037 pre-authorized; init's profile/opener/routing chips,
release, hotfix, and design-interview stay unwired (premise holds there).

**Review:** 5/5 criteria, fresh command evidence; suites 211 + 84 OK;
validate all-pass. Fan-out: 1 finding (F1/92 — work-log claimed 6 Mutation
entries, diff adds 5; the M28/M64 stale-count trap) fixed via appended
correction; blame + prior-PR lenses clean.

**PR:** https://github.com/jmgirard/cairn/pull/64 (squash eb56020)
