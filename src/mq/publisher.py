from faststream.rabbit import RabbitBroker
from mq.router import rabbit_router


class RabbitPublisher:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def publish(
        self,
        message: dict,
        queue: str,
        *,
        correlation_id: str | None = None,
    ) -> None:
        await self.broker.publish(
            message,
            queue=queue,
            correlation_id=correlation_id,
            content_type="application/json",
        )


async def get_rabbit_publisher() -> RabbitPublisher:
    return RabbitPublisher(broker=rabbit_router.broker)
