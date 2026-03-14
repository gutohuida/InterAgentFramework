import { format } from 'date-fns'
import { EventLogEntry } from '@/api/logs'
import { summaryForEvent } from '@/lib/eventSummary'

interface LogLineProps {
  entry: EventLogEntry
}

export function LogLine({ entry }: LogLineProps) {
  const ts = format(new Date(entry.timestamp), 'HH:mm:ss')
  const summary = summaryForEvent(entry.event_type, (entry.data ?? {}) as Record<string, unknown>)

  return (
    <div className="flex gap-3 font-mono text-xs leading-5 hover:bg-white/5 px-2 rounded">
      <span className="text-gray-500 shrink-0 w-16">{ts}</span>
      <span className="text-yellow-400 shrink-0 w-32 truncate">{entry.event_type}</span>
      <span className="text-blue-400 shrink-0 w-20 truncate">{entry.agent ?? ''}</span>
      <span className="text-green-300 flex-1 truncate">{summary}</span>
    </div>
  )
}
