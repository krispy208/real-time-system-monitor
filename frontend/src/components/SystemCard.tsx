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
    <article className="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold text-slate-100">{system.system_id}</h2>
        <StatusBadge status={system.status} />
      </div>

      <dl className="grid grid-cols-2 gap-3 text-sm">
        <Metric label="CPU" value={`${system.cpu_usage.toFixed(1)}%`} />
        <Metric label="Memory" value={`${system.memory_usage.toFixed(1)}%`} />
        <Metric label="Temperature" value={`${system.temperature.toFixed(1)}°C`} />
        <Metric label="Latency" value={`${system.latency.toFixed(1)} ms`} />
      </dl>

      <p className="mt-4 text-xs text-slate-400">
        Last updated: {formatTimestamp(system.timestamp)}
      </p>
    </article>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md bg-slate-950/60 px-3 py-2">
      <dt className="text-xs text-slate-400">{label}</dt>
      <dd className="mt-1 font-medium text-slate-100">{value}</dd>
    </div>
  )
}
