import os

from dotenv import load_dotenv

load_dotenv()

CORS_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:8501",
    ).split(",")
]
