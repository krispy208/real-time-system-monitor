import type { HealthStatus, SystemSummary } from '../types'

interface SummaryBarProps {
  systems: Record<string, SystemSummary>
}

function countByStatus(
  systems: Record<string, SystemSummary>,
  status: HealthStatus,
): number {
  return Object.values(systems).filter((system) => system.status === status).length
}

export function SummaryBar({ systems }: SummaryBarProps) {
  const total = Object.keys(systems).length
  const healthy = countByStatus(systems, 'HEALTHY')
  const warning = countByStatus(systems, 'WARNING')
  const critical = countByStatus(systems, 'CRITICAL')

  return (
    <section className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      <SummaryTile label="Total systems" value={total} />
      <SummaryTile label="Healthy" value={healthy} accent="text-emerald-300" />
      <SummaryTile label="Warning" value={warning} accent="text-amber-300" />
      <SummaryTile label="Critical" value={critical} accent="text-red-300" />
    </section>
  )
}

function SummaryTile({
  label,
  value,
  accent = 'text-slate-100',
}: {
  label: string
  value: number
  accent?: string
}) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/70 px-4 py-3">
      <p className="text-xs uppercase tracking-wide text-slate-400">{label}</p>
      <p className={`mt-1 text-2xl font-semibold ${accent}`}>{value}</p>
    </div>
  )
}
