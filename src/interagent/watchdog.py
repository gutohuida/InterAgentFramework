"""Watchdog script for monitoring new messages and tasks."""

import time
import sys
from pathlib import Path
from typing import Set, Callable

from .constants import MESSAGES_PENDING_DIR, TASKS_ACTIVE_DIR
from .utils import load_json


class Watchdog:
    """Monitors the .interagent directory for changes."""
    
    def __init__(self, callback: Callable = None, poll_interval: float = 5.0):
        """Initialize watchdog.
        
        Args:
            callback: Function to call when changes detected
            poll_interval: How often to check (seconds)
        """
        self.callback = callback or self._default_callback
        self.poll_interval = poll_interval
        self.known_messages: Set[str] = set()
        self.known_tasks: Set[str] = set()
        self.running = False
    
    def _default_callback(self, event_type: str, data: dict):
        """Default callback that prints to stdout."""
        if event_type == "new_message":
            print(f"\n📬 New message for {data['to']} from {data['from']}")
            print(f"   Subject: {data.get('subject', '(no subject)')}")
            print(f"   Run: interagent inbox --agent {data['to']}")
            print()
        elif event_type == "new_task":
            print(f"\n📋 New task assigned to {data.get('assignee', 'unknown')}")
            print(f"   Title: {data.get('title', 'Untitled')}")
            print(f"   Run: interagent task show {data['id']}")
            print()
        elif event_type == "task_completed":
            print(f"\n✅ Task completed: {data.get('title', 'Untitled')}")
            print(f"   Ready for review!")
            print()
    
    def _scan_messages(self) -> Set[str]:
        """Scan for message files."""
        messages = set()
        if MESSAGES_PENDING_DIR.exists():
            for msg_file in MESSAGES_PENDING_DIR.glob("*.json"):
                messages.add(msg_file.stem)
        return messages
    
    def _scan_tasks(self) -> Set[str]:
        """Scan for task files."""
        tasks = set()
        if TASKS_ACTIVE_DIR.exists():
            for task_file in TASKS_ACTIVE_DIR.glob("*.json"):
                tasks.add(task_file.stem)
        return tasks
    
    def _get_message_info(self, msg_id: str) -> dict:
        """Get message info."""
        msg_file = MESSAGES_PENDING_DIR / f"{msg_id}.json"
        return load_json(msg_file) or {}
    
    def _get_task_info(self, task_id: str) -> dict:
        """Get task info."""
        task_file = TASKS_ACTIVE_DIR / f"{task_id}.json"
        return load_json(task_file) or {}
    
    def start(self):
        """Start watching."""
        print("👁️  InterAgent Watchdog started")
        print(f"   Watching: {MESSAGES_PENDING_DIR}")
        print(f"   Watching: {TASKS_ACTIVE_DIR}")
        print(f"   Poll interval: {self.poll_interval}s")
        print("   Press Ctrl+C to stop\n")
        
        # Initial scan
        self.known_messages = self._scan_messages()
        self.known_tasks = self._scan_tasks()
        
        self.running = True
        
        try:
            while self.running:
                self._check_once()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            print("\n\n👋 Watchdog stopped")
    
    def _check_once(self):
        """Check for changes once."""
        # Check messages
        current_messages = self._scan_messages()
        new_messages = current_messages - self.known_messages
        
        for msg_id in new_messages:
            msg_data = self._get_message_info(msg_id)
            self.callback("new_message", msg_data)
        
        self.known_messages = current_messages
        
        # Check tasks
        current_tasks = self._scan_tasks()
        new_tasks = current_tasks - self.known_tasks
        
        for task_id in new_tasks:
            task_data = self._get_task_info(task_id)
            self.callback("new_task", task_data)
        
        self.known_tasks = current_tasks
    
    def stop(self):
        """Stop watching."""
        self.running = False


def main():
    """CLI entry point for watchdog."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Watch for InterAgent changes",
    )
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=5.0,
        help="Poll interval in seconds (default: 5)",
    )
    
    args = parser.parse_args()
    
    watchdog = Watchdog(poll_interval=args.interval)
    watchdog.start()


if __name__ == "__main__":
    main()
