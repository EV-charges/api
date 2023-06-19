import asyncpg

from api.routers.v1.models import AddComment


class CommentsDB:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def is_comment_exist(
        self,
        comment_id: int,
        source: str
    ) -> bool:
        return await self.conn.fetchval(
            """
                SELECT comment_id
                FROM comments
                WHERE comment_id = $1 and source = $2
            """,
            comment_id,
            source
        )

    async def insert_comment(
        self,
        place_id: int,
        comment: AddComment
    ) -> bool:
        return await self.conn.fetchval(
            """
                INSERT INTO comments (
                    place_id,
                    comment_id,
                    author,
                    text,
                    publication_date,
                    source
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
            """,
            place_id,
            comment.comment_id,
            comment.author,
            comment.text,
            comment.publication_date,
            comment.source
        )
