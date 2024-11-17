import asyncio
from src.travel_planner.agents.weather_agent import WeatherAgent
from src.travel_planner.agents.flight_agent import FlightAgent
from src.travel_planner.agents.travel_planner_agent import TravelPlannerAgent

async def get_travel_info(origin: str, destination: str, date: str):
    # Initialize agents
    weather_agent = WeatherAgent()
    flight_agent = FlightAgent()
    
    # Initialize travel planner
    travel_planner = TravelPlannerAgent(
        weather_agent=weather_agent,
        flight_agent=flight_agent
    )
    
    # Get travel plan
    plan = await travel_planner.execute(
        origin=origin,
        destination=destination,
        date=date
    )
    
    return plan

# Example usage
async def main():
    plan = await get_travel_info(
        origin="Boston",
        destination="Chicago",
        date="2024-12-01"
    )
    
    # Access the results
    print(f"Weather: {plan.weather_forecast.temperature}°C, {plan.weather_forecast.condition}")
    for flight in plan.flight_options:
        print(f"Flight: ${flight.price} at {flight.departure_time}")

if __name__ == "__main__":
    asyncio.run(main())