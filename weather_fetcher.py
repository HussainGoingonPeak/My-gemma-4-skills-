import requests
import json

def get_coordinates(location: str):
    """Get lat/lon from location name using Open-Meteo geocoding."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location, "count": 1, "language": "en", "format": "json"}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    if not data.get("results"):
        return None, None, None
    result = data["results"][0]
    return result["latitude"], result["longitude"], result.get("name", location)

def get_current_weather(location: str) -> str:
    """Fetch current weather for a location. No API key needed."""
    try:
        lat, lon, city_name = get_coordinates(location)
        if lat is None:
            return json.dumps({"error": f"Could not find location: {location}"})

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "weather_code",
                "wind_speed_10m",
                "wind_direction_10m"
            ],
            "timezone": "auto"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        current = data.get("current", {})

        weather_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 53: "Drizzle",
            61: "Light rain", 63: "Rain", 65: "Heavy rain",
            71: "Light snow", 73: "Snow", 75: "Heavy snow",
            80: "Light showers", 81: "Showers", 82: "Heavy showers",
            95: "Thunderstorm", 99: "Thunderstorm with hail"
        }

        code = current.get("weather_code", 0)
        condition = weather_codes.get(code, f"Code {code}")

        result = {
            "location": city_name,
            "temperature_c": current.get("temperature_2m"),
            "feels_like_c": current.get("apparent_temperature"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "condition": condition
        }
        return json.dumps(result)

    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    print(get_current_weather("New Delhi"))