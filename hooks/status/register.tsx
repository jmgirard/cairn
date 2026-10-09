import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { CairnBandHidden, CairnStep } from '../../types'
import type { BandLine, Span } from './band'
import { actionsFit, cairnSkill, GAP, GRAY, knownStep, mark, PX_PER_COLUMN, same, stepLines, width } from './band'
import type { PaneButton, PrWord } from './pane'
import {
  CHECK_LABEL,
  CLEAR_LABEL,
  CLEARS_FIRST,
  FINISH_LABEL,
  nextLabel as labelOf,
  NO_ROADMAP,
  paneLines,
  PLAN_LABEL,
  PR_BUTTON,
  prWord,
  REFRESH_LABEL,
  REVISE_LABEL,
  STATUS_LABEL,
} from './pane'
import type { BandState, FileSource, PaneState } from './reader'
import { NO_PANE, readCairn } from './reader'
import { brailleSpans, TRACK_H, TRACK_PX, trackSvg } from './track'

// The milestone band above the prompt (M191, M193 to M201, M206): one row
// for one `in-progress` or `review` ROADMAP row, refreshed when the session
// starts, at the end of each turn, when a cairn skill's prompt is expanded,
// and when a step ends. The row is the bold id and the title, then the flow
// track and its percent (band.ts picks the row and its widths). With no
// active milestone, an idle row names the next workable planned milestone,
// and its `Implement` Button, not a command, starts it (M220). With none
// workable, a found ROADMAP draws the empty row (M213). A press of `Plan`
// or `Implement` runs `/clear`, and its command at the session end that
// the clear brings (M221).
// The track draws as an `Svg` on the desktop and as braille cells in the
// terminal (track.ts). The running cairn skill draws nothing of its own:
// /milestone-review picks the row it shows. A skill's step
// ends at the first main-loop Stop with no background work in flight and no
// one-shot wakeup pending (M210) that no hook
// beneath blocks, or at a prompt the operator types while the session is
// idle, unless a cairn skill's prompt was expanded since the last prompt,
// Stop, or turn end, as a typed cairn slash command's is. A typed prompt
// that a hook beneath drops leaves the step (M210). So the step holds while the skill waits on background work and
// through the turns that the work's notices start (M201). The row sits
// above whatever the hooks beneath draw in the same slot. It ends in a
// close button, which hides the band until the active rows' ids, statuses,
// or order, the row /milestone-review moves the band to, or the idle row's
// id change, or the session ends (M200, M206). A found ROADMAP that cannot
// be read, or is empty, keeps the rows when they came from the same repo
// root (M210), and the close state is compared against them and the
// current step.
//
// The cairn pane (M205) opens from the `/cairn-pane` command, which also
// closes it, or from the band's open button, which a row drawn from a found
// ROADMAP carries beside the close button. It shows the active milestones
// in full and the queue that scripts/cairn_next.py prints (pane.ts), from
// the same refreshes as the band. A head line whose file reads ends with
// the band's percent for its row, so the pane reads the `band` value too
// (M208). While no cairn skill's step is set, the Next line carries a
// Button with the band's next-step label after its pill, and a press runs
// `pressNext`, as the band's does (M218). At the same times, the line
// carries Status after that Button, with Clear before Status while `ended`
// is true, and a press runs `pressStatus` or `pressClear` (M219).
// Each open of the pane, by the command, the band's open button, or the
// session-start reopen, reads the blocked rows' pull request states once
// with `gh`, and so does a press of the Blocked heading's Refresh Button
// (`readPrs`). A blocked line then shows its state word, and a merged,
// changes-requested, or closed line carries a Button for its next step
// (M224).

// Each shape tag names a value's layout; a reload whose value was written
// under another tag reads it as absent. Bump a tag when its type changes.
// The band's value keeps the repo root of the last read, null when no
// ROADMAP was found or the working directory could not be read; the tag
// moved to 4 with the root (M210).
type StoredBand = BandState & { root: string | null }
const BAND_REF = { plugin: 'cairn', key: 'band' } as const
const BAND_SHAPE = 'band-4'
const band = atom(BAND_REF, { rows: [], workable: [], root: null } as StoredBand, { shape: BAND_SHAPE })

// The active ids and statuses, in ROADMAP order, `milestone-review` while
// it moves the band to another row, and the idle row's id while no row is
// active, at the last press of the close button; null while the band shows.
// The tag moved to 4 when the skill's meaning changed (M206 review). The
// press writes through `$.state.set`, which takes the tag with the value and
// a reference written as literals in this file.
const DISMISSED_REF = { plugin: 'cairn', key: 'dismissed' } as const
const DISMISSED_SHAPE = 'dismissed-4'
const dismissed = atom(DISMISSED_REF, null as CairnBandHidden | null, { shape: DISMISSED_SHAPE })

// The running cairn skill, until a main-loop Stop with nothing in flight or
// an idle typed prompt ends it (the `classic.Stop` and `prompt.submit`
// hooks). A typed prompt that finds `expanded` set keeps it; null while no
// cairn skill runs. The chapter it once held went in M206.
const step = atom({ plugin: 'cairn', key: 'step' } as const, null as CairnStep | null, { shape: 'step-2' })

