"""
AgentWeave - Multi-agent AI collaboration framework.

File-based protocol for N AI agents (Claude, Kimi, Gemini, Codex, etc.)
to collaborate through a shared .agentweave/ directory.
"""

__version__ = "0.4.0"
__author__ = "AgentWeave Team"

from .cli import main
from .session import Session
from .task import Task, TaskStatus
from .messaging import Message, MessageBus

__all__ = [
    "main",
    "Session",
    "Task",
    "TaskStatus",
    "Message",
    "MessageBus",
]
