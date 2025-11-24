from fastapi import HTTPException, status

file_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="File not found",
)

invalid_file_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalide file: filename or MIME is missng",
)


class ModelEncodeValidationError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
