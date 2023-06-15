import asyncpg

from api.routers.v1.models import AddComment


class CommentsDB:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def insert_comment(
        self,
        place_id: int,
        comment: AddComment
    ) -> int | None:
        query = await self.conn.fetchval(
            """
                INSERT INTO comments (
                    place_id,
                    comment_id,
                    author,
                    text,
                    publication_date,
                    source
                )
                SELECT $1, $2, $3, $4, $5, $6
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM comments
                    WHERE comment_id = $2 AND source = $6
                )
                RETURNING id;
            """,
            place_id,
            comment.comment_id,
            comment.author,
            comment.text,
            comment.publication_date,
            comment.source
        )
        return query
