import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "GapFinder AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-gapfinder-jwt-key-2026-hackathon")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://thatipellisaikiran.github.io"
    ]

settings = Settings()

