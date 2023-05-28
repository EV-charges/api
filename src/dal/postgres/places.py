import asyncpg

from api.routers.v1.models import AddPlace
from settings import app_settings


class PlacesDB:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def select(
            self,
            limit: int,
            offset: int,
            source: str | None = None
    ) -> list[asyncpg.Record]:
        query = """
            SELECT p.id, ST_AsGeoJson(location)::jsonb, name, city, street, ps.inner_id, ps.source
            FROM places p
            LEFT JOIN places_sources ps ON p.id = ps.place_id
        """
        parameters = [limit, offset]

        if source is not None:
            query += " WHERE ps.source = $3"
            parameters.append(source)

        query += " LIMIT $1 OFFSET $2;"

        return await self.conn.fetch(query, *parameters)

    async def insert_place(
            self,
            place: AddPlace
    ) -> None:
        await self.conn.execute(
            """
            WITH place_data AS (
            INSERT INTO places (location, name, city, street)
            VALUES (ST_Point($1, $2, 4326), $3, $4, $5)
            RETURNING id
            )
            INSERT INTO places_sources (place_id, inner_id, source)
            VALUES ((SELECT id FROM place_data), $6, $7)
            """,
            place.coordinates.lat,
            place.coordinates.lng,
            place.name,
            place.city,
            place.street,
            place.inner_id,
            place.source
        )

    async def get(self, place_id: int) -> asyncpg.Record:
        place = await self.conn.fetchrow(
            """
            SELECT p.id, ST_AsGeoJson(location)::jsonb, name, city, street, ps.inner_id, ps.source
            FROM places p
            LEFT JOIN places_sources ps ON p.id = ps.place_id
            WHERE p.id =$1
            """,
            place_id
        )
        return place

    async def get_nearest_place(self, latitude: float, longitude: float) -> asyncpg.Record | None:
        place = await self.conn.fetchrow(
            """
            SELECT id, (
                SELECT STRING_AGG(ps.source, ', ')
                FROM places_sources ps
                WHERE ps.place_id = places.id
            ) AS sources, ST_Distance(places.location, ST_POINT($1, $2)) AS distance
            FROM places
            WHERE ST_Distance(places.location, ST_POINT($1, $2)) <= $3
            ORDER BY distance
            LIMIT 1;
            """,
            latitude,
            longitude,
            app_settings.DISTANCE_LIMIT
        )
        return place

    async def insert_place_source(
            self,
            place: AddPlace,
            place_id: int
    ) -> None:
        await self.conn.execute(
            """
            INSERT INTO places_sources (place_id, inner_id, source)
            VALUES ($1, $2, $3)
            """,
            place_id,
            place.inner_id,
            place.source
        )
