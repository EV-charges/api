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
        query = """
            SELECT p.id, ST_AsGeoJson(location)::jsonb -> 'coordinates' as coordinates, name, city, street, s.sources
            FROM  places p
            JOIN (
               SELECT ps.place_id, array_agg(json_build_object('inner_id', ps.inner_id, 'source', ps.source)) AS sources
               FROM places_sources ps
               GROUP BY ps.place_id
               ) s
            on p.id = s.place_id
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
            SELECT p.id, ST_AsGeoJson(location)::jsonb -> 'coordinates' as coordinates, name, city, street, ps.inner_id, ps.source
            FROM places p
            LEFT JOIN places_sources ps ON p.id = ps.place_id
            WHERE p.id =$1
            """,
            place_id
        )
        return place

    async def get_nearest_place(self, latitude: float, longitude: float) -> list[asyncpg.Record] | None:
        place = await self.conn.fetch(
            """
            SELECT place_id, source FROM places
            JOIN places_sources
            ON places.id = places_sources.place_id
            WHERE ST_Distance(location, ST_POINT($1, $2)) <= 10
            """,
            latitude,
            longitude
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
