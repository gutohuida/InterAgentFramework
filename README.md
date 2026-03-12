# AgentWeave

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/agentweave-ai.svg)](https://badge.fury.io/py/agentweave-ai)

> **A collaboration framework for N AI agents — Claude, Kimi, Gemini, Codex, and more**

AgentWeave lets multiple AI agents work together on the same project. Agents communicate through a shared `.agentweave/` directory and a local MCP server. With MCP enabled, agents call `send_message` and `get_inbox` as native tools — **no manual relay needed**.

---

## Two Modes

### Mode 1 — Manual relay (zero extra setup)

The original mode. You paste a relay prompt from Claude into Kimi, and back. Works with no dependencies beyond the base package.

### Mode 2 — Zero-relay with MCP (recommended)

Install the MCP extras, run two background watchers, and agents communicate autonomously. The loop:

```
Claude sends message via send_message tool
  → watchdog detects it
  → fires: kimi --print -p "check your inbox"
  → Kimi calls get_inbox, reads it, replies via send_message
  → watchdog detects it
  → fires: claude -p "check your inbox"
  → Claude reads and continues
```

**You only interact with Claude** — the human never relays anything.

---

## Quick Start

### 1. Install

```bash
# Base package (manual relay mode)
pip install agentweave-ai

# With MCP server (zero-relay mode)
pip install "agentweave-ai[mcp]"
```

### 2. Initialize (once per project)

```bash
cd your-project/
agentweave init --project "My App" --agents claude,kimi
```

Creates:
- `AI_CONTEXT.md` (project root) — project DNA: stack, architecture, code standards (static, rarely changes)
- `.agentweave/AGENTS.md` — collaboration protocol: MCP vs manual mode, workflow (per-session)
- `.agentweave/ROLES.md` — agent role assignments: who does what (per-session)
- `.agentweave/shared/context.md` — current focus: what's being worked on today (changes daily)

**Supported agents:** claude, kimi, gemini, codex, aider, cline, cursor, windsurf, copilot, and any name matching `^[a-zA-Z0-9_-]{1,32}$`

### 3. Fill in project context

**AI_CONTEXT.md** — Fill this once with your project's fundamentals:
- Project overview, tech stack, essential commands
- Architecture, directory structure
- Code standards and workflow conventions

**shared/context.md** — Update this daily with current state:
- What phase you're in, what's being worked on
- Recent decisions, blockers, next steps

Agents read all four files on session start.

### 4a. Start working — manual relay mode

Just prompt Claude. It runs all `agentweave` CLI commands via Bash automatically:

> "Claude, delegate the database schema design to Kimi."

Claude runs `agentweave quick` and `agentweave relay`, then shows you a prompt to paste into Kimi Code. When Kimi is done, tell Claude and it reads the reply.

### 4b. Start working — zero-relay MCP mode

**One-time MCP setup:**

```bash
# Configure the MCP server in both agents (auto-detects claude and kimi CLI)
agentweave mcp setup
```

Or manually:

```bash
claude mcp add agentweave -- agentweave-mcp
kimi mcp add --transport stdio agentweave -- agentweave-mcp
```

**Start the watchers** (two terminals, keep them running):

```bash
# Terminal 1 — notifies Claude when Kimi sends a message
agentweave-watch --auto-ping --agent claude

# Terminal 2 — notifies Kimi when Claude sends a message
agentweave-watch --auto-ping --agent kimi
```

**Now just prompt Claude.** It uses `send_message` and `get_task` as native MCP tools. When it sends a message to Kimi, the watchdog fires `kimi --print -p "check inbox"` automatically, and the loop continues without you.

---

## MCP Tools Reference

Once configured, both agents have these tools available natively:

| Tool | What it does |
|---|---|
| `send_message(from_agent, to_agent, subject, content)` | Send a message to another agent |
| `get_inbox(agent)` | Read unread messages |
| `mark_read(message_id)` | Archive a message after processing |
| `list_tasks(agent?)` | List active tasks, optionally filtered |
| `get_task(task_id)` | Get full task details |
| `update_task(task_id, status)` | Update task status |
| `create_task(title, description, assignee, ...)` | Create and assign a new task |
| `get_status()` | Session summary + task counts |

---

## Commands Reference

### Session

```bash
agentweave init --project "Name" --principal claude   # Initialize
agentweave status                                      # Full status
agentweave summary                                     # Quick overview
```

### Delegation (manual relay mode)

```bash
agentweave quick --to kimi "Task description"         # Create + assign task
agentweave relay --agent kimi                         # Generate relay prompt
```

### Tasks

```bash
agentweave task list                                  # List all tasks
agentweave task show <task_id>                        # View task details
agentweave task update <task_id> --status in_progress
agentweave task update <task_id> --status completed
agentweave task update <task_id> --status approved
agentweave task update <task_id> --status revision_needed --note "Fix X"
```

### Messaging

```bash
agentweave inbox --agent claude                       # Check Claude's inbox
agentweave msg send --to claude --subject "Done" --message "Implemented X"
```

### MCP server

```bash
agentweave mcp setup                                  # Configure in Claude + Kimi (once)
agentweave-mcp                                        # Run the MCP server (stdio)
```

### Watchdog

```bash
agentweave-watch                                      # Monitor + print notifications
agentweave-watch --auto-ping --agent claude           # Auto-notify Claude on new messages
agentweave-watch --auto-ping --agent kimi             # Auto-notify Kimi on new messages
agentweave-watch --interval 3                         # Custom poll interval (seconds)
```

### Transport (cross-machine)

```bash
agentweave transport setup --type git                 # Enable git transport
agentweave transport status                           # Show active transport
agentweave transport pull                             # Force immediate fetch
agentweave transport disable                          # Revert to local
```

### Template Maintenance

```bash
agentweave update-template --agent claude --template-path ~/projects/template.txt
agentweave update-template --agent claude --focus "sub-agents"
```

---

## Cross-Machine Collaboration

By default, AgentWeave works on a single machine. For cross-machine sync, enable **git transport**:

```bash
# Both developers run this (same git remote required)
agentweave transport setup --type git --cluster alice   # your workspace name
```

This creates an orphan branch (`agentweave/collab`) on your git remote. Messages and tasks sync through it using git plumbing — your working tree and current branch are never touched.

Messages are stamped `alice.claude → bob.kimi` so multiple workspaces can share the same remote.

The MCP server works transparently with all transports — it calls `get_transport()` internally.

---

## Task Status Lifecycle

```
pending → assigned → in_progress → completed → under_review → approved
                                             ↘ revision_needed (loops back)
                                             ↘ rejected
```

---

## What Gets Created on Init

### Project Root
```
AI_CONTEXT.md             # Project DNA — stack, architecture, standards (static)
```

### .agentweave/ Directory
```
.agentweave/
├── AGENTS.md             # Collaboration protocol — MCP vs manual, workflow
├── ROLES.md              # Agent role assignments — who owns what domain
├── README.md             # Quick command reference
├── session.json          # Session config (gitignored)
├── shared/
│   └── context.md        # Current state — today's focus, recent decisions (dynamic)
├── tasks/
│   ├── active/           # JSON files for each active task (gitignored)
│   └── completed/        # Archived completed tasks (gitignored)
└── messages/
    ├── pending/          # Unread messages (gitignored)
    └── archive/          # Message history (gitignored)
```

### File Purposes

| File | Question It Answers | Change Frequency |
|------|---------------------|------------------|
| `AI_CONTEXT.md` | What is this project? (stack, architecture, commands) | Monthly |
| `AGENTS.md` | How do we collaborate? (MCP vs manual, workflow) | Per session |
| `ROLES.md` | Who does what? (role assignments) | Per session |
| `shared/context.md` | What are we doing today? (focus, decisions, blockers) | Daily |

---

## Safety Features

**File locking** — prevents race conditions when both agents write simultaneously. Tasks and messages use file-based mutexes with a 5-minute automatic timeout.

**Schema validation** — all JSON state files are validated before saving. Agent names, task statuses, and required fields are enforced.

**Input sanitization** — string length limits and type coercion before any write.

**Conflict-free git sync** — GitTransport appends files with UUID-suffixed names; two machines can never produce the same filename.

---

## Roles

| Role | Example Agents | Responsibilities |
|---|---|---|
| Principal | claude | Architecture, planning, review, final decisions |
| Delegate 1 | kimi | Backend implementation |
| Delegate 2 | gemini | Frontend development |
| Delegate 3 | codex | Testing, DevOps |

In hierarchical mode (default), the principal assigns work and reviews results. In peer mode, agents can assign tasks to each other.

Roles are defined in `.agentweave/ROLES.md` — edit this file to customize responsibilities.

---

## Roadmap

| Phase | Status | Description |
|---|---|---|
| Local transport | Done | Single-machine via `.agentweave/` filesystem |
| Git transport | Done (v0.2.0) | Cross-machine via orphan branch, zero infra |
| N-agent support | Done (v0.3.0) | Multi-agent teams with ROLES.md and cluster naming |
| Local MCP server | Done (v0.4.0) | Native tool integration, zero-relay with watchdog pinger |
| AgentWeave Hub | Planned | Hosted MCP server, multi-team, web dashboard |

The Hub (next phase) will be a **hosted MCP server** — any agent connects via HTTP, enabling real-time delivery without polling and a web dashboard for oversight. See [ROADMAP.md](ROADMAP.md) for the full plan.

---

## Installation Options

```bash
# From PyPI — base (manual relay mode)
pip install agentweave-ai

# From PyPI — with MCP server (zero-relay mode)
pip install "agentweave-ai[mcp]"

# From source
git clone https://github.com/gutohuida/AgentWeaveFramework.git
cd AgentWeaveFramework
pip install -e ".[mcp]"
```

---

## FAQ

**Q: Do I need to run CLI commands during my session?**
No. After `agentweave init`, just talk to Claude. It runs all `agentweave` commands via Bash automatically. In MCP mode, even the relay step is automated.

**Q: What's the difference between manual relay and MCP mode?**
In manual mode, you copy-paste a relay prompt from Claude to Kimi. In MCP mode, the watchdog fires a one-liner at the agent's CLI when a message arrives — no human involvement after the watchers are started.

**Q: Do the watchdog processes need to stay running?**
Yes. Run `agentweave-watch --auto-ping --agent <name>` in a terminal (or as a background process / system service) for each agent you want auto-notified. If they're not running, messages still queue up — agents just won't be auto-triggered.

**Q: How do delegate agents know how to use the system?**
`agentweave init` writes `.agentweave/AGENTS.md` — a complete guide covering commands, workflow, and protocol. In MCP mode, agents use the registered tools directly instead of CLI commands.

**Q: Should I commit `.agentweave/` to Git?**
Partially. The `.gitignore` excludes runtime state (tasks, messages, session.json, transport.json) but keeps AGENTS.md and README.md.

**Q: Can I use this with a single agent?**
Yes — skip the relay step. Session, task, and summary commands are useful even for single-agent projects.

**Q: Do both developers need the same git remote for cross-machine sync?**
Yes. Git transport requires a shared remote (e.g. `origin`). One developer creates the orphan branch with `agentweave transport setup --type git`, the other connects with the same command.

---

## Links

- **GitHub:** https://github.com/gutohuida/AgentWeaveFramework
- **PyPI:** https://pypi.org/project/agentweave-ai/
- **Issues:** https://github.com/gutohuida/AgentWeaveFramework/issues
- **Roadmap:** [ROADMAP.md](ROADMAP.md)

---

MIT License
