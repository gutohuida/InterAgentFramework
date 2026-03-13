"""
AgentWeave - Multi-agent AI collaboration framework.

File-based protocol for N AI agents (Claude, Kimi, Gemini, Codex, etc.)
to collaborate through a shared .agentweave/ directory.
"""

try:
    from importlib.metadata import version as _pkg_version, PackageNotFoundError as _PNF

    __version__ = _pkg_version("agentweave")
except _PNF:
    __version__ = "0.5.0"  # fallback during development / editable installs
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
