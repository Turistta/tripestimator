from config import Config
import travel_pb2_grpc as travel_pb2_grpc
import grpc
import travel_pb2 as travel_pb2


def run():
    channel = grpc.insecure_channel(f"localhost:{Config.SERVER_PORT}")
    stub = travel_pb2_grpc.TravelEstimatorStub(channel)

    request = travel_pb2.TravelRequest(
        
    )


if __name__ == "__main__":
    run()
