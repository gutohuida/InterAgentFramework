import { useEffect, useRef, useState } from 'react'
import { useLogs } from '@/api/logs'
import { LogLine } from './LogLine'

const EVENT_TYPES = [
  'message_created', 'message_read',
  'task_created', 'task_updated',
  'question_asked', 'question_answered',
  'agent_heartbeat',
]

export function LogsView() {
  const [agentFilter, setAgentFilter] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const [live, setLive] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  const { data: entries = [], isLoading } = useLogs({
    agent: agentFilter || undefined,
    event_type: typeFilter || undefined,
    live,
  })

  // Auto-scroll when live mode is on and new entries arrive
  useEffect(() => {
    if (live) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [entries, live])

  return (
    <div className="flex flex-col h-full">
      {/* Top bar */}
      <div className="flex items-center gap-3 px-4 py-3 border-b bg-background flex-wrap">
        <input
          type="text"
          placeholder="Filter by agent…"
          value={agentFilter}
          onChange={(e) => setAgentFilter(e.target.value)}
          className="h-8 rounded-md border bg-muted px-3 text-sm w-36 focus:outline-none focus:ring-1 focus:ring-primary"
        />
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="h-8 rounded-md border bg-muted px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="">All event types</option>
          {EVENT_TYPES.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
        <button
          onClick={() => setLive(!live)}
          className={`ml-auto rounded-full px-3 py-1 text-xs font-medium transition-colors ${
            live ? 'bg-green-500 text-white' : 'bg-muted hover:bg-accent text-muted-foreground'
          }`}
        >
          {live ? 'Live' : 'Paused'}
        </button>
      </div>

      {/* Log body */}
      <div className="flex-1 overflow-auto bg-gray-950 p-3">
        {isLoading ? (
          <p className="font-mono text-xs text-gray-500 p-2">Loading…</p>
        ) : entries.length === 0 ? (
          <p className="font-mono text-xs text-gray-500 p-2">No events yet. Create messages or tasks to see activity here.</p>
        ) : (
          entries.map((entry) => <LogLine key={entry.id} entry={entry} />)
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
