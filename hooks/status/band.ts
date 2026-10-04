import type { CairnBandHidden, CairnBandMark, CairnStep } from '../../types'
import type { BandRow, BandState, WorkableRow } from './reader'

// The band's one row, as a plain description that register.tsx draws
// (M206). It shows one active milestone: the first `review` row while
// /milestone-review runs and one exists, else the first `in-progress` row,
// else the first `review` row. With no active row, it shows the idle row
// for the first workable planned milestone, whether or not a cairn skill
// runs. Its left side is the bold id and the title. Its right side is the
// flow track and its percent, the idle row's track and command, or a
// warning label for a row whose counts cannot be read. The track draws as
// an image on the desktop and as braille cells in the terminal (track.ts),
// at the width the row leaves it.

// One run of text and its style. The row draws in `inactive`, the theme's
// gray, but for the warning labels and the terminal track's cells.
export type Span = { text: string; color?: string; backgroundColor?: string; bold?: boolean }

export const GRAY = 'inactive'
export const ORANGE = 'rgb(194,122,92)'
export const GREEN = 'rgb(106,165,122)'
// The plan phase's hue in the track (M204).
export const BLUE = 'rgb(110,140,190)'

// The track and the columns it takes: an image of about PX_PER_COLUMN
// pixels a column on the desktop, one braille cell a column in the
// terminal.
export type TrackPart = { flow: Flow; columns: number }

// `track`, when set, draws before the tail.
export type BandLine = { key: string; id: string; title: string; tail: Span[]; track?: TrackPart }

type Phase = { noun: string }

const PHASES: Record<string, Phase> = {
  'in-progress': { noun: 'tasks' },
  review: { noun: 'criteria' },
}

// The columns between the left and the right group.
export const GAP = 2
// The most columns a row keeps for its title when it picks a form: a
// shorter title needs only its own width.
export const TEXT_ROOM = 10
// The most and least columns the track takes. The desktop counts the full
// TRACK_PX (360) image as TRACK_COLUMNS, at about PX_PER_COLUMN pixels a
// column (M204). Below MIN_TRACK_COLUMNS, the track keeps that width and
// the title takes less room.
export const TRACK_COLUMNS = 52
export const MIN_TRACK_COLUMNS = 12
export const PX_PER_COLUMN = 7

// The cairn skills, by their directories under `skills/`. fixtures.gen.ts
// lists those directories, and a test holds this list to that one. A
// running skill shows nothing of its own (M206): /milestone-review picks the
// row, and a skill's start or end can show a band hidden over a milestone
// row.
export const CAIRN_SKILLS: readonly string[] = [
  'milestone-plan',
  'milestone-implement',
  'milestone-review',
  'hotfix',
  'cairn-triage',
  'cairn-release',
  'milestone',
  'milestone-brief',
  'design-interview',
  'cairn-init',
]

// A skill's bare name when it is a cairn skill, from its bare name or its
// `cairn:` name; null for any other skill.
export function cairnSkill(name: string): string | null {
  const bare = name.startsWith('cairn:') ? name.slice('cairn:'.length) : name
  return CAIRN_SKILLS.includes(bare) ? bare : null
}

// The step, or null when its skill is not a cairn skill, as a step stored
// before a reload can name a skill the list has since dropped.
export function knownStep(step: CairnStep | null): CairnStep | null {
  return step !== null && CAIRN_SKILLS.includes(step.skill) ? step : null
}

// What the close button stores at a press, and what a refresh and the
// drawing compare it with: the ids and statuses of the active rows, in
// ROADMAP order, the running skill while a row is active, and the idle
// row's id while none is (M206). The step is read through knownStep, as the
// drawing reads it (M200). The workable list is left out while a row is
// active, so a planned row added then keeps the band hidden too. The skill
// is left out while no row is active, so a skill's start or end keeps a
// hidden idle row hidden.
export function mark(state: BandState, step: CairnStep | null): CairnBandHidden {
  const current = knownStep(step)
  const marks: CairnBandMark[] = state.rows.map(row => ({ id: row.id, status: row.status }))
  const active = state.rows.length > 0
  return {
    marks,
    skill: active && current !== null ? current.skill : null,
    idle: active ? null : (state.workable[0]?.id ?? null),
  }
}

