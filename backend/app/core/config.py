"""應用程式設定，從環境變數載入。"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    project_name: str = "TalkERP API"
    api_v1_prefix: str = "/api/v1"

    postgres_server: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_db: str = "talkerp"
    postgres_user: str
    postgres_password: str

    cors_origins: list[str] = ["http://localhost:5173"]

    log_level: str = "INFO"
    log_dir: str = "logs"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
