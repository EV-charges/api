import json

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
        final_places = []

        for place in places:
            json_coordinates = json.loads(place['coordinates'])
            lat = json_coordinates[0]
            lng = json_coordinates[1]
            coordinates = {'lat': lat,
                           'lng': lng}

            final_places.append(
                GetPlace(
                    id=place['id'],
                    name=place['name'],
                    coordinates=coordinates,
                    city=place['city'],
                    street=place['street'],
                    source=place['sources']))

        return GetPlaces(places=final_places)

    async def add_place(self, place: AddPlace) -> str:
        nearest_place_data = await self.places_db.get_nearest_place(
            latitude=place.coordinates.lat,
            longitude=place.coordinates.lng
        )

        if not nearest_place_data:
            await self.places_db.insert_place(place)
            return "place add"

        if place.source in nearest_place_data.get('sources'):
            raise PlaceExistError

        place_id = nearest_place_data.get('id')
        await self.places_db.insert_place_source(place, place_id)
        return "place source add"

    async def get_place(self, place_id: int) -> GetPlace | None:
        place = await self.places_db.get(place_id=place_id)
        json_coordinates = json.loads(place['coordinates'])
        lat = json_coordinates[0]
        lng = json_coordinates[1]
        coordinates = {'lat': lat,
                       'lng': lng}
        if not place:
            return
        return GetPlace(
            id=place['id'],
            name=place['name'],
            coordinates=coordinates,
            city=place['city'],
            street=place['street'],
            inner_id=place['inner_id'],
            source=place['source']
        )


class PlaceExistError(Exception):
    def __init__(self) -> None:
        self.text = 'such a place already exists'
