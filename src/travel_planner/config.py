from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    weather_api_key: str
    environment: str = "development"
    weather_api_base_url: str = "http://api.weatherapi.com/v1"
    openai_model: str = "gpt-4-turbo-preview"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()