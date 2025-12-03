from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.models import BaseModel


class File(BaseModel):
    __tablename__ = "files"

    filename: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
