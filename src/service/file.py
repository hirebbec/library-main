from typing import Sequence

from fastapi import Depends, UploadFile

from core.exceptions import file_not_found_exception
from db.repository.file import FileRepository
from s3.storage import S3Storage
from schemas.file import CreateFileSchema, GetFileSchema
from service.base import BaseService


class FileService(BaseService):
    def __init__(
        self,
        file_repository: FileRepository = Depends(),
        s3_storage: S3Storage = Depends(),
    ):
        self._file_repository = file_repository
        self._s3_storage = s3_storage

    async def upload_file(self, file: UploadFile):
        await self._file_repository.create(
            file=CreateFileSchema(filename=file.filename, mime_type=file.content_type)
        )

    async def get_files(self) -> Sequence[GetFileSchema]:
        return await self._file_repository.get_files()

    async def get_file_by_id(self, id: int) -> GetFileSchema:
        file = await self._file_repository.get_by_id(id=id)

        if not file:
            raise file_not_found_exception

        return file

    async def delete_file_by_id(self, id: int) -> None:
        await self._file_repository.delete_by_id(id=id)