// True from a cairn skill's prompt until the next prompt, Stop, turn end, or
// session end.
// The engine expands a typed slash command before it raises the command's
// prompt, so that prompt finds this set and keeps the step the command just
// started (M201).
const expanded = atom({ plugin: 'cairn', key: 'expanded' } as const, false, { shape: 'expanded-1' })

// True from a main-loop Stop that ends a cairn skill's step until the next
// idle typed prompt that enters, the next cairn skill's prompt, or the
// session's end (M216). While it is true, a row that draws the action
// Buttons carries the Clear Button too, when it has room for it.
const ended = atom({ plugin: 'cairn', key: 'ended' } as const, false, { shape: 'ended-1' })

// What the cairn pane shows, written at each refresh (M205). The tag moved
// to 2 when the state gained the candidate rows (M207), to 3 when it
// gained the blocked rows (M223), and to 4 when each blocked row gained its
// pull request's URL (M224).
const pane = atom({ plugin: 'cairn', key: 'pane' } as const, NO_PANE as PaneState, { shape: 'pane-4' })

// Each blocked row's pull request state word by its URL, written by the
// read at a pane open or a Refresh press (M224). A URL with no entry has
// not been read, and its line shows no word.
const prs = atom({ plugin: 'cairn', key: 'prs' } as const, {} as Record<string, PrWord>, { shape: 'prs-1' })

// The pane's id, its title, and the command that opens and closes it.
const PANE = 'cairn'
const PANE_TITLE = 'cairn'
const PANE_COMMAND = 'cairn-pane'
// The key of the Next line's Button (M218).
const PANE_NEXT = 'cairn-pane-next'
// The store key that holds the project roots whose session ended with reason
// `other` while the pane was open and shown (M222). A typed `/clear` in the
// desktop app ends the process that way, and the next process starts with no
// pane at the first message after the clear, so its `session.start` opens
// the pane again. The key is `$.session.root()`, which a shell `cd` does not
// move, so it matches the folder the next session starts in (M222 review). An app quit or a signal that ends the session with reason
// `other` also brings the pane back at the next session in that folder. The
// API does not say which ends those are, and none was checked live.
const REOPEN_KEY = 'reopen'

// The close button's label. The desktop app draws a dismiss Button in the
// band as its label text, so a long label reads as text there. On the
// desktop the label is `✕`, dim at rest, which the operator picked at a
// live look as closest to the app's own close icon (M197).
const CLOSE_GLYPH = '×'
const DESKTOP_CLOSE_GLYPH = '✕'
// The columns the row's close gap and one-glyph label take on either
// surface, which the row leaves free when it picks its form.
const CLOSE_COLUMNS = GAP + width(CLOSE_GLYPH)
// The open button's one-glyph label and the space after it, which a row
// drawn from a found ROADMAP also leaves free (M205).
const OPEN_GLYPH = '≡'
const OPEN_COLUMNS = width(OPEN_GLYPH) + 1

// The action Buttons (M212): the next step's label, from pane.ts's
// `nextLabel`, which the pane's Next Button reads too (M218), and the status
// Button's command. A plugin skill runs as `cairn:<name>` (M195).
const STATUS_COMMAND = 'cairn:milestone'
// The built-in command the Clear Button runs (M216). The Status and Clear
// labels sit in pane.ts, which the pane's Next line reads too (M219).
const CLEAR_COMMAND = 'clear'
// `CLEARS_FIRST`, the next steps whose Button runs `/clear` first (M221),
// sits in pane.ts beside the label map.
// The key and label of each Button after the Next line's action (M219),
// of the Blocked heading's Refresh, and of a blocked line's Button, whose
// key ends in its milestone id (M224).
const PANE_BUTTONS: Record<PaneButton, { key: string; label: string }> = {
  clear: { key: 'cairn-pane-clear', label: CLEAR_LABEL },
  status: { key: 'cairn-pane-status', label: STATUS_LABEL },
  refresh: { key: 'cairn-pane-refresh', label: REFRESH_LABEL },
  finish: { key: 'cairn-pane-finish', label: FINISH_LABEL },
  revise: { key: 'cairn-pane-revise', label: REVISE_LABEL },
  check: { key: 'cairn-pane-check', label: CHECK_LABEL },
}

// The command each blocked line's Button runs, and whether the milestone's
// id is its argument (M224). None runs `/clear` first, as the Review and
// Resume Buttons keep the conversation.
const BLOCKED_COMMANDS: Partial<Record<PaneButton, { command: string; withId: boolean }>> = {
  finish: { command: 'cairn:milestone-review', withId: true },
  revise: { command: 'cairn:milestone-implement', withId: true },
  check: { command: STATUS_COMMAND, withId: false },
}

