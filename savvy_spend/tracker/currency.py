import requests
from django.conf import settings

BASE_URL = "https://v6.exchangerate-api.com/v6"

def get_exchange_rate(from_currency, to_currency):
    url = f"{BASE_URL}/{settings.EXCHANGE_RATE_API_KEY}/latest/{from_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["conversion_rates"].get(to_currency, None)
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
