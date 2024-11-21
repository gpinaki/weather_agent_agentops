from abc import ABC, abstractmethod
from typing import Any
from functools import wraps
import agentops

def monitor_agent(func):
    """Decorator to monitor agent execution"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        agent_name = self.__class__.__name__
        
        # Get current session from the agent if it exists
        session = getattr(self, '_current_session', None)
        
        if not session:
            # Create a new session if none exists
            self._current_session = agentops.start_session(tags=[f"agent:{agent_name}"])
            session = self._current_session
        
        try:
            # Execute the agent
            result = await func(self, *args, **kwargs)
            
            if session:
                session.end_session("Success")
            
            return result
        except Exception as e:
            if session:
                session.end_session("Fail")
            raise
        finally:
            # Clean up session reference
            if hasattr(self, '_current_session'):
                delattr(self, '_current_session')

    return wrapper

class BaseAgent(ABC):
    """Base class for all agents in the travel planner system."""
    def __init__(self):
        self._current_session = None

    @abstractmethod
    @monitor_agent
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the agent's main functionality.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Any: The result of the agent's execution
        """
        pass