from config import Config
import travel_pb2_grpc as travel_pb2_grpc
import grpc
import travel_pb2 as travel_pb2


def run():
    channel = grpc.insecure_channel(f"localhost:{Config.SERVER_PORT}")
    stub = travel_pb2_grpc.CostServiceStub(channel)
    request = travel_pb2.CostRequest(
        state="go", distance_km=12.5, time_estimated=4000, traffic_condition="moderate"
    )
    response = stub.EstimateCost(request)

    if response.warnings:
        print(f"Warnings: {response.warnings}")
    else:
        print(f"Estimated price: {response.cost_estimate.estimated_cost}")


if __name__ == "__main__":
    run()