// How long one `gh pr view` call may run, well under the ten minutes
// `$.process.run` allows. The calls run side by side, and a call still
// running then rejects and reads as `unknown` (M224).
const GH_TIMEOUT_MS = 15_000

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const result = await next(e)
    await refresh($)
    // The band does not depend on the command: a refused registration
    // leaves the band as the refresh drew it.
    try {
      await $.command.register({ name: PANE_COMMAND, description: 'Open or close the cairn pane' })
    } catch {
      // No `/cairn-pane` in this session. The band's open button still opens the pane.
    }
    // After the registration, so a slow open does not hold `/cairn-pane`
    // back (M222 review).
    await reopen($)
    return result
  })

  // A `/clear` that stays in the same process raises no `session.start`, and
  // the host's state starts empty under the new session id, so the band and
  // an open pane read the files again here (M222).
  on('classic.SessionStart', async ($, e, next) => {
    const result = await next(e)
    if (e.source === 'clear') await refresh($)
    return result
  })

  // `/cairn-pane` closes an open pane, and otherwise reads the files and
  // opens it, or says why it did not (M205 AC1). After the open, it reads
  // the pull request states, so its line comes once they are read (M224).
  // Only a pane the person can see is closed: one that waits undrawn, or
  // sits behind another pane's tab, is opened again instead (M205 review).
  // A hook that refuses the open or the close gives a line, not an error.
  on('command.run', { command: PANE_COMMAND }, async $ => {
    try {
      const mine = (await $.ui.panes()).find(open => open.id === PANE)
      if (mine !== undefined && mine.isPlaced && mine.isShown) {
        await $.ui.close({ id: PANE })
        return { text: 'cairn pane closed' }
      }
      await refresh($)
      if (!(await read($, pane)).found) return { text: NO_ROADMAP }
      const opened = await $.ui.open({ id: PANE, title: PANE_TITLE })
      await readPrs($)
      return { text: opened.isPlaced ? 'cairn pane opened' : notPlaced(opened.reason) }
    } catch (error) {
      return { text: `cairn pane: ${error instanceof Error ? error.message : String(error)}` }
    }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Button, Text } = $.ui.resolve(e)
    // The Next line's Button shows while no cairn skill's step is set
    // (M218). A pane gets no `isWorking` prop, so it also shows during a
    // turn outside a cairn skill, and a press then waits for the session to
    // be idle, as `$.command.run` queues.
    // After that Button, the Next line shows Status at the same times, and
    // Clear before Status while `ended` is true (M219).
    const acts = knownStep(await read($, step)) === null
    const lines = paneLines(await read($, pane), (await read($, band)).rows, acts, await read($, ended), await read($, prs))
    // A line's lead and tail keep their width, and its text takes the room
    // left between them: cut to one line with an ellipsis, or wrapped for
    // the goal's lines. The line Box may shrink below its content's width,
    // so a long text is cut rather than pushing the tail past the edge
    // (M208, LESSONS M194). The action Button sits after them in a Box that
    // does not shrink, so the pill is cut first (M218), and so do Clear and
    // Status after it, each in its own such Box (M219). A Text drops its
    // `key`, so each line's key sits on a Box.
    return (
      <Box key="cairn-pane" flexDirection="column">
        {lines.map(line => (
          <Box key={line.key} paddingLeft={line.indent} minWidth={0}>
            {line.lead.length === 0 ? null : (
              <Box key={`${line.key}-lead`} flexShrink={0}>
                {line.lead.map(span => (
                  <Text wrap="truncate-end" {...style(span)}>
                    {span.text}
                  </Text>
                ))}
              </Box>
            )}
            {line.text === null ? null : (
              <Box key={`${line.key}-text`} flexShrink={1} minWidth={0}>
                <Text wrap={line.wraps ? 'wrap' : 'truncate-end'} {...style(line.text)}>
                  {line.text.text}
                </Text>
              </Box>
            )}
            {line.tail === undefined ? null : (
              <Box key={`${line.key}-tail`} flexShrink={0}>
                {line.tail.map(span => (
                  <Text wrap="truncate-end" {...style(span)}>
                    {span.text}
                  </Text>
                ))}
              </Box>
            )}
            {line.action === undefined ? null : (
              <Box key={`${line.key}-action`} flexShrink={0} marginLeft={1}>
                <Button
                  key={PANE_NEXT}
                  variant="secondary"
                  label={line.action}
                  onPress={() => pressNext($, line.action)}
                />
              </Box>
            )}
            {(line.buttons ?? []).map(kind => {
              const button = PANE_BUTTONS[kind]
              const target = line.target
              return (
                <Box key={`${line.key}-${kind}`} flexShrink={0} marginLeft={1}>
                  <Button
                    key={target === undefined ? button.key : `${button.key}-${target}`}
                    variant="secondary"
                    label={button.label}
                    onPress={() => pressPane($, kind, target)}
                  />
                </Box>
              )
            })}
          </Box>
        ))}
      </Box>
    )
  })

  // A turn end reads the tracking files again and ends no step (M201). A
  // skill that waits on background work ends its turn, and the work's notice
  // starts the next one, so a turn end is not the skill's end.
  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    await update($, expanded, () => false)
    await refresh($)
    return result
  })

  // The main loop's Stop ends the running cairn skill's step when nothing is
  // in flight: `background_tasks` is empty or absent, and no hook beneath
  // blocked the stop (M201). A Stop with work in flight keeps the step
  // through the wait, and so does a blocked Stop, after which the turn goes
  // on. A Stop inside a subagent carries an `agent_id` and keeps the step.
  // A one-shot entry in `session_crons`, as ScheduleWakeup makes, also keeps
  // the step, so a skill that waits on a wakeup keeps it (M210). A recurring
  // cron, as `/loop` makes, does not, since it would keep the step for good.
  on('classic.Stop', async ($, e, next) => {
    const result = await next(e)
    await update($, expanded, () => false)
    if (e.agent_id !== undefined || result?.block !== undefined) return result
    const waking = (e.session_crons ?? []).some(cron => cron.recurring === false)
    if ((e.background_tasks ?? []).length === 0 && !waking) {
      if (knownStep(await read($, step)) !== null) await update($, ended, () => true)
      await update($, step, () => null)
      await refresh($)
    }
    return result
  })

  // A prompt the operator typed, at the terminal or the desktop (`composer`)
  // or through Remote Control (`bridge`), while the session was idle (no
  // `turnId`) ends a step that a Stop kept (M201). A background task's
  // notice, a peer's message, or a prompt typed over a running turn keeps
  // it. A typed cairn slash command keeps the step its own skill prompt set:
  // the engine expands the command first, so the prompt finds `expanded`
  // set. Were the skill prompt to run beneath instead, the step would end
  // before `next` and the skill prompt would set the new one. So the step
  // ends before `next`, and a prompt that a hook beneath drops puts it back,
  // unless something set a new step meanwhile (M210).
  on('prompt.submit', async ($, e, next) => {
    const typed = e.origin.kind === 'composer' || e.origin.kind === 'bridge'
    const fresh = await read($, expanded)
    await update($, expanded, () => false)
    if (!typed || e.turnId !== undefined || fresh) return next(e)
    const before = await read($, step)
    const hiddenBefore = await read($, dismissed)
    const endedBefore = await read($, ended)
    await update($, step, () => null)
    await update($, ended, () => false)
    await refresh($)
    const result = await next(e)
    // The refresh above can clear a hide made against the old step, so a
    // drop puts back the close state as well (M210 review).
    if (result?.drop !== undefined && before !== null) {
      await update($, step, current => current ?? before)
      if (hiddenBefore !== null) await update($, dismissed, current => current ?? hiddenBefore)
      await reconcile($)
    }
    // A drop also puts back the Clear Button that a skill's end left, unless
    // a skill started meanwhile (M216).
    if (result?.drop !== undefined && endedBefore && (await read($, step)) === null) {
      await update($, ended, () => true)
    }
    return result
  })

  // A cairn skill's prompt starts its step, the same skill run again
  // included. The event carries no agent id, so a subagent that loads a
  // cairn skill starts a step too. The text passes through as is.
  on('skill.prompt', async ($, e, next) => {
    const result = await next(e)
    const skill = cairnSkill(e.skill)
    if (skill !== null) {
      await update($, step, () => ({ skill }))
      await update($, ended, () => false)
      await update($, expanded, () => true)
      await refresh($)
    }
    return result
  })

  // A file the session writes under a `cairn/` directory, such as a
  // milestone file whose box was just checked, reads the files again, so the
  // track moves inside a long turn (M206 review: the chapter hook, which
  // M206 removed, had done this at each chapter). The tool's own call goes
  // through first, and a refused or failed call reads nothing.
  on('tool.call', { tool: 'Edit' }, afterWrite)
  on('tool.call', { tool: 'Write' }, afterWrite)
  on('tool.call', { tool: 'MultiEdit' }, afterWrite)

  // Every session end, a `/clear` or a resume among them, ends the step and
  // shows a band that a press hid, whatever its reason (M200).
  on('session.end', async ($, e, next) => {
    // A `Plan` or `Implement` press's held command is taken first, so a
    // rejecting `next(e)` below cannot leave it set (M221 review).
    const queued = heldRun
    heldRun = null
    // An `other` end marks this folder for a reopen at the next start
    // (M222). A `clear` end needs nothing, as no pane closes when the clear
    // stays in the same process.
    if (e.reason === 'other') await markReopen($)
    const result = await next(e)
    await update($, step, () => null)
    await update($, expanded, () => false)
    await update($, dismissed, () => null)
    await update($, ended, () => false)
    // A `/clear` from the Clear Button ends the session, and its run may
    // never settle, so the end frees the action Buttons (M216).
    running = false
    // The held command runs now when this end is its `/clear` (M221). The
    // run is not awaited, so the session end does not wait on the command.
    // It takes the next run number, so the `/clear` run that settles after
    // this end does not free a press made while the command runs. Any other
    // end drops the command, and the prompt box and a toast say so, as for
    // a refused run (M221 review).
    if (queued !== null) {
      if (e.reason === 'clear') void run($, queued.command, queued.args)
      else void fallBack($, lineOf(queued.command, queued.args), 'the session ended before /clear')
    }
    return result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const state = await read($, band)
    const { rows, workable } = state
    const current = knownStep(await read($, step))
    // A row drawn from a found ROADMAP carries the pane's open button
    // (M205), and with no active or workable row it is the empty row (M213).
    const { found: canOpen, next: nextStep } = await read($, pane)
    if (rows.length === 0 && workable.length === 0 && !canOpen) return next(e)
    const hidden = await read($, dismissed)
    if (hidden !== null && same(hidden, mark(state, current))) return next(e)
    const beneath = await next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    // The track draws as the `Svg` element on every surface whose table has
    // one, the desktop app's among them (M204), and as braille cells in the
    // terminal (M206). With the image, the row centers its parts, since the
    // track is taller than text.
    const Svg = e.surface === 'terminal' ? undefined : $.ui.resolve(e).Svg
    const center = Svg === undefined ? {} : { alignItems: 'center' as const }
    const close = CLOSE_COLUMNS + (canOpen ? OPEN_COLUMNS : 0)
    // The next-step and status Buttons (M212) show while no cairn skill's
    // step is set and no turn is working, on a row that has room for them
    // (band.ts `actionsFit`). The track gives up columns to them; without
    // them the row draws its track or label alone, and the idle row draws
    // no command in their place (M220). The next step is the
    // pane's: a milestone's step on a milestone or idle row, and planning
    // on the empty row (M213).
    const nextLabel = nextStep == null ? undefined : labelOf(nextStep.action)
    const canAct = canOpen && nextLabel !== undefined && current === null && e.props.isWorking !== true
    // Each action Button draws with its chrome, so the terminal draws it as
    // `[ label ]`: its label and 4 columns. One space follows each. Both take
    // the `secondary` look: an accent color beside the track's phase colors
    // clashed at a live look.
    // The Clear Button (M216) shows with them after a cairn skill ends, and
    // the row drops it first when the three do not fit.
    const actionColumns = nextLabel === undefined ? 0 : width(nextLabel) + 4 + 1 + width(STATUS_LABEL) + 4 + 1
    const clearColumns = width(CLEAR_LABEL) + 4 + 1
    const tries = !canAct ? [] : (await read($, ended)) ? [actionColumns + clearColumns, actionColumns] : [actionColumns]
    let acts = false
    let clears = false
    let lines: BandLine[] = []
    for (const taken of tries) {
      const reserved = close + taken
      const withActs = stepLines(rows, current, e.props.bodyColumns, reserved, workable, canOpen)
      if (withActs.length > 0 && actionsFit(withActs[0], e.props.bodyColumns, reserved)) {
        acts = true
        clears = taken > actionColumns
        lines = withActs
        break
      }
    }
    if (!acts) lines = stepLines(rows, current, e.props.bodyColumns, close, workable, canOpen)
    const spans = (list: Span[]) =>
      list.map(span => (
        <Text wrap="truncate-end" {...style(span)}>
          {span.text}
        </Text>
      ))
    const track = (line: BandLine) => {
      if (line.track === undefined) return null
      if (Svg === undefined) return spans(brailleSpans(line.track.flow, line.track.columns))
      const px = Math.min(TRACK_PX, line.track.columns * PX_PER_COLUMN)
      return <Svg source={trackSvg(line.track.flow, px)} alt={line.track.flow.alt} width={px} height={TRACK_H} />
    }

    // Two groups: the bold id and the title on the left, where the title
    // gives way first, and the track and the tail on the right, which keep
    // their width. The engine cuts the title to the room that is left.
    // A shrinking Box also takes `minWidth: 0`, and the id sits in a Box
    // that never shrinks. Without both, the desktop app drew a long text at
    // full width past the edge with no `…`, and the short parts beside it
    // shrank to nothing (M194). The empty row has no id, so no head (M213).
    const row = (line: BandLine, isFirst: boolean) => (
      <Box key={line.key} justifyContent="space-between" {...center}>
        <Box key={`${line.key}-left`} flexShrink={1} minWidth={0}>
          {line.id === '' ? null : (
            <Box key={`${line.key}-head`} flexShrink={0}>
              <Text wrap="truncate-end" color={GRAY} bold>
                {line.id}
              </Text>
              <Text wrap="truncate-end">{' '}</Text>
            </Box>
          )}
          <Box key={`${line.key}-text`} flexShrink={1} minWidth={0}>
            <Text wrap="truncate-end" color={GRAY}>
              {line.title}
            </Text>
          </Box>
        </Box>
        <Box key={`${line.key}-right`} flexShrink={0} marginLeft={GAP} {...center}>
          {track(line)}
          {spans(line.tail)}
          {isFirst ? (
            <Text wrap="truncate-end">{' '.repeat(GAP)}</Text>
          ) : null}
          {isFirst && clears ? (
            <Button key="cairn-clear" variant="secondary" label={CLEAR_LABEL} onPress={() => pressClear($)} />
          ) : null}
          {isFirst && clears ? <Text wrap="truncate-end">{' '}</Text> : null}
          {isFirst && acts ? (
            <Button
              key="cairn-next"
              variant="secondary"
              label={nextLabel}
              onPress={() => pressNext($, nextLabel)}
            />
          ) : null}
          {isFirst && acts ? <Text wrap="truncate-end">{' '}</Text> : null}
          {isFirst && acts ? (
            <Button key="cairn-status" variant="secondary" label={STATUS_LABEL} onPress={() => pressStatus($)} />
          ) : null}
          {isFirst && acts ? <Text wrap="truncate-end">{' '}</Text> : null}
          {isFirst && canOpen ? (
            <Button
              key="cairn-open"
              plain
              {...(e.surface === 'terminal' ? {} : { dimColor: true })}
              label={OPEN_GLYPH}
              onPress={() => openPane($)}
            />
          ) : null}
          {isFirst && canOpen ? <Text wrap="truncate-end">{' '.repeat(OPEN_COLUMNS - width(OPEN_GLYPH))}</Text> : null}
          {isFirst ? (
            <Button
              key="cairn-close"
              role="dismiss"
              plain
              {...(e.surface === 'terminal' ? {} : { dimColor: true })}
              label={e.surface === 'terminal' ? CLOSE_GLYPH : DESKTOP_CLOSE_GLYPH}
              onPress={() => dismiss($)}
            />
          ) : null}
        </Box>
      </Box>
    )

    return (
      <Box key="cairn-stack" flexDirection="column">
        <Box key="cairn-band" flexDirection="column">
          {/* A Text drops its `key`, so each row's key sits on a Box. */}
          {lines.map((line, i) => row(line, i === 0))}
        </Box>
        {beneath ?? null}
      </Box>
    )
  })
}

