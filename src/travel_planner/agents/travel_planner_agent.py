from typing import Optional, List
import asyncio
from .base import BaseAgent
from .weather_agent import WeatherAgent
from .flight_agent import FlightAgent
from .hotel_agent import HotelAgent
from ..schemas.models import TravelPlan, WeatherForecast, FlightOption, HotelOption, ServiceStatus
from ..utils.logger import logger
from agentops import track_agent, record_tool


@track_agent(name="TravelPlannerAgent")
class TravelPlannerAgent(BaseAgent):
    def __init__(
        self,
        weather_agent: WeatherAgent,
        flight_agent: FlightAgent,
        hotel_agent: HotelAgent
    ):
        self.weather_agent = weather_agent
        self.flight_agent = flight_agent
        self.hotel_agent = hotel_agent

    @record_tool(tool_name="execute")
    async def execute(
        self,
        origin: str,
        destination: str,
        date: str
    ) -> TravelPlan:
        try:
            # Execute all agents concurrently
            weather_task = self.weather_agent.execute(destination, date)
            flights_task = self.flight_agent.execute(origin, destination, date)
            hotels_task = self.hotel_agent.execute(destination, date)

            results = await asyncio.gather(
                weather_task, flights_task, hotels_task,
                return_exceptions=True
            )

            service_statuses = {
                "weather": ServiceStatus(),
                "flights": ServiceStatus(),
                "hotels": ServiceStatus()
            }

            # Process weather result
            if isinstance(results[0], Exception):
                service_statuses["weather"].error = str(results[0])
                weather_forecast = WeatherForecast()
            else:
                service_statuses["weather"].status = True
                weather_forecast = results[0]

            # Process flight result
            if isinstance(results[1], Exception):
                service_statuses["flights"].error = str(results[1])
                flight_options = []
            else:
                service_statuses["flights"].status = True
                flight_options = results[1]

            # Process hotel result
            if isinstance(results[2], Exception):
                service_statuses["hotels"].error = str(results[2])
                hotel_options = []
            else:
                service_statuses["hotels"].status = True
                hotel_options = results[2]

            # Create travel plan
            plan = TravelPlan(
                weather_forecast=weather_forecast,
                flight_options=flight_options,
                hotel_options=hotel_options,
                service_status=service_statuses
            )

            return plan

        except Exception as e:
            logger.error("trip_planning_error", error=str(e))
            raise
