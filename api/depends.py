import asyncpg
from fastapi import Depends, Request

from src.services.places import CommentsServices, PlacesServices


async def get_pg_connection(request: Request) -> asyncpg.Connection:
    async with request.app.state.pool.acquire() as conn:
        yield conn


async def get_places_service(
        pg_conn: asyncpg.Connection = Depends(get_pg_connection)
) -> PlacesServices:
    return PlacesServices(conn=pg_conn)


async def get_comments_service(
        pg_conn: asyncpg.Connection = Depends(get_pg_connection)
) -> CommentsServices:
    return CommentsServices(conn=pg_conn)
