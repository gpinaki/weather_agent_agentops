import pytest
from travel_planner.schemas.models import HotelOption, TravelPlan

def test_hotel_option_creation():
    """Test creating a hotel option with valid data."""
    hotel_data = {
        "name": "Test Hotel",
        "rating": 4.5,
        "price_per_night": 150.0,
        "location": "City Center",
        "amenities": ["WiFi", "Pool"]
    }
    
    hotel = HotelOption(**hotel_data)
    assert hotel.name == "Test Hotel"
    assert hotel.rating == 4.5
    assert hotel.price_per_night == 150.0

def test_hotel_option_validation():
    """Test hotel option validation."""
    with pytest.raises(ValueError):
        # Rating too high should fail
        HotelOption(
            name="Test Hotel",
            rating=6.0,  # Invalid rating
            price_per_night=150.0,
            location="City Center"
        )

def test_hotel_option_from_api_response():
    """Test creating hotel option from API response."""
    api_data = {
        "name": "API Hotel",
        "rating": "4.5",
        "price_per_night": "$199.99",
        "location": "Downtown",
        "amenities": "WiFi, Pool, Gym"
    }
    
    hotel = HotelOption.from_api_response(api_data)
    assert hotel.name == "API Hotel"
    assert hotel.rating == 4.5
    assert hotel.price_per_night == 199.99
    assert len(hotel.amenities) == 3