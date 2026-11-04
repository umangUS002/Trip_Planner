import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY") or os.getenv("AVIATION_API_KEY")


def search_flights(query):
    flights = []

    if API_KEY:
        try:
            url = "http://api.aviationstack.com/v1/flights"
            params = {
                "access_key": API_KEY,
                "limit": 5
            }
            response = requests.get(url, params=params, timeout=8)
            data = response.json()

            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                for flight in data["data"][:5]:
                    airline = flight.get("airline", {}).get("name", "Unknown")
                    departure = flight.get("departure", {}).get("airport", "Unknown")
                    arrival = flight.get("arrival", {}).get("airport", "Unknown")
                    status = flight.get("flight_status", "Unknown")

                    flights.append(
                        f"Airline: {airline}\nDeparture: {departure}\nArrival: {arrival}\nStatus: {status}\n"
                    )
        except Exception:
            pass

    # If AviationStack returned no flights (e.g. rate limit, free tier constraints), fallback to Tavily search
    if not flights:
        try:
            from tools.tavily_tool import tavily_search
            return tavily_search(f"Flights and airline options for {query}")
        except Exception:
            pass

    return "\n".join(flights) if flights else "No flight data returned."
