import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import plotly.express as px
import streamlit as st

from travel_planner.agents.flight_agent import FlightAgent
from travel_planner.agents.hotel_agent import HotelAgent
from travel_planner.agents.travel_planner_agent import TravelPlannerAgent
from travel_planner.agents.weather_agent import WeatherAgent
from travel_planner.config import get_settings
from travel_planner.utils.exceptions import (CityValidationError, ServiceError,
                                             WeatherServiceError)

import agentops

# Add the src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

# Weather icons mapping
WEATHER_ICONS = {
    "clear": "☀️",
    "sunny": "☀️",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "mist": "🌫️",
    "fog": "🌫️",
    "rain": "🌧️",
    "light rain": "🌧️",
    "heavy rain": "⛈️",
    "snow": "🌨️",
    "sleet": "🌨️",
    "thunderstorm": "⛈️"
}

def get_weather_icon(condition: str) -> str:
    """Get weather icon based on condition description."""
    condition_lower = condition.lower()
    for key, icon in WEATHER_ICONS.items():
        if key in condition_lower:
            return icon
    return "🌤️"  # default icon

def init_session_state():
    """Initialize session state variables."""
    if 'settings' not in st.session_state:
        st.session_state.settings = get_settings()
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'last_search' not in st.session_state:
        st.session_state.last_search = None

def initialize_agents():
    """Initialize travel planning agents."""
    try:
        weather_agent = WeatherAgent()
        flight_agent = FlightAgent()
        hotel_agent = HotelAgent()
        travel_planner = TravelPlannerAgent(
            weather_agent=weather_agent,
            flight_agent=flight_agent,
            hotel_agent=hotel_agent
        )
        return travel_planner
    except Exception as e:
        st.error(f"Failed to initialize agents: {str(e)}")
        return None

def format_weather_card(weather_data):
    """Format weather information with icons and metrics."""
    if weather_data:
        icon = get_weather_icon(weather_data.condition)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label=f"{icon} Temperature",
                value=f"{weather_data.temperature}°C",
                delta=f"{weather_data.precipitation_chance}mm precipitation"
            )
        with col2:
            st.info(f"Condition: {weather_data.condition}")
    else:
        st.error("Weather data unavailable")

def format_flight_card(flight):
    """Format flight information with pricing and details."""
    try:
        price_display = f"${flight.price:,.2f}" if flight.price else "Price not available"
    except:
        price_display = "Price not available"

    with st.expander(f"✈️ Flight: {flight.departure_time} - {price_display}"):
        if flight.departure_time:
            st.write(f"🛫 Departure: {flight.departure_time}")
        if flight.arrival_time:
            st.write(f"🛬 Arrival: {flight.arrival_time}")
        st.write(f"💰 Price: {price_display}")
        st.write(f"🛑 Stops: {flight.stops}")

def format_hotel_card(hotel):
    """Format hotel information with rating and amenities."""
    try:
        price_display = f"${hotel.price_per_night:,.2f}/night"
    except:
        price_display = "Price not available"

    with st.expander(f"🏨 {hotel.name} - {price_display}"):
        # Rating stars
        st.write("⭐" * int(hotel.rating))
        
        # Location with map emoji
        st.write(f"📍 Location: {hotel.location}")
        
        # Price
        st.write(f"💰 Price: {price_display}")
        
        # Amenities with icons
        amenities_icons = {
            "pool": "🏊‍♂️",
            "wifi": "📶",
            "restaurant": "🍽️",
            "gym": "💪",
            "spa": "💆‍♂️",
            "parking": "🅿️",
            "bar": "🍸"
        }
        
        st.write("✨ Amenities:")
        for amenity in hotel.amenities:
            icon = next((v for k, v in amenities_icons.items() if k in amenity.lower()), "•")
            st.write(f"{icon} {amenity}")

def show_search_history():
    """Display search history in a collapsible section."""
    if st.session_state.search_history:
        with st.expander("🕒 Search History"):
            for search in reversed(st.session_state.search_history[-5:]):  # Show last 5 searches
                st.write(
                    f"🔍 {search['origin']} → {search['destination']} "
                    f"on {search['date']} "
                    f"({search['timestamp'].strftime('%H:%M:%S')})"
                )

async def get_travel_plan(travel_planner, origin, destination, date):
    """Get travel plan with error handling."""
    try:
        with st.spinner('Getting travel information...'):
            plan = await travel_planner.execute(
                origin=origin,
                destination=destination,
                date=date
            )
            # Handle empty plan case
            if not plan:
                st.warning("Unable to get travel information. Please try again.")
                return None
                
            # Check if any service has validation errors
            validation_errors = [
                (service, status.error) 
                for service, status in plan.service_status.items()
                if status.error and "not a valid city" in status.error
            ]
            
            if validation_errors:
                for service, error in validation_errors:
                    show_error_message(error, service)
                return None
            return plan
        
    except Exception as e:
        st.error("Unable to process your request")
        st.info("💡 Please try again later")
        return None
    

