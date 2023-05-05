from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.v1.hello import router as hello_router_v1
from api.routers.v1.places import router as places_router_v1
from settings import app_settings


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.TITLE,
        version=app_settings.VERSION,
    )
    setup_middlewares(app)

    app.include_router(hello_router_v1)
    app.include_router(places_router_v1)

    return app
