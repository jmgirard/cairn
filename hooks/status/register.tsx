import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Span } from './band'
import { bandLines } from './band'
import type { BandRow, FileSource } from './reader'
import { loadBand } from './reader'

// The milestone band above the prompt (M191, M193): a header row per
// `in-progress` or `review` ROADMAP row, and an item row under it when its
// phase section has an open box, refreshed when the session starts and at
// the end of each turn. The rows sit above whatever the hooks beneath draw
// in the same slot.

// The shape tag names the row layout; a reload whose rows were written
// under another tag reads them as absent. Bump it when BandRow changes.
const band = atom({ plugin: 'cairn', key: 'band' } as const, [] as BandRow[], { shape: 'band-2' })

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
    const beneath = await next(e)
    const { Box, Text } = $.ui.resolve(e)
    const lines = rows.flatMap(row => bandLines(row, e.props.bodyColumns))
    return (
      <Box key="cairn-stack" flexDirection="column">
        <Box key="cairn-band" flexDirection="column">
          {/* A Text drops its `key`, so each row's key sits on a Box. */}
          {lines.map(line => (
            <Box key={line.key}>
              <Text wrap="truncate-end" {...(line.dimColor ? { dimColor: true } : {})}>
                {line.spans.map(span => (
                  <Text wrap="truncate-end" {...style(span)}>
                    {span.text}
                  </Text>
                ))}
              </Text>
            </Box>
          ))}
        </Box>
        {beneath ?? null}
      </Box>
    )
  })
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