// After an Edit, Write, or MultiEdit call that went through, a path under a
// `cairn/` directory reads the files again.
async function afterWrite($, e, next) {
  const result = await next(e)
  if (result?.deny !== undefined || result?.isError === true) return result
  if (typeof e.file_path === 'string' && /(^|[\\/])cairn[\\/]/.test(e.file_path)) await refresh($)
  return result
}

// The press reads the rows and the step as they are now, not as they were
// drawn. It writes only while the close state stands at the version it had
// before those reads, so a session end that lands between them wins and the
// band stays shown (M210). Any other write in between drops the press too,
// and a second press hides the band.
async function dismiss($) {
  const held = await $.state.get(DISMISSED_REF)
  const state = await read($, band)
  const current = await read($, step)
  await $.state.set(DISMISSED_REF, { shape: DISMISSED_SHAPE, value: mark(state, current) }, { ifVersion: held.version })
}

// A press of the band's open button opens the pane. The press is the
// person's own act, so the surface places the pane at any width.
// A press has no output line, so an open the surface does not place, or one
// a hook refuses, says why in a toast. An open that does not throw reads
// the pull request states (M224).
async function openPane($) {
  try {
    const opened = await $.ui.open({ id: PANE, title: PANE_TITLE })
    if (!opened.isPlaced) $.ui.toast(notPlaced(opened.reason))
  } catch (error) {
    $.ui.toast(`cairn pane: ${error instanceof Error ? error.message : String(error)}`)
    return
  }
  await readPrs($)
}

