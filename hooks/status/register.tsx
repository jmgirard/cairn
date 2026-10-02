import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { CairnBandMark } from '../../types'
import type { HeaderLine, ItemLine, Span } from './band'
import { bandLines, GAP } from './band'
import type { BandRow, FileSource } from './reader'
import { loadBand } from './reader'

// The milestone band above the prompt (M191, M193, M194): a header row per
// `in-progress` or `review` ROADMAP row, and an item row under it when its
// phase section has an open box, refreshed when the session starts and at
// the end of each turn. The rows sit above whatever the hooks beneath draw
// in the same slot. The first header row ends in a close button, which
// hides the band until the active rows' ids, statuses, or order change.

// The shape tag names the row layout; a reload whose rows were written
// under another tag reads them as absent. Bump it when BandRow changes.
const band = atom({ plugin: 'cairn', key: 'band' } as const, [] as BandRow[], { shape: 'band-2' })

// The active ids and statuses, in ROADMAP order, at the last press of the
// close button; null while the band shows.
const dismissed = atom({ plugin: 'cairn', key: 'dismissed' } as const, null as CairnBandMark[] | null)

// The close button's label: a desktop draws its own close control, the
// label its accessible name; the terminal draws the label.
const CLOSE_LABEL: Record<string, string> = { desktop: 'Close milestone band' }
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

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const rows = await read($, band)
    if (rows.length === 0) return next(e)
    const hidden = await read($, dismissed)
    if (hidden !== null && same(hidden, marks(rows))) return next(e)
    const beneath = await next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const lines = rows.flatMap(row => bandLines(row, e.props.bodyColumns))
    const spans = (list: Span[]) =>
      list.map(span => (
        <Text wrap="truncate-end" {...style(span)}>
          {span.text}
        </Text>
      ))

    // Two groups: the phase, id and title on the left, which give way first,
    // and the bar and counts or the state label on the right, which keep
    // their width. The engine cuts the title to the room that is left.
    const header = (line: HeaderLine, isFirst: boolean) => (
      <Box key={line.key} justifyContent="space-between">
        <Box key={`${line.key}-left`} flexShrink={1}>
          {spans(line.head)}
          <Box key={`${line.key}-title`} flexShrink={1}>
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
              label={CLOSE_LABEL[e.surface] ?? CLOSE_GLYPH}
              onPress={() => dismiss($)}
            />
          ) : null}
        </Box>
      </Box>
    )

    // The positional label draws bold and at full strength, with no
    // dimColor; the rest of the row is dim. The rest sits in a Box of its
    // own that gives way, as the title does. With the arrow, label, and rest
    // nested in one Text, the desktop drew the rest as a bare `…`.
    const item = (line: ItemLine) => (
      <Box key={line.key}>
        <Text wrap="truncate-end" dimColor>
          {line.arrow}
        </Text>
        {line.label === null ? null : (
          <Text wrap="truncate-end" bold>
            {line.label}
          </Text>
        )}
        <Box key={`${line.key}-rest`} flexShrink={1}>
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

// The ids and statuses of the active rows, in ROADMAP order.
function marks(rows: BandRow[]): CairnBandMark[] {
  return rows.map(row => ({ id: row.id, status: row.status }))
}

function same(a: CairnBandMark[], b: CairnBandMark[]): boolean {
  return a.length === b.length && a.every((m, i) => m.id === b[i].id && m.status === b[i].status)
}

// The press reads the rows as they are now, not as they were drawn.
async function dismiss($) {
  const rows = await read($, band)
  await update($, dismissed, () => marks(rows))
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
  // A change to the active ids, statuses, or order brings the band back,
  // and it stays until the next press.
  const hidden = await read($, dismissed)
  if (hidden !== null && !same(hidden, marks(rows))) await update($, dismissed, () => null)
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
