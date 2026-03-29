from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_description: str
    app_version: str
    port: int = 8000

    groq_api_key: str  # <-- correct name

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # change to "forbid" later if you want strict
    )

settings = Settings()
