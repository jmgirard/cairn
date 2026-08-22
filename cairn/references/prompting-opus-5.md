# prompting-opus-5 — Anthropic's model-specific prompting guide for Claude Opus 5

**Provenance.** Ingested 2026-07-27 by M120 from
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
— retrieved by the implementing session as raw Markdown (`curl` of the page's
`.md` sibling, HTTP 200, 11,225 bytes), not through a summarizing fetch; the
`docs.claude.com` path under the same slug 302-redirects to this host.
Pagination: — (a single unpaginated web page; values below anchor on its `##`
section headings).
Extraction: verified 2026-07-27 — full page read directly from the source Markdown; every value quoted below re-read against it — observed 2026-07-27. Re-verified 2026-08-22 (M152): full page re-fetched (`curl` of the `.md` sibling, 12,483 bytes) and re-read whole; every previously extracted value found verbatim, no drift; the § Response length and verbosity and § User-facing progress updates values below extracted in this pass — observed 2026-08-22.

**Citation.** Anthropic. *Prompting Claude Opus 5*. Claude Platform Docs,
`build-with-claude/prompt-engineering/prompting-claude-opus-5`. Subtitle as
printed: "Behavioral differences and prompting patterns for Claude Opus 5,
covering response verbosity, agentic narration, task scoping, subagent
delegation, self-correction, and output artifacts when thinking is disabled."
No author, date, or version is printed on the page.

**Role.** cairn's skills and rulebook are prompts executed by Claude Opus 5
(the orchestrator tier, `tracking-rules.md` "Model and agent strategy"), so
this guide is first-party evidence about how that model reads them. It is here
to settle three conduct questions cairn had no rule for — when a chat
correction is worth narrating, when work warrants a subagent, and whether a
reviewer should filter its own findings before reporting — and to back two
ROADMAP candidate rows it cannot reach today. It is a guidance source, not a
numeric one: nothing here is an oracle.

## Extracted values

Every value carries its `##` section anchor. Values that must be exact are
quoted verbatim, in quotation marks, rather than paraphrased:

- Reviewers instructed to filter report less — "If your review prompt says
  'only report high-severity issues' or 'be conservative,' the model may follow
  that instruction literally and report less; ask it to report everything and
  filter in a separate pass instead." — § Capability improvements, "Code review
  and bug-finding".
- Review accuracy holds at lower effort — "Accuracy holds at lower effort
  settings, which supports a fast pass at review time and a more thorough pass
  later." — § Capability improvements, "Code review and bug-finding".
- Effort is the primary cost control — "use `low` and `medium` liberally as
  your primary control for token cost and response time wherever quality holds,
  and step up to `xhigh` for demanding coding and agentic work" — § Capability
  improvements, "Efficiency at lower effort".
- Cap delegation when cost-sensitive — "For cost-sensitive workloads, cap
  delegation" — § Capability improvements, "Multi-agent coordination".
- The delegation-warrant instruction, quoted whole as the guide's own sample
  prompt — "Delegate to a subagent only for large tasks that are genuinely
  independent and parallelizable, such as a wide multi-file investigation. Do
  not delegate work you can finish yourself in a handful of tool calls, and do
  not use subagents to verify or double-check your own work. If one subagent
  can complete the task, use one rather than several, and keep spawn counts
  low." — § Controlling subagent spawning.
- The behavior the correction-narration instruction answers — "The model also
  narrates corrections to its earlier statements more than prior models do,
  which can be undesirable in user-facing products." — § Self-correction.
- The behavior the delegation instruction answers — "Claude Opus 5 delegates to
  subagents more readily than prior models." — § Controlling subagent spawning.
- The correction-narration instruction, quoted whole as the guide's own sample
  prompt — "Only correct an earlier statement when the error would change the
  user's code, conclusions, or decisions. State corrections plainly and
  briefly, then continue the task. For slips that change nothing for the user,
  make the fix and move on without noting it." — § Self-correction.
