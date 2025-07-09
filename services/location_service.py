import math
import requests
from typing import Tuple, Optional, List, Dict
from flask import current_app


class LocationService:
    """Service class for handling location operations."""
    
    EARTH_RADIUS_KM = 6371
    EARTH_RADIUS_MILES = 3959
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float, unit: str = 'km') -> float:
        """Calculate distance between two points using Haversine formula."""
        
        # Convert latitude and longitude to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        # Calculate distance
        radius = LocationService.EARTH_RADIUS_KM if unit == 'km' else LocationService.EARTH_RADIUS_MILES
        return radius * c
    
    @staticmethod
    def get_nearby_shops(user_lat: float, user_lon: float, shops: List, max_distance: float = 50, unit: str = 'km') -> List[Dict]:
        """Get shops within specified distance, sorted by proximity."""
        
        nearby_shops = []
        
        for shop in shops:
            if shop.latitude and shop.longitude:
                distance = LocationService.calculate_distance(
                    user_lat, user_lon, shop.latitude, shop.longitude, unit
                )
                
                if distance <= max_distance:
                    shop_data = {
                        'shop': shop,
                        'distance': round(distance, 2),
                        'unit': unit
                    }
                    nearby_shops.append(shop_data)
        
        # Sort by distance
        nearby_shops.sort(key=lambda x: x['distance'])
        return nearby_shops
    
    @staticmethod
    def geocode_address(address: str) -> Optional[Tuple[float, float]]:
        """Geocode address to latitude and longitude using a free service."""
        
        try:
            # Using Nominatim (OpenStreetMap) - free geocoding service
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'LocalBasket/1.0 (local-produce-app)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data:
                location = data[0]
                lat = float(location['lat'])
                lon = float(location['lon'])
                return lat, lon
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Geocoding request failed: {str(e)}")
        except (KeyError, ValueError, IndexError) as e:
            current_app.logger.error(f"Geocoding response parsing failed: {str(e)}")
        
        return None
    
    @staticmethod
    def reverse_geocode(lat: float, lon: float) -> Optional[str]:
        """Reverse geocode coordinates to address."""
        
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'LocalBasket/1.0 (local-produce-app)'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'display_name' in data:
                return data['display_name']
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Reverse geocoding request failed: {str(e)}")
        except (KeyError, ValueError) as e:
            current_app.logger.error(f"Reverse geocoding response parsing failed: {str(e)}")
        
        return None
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """Validate latitude and longitude coordinates."""
        try:
            lat = float(lat)
            lon = float(lon)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def format_distance(distance: float, unit: str = 'km') -> str:
        """Format distance for display."""
        if unit == 'km':
            if distance < 1:
                return f"{int(distance * 1000)}m"
            else:
                return f"{distance:.1f}km"
        else:  # miles
            if distance < 1:
                return f"{int(distance * 5280)}ft"
            else:
                return f"{distance:.1f}mi"


# Global location service instance
location_service = LocationService()