// True while a read of the pull request states is in flight, so an open or
// a Refresh press made meanwhile starts no second read (M224). A reload
// starts it over as false.
let readingPrs = false

// Reads each blocked row's pull request with one `gh pr view` call per URL,
// side by side, and writes each state word by its URL (M224). The URL
// names the repo, so the call needs no `--repo`. A call that rejects, as
// when `gh` cannot start or outruns its timeout, reads as `unknown`, as a
// bad result does (pane.ts `prWord`), and the read never throws. It runs
// only at a pane open and a Refresh press: no timer and no turn end starts
// one, since the operator does not want repeating tasks.
async function readPrs($) {
  if (readingPrs) return
  readingPrs = true
  try {
    const urls: string[] = []
    for (const row of (await read($, pane)).blocked) {
      if (row.url !== null && !urls.includes(row.url)) urls.push(row.url)
    }
    if (urls.length === 0) return
    const words = await Promise.all(
      urls.map(async url => {
        try {
          const argv = ['gh', 'pr', 'view', url, '--json', 'state,reviewDecision']
          return prWord(await $.process.run(argv, { timeoutMs: GH_TIMEOUT_MS }))
        } catch {
          return prWord(null)
        }
      }),
    )
    const out: Record<string, PrWord> = {}
    urls.forEach((url, i) => {
      out[url] = words[i]
    })
    await update($, prs, () => out)
  } catch {
    // No write: the lines keep the words they had.
  } finally {
    readingPrs = false
  }
}

