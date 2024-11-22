from .base import BaseAgent
from openai import AsyncOpenAI
from typing import List
from ..schemas.models import HotelOption
from ..config import get_settings
from ..utils.logger import logger
from ..utils.validators import CityValidator
import json
from agentops import track_agent, record_tool


@track_agent(name="HotelAgent")
class HotelAgent(BaseAgent):
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        self.city_validator = CityValidator(self.settings.weather_api_key)

    @record_tool(tool_name="execute")
    async def execute(self, city: str, date: str) -> List[HotelOption]:
        try:
            # Validate city first
            is_valid, validated_city = await self.city_validator.validate_city(city)

            if not is_valid:
                raise ValueError(f"Invalid city: {city}")

            # Use validated city name
            city = validated_city

            system_prompt = """You are a hotel recommendation assistant. 
            IMPORTANT: Generate realistic hotel options based on these rules:
            1. Only suggest hotels for cities that actually exist
            2. Prices should reflect the city's cost of living
            3. Ratings should be realistic (not all hotels are 5-star)
            4. Location descriptions should be specific to the city
            5. Amenities should be realistic for the hotel's rating
            
            Provide hotel options in JSON format with the following structure:
            {
                "hotels": [
                    {
                        "name": "Hotel Name",
                        "rating": float (1-5),
                        "price_per_night": float,
                        "location": "area in city",
                        "amenities": ["amenity1", "amenity2", ...]
                    }
                ]
            }"""

            response = await self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Find hotels in {city} for stay on {date}. If this city is too small or not suitable for tourism, respond with empty hotels array."}
                ],
                response_format={"type": "json_object"}
            )

            hotel_data = json.loads(response.choices[0].message.content)

            if not hotel_data.get("hotels"):
                logger.info(f"No hotels found for city: {city}")
                return []

            return [HotelOption.from_api_response(hotel) for hotel in hotel_data["hotels"]]

        except Exception as e:
            logger.error("hotel_search_error", error=str(e))
            raise
