import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { fetchWithAuth, getJson } from './client'
import { useConfigStore } from '@/store/configStore'

export interface Message {
  id: string
  project_id: string
  from: string
  to: string
  subject?: string
  content: string
  type: string
  timestamp: string
  read: boolean
  read_at?: string
  task_id?: string
}

export function useMessages(agent?: string) {
  const { isConfigured } = useConfigStore()
  const params = agent ? `?agent=${encodeURIComponent(agent)}` : ''
  return useQuery<Message[]>({
    queryKey: ['messages', agent],
    queryFn: () => getJson<Message[]>(`/api/v1/messages${params}`),
    enabled: isConfigured,
  })
}

export interface MessageHistoryOpts {
  sort?: 'asc' | 'desc'
  conversation?: string
}

export function useMessageHistory(opts: MessageHistoryOpts = {}) {
  const { isConfigured } = useConfigStore()
  const params = new URLSearchParams({ history: 'true' })
  if (opts.sort) params.set('sort', opts.sort)
  if (opts.conversation) params.set('conversation', opts.conversation)
  return useQuery<Message[]>({
    queryKey: ['messages', 'history', opts],
    queryFn: () => getJson<Message[]>(`/api/v1/messages?${params}`),
    enabled: isConfigured,
  })
}

export function useMarkRead() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (messageId: string) =>
      fetchWithAuth(`/api/v1/messages/${messageId}/read`, { method: 'PATCH' }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['messages'] }),
  })
}
