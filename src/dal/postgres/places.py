import asyncpg


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
            name: str
    ) -> None:
        await self.conn.execute(
            """
            INSERT INTO places (name)
            VALUES ($1)
            """,
            name
        )

    async def get(self, place_id: int) -> asyncpg.Record:
        place = await self.conn.fetchrow(
            """
            SELECT * FROM places WHERE id = $1
            """,
            place_id
        )
        return place
