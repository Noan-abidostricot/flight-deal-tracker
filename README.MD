# Flight Deal Tracker

Monitors flight prices for a list of destinations and sends email alerts
when a fare drops below the lowest price on record.

## Tech stack

Python 3.12 · SerpAPI (Google Flights) · Sheety (Google Sheets as API)
· smtplib · requests-cache

## Features

- Searches direct flights first, falls back to 1-stop if none found
- Compares against a per-destination minimum stored in Google Sheets
- Updates the minimum on each run
- Sends email alerts to all registered subscribers

## Prerequisites

- Python 3.10+
- A [SerpAPI](https://serpapi.com) account (free tier works)
- A [Sheety](https://sheety.co) project with two sheets: `prices` and `users`

## Installation

```bash
git clone https://github.com/Noan-abidostricot/flight-deal-tracker.git
cd flight-deal-tracker
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the root of the project:

```
API_KEY_SERP_API=your_api_serpapi

URL_SHEETY_FLIGHT=url_of_your_sheety_flight_prices
URL_SHEETY_USERS=url_of_your_sheety_users
SHEETY_USERNAME=your_sheety_username
SHEETY_PASSWORD=your_sheety_password

EMAIL=your_email_address_related_to_your_smtp
PASSWORD=your_smtp_password

```

## Usage

```bash
python main.py
```

## Project structure

| File | Role |
|---|---|
| `main.py` | Orchestrates the full pipeline |
| `flight_search.py` | Wraps SerpAPI, returns raw JSON |
| `flight_data.py` | Structures a single flight result |
| `data_manager.py` | Reads/writes Google Sheets via Sheety |
| `notification_manager.py` | Sends email alerts |
