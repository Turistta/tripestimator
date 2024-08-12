import logging

from bs4 import BeautifulSoup

from models.cost_models import TRAFFIC_CONDITION_WEIGHT

logger = logging.getLogger(__name__)


class CostParser:
    def parse(self, response: str) -> float:
        try:
            soup = BeautifulSoup(response, "html.parser")
            price_element = soup.find(id="telafinal-precofinal")

            if not price_element:
                raise ValueError("Price element not found in HTML")

            price_txt = price_element.get_text().strip()
            price = float(price_txt.replace(",", "."))

            logger.info(f"Successfully parsed fuel price: {price}")
            return price
        except (AttributeError, ValueError) as e:
            logger.error(f"Error parsing fuel price: {e}")
            raise ValueError(f"Failed to parse fuel price: {e}") from e

    def parse_traffic_condition(self, traffic_condition_str: str) -> float:
        try:
            return TRAFFIC_CONDITION_WEIGHT[traffic_condition_str.strip().lower()]
        except KeyError:
            raise ValueError(f"Unknown traffic condition: {traffic_condition_str}")
