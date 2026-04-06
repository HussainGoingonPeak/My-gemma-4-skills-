import urllib.request
import urllib.parse
import json

CITIES = {
    "delhi": (28.61, 77.21, "New Delhi"),
    "new delhi": (28.61, 77.21, "New Delhi"),
    "mumbai": (19.07, 72.88, "Mumbai"),
    "bangalore": (12.97, 77.59, "Bangalore"),
    "kolkata": (22.57, 88.36, "Kolkata"),
    "chennai": (13.08, 80.27, "Chennai"),
    "hyderabad": (17.38, 78.48, "Hyderabad"),
    "pune": (18.52, 73.85, "Pune"),
    "tokyo": (35.67, 139.65, "Tokyo"),
    "japan": (35.67, 139.65, "Tokyo"),
    "london": (51.50, -0.12, "London"),
    "paris": (48.85, 2.35, "Paris"),
    "new york": (40.71, -74.00, "New York"),
    "dubai": (25.20, 55.27, "Dubai"),
    "singapore": (1.35, 103.81, "Singapore"),
    "sydney": (33.86, 151.20, "Sydney"),
    "moscow": (55.75, 37.61, "Moscow"),
    "beijing": (39.90, 116.40, "Beijing"),
    "china": (39.90, 116.40, "Beijing"),
    "bangkok": (13.75, 100.50, "Bangkok"),
    "karachi": (24.86, 67.00, "Karachi"),
    "lahore": (31.52, 74.35, "Lahore"),
    "dhaka": (23.81, 90.41, "Dhaka"),
}

WX = {
    0:"Clear sky", 1:"Mainly clear", 2:"Partly cloudy", 3:"Overcast",
    45:"Fog", 51:"Light drizzle", 61:"Light rain", 63:"Rain",
    65:"Heavy rain", 71:"Light snow", 73:"Snow", 80:"Showers",
    95:"Thunderstorm"
}

def get_current_weather(location: str) -> str:
    try:
        loc = location.lower().strip()
        # Remove digits (pincodes)
        loc = ' '.join(w for w in loc.split() if not w.isdigit())

        # Lookup city
        coords = None
        for key, val in CITIES.items():
            if key in loc or loc in key:
                coords = val
                break

        # Online fallback
        if not coords:
            q = urllib.parse.urlencode({"name": loc, "count": 1, "format": "json"})
            with urllib.request.urlopen(
                f"https://geocoding-api.open-meteo.com/v1/search?{q}", timeout=8
            ) as r:
                d = json.loads(r.read())
            if d.get("results"):
                x = d["results"][0]
                coords = (x["latitude"], x["longitude"], x["name"])

        if not coords:
            return json.dumps({"error": f"City not found: {location}"})

        lat, lon, name = coords
        q = urllib.parse.urlencode({
            "latitude": lat, "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        })
        with urllib.request.urlopen(
            f"https://api.open-meteo.com/v1/forecast?{q}", timeout=8
        ) as r:
            d = json.loads(r.read())

        c = d["current"]
        t = c["temperature_2m"]
        return json.dumps({
            "city": name,
            "temp_c": t,
            "temp_f": round(t * 9/5 + 32, 1),
            "humidity": c["relative_humidity_2m"],
            "wind_kmh": c["wind_speed_10m"],
            "condition": WX.get(c["weather_code"], "Unknown")
        })

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    print(get_current_weather("delhi"))