from schemas.mixins import UUIDSchema


class MessageSchema(UUIDSchema):
    query: str
