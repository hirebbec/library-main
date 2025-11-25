from datetime import datetime

from schemas.base import BaseSchema


class IDSchema(BaseSchema):
    id: int


class UUIDSchema(BaseSchema):
    uuid: str


class CreatedAtSchema(BaseSchema):
    created_at: datetime


class UpdatedAtSchema(BaseSchema):
    updated_at: datetime | None = None
