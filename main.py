from datetime import datetime, timedelta

import requests_cache

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
# ================= CACHE =================
requests_cache.install_cache("flight_cache", expire_after=3600)


# ================= DATES =================
TODAY = datetime.now()
TOMORROW = (TODAY + timedelta(days=1)).strftime("%Y-%m-%d")


# ================= SERVICES =================
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()


# ================= DATA =================
sheet_data = data_manager.get_destination_data()


# ================= MAIN LOOP =================

customer_emails = data_manager.get_customer_emails()


def get_flights(country: dict, is_direct: bool):
    return flight_search.check_flights(
        origin_city_code="LHR",
        destination_city_code=country["iataCode"],
        from_time=TOMORROW,
        is_direct=is_direct,
    )


for country in sheet_data:
    logger.info(f"🔎 Searching flights to {country['city']} ({country['iataCode']})")

    # 1. DIRECT
    try:
        flight_data = get_flights(country, True)

        if not flight_data.get("best_flights"):
            logger.warning(f"❌ No direct flight to {country['city']}. Searching indirect...")
            flight_data = get_flights(country, False)
    except Exception as e:
        logger.error(f"Erreur API pour {country['city']}: {e}", exc_info=True)
        continue
    if not flight_data.get("best_flights"):
        logger.warning("❌ No flights at all")
        continue

    flights = [FlightData(f) for f in flight_data["best_flights"]]

    cheapest = min(flights, key=lambda x: x.price)

    logger.info(f"💰 Price: {cheapest.price}")
    logger.info(f"✈️ Airline: {cheapest.airline}")
    logger.info(f"🛑 Stops: {cheapest.stops}")
    if cheapest.price < country["lowestPrice"]:
        logger.info("🔥 DEAL FOUND!")
        data_manager.update_lowest_price(country["id"], cheapest.price)
        notification_manager.send_email(
            emails=customer_emails,
            message=(
                f"🔥 Low price alert!\n"
                f"{country['city']} ({country['iataCode']})\n"
                f"Price: GBP {cheapest.price}\n"
                f"Airline: {cheapest.airline}\n"
                f"Stops: {cheapest.stops}"
            ),
        )