export function same(a: CairnBandHidden, b: CairnBandHidden): boolean {
  return (
    a.skill === b.skill &&
    a.idle === b.idle &&
    a.marks.length === b.marks.length &&
    a.marks.every((m, i) => m.id === b.marks[i].id && m.status === b.marks[i].status)
  )
}

export function phaseOf(row: BandRow): Phase {
  return PHASES[row.status]
}

// The flow track (M204): one flow of three equal segments, plan, then
// implement, then review. track.ts draws it; the model is here.
export type FlowPhase = 'plan' | 'implement' | 'review'
export const FLOW_PHASES: readonly FlowPhase[] = ['plan', 'implement', 'review']
export const FLOW_COLORS: Record<FlowPhase, string> = { plan: BLUE, implement: ORANGE, review: GREEN }

// A segment's fill as a whole-number fraction, so the percent needs no
// floating point.
export type Fill = { num: number; den: number }

export type Flow = {
  // The phase the pill sits on and takes its color from.
  phase: FlowPhase
  // Plan, implement, review.
  fills: [Fill, Fill, Fill]
  // The items in the implement and review segments. The active segment's
  // count sets its ticks; 0 draws none.
  items: [number, number]
  pill: string
  // The pill's text on a track too short for `pill`: the count alone, or
  // `none` for a section with no items (M206).
  short: string
  // The flow's percent, or null on a row that shows none.
  percent: number | null
  // What the drawing says, for a reader that cannot see it.
  alt: string
}

const FULL: Fill = { num: 1, den: 1 }
const NONE: Fill = { num: 0, den: 1 }

// A section of zero items is empty.
function share(checked: number, total: number): Fill {
  return total === 0 ? NONE : { num: checked, den: total }
}

// floor(100 × (sum of the fills) / 3), in whole numbers.
export function percentOf(fills: readonly Fill[]): number {
  const den = fills.reduce((d, f) => d * f.den, 1)
  const num = fills.reduce((n, f) => n + f.num * (den / f.den), 0)
  const top = 100 * num
  return (top - (top % (3 * den))) / (3 * den)
}

// A milestone row's flow, or null when its counts cannot be read. Plan is
// full. An `in-progress` row fills implement by its tasks and leaves review
// empty; a `review` row fills implement and fills review by its criteria.
export function flowOf(row: BandRow): Flow | null {
  const { tasksChecked, tasksTotal, criteriaChecked, criteriaTotal } = row
  if (tasksChecked === null || tasksTotal === null || criteriaChecked === null || criteriaTotal === null) return null
  const isTasks = phaseOf(row).noun === 'tasks'
  const fills: [Fill, Fill, Fill] = isTasks
    ? [FULL, share(tasksChecked, tasksTotal), NONE]
    : [FULL, FULL, share(criteriaChecked, criteriaTotal)]
  const [checked, total, noun] = isTasks ? [tasksChecked, tasksTotal, 'tasks'] : [criteriaChecked, criteriaTotal, 'criteria']
  const phase: FlowPhase = isTasks ? 'implement' : 'review'
  const name = isTasks ? 'Implement' : 'Review'
  const percent = percentOf(fills)
  const counts = total === 0 ? `no ${noun}` : `${checked}/${total} ${noun}`
  return {
    phase,
    fills,
    items: [tasksTotal, criteriaTotal],
    pill: total === 0 ? `no ${noun}` : `${name} ${checked}/${total}`,
    short: total === 0 ? 'none' : `${checked}/${total}`,
    percent,
    alt: `${phase} ${counts}, ${percent}% through plan, implement, review`,
  }
}

// The idle row's flow: plan full, the rest empty, no percent.
export function idleFlow(): Flow {
  return {
    phase: 'plan',
    fills: [FULL, NONE, NONE],
    items: [0, 0],
    pill: 'Planned',
    short: 'Planned',
    percent: null,
    alt: 'plan done, implement next',
  }
}

