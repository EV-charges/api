from fastapi import APIRouter, Query, status
from pydantic import BaseModel

router = APIRouter(prefix='/api/v1', tags=['hello'])


class Hello(BaseModel):
    a: int
    b: str


@router.get(
    '/hello',
    status_code=status.HTTP_200_OK,
    response_model=Hello
)
async def hello(
        a: int = Query(...),
        b: str = Query(...)
) -> Hello:
    return Hello(a=a, b=b)
