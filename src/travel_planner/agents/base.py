from abc import ABC, abstractmethod
from typing import Any

class BaseAgent(ABC):
    """
    Base class for all agents in the travel planner system.
    """
    @abstractmethod
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