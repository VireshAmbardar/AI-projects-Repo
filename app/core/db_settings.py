from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = "bond_scanner"

# Since i am using WSL so i need to use the localhost ip address of the host machine
# HOST_IP = "172.18.0.1" <- moved to docker-compose.yml


class Settings(BaseSettings):
    app_name: str = Field(default='App Name')
    app_description: str = Field(default='App description')
    app_version: str = Field(default='1')
    port: int = 8000

    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="postgre")
    postgres_password: str = Field(default="1998")
    postgres_db: str = Field(default=DB_NAME)

    

    # groq_api_key: str  # <-- correct name

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",  # change to "forbid" later if you want strict
    )

    @property
    def database_url(self) -> str:
        """asyncpg-compatible DSN, no '+asyncpg' driver suffix needed.
        Built from the fields above so it can never drift out of sync with them."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()