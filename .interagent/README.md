# InterAgent Session: Test

**ID:** session-685251  
**Mode:** hierarchical  
**Principal:** claude

## Quick Commands

```bash
# Check status
interagent status

# Create task
interagent task create --title "Task name" --assignee kimi

# List tasks
interagent task list

# Quick delegation
interagent quick --to kimi "Implement auth"

# Check inbox
interagent inbox --agent kimi

# Get relay prompt
interagent relay --to kimi

# Summary
interagent summary
```

## Files

- `session.json` - Session configuration
- `agents/` - Agent status
- `tasks/active/` - Active tasks
- `tasks/completed/` - Completed tasks
- `messages/pending/` - Unread messages
- `messages/archive/` - Message history
- `shared/` - Shared context and decisions
