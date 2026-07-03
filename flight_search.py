import os

import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_FLIGHT_API = "https://serpapi.com/search"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["API_KEY_SERP_API"]

    def check_flights(
        self,
        origin_city_code,
        destination_city_code,
        from_time,
        is_direct=True,
    ):
        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time,
            "type": "2",
            "adults": "1",
            "stops": "1" if is_direct else "2",
            "currency": "EUR",
            "api_key": self._api_key,
        }

        response = requests.get(GOOGLE_FLIGHT_API, params=params)
        response.raise_for_status()

        return response.json()
