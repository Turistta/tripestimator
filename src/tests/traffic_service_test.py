from config import Config
import travel_pb2_grpc as travel_pb2_grpc
import grpc
import travel_pb2 as travel_pb2


def run():
    channel = grpc.insecure_channel(f"localhost:{Config.SERVER_PORT}")
    stub = travel_pb2_grpc.TrafficServiceStub(channel)

    request = travel_pb2.TrafficRequest(
        start_coords="-16.694015,-49.2578243",  # Praça Cívica, Goiânia
        end_coords="-16.7083507,-49.2753839",  # Goiânia Shopping
        vehicle_type="",
        avoid_toll_roads=False,
        avoid_subscription_roads=False,
        avoid_ferries=False,
    )
    response = stub.GetTrafficInfo(request)

    if response.warnings:
        print(f"Warnings: {response.warnings}")
    else:
        time_estimate = response.time_estimate
        print(f"Distance: {time_estimate.distance} km")
        print(f"Estimated Time: {time_estimate.estimated_time} minutes")
        print(f"Traffic Condition: {time_estimate.traffic_condition}%")


if __name__ == "__main__":
    run()
