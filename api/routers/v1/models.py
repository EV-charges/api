from pydantic import BaseModel


class AddPlace(BaseModel):
    name: str


class GetPlace(BaseModel):
    id: int  # noqa
    name: str


class GetPlaces(BaseModel):
    places: list[GetPlace]


class AddPlaceResponse(BaseModel):
    message: str
