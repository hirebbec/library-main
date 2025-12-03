import uuid
from typing import Sequence

from fastapi import Depends

from core.config import settings
from core.exceptions import result_not_ready_exception
from db.repository.file import FileRepository
from mq.publisher import RabbitPublisher, get_rabbit_publisher
from nosql.storage.storage import CacheStorage
from schemas.message import MessageSchema
from schemas.mixins import UUIDSchema
from schemas.search_result import SearchResultSchema
from service.base import BaseService


class SearchService(BaseService):
    def __init__(
        self,
        rabbit_publisher: RabbitPublisher = Depends(get_rabbit_publisher),
        cache_storage: CacheStorage = Depends(),
        file_repository: FileRepository = Depends(),
    ):
        self._rabbit_publisher = rabbit_publisher
        self._cache_storage = cache_storage
        self._file_repository = file_repository

    async def create_search_task(self, query: str) -> UUIDSchema:
        message = MessageSchema(uuid=str(uuid.uuid4()), query=query)

        await self._rabbit_publisher.publish(
            message=message.model_dump(),
            queue=settings().RABBITMQ_SEARCH_QUEUE,
            correlation_id=message.uuid,
        )

        return UUIDSchema(uuid=message.uuid)

    async def get_search_result(self, task_uuid: str) -> Sequence[SearchResultSchema]:
        results = await self._cache_storage.get_search_results(uuid=task_uuid)

        if results is None:
            raise result_not_ready_exception

        return [
            SearchResultSchema.model_encode(
                result, await self._file_repository.get_by_id(result.file_id)
            )
            for result in results
        ]
