from models.traffic_models import TrafficCondition


class TrafficParser:
    @staticmethod
    def parse(response: str) -> TrafficCondition:
        return TrafficCondition()
