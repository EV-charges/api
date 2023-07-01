import asyncpg

from api.routers.v1.models import AddComment
from src.dal.postgres.comments import CommentsDB
from src.dal.postgres.places import PlacesDB
from src.services.places import PlaceNotExistError


class CommentsServices:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn
        self.comments_db = CommentsDB(conn=conn)
        self.places_db = PlacesDB(conn=conn)

    async def add_comment(
            self,
            comment: AddComment,
    ) -> int | str:
        place_id = await self.places_db.get_place_id(
            inner_id=comment.place_id,
            source=comment.source
        )

        if not place_id:
            raise PlaceNotExistError

        result = await self.comments_db.insert_comment(
            place_id=place_id,
            comment=comment,
        )

        if not result:
            raise CommentExistError()
        return result


class CommentExistError(Exception):
    def __init__(self) -> None:
        self.text = 'Comment already added'
