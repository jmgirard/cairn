import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { CairnBandHidden, CairnStep } from '../../types'
import type { BandLine, Span } from './band'
import { ARROW, cairnSkill, GAP, GRAY, knownStep, mark, same, stepLines, width } from './band'
import type { BandState, FileSource } from './reader'
import { loadBand } from './reader'
import { TRACK_H, TRACK_PX, trackSvg } from './track'

// The milestone band above the prompt (M191, M193 to M201): one row for one
// `in-progress` or `review` ROADMAP row, refreshed when the session starts,
// at the end of each turn, when a cairn skill's prompt is expanded, at each
// chapter the session marks, and when a step ends. A running cairn skill
// shows its label and the last chapter on that row, or on a skill row when
// no milestone is active. With neither, an idle row names the next workable
// planned milestone (band.ts picks the row). On the desktop, a row with
// room draws the flow track as an `Svg` (track.ts, M204). A skill's step
// ends at the first main-loop Stop with no background work in flight that no hook
// beneath blocks, or at a prompt the operator types while the session is
// idle, unless a cairn skill's prompt was expanded since the last prompt,
// Stop, or turn end, as a typed cairn slash command's is. So the label holds while the skill waits on background work and
// through the turns that the work's notices start (M201). The row sits
// above whatever the hooks beneath draw in the same slot. It ends in a
// close button, which hides the band until the active rows' ids, statuses,
// or order, the running skill, or the idle row's id change, or the session
// ends (M200). A found ROADMAP that cannot be read keeps the rows, and the
// close state is compared against them and the current step.

// Each shape tag names a value's layout; a reload whose value was written
// under another tag reads it as absent. Bump a tag when its type changes.
const band = atom({ plugin: 'cairn', key: 'band' } as const, { rows: [], workable: [] } as BandState, {
  shape: 'band-3',
})

// The active ids and statuses, in ROADMAP order, the running skill, and the
// idle row's id, at the last press of the close button; null while the band
// shows.
const dismissed = atom({ plugin: 'cairn', key: 'dismissed' } as const, null as CairnBandHidden | null, {
  shape: 'dismissed-3',
})

// The running cairn skill and the last chapter marked since its prompt was
// expanded, until a main-loop Stop with nothing in flight or an idle typed
// prompt ends it (the `classic.Stop` and `prompt.submit` hooks). A typed
// prompt that finds `expanded` set keeps it; null while no cairn skill runs.
const step = atom({ plugin: 'cairn', key: 'step' } as const, null as CairnStep | null, { shape: 'step-1' })

// True from a cairn skill's prompt until the next prompt, Stop, turn end, or
// session end.
// The engine expands a typed slash command before it raises the command's
// prompt, so that prompt finds this set and keeps the step the command just
// started (M201).
const expanded = atom({ plugin: 'cairn', key: 'expanded' } as const, false, { shape: 'expanded-1' })

// The desktop app's chapter tool. In a session without it, such as one in
// the terminal, the chapter stays null.
const CHAPTER_TOOL = 'mcp__ccd_session__mark_chapter'

