"""Shared types for claw-cog."""

from typing import Any, Protocol


class Subscriber(Protocol):
    """Protocol for global workspace subscribers.

    Subscribers are callables that accept content and return a result.
    """

    def __call__(self, content: Any) -> Any: ...
