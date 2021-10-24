from typing import Optional, Dict, Any
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    app_name: str = "Tagihan.Ku"
    openapi_url: str = "/api/v1/openapi.json"
    prefix: str = "/api/v1"

    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "kurdiansyah1995"
    POSTGRES_SERVER: str = "localhost:5432"
    POSTGRES_DB: str = "app"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    # --
# --


settings = Settings()
