#!/usr/bin/env python3
"""
Weather fetcher for Gemma 4 Agent Skills
Uses Open-Meteo API (free, no API key required)
"""

import json
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

# WMO Weather interpretation codes
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

def search_location(query: str, limit: int = 5) -> dict:
    """Search for location coordinates using Open-Meteo Geocoding API"""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_query}&count={limit}&language=en&format=json"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if not data.get("results"):
            return {"error": f"No locations found for '{query}'", "results": []}
        
        results = []
        for loc in data["results"]:
            results.append({
                "name": loc.get("name"),
                "country": loc.get("country"),
                "admin1": loc.get("admin1"),
                "latitude": loc.get("latitude"),
                "longitude": loc.get("longitude"),
                "timezone": loc.get("timezone"),
                "population": loc.get("population")
            })
        
        return {
            "query": query,
            "results": results,
            "top_result": results[0] if results else None
        }
        
    except Exception as e:
        return {"error": f"Search failed: {str(e)}", "results": []}

def get_current_weather(latitude: float, longitude: float, location_name: str = "Unknown", units: str = "celsius") -> dict:
    """Get current weather conditions"""
    try:
        temp_unit = "fahrenheit" if units == "fahrenheit" else "celsius"
        wind_unit = "mph" if units == "fahrenheit" else "kmh"
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl",
            "timezone": "auto",
            "temperature_unit": temp_unit,
            "wind_speed_unit": wind_unit
        }
        
        query_string = urllib.parse.urlencode(params)
        url = f"https://api.open-meteo.com/v1/forecast?{query_string}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        current = data.get("current", {})
        weather_code = current.get("weather_code", 0)
        condition = WMO_CODES.get(weather_code, "Unknown")
        is_day = current.get("is_day", 1) == 1
        
        return {
            "location": location_name,
            "coordinates": {"lat": latitude, "lon": longitude},
            "timezone": data.get("timezone"),
            "current": {
                "temperature": current.get("temperature_2m"),
                "feels_like": current.get("apparent_temperature"),
                "humidity_percent": current.get("relative_humidity_2m"),
                "condition": condition,
                "is_daytime": is_day,
                "precipitation_mm": current.get("precipitation"),
                "rain_mm": current.get("rain"),
                "snowfall_cm": current.get("snowfall"),
                "cloud_cover_percent": current.get("cloud_cover"),
                "wind_speed": current.get("wind_speed_10m"),
                "wind_direction_degrees": current.get("wind_direction_10m"),
                "pressure_hpa": current.get("pressure_msl")
            },
            "units": {
                "temperature": "°F" if units == "fahrenheit" else "°C",
                "wind_speed": "mph" if units == "fahrenheit" else "km/h",
                "precipitation": "mm"
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}

def get_hourly_forecast(latitude: float, longitude: float, location_name: str = "Unknown", hours: int = 24, units: str = "celsius") -> dict:
    """Get hour-by-hour weather forecast"""
    try:
        hours = min(max(hours, 1), 48)
        temp_unit = "fahrenheit" if units == "fahrenheit" else "celsius"
        wind_unit = "mph" if units == "fahrenheit" else "kmh"
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,weather_code,cloud_cover,wind_speed_10m,is_day",
            "timezone": "auto",
            "forecast_days": 2,
            "temperature_unit": temp_unit,
            "wind_speed_unit": wind_unit
        }
        
        query_string = urllib.parse.urlencode(params)
        url = f"https://api.open-meteo.com/v1/forecast?{query_string}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])[:hours]
        
        forecast = []
        for i in range(len(times)):
            weather_code = hourly.get("weather_code", [0])[i] if i < len(hourly.get("weather_code", [])) else 0
            condition = WMO_CODES.get(weather_code, "Unknown")
            
            forecast.append({
                "time": times[i],
                "temperature": hourly.get("temperature_2m", [None])[i] if i < len(hourly.get("temperature_2m", [])) else None,
                "feels_like": hourly.get("apparent_temperature", [None])[i] if i < len(hourly.get("apparent_temperature", [])) else None,
                "humidity_percent": hourly.get("relative_humidity_2m", [None])[i] if i < len(hourly.get("relative_humidity_2m", [])) else None,
                "condition": condition,
                "precipitation_probability_percent": hourly.get("precipitation_probability", [None])[i] if i < len(hourly.get("precipitation_probability", [])) else None,
                "precipitation_mm": hourly.get("precipitation", [None])[i] if i < len(hourly.get("precipitation", [])) else None,
                "cloud_cover_percent": hourly.get("cloud_cover", [None])[i] if i < len(hourly.get("cloud_cover", [])) else None,
                "wind_speed": hourly.get("wind_speed_10m", [None])[i] if i < len(hourly.get("wind_speed_10m", [])) else None,
                "is_daytime": bool(hourly.get("is_day", [1])[i]) if i < len(hourly.get("is_day", [])) else True
            })
        
        temps = [f["temperature"] for f in forecast if f["temperature"] is not None]
        rain_probs = [f["precipitation_probability_percent"] for f in forecast if f["precipitation_probability_percent"] is not None]
        
        return {
            "location": location_name,
            "timezone": data.get("timezone"),
            "forecast_period_hours": hours,
            "hourly_data": forecast,
            "summary": {
                "temp_high": max(temps) if temps else None,
                "temp_low": min(temps) if temps else None,
                "max_precipitation_probability": max(rain_probs) if rain_probs else 0,
                "will_rain": any(p and p > 50 for p in rain_probs)
            },
            "units": {
                "temperature": "°F" if units == "fahrenheit" else "°C",
                "wind_speed": "mph" if units == "fahrenheit" else "km/h"
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch forecast: {str(e)}"}

def get_daily_forecast(latitude: float, longitude: float, location_name: str = "Unknown", days: int = 7, units: str = "celsius") -> dict:
    """Get daily weather forecast"""
    try:
        days = min(max(days, 1), 16)
        temp_unit = "fahrenheit" if units == "fahrenheit" else "celsius"
        wind_unit = "mph" if units == "fahrenheit" else "kmh"
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,uv_index_max,sunrise,sunset",
            "timezone": "auto",
            "forecast_days": days,
            "temperature_unit": temp_unit,
            "wind_speed_unit": wind_unit
        }
        
        query_string = urllib.parse.urlencode(params)
        url = f"https://api.open-meteo.com/v1/forecast?{query_string}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        
        forecast = []
        for i in range(len(dates)):
            weather_code = daily.get("weather_code", [0])[i] if i < len(daily.get("weather_code", [])) else 0
            condition = WMO_CODES.get(weather_code, "Unknown")
            
            forecast.append({
                "date": dates[i],
                "condition": condition,
                "temp_high": daily.get("temperature_2m_max", [None])[i] if i < len(daily.get("temperature_2m_max", [])) else None,
                "temp_low": daily.get("temperature_2m_min", [None])[i] if i < len(daily.get("temperature_2m_min", [])) else None,
                "feels_like_high": daily.get("apparent_temperature_max", [None])[i] if i < len(daily.get("apparent_temperature_max", [])) else None,
                "feels_like_low": daily.get("apparent_temperature_min", [None])[i] if i < len(daily.get("apparent_temperature_min", [])) else None,
                "precipitation_mm": daily.get("precipitation_sum", [None])[i] if i < len(daily.get("precipitation_sum", [])) else None,
                "rain_probability_percent": daily.get("precipitation_probability_max", [None])[i] if i < len(daily.get("precipitation_probability_max", [])) else None,
                "wind_speed_max": daily.get("wind_speed_10m_max", [None])[i] if i < len(daily.get("wind_speed_10m_max", [])) else None,
                "uv_index_max": daily.get("uv_index_max", [None])[i] if i < len(daily.get("uv_index_max", [])) else None,
                "sunrise": daily.get("sunrise", [None])[i] if i < len(daily.get("sunrise", [])) else None,
                "sunset": daily.get("sunset", [None])[i] if i < len(daily.get("sunset", [])) else None
            })
        
        return {
            "location": location_name,
            "timezone": data.get("timezone"),
            "forecast_period_days": days,
            "daily_forecast": forecast,
            "units": {
                "temperature": "°F" if units == "fahrenheit" else "°C",
                "wind_speed": "mph" if units == "fahrenheit" else "km/h",
                "precipitation": "mm"
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch daily forecast: {str(e)}"}

# Main execution for command-line calls
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No function specified"}))
        sys.exit(1)
    
    function_name = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    if function_name == "search_location":
        result = search_location(args.get("query", ""), args.get("limit", 5))
    elif function_name == "get_current_weather":
        result = get_current_weather(
            args.get("latitude"), 
            args.get("longitude"),
            args.get("location_name", "Unknown"),
            args.get("units", "celsius")
        )
    elif function_name == "get_hourly_forecast":
        result = get_hourly_forecast(
            args.get("latitude"),
            args.get("longitude"),
            args.get("location_name", "Unknown"),
            args.get("hours", 24),
            args.get("units", "celsius")
        )
    elif function_name == "get_daily_forecast":
        result = get_daily_forecast(
            args.get("latitude"),
            args.get("longitude"),
            args.get("location_name", "Unknown"),
            args.get("days", 7),
            args.get("units", "celsius")
        )
    else:
        result = {"error": f"Unknown function: {function_name}"}
    
    print(json.dumps(result))
            