// Columns at one per code point: true for ASCII and the band's own glyphs.
// A wide character in a title, such as a CJK character or an emoji, is
// undercounted.
export function width(text: string): number {
  return [...text].length
}

const spansWidth = (spans: Span[]) => spans.reduce((n, span) => n + width(span.text), 0)

// The columns of the left group's part that does not shrink: the id and
// the space after it.
function headWidth(id: string): number {
  return width(id) + 1
}

// The columns the title needs to pick a form: its full width, or TEXT_ROOM
// when that is less.
function textNeed(title: string): number {
  return Math.min(width(title), TEXT_ROOM)
}

// The columns a row leaves the right group, less `tail` and the title's
// need. `close` is the columns the row's close gap and buttons take.
function room(columns: number, close: number, line: { id: string; title: string }, tail: Span[]): number {
  return columns - headWidth(line.id) - textNeed(line.title) - GAP - spansWidth(tail) - close
}

// The track's columns in that room: at most TRACK_COLUMNS, and at least
// MIN_TRACK_COLUMNS.
function trackColumns(left: number): number {
  return Math.max(MIN_TRACK_COLUMNS, Math.min(TRACK_COLUMNS, left))
}

// The space between the track and what follows it.
const SPACE: Span = { text: ' ' }

// The idle row: the bold id and the title, and on the right the track
// (plan full) and the command that starts the milestone. Where the row
// leaves the track too little room, the track goes, and then the command.
export function idleLines(next: WorkableRow, columns: number, close = 0): BandLine[] {
  const line = { key: 'idle-row', id: next.id, title: next.title }
  const command: Span = { text: `/milestone-implement ${next.id}`, color: GRAY }
  const withTrack = [SPACE, command]
  const left = room(columns, close, line, withTrack)
  if (left >= MIN_TRACK_COLUMNS) {
    return [{ ...line, tail: withTrack, track: { flow: idleFlow(), columns: trackColumns(left) } }]
  }
  return [{ ...line, tail: room(columns, close, line, [command]) >= 0 ? [command] : [] }]
}

// The band's one row, or none: the first `review` row under
// /milestone-review, else the first `in-progress` row, else the first
// `review` row; with no active row, an idle row for the first workable
// planned row, else nothing. `rows` are the active rows in ROADMAP order,
// and `workable` the workable planned rows in their order. `close` is the
// columns the close gap and buttons take.
export function stepLines(
  rows: BandRow[],
  step: CairnStep | null,
  columns: number,
  close = 0,
  workable: WorkableRow[] = [],
): BandLine[] {
  const first = (status: string) => rows.find(row => row.status === status)
  const reviewed = step?.skill === 'milestone-review' ? first('review') : undefined
  const row = reviewed ?? first('in-progress') ?? first('review')
  if (row !== undefined) return bandLines(row, columns, close)
  return workable.length === 0 ? [] : idleLines(workable[0], columns, close)
}

// One milestone's row: the track and its percent, or a warning label when
// its counts cannot be read. The track keeps its least width even where
// that leaves the title less than its room.
export function bandLines(row: BandRow, columns: number, close = 0): BandLine[] {
  const line = { key: `${row.id}-row`, id: row.id, title: row.title }
  const flow = flowOf(row)
  if (flow === null) {
    const long: Span[] = [{ text: 'no milestone file', color: 'warning' }]
    const short: Span[] = [{ text: 'no file', color: 'warning' }]
    return [{ ...line, tail: room(columns, close, line, long) >= 0 ? long : short }]
  }
  const tail: Span[] = [SPACE, { text: `${flow.percent}%`, color: GRAY }]
  return [{ ...line, tail, track: { flow, columns: trackColumns(room(columns, close, line, tail)) } }]
}

// A line's text with the two groups GAP spaces apart (the least gap a row
// draws; a wide row spreads them further), for the tests. The track draws
// as `[track N]`, N its columns.
export function lineText(line: BandLine): string {
  const text = (spans: Span[]) => spans.map(s => s.text).join('')
  const track = line.track === undefined ? '' : `[track ${line.track.columns}]`
  return `${line.id} ${line.title}${' '.repeat(GAP)}${track}${text(line.tail)}`.trimEnd()
}
