import type { AlertRecord, HealthStatus } from './api'

export interface TelemetryUpdate {
  system_id: string
  timestamp: string
  cpu_usage: number
  memory_usage: number
  temperature: number
  latency: number
  status: HealthStatus
  metric_statuses: Record<string, HealthStatus>
  alerts: AlertRecord[]
}

export type WebSocketConnectionState =
  | 'connected'
  | 'reconnecting'
  | 'disconnected'

export interface ChartPoint {
  timestamp: string
  temperature: number
  latency: number
  label: string
}
