from typing import Any


class PepkioError(Exception):
    """Base exception for all Pepkio client errors."""

    pass


class PepkioAPIError(PepkioError):
    """Raised when the API returns an error HTTP status or error payload."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: Any = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class PepkioAuthError(PepkioAPIError):
    """Raised when authentication fails (HTTP 401/403)."""

    pass


class PepkioNotFoundError(PepkioAPIError):
    """Raised when a resource or endpoint is not found (HTTP 404)."""

    pass


class PepkioValidationError(PepkioError):
    """Raised when client-side input validation fails."""

    pass
