from faststream.rabbit import RabbitBroker, RabbitQueue
from mq.router import rabbit_router


class RabbitPublisher:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker
        self._declared_queues: set[str] = set()

    async def _ensure_queue(self, queue: str):
        if queue not in self._declared_queues:
            await self.broker.declare_queue(RabbitQueue(queue))
            self._declared_queues.add(queue)

    async def publish(
        self,
        message: dict,
        queue: str,
        *,
        correlation_id: str | None = None,
    ) -> None:
        await self._ensure_queue(queue=queue)

        await self.broker.publish(
            message,
            queue=queue,
            correlation_id=correlation_id,
            content_type="application/json",
        )


async def get_rabbit_publisher() -> RabbitPublisher:
    return RabbitPublisher(broker=rabbit_router.broker)
