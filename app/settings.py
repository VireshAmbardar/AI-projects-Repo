from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = Field(default='App Name')
    app_description:str =  Field(default='App description')
    app_version: str = Field(default='1')
    port: int = 8000

    # groq_api_key: str  # <-- correct name

    model_config = SettingsConfigDict(
        env_file= BASE_DIR /".env",
        env_file_encoding="utf-8",
        extra="ignore",  # change to "forbid" later if you want strict
    )

settings = Settings()
