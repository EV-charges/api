import datetime

from pydantic import BaseModel


class Coordinates(BaseModel):
    lat: float
    lng: float


class AddPlace(BaseModel):
    inner_id: int
    coordinates: Coordinates
    name: str
    city: str | None
    street: str | None
    source: str


class AddComment(BaseModel):
    place_id: int
    comment_id: int
    author: str
    text: str
    publication_date: datetime.datetime
    source: str


class PlaceSources(BaseModel):
    inner_id: int
    source: str


class GetPlace(BaseModel):
    id: int  # noqa
    name: str
    coordinates: Coordinates
    city: str | None
    street: str | None
    sources: list[PlaceSources]


class GetPlaces(BaseModel):
    places: list[GetPlace]


class AddPlaceResponse(BaseModel):
    message: str
