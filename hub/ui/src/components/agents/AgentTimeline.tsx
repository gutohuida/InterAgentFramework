import { formatDistanceToNow } from 'date-fns'
import { MessageSquare, CheckSquare, Zap } from 'lucide-react'
import { AgentSummary, useAgentTimeline } from '@/api/agents'

function iconForType(type: string) {
  if (type === 'message') return MessageSquare
  if (type.startsWith('task')) return CheckSquare
  return Zap
}

interface AgentTimelineProps {
  agent: AgentSummary
}

export function AgentTimeline({ agent }: AgentTimelineProps) {
  const { data: events = [], isLoading } = useAgentTimeline(agent.name)

  return (
    <div className="flex flex-col h-full overflow-auto p-4 gap-4">
      {/* Current activity banner */}
      {agent.latest_status_msg && (
        <div className="rounded-lg border border-primary/30 bg-primary/5 px-4 py-3">
          <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
            <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
            Current activity
          </div>
          <p className="text-sm">{agent.latest_status_msg}</p>
        </div>
      )}

      {/* Timeline */}
      <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Timeline</h3>
      {isLoading ? (
        <p className="text-sm text-muted-foreground">Loading…</p>
      ) : events.length === 0 ? (
        <p className="text-sm text-muted-foreground">No timeline events yet.</p>
      ) : (
        <div className="space-y-3">
          {events.map((event) => {
            const Icon = iconForType(event.event_type)
            return (
              <div key={event.id} className="flex items-start gap-3 text-sm">
                <Icon className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-xs uppercase tracking-wide text-muted-foreground">
                    {event.event_type}
                  </p>
                  <p className="text-sm truncate">{event.summary}</p>
                </div>
                <span className="text-xs text-muted-foreground whitespace-nowrap shrink-0">
                  {formatDistanceToNow(new Date(event.timestamp), { addSuffix: true })}
                </span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
