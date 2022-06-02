from typing import Optional, Dict, Any
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    app_name: str = "Tagihan.Ku"
    openapi_url: str = "/api/v1/openapi.json"
    prefix: str = "/api/v1"

    # Database Settings
    # POSTGRES_USER: str = "postgres"
    # POSTGRES_PASSWORD: str = "kurdiansyah1995"
    # POSTGRES_SERVER: str = "localhost:5432"
    # POSTGRES_DB: str = "app"
    POSTGRES_USER: str = "ppybttvixunchd"
    POSTGRES_PASSWORD: str = "6dbc90ba9d51af753fc696df82f6b7fef61167531742e7d62cdba2ced4421fd2"
    POSTGRES_SERVER: str = "ec2-34-197-84-74.compute-1.amazonaws.com:5432"
    POSTGRES_DB: str = "dc2r0mln1dkrmh"
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

    TOKEN = "5458637763:AAGKDJTRPARSHqx1kJ0uSp3wUSbgzTDN3oM"
# --


settings = Settings()
