from typing import Annotated

import uvicorn
from fastapi import Body, FastAPI, HTTPException

from builders.tour_itinerary_builder import TourItineraryBuilder
from config import settings
from models.tour_itinerary_models import TourItinerary, TourRequest

app = FastAPI(title="TripEstimatorAPI")


tour_builder = TourItineraryBuilder()


@app.post("/travel/", response_model=TourItinerary, description="Returns a travel estimation between two routes.")
async def build_tour(
    tour_request: Annotated[TourRequest, Body(openapi_examples=TourRequest.Config.schema_extra["examples"])],  # type: ignore
):
    try:
        tour_itinerary = tour_builder.build(
            tour_request.place_a, tour_request.place_b, tour_request.transportation_method
        )
        return tour_itinerary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=settings.server_port, reload=True)  # type: ignore
