import type { WebSocketConnectionState } from '../types'

const STATE_STYLES: Record<
  WebSocketConnectionState,
  { dot: string; label: string }
> = {
  connected: {
    dot: 'bg-emerald-400',
    label: 'Connected',
  },
  reconnecting: {
    dot: 'bg-amber-400',
    label: 'Reconnecting',
  },
  disconnected: {
    dot: 'bg-red-400',
    label: 'Disconnected',
  },
}

interface ConnectionStatusProps {
  state: WebSocketConnectionState
}

export function ConnectionStatus({ state }: ConnectionStatusProps) {
  const styles = STATE_STYLES[state]

  return (
    <div className="flex items-center gap-2 text-sm text-slate-300">
      <span className={`h-2.5 w-2.5 rounded-full ${styles.dot}`} />
      <span>{styles.label}</span>
    </div>
  )
}
