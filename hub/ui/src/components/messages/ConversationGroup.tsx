import { Message } from '@/api/messages'
import { MessageCard } from './MessageCard'

interface ConversationGroupProps {
  pairKey: string
  messages: Message[]
}

export function ConversationGroup({ pairKey, messages }: ConversationGroupProps) {
  const [a, b] = pairKey.split(':')
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wide">
        <span className="text-foreground">{a}</span>
        <span>↔</span>
        <span className="text-foreground">{b}</span>
        <span className="ml-1 rounded-full bg-muted px-2 py-0.5 text-xs font-normal normal-case">
          {messages.length} message{messages.length !== 1 ? 's' : ''}
        </span>
      </div>
      <div className="space-y-2 pl-2 border-l-2 border-muted">
        {messages.map((msg) => (
          <MessageCard key={msg.id} message={msg} />
        ))}
      </div>
    </div>
  )
}