// A press of a pane Button (M219, M224).
async function pressPane($, kind: PaneButton, target: string | undefined) {
  if (kind === 'clear') return pressClear($)
  if (kind === 'status') return pressStatus($)
  if (kind === 'refresh') return pressRefresh($)
  if (target !== undefined) return pressBlocked($, kind, target)
}

// A press of the Blocked heading's Refresh reads the files and then the
// pull request states again (M224).
async function pressRefresh($) {
  await refresh($)
  await readPrs($)
}

// A press of a blocked line's Button runs its command as a typed command
// would, through the Status Button's path, with no `/clear` first (M224).
// It reads the row's state word as it is now, not as it was drawn, and
// does nothing when that word no longer carries this Button, or while
// another Button's run is in flight.
async function pressBlocked($, kind: PaneButton, id: string) {
  if (busy()) return
  const row = (await read($, pane)).blocked.find(each => each.id === id)
  if (row === undefined || row.url === null) return
  const words = await read($, prs)
  const word = Object.prototype.hasOwnProperty.call(words, row.url) ? words[row.url] : undefined
  const route = BLOCKED_COMMANDS[kind]
  if (word === undefined || PR_BUTTON[word] !== kind || route === undefined) return
  await run($, route.command, route.withId ? id : '')
}

// True while an action Button's run is in flight, so a second press, such
// as a double click, does not queue the command again (M212 review). A
// reload starts it over as false. Each run takes the next number in
// `runs`, and only the latest run clears `running` as it settles, so a run
// from before a session end that settles late does not free a newer run's
// press (M216 review).
let running = false
let runs = 0

