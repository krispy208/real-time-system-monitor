import type { AlertRecord } from '../types'

interface AlertPanelProps {
  alerts: AlertRecord[]
}

const SEVERITY_STYLES: Record<string, string> = {
  HEALTHY: 'text-emerald-300',
  WARNING: 'text-amber-300',
  CRITICAL: 'text-red-300',
}

function formatTimestamp(timestamp: string): string {
  return new Date(timestamp).toLocaleString()
}

export function AlertPanel({ alerts }: AlertPanelProps) {
  return (
    <section className="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
      <h3 className="mb-4 text-sm font-medium text-slate-200">Recent Alerts</h3>

      {alerts.length === 0 ? (
        <p className="text-sm text-slate-500">No alerts yet.</p>
      ) : (
        <ul className="max-h-96 space-y-3 overflow-y-auto pr-1">
          {alerts.map((alert, index) => (
            <li
              key={`${alert.timestamp}-${alert.system_id}-${alert.metric}-${index}`}
              className="rounded-md border border-slate-800 bg-slate-950/60 p-3"
            >
              <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
                <span>{formatTimestamp(alert.timestamp)}</span>
                <span>•</span>
                <span>{alert.system_id}</span>
                <span>•</span>
                <span>{alert.metric}</span>
                <span>•</span>
                <span
                  className={
                    SEVERITY_STYLES[alert.severity] ?? 'text-slate-300'
                  }
                >
                  {alert.severity}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-200">{alert.message}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
