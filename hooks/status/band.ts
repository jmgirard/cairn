import type { BandRow } from './reader'

const PHASE: Record<string, string> = { 'in-progress': 'implement', review: 'review' }

// One band line: id, title, phase, and the task counts or their absence.
export function bandLine(row: BandRow): string {
  const counts = row.tasksTotal === null ? 'no milestone file' : `${row.tasksChecked}/${row.tasksTotal} tasks`
  return `${row.id} ${row.title} · ${PHASE[row.status] ?? row.status} · ${counts}`
}
