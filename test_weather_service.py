#!/usr/bin/env python3
"""
Simple test script for the weather service
Shows how to use the get_weather_dates function
"""

import os
from dotenv import load_dotenv
from Services.weather_service import get_weather_dates

# Load environment variables
load_dotenv()

def test_weather_service():
    """Test the simple weather service function"""
    
    print("🌤️  Simple Weather Service Test")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("❌ OPENWEATHER_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenWeatherMap API key")
        print("Get your free API key from: https://openweathermap.org/api")
        return
    
    try:
        from Services.weather_service import get_weather_dates
        
        # Test cases
        test_cases = [
            ("San Francisco, CA", "sunny", 15),
            ("New York, NY", "rainy", 20),
            ("Miami, FL", "sunny", 30),
            ("Seattle, WA", "cloudy", 25)
        ]
        
        for location, condition, days in test_cases:
            print(f"\n📍 Location: {location}")
            print(f"🌦️  Condition: {condition}")
            print(f"📅 Days: {days}")
            print("-" * 40)
            
            # Get relevant dates
            relevant_dates = get_weather_dates(location, condition, days)
            
            if relevant_dates:
                print(f"✅ Found {len(relevant_dates)} {condition} days:")
                for date in relevant_dates:
                    print(f"   📅 {date}")
            else:
                print(f"❌ No {condition} days found in the next {days} days")
        
        print("\n" + "=" * 50)
        print("🎯 Test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the weather_service.py file is in the Services/ directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_simple_usage():
    """Show simple usage examples"""
    
    print("\n📚 Simple Usage Examples")
    print("=" * 30)
    
    try:
        
        print("\nExample 1: Get sunny days in California (next 15 days)")
        print("get_weather_dates('California', 'sunny', 15)")
        
        print("\nExample 2: Get rainy days in New York (next 30 days)")
        print("get_weather_dates('New York, NY', 'rainy')")
        
        print("\nExample 3: Get cloudy days in Seattle (next 20 days)")
        print("get_weather_dates('Seattle, WA', 'cloudy', 20)")
        
        print("\nSupported weather conditions:")
        print("- sunny, cloudy, rainy, snowy, stormy, foggy, windy")
        
    except ImportError:
        print("Weather service not available")

if __name__ == "__main__":
    test_weather_service()
    test_simple_usage()
