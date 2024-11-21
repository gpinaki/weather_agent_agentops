import asyncio
import os
from dotenv import load_dotenv
import agentops
from travel_planner.config import get_settings
from travel_planner.agents.weather_agent import WeatherAgent
from travel_planner.agents.flight_agent import FlightAgent
from travel_planner.agents.hotel_agent import HotelAgent

class TestSession:
    def __init__(self, name):
        self.session = None
        self.name = name

    def __enter__(self):
        if self.session:
            self.session.end_session("Success")
        self.session = agentops.start_session(tags=[f"test:{self.name}"])
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.end_session("Success" if not exc_type else "Fail")
            self.session = None

async def test_weather_agent(parent_session):
    try:
        print("\nTesting Weather Agent...")
        with TestSession("weather") as session:
            # Record in parent session
            parent_session.record(
                agentops.ActionEvent(
                    action_type="weather_test_start",
                    params="Starting weather agent test"
                )
            )
            
            agent = WeatherAgent()
            result = await agent.execute("London", "2024-12-25")
            print("Weather Agent Test - Success:")
            print(result)
            
            # Record success in parent session
            parent_session.record(
                agentops.ActionEvent(
                    action_type="weather_test_complete",
                    returns=str(result)
                )
            )
            return True
    except Exception as e:
        print(f"Weather Agent Test - Failed: {str(e)}")
        parent_session.record(
            agentops.ActionEvent(
                action_type="weather_test_error",
                returns=str(e)
            )
        )
        return False

async def test_flight_agent(parent_session):
    try:
        print("\nTesting Flight Agent...")
        with TestSession("flight") as session:
            # Record in parent session
            parent_session.record(
                agentops.ActionEvent(
                    action_type="flight_test_start",
                    params="Starting flight agent test"
                )
            )
            
            agent = FlightAgent()
            result = await agent.execute("London", "Paris", "2024-12-25")
            print("Flight Agent Test - Success:")
            print(result)
            
            # Record success in parent session
            parent_session.record(
                agentops.ActionEvent(
                    action_type="flight_test_complete",
                    returns=str(result)
                )
            )
            return True
    except Exception as e:
        print(f"Flight Agent Test - Failed: {str(e)}")
        parent_session.record(
            agentops.ActionEvent(
                action_type="flight_test_error",
                returns=str(e)
            )
        )
        return False

async def test_hotel_agent(parent_session):
    try:
        print("\nTesting Hotel Agent...")
        with TestSession("hotel") as session:
            # Record in parent session
            parent_session.record(
                agentops.ActionEvent(
                    action_type="hotel_test_start",
                    params="Starting hotel agent test"
                )
            )
            
            agent = HotelAgent()
            result = await agent.execute("Paris", "2024-12-25")
            print("Hotel Agent Test - Success:")
            print(result)
            
            # Record success in parent session
            parent_session.record(
                agentops.ActionEvent(
                    action_type="hotel_test_complete",
                    returns=str(result)
                )
            )
            return True
    except Exception as e:
        print(f"Hotel Agent Test - Failed: {str(e)}")
        parent_session.record(
            agentops.ActionEvent(
                action_type="hotel_test_error",
                returns=str(e)
            )
        )
        return False

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize settings (which will initialize AgentOps)
    settings = get_settings()
    print("Settings initialized")
    
    # Create main test session using context manager
    with TestSession("main") as main_session:
        try:
            # Record start of testing
            main_session.record(
                agentops.ActionEvent(
                    action_type="test_suite_start",
                    params="Starting agent tests"
                )
            )
            
            # Run tests sequentially, passing the main session
            results = []
            results.append(await test_weather_agent(main_session))
            results.append(await test_flight_agent(main_session))
            results.append(await test_hotel_agent(main_session))
            
            # Print summary
            print("\n=== Test Summary ===")
            test_names = ["Weather", "Flight", "Hotel"]
            for name, result in zip(test_names, results):
                status = "Success" if result else "Failed"
                print(f"{name} Agent Test: {status}")
                
            # Record final results
            main_session.record(
                agentops.ActionEvent(
                    action_type="test_suite_complete",
                    returns=str(dict(zip(test_names, results)))
                )
            )
            
        except Exception as e:
            print(f"Test suite failed: {str(e)}")
            main_session.record(
                agentops.ActionEvent(
                    action_type="test_suite_error",
                    returns=str(e)
                )
            )
            raise

if __name__ == "__main__":
    asyncio.run(main())