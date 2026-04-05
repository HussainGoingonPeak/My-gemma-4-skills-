#!/usr/bin/env python3
"""
Real-Time Weather MCP Server for Gemma 4
Uses Open-Meteo API (free, no API key required)
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.parse import urlencode

# MCP protocol implementation (lightweight, no external deps)
class MCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        
    def tool(self, name: str, description: str, schema: dict):
        def decorator(func):
            self.tools[name] = {
                "name": name,
                "description": description,
                "inputSchema": schema,
                "handler": func
            }
            return func
        return decorator
    
    async def handle_request(self, request: dict) -> dict:
        method = request.get("method")
        id = request.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": self.name, "version": "1.0.0"}
                }
            }
        
        elif method == "tools/list":
            tools_list = [{
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["inputSchema"]
            } for t in self.tools.values()]
            return {
                "jsonrpc": "2.0",
                "id": id,
                "result": {"tools": tools_list}
            }
        
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                }
            
            try:
                result = await self.tools[tool_name]["handler"](**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                        "isError": False
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                        "isError": True
                    }
                }
        
        return {
            "jsonrpc": "2.0",
            "id": id,
            "error": {"code": -32601, "message": f"Method '{method}' not found"}
        }

# Initialize server
server = MCPServer("realtime-weather")

# ============ TOOL IMPLEMENTATIONS ============

@server.tool(
    name="search_location",
    description="Search for a location by name to get coordinates (latitude/longitude)",
    schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Location name to search (city, region, country)"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results",
                "default": 5
            }
        },
        "required": ["query"]
    }
)
async def search_location(query: str, limit: int = 5) -> dict:
    """Search location using Open-Meteo Geocoding API"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urlencode({'name': query})}&count={limit}&language=en&format=json"
    
    req = Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
    
    with urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    if not data.get("results"):
        return {"error": f"No locations found for '{query}'", "suggestions": []}
    
    results = []
    for loc in data["results"]:
        results.append({
            "name": loc.get("name"),
            "country": loc.get("country"),
            "admin1": loc.get("admin1"),  # State/Province
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

@server.tool(
    name="get_current_weather",
    description="Get current weather conditions including temperature, humidity, wind, and conditions",
    schema={
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "Location latitude (-90 to 90)"
            },
            "longitude": {
                "type": "number",
                "description": "Location longitude (-180 to 180)"
            },
            "location_name": {
                "type": "string",
                "description": "Human-readable location name for display",
                "default": "Unknown Location"
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature units",
                "default": "celsius"
            }
        },
        "required": ["latitude", "longitude"]
    }
)
async def get_current_weather(
    latitude: float, 
    longitude: float, 
    location_name: str = "Unknown Location",
    units: str = "celsius"
) -> dict:
    """Get current weather from Open-Meteo API"""
    
    temp_unit = "fahrenheit" if units == "fahrenheit" else "celsius"
    wind_unit = "mph" if units == "fahrenheit" else "kmh"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", 
                   "is_day", "precipitation", "rain", "showers", "snowfall",
                   "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m",
                   "pressure_msl", "surface_pressure"],
        "timezone": "auto",
        "temperature_unit": temp_unit,
        "wind_speed_unit": wind_unit,
        "precipitation_unit": "mm"
    }
    
    url = f"https://api.open-meteo.com/v1/forecast?{urlencode(params, doseq=True)}"
    
    req = Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
    
    with urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    current = data.get("current", {})
    
    # Map WMO weather codes to human-readable conditions
    weather_code = current.get("weather_code", 0)
    condition = WMO_WEATHER_CODES.get(weather_code, "Unknown")
    
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
        },
        "retrieved_at": data.get("current", {}).get("time")
    }

