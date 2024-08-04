import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class FuelPriceParser:
    @staticmethod
    def parse_fuel_price(html_text: str) -> float:
        try:
            soup = BeautifulSoup(html_text, "html.parser")
            price_txt = soup.find(id="telafinal-precofinal").get_text()
            price = float(price_txt.replace(",", "."))
            return price
        except (AttributeError, ValueError) as e:
            logger.error(f"Parsing error: {e}")
            return 0
