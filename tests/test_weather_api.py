import asyncio

from dotenv import load_dotenv

from src.travel_planner.agents.weather_agent import WeatherAgent


async def test_weather():
    # Initialize the weather agent
    weather_agent = WeatherAgent()
    
    try:
        # Test current weather
        forecast = await weather_agent.execute(
            city="New York",
            date="2024-12-01"
        )
        
        print("\nWeather Forecast Results:")
        print(f"Temperature: {forecast.temperature}°C")
        print(f"Condition: {forecast.condition}")
        print(f"Precipitation Chance: {forecast.precipitation_chance}%")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run the test
    asyncio.run(test_weather())