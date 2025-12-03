from typing import Sequence

from sqlalchemy import insert, select, delete

from db.models import File
from db.repository.base import BaseDatabaseRepository
from schemas.file import CreateFileSchema, GetFileSchema
from schemas.mixins import IDSchema


class FileRepository(BaseDatabaseRepository):
    async def create(self, file: CreateFileSchema) -> IDSchema:
        query = insert(File).values(**file.model_dump()).returning(File.id)

        result = await self._session.execute(query)
        return IDSchema(id=result.scalar_one())

    async def get_files(self) -> Sequence[GetFileSchema]:
        query = select(File)

        result = await self._session.execute(query)
        return [
            GetFileSchema.model_validate(obj=file) for file in result.scalars().all()
        ]

    async def get_by_id(self, id: int) -> GetFileSchema | None:
        query = select(File).where(File.id == id)

        result = await self._session.execute(query)
        raw_file = result.scalars().first()
        return GetFileSchema.model_validate(obj=raw_file) if raw_file else None

    async def delete_by_id(self, id: int) -> None:
        query = delete(File).where(File.id == id)

        await self._session.execute(query)
        await self._session.flush()
