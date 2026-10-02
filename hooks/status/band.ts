import type { CairnStep } from '../../types'
import type { BandRow } from './reader'

// The band's rows, as plain descriptions that register.tsx draws. A
// milestone's header row names the phase, id, and title on the left, and
// either a bar and the counts or a state label on the right. An item row
// under it names the session's last chapter while the running skill is on
// that row, and otherwise the phase's next open task or criterion. A
// running cairn skill with no milestone row of its phase gets a skill row
// of its own, above the milestone rows.

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

// The band's label for each cairn skill, by its directory under `skills/`.
// fixtures.gen.ts lists those directories, and a test holds this map to
// that list.
export const SKILL_LABELS: Record<string, string> = {
  'milestone-plan': 'plan',
  'milestone-implement': 'implement',
  'milestone-review': 'review',
  hotfix: 'hotfix',
  'cairn-triage': 'triage',
  'cairn-release': 'release',
  milestone: 'status',
  'milestone-brief': 'brief',
  'design-interview': 'design',
  'cairn-init': 'init',
}

// The ROADMAP status of the milestone row a skill runs on, for the two
// skills that run on one.
const CARRIES: Record<string, string> = {
  'milestone-implement': 'in-progress',
  'milestone-review': 'review',
}

// A skill's bare name when it is a cairn skill, from its bare name or its
// `cairn:` name; null for any other skill.
export function cairnSkill(name: string): string | null {
  const bare = name.startsWith('cairn:') ? name.slice('cairn:'.length) : name
  return Object.prototype.hasOwnProperty.call(SKILL_LABELS, bare) ? bare : null
}

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

// An item row: the arrow, then the text, its positional label split off.
function itemLine(key: string, text: string): ItemLine {
  const label = POSITIONAL.exec(text)?.[0] ?? null
  return { kind: 'item', key, arrow: `  ${ARROW} `, label, rest: label === null ? text : text.slice(label.length) }
}

// A skill row: the skill's label, its slash command, nothing on the right,
// and the chapter under it when one is set.
export function skillLines(step: CairnStep): BandLine[] {
  const color = step.skill === 'milestone-review' ? PHASES.review.color : PHASES['in-progress'].color
  const head: Span[] = [{ text: SKILL_LABELS[step.skill].padEnd(LABEL_WIDTH), color }, { text: ' ' }]
  const lines: BandLine[] = [{ kind: 'header', key: 'skill-header', head, title: `/${step.skill}`, tail: [] }]
  if (step.chapter !== null) lines.push(itemLine('skill-item', step.chapter))
  return lines
}

// Every row of the band. With a running skill, the first milestone row of
// its phase carries it and shows the chapter, or a skill row comes first
// when no row does.
export function stepLines(rows: BandRow[], step: CairnStep | null, columns: number): BandLine[] {
  const status = step === null ? undefined : CARRIES[step.skill]
  const carrier = status === undefined ? -1 : rows.findIndex(row => row.status === status)
  const chapter = step === null ? null : step.chapter
  const milestones = rows.flatMap((row, i) => bandLines(row, columns, i === carrier ? chapter : null))
  return step !== null && carrier < 0 ? [...skillLines(step), ...milestones] : milestones
}

// One milestone's rows. A chapter, when given, takes the item row.
export function bandLines(row: BandRow, columns: number, chapter: string | null = null): BandLine[] {
  const phase = phaseOf(row)
  const isTasks = phase.noun === 'tasks'
  const checked = isTasks ? row.tasksChecked : row.criteriaChecked
  const total = isTasks ? row.tasksTotal : row.criteriaTotal
  const next = isTasks ? row.nextTask : row.nextCriterion

  // The right group: the counts with a bar, or a state label that stands
  // alone, with no bar and no item row of its own.
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
  const text = chapter ?? item
  if (text !== null) lines.push(itemLine(`${row.id}-item`, text))
  return lines
}

// A line's text with the two groups GAP spaces apart (the least gap a row
// draws; a wide row spreads them further), for the tests. A skill row has
// no right group, so its text ends at the title.
export function lineText(line: BandLine): string {
  if (line.kind === 'item') return `${line.arrow}${line.label ?? ''}${line.rest}`
  const text = (spans: Span[]) => spans.map(s => s.text).join('')
  return `${text(line.head)}${line.title}${' '.repeat(GAP)}${text(line.tail)}`.trimEnd()
}
