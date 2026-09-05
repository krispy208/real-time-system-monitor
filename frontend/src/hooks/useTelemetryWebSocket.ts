/**
 * Live telemetry WebSocket hook.
 *
 * Manages connect / reconnect / cleanup lifecycle. Uses a ref for onMessage so
 * the socket is not recreated every time the parent callback identity changes.
 */
import { useEffect, useRef, useState } from 'react'

import { WS_RECONNECT_DELAY_MS, WS_TELEMETRY_URL } from '../config'
import type { TelemetryUpdate, WebSocketConnectionState } from '../types'

interface UseTelemetryWebSocketOptions {
  onMessage: (message: TelemetryUpdate) => void
  enabled?: boolean
}

export function useTelemetryWebSocket({
  onMessage,
  enabled = true,
}: UseTelemetryWebSocketOptions) {
  const [connectionState, setConnectionState] =
    useState<WebSocketConnectionState>('disconnected')
  const onMessageRef = useRef(onMessage)

  useEffect(() => {
    onMessageRef.current = onMessage
  }, [onMessage])

  useEffect(() => {
    if (!enabled) {
      setConnectionState('disconnected')
      return
    }

    let websocket: WebSocket | null = null
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null
    let unmounted = false

    const connect = () => {
      if (unmounted) {
        return
      }

      websocket = new WebSocket(WS_TELEMETRY_URL)

      websocket.onopen = () => {
        if (unmounted) {
          return
        }
        setConnectionState('connected')
      }

      websocket.onmessage = (event) => {
        const message = JSON.parse(event.data) as TelemetryUpdate
        onMessageRef.current(message)
      }

      websocket.onerror = () => {
        if (unmounted) {
          return
        }
        setConnectionState('reconnecting')
      }

      websocket.onclose = () => {
        if (unmounted) {
          return
        }
        setConnectionState('reconnecting')
        reconnectTimer = setTimeout(connect, WS_RECONNECT_DELAY_MS)
      }
    }

    connect()

    return () => {
      unmounted = true
      if (reconnectTimer) {
        clearTimeout(reconnectTimer)
      }
      websocket?.close()
      setConnectionState('disconnected')
    }
  }, [enabled])

  return { connectionState }
}
