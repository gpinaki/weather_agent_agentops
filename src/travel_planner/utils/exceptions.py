class CityValidationError(Exception):
    """Raised when a city cannot be validated"""
    pass

class ServiceError(Exception):
    """Base class for service-related errors"""
    pass

class WeatherServiceError(ServiceError):
    """Raised when weather service fails"""
    pass

class FlightServiceError(ServiceError):
    """Raised when flight service fails"""
    pass

class HotelServiceError(ServiceError):
    """Raised when hotel service fails"""
    pass