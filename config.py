from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    MPS_DATABASE_USERNAME: str
    MPS_DATABASE_PASSWORD: str
    MPS_DATABASE_BASEURL: str


settings = Settings()