@server.tool(
    name="get_hourly_forecast",
    description="Get hour-by-hour weather forecast for the next 24-48 hours",
    schema={
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "Location latitude"
            },
            "longitude": {
                "type": "number",
                "description": "Location longitude"
            },
            "location_name": {
                "type": "string",
                "description": "Human-readable location name",
                "default": "Unknown Location"
            },
            "hours": {
                "type": "integer",
                "description": "Number of hours to forecast (1-48)",
                "default": 24
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "default": "celsius"
            }
        },
        "required": ["latitude", "longitude"]
    }
)
async def get_hourly_forecast(
    latitude: float,
    longitude: float,
    location_name: str = "Unknown Location",
    hours: int = 24,
    units: str = "celsius"
) -> dict:
    """Get hourly forecast from Open-Meteo"""
    
    hours = min(max(hours, 1), 48)  # Clamp 1-48
    temp_unit = "fahrenheit" if units == "fahrenheit" else "celsius"
    wind_unit = "mph" if units == "fahrenheit" else "kmh"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature",
                  "precipitation_probability", "precipitation", "weather_code",
                  "cloud_cover", "wind_speed_10m", "wind_direction_10m", 
                  "is_day", "visibility"],
        "timezone": "auto",
        "forecast_days": 2,
        "temperature_unit": temp_unit,
        "wind_speed_unit": wind_unit
    }
    
    url = f"https://api.open-meteo.com/v1/forecast?{urlencode(params, doseq=True)}"
    
    req = Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
    
    with urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])[:hours]
    
    forecast = []
    for i in range(len(times)):
        weather_code = hourly.get("weather_code", [])[i] if i < len(hourly.get("weather_code", [])) else 0
        condition = WMO_WEATHER_CODES.get(weather_code, "Unknown")
        
        forecast.append({
            "time": times[i],
            "temperature": hourly.get("temperature_2m", [])[i] if i < len(hourly.get("temperature_2m", [])) else None,
            "feels_like": hourly.get("apparent_temperature", [])[i] if i < len(hourly.get("apparent_temperature", [])) else None,
            "humidity_percent": hourly.get("relative_humidity_2m", [])[i] if i < len(hourly.get("relative_humidity_2m", [])) else None,
            "condition": condition,
            "precipitation_probability_percent": hourly.get("precipitation_probability", [])[i] if i < len(hourly.get("precipitation_probability", [])) else None,
            "precipitation_mm": hourly.get("precipitation", [])[i] if i < len(hourly.get("precipitation", [])) else None,
            "cloud_cover_percent": hourly.get("cloud_cover", [])[i] if i < len(hourly.get("cloud_cover", [])) else None,
            "wind_speed": hourly.get("wind_speed_10m", [])[i] if i < len(hourly.get("wind_speed_10m", [])) else None,
            "is_daytime": bool(hourly.get("is_day", [])[i]) if i < len(hourly.get("is_day", [])) else True
        })
    
    # Calculate summary
    temps = [f["temperature"] for f in forecast if f["temperature"] is not None]
    rain_prob = [f["precipitation_probability_percent"] for f in forecast if f["precipitation_probability_percent"] is not None]
    
    return {
        "location": location_name,
        "coordinates": {"lat": latitude, "lon": longitude},
        "timezone": data.get("timezone"),
        "forecast_period_hours": hours,
        "hourly_data": forecast,
        "summary": {
            "temp_high": max(temps) if temps else None,
            "temp_low": min(temps) if temps else None,
            "max_precipitation_probability": max(rain_prob) if rain_prob else 0,
            "will_rain": any(p and p > 50 for p in rain_prob)
        },
        "units": {
            "temperature": "°F" if units == "fahrenheit" else "°C",
            "wind_speed": "mph" if units == "fahrenheit" else "km/h"
        }
    }

