import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { CairnBandHidden, CairnStep } from '../../types'
import type { BandLine, Span } from './band'
import { cairnSkill, GAP, GRAY, knownStep, mark, PX_PER_COLUMN, same, stepLines, width } from './band'
import { NO_ROADMAP, paneLines } from './pane'
import type { BandState, FileSource, PaneState } from './reader'
import { loadCairn, NO_PANE } from './reader'
import { brailleSpans, TRACK_H, TRACK_PX, trackSvg } from './track'

// The milestone band above the prompt (M191, M193 to M201, M206): one row
// for one `in-progress` or `review` ROADMAP row, refreshed when the session
// starts, at the end of each turn, when a cairn skill's prompt is expanded,
// and when a step ends. The row is the bold id and the title, then the flow
// track and its percent (band.ts picks the row and its widths). With no
// active milestone, an idle row names the next workable planned milestone.
// The track draws as an `Svg` on the desktop and as braille cells in the
// terminal (track.ts). The running cairn skill draws nothing of its own:
// /milestone-review picks the row it shows. A skill's step
// ends at the first main-loop Stop with no background work in flight that no hook
// beneath blocks, or at a prompt the operator types while the session is
// idle, unless a cairn skill's prompt was expanded since the last prompt,
// Stop, or turn end, as a typed cairn slash command's is. So the step holds while the skill waits on background work and
// through the turns that the work's notices start (M201). The row sits
// above whatever the hooks beneath draw in the same slot. It ends in a
// close button, which hides the band until the active rows' ids, statuses,
// or order, the row /milestone-review moves the band to, or the idle row's
// id change, or the session ends (M200, M206). A found ROADMAP that cannot be read keeps the rows, and the
// close state is compared against them and the current step.
//
// The cairn pane (M205) opens from the `/cairn-pane` command, which also
// closes it, or from the band's open button, which a row drawn from a found
// ROADMAP carries beside the close button. It shows the active milestones
// in full and the queue that scripts/cairn_next.py prints (pane.ts), from
// the same refreshes as the band. A head line whose file reads ends with
// the band's percent for its row, so the pane reads the `band` value too
// (M208).

// Each shape tag names a value's layout; a reload whose value was written
// under another tag reads it as absent. Bump a tag when its type changes.
const band = atom({ plugin: 'cairn', key: 'band' } as const, { rows: [], workable: [] } as BandState, {
  shape: 'band-3',
})

// The active ids and statuses, in ROADMAP order, `milestone-review` while
// it moves the band to another row, and the idle row's id while no row is
// active, at the last press of the close button; null while the band shows.
// The tag moved to 4 when the skill's meaning changed (M206 review).
const dismissed = atom({ plugin: 'cairn', key: 'dismissed' } as const, null as CairnBandHidden | null, {
  shape: 'dismissed-4',
})

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

// What the cairn pane shows, written at each refresh (M205). The tag moved
// to 2 when the state gained the candidate rows (M207).
const pane = atom({ plugin: 'cairn', key: 'pane' } as const, NO_PANE as PaneState, { shape: 'pane-2' })

