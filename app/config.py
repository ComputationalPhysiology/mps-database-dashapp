from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    MPS_DATABASE_USERNAME: str
    MPS_DATABASE_PASSWORD: str
    MPS_DATABASE_BASEURL: str
    MPS_DATABASE_CACHE_DIR: str = (Path.home() / ".cache" / "mps_database").as_posix()
    MPS_DATABASE_CACHE_DEFAULT_TIMEOUT: int = 3600


settings = Settings()
