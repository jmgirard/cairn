import type { BandRow } from './reader'

const PHASE: Record<string, string> = { 'in-progress': 'implement', review: 'review' }

// One band line: id, title, phase, and the task counts or their absence.
export function bandLine(row: BandRow): string {
  const counts = row.total === null ? 'no milestone file' : `${row.checked}/${row.total} tasks`
  return `${row.id} ${row.title} · ${PHASE[row.status] ?? row.status} · ${counts}`
}
