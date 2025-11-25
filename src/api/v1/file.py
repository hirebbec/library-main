from typing import Sequence

from fastapi import APIRouter, status, File, UploadFile, Depends, Response

from schemas.file import GetFileSchema
from service.file import FileService

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(path="", status_code=status.HTTP_200_OK, response_model=None)
async def upload_file(
    file: UploadFile = File(...), file_service: FileService = Depends()
) -> None:
    await file_service.upload_file(file=file)


@router.get(
    path="", status_code=status.HTTP_200_OK, response_model=Sequence[GetFileSchema]
)
async def get_files(file_service: FileService = Depends()) -> Sequence[GetFileSchema]:
    return await file_service.get_files()


@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=GetFileSchema)
async def get_file_by_id(
    id: int, file_service: FileService = Depends()
) -> GetFileSchema:
    return await file_service.get_file_by_id(id=id)


@router.get(
    path="/{id}/download",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def download_file_by_id(
    id: int, file_service: FileService = Depends()
) -> Response:
    return await file_service.download_file_by_id(id=id)


@router.delete(path="/{id}", status_code=status.HTTP_200_OK, response_model=None)
async def delete_file_by_id(id: int, file_service: FileService = Depends()):
    await file_service.delete_file_by_id(id=id)
