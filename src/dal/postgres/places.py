import asyncpg

from api.routers.v1.models import AddPlace


class PlacesDB:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def select(
            self,
            limit: int,
            offset: int,
            source: str | None = None
    ) -> list[asyncpg.Record]:
        pass

    async def insert(
            self,
            place: AddPlace
    ) -> None:
        await self.conn.execute(
            """
            INSERT INTO places (location, name, city, street)
            VALUES (ST_Point($1, $2, 4326), $3, $4, $5)
            """,
            place.lat,
            place.lng,
            place.name,
            place.city,
            place.street
        )

    async def get(self, place_id: int) -> asyncpg.Record:
        place = await self.conn.fetchrow(
            """
            SELECT * FROM places WHERE id = $1
            """,
            place_id
        )
        return place

    async def get_nearest_place(self, latitude: float, longitude: float) -> asyncpg.Record:
        place = await self.conn.fetchrow(
            """
            SELECT id, name
            FROM places
            WHERE ST_Distance(location, ST_POINT($1, $2)) <= 10
            """,
            latitude,
            longitude
        )
        return place
