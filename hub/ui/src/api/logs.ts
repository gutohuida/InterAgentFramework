import { useQuery } from '@tanstack/react-query'
import { getJson } from './client'
import { useConfigStore } from '@/store/configStore'

export interface EventLogEntry {
  id: string
  project_id: string
  event_type: string
  agent?: string
  data?: Record<string, unknown>
  timestamp: string
}

export interface LogsOpts {
  agent?: string
  event_type?: string
  since?: string
  live?: boolean
}

export function useLogs(opts: LogsOpts = {}) {
  const { isConfigured } = useConfigStore()
  const params = new URLSearchParams()
  if (opts.agent) params.set('agent', opts.agent)
  if (opts.event_type) params.set('event_type', opts.event_type)
  if (opts.since) params.set('since', opts.since)
  params.set('limit', '200')
  return useQuery<EventLogEntry[]>({
    queryKey: ['logs', opts],
    queryFn: () => getJson<EventLogEntry[]>(`/api/v1/logs?${params}`),
    enabled: isConfigured,
    refetchInterval: opts.live ? 2000 : false,
  })
}
