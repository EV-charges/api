from fastapi import APIRouter, Depends, HTTPException, status

from api.depends import get_comments_service
from api.routers.v1.models import AddComment, AddPlaceResponse
from src.services.comments import CommentExistError, CommentsServices
from src.services.places import PlaceExistError

router = APIRouter(prefix='/api/v1', tags=['places'])


@router.post(
    '/comments',
    status_code=status.HTTP_201_CREATED
)
async def add_comment(
    comment: AddComment,
    comment_service: CommentsServices = Depends(get_comments_service)
) -> AddPlaceResponse:
    try:
        service_response = await comment_service.add_comment(comment=comment)
        return AddPlaceResponse(message=service_response)
    except CommentExistError as e:
        raise HTTPException(status_code=409, detail=e.text) from None
    except PlaceExistError as e:
        raise HTTPException(status_code=409, detail=e.text) from None
