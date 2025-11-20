from faststream.rabbit.fastapi import RabbitRouter

from core.config import settings

rabbit_router = RabbitRouter(url=settings().rabbit_dsn)
