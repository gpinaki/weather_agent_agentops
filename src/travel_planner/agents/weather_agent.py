from .base import BaseAgent
import requests
from ..schemas.models import WeatherForecast
from ..config import get_settings
from ..utils.logger import logger
from ..utils.validators import CityValidator
from ..utils.exceptions import CityValidationError, ServiceError

class WeatherAgent(BaseAgent):
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.weather_api_key
        self.base_url = self.settings.weather_api_base_url
        self.city_validator = CityValidator(self.api_key)
        
        if not self.api_key or self.api_key == "your_weather_api_key":
            raise ValueError("Weather API key not found in environment variables")
    
    async def execute(self, destination: str, date: str) -> WeatherForecast:
        try:
            # First validate the city
            is_valid, validated_city = await self.city_validator.validate_city(destination)
            
            if not is_valid:
                raise CityValidationError(f"'{destination}' is not a valid city name. Please check the spelling and try again.")

            endpoint = f"{self.base_url}/current.json"
            params = {
                "key": self.api_key,
                "q": validated_city  # Use the validated city name
            }
            
            logger.info("calling_weather_api", 
                       destination=validated_city,
                       endpoint=endpoint)
            
            response = requests.get(endpoint, params=params)
            
            if response.status_code != 200:
                raise ServiceError(f"Weather service error (Status: {response.status_code})")
            
            data = response.json()
            
            if "current" not in data:
                raise ServiceError("Invalid response from Weather API")
            
            current = data["current"]
            condition = current.get("condition", {})
            
            return WeatherForecast(
                temperature=current.get("temp_c", 0.0),
                condition=condition.get("text", "Unknown"),
                precipitation_chance=current.get("precip_mm", 0.0)
            )
                
        except CityValidationError as e:
            logger.warning(f"Invalid city: {destination}", error=str(e))
            raise
        except requests.exceptions.ConnectionError:
            raise ServiceError("Unable to connect to weather service. Please check your internet connection.")
        except requests.exceptions.Timeout:
            raise ServiceError("Weather service request timed out. Please try again.")
        except Exception as e:
            logger.error("weather_api_error", error=str(e))
            raise ServiceError("An unexpected error occurred while fetching weather data.")