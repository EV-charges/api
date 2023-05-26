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
    # TODO: почему source None? ты же взял эту инфу откуда-то
    source: str | None


# TODO: тут такая штука, у одного места может быть много source - поэтому надо расширить модель!


class PlaceSourse(BaseModel):
    inner_id: int
    sourse: str


class GetPlace(BaseModel):
    id: int  # noqa
    name: str
    coordinates: Coordinates
    city: str | None
    street: str | None
    inner_id: int
    # TODO: почему source None
    # source: str | None
    place_sourse: list[PlaceSourse]



class GetPlaces(BaseModel):
    places: list[GetPlace]


class AddPlaceResponse(BaseModel):
    message: str
