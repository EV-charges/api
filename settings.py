from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = Path(BASE_DIR, 'images')

ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)


class AppSettings(BaseSettings):
    PORT: int = 8080
    IS_DEBUG: bool = False

    TITLE: str = 'EV-chargers API'
    VERSION: str = '0.1.0'

    class Config:
        case_sensitive = False


app_settings = AppSettings()
