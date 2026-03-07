"""Session management for InterAgent."""

from typing import Any, Dict, List, Optional

from .constants import SESSION_FILE, VALID_AGENTS, VALID_MODES
from .utils import load_json, save_json, generate_id, now_iso


class Session:
    """Manages an inter-agent collaboration session."""

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """Initialize session with data."""
        self._data = data or {}

    @property
    def id(self) -> str:
        """Get session ID."""
        return self._data.get("id", "unknown")

    @property
    def name(self) -> str:
        """Get session name."""
        return self._data.get("name", "Unnamed Session")

    @property
    def mode(self) -> str:
        """Get collaboration mode."""
        return self._data.get("mode", "hierarchical")

    @property
    def principal(self) -> str:
        """Get principal agent."""
        return self._data.get("principal", "claude")

    @property
    def agents(self) -> Dict[str, Dict[str, Any]]:
        """Get agent configurations."""
        return self._data.get("agents", {})

    def get_agent_role(self, agent: str) -> str:
        """Get role for an agent."""
        return self.agents.get(agent, {}).get("role", "delegate")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self._data

    @classmethod
    def load(cls) -> Optional["Session"]:
        """Load session from file."""
        data = load_json(SESSION_FILE)
        if data:
            return cls(data)
        return None

    def save(self) -> bool:
        """Save session to file."""
        return save_json(SESSION_FILE, self._data)

    @classmethod
    def create(
        cls,
        name: str,
        principal: str = "claude",
        mode: str = "hierarchical",
    ) -> "Session":
        """Create a new session."""
        if principal not in VALID_AGENTS:
            raise ValueError(f"Invalid principal: {principal}")
        if mode not in VALID_MODES:
            raise ValueError(f"Invalid mode: {mode}")

        agents = {}
        for agent in VALID_AGENTS:
            agents[agent] = {
                "role": "principal" if agent == principal else "delegate",
                "since": now_iso(),
            }

        data = {
            "id": generate_id("session"),
            "name": name,
            "created": now_iso(),
            "updated": now_iso(),
            "mode": mode,
            "principal": principal,
            "agents": agents,
            "active_tasks": [],
            "completed_tasks": [],
            "discussions": [],
        }

        return cls(data)

    def update(self, **kwargs) -> None:
        """Update session fields."""
        self._data.update(kwargs)
        self._data["updated"] = now_iso()

    def add_task(self, task_id: str) -> None:
        """Add task to active tasks."""
        tasks = self._data.get("active_tasks", [])
        if task_id not in tasks:
            tasks.append(task_id)
            self._data["active_tasks"] = tasks

    def complete_task(self, task_id: str) -> None:
        """Move task from active to completed."""
        active = self._data.get("active_tasks", [])
        completed = self._data.get("completed_tasks", [])
        
        if task_id in active:
            active.remove(task_id)
            completed.append(task_id)
            self._data["active_tasks"] = active
            self._data["completed_tasks"] = completed

    def get_summary(self) -> Dict[str, Any]:
        """Get session summary."""
        return {
            "id": self.id,
            "name": self.name,
            "mode": self.mode,
            "principal": self.principal,
            "agents": self.agents,
            "active_tasks_count": len(self._data.get("active_tasks", [])),
            "completed_tasks_count": len(self._data.get("completed_tasks", [])),
        }
