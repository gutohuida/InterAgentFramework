import { useState } from 'react'
import { MessageSquare } from 'lucide-react'
import { useMessages, useMessageHistory, Message } from '@/api/messages'
import { MessageCard } from './MessageCard'
import { ConversationGroup } from './ConversationGroup'
import { EmptyState } from '@/components/common/EmptyState'

type Mode = 'inbox' | 'history'

function convKey(msg: Message): string {
  return [msg.from, msg.to].sort().join(':')
}

export function MessagesFeed() {
  const [mode, setMode] = useState<Mode>('inbox')
  const [agentFilter, setAgentFilter] = useState<string | undefined>(undefined)
  const [sort, setSort] = useState<'asc' | 'desc'>('asc')
  const [grouped, setGrouped] = useState(false)

  const { data: inboxMessages, isLoading: inboxLoading } = useMessages(agentFilter)
  const { data: historyMessages, isLoading: historyLoading } = useMessageHistory({ sort })

  const isLoading = mode === 'inbox' ? inboxLoading : historyLoading
  const messages = mode === 'inbox' ? inboxMessages : historyMessages

  // Agent filter pills from history (all participants)
  const { data: allMessages } = useMessageHistory({})
  const agents = [...new Set(allMessages?.flatMap((m) => [m.from, m.to]) ?? [])]

  // Build grouped view for history mode
  const groupedMessages: Record<string, Message[]> = {}
  if (grouped && messages) {
    for (const msg of messages) {
      const key = convKey(msg)
      ;(groupedMessages[key] ??= []).push(msg)
    }
  }

  if (isLoading) {
    return <div className="p-6 text-sm text-muted-foreground">Loading messages…</div>
  }

  return (
    <div className="flex flex-col gap-4 p-6">
      {/* Mode toggle */}
      <div className="flex items-center gap-3 flex-wrap">
        <div className="flex rounded-lg border overflow-hidden text-sm">
          {(['inbox', 'history'] as Mode[]).map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={`px-3 py-1.5 capitalize transition-colors ${
                mode === m ? 'bg-primary text-primary-foreground' : 'bg-muted hover:bg-accent text-muted-foreground'
              }`}
            >
              {m}
            </button>
          ))}
        </div>

        {mode === 'inbox' && (
          <>
            <button
              onClick={() => setAgentFilter(undefined)}
              className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                agentFilter === undefined ? 'bg-primary text-primary-foreground' : 'bg-muted hover:bg-accent'
              }`}
            >
              All
            </button>
            {agents.map((agent) => (
              <button
                key={agent}
                onClick={() => setAgentFilter(agent)}
                className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                  agentFilter === agent ? 'bg-primary text-primary-foreground' : 'bg-muted hover:bg-accent'
                }`}
              >
                {agent}
              </button>
            ))}
          </>
        )}

        {mode === 'history' && (
          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={() => setSort(sort === 'asc' ? 'desc' : 'asc')}
              className="rounded-full px-3 py-1 text-xs font-medium bg-muted hover:bg-accent transition-colors"
            >
              {sort === 'asc' ? 'Oldest first' : 'Newest first'}
            </button>
            <button
              onClick={() => setGrouped(!grouped)}
              className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                grouped ? 'bg-primary text-primary-foreground' : 'bg-muted hover:bg-accent'
              }`}
            >
              Group by conversation
            </button>
          </div>
        )}
      </div>

      {/* Content */}
      {!messages || messages.length === 0 ? (
        <EmptyState
          icon={MessageSquare}
          title={mode === 'inbox' ? 'No messages' : 'No message history'}
          description="Messages between agents will appear here."
        />
      ) : mode === 'history' && grouped ? (
        <div className="space-y-6">
          {Object.entries(groupedMessages).map(([key, msgs]) => (
            <ConversationGroup key={key} pairKey={key} messages={msgs} />
          ))}
        </div>
      ) : (
        <div className="space-y-3">
          {messages.map((msg) => (
            <MessageCard key={msg.id} message={msg} />
          ))}
        </div>
      )}
    </div>
  )
}
