# InterAgent

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/interagent-framework.svg)](https://badge.fury.io/py/interagent-framework)

> **A collaboration framework for Claude Code and Kimi Code**

InterAgent lets Claude Code and Kimi Code work together on the same project — on the same machine or across machines. After a one-time setup, you orchestrate everything through **natural language prompts** — no manual CLI commands required during your session.

---

## How It Works

InterAgent creates a shared `.interagent/` directory that both agents use as a communication channel. The user acts as the messenger, passing relay prompts between agents.

```
You (setup once)
  └─ interagent init --project "My App" --principal claude

You (natural language)
  └─ "Claude, delegate the auth module to Kimi"

Claude (runs CLI via Bash automatically)
  └─ interagent quick --to kimi "Implement auth module"
  └─ interagent relay --agent kimi
  └─ [shows you the relay prompt to paste into Kimi]

You
  └─ paste relay prompt into Kimi Code

Kimi (reads AGENTS.md + context.md, runs CLI via terminal)
  └─ interagent task update <id> --status in_progress
  └─ [does the work]
  └─ interagent task update <id> --status completed
  └─ interagent msg send --to claude --subject "Done" --message "..."

You
  └─ "Claude, Kimi is done"

Claude (runs CLI via Bash automatically)
  └─ interagent inbox --agent claude
  └─ interagent summary
  └─ [reviews Kimi's work and continues]
```

**The only manual step is pasting the relay prompt into Kimi.** Both agents handle all CLI commands themselves — you just have a conversation.

---

## Quick Start

### 1. Install

```bash
pip install interagent-framework
```

### 2. Initialize (once per project)

```bash
cd your-project/
interagent init --project "My App" --principal claude
```

This creates:
- `.interagent/AGENTS.md` — full collaboration guide that both agents read on startup
- `.interagent/shared/context.md` — fill this with your project description
- `.interagent/session.json` — session state

### 3. Fill in project context

Edit `.interagent/shared/context.md` and paste in your project description, current state, and any constraints. Both agents read this at the start of every task.

### 4. Start working — just prompt Claude

From this point, use natural language. Claude handles the CLI:

> "Claude, read `.interagent/AGENTS.md` to understand how we're collaborating,
> then delegate the database schema design to Kimi."

Claude will run `interagent quick` and `interagent relay` via Bash, then show you a prompt to paste into Kimi Code.

---

## Cross-Machine Collaboration (v0.2.0+)

By default, InterAgent works on a single machine via the local `.interagent/` directory. If your collaborator is on a different machine, enable **Git transport** with one command:

```bash
interagent transport setup --type git
```

This creates an orphan branch (`interagent/collab`) on your git remote. Messages and tasks are synced through it using git plumbing — your working tree and current branch are never touched.

### How to set up cross-machine

```bash
# Both developers run this (same git remote required):
interagent transport setup --type git --remote origin

# Check status
interagent transport status

# Force-fetch latest messages
interagent transport pull

# Revert to local-only
interagent transport disable
```

All existing commands (`quick`, `inbox`, `relay`, `task`, etc.) work identically — transport is transparent.

### Start watching for incoming messages

```bash
interagent-watch
```

Automatically adapts to the active transport. For git transport, polls every 10 seconds instead of 5.

---

## Commands Reference

### Session

```bash
interagent init --project "Name" --principal claude   # Initialize
interagent status                                      # Full status
interagent summary                                     # Quick overview
```

### Delegation

```bash
interagent quick --to kimi "Task description"         # Create + assign task
interagent relay --agent kimi                         # Generate relay prompt
interagent relay --agent claude                       # Generate relay for Claude
```

### Tasks

```bash
interagent task list                                  # List all tasks
interagent task show <task_id>                        # View task details
interagent task update <task_id> --status in_progress
interagent task update <task_id> --status completed
interagent task update <task_id> --status approved
interagent task update <task_id> --status needs_revision --note "Fix X"
```

### Messaging

```bash
interagent inbox --agent claude                       # Check Claude's inbox
interagent inbox --agent kimi                         # Check Kimi's inbox
interagent msg send --to claude --subject "Done" --message "Implemented X"
```

### Transport (cross-machine)

```bash
interagent transport setup --type git                 # Enable git transport
interagent transport status                           # Show active transport
interagent transport pull                             # Force immediate fetch
interagent transport disable                          # Revert to local
```

### Template Maintenance

```bash
interagent update-template --agent claude --template-path ~/projects/template.txt
interagent update-template --agent claude --focus "sub-agents"
```

---

## What Gets Created on Init

```
.interagent/
├── AGENTS.md             # Collaboration guide — both agents read this
├── README.md             # Quick command reference
├── session.json          # Session config (id, mode, principal)
├── shared/
│   └── context.md        # Project state — fill this with your project description
├── tasks/
│   ├── active/           # JSON files for each active task
│   └── completed/        # Archived completed tasks
├── messages/
│   ├── pending/          # Unread messages
│   └── archive/          # Message history
└── agents/               # Agent status files
```

`.interagent/AGENTS.md` is the key file. Both Claude and Kimi read it on every session start to understand their roles, available commands, and the collaboration protocol.

---

## Prompt-First Workflow

### Delegating to Kimi

Just tell Claude what to assign. No CLI needed.

**You → Claude:**
> "Delegate the user authentication module to Kimi. It should include login, logout,
> JWT tokens, and password reset. See PLAN.md for the API design."

**Claude does automatically:**
```bash
interagent quick --to kimi "Implement user authentication: login, logout, JWT tokens, password reset. See PLAN.md §3 for API design."
interagent relay --agent kimi
```

**Claude shows you:**
```
====================================================================
RELAY PROMPT FOR KIMI
====================================================================
Copy and paste this to the agent:

@kimi - You have work in the InterAgent collaboration system.

Your role: delegate
Collaboration guide: read .interagent/AGENTS.md for commands, workflow, and protocol.
Project context: read .interagent/shared/context.md before starting.

[TASK] You have 1 new task(s):
   - Implement user authentication (task-a3f2c1)
...
====================================================================
```

**You:** paste that into Kimi Code.

---

### Getting Kimi's Work Back to Claude

When Kimi is done:

**You → Claude:**
> "Kimi is done."

**Claude does automatically:**
```bash
interagent inbox --agent claude
interagent summary
```

---

## Safety Features

**File locking** — prevents race conditions when both agents work simultaneously. Tasks and messages use file-based mutexes with a 5-minute automatic timeout.

**Schema validation** — all JSON state files are validated before saving. Agent names, task statuses, and required fields are enforced.

**Input sanitization** — string length limits and type coercion before any write.

**Conflict-free git sync** — GitTransport appends files with UUID-suffixed names; two machines can never produce the same filename. Push conflicts are retried automatically.

---

## Roles

| Role | Agent | Responsibilities |
|---|---|---|
| Principal | Claude | Architecture, planning, review, final decisions |
| Delegate | Kimi | Implementation, execution, reporting back |

In hierarchical mode (default), Claude assigns work and reviews results.
In peer mode, both agents can assign tasks to each other.

---

## Roadmap

| Phase | Status | Description |
|---|---|---|
| Local transport | Done | Single-machine via `.interagent/` filesystem |
| Git transport | Done (v0.2.0) | Cross-machine via orphan branch, zero infra |
| InterAgent Hub | Planned | MCP server for multi-team collaboration, web dashboard |

The Hub (Phase 3) will be an **MCP server** — Claude Code and Kimi Code connect to it as a native MCP tool provider, enabling real-time delivery without polling and a web dashboard for project oversight. See [ROADMAP.md](ROADMAP.md) for the full plan.

---

## Installation Options

```bash
# From PyPI
pip install interagent-framework

# From source
git clone https://github.com/gutohuida/InterAgentFramework.git
cd InterAgentFramework
pip install -e .
```

---

## FAQ

**Q: Do I need to run CLI commands during my session?**
No. After `interagent init`, just talk to Claude. It runs all `interagent` commands via Bash automatically. The only manual step is pasting the relay prompt into Kimi.

**Q: How does Kimi know how to use the system?**
`interagent init` writes `.interagent/AGENTS.md` — a complete guide covering commands, workflow, and protocol. The relay prompt tells Kimi to read it before starting work.

**Q: Should I commit `.interagent/` to Git?**
Partially. The `.gitignore` excludes runtime state (tasks, messages, session.json, transport.json) but keeps AGENTS.md and README.md. This gives you documentation without committing transient data.

**Q: Can I use this with just Claude (no Kimi)?**
Yes — just skip the relay step. The session, task, and summary commands are useful even for single-agent projects to track progress.

**Q: Do both developers need the same git remote for cross-machine sync?**
Yes. Git transport requires a shared remote (e.g. `origin`). One developer runs `interagent transport setup --type git` to create the orphan branch, then the other runs the same command to connect to it.

**Q: What if Kimi doesn't have terminal access?**
The relay prompt includes the task details inline, so Kimi can read and respond without running any commands. The collaboration is less structured but still works.

---

## Links

- **GitHub:** https://github.com/gutohuida/InterAgentFramework
- **PyPI:** https://pypi.org/project/interagent-framework/
- **Issues:** https://github.com/gutohuida/InterAgentFramework/issues
- **Roadmap:** [ROADMAP.md](ROADMAP.md)

---

MIT License
