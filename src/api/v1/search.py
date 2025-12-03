from typing import Sequence

from fastapi import APIRouter, status, Depends

from schemas.mixins import UUIDSchema
from schemas.search_result import SearchResultSchema
from service.search import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(path="", status_code=status.HTTP_202_ACCEPTED, response_model=UUIDSchema)
async def search_files(
    query: str, search_service: SearchService = Depends()
) -> UUIDSchema:
    return await search_service.create_search_task(query=query)


@router.get("/{task_uuid}", response_model=Sequence[SearchResultSchema])
async def get_search_result(
    task_uuid: str, search_service: SearchService = Depends()
) -> Sequence[SearchResultSchema]:
    return await search_service.get_search_result(task_uuid=task_uuid)
