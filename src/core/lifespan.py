from contextlib import asynccontextmanager

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from loguru import logger
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.es = AsyncElasticsearch(settings().elastic_dsn)

    exists = await app.state.es.indices.exists(index=settings().ELASTIC_PDF_INDEX)
    if not exists:
        await app.state.es.indices.create(
            index=settings().ELASTIC_PDF_INDEX,
            body={
                "mappings": {
                    "properties": {
                        "file_id": {"type": "keyword"},
                        "content": {"type": "text"},
                    }
                }
            },
        )

    logger.info("Elastic initialized")

    yield

    await app.state.es.close()
