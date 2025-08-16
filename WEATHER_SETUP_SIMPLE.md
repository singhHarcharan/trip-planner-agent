# Simple Weather Service Setup

## Quick Setup

### 1. Get OpenWeatherMap API Key
- Go to [OpenWeatherMap](https://openweathermap.org/api)
- Sign up for a free account
- Get your API key from the dashboard
- Free tier: 1000 calls/day

### 2. Create .env file
Create a `.env` file in your project root:
```bash
OPENWEATHER_API_KEY=your_api_key_here
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Simple Function Call
```python
from Services.weather_service import get_weather_dates

# Get sunny days in California (next 15 days)
sunny_dates = get_weather_dates("California", "sunny", 15)
print(sunny_dates)
# Output: ['2024-01-15', '2024-01-16', '2024-01-20']

# Get rainy days in New York (next 30 days)
rainy_dates = get_weather_dates("New York, NY", "rainy")
print(rainy_dates)
```

### Class-based Usage
```python
from Services.weather_service import WeatherService

weather_service = WeatherService()
dates = weather_service.get_relevant_dates("San Francisco, CA", "sunny", 20)
```

## Parameters

- **location**: City name (e.g., "San Francisco, CA", "New York", "Miami, FL")
- **condition**: Weather condition (e.g., "sunny", "rainy", "cloudy")
- **days**: Number of days to look ahead (1-30, default: 30)

## Supported Weather Conditions

- ☀️ **sunny** → clear, clear sky
- ☁️ **cloudy** → clouds, scattered clouds, overcast
- 🌧️ **rainy** → rain, light rain, drizzle
- ❄️ **snowy** → snow, light snow, heavy snow
- ⛈️ **stormy** → thunderstorm, storm
- 🌫️ **foggy** → fog, mist, haze
- 💨 **windy** → wind, breeze

## Test the Service

```bash
python test_weather_simple.py
```

## Example Output

```
🌤️  Simple Weather Service Test
==================================================

📍 Location: San Francisco, CA
🌦️  Condition: sunny
📅 Days: 15
----------------------------------------
✅ Found 8 sunny days:
   📅 2024-01-15
   📅 2024-01-16
   📅 2024-01-20
   📅 2024-01-22
   📅 2024-01-25
   📅 2024-01-27
   📅 2024-01-29
   📅 2024-01-30
```

## Error Handling

The service gracefully handles:
- Invalid locations
- API errors
- Network issues
- Missing API keys

Returns empty list `[]` if no matching dates found or errors occur.
