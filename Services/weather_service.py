import os
import httpx
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv
from httpx import HTTPStatusError

# Load environment variables
load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY not found in environment variables")
    
    def get_coordinates(self, location: str) -> Optional[Dict]:
        """Get coordinates for a location using OpenWeatherMap Geocoding API"""
        try:
            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": location,
                "limit": 1,
                "appid": self.api_key
            }
            
            response = httpx.get(url, params=params, timeout=30.0)
            
            # Check for specific error status codes
            if response.status_code == 401:
                print(f"❌ API Key Error: Your OpenWeatherMap API key is invalid or expired")
                print(f"   Please get a new API key from: https://openweathermap.org/api")
                print(f"   Current key: {self.api_key[:8]}...")
                return None
            elif response.status_code == 429:
                print(f"❌ Rate Limit Exceeded: You've exceeded the API call limit")
                print(f"   Free tier allows 1000 calls/day")
                return None
            elif response.status_code == 400:
                print(f"❌ Bad Request: Invalid location format '{location}'")
                return None
            
            response.raise_for_status()
            
            data = response.json()
            if data:
                return {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"],
                    "name": data[0]["name"],
                    "state": data[0].get("state", ""),
                    "country": data[0]["country"]
                }
            else:
                print(f"❌ No coordinates found for location: {location}")
                print(f"   Try: {location.split(',')[0]} (just city name)")
                return None
            
        except HTTPStatusError as e:
            print(f"❌ HTTP Error {e.response.status_code}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error getting coordinates for {location}: {e}")
            return None
    
    def get_weather_forecast(self, lat: float, lon: float, days: int = 30) -> Optional[List[Dict]]:
        """Get weather forecast for the next N days"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"  # Use Celsius
            }
            
            response = httpx.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            forecasts = []
            
            # Group forecasts by day (OpenWeatherMap provides 3-hour forecasts)
            daily_forecasts = {}
            
            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(item)
            
            # Process each day's forecasts
            for date, hourly_forecasts in daily_forecasts.items():
                # Get the most common weather condition for the day
                conditions = [f["weather"][0]["main"].lower() for f in hourly_forecasts]
                condition_counts = {}
                for condition in conditions:
                    condition_counts[condition] = condition_counts.get(condition, 0) + 1
                
                # Get the dominant condition
                dominant_condition = max(condition_counts.items(), key=lambda x: x[1])[0]
                
                # Get average temperature
                avg_temp = sum(f["main"]["temp"] for f in hourly_forecasts) / len(hourly_forecasts)
                
                forecasts.append({
                    "date": date,
                    "condition": dominant_condition,
                    "description": hourly_forecasts[0]["weather"][0]["description"],
                    "temperature": round(avg_temp, 1),
                    "humidity": hourly_forecasts[0]["main"]["humidity"]
                })
            
            return forecasts[:days]
            
        except Exception as e:
            print(f"Error getting weather forecast: {e}")
            return None
    
    def get_relevant_dates(self, location: str, condition: str, days: int = 30) -> List[str]:
        """
        Simple function to get relevant dates for a weather condition in a location
        
        Args:
            location (str): City name, can include state/country (e.g., "San Francisco, CA")
            condition (str): Weather condition to search for (e.g., "sunny", "rainy")
            days (int): Number of days to look ahead (default 30, max 30)
        
        Returns:
            List[str]: List of dates in YYYY-MM-DD format where the weather condition matches
        """
        try:
            print(f"Searching for {condition} days in {location} for the next {days} days")
            
            # Limit days to 30 (OpenWeatherMap free tier limit)
            days = min(days, 30)
            
            # Get coordinates for the location
            coords = self.get_coordinates(location)
            if not coords:
                print(f"Could not find coordinates for {location}")
                return []
            
            print(f"Found coordinates: {coords['lat']:.4f}, {coords['lon']:.4f}")
            
            # Get weather forecast
            forecasts = self.get_weather_forecast(coords["lat"], coords["lon"], days)
            if not forecasts:
                print("Could not get weather forecast")
                return []
            
            # Filter dates based on weather condition
            condition = condition.lower().strip()
            relevant_dates = []
            
            for forecast in forecasts:
                forecast_condition = forecast["condition"]
                
                # Check if the forecast condition matches the requested condition
                if self._matches_condition(forecast_condition, condition):
                    relevant_dates.append(forecast["date"])
            
            print(f"Found {len(relevant_dates)} relevant dates for {condition} weather in {location}")
            return relevant_dates
            
        except Exception as e:
            print(f"Error getting relevant dates: {e}")
            return []
    
    def _matches_condition(self, forecast_condition: str, requested_condition: str) -> bool:
        """Check if forecast condition matches requested condition"""
        # Create mapping for common weather conditions
        condition_mapping = {
            "sunny": ["clear", "clear sky"],
            "cloudy": ["clouds", "scattered clouds", "broken clouds", "overcast clouds"],
            "rainy": ["rain", "light rain", "moderate rain", "heavy rain", "drizzle"],
            "snowy": ["snow", "light snow", "moderate snow", "heavy snow"],
            "stormy": ["thunderstorm", "storm"],
            "foggy": ["fog", "mist", "haze"],
            "windy": ["wind", "breeze"]
        }
        
        # Check exact match first
        if forecast_condition == requested_condition:
            return True
        
        # Check mapped conditions
        if requested_condition in condition_mapping:
            return forecast_condition in condition_mapping[requested_condition]
        
        # Check if requested condition is contained in forecast condition
        return requested_condition in forecast_condition or forecast_condition in requested_condition


# Simple function interface for easy use
def get_weather_dates(location: str, condition: str, days: int = 30) -> List[str]:
    """
    Simple function to get relevant dates for a weather condition
    
    Args:
        location (str): City name (e.g., "San Francisco, CA")
        condition (str): Weather condition (e.g., "sunny", "rainy")
        days (int): Number of days to look ahead (default 30)
    
    Returns:
        List[str]: List of dates where weather condition matches
    
    Example:
        >>> get_weather_dates("San Francisco, CA", "sunny", 15)
        ['2024-01-15', '2024-01-16', '2024-01-20']
    """
    try:
        weather_service = WeatherService()
        return weather_service.get_relevant_dates(location, condition, days)
    except Exception as e:
        print(f"Error: {e}")
        return []
