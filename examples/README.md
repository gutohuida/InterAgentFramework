# InterAgent Examples

This directory contains example scripts demonstrating how to use InterAgent.

---

## 📁 Available Examples

### Python API Examples

| Example | Description | Run |
|---------|-------------|-----|
| `basic_workflow.py` | Complete workflow: init, tasks, messages, reviews | `python basic_workflow.py` |
| `parallel_workflow.py` | Parallel work: agents working simultaneously | `python parallel_workflow.py` |

### CLI Examples

| Example | Description | Run |
|---------|-------------|-----|
| `cli_session.sh` | Bash script with CLI commands | `bash cli_session.sh` |
| `cli_session.bat` | Windows batch script | `cli_session.bat` |

---

## 🚀 Running Examples

### Prerequisites

```bash
# Install InterAgent
pip install -e ..

# Or if already installed
pip install interagent
```

### Python Examples

```bash
# Basic workflow
cd examples
python basic_workflow.py

# Parallel workflow
python parallel_workflow.py
```

### CLI Examples

```bash
# Linux/Mac
cd examples
bash cli_session.sh

# Windows
cli_session.bat
```

---

## 📖 Example Scenarios

### Scenario 1: Simple Task Delegation

```python
from interagent import Session, Task

# Initialize
session = Session.create("My Project", principal="claude")
session.save()

# Create task for Kimi
task = Task.create(
    title="Implement feature",
    assignee="kimi",
    priority="high",
)
task.save()

# Update status
task.update(status="in_progress")
task.save()

# Complete
task.update(status="completed")
task.save()
```

### Scenario 2: Code Review Workflow

```python
from interagent import Task, Message, MessageBus

# Kimi completes work
task = Task.load("task-xxx")
task.update(status="completed")
task.save()

# Kimi requests review
msg = Message.create(
    sender="kimi",
    recipient="claude",
    subject="Review Request",
    content="Please review my implementation",
    message_type="review",
    task_id=task.id,
)
MessageBus.send(msg)

# Claude reviews and approves
claude_msgs = MessageBus.get_inbox("claude")
for msg in claude_msgs:
    msg.mark_read()

task.update(status="approved")
task.save()
```

### Scenario 3: Using CLI

```bash
# Initialize
interagent init --project "API" --principal claude

# Create task
interagent task create --title "Design" --assignee kimi

# Check status
interagent status

# Send message
interagent msg send --to kimi --message "Task assigned!"
```

---

## 🎓 Learning Path

1. **Start with `basic_workflow.py`**
   - Understand the core concepts
   - See how Session, Task, and Message work together

2. **Try `cli_session.sh`**
   - Learn the CLI commands
   - See the file structure created

3. **Explore `parallel_workflow.py`**
   - See how agents work in parallel
   - Understand task dependencies

---

## 📝 Creating Your Own Examples

Template for new examples:

```python
#!/usr/bin/env python3
"""
Example: [Name]

[Description of what this example demonstrates]
"""

from interagent import Session, Task, Message, MessageBus


def main():
    # Your example code here
    pass


if __name__ == "__main__":
    main()
```

---

## 🔗 Related Documentation

- [Main README](../README.md)
- [Python API Documentation](../docs/api.md) (if available)
- [CLI Reference](../docs/cli.md) (if available)

---

**Have an interesting example?** Submit a PR!
