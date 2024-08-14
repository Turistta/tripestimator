from typing import Annotated

import uvicorn
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field

from builders.tour_itinerary_builder import PlaceQuery, TourItineraryBuilder
from models.route_models import TransportationMode
from models.tour_itinerary_models import TourItinerary

app = FastAPI(title="TripEstimatorAPI")


class TourRequest(BaseModel):
    place_a: Annotated[
        PlaceQuery,
        Field(
            ...,
            examples=[{"place_a": {"text_input": "Art Museum of Goiânia", "inputtype": "textquery"}}],
        ),
    ]
    place_b: Annotated[
        PlaceQuery,
        Field(
            ...,
            examples=[{"place_b": {"text_input": "Central Bus Station of Goiânia", "inputtype": "textquery"}}],
        ),
    ]
    transportation_method: Annotated[TransportationMode, Field(examples=[])]


tour_builder = TourItineraryBuilder()


@app.post("/travel/", response_model=TourItinerary, description="Returns a travel estimation between two routes.")
async def build_tour(
    place_a: Annotated[PlaceQuery, Body()],
    place_b: Annotated[PlaceQuery, Body()],
    transportation_method: Annotated[TransportationMode, Body()],
):
    try:
        tour_itinerary = tour_builder.build(place_a, place_b, transportation_method)
        return tour_itinerary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=3000, reload=True)


