from fastapi import HTTPException, status

from app.config.logger import logger


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with ID: {user_id} found!!",
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials entered!!",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UsernameAlreadyExistsException(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The username: {username} already exists!!",
        )


class PermissionDeniedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action",
        )


class DatabaseIntegrityError(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail or "Database integrity error occurred",
        )


class TokenCreationError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create authentication token",
        )


class RequiredEnvVarError(Exception):
    def __init__(self, var_name: str):
        super().__init__(f"Required environment variable '{var_name}' is not set")
        self.var_name = var_name


class TitleAlreadyExistsException(HTTPException):
    def __init__(self, title: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Note with title: {title} already exists!!",
        )


class LabelAlreadyExistsException(HTTPException):
    def __init__(self, title: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Label with title: {title} already exists!!",
        )


class LabelRequiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"At least one Label required!!",
        )


class LabelDoesNotExistException(HTTPException):
    def __init__(self, title: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Label with name {title} does not exist, create the label to continue!!",
        )