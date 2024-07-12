import os
from dotenv import load_dotenv
import logging

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=logging.getLevelName(LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Config:
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 50051))

    @classmethod
    def validate(cls):
        missing_vars = [var for var, value in cls.__dict__.items() if value is None]
        if missing_vars:
            logging.warning(f'Missing environment variables: {", ".join(missing_vars)}')
        return not missing_vars


Config.validate()
