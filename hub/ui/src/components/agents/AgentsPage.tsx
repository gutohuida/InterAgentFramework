import { useState } from 'react'
import { Bot } from 'lucide-react'
import { useAgents } from '@/api/agents'
import { AgentCard } from './AgentCard'
import { AgentTimeline } from './AgentTimeline'
import { EmptyState } from '@/components/common/EmptyState'

export function AgentsPage() {
  const { data: agents = [], isLoading } = useAgents()
  const [selected, setSelected] = useState<string | null>(null)
  const selectedAgent = agents.find((a) => a.name === selected) ?? null

  if (isLoading) {
    return <div className="p-6 text-sm text-muted-foreground">Loading agents…</div>
  }

  if (agents.length === 0) {
    return (
      <EmptyState
        icon={Bot}
        title="No agents detected"
        description="Agents appear here once they send messages or are assigned tasks in the last 24 hours."
      />
    )
  }

  return (
    <div className="flex h-full overflow-hidden">
      {/* Left panel — agent list */}
      <div className="w-1/3 border-r overflow-auto p-3 space-y-1">
        {agents.map((agent) => (
          <AgentCard
            key={agent.name}
            agent={agent}
            selected={selected === agent.name}
            onClick={() => setSelected(agent.name)}
          />
        ))}
      </div>

      {/* Right panel — timeline */}
      <div className="flex-1 overflow-auto">
        {selectedAgent ? (
          <AgentTimeline agent={selectedAgent} />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
            Select an agent to view their timeline.
          </div>
        )}
      </div>
    </div>
  )
}
