import asyncpg

from api.routers.v1.models import AddPlace, GetPlace, GetPlaces
from src.dal.postgres.places import PlacesDB


class PlacesServices:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn
        self.places_db = PlacesDB(conn=conn)

    async def get_places(
            self,
            limit: int,
            offset: int,
            source: str | None = None
    ) -> GetPlaces:
        places = await self.places_db.select(
            limit=limit,
            offset=offset,
            source=source
        )
        return GetPlaces(places=places)

    async def add_place(self, place: AddPlace) -> None:
        nearest_place_data = await self.places_db.get_nearest_place(latitude=place.coordinates.lat,
                                                                    longitude=place.coordinates.lng)

        if not nearest_place_data:
            await self.places_db.insert_place(place)
            raise PlaceAddError

        for nearest_place in nearest_place_data:
            if nearest_place.get('source') == place.source:
                raise PlaceExistError

        place_id = nearest_place_data[0].get('place_id')
        await self.places_db.insert_place_source(place, place_id)

        raise SourceAddError

    async def get_place(self, place_id: int) -> GetPlace | None:
        place = await self.places_db.get(place_id=place_id)
        if not place:
            return
        return GetPlace(
            id=place['id'],
            name=place['name'],
        )


class PlaceExistError(Exception):
    def __init__(self) -> None:
        self.text = 'such a place already exists'


class PlaceAddError(Exception):
    def __init__(self) -> None:
        self.text = 'place added'


class SourceAddError(Exception):
    def __init__(self) -> None:
        self.text = 'source added'
