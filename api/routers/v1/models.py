from pydantic import BaseModel


class AddPlace(BaseModel):
    lat: float
    lng: float
    name: str
    city: str | None
    street: str | None


class GetPlace(BaseModel):
    id: int  # noqa
    name: str


class GetPlaces(BaseModel):
    places: list[GetPlace]


class AddPlaceResponse(BaseModel):
    message: str
