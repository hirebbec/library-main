from fastapi import APIRouter, status, Depends

from schemas.mixins import UUIDSchema
from service.search import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(path="", status_code=status.HTTP_202_ACCEPTED, response_model=UUIDSchema)
async def search_files(
    query: str, search_service: SearchService = Depends()
) -> UUIDSchema:
    return await search_service.create_search_task(query=query)
