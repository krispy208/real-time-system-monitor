export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export const WS_TELEMETRY_URL =
  import.meta.env.VITE_WS_TELEMETRY_URL ?? 'ws://localhost:8000/ws/telemetry'

export const SYSTEM_IDS = ['SYSTEM-01', 'SYSTEM-02', 'SYSTEM-03'] as const

export type SystemId = (typeof SYSTEM_IDS)[number]

export const MAX_CHART_POINTS = 60

export const WS_RECONNECT_DELAY_MS = 3000
