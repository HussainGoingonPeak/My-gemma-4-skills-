import urllib.request
import urllib.parse
import json
import re

# ============================================================
# OFFLINE CITY DATABASE - Works without internet
# ============================================================
CITY_COORDS = {
    # India - Major Cities
    "new delhi": (28.6139, 77.2090, "New Delhi, India"),
    "delhi": (28.6139, 77.2090, "New Delhi, India"),
    "india": (28.6139, 77.2090, "New Delhi, India"),
    "mumbai": (19.0760, 72.8777, "Mumbai, India"),
    "bombay": (19.0760, 72.8777, "Mumbai, India"),
    "bangalore": (12.9716, 77.5946, "Bangalore, India"),
    "bengaluru": (12.9716, 77.5946, "Bengaluru, India"),
    "kolkata": (22.5726, 88.3639, "Kolkata, India"),
    "calcutta": (22.5726, 88.3639, "Kolkata, India"),
    "chennai": (13.0827, 80.2707, "Chennai, India"),
    "madras": (13.0827, 80.2707, "Chennai, India"),
    "hyderabad": (17.3850, 78.4867, "Hyderabad, India"),
    "pune": (18.5204, 73.8567, "Pune, India"),
    "ahmedabad": (23.0225, 72.5714, "Ahmedabad, India"),
    "jaipur": (26.9124, 75.7873, "Jaipur, India"),
    "lucknow": (26.8467, 80.9462, "Lucknow, India"),
    "surat": (21.1702, 72.8311, "Surat, India"),
    "patna": (25.5941, 85.1376, "Patna, India"),
    "bhopal": (23.2599, 77.4126, "Bhopal, India"),
    "indore": (22.7196, 75.8577, "Indore, India"),
    "agra": (27.1767, 78.0081, "Agra, India"),
    "varanasi": (25.3176, 82.9739, "Varanasi, India"),
    "noida": (28.5355, 77.3910, "Noida, India"),
    "gurgaon": (28.4595, 77.0266, "Gurgaon, India"),
    "gurugram": (28.4595, 77.0266, "Gurugram, India"),
    "okhla": (28.5500, 77.2700, "Okhla, New Delhi, India"),
    "faridabad": (28.4089, 77.3178, "Faridabad, India"),
    "ghaziabad": (28.6692, 77.4538, "Ghaziabad, India"),
    "kanpur": (26.4499, 80.3319, "Kanpur, India"),
    "nagpur": (21.1458, 79.0882, "Nagpur, India"),
    "visakhapatnam": (17.6868, 83.2185, "Visakhapatnam, India"),
    "coimbatore": (11.0168, 76.9558, "Coimbatore, India"),
    "kochi": (9.9312, 76.2673, "Kochi, India"),
    "thiruvananthapuram": (8.5241, 76.9366, "Thiruvananthapuram, India"),
    "chandigarh": (30.7333, 76.7794, "Chandigarh, India"),
    "amritsar": (31.6340, 74.8723, "Amritsar, India"),
    "dehradun": (30.3165, 78.0322, "Dehradun, India"),
    "shimla": (31.1048, 77.1734, "Shimla, India"),
    "srinagar": (34.0837, 74.7973, "Srinagar, India"),
    "jammu": (32.7266, 74.8570, "Jammu, India"),
    "ranchi": (23.3441, 85.3096, "Ranchi, India"),
    "bhubaneswar": (20.2961, 85.8245, "Bhubaneswar, India"),
    "guwahati": (26.1445, 91.7362, "Guwahati, India"),
    "raipur": (21.2514, 81.6296, "Raipur, India"),
    "jodhpur": (26.2389, 73.0243, "Jodhpur, India"),
    "udaipur": (24.5854, 73.7125, "Udaipur, India"),
    "mysuru": (12.2958, 76.6394, "Mysuru, India"),
    "mysore": (12.2958, 76.6394, "Mysore, India"),
    "mangalore": (12.9141, 74.8560, "Mangalore, India"),
    "hubli": (15.3647, 75.1240, "Hubli, India"),

    # South Asia
    "karachi": (24.8607, 67.0011, "Karachi, Pakistan"),
    "lahore": (31.5204, 74.3587, "Lahore, Pakistan"),
    "islamabad": (33.6844, 73.0479, "Islamabad, Pakistan"),
    "pakistan": (33.6844, 73.0479, "Islamabad, Pakistan"),
    "dhaka": (23.8103, 90.4125, "Dhaka, Bangladesh"),
    "bangladesh": (23.8103, 90.4125, "Dhaka, Bangladesh"),
    "colombo": (6.9271, 79.8612, "Colombo, Sri Lanka"),
    "sri lanka": (6.9271, 79.8612, "Colombo, Sri Lanka"),
    "kathmandu": (27.7172, 85.3240, "Kathmandu, Nepal"),
    "nepal": (27.7172, 85.3240, "Kathmandu, Nepal"),
    "kabul": (34.5553, 69.2075, "Kabul, Afghanistan"),
    "thimphu": (27.4728, 89.6393, "Thimphu, Bhutan"),
    "bhutan": (27.4728, 89.6393, "Thimphu, Bhutan"),
    "male": (4.1755, 73.5093, "Male, Maldives"),
    "maldives": (4.1755, 73.5093, "Male, Maldives"),

    # East Asia
    "tokyo": (35.6762, 139.6503, "Tokyo, Japan"),
    "japan": (35.6762, 139.6503, "Tokyo, Japan"),
    "osaka": (34.6937, 135.5023, "Osaka, Japan"),
    "kyoto": (35.0116, 135.7681, "Kyoto, Japan"),
    "beijing": (39.9042, 116.4074, "Beijing, China"),
    "china": (39.9042, 116.4074, "Beijing, China"),
    "shanghai": (31.2304, 121.4737, "Shanghai, China"),
    "shenzhen": (22.5431, 114.0579, "Shenzhen, China"),
    "guangzhou": (23.1291, 113.2644, "Guangzhou, China"),
    "hong kong": (22.3193, 114.1694, "Hong Kong"),
    "seoul": (37.5665, 126.9780, "Seoul, South Korea"),
    "south korea": (37.5665, 126.9780, "Seoul, South Korea"),
    "korea": (37.5665, 126.9780, "Seoul, South Korea"),
    "taipei": (25.0330, 121.5654, "Taipei, Taiwan"),
    "taiwan": (25.0330, 121.5654, "Taipei, Taiwan"),
    "ulaanbaatar": (47.8864, 106.9057, "Ulaanbaatar, Mongolia"),

    # Southeast Asia
    "bangkok": (13.7563, 100.5018, "Bangkok, Thailand"),
    "thailand": (13.7563, 100.5018, "Bangkok, Thailand"),
    "singapore": (1.3521, 103.8198, "Singapore"),
    "jakarta": (6.2088, 106.8456, "Jakarta, Indonesia"),
    "indonesia": (6.2088, 106.8456, "Jakarta, Indonesia"),
    "bali": (8.3405, 115.0920, "Bali, Indonesia"),
    "kuala lumpur": (3.1390, 101.6869, "Kuala Lumpur, Malaysia"),
    "malaysia": (3.1390, 101.6869, "Kuala Lumpur, Malaysia"),
    "manila": (14.5995, 120.9842, "Manila, Philippines"),
    "philippines": (14.5995, 120.9842, "Manila, Philippines"),
    "ho chi minh": (10.8231, 106.6297, "Ho Chi Minh City, Vietnam"),
    "hanoi": (21.0278, 105.8342, "Hanoi, Vietnam"),
    "vietnam": (21.0278, 105.8342, "Hanoi, Vietnam"),
    "yangon": (16.8661, 96.1951, "Yangon, Myanmar"),
    "phnom penh": (11.5564, 104.9282, "Phnom Penh, Cambodia"),
    "vientiane": (17.9757, 102.6331, "Vientiane, Laos"),

    # Middle East
    "dubai": (25.2048, 55.2708, "Dubai, UAE"),
    "uae": (25.2048, 55.2708, "Dubai, UAE"),
    "abu dhabi": (24.4539, 54.3773, "Abu Dhabi, UAE"),
    "riyadh": (24.7136, 46.6753, "Riyadh, Saudi Arabia"),
    "saudi arabia": (24.7136, 46.6753, "Riyadh, Saudi Arabia"),
    "doha": (25.2854, 51.5310, "Doha, Qatar"),
    "qatar": (25.2854, 51.5310, "Doha, Qatar"),
    "kuwait": (29.3759, 47.9774, "Kuwait City, Kuwait"),
    "muscat": (23.5880, 58.3829, "Muscat, Oman"),
    "oman": (23.5880, 58.3829, "Muscat, Oman"),
    "manama": (26.2235, 50.5876, "Manama, Bahrain"),
    "bahrain": (26.2235, 50.5876, "Manama, Bahrain"),
    "tehran": (35.6892, 51.3890, "Tehran, Iran"),
    "iran": (35.6892, 51.3890, "Tehran, Iran"),
    "baghdad": (33.3152, 44.3661, "Baghdad, Iraq"),
    "iraq": (33.3152, 44.3661, "Baghdad, Iraq"),
    "amman": (31.9454, 35.9284, "Amman, Jordan"),
    "beirut": (33.8938, 35.5018, "Beirut, Lebanon"),
    "damascus": (33.5138, 36.2765, "Damascus, Syria"),
    "jerusalem": (31.7683, 35.2137, "Jerusalem"),
    "tel aviv": (32.0853, 34.7818, "Tel Aviv, Israel"),
    "israel": (31.7683, 35.2137, "Jerusalem, Israel"),
    "ankara": (39.9334, 32.8597, "Ankara, Turkey"),
    "istanbul": (41.0082, 28.9784, "Istanbul, Turkey"),
    "turkey": (39.9334, 32.8597, "Ankara, Turkey"),

    # Europe
    "london": (51.5074, -0.1278, "London, UK"),
    "uk": (51.5074, -0.1278, "London, UK"),
    "england": (51.5074, -0.1278, "London, England"),
    "manchester": (53.4808, -2.2426, "Manchester, UK"),
    "birmingham": (52.4862, -1.8904, "Birmingham, UK"),
    "edinburgh": (55.9533, -3.1883, "Edinburgh, Scotland"),
    "paris": (48.8566, 2.3522, "Paris, France"),
    "france": (48.8566, 2.3522, "Paris, France"),
    "berlin": (52.5200, 13.4050, "Berlin, Germany"),
    "germany": (52.5200, 13.4050, "Berlin, Germany"),
    "munich": (48.1351, 11.5820, "Munich, Germany"),
    "hamburg": (53.5753, 10.0153, "Hamburg, Germany"),
    "madrid": (40.4168, -3.7038, "Madrid, Spain"),
    "spain": (40.4168, -3.7038, "Madrid, Spain"),
    "barcelona": (41.3851, 2.1734, "Barcelona, Spain"),
    "rome": (41.9028, 12.4964, "Rome, Italy"),
    "italy": (41.9028, 12.4964, "Rome, Italy"),
    "milan": (45.4642, 9.1900, "Milan, Italy"),
    "amsterdam": (52.3676, 4.9041, "Amsterdam, Netherlands"),
    "netherlands": (52.3676, 4.9041, "Amsterdam, Netherlands"),
    "brussels": (50.8503, 4.3517, "Brussels, Belgium"),
    "belgium": (50.8503, 4.3517, "Brussels, Belgium"),
    "vienna": (48.2082, 16.3738, "Vienna, Austria"),
    "austria": (48.2082, 16.3738, "Vienna, Austria"),
    "zurich": (47.3769, 8.5417, "Zurich, Switzerland"),
    "switzerland": (47.3769, 8.5417, "Zurich, Switzerland"),
    "stockholm": (59.3293, 18.0686, "Stockholm, Sweden"),
    "sweden": (59.3293, 18.0686, "Stockholm, Sweden"),
    "oslo": (59.9139, 10.7522, "Oslo, Norway"),
    "norway": (59.9139, 10.7522, "Oslo, Norway"),
    "copenhagen": (55.6761, 12.5683, "Copenhagen, Denmark"),
    "denmark": (55.6761, 12.5683, "Copenhagen, Denmark"),
    "helsinki": (60.1699, 24.9384, "Helsinki, Finland"),
    "finland": (60.1699, 24.9384, "Helsinki, Finland"),
    "lisbon": (38.7169, -9.1395, "Lisbon, Portugal"),
    "portugal": (38.7169, -9.1395, "Lisbon, Portugal"),
    "athens": (37.9838, 23.7275, "Athens, Greece"),
    "greece": (37.9838, 23.7275, "Athens, Greece"),
    "warsaw": (52.2297, 21.0122, "Warsaw, Poland"),
    "poland": (52.2297, 21.0122, "Warsaw, Poland"),
    "prague": (50.0755, 14.4378, "Prague, Czech Republic"),
    "budapest": (47.4979, 19.0402, "Budapest, Hungary"),
    "bucharest": (44.4268, 26.1025, "Bucharest, Romania"),
    "moscow": (55.7558, 37.6173, "Moscow, Russia"),
    "russia": (55.7558, 37.6173, "Moscow, Russia"),
    "st petersburg": (59.9311, 30.3609, "St. Petersburg, Russia"),
    "kyiv": (50.4501, 30.5234, "Kyiv, Ukraine"),
    "ukraine": (50.4501, 30.5234, "Kyiv, Ukraine"),

    # Americas
    "new york": (40.7128, -74.0060, "New York, USA"),
    "usa": (40.7128, -74.0060, "New York, USA"),
    "america": (40.7128, -74.0060, "New York, USA"),
    "los angeles": (34.0522, -118.2437, "Los Angeles, USA"),
    "chicago": (41.8781, -87.6298, "Chicago, USA"),
    "houston": (29.7604, -95.3698, "Houston, USA"),
    "washington": (38.9072, -77.0369, "Washington DC, USA"),
    "miami": (25.7617, -80.1918, "Miami, USA"),
    "san francisco": (37.7749, -122.4194, "San Francisco, USA"),
    "seattle": (47.6062, -122.3321, "Seattle, USA"),
    "toronto": (43.6532, -79.3832, "Toronto, Canada"),
    "canada": (43.6532, -79.3832, "Toronto, Canada"),
    "vancouver": (49.2827, -123.1207, "Vancouver, Canada"),
    "montreal": (45.5017, -73.5673, "Montreal, Canada"),
    "mexico city": (19.4326, -99.1332, "Mexico City, Mexico"),
    "mexico": (19.4326, -99.1332, "Mexico City, Mexico"),
    "sao paulo": (23.5505, -46.6333, "São Paulo, Brazil"),
    "brazil": (23.5505, -46.6333, "São Paulo, Brazil"),
    "rio de janeiro": (22.9068, -43.1729, "Rio de Janeiro, Brazil"),
    "buenos aires": (34.6037, -58.3816, "Buenos Aires, Argentina"),
    "argentina": (34.6037, -58.3816, "Buenos Aires, Argentina"),
    "bogota": (4.7110, -74.0721, "Bogotá, Colombia"),
    "colombia": (4.7110, -74.0721, "Bogotá, Colombia"),
    "lima": (12.0464, -77.0428, "Lima, Peru"),
    "peru": (12.0464, -77.0428, "Lima, Peru"),
    "santiago": (33.4489, -70.6693, "Santiago, Chile"),
    "chile": (33.4489, -70.6693, "Santiago, Chile"),

    # Africa
    "cairo": (30.0444, 31.2357, "Cairo, Egypt"),
    "egypt": (30.0444, 31.2357, "Cairo, Egypt"),
    "nairobi": (1.2921, 36.8219, "Nairobi, Kenya"),
    "kenya": (1.2921, 36.8219, "Nairobi, Kenya"),
    "lagos": (6.5244, 3.3792, "Lagos, Nigeria"),
    "nigeria": (9.0820, 8.6753, "Abuja, Nigeria"),
    "abuja": (9.0820, 8.6753, "Abuja, Nigeria"),
    "johannesburg": (26.2041, 28.0473, "Johannesburg, South Africa"),
    "south africa": (26.2041, 28.0473, "Johannesburg, South Africa"),
    "cape town": (33.9249, 18.4241, "Cape Town, South Africa"),
    "addis ababa": (9.0320, 38.7469, "Addis Ababa, Ethiopia"),
    "ethiopia": (9.0320, 38.7469, "Addis Ababa, Ethiopia"),
    "accra": (5.6037, -0.1870, "Accra, Ghana"),
    "ghana": (5.6037, -0.1870, "Accra, Ghana"),
    "casablanca": (33.5731, -7.5898, "Casablanca, Morocco"),
    "morocco": (33.5731, -7.5898, "Casablanca, Morocco"),
    "tunis": (36.8190, 10.1658, "Tunis, Tunisia"),
    "algiers": (36.7372, 3.0865, "Algiers, Algeria"),
    "khartoum": (15.5518, 32.5324, "Khartoum, Sudan"),
    "dar es salaam": (6.7924, 39.2083, "Dar es Salaam, Tanzania"),

    # Oceania
    "sydney": (33.8688, 151.2093, "Sydney, Australia"),
    "australia": (33.8688, 151.2093, "Sydney, Australia"),
    "melbourne": (37.8136, 144.9631, "Melbourne, Australia"),
    "brisbane": (27.4698, 153.0251, "Brisbane, Australia"),
    "perth": (31.9505, 115.8605, "Perth, Australia"),
    "auckland": (36.8485, 174.7633, "Auckland, New Zealand"),
    "new zealand": (36.8485, 174.7633, "Auckland, New Zealand"),
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_location(location: str) -> str:
    """Remove pincodes and normalize location string."""
    # Remove 5-6 digit pincodes
    cleaned = re.sub(r'\b\d{5,6}\b', '', location)
    # Remove extra spaces
    cleaned = ' '.join(cleaned.split()).strip().lower()
    return cleaned


def offline_lookup(location: str):
    """Search hardcoded city database."""
    loc = clean_location(location)

    # Exact match
    if loc in CITY_COORDS:
        return CITY_COORDS[loc]

    # Partial match - location contains a key
    for key, val in CITY_COORDS.items():
        if key in loc:
            return val

    # Partial match - key contains location
    for key, val in CITY_COORDS.items():
        if loc in key:
            return val

    return None


def online_lookup(location: str):
    """Live geocoding via Open-Meteo API."""
    try:
        query = urllib.parse.urlencode({
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        })
        url = f"https://geocoding-api.open-meteo.com/v1/search?{query}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if data.get("results"):
            r = data["results"][0]
            country = r.get("country", "")
            name = r.get("name", location)
            full_name = f"{name}, {country}" if country else name
            return r["latitude"], r["longitude"], full_name
    except Exception:
        pass
    return None


def get_coordinates(location: str):
    """
    Smart coordinate resolver:
    1. Try offline database first (instant, no internet)
    2. Fall back to live geocoding API
    3. Try cleaned location string in both
    """
    # Step 1: Try offline with original input
    result = offline_lookup(location)
    if result:
        return result[0], result[1], result[2]

    # Step 2: Try online with original input
    result = online_lookup(location)
    if result:
        return result[0], result[1], result[2]

    # Step 3: Clean location and retry offline
    cleaned = clean_location(location)
    if cleaned != location.lower():
        result = offline_lookup(cleaned)
        if result:
            return result[0], result[1], result[2]

        # Step 4: Clean location and retry online
        result = online_lookup(cleaned)
        if result:
            return result[0], result[1], result[2]

    return None, None, None


def celsius_to_fahrenheit(c):
    return round((c * 9 / 5) + 32, 1)


def get_wind_direction(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(degrees / 45) % 8]


WEATHER_CODES = {
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
    96: "⛈️ Thunderstorm + Hail",
    99: "⛈️ Heavy Thunderstorm + Hail"
}

# ============================================================
# MAIN FUNCTION
# ============================================================

def get_current_weather(location: str) -> str:
    """
    Fetch real-time weather for any location on Earth.
    Uses offline DB first, then live geocoding as fallback.
    Weather data always fetched live from Open-Meteo API.
    No API key required.
    """
    try:
        lat, lon, city_name = get_coordinates(location)

        if lat is None:
            return json.dumps({
                "error": True,
                "message": f"Could not find location: '{location}'",
                "suggestion": "Try a major city name e.g. 'Mumbai', 'Tokyo', 'London'"
            })

        # Fetch live weather data
        params = urllib.parse.urlencode({
            "latitude": lat,
            "longitude": lon,
            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "weather_code",
                "wind_speed_10m",
                "wind_direction_10m",
                "precipitation",
                "surface_pressure",
                "visibility",
                "uv_index"
            ]),
            "timezone": "auto",
            "wind_speed_unit": "kmh"
        })

        url = f"https://api.open-meteo.com/v1/forecast?{params}"

        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        current = data.get("current", {})
        code = current.get("weather_code", 0)
        temp_c = current.get("temperature_2m", 0)
        feels_c = current.get("apparent_temperature", 0)
        wind_deg = current.get("wind_direction_10m", 0)

        return json.dumps({
            "error": False,
            "location": city_name,
            "condition": WEATHER_CODES.get(code, "🌡️ Unknown"),
            "temperature_c": temp_c,
            "temperature_f": celsius_to_fahrenheit(temp_c),
            "feels_like_c": feels_c,
            "feels_like_f": celsius_to_fahrenheit(feels_c),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "wind_direction": get_wind_direction(wind_deg),
            "precipitation_mm": current.get("precipitation", 0),
            "pressure_hpa": current.get("surface_pressure"),
            "visibility_m": current.get("visibility"),
            "uv_index": current.get("uv_index"),
            "timezone": data.get("timezone", ""),
            "source": "Open-Meteo (live)"
        })

    except Exception as e:
        return json.dumps({
            "error": True,
            "message": f"Weather fetch failed: {str(e)}",
            "suggestion": "Please try again in a moment."
        })


# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    tests = ["new delhi 110020", "japan", "okhla new delhi",
             "london", "tokyo", "sydney", "unknown city xyz"]
    for city in tests:
        result = json.loads(get_current_weather(city))
        if result["error"]:
            print(f"❌ {city}: {result['message']}")
        else:
            print(f"✅ {result['location']}: {result['condition']} {result['temperature_c']}°C / {result['temperature_f']}°F")