from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from api.depends import get_places_service
from api.routers.v1.models import AddComment, AddPlace, AddPlaceResponse, GetPlace, GetPlaces
from src.services.places import CommentExistError, PlaceExistError, PlacesServices

router = APIRouter(prefix='/api/v1', tags=['places'])


@router.get('/places')
async def get_places(
        limit: int = Query(20),
        offset: int = Query(0),
        source: str | None = None,
        places_service: PlacesServices = Depends(get_places_service)
) -> GetPlaces:
    places = await places_service.get_places(
        limit=limit,
        offset=offset,
        source=source
    )
    return places


@router.post(
    '/places',
    status_code=status.HTTP_201_CREATED,
)
async def add_place(
    place: AddPlace,
    places_service: PlacesServices = Depends(get_places_service)
) -> AddPlaceResponse:
    try:
        service_response = await places_service.add_place(place=place)
        return AddPlaceResponse(message=service_response)
    except PlaceExistError as e:
        raise HTTPException(status_code=409, detail=e.text) from None


@router.get(
    '/places/{place_id}',
    response_model=GetPlace
)
async def get_place(
    place_id: int = Path(...),
    places_service: PlacesServices = Depends(get_places_service)
) -> GetPlace:
    place = await places_service.get_place(place_id=place_id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='place not found')
    return place


@router.post(
    '/comments',
    status_code=status.HTTP_201_CREATED
)
async def add_comment(
    comment: AddComment,
    places_service: PlacesServices = Depends(get_places_service)
) -> AddPlaceResponse:
    try:
        service_response = await places_service.add_comment(comment=comment)
        return AddPlaceResponse(message=service_response)
    except CommentExistError as e:
        raise HTTPException(status_code=409, detail=e.text) from None
