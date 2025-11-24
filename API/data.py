"""
This module is responsible for fetching and processing data from the external API.
"""

import logging
import os
import requests
from dotenv import load_dotenv

# Load .env File
load_dotenv()

# ------------------------------
# Logging Module Configuration
# ------------------------------
logger = logging.getLogger()

# --------------------------------------------------
# API Configuration
# --------------------------------------------------
API_URL = os.getenv('API_URL')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}


def fetch_data_from_api():
    """
    Attempts to fetch data from the API and handles potential errors.
    Returns JSON data on success, or None on failure.
    """
    if not API_URL:
        logger.error("API_URL is not set in environment variables.")
        return None

    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        #  if status_code == 200
        response_data = response.json()
        logger.info("API data successfully fetched.")
        return response_data

    except requests.exceptions.RequestException as e:
        # logging.error has been removed to avoid duplicate logs in main.py
        logger.warning("API fetch failed. Error: %s", e)
        return None

    except Exception as e:
        logger.error("A critical and unexpected error occurred: %s", e)
        return None


def get_gold_prices():
    """
    Retrieve current gold and coin prices from the API response.
    Fetches data on every call.

    Returns:
        dict: A dictionary containing gold item names as keys
              and their corresponding prices as values, or None if data fetching fails.
    """
    data = fetch_data_from_api()
    if not data:
        return None

    try:
        gold = data.get('gold')
        if not gold:
            logger.error("API response is missing the 'gold' key or it is empty.")
            return {}
    except AttributeError:
        logger.error("API response is not in expected format.")
        return {}

    gold_dict = {}

    for item in gold:
        name = item.get('name')
        price = item.get('price')
        if name and price is not None:
            gold_dict.update({name: price})
    return gold_dict


def get_currency_prices():
    """
    Retrieve current currency exchange rates from the API response.
    Fetches data on every call.

    Returns:
        dict: A dictionary with currency names as keys
              and their corresponding prices as values, or None if data fetching fails.
    """
    data = fetch_data_from_api()
    if not data:
        return None

    try:
        currency = data.get('currency')
        if not currency:
            logger.error("API response is missing the 'currency' key or it is empty.")
            return {}
    except AttributeError:
        logger.error("API response is not in expected format.")
        return {}

    currency_dict = {}

    for item in currency:
        name = item.get('name')
        price = item.get('price')
        if name and price is not None:
            currency_dict.update({name: price})
    return currency_dict


def get_cryptocurrency_prices():
    """
    Retrieve cryptocurrency market prices from the API response.
    Fetches data on every call.

    Returns:
        dict: A dictionary containing cryptocurrency names as keys
              and their corresponding prices as values, or None if data fetching fails.
    """
    data = fetch_data_from_api()
    if not data:
        return None

    try:
        cryptocurrency = data.get('cryptocurrency')
        if not cryptocurrency:
            logger.error("API response is missing the 'cryptocurrency' key or it is empty.")
            return {}
    except AttributeError:
        logger.error("API response is not in expected format.")
        return {}

    cryptocurrency_dict = {}

    for item in cryptocurrency:
        name = item.get('name')
        price = item.get('price')
        if name and price is not None:
            cryptocurrency_dict.update({name: price})
    return cryptocurrency_dict
