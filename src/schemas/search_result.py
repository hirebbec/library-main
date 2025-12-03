from schemas.base import BaseSchema


class RedisSearchResultSchema(BaseSchema):
    query: str
    file_id: int
    snippet: str
    score: float


class SearchResultSchema(RedisSearchResultSchema):
    filename: str