// The close button's label. The desktop app draws a dismiss Button in the
// band as its label text, so a long label reads as text there. On the
// desktop the label is `✕`, dim at rest, which the operator picked at a
// live look as closest to the app's own close icon (M197).
const CLOSE_GLYPH = '×'
const DESKTOP_CLOSE_GLYPH = '✕'
// The columns the row's close gap and one-glyph label take on either
// surface, which the row leaves free when it picks its form.
const CLOSE_COLUMNS = GAP + width(CLOSE_GLYPH)

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const result = await next(e)
    await refresh($)
    return result
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

  // A cairn skill's prompt starts its step with no chapter, the same skill
  // run again included. The event carries no agent id, so a subagent that
  // loads a cairn skill starts a step too. The text passes through as is.
  on('skill.prompt', async ($, e, next) => {
    const result = await next(e)
    const skill = cairnSkill(e.skill)
    if (skill !== null) {
      await update($, step, () => ({ skill, chapter: null }))
      await update($, expanded, () => true)
      await refresh($)
    }
    return result
  })

  // A chapter the main loop marks becomes the step's chapter once the call
  // went through, while a cairn skill runs, and the tracking files are read
  // again. An empty title sets no chapter.
  on('tool.call', { tool: CHAPTER_TOOL }, async ($, e, next) => {
    const result = await next(e)
    if (e.agentId !== undefined || result?.deny !== undefined || result?.isError === true) return result
    const title = typeof e.title === 'string' && e.title !== '' ? e.title : null
    if (title !== null) await update($, step, current => (current === null ? null : { ...current, chapter: title }))
    await refresh($)
    return result
  })

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
    if (rows.length === 0 && current === null && workable.length === 0) return next(e)
    const hidden = await read($, dismissed)
    if (hidden !== null && same(hidden, mark(state, current))) return next(e)
    const beneath = await next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    // The track draws on the desktop alone, as its `Svg` element (M204).
    // There the row centers its parts, since the track is taller than text.
    const Svg = e.surface === 'desktop' ? $.ui.resolve(e).Svg : undefined
    const center = Svg === undefined ? {} : { alignItems: 'center' as const }
    const lines = stepLines(rows, current, e.props.bodyColumns, CLOSE_COLUMNS, workable, Svg !== undefined)
    const spans = (list: Span[]) =>
      list.map(span => (
        <Text wrap="truncate-end" {...style(span)}>
          {span.text}
        </Text>
      ))

    // Two groups: the phase, id, and text on the left, which give way first,
    // and the bar and counts or the state label on the right, which keep
    // their width. The engine cuts the text to the room that is left.
    // A shrinking Box also takes `minWidth: 0`, and the short parts sit in a
    // Box that never shrinks. Without both, the desktop app drew a long text
    // at full width past the edge with no `…`, and the arrow and label
    // beside it shrank to nothing. A step's arrow, its positional label, and
    // the text draw in the theme's gray with no dimColor, the label bold.
    const row = (line: BandLine, isFirst: boolean) => (
      <Box key={line.key} justifyContent="space-between" {...center}>
        <Box key={`${line.key}-left`} flexShrink={1} minWidth={0}>
          <Box key={`${line.key}-head`} flexShrink={0}>
            {spans(line.head)}
            {line.body?.kind === 'step' ? (
              <Text wrap="truncate-end" color={GRAY}>
                {ARROW}
              </Text>
            ) : null}
            {line.body?.kind === 'step' && line.body.label !== null ? (
              <Text wrap="truncate-end" color={GRAY} bold>
                {line.body.label}
              </Text>
            ) : null}
          </Box>
          {line.body === null ? null : (
            <Box key={`${line.key}-text`} flexShrink={1} minWidth={0}>
              <Text wrap="truncate-end" color={GRAY}>
                {line.body.kind === 'title' ? line.body.title : line.body.rest}
              </Text>
            </Box>
          )}
        </Box>
        <Box key={`${line.key}-right`} flexShrink={0} marginLeft={GAP} {...center}>
          {line.track !== undefined && Svg !== undefined ? (
            <Svg source={trackSvg(line.track)} alt={line.track.alt} width={TRACK_PX} height={TRACK_H} />
          ) : null}
          {spans(line.tail)}
          {isFirst ? (
            <Text wrap="truncate-end">{' '.repeat(GAP)}</Text>
          ) : null}
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

// The press reads the rows and the step as they are now, not as they were
// drawn.
async function dismiss($) {
  const state = await read($, band)
  const current = await read($, step)
  await update($, dismissed, () => mark(state, current))
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
  const props: { color?: string; bold?: boolean } = {}
  if (span.color !== undefined) props.color = span.color
  if (span.bold) props.bold = true
  return props
}

// No ROADMAP found empties the band. A found ROADMAP that cannot be read
// keeps the rows as they were (M200). Any throw from `loadBand`, its
// parsing included, keeps them too. Of the calls `fsSource` makes, only
// `$.session.cwd()` is not caught. The close state is then compared
// against the kept rows and the current step.
async function refresh($) {
  let state: BandState | null = null
  try {
    state = await loadBand(fsSource($))
  } catch {
    state = null
  }
  if (state !== null) {
    const next = state
    await update($, band, () => next)
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
