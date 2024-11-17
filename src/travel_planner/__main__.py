import asyncio
import argparse
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from .agents.weather_agent import WeatherAgent
from .agents.flight_agent import FlightAgent
from .agents.hotel_agent import HotelAgent
from .agents.travel_planner_agent import TravelPlannerAgent
from .config import get_settings
from .utils.logger import logger
from .utils.exceptions import CityValidationError, ServiceError

# Initialize colorama
init()

def validate_date(date_str: str) -> str:
    """Validate date format and ensure it's not in the past."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        if date < today:
            raise ValueError("Date cannot be in the past")
        if date > today + timedelta(days=365):
            raise ValueError("Date cannot be more than 1 year in the future")
        return date_str
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))

def setup_argparse():
    """Setup command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Travel Planner - Get weather, flights, and hotel information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m travel_planner
  python -m travel_planner -o "London" -d "Paris" -D 2024-12-01
  python -m travel_planner --origin "New York" --destination "Tokyo" --date 2024-12-25
  python -m travel_planner --no-weather --no-hotels  # Skip weather and hotel search
        """
    )
    
    parser.add_argument(
        "-o", "--origin",
        default="San Francisco",
        help="Origin city (default: San Francisco)"
    )
    
    parser.add_argument(
        "-d", "--destination",
        default="New York",
        help="Destination city (default: New York)"
    )
    
    parser.add_argument(
        "-D", "--date",
        type=validate_date,
        default=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        help="Travel date in YYYY-MM-DD format (default: 7 days from today)"
    )
    
    parser.add_argument(
        "--no-weather",
        action="store_true",
        help="Skip weather information"
    )
    
    parser.add_argument(
        "--no-flights",
        action="store_true",
        help="Skip flight search"
    )
    
    parser.add_argument(
        "--no-hotels",
        action="store_true",
        help="Skip hotel search"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Minimal output (errors only)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    return parser

def print_weather(weather_forecast):
    """Print weather information with formatting."""
    print(f"\n{Fore.CYAN}=== Current Weather ==={Style.RESET_ALL}")
    print(f"Temperature: {Fore.YELLOW}{weather_forecast.temperature}°C{Style.RESET_ALL}")
    print(f"Condition: {Fore.YELLOW}{weather_forecast.condition}{Style.RESET_ALL}")
    print(f"Precipitation: {Fore.YELLOW}{weather_forecast.precipitation_chance}mm{Style.RESET_ALL}")

def print_flights(flight_options):
    """Print flight information with formatting."""
    if not flight_options:
        print(f"\n{Fore.YELLOW}No flights found for this route{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}=== Flight Options ==={Style.RESET_ALL}")
    for i, flight in enumerate(flight_options, 1):
        print(f"\n{Fore.GREEN}Flight Option {i}:{Style.RESET_ALL}")
        print(f"Departure: {Fore.YELLOW}{flight.departure_time}{Style.RESET_ALL}")
        print(f"Arrival: {Fore.YELLOW}{flight.arrival_time}{Style.RESET_ALL}")
        print(f"Price: {Fore.YELLOW}${flight.price}{Style.RESET_ALL}")
        print(f"Stops: {Fore.YELLOW}{flight.stops}{Style.RESET_ALL}")

def print_hotels(hotel_options):
    """Print hotel information with formatting."""
    if not hotel_options:
        print(f"\n{Fore.YELLOW}No hotels found at this destination{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}=== Hotel Options ==={Style.RESET_ALL}")
    for i, hotel in enumerate(hotel_options, 1):
        print(f"\n{Fore.GREEN}Hotel Option {i}:{Style.RESET_ALL}")
        print(f"Name: {Fore.YELLOW}{hotel.name}{Style.RESET_ALL}")
        print(f"Rating: {Fore.YELLOW}{'⭐' * int(hotel.rating)}{Style.RESET_ALL}")
        print(f"Price per night: {Fore.YELLOW}${hotel.price_per_night}{Style.RESET_ALL}")
        print(f"Location: {Fore.YELLOW}{hotel.location}{Style.RESET_ALL}")
        print(f"Amenities: {Fore.YELLOW}{', '.join(hotel.amenities)}{Style.RESET_ALL}")

async def main():
    parser = setup_argparse()
    args = parser.parse_args()
    
    try:
        settings = get_settings()
        
        # Initialize only required agents
        agents = {}
        if not args.no_weather:
            agents['weather'] = WeatherAgent()
        if not args.no_flights:
            agents['flight'] = FlightAgent()
        if not args.no_hotels:
            agents['hotel'] = HotelAgent()
        
        # Initialize travel planner with available agents
        travel_planner = TravelPlannerAgent(
            weather_agent=agents.get('weather'),
            flight_agent=agents.get('flight'),
            hotel_agent=agents.get('hotel')
        )
        
        if not args.quiet:
            print(f"\n{Fore.CYAN}Searching travel options...{Style.RESET_ALL}")
            print(f"From: {Fore.YELLOW}{args.origin}{Style.RESET_ALL}")
            print(f"To: {Fore.YELLOW}{args.destination}{Style.RESET_ALL}")
            print(f"Date: {Fore.YELLOW}{args.date}{Style.RESET_ALL}\n")
        
        # Plan a trip
        plan = await travel_planner.execute(
            origin=args.origin,
            destination=args.destination,
            date=args.date
        )
        
        if args.json:
            import json
            print(json.dumps(plan.dict(), indent=2, default=str))
            return
        
        # Display results based on service availability and user preferences
        if not args.quiet:
            for service, status in plan.service_status.items():
                if not status.status:
                    print(f"{Fore.RED}⚠️ {service.title()} service error: {status.error}{Style.RESET_ALL}")
            
            if not args.no_weather and plan.service_status["weather"].status:
                print_weather(plan.weather_forecast)
            
            if not args.no_flights and plan.service_status["flights"].status:
                print_flights(plan.flight_options)
            
            if not args.no_hotels and plan.service_status["hotels"].status:
                print_hotels(plan.hotel_options)
        
        logger.info("trip_planning_completed",
                   origin=args.origin,
                   destination=args.destination,
                   services_used={k: v.status for k, v in plan.service_status.items()})
        
    except CityValidationError as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please check the city names and try again.{Style.RESET_ALL}")
        logger.error("city_validation_error", error=str(e))
        return 1
        
    except ServiceError as e:
        print(f"\n{Fore.RED}Service Error: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please try again later.{Style.RESET_ALL}")
        logger.error("service_error", error=str(e))
        return 1
        
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
        logger.error("main_error", error=str(e))
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
        exit(1)