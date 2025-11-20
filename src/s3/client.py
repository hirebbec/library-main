import functools
import typing

from aioboto3 import Session
from aiobotocore.client import AioBaseClient

from core.config import settings


@functools.lru_cache
def get_s3_session() -> Session:
    return Session(
        aws_access_key_id=settings().MINIO_ACCESS_KEY_ID,
        aws_secret_access_key=settings().MINIO_SECRET_ACCESS_KEY,
        region_name=settings().MINIO_REGION_NAME,
    )


async def get_s3_client() -> typing.AsyncGenerator[AioBaseClient, None]:
    session = get_s3_session()
    async with session.client("s3", endpoint_url=settings().s3_dsn) as client:
        yield client
