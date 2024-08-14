from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from builders.tour_itinerary_builder import TourItineraryBuilder
from models.route_models import TransportationMode
from models.tour_itinerary_models import TourItinerary

app = FastAPI(title="TripEstimatorAPI")


class TourRequest(BaseModel):
    place_a: dict[str, Any]
    place_b: dict[str, Any]
    transportation_method: TransportationMode


tour_builder = TourItineraryBuilder()


@app.post("/travel/", response_model=TourItinerary)
async def build_tour(request: TourRequest):
    try:
        tour_itinerary = tour_builder.build(request.place_a, request.place_b, request.transportation_method)
        return tour_itinerary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=3000)
