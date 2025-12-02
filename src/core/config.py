import functools
from datetime import timedelta, timezone
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    root_dir: Path = Path(__file__).resolve().parent.parent.parent
    src_dir: Path = root_dir.joinpath("src")
    env_file: Path = src_dir.joinpath(".env.local")

    PROJECT_NAME: str = "library-main"

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8888
    SERVER_WORKERS_COUNT: int = 5

    RABBITMQ_SEARCH_QUEUE: str = "search"

    ELASTIC_PDF_INDEX: str = "pdf_index"

    ENVIRONMENT: str = "local"
    TIME_ZONE: timezone = timezone(offset=timedelta(hours=+3))
    CORS_ALLOW_ORIGIN_LIST: str = "*"

    USE_CORS_MIDDLEWARE: bool = True
    USE_TIMER_MIDDLEWARE: bool = False
    USE_KEYCLOAK_MIDDLEWARE: bool = False

    POSTGRES_HOST: str = "library-db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "library-db"
    POSTGRES_PASSWORD: str = "library-db"
    POSTGRES_DB: str = "library-db"

    MINIO_HOST: str = "library-s3"
    MINIO_PORT: int = 9000
    MINIO_WEB_PORT: int = 9001
    MINIO_ROOT_USER: str = "library-s3"
    MINIO_ROOT_PASSWORD: str = "library-s3"
    MINIO_ACCESS_KEY_ID: str = "library-s3"
    MINIO_SECRET_ACCESS_KEY: str = "library-s3"
    MINIO_REGION_NAME: str = "eu-central-1"
    MINIO_DEFAULT_BUCKET: str = "library-bucket"

    RABBITMQ_HOST: str = "library-rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_DEFAULT_USER: str = "library-rabbitmq"
    RABBITMQ_DEFAULT_PASS: str = "library-rabbitmq"

    REDIS_HOST: str = "library-redis"
    REDIS_PORT: int = 16379
    REDIS_PASSWORD: str = "library-redis"
    REDIS_DB: int = 0

    ELASTIC_HOST: str = "library-elasticsearch"
    ELASTIC_USER: str = "elastic"
    ELASTIC_PASSWORD: str = "library-elasticsearch"
    ELASTIC_PORT: int = 19200

    @functools.cached_property
    def cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGIN_LIST.split("&")

    @functools.cached_property
    def postgres_dsn(self) -> str:
        postgres_host = (
            "localhost" if self.ENVIRONMENT == "local" else self.POSTGRES_HOST
        )
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{postgres_host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @functools.cached_property
    def s3_dsn(self) -> str:
        s3_host = "localhost" if self.ENVIRONMENT == "local" else self.MINIO_HOST
        return f"http://{s3_host}:{self.MINIO_PORT}"

    @functools.cached_property
    def rabbitmq_dsn(self) -> str:
        rabbitmq_host = (
            "localhost" if self.ENVIRONMENT == "local" else self.RABBITMQ_HOST
        )
        return f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}@{rabbitmq_host}:{self.RABBITMQ_PORT}/"

    @functools.cached_property
    def redis_dsn(self) -> str:
        redis_host = "localhost" if self.ENVIRONMENT == "local" else self.REDIS_HOST
        return f"redis://:{self.REDIS_PASSWORD}@{redis_host}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @functools.cached_property
    def elastic_dsn(self) -> str:
        elastic_host = "localhost" if self.ENVIRONMENT == "local" else self.ELASTIC_HOST
        return f"http://{self.ELASTIC_USER}:{self.ELASTIC_PASSWORD}@{elastic_host}:{self.ELASTIC_PORT}"

    model_config = SettingsConfigDict(
        env_file=env_file if env_file else None,
        env_file_encoding="utf-8",
        extra="allow",
    )


@functools.lru_cache()
def settings() -> Settings:
    return Settings()