// The pane's id, its title, and the command that opens and closes it.
const PANE = 'cairn'
const PANE_TITLE = 'cairn'
const PANE_COMMAND = 'cairn-pane'

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
    return result
  })

  // `/cairn-pane` closes an open pane, and otherwise reads the files and
  // opens it, or says why it did not (M205 AC1).
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
      return { text: opened.isPlaced ? 'cairn pane opened' : notPlaced(opened.reason) }
    } catch (error) {
      return { text: `cairn pane: ${error instanceof Error ? error.message : String(error)}` }
    }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const lines = paneLines(await read($, pane), (await read($, band)).rows)
    // A line's lead and tail keep their width, and its text takes the room
    // left between them: cut to one line with an ellipsis, or wrapped for
    // the goal's lines. The line Box may shrink below its content's width,
    // so a long text is cut rather than pushing the tail past the edge
    // (M208, LESSONS M194). A Text drops its `key`, so each line's key sits
    // on a Box.
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
  // A skill that waits through ScheduleWakeup or a cron lists nothing here,
  // so its step ends at that Stop.
  on('classic.Stop', async ($, e, next) => {
    const result = await next(e)
    await update($, expanded, () => false)
    if (e.agent_id !== undefined || result?.block !== undefined) return result
    if ((e.background_tasks ?? []).length === 0) {
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
  // before `next` and the skill prompt would set the new one. A prompt that
  // a hook beneath blocks or drops has already ended the step.
  on('prompt.submit', async ($, e, next) => {
    const typed = e.origin.kind === 'composer' || e.origin.kind === 'bridge'
    const fresh = await read($, expanded)
    await update($, expanded, () => false)
    if (typed && e.turnId === undefined && !fresh) {
      await update($, step, () => null)
      await refresh($)
    }
    return next(e)
  })

  // A cairn skill's prompt starts its step, the same skill run again
  // included. The event carries no agent id, so a subagent that loads a
  // cairn skill starts a step too. The text passes through as is.
  on('skill.prompt', async ($, e, next) => {
    const result = await next(e)
    const skill = cairnSkill(e.skill)
    if (skill !== null) {
      await update($, step, () => ({ skill }))
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
    const result = await next(e)
    await update($, step, () => null)
    await update($, expanded, () => false)
    await update($, dismissed, () => null)
    return result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const state = await read($, band)
    const { rows, workable } = state
    const current = knownStep(await read($, step))
    if (rows.length === 0 && workable.length === 0) return next(e)
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
    // A row drawn from a found ROADMAP carries the pane's open button (M205).
    const canOpen = (await read($, pane)).found
    const close = CLOSE_COLUMNS + (canOpen ? OPEN_COLUMNS : 0)
    const lines = stepLines(rows, current, e.props.bodyColumns, close, workable)
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
    // shrank to nothing (M194).
    const row = (line: BandLine, isFirst: boolean) => (
      <Box key={line.key} justifyContent="space-between" {...center}>
        <Box key={`${line.key}-left`} flexShrink={1} minWidth={0}>
          <Box key={`${line.key}-head`} flexShrink={0}>
            <Text wrap="truncate-end" color={GRAY} bold>
              {line.id}
            </Text>
            <Text wrap="truncate-end">{' '}</Text>
          </Box>
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
// drawn.
async function dismiss($) {
  const state = await read($, band)
  const current = await read($, step)
  await update($, dismissed, () => mark(state, current))
}

// A press of the band's open button opens the pane. The press is the
// person's own act, so the surface places the pane at any width.
// A press has no output line, so an open the surface does not place, or one
// a hook refuses, says why in a toast.
async function openPane($) {
  try {
    const opened = await $.ui.open({ id: PANE, title: PANE_TITLE })
    if (!opened.isPlaced) $.ui.toast(notPlaced(opened.reason))
  } catch (error) {
    $.ui.toast(`cairn pane: ${error instanceof Error ? error.message : String(error)}`)
  }
}

function notPlaced(reason: string): string {
  return `cairn pane not placed: ${reason}`
}

// A change to the active ids, statuses, or order, to the running skill, or
// to the idle row's id brings the band back, and it stays until the next
// press. The end of a skill's step is a change to the running skill. The
// decision reads the close state inside the update, so a press made while
// `reconcile` reads the `band` and `step` values is compared, not lost, and
// it is kept when those reads match it (M200). A hook that changes the rows
// or the step before the update can still clear a press made against the
// new state, because the comparison uses the old reads.
async function reconcile($) {
  const now = mark(await read($, band), await read($, step))
  await update($, dismissed, hidden => (hidden !== null && !same(hidden, now) ? null : hidden))
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
// cannot be read keeps the rows and the pane as they were (M200). Any throw from `loadCairn`, its
// parsing included, keeps them too. Of the calls `fsSource` makes, only
// `$.session.cwd()` is not caught. The close state is then compared
// against the kept rows and the current step.
async function refresh($) {
  let state: { band: BandState; pane: PaneState } | null = null
  try {
    state = await loadCairn(fsSource($))
  } catch {
    state = null
  }
  if (state !== null) {
    const next = state
    await update($, band, () => next.band)
    await update($, pane, () => next.pane)
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
