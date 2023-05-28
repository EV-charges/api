from fastapi import APIRouter, Depends, HTTPException, Path, status

from api.depends import get_places_service
from api.routers.v1.models import AddPlace, AddPlaceResponse, GetPlace, GetPlaces
from src.services.places import PlaceAddError, PlaceExistError, PlacesServices, SourceAddError

router = APIRouter(prefix='/api/v1', tags=['places'])


@router.get('/places')
async def get_places(
        limit: int = 20,
        offset: int = 0,
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
        await places_service.add_place(place=place)
    except (PlaceAddError, PlaceExistError, SourceAddError) as e:
        return AddPlaceResponse(message=e.text)


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
