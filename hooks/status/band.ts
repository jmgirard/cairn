import type { BandRow } from './reader'

// The band's rows for one milestone, as plain descriptions that
// register.tsx draws. A header row names the phase, id, and title on the
// left, and either a bar and the counts or a state label on the right; when
// the section has an open box, an item row under it names the phase's next
// open task or criterion.

// One run of text and its style. Colors are theme keys, so they follow the
// person's light or dark theme.
export type Span = { text: string; color?: string; bold?: boolean; dimColor?: boolean }

// The engine cuts the title to the room the right group leaves, so the
// title is whole here.
export type HeaderLine = { kind: 'header'; key: string; head: Span[]; title: string; tail: Span[] }

// `label` is the item's positional label (`T2:`, `AC3:`), or null when the
// item has none; `rest` is the text after it.
export type ItemLine = { kind: 'item'; key: string; arrow: string; label: string | null; rest: string }

export type BandLine = HeaderLine | ItemLine

type Phase = { label: string; color: string; noun: string }

const PHASES: Record<string, Phase> = {
  'in-progress': { label: 'implement', color: 'claude', noun: 'tasks' },
  review: { label: 'review', color: 'success', noun: 'criteria' },
}

export const BAR_CELLS = 10
// Below this many band columns the header row drops the bar.
export const BAR_MIN_COLUMNS = 60
// The columns between the left and the right group.
export const GAP = 2
const LABEL_WIDTH = 9
const FILLED = '█'
const EMPTY = '░'
const ARROW = '→'
const POSITIONAL = /^(T|AC)\d+[a-z]*:/

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

export function bandLines(row: BandRow, columns: number): BandLine[] {
  const phase = phaseOf(row)
  const isTasks = phase.noun === 'tasks'
  const checked = isTasks ? row.tasksChecked : row.criteriaChecked
  const total = isTasks ? row.tasksTotal : row.criteriaTotal
  const next = isTasks ? row.nextTask : row.nextCriterion

  // The right group: the counts with a bar, or a state label that stands
  // alone, with no bar and no item row.
  let tail: Span[]
  let item: string | null = null
  if (checked === null || total === null) {
    tail = [{ text: 'no milestone file', color: 'warning' }]
  } else if (total === 0) {
    tail = [{ text: `no ${phase.noun}`, dimColor: true }]
  } else if (next === null) {
    tail = [{ text: `all ${total} ${phase.noun} checked`, dimColor: true }]
  } else {
    const cells = columns >= BAR_MIN_COLUMNS ? [...bar(checked, total, phase.color), { text: '  ' }] : []
    tail = [...cells, { text: `${checked}/${total} ${phase.noun}` }]
    item = next
  }

  const head: Span[] = [
    { text: phase.label.padEnd(LABEL_WIDTH), color: phase.color },
    { text: ' ' },
    { text: row.id, bold: true },
    { text: ' ' },
  ]
  const lines: BandLine[] = [{ kind: 'header', key: `${row.id}-header`, head, title: row.title, tail }]
  if (item !== null) {
    const label = POSITIONAL.exec(item)?.[0] ?? null
    lines.push({
      kind: 'item',
      key: `${row.id}-item`,
      arrow: `  ${ARROW} `,
      label,
      rest: label === null ? item : item.slice(label.length),
    })
  }
  return lines
}

// A line's text as drawn, the gap between the groups written as spaces, for
// the tests.
export function lineText(line: BandLine): string {
  if (line.kind === 'item') return `${line.arrow}${line.label ?? ''}${line.rest}`
  const text = (spans: Span[]) => spans.map(s => s.text).join('')
  return `${text(line.head)}${line.title}${' '.repeat(GAP)}${text(line.tail)}`
}
