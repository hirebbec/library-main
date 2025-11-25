from fastapi import HTTPException, status

file_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="File not found",
)

invalid_file_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalide file: filename or MIME is missng",
)

file_upload_failed_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed to upload file.",
)

file_download_failed_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed to download file.",
)

file_delete_failed_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed to delete file.",
)


class ModelEncodeValidationError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
