import { useQuery } from '@tanstack/react-query'
import { getJson } from './client'
import { useConfigStore } from '@/store/configStore'

export interface AgentSummary {
  name: string
  status: string
  latest_status_msg?: string
  last_seen?: string
  message_count: number
  active_task_count: number
}

export interface AgentTimelineEvent {
  id: string
  event_type: string
  timestamp: string
  summary: string
  data: Record<string, unknown>
}

export function useAgents() {
  const { isConfigured } = useConfigStore()
  return useQuery<AgentSummary[]>({
    queryKey: ['agents'],
    queryFn: () => getJson<AgentSummary[]>('/api/v1/agents'),
    enabled: isConfigured,
    refetchInterval: 10000,
  })
}

export function useAgentTimeline(name: string | null) {
  const { isConfigured } = useConfigStore()
  return useQuery<AgentTimelineEvent[]>({
    queryKey: ['agents', name, 'timeline'],
    queryFn: () => getJson<AgentTimelineEvent[]>(`/api/v1/agents/${name}/timeline`),
    enabled: isConfigured && !!name,
    refetchInterval: 5000,
  })
}
