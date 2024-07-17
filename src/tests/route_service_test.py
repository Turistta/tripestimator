from config import Config
import travel_pb2_grpc as travel_pb2_grpc
import grpc
import travel_pb2 as travel_pb2


def run():
    channel = grpc.insecure_channel(f"localhost:{Config.SERVER_PORT}")
    stub = travel_pb2_grpc.RouteServiceStub(channel)

    request = travel_pb2.RouteRequest(
        origin="New York, NY", destination="Boston, MA", transportation_method="driving"
    )

    response = stub.CalculateRoute(request)

    if response.warnings:
        print(f"Warnings: {response.warnings}")
    else:
        print(f"Origin: {response.route_info.origin}")
        print(f"Destination: {response.route_info.destination}")
        print(f"Distance (km): {response.route_info.distance_km}")
        print(f"Duration: {response.route_info.duration}")
        print("Steps:")
        for step in response.route_info.steps:
            print(f" - {step}")


if __name__ == "__main__":
    run()
