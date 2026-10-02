import type { CairnStep } from '../../types'
import type { BandRow } from './reader'

// The band's rows, as plain descriptions that register.tsx draws. Each
// milestone gets one row. Its left side names the phase, the id, and one
// text: the session's last chapter while the running skill is on that row,
// else the phase's next open task or criterion, else the title. Its right
// side holds the bar and the counts, the counts alone, or a state label. A
// running cairn skill with no milestone row of its phase gets a skill row
// of its own, above the milestone rows.

// One run of text and its style. Colors are theme keys, so they follow the
// person's light or dark theme.
export type Span = { text: string; color?: string; bold?: boolean; dimColor?: boolean }

// A step: a chapter or an open item. `label` is its positional label
// (`T2:`, `AC3:`), or null when it has none; `rest` is the text after it.
export type Step = { kind: 'step'; label: string | null; rest: string }

// The title, or a step. The engine cuts the text to the room the right
// group leaves, so the text is whole here. A skill row with no chapter has
// none.
export type Body = Step | { kind: 'title'; title: string } | null

export type BandLine = { key: string; head: Span[]; body: Body; tail: Span[] }

type Phase = { label: string; color: string; noun: string }

const PHASES: Record<string, Phase> = {
  'in-progress': { label: 'implement', color: 'claude', noun: 'tasks' },
  review: { label: 'review', color: 'success', noun: 'criteria' },
}

export const BAR_CELLS = 10
// Below this many band columns a row drops the bar.
export const BAR_MIN_COLUMNS = 60
// The columns between the left and the right group.
export const GAP = 2
const LABEL_WIDTH = 9
const FILLED = '█'
const EMPTY = '░'
export const ARROW = '→ '
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

// The step, or null when its skill has no label, as a step stored before a
// reload can name a skill the label map has since dropped.
export function knownStep(step: CairnStep | null): CairnStep | null {
  return step !== null && Object.prototype.hasOwnProperty.call(SKILL_LABELS, step.skill) ? step : null
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

// A chapter or an open item, its positional label split off.
function stepOf(text: string): Step {
  const label = POSITIONAL.exec(text)?.[0] ?? null
  return { kind: 'step', label, rest: label === null ? text : text.slice(label.length) }
}

// A skill row: the skill's label, its slash command, the chapter when one
// is set, and nothing on the right.
export function skillLines(step: CairnStep): BandLine[] {
  const color = step.skill === 'milestone-review' ? PHASES.review.color : PHASES['in-progress'].color
  const head: Span[] = [
    { text: SKILL_LABELS[step.skill].padEnd(LABEL_WIDTH), color },
    { text: ' ' },
    { text: `/${step.skill}` },
    { text: ' ' },
  ]
  return [{ key: 'skill-row', head, body: step.chapter === null ? null : stepOf(step.chapter), tail: [] }]
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

// One milestone's row. A chapter, when given, takes the place of the next
// open item.
export function bandLines(row: BandRow, columns: number, chapter: string | null = null): BandLine[] {
  const phase = phaseOf(row)
  const isTasks = phase.noun === 'tasks'
  const checked = isTasks ? row.tasksChecked : row.criteriaChecked
  const total = isTasks ? row.tasksTotal : row.criteriaTotal
  const next = isTasks ? row.nextTask : row.nextCriterion
  const text = chapter ?? next
  const body: Body = text === null ? { kind: 'title', title: row.title } : stepOf(text)

  // The right group: a state label that stands alone, or the counts. The
  // bar comes before the counts while the row is in its task or criterion
  // loop: no chapter, or a chapter with a positional label.
  let tail: Span[]
  if (checked === null || total === null) {
    tail = [{ text: 'no milestone file', color: 'warning' }]
  } else if (total === 0) {
    tail = [{ text: `no ${phase.noun}`, dimColor: true }]
  } else if (next === null) {
    tail = [{ text: `all ${total} ${phase.noun} checked`, dimColor: true }]
  } else {
    const inLoop = chapter === null || POSITIONAL.test(chapter)
    const cells = inLoop && columns >= BAR_MIN_COLUMNS ? [...bar(checked, total, phase.color), { text: '  ' }] : []
    tail = [...cells, { text: `${checked}/${total} ${phase.noun}` }]
  }

  const head: Span[] = [
    { text: phase.label.padEnd(LABEL_WIDTH), color: phase.color },
    { text: ' ' },
    { text: row.id, bold: true },
    { text: ' ' },
  ]
  return [{ key: `${row.id}-row`, head, body, tail }]
}

// A line's text with the two groups GAP spaces apart (the least gap a row
// draws; a wide row spreads them further), for the tests. A skill row has
// no right group, so its text ends at its body.
export function lineText(line: BandLine): string {
  const text = (spans: Span[]) => spans.map(s => s.text).join('')
  const body =
    line.body === null ? '' : line.body.kind === 'title' ? line.body.title : `${ARROW}${line.body.label ?? ''}${line.body.rest}`
  return `${text(line.head)}${body}${' '.repeat(GAP)}${text(line.tail)}`.trimEnd()
}
