# impeccable — skill-architecture comparandum (M133)

**Provenance.** Ingested 2026-08-04 by M133 from the local install at
`~/.claude/skills/impeccable` — the install is the source; nothing sits on the
sources shelf. Pagination: —.
Extraction: read directly in full 2026-08-04 — all twelve corpus files read whole in-session, byte counts pinned in the Read corpus section below and re-checkable by AC1's command — observed 2026-08-04.

**Citation.** *impeccable*, a frontend-design skill for Claude Code and
sibling harnesses, version 4.0.4 (frontmatter of the install's SKILL.md),
license Apache 2.0, distributed as `npx impeccable`. No author is named
anywhere in the read corpus.

**Role.** What this page settles: whether a mature, script-heavy skill in an
unrelated domain (frontend design) carries architecture cairn lacks, across
the four mechanism classes cairn has counterparts for — request routing,
self-document loading, drift detection/repair, and hook-finding grading. A
comparandum in the M06 series; nothing numeric traces here. The ~15 design
playbooks and ~100 scripts were deliberately not read (M133 scope).

## Read corpus

Install path `~/.claude/skills/impeccable` · `version: 4.0.4` · read
first-hand 2026-08-04. One path per line with the byte count observed at read
time:

- SKILL.md — 10744 bytes
- reference/routing.md — 2915 bytes
- reference/craft-floor.md — 3811 bytes
- reference/operate.md — 4145 bytes
- reference/doctor.md — 4752 bytes
- reference/hooks.md — 11871 bytes
- reference/init.md — 8777 bytes
- reference/live-setup.md — 7422 bytes
- reference/degraded/asset-producer.md — 10054 bytes
- reference/degraded/documenter.md — 3365 bytes
- reference/degraded/finish-reviewer.md — 9170 bytes
- reference/degraded/manual-edit-applier.md — 7182 bytes

## Architecture in one paragraph

A ~10.7KB always-loaded SKILL.md carries identity, a mode taxonomy, and a
23-command routing table; everything else is loaded conditionally — one
playbook per command, a quality floor loaded only at edit time, setup files
loaded only when a boot script reports their trigger state. Scripts do the
measuring (context resolution, project signals, a rule-based design detector,
a drift doctor); prose does the judging. Four "degraded" prompts are
build-time renderings of subagent definitions for harnesses that cannot
spawn, each opening with a disclosure mandate.

## Findings

1. The no-argument menu is composed from measured, current signals —
   `reference/routing.md:5` runs a signals script plus the local detector and
   leads with 2–3 recommendations, each reason pulled from those signals
   ("Reason over the signals; there is no score to obey",
   `reference/routing.md:7`), never auto-running
   one. cairn's counterpart is the contextual-chip rule: options composed
   from actual session state, and a chip is a user stop.
   Disposition: already-has — `skills/shared/tracking-rules.md:646`
   (contextual chip construction; the never-auto-run invariant is the
   chip-is-a-stop clause).

2. Routing is a classify-first table read before acting — `SKILL.md:43` maps
   every request to exactly one owning playbook, with "Ask once if two
   commands fit" (`SKILL.md:74`) and a stated fallback for requests no
   command owns. cairn's CLAUDE.md section is the same move at repo level.
   Disposition: already-has — `CLAUDE.md:10` (the classify-first router;
   D-009 keeps it routing-only).

3. A boot script injects resolved context under a follow-its-directives
   contract — `SKILL.md:22` runs context.mjs once per session; it decides
   what loads and its output is authoritative ("follow its directives and do
   not rerun it"). cairn's session_context hook injects ROADMAP plus the
   active milestone on the same run-once, output-authoritative shape.
   Disposition: covered-by-D — D-063 (the SessionStart injection and its
   newest-content read-bound).

4. Implement-time doctrine is loaded at the moment of implementation, not at
   session start — `SKILL.md:24` loads the quality floor "immediately before
   editing UI" and forbids loading it for planning-only work;
   `reference/craft-floor.md:3` is written for that moment ("Load this after
   the direction is settled"). cairn's conditional modules already work this
   way (D-031), but the always-read rulebook is read whole at skill fire
   regardless of phase.
   Disposition: candidate — "Phase-gated loading of implement-time doctrine".

5. Drift findings are graded by the action they require, not their badness —
   `reference/doctor.md:27`: "The severity says what should happen, not how
   bad it is" — `auto` applies without asking, `mention` informs, `route`
   names the owning command; and `reference/doctor.md:7` keeps tool-version,
   schema, and truth drift apart so each gets its own remedy path. cairn's
   CHECK-FAIL / advisory-WARN vocabulary grades severity and leaves the
   required action to the reader.
   Disposition: candidate — "Action-graded finding vocabulary".

6. Maintenance never rides along on another task — `SKILL.md:86`: "Never
   repair drift as a side effect of a design task"; findings are reported,
   not acted on, except the `auto` class. cairn's audit frame states the same
   conduct: findings are a judgment, reported and never auto-fixed.
   Disposition: already-has — `skills/shared/tracking-rules.md:207`.

7. A proxy number is reported as what it measures, never asserted as the
   conclusion — `reference/doctor.md:41`: "A commit count is not a
   contradiction … Never assert that DESIGN.md is stale because the number is
   large." cairn states the restraint twice: page age stays a judgment, and
   the cost line is never a finding to act on.
   Disposition: already-has — `skills/shared/tracking-rules.md:890` (and
   `skills/milestone/SKILL.md:79`).

8. Generated artifacts carry a schema version stamp — `reference/init.md:63`
   embeds `impeccable:product-schema 1` in every product record, and
   `reference/init.md:102` reads it to tell a deliberately short record from
   one written before a section existed, so no user re-sits an interview;
   retired sections surface as deprecated and are deleted only on user
   agreement. cairn stamps no version into adopted scaffolds; the idea is
   already banked.
   Disposition: already-has — `cairn/ROADMAP.md:46` (what cairn already
   carries is the banked M24 scaffold-spec version-stamp row — an idea on
   file awaiting its promotion trigger, not a shipped rule; the stamp's
   second job this finding surfaced — distinguishing "short by choice" from
   "predates the section" — was absorbed into that row at M133's review,
   per search-first).

9. Hook findings run in two tiers — `reference/hooks.md:7`: the per-edit
   hook surfaces only "mechanical, unambiguous problems worth interrupting
   an edit for"; the taste tier defers to one deduplicated deep pass on the
   Stop event, and a session with nothing left stops silently. cairn's guard
   nudges (memory_guard, idea_guard) fire unconditionally per event with no
   deferred tier.
   Disposition: candidate — "Deferred second tier for hook nudges".

10. Suppressions descend a narrowest-exception ladder and the hook never
    writes its own — `reference/hooks.md:53`: persist an exception only
    after explicit user confirmation, then value-scoped before rule-in-file
    before whole-rule before whole-file (`reference/hooks.md:57`). cairn has
    no machine-readable suppression store for a ladder to govern: advisories
    are judgments read by one operator, and overrides are logged work-log
    conduct.
    Disposition: not-applicable — an ignore store would be new governing
    apparatus with no shipped-behavior defect behind it (D-090's door).

11. The reviewer anchors on its own inventory of the artifact, never the
    builder's summary — `reference/degraded/finish-reviewer.md:14`:
    inventory the comp "in your own words" before reading the direction
    contract, because "a review anchored on the contract inherits whatever
    the builder's abstraction dropped"; the verdict pass scores only what
    recaptures visibly show, never the parent's narration. This is cairn's
    diagnosed root cause, independently derived: an author verifies a
    description against its generative model rather than the artifact.
    Disposition: covered-by-D — D-067 (the fresh-context reader
    instruments).

12. A review verdict travels verbatim and the parent may not soften it —
    `reference/degraded/finish-reviewer.md:29`: the disposition "is derived,
    never felt", and "The parent reports your disposition word verbatim and
    has no authority to soften it."
    Disposition: covered-by-D — D-037 (acceptance chips show the verdict
    verbatim; a paraphrase never stands in).

13. Verification runs in bounded passes under a ceiling that covers the
    whole cycle — `SKILL.md:18`: one batched inspection, one batch of fixes,
    at most one confirming round, "and stop polishing", because open-ended
    self-QA "burns the user's money doing worse what the finish handoffs do
    better". cairn reached the same rule from measured thrash: per-milestone
    return counting with hard stops.
    Disposition: covered-by-D — D-064 (return counting and the shape-repeat
    trigger; D-097 adds the amendment-return stop).

14. Degraded harnesses get build-time inline renderings of subagent roles,
    each with a disclosure mandate and a turn-ceiling warning —
    `reference/degraded/documenter.md:2` (run the role inline, "disclose the
    substitution in one line"), `reference/degraded/finish-reviewer.md:10`
    (a hard ceiling ends the run without warning, so batch reads and write
    by the midpoint). cairn targets one harness whose Agent tool it
    presumes, and its fan-out's value is reader freshness (D-067), which
    inline role-play in the authoring context cannot preserve; no cairn
    subagent truncation has been observed that the ceiling warning would
    fix.
    Disposition: not-applicable — single-harness by design; the substitution
    would forfeit the property that justifies the spawn.

## Verification

AC1 — every corpus path exists in the install at its recorded byte count
(run from the repo root; reports nothing when clean):

```bash
sed -n '/^## Read corpus/,/^## /p' cairn/references/impeccable.md \
| grep -E '^- .+ — [0-9]+ bytes$' \
| while read -r _ p _ bytes _; do
    f="$HOME/.claude/skills/impeccable/$p"
    if [ ! -f "$f" ]; then echo "ABSENT: $p"; continue; fi
    a=$(wc -c < "$f" | tr -d ' ')
    [ "$a" = "$bytes" ] || echo "MISMATCH: $p recorded $bytes actual $a"
  done
```

AC2 — every numbered finding cites a corpus path, and cites nothing outside
the corpus (citation form: a backticked install path, optionally `:line`):

```bash
python3 - <<'EOF'
import re
text = open("cairn/references/impeccable.md").read()
corpus = re.findall(r'^- (\S+) — \d+ bytes$',
                    text.split("## Read corpus")[1].split("\n## ")[0], re.M)
findings = text.split("## Findings")[1].split("\n## ")[0]
entries = [e for e in re.split(r'\n(?=\d+\.\s)', findings)
           if re.match(r'\d+\.\s', e)]
cite = re.compile(
    r'`((?:SKILL\.md|(?:reference|scripts)/[\w./-]+|[\w.-]+\.mjs))(?::\d+)?`')
for e in entries:
    n = e.split('.')[0]
    hits = cite.findall(e)
    if not hits:
        print(f"NO-CITATION: entry {n}")
    for p in sorted(set(hits)):
        if p not in corpus:
            print(f"NOT-IN-CORPUS: entry {n} cites {p}")
EOF
```

AC3 — every numbered finding carries a well-formed `Disposition:` line:

```bash
python3 - <<'EOF'
import re
text = open("cairn/references/impeccable.md").read()
findings = text.split("## Findings")[1].split("\n## ")[0]
entries = [e for e in re.split(r'\n(?=\d+\.\s)', findings)
           if re.match(r'\d+\.\s', e)]
for e in entries:
    n = e.split('.')[0]
    m = re.search(r'Disposition:\s*(.+)', e)
    if not m:
        print(f"NO-DISPOSITION: entry {n}"); continue
    v = m.group(1).strip()
    tok = next((t for t in ("already-has", "candidate", "covered-by-D",
                            "not-applicable") if v.startswith(t)), None)
    if tok is None:
        print(f"BAD-TOKEN: entry {n}: {v[:40]}"); continue
    if tok != "not-applicable" and not v[len(tok):].strip(" —:"):
        print(f"NO-REFERENCE: entry {n}")
EOF
```

AC4 — every candidate-dispositioned finding has its ROADMAP bullet with the
M133 provenance tail, a sweep sentence, and a falsifying promotion condition:

```bash
python3 - <<'EOF'
import re
page = open("cairn/references/impeccable.md").read()
road = open("cairn/ROADMAP.md").read()
findings = page.split("## Findings")[1].split("\n## ")[0]
phrases = re.findall(r'Disposition:\s*candidate — "([^"]+)"', findings)
tail = "— added 2026-08-04 — M133 (references/impeccable.md)"
bullets = [b for b in road.splitlines()
           if b.startswith("- ") and b.endswith(tail)]
for ph in phrases:
    if not any(b.startswith(f"- {ph}") for b in bullets):
        print(f"BULLET-ABSENT: {ph}")
for b in bullets:
    if "Swept " not in b: print(f"NO-SWEEP: {b[:60]}")
    if "Promote when" not in b: print(f"NO-PROMOTE-WHEN: {b[:60]}")
EOF
```

Recorded outputs: all four commands ran clean (no output) at the page's
commit — 2026-08-04.