- Self-verification instructions cause over-verification — "If your prompt
  contains explicit verification instructions ('include a final verification
  step for any non-trivial task,' 'use a subagent to verify'), remove them:
  instructions like these cause over-verification on Claude Opus 5, and
  removing them reduces wasted tokens with no loss in quality. The same applies
  to legacy harness scaffolding that adds separate verification steps." —
  § Task scope and over-verification. The stated mechanism is the model's own:
  "Claude Opus 5 verifies its own work without being told to."
- Responses run long by default, and effort does not shorten them — "Claude
  Opus 5's default user-facing responses run longer than prior Opus models'"
  and "lowering effort can reduce thinking volume without reliably shortening
  the visible response. To control response length, prompt for it explicitly."
  — § Response length and verbosity.
- The conciseness instruction, quoted whole as the guide's own sample prompt —
  "Keep responses focused, brief, and concise. Keep disclaimers and caveats
  short, and spend most of the response on the main answer. When asked to
  explain something, give a high-level summary unless an in-depth explanation
  is specifically requested." — § Response length and verbosity.
- The narration-cadence instruction, quoted whole as the guide's own sample
  prompt — "Before your first tool call, say in one sentence what you're about
  to do. While working, give a brief update only when you find something
  important or change direction. When you finish, lead with the outcome: your
  first sentence should answer 'what happened' or 'what did you find,' with
  supporting detail after it for readers who want it." — § User-facing
  progress updates.
- Positive examples beat prohibitions for style steering — "Positive examples
  of the communication style you want tend to be more effective than
  instructions about what not to do." — § User-facing progress updates.
- Written deliverables run long — "files that Claude Opus 5 writes to disk
  (reports, Markdown documents, summaries) are often longer than on prior
  models", with the remedy "Match the length of written documents to what the
  task needs: cover the substance, but do not pad with filler sections,
  redundant summaries, or boilerplate." — § Written deliverable length.

## Traces to

What in the repo reads this page: tests, oracle-registry entries, vignette or
documentation claims, other `references/` pages. This is the list a corrector
walks when a value here changes, so name specific files and lines, not areas.

- `skills/shared/tracking-rules.md` — the "Correct what matters, and only
  narrate that" bullet, in Output & interaction discipline. Takes the § Self-correction
  instruction: correct only what would change the user's code, conclusions, or
  decisions. Guarded by `skills/tests/test_narration_discipline.py:58`
  (`TestCorrectionNarrationRule`), four asserts, four mutation entries.
- `skills/shared/tracking-rules.md` — the "Delegate only what warrants it"
  bullet, in Model and agent strategy. Takes the § Controlling subagent spawning
  instruction: nothing finishable in a handful of tool calls is delegated, and
  one subagent rather than several. Guarded by
  `skills/tests/test_delegation_warrant.py:44` (`TestDelegationWarrantRule`),
  three asserts, three mutation entries. cairn does **not** take that
  instruction's third clause ("do not use subagents to verify or double-check
  your own work") — M121 owns it.
- `skills/shared/tracking-rules.md` — the "Plain style" bullet, in Output &
  interaction discipline (M152). Takes the § Response length and verbosity
  finding: length is prompted for explicitly, the main answer carries the
  response, caveats stay short. The jargon and filler clauses are cairn's own,
  beyond what the guide states.
- `skills/shared/tracking-rules.md` — the "Records are written plain" bullet,
  in Universal tracking rules (M152). Takes the § Written deliverable length
  remedy (length matched to what the task needs, no filler or boilerplate),
  applied to cairn's durable records; the no-characterizations clause is the
  M114 lesson's standard, not the guide's.
- `skills/milestone-review/SKILL.md:178` — step 5's reviewer instruction, now
  report-everything-filter-nothing. Takes the § Capability improvements finding
  that a reviewer told to be conservative reports less. Recorded as
  `cairn/DECISIONS.md` D-078; guarded by
  `skills/tests/test_review_fanout.py:123`.
- `skills/milestone-review/SKILL.md:198` — the false-positive taxonomy, now
  inside the `[S]` scorer's rubric blockquote rather than the reviewers'
  instruction; the downstream half of the same finding. Guarded by
  `skills/tests/test_review_fanout.py:97`.
- `cairn/ROADMAP.md` — the §8 description-layer candidate row cites this page's
  § Written deliverable length finding as third-party corroboration and as a
  third disposition; it changes no promotion condition.

## Open questions

Claims about the *repo's own state* — what is on the shelf, what has not been
read, what a later task must still check — are dated observations, not
standing facts. Each carries `— observed YYYY-MM-DD` inline, and is re-checked
before the milestone merges.

- The page prints no version or last-updated date, so a later re-verification
  can detect drift only by re-reading the whole page — observed 2026-07-27.
- The guide's linked companion pages (`Effort`, `What's new in Claude Opus 5`,
  the migration guide) are not ingested; the effort recommendations quoted
  above are taken from this page's own summary of them, and the `Effort` page
  is the fuller source a spawn-effort milestone would owe a page to —
  observed 2026-07-27.
- The over-verification finding is extracted here but not acted on by M120;
  M121 owns its triage — observed 2026-07-27.
