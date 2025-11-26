import uuid

from fastapi import Depends

from core.config import settings
from mq.publisher import RabbitPublisher, get_rabbit_publisher
from schemas.message import MessageSchema
from schemas.mixins import UUIDSchema
from service.base import BaseService


class SearchService(BaseService):
    def __init__(
        self, rabbit_publisher: RabbitPublisher = Depends(get_rabbit_publisher)
    ):
        self._rabbit_publisher = rabbit_publisher

    async def create_search_task(self, query: str) -> UUIDSchema:
        message = MessageSchema(uuid=str(uuid.uuid4()), query=query)

        await self._rabbit_publisher.publish(
            message=message.model_dump(),
            queue=settings().SEARCH_QUEUE,
            correlation_id=message.uuid,
        )

        return UUIDSchema(uuid=message.uuid)
