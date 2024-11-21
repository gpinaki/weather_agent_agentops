from abc import ABC, abstractmethod
from typing import Any
from functools import wraps
import agentops

def monitor_agent(func):
    """Decorator to monitor agent execution with proper multi-session support"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        agent_name = self.__class__.__name__
        
        # Create a new session specific to this agent execution
        current_session = agentops.start_session(tags=[f"agent:{agent_name}"])
        
        try:
            # Record the input parameters using this specific session
            current_session.record(
                agentops.ActionEvent(
                    action_type=f"{agent_name}_input",
                    params=str({"args": args, "kwargs": kwargs})
                )
            )
            
            # Execute the agent
            result = await func(self, *args, **kwargs)
            
            # Record the successful result using this specific session
            current_session.record(
                agentops.ActionEvent(
                    action_type=f"{agent_name}_output",
                    returns=str(result)
                )
            )
            
            # End this specific session
            current_session.end_session("Success")
            return result
            
        except Exception as e:
            # Record the failure using this specific session
            current_session.record(
                agentops.ActionEvent(
                    action_type=f"{agent_name}_error",
                    returns=str(e)
                )
            )
            current_session.end_session("Fail")
            raise

    return wrapper

class BaseAgent(ABC):
    """Base class for all agents in the travel planner system."""
    
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