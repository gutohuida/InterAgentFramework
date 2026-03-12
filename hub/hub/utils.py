"""Shared utilities for the Hub package."""

import uuid


def short_id() -> str:
    """Return an 8-character random hex ID segment."""
    return str(uuid.uuid4())[:8]
