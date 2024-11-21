from functools import lru_cache
from pydantic_settings import BaseSettings
import agentops

class Settings(BaseSettings):
    openai_api_key: str
    weather_api_key: str
    environment: str = "development"
    weather_api_base_url: str = "http://api.weatherapi.com/v1"
    openai_model: str = "gpt-4-turbo-preview"
    agentops_api_key: str

    class Config:
        env_file = ".env"

    def initialize_agentops(self) -> bool:
        """Initialize AgentOps with default tags and return success status"""
        try:
            # First, check if AgentOps is already initialized
            if not hasattr(agentops, '_initialized'):
                agentops.init(
                    api_key=self.agentops_api_key,
                    default_tags=[
                        f"env:{self.environment}",
                        "app:travel-planner"
                    ]
                )
                setattr(agentops, '_initialized', True)
            return True
        except Exception as e:
            print(f"Failed to initialize AgentOps: {str(e)}")
            return False

@lru_cache()
def get_settings():
    settings = Settings()
    settings.initialize_agentops()
    return settings
