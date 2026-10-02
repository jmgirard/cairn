import type { BandRow } from './reader'

// The band's rows for one milestone, as plain descriptions that
// register.tsx draws as Text elements. A header row names the phase, id,
// title, and either a bar and the counts or a state label; when the section
// has an open box, an item row under it names the phase's next open task or
// criterion.

// One run of text and its style. Colors are theme keys, so they follow the
// person's light or dark theme.
export type Span = { text: string; color?: string; bold?: boolean; dimColor?: boolean }

export type BandLine = { key: string; spans: Span[]; dimColor?: boolean }

type Phase = { label: string; color: string; noun: string }

const PHASES: Record<string, Phase> = {
  'in-progress': { label: 'implement', color: 'claude', noun: 'tasks' },
  review: { label: 'review', color: 'success', noun: 'criteria' },
}

export const BAR_CELLS = 10
// Below this many band columns the header row drops the bar.
export const BAR_MIN_COLUMNS = 60
const LABEL_WIDTH = 9
const FILLED = '█'
const EMPTY = '░'
const ARROW = '→'

export function phaseOf(row: BandRow): Phase {
  return PHASES[row.status]
}

// Filled cells round down, so the bar is never full while a box is open; an
// all-checked section shows a label instead.
export function bar(checked: number, total: number, color: string): Span[] {
  const filled = Math.floor((BAR_CELLS * checked) / total)
  return [
    { text: FILLED.repeat(filled), color },
    { text: EMPTY.repeat(BAR_CELLS - filled), dimColor: true },
  ]
}

// The title cut to `width` characters, an ellipsis marking the cut.
function fit(title: string, width: number): string {
  if (title.length <= width) return title
  if (width <= 0) return ''
  return `${title.slice(0, width - 1)}…`
}

function width(spans: Span[]): number {
  return spans.reduce((n, s) => n + s.text.length, 0)
}

export function bandLines(row: BandRow, columns: number): BandLine[] {
  const phase = phaseOf(row)
  const isTasks = phase.noun === 'tasks'
  const checked = isTasks ? row.tasksChecked : row.criteriaChecked
  const total = isTasks ? row.tasksTotal : row.criteriaTotal
  const next = isTasks ? row.nextTask : row.nextCriterion

  // The spans after the title: the counts with a bar, or a state label that
  // stands alone, with no bar and no item row.
  let tail: Span[]
  let item: string | null = null
  if (checked === null || total === null) {
    tail = [{ text: '  ' }, { text: 'no milestone file', color: 'warning' }]
  } else if (total === 0) {
    tail = [{ text: '  ' }, { text: `no ${phase.noun}`, dimColor: true }]
  } else if (next === null) {
    tail = [{ text: '  ' }, { text: `all ${total} ${phase.noun} checked`, dimColor: true }]
  } else {
    const cells = columns >= BAR_MIN_COLUMNS ? [{ text: '  ' }, ...bar(checked, total, phase.color)] : []
    tail = [...cells, { text: '  ' }, { text: `${checked}/${total} ${phase.noun}` }]
    item = next
  }

  const head: Span[] = [
    { text: phase.label.padEnd(LABEL_WIDTH), color: phase.color },
    { text: ' ' },
    { text: row.id, bold: true },
    { text: ' ' },
  ]
  // The title takes what is left, so a narrow band cuts the title before the
  // counts.
  const title = fit(row.title, Math.max(columns - width(head) - width(tail), 0))
  const lines: BandLine[] = [{ key: `${row.id}-header`, spans: [...head, { text: title }, ...tail] }]
  if (item !== null) {
    lines.push({ key: `${row.id}-item`, spans: [{ text: `  ${ARROW} ${item}`, dimColor: true }], dimColor: true })
  }
  return lines
}

// A line's text as drawn, for the tests.
export function lineText(line: BandLine): string {
  return line.spans.map(s => s.text).join('')
}
