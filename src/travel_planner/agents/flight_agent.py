from .base import BaseAgent
from openai import AsyncOpenAI
from typing import List
from ..schemas.models import FlightOption
from ..config import get_settings
from ..utils.logger import logger
from ..utils.validators import CityValidator
import json

class FlightAgent(BaseAgent):
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        self.city_validator = CityValidator(self.settings.weather_api_key)
    
    async def execute(self, origin: str, destination: str, date: str) -> List[FlightOption]:
        try:
            # Validate cities first
            origin_valid, origin_msg = await self.city_validator.validate_city(origin)
            dest_valid, dest_msg = await self.city_validator.validate_city(destination)

            if not origin_valid or not dest_valid:
                error_msg = []
                if not origin_valid:
                    error_msg.append(f"Invalid origin city: {origin}")
                if not dest_valid:
                    error_msg.append(f"Invalid destination city: {destination}")
                raise ValueError(" && ".join(error_msg))

            # Use validated city names
            origin = origin_msg
            destination = dest_msg

            system_prompt = """You are a flight search assistant. 
            IMPORTANT: Generate realistic flight options based on these rules:
            1. Flight durations should be realistic based on distance
            2. Prices should be realistic for the route
            3. Number of stops should make sense for the distance
            4. Early morning and late evening flights are more common
            5. Prices should vary based on time of day
            
            Provide flight options in JSON format with the following structure:
            {
                "flights": [
                    {
                        "departure_time": "HH:MM",
                        "arrival_time": "HH:MM",
                        "price": float,
                        "stops": integer
                    }
                ]
            }"""

            response = await self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Find flights from {origin} to {destination} on {date}. If this route is not realistic or cities are too small for direct flights, respond with empty flights array."}
                ],
                response_format={"type": "json_object"}
            )
            
            flight_data = json.loads(response.choices[0].message.content)
            
            if not flight_data.get("flights"):
                logger.info(f"No flights found for route: {origin} to {destination}")
                return []
                
            return [FlightOption(**flight) for flight in flight_data["flights"]]
                
        except Exception as e:
            logger.error("flight_search_error", error=str(e))
            raise