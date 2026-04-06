import urllib.request
import json

def get_current_weather(location: str) -> str:
    try:
        loc = location.strip().replace(" ", "+")
        url = f"https://wttr.in/{loc}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())

        c = d["current_condition"][0]
        area = d["nearest_area"][0]
        city = area["areaName"][0]["value"]
        country = area["country"][0]["value"]
        temp_c = int(c["temp_C"])

        return json.dumps({
            "city": f"{city}, {country}",
            "temp_c": temp_c,
            "temp_f": int(c["temp_F"]),
            "humidity": c["humidity"],
            "wind_kmh": c["windspeedKmph"],
            "condition": c["weatherDesc"][0]["value"]
        })

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    print(get_current_weather("mumbai"))