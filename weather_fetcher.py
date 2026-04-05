import urllib.request
import urllib.parse
import json

def get_coordinates(location: str):
    """Get coordinates using Open-Meteo geocoding - no API key needed."""
    query = urllib.parse.urlencode({"name": location, "count": 1, "language": "en", "format": "json"})
    url = f"https://geocoding-api.open-meteo.com/v1/search?{query}"
    
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode())
        
        if not data.get("results"):
            # Try stripping pincode and retry with just city name
            words = location.split()
            words = [w for w in words if not w.isdigit()]
            clean_location = " ".join(words)
            if clean_location != location:
                return get_coordinates(clean_location)
            return None, None, None
        
        result = data["results"][0]
        return result["latitude"], result["longitude"], result.get("name", location)
    
    except Exception as e:
        return None, None, str(e)


def celsius_to_fahrenheit(c):
    return round((c * 9/5) + 32, 1)


def get_wind_direction(degrees):
    directions = ["N","NE","E","SE","S","SW","W","NW"]
    index = round(degrees / 45) % 8
    return directions[index]


def get_current_weather(location: str) -> str:
    """
    Fetch real-time weather for any location.
    Uses Open-Meteo API — completely free, no API key required.
    Falls back to stripping pincodes if location not found.
    """
    try:
        lat, lon, city_name = get_coordinates(location)
        
        if lat is None:
            return json.dumps({
                "error": True,
                "message": f"Location '{location}' not found. Please try a nearby city name.",
                "suggestion": "Try using just the city name without pincode."
            })

        params = urllib.parse.urlencode({
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,precipitation,surface_pressure",
            "timezone": "auto",
            "wind_speed_unit": "kmh"
        })
        
        url = f"https://api.open-meteo.com/v1/forecast?{params}"
        
        with urllib.request.urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode())
        
        current = data.get("current", {})

        weather_codes = {
            0: "☀️ Clear Sky",
            1: "🌤️ Mainly Clear",
            2: "⛅ Partly Cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Foggy",
            48: "🌫️ Icy Fog",
            51: "🌦️ Light Drizzle",
            53: "🌦️ Drizzle",
            55: "🌧️ Heavy Drizzle",
            61: "🌧️ Light Rain",
            63: "🌧️ Rain",
            65: "🌧️ Heavy Rain",
            71: "🌨️ Light Snow",
            73: "❄️ Snow",
            75: "❄️ Heavy Snow",
            77: "🌨️ Snow Grains",
            80: "🌦️ Light Showers",
            81: "🌧️ Showers",
            82: "⛈️ Heavy Showers",
            85: "🌨️ Snow Showers",
            95: "⛈️ Thunderstorm",
            96: "⛈️ Thunderstorm with Hail",
            99: "⛈️ Heavy Thunderstorm with Hail"
        }

        code = current.get("weather_code", 0)
        condition = weather_codes.get(code, "🌡️ Unknown")
        temp_c = current.get("temperature_2m", 0)
        feels_c = current.get("apparent_temperature", 0)
        wind_dir = get_wind_direction(current.get("wind_direction_10m", 0))

        result = {
            "error": False,
            "location": city_name,
            "temperature_c": temp_c,
            "temperature_f": celsius_to_fahrenheit(temp_c),
            "feels_like_c": feels_c,
            "feels_like_f": celsius_to_fahrenheit(feels_c),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "wind_direction": wind_dir,
            "precipitation_mm": current.get("precipitation", 0),
            "pressure_hpa": current.get("surface_pressure"),
            "condition": condition,
            "timezone": data.get("timezone", "")
        }

        return json.dumps(result)

    except Exception as e:
        return json.dumps({
            "error": True,
            "message": f"Failed to fetch weather: {str(e)}",
            "suggestion": "Check internet connection or try again."
        })


if __name__ == "__main__":
    # Test
    print(get_current_weather("New Delhi 110020"))
    print(get_current_weather("Mumbai"))