def show_error_message(error_msg: str, service_type: str):
    """Display formatted error message with appropriate icon and suggestion."""
    if "not a valid city" in error_msg:
        st.error("🌍 " + error_msg)
        st.markdown("""
        **💡 Tips for entering city names:**
        - Use complete city names (e.g., 'Los Angeles' not 'LA')
        - For common city names, add country (e.g., 'Paris, France')
        - Check spelling carefully
        - Avoid abbreviations or local names
        """)
    elif "connection" in error_msg.lower():
        st.error("🌐 " + error_msg)
        st.info("💡 Please check your internet connection and try again")
    else:
        st.error("⚠️ " + error_msg)
        st.info("💡 Please try again later")

def main():
    st.set_page_config(
        page_title="Travel Planner Agent",
        page_icon="✈️",
        layout="wide"
    )

    st.title("✈️ Travel Planner Agent")
    st.markdown("""
    Plan your perfect trip with real-time weather, flights, and hotel information.
    """)
# Initialize session state
    init_session_state()
    
    # Show search history
    show_search_history()
    
    # Create columns for input
    col1, col2, col3 = st.columns(3)
    
    with col1:
        origin = st.text_input("🛫 Origin City", "San Francisco")
    with col2:
        destination = st.text_input("🛬 Destination City", "New York")
    with col3:
        min_date = datetime.now().date()
        max_date = min_date + timedelta(days=365)
        date = st.date_input(
            "📅 Travel Date",
            min_value=min_date,
            max_value=max_date,
            value=min_date + timedelta(days=7)
        )

    if st.button("🔍 Search Travel Options", type="primary"):
        travel_planner = initialize_agents()
        if travel_planner:
            plan = asyncio.run(get_travel_plan(
                travel_planner,
                origin,
                destination,
                date.strftime("%Y-%m-%d")
            ))
            
            if plan:
                # Add to search history
                st.session_state.search_history.append({
                    'origin': origin,
                    'destination': destination,
                    'date': date,
                    'timestamp': datetime.now()
                })
                st.session_state.last_search = plan
                
                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["Weather", "Flights", "Hotels"])
                
                with tab1:
                    weather_status = plan.service_status["weather"]
                    if weather_status.status:  # Access as property, not dict
                        st.subheader(f"🌤️ Weather in {destination}")
                        format_weather_card(plan.weather_forecast)
                    else:
                        if weather_status.error:  # Access as property
                            show_error_message(weather_status.error, "weather")
                        else:
                            st.error("Weather service is temorarily unavailable")
                
                with tab2:
                    flight_status = plan.service_status["flights"]
                    if flight_status.status:  # Access as property
                        st.subheader("✈️ Flight Options")
                        if plan.flight_options:
                            # Price filter for flights
                            max_price = max(f.price for f in plan.flight_options)
                            price_filter = st.slider(
                                "Filter by maximum flight price ($)",
                                min_value=0,
                                max_value=int(max_price),
                                value=int(max_price)
                            )
                            
                            filtered_flights = [f for f in plan.flight_options if f.price <= price_filter]
                            if filtered_flights:
                                for flight in filtered_flights:
                                    format_flight_card(flight)
                            else:
                                st.info("No flights found within the selected price range")
                        else:
                            st.info(f"No flights found between {origin} and {destination}")
                    else:
                        if flight_status.error:  # Access as property
                            if "Invalid city" in flight_status.error:
                                st.error(f"❌ {flight_status.error}")
                            else:
                                st.error("⚠️ Flight information is temporarily unavailable")
                                st.info(f"Details: {flight_status.error}")
                        else:
                            st.error("Flight service is unavailable")
                
                with tab3:
                    hotel_status = plan.service_status["hotels"]
                    if hotel_status.status:  # Access as property
                        st.subheader("🏨 Hotel Options")
                        if plan.hotel_options:
                            col1, col2 = st.columns(2)
                            with col1:
                                max_hotel_price = max(h.price_per_night for h in plan.hotel_options)
                                price_filter = st.slider(
                                    "Filter by maximum price per night ($)",
                                    min_value=0,
                                    max_value=int(max_hotel_price),
                                    value=int(max_hotel_price)
                                )
                            with col2:
                                min_rating = st.select_slider(
                                    "Minimum Rating",
                                    options=[1, 2, 3, 4, 5],
                                    value=1
                                )
                            
                            filtered_hotels = [
                                h for h in plan.hotel_options 
                                if h.price_per_night <= price_filter and h.rating >= min_rating
                            ]
                            
                            if filtered_hotels:
                                for hotel in filtered_hotels:
                                    format_hotel_card(hotel)
                            else:
                                st.info("No hotels found matching your criteria")
                        else:
                            st.info(f"No hotels found in {destination}")
                    else:
                        if hotel_status.error:  # Access as property
                            if "Invalid city" in hotel_status.error:
                                st.error(f"❌ {hotel_status.error}")
                            else:
                                st.error("⚠️ Hotel information is temporarily unavailable")
                                st.info(f"Details: {hotel_status.error}")
                        else:
                            st.error("Hotel service is unavailable")
                
                # Show overall status for failed services
                failed_services = [
                    service for service, status in plan.service_status.items() 
                    if not status.status  # Access as property
                ]
                
                if failed_services:
                    st.markdown("---")
                    st.error("Some services encountered errors:")
                    for service in failed_services:
                        error_msg = plan.service_status[service].error  # Access as property
                        if error_msg:
                            st.warning(f"⚠️ {service.title()}: {error_msg}")
                
if __name__ == "__main__":
    main()