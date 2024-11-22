from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Dict, Optional

import agentops

from .config import get_settings


class MonitoringConfig:
    """Centralized monitoring configuration for the travel planner."""

    def __init__(self):
        self._initialized = False
        self._enabled = True
        self.settings = get_settings()
        self._active_session = None

    def initialize(self) -> None:
        """Initialize AgentOps with API key from settings."""
        if not self._initialized:
            try:
                agentops.init()
                self._initialized = True
            except Exception as e:
                print(f"Warning: Failed to initialize AgentOps: {e}")
                self._enabled = False

    @property
    def enabled(self) -> bool:
        """Check if monitoring is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable monitoring."""
        self._enabled = value

    @contextmanager
    def session(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        """Context manager for AgentOps sessions."""
        if not self._enabled:
            yield None
            return

        try:
            self.initialize()
            session = agentops.Session(
                name=name,
                metadata=metadata or {}
            )
            self._active_session = session
            yield session
        except Exception as e:
            print(f"Warning: Failed to create monitoring session: {e}")
            yield None
        finally:
            self._active_session = None

    def track_agent(self, name: str) -> Callable:
        """Decorator for tracking agent operations."""
        def decorator(cls):
            if not self._enabled:
                return cls

            try:
                return agentops.track_agent(name=name)(cls)
            except Exception as e:
                print(f"Warning: Failed to track agent {name}: {e}")
                return cls
        return decorator

    def record_action(self, action_name: str) -> Callable:
        """Decorator for recording agent actions."""
        def decorator(func):
            if not self._enabled:
                return func

            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    # Convert non-serializable objects to strings in kwargs
                    serializable_kwargs = {
                        k: str(v) if not isinstance(
                            v, (str, int, float, bool, list, dict)) else v
                        for k, v in kwargs.items()
                    }

                    with agentops.record_action(
                        action_name,
                        metadata=serializable_kwargs
                    ):
                        return await func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"Warning: Failed to record action {action_name}: {e}")
                    return await func(*args, **kwargs)
            return wrapper
        return decorator

    @property
    def current_session(self) -> Optional[agentops.Session]:
        """Get the current active session."""
        return self._active_session


# Create a singleton instance
monitoring = MonitoringConfig()

# Export common decorators
track_agent = monitoring.track_agent
record_action = monitoring.record_action
