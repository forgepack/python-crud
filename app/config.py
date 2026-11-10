from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 9000
    root_path: str = ""
    reload: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="UVICORN_",
        extra="ignore",
    )


settings = Settings()
