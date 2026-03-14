import { formatDistanceToNow } from 'date-fns'
import { AgentSummary } from '@/api/agents'
import { cn } from '@/lib/utils'

const STATUS_COLORS: Record<string, string> = {
  active: 'bg-green-500',
  idle: 'bg-gray-400',
  waiting: 'bg-yellow-400',
}

interface AgentCardProps {
  agent: AgentSummary
  selected: boolean
  onClick: () => void
}

export function AgentCard({ agent, selected, onClick }: AgentCardProps) {
  const dotColor = STATUS_COLORS[agent.status] ?? 'bg-gray-400'

  return (
    <button
      onClick={onClick}
      className={cn(
        'w-full text-left rounded-lg border p-3 transition-colors',
        selected
          ? 'bg-primary/10 border-primary/30'
          : 'hover:bg-accent border-transparent'
      )}
    >
      <div className="flex items-center gap-2">
        <span className={`h-2.5 w-2.5 rounded-full shrink-0 ${dotColor}`} />
        <span className="font-medium text-sm">{agent.name}</span>
        <span className="ml-auto text-xs text-muted-foreground capitalize">{agent.status}</span>
      </div>
      <div className="mt-1 flex gap-3 text-xs text-muted-foreground">
        <span>{agent.message_count} msgs</span>
        <span>{agent.active_task_count} tasks</span>
        {agent.last_seen && (
          <span className="ml-auto">
            {formatDistanceToNow(new Date(agent.last_seen), { addSuffix: true })}
          </span>
        )}
      </div>
      {agent.latest_status_msg && (
        <p className="mt-1 text-xs text-muted-foreground truncate">{agent.latest_status_msg}</p>
      )}
    </button>
  )
}
