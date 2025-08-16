#!/usr/bin/env python3
"""
Simple script to test OpenWeatherMap API key
"""

import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if the OpenWeatherMap API key is working"""
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("❌ No API key found in .env file")
        print("Please create a .env file with: OPENWEATHER_API_KEY=your_key_here")
        return False
    
    print(f"🔑 Testing API key: {api_key[:8]}...")
    
    # Test 1: Geocoding API
    print("\n📍 Testing Geocoding API...")
    try:
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": "Amritsar, Punjab",
            "limit": 1,
            "appid": api_key
        }
        
        response = httpx.get(url, params=params, timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                coords = data[0]
                print(f"✅ Geocoding successful!")
                print(f"   City: {coords['name']}")
                print(f"   State: {coords.get('state', 'N/A')}")
                print(f"   Country: {coords['country']}")
                print(f"   Coordinates: {coords['lat']:.4f}, {coords['lon']:.4f}")
            else:
                print("❌ No results found for 'Amritsar, Punjab'")
        else:
            print(f"❌ Geocoding failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Geocoding error: {e}")
    
    # Test 2: Weather Forecast API
    print("\n🌤️  Testing Weather Forecast API...")
    try:
        # Use coordinates from previous test or default coordinates
        lat, lon = 31.6340, 74.8723  # Amritsar coordinates
        
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }
        
        response = httpx.get(url, params=params, timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Weather forecast successful!")
            print(f"   City: {data['city']['name']}")
            print(f"   Country: {data['city']['country']}")
            print(f"   Forecast entries: {len(data['list'])}")
            
            # Show first few forecasts
            for i, item in enumerate(data['list'][:3]):
                date = item['dt_txt']
                temp = item['main']['temp']
                condition = item['weather'][0]['main']
                print(f"   {date}: {temp}°C, {condition}")
                
        else:
            print(f"❌ Weather forecast failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Weather forecast error: {e}")
    
    return True

def check_env_file():
    """Check if .env file exists and has the right format"""
    
    print("🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Please create a .env file with your API key")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        
    if 'OPENWEATHER_API_KEY' in content:
        print("✅ .env file found with OPENWEATHER_API_KEY")
        return True
    else:
        print("❌ .env file found but no OPENWEATHER_API_KEY")
        return False

if __name__ == "__main__":
    print("🚀 OpenWeatherMap API Key Test")
    print("=" * 40)
    
    # Check .env file
    check_env_file()
    
    # Test API key
    test_api_key()
    
    print("\n" + "=" * 40)
    print("💡 If you see errors above:")
    print("1. Get a new API key from OpenWeatherMap")
    print("2. Update your .env file")
    print("3. Make sure the key has Geocoding and Forecast permissions")
