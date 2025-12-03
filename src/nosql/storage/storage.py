import json
from typing import Sequence

from fastapi import Depends
from redis.asyncio import Redis

from nosql.storage.client import get_redis
from schemas.search_result import RedisSearchResultSchema


class CacheStorage:
    def __init__(self, redis: Redis = Depends(get_redis)):
        self._redis = redis

    async def get_search_results(self, uuid: str) -> Sequence[RedisSearchResultSchema]:
        data = await self._redis.get(uuid)

        if data is None:
            return []

        results = json.loads(data.decode("utf-8"))

        return [RedisSearchResultSchema.model_validate(result) for result in results]
