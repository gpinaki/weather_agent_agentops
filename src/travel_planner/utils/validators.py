import requests
from typing import Tuple, Optional
from ..utils.logger import logger

class CityValidator:
    def __init__(self, weather_api_key: str):
        self.api_key = weather_api_key
        self.base_url = "http://api.weatherapi.com/v1"
        self.valid_cities_cache = {}  # Cache validation results

    async def validate_city(self, city: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if a city exists using WeatherAPI.
        Returns (is_valid, error_message)
        """
        if city in self.valid_cities_cache:
            return self.valid_cities_cache[city], None

        try:
            # Use weather API to validate city
            response = requests.get(
                f"{self.base_url}/current.json",
                params={
                    "key": self.api_key,
                    "q": city
                }
            )

            if response.status_code == 200:
                data = response.json()
                validated_city = f"{data['location']['name']}, {data['location']['country']}"
                self.valid_cities_cache[city] = True
                return True, validated_city
            else:
                error_msg = f"Invalid city: {city}"
                self.valid_cities_cache[city] = False
                return False, error_msg

        except Exception as e:
            logger.error(f"City validation error: {str(e)}")
            return False, f"Error validating city: {str(e)}"