// The command a `Plan` or `Implement` press holds from the press until the
// next session end, which runs it when the end's reason is `clear` (M221).
// While it is set, a press does nothing, as while a run is in flight. A
// refused `/clear` drops it. A reload starts it over as null.
let heldRun: { command: string; args: string } | null = null

// A press of the next-step Button reads the next step and the step as they
// are now, not as they were drawn, as the close press does (M212 review). A
// cairn skill that started since the drawing, or no next step, makes the
// press do nothing. A Button drawn for a milestone (`Implement`, `Resume`,
// `Review`) also does nothing when the next step no longer names one, as
// in M212 (M213 review). `Plan` runs the next step as it is now, which is
// planning with no arguments while nothing is workable (M213).
// `Plan` and `Implement` run `/clear` first and hold the command for the
// session end it brings (M221). The press is the person's consent to drop
// the conversation, as a press of Clear is (M216), so it clears only when
// the drawn label is the next step's label as it is now: a `Resume` or
// `Review` drawing whose next step has since become planning or implement
// runs the command and keeps the conversation (M221 review).
async function pressNext($, drawn: string | undefined) {
  if (busy() || knownStep(await read($, step)) !== null) return
  const next = (await read($, pane)).next
  if (next === null) return
  if (next.id === null && drawn !== PLAN_LABEL) return
  const command = `cairn:${next.command.slice(1)}`
  const args = next.id ?? ''
  if (!CLEARS_FIRST.includes(next.action) || drawn !== labelOf(next.action)) {
    await run($, command, args)
    return
  }
  const mine = { command, args }
  heldRun = mine
  if (!(await run($, CLEAR_COMMAND, '')) && heldRun === mine) heldRun = null
}

// True while a run is in flight or a command waits for its `/clear`.
function busy(): boolean {
  return running || heldRun !== null
}

async function pressStatus($) {
  if (busy() || knownStep(await read($, step)) !== null) return
  await run($, STATUS_COMMAND, '')
}

// A press of Clear runs the built-in `/clear` (M216), under the same checks
// as the other action Buttons. It also reads `ended` as it is now, so a
// press of a drawing made before a typed prompt, a skill, or a session end
// cleared it does nothing (M216 review).
async function pressClear($) {
  if (busy() || knownStep(await read($, step)) !== null || !(await read($, ended))) return
  await run($, CLEAR_COMMAND, '')
}

// An action Button's command runs as if the person typed it (M212). A run
// that rejects puts the command line after the prompt box's draft, so the
// person can send it, and a toast says why and names the command line, for
// a box that could not take it. It answers false for a run that rejects.
async function run($, command: string, args: string): Promise<boolean> {
  running = true
  runs += 1
  const mine = runs
  try {
    await $.command.run({ command, args })
    return true
  } catch (error) {
    await fallBack($, lineOf(command, args), error instanceof Error ? error.message : String(error))
    return false
  } finally {
    if (runs === mine) running = false
  }
}

// A command's line as the person would type it.
function lineOf(command: string, args: string): string {
  return args === '' ? `/${command}` : `/${command} ${args}`
}

// Puts a command line that did not run after the prompt box's draft, and
// toasts why (M212). A held command that a session end dropped goes the
// same way (M221 review).
async function fallBack($, text: string, why: string) {
  try {
    await $.prompt.fill({ text, mode: 'append' })
  } catch {
    // A fill that rejects leaves the draft as it was; the toast still
    // names the refusal.
  }
  try {
    await $.ui.toast(`cairn: ${why} (${text})`)
  } catch {
    // No toast shows; the press has nothing else to say.
  }
}

