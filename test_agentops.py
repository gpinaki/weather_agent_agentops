import asyncio
import os
from dotenv import load_dotenv
import agentops
from travel_planner.config import get_settings
from travel_planner.agents.weather_agent import WeatherAgent
from travel_planner.agents.flight_agent import FlightAgent
from travel_planner.agents.hotel_agent import HotelAgent

async def test_weather_agent():
    try:
        print("\nTesting Weather Agent...")
        # Create a session specifically for this test
        session = agentops.start_session(tags=["test:weather"])
        
        agent = WeatherAgent()
        result = await agent.execute("London", "2024-12-25")
        print("Weather Agent Test - Success:")
        print(result)
        
        session.end_session("Success")
        return True
    except Exception as e:
        print(f"Weather Agent Test - Failed: {str(e)}")
        if 'session' in locals():
            session.end_session("Fail")
        return False

async def test_flight_agent():
    try:
        print("\nTesting Flight Agent...")
        session = agentops.start_session(tags=["test:flight"])
        
        agent = FlightAgent()
        result = await agent.execute("London", "Paris", "2024-12-25")
        print("Flight Agent Test - Success:")
        print(result)
        
        session.end_session("Success")
        return True
    except Exception as e:
        print(f"Flight Agent Test - Failed: {str(e)}")
        if 'session' in locals():
            session.end_session("Fail")
        return False

async def test_hotel_agent():
    try:
        print("\nTesting Hotel Agent...")
        session = agentops.start_session(tags=["test:hotel"])
        
        agent = HotelAgent()
        result = await agent.execute("Paris", "2024-12-25")
        print("Hotel Agent Test - Success:")
        print(result)
        
        session.end_session("Success")
        return True
    except Exception as e:
        print(f"Hotel Agent Test - Failed: {str(e)}")
        if 'session' in locals():
            session.end_session("Fail")
        return False

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize settings (which will initialize AgentOps)
    settings = get_settings()
    print("Settings initialized")
    
    # Create main test session
    main_session = agentops.start_session(tags=["test:main"])
    
    try:
        # Run tests sequentially to avoid session conflicts
        results = []
        results.append(await test_weather_agent())
        results.append(await test_flight_agent())
        results.append(await test_hotel_agent())
        
        # Print summary
        print("\n=== Test Summary ===")
        test_names = ["Weather", "Flight", "Hotel"]
        for name, result in zip(test_names, results):
            status = "Success" if result else "Failed"
            print(f"{name} Agent Test: {status}")
        
        main_session.end_session("Success")
            
    except Exception as e:
        print(f"Test suite failed: {str(e)}")
        if 'main_session' in locals():
            main_session.end_session("Fail")
        raise
    
def verify_session_state():
    """Helper function to verify AgentOps session state"""
    try:
        # Try to get current session info
        session = agentops.start_session(tags=["test:verify"])
        print("AgentOps session test: Success")
        session.end_session("Success")
        return True
    except Exception as e:
        print(f"AgentOps session test failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(main())