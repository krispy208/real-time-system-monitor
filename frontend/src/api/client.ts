import { API_BASE_URL } from '../config'
import type { AlertRecord, SystemSummary } from '../types'

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`)
  }
  return response.json() as Promise<T>
}

export function fetchSystems(): Promise<SystemSummary[]> {
  return fetchJson<SystemSummary[]>('/api/systems')
}

export function fetchAlerts(): Promise<AlertRecord[]> {
  return fetchJson<AlertRecord[]>('/api/alerts')
}