// Marks the session's folder for a reopen when the pane is open and shown
// (M222). A store or pane call that fails marks nothing.
async function markReopen($) {
  try {
    const mine = (await $.ui.panes()).find(open => open.id === PANE)
    if (mine === undefined || !mine.isShown || !mine.isPlaced) return
    const cwd = await $.session.root()
    const held = await reopenList($)
    if (!held.includes(cwd)) await $.store.set(REOPEN_KEY, [...held, cwd])
  } catch {
    // No mark: the next start opens no pane.
  }
}

// At the first start in a marked folder, clears the mark and, when the
// refresh found a ROADMAP, opens the pane (M222). A reopen that is not placed waits
// with no toast, and a refused one gives nothing. An open reads the pull
// request states (M224).
async function reopen($) {
  try {
    const cwd = await $.session.root()
    const held = await reopenList($)
    if (!held.includes(cwd)) return
    await $.store.set(REOPEN_KEY, held.filter(each => each !== cwd))
    if (!(await read($, pane)).found) return
    await $.ui.open({ id: PANE, title: PANE_TITLE })
  } catch {
    // No reopen.
    return
  }
  // The reopen is an open, so it reads the pull request states (M224).
  await readPrs($)
}

async function reopenList($): Promise<string[]> {
  const held = await $.store.get(REOPEN_KEY)
  return Array.isArray(held) ? held.filter((each): each is string => typeof each === 'string') : []
}

function notPlaced(reason: string): string {
  return `cairn pane not placed: ${reason}`
}

// A change to the active ids, statuses, or order, to the running skill, or
// to the idle row's id brings the band back, and it stays until the next
// press. The end of a skill's step is a change to the running skill. The
// decision reads the close state at a version and clears it only at that
// version, so a press made while `reconcile` reads the `band` and `step`
// values is compared, not lost, and it is kept when those reads match it
// (M200, M210 review). A hook that changes the rows or the step before the
// clear can still clear a press made against the new state, because the
// comparison uses the old reads. With nothing to clear, it writes nothing
// (M210).
async function reconcile($) {
  const now = mark(await read($, band), await read($, step))
  for (let tries = 0; tries < 3; tries += 1) {
    const held = await $.state.get(DISMISSED_REF)
    const hidden = held.value !== undefined && held.value.shape === DISMISSED_SHAPE ? held.value.value : null
    if (hidden === null || same(hidden, now)) return
    const done = await $.state.set(DISMISSED_REF, { shape: DISMISSED_SHAPE, value: null }, { ifVersion: held.version })
    if (done.isSet) return
  }
}

// A span's style props, leaving out the ones it does not set.
function style(span: Span) {
  const props: { color?: string; backgroundColor?: string; bold?: boolean } = {}
  if (span.color !== undefined) props.color = span.color
  if (span.backgroundColor !== undefined) props.backgroundColor = span.backgroundColor
  if (span.bold) props.bold = true
  return props
}

// No ROADMAP found empties the band and the pane. A found ROADMAP that
// cannot be read, or whose text is empty or only whitespace, keeps the rows
// and the pane as they were (M200), and so does a throw while parsing it,
// but only when the kept rows came from the same root (M210). A failed read
// in another root, a throw from `$.session.cwd()`, and kept rows with no
// root all empty the band and the pane, so no row from another repo shows.
// The close state is then compared against the rows and the current step.
async function refresh($) {
  let got: { root: string | null; state: { band: BandState; pane: PaneState } | null } | null
  try {
    got = await readCairn(fsSource($))
  } catch {
    got = null
  }
  const root = got === null ? null : got.root
  if (got !== null && got.state !== null) {
    const next = got.state
    await update($, band, () => ({ ...next.band, root }))
    await update($, pane, () => next.pane)
  } else {
    // The keep-or-empty decision and the write stand at one version, so a
    // good read that lands in between is decided again, not overwritten
    // (M210 review). Keeping writes nothing.
    for (let tries = 0; tries < 3; tries += 1) {
      const held = await $.state.get(BAND_REF)
      const kept = held.value !== undefined && held.value.shape === BAND_SHAPE ? held.value.value.root : null
      if (kept !== null && root !== null && kept === root) break
      const empty = { rows: [], workable: [], root }
      const done = await $.state.set(BAND_REF, { shape: BAND_SHAPE, value: empty }, { ifVersion: held.version })
      if (done.isSet) {
        await update($, pane, () => NO_PANE)
        break
      }
    }
  }
  await reconcile($)
}

function fsSource($): FileSource {
  return {
    cwd: () => $.session.cwd(),
    isFile: path => isFile($, path),
    read: path => readText($, path),
    list: path => listNames($, path),
  }
}

async function listNames($, path: string): Promise<string[] | null> {
  try {
    return (await $.fs.list(path)).map(entry => entry.name)
  } catch {
    return null
  }
}

async function isFile($, path: string): Promise<boolean> {
  try {
    return (await $.fs.stat(path)).kind === 'file'
  } catch {
    return false
  }
}

async function readText($, path: string): Promise<string | null> {
  try {
    return await $.fs.read(path)
  } catch {
    return null
  }
}
