{
  "name": "realtime_weather",
  "version": "1.0.0",
  "description": "Get real-time weather data for any location worldwide using Open-Meteo API. Provides current conditions, hourly forecasts, and daily predictions. Invoke when user asks about weather, temperature, rain, wind, forecasts, or atmospheric conditions.",
  "author": "Community",
  "license": "MIT",
  "mcp_server": {
    "command": "python3",
    "args": ["mcp_server/server.py"],
    "env": {},
    "timeout": 30
  },
  "tools": [
    {
      "name": "get_current_weather",
      "description": "Get current weather conditions for a specific location. Use when user asks 'what's the weather now', 'current temperature', or 'is it raining'."
    },
    {
      "name": "get_hourly_forecast",
      "description": "Get hour-by-hour weather forecast. Use when user asks about weather for specific hours, 'will it rain this afternoon', or hourly predictions."
    },
    {
      "name": "get_daily_forecast",
      "description": "Get multi-day weather forecast. Use when user asks 'weather this week', 'forecast for next days', or daily predictions."
    },
    {
      "name": "search_location",
      "description": "Search for a location by name to get coordinates. Use when user provides a city name without coordinates, or to disambiguate locations."
    }
  ],
  "permissions": ["internet", "location_services"],
  "examples": [
    "What's the weather in Tokyo?",
    "Will it rain in London tomorrow?",
    "Hourly forecast for New York",
    "Weather for Paris this week"
  ]
}
