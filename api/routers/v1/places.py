from fastapi import APIRouter

router = APIRouter(prefix='/api/v1', tags=['places'])


@router.get('/places')
async def get_places() -> None:
    pass


@router.post('/places')
async def add_place() -> None:
    pass
