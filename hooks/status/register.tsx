import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { CairnBandHidden, CairnBandMark, CairnStep } from '../../types'
import type { HeaderLine, ItemLine, Span } from './band'
import { cairnSkill, GAP, knownStep, stepLines } from './band'
import type { BandRow, FileSource } from './reader'
import { loadBand } from './reader'

// The milestone band above the prompt (M191, M193, M194, M195): a header
// row per `in-progress` or `review` ROADMAP row, and an item row under it,
// refreshed when the session starts, at the end of each turn, when a cairn
// skill's prompt is expanded, and at each chapter the session marks. A
// running cairn skill shows its label and the last chapter, on the
// milestone row of its phase or on a skill row of its own. The rows sit
// above whatever the hooks beneath draw in the same slot. The first header
// row ends in a close button, which hides the band until the active rows'
// ids, statuses, or order, or the running skill, change.

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

// The close button's label on every surface. The desktop app draws a
// dismiss Button in the band as its label text, so a long label reads as
// text there.
const CLOSE_GLYPH = '×'

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
    const lines = stepLines(rows, current, e.props.bodyColumns)
    const spans = (list: Span[]) =>
      list.map(span => (
        <Text wrap="truncate-end" {...style(span)}>
          {span.text}
        </Text>
      ))

    // Two groups: the phase, id and title on the left, which give way first,
    // and the bar and counts or the state label on the right, which keep
    // their width. The engine cuts the title to the room that is left.
    // A shrinking Box also takes `minWidth: 0`, and the short parts sit in a
    // Box that never shrinks. Without both, the desktop app drew an item
    // row's long text at full width past the edge with no `…`, and its
    // arrow and label shrank to nothing.
    const header = (line: HeaderLine, isFirst: boolean) => (
      <Box key={line.key} justifyContent="space-between">
        <Box key={`${line.key}-left`} flexShrink={1} minWidth={0}>
          <Box key={`${line.key}-head`} flexShrink={0}>
            {spans(line.head)}
          </Box>
          <Box key={`${line.key}-title`} flexShrink={1} minWidth={0}>
            <Text wrap="truncate-end">{line.title}</Text>
          </Box>
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
              label={CLOSE_GLYPH}
              onPress={() => dismiss($)}
            />
          ) : null}
        </Box>
      </Box>
    )

    // The positional label draws bold and at full strength, with no
    // dimColor; the rest of the row is dim. The arrow and label keep their
    // width, and the rest gives way, as the title does. With the arrow,
    // label, and rest nested in one Text, the desktop drew the rest as a
    // bare `…`.
    const item = (line: ItemLine) => (
      <Box key={line.key}>
        <Box key={`${line.key}-label`} flexShrink={0}>
          <Text wrap="truncate-end" dimColor>
            {line.arrow}
          </Text>
          {line.label === null ? null : (
            <Text wrap="truncate-end" bold>
              {line.label}
            </Text>
          )}
        </Box>
        <Box key={`${line.key}-rest`} flexShrink={1} minWidth={0}>
          <Text wrap="truncate-end" dimColor>
            {line.rest}
          </Text>
        </Box>
      </Box>
    )

    return (
      <Box key="cairn-stack" flexDirection="column">
        <Box key="cairn-band" flexDirection="column">
          {/* A Text drops its `key`, so each row's key sits on a Box. */}
          {lines.map((line, i) => (line.kind === 'header' ? header(line, i === 0) : item(line)))}
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
  const props: { color?: string; bold?: boolean; dimColor?: boolean } = {}
  if (span.color !== undefined) props.color = span.color
  if (span.bold) props.bold = true
  if (span.dimColor) props.dimColor = true
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
