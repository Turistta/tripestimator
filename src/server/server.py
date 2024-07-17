import travel_pb2_grpc as travel_pb2_grpc
import travel_pb2 as travel_pb2
import grpc
from services.traffic_service import TrafficService
from services.place_service import PlaceService
from services.route_service import RouteService
from services.cost_service import CostService
from concurrent import futures
from config import Config


class TravelEstimatorServicer(travel_pb2_grpc.TravelEstimatorServicer):
    def __init__(self):
        self.place_service = PlaceService()
        self.route_service = RouteService()
        self.traffic_service = TrafficService()
        self.cost_service = CostService()

    def GetTravelEstimates(self, request, context):
        route_response = self.route_service.calculate_route(
            request.origin, request.destination, request.transportation_method
        )
        if not route_response.route_info:
            return travel_pb2.TravelResponse(warnings=["Route calculation failed"])

        traffic_response = self.traffic_service.get_traffic_info(
            route_response.route_info.origin
            + "_"
            + route_response.route_info.destination
        )
        if not traffic_response.time_estimate:
            return travel_pb2.TravelResponse(warnings=["Traffic info retrieval failed"])

        cost_response = self.cost_service.estimate_cost(
            route_response.route_info.distance_km,
            traffic_response.time_estimate.traffic_condition,
        )
        if not cost_response.cost_estimate:
            return travel_pb2.TravelResponse(warnings=["Cost estimation failed"])

        return travel_pb2.TravelResponse(
            route_info=route_response.route_info,
            time_estimate=traffic_response.time_estimate,
            cost_estimate=cost_response.cost_estimate,
        )


class PlaceServiceServicer(travel_pb2_grpc.PlaceServiceServicer):
    def __init__(self):
        self.place_service = PlaceService()

    def ValidatePlace(self, request, context):
        return self.place_service.validate_place(request.place)


class RouteServiceServicer(travel_pb2_grpc.RouteServiceServicer):
    def __init__(self):
        self.route_service = RouteService()

    def CalculateRoute(self, request, context):
        return self.route_service.calculate_route(
            request.origin, request.destination, request.transportation_method
        )


class TrafficServiceServicer(travel_pb2_grpc.TrafficServiceServicer):
    def __init__(self):
        self.traffic_service = TrafficService()

    def GetTrafficInfo(self, request, context):
        return self.traffic_service.get_traffic_info(request.route_id)


class CostServiceServicer(travel_pb2_grpc.CostServiceServicer):
    def __init__(self):
        self.cost_service = CostService()

    def EstimateCost(self, request, context):
        return self.cost_service.estimate_cost(
            request.state,
            request.distance_km,
            request.time_estimated,
            request.traffic_condition,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_TravelEstimatorServicer_to_server(
        TravelEstimatorServicer(), server
    )
    travel_pb2_grpc.add_PlaceServiceServicer_to_server(PlaceServiceServicer(), server)
    travel_pb2_grpc.add_RouteServiceServicer_to_server(RouteServiceServicer(), server)
    travel_pb2_grpc.add_TrafficServiceServicer_to_server(
        TrafficServiceServicer(), server
    )
    travel_pb2_grpc.add_CostServiceServicer_to_server(CostServiceServicer(), server)
    server.add_insecure_port(f"[::]:{Config.SERVER_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
