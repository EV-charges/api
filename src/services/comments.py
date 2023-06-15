import asyncpg

from api.routers.v1.models import AddComment, PlaceSources
from src.dal.postgres.comments import CommentsDB
from src.dal.postgres.places import PlacesDB


class CommentsServices:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn
        self.comments_db = CommentsDB(conn=conn)
        self.places_db = PlacesDB(conn=conn)

    async def add_comment(
            self,
            comment: AddComment,
    ) -> str:
        place_source = PlaceSources(
            inner_id=comment.place_id,
            source=comment.source
        )
        place_id = await self.places_db.place_is_exist(place_source)
        if not place_id:
            return "Place doesn't exist"

        response = await self.comments_db.insert_comment(
            place_id=place_id,
            comment=comment,
        )

        if not response:
            raise CommentExistError
        return "place comment add"


class CommentExistError(Exception):
    def __init__(self) -> None:
        self.text = 'Comment already added'
