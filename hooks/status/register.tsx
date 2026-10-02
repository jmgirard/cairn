import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { CairnBandHidden, CairnBandMark, CairnStep } from '../../types'
import type { BandLine, Span } from './band'
import { ARROW, cairnSkill, GAP, GRAY, knownStep, stepLines, width } from './band'
import type { BandRow, FileSource } from './reader'
import { loadBand } from './reader'

// The milestone band above the prompt (M191, M193 to M197): one row for one
// `in-progress` or `review` ROADMAP row, refreshed when the session starts,
// at the end of each turn, when a cairn skill's prompt is expanded, and at
// each chapter the session marks. A running cairn skill shows its label and
// the last chapter on that row, or on a skill row when no milestone is
// active (band.ts picks the row). The row sits above whatever the hooks
// beneath draw in the same slot. It ends in a close button, which hides the
// band until the active rows' ids, statuses, or order, or the running
// skill, change.

// Each shape tag names a value's layout; a reload whose value was written
// under another tag reads it as absent. Bump a tag when its type changes.
const band = atom({ plugin: 'cairn', key: 'band' } as const, [] as BandRow[], { shape: 'band-2' })

// The active ids and statuses, in ROADMAP order, and the running skill, at
// the last press of the close button; null while the band shows.
const dismissed = atom({ plugin: 'cairn', key: 'dismissed' } as const, null as CairnBandHidden | null, {
  shape: 'dismissed-2',
})

// The running cairn skill and the last chapter marked since its prompt was
// expanded; null while no cairn skill runs.
const step = atom({ plugin: 'cairn', key: 'step' } as const, null as CairnStep | null, { shape: 'step-1' })

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

  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    // A subagent's turn ending is not the session's turn ending.
    if (e.agentId === undefined) await refresh($)
    return result
  })

  // A cairn skill's prompt starts its step with no chapter, the same skill
  // run again included. The event carries no agent id, so a subagent that
  // loads a cairn skill starts a step too. The text passes through as is.
  on('skill.prompt', async ($, e, next) => {
    const result = await next(e)
    const skill = cairnSkill(e.skill)
    if (skill !== null) {
      await update($, step, () => ({ skill, chapter: null }))
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

  // Every session end, a `/clear` or a resume among them, ends the step.
  on('session.end', async ($, e, next) => {
    const result = await next(e)
    await update($, step, () => null)
    await reconcile($)
    return result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const rows = await read($, band)
    const current = knownStep(await read($, step))
    if (rows.length === 0 && current === null) return next(e)
    const hidden = await read($, dismissed)
    if (hidden !== null && same(hidden, mark(rows, current))) return next(e)
    const beneath = await next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const lines = stepLines(rows, current, e.props.bodyColumns, CLOSE_COLUMNS)
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
      <Box key={line.key} justifyContent="space-between">
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
        <Box key={`${line.key}-right`} flexShrink={0} marginLeft={GAP}>
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

// The ids and statuses of the active rows, in ROADMAP order, and the
// running skill. The chapter is left out, so a new chapter alone keeps the
// band hidden.
function mark(rows: BandRow[], current: CairnStep | null): CairnBandHidden {
  const marks: CairnBandMark[] = rows.map(row => ({ id: row.id, status: row.status }))
  return { marks, skill: current === null ? null : current.skill }
}

function same(a: CairnBandHidden, b: CairnBandHidden): boolean {
  return (
    a.skill === b.skill &&
    a.marks.length === b.marks.length &&
    a.marks.every((m, i) => m.id === b.marks[i].id && m.status === b.marks[i].status)
  )
}

// The press reads the rows and the step as they are now, not as they were
// drawn.
async function dismiss($) {
  const rows = await read($, band)
  const current = await read($, step)
  await update($, dismissed, () => mark(rows, current))
}

// A change to the active ids, statuses, or order, or to the running skill,
// brings the band back, and it stays until the next press.
async function reconcile($) {
  const hidden = await read($, dismissed)
  if (hidden === null) return
  const now = mark(await read($, band), await read($, step))
  if (!same(hidden, now)) await update($, dismissed, () => null)
}

// A span's style props, leaving out the ones it does not set.
function style(span: Span) {
  const props: { color?: string; bold?: boolean } = {}
  if (span.color !== undefined) props.color = span.color
  if (span.bold) props.bold = true
  return props
}

async function refresh($) {
  let rows: BandRow[] = []
  try {
    rows = await loadBand(fsSource($))
  } catch {
    // No readable working directory or ROADMAP: the band is cleared.
    rows = []
  }
  await update($, band, () => rows)
  await reconcile($)
}

function fsSource($): FileSource {
  return {
    cwd: () => $.session.cwd(),
    isFile: path => isFile($, path),
    read: path => readText($, path),
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
