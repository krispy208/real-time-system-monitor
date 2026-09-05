import type { HealthStatus } from '../types'

const STATUS_STYLES: Record<HealthStatus, string> = {
  HEALTHY: 'bg-emerald-500/15 text-emerald-300 ring-emerald-500/30',
  WARNING: 'bg-amber-500/15 text-amber-300 ring-amber-500/30',
  CRITICAL: 'bg-red-500/15 text-red-300 ring-red-500/30',
}

interface StatusBadgeProps {
  status: HealthStatus
  className?: string
}

export function StatusBadge({ status, className = '' }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ring-1 ring-inset ${STATUS_STYLES[status]} ${className}`}
    >
      {status}
    </span>
  )
}
