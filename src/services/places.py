import json

import asyncpg

from api.routers.v1.models import AddComment, AddPlace, GetPlace, GetPlaces, PlaceSources
from src.dal.postgres.places import CommentsDB, PlacesDB


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
            coordinates = {
                'lat': lat,
                'lng': lng
            }
            sources = [PlaceSources.parse_raw(s) for s in place['sources']]
            final_places.append(
                GetPlace(
                    id=place['id'],
                    name=place['name'],
                    coordinates=coordinates,
                    city=place['city'],
                    street=place['street'],
                    sources=sources
                )
            )

        return GetPlaces(places=final_places)

    async def add_place(
            self,
            place: AddPlace
    ) -> str:
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
        if not place:
            return

        json_coordinates = json.loads(place['coordinates'])
        lat = json_coordinates[0]
        lng = json_coordinates[1]
        coordinates = {
            'lat': lat,
            'lng': lng
        }

        sources = [PlaceSources.parse_raw(s) for s in place['sources']]
        return GetPlace(
            id=place['id'],
            name=place['name'],
            coordinates=coordinates,
            city=place['city'],
            street=place['street'],
            sources=sources
        )


class CommentsServices:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn
        self.comments_db = CommentsDB(conn=conn)

    async def add_comment(self, comment: AddComment) -> str:
        response = await self.comments_db.insert_comment(comment)
        if response:
            return "place comment add"
        raise CommentExistError


class PlaceExistError(Exception):
    def __init__(self) -> None:
        self.text = 'such a place already exists'


class CommentExistError(Exception):
    def __init__(self) -> None:
        self.text = 'Place not exists or comment already added'
