import io
from typing import Sequence
from urllib.parse import quote

from elasticsearch import AsyncElasticsearch
from fastapi import Depends, UploadFile
from starlette.responses import StreamingResponse

from core.config import settings
from core.exceptions import (
    file_not_found_exception,
    invalid_file_exception,
    file_upload_failed_exception,
    file_download_failed_exception,
    file_delete_failed_exception,
)
from db.repository.file import FileRepository
from elk.elastic import get_es
from s3.storage import S3Storage
from schemas.file import CreateFileSchema, GetFileSchema
from service.base import BaseService
from utils.pdf import extract_pdf_text


class FileService(BaseService):
    def __init__(
        self,
        file_repository: FileRepository = Depends(),
        s3_storage: S3Storage = Depends(),
        es: AsyncElasticsearch = Depends(get_es),
    ):
        self._file_repository = file_repository
        self._s3_storage = s3_storage
        self._es = es

    async def upload_file(self, file: UploadFile):
        if not file.filename or not file.content_type:
            raise invalid_file_exception

        raw_bytes = await file.read()

        file_id_schema = await self._file_repository.create(
            file=CreateFileSchema(filename=file.filename, mime_type=file.content_type)
        )

        text = await extract_pdf_text(io.BytesIO(raw_bytes))

        success = await self._s3_storage.upload_file(
            key=str(file_id_schema.id),
            data=raw_bytes,
            content_type=file.content_type,
        )

        if not success:
            raise file_upload_failed_exception

        await self._es.index(
            index=settings().ELASTIC_PDF_INDEX,
            document={
                "file_id": str(file_id_schema.id),
                "content": text,
            },
        )

    async def get_files(self) -> Sequence[GetFileSchema]:
        return await self._file_repository.get_files()

    async def get_file_by_id(self, id: int) -> GetFileSchema:
        file = await self._file_repository.get_by_id(id=id)

        if not file:
            raise file_not_found_exception

        return file

    async def delete_file_by_id(self, id: int) -> None:
        if not await self._s3_storage.is_file_exists(key=str(id)):
            raise file_not_found_exception

        if not await self._s3_storage.delete_file_by_key(key=str(id)):
            raise file_delete_failed_exception

        await self._file_repository.delete_by_id(id=id)

    async def download_file_by_id(self, id: int) -> StreamingResponse:
        file = await self._file_repository.get_by_id(id=id)

        if not file or not await self._s3_storage.is_file_exists(key=str(id)):
            raise file_not_found_exception

        obj = await self._s3_storage.get_file_by_key(key=str(id))

        if not obj:
            raise file_download_failed_exception

        stream = obj["Body"]

        return StreamingResponse(
            stream,
            media_type=file.mime_type,
            headers={
                "Content-Disposition": (
                    f"attachment; filename*=UTF-8''{quote(file.filename)}"
                )
            },
        )
