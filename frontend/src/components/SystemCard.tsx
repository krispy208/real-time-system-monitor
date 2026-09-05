import type { SystemSummary } from '../types'
import { StatusBadge } from './StatusBadge'

interface SystemCardProps {
  system: SystemSummary
}

function formatTimestamp(timestamp: string): string {
  return new Date(timestamp).toLocaleTimeString()
}

export function SystemCard({ system }: SystemCardProps) {
  return (
    <article className="rounded-lg border border-slate-800 bg-slate-900/70 p-3">
      <div className="mb-2 flex items-center justify-between gap-2">
        <h2 className="text-base font-semibold text-slate-100">{system.system_id}</h2>
        <StatusBadge status={system.status} />
      </div>

      <dl className="grid grid-cols-2 gap-x-3 gap-y-1">
        <Metric label="CPU" value={`${system.cpu_usage.toFixed(1)}%`} />
        <Metric label="Memory" value={`${system.memory_usage.toFixed(1)}%`} />
        <Metric label="Temp" value={`${system.temperature.toFixed(1)}°C`} />
        <Metric label="Latency" value={`${system.latency.toFixed(1)} ms`} />
      </dl>

      <p className="mt-2 text-[11px] text-slate-500">
        Updated {formatTimestamp(system.timestamp)}
      </p>
    </article>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-baseline justify-between gap-2 rounded bg-slate-950/50 px-2 py-1">
      <dt className="text-xs text-slate-400">{label}</dt>
      <dd className="text-sm font-medium tabular-nums text-slate-100">{value}</dd>
    </div>
  )
}
