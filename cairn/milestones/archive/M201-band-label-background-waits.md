# M201: A band label that holds through background waits

**Status:** done (2026-10-03, PR #208 https://github.com/jmgirard/cairn/pull/208)

**Goal:** Keep a cairn skill's label on the band while the skill waits on background work and through the turns that the work's notices start.

**Outcome:** `register.tsx` ends a skill's step at a main-loop `classic.Stop` whose `background_tasks` is empty or absent and that no hook beneath blocks, or at an idle `composer` or `bridge` prompt. A `turn.complete` now only refreshes. A new `expanded` state value, set by a cairn `skill.prompt` and cleared at every Stop, turn end, prompt, and session end, lets a typed cairn slash command keep its own label, because the engine expands the command before it raises the prompt. The live look found that order, and AC2 was amended for it. The live look also showed that an Esc interrupt raises no Stop, so the label stays until the next typed prompt or the next Stop with nothing in flight. README, CHANGELOG, and DESIGN state the rule and three limits: ScheduleWakeup and cron waits, background work that the skill did not start, and a prompt that a hook drops. Mod tests went from 615 to 632.

**Decisions:** The plan gate chose the Stop rule over a typed-prompt-only end and a restore at a notice, and chose the idle typed-prompt end over a Stop-only end. The amendment gate chose the `expanded` mark over matching command text. The falsifiers are in the milestone file's work log, which git holds.

**Review:** Three lenses with 27 findings. Five were fixed at the gate, among them an AC5 comment gap the operator fixed in place of a return. Five went to DESIGN Known issues as accepted limitations, and the rest were rejected or noted with reasons. Live looks were driven from a second session by peer messages and `stop_session`, with debug lines written to a file. One lesson was added.