@server.tool(
    name="get_daily_forecast",
    description="Get daily weather forecast for multiple days ahead",
    schema={
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "Location latitude"
            },
            "longitude": {
                "type": "number",
                "description": "Location longitude"
            },
            "location_name": {
                "type": "string",
                "description": "Human-readable location name",
                "default": "Unknown Location"
            },
            "days": {
                "type": "integer",
                "description": "Number of days to forecast (1-16)",
                "default": 7
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "default": "celsius"
            }
        },
        "required": ["latitude", "longitude"]
    }
)
async def get_daily_forecast(
    latitude: float,
    longitude: float,
    location_name: str = "Unknown Location",
    days: int = 7,
    units: str = "celsius"
) -> dict:
    """Get daily forecast from Open-Meteo"""
    
    days = min(max(days, 1), 16)  # Clamp 1-16
    temp_unit = "fahrenheit" if units == "fahrenheit" else "celsius"
    wind_unit = "mph" if units == "fahrenheit" else "kmh"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min",
                 "apparent_temperature_max", "apparent_temperature_min",
                 "precipitation_sum", "precipitation_probability_max",
                 "wind_speed_10m_max", "wind_direction_10m_dominant",
                 "sunrise", "sunset", "uv_index_max"],
        "timezone": "auto",
        "forecast_days": days,
        "temperature_unit": temp_unit,
        "wind_speed_unit": wind_unit
    }
    
    url = f"https://api.open-meteo.com/v1/forecast?{urlencode(params, doseq=True)}"
    
    req = Request(url, headers={"User-Agent": "Gemma4-Weather-Skill/1.0"})
    
    with urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    
    forecast = []
    for i in range(len(dates)):
        weather_code = daily.get("weather_code", [])[i] if i < len(daily.get("weather_code", [])) else 0
        condition = WMO_WEATHER_CODES.get(weather_code, "Unknown")
        
        forecast.append({
            "date": dates[i],
            "condition": condition,
            "temp_high": daily.get("temperature_2m_max", [])[i] if i < len(daily.get("temperature_2m_max", [])) else None,
            "temp_low": daily.get("temperature_2m_min", [])[i] if i < len(daily.get("temperature_2m_min", [])) else None,
            "feels_like_high": daily.get("apparent_temperature_max", [])[i] if i < len(daily.get("apparent_temperature_max", [])) else None,
            "feels_like_low": daily.get("apparent_temperature_min", [])[i] if i < len(daily.get("apparent_temperature_min", [])) else None,
            "precipitation_mm": daily.get("precipitation_sum", [])[i] if i < len(daily.get("precipitation_sum", [])) else None,
            "rain_probability_percent": daily.get("precipitation_probability_max", [])[i] if i < len(daily.get("precipitation_probability_max", [])) else None,
            "wind_speed_max": daily.get("wind_speed_10m_max", [])[i] if i < len(daily.get("wind_speed_10m_max", [])) else None,
            "uv_index_max": daily.get("uv_index_max", [])[i] if i < len(daily.get("uv_index_max", [])) else None,
            "sunrise": daily.get("sunrise", [])[i] if i < len(daily.get("sunrise", [])) else None,
            "sunset": daily.get("sunset", [])[i] if i < len(daily.get("sunset", [])) else None
        })
    
    return {
        "location": location_name,
        "coordinates": {"lat": latitude, "lon": longitude},
        "timezone": data.get("timezone"),
        "forecast_period_days": days,
        "daily_forecast": forecast,
        "units": {
            "temperature": "°F" if units == "fahrenheit" else "°C",
            "wind_speed": "mph" if units == "fahrenheit" else "km/h",
            "precipitation": "mm"
        }
    }

# WMO Weather interpretation codes
WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

# ============ MAIN ENTRY POINT ============

async def main():
    """Run MCP server over stdio"""
    server_instance = server
    
    # Send initialization message
    init_response = await server_instance.handle_request({
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "gemma4", "version": "1.0"}}
    })
    print(json.dumps(init_response), flush=True)
    
    # Send initialized notification
    print(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}), flush=True)
    
    # Main loop
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server_instance.handle_request(request)
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
