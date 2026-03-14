export function summaryForEvent(type: string, data: Record<string, unknown>): string {
  switch (type) {
    case 'message_created': return `New message from ${data.from} to ${data.to}`
    case 'message_read': return `Message ${data.id} marked as read`
    case 'task_created': return `Task created: ${data.title}`
    case 'task_updated': return `Task ${data.id} → ${data.status}`
    case 'question_asked': return `Question from ${data.from_agent}${data.blocking ? ' (blocking)' : ''}`
    case 'question_answered': return `Question ${data.id} answered`
    case 'agent_heartbeat': return `[${data.status}] ${data.message || ''}`
    default: return type
  }
}
