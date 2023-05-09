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
        await self.places_db.insert(name=place.name)

    async def get_place(self, place_id: int) -> GetPlace | None:
        place = await self.places_db.get(place_id=place_id)
        if not place:
            return
        return GetPlace(
            id=place['id'],
            name=place['name'],
        )
