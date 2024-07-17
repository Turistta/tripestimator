from config import Config
import travel_pb2_grpc as travel_pb2_grpc
import grpc
import travel_pb2 as travel_pb2


def run():
    channel = grpc.insecure_channel(f"localhost:{Config.SERVER_PORT}")
    stub = travel_pb2_grpc.PlaceServiceStub(channel)

    request = travel_pb2.PlaceRequest(place="Goiânia, GO")
    response = stub.ValidatePlace(request)

    if response.warnings:
        print(f"Warnings: {response.warnings}")
    else:
        print(f"Name: {response.place_info.name}")
        print(f"Address: {response.place_info.address}")
        print(f"Latitude: {response.place_info.latitude}")
        print(f"Longitude: {response.place_info.longitude}")
        print(f"Place ID: {response.place_info.place_id}")
        print(f"Types: {response.place_info.types}")
        for review in response.place_info.reviews:
            print(
                f"Review by {review.author_name}: {review.text} (Rating: {review.rating})"
            )
        for picture in response.place_info.pictures:
            print(
                f"Picture URL: https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={picture.url}&key={Config.GOOGLE_MAPS_API_KEY}, Width: {picture.width}, Height: {picture.height}"
            )


if __name__ == "__main__":
    run()
