from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict

class WeatherForecast(BaseModel):
    """Weather forecast data model."""
    temperature: float = Field(default=0.0, description="Current temperature in Celsius")
    condition: str = Field(default="Unknown", description="Weather condition description")
    precipitation_chance: float = Field(default=0.0, description="Precipitation in millimeters")

class FlightOption(BaseModel):
    """Flight option data model."""
    departure_time: str = Field(..., description="Departure time in HH:MM format")
    arrival_time: str = Field(..., description="Arrival time in HH:MM format")
    price: float = Field(..., description="Flight price in USD")
    stops: int = Field(default=0, description="Number of stops")

class HotelOption(BaseModel):
    """Hotel option data model."""
    name: str = Field(..., description="Name of the hotel")
    rating: float = Field(
        ...,
        description="Hotel rating from 1-5",
        ge=1,  # greater than or equal to 1
        le=5   # less than or equal to 5
    )
    price_per_night: float = Field(..., description="Price per night in USD")
    location: str = Field(..., description="Location/area within the city")
    amenities: List[str] = Field(
        default_factory=list,
        description="List of available amenities"
    )

    @classmethod
    def from_api_response(cls, data: dict):
        """Create HotelOption from API response data."""
        try:
            rating = float(data.get('rating', 0))
            rating = max(1, min(5, rating))
            
            price_str = str(data.get('price_per_night', '0'))
            price = float(price_str.replace('$', '').replace(',', ''))
            
            amenities = data.get('amenities', [])
            if isinstance(amenities, str):
                amenities = [a.strip() for a in amenities.split(',')]
            
            return cls(
                name=data.get('name', 'Unknown Hotel'),
                rating=rating,
                price_per_night=price,
                location=data.get('location', 'Location not specified'),
                amenities=amenities
            )
        except Exception as e:
            print(f"Error parsing hotel data: {e}")
            print(f"Raw data: {data}")
            raise

class ServiceStatus(BaseModel):
    """Status information for a service."""
    status: bool = Field(default=False, description="Whether the service is working")
    error: Optional[str] = Field(default=None, description="Error message if service failed")

class TravelPlan(BaseModel):
    """Complete travel plan combining all components."""
    weather_forecast: WeatherForecast = Field(default_factory=WeatherForecast)
    flight_options: List[FlightOption] = Field(default_factory=list)
    hotel_options: List[HotelOption] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    service_status: Dict[str, ServiceStatus] = Field(
        default_factory=lambda: {
            "weather": ServiceStatus(),
            "flights": ServiceStatus(),
            "hotels": ServiceStatus()
        }
    )

    class Config:
        """Model configuration."""
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }