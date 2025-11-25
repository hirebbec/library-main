from schemas.base import BaseSchema
from schemas.mixins import CreatedAtSchema, UpdatedAtSchema, IDSchema


class CreateFileSchema(BaseSchema):
    filename: str
    mime_type: str


class UpdateFileSchema(CreateFileSchema):
    pass


class GetFileSchema(UpdateFileSchema, IDSchema, CreatedAtSchema, UpdatedAtSchema):
    pass
